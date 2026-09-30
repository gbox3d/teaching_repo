"""mini_rag 공통 모듈: 설정(환경변수 + 기본값), 청크, Ollama 연결 확인, 임베딩 백엔드, 인덱스, 코사인 top-k."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# 모델 이름·주소는 코드에 고정하지 않고 환경변수 + 기본값으로 읽는다.
# 아래 기본값은 교재 검증용이며 실제 값은 학기별 환경 기준표에서 확정한다.
OLLAMA_HOST: str = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL: str = os.environ.get("OLLAMA_MODEL", "qwen3:8b")
OLLAMA_EMBED_MODEL: str = os.environ.get("OLLAMA_EMBED_MODEL", "bge-m3")
HF_EMBED_MODEL: str = os.environ.get("HF_EMBED_MODEL", "intfloat/multilingual-e5-small")
EMBED_BACKEND: str = os.environ.get("EMBED_BACKEND", "st")
OUTPUT_DIR: Path = Path(os.environ.get("RAG_OUTPUT_DIR", "outputs"))
CONNECT_HINT = "Ollama 실행 여부와 .env 의 OLLAMA_HOST 를 확인한다."


class RagError(Exception):
    """사람이 읽을 메시지를 담은 예외. 각 스크립트의 main()이 잡아서 출력한다."""


@dataclass
class Chunk:
    id: str  # "파일명#번호" — 답변의 출처 표시에 그대로 쓴다
    source: str
    start: int
    end: int
    text: str


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def ensure_outputs() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RagError(f"파일이 없다: {path}\n  앞 단계 스크립트(chunk.py → embed.py)를 먼저 실행한다.")
    return json.loads(path.read_text(encoding="utf-8"))


def load_chunks(path: Path) -> list[Chunk]:
    return [Chunk(**c) for c in load_json(path)["chunks"]]


def ollama_post(endpoint: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
    """/api/* POST. 연결 실패·HTTP 오류를 사람이 읽을 RagError 로 바꾼다."""
    try:
        r = httpx.post(f"{OLLAMA_HOST}{endpoint}", json=payload, timeout=timeout)
        r.raise_for_status()
    except httpx.ConnectError as exc:
        raise RagError(f"Ollama 서버에 연결할 수 없다: {OLLAMA_HOST}\n  {CONNECT_HINT}") from exc
    except httpx.HTTPStatusError as exc:
        raise RagError(f"{endpoint} 오류 {exc.response.status_code}: {exc.response.text[:200]}") from exc
    except httpx.HTTPError as exc:
        raise RagError(f"{endpoint} 호출 실패: {exc}") from exc
    return r.json()


def check_ollama_model(model: str) -> None:
    """/api/tags 로 모델 설치 여부를 확인한다. 없으면 설치된 목록과 함께 RagError."""
    try:
        r = httpx.get(f"{OLLAMA_HOST}/api/tags", timeout=10)
        r.raise_for_status()
    except httpx.HTTPError as exc:
        raise RagError(f"Ollama 서버에 연결할 수 없다: {OLLAMA_HOST}\n  {CONNECT_HINT}") from exc
    names = [m.get("name", "") for m in r.json().get("models", [])]
    tagged = model if ":" in model else f"{model}:latest"
    if model not in names and tagged not in names:
        raise RagError(
            f"Ollama에 모델이 없다: {model}\n  설치된 모델: {', '.join(names) or '(없음)'}\n"
            "  수업 전 사전 캐시 목록을 확인한다(실습 중 다운로드 금지)."
        )


class Embedder:
    """텍스트 목록 → 정규화된 float32 행렬(N × dim). st=sentence-transformers(HF_EMBED_MODEL), ollama=/api/embed(OLLAMA_EMBED_MODEL)."""

    def __init__(self, backend: str = EMBED_BACKEND, device: str | None = None) -> None:
        if backend not in ("st", "ollama"):
            raise RagError(f"알 수 없는 백엔드: {backend} (st 또는 ollama)")
        self.backend = backend
        self.device = device or "auto"
        self.model_name = HF_EMBED_MODEL if backend == "st" else OLLAMA_EMBED_MODEL
        self._st_model: Any = None
        if backend == "st":
            self._load_st(device)
        else:
            check_ollama_model(self.model_name)

    def _load_st(self, device: str | None) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RagError("sentence-transformers가 없다. 프로젝트 폴더에서 `uv sync`를 실행한다.") from exc
        try:
            self._st_model = SentenceTransformer(self.model_name, device=device)
        except Exception as exc:  # 모델 ID 오류·캐시 없음·네트워크 없음을 한 메시지로
            raise RagError(
                f"임베딩 모델을 불러올 수 없다: {self.model_name}\n"
                "  - .env 의 HF_EMBED_MODEL 과 사전 캐시 여부를 확인한다.\n"
                "  - 네트워크가 없으면 HF_HUB_OFFLINE=1 로 캐시만 사용한다.\n"
                f"  - 대안: embed.py --backend ollama\n  - 원인: {exc}"
            ) from exc
        self.device = str(self._st_model.device)

    def encode(self, texts: list[str], kind: str = "passage") -> np.ndarray:
        if self.backend == "ollama":
            return self._encode_ollama(texts)
        # e5 계열은 학습 때 "query: " / "passage: " 접두어를 썼으므로 같은 형식으로 넣는다.
        if "e5" in self.model_name.lower():
            texts = [f"{kind}: {t}" for t in texts]
        vec = self._st_model.encode(texts, batch_size=32, convert_to_numpy=True, normalize_embeddings=True)
        return np.asarray(vec, dtype=np.float32)

    def _encode_ollama(self, texts: list[str], batch: int = 16) -> np.ndarray:
        rows: list[list[float]] = []
        for i in range(0, len(texts), batch):
            # /api/embed 는 stream·think 항목이 없는 단발 호출이다. options 만 명시한다.
            payload = {"model": self.model_name, "input": texts[i : i + batch], "options": {}}
            rows.extend(ollama_post("/api/embed", payload, timeout=120)["embeddings"])
        return normalize(np.asarray(rows, dtype=np.float32))


def normalize(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


def save_index(meta: dict[str, Any], chunks: list[Chunk], vectors: np.ndarray, stem: Path) -> tuple[Path, Path]:
    """stem.json(메타 + 청크)과 stem.npy(벡터 행렬) 두 파일로 저장한다."""
    json_path, npy_path = stem.with_suffix(".json"), stem.with_suffix(".npy")
    record = {**meta, "count": len(chunks), "dim": int(vectors.shape[1]), "chunks": [asdict(c) for c in chunks]}
    save_json(json_path, record)
    np.save(npy_path, vectors.astype(np.float32))
    return json_path, npy_path


def load_index(stem: Path) -> tuple[dict[str, Any], list[Chunk], np.ndarray]:
    meta = load_json(stem.with_suffix(".json"))
    npy_path = stem.with_suffix(".npy")
    if not npy_path.exists():
        raise RagError(f"벡터 파일이 없다: {npy_path}\n  embed.py 를 다시 실행한다.")
    vectors = np.load(npy_path)
    chunks = [Chunk(**c) for c in meta["chunks"]]
    if len(chunks) != vectors.shape[0]:
        raise RagError("인덱스 메타의 청크 수와 벡터 수가 다르다. embed.py 를 다시 실행한다.")
    return meta, chunks, vectors


def cosine_top_k(vectors: np.ndarray, query: np.ndarray, k: int) -> list[tuple[int, float]]:
    """정규화된 행렬·벡터의 내적 = 코사인 유사도. 큰 순서로 k개 (index, score)."""
    scores = vectors @ query
    order = np.argsort(-scores)[: max(1, k)]
    return [(int(i), float(scores[i])) for i in order]
