# 6주차 2교시 — 검색 근거로 답변하기

1교시와 같은 **프로젝트 루트**에서 계속한다. `outputs/index.json`·`index.npy`를 그대로 사용한다.

[ex04_rag](../src/ex04_rag/__init__.py)는 질문 입력 → 검색 → 답변 → 결과 저장 순서다. 프롬프트와 출처 판정은 [shared/generation.py](../src/shared/generation.py)에 있다. Ollama는 `.env`의 `OLLAMA_MODEL`을 실행할 수 있어야 한다.

```powershell
uv run ex04
```

`uv.lock은 왜 커밋하는가`와 `Apache-2.0 라이선스가 MIT와 다른 점은?`를 입력해 출처를 확인한다. 이어서 자료 밖 질문 `LoRA의 rank는 무엇인가`를 입력하고 답을 관찰한다. `/bye`로 종료한다. 질문들은 독립적이며 이전 대화 이력을 보내지 않는다.

조건을 고정해 비교할 때는 기존 옵션을 사용한다.

```powershell
uv run ex04 --query "uv.lock은 왜 커밋하는가" --show-prompt
uv run ex04 --query "LoRA의 rank는 무엇인가" --no-context
uv run ex04 --query "uv.lock은 왜 커밋하는가" --num-ctx 256
```

답변마다 `outputs/rag-*.json`에 질문·검색 출처·답·실제 요청을 저장한다. 출력의 `cited`·`cited_in_retrieved`·`refused`를 확인하고 문서 본문과 대조한다.

실습 문제·시간표·완료 조건은 [2교시 실습지](../../lab.md#2교시-실습--출처-있는-답-생성과-거부-경로)를 따른다.
