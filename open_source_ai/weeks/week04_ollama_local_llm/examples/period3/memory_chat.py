"""대화 기억: 메시지 목록을 다시 보내고 JSON에 저장해 다음 실행에서 읽는다.

uv run python memory_chat.py
uv run python memory_chat.py --no-memory --session outputs/no-memory.json
"""

import argparse
import json
import sys
from pathlib import Path

import httpx
from ollama import Client, ResponseError

from config import load_settings

SYSTEM = "한국어로 짧게 답하는 수업 도우미다. 대화에 없는 사용자 정보는 모른다고 말한다."


def load_messages(path: Path, system: str) -> list[dict[str, str]]:
    """처음에는 system만, 재실행할 때는 저장했던 대화를 읽는다."""
    if not path.exists():
        return [{"role": "system", "content": system}]
    messages = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(messages, list) or not messages:
        raise ValueError("대화 파일은 비어 있지 않은 메시지 목록이어야 합니다.")
    for index, message in enumerate(messages):
        role = "system" if index == 0 else ("user" if index % 2 else "assistant")
        if not isinstance(message, dict) or message.get("role") != role or not isinstance(message.get("content"), str):
            raise ValueError("system 다음에 user·assistant가 번갈아 있어야 합니다.")
    if len(messages) % 2 == 0:
        raise ValueError("대화 파일의 마지막 메시지는 assistant여야 합니다.")
    return messages


def save_messages(path: Path, messages: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="대화 기록을 기억하는 Ollama 채팅")
    parser.add_argument("--model", help=".env 또는 기본 모델 대신 사용할 모델")
    parser.add_argument("--host", help="Ollama 서버 주소")
    parser.add_argument("--session", default="outputs/conversation.json", help="대화 저장 파일")
    parser.add_argument("--system", default=SYSTEM, help="새 대화의 규칙. 기존 파일은 저장된 규칙을 사용")
    parser.add_argument("--no-memory", action="store_true", help="이전 대화를 보내지 않는 비교 모드")
    args = parser.parse_args()
    settings = load_settings(host=args.host, model=args.model)
    path = Path(args.session)
    try:
        messages = load_messages(path, args.system)
    except (OSError, ValueError) as exc:
        print(f"대화 파일 읽기 실패: {exc}. 파일을 확인하거나 --session으로 새 파일을 지정하세요.", file=sys.stderr)
        return 1

    client = Client(host=settings.host, timeout=settings.timeout)
    print(f"모델: {settings.model} / 저장 파일: {path}")
    print(f"불러온 대화: {(len(messages) - 1) // 2}회 / 기억: {'끄기' if args.no_memory else '켜기'}")
    print("/bye 종료, /reset 이 파일의 대화 초기화. 저장 파일이 있으면 그 시스템 프롬프트를 사용합니다.")
    while True:
        try:
            text = input("나> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if text == "/bye":
            return 0
        if not text:
            continue
        if text == "/reset":
            reset = [{"role": "system", "content": args.system}]
            try:
                save_messages(path, reset)
            except OSError as exc:
                print(f"초기화 저장 실패: {exc}", file=sys.stderr)
                return 1
            messages = reset
            print("이 파일의 대화를 초기화했습니다.")
            continue

        user = {"role": "user", "content": text}
        # 기억 켜기: 이전 대화 + 이번 질문. 끄기: system + 이번 질문만.
        request = [*messages, user] if not args.no_memory else [messages[0], user]
        print(f"보내는 메시지: {len(request)}개")
        try:
            response = client.chat(model=settings.model, messages=request, think=False)
        except (ConnectionError, httpx.RequestError) as exc:
            print(f"연결 또는 응답 실패: Ollama 실행·서버 주소·제한 시간을 확인하세요. ({exc})", file=sys.stderr)
            return 1
        except ResponseError as exc:
            print(f"Ollama 오류: {exc}. ollama list로 모델 이름을 확인하세요.", file=sys.stderr)
            return 1

        answer = response.message.content or ""
        print(f"AI> {answer}")
        # 모델의 가중치를 바꾸는 것이 아니라 user와 assistant 메시지를 보관한다.
        messages.extend([user, {"role": "assistant", "content": answer}])
        try:
            save_messages(path, messages)
        except OSError as exc:
            print(f"대화 저장 실패: {exc}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
