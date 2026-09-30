"""split.py — 정제된 JSONL을 train/val/test로 나누고 누수(같은 질문이 두 split에 있는지)를 검사한다.

실행: uv run python split.py                 # test 20, val 4, 나머지 train (seed 42)
      uv run python split.py --test 10 --val 5 --seed 7
      uv run python split.py --against ..\\..\\..\\week10_peft_lora\\examples\\lora_lab\\data\\sample_sft.jsonl
          # 외부 학습 파일(10주차 LoRA 학습 데이터)과 test 문항이 겹치는지(벤치마크 오염) 함께 검사

분할은 Hugging Face `datasets`의 `Dataset.train_test_split(seed=...)`를 두 번 써서 만든다.
이번 주는 평가가 목적이라 test를 크게 잡는다. 실제 프로젝트에서는 8:1:1 같은 비율이 흔하다.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from clean import char_bigrams, dedup_key, jaccard


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig") as f:  # BOM이 있어도 읽는다
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def make_splits(rows: list[dict], test_n: int, val_n: int, seed: int) -> dict[str, list[dict]]:
    from datasets import Dataset  # 무거운 의존성은 함수 안에서 불러온다

    ds = Dataset.from_list(rows)
    first = ds.train_test_split(test_size=test_n, seed=seed, shuffle=True)
    second = first["train"].train_test_split(test_size=val_n, seed=seed, shuffle=True)
    return {
        "train": [dict(r) for r in second["train"]],
        "val": [dict(r) for r in second["test"]],
        "test": [dict(r) for r in first["test"]],
    }


def leak_check(splits: dict[str, list[dict]]) -> list[dict]:
    """정규화한 instruction 키가 둘 이상의 split에 나타나면 누수로 기록한다."""
    where: dict[str, list[str]] = {}
    for name, rows in splits.items():
        for row in rows:
            where.setdefault(dedup_key(row["instruction"]), []).append(f"{name}:{row['id']}")
    return [{"key": k[:30], "found_in": v} for k, v in where.items() if len(v) > 1]


def contamination_check(test_rows: list[dict], against_rows: list[dict], threshold: float) -> list[dict]:
    """외부 학습 파일의 instruction과 test 문항의 근사 중복(문자 2-gram Jaccard)을 찾는다.

    LoRA 학습에 쓴 질문이 test에 그대로 있으면 그 문항 점수는 '외운 것'일 수 있다(벤치마크 오염).
    """
    ext = [
        (i, row.get("instruction", ""), char_bigrams(dedup_key(row.get("instruction", ""))))
        for i, row in enumerate(against_rows, 1)
    ]
    hits: list[dict] = []
    for row in test_rows:
        grams = char_bigrams(dedup_key(row["instruction"]))
        sim, line, text = max(((jaccard(grams, g), i, t) for i, t, g in ext), default=(0.0, 0, ""))
        if sim >= threshold:
            hits.append({"test_id": row["id"], "similarity": round(sim, 3), "against_line": line, "against_instruction": text[:60]})
    return hits


def main() -> None:
    parser = argparse.ArgumentParser(description="train/val/test 분할과 누수·오염 검사")
    parser.add_argument("--input", default="outputs/masked.jsonl")
    parser.add_argument("--out-dir", default="outputs/split")
    parser.add_argument("--report", default="outputs/split_report.json")
    parser.add_argument("--test", type=int, default=20, help="test 건수")
    parser.add_argument("--val", type=int, default=4, help="val 건수")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--against", help="test와 겹치는지 검사할 외부 학습 JSONL(예: 10주차 sample_sft.jsonl)")
    parser.add_argument("--against-threshold", type=float, default=0.5, help="오염 판정 유사도 기준(0~1)")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"[오류] 입력 파일이 없다: {src} — 먼저 clean.py, pii_check.py를 실행한다")
        sys.exit(1)
    rows = load_jsonl(src)
    if args.test + args.val >= len(rows):
        print(f"[오류] test({args.test}) + val({args.val})이 전체 {len(rows)}건 이상이다. 값을 줄인다")
        sys.exit(1)

    splits = make_splits(rows, args.test, args.val, args.seed)
    leaks = leak_check(splits)

    contamination: list[dict] | None = None
    if args.against:
        against_path = Path(args.against)
        if not against_path.exists():
            print(f"[오류] --against 파일이 없다: {against_path}")
            sys.exit(1)
        contamination = contamination_check(splits["test"], load_jsonl(against_path), args.against_threshold)

    out_dir = Path(args.out_dir)
    for name, part in splits.items():
        write_jsonl(out_dir / f"{name}.jsonl", part)

    report = {
        "input": str(src),
        "total": len(rows),
        "seed": args.seed,
        "counts": {name: len(part) for name, part in splits.items()},
        "ids": {name: [r["id"] for r in part] for name, part in splits.items()},
        "leak_count": len(leaks),
        "leaks": leaks,
        "against": args.against,
        "against_threshold": args.against_threshold if args.against else None,
        "contamination_count": len(contamination) if contamination is not None else None,
        "contamination": contamination,
    }
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = report["counts"]
    print(f"전체 {len(rows)}건 → train {counts['train']} / val {counts['val']} / test {counts['test']} (seed {args.seed})")
    print(f"test ids: {', '.join(report['ids']['test'])}")
    print(f"누수 {len(leaks)}건" + ("" if not leaks else f" — {leaks}"))
    if contamination is not None:
        print(f"외부 학습 데이터와 겹치는 test 문항 {len(contamination)}건 (기준 {args.against_threshold})")
        for h in contamination:
            print(f"  - {h['test_id']} ~ {h['against_line']}행 (유사도 {h['similarity']}): {h['against_instruction']}")
    print(f"저장: {out_dir}/, 보고서: {args.report}")


if __name__ == "__main__":
    main()
