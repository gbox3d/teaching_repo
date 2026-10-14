"""첫 질문 보내기: uv run python ex01_hello.py"""

import ollama

MODEL = "qwen3.5:2b"  # ollama list 에 보이는 이름

response = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": "안녕. 한국어로 한 문장만 인사해 줘."}],
    think=False,  # Qwen3.5 의 생각 출력을 끄고 답만 받는다
)
print(response.message.content)
