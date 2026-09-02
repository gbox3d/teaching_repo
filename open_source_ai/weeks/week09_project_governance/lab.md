# 9주차 실습 — 규칙과 계획을 저장소에 커밋하라

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 이번 주는 모델을 내려받지 않는다. 3교시 `doctor` 검사는 이미 캐시된 모델 목록만 읽는다.
- GitHub 토큰은 `.env`에만 둔다. 제안서·조사표·Issue 본문에 실명·학번·토큰을 쓰지 않는다. 팀명은 `team-a`, 팀원 표시는 `student01` 같은 수업용 값을 쓴다.

## 1교시 실습 — 거버넌스 문서 분석표

### 상황

팀이 15주차까지 키울 저장소의 규칙을 정해야 한다. 팀원이 "큰 프로젝트가 하는 대로 하자"고 제안했다. 공개 프로젝트 두 개의 거버넌스 문서를 같은 표로 읽고, 우리 팀이 실제로 가져올 규칙 3개를 근거와 함께 고르라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 두 저장소에 어떤 문서가 있을지 예상표 작성 |
| 저장소 1 조사 | 5–11분 | Community Standards·`.github/`·Releases·Contributors 읽기 |
| 저장소 2 조사 | 11–17분 | 같은 순서로 두 번째 저장소 |
| 규칙 선정 | 17–24분 | 스크립트로 수치 보강, 가져올 규칙 3개와 적용 방식 |
| 검증·기록 | 24–30분 | 근거 URL 점검, 개인 저장소에 commit |

### 준비

이어받는 것: 8주차까지의 개인 저장소(2차 종합과제 제출 상태)와 GitHub 로그인. 팀(2~3명, 팀명 `team-a`)은 이 교시 시작 전에 정해 둔다.

원본 `examples/`를 훼손하지 않도록 개인 실습 폴더에 복사한다. 아래 명령은 주차 폴더(`week09_project_governance`)에서 실행한다.

```powershell
Copy-Item -Recurse examples\proposal_tools C:\classwork\week09\proposal_tools
Copy-Item examples\governance_survey_template.md C:\classwork\week09\governance_survey.md
Set-Location C:\classwork\week09\proposal_tools
Copy-Item .env.example .env
```

조사 대상은 기본값 `huggingface/transformers`, `ollama/ollama`다. 강의자가 다른 저장소를 지정하면 `.env`의 `SURVEY_REPOS`를 바꾼다.

### 문제 1 · 두 저장소를 같은 표로 읽기

1. `governance_survey.md`의 표를 열고, 조사 전에 각 항목의 **예상**(있다/없다, 대략 수치)을 먼저 적는다.
2. 저장소 1의 GitHub 페이지에서 **Insights → Community Standards**를 열어 CoC·CONTRIBUTING·이슈 템플릿·PR 템플릿·LICENSE 체크 여부를 기록하고, 각 파일을 열어 근거 URL을 적는다.
3. `.github/ISSUE_TEMPLATE/` 폴더에서 템플릿 종류 수를 세고, `CONTRIBUTING.md`에서 눈에 띄는 규칙 3개(브랜치·PR 크기·리뷰·테스트 요구 등)를 한 줄씩 옮긴다.
4. **Releases** 탭에서 최근 릴리스 5개의 날짜를 적고 평균 간격(일)을 계산한다.
5. **Issues** 탭에서 최근 Issue 3개를 열어 첫 코멘트까지 걸린 시간을 표본으로 적는다. **Insights → Contributors**에서 상위 3인의 커밋 비율을 어림한다(버스 팩터 단서).
6. 저장소 2를 같은 순서로 채운다. 수치 항목은 스크립트로 보강한다.

```powershell
uv run python repo_health.py
```

완료 조건:

- [ ] 두 저장소 모두 CoC·CONTRIBUTING·이슈 템플릿 수·PR 템플릿·라이선스가 근거 URL과 함께 있다.
- [ ] 릴리스 평균 간격, 첫 응답 시간 표본 3개, 상위 3인 커밋 비율이 있다.
- [ ] 예상과 실제가 달랐던 항목 1개를 한 문장으로 적었다.

### 문제 2 · 우리 팀이 가져올 규칙 3개

1. 두 저장소의 `CONTRIBUTING.md`·CoC·템플릿에서 우리 팀(3명, 6주)에 맞는 규칙 3개를 고른다.
2. 각 규칙에 **출처 프로젝트**, **원문 요약 한 줄**, **우리 팀 적용 방식**(무엇을 언제 누가)을 적는다.
3. 큰 프로젝트에는 있지만 우리 팀이 **가져오지 않을** 규칙 1개와 그 이유를 적는다.

완료 조건:

- [ ] 규칙 3개에 출처·요약·적용 방식이 모두 있다.
- [ ] 가져오지 않을 규칙 1개와 이유가 있다.
- [ ] `governance_survey.md`를 개인 저장소에 commit했다(`Add governance survey`).

### 단계별 힌트

<details>
<summary>힌트 1 — Community Standards 메뉴가 보이지 않는다</summary>

저장소 페이지 상단의 **Insights** 탭 안에 있다. 왼쪽 목록에서 **Community Standards**를 고른다. 비공개 저장소나 fork에는 표시되지 않으므로 원본 저장소에서 연다.
</details>

<details>
<summary>힌트 2 — `repo_health.py`가 403 또는 rate limit 메시지를 낸다</summary>

인증 없는 GitHub API는 시간당 요청 수가 적고 같은 공인 IP를 쓰는 실습실에서는 금방 소진된다. 메시지에 적힌 재시도 시각을 확인하고, 스크립트 없이 브라우저 값으로 표를 완성한다. 개인 토큰이 있으면 `.env`의 `GITHUB_TOKEN`에만 넣는다. 토큰을 명령줄이나 문서에 쓰지 않는다.
</details>

<details>
<summary>힌트 3 — 릴리스가 너무 많아 간격을 계산하기 어렵다</summary>

최근 5개만 쓴다. 첫 번째와 다섯 번째 날짜 차이를 4로 나누면 평균 간격이다. 사전 릴리스(pre-release)는 제외했는지 표에 적는다.
</details>

### 검증

- 정상: `outputs/health-*.json`의 `community_files`에 브라우저에서 확인한 파일이 같은 값으로 들어 있다.
- 경계 또는 실패: `.env`의 `SURVEY_REPOS`에 존재하지 않는 저장소를 넣고 실행해 "찾을 수 없음" 메시지가 사람이 읽을 형태로 나오는지 확인한다.
- 설명: "이 두 프로젝트 중 어느 쪽이 버스 팩터가 낮은가, 그 근거는 무엇인가"를 한 문장으로 쓴다.

### 확장 문제

1. 두 저장소의 최근 merge된 PR 3개를 열어 리뷰어 수와 첫 리뷰까지 걸린 시간을 표에 추가한다.
2. 두 저장소가 채택한 의사결정 모델(BDFL·위원회·재단)을 추정하고 근거 문서(GOVERNANCE 파일, 재단 페이지, 메인테이너 목록) URL을 적는다.

## 2교시 실습 — 팀 제안서 초안

### 상황

팀은 "로컬 AI 도우미"를 만들기로 했지만 아직 아이디어 수준이다. 12주차 베타와 15주차 릴리스를 심사할 사람이 읽을 제안서를 써야 한다. 문제 한 문장부터 시작해 사용자, Must 3개, 모델·데이터 후보, 위험 2개를 근거와 함께 채우라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 팀 문제 후보 2개를 한 문장씩, 하나 선택 |
| 사용자·범위 | 5–13분 | 사용자 한 명(상황·해법·한계·성공 신호), Must 3개·Should·Could |
| 모델·데이터 | 13–21분 | 모델 후보 2개(라이선스·VRAM), 데이터 후보(확보·라이선스·개인정보) |
| 위험 | 21–25분 | 위험 2개의 신호와 완화책 |
| 검증·기록 | 25–30분 | 체크리스트 점검, 팀 저장소 또는 공유 문서에 저장 |

### 준비

이어받는 것: 1교시 `governance_survey.md`의 "우리 팀이 가져올 규칙 3개"와 `C:\classwork\week09\proposal_tools` 복사본(`.env` 포함).

팀원 중 한 명이 제안서 파일을 만들고 나머지는 같은 문서를 나누어 채운다. 아직 팀 저장소가 없으므로 이번 교시에는 한 사람의 개인 저장소 브랜치나 공유 문서에 두고, 3교시에 팀 저장소 `docs/proposal.md`로 옮긴다.

주차 폴더(`week09_project_governance`)에서 양식을 복사한 뒤 도구 폴더로 이동한다.

```powershell
Copy-Item proposal_template.md C:\classwork\week09\proposal.md
Set-Location C:\classwork\week09\proposal_tools
```

5주차 `model_cards.md`·`SOURCES.md`, 4주차 `model_report.md`, 7주차 `evalset.json`을 열어 둔다. 모델·데이터 후보는 여기서 가져온다.

### 문제 1 · 문제·사용자·범위

1. 팀 문제 후보 2개를 "[사용자]가 [상황]에서 [문제]를 겪는다. 지금은 [기존 해법]으로 해결하지만 [한계]가 있다" 틀로 적는다. 12주차까지 베타를 만들 수 있는 쪽을 고른다.
2. 사용자 한 명을 표로 적는다: 사용자, 상황, 현재 해법, 한계, 성공 신호(12주차에 측정 가능한 것).
3. Must 3개를 적는다. 각 Must는 "12주차 베타에서 무엇을 보여 주면 충족인가"가 한 줄로 따라온다.
4. Should 2개, Could 1개를 적고 마일스톤 M3 이후로 둔다고 표시한다.

완료 조건:

- [ ] 문제 한 문장에 사용자·상황·문제·기존 해법·한계가 모두 있다.
- [ ] 성공 신호가 측정 가능한 문장이다("답이 좋다"가 아니라 "출처 표시율 80% 이상" 같은 형태).
- [ ] Must가 정확히 3개이고 각각 확인 방법이 있다.

### 문제 2 · 모델·데이터 후보와 위험

1. 모델 후보 2개를 표로 적는다: 정확한 ID(Ollama 태그 또는 HF ID와 revision), 파라미터 수, 라이선스(SPDX ID 또는 약관 이름), 상업적 이용·재배포 조건, 근거 URL.
2. 각 후보의 VRAM을 추정한다. 4주차 실측값(`ollama ps`)이 있으면 나란히 적는다.

```powershell
uv run python vram_estimate.py --candidate "qwen3:4b,4B,4" --candidate "qwen3:0.6b,0.6B,4" --ctx 8192
```

3. 데이터 후보를 표로 적는다: 이름, 출처(자체 작성·공개·사용자 생성), 라이선스, 용도(학습·평가·RAG 문서), 확보 방법과 담당, 개인정보 점검 방법.
4. 위험 2개를 적는다: 위험, 그것이 현실이 되었음을 알려 주는 신호, 완화책, 완화 담당.

완료 조건:

- [ ] 모델 후보 2개에 라이선스 근거 URL과 VRAM 추정치(가능하면 실측치)가 있다.
- [ ] 데이터 후보에 확보 방법·담당·라이선스·개인정보 점검이 있다.
- [ ] 위험 2개에 신호·완화·담당이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — 문제 문장이 "챗봇을 만든다"로 자꾸 돌아간다</summary>

만들 것을 지우고 사용자가 지금 겪는 불편만 남긴다. "누가, 언제, 무엇 때문에 시간을 잃는가"에 답이 없으면 아직 문제가 아니다.
</details>

<details>
<summary>힌트 2 — `vram_estimate.py`의 KV 캐시가 0으로 나온다</summary>

층 수·KV 헤드 수·헤드 차원을 주지 않으면 가중치만 계산한다. 후보 형식을 `"이름,파라미터,비트,층수,KV헤드,헤드차원"`으로 늘리거나 `--layers --kv-heads --head-dim`을 준다. 값은 모델 카드의 `config.json`(`num_hidden_layers`, `num_key_value_heads`, `hidden_size ÷ num_attention_heads`)에서 읽는다.
</details>

<details>
<summary>힌트 3 — 라이선스 칸에 "오픈소스"라고만 쓰게 된다</summary>

SPDX ID(`Apache-2.0`, `MIT`)나 약관 이름(예: 커뮤니티 라이선스, RAIL 계열)을 그대로 적고, 2주차 `license_matrix.md`의 상업적 이용·재배포 열을 옮겨 온다. 라이선스가 없는 자원은 후보에서 뺀다.
</details>

### 검증

- 정상: `outputs/vram-*.md`에 후보 2개의 가중치·KV·여유·합계와 12 GB 대비 판정이 있다.
- 경계 또는 실패: 파라미터를 `70B`, 비트를 `16`으로 넣어 12 GB를 초과하는 후보가 "초과"로 판정되는지 확인하고, 잘못된 형식(`"qwen3:4b,4B"`처럼 비트 누락)에서 사람이 읽을 오류가 나오는지 확인한다.
- 설명: "두 후보 중 12주차 베타에 먼저 쓸 모델과 그 이유"를 한 문장으로 쓴다.

### 확장 문제

1. 아키텍처 텍스트 도식(사용자 → UI → FastAPI → Ollama/모델, 데이터·평가셋 위치)을 `proposal.md`에 추가한다.
2. 후보 모델 하나에 대해 `--ctx`를 2048·8192·32768로 바꿔 KV 캐시가 VRAM 판정을 어떻게 바꾸는지 표로 적는다.

## 3교시 실습 — 팀 저장소와 이슈 분해

### 상황

제안서가 있으니 이제 저장소가 필요하다. 팀 저장소를 만들고 거버넌스 문서를 배치한 뒤, 10~15주 일정을 마일스톤 3개와 Issue 8~10개로 분해하라. 마지막에는 3분 제안 발표를 타이머로 리허설한다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 마일스톤 3개 정의, Issue 후보 목록 브레인스토밍 |
| 저장소 골격 | 5–12분 | 팀 저장소 생성, 템플릿 복사, LICENSE·CoC·CONTRIBUTING commit, `doctor` 실행 |
| 이슈 분해 | 12–22분 | `issue_plan.json` 작성·검사 → 마일스톤·Issue 등록 |
| 발표 리허설 | 22–27분 | 타이머 3분, 소요 시간·빠진 항목 기록 |
| 검증·기록 | 27–30분 | 저장소 URL·Issue 목록·리허설 기록 정리 |

### 준비

이어받는 것: 2교시 `proposal.md`, 1교시 `governance_survey.md`, `C:\classwork\week09\proposal_tools` 복사본. 아래 복사 명령은 주차 폴더(`week09_project_governance`)에서 실행한다.

팀원 한 명이 GitHub에서 빈 저장소(`team-a-local-helper` 같은 이름)를 만들고 나머지 팀원을 collaborator로 추가한다. 그 사람이 템플릿을 복사해 첫 commit을 올리고, 나머지는 clone한다.

```powershell
Copy-Item -Recurse examples\project_template C:\classwork\week09\team-repo
Set-Location C:\classwork\week09\team-repo
Copy-Item .env.example .env
git init
git branch -M main
```

2교시의 `proposal.md`는 `docs/proposal.md`로 복사한다. 1교시의 규칙 3개는 `CONTRIBUTING.md`의 "팀 규칙" 절에 넣는다.

### 문제 1 · 거버넌스 문서를 갖춘 저장소 골격

1. `LICENSE_CHOICE.md`를 읽고 MIT 또는 Apache-2.0을 고른 뒤 `LICENSE` 파일을 만든다. 선택 이유 한 문장을 `README.md`의 라이선스 절에 적는다.
2. `CODE_OF_CONDUCT.md`의 신고 경로, `CONTRIBUTING.md`의 "팀 규칙" 절(1교시 규칙 3개), `pyproject.toml`의 `name`을 팀 값으로 바꾼다.
3. 저장소 골격이 실행되는지 확인한다. Ollama가 꺼져 있으면 연결 실패가 사람이 읽을 메시지로 나와야 한다.

```powershell
uv run team-project doctor
```

4. `git status`로 `.env`가 추적되지 않는지 확인한 뒤 첫 commit(`Add project skeleton with governance files`)을 만들고 push한다.
5. GitHub에서 Insights → Community Standards를 열어 체크 항목이 채워졌는지 본다.

완료 조건:

- [ ] LICENSE, CODE_OF_CONDUCT.md, CONTRIBUTING.md, `.github/ISSUE_TEMPLATE/*.md`, `.github/PULL_REQUEST_TEMPLATE.md`가 push되었다.
- [ ] `uv run team-project doctor`의 결과 파일이 `outputs/`에 생겼고 `.env`·`outputs/`는 커밋되지 않았다.
- [ ] Community Standards에서 CoC·CONTRIBUTING·이슈 템플릿·PR 템플릿·LICENSE가 체크되었다.

### 문제 2 · 마일스톤 3개와 Issue 8~10개, 그리고 3분 리허설

1. `examples/milestone_plan_template.md`를 `docs/milestones.md`로 복사해 M1(11주)·M2(12주)·M3(15주)의 "닫히는 조건"을 적는다.
2. `proposal_tools/issue_plan.sample.json`을 `issue_plan.json`으로 복사해 팀의 Issue 8~10개로 바꾼다. 각 Issue에 제목, 마일스톤, 담당(`student01` 등 수업용 GitHub 계정), 예상 일수(3일 이하), 완료 조건이 있어야 한다.
3. 검사 스크립트를 돌려 경고를 0개로 만든다.

```powershell
Set-Location C:\classwork\week09\proposal_tools
uv run python issue_plan_check.py --plan issue_plan.json
```

4. GitHub에 마일스톤 3개와 Issue를 등록한다. 브라우저에서 직접 만들거나, 팀 저장소 토큰이 `.env`에 있으면 스크립트로 올린다(`--dry-run`으로 먼저 확인).

```powershell
uv run python issue_plan_push.py --plan issue_plan.json --repo team-a/team-a-local-helper --dry-run
uv run python issue_plan_push.py --plan issue_plan.json --repo team-a/team-a-local-helper
```

5. 타이머 3분을 켜고 제안 발표를 한 번 한다. 발표자 1명, 나머지는 `proposal_rubric.md`를 보며 빠진 항목을 적는다. `docs/rehearsal.md`에 소요 시간, 빠진 항목, 예상 질문 2개를 기록한다.

완료 조건:

- [ ] 마일스톤 3개와 Issue 8~10개가 GitHub에 있고 각 Issue에 완료 조건·담당·마일스톤이 있다.
- [ ] 팀원 각자가 최소 1개 Issue의 담당이며 본인이 등록한 Issue URL을 적었다.
- [ ] `docs/rehearsal.md`에 소요 시간·빠진 항목·예상 질문 2개가 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — `uv run team-project doctor`가 "command not found" 또는 import 오류를 낸다</summary>

`pyproject.toml`의 `[project.scripts]`와 `src/team_project/` 폴더 이름이 일치해야 한다. 패키지 이름을 바꿨다면 `src/` 아래 폴더 이름, `cli.py`의 import, `[tool.hatch.build.targets.wheel]`의 경로를 함께 바꾼다. 바꾼 뒤 `uv sync`를 다시 실행한다.
</details>

<details>
<summary>힌트 2 — `issue_plan_check.py`가 "마일스톤 없음" 경고를 낸다</summary>

Issue의 `milestone` 문자열이 `milestones` 배열의 `name`과 글자 단위로 같아야 한다. 공백·번호 표기(`M1`과 `M1 `)를 확인한다.
</details>

<details>
<summary>힌트 3 — `issue_plan_push.py`가 401·404·422를 낸다</summary>

401은 토큰이 없거나 틀린 것, 404는 저장소 이름이 틀렸거나 토큰에 그 저장소 권한이 없는 것, 422는 담당자가 collaborator가 아닌 경우가 대부분이다. 스크립트는 422에서 담당자를 비우고 다시 시도하므로, 등록 후 GitHub에서 담당자를 손으로 지정한다. 토큰은 `.env`에만 둔다.
</details>

### 검증

- 정상: `outputs/doctor-*.json`에 Ollama 연결 결과와 모델 목록(또는 연결 실패 사유)이 있고, `outputs/issue_plan_report.md`의 경고가 0개다.
- 경계 또는 실패: `issue_plan.json`에서 Issue 하나의 `done_when`을 비우고 검사해 경고가 나오는지 확인한 뒤 되돌린다. Ollama를 끈 상태에서 `doctor`를 실행해 연결 실패가 예외 스택이 아니라 한 줄 메시지로 나오는지 확인한다.
- 설명: "우리 팀에서 Issue 하나가 3일을 넘기면 어떻게 쪼갤 것인가"를 한 문장으로 쓴다.

### 확장 문제

1. 팀원 한 명이 Issue 하나를 골라 `feat/<번호>-...` 브랜치에서 `README.md` 한 줄을 고치고 PR을 열어 다른 팀원이 리뷰·merge한다. PR 템플릿이 자동으로 채워지는지 확인한다.
2. `CONTRIBUTING.md`의 응답 기대 시간(48시간)을 팀 상황에 맞게 조정하고, 그 근거를 1교시 조사표의 첫 응답 시간과 비교해 적는다.

## 제출 체크

- `governance_survey.md`: 공개 프로젝트 2개 분석표, 예상과 달랐던 항목 1개, 우리 팀이 가져올 규칙 3개와 가져오지 않을 규칙 1개
- 팀 저장소 URL: LICENSE·CoC·CONTRIBUTING·이슈·PR 템플릿, `docs/proposal.md`, `docs/milestones.md`
- `outputs/vram-*.md`: 모델 후보 2개의 VRAM 추정과 12 GB 판정(개인 폴더, 커밋하지 않음)
- 팀 저장소 Issue 목록: 마일스톤 3개, Issue 8~10개, 본인이 등록한 Issue URL
- `docs/rehearsal.md`: 3분 리허설 소요 시간, 빠진 항목, 예상 질문 2개
- 선택: 확장 문제 결과
