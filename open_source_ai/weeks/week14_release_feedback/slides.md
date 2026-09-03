---
marp: true
theme: default
paginate: true
header: "오픈소스 AI 응용 · 14주차"
footer: "릴리스와 커뮤니티 피드백"
---

# 14주차
## 릴리스와 커뮤니티 피드백

**60분 블록 × 3**<br>
매 블록 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분

---

## 이번 주 세 블록

| 교시 | 설명 20분 | 실습 30분 |
|---|---|---|
| 1교시 | 릴리스 문서 세트 | 릴리스 문서 세트 보완 |
| 2교시 | 버전과 릴리스 | 릴리스 생성과 교차 재현 |
| 3교시 | 커뮤니티 피드백과 시연 준비 | 피드백 응답과 시연 리허설 |

이번 주 질문: **처음 보는 사람이 README만 읽고 10분 안에 실행하고, 의견을 남기고 싶어지는 릴리스는 무엇으로 이루어지는가?**

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 릴리스 문서 세트

---

## 0–3분 · 릴리스는 코드가 아니라 약속이다

- 이어받는 것: 13주차 초록불(pytest·ruff·CI), 9주차 LICENSE·CONTRIBUTING·CoC, `SOURCES.md`
- 릴리스 = "이 시점의 이 파일들을 남이 써도 된다"는 약속
- 처음 보는 사람은 코드가 아니라 **문서를 먼저 읽는다**
- 이번 주 산출물: 문서 세트 → `v0.1.0` → 교차 재현 → 피드백 응답

**질문:** 우리 저장소를 처음 본 사람이 README에서 가장 먼저 찾을 정보는 무엇인가?

---

## 3–6분 · README 8개 절

```text
무엇      한 줄: 누구를 위한 어떤 도구인가
왜        사용자·상황, 기존 해법의 한계
설치      clone → checkout 태그 → uv sync --frozen → .env
실행      복사·붙여넣기로 동작하는 명령 2~3개
예시      입력 1개 → 출력 1개 (출처가 보이게)
제한      안 되는 것, VRAM·모델·데이터 조건
라이선스  코드 + 모델·데이터의 가장 제한적인 조건
출처      SOURCES.md · CHANGELOG · CITATION
```

**설치·실행 절은 새 창에서 붙여넣어 한 번 실행해 본 뒤 commit한다.**

---

## 6–9분 · LICENSE 재확인 — 호환의 방향

```text
코드 MIT ──┬── 의존성 Apache-2.0        → 호환
           ├── 모델   Apache-2.0 (Qwen)  → 호환
           ├── 데이터 CC-BY-NC-4.0       → 어댑터·산출물에 NC 조건 전파
           └── 의존성 GPL-3.0            → 배포본 전체가 GPL 조건
```

- 가장 제한적인 조건이 전체에 적용된다
- 판단 결과는 README 「제한」·「라이선스」 절에 **문장으로** 적는다
- 근거는 `SOURCES.md`의 SPDX ID와 URL

**질문:** 학습 데이터가 CC-BY-NC라면 어댑터를 MIT로 공개할 수 있는가?

---

## 9–12분 · CONTRIBUTING과 Model Card

| 문서 | 없으면 생기는 일 | 최소 내용 |
|---|---|---|
| CONTRIBUTING.md | 의견이 오지 않거나 형식이 제각각 | Issue 양식, 브랜치·PR 규칙, 첫 응답 담당 |
| MODEL_CARD.md | 어댑터를 받은 사람이 용도·한계를 모른다 | 기반 모델·revision, 데이터·라이선스, 학습 설정, 평가표, 한계 |
| CODE_OF_CONDUCT.md | 갈등이 생겼을 때 기준이 없다 | 채택 문구와 연락 통로 |

- Hub 모델 저장소에 `README.md`로 올리면 frontmatter(`license`·`base_model`)가 메타데이터가 된다
- 어댑터를 공개하지 않는 팀은 Model Card 대신 `SOURCES.md`만 최종화한다

---

## 12–15분 · CHANGELOG와 CITATION.cff

```markdown
## [Unreleased]
### Added
- 출처를 표시하는 문서 검색 답변기
### Fixed
- Ollama 미기동 시 연결 안내 메시지를 반환 (#12)
```

- Keep a Changelog: 최신이 위, Added / Changed / Fixed, **사용자 관점 문장**
- commit 제목 복사 금지. "무엇이 사용자에게 달라졌는가"로 다시 쓴다
- CITATION.cff 필수 4개: `cff-version`·`message`·`title`·`authors`. `version`은 선택이지만 `pyproject.toml`과 같게 적는다

**질문:** "refactor config loader"는 CHANGELOG에 들어가는가?

---

## 15–17분 · AI 도구 사용 내역과 자동 점검

```powershell
uv run python release_check.py --repo C:\classwork\team-a-repo --tag v0.1.0
```

- AI 도구 사용 내역 표 세 칸: 파일·범위 / AI가 만든 것 / 사람이 검증·수정한 것
- `release_check.py`: README 8개 절, LICENSE, CONTRIBUTING, CHANGELOG, CITATION, SOURCES, `.env` 추적, version과 태그 → `outputs/release-check-*.json`
- 종료 코드 1 = FAIL 있음. 읽기 전용이라 아무 파일도 고치지 않는다
- **도구는 "있다"만 본다. "맞다"는 사람이 본다**

---

## 17–20분 · 실습 인계

[1교시 실습 — 릴리스 문서 세트 보완](lab.md#1교시-실습--릴리스-문서-세트-보완)

완료 조건:

1. `release_check.py` 결과에 FAIL이 없다(남은 WARN은 이유를 적었다).
2. `SOURCES.md` 모든 행에 라이선스·SPDX ID·URL이 있고 README 「제한」에 가장 제한적인 조건이 있다.
3. CHANGELOG `[Unreleased]`에 사용자 관점 항목 3개 이상, 보완 commit 1개.

실습 30분 뒤 휴식 10분, 휴식 후 2교시.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## 버전과 릴리스

---

## 0–3분 · 릴리스는 시점을 고정하는 것

- 이어받는 것: 1교시 FAIL 0 저장소(push됨), 정리된 `[Unreleased]`
- 태그 = commit 하나에 붙인 이름. 릴리스 = 태그 + 노트 + (첨부 파일)
- 릴리스한 commit은 바꾸지 않는다. 고치면 **새 버전**
- 오늘 산출: `v0.1.0` → 짝 팀이 재현 → Issue

**질문:** `main`의 최신 commit과 태그 `v0.1.0`이 가리키는 commit은 무엇이 다른가?

---

## 3–6분 · Semantic Versioning

```text
v0.1.0
 │ │ └── PATCH  문서·버그 수정, 동작 호환
 │ └──── MINOR  기능 추가, 하위 호환
 └────── MAJOR  호환 깨짐 (0.x 는 아직 불안정 단계)
```

- 첫 공개는 `0.1.0`. 교차 재현 결함을 고치면 `0.1.1`, 기능이 늘면 `0.2.0`
- 한곳에서만 정한다: `pyproject.toml` version = 태그 = `CITATION.cff` version
- 어댑터 실험 이름(`adapters/run-002`)은 릴리스 버전이 아니다

**질문:** README 오타만 고쳤다. 세 자리 중 무엇이 오르는가?

---

## 6–9분 · 태그와 GitHub Release

```powershell
uv run python tag_notes.py --repo C:\classwork\team-a-repo --version 0.1.0 --promote
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
git show v0.1.0 --stat | Select-Object -First 8
```

- `-a` 주석 태그: Tagger·날짜·메시지가 남는다. 가벼운 태그는 쓰지 않는다
- `tag_notes.py`: `[Unreleased]` → `[0.1.0] - 날짜`, `outputs/release-notes-v0.1.0.md`
- GitHub → Releases → Draft a new release → 태그 선택 → 노트 붙여넣기 → Publish
- 릴리스 노트 = 변경 내역 + 실행 3줄 + 제한 + 피드백 통로

---

## 9–12분 · 재현 검증 — 처음 보는 사람이 되어

```powershell
.\reproduce_by_stranger.ps1 -Source https://github.com/team-b/local-ai-helper -Tag v0.1.0
```

- 규칙: 새 폴더, README만, 팀원에게 묻지 않기, 타이머 10분
- clone → checkout 태그 → `uv sync --frozen` → `.env` → 실행 → 예시 → 테스트
- 막힌 곳 = README의 결함. 30초만 시도하고 기록, 고쳐 주지 않는다
- **내 PC에서 되는 것은 증거가 아니다**

**질문:** `uv sync --frozen`이 "uv.lock 없음"으로 실패했다. 누구의 문제인가?

---

## 12–15분 · 릴리스 후 고칠 때

| 상황 | 하지 않는 것 | 하는 것 |
|---|---|---|
| README 오타 | 태그를 지우고 다시 만들기 | 고치고 `v0.1.1` |
| 실행 실패 결함 | 릴리스 commit 수정 후 force push | 수정 commit → CHANGELOG → `v0.1.1` |
| 새 기능 요청 | 패치 버전에 끼워 넣기 | `[Unreleased]`에 쌓아 `v0.2.0` |

- 이미 받아 간 사람이 있다. **push한 태그는 옮기지 않는다**
- 패치 릴리스도 같은 절차: CHANGELOG 승격 → 태그 → Release 노트

---

## 15–17분 · 모델·어댑터 산출물 배포

- 가중치는 코드 저장소에 커밋하지 않는다(용량·이력 부담)
- Release asset: 작은 어댑터(`adapter_model.safetensors` + `adapter_config.json`) 첨부, README에 SHA256
- Hugging Face Hub: 모델 저장소 + Model Card frontmatter(`license`·`base_model`), `huggingface_hub` Python API로 업로드(확장 과제)
- 먼저 확인: 기반 모델·데이터 라이선스가 **배포를 허용하는가**
- 큰 가중치·GGUF 변환은 이번 학기 범위 밖

**질문:** 어댑터만 첨부하면 받는 사람은 무엇을 더 준비해야 하는가?

---

## 17–20분 · 실습 인계

[2교시 실습 — 릴리스 생성과 교차 재현](lab.md#2교시-실습--릴리스-생성과-교차-재현)

완료 조건:

1. `v0.1.0` 주석 태그가 push되고 GitHub Release에 릴리스 노트가 있다.
2. 짝 팀 릴리스를 새 폴더에서 재현한 `repro-log-*.md`에 단계별 초와 결과가 있다.
3. 막힌 단계마다 환경·명령·출력·README 위치가 있는 Issue를 등록했다(막히지 않았으면 총 소요 시간을 전달했다).

실습 30분 뒤 휴식 10분, 휴식 후 3교시.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 커뮤니티 피드백과 시연 준비

---

## 0–3분 · 피드백은 릴리스의 첫 결과물

- 이어받는 것: 2교시 릴리스 URL, 우리 팀이 받은 Issue, 우리가 남긴 Issue
- 첫 Issue가 오면 프로젝트는 "혼자 쓰는 코드"에서 벗어난다
- 오늘: 분류 → 재현 시도 → 응답 → 결정 기록 → 3분 시연 리허설
- 응답 속도보다 **응답의 예측 가능성**(라벨·결정·반영 버전)

**질문:** 응답 없이 열린 채 남은 Issue는 처음 보는 사람에게 무엇을 말하는가?

---

## 3–6분 · triage 라벨 5개

| 라벨 | 뜻 | 붙이는 기준 |
|---|---|---|
| `bug` | 문서대로 했는데 다르게 동작 | 재현 명령·출력이 있고 우리 PC에서도 재현됨 |
| `docs` | 코드는 맞고 README가 틀리거나 부족 | 문서만 고치면 해결 |
| `enhancement` | 새 기능·개선 제안 | 현재 동작은 정상 |
| `question` | 사용법 질문 | 답이 docs 수정으로 이어질 수 있음 |
| `needs-repro` | 재현 정보 부족 | 환경·명령·출력 중 하나라도 없음 |

제목만 보고 붙이지 않는다. 정보가 부족하면 결정하지 말고 `needs-repro`만 붙인다.

---

## 6–9분 · 응답 예절과 기대 관리

```text
[재현 성공·수용]   같은 명령으로 재현했다 → 원인 한 줄 → 반영 버전
[재현 실패]        우리 환경의 결과 → 차이를 찾을 정보 요청 (needs-repro)
[보류·범위 밖]     이유 → 우회 방법 → DECISIONS.md 에 후보로 기록
```

- 사람이 아니라 동작에 대해 말한다. 기한을 약속하지 않는다
- "제 PC에서는 됩니다"로 끝내지 않는다
- 재현 불가 보고에 요청할 세 가지: 버전 출력, 실행한 명령 전체, 오류 시점의 전체 출력

**질문:** 보고자가 홈 경로와 실명이 든 출력을 붙였다. 먼저 무엇을 하는가?

---

## 9–12분 · 반영 결정 기록

```markdown
| Issue | 요약 | 라벨 | 결정 | 근거 | 반영 |
|---|---|---|---|---|---|
| #3 | uv sync --frozen 실패 | bug | 수용 | uv.lock 미커밋, 재현됨 | v0.1.1 |
| #4 | GPU 없이 실행 지원 | enhancement | 보류 | 범위 밖, 소형 모델 안내로 대체 | 미정 |
```

- 수용·보류·거절 모두 `DECISIONS.md`에 적는다. 거절에도 근거
- 수용했지만 이번 학기에 못 고치면 "수용 · 반영 미정"과 이유
- 이 표가 4차 종합과제의 **피드백 반영 근거**다

---

## 12–15분 · 3분 시연 구성

| 구간 | 시간 | 말할 것 | 화면 |
|---|---:|---|---|
| 문제 | 0:00–0:30 | 누구의 어떤 상황, 기존 해법이 안 되는 이유 | README 첫 화면 |
| 시연 | 0:30–2:00 | 실행 명령 → 입력 1개 → 출력 1개 → 출처가 보이는 곳 | 터미널 또는 UI |
| 한계 | 2:00–2:30 | 안 되는 것 2개, 조건(VRAM·모델·데이터 라이선스) | README 「제한」 |
| 다음 | 2:30–3:00 | 받은 피드백 1건, `v0.1.1` 계획, 기여 방법 | Issue 목록 |

- 서버·모델은 미리 켜고 첫 응답을 받아 둔다. 첫 요청은 느리다
- **입력 1개·출력 1개.** 설명을 줄이지 말고 화면 전환을 줄인다

---

## 15–17분 · 질의 예상과 실패 대비

- 예상 질문 5개: 왜 이 모델 / 데이터 출처 / 재현에 걸리는 시간 / 안 되는 것 / 기여 방법
- 답의 근거는 저장소 안의 파일: `SOURCES.md`, `experiments/run-*.md`, `docs/repro/`, `FAILURE_ANALYSIS.md`, `CONTRIBUTING.md`
- 답하는 순서: 질문 재진술 → 사실(파일·수치) → 이유 → 한계·다음 조치
- 실패 대비: Ollama 응답 없음 → 사전 출력 JSON, 서비스 안 뜸 → CLI, 네트워크 없음 → 로컬 파일
- 리허설은 다른 팀원이 시계를 잰다. 3분 30초를 넘기면 시연 구간에서 줄인다

**질문:** 답의 근거가 되는 파일을 10초 안에 열 수 있는가?

---

## 17–20분 · 실습 인계

[3교시 실습 — 피드백 응답과 시연 리허설](lab.md#3교시-실습--피드백-응답과-시연-리허설)

완료 조건:

1. 받은 Issue 2건 이상에 라벨·재현 시도 결과·응답 코멘트가 있다.
2. `DECISIONS.md`에 수용·보류·거절과 근거·반영 버전이 있다.
3. 3분 시연 리허설 2회의 구간별 시간이 `docs/demo_outline.md`에 있고 2회차가 3분 30초 이내다.

실습 30분 뒤 휴식 10분. 다음 주는 최종 발표다.

---

## 이번 주 정리

```text
문서:   README 8절 · LICENSE 호환 · CONTRIBUTING · CHANGELOG · CITATION · SOURCES · (Model Card)
버전:   [Unreleased] → v0.1.0 태그(-a) → Release 노트 → 고치면 v0.1.1
재현:   새 폴더 · README만 · 10분 · 막힌 곳 = Issue
피드백: 라벨 → 재현 시도 → 응답 → DECISIONS.md → 시연 3분 리허설
```

**처음 보는 사람이 10분 안에 실행하고 Issue를 남길 수 있을 때 비로소 릴리스다.**
