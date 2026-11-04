"""찾은 자료를 근거로 답하고 출처를 보여 주는 신화 도우미."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from shared import create_model, create_myth_store

TOP_K = 3
RULES = "너는 그리스·로마 신화 안내자다. 자료에서 질문의 답을 찾아 한국어로 짧게 답한다. 자료에 답이 없을 때만 \"자료에 없습니다.\"라고 답한다."


def main():
    store = create_myth_store()
    prompt = ChatPromptTemplate.from_messages([
        ("system", RULES),
        ("human", "자료:\n{context}\n\n질문: {question}"),
    ])
    chain = prompt | create_model() | StrOutputParser()
    print("신화에 대해 물어보세요. 자료에 없는 내용도 물어보세요. 종료: /bye")
    while True:
        question = input("나> ").strip()
        if question == "/bye":
            break
        if not question:
            continue
        hits = store.similarity_search_with_score(question, k=TOP_K)
        context = "\n\n".join(doc.page_content for doc, _ in hits)
        print("AI>", chain.invoke({"context": context, "question": question}))
        print("[출처]", " / ".join(f"{doc.metadata['title']} {score:.2f}" for doc, score in hits))
