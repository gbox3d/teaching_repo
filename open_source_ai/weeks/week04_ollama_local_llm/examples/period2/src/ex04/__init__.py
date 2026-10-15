"""temperature 비교: uv run python ex04_temperature.py"""

import ollama

MODEL = "qwen3.5:2b"

print("질문마다 temperature 0과 1로 두 번씩 비교합니다. 이전 대화는 보내지 않습니다. 종료: /bye")
while True:
    text = input("나> ").strip()
    if text == "/bye":
        break
    if not text:
        continue
    for temperature in [0, 1.0]:
        for run in [1, 2]:  # 같은 설정으로 두 번씩 물어 답이 같은지 본다
            print(f"[temperature={temperature}, {run}번째]")
            response = ollama.chat(
                model=MODEL,
                messages=[{"role": "user", "content": text}],
                think=False,
                options={"temperature": temperature},  # 0 이면 거의 같은 답, 클수록 다양한 답
            )
            print("AI>", response.message.content)
