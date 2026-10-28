"""프롬프트의 변수와 모델, 문자열 출력을 연결한다."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from shared import create_model

ROLE = "초보자용 Python 선생님"


def main():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 {role}이다. 한국어로 두 문장 이내로 답한다."),
        ("human", "{question}"),
    ])
    chain = prompt | create_model() | StrOutputParser()
    print("역할:", ROLE)
    print("이번 질문만 보냅니다. 질문을 입력하세요. 종료: /bye")
    while True:
        question = input("나> ").strip()
        if question == "/bye":
            break
        if not question:
            continue
        answer = chain.invoke({"role": ROLE, "question": question})
        print("AI>", answer)
