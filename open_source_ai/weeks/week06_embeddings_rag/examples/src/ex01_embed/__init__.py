"""문장을 숫자 벡터(임베딩)로 바꾸고, 뜻이 비슷한 문장이 가까운지 본다."""

import numpy as np

from shared import create_embeddings

SENTENCES = [
    "제우스는 하늘에서 번개를 던진다.",
    "포세이돈은 바다와 지진을 다스린다.",
    "하데스는 죽은 자들의 세계를 지배한다.",
    "학생 식당의 오늘 점심은 김치찌개다.",
    "파이썬 리스트는 대괄호로 만든다.",
]


def cosine(a, b):
    """두 벡터의 방향이 얼마나 같은가. 1에 가까우면 뜻이 비슷하다."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def main():
    embeddings = create_embeddings()
    vectors = embeddings.embed_documents(SENTENCES)
    print(f"문장 하나가 숫자 {len(vectors[0])}개가 됩니다. 첫 문장의 앞 다섯 개: {np.round(vectors[0][:5], 3)}")
    print("기준 문장:")
    for sentence in SENTENCES:
        print(" -", sentence)
    print("문장을 입력하면 기준 문장과의 유사도를 보여 줍니다. 종료: /bye")
    while True:
        question = input("나> ").strip()
        if question == "/bye":
            break
        if not question:
            continue
        query = embeddings.embed_query(question)
        scores = [(cosine(query, vector), sentence) for vector, sentence in zip(vectors, SENTENCES)]
        for score, sentence in sorted(scores, reverse=True):
            print(f"  {score:.3f}  {sentence}")
