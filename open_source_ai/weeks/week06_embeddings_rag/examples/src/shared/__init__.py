"""예제들이 함께 사용하는 모델 설정과 신화 자료."""

import os
from pathlib import Path

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import ChatOllama, OllamaEmbeddings

MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:2b")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "bge-m3")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DATA_DIR = Path(__file__).parent / "data"


def create_model():
    return ChatOllama(model=MODEL, base_url=HOST, temperature=0, reasoning=False)


def create_embeddings():
    return OllamaEmbeddings(model=EMBED_MODEL, base_url=HOST)


def load_myths():
    """myths.md를 '## 제목' 단위로 나눠 (제목, 본문) 목록을 돌려준다."""
    text = (DATA_DIR / "myths.md").read_text(encoding="utf-8")
    myths = []
    for section in text.split("\n## ")[1:]:
        title, body = section.split("\n", 1)
        myths.append((title.strip(), body.strip()))
    return myths


def create_myth_store():
    """신화 전체를 벡터로 저장한 검색 저장소를 만든다. ex02에서 직접 쓴 두 줄과 같다."""
    myths = load_myths()
    store = InMemoryVectorStore(create_embeddings())
    store.add_texts([f"{title}: {body}" for title, body in myths], [{"title": title} for title, _ in myths])
    return store
