# 14주차 실습 — 릴리스하고, 재현받고, 응답하라

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 다른 팀 저장소에는 Issue 외의 쓰기(push·PR)를 하지 않는다. push한 릴리스 태그는 지우거나 옮기지 않는다.
- 실습 시간에 모델을 내려받지 않는다. 이번 주 예제는 모델·GPU 없이 동작하며, 3교시 시연 리허설에서만 사전 캐시된 모델을 쓴다.

## 1교시 실습 — 릴리스 문서 세트 보완

### 상황

팀 저장소는 13주차에 pytest·ruff·CI가 초록불이 되었다. 2교시에 짝 팀이 우리 README만 보고 재현을 시도한다. 그 전에 처음 보는 사람이 읽을 문서 세트를 갖추고, 모델·데이터·의존성 라이선스가 우리 릴리스에 어떤 조건을 거는지 문서에 적어야 한다.

이어받는 것: 팀 저장소 clone본(`main` 최신), 9주차 템플릿의 LICENSE·CONTRIBUTING·CODE_OF_CONDUCT, 5·8주차 `SOURCES.md`, 10·11주차 실험 기록·데이터 카드·평가 결과.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 점검 전 예상: FAIL이 날 항목 3개와 이유 적기 |
| 자동 점검 | 4–9분 | `release_check.py` 실행, FAIL·WARN 목록 기록, 예상과 비교 |
| 문서 보완 | 9–22분 | README 8개 절·AI 도구 사용 내역, `SOURCES.md` 최종화, CHANGELOG `[Unreleased]` 정리, 어댑터 공개 팀은 `MODEL_CARD.md` |
| 재점검·commit | 22–26분 | 재실행으로 FAIL 0 확인, 보완 commit·push |
| 검증·기록 | 26–30분 | `release_checklist.md` 1·2절 결과 채우기, `outputs/` JSON 경로 기록 |

### 준비

원본을 훼손하지 않도록 `examples/`를 개인 실습 폴더에 복사한다. 팀 저장소 clone본은 `C:\classwork\team-a-repo`처럼 별도 폴더에 있다고 가정한다.

```powershell
New-Item -ItemType Directory week14-practice
Copy-Item -Recurse <교재 경로>\week14_release_feedback\examples\* .\week14-practice\
Set-Location .\week14-practice\release_check
Copy-Item .env.example .env
uv sync
```

`.env`의 `RELEASE_REPO`에 팀 저장소 경로를 적으면 아래 명령의 `--repo`를 생략할 수 있다. 팀 저장소에서는 `git switch -c release/v0.1.0-docs`로 문서 보완 브랜치를 만들어 작업하고, 끝나면 PR 또는 직접 merge한다(팀 규칙을 따른다).

### 문제 1 · 자동 점검과 README 보완

1. 실행 전에 예상표를 적는다. `release_check.py`가 보는 항목(README 8개 절, AI 도구 사용 내역, LICENSE, CONTRIBUTING, CHANGELOG, CITATION, SOURCES, `.env` 추적, version과 태그, `uv.lock`) 중 FAIL이 날 것 3개와 이유.
2. 점검을 실행하고 화면의 FAIL·WARN을 옮겨 적은 뒤 예상과 비교한다.

   ```powershell
   uv run python release_check.py --repo C:\classwork\team-a-repo --tag v0.1.0
   ```

3. README를 `release_kit/README_TEMPLATE.md`의 8개 절 순서로 보완한다. 절 제목에 단서 단어(소개·왜·설치·실행·예시·제한·라이선스·출처)를 남긴다. 「설치」·「실행」 절의 명령은 새 PowerShell 창을 열어 복사·붙여넣기로 한 번 실행해 본다.
4. 「AI 도구 사용 내역」 표를 채운다. 파일·범위마다 AI 도구가 만든 것과 사람이 검증·수정한 것을 나눈다. 없는 항목은 "없음"이라고 적는다.
5. 없는 파일을 만든다. CONTRIBUTING.md는 9주차 템플릿에 Issue 양식·브랜치·PR 규칙·첫 응답 담당이 있는지 확인하고, CITATION.cff는 `release_kit/CITATION.cff`를 복사해 `title`·`version`·`authors`·`repository-code`를 팀 값으로 바꾼다. 어댑터를 공개하는 팀은 `MODEL_CARD_TEMPLATE.md`로 `MODEL_CARD.md`를 만들고 `--require-model-card`로 다시 점검한다.
6. 다시 실행해 FAIL이 0인지 확인한다. 남는 WARN(예: `uv.lock` 없음)은 이유와 처리 계획을 적는다.

완료 조건:

- [ ] `outputs/release-check-*.json`의 `counts.fail`이 0이다.
- [ ] README 「설치」·「실행」 명령을 새 창에서 실행해 오류가 없었다.
- [ ] AI 도구 사용 내역 표에 파일·범위가 2행 이상 있다.

### 문제 2 · SOURCES.md 최종화와 CHANGELOG 정리

1. `SOURCES.md`의 행마다 이름·버전(revision 또는 태그)·라이선스·SPDX ID·용도·변경 내용·URL이 있는지 확인한다. 빈 칸은 모델 카드·데이터 카드·`pyproject.toml`에서 찾아 채운다.
2. 라이선스 호환을 판단한다. copyleft(GPL 계열)·NC·SA 조건이 있는 항목을 표시하고, 우리 릴리스에 적용되는 가장 제한적인 조건을 한 문장으로 README 「제한」과 「라이선스」 절에 적는다. 예: "학습 데이터가 CC-BY-NC-4.0이므로 어댑터는 비상업 용도로만 배포한다."
3. CHANGELOG `[Unreleased]`를 Keep a Changelog 형식으로 정리한다. `git log --oneline`을 보되 commit 제목을 복사하지 않고 Added / Changed / Fixed 아래에 사용자 관점 문장으로 다시 쓴다. 관련 Issue 번호를 붙인다.
4. `pyproject.toml`의 `version`이 `0.1.0`인지, CITATION.cff의 `version`이 같은지 확인한다.
5. 보완을 commit·push한다. 메시지는 `Prepare release docs for v0.1.0`. `release_kit/release_checklist.md`를 팀 저장소 `docs/release_checklist.md`로 복사해 1·2절의 「결과」를 채우고 같이 commit한다.

완료 조건:

- [ ] `SOURCES.md` 모든 행에 라이선스·SPDX ID·URL이 있다.
- [ ] README 「제한」 절에 가장 제한적인 라이선스 조건이 한 문장으로 있다.
- [ ] `[Unreleased]`에 사용자 관점 항목이 3개 이상이고 보완 commit이 push되었다.

### 단계별 힌트

<details>
<summary>힌트 1 — 절은 다 있는데 readme.sections가 FAIL이다</summary>

도구는 `#`으로 시작하는 제목 줄만 본다. 제목에 단서 단어가 없으면(예: "Getting Started") 찾지 못한다. 제목을 "설치 (Getting Started)"처럼 바꾸거나, `release_check.py`의 `README_SECTIONS`에 팀이 쓰는 단어를 추가한다. 본문에 내용이 있어도 제목이 없으면 처음 보는 사람도 못 찾는다.
</details>

<details>
<summary>힌트 2 — env.tracked가 FAIL이다</summary>

`.env`가 commit되어 있다. `git rm --cached .env` → `.gitignore`에 `.env`가 있는지 확인 → commit. 이력에는 남으므로 안에 있던 토큰은 회전하고, 13주차 `security_check.ps1`로 다른 비밀이 없는지 검사한다.
</details>

<details>
<summary>힌트 3 — 어떤 라이선스가 copyleft·NC인지 모르겠다</summary>

SPDX ID로 본다. `GPL-*`·`AGPL-*`·`LGPL-*`는 copyleft, `CC-BY-NC-*`는 비상업, `CC-BY-SA-*`는 동일조건. Llama·Gemma 같은 커뮤니티 라이선스는 SPDX ID가 없으므로 `LicenseRef-Llama-3-Community`처럼 적고 URL과 핵심 조건(사용자 수 제한, 재배포 표기 의무)을 옆에 적는다.
</details>

### 검증

- 정상: `release_check.py` 종료 코드 0, FAIL 0. README 「설치」·「실행」 명령이 새 창에서 동작한다.
- 경계 또는 실패: 일부러 `.env`를 만들어 `git add .env`만 한 상태에서 점검을 실행하면 `env.tracked`가 FAIL로 바뀐다. `git restore --staged .env` 뒤 다시 PASS가 되는지 확인한다.
- 설명: "도구가 PASS를 줬지만 사람이 확인해야 하는 항목"을 하나 골라 그 이유를 한 문장으로 적는다.

### 확장 문제

1. `release_check.py`의 `README_SECTIONS`에 "GPU 없는 대체 경로" 항목을 추가하고 팀 README를 다시 점검해 그 절을 채운다.
2. CODE_OF_CONDUCT.md에 Contributor Covenant 채택 문구와 연락 통로(수업용 값)가 있는지 확인하고 부족하면 보완한다.

## 2교시 실습 — 릴리스 생성과 교차 재현

### 상황

문서 세트가 갖춰졌다. 팀 저장소를 `v0.1.0`으로 릴리스하고, 짝 팀은 우리 README만 보고 새 폴더에서 10분 안에 재현한다. 우리도 짝 팀 릴리스를 같은 방식으로 재현한다. 막힌 곳이 곧 README의 결함이며, 그것을 Issue로 보고한다.

이어받는 것: 1교시 FAIL 0 저장소(push됨), 정리된 `[Unreleased]`, 짝 팀 저장소 URL.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–3분 | 우리 README에서 남이 가장 먼저 막힐 곳 1개 예상 |
| 태그·릴리스 | 3–12분 | `tag_notes.py --promote` → commit → `git tag -a` → push → GitHub Release 생성 |
| 교차 재현 | 12–24분 | 짝 팀 릴리스를 `reproduce_by_stranger.ps1`로 재현(타이머 10분), README 실행·예시 확인 |
| 검증·기록 | 24–30분 | 막힌 단계마다 Issue 등록, `repro-log-*.md`를 `docs/repro/`에 commit |

### 준비

```powershell
Set-Location .\week14-practice\release_check
uv run python tag_notes.py --repo C:\classwork\team-a-repo --version 0.1.0
New-Item -ItemType Directory -Force C:\classwork\repro | Out-Null
```

`--promote` 없이 먼저 실행해 `outputs/release-notes-v0.1.0.md` 초안을 읽는다. 재현용 폴더 `C:\classwork\repro`는 이전 clone·가상환경이 없는 새 폴더여야 한다.

### 문제 1 · v0.1.0 태그와 GitHub Release

1. 예상을 적는다. 짝 팀이 우리 README에서 가장 먼저 막힐 곳과 그 이유 한 줄.
2. CHANGELOG를 승격한다. `git diff CHANGELOG.md`로 `[Unreleased]`가 비고 `[0.1.0] - 날짜` 절이 생겼는지 확인하고, 맨 아래 링크 줄의 `REPO_URL`을 팀 저장소 주소로 바꾼다.

   ```powershell
   uv run python tag_notes.py --repo C:\classwork\team-a-repo --version 0.1.0 --promote
   ```

3. 팀 저장소에서 commit·push하고 주석 태그를 만든다.

   ```powershell
   Set-Location C:\classwork\team-a-repo
   git add CHANGELOG.md
   git commit -m "Release v0.1.0"
   git push
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   git show v0.1.0 --stat | Select-Object -First 8
   ```

4. GitHub → Releases → Draft a new release → 태그 `v0.1.0` 선택 → 제목 `v0.1.0` → `outputs/release-notes-v0.1.0.md` 내용 붙여넣기 → Publish. 어댑터를 공개하는 팀은 라이선스가 허용할 때만 `adapter_model.safetensors`와 `adapter_config.json`을 첨부한다.
5. 릴리스 URL과 태그가 가리키는 commit id(`git rev-list -n 1 v0.1.0`)를 기록하고 짝 팀에 전달한다.

완료 조건:

- [ ] `git show v0.1.0`에 Tagger와 메시지가 있고 `git ls-remote --tags origin`에 `v0.1.0`이 보인다.
- [ ] GitHub Release 페이지에 릴리스 노트(변경 내역·실행 3줄·제한·피드백 통로)가 있다.
- [ ] `pyproject.toml` version·CITATION.cff version·태그 번호가 같다.

### 문제 2 · 짝 팀 릴리스 교차 재현

1. 타이머 10분을 켜고 시작 시각을 적는다. 새 폴더에서 스크립트를 실행한다. 팀원에게 아무것도 묻지 않는다.

   ```powershell
   Set-Location C:\classwork\repro
   <실습 폴더>\week14-practice\release_kit\reproduce_by_stranger.ps1 -Source <짝 팀 저장소 URL> -Tag v0.1.0
   ```

2. clone·checkout·`uv sync --frozen`·pytest 단계의 초와 결과가 `repro-log-<시각>.md`에 남는다. `.env`는 짝 팀 README가 시키는 대로만 채운다.
3. clone된 폴더에서 README 「실행」 절의 첫 명령과 「예시」 절의 입력을 그대로 실행한다. 막히면 30초만 시도하고 기록한 뒤 다음 단계로 간다. 코드를 읽어 원인을 찾거나 고쳐 주지 않는다.
4. 타이머를 멈추고 총 소요, 가장 먼저 막힌 곳, 그것이 코드 문제인지 문서 문제인지(근거)를 기록 파일 아래에 적는다.
5. 막힌 단계마다 Issue 1건을 짝 팀 저장소에 등록한다. 양식은 `release_kit/feedback_issue_template.md`, 제목은 `[repro] 단계 이름 — 한 줄 증상`. 환경·실행한 명령·전체 출력(홈 경로·계정 이름 삭제)·README 위치 네 가지를 반드시 넣는다. 막히지 않았으면 총 소요 시간과 환경을 Issue 또는 코멘트로 알린다.
6. `repro-log-*.md`를 우리 팀 저장소 `docs/repro/`에 commit한다.

완료 조건:

- [ ] `repro-log-*.md`에 단계별 초·결과·막힌 곳과 총 소요가 있다.
- [ ] 막힌 단계마다 환경·명령·출력·README 위치가 있는 Issue를 등록했다(없으면 성공 기록을 전달했다).
- [ ] 짝 팀이 우리 저장소에 남긴 Issue 또는 성공 기록을 확인했다.

### 단계별 힌트

<details>
<summary>힌트 1 — `tag_notes.py --promote`가 "[0.1.0] 절이 이미 있다"고 멈춘다</summary>

이미 승격된 것이다. `--promote` 없이 실행하면 그 절로 릴리스 노트를 만든다. 승격을 되돌리려면 `outputs/CHANGELOG.before-*.md` 사본을 다시 복사한다.
</details>

<details>
<summary>힌트 2 — `uv sync --frozen`이 실패한다</summary>

메시지 첫 줄을 본다. `uv.lock`이 없다거나 `pyproject.toml`과 맞지 않는다는 내용이면 릴리스 결함이다(Issue, `bug`). 패키지 다운로드·프록시·타임아웃이면 환경 문제로 기록만 한다. 우리 저장소도 `git ls-files uv.lock`으로 lock 파일이 커밋되어 있는지 지금 확인한다. 이번 주 가장 흔한 Issue다.
</details>

<details>
<summary>힌트 3 — 태그를 잘못 만들었다</summary>

push 전이면 `git tag -d v0.1.0`으로 지우고 다시 만든다. push한 뒤라면 지우거나 옮기지 않는다. 고친 commit을 올리고 `v0.1.1`을 낸다. 이미 받아 간 사람이 있을 수 있다.
</details>

<details>
<summary>힌트 4 — 네트워크가 없다</summary>

`-Source`에 짝 팀 저장소의 로컬 경로(USB·공유 폴더)를 준다. GitHub Release는 네트워크가 돌아온 뒤 만들고, 지금은 `git tag -a`와 `outputs/release-notes-v0.1.0.md`까지 한다. Issue는 `docs/issues/<번호>.md`로 적어 두었다가 옮긴다.
</details>

### 검증

- 정상: 새 폴더에서 `git checkout v0.1.0` → `uv sync --frozen` → README 「실행」 명령이 10분 안에 동작한다.
- 경계 또는 실패: 존재하지 않는 태그(`-Tag v9.9.9`)로 스크립트를 실행하면 checkout 단계에서 실패로 기록하고 멈춘다. 그 메시지가 사람이 읽을 수 있는지 확인한다.
- 설명: "짝 팀이 우리 README에서 실제로 막힌 곳과 우리가 예상한 곳이 같았는가, 달랐다면 왜인가"를 한 문장으로 적는다.

### 확장 문제

1. 릴리스에 첨부한 파일이 있으면 `Get-FileHash -Algorithm SHA256`으로 해시를 구해 릴리스 노트에 적는다.
2. 우리 릴리스를 GPU 없는 PC(또는 `OLLAMA_MODEL=qwen3:0.6b`)에서 재현해 걸린 시간과 결과를 README 「제한」 절에 적는다.

## 3교시 실습 — 피드백 응답과 시연 리허설

### 상황

우리 릴리스에 짝 팀의 Issue가 도착했다. 메인테이너로서 분류하고, 재현을 시도하고, 응답하고, 결정을 기록한다. 그리고 다음 주 발표를 위해 문제 → 시연 → 한계 → 다음 순서의 3분 시연을 리허설한다.

이어받는 것: 2교시 릴리스 URL, 우리 팀이 받은 Issue, 우리가 짝 팀에 남긴 Issue, `docs/repro/repro-log-*.md`.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–3분 | 받은 Issue마다 라벨 예상, 저장소에 라벨 5개 준비 |
| Issue 작성·응답 | 3–13분 | 짝 팀에 제안 Issue 1건 추가, 받은 Issue 2건 이상에 재현 시도·라벨·응답 |
| 결정 기록 | 13–18분 | `DECISIONS.md` 작성(수용·보류·거절, 근거, 반영 버전), commit |
| 시연 리허설 | 18–26분 | `demo_outline.md` 채우고 3분 리허설 2회 측정 |
| 검증·기록 | 26–30분 | Issue·응답 URL과 리허설 시간표 기록, commit |

### 준비

```powershell
Set-Location .\week14-practice\release_kit
Get-Content .\triage_labels.md
Copy-Item .\demo_outline.md C:\classwork\team-a-repo\docs\demo_outline.md
```

GitHub 팀 저장소 → Issues → Labels에서 `docs`·`needs-repro`를 추가한다(색은 `triage_labels.md`). 시연 리허설을 위해 Ollama 서버와 12주차 서비스를 켜고 `ollama list`로 시연 모델이 캐시되어 있는지 확인한다. 없으면 내려받지 말고 실패 대비 경로로 리허설한다.

### 문제 1 · 피드백 Issue 작성·응답·라벨

1. 예상을 적는다. 받은 Issue마다 붙일 라벨과 예상 결정(수용·보류·거절)을 먼저 적어 둔다. 아직 붙이지 않는다.
2. 짝 팀 저장소에 제안(`[proposal]`) 또는 질문(`[question]`) Issue 1건을 추가한다. 2교시의 재현 Issue와 합쳐 우리가 남긴 Issue가 2건 이상이 되게 한다. 제안에는 "처음 보는 사람이 덜 막힐" 근거를 적는다.
3. 받은 Issue 각각에 대해 읽기 → 우리 PC에서 재현 시도(10분 이내) → 라벨 1~2개 → 응답 코멘트 순으로 처리한다. 응답은 `triage_labels.md`의 세 가지 문장 예시 중 하나를 골라 우리 상황으로 바꾼다. 정보가 부족하면 `needs-repro`만 붙이고 세 가지(버전 출력·명령 전체·오류 시점 전체 출력)를 요청한다.
4. 결정을 내린다. 수용·보류·거절과 근거, 반영 예정 버전(`v0.1.1` 또는 미정)을 `DECISIONS.md` 표에 한 줄씩 적고 commit한다.
5. 수용한 문서 결함(`docs`)이 있으면 바로 고쳐 commit하고 CHANGELOG `[Unreleased]`의 Fixed에 Issue 번호와 함께 적는다. 패치 태그는 15주차 발표 전까지 찍는다.

완료 조건:

- [ ] 우리가 남긴 Issue 2건 이상, 받은 Issue 2건 이상에 라벨·응답 코멘트가 있다.
- [ ] `DECISIONS.md`에 받은 Issue 전부가 결정·근거·반영 버전과 함께 있다.
- [ ] 응답 문장에 사람에 대한 표현·기한 약속·"제 PC에서는 됩니다"가 없다.

### 문제 2 · 3분 시연 리허설

1. `docs/demo_outline.md`의 4구간(문제·시연·한계·다음) 표에서 「말할 것」·「화면」을 우리 프로젝트 값으로 바꾼다. 시연 구간은 입력 1개·출력 1개로 정한다.
2. 실패 대비 표를 채운다. 사전 실행 출력 JSON 경로, CLI 대체 명령, 네트워크 없을 때 열 로컬 파일. 경로가 실제로 존재하는지 `Test-Path`로 확인한다.
3. 서비스와 모델을 켜고 응답 1회를 미리 받아 둔다. 첫 요청은 느리다.
4. 1회차 리허설. 다른 팀원이 시계를 재고 구간이 끝날 때마다 초를 부른다. 구간별·총 시간을 리허설 기록표에 적는다.
5. 3분 30초를 넘겼으면 시연 구간에서 화면 전환을 줄인다. 설명을 줄이지 않는다. 2회차를 측정한다.
6. 예상 질문 5개의 「근거 파일」 열에 우리 저장소의 실제 경로를 적고 commit한다.

완료 조건:

- [ ] 리허설 2회의 구간별·총 시간이 `docs/demo_outline.md`에 있다.
- [ ] 2회차 총 시간이 3분 30초 이내다.
- [ ] 실패 대비 표 3행에 실제로 존재하는 파일 경로·명령이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — 받은 Issue가 없다</summary>

짝 팀이 재현에 성공했다면 성공 기록(총 소요·환경)을 Issue로 남겨 달라고 요청하고 `question` 또는 `docs`로 분류해 응답한다. 그래도 2건이 안 되면 우리 `repro-log`에서 우리가 짝 팀에 남긴 Issue를 대상으로 역할을 바꿔 응답을 연습하고, 그 사실을 `DECISIONS.md`에 적는다.
</details>

<details>
<summary>힌트 2 — 보고된 현상이 우리 PC에서 재현되지 않는다</summary>

"제 PC에서는 됩니다"로 끝내지 않는다. 우리 환경과 결과를 적고 `needs-repro`를 붙인 뒤 `feedback_issue_template.md`의 요청 문장으로 세 가지 정보를 요청한다. 결정은 정보가 올 때까지 보류로 기록한다.
</details>

<details>
<summary>힌트 3 — 시연이 3분을 넘는다</summary>

저장소 열기·서버 켜기·모델 로드는 발표 전에 끝낸다. 시연 구간은 명령 1개·입력 1개·출력 1개로 제한하고, 한계와 다음은 파일을 열어 한 줄씩 가리키는 것으로 끝낸다.
</details>

### 검증

- 정상: 받은 Issue에 라벨·재현 시도 결과·응답·결정이 있고 `DECISIONS.md`가 commit되었으며, 리허설 2회차가 3분 30초 이내다.
- 경계 또는 실패: Ollama 서버를 끈 상태에서 시연 흐름을 한 번 돌려 실패 대비 경로(사전 출력 JSON·CLI)로 3분 안에 마칠 수 있는지 확인한다.
- 설명: "수용하지 않은 Issue에 우리가 적은 근거가 보고자에게 충분한가"를 한 문장으로 적는다.

### 확장 문제

1. 수용한 Issue 하나를 실제로 고쳐 PR → 리뷰 → merge → CHANGELOG 승격 → `v0.1.1` 태그·릴리스까지 진행한다.
2. `feedback_issue_template.md`를 팀 저장소 `.github/ISSUE_TEMPLATE/feedback.md`로 넣고 새 Issue 화면에서 양식이 뜨는지 확인한다.

## 제출 체크

- `outputs/release-check-*.json`과 `docs/release_checklist.md`: 1교시 점검 결과와 WARN 처리 이유
- 문서 보완 commit과 CHANGELOG `[0.1.0]` 절: `Prepare release docs for v0.1.0`, `Release v0.1.0`
- 릴리스 URL, `git show v0.1.0 --stat` 출력 첫 8줄, 태그가 가리키는 commit id
- `docs/repro/repro-log-*.md`와 짝 팀 저장소에 등록한 Issue URL
- 받은 Issue의 응답 URL과 `DECISIONS.md`
- `docs/demo_outline.md`: 리허설 2회 시간표, 실패 대비 표, 예상 질문 근거 파일
- 선택: 확장 문제 결과(패치 태그 `v0.1.1`, Issue 템플릿 화면)
