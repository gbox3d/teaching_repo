"""의존성 취약점 감사 보고서 — `uv export` → `pip-audit` → `outputs/` 요약.

사용:
    uv run python audit_report.py                       # 내보내기 + 감사 + 요약(네트워크 필요)
    uv run python audit_report.py --from-json 파일.json  # 저장된 JSON 만 요약(네트워크 불필요)
    uv run python audit_report.py --sample              # 동봉 샘플로 보고서 형식 익히기

pip-audit 은 PyPI 취약점 DB 를 조회하므로 네트워크가 필요하다. 실습실에 네트워크가 없으면
`--from-json` 또는 `--sample` 로 보고서 읽는 법만 연습하고, 실제 감사는 네트워크가 있는 PC 에서
한다. `uv export` 는 uv.lock 이 없으면 먼저 만든다(복사본에서 실행할 것).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# 실제 패키지가 아닌, 보고서 형식을 보여 주기 위한 가상의 결과다.
SAMPLE_AUDIT: dict[str, Any] = {
    "dependencies": [
        {
            "name": "sample-web",
            "version": "1.2.0",
            "vulns": [
                {
                    "id": "SAMPLE-2024-0001",
                    "fix_versions": ["1.2.3"],
                    "aliases": ["CVE-0000-00000"],
                    "description": "샘플: 요청 헤더 파싱에서 서비스 거부가 가능하다.",
                }
            ],
        },
        {"name": "sample-http", "version": "0.9.1", "vulns": []},
        {"name": "sample-json", "version": "3.0.0", "vulns": []},
    ],
    "fixes": [],
}


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8")


def export_requirements(project: Path, target: Path) -> None:
    """uv 가 해석한 의존성 전체(dev 그룹 포함)를 고정 버전 목록으로 내보낸다."""
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["uv", "export", "--format", "requirements-txt", "--no-hashes", "-o", str(target)]
    result = run(cmd, project)
    if result.returncode != 0:
        raise RuntimeError(f"uv export 실패:\n{result.stderr.strip()}")
    print(f"의존성 목록: {target}")


def run_pip_audit(project: Path, requirements: Path, raw_json: Path) -> int:
    """pip-audit 을 JSON 출력으로 실행한다. 종료 코드 0=취약점 없음, 1=있음(또는 오류)."""
    # `uv run python` 아래에서 sys.executable 은 .venv 의 파이썬이다. -m pip_audit 이 바로 잡힌다.
    cmd = [
        sys.executable,
        "-m",
        "pip_audit",
        "-r",
        str(requirements),
        "--no-deps",  # uv export 가 이미 전부 == 로 고정했다. 다시 해석하지 않는다.
        "-f",
        "json",
        "-o",
        str(raw_json),
    ]
    result = run(cmd, project)
    if result.stderr.strip():
        print(result.stderr.strip())
    if not raw_json.exists():
        raise RuntimeError(
            "pip-audit 이 결과 파일을 만들지 못했다. 네트워크(취약점 DB 조회)와 "
            "`uv sync` 로 pip-audit 이 설치되었는지 확인한다."
        )
    return result.returncode


def summarize(data: dict[str, Any], source: str) -> dict[str, Any]:
    """pip-audit JSON 을 사람이 읽을 요약으로 바꾼다."""
    dependencies = data.get("dependencies", [])
    rows: list[dict[str, Any]] = []
    for dep in dependencies:
        for vuln in dep.get("vulns", []):
            rows.append(
                {
                    "package": dep.get("name"),
                    "version": dep.get("version"),
                    "id": vuln.get("id"),
                    "fix_versions": vuln.get("fix_versions", []),
                    "aliases": vuln.get("aliases", []),
                    "description": (vuln.get("description") or "").strip()[:160],
                }
            )
    skipped = [d for d in dependencies if d.get("skip_reason")]
    return {
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "source": source,
        "dependency_count": len(dependencies),
        "vulnerable_package_count": len({r["package"] for r in rows}),
        "vulnerability_count": len(rows),
        "skipped_count": len(skipped),
        "rows": rows,
    }


def write_markdown(summary: dict[str, Any], target: Path) -> None:
    lines = [
        "# 의존성 감사 결과",
        "",
        f"- 시각: {summary['checked_at']}",
        f"- 입력: {summary['source']}",
        f"- 검사한 패키지: {summary['dependency_count']}개, "
        f"취약 패키지: {summary['vulnerable_package_count']}개, "
        f"취약점: {summary['vulnerability_count']}건, 건너뜀: {summary['skipped_count']}개",
        "",
    ]
    if summary["rows"]:
        lines += ["| 패키지 | 설치 버전 | 취약점 ID | 고친 버전 | 설명 |", "|---|---|---|---|---|"]
        for r in summary["rows"]:
            fix = ", ".join(r["fix_versions"]) or "(없음)"
            lines.append(
                f"| {r['package']} | {r['version']} | {r['id']} | {fix} | {r['description']} |"
            )
        lines += [
            "",
            "## 다음 행동",
            "",
            "1. `고친 버전` 이 있으면 `pyproject.toml` 의 하한을 올리거나 "
            "`uv lock --upgrade-package <이름>` 으로 lock 을 갱신한다.",
            "2. 고친 버전이 없으면 취약점 설명을 읽고 우리 코드가 그 기능을 쓰는지 판단해 "
            "`SOURCES.md` 나 Issue 에 기록한다.",
            "3. 갱신 뒤 `uv run pytest` 와 CI 가 초록불인지 확인한다.",
        ]
    else:
        lines += ["알려진 취약점이 없다. 이 결과와 시각을 릴리스 점검표에 적는다."]
    lines.append("")
    target.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="uv export → pip-audit → outputs/ 요약")
    parser.add_argument("--project", default=".", help="pyproject.toml 이 있는 폴더")
    parser.add_argument("--out-dir", default="outputs", help="결과 저장 폴더")
    parser.add_argument(
        "--from-json", help="이미 저장된 pip-audit JSON 만 요약한다(네트워크 불필요)"
    )
    parser.add_argument("--sample", action="store_true", help="동봉된 샘플 결과로 형식을 익힌다")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    out_dir = project / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    exit_code = 0
    if args.sample:
        data, source = SAMPLE_AUDIT, "sample"
    elif args.from_json:
        path = Path(args.from_json)
        data, source = json.loads(path.read_text(encoding="utf-8")), str(path)
    else:
        requirements = out_dir / "requirements-audit.txt"
        raw_json = out_dir / f"audit-raw-{stamp}.json"
        try:
            export_requirements(project, requirements)
            exit_code = run_pip_audit(project, requirements, raw_json)
        except (RuntimeError, FileNotFoundError) as exc:
            print(f"[실패] {exc}")
            print("네트워크가 없으면 --sample 또는 --from-json 으로 보고서 읽기만 연습한다.")
            return 2
        data, source = json.loads(raw_json.read_text(encoding="utf-8")), str(raw_json)

    summary = summarize(data, source)
    (out_dir / f"audit-{stamp}.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    md_path = out_dir / f"audit-{stamp}.md"
    write_markdown(summary, md_path)
    print(
        f"패키지 {summary['dependency_count']}개 중 취약 {summary['vulnerable_package_count']}개, "
        f"취약점 {summary['vulnerability_count']}건 → {md_path}"
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
