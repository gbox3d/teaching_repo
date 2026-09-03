"""설정 로더 — 기본값 < .env·환경변수 < 명령행 인자.

3주차 oss_tool 의 config.py 와 같은 우선순위 규칙을 쓴다.
모델 이름과 서버 주소는 코드에 고정하지 않고 환경변수로 읽는다.

확인 실행:
    uv run python config.py
    uv run python config.py --model qwen3:0.6b
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

from dotenv import load_dotenv

# 교재 검증용 기본값. 실제 학기의 모델 ID·양자화는 환경 기준표에서 확정한다.
DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:8b"  # Q4_K_M 약 5.2 GB, RTX 4070 기준. CPU 대체는 qwen3:0.6b
DEFAULT_TIMEOUT = 180.0  # 초. 첫 호출은 모델 로드 시간이 포함된다.


@dataclass(frozen=True)
class Settings:
    """한 번 만들어지면 바뀌지 않는 실행 설정."""

    host: str
    model: str
    timeout: float

    def url(self, path: str) -> str:
        """`/api/chat` 같은 경로를 서버 주소에 붙인다."""
        return f"{self.host}/{path.lstrip('/')}"


def normalize_host(raw: str) -> str:
    """ollama CLI 는 OLLAMA_HOST 를 `0.0.0.0:11434` 처럼 스킴 없이 쓰기도 한다.

    HTTP 클라이언트는 스킴이 필요하므로 없으면 http:// 를 붙이고, 끝의 / 는 뗀다.
    """
    value = raw.strip()
    if not value:
        return DEFAULT_HOST
    if not value.startswith(("http://", "https://")):
        value = "http://" + value
    return value.rstrip("/")


def load_settings(
    host: str | None = None,
    model: str | None = None,
    timeout: float | None = None,
) -> Settings:
    """인자 > 환경변수(.env 포함) > 기본값 순서로 설정을 결정한다."""
    # .env 가 있으면 읽는다. 이미 설정된 환경변수는 덮어쓰지 않는다(override=False 기본).
    load_dotenv()
    resolved_host = host or os.environ.get("OLLAMA_HOST") or DEFAULT_HOST
    resolved_model = model or os.environ.get("OLLAMA_MODEL") or DEFAULT_MODEL
    if timeout is None:
        try:
            timeout = float(os.environ.get("OLLAMA_TIMEOUT", DEFAULT_TIMEOUT))
        except ValueError:
            timeout = DEFAULT_TIMEOUT
    return Settings(host=normalize_host(resolved_host), model=resolved_model, timeout=timeout)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="설정 우선순위를 확인한다.")
    parser.add_argument("--host", help="Ollama 서버 주소. 생략하면 OLLAMA_HOST 또는 기본값")
    parser.add_argument("--model", help="모델 이름. 생략하면 OLLAMA_MODEL 또는 기본값")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    settings = load_settings(host=args.host, model=args.model)
    print("설정 우선순위: 인자 > .env/환경변수 > 기본값")
    print(f"host    = {settings.host}")
    print(f"model   = {settings.model}")
    print(f"timeout = {settings.timeout:.0f}s")
    print(f"chat url= {settings.url('/api/chat')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
