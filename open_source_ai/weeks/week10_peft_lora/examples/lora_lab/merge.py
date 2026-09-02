"""3교시 확장 — 어댑터를 기본 가중치에 병합해 단독 모델 폴더로 저장한다.

실행 예:
  uv run python merge.py                                # adapters/run-001 → models/merged-run-001
  uv run python merge.py --adapter adapters/run-002 --dtype fp32 --check

결과: models/merged-<run-name>/ (safetensors + 토크나이저), outputs/merge-<run-name>.json
병합본은 Ollama 가져오기(safetensors 또는 GGUF 변환)의 입력이 된다. 절차는 Ollama 공식 import 문서를 따른다.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import torch
from peft import PeftModel

from common import (
    OUTPUTS_DIR,
    build_messages,
    load_tokenizer_and_model,
    model_id_from_env,
    resolve_device,
    resolve_dtype,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LoRA 어댑터 병합")
    parser.add_argument("--model", default=model_id_from_env())
    parser.add_argument("--adapter", default="adapters/run-001")
    parser.add_argument("--output-dir", default="models")
    parser.add_argument("--check", action="store_true", help="병합본으로 짧은 생성 1회 실행")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--dtype", default="auto", choices=["auto", "fp32", "bf16", "fp16"])
    return parser.parse_args()


def folder_size_mb(path: Path) -> float:
    total = sum(file.stat().st_size for file in path.rglob("*") if file.is_file())
    return round(total / (1024 * 1024), 1)


def quick_check(model, tokenizer, device: torch.device) -> str:
    text = tokenizer.apply_chat_template(
        build_messages("LoRA 어댑터를 병합하면 무엇이 달라지는가?"), tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt", add_special_tokens=False).to(device)
    with torch.no_grad():
        output_ids = model.generate(**inputs, max_new_tokens=80, do_sample=False, pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(output_ids[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()


def main() -> None:
    args = parse_args()
    device = resolve_device(args.device)
    dtype = resolve_dtype(args.dtype, device)
    adapter_dir = Path(args.adapter)
    if not (adapter_dir / "adapter_config.json").exists():
        print(f"[오류] 어댑터 폴더가 아니다: {adapter_dir} (adapter_config.json 없음)")
        sys.exit(2)

    tokenizer, base = load_tokenizer_and_model(args.model, device, dtype)
    peft_model = PeftModel.from_pretrained(base, str(adapter_dir))
    started = time.perf_counter()
    # merge_and_unload: W + (alpha/r)·B·A 를 계산해 원래 Linear에 써 넣고 LoRA 계층을 제거한다.
    merged = peft_model.merge_and_unload()
    elapsed = round(time.perf_counter() - started, 2)

    target = Path(args.output_dir) / f"merged-{adapter_dir.name}"
    merged.save_pretrained(target, safe_serialization=True)
    tokenizer.save_pretrained(target)
    size_mb = folder_size_mb(target)
    print(f"병합 완료: {target} · {size_mb} MB · {elapsed}s · dtype {dtype}")

    sample = quick_check(merged, tokenizer, device) if args.check else None
    if sample is not None:
        print("\n병합본 생성 확인:\n" + sample)

    payload = {
        "adapter": str(adapter_dir), "model": args.model, "merged_dir": str(target),
        "size_mb": size_mb, "dtype": str(dtype), "device": str(device), "merge_sec": elapsed,
        "check_output": sample,
        "note": "bf16/fp16 병합은 작은 반올림 차이가 생긴다. 정밀 비교가 필요하면 --dtype fp32 로 병합한다.",
    }
    out_path = write_json(OUTPUTS_DIR / f"merge-{adapter_dir.name}.json", payload)
    print(f"기록: {out_path}")


if __name__ == "__main__":
    main()
