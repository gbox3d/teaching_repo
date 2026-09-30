"""앱 서버 — 요청을 검증하고 모델 서버(Ollama)에 전달한 뒤 응답을 돌려준다.

실행:  uv run uvicorn app.main:app --port 8000 --reload   (문서: http://localhost:8000/docs)
상태 코드 약속: 200 정상 · 422 요청 형식 오류(pydantic) · 502 모델 서버 연결 실패 · 503 모델 없음 · 504 시간 초과
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import time
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from app.ollama_client import OllamaClient, OllamaError, OllamaModelMissing, OllamaTimeout, OllamaUnavailable
from app.schemas import ChatMessage, ChatRequest, ChatResponse, ErrorResponse, HealthResponse, OllamaStatus

load_dotenv()
SERVICE_NAME = os.environ.get("SERVICE_NAME", "osa-ai-service")
SERVICE_VERSION = "0.1.0"
SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT", "너는 오픈소스 AI 응용 수업의 도우미다. 한국어로 짧고 정확하게 답한다.")
CORS_ORIGINS = [o.strip() for o in os.environ.get("CORS_ORIGINS", "http://localhost:7860,http://127.0.0.1:7860").split(",") if o.strip()]
LOG_DIR = Path(os.environ.get("LOG_DIR", "outputs"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("ai_service")


def status_for(exc: OllamaError) -> int:
    """예외 종류 → HTTP 상태 코드. 원인이 다르면 코드도 달라야 사용자가 조치를 고를 수 있다."""
    if isinstance(exc, OllamaUnavailable):
        return 502
    if isinstance(exc, OllamaModelMissing):
        return 503
    if isinstance(exc, OllamaTimeout):
        return 504
    return 502


def record(entry: dict[str, Any]) -> None:
    """요청 한 건을 outputs/requests.jsonl 에 한 줄로 남긴다(로그와 별개인 구조화 기록)."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with (LOG_DIR / "requests.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": datetime.now().isoformat(timespec="seconds"), **entry}, ensure_ascii=False) + "\n")
    except OSError as exc:
        log.warning("기록 실패: %s", exc)


def ns_to_ms(value: int | None) -> float | None:
    return None if value is None else round(value / 1_000_000, 1)  # Ollama 메타는 나노초다.


def with_system(messages: list[ChatMessage]) -> list[dict[str, str]]:
    """클라이언트가 system 을 보내지 않았으면 서버 기본 system 프롬프트를 앞에 붙인다."""
    out = [m.model_dump() for m in messages]
    if out[0]["role"] != "system":
        out.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
    return out


def sse(event: dict[str, Any]) -> str:
    """Server-Sent Events 한 건: `data: {...}` 한 줄 + 빈 줄."""
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.client = OllamaClient.from_env()
    log.info("모델 서버 %s, 기본 모델 %s", app.state.client.host, app.state.client.model)
    yield
    await app.state.client.aclose()


app = FastAPI(title="오픈소스 AI 응용 — AI 서비스 베타", version=SERVICE_VERSION, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])


def get_client(request: Request) -> OllamaClient:
    """의존성 주입 지점. 13주차에서 테스트용 가짜 클라이언트로 바꿔 끼운다."""
    return request.app.state.client


@app.middleware("http")
async def request_id_and_timing(request: Request, call_next):  # type: ignore[no-untyped-def]
    request.state.request_id = uuid.uuid4().hex[:8]
    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - started) * 1000)  # 스트리밍은 헤더까지의 시간이다.
    response.headers["X-Request-ID"] = request.state.request_id
    log.info("%s %s %s -> %s %dms", request.state.request_id, request.method, request.url.path, response.status_code, elapsed_ms)
    record({"request_id": request.state.request_id, "method": request.method, "path": request.url.path, "status": response.status_code, "elapsed_ms": elapsed_ms})
    return response


@app.exception_handler(OllamaError)
async def ollama_error_handler(request: Request, exc: OllamaError) -> JSONResponse:
    body = ErrorResponse(request_id=request.state.request_id, error=type(exc).__name__, detail=str(exc))
    log.warning("%s %s: %s", body.request_id, body.error, body.detail)
    return JSONResponse(status_code=status_for(exc), content=body.model_dump())


@app.get("/health", response_model=HealthResponse)
async def health(client: OllamaClient = Depends(get_client)) -> HealthResponse:
    """앱 서버가 응답하면 200. 모델 서버 상태는 본문의 status 로 구분한다(ok / degraded)."""
    try:
        models = await client.list_models()
        has_model = client.model in models or f"{client.model}:latest" in models
        ollama = OllamaStatus(host=client.host, reachable=True, model=client.model, has_model=has_model, detail=f"모델 {len(models)}개")
    except OllamaError as exc:
        ollama = OllamaStatus(host=client.host, reachable=False, model=client.model, has_model=False, detail=str(exc))
    overall = "ok" if ollama.reachable and ollama.has_model else "degraded"
    return HealthResponse(status=overall, service=SERVICE_NAME, version=SERVICE_VERSION, ollama=ollama)


ERROR_DOCS = {502: {"model": ErrorResponse}, 503: {"model": ErrorResponse}, 504: {"model": ErrorResponse}}  # /docs 에 실을 오류 형식


@app.post("/chat", response_model=ChatResponse, responses=ERROR_DOCS)
async def chat(body: ChatRequest, request: Request, client: OllamaClient = Depends(get_client)) -> ChatResponse:
    """요청 검증(pydantic) → Ollama 호출 → 응답 메타 포함해 반환."""
    data = await client.chat(with_system(body.messages), model=body.model, temperature=body.temperature, max_tokens=body.max_tokens)
    return ChatResponse(
        request_id=request.state.request_id,
        model=data.get("model", body.model or client.model),
        reply=data.get("message", {}).get("content", ""),
        eval_count=data.get("eval_count"),
        eval_duration_ms=ns_to_ms(data.get("eval_duration")),
        total_duration_ms=ns_to_ms(data.get("total_duration")),
    )


@app.post("/chat/stream", responses=ERROR_DOCS)
async def chat_stream(body: ChatRequest, request: Request, client: OllamaClient = Depends(get_client)) -> StreamingResponse:
    """SSE 스트리밍. 첫 청크를 받은 뒤에야 200 을 확정한다 — 그 전 실패는 502·503·504 로 나간다."""
    stream = client.chat_stream(with_system(body.messages), model=body.model, temperature=body.temperature, max_tokens=body.max_tokens)
    first = await anext(stream)  # 연결 실패·모델 없음·시간 초과는 여기서 OllamaError 로 터져 핸들러가 처리한다.

    async def event_source() -> AsyncIterator[str]:
        try:
            chunk = first
            while True:
                piece = chunk.get("message", {}).get("content", "")
                if piece:
                    yield sse({"delta": piece})
                if chunk.get("done"):
                    yield sse({"done": True, "eval_count": chunk.get("eval_count"), "total_duration_ms": ns_to_ms(chunk.get("total_duration"))})
                    return
                chunk = await anext(stream)
        except OllamaError as exc:
            # 본문이 이미 흐르기 시작하면 상태 코드를 바꿀 수 없다. 오류를 이벤트로 보낸다.
            yield sse({"error": type(exc).__name__, "detail": str(exc), "status": status_for(exc)})

    return StreamingResponse(event_source(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Request-ID": request.state.request_id})


def main() -> None:
    parser = argparse.ArgumentParser(description="앱 서버를 uvicorn 으로 실행한다.")
    parser.add_argument("--host", default=os.environ.get("APP_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("APP_PORT", "8000")))
    parser.add_argument("--reload", action="store_true", help="코드 변경 시 자동 재시작(개발용)")
    args = parser.parse_args()
    import uvicorn

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
