"""Gradio 최소 채팅 UI — 앱 서버의 /chat/stream(기본) 또는 /chat(--no-stream) 에 붙는다.

실행:  uv run python ui/gradio_app.py               # 스트리밍 표시
       uv run python ui/gradio_app.py --no-stream   # 답이 다 만들어진 뒤 한 번에 표시
브라우저: http://localhost:7860

UI 는 모델을 모른다. 앱 서버의 HTTP 계약(스키마·상태 코드)만 안다.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Any

import gradio as gr
import httpx
from dotenv import load_dotenv

load_dotenv()
DEFAULT_API = os.environ.get("API_BASE_URL", "http://localhost:8000")
LOG_DIR = Path(os.environ.get("LOG_DIR", "outputs"))

# 상태 코드별 사용자 안내. 앱 서버의 detail 을 그대로 보여 주되 다음 행동을 덧붙인다.
ERROR_HINTS = {
    422: "요청 형식이 잘못됐다. 빈 메시지나 범위 밖 옵션이 아닌지 확인한다.",
    502: "모델 서버(Ollama)에 연결하지 못했다. Ollama 실행 여부와 OLLAMA_HOST 를 확인한다.",
    503: "요청한 모델이 모델 서버에 없다. `ollama list` 로 이름을 확인한다.",
    504: "모델 서버가 제한 시간 안에 답하지 않았다. 잠시 뒤 다시 시도하거나 max_tokens 를 줄인다.",
}


def to_messages(message: str, history: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Gradio 의 대화 이력(role·content 딕셔너리 목록)을 앱 서버 스키마로 바꾼다."""
    msgs = [{"role": h["role"], "content": h["content"]} for h in history if h.get("role") in ("user", "assistant") and isinstance(h.get("content"), str)]
    msgs.append({"role": "user", "content": message})
    return msgs


def format_error(resp: httpx.Response) -> str:
    try:
        detail = resp.json().get("detail", resp.text[:200])
    except ValueError:
        detail = resp.text[:200]
    hint = ERROR_HINTS.get(resp.status_code, "앱 서버가 예상 밖의 상태 코드를 돌려줬다.")
    return f"[오류 {resp.status_code}] {detail}\n\n{hint}"


def ask_once(api: str, messages: list[dict[str, str]], timeout: float) -> Iterator[str]:
    """POST /chat — 답이 완성될 때까지 아무것도 표시하지 못한다."""
    with httpx.Client(base_url=api, timeout=timeout) as http:
        resp = http.post("/chat", json={"messages": messages})
    if resp.status_code != 200:
        yield format_error(resp)
        return
    yield resp.json()["reply"]


def ask_stream(api: str, messages: list[dict[str, str]], timeout: float) -> Iterator[str]:
    """POST /chat/stream — SSE 의 delta 를 이어 붙이며 누적 문자열을 계속 내보낸다."""
    text = ""
    with httpx.Client(base_url=api, timeout=timeout) as http, http.stream("POST", "/chat/stream", json={"messages": messages}) as resp:
        if resp.status_code != 200:
            resp.read()
            yield format_error(resp)
            return
        for line in resp.iter_lines():
            if not line.startswith("data: "):
                continue
            event = json.loads(line[6:])
            if "delta" in event:
                text += event["delta"]
                yield text
            elif "error" in event:
                yield text + f"\n\n[중단 {event.get('status')}] {event.get('detail')}"
                return
            elif event.get("done"):
                return


def record(entry: dict[str, Any]) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with (LOG_DIR / "ui-turns.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": datetime.now().isoformat(timespec="seconds"), **entry}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def build(api: str, stream: bool, timeout: float) -> gr.ChatInterface:
    mode = "stream" if stream else "once"

    def respond(message: str, history: list[dict[str, Any]]) -> Iterator[str]:
        messages = to_messages(message, history)
        started = time.perf_counter()
        first_ms: int | None = None
        last = ""
        try:
            for last in ask_stream(api, messages, timeout) if stream else ask_once(api, messages, timeout):
                if first_ms is None:
                    first_ms = round((time.perf_counter() - started) * 1000)
                yield last
        except httpx.ConnectError:
            last = f"[연결 실패] 앱 서버 {api} 에 연결할 수 없다. `uv run uvicorn app.main:app --port 8000` 이 실행 중인지 확인한다."
            yield last
        except httpx.TimeoutException:
            last = f"[시간 초과] 앱 서버가 {timeout:g}초 안에 응답하지 않았다."
            yield last
        record({"mode": mode, "prompt": message, "reply_chars": len(last), "first_ms": first_ms, "total_ms": round((time.perf_counter() - started) * 1000), "error": last.startswith("[")})

    # 대화 이력은 role·content 딕셔너리 목록으로만 오간다(옛 tuples 형식과 type 인자는 없어졌다).
    return gr.ChatInterface(
        fn=respond,
        title="오픈소스 AI 응용 · 수업 도우미 (베타)",
        description=f"앱 서버 {api} · 모드 {mode}. 답이 길면 Stop 으로 중단할 수 있다.",
        examples=["uv lock 과 uv sync 의 차이를 한 문장으로.", "MIT 와 Apache-2.0 의 가장 큰 차이는?", "LoRA 의 rank 를 키우면 무엇이 늘어나는가?"],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="앱 서버에 붙는 최소 채팅 UI")
    parser.add_argument("--api", default=DEFAULT_API, help="앱 서버 주소 (기본 API_BASE_URL)")
    parser.add_argument("--port", type=int, default=int(os.environ.get("UI_PORT", "7860")))
    parser.add_argument("--timeout", type=float, default=120.0, help="앱 서버 응답 대기 시간(초)")
    parser.add_argument("--no-stream", action="store_true", help="/chat/stream 대신 /chat 을 쓴다")
    args = parser.parse_args()
    demo = build(args.api, stream=not args.no_stream, timeout=args.timeout)
    # footer_links 에서 "api" 를 빼 API 문서 링크를 숨긴다.
    demo.launch(server_name="127.0.0.1", server_port=args.port, footer_links=["gradio", "settings"])


if __name__ == "__main__":
    main()
