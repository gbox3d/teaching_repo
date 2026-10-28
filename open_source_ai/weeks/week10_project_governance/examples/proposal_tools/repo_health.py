"""GitHub 공개 저장소의 거버넌스 문서와 건강 지표를 REST API로 수집한다.

수집 항목: 라이선스, 열린 Issue 수, 마지막 push, 커뮤니티 파일 유무(CoC·CONTRIBUTING·
이슈·PR 템플릿·LICENSE·README), 최근 릴리스 간격, 기여자 상위 3인 비율(버스 팩터 단서).
첫 응답 시간은 API 호출이 많이 필요하므로 브라우저에서 Issue 3개를 직접 읽어 표본으로 적는다.

인증 없는 호출은 시간당 요청 한도가 낮다. 개인 토큰이 있으면 .env 의 GITHUB_TOKEN 에만 둔다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

API = "https://api.github.com"
DEFAULT_REPOS = "huggingface/transformers,ollama/ollama"
COMMUNITY_KEYS = ("code_of_conduct", "contributing", "issue_template", "pull_request_template", "license", "readme")


class ApiError(Exception):
    """사람이 읽을 메시지를 담은 API 오류."""


def build_headers(token: str | None) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_json(client: httpx.Client, path: str, params: dict[str, Any] | None = None) -> Any:
    response = client.get(f"{API}{path}", params=params)
    if response.status_code == 404:
        raise ApiError(f"찾을 수 없음: {path} (저장소 이름 또는 접근 권한 확인)")
    if response.status_code in (403, 429):
        if response.headers.get("x-ratelimit-remaining") == "0":
            reset = int(response.headers.get("x-ratelimit-reset", "0"))
            when = datetime.fromtimestamp(reset, tz=UTC).isoformat(timespec="minutes")
            raise ApiError(f"GitHub API 요청 한도 소진. 재시도 가능 시각(UTC) {when}. GITHUB_TOKEN 설정 시 한도가 늘어난다.")
        raise ApiError(f"접근 거부(HTTP {response.status_code}): {path}")
    response.raise_for_status()
    return response.json()


def release_interval_days(releases: list[dict[str, Any]]) -> tuple[int, float | None]:
    dates = sorted(
        datetime.fromisoformat(item["published_at"].replace("Z", "+00:00"))
        for item in releases
        if item.get("published_at") and not item.get("prerelease")
    )
    if len(dates) < 2:
        return len(dates), None
    span = (dates[-1] - dates[0]).total_seconds() / 86400
    return len(dates), round(span / (len(dates) - 1), 1)


def survey(client: httpx.Client, owner: str, name: str) -> dict[str, Any]:
    base = f"/repos/{owner}/{name}"
    repo = get_json(client, base)
    profile = get_json(client, f"{base}/community/profile")
    files = profile.get("files") or {}
    releases = get_json(client, f"{base}/releases", {"per_page": 6})
    count, interval = release_interval_days(releases)
    contributors = get_json(client, f"{base}/contributors", {"per_page": 100})
    total = sum(item.get("contributions", 0) for item in contributors)
    top3 = sum(item.get("contributions", 0) for item in contributors[:3])
    return {
        "repo": f"{owner}/{name}",
        "url": repo.get("html_url"),
        "license_spdx": (repo.get("license") or {}).get("spdx_id"),
        "open_issues_and_prs": repo.get("open_issues_count"),
        "pushed_at": repo.get("pushed_at"),
        "default_branch": repo.get("default_branch"),
        "community_health_percentage": profile.get("health_percentage"),
        "community_files": {key: bool(files.get(key)) for key in COMMUNITY_KEYS},
        "recent_releases": count,
        "release_interval_days": interval,
        "contributors_first_page": len(contributors),
        "top3_contribution_share": round(top3 / total, 2) if total else None,
        "note": "기여자 비율은 첫 페이지(최대 100명) 기준 근사치. 첫 응답 시간은 브라우저에서 Issue 3개를 읽어 적는다.",
    }


def print_summary(row: dict[str, Any]) -> None:
    files = ", ".join(key for key, present in row["community_files"].items() if present) or "(없음)"
    print(f"== {row['repo']}")
    print(f"   라이선스 {row['license_spdx']} · 열린 Issue+PR {row['open_issues_and_prs']} · 마지막 push {row['pushed_at']}")
    print(f"   커뮤니티 파일: {files} (health {row['community_health_percentage']}%)")
    print(f"   최근 릴리스 {row['recent_releases']}개 · 평균 간격 {row['release_interval_days']}일")
    print(f"   상위 3인 기여 비율 {row['top3_contribution_share']} (첫 페이지 {row['contributors_first_page']}명 기준)")


def parse_repo(text: str) -> tuple[str, str]:
    owner, _, name = text.strip().partition("/")
    if not owner or not name or "/" in name:
        raise ValueError(f"저장소 표기는 owner/name 형식이어야 한다: {text!r}")
    return owner, name


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GitHub 저장소 거버넌스·건강 지표 수집")
    parser.add_argument("--repo", action="append", default=[], help="owner/name (반복 가능, 기본: SURVEY_REPOS)")
    parser.add_argument("--timeout", type=float, default=20.0, help="초 단위 시간 제한")
    parser.add_argument("--out-dir", default="outputs", help="결과 폴더")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # Windows 콘솔(cp949)에서 인코딩 오류로 멈추지 않게 한다
    load_dotenv()
    args = build_parser().parse_args(argv)
    repos = args.repo or [item for item in os.environ.get("SURVEY_REPOS", DEFAULT_REPOS).split(",") if item.strip()]
    token = os.environ.get("GITHUB_TOKEN") or None
    if not token:
        print("[안내] GITHUB_TOKEN 없음 - 비인증 호출(시간당 한도 낮음)로 진행한다.")

    results: list[dict[str, Any]] = []
    failures = 0
    with httpx.Client(headers=build_headers(token), timeout=args.timeout) as client:
        for text in repos:
            try:
                owner, name = parse_repo(text)
                row = survey(client, owner, name)
                results.append(row)
                print_summary(row)
            except (ApiError, ValueError) as exc:
                failures += 1
                print(f"[실패] {text}: {exc}")
                results.append({"repo": text, "error": str(exc)})
            except httpx.ConnectError:
                failures += 1
                print(f"[실패] {text}: api.github.com 에 연결할 수 없다. 네트워크·프록시를 확인하고 브라우저 값으로 표를 채운다.")
                results.append({"repo": text, "error": "network"})
            except httpx.HTTPError as exc:
                failures += 1
                print(f"[실패] {text}: HTTP 오류 {exc}")
                results.append({"repo": text, "error": str(exc)})

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"health-{stamp}.json"
    path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"기록: {path}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
