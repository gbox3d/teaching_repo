"""응답 계약과 대화 화면. 이 모듈은 평가 정답을 읽지 않는다."""

import json
from pathlib import Path
import sys
import unicodedata

DATA_DIR = Path(__file__).parent / "data"
MAX_ITEMS = 16
MAX_ANSWER_LENGTH = 256
MAX_SOURCE_LENGTH = 128
MAX_QUESTION_LENGTH = 4000

def normalize(text: str) -> str:
    """NFKC, casefold, 공백, 끝의 ASCII 마침표만 정규화한다."""
    return "".join(unicodedata.normalize("NFKC", text).casefold().split()).rstrip(".")


def validate_strings(value: object, name: str, max_length: int) -> list[str]:
    if type(value) is not list or len(value) > MAX_ITEMS:
        raise ValueError(f"{name}: 최대 {MAX_ITEMS}개의 문자열 배열이어야 합니다.")
    for item in value:
        if type(item) is not str or not 1 <= len(item) <= max_length:
            raise ValueError(f"{name}: 각 항목은 1~{max_length}자 문자열이어야 합니다.")
        if not normalize(item):
            raise ValueError(f"{name}: 정규화 후 빈 문자열은 허용하지 않습니다.")
    return value


def validate_response(response: object) -> dict:
    if type(response) is not dict or set(response) != {"answers", "sources", "abstain"}:
        raise ValueError("응답에는 answers, sources, abstain 세 키만 있어야 합니다.")
    if type(response["abstain"]) is not bool:
        raise ValueError("abstain은 true 또는 false여야 합니다. 숫자와 문자열은 허용하지 않습니다.")
    validate_strings(response["answers"], "answers", MAX_ANSWER_LENGTH)
    validate_strings(response["sources"], "sources", MAX_SOURCE_LENGTH)
    return response


def configure_utf8() -> None:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def chat() -> None:
    """두 대화 명령이 동일한 학생 함수를 호출한다. 이전 대화는 보내지 않는다."""
    from student_bot import answer

    configure_utf8()
    print("원광대학교 소개 챗봇입니다. /bye 또는 Ctrl+C로 종료하세요.")
    while True:
        try:
            question = input("나> ").strip()
            if question == "/bye":
                break
            if not question:
                continue
            if len(question) > MAX_QUESTION_LENGTH:
                print(f"질문은 {MAX_QUESTION_LENGTH}자 이내로 입력하세요.")
                continue
            response = validate_response(answer(question))
            print("AI>", json.dumps(response, ensure_ascii=False))
        except (EOFError, KeyboardInterrupt):
            print("\n대화 종료")
            break
        except Exception as exc:
            print(f"응답 오류: {type(exc).__name__}: {exc}")
            print("Ollama 실행 상태와 student_bot의 모델·주소·응답 형식을 확인하세요.")
