# 5주차 — LangChain 맛보기

4주차의 Ollama 모델을 그대로 사용해 프롬프트와 모델 호출을 연결한다. 이번 주 결과물은 터미널에서 질문하고, 대화를 기억하며, 답을 조금씩 출력하는 프로그램이다.

## 목표와 교시별 결과

| 교시 | 설명·시연 20분 | 실습 30분 | 실행 |
|---|---|---|---|
| 1 | ChatOllama, 메시지와 invoke | 직접 질문 두 개, 4주차 호출과 비교 | `uv run ex01` |
| 2 | 프롬프트 변수, 파이프 연결, 문자열 출력 | 역할을 바꿔 같은 질문 비교 | `uv run ex02` |
| 3 | 대화 이력, MessagesPlaceholder, stream | 앞 질문을 이어서 묻고 스트리밍 관찰 | `uv run ex03` |

각 교시는 설명·시연 20분, 실습 30분, 휴식 10분이다. 에이전트·LangGraph·외부 메모리 저장소는 이번 주 범위에 넣지 않는다.

## 준비와 구조

Ollama와 4주차에 준비한 `qwen3.5:2b`를 사용한다. 유료 API 키와 별도 서비스 가입은 필요 없다. `OLLAMA_MODEL`·`OLLAMA_HOST`는 [shared](examples/src/shared/__init__.py)에서 읽는다.

[실습지](lab.md)대로 `uv init --package --python 3.12 --vcs none week06-skeleton`으로 구조를 확인한 뒤 교재 `examples` 전체를 개인 작업 폴더에 복사한다. 한 uv 프로젝트에서 세 교시를 이어간다. 설치와 모델 준비는 수업 전에 마친다.

각 `src/<모듈>/__init__.py`의 `main()`이 실행 시작점이다. `[project.scripts]`가 명령과 함수를 연결하고 `[build-system]`의 `uv_build`가 패키지를 설치한다. scripts를 바꾸면 `uv sync`를 다시 실행한다.

## 입력과 대화 기억

세 예제 모두 질문을 반복해서 받으며 빈 줄은 건너뛰고 `/bye`로 종료한다. `ex01`·`ex02`는 이번 질문만 보낸다. `ex03`은 앞의 질문과 답을 `history`에 쌓아 함께 보낸다. LangChain을 쓴다는 이유만으로 대화가 자동 저장되는 것은 아니다.

## 자료와 완료 기준

[슬라이드](slides.md) · [실습지](lab.md) · [따라하기](walkthrough.md) · [예제](examples/README.md)

- [ ] ChatOllama가 기존 Ollama 서버를 호출하는 연결이라는 점을 설명했다.
- [ ] 프롬프트의 `role`·`question` 변수와 `invoke` 입력 키를 연결했다.
- [ ] `prompt | model | StrOutputParser()`의 각 단계가 내놓는 값을 설명했다.
- [ ] `ex03`에서 알려 준 수업용 색을 후속 질문으로 확인했다.
- [ ] 이력을 비운 경우와 비교하고, 새 실행에서는 기억이 사라지는 이유를 적었다.
- [ ] 역할을 바꾼 코드와 `week06_note.md`를 개인 저장소에 남겼다.

6주차에는 이번 주 연결의 입력에 검색한 문서를 넣어 출처 있는 RAG 답변기를 만든다. [다음 주 안내](../week06_embeddings_rag/README.md)

## 공식 자료

[ChatOllama](https://docs.langchain.com/oss/python/integrations/chat/ollama) · [LangChain 모델](https://docs.langchain.com/oss/python/langchain/models) · [프롬프트 API](https://reference.langchain.com/python/langchain-core/prompts/)
