# 1주차 실습 — 내 PC와 생태계를 점검하라

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 이번 주에는 모델을 내려받지 않는다. `ollama pull`과 Hugging Face 다운로드는 4·5주차 전에 조교가 사전 캐시한다.
- 비밀번호·토큰·실명·학번·이메일을 어떤 파일에도 쓰지 않는다. 계정 확인은 "확인함/미확인"으로만 적는다.

## 1교시 실습 — 실습환경 점검표 만들기

**이어받는 것:** 없음(첫 블록). 도구 설치는 조교가 환경 기준표에 따라 마친 상태를 전제한다.

### 상황

조교가 "다음 주부터 실습을 시작하려면 각자 PC가 준비되었는지 알아야 한다"며 점검표를 요청했다. 설치창의 "성공"이 아니라 **새 PowerShell 창에서 버전 문자열이 나오는지**가 기준이다. 실패 항목은 조치까지 적어야 조교가 도울 수 있다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 도구 5개 중 무엇이 없을지 예상, 예제 복사, 템플릿 복사 |
| 도구 점검 | 5–15분 | `env_check.ps1` 실행, 실패 항목을 수동 명령으로 재확인 |
| 계정 확인 | 15–22분 | GitHub·Hugging Face 로그인과 공개 프로필 점검 |
| 검증·기록 | 22–30분 | `env_check.md` 완성, 실패 항목 조치 문장 |

### 준비

교재 원본을 훼손하지 않도록 `examples/` 폴더를 개인 실습 폴더에 복사한다. 이 문서는 개인 실습 폴더를 `C:\classwork`로 쓴다. 강의자가 다른 경로를 안내하면 그 경로로 바꾼다. `<교재 폴더>`는 수업 자료를 받아 둔 위치다.

```powershell
New-Item -ItemType Directory -Force C:\classwork\osa-week01
Copy-Item -Recurse "<교재 폴더>\open_source_ai\weeks\week01_oss_ai_ecosystem\examples\*" C:\classwork\osa-week01\
Set-Location C:\classwork\osa-week01
Get-ChildItem
```

`README.md`(예제 안내), `env_check.ps1`, `env_check_template.md`, `oss_survey_template.md`, `first_run` 폴더가 보여야 한다.

### 문제 1 · 도구 5개 점검

1. 실행 전에 예상을 적는다. 다섯 도구(`git`, `code`, `uv`, `ollama`, `nvidia-smi`) 중 이 PC에 없을 것 같은 것과 그 이유.
2. `env_check_template.md`를 `env_check.md`로 복사한다.

   ```powershell
   Copy-Item env_check_template.md env_check.md
   ```

3. 점검 스크립트를 실행한다. 결과를 파일로도 남긴다.

   ```powershell
   .\env_check.ps1 -OutFile env_check_raw.md
   ```

4. 표의 상태가 `실패`인 항목은 같은 명령을 직접 실행해 오류 첫 줄을 읽는다(예: `uv --version`).
5. `env_check.md`의 도구 표에 버전 문자열(첫 줄 그대로)과 상태를 옮겨 적는다. GPU 표에는 이름·VRAM·드라이버 버전을, GPU가 없으면 "GPU 없음"과 대체 경로를 적는다.
6. 실패 항목마다 조치 한 문장을 적는다(예: "설치 후 새 창을 열지 않아 PATH가 갱신되지 않음 → 새 PowerShell 창에서 재확인").

완료 조건:

- [ ] 다섯 도구의 상태가 정상/실패로 표에 있다.
- [ ] GPU 이름과 VRAM(또는 "GPU 없음"과 대체 경로)이 있다.
- [ ] 실패 항목마다 조치 문장이 있다(실패가 없으면 "없음").

### 문제 2 · 계정과 공개 프로필 점검

1. 브라우저에서 GitHub에 로그인한다. 프로필 페이지에 실명·전화번호·학번 같은 불필요한 개인정보가 공개되어 있는지 본다.
2. Hugging Face에 로그인한다. 토큰은 만들지 않는다. 필요해지는 5주차에 `.env`로만 다룬다.
3. `env_check.md`의 계정 표에 "확인함/미확인"과 수업용 표시 이름만 적는다. 비밀번호·이메일은 적지 않는다.
4. `env_check_raw.md`의 표와 `env_check.md`의 도구 표가 같은 값인지 대조한다. `env_check_raw.md`에 사용자 이름이나 홈 경로가 없는지도 본다.

완료 조건:

- [ ] 두 계정의 확인 여부가 적혀 있다.
- [ ] 두 파일 어디에도 비밀번호·토큰·이메일·홈 경로가 없다.

### 단계별 힌트

<details>
<summary>힌트 1 — "이 시스템에서 스크립트를 실행할 수 없으므로" 오류로 멈춘다</summary>

실행 정책 문제다. 정책을 바꾸지 않고 이번 실행만 우회한다.

```powershell
powershell -ExecutionPolicy Bypass -File .\env_check.ps1 -OutFile env_check_raw.md
```

PowerShell 7을 쓰고 있으면 `powershell` 대신 `pwsh`를 쓴다.
</details>

<details>
<summary>힌트 2 — 설치했는데 "명령을 찾을 수 없음"이 나온다</summary>

설치 프로그램이 PATH를 바꿔도 이미 열린 창에는 반영되지 않는다. PowerShell 창을 닫고 새로 연다. 그래도 같으면 조교에게 설치 여부와 설치 방식을 확인한다. 이 상태를 "실패"로 적고 조치 칸에 "새 창에서 재확인"을 적는 것이 정답이다.
</details>

<details>
<summary>힌트 3 — nvidia-smi는 되는데 VRAM 숫자가 이상하다</summary>

`memory.total`은 MiB 단위다. 12282 MiB는 약 12 GB다. 노트북이면 내장 GPU가 아니라 NVIDIA GPU 행을 본다. 행이 두 개 나오면 둘 다 적는다.
</details>

### 검증

- 정상: 다섯 도구 모두 버전 문자열이 있고, GPU 표에 이름과 VRAM이 있다.
- 경계 또는 실패: 도구 하나가 없거나 GPU가 없는 PC에서도 점검표를 끝까지 채웠고, 조치와 대체 경로가 적혀 있다.
- 설명: "설치 프로그램이 성공했다"와 "새 창에서 버전이 나온다"가 왜 다른지 한 문장으로 적었다.

### 확장 문제

1. `env_check.ps1`의 결과 표에 PowerShell 자체 버전(`$PSVersionTable.PSVersion`)을 표시하는 행을 추가하고, 스크립트가 어느 PowerShell에서 실행되었는지 기록한다. `$PSVersionTable`은 실행할 명령이 아니라 변수라는 점에 주의한다.
2. `uv python list`를 실행해 uv가 알고 있는 Python 목록을 읽고, 환경 기준표의 Python이 그 목록에 있는지 한 문장으로 적는다. 다운로드가 시작되면 중단한다.

## 2교시 실습 — 공개 AI 프로젝트 탐색표

**이어받는 것:** 1교시의 개인 실습 폴더 `C:\classwork\osa-week01`과 브라우저의 GitHub 로그인 상태.

### 상황

팀이 다음 프로젝트에 쓸 도구를 고르려 한다. 후보 저장소 세 개가 "살아 있는 오픈소스 프로젝트"인지 판단할 근거를 같은 항목으로 조사해 달라는 요청이다. 인상이 아니라 **화면에서 읽은 값과 그 URL**을 적어야 한다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 세 저장소의 라이선스와 활동 수준을 예상, 템플릿 복사 |
| 조사 | 5–20분 | 저장소별 5개 항목을 화면에서 읽어 표에 기록 |
| OSAID 판정 | 20–25분 | 저장소마다 "어느 항목을 만족하는가" 한 문장 |
| 검증·기록 | 25–30분 | 근거 URL 대조, 표 완성 |

### 준비

```powershell
Set-Location C:\classwork\osa-week01
Copy-Item oss_survey_template.md oss_survey.md
code oss_survey.md
```

조사 대상(지정): `ollama/ollama`, `huggingface/transformers`, `vllm-project/vllm`. 강의자가 다른 저장소를 지정하면 그것을 따른다. 저장소 주소는 `https://github.com/<소유자>/<이름>`이다.

### 문제 1 · 다섯 항목 조사

각 저장소에서 다음을 읽어 표에 적는다. 값마다 확인한 화면의 URL을 근거 표에 함께 적는다.

1. 라이선스: 저장소 첫 화면 오른쪽 About의 라이선스 표기와 `LICENSE` 파일의 첫 줄. SPDX ID(`MIT`, `Apache-2.0` 등)로 적는다.
2. 최근 커밋: 기본 브랜치 파일 목록 위에 보이는 마지막 커밋 시각. 오늘 기준 며칠 전인지 적는다.
3. 열린 이슈 수: Issues 탭의 `Open` 개수.
4. 기여 가이드: `CONTRIBUTING.md`(또는 `docs/` 아래 기여 문서)가 있는가. 있으면 첫 절 제목 하나를 적는다.
5. 릴리스 주기: Releases에서 최근 태그 3개의 날짜 간격(예: "약 2주").

완료 조건:

- [ ] 세 저장소 × 다섯 항목이 모두 채워졌다.
- [ ] 값마다 근거 URL이 있다.
- [ ] 라이선스는 SPDX ID로 적혀 있다.

### 문제 2 · 오픈소스 AI 정의로 판정하기

세 저장소는 모두 **모델이 아니라 소프트웨어**다. 그래도 OSAID의 세 공개 항목(데이터 정보·코드·파라미터)에 대응시켜 본다.

1. 저장소마다 한 문장을 적는다: "이 프로젝트는 OSAID의 ___ 항목을 만족하고, ___ 항목은 프로젝트가 아니라 개별 모델의 문제다."
2. `ollama/ollama`에 대해 한 문장을 더 적는다: 도구의 라이선스와 그 도구로 실행하는 모델(예: `qwen3:8b`)의 라이선스가 같은가. 모델 라이선스는 Ollama 라이브러리에서 크기 태그 하나를 연 페이지(예: `https://ollama.com/library/qwen3:8b`)의 파일 목록 `license` 항목에서 확인한다. 모델 첫 화면(`/library/qwen3`)에는 라이선스가 표시되지 않는다.
3. 셋 중 "살아 있는 프로젝트"라고 판단하는 근거를 활동 지표 2개로 적는다.

완료 조건:

- [ ] OSAID 판정 문장 3개가 있다.
- [ ] 도구 라이선스와 모델 라이선스를 구분한 문장이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — About에 라이선스가 "View license"로만 보인다</summary>

GitHub이 자동 인식하지 못한 라이선스다. `LICENSE` 파일을 열어 첫 줄과 본문의 이름을 읽고, 표에는 파일에서 읽은 이름을 적는다. 이름이 표준 라이선스와 다르면 그 사실 자체를 적는다.
</details>

<details>
<summary>힌트 2 — 열린 이슈 수가 너무 커서 의미를 모르겠다</summary>

숫자 자체보다 비율을 본다. `Closed` 개수와 최근 이슈에 메인테이너 응답이 있는지를 함께 적으면 "활동 중"의 근거가 된다.
</details>

<details>
<summary>힌트 3 — Releases가 없거나 태그만 있다</summary>

Tags 화면의 날짜 간격으로 대신한다. 둘 다 없으면 "릴리스 없음(커밋으로만 배포)"이라고 적는 것이 정답이다.
</details>

### 검증

- 정상: 세 저장소의 라이선스가 모두 OSI 승인 라이선스의 SPDX ID로 적혀 있다.
- 경계 또는 실패: 항목 하나를 화면에서 찾지 못했을 때 "없음"과 그렇게 판단한 근거 URL을 적었다.
- 설명: "코드는 오픈소스지만 그 위에서 돌아가는 모델은 별도 조건일 수 있다"를 자기 말로 한 문장 적었다.

### 확장 문제

1. 저장소 하나의 Insights 화면에서 Contributors를 열어 상위 기여자 수와 소속(프로필 기준)을 보고, 이 프로젝트의 거버넌스가 재단형인지 기업 주도형인지 추정 근거와 함께 적는다.
2. Hugging Face에서 `Qwen/Qwen2.5-0.5B-Instruct` 모델 카드의 라이선스 표기를 찾아, 2교시에 조사한 소프트웨어 라이선스와 같은 이름인지 확인한다.

## 3교시 실습 — 첫 uv 실행과 첫 commit

**이어받는 것:** 1·2교시에서 만든 `env_check.md`, `oss_survey.md`가 있는 개인 실습 폴더 `C:\classwork\osa-week01`.

### 상황

3주차부터 모든 실습은 uv 프로젝트로 배포된다. 그 전에 "복사 → `uv run` → 결과 파일 → commit" 한 바퀴를 혼자 돌려 보라는 요청이다. 오늘 만드는 개인 저장소는 학기 내내 자라며 2주차에 GitHub와 연결된다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 보고서 JSON에 들어갈 항목 예상, `first_run` 확인 |
| uv 실행 | 4–14분 | `uv run python sysinfo.py`, `outputs/sysinfo.json`과 `.venv` 관찰 |
| 환경변수·경계 | 14–20분 | `.env`로 `OLLAMA_MODEL` 변경 후 재실행, `--no-gpu` 경계 경로 |
| 저장소·commit | 20–26분 | `git init`, 보고서 복사, `Add environment report` commit |
| 검증·기록 | 26–30분 | `git log --oneline -1`, `git status`, 미추적 항목 확인 |

### 준비

`first_run/`은 1교시에 복사한 폴더 안에 이미 있다.

```powershell
Set-Location C:\classwork\osa-week01\first_run
Get-ChildItem -Force
uv --version
```

`pyproject.toml`, `sysinfo.py`, `.env.example`, `.gitignore`, `README.md`가 보여야 한다. `.venv`와 `outputs`는 아직 없다.

### 문제 1 · 첫 uv 실행과 환경 보고서

1. 실행 전에 예상을 적는다. JSON에 GPU 이름이 들어갈지, Python이 어느 폴더의 것일지, `OLLAMA_MODEL` 값은 무엇으로 나올지.
2. 실행한다. 처음에는 uv가 `.venv`를 만들고 `python-dotenv`를 설치하는 메시지가 지나간다. 잠금 파일 `uv.lock`도 함께 생긴다. 잠금 파일의 역할은 3주차에 다루므로 오늘은 지우지 않는다.

   ```powershell
   uv run python sysinfo.py
   ```

3. `outputs\sysinfo.json`을 열어 `os`, `cpu`, `memory`, `disk`, `gpu`, `python`, `env` 항목을 읽는다. `python.in_project_venv`가 `true`인지, `python.venv_location`이 `.venv`인지 본다.
4. `.env.example`을 `.env`로 복사하고 `OLLAMA_MODEL=qwen3:0.6b`로 바꾼 뒤 다시 실행한다. `env.OLLAMA_MODEL.source`가 `기본값`에서 `.env 또는 환경변수`로 바뀌는지 확인한다.

   ```powershell
   Copy-Item .env.example .env
   code .env
   uv run python sysinfo.py
   ```

5. 경계 경로: `uv run python sysinfo.py --no-gpu`를 실행해 `gpu.available`이 `false`이고 `reason`이 적혀 있는지 본다. GPU가 없는 PC라면 옵션 없이도 같은 형태가 나온다. 확인한 뒤 **옵션 없이 한 번 더 실행해** 보고서를 이 PC의 정상 값으로 되돌린다. `outputs/sysinfo.json`은 실행할 때마다 덮어써지고, 문제 2에서 이 파일을 증거로 복사한다.

완료 조건:

- [ ] `outputs/sysinfo.json`이 있고 GPU 항목(또는 "GPU 없음" 사유)이 있다.
- [ ] 코드 수정 없이 `.env`만으로 `env.OLLAMA_MODEL.value`가 바뀌었다.
- [ ] `--no-gpu` 실행 결과를 정상 실행과 비교해 한 문장으로 적었다.

### 문제 2 · 개인 저장소와 첫 commit

수업 자료 저장소 안에서 `git init`하지 않는다. 개인 실습 폴더 `C:\classwork\osa-week01`이 저장소 루트가 된다.

1. 저장소를 만든다.

   ```powershell
   Set-Location C:\classwork\osa-week01
   git init
   git branch -M main
   git status
   ```

2. 보관할 증거를 `reports\`에 모은다. `first_run\outputs\`는 `.gitignore`로 무시되므로 **보고서를 복사해 둔다**.

   ```powershell
   New-Item -ItemType Directory -Force reports
   Copy-Item first_run\outputs\sysinfo.json reports\week01_sysinfo.json
   Move-Item env_check.md, oss_survey.md reports\
   git status
   ```

3. `git status`의 untracked 목록에 `first_run/.venv/`, `first_run/outputs/`, `first_run/.env`가 **없는지** 확인한다. 보이면 `first_run\.gitignore`가 복사되었는지 확인한다.
4. 전부 stage하고, stage된 목록을 다시 읽은 뒤 commit한다.

   ```powershell
   git add .
   git status
   git commit -m "Add environment report"
   git log --oneline -1
   git status
   ```

5. `reports\week01_sysinfo.json`에 사용자 홈 경로·이름이 없는지 한 번 더 읽는다.

완료 조건:

- [ ] `git log --oneline -1`에 `Add environment report`가 보인다.
- [ ] `git status`가 clean이고 `.venv`·`outputs`·`.env`가 commit에 없다.
- [ ] `reports/` 안에 점검표·탐색표·보고서 세 파일이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — uv run이 Python을 내려받기 시작한다</summary>

환경 기준표의 Python이 이 PC에 아직 설치되지 않은 것이다. 다운로드가 작고 네트워크가 열려 있으면 기다린다. 막혀 있으면 조교에게 알리고, 기다리는 동안 문제 2의 `git init`과 `reports` 정리를 먼저 한다.
</details>

<details>
<summary>힌트 2 — python-dotenv 설치가 실패한다(네트워크 없음)</summary>

프로젝트 없이 실행한다. 이때 `.env`는 읽지 않으므로 환경변수를 셸에서 직접 준다.

```powershell
$env:OLLAMA_MODEL = "qwen3:0.6b"
uv run --no-project python sysinfo.py
```

스크립트가 "python-dotenv가 없어 .env를 읽지 않는다"고 안내하면 정상이다. 이 경로에서는 `.venv`가 만들어지지 않으므로 `python.in_project_venv`가 `false`, `venv_location`이 `(프로젝트 폴더 밖)`으로 나오는 것도 정상이며, 그 사실을 비교 문장에 적는다.
</details>

<details>
<summary>힌트 3 — git status에 .venv/가 보인다</summary>

현재 폴더가 어디인지, `first_run\.gitignore`가 있는지(`Get-ChildItem first_run -Force`) 확인한다. 파일이 없으면 교재의 `examples\first_run\.gitignore`를 다시 복사한다. 이미 `git add`했다면 `git restore --staged first_run/.venv`로 내린다.
</details>

### 검증

- 정상: `outputs/sysinfo.json`에 GPU 이름·VRAM이 있고, commit이 1개 있으며 `git status`가 clean이다.
- 경계 또는 실패: `--no-gpu`(또는 GPU 없는 PC)에서 스크립트가 오류 없이 끝나고 `reason`이 남는다. `.venv`가 commit에 포함되지 않았다.
- 설명: `outputs/`를 `.gitignore`에 넣고도 보고서를 `reports/`에 복사해 commit한 이유를 한 문장으로 적었다.

### 확장 문제

1. `sysinfo.py`에 `--check-ollama` 옵션을 추가해 `OLLAMA_HOST`의 `/api/tags`에 GET 요청(표준 라이브러리 `urllib.request`, 타임아웃 3초)을 보내고, 연결 실패를 사람이 읽을 메시지로 보고서에 기록한다. Ollama 서버가 꺼진 상태를 먼저 재현한다.
2. 보고서의 `disk.free_gb`를 읽어 "모델 캐시 12 GB가 들어갈 여유가 있는가"를 판단하는 `warnings` 목록을 보고서에 추가한다.

## 제출 체크

- `reports/env_check.md`: 도구 5개 상태·버전, GPU, 계정 확인 여부, 실패 항목과 조치
- `reports/oss_survey.md`: 저장소 3행 표, 근거 URL, OSAID 판정 3문장, 도구·모델 라이선스 구분 문장
- `reports/week01_sysinfo.json`: `sysinfo.py` 보고서(홈 경로·개인정보 없음)
- 개인 저장소: `Add environment report` commit, `git log --oneline -1` 출력, `git status` clean
- 선택: 확장 문제 결과
