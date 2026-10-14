"""이미지 인식: 그림 파일을 함께 보내 묻는다. uv run python ex06_vision.py"""

import ollama

MODEL = "qwen3.5:2b"  # 그림을 읽는 모델(VLM). ollama show 의 Capabilities 에 vision 이 있다
IMAGE = "error_screen.png"  # 자기 사진·화면 캡처로 바꿔 본다

messages = []
print(f"이미지: {IMAGE} — 그림에 대해 이어서 질문하세요. 종료: /bye")
while True:
    text = input("나> ").strip()
    if text == "/bye":
        break
    if not text:
        continue
    message = {"role": "user", "content": text}
    if not messages:
        message["images"] = [IMAGE]
    messages.append(message)
    response = ollama.chat(model=MODEL, messages=messages, think=False)
    print("AI>", response.message.content)
    messages.append(response.message)
