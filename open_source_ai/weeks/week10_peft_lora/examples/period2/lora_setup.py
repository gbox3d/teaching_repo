"""1교시 — 소형 모델에 LoRA를 붙이고 학습 파라미터 비율과 VRAM 예측표를 만든다.

실행 예:
  uv run python lora_setup.py
  uv run python lora_setup.py --ranks 4,8,16 --seq-len 512 --batch-size 4
  uv run python lora_setup.py --target-modules q_proj,v_proj --device cpu

결과: outputs/setup-<시각>.json, outputs/setup-<시각>.md
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

# common 이 .env 를 읽는다. HF_HOME·HF_HUB_OFFLINE 은 huggingface 라이브러리가 import 될 때
# 한 번만 읽히므로, common 을 peft·transformers 보다 먼저 import 해야 .env 값이 적용된다.
from common import (
    DEFAULT_TARGET_MODULES,
    OUTPUTS_DIR,
    dtype_bytes,
    gpu_name,
    load_tokenizer_and_model,
    model_id_from_env,
    resolve_device,
    resolve_dtype,
    split_modules,
    timestamp,
    write_json,
    write_text,
)

import torch
from peft import LoraConfig, get_peft_model

MB = 1024 * 1024
ADAM_BYTES_PER_TRAINABLE = 16  # fp32 가중치 4 + 그래디언트 4 + Adam 1차·2차 상태 8


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LoRA 설정과 학습 파라미터·VRAM 예측표")
    parser.add_argument("--model", default=model_id_from_env(), help="HF 모델 ID (기본: HF_TEXT_MODEL)")
    parser.add_argument("--ranks", default="4,8,16", help="비교할 rank 목록 (쉼표 구분)")
    parser.add_argument("--alpha", type=int, default=16, help="lora_alpha")
    parser.add_argument("--target-modules", default=DEFAULT_TARGET_MODULES)
    parser.add_argument("--seq-len", type=int, default=512, help="활성화 메모리 예측용 시퀀스 길이")
    parser.add_argument("--batch-size", type=int, default=4, help="활성화 메모리 예측용 배치 크기")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--dtype", default="auto", choices=["auto", "fp32", "bf16", "fp16"])
    return parser.parse_args()


def activation_bytes(config: Any, seq_len: int, batch: int) -> int:
    """활성화 메모리 경험식(재계산 없음, 16비트 기준). 근사값이며 실측과 비교하는 용도다."""
    hidden = int(getattr(config, "hidden_size", 0))
    layers = int(getattr(config, "num_hidden_layers", 0))
    heads = int(getattr(config, "num_attention_heads", 1))
    if hidden == 0 or layers == 0:
        return 0
    per_layer = seq_len * batch * hidden * (34 + 5 * heads * seq_len / hidden)
    return int(per_layer * layers)


def lora_row(model_id: str, rank: int, args: argparse.Namespace, device: torch.device, dtype: torch.dtype) -> dict[str, Any]:
    """rank 하나에 대해 실제로 LoRA를 붙여 학습 파라미터 수를 센다."""
    _, base = load_tokenizer_and_model(model_id, device, dtype)
    total_before = sum(p.numel() for p in base.parameters())
    config = LoraConfig(
        r=rank,
        lora_alpha=args.alpha,
        lora_dropout=0.05,
        target_modules=split_modules(args.target_modules),
        bias="none",
        task_type="CAUSAL_LM",
    )
    try:
        peft_model = get_peft_model(base, config)
    except ValueError as exc:
        # 모델마다 선형 계층 이름이 다르다. 이름이 틀리면 peft가 ValueError를 낸다.
        print(f"[오류] target_modules `{args.target_modules}` 를 모델에서 찾지 못했다: {str(exc).splitlines()[0]}")
        print("       모델 구조를 출력해 실제 계층 이름을 확인한 뒤 --target-modules 를 고친다.")
        sys.exit(2)
    print(f"\n[rank={rank}] ", end="")
    peft_model.print_trainable_parameters()
    trainable, total = peft_model.get_nb_trainable_parameters()
    act = activation_bytes(base.config, args.seq_len, args.batch_size)
    weights = total_before * dtype_bytes(dtype)
    optimizer = trainable * ADAM_BYTES_PER_TRAINABLE
    row = {
        "rank": rank,
        "alpha": args.alpha,
        "trainable_params": trainable,
        "total_params": total,
        "base_params": total_before,  # 어댑터를 뺀 기본 모델 파라미터 수(전체 파인튜닝 비교용)
        "trainable_ratio_pct": round(100.0 * trainable / total, 4),
        "predict_weights_mb": round(weights / MB),
        "predict_trainable_state_mb": round(optimizer / MB),
        "predict_activation_mb": round(act / MB),
        "predict_total_mb": round((weights + optimizer + act) / MB),
    }
    del peft_model, base
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return row


def full_ft_row(total_params: int, act_mb: int) -> dict[str, Any]:
    """비교용: 같은 모델을 전체 파인튜닝할 때의 예측."""
    state = total_params * ADAM_BYTES_PER_TRAINABLE
    return {
        "rank": "full",
        "trainable_params": total_params,
        "trainable_ratio_pct": 100.0,
        "predict_trainable_state_mb": round(state / MB),
        "predict_activation_mb": act_mb,
        "predict_total_mb": round(state / MB) + act_mb,
    }


def render_markdown(model_id: str, rows: list[dict[str, Any]], full: dict[str, Any], args: argparse.Namespace) -> str:
    lines = [
        f"# LoRA 설정 보고 — {model_id}",
        "",
        f"- target modules: `{args.target_modules}` · alpha: {args.alpha}",
        f"- 예측 조건: seq_len {args.seq_len} · batch {args.batch_size} · 장치 {gpu_name()}",
        "",
        "| rank | 학습 파라미터 | 비율(%) | 가중치(MB) | 학습 상태(MB) | 활성화(MB) | 예측 합계(MB) |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['rank']} | {row['trainable_params']:,} | {row['trainable_ratio_pct']} | "
            f"{row['predict_weights_mb']} | {row['predict_trainable_state_mb']} | "
            f"{row['predict_activation_mb']} | {row['predict_total_mb']} |"
        )
    lines.append(
        f"| full | {full['trainable_params']:,} | 100 | (포함) | {full['predict_trainable_state_mb']} | "
        f"{full['predict_activation_mb']} | {full['predict_total_mb']} |"
    )
    lines += [
        "",
        "예측은 경험식이다. 2교시 학습 뒤 `outputs/train-*.json`의 `max_vram_mb`와 비교해 차이 이유를 적는다.",
    ]
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    device = resolve_device(args.device)
    dtype = resolve_dtype(args.dtype, device)
    ranks = [int(r) for r in args.ranks.split(",") if r.strip()]
    print(f"모델: {args.model} · 장치: {device} · dtype: {dtype}")

    rows = [lora_row(args.model, rank, args, device, dtype) for rank in ranks]
    full = full_ft_row(rows[0]["base_params"], rows[0]["predict_activation_mb"])

    stamp = timestamp()
    payload = {
        "model": args.model,
        "device": str(device),
        "dtype": str(dtype),
        "target_modules": split_modules(args.target_modules),
        "seq_len": args.seq_len,
        "batch_size": args.batch_size,
        "rows": rows,
        "full_finetune": full,
    }
    json_path = write_json(OUTPUTS_DIR / f"setup-{stamp}.json", payload)
    md_path = write_text(OUTPUTS_DIR / f"setup-{stamp}.md", render_markdown(args.model, rows, full, args))
    print("\n" + render_markdown(args.model, rows, full, args))
    print(f"\n기록: {json_path} · {md_path}")


if __name__ == "__main__":
    main()
