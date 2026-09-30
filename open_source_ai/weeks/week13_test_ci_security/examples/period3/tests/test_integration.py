"""통합 테스트 — 실제 Ollama 서버와 모델이 필요하다. 기본 `uv run pytest` 에서는 제외된다.

pyproject 의 `addopts = "-m 'not integration'"` 이 이 파일의 테스트를 걸러 낸다.
실행하려면 두 가지가 모두 필요하다.

    $env:RUN_INTEGRATION = "1"
    uv run pytest -m integration --durations=3

마커로 거르는 이유: 느리고(수 초~수십 초), 환경(서버·모델·GPU)에 따라 결과가 달라지므로
CI 의 매 push 검사에 넣지 않는다. 대신 릴리스 전 수동 점검 항목으로 둔다.
"""

from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv

from app.ollama_client import HttpOllamaClient
from app.schemas import ChatRequest
from app.service import ChatService

pytestmark = pytest.mark.integration


@pytest.fixture
def real_service() -> ChatService:
    load_dotenv()  # .env 의 RUN_INTEGRATION·OLLAMA_* 를 읽는다. 셸 환경변수가 우선한다.
    if os.environ.get("RUN_INTEGRATION") != "1":
        pytest.skip("RUN_INTEGRATION=1 이 아니면 실제 서버 테스트를 건너뛴다")
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    model = os.environ.get("OLLAMA_MODEL", "qwen3:8b")  # CPU 대체: qwen3:0.6b
    timeout = float(os.environ.get("OLLAMA_TIMEOUT", "60"))
    return ChatService(client=HttpOllamaClient(host, timeout=timeout), model=model, host=host)


def test_real_health(real_service: ChatService) -> None:
    health = real_service.health()
    assert health.ok, health.detail


def test_real_chat_returns_text_and_meta(real_service: ChatService) -> None:
    request = ChatRequest(prompt="uv가 무엇인지 한 문장으로 답해.", max_tokens=48)
    response = real_service.chat(request)
    # 답의 내용은 검사하지 않는다. 비어 있지 않고 메타가 붙어 오는지만 본다.
    assert response.answer
    assert response.eval_count is not None
    assert response.total_duration_ms is not None
