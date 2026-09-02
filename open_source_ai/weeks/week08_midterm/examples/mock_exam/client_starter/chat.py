"""모의 실기 B 시작 코드 — 최소 Ollama /api/chat 클라이언트.

`TODO(B-1)` 표시가 있는 곳을 `../tasks_B.md` 의 요구사항에 맞게 완성한다.
이 파일은 고치기 전에도 그대로 실행된다(기본 기능만 있는 상태).

실행: uv run python chat.py --prompt "질문"
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import httpx

from config import Settings, load_settings

OUTPUT_DIR = Path("outputs")


def build_messages(prompt: str, system: str | None = None) -> list[dict[str, str]]:
    """대화 메시지 목록을 만든다."""
    messages: list[dict[str, str]] = []
    # TODO(B-1): system 이 비어 있지 않으면 {"role": "system", "content": system} 을 맨 앞에 넣는다.
    messages.append({"role": "user", "content": prompt})
    return messages


def request_chat(
    settings: Settings, messages: list[dict[str, str]], temperature: float
) -> dict[str, Any]:
    """Ollama /api/chat 을 비스트리밍으로 호출한다."""
    payload = {
        "model": settings.model,
        "messages": messages,
        "stream": False,  # 응답을 하나의 JSON 으로 받는다. True 면 NDJSON 줄 단위
        # Qwen3 계열은 thinking 출력이 답에 섞이므로 끈다. 다른 모델은 이 키를 무시한다.
        "think": False,
        "options": {"temperature": temperature},
    }
    response = httpx.post(f"{settings.host}/api/chat", json=payload, timeout=settings.timeout)
    response.raise_for_status()
    return response.json()


def summarize(
    data: dict[str, Any], prompt: str, system: str | None, settings: Settings
) -> dict[str, Any]:
    """outputs/ 에 저장할 기록을 만든다."""
    record: dict[str, Any] = {
        "model": data.get("model", settings.model),
        "host": settings.host,
        "prompt": prompt,
        "content": data.get("message", {}).get("content", ""),
    }
    # TODO(B-1): 다음 키를 추가한다.
    #   "system": system (없으면 None)
    #   "eval_count", "eval_duration", "total_duration": data 의 값 그대로 (없으면 None)
    #   "tokens_per_sec": eval_count / (eval_duration / 1e9) 를 소수 첫째 자리까지.
    #                     eval_duration 이 0 이거나 없으면 None. (eval_duration 단위는 나노초)
    return record


def save_record(record: dict[str, Any]) -> Path:
    """outputs/chat-<시각>.json 으로 저장하고 경로를 돌려준다."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / f"chat-{time.strftime('%Y%m%d-%H%M%S')}.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="최소 Ollama /api/chat 클라이언트 (모의 실기 B 시작 코드)")
    parser.add_argument("--prompt", required=True, help="사용자 질문")
    parser.add_argument("--model", help="모델 이름 (기본: OLLAMA_MODEL 환경변수)")
    parser.add_argument("--host", help="Ollama 주소 (기본: OLLAMA_HOST 환경변수)")
    parser.add_argument("--temperature", type=float, default=0.2, help="샘플링 온도 (기본 0.2)")
    # TODO(B-1): --system 인자를 추가한다 (기본 None). help 에 용도를 적는다.
    return parser


def main() -> int:
    # Windows 에서 출력이 파이프·파일로 넘어가면 콘솔 인코딩(cp949)이 적용되어 일부 기호에서 예외가 난다.
    # 인코딩은 그대로 두고, 표현할 수 없는 문자만 '?' 로 바꿔 프로그램이 죽지 않게 한다.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    args = build_parser().parse_args()
    settings = load_settings(host=args.host, model=args.model)
    system: str | None = getattr(args, "system", None)
    messages = build_messages(args.prompt, system)

    try:
        data = request_chat(settings, messages, args.temperature)
    except httpx.ConnectError:
        print(f"[오류] Ollama 서버에 연결할 수 없다: {settings.host}", file=sys.stderr)
        print("       `ollama serve` 가 떠 있는지, OLLAMA_HOST 값이 맞는지 확인한다.", file=sys.stderr)
        return 1
    except httpx.TimeoutException:
        print(f"[오류] {settings.timeout}초 안에 응답이 없다. 모델 로딩 중이면 잠시 뒤 다시 실행한다.", file=sys.stderr)
        return 1
    except httpx.HTTPStatusError as exc:
        # 404 는 보통 "model '...' not found" 다. 연결 실패와는 다른 원인이므로 다른 문장으로 알린다.
        if exc.response.status_code == 404:
            print(f"[오류] 모델을 찾을 수 없다: {settings.model}", file=sys.stderr)
            print("       `ollama list` 로 이름과 태그를 확인한다. 수업 중에는 새로 내려받지 않는다.", file=sys.stderr)
        else:
            print(f"[오류] HTTP {exc.response.status_code}: {exc.response.text[:200]}", file=sys.stderr)
        return 1

    print(data.get("message", {}).get("content", ""))
    record = summarize(data, args.prompt, system, settings)
    path = save_record(record)
    print(f"[저장] {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
