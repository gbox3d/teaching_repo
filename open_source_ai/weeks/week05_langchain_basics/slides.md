---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# 1교시 · 설명 20분
## LangChain 소개와 Ollama 연결

---

## 0–2분 · LLM 앱을 만드는 LangChain

LangChain은 언어 모델을 이용한 앱과 에이전트를 만드는 오픈소스 프레임워크다.

프롬프트 작성, 모델 호출, 응답 처리를 조합하는 구성 요소를 제공한다. 문서 검색이나 외부 도구도 연결할 수 있다.

이번 주에는 **질문을 받아 답하는 터미널 챗봇**으로 기본 연결을 익힌다. 다음 주에는 문서를 찾아 답하는 RAG로 확장한다.

[공식 소개](https://docs.langchain.com/oss/python/langchain/overview) · [구성 요소](https://reference.langchain.com/python/langchain-core)

---

## 2–4분 · 모델·Ollama·LangChain의 역할

| 구성 요소 | 이 수업에서 맡는 일 |
|---|---|
| Qwen 모델 | 입력한 메시지를 바탕으로 답변 생성 |
| Ollama | 내 PC에서 모델을 실행하고 API 제공 |
| LangChain | 프롬프트·모델 호출·응답 처리를 연결 |

`ChatOllama`가 LangChain 코드와 Ollama 서버를 연결한다.
4주차에 준비한 서버와 모델을 그대로 사용한다.

[ChatOllama 공식 안내](https://docs.langchain.com/oss/python/integrations/chat/ollama)

---

## 4–6분 · 호출 앞뒤의 작업을 연결한다

4주차에는 `ollama.chat()`에 메시지를 보내고 응답을 출력했다.
역할·질문 형식을 재사용하고 응답을 가공할 때는 처리 단계를 나누어 연결한다.

```python
chain = prompt | model | StrOutputParser()
```

질문으로 메시지 만들기 → 모델 호출 → 답변 문자열 꺼내기.
역할을 바꿀 때는 프롬프트를 수정하고 나머지 연결은 재사용한다.

2교시에 이 코드를 실행하며 각 단계의 입력과 출력을 확인한다.

---

## 6–8분 · 이번 예제의 두 패키지

| pyproject.toml의 패키지 | 사용하는 구성 요소 |
|---|---|
| `langchain-core` | 프롬프트 템플릿, 메시지, 문자열 출력기 |
| `langchain-ollama` | Ollama를 호출하는 `ChatOllama` |

공식 문서에는 도구를 선택해 실행하는 에이전트도 나온다.
이번 예제는 위 두 패키지로 **직접 정한 순서의 연결**부터 배운다.

[패키지·API 목록](https://reference.langchain.com/python/)

---

## 8–10분 · 한 프로젝트의 세 명령

`uv init --package --python 3.12 --vcs none`으로 구조를 확인한다.

`src/` 패키지의 `main()`을 scripts가 명령으로 연결한다. build-system은 설치 방법이다. `uv sync` 뒤 프로젝트 루트에서 `uv run ex01`을 실행한다.

---

## 10–12분 · 모델 설정은 한곳에 둔다

```python
from shared import create_model
model = create_model()
```

`shared`는 `OLLAMA_MODEL`·`OLLAMA_HOST`를 읽는다. 기본 모델은 4주차 `qwen3.5:2b`다. `reasoning=False`로 생각 출력을 끈다.

이 로컬 예제는 API 키나 외부 추적 서비스 가입 없이 실행한다.

---

## 12–15분 · 메시지를 invoke에 보낸다

```python
response = model.invoke([
    ("system", "한국어로 짧게 답한다."),
    ("human", question),
])
print(response.content)
```

system은 규칙, human은 사용자 질문이다.

---

## 15–18분 · 질문을 반복해서 입력한다

`나>` → 답 → 다음 `나>` 순서다. 빈 줄은 건너뛰고 `/bye`로 종료한다.

`ex01`은 이번 질문만 보낸다. 반복 입력과 대화 기억은 다르며 이력은 3교시에 추가한다.

---

## 18–20분 · 실습 인계

[1교시 실습](lab.md#1교시-실습--ollama-연결)

리스트·튜플을 직접 질문하고 4주차 `ollama.chat()`과 비교한다. 같은 서버·모델인지 확인한다. 실습 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## 프롬프트와 모델 연결

---

## 0–3분 · 바꿀 부분을 변수로 둔다

```text
너는 {role}이다.
{question}
```

역할과 질문을 문자열에 직접 붙이지 않고 프롬프트의 변수로 전달한다.

---

## 3–6분 · 템플릿으로 메시지를 만든다

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 {role}이다. 한국어로 짧게 답한다."),
    ("human", "{question}"),
])
```

키 이름은 invoke의 입력과 맞아야 한다.

---

## 6–9분 · 연결의 세 단계

```python
chain = prompt | model | StrOutputParser()
```

입력 사전 → 메시지 목록 → 모델 응답 → 문자열.

`|`는 앞 단계의 출력을 다음 단계의 입력으로 연결한다.

---

## 9–12분 · 입력 키를 맞춘다

```python
answer = chain.invoke({
    "role": ROLE,
    "question": question,
})
```

예제는 이번 질문만 처리하며 이전 대화를 자동 저장하지 않는다.

---

## 12–16분 · 역할 하나를 바꿔 비교한다

`ROLE`을 비유로 설명하는 Python 선생님으로 바꾸고 같은 질문을 한다.

코드 연결은 유지하고 프롬프트 값만 바꾼다. 두 문장 규칙을 지키지 않았다면 실제 답을 근거로 기록한다.

---

## 16–20분 · 실습 인계

[2교시 실습](lab.md#2교시-실습--프롬프트-연결)

질문 두 개를 입력하고 역할 변경 전후를 비교한다. 세 단계의 입력·출력을 한 문장씩 설명한다. 실습 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 기억하며 스트리밍 대화

---

## 0–3분 · 이력은 프로그램이 보낸다

4주차처럼 앞의 질문과 답을 함께 보내야 문맥이 이어진다.

LangChain을 쓴다는 이유만으로 대화가 장기 저장되지는 않는다. 이번 예제의 `history`는 프로그램 메모리의 목록이다.

---

## 3–6분 · 이력이 들어갈 자리를 만든다

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "한국어로 짧게 답한다."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
```

규칙 → 지난 대화 → 이번 질문 순서다.

---

## 6–9분 · 도착한 답을 바로 출력한다

```python
for part in chain.stream(inputs):
    print(part, end="", flush=True)
    answer += part
```

문자열 출력기를 거친 조각을 출력하면서 전체 답도 모은다.

---

## 9–12분 · 질문과 완성 답을 남긴다

```python
history.extend([
    ("human", question),
    ("ai", answer),
])
```

다음 요청에 이 목록을 보낸다. 프로그램을 새로 시작하면 빈 목록부터 시작한다.

---

## 12–16분 · 이력을 보낸 실행과 비교한다

색을 먼저 알리고 다시 묻는다. 종료 후 `"history": []`로 바꿔 같은 순서를 반복한다.

우연히 답을 맞힌 경우와 실제로 이력을 보낸 경우를 구분한다. 답과 함께 요청 코드를 확인한다.

---

## 16–20분 · 다음 주 검색으로 연결한다

[3교시 실습](lab.md#3교시-실습--대화-기억과-스트리밍)

이번 주는 프롬프트·모델·문자열 출력을 연결한다. 6주차에는 검색 문서를 context에 넣고 출처를 확인한다. 실습 30분 뒤 휴식 10분.
