"""지난 대화를 함께 보내고 도착한 답을 바로 출력한다."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from shared import create_model


def main():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "한국어로 짧게 답한다."),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ])
    chain = prompt | create_model() | StrOutputParser()
    history = []
    print("앞의 질문과 답을 함께 보냅니다. 종료: /bye")
    while True:
        question = input("나> ").strip()
        if question == "/bye":
            break
        if not question:
            continue
        print("AI> ", end="", flush=True)
        answer = ""
        for part in chain.stream({"history": history, "question": question}):
            print(part, end="", flush=True)
            answer += part
        print()
        history.extend([("human", question), ("ai", answer)])
