"""서비스 로직 테스트 — 가짜 클라이언트를 주입해 모델 없이 검사한다.

검사하는 것: 응답 변환, 클라이언트에 넘기는 인자, 오류가 그대로 올라오는지.
검사하지 않는 것: 모델 답의 내용(그것은 11주차 평가의 일이다).

실습 1교시에서 이 파일에 "system 프롬프트가 messages 맨 앞에 오는지" 테스트를 추가한다.
"""

from __future__ import annotations

import pytest

from app.ollama_client import OllamaUnavailableError
from app.schemas import ChatRequest
from app.service import ChatService
from tests.conftest import FAKE_MODEL, FakeOllamaClient, ServiceFactory


def test_chat_converts_fake_response(service: ChatService) -> None:
    response = service.chat(ChatRequest(prompt="안녕"))
    assert response.answer == "가짜 답입니다."
    assert response.model == FAKE_MODEL
    assert response.eval_count == 12
    # 나노초 1_500_000_000 → 밀리초 1500.0. 단위 변환은 가장 흔한 버그 자리다.
    assert response.total_duration_ms == 1500.0


def test_chat_passes_options_and_user_message(
    service: ChatService, fake_client: FakeOllamaClient
) -> None:
    service.chat(ChatRequest(prompt="안녕", temperature=0.7, max_tokens=64))
    call = fake_client.calls[-1]
    assert call["model"] == FAKE_MODEL
    assert call["options"] == {"temperature": 0.7, "num_predict": 64}
    assert call["messages"] == [{"role": "user", "content": "안녕"}]


def test_health_ok_when_model_is_listed(service: ChatService) -> None:
    health = service.health()
    assert health.ok is True
    assert FAKE_MODEL in health.detail


def test_health_not_ok_when_model_is_missing(make_service: ServiceFactory) -> None:
    service, _ = make_service(models=["another-model:latest"])
    health = service.health()
    assert health.ok is False
    assert "another-model:latest" in health.detail  # 설치된 모델을 알려 줘야 사용자가 조치한다


def test_health_not_ok_when_server_unavailable(make_service: ServiceFactory) -> None:
    service, _ = make_service(fail_with=OllamaUnavailableError("연결 불가"))
    health = service.health()
    assert health.ok is False
    assert "연결 불가" in health.detail


def test_chat_raises_when_server_unavailable(make_service: ServiceFactory) -> None:
    # health 는 예외를 삼키지만 chat 은 그대로 올린다. HTTP 계층이 상태 코드로 바꿀 책임을 진다.
    service, client = make_service(fail_with=OllamaUnavailableError("연결 불가"))
    with pytest.raises(OllamaUnavailableError):
        service.chat(ChatRequest(prompt="안녕"))
    assert len(client.calls) == 1
