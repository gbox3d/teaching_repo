"""요청·응답 스키마 — 앱 서버가 받는 것과 돌려주는 것의 계약.

pydantic 모델은 세 가지 일을 한다.
1. 잘못된 요청을 코드가 실행되기 전에 422로 거절한다(빈 메시지, 범위 밖 temperature).
2. 응답 형식을 문서(/docs)에 자동으로 싣는다.
3. 13주차 테스트가 "이 형식이 지켜지는가"를 검사하는 기준이 된다.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Role = Literal["system", "user", "assistant"]


class ChatMessage(BaseModel):
    """대화 한 줄. Ollama /api/chat 의 messages 항목과 같은 모양이다."""

    role: Role
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    """POST /chat, POST /chat/stream 요청 본문."""

    messages: list[ChatMessage] = Field(min_length=1, max_length=40)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=256, ge=1, le=2048, description="Ollama options.num_predict")
    model: str | None = Field(default=None, description="비우면 서버 기본 모델(OLLAMA_MODEL)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "messages": [
                        {"role": "user", "content": "uv lock과 uv sync의 차이를 한 문장으로 설명해 줘."}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 128,
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """POST /chat 정상 응답. Ollama 응답 메타를 밀리초 단위로 바꿔 싣는다."""

    request_id: str
    model: str
    reply: str
    eval_count: int | None = None
    eval_duration_ms: float | None = None
    total_duration_ms: float | None = None


class OllamaStatus(BaseModel):
    """모델 서버 상태. 필드 이름에 model_ 접두사를 쓰면 pydantic 보호 이름과 겹치므로 피한다."""

    host: str
    reachable: bool
    model: str
    has_model: bool
    detail: str = ""


class HealthResponse(BaseModel):
    """GET /health 응답. 앱 서버가 살아 있는가와 모델 서버가 준비되었는가를 구분한다."""

    status: Literal["ok", "degraded"]
    service: str
    version: str
    ollama: OllamaStatus


class ErrorResponse(BaseModel):
    """502·503·504 오류 응답 본문. 사람이 읽을 detail 과 추적용 request_id 를 항상 넣는다."""

    request_id: str
    error: str
    detail: str
