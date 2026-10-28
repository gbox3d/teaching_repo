"""1교시: docs/ 아래 문서를 고정 크기 청크로 나눈다.

실행: uv run python chunk.py --docs docs --size 300 --overlap 50
결과: outputs/chunks-300.json  (id, source, start, end, text)

--hard 를 주면 문장 경계를 무시하고 정확히 size 글자마다 자른다(경계 실패 관찰용).
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import asdict
from pathlib import Path

from ragcore import Chunk, RagError, ensure_outputs, save_json, timestamp

# 창의 뒤쪽(size × 0.6 지점 이후)에서만 경계를 찾는다. 너무 앞에서 자르면 청크가 지나치게 짧아진다.
FLOOR_RATIO = 0.6
BOUNDARY_MARKS = ("\n", ". ", "다.", "요.")


def find_cut(window: str, floor: int) -> int:
    """창 안에서 floor 이후에 나오는 마지막 문장·문단 경계 위치(자를 길이)를 돌려준다. 없으면 -1."""
    best = -1
    for mark in BOUNDARY_MARKS:
        pos = window.rfind(mark)
        if pos >= floor:
            best = max(best, pos + len(mark))
    return best


def split_text(text: str, size: int, overlap: int, hard: bool = False) -> list[tuple[int, int, str]]:
    """(start, end, text) 목록. 다음 청크는 end - overlap 에서 시작한다."""
    pieces: list[tuple[int, int, str]] = []
    n, pos = len(text), 0
    while pos < n:
        end = min(pos + size, n)
        if end < n and not hard:
            cut = find_cut(text[pos:end], int(size * FLOOR_RATIO))
            if cut > 0:
                end = pos + cut
        piece = text[pos:end].strip()
        if piece:
            pieces.append((pos, end, piece))
        if end >= n:
            break
        next_pos = end - overlap
        pos = next_pos if next_pos > pos else end  # 항상 앞으로 나아가야 무한 루프가 없다
    return pieces


def chunk_docs(docs_dir: Path, size: int, overlap: int, hard: bool) -> tuple[list[Chunk], list[dict[str, int | str]]]:
    files = sorted(p for p in docs_dir.glob("*.md") if p.is_file())
    if not files:
        raise RagError(f"문서가 없다: {docs_dir}\n  --docs 로 .md 파일이 있는 폴더를 지정한다.")
    chunks: list[Chunk] = []
    summary: list[dict[str, int | str]] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        pieces = split_text(text, size, overlap, hard)
        for i, (start, end, piece) in enumerate(pieces):
            chunks.append(Chunk(id=f"{path.name}#{i}", source=path.name, start=start, end=end, text=piece))
        summary.append({"file": path.name, "chars": len(text), "chunks": len(pieces)})
    return chunks, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="문서를 청크로 분할한다.")
    parser.add_argument("--docs", default="docs", help="문서 폴더(.md)")
    parser.add_argument("--size", type=int, default=300, help="청크 최대 글자 수")
    parser.add_argument("--overlap", type=int, default=50, help="앞 청크와 겹치는 글자 수")
    parser.add_argument("--hard", action="store_true", help="문장 경계를 무시하고 자른다")
    parser.add_argument("--out", default=None, help="결과 JSON 경로(기본 outputs/chunks-<size>.json)")
    args = parser.parse_args()

    if args.size < 50 or not 0 <= args.overlap < args.size:
        print("오류: --size 는 50 이상, --overlap 은 0 이상 size 미만이어야 한다.", file=sys.stderr)
        return 2
    try:
        chunks, summary = chunk_docs(Path(args.docs), args.size, args.overlap, args.hard)
    except RagError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1

    out = Path(args.out) if args.out else ensure_outputs() / f"chunks-{args.size}{'-hard' if args.hard else ''}.json"
    lengths = [len(c.text) for c in chunks]
    record = {
        "created": timestamp(),
        "docs_dir": str(args.docs),
        "size": args.size,
        "overlap": args.overlap,
        "hard": args.hard,
        "files": summary,
        "count": len(chunks),
        "avg_chars": round(sum(lengths) / len(lengths), 1),
        "chunks": [asdict(c) for c in chunks],
    }
    save_json(out, record)

    print(f"{'파일':<22}{'글자':>6}{'청크':>6}")
    for row in summary:
        print(f"{row['file']:<22}{row['chars']:>6}{row['chunks']:>6}")
    print(f"합계 청크 {len(chunks)}개, 평균 {record['avg_chars']}자 → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
