"""같은 질문을 자료 없이 묻고, 찾은 자료를 넣어 다시 묻는다. 모델은 그대로다."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from shared import create_model, create_myth_store

TOP_K = 3


def main():
    model = create_model()
    store = create_myth_store()
    plain = ChatPromptTemplate.from_messages([
        ("system", "그리스·로마 신화 질문에 한국어로 세 문장 이내로 답한다."),
        ("human", "{question}"),
    ]) | model | StrOutputParser()
    with_docs = ChatPromptTemplate.from_messages([
        ("system", "자료에서 질문의 답을 찾아 한국어로 세 문장 이내로 답한다. 자료에 답이 없을 때만 \"자료에 없습니다.\"라고 답한다."),
        ("human", "자료:\n{context}\n\n질문: {question}"),
    ]) | model | StrOutputParser()
    print("질문을 입력하면 자료 없는 답과 자료를 넣은 답을 차례로 보여 줍니다. 종료: /bye")
    while True:
        question = input("나> ").strip()
        if question == "/bye":
            break
        if not question:
            continue
        print("자료 없이>", plain.invoke({"question": question}))
        docs = store.similarity_search(question, k=TOP_K)
        context = "\n\n".join(doc.page_content for doc in docs)
        print("자료 넣고>", with_docs.invoke({"context": context, "question": question}))
        print("찾은 자료:", ", ".join(doc.metadata["title"] for doc in docs))
