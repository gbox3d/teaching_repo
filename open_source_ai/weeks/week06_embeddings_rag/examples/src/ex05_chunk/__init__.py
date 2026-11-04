"""긴 글은 통째로 넣을 수 없으니 조각(청크)으로 나눈 뒤 찾는다."""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from shared import DATA_DIR, create_embeddings

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TOP_K = 3


def main():
    text = (DATA_DIR / "odyssey.md").read_text(encoding="utf-8")
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_text(text)
    print(f"글자 {len(text)}개를 최대 {CHUNK_SIZE}자 조각 {len(chunks)}개로 나눴습니다.")
    for number, chunk in enumerate(chunks[:4]):
        flat = chunk.replace("\n", " ")
        print(f"  조각 {number} ({len(chunk)}자): {flat[:30]} … {flat[-30:]}")
    store = InMemoryVectorStore(create_embeddings())
    store.add_texts(chunks, [{"number": number} for number in range(len(chunks))])
    print("오디세우스의 귀향에 대해 물어보세요. 종료: /bye")
    while True:
        question = input("나> ").strip()
        if question == "/bye":
            break
        if not question:
            continue
        for doc, score in store.similarity_search_with_score(question, k=TOP_K):
            print(f"  {score:.3f}  조각 {doc.metadata['number']}: {doc.page_content[:60]}...")
