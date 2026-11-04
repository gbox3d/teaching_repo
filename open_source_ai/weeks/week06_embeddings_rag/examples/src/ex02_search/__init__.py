"""신화 자료 전체를 벡터로 저장해 두고, 질문과 뜻이 가까운 글을 찾는다."""

from langchain_core.vectorstores import InMemoryVectorStore

from shared import create_embeddings, load_myths

TOP_K = 3


def main():
    myths = load_myths()
    store = InMemoryVectorStore(create_embeddings())
    store.add_texts([f"{title}: {body}" for title, body in myths], [{"title": title} for title, _ in myths])
    print(f"신화 {len(myths)}편을 벡터로 저장했습니다. 질문을 입력하세요. 종료: /bye")
    while True:
        question = input("나> ").strip()
        if question == "/bye":
            break
        if not question:
            continue
        for doc, score in store.similarity_search_with_score(question, k=TOP_K):
            print(f"  {score:.3f}  {doc.page_content[:50]}...")
