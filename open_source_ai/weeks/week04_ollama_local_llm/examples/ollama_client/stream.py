"""스트리밍 /api/chat 호출. 조각(NDJSON 한 줄)을 받는 대로 출력하고 마지막 줄의 메타를 기록한다.

실행 예:
    uv run python stream.py --prompt "MIT 라이선스와 GPL의 차이를 표로 정리해 줘."
    uv run python stream.py --prompt "안녕" --num-predict 32 --tag short

종료 코드: 0 성공, 1 기타 오류, 2 연결 실패, 3 모델 없음
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import httpx

from config import load_settings
from ollama_api import EXIT_OK, explain_error, format_metrics, metrics_from, save_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ollama /api/chat 스트리밍 클라이언트")
    parser.add_argument("--prompt", required=True, help="사용자 메시지")
    parser.add_argument("--system", default=None, help="시스템 메시지(역할·제약). 생략 가능")
    parser.add_argument("--model", default=None, help="모델 이름. 생략하면 OLLAMA_MODEL")
    parser.add_argument("--host", default=None, help="서버 주소. 생략하면 OLLAMA_HOST")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--num-ctx", type=int, default=4096)
    parser.add_argument("--num-predict", type=int, default=256)
    parser.add_argument("--tag", default=None, help="출력 파일 이름 뒤에 붙일 짧은 표식")
    parser.add_argument("--outputs", default="outputs")
    return parser


def build_payload(args: argparse.Namespace, model: str) -> dict:
    messages: list[dict[str, str]] = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": args.prompt})
    return {
        "model": model,
        "messages": messages,
        "stream": True,
        # Qwen3 계열의 thinking 텍스트를 끈다. 이유는 chat.py 와 같다.
        "think": False,
        "options": {
            "temperature": args.temperature,
            "num_ctx": args.num_ctx,
            "num_predict": args.num_predict,
        },
    }


def main() -> int:
    args = build_parser().parse_args()
    settings = load_settings(host=args.host, model=args.model)
    payload = build_payload(args, settings.model)
    url = settings.url("/api/chat")

    pieces: list[str] = []
    chunk_count = 0
    first_piece_seconds: float | None = None
    final: dict = {}
    started = time.perf_counter()

    try:
        with httpx.Client(timeout=settings.timeout) as client:
            with client.stream("POST", url, json=payload) as response:
                if response.status_code != 200:
                    response.read()  # 오류 본문(JSON)을 읽어야 메시지를 만들 수 있다
                    response.raise_for_status()
                for line in response.iter_lines():
                    if not line.strip():
                        continue
                    chunk = json.loads(line)
                    if "error" in chunk:
                        raise RuntimeError(chunk["error"])
                    chunk_count += 1
                    piece = str(chunk.get("message", {}).get("content", ""))
                    if piece and first_piece_seconds is None:
                        first_piece_seconds = time.perf_counter() - started
                    print(piece, end="", flush=True)
                    pieces.append(piece)
                    if chunk.get("done"):
                        final = chunk  # 메타는 마지막 줄에만 있다
    except Exception as exc:
        print()  # 조각을 찍던 줄을 정리한다
        code, message = explain_error(exc, settings.host, settings.model)
        print(message, file=sys.stderr)
        return code

    elapsed = time.perf_counter() - started
    metrics = metrics_from(final)
    metrics["chunks"] = chunk_count
    metrics["first_piece_seconds"] = round(first_piece_seconds or 0.0, 3)
    metrics["wall_seconds"] = round(elapsed, 3)

    print()
    print("---")
    print(format_metrics(str(final.get("model", settings.model)), metrics))
    print(f"chunks={chunk_count} first_piece={metrics['first_piece_seconds']}s wall={metrics['wall_seconds']}s")

    record = {
        "endpoint": "/api/chat",
        "host": settings.host,
        "request": payload,
        "answer": "".join(pieces),
        "final_chunk": final,
        "metrics": metrics,
    }
    path = save_json(Path(args.outputs), "stream", args.tag, record)
    print(f"saved: {path}")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
