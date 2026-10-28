"""2교시: 검색 결과를 근거로 출처가 붙은 답을 반복해서 받는다.

실행: uv run ex04
      uv run ex04 --query "uv.lock은 왜 커밋하는가" --show-prompt
결과: outputs/rag-<시각>.json (질문마다 한 파일)
"""

import argparse
import sys
from pathlib import Path

from shared import OLLAMA_MODEL, RagError, ensure_outputs, read_questions, save_json, timestamp
from shared.generation import answer_question
from shared.retrieval import load_search_index, search


def main() -> int:
    parser = argparse.ArgumentParser(description="검색 결과를 근거로 출처 있는 답을 생성한다.")
    parser.add_argument("--query", action="append", help="질문(생략하면 대화식, 여러 번 지정 가능)")
    parser.add_argument("--index", default="outputs/index", help="ex02 가 만든 인덱스 stem")
    parser.add_argument("--top-k", type=int, default=3, help="프롬프트에 넣을 청크 수")
    parser.add_argument("--model", default=OLLAMA_MODEL, help="생성 모델(OLLAMA_MODEL)")
    parser.add_argument("--num-ctx", type=int, default=4096, help="Ollama options.num_ctx")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--no-context", action="store_true", help="검색을 건너뛰고 질문만 보낸다")
    parser.add_argument("--show-prompt", action="store_true", help="보낸 메시지를 전부 출력한다")
    args = parser.parse_args()

    try:
        meta = {}
        if not args.no_context:
            meta, chunks, vectors, embedder = load_search_index(Path(args.index))
        for question in read_questions(args.query):
            hits = [] if args.no_context else search(embedder, chunks, vectors, question, args.top_k)
            result = answer_question(question, hits, args.model, args.temperature, args.num_ctx)
            if args.show_prompt:
                for message in result["messages"]:
                    print(f"--- {message['role']} ---\n{message['content']}\n")
            print(f"질문: {question}")
            print(f"검색: {[h['id'] for h in hits] or '(컨텍스트 없음)'}")
            print(f"AI> {result['answer']}\n")
            print(f"인용 {result['cited']} · 검색 결과 안의 인용 {result['cited_in_retrieved']} · 거부 {result['refused']}")
            print(f"프롬프트 {result['prompt_chars']}자 · 토큰 {result['meta']}")
            stamp = timestamp()
            out = ensure_outputs() / f"rag-{stamp}.json"
            save_json(out, {"created": stamp, "index": None if args.no_context else str(args.index), "embed": meta.get("model"), **result})
            print(f"저장 → {out}")
    except RagError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1
    return 0
