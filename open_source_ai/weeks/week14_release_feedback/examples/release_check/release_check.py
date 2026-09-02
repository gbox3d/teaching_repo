"""릴리스 준비 점검 도구.

저장소 폴더를 읽기 전용으로 검사해 릴리스 문서 세트·버전·비밀 관리 상태를 표로 보여 주고,
결과를 outputs/release-check-<시각>.json 에 남긴다. 어떤 파일도 수정하지 않는다.
모델·GPU·네트워크가 필요 없다.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# README 에서 찾을 8개 절과, 제목 줄에 나타날 수 있는 단서(소문자로 비교)
README_SECTIONS: dict[str, tuple[str, ...]] = {
    "무엇": ("무엇", "소개", "개요", "about", "overview"),
    "왜": ("왜", "동기", "배경", "why", "motivation"),
    "설치": ("설치", "install", "setup"),
    "실행": ("실행", "사용법", "usage", "run", "quick start"),
    "예시": ("예시", "예제", "example"),
    "제한": ("제한", "한계", "limitation", "known issue"),
    "라이선스": ("라이선스", "license"),
    "출처": ("출처", "source", "credit", "acknowledg"),
}
LICENSE_HINTS = ("MIT", "Apache", "BSD", "GPL", "MPL", "Unlicense")
CITATION_FIELDS = ("cff-version", "title", "version", "authors")

Item = dict[str, str]


def item(check: str, level: str, message: str) -> Item:
    return {"check": check, "level": level, "message": message}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def heading_lines(text: str) -> list[str]:
    return [line.lstrip("#").strip().lower() for line in text.splitlines() if line.startswith("#")]


def check_file(repo: Path, name: str, level_if_missing: str, why: str) -> Item:
    if (repo / name).is_file():
        return item(name.lower(), "pass", f"{name} 있음")
    return item(name.lower(), level_if_missing, f"{name} 없음 - {why}")


def check_readme(repo: Path) -> list[Item]:
    text = read_text(repo / "README.md")
    if not text:
        return [item("readme", "fail", "README.md 가 없다")]
    heads = heading_lines(text)
    items = [item("readme", "pass", f"README.md 제목 {len(heads)}개")]
    missing = [
        name
        for name, hints in README_SECTIONS.items()
        if not any(hint in head for head in heads for hint in hints)
    ]
    if missing:
        items.append(item("readme.sections", "fail", "빠진 절: " + ", ".join(missing)))
    else:
        items.append(item("readme.sections", "pass", "8개 절이 모두 있다"))
    has_ai = any(re.search(r"\bai\b", head) or "인공지능" in head for head in heads)
    if has_ai or (repo / "AI_USAGE.md").is_file():
        items.append(item("readme.ai_usage", "pass", "AI 도구 사용 내역 표기가 있다"))
    else:
        items.append(item("readme.ai_usage", "warn", "AI 도구 사용 내역 절(README) 또는 AI_USAGE.md 가 없다"))
    return items


def check_license(repo: Path) -> list[Item]:
    text = read_text(repo / "LICENSE")
    if not text:
        return [item("license", "fail", "LICENSE 없음 - 라이선스 없는 코드는 남이 쓸 수 없다")]
    head = text[:400].lower()
    kind = next((h for h in LICENSE_HINTS if h.lower() in head), None)
    if kind:
        return [item("license", "pass", f"LICENSE 있음 ({kind} 계열로 보임)")]
    return [item("license", "warn", "LICENSE 는 있지만 첫 부분에서 라이선스 이름을 찾지 못했다")]


def check_changelog(repo: Path) -> list[Item]:
    text = read_text(repo / "CHANGELOG.md")
    if not text:
        return [item("changelog", "fail", "CHANGELOG.md 없음 - Keep a Changelog 형식으로 만든다")]
    match = re.search(r"^## \[Unreleased\]\s*$(.*?)(?=^## \[|\Z)", text, re.M | re.S)
    if not match:
        return [item("changelog", "fail", "CHANGELOG.md 에 '## [Unreleased]' 절이 없다")]
    entries = [ln for ln in match.group(1).splitlines() if ln.strip().startswith("-")]
    return [item("changelog", "pass" if entries else "warn", f"Unreleased 항목 {len(entries)}개")]


def check_citation(repo: Path) -> list[Item]:
    text = read_text(repo / "CITATION.cff")
    if not text:
        return [item("citation", "warn", "CITATION.cff 없음 - 인용 정보를 원하면 추가한다")]
    missing = [f for f in CITATION_FIELDS if not re.search(rf"^{f}\s*:", text, re.M)]
    if missing:
        return [item("citation", "fail", "CITATION.cff 필드 부족: " + ", ".join(missing))]
    return [item("citation", "pass", "CITATION.cff 필수 필드 있음")]


def git_tracked(repo: Path, name: str) -> bool | None:
    """git 이 name 을 추적하면 True, 아니면 False, 확인 불가면 None."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "--", name],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return bool(out.stdout.strip()) if out.returncode == 0 else None


def check_secrets(repo: Path) -> list[Item]:
    items = [check_file(repo, ".env.example", "fail", "설정 항목을 보여 줄 견본이 필요하다")]
    tracked = git_tracked(repo, ".env")
    if tracked is None:
        items.append(item("env.tracked", "warn", "git 으로 .env 추적 여부를 확인하지 못했다"))
    elif tracked:
        items.append(item("env.tracked", "fail", ".env 가 git 에 추적되고 있다 - 추적을 끊고 토큰을 회전한다"))
    else:
        items.append(item("env.tracked", "pass", ".env 는 git 에 추적되지 않는다"))
    ignore = read_text(repo / ".gitignore")
    for pattern in (".env", ".venv"):
        present = pattern in ignore
        items.append(item(f"gitignore{pattern}", "pass" if present else "warn",
                          f".gitignore 에 {pattern} {'있음' if present else '없음'}"))
    return items


def check_version(repo: Path, tag: str | None) -> list[Item]:
    text = read_text(repo / "pyproject.toml")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
    if not match:
        return [item("version", "fail", "pyproject.toml 에서 version 을 찾지 못했다")]
    version = match.group(1)
    items = [item("version", "pass", f"pyproject version = {version}")]
    if tag:
        expected = tag[1:] if tag.startswith("v") else tag
        items.append(item("version.tag", "pass" if expected == version else "fail",
                          f"태그 {tag} <-> version {version}"))
    items.append(check_file(repo, "uv.lock", "warn", "없으면 남의 PC 에서 uv sync --frozen 이 불가능하다"))
    return items


def run_checks(repo: Path, tag: str | None, require_model_card: bool) -> list[Item]:
    items: list[Item] = []
    items += check_readme(repo)
    items += check_license(repo)
    items.append(check_file(repo, "CONTRIBUTING.md", "fail", "기여 방법을 모르면 의견이 오지 않는다"))
    items += check_changelog(repo)
    items += check_citation(repo)
    items.append(check_file(repo, "SOURCES.md", "fail", "모델·데이터·코드 출처와 라이선스 표가 필요하다"))
    items.append(check_file(repo, "MODEL_CARD.md", "fail" if require_model_card else "info",
                            "어댑터·모델을 공개하면 모델 카드가 필요하다"))
    items += check_secrets(repo)
    items += check_version(repo, tag)
    return items


def main() -> int:
    load_dotenv()
    if hasattr(sys.stdout, "reconfigure"):
        # 한국어 Windows 콘솔(cp949)에서 특수문자 때문에 출력이 죽지 않게 한다.
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description="릴리스 준비 점검 (읽기 전용)")
    parser.add_argument("--repo", default=os.environ.get("RELEASE_REPO", "."), help="점검할 저장소 폴더")
    parser.add_argument("--tag", default=os.environ.get("RELEASE_TAG"), help="version 과 비교할 태그 (예: v0.1.0)")
    parser.add_argument("--require-model-card", action="store_true", help="MODEL_CARD.md 를 필수로 본다")
    parser.add_argument("--out-dir", default="outputs", help="결과 JSON 을 남길 폴더")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"저장소 폴더를 찾을 수 없다: {repo}")
        return 2

    items = run_checks(repo, args.tag, args.require_model_card)
    counts = {lvl: sum(1 for it in items if it["level"] == lvl) for lvl in ("pass", "warn", "fail", "info")}
    print(f"점검 대상: {repo}")
    for it in items:
        print(f"[{it['level'].upper():4}] {it['check']:<18} {it['message']}")
    print(f"통과 {counts['pass']} · 경고 {counts['warn']} · 실패 {counts['fail']} · 참고 {counts['info']}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = out_dir / f"release-check-{stamp}.json"
    report = {"repo": str(repo), "tag": args.tag, "checked_at": stamp, "counts": counts, "items": items}
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"결과 저장: {out_path}")
    return 1 if counts["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
