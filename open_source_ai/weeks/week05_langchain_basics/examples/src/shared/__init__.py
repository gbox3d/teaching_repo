"""예제들이 함께 사용하는 로컬 Ollama 모델 설정."""

import os

from langchain_ollama import ChatOllama

MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:2b")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


def create_model():
    return ChatOllama(model=MODEL, base_url=HOST, temperature=0, reasoning=False)
