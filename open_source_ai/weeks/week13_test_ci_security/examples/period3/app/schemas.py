"""요청·응답 스키마.

12주차 `schemas.py`와 같은 역할을 하되, 테스트가 쉬운 최소 형태로 줄여 썼다
(`messages` 목록 대신 `prompt`·`system`).
스키마는 서버도 모델도 없이 검증할 수 있으므로 가장 빠르고 확실한 단위 테스트 대상이다.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    """`/chat` 요청 본문."""

    prompt: str = Field(min_length=1, max_length=4000, description="사용자 질문")
    system: str | None = Field(default=None, max_length=2000, description="시스템 프롬프트")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=256, ge=1, le=2048, description="Ollama options.num_predict")

    @field_validator("prompt")
    @classmethod
    def prompt_must_have_text(cls, value: str) -> str:
        # min_length=1 은 "   " 같은 공백 문자열을 막지 못한다. 경계 조건은 따로 검사한다.
        if not value.strip():
            raise ValueError("prompt는 공백만으로 이루어질 수 없다")
        return value.strip()


class ChatResponse(BaseModel):
    """`/chat` 응답 본문. Ollama 응답 메타 중 기록 가치가 있는 것만 남긴다."""

    model: str
    answer: str
    eval_count: int | None = None
    total_duration_ms: float | None = None


class HealthResponse(BaseModel):
    """`/health` 응답 본문."""

    ok: bool
    ollama_host: str
    model: str
    detail: str
