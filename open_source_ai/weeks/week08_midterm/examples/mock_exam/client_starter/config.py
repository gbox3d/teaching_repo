"""설정 로더 — 명령행 인자, 환경변수(.env 포함), 기본값의 우선순위를 정한다.

우선순위: 명령행 인자 > 환경변수(.env) > 기본값
모델 이름·주소를 코드에 하드코딩하지 않기 위해 모든 스크립트가 이 모듈을 거친다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:4b"  # 교재 검증용 기본값. CPU 대체는 qwen3:0.6b. 확정 값은 환경 기준표
DEFAULT_TIMEOUT = 120.0


@dataclass(frozen=True)
class Settings:
    host: str
    model: str
    timeout: float


def _normalize_host(raw: str) -> str:
    """끝의 '/' 를 지우고, scheme 이 없으면 http:// 를 붙인다."""
    host = raw.strip().rstrip("/")
    if not host.startswith("http://") and not host.startswith("https://"):
        host = "http://" + host
    return host


def load_settings(
    host: str | None = None,
    model: str | None = None,
    timeout: float | None = None,
) -> Settings:
    """인자 > 환경변수 > 기본값 순서로 Settings 를 만든다."""
    load_dotenv()
    resolved_host = _normalize_host(host or os.environ.get("OLLAMA_HOST") or DEFAULT_HOST)
    resolved_model = (model or os.environ.get("OLLAMA_MODEL") or DEFAULT_MODEL).strip()

    if timeout is not None:
        resolved_timeout = timeout
    else:
        raw_timeout = os.environ.get("OLLAMA_TIMEOUT", "").strip()
        try:
            resolved_timeout = float(raw_timeout) if raw_timeout else DEFAULT_TIMEOUT
        except ValueError:
            resolved_timeout = DEFAULT_TIMEOUT

    return Settings(host=resolved_host, model=resolved_model, timeout=resolved_timeout)
