"""3교시 — 같은 프롬프트·같은 조건으로 기본 모델과 어댑터 적용 모델의 출력을 나란히 놓는다.

실행 예:
  uv run python compare.py                              # adapters/run-001, data/eval_prompts.json
  uv run python compare.py --adapter adapters/run-002 --max-new-tokens 160
  uv run python compare.py --prompt "uv.lock은 왜 커밋하는가?"

결과: outputs/compare-<run-name>.json, outputs/compare-<run-name>.md
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import torch
from peft import PeftModel
from transformers import set_seed

from common import (
    OUTPUTS_DIR,
    build_messages,
    load_tokenizer_and_model,
    model_id_from_env,
    resolve_device,
    resolve_dtype,
    write_json,
    write_text,
)

FORMAT_MARKERS = ("핵심:", "이유:", "다음 할 일:")  # sample_sft.jsonl의 답변 형식


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="기본 모델 vs LoRA 어댑터 전후 비교")
    parser.add_argument("--model", default=model_id_from_env())
    parser.add_argument("--adapter", default="adapters/run-001")
    parser.add_argument("--prompts", default="data/eval_prompts.json", help="[{id, prompt}] 형식 JSON")
    parser.add_argument("--prompt", action="append", default=[], help="직접 지정하는 프롬프트(반복 가능)")
    parser.add_argument("--max-new-tokens", type=int, default=120)
    parser.add_argument("--tag", default="", help="기록 파일 이름에 붙일 꼬리표(예: offtopic). 기본 기록을 덮어쓰지 않으려 할 때")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--dtype", default="auto", choices=["auto", "fp32", "bf16", "fp16"])
    return parser.parse_args()


def load_prompts(args: argparse.Namespace) -> list[dict[str, str]]:
    if args.prompt:
        return [{"id": f"cli-{index + 1}", "prompt": text} for index, text in enumerate(args.prompt)]
    path = Path(args.prompts)
    if not path.exists():
        print(f"[오류] 프롬프트 파일이 없다: {path}")
        sys.exit(2)
    return json.loads(path.read_text(encoding="utf-8"))


def generate(model: Any, tokenizer: Any, prompt: str, device: torch.device, max_new_tokens: int) -> str:
    text = tokenizer.apply_chat_template(build_messages(prompt), tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt", add_special_tokens=False).to(device)
    with torch.no_grad():
        # do_sample=False(greedy)라서 같은 입력이면 같은 출력이 나온다. 전후 비교의 전제다.
        output_ids = model.generate(
            **inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.pad_token_id
        )
    new_ids = output_ids[0, inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_ids, skip_special_tokens=True).strip()


def follows_format(text: str) -> bool:
    return all(marker in text for marker in FORMAT_MARKERS)


def render_markdown(run_name: str, model_id: str, rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        f"# 전후 비교 — {run_name}",
        "",
        f"- 기본 모델: `{model_id}` · 어댑터: `{summary['adapter']}`",
        f"- 조건: greedy(do_sample=False) · max_new_tokens {summary['max_new_tokens']} · seed {summary['seed']} · 장치 {summary['device']}",
        f"- 형식 준수(핵심/이유/다음 할 일 모두 포함): 기본 {summary['base_format_hits']}/{len(rows)} · 어댑터 {summary['lora_format_hits']}/{len(rows)}",
        "",
    ]
    for row in rows:
        lines += [
            f"## {row['id']} · {row['prompt']}",
            "",
            "**기본 모델**",
            "",
            "```text",
            row["base"],
            "```",
            "",
            f"**어댑터 적용** (형식 준수: {'예' if row['lora_format_ok'] else '아니오'})",
            "",
            "```text",
            row["lora"],
            "```",
            "",
        ]
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    device = resolve_device(args.device)
    dtype = resolve_dtype(args.dtype, device)
    set_seed(args.seed)

    adapter_dir = Path(args.adapter)
    if not (adapter_dir / "adapter_config.json").exists():
        print(f"[오류] 어댑터 폴더에 adapter_config.json이 없다: {adapter_dir}")
        print("       먼저 train_lora.py 로 학습하거나 --adapter 경로를 확인한다.")
        sys.exit(2)

    prompts = load_prompts(args)
    tokenizer, base = load_tokenizer_and_model(args.model, device, dtype)
    model = PeftModel.from_pretrained(base, str(adapter_dir))
    model.eval()
    print(f"모델: {args.model} · 어댑터: {adapter_dir} · 장치: {device} · 프롬프트 {len(prompts)}개")

    rows: list[dict[str, Any]] = []
    started = time.perf_counter()
    for item in prompts:
        with model.disable_adapter():
            base_text = generate(model, tokenizer, item["prompt"], device, args.max_new_tokens)
        lora_text = generate(model, tokenizer, item["prompt"], device, args.max_new_tokens)
        rows.append({
            "id": item["id"], "prompt": item["prompt"], "base": base_text, "lora": lora_text,
            "base_format_ok": follows_format(base_text), "lora_format_ok": follows_format(lora_text),
        })
        print(f"\n[{item['id']}] {item['prompt']}")
        print(f"  기본  : {base_text[:80].replace(chr(10), ' / ')}")
        print(f"  어댑터: {lora_text[:80].replace(chr(10), ' / ')}")

    run_name = adapter_dir.name if not args.tag else f"{adapter_dir.name}-{args.tag}"
    summary = {
        "adapter": str(adapter_dir), "model": args.model, "device": str(device), "dtype": str(dtype),
        "seed": args.seed, "max_new_tokens": args.max_new_tokens,
        "base_format_hits": sum(1 for r in rows if r["base_format_ok"]),
        "lora_format_hits": sum(1 for r in rows if r["lora_format_ok"]),
        "elapsed_sec": round(time.perf_counter() - started, 1),
    }
    json_path = write_json(OUTPUTS_DIR / f"compare-{run_name}.json", {"summary": summary, "rows": rows})
    md_path = write_text(OUTPUTS_DIR / f"compare-{run_name}.md", render_markdown(run_name, args.model, rows, summary))
    print(f"\n형식 준수: 기본 {summary['base_format_hits']}/{len(rows)} · 어댑터 {summary['lora_format_hits']}/{len(rows)}")
    print(f"기록: {json_path} · {md_path}")


if __name__ == "__main__":
    main()
