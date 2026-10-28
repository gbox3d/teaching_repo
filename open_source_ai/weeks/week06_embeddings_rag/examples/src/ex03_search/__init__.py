"""1교시: 질문을 입력해 인덱스에서 코사인 유사도 top-k 청크를 찾는다.

실행: uv run ex03
      uv run ex03 --query "uv.lock은 왜 커밋하는가" --top-k 3
결과: outputs/search-<시각>.json (한 실행에서 입력한 질문 목록)
"""

import argparse
import sys
from pathlib import Path

from shared import RagError, ensure_outputs, read_questions, save_json, timestamp
from shared.retrieval import load_search_index, preview, search


def main() -> int:
    parser = argparse.ArgumentParser(description="임베딩 인덱스에서 top-k 청크를 검색한다.")
    parser.add_argument("--query", action="append", help="질의(생략하면 대화식, 여러 번 지정 가능)")
    parser.add_argument("--index", default="outputs/index", help="ex02가 만든 인덱스 stem")
    parser.add_argument("--top-k", type=int, default=3, help="가져올 청크 수")
    parser.add_argument("--device", default=None, help="st 백엔드 장치(cuda, cpu)")
    args = parser.parse_args()

    try:
        meta, chunks, vectors, embedder = load_search_index(Path(args.index), args.device)
        results = []
        stamp = timestamp()
        for question in read_questions(args.query):
            hits = search(embedder, chunks, vectors, question, args.top_k)
            results.append({"query": question, "hits": hits})
            print(f"\n질의: {question}")
            print(f"{'순위':<4}{'점수':>8}  {'id':<22}미리보기")
            for h in hits:
                print(f"{h['rank']:<4}{h['score']:>8.4f}  {h['id']:<22}{preview(h['text'])}")
            out = ensure_outputs() / f"search-{stamp}.json"
            save_json(out, {
                "created": stamp, "index": str(args.index),
                "backend": meta["backend"], "model": meta["model"],
                "chunk_size": meta.get("chunk_size"), "overlap": meta.get("overlap"),
                "top_k": args.top_k, "results": results,
            })
            print(f"\n저장 → {out}")
    except RagError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1
    return 0
