"""clean.py — 원시 JSONL을 정규화하고 빈 값·정확 중복·근사 중복을 제거한다.

실행: uv run python clean.py
      uv run python clean.py --near-threshold 0.95   # 근사 중복 판정을 느슨하게

입력 한 줄: {"id", "instruction", "output", "keywords", "source"}
출력: outputs/clean.jsonl, outputs/clean_report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

REQUIRED_FIELDS = ("id", "instruction", "output")


def normalize_text(text: str) -> str:
    """유니코드 정규화(NFKC) 후 앞뒤 공백 제거, 연속 공백은 하나로 줄인다."""
    text = unicodedata.normalize("NFKC", text or "")
    return re.sub(r"\s+", " ", text).strip()


def dedup_key(text: str) -> str:
    """중복 판정용 키: 소문자화 + 공백·문장부호 제거. 한글·영문·숫자만 남는다."""
    return re.sub(r"[\W_]+", "", normalize_text(text).lower())


def char_bigrams(text: str) -> set[str]:
    return {text[i : i + 2] for i in range(len(text) - 1)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def load_jsonl(path: Path) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    bad: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                bad.append({"line": lineno, "reason": f"JSON 파싱 실패: {exc.msg}"})
    return rows, bad


def clean(rows: list[dict], min_output_chars: int, near_threshold: float) -> tuple[list[dict], list[dict]]:
    """정규화 → 필수 필드·길이 검사 → 정확 중복 → 근사 중복 순으로 걸러 낸다."""
    kept: list[dict] = []
    dropped: list[dict] = []
    seen_keys: dict[str, str] = {}
    kept_grams: list[tuple[str, set[str]]] = []

    for row in rows:
        rid = str(row.get("id", "?"))
        missing = [f for f in REQUIRED_FIELDS if not str(row.get(f, "")).strip()]
        if missing:
            dropped.append({"id": rid, "reason": f"필수 필드 비어 있음: {','.join(missing)}"})
            continue
        row = dict(row)
        row["instruction"] = normalize_text(row["instruction"])
        row["output"] = "\n".join(normalize_text(l) for l in row["output"].splitlines() if l.strip())
        if len(row["output"]) < min_output_chars:
            dropped.append({"id": rid, "reason": f"output이 {min_output_chars}자 미만"})
            continue

        key = dedup_key(row["instruction"])
        if key in seen_keys:
            dropped.append({"id": rid, "reason": "정확 중복(instruction)", "dup_of": seen_keys[key]})
            continue

        grams = char_bigrams(dedup_key(row["instruction"] + row["output"]))
        near = [(jaccard(grams, g), other) for other, g in kept_grams]
        best = max(near, default=(0.0, None))
        if best[1] is not None and best[0] >= near_threshold:
            dropped.append(
                {"id": rid, "reason": "근사 중복(instruction+output)", "dup_of": best[1], "similarity": round(best[0], 3)}
            )
            continue

        seen_keys[key] = rid
        kept_grams.append((rid, grams))
        kept.append(row)
    return kept, dropped


def main() -> None:
    parser = argparse.ArgumentParser(description="원시 JSONL 정제·중복 제거")
    parser.add_argument("--input", default="data/raw.jsonl")
    parser.add_argument("--output", default="outputs/clean.jsonl")
    parser.add_argument("--report", default="outputs/clean_report.json")
    parser.add_argument("--min-output-chars", type=int, default=10)
    parser.add_argument("--near-threshold", type=float, default=0.8, help="문자 2-gram Jaccard 유사도 기준(0~1)")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"[오류] 입력 파일이 없다: {src}")
        sys.exit(1)

    rows, bad_lines = load_jsonl(src)
    kept, dropped = clean(rows, args.min_output_chars, args.near_threshold)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for row in kept:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    report = {
        "input": str(src),
        "raw_count": len(rows),
        "bad_lines": bad_lines,
        "kept_count": len(kept),
        "dropped_count": len(dropped),
        "near_threshold": args.near_threshold,
        "dropped": dropped,
    }
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"원시 {len(rows)}건 → 유지 {len(kept)}건, 제거 {len(dropped)}건 (파싱 실패 {len(bad_lines)}줄)")
    for d in dropped:
        extra = f" ← {d['dup_of']}" if "dup_of" in d else ""
        sim = f" (유사도 {d['similarity']})" if "similarity" in d else ""
        print(f"  - {d['id']}: {d['reason']}{extra}{sim}")
    print(f"저장: {out}, 보고서: {args.report}")


if __name__ == "__main__":
    main()
