"""서비스 로직 — 클라이언트를 밖에서 주입받는다.

`ChatService` 는 어떤 클라이언트가 들어오든 `OllamaClient` 프로토콜의 두 메서드만 쓴다.
운영에서는 `HttpOllamaClient`, 테스트에서는 `FakeOllamaClient` 가 들어온다.
"""

from __future__ import annotations

from app.ollama_client import OllamaClient, OllamaError
from app.schemas import ChatRequest, ChatResponse, HealthResponse


class ChatService:
    def __init__(self, client: OllamaClient, model: str, host: str) -> None:
        self.client = client
        self.model = model
        self.host = host

    def health(self) -> HealthResponse:
        """서버 연결과 모델 존재 여부를 확인한다. 실패해도 예외 대신 ok=False 를 돌려준다."""
        try:
            names = self.client.list_models()
        except OllamaError as exc:
            return HealthResponse(
                ok=False, ollama_host=self.host, model=self.model, detail=str(exc)
            )

        if self.model in names or f"{self.model}:latest" in names:
            detail = f"모델 {len(names)}개 중 {self.model} 사용 가능"
            return HealthResponse(ok=True, ollama_host=self.host, model=self.model, detail=detail)

        installed = ", ".join(names) if names else "없음"
        detail = f"{self.model} 이(가) 서버에 없다. 설치된 모델: {installed}"
        return HealthResponse(ok=False, ollama_host=self.host, model=self.model, detail=detail)

    def build_messages(self, request: ChatRequest) -> list[dict[str, str]]:
        """system 이 있으면 맨 앞에, 그 다음 user. 이 순서가 바뀌면 모델 답이 달라진다."""
        messages: list[dict[str, str]] = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})
        return messages

    def chat(self, request: ChatRequest) -> ChatResponse:
        """요청을 Ollama 메시지로 조립하고 응답을 우리 스키마로 바꾼다. 오류는 그대로 올린다."""
        options = {"temperature": request.temperature, "num_predict": request.max_tokens}
        data = self.client.chat(self.model, self.build_messages(request), options)

        message = data.get("message") or {}
        answer = str(message.get("content", "")).strip()
        duration_ns = data.get("total_duration")
        duration_ms = duration_ns / 1_000_000 if isinstance(duration_ns, int | float) else None

        return ChatResponse(
            model=str(data.get("model", self.model)),
            answer=answer,
            eval_count=data.get("eval_count"),
            total_duration_ms=duration_ms,
        )
