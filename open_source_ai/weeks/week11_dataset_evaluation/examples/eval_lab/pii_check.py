"""pii_check.py — 정규식으로 전화번호·이메일·주민등록번호 패턴을 찾아 보고하고 마스킹하거나 삭제한다.

실행: uv run python pii_check.py                  # 검출 + 마스킹(기본)
      uv run python pii_check.py --action report  # 검출만
      uv run python pii_check.py --action drop    # 검출된 레코드 삭제

정규식은 문맥을 모른다. 검출 목록(outputs/pii_report.json)을 사람이 다시 읽고
오탐(예: 설명용 예시 번호)과 미탐(패턴이 다른 번호)을 데이터 카드에 기록한다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PATTERNS: dict[str, re.Pattern[str]] = {
    "PHONE": re.compile(r"(?<!\d)01[016789][-.\s]?\d{3,4}[-.\s]?\d{4}(?!\d)"),
    "EMAIL": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "RRN": re.compile(r"(?<!\d)\d{6}[-\s]?[1-4]\d{6}(?!\d)"),
}
FIELDS = ("instruction", "output")


def scan_text(text: str) -> list[dict]:
    """텍스트에서 패턴별 매치를 찾아 [{"type", "match", "start"}] 목록으로 돌려준다."""
    hits: list[dict] = []
    for name, pattern in PATTERNS.items():
        for m in pattern.finditer(text):
            hits.append({"type": name, "match": m.group(0), "start": m.start()})
    return sorted(hits, key=lambda h: h["start"])


def mask_text(text: str) -> str:
    for name, pattern in PATTERNS.items():
        text = pattern.sub(f"[{name}]", text)
    return text


def process(rows: list[dict], action: str) -> tuple[list[dict], list[dict]]:
    """레코드마다 필드를 검사한다. action에 따라 그대로 두거나 마스킹하거나 삭제한다."""
    out_rows: list[dict] = []
    findings: list[dict] = []
    for row in rows:
        row = dict(row)
        types: list[str] = []
        for field in FIELDS:
            for hit in scan_text(str(row.get(field, ""))):
                findings.append({"id": row.get("id"), "field": field, **hit})
                if hit["type"] not in types:
                    types.append(hit["type"])
        if types and action == "drop":
            continue
        if types and action == "mask":
            for field in FIELDS:
                row[field] = mask_text(str(row.get(field, "")))
        row["pii_types"] = types
        out_rows.append(row)
    return out_rows, findings


def main() -> None:
    parser = argparse.ArgumentParser(description="개인정보 패턴 검출·마스킹")
    parser.add_argument("--input", default="outputs/clean.jsonl")
    parser.add_argument("--output", default="outputs/masked.jsonl")
    parser.add_argument("--report", default="outputs/pii_report.json")
    parser.add_argument("--action", choices=["report", "mask", "drop"], default="mask")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"[오류] 입력 파일이 없다: {src} — 먼저 clean.py를 실행한다")
        sys.exit(1)
    with src.open(encoding="utf-8-sig") as f:  # BOM이 있어도 읽는다
        rows = [json.loads(line) for line in f if line.strip()]

    out_rows, findings = process(rows, args.action)
    by_type = {name: sum(1 for h in findings if h["type"] == name) for name in PATTERNS}
    report = {
        "input": str(src),
        "action": args.action,
        "scanned": len(rows),
        "records_with_pii": len({h["id"] for h in findings}),
        "hits_by_type": by_type,
        "kept": len(out_rows) if args.action != "report" else len(rows),
        "findings": findings,
    }
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"검사 {len(rows)}건, 검출 레코드 {report['records_with_pii']}건, 유형별 {by_type}")
    for h in findings:
        print(f"  - {h['id']} [{h['field']}] {h['type']}: {h['match']}")
    if args.action == "report":
        print(f"보고서만 저장: {args.report} (출력 파일 없음)")
        return
    out = Path(args.output)
    with out.open("w", encoding="utf-8") as f:
        for row in out_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"{args.action} 적용 후 {len(out_rows)}건 저장: {out}, 보고서: {args.report}")


if __name__ == "__main__":
    main()
