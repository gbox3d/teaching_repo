"""세 예제가 함께 쓰는 모델 설정과 터미널 출력."""

import os
import sys
from time import sleep

from langchain_ollama import ChatOllama

MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:2b")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
REASONING = True
NUM_PREDICT = 128  # 한 요청에서 추론과 본문을 합쳐 생성할 최대 토큰 수
TYPE_DELAY = 0.03  # ex03 터미널에서 본문 한 글자를 표시한 뒤 기다리는 초
CHAT_PROMPT = (
    "한국어로 짧게 답한다. 사용자가 사실만 알려 주면 짧게 확인한다. "
    "수량을 물으면 앞선 대화의 수와 변화를 반영해 계산식과 단위를 쓴다."
)
EMPTY_ANSWER = "모델이 답변 본문을 보내지 않았습니다."


def create_model():
    return ChatOllama(model=MODEL, base_url=HOST, temperature=0, reasoning=REASONING, num_predict=NUM_PREDICT)


def type_text(text):
    if TYPE_DELAY <= 0 or not sys.stdout.isatty():
        print(text, end="", flush=True)
        return
    for char in text:
        print(char, end="", flush=True)
        sleep(TYPE_DELAY)
