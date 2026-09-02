"""이슈 계획(issue_plan.json)의 라벨·마일스톤·Issue 를 GitHub 저장소에 등록한다.

순서: 라벨 생성(있으면 건너뜀) → 마일스톤 생성(같은 제목이 있으면 재사용) → Issue 생성.
담당자(assignee)가 collaborator 가 아니어서 422 가 나면 담당자를 비우고 다시 등록한다.
토큰은 .env 의 GITHUB_TOKEN 에만 둔다. --dry-run 은 네트워크 없이 등록 내용만 보여 준다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

API = "https://api.github.com"
LABEL_COLOR = "0e8a16"


def load_plan(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"계획 파일이 없다: {path}")
    plan = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(plan.get("milestones"), list) or not isinstance(plan.get("issues"), list):
        raise ValueError("계획 파일에 'milestones' 와 'issues' 배열이 필요하다.")
    return plan


def issue_body(issue: dict[str, Any]) -> str:
    return "\n".join(
        [
            "## 목적", issue.get("body", "") or "(제안서 Must 와의 연결을 적는다)", "",
            "## 완료 조건", f"- [ ] {issue.get('done_when', '')}", "",
            f"예상 {issue.get('days', '?')}일 · 마일스톤 {issue.get('milestone', '')}",
        ]
    )


def due_on(week: Any, week10: date | None) -> str | None:
    if week10 is None or not isinstance(week, int):
        return None
    return (week10 + timedelta(days=7 * (week - 10))).strftime("%Y-%m-%dT23:59:00Z")


def describe_error(response: httpx.Response) -> str:
    hints = {401: "토큰이 없거나 틀렸다", 403: "권한 부족 또는 요청 한도", 404: "저장소 이름 또는 토큰 권한 확인", 422: "입력값 검증 실패"}
    try:
        message = response.json().get("message", "")
    except ValueError:
        message = response.text[:200]
    return f"HTTP {response.status_code} ({hints.get(response.status_code, '')}): {message}"


def ensure_labels(client: httpx.Client, repo: str, labels: set[str]) -> None:
    for name in sorted(labels):
        response = client.post(f"{API}/repos/{repo}/labels", json={"name": name, "color": LABEL_COLOR})
        if response.status_code == 422:
            continue  # 이미 있음
        if response.status_code >= 400:
            raise RuntimeError(f"라벨 '{name}' 생성 실패 - {describe_error(response)}")


def ensure_milestones(client: httpx.Client, repo: str, milestones: list[dict[str, Any]], week10: date | None) -> dict[str, int]:
    response = client.get(f"{API}/repos/{repo}/milestones", params={"state": "all", "per_page": 100})
    if response.status_code >= 400:
        raise RuntimeError(f"마일스톤 조회 실패 - {describe_error(response)}")
    numbers = {item["title"]: item["number"] for item in response.json()}
    for item in milestones:
        title = str(item.get("name", "")).strip()
        if title in numbers:
            print(f"[재사용] 마일스톤 '{title}' #{numbers[title]}")
            continue
        payload: dict[str, Any] = {"title": title, "description": item.get("done_when", "")}
        if (due := due_on(item.get("week"), week10)):
            payload["due_on"] = due
        created = client.post(f"{API}/repos/{repo}/milestones", json=payload)
        if created.status_code >= 400:
            raise RuntimeError(f"마일스톤 '{title}' 생성 실패 - {describe_error(created)}")
        numbers[title] = created.json()["number"]
        print(f"[생성] 마일스톤 '{title}' #{numbers[title]}")
    return numbers


def create_issue(client: httpx.Client, repo: str, issue: dict[str, Any], milestone_number: int | None) -> dict[str, Any]:
    payload: dict[str, Any] = {"title": issue.get("title", ""), "body": issue_body(issue), "labels": issue.get("labels", [])}
    if milestone_number:
        payload["milestone"] = milestone_number
    if issue.get("assignee"):
        payload["assignees"] = [issue["assignee"]]
    response = client.post(f"{API}/repos/{repo}/issues", json=payload)
    if response.status_code == 422 and "assignees" in payload:
        print(f"[주의] '{payload['title']}': 담당자 {issue['assignee']} 지정 실패(collaborator 아님). 담당자 없이 등록한다.")
        payload.pop("assignees")
        response = client.post(f"{API}/repos/{repo}/issues", json=payload)
    if response.status_code >= 400:
        raise RuntimeError(f"Issue '{payload['title']}' 생성 실패 - {describe_error(response)}")
    data = response.json()
    return {"title": data.get("title"), "number": data.get("number"), "url": data.get("html_url")}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="이슈 계획을 GitHub 에 등록")
    parser.add_argument("--plan", default="issue_plan.json", help="계획 JSON 경로")
    parser.add_argument("--repo", required=True, help="owner/name")
    parser.add_argument("--week10-date", help="10주차 수업일(YYYY-MM-DD). 주면 마일스톤 마감일을 계산한다")
    parser.add_argument("--dry-run", action="store_true", help="등록하지 않고 내용만 출력")
    parser.add_argument("--timeout", type=float, default=20.0, help="초 단위 시간 제한")
    parser.add_argument("--out-dir", default="outputs", help="결과 폴더")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # Windows 콘솔(cp949)에서 인코딩 오류로 멈추지 않게 한다
    load_dotenv()
    args = build_parser().parse_args(argv)
    try:
        plan = load_plan(Path(args.plan))
        week10 = date.fromisoformat(args.week10_date) if args.week10_date else None
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"[오류] {exc}", file=sys.stderr)
        return 2
    if "/" not in args.repo:
        print("[오류] --repo 는 owner/name 형식이어야 한다.", file=sys.stderr)
        return 2

    labels = {label for issue in plan["issues"] for label in issue.get("labels", [])}
    if args.dry_run:
        print(f"[dry-run] {args.repo} 에 라벨 {len(labels)}개, 마일스톤 {len(plan['milestones'])}개, Issue {len(plan['issues'])}개를 등록할 예정")
        for item in plan["milestones"]:
            print(f"  마일스톤: {item.get('name')} (week {item.get('week')}, due {due_on(item.get('week'), week10) or '없음'})")
        for issue in plan["issues"]:
            print(f"  Issue: [{issue.get('milestone')}] {issue.get('title')} → {issue.get('assignee') or '(담당 없음)'}")
        return 0

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("[오류] GITHUB_TOKEN 이 없다. .env 에만 넣고 다시 실행한다(문서·명령줄에 쓰지 않는다).", file=sys.stderr)
        return 2
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "Authorization": f"Bearer {token}"}
    created: list[dict[str, Any]] = []
    try:
        with httpx.Client(headers=headers, timeout=args.timeout) as client:
            ensure_labels(client, args.repo, labels)
            numbers = ensure_milestones(client, args.repo, plan["milestones"], week10)
            for issue in plan["issues"]:
                result = create_issue(client, args.repo, issue, numbers.get(str(issue.get("milestone", "")).strip()))
                created.append(result)
                print(f"[생성] #{result['number']} {result['title']} → {result['url']}")
    except httpx.ConnectError:
        print("[실패] api.github.com 에 연결할 수 없다. 네트워크를 확인하거나 브라우저에서 직접 등록한다.", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"[실패] {exc}", file=sys.stderr)
        return 1
    finally:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = out_dir / f"issue_push-{stamp}.json"
        path.write_text(json.dumps({"repo": args.repo, "created": created}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"기록: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
