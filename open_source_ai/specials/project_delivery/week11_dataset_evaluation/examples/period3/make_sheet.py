"""make_sheet.py — evaluate.py 결과(JSON)에서 수동 채점표(Markdown)를 만든다.

실행: uv run python make_sheet.py                       # outputs/ 안의 가장 최근 eval-*.json
      uv run python make_sheet.py --eval outputs/eval-20xx.json --run lora

채점표의 점수·오류 유형·메모 열은 비어 있다. 사람이 채운다(3교시 실습).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RUBRIC = """## 채점 기준(3단계)

| 점수 | 뜻 | 판단 |
|---:|---|---|
| 2 | 적합 | 질문에 맞는 내용이고 형식(핵심:/이유:/다음 할 일:)을 지켰으며 틀린 정보가 없다 |
| 1 | 부분 | 내용은 대체로 맞지만 형식 위반, 누락, 불필요한 내용 중 하나가 있다 |
| 0 | 부적합 | 틀린 정보, 무관한 답, 거부, 반복, 빈 출력 중 하나에 해당한다 |

오류 유형 코드: `H` 환각(틀린 사실·없는 명령) · `F` 형식 위반 · `R` 거부·회피 · `P` 반복 · `L` 언어 혼합 · `S` 안전·개인정보 · `N` 없음
"""


def one_line(text: str | None, limit: int = 160) -> str:
    if text is None:
        return "(출력 없음)"
    flat = " / ".join(l.strip() for l in text.splitlines() if l.strip()).replace("|", "\\|")
    return flat if len(flat) <= limit else flat[: limit - 1] + "…"


def latest_eval(out_dir: Path) -> Path | None:
    files = sorted(out_dir.glob("eval-*.json"))
    return files[-1] if files else None


def render(payload: dict, run_names: list[str] | None) -> str:
    lines = [f"# 수동 채점표 — {payload['created']}", "", f"- 평가 파일 모드: `{payload['mode']}`, 문항 {payload['n_items']}개",
             "- 채점자: student01 (수업용 표시 이름)", "", RUBRIC]
    for run in payload["runs"]:
        if run_names and run["name"] not in run_names:
            continue
        s = run["summary"]
        lines += [f"## 실행 `{run['name']}` — 모델 {run.get('model') or '-'}, 어댑터 {run.get('adapter') or '-'}", "",
                  f"자동 지표: 키워드 일치율 {s['keyword_hit_rate']}, 형식 준수율 {s['format_rate']}, 유사도 평균 {s['similarity_mean']}", "",
                  "| # | id | 질문 | 모델 출력 | 키워드 | 형식 | 점수 | 오류 유형 | 메모 |", "|---:|---|---|---|---:|:---:|---:|---|---|"]
        for i, item in enumerate(run["items"], 1):
            lines.append(f"| {i} | {item['id']} | {one_line(item['instruction'], 60)} | {one_line(item['output'])} "
                         f"| {item['keyword_hit']} | {'O' if item['format_ok'] else 'X'} |  |  |  |")
        lines += ["", "집계: 2점 ___건 / 1점 ___건 / 0점 ___건 → 평균 ___ (2점 만점)", ""]
    lines += ["## 일관성 점검", "", "- 짝과 같은 5건을 따로 채점하고 일치한 건수를 적는다: ___ / 5",
              "- 불일치한 건의 id와 이유 한 줄: ", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="수동 채점표 생성")
    parser.add_argument("--eval", help="evaluate.py가 만든 eval-*.json 경로")
    parser.add_argument("--run", nargs="*", help="채점표에 넣을 실행 이름(base, lora 등). 생략하면 전부")
    parser.add_argument("--out-dir", default="outputs")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    eval_path = Path(args.eval) if args.eval else latest_eval(out_dir)
    if eval_path is None or not eval_path.exists():
        print("[오류] eval-*.json을 찾지 못했다. 먼저 evaluate.py를 실행하거나 --eval 경로를 준다")
        sys.exit(1)
    payload = json.loads(eval_path.read_text(encoding="utf-8"))
    sheet = render(payload, args.run)
    out_path = out_dir / f"scoring-{payload['created']}.md"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(sheet, encoding="utf-8")
    rows = sum(len(r["items"]) for r in payload["runs"] if not args.run or r["name"] in args.run)
    print(f"채점표 {rows}행 생성: {out_path}")


if __name__ == "__main__":
    main()
