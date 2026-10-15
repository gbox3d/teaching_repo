"""이미지 인식: 그림 파일을 함께 보내 묻는다. uv run ex06"""

from pathlib import Path

import ollama

MODEL = "qwen3.5:2b"  # 그림을 읽는 모델(VLM). ollama show 의 Capabilities 에 vision 이 있다
IMAGE = Path(__file__).parent / "error_screen.png"  # 패키지 안의 그림. 내 그림은 r"C:\사진\a.png" 처럼 경로를 적는다


def main() -> None:
    messages = []
    print(f"이미지: {IMAGE.name if isinstance(IMAGE, Path) else IMAGE} — 그림에 대해 이어서 질문하세요. 종료: /bye")
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
