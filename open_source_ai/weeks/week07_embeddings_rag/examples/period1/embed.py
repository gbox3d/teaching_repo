"""1교시: 청크 JSON을 읽어 임베딩 인덱스를 만든다.

실행: uv run python embed.py --chunks outputs/chunks-300.json
      uv run python embed.py --chunks outputs/chunks-300.json --backend ollama
결과: outputs/index.json (메타 + 청크) 와 outputs/index.npy (청크 수 × 차원 float32)

--out 은 확장자 없는 stem 이다. --out outputs/index-150 → index-150.json / index-150.npy
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from ragcore import EMBED_BACKEND, Embedder, RagError, ensure_outputs, load_chunks, load_json, save_index, timestamp


def main() -> int:
    parser = argparse.ArgumentParser(description="청크를 임베딩해 인덱스를 저장한다.")
    parser.add_argument("--chunks", default="outputs/chunks-300.json", help="chunk.py 결과 JSON")
    parser.add_argument("--backend", default=EMBED_BACKEND, choices=["st", "ollama"], help="임베딩 백엔드")
    parser.add_argument("--device", default=None, help="st 백엔드 장치(cuda, cpu). 기본은 자동")
    parser.add_argument("--out", default="outputs/index", help="인덱스 stem(확장자 없이)")
    args = parser.parse_args()

    try:
        chunk_meta = load_json(Path(args.chunks))
        chunks = load_chunks(Path(args.chunks))
        if not chunks:
            raise RagError("청크가 0개다. chunk.py 결과를 확인한다.")
        print(f"청크 {len(chunks)}개 로드 ← {args.chunks}")
        started = time.perf_counter()
        embedder = Embedder(args.backend, args.device)
        loaded = time.perf_counter()
        vectors = embedder.encode([c.text for c in chunks], kind="passage")
        finished = time.perf_counter()
    except RagError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1

    ensure_outputs()
    meta = {
        "created": timestamp(),
        "backend": embedder.backend,
        "model": embedder.model_name,
        "device": embedder.device,
        "chunks_file": str(args.chunks),
        "chunk_size": chunk_meta.get("size"),
        "overlap": chunk_meta.get("overlap"),
        "hard": chunk_meta.get("hard", False),
        "load_sec": round(loaded - started, 2),
        "encode_sec": round(finished - loaded, 2),
    }
    json_path, npy_path = save_index(meta, chunks, vectors, Path(args.out))

    print(f"백엔드 {meta['backend']} · 모델 {meta['model']} · 장치 {meta['device']}")
    print(f"벡터 {vectors.shape[0]} × {vectors.shape[1]} · 모델 로드 {meta['load_sec']}s · 인코딩 {meta['encode_sec']}s")
    print(f"저장 → {json_path}, {npy_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
