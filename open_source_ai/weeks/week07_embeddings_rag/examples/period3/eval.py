"""3교시: 평가셋으로 retrieval hit rate 와 (선택) 키워드·출처 일치율을 잰다.

실행: uv run python eval.py --evalset evalset.json --top-k 3
      uv run python eval.py --evalset evalset.json --top-k 3 --generate      # Ollama 생성까지
      uv run python eval.py --evalset evalset.json --ids q01,q05 --generate  # 일부 문항만
결과: outputs/eval-<시각>.json, outputs/eval-<시각>.md

hit          : 기대 출처 파일의 청크가 top-k 안에 있는가
keyword_ok   : 생성한 답에 정답 키워드가 하나라도 있는가 (--generate)
source_ok    : 답이 인용한 출처가 기대 출처 파일인가 (--generate)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from rag_answer import answer_question
from ragcore import OLLAMA_MODEL, Embedder, RagError, ensure_outputs, load_index, load_json, save_json, timestamp
from search import search


def evaluate_item(item: dict[str, Any], hits: list[dict[str, Any]], known_sources: set[str]) -> dict[str, Any]:
    expected = item["expected_source"]
    ranks = [h["rank"] for h in hits if h["source"] == expected]
    return {
        "id": item["id"],
        "question": item["question"],
        "expected_source": expected,
        "expected_known": expected in known_sources,  # 평가셋 오타를 잡는다
        "top": [h["id"] for h in hits],
        "hit": bool(ranks),
        "rank": ranks[0] if ranks else None,
        "keywords": item.get("keywords", []),
    }


def add_generation(row: dict[str, Any], hits: list[dict[str, Any]], model: str, num_ctx: int) -> None:
    gen = answer_question(row["question"], hits, model=model, num_ctx=num_ctx)
    matched = [k for k in row["keywords"] if k in gen["answer"]]
    cited_sources = {c.split("#")[0] for c in gen["cited"]}
    row.update(
        answer=gen["answer"],
        cited=gen["cited"],
        refused=gen["refused"],
        matched_keywords=matched,
        keyword_ok=bool(matched),
        source_ok=row["expected_source"] in cited_sources,
    )


def rate(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [r[key] for r in rows if key in r]
    return round(sum(1 for v in values if v) / len(values), 3) if values else None


def to_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    mark = lambda v: "O" if v else "X"  # noqa: E731 — 표에 쓸 짧은 기호
    generated = "keyword_rate" in summary and summary["keyword_rate"] is not None
    head = "| id | 질문 | 기대 출처 | hit | 순위 | top-k |"
    sep = "|---|---|---|:-:|:-:|---|"
    if generated:
        head += " 키워드 | 출처 일치 | 거부 |"
        sep += ":-:|:-:|:-:|"
    lines = [f"# 평가 결과 ({summary['created']})", "", f"- 인덱스: `{summary['index']}` (모델 {summary['embed_model']}, 청크 {summary['chunk_size']}자)", f"- top-k: {summary['top_k']} · 문항 {summary['items']}개", f"- **retrieval hit rate: {summary['hit_rate']}**"]
    if generated:
        lines += [f"- 생성 모델: {summary['gen_model']} · keyword rate: {summary['keyword_rate']} · source match rate: {summary['source_match_rate']}"]
    lines += ["", head, sep]
    for r in rows:
        line = f"| {r['id']} | {r['question']} | {r['expected_source']}{'' if r['expected_known'] else ' (인덱스에 없음)'} | {mark(r['hit'])} | {r['rank'] or '-'} | {', '.join(r['top'])} |"
        if generated:
            line += f" {mark(r.get('keyword_ok'))} | {mark(r.get('source_ok'))} | {mark(r.get('refused'))} |"
        lines.append(line)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="평가셋으로 검색·생성 품질을 잰다.")
    parser.add_argument("--evalset", default="evalset.json", help="평가셋 JSON")
    parser.add_argument("--index", default="outputs/index", help="embed.py 가 만든 인덱스 stem")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--ids", default=None, help="쉼표로 나눈 문항 id (일부만 평가)")
    parser.add_argument("--generate", action="store_true", help="Ollama 로 답을 생성해 키워드·출처도 잰다")
    parser.add_argument("--model", default=OLLAMA_MODEL, help="생성 모델(OLLAMA_MODEL)")
    parser.add_argument("--num-ctx", type=int, default=4096)
    args = parser.parse_args()

    try:
        items = load_json(Path(args.evalset))["items"]
        if args.ids:
            wanted = {s.strip() for s in args.ids.split(",")}
            items = [it for it in items if it["id"] in wanted]
        if not items:
            raise RagError("평가할 문항이 없다. --ids 값과 evalset.json 을 확인한다.")
        meta, chunks, vectors = load_index(Path(args.index))
        embedder = Embedder(meta["backend"])
        known_sources = {c.source for c in chunks}
        rows: list[dict[str, Any]] = []
        for it in items:
            hits = search(embedder, chunks, vectors, it["question"], args.top_k)
            row = evaluate_item(it, hits, known_sources)
            if args.generate:
                add_generation(row, hits, args.model, args.num_ctx)
                print(f"{row['id']} hit={row['hit']} keyword={row['keyword_ok']} source={row['source_ok']} refused={row['refused']}")
            else:
                print(f"{row['id']} hit={row['hit']} rank={row['rank']} top={row['top']}")
            rows.append(row)
    except RagError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1

    stamp = timestamp()
    summary = {
        "created": stamp,
        "index": str(args.index),
        "embed_model": meta["model"],
        "chunk_size": meta.get("chunk_size"),
        "top_k": args.top_k,
        "items": len(rows),
        "hit_rate": rate(rows, "hit"),
        "gen_model": args.model if args.generate else None,
        "keyword_rate": rate(rows, "keyword_ok"),
        "source_match_rate": rate(rows, "source_ok"),
        "unknown_sources": [r["id"] for r in rows if not r["expected_known"]],
    }
    out_dir = ensure_outputs()
    save_json(out_dir / f"eval-{stamp}.json", {**summary, "rows": rows})
    (out_dir / f"eval-{stamp}.md").write_text(to_markdown(rows, summary), encoding="utf-8")

    print(f"\nhit rate {summary['hit_rate']}" + (f" · keyword {summary['keyword_rate']} · source {summary['source_match_rate']}" if args.generate else ""))
    if summary["unknown_sources"]:
        print(f"경고: 인덱스에 없는 기대 출처를 가진 문항 {summary['unknown_sources']} — evalset.json 의 파일명을 확인한다.")
    print(f"저장 → {out_dir / f'eval-{stamp}.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
