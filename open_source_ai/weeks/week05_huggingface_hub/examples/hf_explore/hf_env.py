"""5주차 예제 공통 도우미 — 환경변수, 캐시 위치, commit hash, 오류 문장, 결과 저장.

네 스크립트(precache.py, cache_report.py, pipeline_demo.py, dataset_peek.py)가 같이 쓴다.
huggingface_hub·transformers·datasets 는 import 시점에 HF_HOME·HF_HUB_OFFLINE 을 읽으므로,
각 스크립트는 그 라이브러리를 import 하기 전에 prepare_env() 를 먼저 호출한다.

확인 실행:
    uv run python hf_env.py
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# 교재 검증용 기본값. 실제 학기의 모델 ID·revision 은 환경 기준표에서 확정한다.
DEFAULTS: dict[str, str] = {
    "HF_TEXT_MODEL": "Qwen/Qwen2.5-0.5B-Instruct",
    "HF_CLS_MODEL": "lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    "HF_EMBED_MODEL": "intfloat/multilingual-e5-small",
}

# 값이 비어 있으면 "설정하지 않은 것"으로 다룰 변수. 빈 HF_HOME 은 상대 경로 hub/ 를 만들고,
# 빈 HF_TOKEN 은 "Bearer " 헤더를 보내 401 을 일으킨다.
_BLANK_MEANS_UNSET = ("HF_HOME", "HF_HUB_CACHE", "HF_TOKEN", "HF_HUB_OFFLINE")


def prepare_env() -> None:
    """.env 를 읽고 빈 값을 정리한다. huggingface_hub 계열을 import 하기 전에 호출한다."""
    load_dotenv()  # 이미 설정된 환경변수는 덮어쓰지 않는다
    for name in _BLANK_MEANS_UNSET:
        if name in os.environ and not os.environ[name].strip():
            del os.environ[name]


def env(name: str, default: str | None = None) -> str | None:
    """환경변수를 읽되 빈 값은 없는 것으로 본다. 기본값은 인자 > DEFAULTS 순서."""
    value = os.environ.get(name, "").strip()
    if value:
        return value
    return default if default is not None else DEFAULTS.get(name)


def offline_mode() -> bool:
    return os.environ.get("HF_HUB_OFFLINE", "0").strip().lower() in ("1", "true", "yes")


def resolve_cache_dir(explicit: str | None = None) -> Path:
    """인자 > HF_HUB_CACHE > HF_HOME/hub > ~/.cache/huggingface/hub 순서로 캐시 폴더를 정한다."""
    if explicit:
        return Path(explicit).expanduser()
    hub_cache = env("HF_HUB_CACHE")
    if hub_cache:
        return Path(hub_cache).expanduser()
    hf_home = env("HF_HOME")
    if hf_home:
        return Path(hf_home).expanduser() / "hub"
    return Path.home() / ".cache" / "huggingface" / "hub"


def cached_commit_hash(repo_id: str, requested: str | None = None) -> str | None:
    """캐시에서 repo_id 의 commit hash 를 찾는다. requested(접두사)와 맞는 것 > refs 에 main 이 있는 것 > 최신."""
    try:
        from huggingface_hub import scan_cache_dir

        info = scan_cache_dir(resolve_cache_dir())
    except Exception:
        return None
    for repo in info.repos:
        if repo.repo_id != repo_id:
            continue
        revisions = sorted(repo.revisions, key=lambda r: r.last_modified, reverse=True)
        for rev in revisions:
            if requested and rev.commit_hash.startswith(requested):
                return rev.commit_hash
        for rev in revisions:
            if "main" in rev.refs:
                return rev.commit_hash
        return revisions[0].commit_hash if revisions else None
    return None


def explain_hub_error(exc: BaseException, repo_id: str) -> str:
    """Hub 조회·다운로드 실패를 사람이 읽을 한 문장으로 바꾼다."""
    try:
        from huggingface_hub.errors import GatedRepoError, RepositoryNotFoundError, RevisionNotFoundError
    except ImportError:  # 오래된 huggingface_hub
        from huggingface_hub.utils import GatedRepoError, RepositoryNotFoundError, RevisionNotFoundError

    if isinstance(exc, GatedRepoError):  # RepositoryNotFoundError 의 하위 클래스라 먼저 본다
        return f"gated 저장소다: {repo_id} — 카드에서 약관에 동의하고 .env 의 HF_TOKEN 을 설정해야 파일에 접근할 수 있다"
    if isinstance(exc, RepositoryNotFoundError):
        return f"저장소를 찾지 못했다: {repo_id} — 이름 철자(조직/이름)를 확인한다. 비공개 저장소면 토큰이 필요하다"
    if isinstance(exc, RevisionNotFoundError):
        return f"revision 을 찾지 못했다: {repo_id} — commit hash·브랜치 이름을 Files and versions 탭에서 다시 확인한다"
    if offline_mode():
        return f"오프라인 모드(HF_HUB_OFFLINE=1)라 Hub 에 물어볼 수 없다: {repo_id} — .env 에서 0 으로 되돌리거나 캐시만 쓴다"
    return f"Hub 접근 실패: {repo_id} — 네트워크·프록시를 확인한다 ({exc.__class__.__name__}: {first_line(exc)})"


def format_bytes(num: float) -> str:
    value = float(num)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024:
            return f"{int(value)} B" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.2f} TB"


def first_line(exc: BaseException, limit: int = 400) -> str:
    """예외 메시지의 첫 줄만. 스택 트레이스 대신 기록에 옮길 한 줄."""
    text = str(exc).strip() or exc.__class__.__name__
    line = text.splitlines()[0].strip()
    return line if len(line) <= limit else line[:limit] + "…"


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def save_json(outputs: Path, prefix: str, tag: str | None, record: dict[str, Any]) -> Path:
    """outputs/<prefix>-<시각>[-<tag>].json 으로 저장한다. 폴더는 없으면 만든다."""
    outputs.mkdir(parents=True, exist_ok=True)
    name = f"{prefix}-{timestamp()}" + (f"-{tag}" if tag else "") + ".json"
    path = outputs / name
    body = {"created_at": datetime.now().isoformat(timespec="seconds"), **record}
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return path


def main() -> int:
    prepare_env()
    print("설정 우선순위: 인자 > .env/환경변수 > 기본값")
    for name in DEFAULTS:
        print(f"{name:<15}= {env(name)}")
    print(f"{'cache_dir':<15}= {resolve_cache_dir()}")
    print(f"{'offline':<15}= {offline_mode()}")
    print(f"{'HF_TOKEN':<15}= {'설정됨(값은 표시하지 않음)' if env('HF_TOKEN') else '없음'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
