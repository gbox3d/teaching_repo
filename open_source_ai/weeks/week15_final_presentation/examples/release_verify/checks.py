"""릴리스 패키지 정적 검사 함수 모음.

verify_release.py가 호출한다. 모델·GPU·네트워크 없이 파일과 git 상태만 본다.
검사 결과는 CheckResult(name, status, detail)로 통일한다.
status: PASS(통과) · WARN(사람 확인 필요) · FAIL(릴리스 결함) · SKIP(해당 없음)
"""

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FILES: dict[str, tuple[str, ...]] = {
    "README": ("README.md",),
    "LICENSE": ("LICENSE", "LICENSE.md", "LICENSE.txt"),
    "CONTRIBUTING": ("CONTRIBUTING.md",),
    "CHANGELOG": ("CHANGELOG.md",),
    "SOURCES": ("SOURCES.md",),
    "pyproject": ("pyproject.toml",),
    "uv.lock": ("uv.lock",),
    ".gitignore": (".gitignore",),
    ".env.example": (".env.example",),
}

OPTIONAL_FILES: dict[str, tuple[str, ...]] = {
    "CODE_OF_CONDUCT": ("CODE_OF_CONDUCT.md",),
    "CITATION.cff": ("CITATION.cff",),
    "MODEL_CARD": ("MODEL_CARD.md", "model_card.md", "docs/MODEL_CARD.md"),
    "tests/": ("tests",),
    "CI workflow": (".github/workflows",),
}

# README에 있어야 하는 절. 정규식은 느슨하게 두고 최종 판단은 사람이 한다.
README_SECTIONS: dict[str, str] = {
    "실행 절차(uv sync 또는 uv run)": r"uv (sync|run)",
    "라이선스 언급": r"(?i)licen[cs]e|라이선스",
    "출처·SOURCES 언급": r"(?i)sources\.md|출처",
    "한계·알려진 문제": r"(?i)limitation|known issue|한계|알려진",
}

# 비밀 패턴. 자리표시자도 걸리므로 결과는 사람이 확인하고 이유를 기록한다.
SECRET_PATTERNS: dict[str, str] = {
    "Hugging Face token": r"hf_[A-Za-z0-9]{30,}",
    "GitHub token": r"(ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{20,})",
    "generic sk- key": r"sk-[A-Za-z0-9_\-]{20,}",
    "AWS access key": r"AKIA[0-9A-Z]{16}",
    "private key block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "key=value 형태의 값": r"(?i)\b(token|secret|password|api_key)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}",
}

GITIGNORE_REQUIRED: tuple[str, ...] = (".venv", ".env", "outputs")
TEXT_SUFFIXES = frozenset({".py", ".md", ".toml", ".txt", ".yml", ".yaml", ".json", ".cfg", ".ini", ".ps1", ".example", ".cff", ""})
MAX_SCAN_BYTES = 1_000_000


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str


def find_file(repo: Path, candidates: tuple[str, ...]) -> Path | None:
    """후보 이름 중 처음 존재하는 경로를 돌려준다."""
    for name in candidates:
        path = repo / name
        if path.exists():
            return path
    return None


def check_required_files(repo: Path, tracked: list[str] | None = None) -> list[CheckResult]:
    """필수·권장 파일 존재 검사. tracked(git ls-files)가 있으면 필수 파일이 git에 추적되는지도 본다(검증 중 생긴 uv.lock 등 미추적 파일은 릴리스에 없다)."""
    tracked_set = set(tracked or [])
    results: list[CheckResult] = []
    for label, candidates in REQUIRED_FILES.items():
        found = find_file(repo, candidates)
        if found is None:
            results.append(CheckResult(f"필수 파일 · {label}", "FAIL", f"없음 (후보: {', '.join(candidates)})"))
        elif tracked_set and found.relative_to(repo).as_posix() not in tracked_set:
            results.append(CheckResult(f"필수 파일 · {label}", "FAIL", f"{found.name} 존재하지만 git 추적 안 됨 — 릴리스(태그)에 포함되지 않은 파일"))
        else:
            results.append(CheckResult(f"필수 파일 · {label}", "PASS", found.name))
    for label, candidates in OPTIONAL_FILES.items():
        found = find_file(repo, candidates)
        detail = str(found.relative_to(repo)) if found else "없음 — 권장 항목, 사람이 판단"
        results.append(CheckResult(f"권장 파일 · {label}", "PASS" if found else "WARN", detail))
    return results


def check_gitignore(repo: Path) -> CheckResult:
    path = repo / ".gitignore"
    if not path.exists():
        return CheckResult(".gitignore 항목", "FAIL", ".gitignore 없음")
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [item for item in GITIGNORE_REQUIRED if item not in text]
    if missing:
        return CheckResult(".gitignore 항목", "FAIL", f"누락: {', '.join(missing)}")
    return CheckResult(".gitignore 항목", "PASS", f"{', '.join(GITIGNORE_REQUIRED)} 포함")


def git_output(repo: Path, *args: str) -> str | None:
    """git 명령의 표준 출력을 돌려준다. git이 없거나 저장소가 아니면 None."""
    cmd = ["git", "-C", str(repo), *args]
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def tracked_files(repo: Path) -> list[str]:
    output = git_output(repo, "ls-files")
    return output.splitlines() if output else []


def check_git_state(repo: Path) -> tuple[list[CheckResult], dict[str, str]]:
    """태그·HEAD·작업 트리·추적 파일을 검사하고 보고서용 메타(commit, tag)를 함께 돌려준다."""
    results: list[CheckResult] = []
    meta = {"commit": "", "tag": ""}
    head = git_output(repo, "rev-parse", "--short", "HEAD")
    if head is None:
        results.append(CheckResult("git 저장소", "FAIL", "git 저장소가 아니거나 git을 찾을 수 없음"))
        return results, meta
    meta["commit"] = head
    results.append(CheckResult("git 저장소", "PASS", f"HEAD {head}"))

    tags = git_output(repo, "tag", "--list", "v*") or ""
    tag_list = [t for t in tags.splitlines() if t]
    described = git_output(repo, "describe", "--tags", "--exact-match", "HEAD")
    meta["tag"] = described or ""
    if not tag_list:
        results.append(CheckResult("릴리스 태그", "FAIL", "v* 태그 없음 — 14주차 릴리스 절차 확인"))
    elif described:
        results.append(CheckResult("릴리스 태그", "PASS", f"HEAD가 태그 {described}를 가리킴"))
    else:
        results.append(CheckResult("릴리스 태그", "WARN", f"태그 {', '.join(tag_list)} 있으나 HEAD는 태그 밖 — 기준본 확인"))

    porcelain = git_output(repo, "status", "--porcelain")
    if porcelain:
        results.append(CheckResult("작업 트리", "WARN", f"수정·미추적 파일 {len(porcelain.splitlines())}개 — 기준본이 아닐 수 있음"))
    else:
        results.append(CheckResult("작업 트리", "PASS", "clean"))

    files = tracked_files(repo)
    bad = [f for f in files if f == ".env" or f.startswith(".venv/") or f.endswith((".pt", ".safetensors", ".gguf"))]
    if bad:
        results.append(CheckResult("추적하면 안 되는 파일", "FAIL", ", ".join(bad[:5])))
    else:
        results.append(CheckResult("추적하면 안 되는 파일", "PASS", f"추적 파일 {len(files)}개 중 .env·.venv·모델 가중치 없음"))
    return results, meta


def check_readme(repo: Path) -> list[CheckResult]:
    path = repo / "README.md"
    if not path.exists():
        return [CheckResult("README 절", "SKIP", "README.md 없음")]
    text = path.read_text(encoding="utf-8", errors="ignore")
    results: list[CheckResult] = []
    for label, pattern in README_SECTIONS.items():
        hit = re.search(pattern, text) is not None
        results.append(CheckResult(f"README · {label}", "PASS" if hit else "WARN", "발견" if hit else "패턴 없음 — 직접 읽고 판단"))
    return results


def scan_secrets(repo: Path, files: list[str]) -> CheckResult:
    """추적 중인 텍스트 파일에서 비밀 패턴을 찾는다. 결과는 사람이 확인한다."""
    hits: list[str] = []
    for rel in files:
        path = repo / rel
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > MAX_SCAN_BYTES:
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            for label, pattern in SECRET_PATTERNS.items():
                if re.search(pattern, line):
                    hits.append(f"{rel}:{lineno} ({label})")
                    break
    if hits:
        return CheckResult("비밀 패턴", "FAIL", "; ".join(hits[:8]) + " — 자리표시자면 기록에 이유를 적는다")
    return CheckResult("비밀 패턴", "PASS", "텍스트 파일 검사 완료, 의심 줄 없음")
