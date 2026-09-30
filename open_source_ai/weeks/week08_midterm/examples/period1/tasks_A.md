# 모의 실기 A — 프로젝트 복구와 판별 문항

공개 동형 모의 문제다. 실제 실기 패킷의 문항·값·정답이 아니다. 제한 시간은 30분이며, 답안은 실습 폴더의 `answers_A.md`에 맨 아래 양식으로 쓴다. 허용 자료·AI 도구 범위는 실제 시험에서는 시험 공지를 따른다.

## A-1 · 깨진 uv 프로젝트 복구

### 요구사항

`make_broken_repo.ps1`이 만든 `week08-mock-a` 저장소를 다음 상태로 만든다.

1. `uv sync`가 오류 없이 끝나고 의존성이 설치된다.
2. `uv run python report.py`가 `outputs/report.json`을 만든다.
3. `.env`는 Git 추적에서 빠지고, `.gitignore`와 값이 비어 있는 `.env.example`이 추적된다.
4. 위 변경이 한 commit으로 정리되어 있고 `git status`가 clean이다.

`report.py`는 고치지 않는다. 그 파일에는 오류가 없다.

### 완료 조건

- [ ] `uv sync` 출력의 `Resolved N packages`에서 N이 2 이상이고 설치 줄이 보인다.
- [ ] `uv run python report.py`의 종료 코드가 0(연결됨) 또는 2(연결 실패)다.
- [ ] `outputs/report.json`에 `host`, `model`, `ollama_reachable`, `model_available`, `hf_token_present` 키가 있다.
- [ ] `git ls-files`에 `.env`가 없고 `.gitignore`, `.env.example`이 있다.
- [ ] `git status`가 clean이다.

### 검증 순서

```powershell
uv sync
uv run python report.py
$LASTEXITCODE
Get-Content outputs\report.json
git ls-files
git status
git log --oneline
```

### 답안에 적을 것

고친 항목마다 한 줄: `증상(첫 오류 메시지의 핵심) → 원인 → 고친 내용`. 그리고 "`.env`를 `git rm --cached`로 뺀 뒤에도 남아 있는 문제"를 한 줄로 적는다.

## A-2 · 라이선스 판별 3문항

각 문항은 **판단 + 근거 + (있으면) 출처** 세 줄 이내로 답한다. 확신이 없으면 "확인할 문서"를 적는다.

### A-2-1 · 모델 라이선스

모델 M의 Hugging Face 저장소에는 가중치가 공개되어 있고, 모델 카드의 라이선스 항목에 "M 커뮤니티 라이선스"라고 적혀 있다. 라이선스 본문에는 다음 조항이 있다.

- (a) 월간 활성 사용자가 일정 수를 넘는 서비스는 별도 계약이 필요하다.
- (b) 파생 모델 이름에 원 모델명을 포함해야 한다.
- (c) 허용 정책에 적힌 특정 용도로는 쓸 수 없다.

질문: 이 모델을 OSI 오픈소스 정의 기준으로 "오픈소스"라고 부를 수 있는가? 판단과 근거(정의의 어떤 항목과 충돌하는지)를 적고, 교재에서 이런 모델을 부르는 표현을 적는다.

### A-2-2 · 의존성 라이선스

내 RAG 미니프로젝트를 MIT로 공개하려 한다. 코드에서 `import`해 함께 배포하는 라이브러리 L은 `GPL-3.0-only`이고, 나머지 의존성은 `Apache-2.0`·`MIT`·`BSD-3-Clause`다.

질문: 다음 세 선택지 각각에 대해 가능·불가능·조건부를 판단하고 근거를 한 줄씩 적는다. 라이선스는 SPDX 식별자로 표기한다.

- (a) 그대로 MIT로 공개한다.
- (b) 프로젝트를 `GPL-3.0-or-later`로 공개한다.
- (c) L을 `Apache-2.0` 라이선스의 대체 라이브러리로 교체하고 MIT를 유지한다.

### A-2-3 · 데이터 라이선스

RAG 문서로 넣으려는 공개 데이터셋 D의 Dataset Card에 `license: cc-by-nc-4.0`이 적혀 있다.

질문:

- (a) 수업 프로젝트(비상업)에서 D를 쓸 수 있는가?
- (b) 같은 프로젝트를 나중에 유료 서비스로 바꾸면 어떻게 되는가?
- (c) `SOURCES.md`에 D를 기록할 때 반드시 적을 항목 4가지.

## A-3 · Git 브랜치·PR 상황 문제

팀 저장소 `origin`의 `main`은 보호되어 직접 push할 수 없다. 당신은 `feature/config-loader` 브랜치에서 `config.py`를 고쳐 push하고 PR을 열었다. 리뷰어가 두 가지를 알렸다.

1. PR diff에 `.env`가 들어 있다.
2. 그 사이 다른 PR이 `main`에 merge되어 `config.py`에서 충돌이 난다.

현재 위치는 `feature/config-loader`이고 working tree는 clean이다.

질문:

- (a) 지금부터 실행할 Git 명령을 순서대로 쓰고, 각 명령이 바꾸는 영역(working tree / stage / commit / remote)을 괄호로 붙인다.
- (b) `.env`를 지우는 commit을 추가로 push하면 리뷰어의 지적 1이 해결되는가? 판단과 근거.
- (c) 충돌 표시(`<<<<<<<`, `=======`, `>>>>>>>`)를 만났을 때 하지 말아야 할 행동 1가지.

## `answers_A.md` 양식

```markdown
# 모의 실기 A 답안 — student01

## A-1 복구 기록

| 순서 | 증상(첫 오류의 핵심) | 원인 | 고친 내용 |
|---:|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |

`.env`를 추적에서 뺀 뒤에도 남는 문제:

마지막 commit id:

## A-2 라이선스

### A-2-1
판단:
근거:
출처:

### A-2-2
(a) 판단 / 근거:
(b) 판단 / 근거:
(c) 판단 / 근거:

### A-2-3
(a):
(b):
(c) 항목 4가지:

## A-3 Git 상황

(a) 명령 순서:
1. `...` (영역)
2. `...` (영역)
3. `...` (영역)
4. `...` (영역)

(b) 판단 / 근거:
(c):

## 못 끝낸 항목 (증상·관찰·시도)
```
