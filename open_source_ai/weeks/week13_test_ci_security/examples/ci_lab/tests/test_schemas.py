"""스키마 단위 테스트 — 서버도 모델도 없이 돈다. 가장 빠르고 가장 확실한 테스트다.

실습 1교시에서 이 파일에 "공백만 있는 prompt" 테스트를 추가한다.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.schemas import ChatRequest, ChatResponse, HealthResponse


def test_valid_request_uses_defaults() -> None:
    request = ChatRequest(prompt="uv lock과 uv sync의 차이는?")
    assert request.temperature == 0.2
    assert request.max_tokens == 256
    assert request.system is None


def test_prompt_is_stripped() -> None:
    request = ChatRequest(prompt="  질문  ")
    assert request.prompt == "질문"


@pytest.mark.parametrize(
    "body",
    [
        {"prompt": ""},  # min_length=1
        {"prompt": "안녕", "temperature": 5.0},  # le=2.0
        {"prompt": "안녕", "max_tokens": 0},  # ge=1
        {"prompt": "안녕", "max_tokens": 99_999},  # le=2048
    ],
)
def test_out_of_range_request_is_rejected(body: dict[str, object]) -> None:
    # 코드가 한 줄도 돌기 전에 pydantic 이 거절해야 한다. 어떤 필드가 문제인지는 오류 메시지에 있다.
    with pytest.raises(ValidationError):
        ChatRequest(**body)


def test_response_allows_missing_meta() -> None:
    # Ollama 응답에 eval_count 가 없어도 응답 스키마는 만들어져야 한다(None 허용).
    response = ChatResponse(model="m", answer="a")
    assert response.eval_count is None
    assert response.total_duration_ms is None


def test_health_response_round_trip() -> None:
    health = HealthResponse(ok=False, ollama_host="http://x:11434", model="m", detail="없음")
    data = health.model_dump()
    assert data["ok"] is False
    assert HealthResponse(**data) == health
