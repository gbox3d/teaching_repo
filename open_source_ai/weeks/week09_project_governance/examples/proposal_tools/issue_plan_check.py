"""이슈 계획(issue_plan.json)이 '작고 검증 가능한 단위'인지 검사하고 보고서를 남긴다.

검사 항목:
  - 마일스톤 3개, 각각 이름·주차(10~15)·닫히는 조건(done_when)
  - Issue 8~10개, 각각 제목 60자 이하·마일스톤 일치·담당 1명·예상 3일 이하·완료 조건
  - 마일스톤마다 Issue 2개 이상, 담당자별 Issue 수 편차 2 이하
결과는 outputs/issue_plan_report.md 와 .json 에 기록한다. 경고가 있으면 종료 코드 1.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

MAX_TITLE = 60
MAX_DAYS = 3


def load_plan(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"계획 파일이 없다: {path} (issue_plan.sample.json 을 복사해 시작한다)")
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 문법 오류: {path} {exc.lineno}행 - {exc.msg}") from exc
    for key in ("milestones", "issues"):
        if not isinstance(plan.get(key), list):
            raise ValueError(f"'{key}' 배열이 필요하다: {path}")
    return plan


def check_milestones(milestones: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    if len(milestones) != 3:
        warnings.append(f"마일스톤은 3개를 권장한다(현재 {len(milestones)}개).")
    for index, item in enumerate(milestones, start=1):
        label = item.get("name") or f"#{index}"
        if not item.get("name"):
            warnings.append(f"마일스톤 {index}: 이름(name)이 없다.")
        week = item.get("week")
        if not isinstance(week, int) or not 10 <= week <= 15:
            warnings.append(f"마일스톤 {label}: week 는 10~15 사이 정수여야 한다(현재 {week!r}).")
        if len(str(item.get("done_when", "")).strip()) < 10:
            warnings.append(f"마일스톤 {label}: 닫히는 조건(done_when)을 구체적으로 적는다.")
    return warnings


def check_issues(issues: list[dict[str, Any]], milestone_names: set[str]) -> list[str]:
    warnings: list[str] = []
    if not 8 <= len(issues) <= 10:
        warnings.append(f"Issue 는 8~10개를 권장한다(현재 {len(issues)}개).")
    for index, issue in enumerate(issues, start=1):
        title = str(issue.get("title", "")).strip()
        label = f"Issue {index} '{title[:20]}'" if title else f"Issue {index}"
        if not title:
            warnings.append(f"{label}: 제목이 없다.")
        elif len(title) > MAX_TITLE:
            warnings.append(f"{label}: 제목이 {MAX_TITLE}자를 넘는다({len(title)}자). 완료된 상태를 짧게 쓴다.")
        if issue.get("milestone") not in milestone_names:
            warnings.append(f"{label}: 마일스톤 '{issue.get('milestone')}' 이 milestones 의 name 과 일치하지 않는다.")
        if not str(issue.get("assignee", "")).strip():
            warnings.append(f"{label}: 담당(assignee) 1명이 필요하다.")
        days = issue.get("days")
        if not isinstance(days, (int, float)) or days <= 0:
            warnings.append(f"{label}: 예상 일수(days)는 0보다 큰 수여야 한다.")
        elif days > MAX_DAYS:
            warnings.append(f"{label}: 예상 {days}일 - {MAX_DAYS}일 이하로 쪼갠다.")
        if len(str(issue.get("done_when", "")).strip()) < 10:
            warnings.append(f"{label}: 완료 조건(done_when)이 없거나 너무 짧다.")
    return warnings


def check_balance(issues: list[dict[str, Any]], milestone_names: list[str]) -> list[str]:
    warnings: list[str] = []
    per_milestone = Counter(str(issue.get("milestone")) for issue in issues)
    for name in milestone_names:
        if per_milestone[name] < 2:
            warnings.append(f"마일스톤 '{name}': Issue 가 {per_milestone[name]}개다. 2개 이상 둔다.")
    per_assignee = Counter(str(issue.get("assignee", "")).strip() for issue in issues if issue.get("assignee"))
    if per_assignee and max(per_assignee.values()) - min(per_assignee.values()) > 2:
        detail = ", ".join(f"{who} {count}" for who, count in per_assignee.most_common())
        warnings.append(f"담당자별 Issue 수 편차가 크다({detail}). 개인 기여 증거가 고르게 남도록 조정한다.")
    return warnings


def render_report(plan: dict[str, Any], warnings: list[str]) -> str:
    lines = [f"# 이슈 계획 검사 ({datetime.now().isoformat(timespec='seconds')})", ""]
    lines.append(f"- 팀: {plan.get('team', '(미기재)')} · 마일스톤 {len(plan['milestones'])}개 · Issue {len(plan['issues'])}개 · 경고 {len(warnings)}개")
    lines.append("")
    for milestone in plan["milestones"]:
        name = milestone.get("name", "")
        lines += [f"## {name} (week {milestone.get('week')})", "", f"닫히는 조건: {milestone.get('done_when', '')}", ""]
        lines += ["| 제목 | 담당 | 일수 | 완료 조건 |", "|---|---|---:|---|"]
        for issue in plan["issues"]:
            if issue.get("milestone") == name:
                lines.append(f"| {issue.get('title', '')} | {issue.get('assignee', '')} | {issue.get('days', '')} | {issue.get('done_when', '')} |")
        lines.append("")
    lines.append("## 경고")
    lines.append("")
    lines += [f"- {item}" for item in warnings] or ["- 없음"]
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="이슈 계획 검사")
    parser.add_argument("--plan", default="issue_plan.sample.json", help="계획 JSON 경로")
    parser.add_argument("--out-dir", default="outputs", help="보고서 폴더")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # Windows 콘솔(cp949)에서 인코딩 오류로 멈추지 않게 한다
    args = build_parser().parse_args(argv)
    try:
        plan = load_plan(Path(args.plan))
    except (FileNotFoundError, ValueError) as exc:
        print(f"[오류] {exc}", file=sys.stderr)
        return 2
    names = [str(item.get("name", "")) for item in plan["milestones"]]
    warnings = check_milestones(plan["milestones"]) + check_issues(plan["issues"], set(names)) + check_balance(plan["issues"], names)
    report = render_report(plan, warnings)
    print(report)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "issue_plan_report.md").write_text(report, encoding="utf-8")
    summary = {"plan": args.plan, "milestones": len(plan["milestones"]), "issues": len(plan["issues"]), "warnings": warnings}
    (out_dir / "issue_plan_report.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"기록: {out_dir / 'issue_plan_report.md'}")
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
