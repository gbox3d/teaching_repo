"""Ollama REST API 공통 도우미 — 오류 문장, 메타 계산, 결과 저장.

chat.py 와 stream.py 가 같이 쓴다. 이 파일은 직접 실행하지 않는다.

- 요청 JSON 에는 stream·think·options 를 항상 명시한다(각 스크립트가 만든다).
- 연결 실패·모델 없음을 사람이 읽을 문장과 종료 코드로 바꾼다.
- 응답 메타(eval_count, eval_duration …)에서 tokens/s 를 계산한다.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_CONNECT = 2  # 서버에 연결할 수 없음
EXIT_MODEL = 3  # 모델 이름을 찾을 수 없음(HTTP 404)

NS_PER_SECOND = 1_000_000_000


def _error_text(response: httpx.Response) -> str:
    """Ollama 는 오류를 {"error": "..."} JSON 으로 돌려준다. 본문이 비었으면 상태 문구를 쓴다."""
    try:
        body = response.json()
        if isinstance(body, dict) and "error" in body:
            return str(body["error"])
    except (json.JSONDecodeError, ValueError):
        pass
    text = response.text.strip()
    return text[:200] if text else response.reason_phrase


def explain_error(exc: Exception, host: str, model: str) -> tuple[int, str]:
    """예외를 (종료 코드, 사람이 읽을 메시지) 로 바꾼다. 스택 트레이스를 보여 주지 않는다."""
    if isinstance(exc, httpx.ConnectError):
        return EXIT_CONNECT, (
            f"[연결 실패] {host} 에 접속할 수 없다. "
            "Ollama 서버가 켜져 있는지(트레이 아이콘 또는 `ollama serve`), "
            "OLLAMA_HOST 값과 포트가 맞는지 확인한다."
        )
    if isinstance(exc, httpx.TimeoutException):
        return EXIT_ERROR, (
            "[시간 초과] 서버가 제한 시간 안에 응답하지 않았다. "
            "첫 호출은 모델 로드가 포함되므로 OLLAMA_TIMEOUT 을 늘리거나 "
            "`ollama ps` 로 모델이 GPU 에 올라갔는지 확인한다."
        )
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        detail = _error_text(exc.response)
        if status == 404:
            return EXIT_MODEL, (
                f"[모델 없음] '{model}' 을(를) 서버에서 찾을 수 없다. "
                f"`ollama list` 로 정확한 이름:태그 를 확인한다. 서버 응답: {detail}"
            )
        return EXIT_ERROR, f"[HTTP {status}] 서버가 요청을 거절했다. 서버 응답: {detail}"
    if isinstance(exc, httpx.HTTPError):
        return EXIT_ERROR, f"[HTTP 오류] {type(exc).__name__}: {exc}"
    return EXIT_ERROR, f"[오류] {type(exc).__name__}: {exc}"


def metrics_from(meta: dict[str, Any]) -> dict[str, Any]:
    """응답(또는 스트리밍 마지막 줄)의 메타에서 사람이 보는 지표를 계산한다.

    duration 값은 모두 나노초다. tokens/s = eval_count / (eval_duration / 1e9).
    """
    eval_count = int(meta.get("eval_count", 0) or 0)
    eval_ns = int(meta.get("eval_duration", 0) or 0)
    prompt_count = int(meta.get("prompt_eval_count", 0) or 0)
    prompt_ns = int(meta.get("prompt_eval_duration", 0) or 0)
    load_ns = int(meta.get("load_duration", 0) or 0)
    total_ns = int(meta.get("total_duration", 0) or 0)
    tokens_per_second = eval_count / (eval_ns / NS_PER_SECOND) if eval_ns > 0 else 0.0
    return {
        "prompt_eval_count": prompt_count,
        "eval_count": eval_count,
        "prompt_eval_seconds": round(prompt_ns / NS_PER_SECOND, 3),
        "eval_seconds": round(eval_ns / NS_PER_SECOND, 3),
        "load_seconds": round(load_ns / NS_PER_SECOND, 3),
        "total_seconds": round(total_ns / NS_PER_SECOND, 3),
        "tokens_per_second": round(tokens_per_second, 2),
        "done_reason": meta.get("done_reason"),
    }


def format_metrics(model: str, metrics: dict[str, Any]) -> str:
    """터미널에 한 줄로 보여 줄 요약."""
    return (
        f"model={model} prompt_tokens={metrics['prompt_eval_count']} "
        f"eval_tokens={metrics['eval_count']} tokens/s={metrics['tokens_per_second']} "
        f"load={metrics['load_seconds']}s total={metrics['total_seconds']}s "
        f"done_reason={metrics['done_reason']}"
    )


def save_json(outputs_dir: Path, prefix: str, tag: str | None, record: dict[str, Any]) -> Path:
    """outputs/<prefix>-<날짜시각>[-<tag>].json 으로 저장하고 경로를 돌려준다."""
    outputs_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    name = f"{prefix}-{stamp}" + (f"-{tag}" if tag else "") + ".json"
    path = outputs_dir / name
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
