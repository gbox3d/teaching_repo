"""앞의 대화를 함께 보내고 추론이 길어지면 본문을 이어 쓴다."""

from shared import CHAT_PROMPT, EMPTY_ANSWER, create_model
from shared.recovery import answer_with_recovery


def main():
    model = create_model()
    history = []
    print("앞의 질문과 답을 함께 보냅니다. 이력 지우기: /clear, 종료: /bye")
    while True:
        try:
            question = input("나> ").strip()
        except EOFError:
            break
        if question == "/bye":
            break
        if question == "/clear":
            history.clear()
            print("대화를 지웠습니다.")
            continue
        if not question:
            continue
        history.append(("human", question))
        messages = [("system", CHAT_PROMPT), *history]
        answer = answer_with_recovery(model, messages)
        if answer:
            history.append(("ai", answer))
        else:
            print("AI>", EMPTY_ANSWER)
