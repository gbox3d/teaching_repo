"""같은 Ollama 모델을 LangChain의 invoke로 호출한다."""

from shared import create_model


def main():
    model = create_model()
    print("이번 질문만 보냅니다. 질문을 입력하세요. 종료: /bye")
    while True:
        question = input("나> ").strip()
        if question == "/bye":
            break
        if not question:
            continue
        response = model.invoke([
            ("system", "한국어로 짧게 답한다."),
            ("human", question),
        ])
        print("AI>", response.content)
