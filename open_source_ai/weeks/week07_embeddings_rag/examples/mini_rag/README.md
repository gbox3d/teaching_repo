# mini_rag — 7주차 예제 프로젝트

문서 분할 → 임베딩 인덱스 → 코사인 검색 → 출처 있는 답 생성 → 평가셋 측정까지를 스크립트 다섯 개(`chunk.py`·`embed.py`·`search.py`·`rag_answer.py`·`eval.py`)와 공통 모듈 `ragcore.py`로 나눈 최소 RAG다.
자세한 실행 순서·관찰 지점·대체 경로는 상위 [`../README.md`](../README.md)에 있다.

```powershell
Copy-Item .env.example .env
uv sync
uv run python chunk.py --size 300 --overlap 50
uv run python embed.py --chunks outputs/chunks-300.json
uv run python search.py --query "uv.lock은 왜 커밋하는가" --top-k 3
uv run python rag_answer.py --query "uv.lock은 왜 커밋하는가" --top-k 3
uv run python eval.py --evalset evalset.json --top-k 3
```

- `uv.lock`은 이 저장소에 없다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
- 모델 ID·양자화·용량은 환경 기준표에서 확정하며 `.env.example`의 값은 교재 검증용 기본값이다.
- 실습 시간에 모델을 내려받지 않는다. 임베딩 모델과 생성 모델은 사전 캐시가 전제다.
