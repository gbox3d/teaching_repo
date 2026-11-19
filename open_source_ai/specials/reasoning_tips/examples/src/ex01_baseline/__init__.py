"""본문만 읽으면 추론에 생성 예산을 쓴 요청은 빈 답으로 보인다."""

from shared import CHAT_PROMPT, EMPTY_ANSWER, create_model


def main():
    model = create_model()
    print("이번 질문만 보냅니다. 종료: /bye")
    while True:
        try:
            question = input("나> ").strip()
        except EOFError:
            break
        if question == "/bye":
            break
        if question == "/clear":
            print("이번 질문만 사용하므로 지울 이력이 없습니다.")
            continue
        if not question:
            continue
        reply = model.invoke([("system", CHAT_PROMPT), ("human", question)])
        print("AI>", reply.text if reply.text.strip() else EMPTY_ANSWER)
