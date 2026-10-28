"""검색·RAG·평가가 함께 쓰는 인덱스 로드와 유사도 검색."""

from pathlib import Path
from typing import Any

from shared import Chunk, Embedder, RagError, cosine_top_k, load_index


def load_search_index(stem: Path, device: str | None = None):
    meta, chunks, vectors = load_index(stem)
    embedder = Embedder(meta["backend"], device)
    if embedder.model_name != meta["model"]:
        raise RagError(f"인덱스 모델({meta['model']})과 현재 설정({embedder.model_name})이 다르다. .env 를 확인한다.")
    return meta, chunks, vectors, embedder


def search(embedder: Embedder, chunks: list[Chunk], vectors: Any, query: str, k: int) -> list[dict[str, Any]]:
    """질의 하나의 top-k. rank, id, source, score, text 를 담은 목록."""
    q = embedder.encode([query], kind="query")[0]
    hits = cosine_top_k(vectors, q, k)
    return [
        {"rank": r + 1, "id": chunks[i].id, "source": chunks[i].source, "score": round(s, 4), "text": chunks[i].text}
        for r, (i, s) in enumerate(hits)
    ]


def preview(text: str, width: int = 60) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= width else flat[: width - 1] + "…"
