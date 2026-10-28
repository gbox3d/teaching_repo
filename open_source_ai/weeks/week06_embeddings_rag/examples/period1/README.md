# 6주차 1교시 — 문서 분할·임베딩·검색

[공통 준비](../README.md#수업-전-준비)를 마친 **프로젝트 루트**에서 실행한다. 이 폴더에는 교시 안내만 있다.

| 순서 | 소스 | 확인할 것 |
|---|---|---|
| 1 | [ex01_chunk](../src/ex01_chunk/__init__.py) | 문서를 청크로 나누는 크기·겹침·경계 |
| 2 | [ex02_embed](../src/ex02_embed/__init__.py) | 청크 임베딩과 인덱스 저장 |
| 3 | [ex03_search](../src/ex03_search/__init__.py) | 질문 입력과 top-k 출력 |

```powershell
uv run ex01 --size 300 --overlap 50
uv run ex02 --chunks outputs/chunks-300.json
uv run ex03
```

`uv.lock은 왜 커밋하는가`와 `Apache-2.0 라이선스가 MIT와 다른 점은?`를 차례로 입력한다. 빈 줄은 건너뛰고 `/bye`로 종료한다. 질문별 상위 3개 청크의 출처와 본문을 확인한다.

150자 청크와 비교할 때는 다음을 실행한다.

```powershell
uv run ex01 --size 150 --overlap 30
uv run ex02 --chunks outputs/chunks-150.json --out outputs/index-150
uv run ex03 --index outputs/index-150
```

공용 [retrieval.py](../src/shared/retrieval.py)의 `search()`가 질의를 임베딩하고 코사인 유사도로 정렬한다. 두 인덱스는 같은 `outputs/`에 보존하고 다음 교시에도 쓴다.

실습 문제·시간표·완료 조건은 [1교시 실습지](../../lab.md#1교시-실습--문서를-나누고-임베딩으로-찾기)를 따른다.
