"""자료 폴더의 모든 글을 조각으로 나눠 저장하고, 출처를 붙여 답한다."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from shared import DATA_DIR, create_embeddings, create_model

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4
RULES = "자료에서 질문의 답을 찾아 한국어로 짧게 답한다. 자료에 답이 없을 때만 \"자료에 없습니다.\"라고 답한다."


def main():
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    store = InMemoryVectorStore(create_embeddings())
    for path in sorted(DATA_DIR.glob("*.md")):
        chunks = splitter.split_text(path.read_text(encoding="utf-8"))
        store.add_texts(chunks, [{"source": f"{path.name}#{number}"} for number in range(len(chunks))])
        print(f"{path.name}: 조각 {len(chunks)}개")
    prompt = ChatPromptTemplate.from_messages([
        ("system", RULES),
        ("human", "자료:\n{context}\n\n질문: {question}"),
    ])
    chain = prompt | create_model() | StrOutputParser()
    print("자료 폴더의 글에 대해 물어보세요. 종료: /bye")
    while True:
        question = input("나> ").strip()
        if question == "/bye":
            break
        if not question:
            continue
        docs = store.similarity_search(question, k=TOP_K)
        context = "\n\n".join(doc.page_content for doc in docs)
        print("AI>", chain.invoke({"context": context, "question": question}))
        print("[출처]", ", ".join(doc.metadata["source"] for doc in docs))
