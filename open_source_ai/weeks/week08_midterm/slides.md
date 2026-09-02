---
marp: true
theme: default
paginate: true
header: "오픈소스 AI 응용 · 8주차"
footer: "수시평가와 2차 종합과제"
---

# 8주차
## 수시평가와 2차 종합과제

**60분 블록 × 3**<br>
매 블록 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분

---

## 이번 주 세 블록

| 교시 | 설명·시연 20분 | 직접 해결 실습 30분 |
|---|---|---|
| 1교시 | 실기평가 구조와 모의 문제 읽는 법 | 모의 실기 A 프로젝트 복구와 판별 문항 |
| 2교시 | 로컬 AI 실기 진단 포인트와 채점표 | 모의 실기 B 클라이언트 기능 추가와 결과 해석 |
| 3교시 | 실기평가 운영과 2차 과제 최종 점검 | 개인 실기평가와 대체 운영 |

이번 주 질문: **1~7주의 내용을 혼자서 재현하고 설명할 수 있는가?**

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 실기평가 구조와 모의 문제 읽는 법

---

## 0–3분 · 이번 주는 새 기능이 아니라 재현이다

```text
1~7주 실습 ──▶ 혼자서 다시 만들 수 있는가   → 수시 실기평가
5~7주 누적 ──▶ 남이 재현할 수 있게 묶었는가 → 2차 종합과제
```

- 실기: 1·2교시 공개 동형 모의 → 3교시 개인 실기(비공개 패킷)
- 과제: 라이선스·출처 분석 + RAG 미니프로젝트 + 재현 절차
- 이 자료에는 실제 문항·정답이 없다

**질문:** 7주 동안 만든 것 중 지금 당장 빈 폴더에서 다시 만들 수 있는 것은 무엇인가?

---

## 3–6분 · 평가 범위 여섯 영역

| 영역 | 확인하는 것 |
|---|---|
| Git·협업 | 브랜치·commit·충돌·PR 판단, 비밀 분리 |
| 라이선스·출처 | permissive/copyleft, 모델·데이터 조건, SPDX, `SOURCES.md` |
| uv 재현성 | pyproject 복구, sync·run, `.gitignore`·`.env.example` |
| Ollama 실행·API | 요청 JSON, `stream`·`think`·`options`, 메타, 실패 처리 |
| HF pipeline·모델 카드 | label·score·device·경고 해석, 용도·제한 |
| 검증·설명 | 정상·실패 경로 재현, `outputs/`, 근거 문장 |

자세한 표는 [exam_structure.md](exam_structure.md)에 있다.

---

## 6–9분 · 규정: 허용 자료·AI 도구·제출

- 허용 자료: 공개 교재, 본인 저장소, 공식 문서 — 범위는 시험 공지가 확정한다
- AI 도구: 허용 범위와 표기 방식은 학교 운영 문서가 정한다
- 제출: 지정 파일 + 마지막 commit id + 짧은 설명(무엇을·왜)
- 안내는 모두에게 같은 수준으로, 정답에 해당하는 개별 힌트는 없다
- 학생 코드·점수는 공개 저장소에 올리지 않는다

**핵심:** 채점자는 캡처가 아니라 **재현 가능한 파일과 commit**을 본다.

---

## 9–12분 · 문제를 읽는 순서

```text
요구사항   "uv sync 가 되게 고쳐라"
    ↓
완료 조건  "uv run python report.py 가 outputs/report.json 을 만든다"
    ↓
검증 순서  "1) uv sync  2) uv run  3) 파일 열기  4) git ls-files"
```

- 코드를 만지기 전에 완료 조건을 체크 항목으로 바꾼다
- 검증 명령을 정해 두면 "됐다"를 남에게 보일 수 있다

**질문:** 완료 조건에 없는 것을 먼저 고치면 무엇을 잃는가?

---

## 12–15분 · 모의 A 미리 보기: 깨진 프로젝트

```powershell
uv sync
# TOML parse error at line 8 ... missing comma between array elements
```

- 결함 1: `pyproject.toml` 문법 오류 — 첫 실행에서 바로 보인다
- 결함 2: 테이블 이름 오타 — sync는 성공한 척하고 `import`가 실패한다
- 결함 3: `requires-python` 표기 오류 — 결함 2를 고쳐야 나타난다
- 결함 4: `.gitignore` 없음 + `.env` 커밋됨 — 명령 오류 없이 이력에 남는다

오류는 **한 번에 하나씩** 나타난다. 고치고, 다시 실행하고, 다음 오류를 읽는다.

---

## 15–17분 · 판별 문항은 근거 한 줄이 점수다

| 나쁜 답 | 좋은 답 |
|---|---|
| "쓸 수 있다" | "쓸 수 있다 — MIT는 재배포 시 저작권 고지만 요구한다" |
| "안 된다" | "GPL-3.0 코드를 import해 배포하면 결합물도 GPL 조건을 따른다" |
| "pull 한다" | "`git fetch` 뒤 `git merge origin/main` — 충돌은 working tree에서 푼다" |

답 형식: **판단 + 근거 + (있으면) 출처**. 세 줄을 넘기지 않는다.

**질문:** "확실하지 않다"를 점수가 되는 문장으로 바꾸면 어떻게 쓰는가?

---

## 17–20분 · 실습 인계

[1교시 실습 — 모의 실기 A 프로젝트 복구와 판별 문항](lab.md#1교시-실습--모의-실기-a-프로젝트-복구와-판별-문항)

완료 조건:

1. `uv run python report.py`가 `outputs/report.json`을 만든다
2. `git ls-files`에 `.env`가 없고 `.gitignore`·`.env.example`이 커밋되어 있다
3. `answers_A.md`에 라이선스 3문항·Git 1문항의 판단과 근거가 있다

타이머 30분. 실습 30분 뒤 휴식 10분, 휴식 후 2교시.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## 로컬 AI 실기 진단 포인트와 채점표

---

## 0–3분 · 로컬 AI 문항이 확인하는 것

- 요청 JSON을 **읽고 쓸** 수 있는가 — `model`·`messages`·`stream`·`think`·`options`
- 실패를 사람이 읽을 메시지로 바꾸는가 — 연결 실패와 모델 없음은 다르다
- 응답 메타를 기록해 "느리다"를 숫자로 말하는가
- 모델 이름·주소를 하드코딩하지 않고 환경변수 + 기본값으로 읽는가

**질문:** 서버가 꺼졌을 때와 모델이 없을 때, 프로그램은 어떤 예외를 각각 만나는가?

---

## 3–6분 · 진단 1: 연결 실패와 모델 없음

| 증상 | 예외·응답 | 먼저 확인할 것 |
|---|---|---|
| 응답 없이 즉시 실패 | `httpx.ConnectError` | `ollama serve` 여부, `OLLAMA_HOST` |
| 오래 기다리다 실패 | `httpx.TimeoutException` | 첫 로딩 중인가, `timeout` 값 |
| 즉시 실패, 본문에 `not found` | HTTP 404 | `ollama list`, 모델 이름·태그 |
| 200인데 답이 이상함 | 정상 응답 | `think`, `temperature`, 프롬프트 |

같은 "안 된다"도 **예외 종류**가 다르면 원인이 다르다.

---

## 6–9분 · 진단 2: 스트리밍 파싱과 옵션 효과

```json
{"model": "qwen3:4b",
 "messages": [{"role": "user", "content": "..."}],
 "stream": false,
 "think": false,
 "options": {"temperature": 0.2, "num_predict": 256}}
```

- `stream: true`면 응답은 **NDJSON 줄 단위** — 한 줄씩 `json.loads`
- `think: false`는 Qwen3 계열의 사고 출력을 답에서 분리한다
- `options`는 Modelfile 기본값을 요청 단위로 덮어쓴다

---

## 9–12분 · 응답 메타를 읽는 법

```python
eval_count = data["eval_count"]        # 생성 토큰 수
eval_ns = data["eval_duration"]        # 나노초
tokens_per_sec = eval_count / (eval_ns / 1e9)
```

- `total_duration`: 로딩 + 프롬프트 처리 + 생성 전체
- `prompt_eval_count`: 입력 토큰 수 — 컨텍스트가 길어지면 커진다
- 기록 없이 "빠르다·느리다"는 채점 근거가 되지 않는다

**질문:** 같은 모델인데 첫 호출만 `total_duration`이 큰 이유는?

---

## 12–15분 · 채점표 읽는 법

| 영역 | 배점 |
|---|---:|
| 재현·실행 | 15 |
| Git·협업 | 15 |
| 라이선스·출처 | 15 |
| 로컬 AI API | 25 |
| HF 활용 | 15 |
| 검증·설명 | 15 |

100점 상대 배점이다. 수준은 완전·부분·미충족 세 단계 — [exam_rubric.md](exam_rubric.md).

---

## 15–17분 · 흔한 감점 원인

- `outputs/`가 없거나 실행 결과가 파일로 남지 않음
- 예외를 잡아 놓고 원인이 안 보이는 메시지("에러 발생")만 출력
- 모델 이름·주소를 코드에 하드코딩
- `.env`·`.venv`·`outputs/`가 commit에 포함
- 정상 경로만 시연하고 실패 경로 증거가 없음
- 실행은 되지만 어떤 코드를 왜 바꿨는지 설명하지 못함

**핵심:** 기능 하나를 덜 하더라도 **한 경로를 끝까지** 증거로 남긴다.

---

## 17–20분 · 실습 인계

[2교시 실습 — 모의 실기 B 클라이언트 기능 추가와 결과 해석](lab.md#2교시-실습--모의-실기-b-클라이언트-기능-추가와-결과-해석)

완료 조건:

1. `--system` 옵션이 동작하고 전후 답이 달라진 근거를 한 문장으로 적었다
2. `outputs/chat-*.json`에 `eval_count`·`eval_duration`·`tokens_per_sec`가 기록된다
3. `answers_B.md`에 pipeline 해석 3문항의 판단과 근거가 있다

타이머 30분. 실습 30분 뒤 휴식 10분, 휴식 후 3교시.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 실기평가 운영과 2차 과제 최종 점검

---

## 0–3분 · 시작 전 환경 점검 다섯 가지

```powershell
uv run python check_env.py     # Ollama 연결 + 기본 모델 존재
git status                     # working tree clean
ollama list                    # 사전 캐시 모델
Get-Location                   # 지정 저장 경로
```

- 제출 경로에 테스트 파일을 올리고 다시 내려받아 본다
- 점검 결과는 `outputs/env-check.json`으로 남는다 — 장애가 나면 증거가 된다

---

## 3–6분 · 패킷 구조와 제출물

```text
패킷: 요구사항 문서 + starter + fixture + 제출 파일명
제출: 지정 파일 + 마지막 commit id + 짧은 설명(무엇을·왜)
```

- 요구사항마다 완료 조건을 체크 항목으로 옮긴 뒤 시작한다
- commit하지 않은 변경은 제출에 없다 — `git status`로 마지막 확인
- 제출 파일을 **다시 열어** 같은 내용인지 본다

**질문:** commit id를 함께 내는 이유는 무엇인가?

---

## 6–9분 · 장애가 생겼을 때

| 상황 | 대체 |
|---|---|
| GPU 인식 실패 | CPU 대체 모델(`qwen3:0.6b`)로 진행, 사실을 답안에 기록 |
| Ollama 서버 미기동 | 재시작 1회, 안 되면 감독에게 시각과 함께 알림 |
| 네트워크 없음 | `uv sync --offline`, 사전 캐시 모델만 사용 |
| 제출 시스템 장애 | 대체 제출 창구, 장애 시각 기록 |

장애는 학생 오류와 **기록상 구분**된다. 감추지 말고 알린다.

---

## 9–12분 · 2차 종합과제 필수 산출물

1. 라이선스·출처 분석 보고: `model_cards.md`·`SOURCES.md`·`license_matrix.md` 확장
2. RAG 미니프로젝트: 자기 문서 10개 이상, 출처 표시, 컨텍스트 밖 질문 처리
3. 평가: `evalset.json` 10문항, hit rate·출처 일치율, 실패 분석 2건
4. 재현 절차: README, `uv.lock`, `.env.example`
5. 개인 기여 증거: commit·Issue·PR·Review

[assignment_brief.md](assignment_brief.md) · [assignment_rubric.md](assignment_rubric.md)

---

## 12–15분 · 최종 점검은 깨끗한 폴더에서

```powershell
git clone 저장소URL check-clean
Set-Location check-clean
uv sync --frozen
uv run python eval.py --evalset evalset.json
```

- README에 적힌 명령을 **그대로** 복사해 실행한다
- 한 줄이라도 README에 없는 조작이 필요하면 README가 미완성이다
- `examples/assignment_check.ps1`로 파일 존재·비밀 흔적을 먼저 훑는다

**질문:** "내 PC에서만 된다"의 가장 흔한 원인은?

---

## 15–17분 · 제출 직전 비밀·개인정보 검사

```powershell
git ls-files | Select-String "\.env$"
git log --all -p -S "hf_" | Select-String "hf_"
```

- `.env`가 이력에 한 번이라도 들어갔다면 삭제 commit으로는 부족하다 — 토큰 회전
- RAG 문서·평가셋에 실제 이름·연락처가 없는지 본다
- `outputs/`의 응답 JSON에 개인정보가 섞였는지 본다

---

## 17–20분 · 실습 인계

[3교시 실습 — 개인 실기평가와 대체 운영](lab.md#3교시-실습--개인-실기평가와-대체-운영)

완료 조건:

1. `outputs/env-check.json`이 있고 `git status`가 clean인 상태로 시작했다
2. 제출 파일과 commit id를 기록하고 제출물을 다시 열어 확인했다
3. 대체 운영이면 2차 과제를 깨끗한 폴더에서 재현하고 검사 결과를 기록했다

실기 시간은 기관 시간표를 따른다. 실습 30분 뒤 휴식 10분.

---

## 이번 주 정리

```text
실기: 요구사항 → 완료 조건 → 검증 순서 → 증거(파일 + commit id)
과제: 깨끗한 폴더에서 README 그대로 → 같은 결과 → 비밀 없음
```

- 오류는 한 번에 하나씩 읽는다
- 판단에는 근거 한 줄을 붙인다
- 다음 주 `week09_project_governance`는 팀 프로젝트 제안이다
