"""5주차의 ChatOllama로 대화하고, 프롬프트로 답변 형식을 바꿔 본다."""

from langchain_ollama import ChatOllama

from shared import SYSTEM_PROMPT, questions

MODEL = "qwen3.5:2b"  # 마지막 시연에서는 "week07-lora"로 바꾼다.
PROMPT = SYSTEM_PROMPT  # 실습: SYSTEM_PROMPT + " 이름, 소개, 기억할 점을 한 줄씩 답하세요."로 바꾼다.


def main():
    model = ChatOllama(model=MODEL, temperature=0, reasoning=False)
    for question in questions():
        reply = model.invoke([("system", PROMPT), ("human", question)])
        print("AI>", reply.content)
