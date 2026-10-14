"""대화 기억: 앞의 질문과 답을 messages 에 쌓아 함께 보낸다.

uv run python ex05_memory.py   (끝낼 때 /bye)
"""

import ollama

MODEL = "qwen3.5:2b"

messages = [{"role": "system", "content": "한국어로 짧게 답한다."}]

print("앞의 질문과 답을 함께 보내 대화를 이어 갑니다. 종료: /bye")
while True:
    text = input("나> ").strip()
    if text == "/bye":
        break
    if not text:
        continue
    messages.append({"role": "user", "content": text})
    request = messages  # 기억 끄기 비교: [messages[0], messages[-1]] (규칙과 이번 질문만)
    print(f"(보내는 메시지 {len(request)}개)")
    response = ollama.chat(model=MODEL, messages=request, think=False)
    answer = response.message.content
    print("AI>", answer)
    messages.append({"role": "assistant", "content": answer})  # 답도 쌓아야 다음에 기억한다
