"""HTTP 계층 테스트 — 서비스 예외가 상태 코드로 바뀌는지를 TestClient 로 검사한다.

uvicorn 을 띄우지 않는다. `api_for(service)` 가 `get_service` 의존성을 덮어써서
FastAPI 라우팅·pydantic 검증·예외 매핑을 프로세스 안에서 그대로 실행한다.

실습 1교시에서 이 파일에 "모델 없음 → 404" 테스트를 추가한다.
"""

from __future__ import annotations

from collections.abc import Callable

from fastapi.testclient import TestClient

from app.ollama_client import OllamaError, OllamaUnavailableError
from app.service import ChatService
from tests.conftest import ServiceFactory

ApiFactory = Callable[[ChatService], TestClient]


def test_health_endpoint_reports_ok(api_for: ApiFactory, service: ChatService) -> None:
    response = api_for(service).get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["model"] == "fake-model:test"


def test_chat_endpoint_returns_answer(api_for: ApiFactory, service: ChatService) -> None:
    response = api_for(service).post("/chat", json={"prompt": "안녕"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "가짜 답입니다."
    assert body["eval_count"] == 12


def test_invalid_body_is_422(api_for: ApiFactory, service: ChatService) -> None:
    # 서비스까지 가지도 않는다. 422 본문의 loc 에 어느 필드인지 적혀 있다.
    response = api_for(service).post("/chat", json={"prompt": "안녕", "temperature": 9})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "temperature"


def test_unavailable_server_becomes_503(api_for: ApiFactory, make_service: ServiceFactory) -> None:
    service, _ = make_service(fail_with=OllamaUnavailableError("연결 불가"))
    response = api_for(service).post("/chat", json={"prompt": "안녕"})
    assert response.status_code == 503
    assert "연결 불가" in response.json()["detail"]


def test_generic_ollama_error_becomes_502(
    api_for: ApiFactory, make_service: ServiceFactory
) -> None:
    service, _ = make_service(fail_with=OllamaError("HTTP 500 upstream"))
    response = api_for(service).post("/chat", json={"prompt": "안녕"})
    assert response.status_code == 502
