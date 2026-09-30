"""텐서 기초 관찰 — 1교시.

pipeline 한 줄 뒤에서 일어나는 일을 여섯 조각으로 나누어 직접 관찰한다.

1. Tensor 세 속성(shape, dtype, device)
2. 행렬곱 CPU vs GPU 시간(동기화 포함)과 CPU→GPU 복사 시간
3. dtype 변환과 메모리 크기
4. 작은 선형 모델의 파라미터와 forward
5. 자동미분(requires_grad → backward → grad)
6. no_grad 유무에 따른 메모리 차이

결과는 outputs/tensor_report.json에 남긴다.

    uv run python tensor_basics.py
    uv run python tensor_basics.py --size 512 --device cpu
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import torch
from torch import nn

from runlog import gpu_name, pick_device, set_seed, sync


def describe(name: str, t: torch.Tensor) -> dict[str, Any]:
    info = {
        "name": name,
        "shape": list(t.shape),
        "dtype": str(t.dtype).replace("torch.", ""),
        "device": str(t.device),
        "numel": t.numel(),
        "bytes": t.numel() * t.element_size(),
    }
    print(f"  {name:<12} shape={info['shape']!s:<12} dtype={info['dtype']:<8} device={info['device']:<6} bytes={info['bytes']}")
    return info


def section_tensor_info(device: torch.device) -> list[dict[str, Any]]:
    print("\n[1] Tensor 세 속성 — shape · dtype · device")
    rows = [
        describe("scalar", torch.tensor(3.0)),
        describe("token_ids", torch.tensor([[101, 2023, 102]])),
        describe("matrix_f32", torch.zeros(2, 3)),
        describe("matrix_f16", torch.zeros(2, 3, dtype=torch.float16)),
        describe("on_device", torch.zeros(2, 3).to(device)),
    ]
    return rows


def time_matmul(size: int, repeat: int, device: torch.device) -> float:
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)
    _ = a @ b  # 첫 호출은 커널 준비 비용이 섞이므로 예열로 버린다
    sync(device)
    t0 = time.perf_counter()
    for _ in range(repeat):
        _ = a @ b
    sync(device)  # GPU는 비동기이므로 끝날 때까지 기다린 뒤 시간을 잰다
    return (time.perf_counter() - t0) / repeat


def section_matmul(size: int, repeat: int, device: torch.device) -> dict[str, Any]:
    print(f"\n[2] 행렬곱 {size}×{size} · {repeat}회 평균")
    cpu = torch.device("cpu")
    cpu_s = time_matmul(size, repeat, cpu)
    print(f"  cpu : {cpu_s * 1000:8.2f} ms")
    result: dict[str, Any] = {"size": size, "repeat": repeat, "cpu_s": round(cpu_s, 6)}
    if device.type == "cuda":
        gpu_s = time_matmul(size, repeat, device)
        a = torch.randn(size, size)
        sync(device)
        t0 = time.perf_counter()
        _ = a.to(device)
        sync(device)
        copy_s = time.perf_counter() - t0
        print(f"  cuda: {gpu_s * 1000:8.2f} ms   (CPU→GPU 복사 {copy_s * 1000:.2f} ms)")
        print(f"  speedup ×{cpu_s / gpu_s:.1f}  — 복사 시간을 더하면 ×{cpu_s / (gpu_s + copy_s):.1f}")
        result.update(
            {"gpu_s": round(gpu_s, 6), "h2d_copy_s": round(copy_s, 6), "speedup": round(cpu_s / gpu_s, 2)}
        )
    else:
        print("  cuda: 사용 불가 — CPU 값만 기록한다. (GPU PC에서는 같은 명령으로 두 값이 함께 나온다)")
        result.update({"gpu_s": None, "h2d_copy_s": None, "speedup": None})
    return result


def section_dtype(size: int) -> dict[str, Any]:
    print("\n[3] dtype 변환 — 같은 숫자, 다른 표현")
    x = torch.tensor([1 / 3, 2 / 3, 1e-5])
    values: dict[str, list[float]] = {}
    for dt in (torch.float32, torch.float16, torch.bfloat16):
        y = x.to(dt)
        key = str(dt).replace("torch.", "")
        values[key] = [float(v) for v in y.float()]
        print(f"  {key:<9} element_size={y.element_size()}B  값={values[key]}")
    truncated = torch.tensor([1.7, -1.7]).to(torch.int64).tolist()
    print(f"  float→int64: [1.7, -1.7] → {truncated} (반올림이 아니라 버림)")
    mb_f32 = size * size * 4 / (1024**2)
    mb_f16 = size * size * 2 / (1024**2)
    print(f"  {size}×{size} 행렬 하나: float32 {mb_f32:.1f} MB, float16 {mb_f16:.1f} MB")
    return {
        "values": values,
        "float_to_int64": truncated,
        "matrix_mb": {"float32": round(mb_f32, 2), "float16": round(mb_f16, 2)},
    }


def section_linear_model(device: torch.device) -> dict[str, Any]:
    print("\n[4] 모델 = 파라미터 + forward")
    model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 2)).to(device)
    params = [(name, list(p.shape)) for name, p in model.named_parameters()]
    n_params = sum(p.numel() for p in model.parameters())
    for name, shape in params:
        print(f"  {name:<12} {shape}")
    x = torch.randn(3, 4, device=device)
    out = model(x)
    print(f"  입력 {list(x.shape)} → 출력 {list(out.shape)}  파라미터 {n_params}개")
    return {"parameters": params, "n_params": n_params, "input_shape": list(x.shape), "output_shape": list(out.shape)}


def section_autograd() -> dict[str, Any]:
    print("\n[5] 자동미분 — y = sum(x²) 의 dy/dx")
    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    y = (x**2).sum()
    y.backward()
    grad = x.grad.tolist() if x.grad is not None else None
    print(f"  x={x.tolist()}  y={y.item():.1f}  x.grad={grad}")
    with torch.no_grad():
        z = (x**2).sum()
    print(f"  no_grad 안에서 만든 z.requires_grad={z.requires_grad}, z.grad_fn={z.grad_fn}")
    return {"x": x.tolist(), "y": y.item(), "grad": grad, "no_grad_requires_grad": z.requires_grad}


def measure_forward(model: nn.Module, x: torch.Tensor, use_no_grad: bool, device: torch.device) -> dict[str, Any]:
    base = 0
    if device.type == "cuda":
        sync(device)
        torch.cuda.reset_peak_memory_stats(device)
        base = torch.cuda.memory_allocated(device)
    if use_no_grad:
        with torch.no_grad():
            out = model(x)
    else:
        out = model(x)
    extra_mb: float | None = None
    if device.type == "cuda":
        sync(device)
        extra_mb = round((torch.cuda.max_memory_allocated(device) - base) / (1024**2), 1)
    return {
        "no_grad": use_no_grad,
        "output_requires_grad": out.requires_grad,
        "grad_fn": type(out.grad_fn).__name__ if out.grad_fn is not None else None,
        "peak_extra_mb": extra_mb,
    }


def section_no_grad(hidden: int, batch: int, layers: int, device: torch.device) -> dict[str, Any]:
    print(f"\n[6] no_grad 유무 — Linear({hidden}) × {layers}, batch {batch}")
    blocks: list[nn.Module] = []
    for _ in range(layers):
        blocks += [nn.Linear(hidden, hidden), nn.ReLU()]
    model = nn.Sequential(*blocks).to(device)
    x = torch.randn(batch, hidden, device=device)
    with_grad = measure_forward(model, x, use_no_grad=False, device=device)
    no_grad = measure_forward(model, x, use_no_grad=True, device=device)
    theory_mb = round(layers * batch * hidden * 4 / (1024**2), 1)
    for r in (with_grad, no_grad):
        mem = "측정 불가(CPU)" if r["peak_extra_mb"] is None else f"{r['peak_extra_mb']} MB"
        print(f"  no_grad={r['no_grad']!s:<5} requires_grad={r['output_requires_grad']!s:<5} grad_fn={r['grad_fn']!s:<14} 추가 메모리={mem}")
    print(f"  역전파용으로 저장되는 활성화(이론값): {theory_mb} MB")
    return {"with_grad": with_grad, "no_grad": no_grad, "theory_activation_mb": theory_mb}


def main() -> None:
    parser = argparse.ArgumentParser(description="텐서·자동미분·no_grad 관찰 보고서를 만든다.")
    parser.add_argument("--size", type=int, default=2048, help="행렬곱 크기 N (N×N)")
    parser.add_argument("--repeat", type=int, default=3, help="행렬곱 반복 횟수")
    parser.add_argument("--device", default="auto", help="auto | cpu | cuda")
    parser.add_argument("--hidden", type=int, default=1024, help="no_grad 실험용 은닉 크기")
    parser.add_argument("--batch", type=int, default=256, help="no_grad 실험용 배치 크기")
    parser.add_argument("--layers", type=int, default=4, help="no_grad 실험용 층 수")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="outputs/tensor_report.json")
    args = parser.parse_args()

    set_seed(args.seed)
    device = pick_device(args.device)
    print(f"torch {torch.__version__} · device={device} · gpu={gpu_name(device) or '-'}")

    report: dict[str, Any] = {
        "torch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "device": str(device),
        "gpu_name": gpu_name(device),
        "args": vars(args),
        "tensor_info": section_tensor_info(device),
        "matmul": section_matmul(args.size, args.repeat, device),
        "dtype": section_dtype(args.size),
        "linear_model": section_linear_model(device),
        "autograd": section_autograd(),
        "no_grad": section_no_grad(args.hidden, args.batch, args.layers, device),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n보고서 저장: {out}")


if __name__ == "__main__":
    main()
