"""시스템·사용자 프롬프트 실습. 한 번 실행할 때 한 번만 질문한다."""

import argparse
import json
import sys
from pathlib import Path

import httpx
from ollama import Client, ResponseError

from config import load_settings


def main() -> int:
    parser = argparse.ArgumentParser(description="Ollama Python 라이브러리로 한 번 질문하기")
    parser.add_argument("--prompt", required=True, help="사용자 프롬프트: 이번 질문")
    parser.add_argument("--system", default="한국어로 짧고 쉽게 답한다.", help="시스템 프롬프트: 역할·답변 규칙")
    parser.add_argument("--model", help="모델 이름. 생략하면 .env·환경변수 또는 config.py 기본값")
    parser.add_argument("--host", help="서버 주소. 기본값은 http://localhost:11434")
    parser.add_argument("--output", default="outputs/prompt.json", help="요청과 답을 저장할 JSON 파일")
    args = parser.parse_args()
    settings = load_settings(host=args.host, model=args.model)

    # system에는 대화 전체의 규칙, user에는 지금 묻는 내용을 넣는다.
    messages = [
        {"role": "system", "content": args.system},
        {"role": "user", "content": args.prompt},
    ]
    client = Client(host=settings.host, timeout=settings.timeout)
    try:
        response = client.chat(model=settings.model, messages=messages, think=False)
    except (ConnectionError, httpx.RequestError) as exc:
        print(f"연결 또는 응답 실패: Ollama 실행·서버 주소·제한 시간을 확인하세요. ({exc})", file=sys.stderr)
        return 1
    except ResponseError as exc:
        print(f"Ollama 오류: {exc}. ollama list로 모델 이름을 확인하세요.", file=sys.stderr)
        return 1

    answer = response.message.content or ""
    print(answer)
    record = {"model": settings.model, "messages": messages, "answer": answer}
    try:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"답은 받았지만 파일 저장에 실패했습니다: {exc}", file=sys.stderr)
        return 1
    print(f"저장: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
