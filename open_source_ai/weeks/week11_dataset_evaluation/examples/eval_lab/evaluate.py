"""evaluate.py — 기준선(base) 모델과 LoRA 어댑터 모델을 test split 문항으로 정량 비교한다.

모드 1(모델): 실제로 생성한 뒤 채점한다. GPU가 없으면 --limit 5 정도로 줄인다.
    uv run python evaluate.py --adapter adapters/run-001
모드 2(예측): 이미 만들어 둔 예측 JSON만 채점한다. 모델·GPU가 필요 없다.
    uv run python evaluate.py --predictions data/sample_predictions/base.json data/sample_predictions/lora.json

예측 JSON 형식: {"model": "이름", "adapter": null, "predictions": [{"id": "q001", "output": "..."}]}
결과: outputs/eval-<시각>.json (실행별 요약 + 문항별 출력·지표)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from metrics import score_item, summarize

# 10주차 lora_lab/common.py의 SYSTEM_PROMPT와 같은 문장. 학습 때와 다른 system 프롬프트로 평가하면 전후 비교가 공정하지 않다.
DEFAULT_SYSTEM = "당신은 오픈소스 AI 응용 수업의 도우미입니다. 한국어로 짧고 정확하게 답합니다."


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_predictions(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "predictions" not in data:
        raise ValueError(f"{path}: 'predictions' 키가 없다")
    return {
        "name": data.get("model", path.stem),
        "model": data.get("model"),
        "adapter": data.get("adapter"),
        "outputs": {p["id"]: p["output"] for p in data["predictions"]},
        "elapsed_sec": None,
    }


def pick_device(requested: str) -> str:
    import torch

    if requested == "cpu":
        return "cpu"
    if torch.cuda.is_available():
        return "cuda"
    if requested == "cuda":
        print("[경고] CUDA를 쓸 수 없어 CPU로 실행한다. --limit로 문항 수를 줄인다")
    return "cpu"


def generate_outputs(
    model_id: str, adapter: str | None, items: list[dict], system: str, max_new_tokens: int, seed: int, device: str
) -> tuple[dict[str, str], float]:
    """같은 프롬프트·같은 디코딩(greedy)·같은 seed로 문항별 출력을 만든다."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    model = model.to(device=device, dtype=torch.float16 if device == "cuda" else torch.float32)
    if adapter:
        if not (Path(adapter) / "adapter_config.json").exists():
            raise ValueError(f"어댑터 폴더에 adapter_config.json이 없다: {adapter}")
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, adapter)
    model.eval()

    outputs: dict[str, str] = {}
    t0 = time.perf_counter()
    for i, item in enumerate(items, 1):
        torch.manual_seed(seed)
        messages = [{"role": "system", "content": system}, {"role": "user", "content": item["instruction"]}]
        prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        # 템플릿이 특수 토큰을 이미 붙였으므로 다시 붙이지 않는다(10주차 compare.py와 같은 조건).
        enc = tok(prompt, return_tensors="pt", add_special_tokens=False).to(device)
        with torch.no_grad():
            gen = model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tok.eos_token_id)
        text = tok.decode(gen[0][enc["input_ids"].shape[1] :], skip_special_tokens=True).strip()
        outputs[item["id"]] = text
        print(f"  [{i}/{len(items)}] {item['id']} → {len(text)}자")
    elapsed = round(time.perf_counter() - t0, 1)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return outputs, elapsed


def score_run(run: dict, items: list[dict]) -> dict:
    rows = []
    for item in items:
        pred = run["outputs"].get(item["id"])
        row = {"id": item["id"], "instruction": item["instruction"], "reference": item["output"],
               "keywords": item.get("keywords", []), "output": pred, "missing": pred is None}
        row.update(score_item(pred or "", item["output"], item.get("keywords", [])))
        rows.append(row)
    return {"name": run["name"], "model": run.get("model"), "adapter": run.get("adapter"),
            "elapsed_sec": run.get("elapsed_sec"), "summary": summarize(rows), "items": rows}


def print_table(results: list[dict]) -> None:
    print("\n| 실행 | n | 키워드 일치율 | 형식 준수율 | 정확 일치율 | 유사도 평균 | 한글 비율 | 반복 | 누락 |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in results:
        s = r["summary"]
        print(f"| {r['name']} | {s['n']} | {s['keyword_hit_rate']:.3f} | {s['format_rate']:.3f} | {s['exact_rate']:.3f} "
              f"| {s['similarity_mean']:.3f} | {s['hangul_ratio_mean']:.3f} | {s['repetition_count']} | {s['missing_count']} |")


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="기준선 vs LoRA 정량 비교")
    parser.add_argument("--test", default="outputs/split/test.jsonl")
    parser.add_argument("--predictions", nargs="*", help="예측 JSON 경로들. 주면 모델을 로드하지 않는다")
    parser.add_argument("--base", default=os.environ.get("HF_TEXT_MODEL", "Qwen/Qwen2.5-0.5B-Instruct"))
    parser.add_argument("--adapter", default=os.environ.get("LORA_ADAPTER_DIR") or None)
    parser.add_argument("--skip-base", action="store_true", help="기준선 생성을 건너뛴다")
    parser.add_argument("--system", default=DEFAULT_SYSTEM, help="두 모델에 똑같이 넣는 시스템 프롬프트")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--exclude", nargs="*", default=[], metavar="ID",
                        help="채점에서 뺄 문항 id(예: split.py --against가 보고한 겹침 문항)")
    parser.add_argument("--max-new-tokens", type=int, default=160)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument("--out-dir", default="outputs")
    args = parser.parse_args()

    test_path = Path(args.test)
    if not test_path.exists():
        print(f"[오류] test 파일이 없다: {test_path} — 먼저 split.py를 실행한다")
        sys.exit(1)
    excluded = set(args.exclude)
    items = [it for it in load_jsonl(test_path) if it["id"] not in excluded][: args.limit]
    if excluded:
        print(f"제외 {len(excluded)}건: {', '.join(sorted(excluded))} → 채점 {len(items)}문항")

    runs: list[dict] = []
    if args.predictions:
        mode = "predictions"
        for p in args.predictions:
            runs.append(load_predictions(Path(p)))
    else:
        mode = "model"
        try:
            device = pick_device(args.device)
            print(f"device={device}, base={args.base}, adapter={args.adapter or '(없음)'}, n={len(items)}")
            if not args.skip_base:
                out, el = generate_outputs(args.base, None, items, args.system, args.max_new_tokens, args.seed, device)
                runs.append({"name": "base", "model": args.base, "adapter": None, "outputs": out, "elapsed_sec": el})
            if args.adapter:
                out, el = generate_outputs(args.base, args.adapter, items, args.system, args.max_new_tokens, args.seed, device)
                runs.append({"name": "lora", "model": args.base, "adapter": args.adapter, "outputs": out, "elapsed_sec": el})
            else:
                print("[안내] --adapter 또는 LORA_ADAPTER_DIR가 없어 기준선만 평가한다")
        except (OSError, ImportError, ValueError) as exc:
            print(f"[오류] 모델 준비 실패: {exc}\n  HF 캐시(HF_HOME)·HF_TEXT_MODEL·어댑터 경로를 확인한다. "
                  "모델 없이 채점만 하려면 --predictions를 쓴다")
            sys.exit(2)
    if not runs:
        print("[오류] 평가할 실행이 없다")
        sys.exit(1)

    results = [score_run(run, items) for run in runs]
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"eval-{stamp}.json"
    payload = {"created": stamp, "mode": mode, "test_file": str(test_path), "n_items": len(items),
               "system": args.system if mode == "model" else None, "seed": args.seed, "runs": results}
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print_table(results)
    print(f"\n저장: {out_path}")


if __name__ == "__main__":
    main()
