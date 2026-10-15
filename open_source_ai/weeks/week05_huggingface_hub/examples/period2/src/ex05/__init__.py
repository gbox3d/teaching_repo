"""텍스트 생성: 4주차와 같은 messages 를 pipeline 에 넣는다. uv run ex05"""

import time

from transformers import pipeline

from shared import TEXT_MODEL, TEXT_REVISION, pick_device

DEVICE = pick_device()  # CPU 와 비교할 때는 "cpu" 로 바꾼다
SYSTEM = "너는 오픈소스 AI 수업의 도우미다. 한국어로 세 문장 이내로 짧게 답한다."


def main() -> None:
    start = time.perf_counter()
    generate = pipeline("text-generation", model=TEXT_MODEL, revision=TEXT_REVISION, device=DEVICE)
    print(f"로드 {time.perf_counter() - start:.1f}초  device={DEVICE}")
    print("질문을 입력하면 답합니다. 이전 대화는 보내지 않습니다. 종료: /bye")
    while True:
        text = input("나> ").strip()
        if text == "/bye":
            break
        if not text:
            continue
        messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}]
        start = time.perf_counter()
        # do_sample=False: 가장 그럴듯한 토큰만 고른다(temperature 0 과 같다)
        output = generate(messages, max_new_tokens=120, do_sample=False)
        answer = output[0]["generated_text"][-1]["content"]  # 마지막 메시지가 모델의 답
        print("AI>", answer)
        print(f"({time.perf_counter() - start:.1f}초)")
