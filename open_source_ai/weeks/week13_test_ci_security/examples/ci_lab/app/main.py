"""FastAPI 앱 — 12주차 `main.py` 의 최소 발췌.

`get_service` 를 의존성 함수로 두었기 때문에 테스트에서는
`app.dependency_overrides[get_service] = ...` 로 가짜 서비스를 끼워 넣을 수 있다.

실행: uv run uvicorn app.main:app --port 8000
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException

from app.ollama_client import (
    HttpOllamaClient,
    ModelNotFoundError,
    OllamaError,
    OllamaUnavailableError,
)
from app.schemas import ChatRequest, ChatResponse, HealthResponse
from app.service import ChatService

load_dotenv()

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:4b"  # CPU 대체: qwen3:0.6b. 실제 값은 환경 기준표에서 확정한다.

app = FastAPI(title="osa-week13 ci_lab", version="0.1.0")


@lru_cache(maxsize=1)
def get_service() -> ChatService:
    """환경변수 + 기본값으로 실제 서비스를 만든다. 한 번 만들면 재사용한다."""
    host = os.environ.get("OLLAMA_HOST", DEFAULT_HOST)
    model = os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)
    timeout = float(os.environ.get("OLLAMA_TIMEOUT", "60"))
    return ChatService(client=HttpOllamaClient(host, timeout=timeout), model=model, host=host)


ServiceDep = Annotated[ChatService, Depends(get_service)]


@app.get("/health", response_model=HealthResponse)
def health(service: ServiceDep) -> HealthResponse:
    return service.health()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, service: ServiceDep) -> ChatResponse:
    # 서비스 예외를 HTTP 상태 코드로 바꾸는 곳. 이 매핑 자체가 테스트 대상이다.
    try:
        return service.chat(request)
    except OllamaUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ModelNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except OllamaError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
