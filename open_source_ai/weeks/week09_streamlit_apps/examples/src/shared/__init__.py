"""채팅과 문서 검색 앱에서 사용하는 모델·검색 함수."""

import os
from pathlib import Path

import streamlit as st

MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:2b")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.getenv("HF_EMBED_MODEL", "intfloat/multilingual-e5-small")
DOCUMENT = Path(__file__).parent / "data/library.txt"
CHAT_PROMPT = (
    "한국어로 짧게 답한다. 사용자가 사실만 알려 주면 짧게 확인한다. "
    "수량을 물으면 앞선 대화의 수와 변화를 반영해 계산식과 단위를 쓴다."
)


def prepare():
    from sentence_transformers import SentenceTransformer

    SentenceTransformer(EMBED_MODEL)
    print("임베딩 모델 준비 완료:", EMBED_MODEL)


def stream_text(messages):
    from langchain_ollama import ChatOllama

    model = ChatOllama(model=MODEL, base_url=HOST, temperature=0, reasoning=False)
    for part in model.stream(messages):
        if part.text:
            yield part.text


@st.cache_resource
def embedder():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBED_MODEL, local_files_only=True)


@st.cache_data
def document_vectors(chunks):
    return embedder().encode(["passage: " + chunk for chunk in chunks], normalize_embeddings=True)


def retrieve(text, question):
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    if not chunks:
        return []
    vectors = document_vectors(chunks)
    query = embedder().encode(["query: " + question], normalize_embeddings=True)[0]
    scores = vectors @ query
    return [(index + 1, float(scores[index]), chunks[index]) for index in scores.argsort()[::-1][:3]]
