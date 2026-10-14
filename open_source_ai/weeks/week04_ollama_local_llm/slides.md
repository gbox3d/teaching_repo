---
marp: true
theme: default
paginate: true
header: "오픈소스 AI 응용 · 4주차"
footer: "Ollama와 로컬 LLM"
---

# 4주차
## Ollama와 로컬 LLM

**60분 블록 × 3**<br>
매 블록 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분

---

## 이번 주 세 블록

| 교시 | 설명·시연 20분 | 직접 해결 실습 30분 |
|---|---|---|
| 1교시 | 모델은 어떻게 실행되는가 | 터미널에서 모델 실행하고 숫자 읽기 |
| 2교시 | Python 라이브러리로 대화하기 | `ex01`~`ex05` 실행하고 바꿔 보기 |
| 3교시 | 이미지 인식과 툴 콜링, Modelfile | `ex06`·`ex07`, 함수 추가, 내 도우미 모델 |

이번 주 질문: **공개된 오픈소스 모델을 내 PC에서 돌리고, 내 프로그램에서 가져다 쓰려면 무엇이 필요한가?**

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 모델은 어떻게 실행되는가

---

## 0–3분 · 오늘은 만들지 않고 가져다 쓴다

| 무엇 | 오픈소스 | 라이선스 |
|---|---|---|
| 모델을 돌리는 프로그램 | Ollama | MIT |
| 모델(가중치) | Qwen3.5 2B | Apache-2.0 |
| Python에서 부르는 도구 | `ollama` 라이브러리 | MIT |

- 모델은 **수업 전에 받아 둔다**(`ollama pull qwen3.5:2b`, 약 2.7 GB).
- 서버·HTTP·오류 처리는 직접 짜지 않는다. 남이 만들어 공개한 것을 **읽고, 돌리고, 바꿔 본다.**

**질문:** "모델을 실행한다"고 할 때 디스크에서 메모리로 올라가는 것은 정확히 무엇인가?

---

## 3–6분 · LLM 실행 구조 세 조각

```text
텍스트 ─ 토크나이저 ─▶ 토큰 ID ─▶ [가중치 × 컨텍스트] ─▶ 다음 토큰 확률 ─▶ 토큰 하나
                                        ▲                                  │
                                        └──────── 이어 붙여 반복 ──────────┘
```

| 조각 | 무엇 | 크기를 정하는 것 |
|---|---|---|
| 가중치 | 학습된 숫자 행렬 | 파라미터 수 × 파라미터당 바이트 |
| 토크나이저 | 텍스트↔토큰 ID 변환표 | 어휘 크기 |
| 컨텍스트 | 지금까지의 토큰과 계산 캐시 | 대화 길이 |

생성은 **토큰 하나씩 반복**이다. 그래서 속도 단위가 tokens/s다.

---

## 6–9분 · 양자화: 같은 모델, 다른 바이트

| 태그 | 파라미터당 바이트 | `qwen3.5:2b` 받는 크기 |
|---|---:|---:|
| `2b-bf16` | 2 | 4.6 GB |
| `2b` = `2b-q8_0` | 약 1 | 2.7 GB |
| `2b-q4_K_M` | 약 0.6 | 2.0 GB |

- 숫자를 덜 정밀하게 저장할수록 작고 빨라지며 **답의 품질은 조금 떨어진다.**
- 이 모델의 파일에는 그림을 읽는 부분(projector)도 함께 들어 있다(3교시).

**질문:** `ollama list`의 SIZE와 `ollama ps`의 SIZE가 다르다면 무엇이 더해진 것인가?

---

## 9–12분 · 파라미터 수 → 메모리 어림

```text
필요 메모리 ≈ 가중치 크기 + 컨텍스트 + 여유
```

| 모델 (Qwen3.5) | 받는 크기 | 8 GB GPU에서 |
|---|---:|---|
| `0.8b` | 1.3 GB | 여유. CPU로도 쓸 만함 |
| `2b` | 2.7 GB | 여유. **이번 주 모델** |
| `4b` | 3.3 GB | 여유 |
| `9b` | 6.6 GB | 빠듯함 |
| `27b` | 17.5 GB | 불가. CPU 분담 → 매우 느림 |

숫자는 어림값이고 **실측은 `ollama ps`가 한다.**

---

## 12–15분 · Ollama의 네 부분

```text
Ollama 서버 (:11434) ◀── ollama run/show/ps/list   (터미널, 1교시)
        │            ◀── Python ollama 라이브러리   (내 프로그램, 2·3교시)
        ├─ 모델 저장소  %USERPROFILE%\.ollama\models
        └─ Modelfile → ollama create               (3교시)
```

- 터미널 명령도, Python 라이브러리도 같은 서버에 묻는 **손님**이다. 서버가 꺼지면 둘 다 안 된다.
- Windows에서는 Ollama 앱이 켜져 있으면 서버도 켜져 있다.
- 모델 이름 규칙은 `이름:태그`(`qwen3.5:2b`). 태그가 크기·양자화를 뜻한다.

---

## 15–17분 · 오늘 쓰는 명령 다섯 개

```powershell
ollama list                            # 받아 둔 모델과 파일 크기
ollama show qwen3.5:2b                 # 파라미터·양자화·Capabilities
ollama run qwen3.5:2b --think=false    # 대화. /set verbose 로 속도 표시, /bye 로 종료
ollama ps                              # 메모리에 올라간 모델, SIZE, GPU/CPU
ollama pull qwen3.5:2b                 # 다운로드 — 수업 전에 한 번만
```

- `--think=false`: 답 전에 늘어놓는 생각 출력을 끈다.
- 첫 답이 늦은 것은 모델을 메모리에 올리는 **로드 시간**이다. 두 번째부터는 빠르다.

---

## 17–20분 · 실습 인계

[1교시 실습 — 터미널에서 모델 실행하고 숫자 읽기](lab.md#1교시-실습--터미널에서-모델-실행하고-숫자-읽기) · [1교시 안내](examples/period1/README.md)

완료 조건:

1. `ollama show`에서 파라미터 수·양자화·Capabilities를 옮겨 적었다.
2. `/set verbose`의 eval rate와 `ollama ps`의 SIZE·PROCESSOR를 적었다.
3. `ollama list`의 SIZE와 `ollama ps`의 SIZE가 다른 이유를 한 문장으로 적었다.

실습 30분 뒤 휴식 10분. 휴식 후 2교시.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## Python 라이브러리로 대화하기

---

## 0–3분 · 첫 질문은 한 줄

```python
import ollama

MODEL = "qwen3.5:2b"

response = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": "안녕. 한국어로 한 문장만 인사해 줘."}],
    think=False,
)
print(response.message.content)
```

- 서버 주소, 요청 형식, 응답 해석은 **라이브러리가 한다.** 우리는 `ollama.chat()`만 부른다.
- 서버가 꺼져 있으면 라이브러리가 `Failed to connect to Ollama`라고 알려 준다.

---

## 3–6분 · 메시지 세 가지 역할

| `role` | 누구의 말 | 예 |
|---|---|---|
| `system` | 도우미의 역할과 답변 규칙 | "초보자용 Python 선생님. 비유 하나로 두 문장." |
| `user` | 사용자가 지금 묻는 것 | "리스트가 무엇이야?" |
| `assistant` | 모델이 앞서 한 답 | "리스트는 여러 값을 순서대로 담는…" |

`ex02_system_prompt.py`: `나>`에 입력한 **같은 질문에 system만 바꿔** 답을 비교한다. 답을 받은 뒤 다음 질문을 입력하고 `/bye`로 종료한다.

**질문:** system에 "두 문장으로"라고 적었는데 다섯 문장이 나왔다. 무엇을 알 수 있는가?

---

## 6–9분 · 스트리밍: 도착하는 대로 보여 주기

```python
stream = ollama.chat(model=MODEL, messages=[...], think=False, stream=True)
for part in stream:
    print(part.message.content, end="", flush=True)
```

- `stream=True`이면 답이 다 만들어질 때까지 기다리지 않고 **조각**이 차례로 온다.
- 챗봇 화면에서 글자가 흘러나오는 것이 이것이다. 전체 시간은 같아도 **기다리는 느낌**이 줄어든다.
- `ex03_stream.py`: `나>`에 질문 → 조각별 출력 → 다음 질문. 종료는 `/bye`.

---

## 9–12분 · options와 think

```python
ollama.chat(model=MODEL, messages=[...], think=False,
            options={"temperature": 0})
```

| 키 | 뜻 |
|---|---|
| `temperature` | 0이면 가장 그럴듯한 답만, 클수록 다양한 답 |
| `num_predict` | 답의 최대 길이(토큰 수) |
| `think` | `False`면 생각 출력 없이 답만 받는다 |

`ex04_temperature.py`: `나>`에 입력한 질문을 temperature 0과 1로 **두 번씩** 묻고 다음 입력을 기다린다. 종료는 `/bye`.

**질문:** 시험 문제 채점 도우미와 소설 아이디어 도우미에는 각각 어떤 temperature가 맞는가?

---

## 12–15분 · 기억 = 메시지를 쌓아 다시 보내기

```python
messages = [{"role": "system", "content": "한국어로 짧게 답한다."}]
while True:
    messages.append({"role": "user", "content": input("나> ")})
    response = ollama.chat(model=MODEL, messages=messages, think=False)
    messages.append({"role": "assistant", "content": response.message.content})
```

- `ex02`~`ex04`는 입력을 반복해도 이번 질문만 보낸다. `ex05`는 지난 질문·답도 함께 보내며 `/bye`로 종료한다.
- 대화가 길어지면 컨텍스트가 커지고 결국 한계를 넘는다. 긴 자료를 다루는 법은 7주차 RAG.

---

## 15–17분 · 응답 안의 숫자

```python
response.message.content   # 답
response.eval_count        # 만든 토큰 수
response.eval_duration     # 만드는 데 걸린 시간(나노초)
```

```text
tokens/s = eval_count ÷ (eval_duration ÷ 1e9)
```

1교시 `/set verbose`의 eval rate와 같은 값이다. 터미널과 Python이 **같은 서버의 같은 숫자**를 본다.

---

## 17–20분 · 실습 인계

[2교시 실습 — Python에서 대화하기](lab.md#2교시-실습--python에서-대화하기) · [2교시 예제](examples/period2/README.md)

완료 조건:

1. `ex02_system_prompt.py`에 내 역할을 추가하고 답의 차이를 적었다.
2. temperature 0과 1의 차이를 한 문장으로 적었다.
3. 기억 켜기·끄기의 "보내는 메시지" 개수와 답을 비교했다.

실습 30분 뒤 휴식 10분. 휴식 후 3교시.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 이미지 인식과 툴 콜링, Modelfile

---

## 0–3분 · 이 모델이 할 줄 아는 것

```text
ollama show qwen3.5:2b

  Capabilities
    completion     글로 답하기
    vision         그림 읽기
    thinking       생각 과정 출력
    tools          함수 불러 달라고 요청하기
```

- 2교시는 `completion`만 썼다. 3교시는 **`vision`과 `tools`**를 쓴다.
- 모델마다 Capabilities가 다르다. 쓰기 전에 `ollama show`로 확인한다.

---

## 3–6분 · 이미지 인식: 그림을 메시지에 붙인다

```python
response = ollama.chat(
    model=MODEL,
    messages=[{
        "role": "user",
        "content": "이 화면의 마지막 오류 줄을 그대로 옮겨 적고, 무슨 뜻인지 한 문장으로 설명해 줘.",
        "images": ["error_screen.png"],
    }],
    think=False,
)
```

- 글과 그림을 함께 읽는 모델을 **VLM**(Vision Language Model)이라 한다.
- `ex06`은 `나>`의 첫 질문에 이미지를 붙이고, 다음 질문에는 그 대화 이력도 함께 보낸다. 종료는 `/bye`.

---

## 6–9분 · VLM이 잘하는 것과 조심할 것

| 잘하는 것 | 조심할 것 |
|---|---|
| 화면·사진 속 글자 옮기기 | 작은 글씨, 손글씨 |
| 무엇이 찍혔는지 설명하기 | 개수 세기, 위치 비교 |
| 표·그래프 내용 요약 | 그림에 없는 내용을 지어내기 |

시연: 오류 화면을 보여 주면 `ModuleNotFoundError: No module named 'ollama'`는 정확히 읽는다. "어떻게 고치나"를 물으면 **엉뚱한 해결책**을 말하기도 한다.

**질문:** 읽기는 맞고 판단은 틀릴 때, 프로그램은 VLM의 답을 어디까지 믿어야 하는가?

---

## 9–12분 · 툴 콜링: 모델이 못 하는 일을 함수에 맡긴다

```text
① 내 프로그램 → 모델     질문 + 함수 목록(get_current_time, multiply)
② 모델 → 내 프로그램     "multiply(a=1234, b=5678)을 불러 줘"   ← tool_calls
③ 내 프로그램            함수를 직접 실행 → 7006652
④ 내 프로그램 → 모델     결과를 role "tool" 로 전달
⑤ 모델 → 사람            "1234 × 5678 = 7,006,652 입니다"
```

- 모델은 지금 시각을 모르고, 큰 수 계산도 자주 틀린다.
- 모델은 **부탁만** 한다. 함수를 실행하는 것은 언제나 **내 프로그램**이다.
- `ex07`에서 `그 계산 결과에 2를 곱해 줘.`라고 이어서 묻는다. 종료는 `/bye`.

---

## 12–14분 · 툴 콜링 코드: 함수를 그대로 넘긴다

```python
def multiply(a: float, b: float) -> float:
    """두 수를 곱한다."""
    return a * b

response = ollama.chat(model=MODEL, messages=messages, tools=[multiply], think=False)
for call in response.message.tool_calls or []:
    result = multiply(**call.function.arguments)
    messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})
```

- 라이브러리가 함수 **이름·타입·docstring**을 읽어 모델에게 설명서로 보낸다.
- 숫자를 받는 함수는 잘 맞고, 글자를 정확히 맞춰야 하는 함수는 작은 모델이 자주 틀린다.

---

## 14–17분 · Modelfile: 역할을 모델 이름에 담기

```text
FROM qwen3.5:2b
SYSTEM """너는 '오픈소스 AI 응용' 수업의 실습 도우미다. 한국어로 다섯 문장 이내로 답한다."""
PARAMETER temperature 0.3
```

```powershell
ollama create student01-helper -f Modelfile
ollama run student01-helper --think=false
```

- 가중치를 복사하거나 다시 학습시키지 않는다. 설정만 붙인 **새 이름**이다.
- 시스템 프롬프트는 말투·형식을 바꿀 뿐 **모르는 지식을 채워 주지 않는다**(7주차 RAG, 10주차 LoRA).

---

## 17–20분 · 1차 종합과제와 실습 인계

[과제 안내](assignment_brief.md) · [루브릭](assignment_rubric.md) · [3교시 실습](lab.md#3교시-실습--이미지-인식-툴-콜링-내-도우미-모델) · [3교시 예제](examples/period3/README.md)

| 산출물 | 어디서 왔는가 |
|---|---|
| 협업 저장소(LICENSE·README·Issue·PR·Review) | 2주차 |
| uv 프로젝트(`pyproject.toml`·`uv.lock`) | 3주차 |
| 대화(기억)·이미지·툴 콜링 기능, `Modelfile`, `week04_report.md` | 4주차 |

실습 완료 조건: 내 그림 결과, 내가 추가한 함수가 불린 기록, 내 모델과 기준 모델의 비교.

---

## 이번 주 정리

```text
ollama show / run / ps        모델 크기·기능·속도·메모리를 숫자로 읽는다
ollama.chat(messages=…)       system·user·assistant, stream, temperature, 기억 = 메시지 쌓기
images=[…] / tools=[함수]      그림을 읽히고, 못 하는 일은 내 함수에 맡긴다
Modelfile → ollama create     역할은 설정에, 지식은 RAG에, 말투 고정은 LoRA에
```

만들기 전에 **이미 공개된 것을 찾아 가져다 쓴다.** 결과는 숫자와 비교로 확인한다.
