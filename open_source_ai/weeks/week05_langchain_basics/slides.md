---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 같은 Ollama 모델 연결

---

## 0–3분 · 이미 준비한 모델을 연결한다

4주차 Ollama 서버·모델을 그대로 쓴다. 새 모델을 학습하지 않는다.

`ChatOllama`는 LangChain에서 Ollama를 호출하는 연결이다. API 키나 외부 추적 서비스 가입은 필요 없다.

---

## 3–6분 · 한 프로젝트의 세 명령

`uv init --package --python 3.12 --vcs none`으로 구조를 확인한다.

`src/` 패키지의 `main()`을 scripts가 명령으로 연결한다. build-system은 설치 방법이다. `uv sync` 뒤 프로젝트 루트에서 `uv run ex01`을 실행한다.

---

## 6–9분 · 모델 설정은 한곳에 둔다

```python
from shared import create_model
model = create_model()
```

`shared`는 `OLLAMA_MODEL`·`OLLAMA_HOST`를 읽는다. 기본 모델은 4주차 `qwen3.5:2b`다. `reasoning=False`로 생각 출력을 끈다.

---

## 9–12분 · 메시지를 invoke에 보낸다

```python
response = model.invoke([
    ("system", "한국어로 짧게 답한다."),
    ("human", question),
])
print(response.content)
```

system은 규칙, human은 사용자 질문이다.

---

## 12–16분 · 질문을 반복해서 입력한다

`나>` → 답 → 다음 `나>` 순서다. 빈 줄은 건너뛰고 `/bye`로 종료한다.

`ex01`은 이번 질문만 보낸다. 반복 입력과 대화 기억은 다르며 이력은 3교시에 추가한다.

---

## 16–20분 · 실습 인계

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
