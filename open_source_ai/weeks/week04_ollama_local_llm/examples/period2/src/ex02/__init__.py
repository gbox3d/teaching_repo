"""같은 질문, 다른 시스템 프롬프트: uv run ex02"""

import ollama

MODEL = "qwen3.5:2b"
SYSTEMS = [
    "너는 초보자용 Python 선생님이다. 한국어로 비유 하나를 들어 두 문장으로 설명한다.",
    "너는 Python 참고서다. 한국어로 짧은 정의와 코드 예 하나를 보여 준다.",
]


def main() -> None:
    print("질문마다 역할별 답을 비교합니다. 이전 대화는 보내지 않습니다. 종료: /bye")
    while True:
        text = input("나> ").strip()
        if text == "/bye":
            break
        if not text:
            continue
        for system in SYSTEMS:
            print("[system]", system)
            response = ollama.chat(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},  # 누구인지, 어떻게 답할지
                    {"role": "user", "content": text},  # 이번에 묻는 것
                ],
                think=False,
            )
            print("AI>", response.message.content)
            print("-" * 40)
