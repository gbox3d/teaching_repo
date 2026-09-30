"""비스트리밍 /api/chat 호출. 답과 응답 메타를 outputs/chat-*.json 에 남긴다.

실행 예:
    uv run python chat.py --prompt "uv가 무엇인지 두 문장으로 설명해 줘."
    uv run python chat.py --prompt "안녕" --model qwen3:0.6b --temperature 0 --tag t0
    uv run python chat.py --prompt "안녕" --system "한 문장으로만 답한다." --show-request

종료 코드: 0 성공, 1 기타 오류, 2 연결 실패, 3 모델 없음
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import httpx

from config import load_settings
from ollama_api import EXIT_OK, explain_error, format_metrics, metrics_from, save_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ollama /api/chat 비스트리밍 클라이언트")
    parser.add_argument("--prompt", required=True, help="사용자 메시지")
    parser.add_argument("--system", default=None, help="시스템 메시지(역할·제약). 생략 가능")
    parser.add_argument("--model", default=None, help="모델 이름. 생략하면 OLLAMA_MODEL")
    parser.add_argument("--host", default=None, help="서버 주소. 생략하면 OLLAMA_HOST")
    parser.add_argument("--temperature", type=float, default=0.2, help="0이면 결정적, 클수록 다양")
    parser.add_argument("--num-ctx", type=int, default=4096, help="컨텍스트 창 토큰 수")
    parser.add_argument("--num-predict", type=int, default=256, help="최대 생성 토큰 수")
    parser.add_argument("--think", action="store_true", help="thinking 출력을 켠다(기본은 끔)")
    parser.add_argument("--tag", default=None, help="출력 파일 이름 뒤에 붙일 짧은 표식")
    parser.add_argument("--outputs", default="outputs", help="결과 JSON 을 둘 폴더")
    parser.add_argument("--show-request", action="store_true", help="보내는 JSON 을 먼저 출력")
    return parser


def build_payload(args: argparse.Namespace, model: str) -> dict:
    messages: list[dict[str, str]] = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": args.prompt})
    return {
        "model": model,
        "messages": messages,
        "stream": False,
        # Qwen3 계열은 답 앞에 thinking 텍스트를 먼저 만든다. 수업에서는 답만 보고
        # 토큰 수를 비교하기 위해 기본으로 끈다. --think 를 주면 켠다.
        # 기본 모델은 하이브리드라 이 값으로 꺼지지만, 생각 전용 빌드(접미사 없는
        # 4b·30b·235b)는 꺼지지 않는다. 태그 고르는 기준은 weeks/README.md 에 있다.
        "think": bool(args.think),
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

    if args.show_request:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print("---")

    try:
        with httpx.Client(timeout=settings.timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:  # 모든 실패를 사람이 읽을 문장 하나로 바꾼다
        code, message = explain_error(exc, settings.host, settings.model)
        print(message, file=sys.stderr)
        return code

    answer = str(data.get("message", {}).get("content", "")).strip()
    metrics = metrics_from(data)

    print(answer)
    print("---")
    print(format_metrics(str(data.get("model", settings.model)), metrics))

    record = {
        "endpoint": "/api/chat",
        "host": settings.host,
        "request": payload,
        "response": data,
        "metrics": metrics,
    }
    path = save_json(Path(args.outputs), "chat", args.tag, record)
    print(f"saved: {path}")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
