# 특강 2교시: 임베딩 RAG와 검색 관찰

실행 위치는 이 폴더가 아니라 `examples/` 루트다. 1교시에 만든 내 문항과 기록표를 그대로 이어 쓴다.

읽을 파일은 [rag_bot](../src/rag_bot/__init__.py), [ex05_search](../src/ex05_search/__init__.py)이고, 비교할 기준은 14주차 [student_bot](../../../../weeks/week14_chatbot_project/examples/src/student_bot/__init__.py)이다. `rag_bot`은 `student_bot`과 응답 계약·시스템 지시·요청 본문의 값이 같다. 두 파일을 나란히 열어 상수 블록, 검색 함수, `answer()`를 차례로 비교한다.

## 목표

- 낱말 겹침 검색과 bge-m3 임베딩 검색이 문항마다 어떤 문서를 고르는지 비교한다.
- 정답의 근거 문서(`fact_sources`)가 검색 결과에 들었는지로 검색을 평가하고, 답변 점수와 나눠서 본다.
- 기본값 `rag_bot`의 점수를 먼저 재고, `TOP_K`나 `MIN_SCORE` 하나만 바꿔 다시 잰다.

## 6주차 예제와의 대응

| 6주차(LangChain) | rag_bot(urllib) |
|---|---|
| `OllamaEmbeddings(model="bge-m3")` | `EMBED_MODEL`, `embed()`가 `/api/embed`를 부른다 |
| `InMemoryVectorStore.add_texts(...)` | 첫 검색 때 `rank()`가 문서 전체를 한 번 임베딩해 `index`에 둔다 |
| `similarity_search_with_score(질문, k)` | `rank()`가 모든 문서를 코사인 유사도 순으로 돌려주고, `retrieve()`가 `TOP_K`와 `MIN_SCORE`로 자른다 |

LangChain 대신 표준 라이브러리 `urllib`로 쓴 이유는 14주차 `student_bot`과 같은 방식이어야 하기 때문이다. 추가 패키지가 필요 없어 과제 폴더의 `student_bot/__init__.py`에 이 파일 내용을 그대로 옮겨도 돈다.

## 실행

```powershell
uv run ex05
```

`ex05`는 내 문항과 공개 20문항에서 두 봇의 검색 결과를 문항마다 보여 준다. 정답이 있는 문항은 근거 문서를 모두 찾았는지(`포함`, `놓침`)를, 답변 불가 문항은 보낸 문서 수를 출력한다. 임베딩 봇은 가장 가까운 문서의 유사도도 함께 보여 준다. 답변은 만들지 않으므로 생성 모델은 필요 없고 `bge-m3`만 있으면 된다.

참고 자료가 문서 5개뿐이라 `TOP_K` 3이면 두 검색 모두 평가 문항의 근거를 대부분 보낸다. `ex05`의 `SETS`에 `"train"`을 더하면 학습 문항의 검색도 보여 준다.

점수는 1교시 `ex04`의 `BOT`을 `"rag_bot"`으로 바꿔 같은 문항으로 잰다. 먼저 기본값(`TOP_K = 3`, `MIN_SCORE = 0.0`)으로 `mine`과 `public`을 재고, 그다음 상수 하나만 바꿔 다시 잰다. 한쪽 점수만 오른 변경은 채택하지 않는다. `rag_bot`은 답을 만드는 모델과 검색하는 임베딩 모델을 함께 쓰므로, `ex04`의 '기록할 값'에 `qwen3.5:2b`와 `bge-m3` 두 모델 줄이 나온다. 두 줄의 이름과 digest를 모두 기록표에 옮기고, '바꾼 상수' 칸에 `TOP_K`·`MIN_SCORE`와 `ex05` 요약을 적는다.

## 30분 실습 흐름

1. 상수 블록, 검색 함수, `answer()` 순서로 `rag_bot`과 `student_bot`을 비교한다.
2. `uv run ex05`로 두 검색을 비교하고, `SETS`에 `"train"`을 더해 다시 실행한다.
3. `ex04`의 `BOT`을 `"rag_bot"`으로 바꿔(검색 상수는 기본값) `mine`·`public`을 재고 기록표에 두 줄을 적는다.
4. `TOP_K`나 `MIN_SCORE` 하나만 바꿔 `ex05`와 `ex04`를 다시 실행하고 두 줄을 더 적는다.
5. 3교시에 쓸 검색 설정을 하나 정해 `rag_bot`에 남긴다. 정하지 못했으면 기본값으로 되돌린다.

`EMBED_MODEL`은 수업 중에 바꾸지 않는다. 다른 임베딩 모델은 과제를 할 때 수업 밖에서 받은 뒤 바꾸고, 바꾸면 `ex05`·`ex06`·학습을 다시 실행한다. 3교시에 학습 예시를 만든 뒤 검색 설정을 바꾸면 학습 예시와 학습을 다시 만든다.
