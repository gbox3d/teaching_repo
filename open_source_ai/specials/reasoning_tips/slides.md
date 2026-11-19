---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# 팁엔트릭엔 추론
## 입력 → 모델 호출 → 출력부터 읽기

Python · LangChain · Ollama · `qwen3.5:2b`

```powershell
cd open_source_ai/specials/reasoning_tips/examples
uv sync --locked
uv run ex01
```

입력: **딸기 3개에서 두 사람이 1개씩 먹으면 몇 개 남나요?**
`/bye`로 종료한 뒤 `uv run ex02`, `uv run ex03`에서 같은 질문을 입력한다.

---

## ex01 · main에서 완성 응답 받기

`uv run ex01` · `src/ex01_baseline/__init__.py`의 호출 흐름:

```python
model = create_model()
question = input("나> ").strip()
reply = model.invoke([("system", CHAT_PROMPT), ("human", question)])
print("AI>", reply.text if reply.text.strip() else EMPTY_ANSWER)
```

`main()`의 `while`에서 입력을 반복하고 `/bye`이면 끝낸다.
`invoke()`는 완성 응답 한 개를 받는다. `reply.text`는 본문 문자열이다.

이번 질문만 보낸다. 추론은 켜져 있지만 읽지 않는다.
본문이 비면 안내한다. 추론 미처리는 추론을 끄는 것과 다르다.

---

## ex02 · 완성 응답의 상태 확인

`uv run ex02` · `src/ex02_observe/__init__.py`:

```python
reply = model.invoke([("system", CHAT_PROMPT), ("human", question)])
thought = reply.additional_kwargs.get("reasoning_content") or ""
done_reason = reply.response_metadata.get("done_reason") or "미제공"
if thought:
    print("추론>", thought)
```

완성 응답에서 `추론>` 원문 → 글자 수·종료 사유 → `AI>` 본문 순서다.
추론이 비면 원문 출력을 건너뛴다. 실시간 출력은 아니다.

이번 질문만 한 번 보낸다.
`length`는 생성 한도 종료다. 이것만으로 반복을 판정하지 않는다.
ex01·ex02의 `/clear`는 지울 이력이 없다는 안내를 표시한다.

---

## ex03 · 생성 중 제어는 복구 함수에

`uv run ex03` · `src/ex03_recover/__init__.py`의 호출:

```python
from shared.recovery import answer_with_recovery
answer = answer_with_recovery(model, messages)
```

`main()`에서 입력·이력을 다룬다. 함수는 추론·본문을 표시하고 본문 문자열을 반환한다.
상세는 `src/shared/recovery.py`: 생성 중 점검하려고 `model.stream()`을 쓴다.

본문이 오기 전에 추론이 2,048자에 닿거나 같은 문장이 세 번 나오면 요청을 닫는다.
본문 없이 끝나면 모아 둔 추론에서 한 번 이어 쓴다. 추론도 비었으면 원래 메시지를 다시 보낸다.
추론 원문은 두 요청 합계 2,048자까지 표시한다. 이력에는 질문과 최종 답만 남긴다.

조각마다 글자 수와 토큰 수가 달라질 수 있다. [복구 조건과 근거](README.md#ex03--main에서-복구-함수-호출)

---

## 한 글자씩 출력하는 터미널 연출

ex03은 본문 조각이 오면 `shared.type_text()`로 표시한다.
`examples/` 기준 `src/shared/__init__.py`:

```python
TYPE_DELAY = 0.03
```

실제 터미널에서 한 글자씩 출력하고 0.03초씩 기다린다.
`0`이면 지연을 끈다. 비TTY 출력도 조각을 지연 없이 출력한다.

`추론>` 원문은 조각대로 즉시 출력한다. 추론에는 타자 지연을 넣지 않는다.
새 시도의 추론은 새 `추론>` 표지로 구분한다.
타자기 효과는 모델의 추론 속도나 토큰 생성 간격을 뜻하지 않는다.

---

## 같은 질문으로 관찰

ex01·ex02는 독립 질문, ex03은 새 대화에서 표지의 딸기 질문을 보낸다.

| 예제 | 호출 | 적을 내용 |
|---|---|---|
| ex01 | `invoke` | 완성 본문 또는 빈 답변 안내 |
| ex02 | `invoke` | 추론 원문·글자 수·종료 사유 |
| ex03 | `stream` | 추론 조각·복구 안내·본문 출력 |

공통 `NUM_PREDICT=128`은 요청당 추론+본문의 **토큰** 예산이다.
ex03 재요청은 예산을 한 번 더 받는다. 같은 총 예산의 비교가 아니다.
`REASONING=False` 대조는 세 예제 모두 한 번만 요청한다.

정상 응답도 관찰이다. [실행·모의 시험·ex03 이력·출처](README.md)
