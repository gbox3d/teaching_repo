"""Ollama HTTP 클라이언트와 클라이언트 프로토콜.

서비스(`service.py`)는 이 모듈의 구체 클래스가 아니라 `OllamaClient` 프로토콜(메서드 모양)에만
의존한다. 그래서 테스트에서는 `tests/conftest.py`의 FakeOllamaClient 를 대신 넣을 수 있다.
"""

from __future__ import annotations

from typing import Any, Protocol

import httpx


class OllamaError(Exception):
    """Ollama 호출 관련 오류의 공통 부모."""


class OllamaUnavailableError(OllamaError):
    """서버에 연결할 수 없거나 응답이 시간 안에 오지 않았다."""


class ModelNotFoundError(OllamaError):
    """요청한 모델이 서버에 없다(`ollama pull` 이 필요하다)."""


class OllamaClient(Protocol):
    """서비스가 기대하는 클라이언트의 모양. 실제 구현과 가짜 구현이 모두 이 모양을 따른다."""

    def chat(
        self, model: str, messages: list[dict[str, str]], options: dict[str, Any]
    ) -> dict[str, Any]: ...

    def list_models(self) -> list[str]: ...


class HttpOllamaClient:
    """`/api/chat`, `/api/tags` 를 호출하는 실제 클라이언트."""

    def __init__(self, host: str, timeout: float = 60.0) -> None:
        self.host = host.rstrip("/")
        self.timeout = timeout

    def chat(
        self, model: str, messages: list[dict[str, str]], options: dict[str, Any]
    ) -> dict[str, Any]:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            # Qwen3 계열은 thinking 출력이 답과 섞여 나오므로 끈다.
            # 응답 형태가 고정되어 테스트에서 검사하기도 쉬워진다.
            "think": False,
            "options": options,
        }
        try:
            response = httpx.post(f"{self.host}/api/chat", json=payload, timeout=self.timeout)
        except httpx.TimeoutException as exc:
            raise OllamaUnavailableError(
                f"Ollama 응답 시간 초과({self.timeout:.0f}초): {self.host}"
            ) from exc
        except httpx.RequestError as exc:
            raise OllamaUnavailableError(f"Ollama 서버에 연결할 수 없다: {self.host}") from exc

        if response.status_code == 404:
            raise ModelNotFoundError(f"모델이 서버에 없다: {model} (ollama pull {model})")
        if response.status_code >= 400:
            raise OllamaError(
                f"Ollama 오류 응답: HTTP {response.status_code} {response.text[:200]}"
            )
        return response.json()

    def list_models(self) -> list[str]:
        try:
            response = httpx.get(f"{self.host}/api/tags", timeout=self.timeout)
        except httpx.RequestError as exc:
            raise OllamaUnavailableError(f"Ollama 서버에 연결할 수 없다: {self.host}") from exc
        if response.status_code >= 400:
            raise OllamaError(f"Ollama 오류 응답: HTTP {response.status_code}")
        data = response.json()
        return [str(item.get("name", "")) for item in data.get("models", [])]
