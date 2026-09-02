"""1교시: 질의를 임베딩해 인덱스에서 코사인 유사도 top-k 청크를 찾는다.

실행: uv run python search.py --query "uv.lock은 왜 커밋하는가" --top-k 3
      uv run python search.py --query "질의1" --query "질의2" --index outputs/index-150
결과: outputs/search-<시각>.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from ragcore import Chunk, Embedder, RagError, cosine_top_k, ensure_outputs, load_index, save_json, timestamp


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


def main() -> int:
    parser = argparse.ArgumentParser(description="임베딩 인덱스에서 top-k 청크를 검색한다.")
    parser.add_argument("--query", action="append", required=True, help="질의(여러 번 지정 가능)")
    parser.add_argument("--index", default="outputs/index", help="embed.py 가 만든 인덱스 stem")
    parser.add_argument("--top-k", type=int, default=3, help="가져올 청크 수")
    parser.add_argument("--device", default=None, help="st 백엔드 장치(cuda, cpu)")
    args = parser.parse_args()

    try:
        meta, chunks, vectors = load_index(Path(args.index))
        # 인덱스를 만든 백엔드·모델과 같은 것으로 질의를 임베딩해야 같은 공간에서 비교된다.
        embedder = Embedder(meta["backend"], args.device)
        if embedder.model_name != meta["model"]:
            raise RagError(f"인덱스 모델({meta['model']})과 현재 설정({embedder.model_name})이 다르다. .env 를 확인한다.")
        results = [{"query": q, "hits": search(embedder, chunks, vectors, q, args.top_k)} for q in args.query]
    except RagError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1

    for item in results:
        print(f"\n질의: {item['query']}")
        print(f"{'순위':<4}{'점수':>8}  {'id':<22}미리보기")
        for h in item["hits"]:
            print(f"{h['rank']:<4}{h['score']:>8.4f}  {h['id']:<22}{preview(h['text'])}")

    out = ensure_outputs() / f"search-{timestamp()}.json"
    save_json(
        out,
        {
            "created": timestamp(),
            "index": str(args.index),
            "backend": meta["backend"],
            "model": meta["model"],
            "chunk_size": meta.get("chunk_size"),
            "overlap": meta.get("overlap"),
            "top_k": args.top_k,
            "results": results,
        },
    )
    print(f"\n저장 → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
