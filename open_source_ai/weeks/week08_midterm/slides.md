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
| 1교시 | 실기평가 구조와 모의 문제 읽는 법 | 모의 실기 A 프로젝트 복구와 uv·프로젝트 개념 문항 |
| 2교시 | Git·Ollama 실기 진단 포인트와 채점표 | 모의 실기 B Git 상황 판단과 Ollama 툴 콜링 |
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

## 3–6분 · 평가 범위 다섯 영역

| 영역 | 확인하는 것 |
|---|---|
| uv 사용법·재현성 | pyproject 복구, `uv add`가 바꾸는 파일, `pyproject.toml`·`uv.lock`, `sync --locked`, `uv run` |
| 프로젝트 관리법 | src 레이아웃, `[project.scripts]`, stdout·stderr, `.env`·`.env.example`, 설정 계층 |
| Git 개념·사용법 | 네 영역, `git status` 읽기, add·commit·push, 브랜치·충돌·PR 판단, 비밀 분리 |
| Ollama 사용법·응용 | `list`·`show`·`run`·`ps`, 메시지 역할, `options`·`think`, 실패 구분, 툴 콜링 |
| 검증·설명 | 정상·실패 경로 재현, 실행 기록, 근거 문장 |

모의 실기 A·B는 1~4주차 내용이다. 라이선스·HF·RAG의 포함 여부는 학기별 시험 공지가 정한다. 자세한 표는 [exam_structure.md](exam_structure.md)에 있다.

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
| "lock은 안 올려도 된다" | "`uv.lock`도 커밋한다 — 없으면 다음 사람은 다른 오늘을 해석한다" |
| "pull 한다" | "`git fetch` 뒤 `git merge origin/main` — 충돌은 working tree에서 푼다" |
| "모델이 기억한다" | "지난 질문·답을 `messages`에 쌓아 다시 보낸다 — 모델은 요청 사이에 아무것도 저장하지 않는다" |

답 형식: **판단 + 근거 + (있으면) 출처**. 세 줄을 넘기지 않는다.

**질문:** "확실하지 않다"를 점수가 되는 문장으로 바꾸면 어떻게 쓰는가?

---

## 17–20분 · 실습 인계

[1교시 실습 — 모의 실기 A 프로젝트 복구와 uv·프로젝트 개념 문항](lab.md#1교시-실습--모의-실기-a-프로젝트-복구와-uv프로젝트-개념-문항) · [교시별 예제](examples/period1/README.md)

완료 조건:

1. `uv run python report.py`가 `outputs/report.json`을 만든다
2. `git ls-files`에 `.env`가 없고 `.gitignore`·`.env.example`이 커밋되어 있다
3. `week8-hello`에서 `uv run hello`가 출력되고 첫 commit이 있으며, `answers_A.md`에 A-3·A-4의 답이 있다

타이머 30분. 실습 30분 뒤 휴식 10분, 휴식 후 2교시.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## Git·Ollama 실기 진단 포인트와 채점표

---

## 0–3분 · Git·Ollama 문항이 확인하는 것

- `git status`의 세 묶음을 **영역**으로 읽고 다음 명령을 고르는가
- `remote add`·`push -u`로 GitHub에 올리고, 다음부터 `git push`만으로 되는 이유를 아는가
- Ollama 서버·터미널 명령·Python 라이브러리의 관계와 메시지 세 역할을 설명하는가
- 툴 콜링에서 함수를 **실행하는 주체**가 누구인지 아는가

**질문:** `Changes to be committed`, `Changes not staged for commit`, `Untracked files`는 각각 어느 영역인가?

---

## 3–6분 · 진단 1: `git status`를 영역으로 읽는다

| 출력 | 영역 | 다음 명령 |
|---|---|---|
| `Changes to be committed: modified: a.py` | staging area | `git commit` |
| `Changes not staged for commit: modified: b.md` | working tree | `git add b.md` |
| `Untracked files: c.txt` | 추적 안 됨(working tree) | `git add c.txt` 또는 `.gitignore` |
| `Your branch is ahead of 'origin/main' by 1 commit` | repository만 앞섬 | `git push` |

`.gitignore`는 **아직 추적되지 않은** 파일만 막는다. 이미 add된 `.env`는 `git restore --staged .env`로 내린다.

---

## 6–9분 · 진단 2: 세 가지 "안 된다"는 원인이 다르다

| 메시지 | 원인 | 먼저 확인할 것 |
|---|---|---|
| `Failed to connect to Ollama` | 서버(앱)가 꺼짐 | `ollama list`가 되는가 |
| `model 'qwen3.5:2b' not found` | 이름·태그 오타, 미다운로드 | `ollama list`의 NAME |
| `No module named 'ollama'` | 프로젝트 환경 밖에서 실행 | `uv run ex01`로 실행했는가, `uv sync` |
| 답이 이상함 | 정상 응답 | `think`, `temperature`, system |

터미널 명령도 Python 라이브러리도 같은 서버에 묻는 **손님**이다. 서버가 꺼지면 둘 다 안 된다.

---

## 9–12분 · 툴 콜링 다섯 줄 다시 읽기

```text
① 내 프로그램 → 모델     질문 + 함수 목록(get_current_time, multiply)
② 모델 → 내 프로그램     "multiply(a=1234, b=5678)을 불러 줘"   ← tool_calls
③ 내 프로그램            함수를 직접 실행 → 7006652
④ 내 프로그램 → 모델     결과를 role "tool" 로 전달
⑤ 모델 → 사람            "1234 × 5678 = 7,006,652 입니다"
```

- 모델은 **부탁만** 한다. 실행은 언제나 내 프로그램이다
- 함수 결과와 `AI>` 답이 다르면 **함수 결과가 정답**이다
- 라이브러리가 이름·타입·docstring을 읽어 설명서로 보낸다 → `Args:`를 비우면 모델이 인자를 못 고른다

**질문:** `tools=`를 빼고 `1234 곱하기 5678은?`을 물으면 무엇이 달라지는가?

---

## 12–15분 · 채점표 읽는 법

| 영역 | 배점 |
|---|---:|
| uv 사용법·재현성 | 20 |
| 프로젝트 관리법 | 15 |
| Git 개념·사용법 | 20 |
| Ollama 사용법·응용 | 30 |
| 검증·설명 | 15 |

100점 상대 배점이다. 수준은 완전·부분·미충족 세 단계 — [exam_rubric.md](exam_rubric.md).

---

## 15–17분 · 흔한 감점 원인

- 명령은 맞는데 어느 영역이 바뀌는지 설명이 없음
- `git add`를 빼먹고 commit해 변경이 기록되지 않았는데 "올렸다"고 적음
- `[함수 실행]` 줄 없이 "됐다"고만 적음 — 실행 기록이 증거다
- `.env`·`.venv`·`outputs/`가 commit에 포함
- 연결 실패·모델 없음·모듈 없음을 한 원인으로 묶어 적음
- 실행은 되지만 어떤 코드를 왜 바꿨는지 설명하지 못함

**핵심:** 기능 하나를 덜 하더라도 **한 경로를 끝까지** 증거로 남긴다.

---

## 17–20분 · 실습 인계

[2교시 실습 — 모의 실기 B Git 상황 판단과 Ollama 툴 콜링](lab.md#2교시-실습--모의-실기-b-git-상황-판단과-ollama-툴-콜링) · [교시별 예제](examples/period2/README.md)

완료 조건:

1. B-1에 세 파일의 영역 판정과 명령 순서의 영역 표기가 있고, B-2의 GitHub 저장소에 commit 2개가 보인다
2. B-3 표에서 세 가지 "안 된다"의 원인과 확인 방법이 서로 다르다
3. `answers_B.md`에 새 함수를 부른 `[함수 실행]` 줄과 세 단계 설명이 있다

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
uv run python chunk.py ; uv run python embed.py   # outputs/ 인덱스는 clone 에 없다
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

[3교시 실습 — 개인 실기평가와 대체 운영](lab.md#3교시-실습--개인-실기평가와-대체-운영) · [교시별 예제](examples/period3/README.md)

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
