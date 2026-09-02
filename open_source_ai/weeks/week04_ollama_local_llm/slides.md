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
| 1교시 | 모델은 어떻게 실행되는가 | 모델 두 개를 실행하고 측정하기 |
| 2교시 | REST API로 대화하기 | REST API로 대화하고 실패를 다루기 |
| 3교시 | Modelfile과 시스템 프롬프트, 1차 종합과제 | 수업 도우미 모델 만들기와 과제 점검 |

이번 주 질문: **내 PC의 GPU에서 언어 모델이 실제로 어떻게 실행되고, 내 프로그램은 그것과 어떻게 대화하는가?**

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 모델은 어떻게 실행되는가

---

## 0–3분 · 이어받는 것: 설정에서 호출로

3주차 `config.py`는 `OLLAMA_HOST`·`OLLAMA_MODEL`을 읽지만 아직 아무것도 호출하지 않았다.

```text
3주차: 설정 읽기    → config.py
4주차: 실제 호출    → ollama run … → /api/chat → Modelfile
```

- 오늘 쓸 모델은 **수업 전에 이미 캐시**되어 있다. 실습 중 `ollama pull`을 하지 않는다.
- 기본 모델 이름은 환경변수 `OLLAMA_MODEL`이 정한다(교재 기본값 `qwen3:4b`, CPU 대체 `qwen3:0.6b`).

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
| 컨텍스트 | 지금까지의 토큰과 계산 캐시(KV) | `num_ctx` × 층 수 |

생성은 **토큰 하나씩 반복**이다. 그래서 속도 단위가 tokens/s다.

---

## 6–9분 · 양자화: 같은 모델, 다른 바이트

| 표기 | 파라미터당 바이트 | 4B 모델 가중치 |
|---|---:|---:|
| FP16·BF16 | 2 | 약 8 GB |
| Q8_0 | 약 1 | 약 4 GB |
| Q4_K_M | 약 0.6 | 약 2.5 GB |

- GGUF는 llama.cpp 계열이 쓰는 파일 형식이며 Ollama 라이브러리 모델 대부분이 이 형식이다.
- Q4로 내려가면 용량·속도는 좋아지고 **답의 품질은 조금 떨어진다**. 얼마나 떨어지는지는 모델·작업마다 다르다.

**질문:** 같은 `qwen3:4b`인데 `ollama list`의 SIZE와 `ollama ps`의 SIZE가 다르다면 무엇이 더해진 것인가?

---

## 9–12분 · 파라미터 수 → VRAM 어림 계산

```text
필요 메모리 ≈ 파라미터 수 × 파라미터당 바이트 + 컨텍스트(KV 캐시) + 여유
```

| 모델 | Q4 가중치 | 12 GB GPU에서 |
|---|---:|---|
| 0.6B | 약 0.5 GB | 여유. CPU로도 쓸 만함 |
| 4B | 약 2.5 GB | 여유 |
| 8B | 약 5 GB | 가능 |
| 14B | 약 9 GB | `num_ctx`를 줄여야 함 |
| 32B | 약 20 GB | 불가. CPU 분담 → 매우 느림 |

숫자는 어림값이고 **실측은 `ollama ps`가 한다.**

**질문:** 14B를 12 GB에 올리려면 무엇을 희생해야 하는가?

---

## 12–15분 · Ollama의 네 부분

```text
ollama serve (서버, :11434) ◀── ollama run/show/ps/list (CLI = 클라이언트)
        │                   ◀── 내 프로그램 (HTTP, 2교시)
        ├─ 모델 저장소  %USERPROFILE%\.ollama\models  (blobs + manifests)
        └─ Modelfile  → ollama create (3교시)
```

- CLI도 서버에 HTTP를 보내는 **클라이언트**다. 서버가 죽으면 CLI도 내 코드도 안 된다.
- 저장 위치는 `OLLAMA_MODELS`로 옮길 수 있다. 실습실 PC는 환경 기준표가 정한 경로를 쓴다.
- 라이브러리 이름 규칙은 `이름:태그`(`qwen3:4b`). 태그가 크기·양자화를 뜻한다.

---

## 15–17분 · 오늘 쓰는 CLI 다섯 개

```powershell
ollama list              # 캐시된 모델과 파일 크기
ollama show qwen3:4b     # 파라미터·양자화·컨텍스트 길이
ollama run qwen3:4b      # 대화. /set verbose 로 속도 표시, /bye 로 종료
ollama ps                # 메모리에 올라간 모델, SIZE, GPU 비율
ollama pull qwen3:0.6b   # 다운로드 — 수업 시간에는 쓰지 않는다
```

`ollama run`의 첫 답이 늦은 것은 **로드 시간**이다. 두 번째부터는 빠르다.

---

## 17–20분 · 실습 인계

[1교시 실습 — 모델 두 개를 실행하고 측정하기](lab.md#1교시-실습--모델-두-개를-실행하고-측정하기)

완료 조건:

1. 기본 모델의 파라미터 수·양자화·컨텍스트 길이·파일 크기를 `ollama show`·`ollama list`에서 옮겨 적었다.
2. `/set verbose`의 eval rate와 `ollama ps`의 SIZE·PROCESSOR를 모델 2개에 대해 기록했다.
3. 같은 질문 3개에 대한 두 모델의 답 차이를 `model_report.md`에 한 문장씩 적었다.

실습 30분 뒤 휴식 10분. 휴식 후 2교시.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## REST API로 대화하기

---

## 0–3분 · 이어받는 것: 서버는 살아 있는가

1교시에서는 `ollama run`으로 대화했다. 이제 같은 서버에 **내 코드**가 말을 건다.

```powershell
Invoke-RestMethod http://localhost:11434/api/tags |
  Select-Object -ExpandProperty models | Format-Table name, size
```

- `/api/tags`는 캐시된 모델 목록이다. 이 한 줄이 되면 서버·포트·모델 이름 세 가지가 확인된다.
- 하루가 바뀌었으면 모델이 메모리에 없다. 첫 호출이 느린 것은 정상이다.

---

## 3–6분 · `/api/generate`와 `/api/chat`

| | `/api/generate` | `/api/chat` |
|---|---|---|
| 입력 | `prompt` 문자열 하나 | `messages` 배열(역할 있음) |
| 대화 이력 | 직접 이어 붙여야 함 | 배열에 쌓으면 됨 |
| 응답 본문 | `response` | `message.content` |
| 쓰임 | 한 번짜리 변환·요약 | 도우미·챗봇 |

둘 다 같은 모델을 쓰고 같은 메타(`eval_count` 등)를 돌려준다. 이번 주 클라이언트는 **`/api/chat`**을 쓴다.<br>
OpenAI 호환 경로(`/v1/chat/completions`)도 있지만 이번 주는 쓰지 않는다.

---

## 6–9분 · 메시지 역할과 이력

```json
{"model": "qwen3:4b",
 "messages": [
   {"role": "system",    "content": "한국어로 세 문장 이내로 답한다."},
   {"role": "user",      "content": "uv가 무엇인가?"},
   {"role": "assistant", "content": "uv는 …"},
   {"role": "user",      "content": "pip와 무엇이 다른가?"}
 ],
 "stream": false, "think": false, "options": {"temperature": 0.2}}
```

- `system`: 역할·제약. 대화 내내 유지된다.
- 서버는 이력을 기억하지 않는다. **이력은 클라이언트가 매번 보낸다.**

**질문:** 대화가 길어지면 무엇이 `num_ctx`를 넘게 되는가?

---

## 9–12분 · 스트리밍: 줄 단위 JSON

`"stream": true`이면 응답이 한 번에 오지 않고 **한 줄에 JSON 하나(NDJSON)** 로 온다.

```text
{"message":{"role":"assistant","content":"uv"},"done":false}
{"message":{"role":"assistant","content":"는 "},"done":false}
…
{"message":{"role":"assistant","content":""},"done":true,"eval_count":57,"eval_duration":812345678}
```

- 조각을 이어 붙이면 전체 답이 된다. 메타는 **마지막 줄**에만 있다.
- 사용자에게는 첫 조각까지의 시간(로드 + 프롬프트 처리)이 체감 지연이다.

**질문:** 조각을 화면에 찍기만 하고 모으지 않으면 무엇을 잃는가?

---

## 12–15분 · options와 think

| 키 | 뜻 | 실습 기본값 |
|---|---|---|
| `temperature` | 0이면 가장 확률 높은 토큰만, 클수록 다양 | 0.2 |
| `num_ctx` | 컨텍스트 창 토큰 수(KV 캐시 크기) | 4096 |
| `num_predict` | 최대 생성 토큰 수 | 256 |
| `seed` | 같은 값이면 같은 표본 순서 | 없음 |

```json
"think": false
```

Qwen3 계열은 답 앞에 **생각 텍스트**를 먼저 만든다. 수업 코드는 답만 보기 위해 끄고, 그 이유를 주석으로 남긴다.

---

## 15–17분 · 응답 메타와 실패 두 가지

```text
tokens/s = eval_count ÷ (eval_duration ÷ 1e9)      duration 단위는 나노초
```

- `prompt_eval_count`·`eval_count`: 입력·출력 토큰 수
- `done_reason`: `stop`(모델이 끝냄) 또는 `length`(`num_predict`에 걸림)

| 실패 | 코드가 받는 것 | 사람에게 보여 줄 말 |
|---|---|---|
| 서버 꺼짐·포트 오류 | `ConnectError` | 서버·`OLLAMA_HOST` 확인 |
| 모델 이름 오류 | HTTP 404 | `ollama list`로 이름 확인 |

**질문:** `done_reason`이 `length`면 코드의 무엇을 바꿔야 하는가?

---

## 17–20분 · 실습 인계

[2교시 실습 — REST API로 대화하고 실패를 다루기](lab.md#2교시-실습--rest-api로-대화하고-실패를-다루기)

완료 조건:

1. `chat.py`가 남긴 `outputs/chat-*.json`에서 `eval_count`·`eval_duration`을 찾아 tokens/s를 직접 계산했다.
2. 연결 실패와 모델 없음 두 경우에 사람이 읽을 메시지와 0이 아닌 종료 코드가 나왔다.
3. `--seed`를 추가한 뒤 temperature 0과 1의 답 차이를 한 문단으로 적었다.

실습 30분 뒤 휴식 10분. 휴식 후 3교시.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## Modelfile과 시스템 프롬프트, 1차 종합과제

---

## 0–3분 · 이어받는 것: 역할은 어디에 두는가

2교시 `chat.py`는 `--system`으로 역할을 매번 보냈다. 같은 역할을 **모델 이름 안에** 넣어 두면 어떤 클라이언트든 같은 도우미를 얻는다.

```text
방법 A: 요청마다 system 메시지   → 클라이언트가 책임 (2교시)
방법 B: Modelfile → ollama create → 서버가 책임 (오늘)
방법 C: 파인튜닝(10주차)          → 가중치가 책임
```

**질문:** 방법 B로 만든 모델은 디스크를 얼마나 더 차지할까?

---

## 3–6분 · Modelfile 네 지시어

```text
FROM qwen3:4b                          # 기준 모델(캐시된 이름 또는 GGUF 경로)
SYSTEM """너는 수업 실습 도우미다. …"""   # 시스템 프롬프트
PARAMETER temperature 0.3              # 기본 옵션. 요청의 options가 우선한다
PARAMETER num_ctx 4096
# TEMPLATE: 프롬프트 조립 틀. FROM에서 물려받으므로 보통 쓰지 않는다
```

- `ollama show qwen3:4b --modelfile`로 기준 모델의 Modelfile 전체를 볼 수 있다.
- 지시어는 대문자, 여러 줄 문자열은 `"""`로 감싼다. `#`은 주석이다.

---

## 6–9분 · `ollama create`는 복사가 아니다

```powershell
ollama create osa-helper -f Modelfile
ollama list                 # osa-helper 가 보인다
ollama show osa-helper      # System 항목이 붙어 있다
ollama rm osa-helper        # 지우기 — 기준 모델은 남는다
```

- 가중치 blob은 **기준 모델과 공유**하고 시스템 프롬프트·파라미터 레이어만 새로 만든다.
- 이름은 소문자·숫자·`-`로 쓴다. 팀명을 앞에 붙이면 겹치지 않는다(`team-a-helper`).

**질문:** `ollama rm qwen3:4b`를 하면 `osa-helper`는 어떻게 되는가?

---

## 9–12분 · 시스템 프롬프트 설계

| 요소 | 나쁜 예 | 좋은 예 |
|---|---|---|
| 역할 | "친절한 AI" | "오픈소스 AI 응용 실습 도우미" |
| 제약 | "잘 답해" | "5문장 이내, 한국어, 모르면 모른다고" |
| 출력 형식 | 없음 | "명령은 PowerShell 코드 블록 하나로" |
| 안전 | 없음 | "토큰·비밀번호를 묻지 않는다" |

**한 번에 하나만 바꾸고 같은 질문으로 전후를 비교**해야 무엇이 효과를 냈는지 안다.

---

## 12–14분 · 프롬프트로 되는 것과 안 되는 것

- 되는 것: 말투, 길이, 언어, 출력 형식, 거절 규칙, 역할극
- 잘 안 되는 것: 모델이 **모르는 지식**, 긴 규칙 수십 개의 동시 준수, 일관된 전문 용어
- 지식은 7주차 RAG(문서를 넣어 준다), 말투·형식의 고정은 10주차 LoRA(가중치를 바꾼다)

**질문:** "우리 수업의 과제 마감을 알려 줘"가 프롬프트만으로 안 되는 이유는 무엇인가?

---

## 14–17분 · 1차 종합과제

[안내서](assignment_brief.md) · [루브릭](assignment_rubric.md)

| 산출물 | 어디서 왔는가 |
|---|---|
| 협업 저장소(LICENSE·README·Issue·PR·Review) | 2주차 |
| uv 프로젝트(`pyproject.toml`·`uv.lock`·`.env.example`) | 3주차 |
| `chat`·`stream` 서브커맨드 CLI + 오류 처리 + `outputs/` | 4주차 2교시 |
| `model_report.md` + Modelfile 전후 비교 | 4주차 1·3교시 |

제출은 **저장소 URL + 최종 commit id + README 재현 절차**. 배점·마감은 학교 운영 문서가 정한다.

---

## 17–20분 · 실습 인계

[3교시 실습 — 수업 도우미 모델 만들기와 과제 점검](lab.md#3교시-실습--수업-도우미-모델-만들기와-과제-점검)

완료 조건:

1. `ollama list`에 내 커스텀 모델이 보이고 `chat.py --model`에 그 이름을 주어 호출했다.
2. 같은 질문 3개에 대해 기준 모델·커스텀 모델·SYSTEM 한 줄 변경 후의 답을 비교표로 남겼다.
3. 1차 과제 체크리스트에서 비어 있는 항목과 채울 계획을 적었다.

실습 30분 뒤 휴식 10분. 이번 주 종료.

---

## 이번 주 정리

```text
가중치 × 양자화 → VRAM        ollama show / ps 로 실측
서버 :11434 ← CLI ← 내 코드    /api/chat + stream + think:false + options
Modelfile → ollama create     역할은 서버에, 지식은 RAG에, 말투 고정은 LoRA에
```

숫자는 어림하고 **실측으로 확인**한다. 실패 메시지는 사람이 읽을 문장으로 바꾼다.
