"""pytest 공통 fixture — 가짜 Ollama 클라이언트와 테스트용 서비스.

실제 서버·모델 없이 서비스 로직을 검사하기 위해 `OllamaClient` 프로토콜과 같은 모양의
가짜 클래스를 둔다. 테스트는 이 가짜에 "무엇을 돌려줄지"를 미리 넣고, 서비스가 그 응답을
올바른 형태로 바꾸는지, 오류를 올바르게 올리는지만 본다. 모델의 답이 "맞는지"는 보지 않는다.

이 파일은 pytest 가 자동으로 읽는다. 각 테스트 파일에서 import 하지 않아도 fixture 이름을
인자로 쓰면 주입된다.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_service
from app.ollama_client import OllamaError
from app.service import ChatService

FAKE_MODEL = "fake-model:test"
FAKE_HOST = "http://fake-ollama:11434"


def fake_chat_response(content: str, model: str = FAKE_MODEL) -> dict[str, Any]:
    """Ollama `/api/chat` 비스트리밍 응답과 같은 모양의 dict. 필드 이름이 실제와 같아야 한다."""
    return {
        "model": model,
        "message": {"role": "assistant", "content": content},
        "done": True,
        "total_duration": 1_500_000_000,  # 나노초. 서비스가 1500.0 ms 로 바꿔야 한다.
        "eval_count": 12,
    }


class FakeOllamaClient:
    """서비스가 기대하는 두 메서드(`chat`, `list_models`)만 가진 가짜 클라이언트.

    - `reply`: `chat()` 이 돌려줄 답 문장
    - `models`: `list_models()` 가 돌려줄 이름 목록
    - `fail_with`: 지정하면 두 메서드가 그 예외를 던진다(오류 경로 검사용)
    - `calls`: 서비스가 넘긴 인자를 기록한다(메시지 순서·옵션 검사용)
    """

    def __init__(
        self,
        reply: str = "가짜 답입니다.",
        models: list[str] | None = None,
        fail_with: OllamaError | None = None,
    ) -> None:
        self.reply = reply
        self.models = models if models is not None else [FAKE_MODEL]
        self.fail_with = fail_with
        self.calls: list[dict[str, Any]] = []

    def chat(
        self, model: str, messages: list[dict[str, str]], options: dict[str, Any]
    ) -> dict[str, Any]:
        self.calls.append({"model": model, "messages": messages, "options": options})
        if self.fail_with is not None:
            raise self.fail_with
        return fake_chat_response(self.reply, model=model)

    def list_models(self) -> list[str]:
        if self.fail_with is not None:
            raise self.fail_with
        return list(self.models)


ServiceFactory = Callable[..., tuple[ChatService, FakeOllamaClient]]


@pytest.fixture
def fake_client() -> FakeOllamaClient:
    """정상 응답만 돌려주는 가짜 클라이언트."""
    return FakeOllamaClient(models=[FAKE_MODEL, "other-model:latest"])


@pytest.fixture
def service(fake_client: FakeOllamaClient) -> ChatService:
    """가짜 클라이언트를 주입한 서비스. 대부분의 정상 경로 테스트가 이것을 쓴다."""
    return ChatService(client=fake_client, model=FAKE_MODEL, host=FAKE_HOST)


@pytest.fixture
def make_service() -> ServiceFactory:
    """오류 경로처럼 클라이언트 설정을 바꿔야 할 때 쓰는 팩토리.

    예: `service, client = make_service(fail_with=OllamaUnavailableError("연결 불가"))`
    """

    def _make(**kwargs: Any) -> tuple[ChatService, FakeOllamaClient]:
        client = FakeOllamaClient(**kwargs)
        return ChatService(client=client, model=FAKE_MODEL, host=FAKE_HOST), client

    return _make


@pytest.fixture
def api_for() -> Iterator[Callable[[ChatService], TestClient]]:
    """FastAPI TestClient 를 만든다. `get_service` 의존성을 주어진 서비스로 덮어쓴다.

    12주차 앱의 `get_client` 와 같은 자리다. 실제 HTTP 서버를 띄우지 않고 라우팅·검증·
    예외→상태 코드 매핑까지 검사할 수 있다. 테스트가 끝나면 덮어쓰기를 반드시 지운다.
    """

    def _api(service: ChatService) -> TestClient:
        app.dependency_overrides[get_service] = lambda: service
        return TestClient(app)

    yield _api
    app.dependency_overrides.clear()
