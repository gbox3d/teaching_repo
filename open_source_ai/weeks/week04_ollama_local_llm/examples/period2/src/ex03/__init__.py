"""답을 조각으로 받기: uv run python ex03_stream.py"""

import ollama

MODEL = "qwen3.5:2b"

print("질문을 입력하면 답을 조금씩 출력합니다. 이전 대화는 보내지 않습니다. 종료: /bye")
while True:
    text = input("나> ").strip()
    if text == "/bye":
        break
    if not text:
        continue
    print("AI> ", end="", flush=True)
    stream = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": text}],
        think=False,
        stream=True,  # 답이 다 만들어질 때까지 기다리지 않고 도착하는 대로 받는다
    )
    for part in stream:
        print(part.message.content, end="", flush=True)
    print()
