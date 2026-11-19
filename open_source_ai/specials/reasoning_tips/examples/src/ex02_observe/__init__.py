"""완성된 응답에서 추론 원문과 본문, 생성 종료 사유를 읽는다."""

from shared import CHAT_PROMPT, EMPTY_ANSWER, create_model


def main():
    model = create_model()
    print("모델의 추론과 답변을 확인합니다. 종료: /bye")
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
        thought = reply.additional_kwargs.get("reasoning_content") or ""
        done_reason = reply.response_metadata.get("done_reason") or "미제공"
        if thought:
            print("추론>", thought)
        print(f"추론 {len(thought)}자 · 본문 {len(reply.text)}자 · 종료 사유: {done_reason}")
        print("AI>", reply.text if reply.text.strip() else EMPTY_ANSWER)
