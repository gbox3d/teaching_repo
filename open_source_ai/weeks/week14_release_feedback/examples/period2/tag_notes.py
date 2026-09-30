"""CHANGELOG 절을 릴리스 노트로 뽑고, 원하면 [Unreleased] 를 버전 절로 승격한다.

- 기본 동작: CHANGELOG.md 의 [<version>] 절(없으면 [Unreleased] 절)을 읽어
  outputs/release-notes-v<version>.md 를 만들고, 태그 명령을 화면에 제안한다.
- --promote: CHANGELOG.md 의 [Unreleased] 를 '## [<version>] - <오늘>' 로 바꾸고
  빈 [Unreleased] 를 위에 새로 둔다. 바꾸기 전 원본을 outputs/ 에 복사한다.
git 명령은 실행하지 않는다. 화면에 제안된 명령을 학생이 읽고 직접 실행한다.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv

SECTION_RE = re.compile(r"^## \[(?P<name>[^\]]+)\](?: - (?P<date>\S+))?\s*$", re.M)
LINK_REF_RE = re.compile(r"^\[[^\]]+\]:\s*\S+")

Section = tuple[str, str | None, str, int, int]  # (이름, 날짜, 본문, 시작, 끝)


def split_sections(text: str) -> list[Section]:
    marks = list(SECTION_RE.finditer(text))
    sections: list[Section] = []
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[mark.end():end].strip("\n")
        sections.append((mark.group("name"), mark.group("date"), body, mark.start(), end))
    return sections


def pyproject_version(repo: Path) -> str | None:
    path = repo / "pyproject.toml"
    if not path.is_file():
        return None
    match = re.search(r'^version\s*=\s*"([^"]+)"', path.read_text(encoding="utf-8"), re.M)
    return match.group(1) if match else None


def promote(text: str, version: str, today: str) -> str:
    sections = split_sections(text)
    if any(name.lower() == version.lower() for name, *_ in sections):
        raise ValueError(
            f"'## [{version}]' 절이 이미 있어 승격하지 않는다. --promote 없이 실행하면 그 절로 노트를 만든다"
        )
    for name, _, body, start, end in sections:
        if name.lower() == "unreleased":
            block = f"## [Unreleased]\n\n## [{version}] - {today}\n\n{body.strip()}\n\n"
            return text[:start] + block + text[end:].lstrip("\n")
    raise ValueError("'## [Unreleased]' 절이 없어 승격할 수 없다")


def build_notes(version: str, body: str, repo_name: str) -> str:
    body_lines = [ln for ln in body.splitlines() if not LINK_REF_RE.match(ln)]
    changes = "\n".join(body_lines).strip() or "- (변경 내역을 CHANGELOG 에 먼저 적는다)"
    lines = [
        f"# {repo_name} v{version}",
        "",
        changes,
        "",
        "## 실행하려면",
        "",
        "```powershell",
        "git clone REPO_URL",
        f"git checkout v{version}",
        "uv sync --frozen",
        "Copy-Item .env.example .env",
        "uv run python -m PACKAGE_NAME --help",
        "```",
        "",
        "## 알려진 제한",
        "",
        "- README 의 「제한」 절을 따른다.",
        "",
        "## 피드백",
        "",
        "- 재현 실패·제안은 Issue 로 남긴다. 환경·명령·출력 세 가지를 함께 적는다.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    load_dotenv()
    if hasattr(sys.stdout, "reconfigure"):
        # 한국어 Windows 콘솔(cp949)에서 특수문자 때문에 출력이 죽지 않게 한다.
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description="CHANGELOG → 릴리스 노트 (git 은 실행하지 않는다)")
    parser.add_argument("--repo", default=os.environ.get("RELEASE_REPO", "."), help="CHANGELOG.md 가 있는 저장소 폴더")
    parser.add_argument("--version", default=os.environ.get("RELEASE_VERSION", "0.1.0"), help="v 없이, 예: 0.1.0")
    parser.add_argument("--promote", action="store_true", help="[Unreleased] 를 버전 절로 바꾼다 (CHANGELOG.md 수정)")
    parser.add_argument("--out-dir", default="outputs", help="릴리스 노트와 원본 사본을 둘 폴더")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    changelog = repo / "CHANGELOG.md"
    if not changelog.is_file():
        print(f"CHANGELOG.md 가 없다: {changelog}")
        return 2
    version = args.version.lstrip("v")
    text = changelog.read_text(encoding="utf-8")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    if args.promote:
        (out_dir / f"CHANGELOG.before-{stamp}.md").write_text(text, encoding="utf-8")
        try:
            text = promote(text, version, date.today().isoformat())
        except ValueError as exc:
            print(exc)
            return 1
        changelog.write_text(text, encoding="utf-8")
        print(f"CHANGELOG.md 승격: [Unreleased] → [{version}] (원본 사본은 {out_dir}/)")

    sections = {name.lower(): body for name, _, body, _, _ in split_sections(text)}
    body = sections.get(version.lower())
    if body is None:
        body = sections.get("unreleased")
        if body is None:
            print(f"CHANGELOG.md 에 [{version}] 절도 [Unreleased] 절도 없다")
            return 1
        print(f"[{version}] 절이 없어 [Unreleased] 절로 노트를 만든다. 태그 전에 --promote 를 고려한다.")

    project_version = pyproject_version(repo)
    if project_version and project_version != version:
        print(f"경고: pyproject version={project_version} 과 --version {version} 이 다르다. 태그 전에 맞춘다.")

    out_path = out_dir / f"release-notes-v{version}.md"
    out_path.write_text(build_notes(version, body, repo.name), encoding="utf-8")
    print(f"릴리스 노트 저장: {out_path}")
    print("\n다음 명령을 저장소 폴더에서 직접 실행한다:")
    print(f'  git tag -a v{version} -m "Release v{version}"')
    print(f"  git push origin v{version}")
    print(f"  GitHub → Releases → Draft a new release → 태그 v{version} 선택 → {out_path.name} 내용 붙여넣기")
    return 0


if __name__ == "__main__":
    sys.exit(main())
