r"""릴리스 패키지 검증 CLI (15주차 교차 재현 검증 · 최종 제출 자가 점검용).

다른 팀(또는 우리 팀) 저장소 폴더를 받아 필수 파일, .gitignore, git 태그·작업 트리,
README 절, 비밀 패턴을 검사하고 outputs/에 JSON과 Markdown 보고서를 남긴다.
선택으로 서비스 /health와 Ollama /api/tags를 확인한다.

    uv run python verify_release.py --repo .\review\team-a --team team-a
    uv run python verify_release.py --repo . --team team-a --health-url http://localhost:8000/health
    uv run python verify_release.py --repo . --team team-a --check-ollama

도구는 사람의 판단을 대신하지 않는다. WARN은 직접 읽고 판단하고, FAIL도 이유를 기록한다.
종료 코드: FAIL이 하나라도 있으면 1, 없으면 0.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv

from checks import CheckResult, check_git_state, check_gitignore, check_readme, check_required_files, scan_secrets, tracked_files

load_dotenv()

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
SERVICE_HEALTH_URL = os.environ.get("SERVICE_HEALTH_URL", "")
REVIEWER = os.environ.get("REVIEWER", "student01")


def check_health(url: str) -> CheckResult:
    """대상 서비스의 /health를 GET 한다. 서버를 켜는 것은 검증자의 몫이다."""
    try:
        res = httpx.get(url, timeout=5.0)
    except httpx.HTTPError as exc:
        return CheckResult("서비스 /health", "WARN", f"연결 실패: {exc.__class__.__name__} — README 절차대로 서버를 켰는지 확인")
    if res.status_code == 200:
        return CheckResult("서비스 /health", "PASS", f"200 {res.text[:80]}")
    return CheckResult("서비스 /health", "WARN", f"status {res.status_code}")


def read_env_example_model(repo: Path) -> str:
    """대상 저장소 .env.example의 OLLAMA_MODEL 값을 읽는다. 없으면 빈 문자열."""
    path = repo / ".env.example"
    if not path.exists():
        return ""
    match = re.search(r"^OLLAMA_MODEL\s*=\s*(\S+)", path.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
    return match.group(1).strip("\"'") if match else ""


def check_ollama_model(host: str, repo: Path) -> CheckResult:
    """Ollama /api/tags(GET, 본문 없음)로 대상 팀이 명시한 모델이 이 PC에 캐시되어 있는지 본다."""
    wanted = read_env_example_model(repo)
    try:
        res = httpx.get(f"{host}/api/tags", timeout=5.0)
        res.raise_for_status()
    except httpx.HTTPError as exc:
        return CheckResult("Ollama 모델 캐시", "WARN", f"{host} 연결 실패: {exc.__class__.__name__} — 환경 문제로 기록")
    names = [m.get("name", "") for m in res.json().get("models", [])]
    if not wanted:
        return CheckResult("Ollama 모델 캐시", "WARN", f".env.example에 OLLAMA_MODEL 없음 (서버 모델 {len(names)}개)")

    def tagged(name: str) -> str:
        """태그를 생략한 이름은 Ollama 기본값 :latest로 본다."""
        return name if ":" in name else f"{name}:latest"

    if any(tagged(n) == tagged(wanted) for n in names):
        return CheckResult("Ollama 모델 캐시", "PASS", f"{wanted} 사용 가능")
    # 같은 계열이어도 크기·양자화가 다르면 같은 모델이 아니다. 대체 실행 허용 여부는 대상 README를 읽고 사람이 판단한다.
    family = [n for n in names if n.split(":")[0] == wanted.split(":")[0]]
    if family:
        return CheckResult("Ollama 모델 캐시", "WARN", f"{wanted} 없음 — 같은 계열 {', '.join(family[:3])} 있음, 대상 README의 대체 경로 허용 여부를 확인해 기록")
    return CheckResult("Ollama 모델 캐시", "WARN", f"{wanted} 없음 — 수업 전 사전 캐시 대상, 실습 중 다운로드 금지")


def write_report(results: list[CheckResult], meta: dict[str, str], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    counts = {s: sum(1 for r in results if r.status == s) for s in ("PASS", "WARN", "FAIL", "SKIP")}
    payload = {**meta, "checked_at": stamp, "summary": counts, "results": [asdict(r) for r in results]}
    json_path = out_dir / f"verify-{meta['team']}-{stamp}.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# 릴리스 검증 보고 — {meta['team']}",
        "",
        f"- 저장소: `{meta['repo']}`",
        f"- commit: `{meta['commit'] or '-'}` · 태그: `{meta['tag'] or '-'}`",
        f"- 검증자: {meta['reviewer']} · 시각: {stamp}",
        f"- 요약: PASS {counts['PASS']} · WARN {counts['WARN']} · FAIL {counts['FAIL']} · SKIP {counts['SKIP']}",
        "",
        "| 항목 | 결과 | 근거 |",
        "|---|---|---|",
    ]
    lines += [f"| {r.name} | {r.status} | {r.detail} |" for r in results]
    lines += ["", "## 사람이 판단한 내용", "", "- WARN 항목별 판단:", "- FAIL 원인(환경 / 릴리스 결함 / 설계 한계):", ""]
    md_path = out_dir / f"verify-{meta['team']}-{stamp}.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="릴리스 패키지 검증 도구 (15주차)")
    parser.add_argument("--repo", required=True, help="검증할 저장소 폴더 (clone 받은 곳 또는 .)")
    parser.add_argument("--team", default="team-a", help="보고서 파일명에 쓸 팀 이름 (수업용 값)")
    parser.add_argument("--health-url", default=SERVICE_HEALTH_URL, help="서비스 /health 주소. 비우면 검사하지 않음")
    parser.add_argument("--check-ollama", action="store_true", help=f"{OLLAMA_HOST}/api/tags로 모델 캐시 확인")
    parser.add_argument("--out-dir", default="outputs", help="보고서 저장 폴더")
    return parser.parse_args()


def main() -> int:
    # Windows 콘솔 기본 인코딩(cp949)에서는 한글·특수 기호 출력이 깨지거나 예외가 난다. 표준 출력을 UTF-8로 고정한다.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()
    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"[오류] 저장소 폴더가 없다: {repo}")
        return 2

    tracked = tracked_files(repo)  # git ls-files. 추적되지 않은 파일은 릴리스(태그)에 없으므로 필수 파일 검사와 비밀 검사 모두 이 목록을 기준으로 한다.
    results: list[CheckResult] = []
    results += check_required_files(repo, tracked)
    results.append(check_gitignore(repo))
    git_results, git_meta = check_git_state(repo)
    results += git_results
    results += check_readme(repo)
    results.append(scan_secrets(repo, tracked))
    if args.health_url:
        results.append(check_health(args.health_url))
    if args.check_ollama:
        results.append(check_ollama_model(OLLAMA_HOST, repo))

    meta = {"team": args.team, "repo": str(repo), "reviewer": REVIEWER, **git_meta}
    json_path, md_path = write_report(results, meta, Path(args.out_dir))

    width = max(len(r.name) for r in results)
    for r in results:
        print(f"[{r.status:4}] {r.name.ljust(width)}  {r.detail}")
    fails = sum(1 for r in results if r.status == "FAIL")
    warns = sum(1 for r in results if r.status == "WARN")
    print(f"\n요약: FAIL {fails} · WARN {warns} · 보고서 {md_path} / {json_path}")
    print("도구 결과는 출발점이다. README 절차대로 직접 실행한 결과를 체크리스트에 기록한다.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
