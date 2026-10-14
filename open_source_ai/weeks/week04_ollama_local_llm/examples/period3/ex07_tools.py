"""툴 콜링: 모델이 혼자 못 하는 일을 Python 함수에 맡긴다. uv run python ex07_tools.py"""

from datetime import datetime

import ollama

MODEL = "qwen3.5:2b"  # ollama show 의 Capabilities 에 tools 가 있다


def get_current_time() -> str:
    """지금 날짜와 시각을 알려 준다."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def multiply(a: float, b: float) -> float:
    """두 수를 곱한다.

    Args:
        a: 첫 번째 수
        b: 두 번째 수
    """
    return a * b


TOOLS = {"get_current_time": get_current_time, "multiply": multiply}

messages = []
print("시각이나 곱셈을 물어보세요. 앞의 대화도 함께 보냅니다. 종료: /bye")
while True:
    text = input("나> ").strip()
    if text == "/bye":
        break
    if not text:
        continue
    messages.append({"role": "user", "content": text})

    # 1) 함수 목록을 함께 보낸다. 모델은 답 대신 "이 함수를 이 값으로 불러 달라"는 요청을 돌려준다.
    response = ollama.chat(model=MODEL, messages=messages, tools=list(TOOLS.values()), think=False)
    messages.append(response.message)

    if response.message.tool_calls:
        # 2) 함수를 실제로 실행하는 쪽은 우리 프로그램이다. 결과를 role "tool" 로 돌려준다.
        for call in response.message.tool_calls:
            result = TOOLS[call.function.name](**call.function.arguments)
            print(f"[함수 실행] {call.function.name}({call.function.arguments}) -> {result}")
            messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})

        # 3) 함수 결과까지 담아 다시 물으면 모델이 사람에게 할 답을 만든다.
        response = ollama.chat(model=MODEL, messages=messages, think=False)
        messages.append(response.message)
    print("AI>", response.message.content)
