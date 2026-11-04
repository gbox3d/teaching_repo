# 6주차 — 임베딩 검색과 RAG

모델이 모르는 글을 찾아서 프롬프트에 넣어 주면, 모델을 바꾸지 않고도 그 글을 근거로 답하게 할 수 있다. 이 방법이 RAG(검색 증강 생성)다. 이번 주 결과물은 그리스·로마 신화 50편을 근거로 출처를 밝히며 답하는 터미널 도우미와, 자기 글을 넣어 쓰는 내 문서 도우미다.

## 목표와 교시별 결과

| 교시 | 설명·시연 20분 | 실습 30분 | 실행 |
|---|---|---|---|
| 1 | 임베딩(문장을 숫자 벡터로), 유사도, 벡터 저장소 검색 | 내 문장의 유사도 보기, 신화 검색과 TOP_K 비교 | `uv run ex01`, `uv run ex02` |
| 2 | 찾은 자료를 프롬프트에 넣는 RAG, 출처와 거부 | 자료 없이 vs 넣고 비교, 규칙 한 줄 바꾸기 | `uv run ex03`, `uv run ex04` |
| 3 | 긴 글을 조각으로 나누기, 조각 크기와 겹침, 내 문서 도우미 | CHUNK_SIZE 비교, 내 글을 자료 폴더에 넣기 | `uv run ex05`, `uv run ex06` |

각 교시는 설명·시연 20분, 실습 30분, 휴식 10분이다. 벡터 데이터베이스 서버, 재순위 모델, 평가셋은 이번 주 범위에 넣지 않는다.

## 준비와 구조

Ollama와 4주차 `qwen3.5:2b`, 임베딩 전용 모델 `bge-m3`를 쓴다. 생성 모델은 답을 만들고 임베딩 모델은 글을 숫자 벡터로 바꾸기만 한다. 두 모델이 `ollama list`에 보여야 하며 다운로드는 수업 전에 마친다.

[실습지](lab.md)대로 `uv init --package --python 3.12 --vcs none my-rag`로 구조를 확인한 뒤 교재 `examples` 전체를 개인 작업 폴더에 복사한다. 한 uv 프로젝트에서 세 교시를 이어간다. 패키지는 5주차의 `langchain-core`·`langchain-ollama`에 `langchain-text-splitters`·`numpy`를 더한 네 개다.

각 `src/<모듈>/__init__.py`의 `main()`이 실행 시작점이다. `[project.scripts]`가 명령과 함수를 연결하고 `[build-system]`의 `uv_build`가 패키지를 설치한다. scripts를 바꾸면 `uv sync`를 다시 실행한다. 모델 설정과 신화 자료는 [shared](examples/src/shared/__init__.py)에 있고, 자료 파일은 `src/shared/data/`에 둔다.

## 자료와 바꿔 보는 값

자료는 수업용으로 새로 쓴 그리스·로마 신화 요약 50편(`myths.md`)과 오디세우스 귀향 이야기 한 편(`odyssey.md`)이다. 신화의 줄거리는 누구나 다시 쓸 수 있어 수업용 요약을 새로 썼다. 번역서의 문장이나 소설처럼 저작권이 있는 글은 교재에 넣지 않으며, 자기 PC에서만 쓰는 글은 3교시 내 문서 도우미에 넣어 볼 수 있다.

예제에 명령행 옵션은 없다. 파일 맨 위의 `TOP_K`, `CHUNK_SIZE`, `RULES` 같은 상수를 고치고 같은 명령을 다시 실행해 비교한다.

## 입력과 검색

여섯 예제 모두 `나>`에서 질문을 반복해 받으며 빈 줄은 건너뛰고 `/bye`로 종료한다. 질문마다 새로 검색하고 이전 대화는 보내지 않는다. 실행할 때마다 처음에 자료를 벡터로 바꾸느라 몇 초 걸린다. 작은 모델은 자료가 있어도 놓치거나, 질문의 표현이 자료와 멀면 검색이 빗나갈 수 있다. 그런 경우도 그대로 기록한다.

## 자료와 완료 기준

[슬라이드](slides.md) · [실습지](lab.md) · [따라하기](walkthrough.md) · [예제](examples/README.md)

- [ ] 문장 하나가 숫자 1024개가 되고, 뜻이 비슷한 문장의 유사도가 더 높다는 것을 실제 값으로 확인했다.
- [ ] 신화 검색에서 `TOP_K`를 바꾼 결과와, 질문의 표현에 따라 1위가 달라진 경우를 적었다.
- [ ] 같은 질문에 대한 자료 없는 답과 자료를 넣은 답을 비교하고 무엇이 달라졌는지 설명했다.
- [ ] 자료에 없는 질문에 도우미가 어떻게 답했는지와 `[출처]` 줄의 점수를 기록했다.
- [ ] `CHUNK_SIZE`를 바꿨을 때 조각 수와 검색 결과가 어떻게 달라졌는지 적었다.
- [ ] 내 글 한 편을 자료 폴더에 넣고 그 글에 대해 질문한 결과와 `week06_note.md`를 개인 저장소에 남겼다.

7주차에는 모델에게 보여 줄 근거를 바꾸는 대신 LoRA로 모델 자체를 조금 바꾼다. [다음 주 안내](../week07_peft_lora/README.md)

## 공식 자료

[LangChain 임베딩](https://docs.langchain.com/oss/python/integrations/text_embedding/ollama) · [벡터 저장소](https://docs.langchain.com/oss/python/langchain/retrieval) · [텍스트 분할기](https://reference.langchain.com/python/langchain-text-splitters/) · [Ollama 임베딩 모델](https://ollama.com/search?c=embedding)
