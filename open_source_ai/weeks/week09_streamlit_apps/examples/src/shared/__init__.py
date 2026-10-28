"""앱 실행과 로컬 모델·검색 함수를 모은다."""

import os
from pathlib import Path
import subprocess
import sys

import streamlit as st

MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:2b")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.getenv("HF_EMBED_MODEL", "intfloat/multilingual-e5-small")
DOCUMENT = Path(__file__).parent / "data/library.txt"


def launch(module_file):
    app = Path(module_file).with_name("app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app), *sys.argv[1:]], check=True)


def prepare():
    from sentence_transformers import SentenceTransformer

    SentenceTransformer(EMBED_MODEL)
    print("임베딩 모델 준비 완료:", EMBED_MODEL)


def stream_text(messages):
    from langchain_ollama import ChatOllama

    model = ChatOllama(model=MODEL, base_url=HOST, temperature=0, reasoning=False)
    for part in model.stream(messages):
        yield part.content or ""


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
