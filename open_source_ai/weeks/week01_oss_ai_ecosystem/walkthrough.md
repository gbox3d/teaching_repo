# 1주차 따라하기 — 실습환경 점검, 생태계 탐색, 첫 uv 실행

이 문서는 1주차 시연·실습을 **순서대로 그대로 재현**하기 위한 절차서다.
강의자는 각 교시의 20분 시연을 이 순서로 진행하고, 학생은 실습 30분과 복습 때 같은 순서로 따라 한다.
각 단계는 `할 일 → 예상 결과 → 확인` 순서로 되어 있다. 예상 결과가 다르면 다음 단계로 넘어가지 않는다.
실습 30분의 시간 배분과 완료 조건은 [`lab.md`](lab.md)가 기준이다.

## 시작 전 준비

- Windows PC. 실습실 PC는 Git, VS Code, uv, Ollama 설치를 조교가 [설치 프로그램 목록](../../ta_setup_guide.md)에 따라 수업 전에 마친다. **개인 노트북은 아무것도 깔려 있지 않아도 된다.** 단계 4에서 직접 설치한다. 정확한 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 브라우저에서 GitHub·Hugging Face에 로그인할 수 있는 상태. 토큰은 만들지 않는다.
- [`examples/`](examples/README.md) 폴더를 개인 실습 폴더에 **복사**해서 사용한다. 수업 자료 원본은 수정하지 않는다.
- 이 문서는 개인 실습 폴더를 `C:\classwork\osa-week01`로 쓴다. 강의자가 다른 경로를 안내하면 그 경로로 바꾼다.
- 명령은 **새 PowerShell 창**에서 현재 경로를 확인한 뒤 실행한다. 이번 주에는 모델을 내려받지 않는다.

---

## 1교시 — 실습환경 점검표 만들기

**이어받는 것:** 없음(첫 블록).

### 단계 1. 개인 실습 폴더 만들기와 예제 복사

**할 일**

1. 새 PowerShell 창을 연다.
2. 다음을 실행한다. `<교재 폴더>`는 수업 자료를 받아 둔 위치다.

```powershell
New-Item -ItemType Directory -Force C:\classwork\osa-week01
Copy-Item -Recurse "<교재 폴더>\open_source_ai\weeks\week01_oss_ai_ecosystem\examples\*" C:\classwork\osa-week01\
Set-Location C:\classwork\osa-week01
Get-ChildItem
```

**예상 결과** — `README.md`(예제 안내), `env_check.ps1`, `env_check_template.md`, `oss_survey_template.md`, `first_run` 다섯 항목이 보인다. `Get-Location`의 결과가 `C:\classwork\osa-week01`이다.

**확인** — [ ] 교재 원본 폴더가 아니라 복사본 안에 있다.

### 단계 2. 도구 5개를 손으로 먼저 확인하기

**할 일**

1. 실행 전에 예상을 적는다: 다섯 도구 중 이 PC에 없을 것 같은 것과 그 이유.
2. 다음 다섯 명령을 한 줄씩 실행하고 출력 첫 줄을 그대로 적는다.

```powershell
git --version
code --version
uv --version
ollama --version
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
```

**예상 결과** — 각 명령이 `git version …`, 버전 숫자, `uv …` 같은 문자열을 출력한다.

`ollama --version`은 세 가지로 갈린다. 어느 쪽인지 구분해서 적는다.

| 출력 | 뜻 |
|---|---|
| `ollama version is 0.x.y` 한 줄 | 설치·서버 모두 정상 |
| `Warning: could not connect to a running Ollama instance` 와 `Warning: client version is 0.x.y` **두 줄** | 설치는 됐고 서버만 꺼짐. **이때 버전 줄은 나오지 않는다** |
| `명령을 찾을 수 없음` | 미설치. 개인 노트북은 이것이 정상이며, 설치는 4주차 전까지 숙제다 |

`nvidia-smi`는 헤더 한 줄 뒤에 `GPU 이름, NNNN MiB, 드라이버 버전` 한 줄을 출력한다. `명령을 찾을 수 없음`이 나오는 도구가 있으면 그 사실 자체가 기록할 값이다.

**확인** — [ ] 예상과 실제가 다른 도구가 있으면 어느 것인지 적었다.

### 단계 3. env_check.ps1로 같은 결과를 파일로 남기기

**할 일**

```powershell
.\env_check.ps1 -OutFile env_check_raw.md
```

**예상 결과** — 화면에 도구 5행 표가 출력되고 각 행이 `정상` 또는 `실패`다. 단계 2에서 손으로 본 버전 문자열과 같은 값이 표에 들어 있다. 실패 행이 있으면 아래에 `실패 항목과 조치 힌트` 절이 생긴다. 마지막 줄은 `저장: env_check_raw.md`다. Git 사용자 설정은 값이 아니라 `설정됨`/`미설정`으로만 나온다.

`이 시스템에서 스크립트를 실행할 수 없으므로`로 멈추면 정책을 바꾸지 않고 이번 실행만 우회한다.

```powershell
powershell -ExecutionPolicy Bypass -File .\env_check.ps1 -OutFile env_check_raw.md
```

**확인** — [ ] `env_check_raw.md`를 열어 사용자 이름·홈 경로가 없는 것을 확인했다.

### 단계 4. uv가 없으면 직접 설치하기

단계 3의 표에서 `uv` 행이 `정상`이면 이 단계는 **4번의 `Get-Command uv`(설치 경로 확인)만** 하고 단계 5로 간다.
`실패`였다면 아래를 순서대로 한다. 관리자 권한은 필요 없다.

**할 일**

1. 설치 전에 예상을 적는다: 설치가 끝난 바로 그 창에서 `uv --version`을 치면 될 것 같은가, 그 이유는 무엇인가.
2. 둘 중 하나로 설치한다. 방법 1이 기본이고, 정책으로 막히면 방법 2를 쓴다.

```powershell
# 방법 1 · 공식 설치 스크립트
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```powershell
# 방법 2 · 스크립트 실행이 막힌 PC
winget install --id=astral-sh.uv -e
```

3. 설치한 그 창에서 그대로 확인해 본다. 결과를 적는다.

```powershell
uv --version
```

4. **PowerShell 창을 완전히 닫고 새 창을 연 뒤** 실습 폴더로 돌아가 다시 확인한다.

```powershell
Set-Location C:\classwork\osa-week01
uv --version
Get-Command uv | Select-Object -ExpandProperty Source
```

5. 점검 스크립트를 다시 돌려 표가 바뀌는지 본다.

```powershell
.\env_check.ps1 -OutFile env_check_raw.md
```

**예상 결과** — 방법 1은 내려받기 줄 몇 개를 찍고 `uv` 와 `uvx` 를 `%USERPROFILE%\.local\bin` 에 두었다는 안내로 끝난다.

3번(설치한 창)에서는 `uv : 'uv' 용어가 cmdlet … 이름으로 인식되지 않습니다` 가 나오는 것이 정상이다. 설치 프로그램이 PATH를 바꿔도 **이미 열려 있던 창은 열리던 순간의 PATH를 그대로 들고 있기 때문**이다.

4번(새 창)에서 `uv 0.x.y` 같은 버전 문자열이 나온다. `Get-Command` 는 방법 1이면 `C:\Users\<사용자>\.local\bin\uv.exe`, 방법 2(winget)면 `…\WinGet\Links\uv.exe` 계열 경로를 출력한다. 경로는 설치 방법에 따라 다른 것이 정상이다.

5번의 표에서 `uv` 행이 `실패`에서 `정상`으로 바뀌고, 아래 `실패 항목과 조치 힌트` 절에서 uv 줄이 사라진다.

> 새 창에서도 `명령을 찾을 수 없음`이면 설치 실패와 PATH 미등록을 구분한다. `Test-Path "$env:USERPROFILE\.local\bin\uv.exe"` 가 `False` 면 설치 자체가 실패한 것이고, `True` 인데 명령만 안 되면 PATH 문제다. 자세한 절차는 [`lab.md`의 힌트 3](lab.md#단계별-힌트)에 있다.

**확인** — [ ] 새 창에서 `uv --version`이 버전 문자열을 출력한다.
**확인** — [ ] 3번과 4번의 결과가 왜 달랐는지(또는 왜 같았는지) 한 문장으로 적었다.
**확인** — [ ] `uv`의 설치 경로를 점검표에 적었다.

> **올라마는 오늘 설치하지 않는다.** 바이너리만 4 GB이고 모델은 그보다 커서 실습 30분에 맞지 않는다.
> Ollama 행이 `실패`면 점검표에 "미설치 → 4주차 전까지 설치"를 적고 넘어간다.
> 설치 절차는 [`lab.md`의 숙제](lab.md#숙제--올라마-설치-4주차-전까지)에 있다.

### 단계 5. 실패 하나를 일부러 재현하기

**할 일**

1. 예측을 적는다: "PATH에 없는 명령을 부르면 스크립트는 멈추는가, 표에 실패로 적고 계속 가는가?"
2. 복사본 `env_check.ps1`의 `$tools` 목록에서 Ollama 행의 `Command = "ollama"`를 `Command = "ollama-x"`로 잠시 바꾼다.

   올라마가 이 PC에 없어서 Ollama 행이 **이미 `실패`**라면 바꿔도 변화가 보이지 않는다. 그때는 Ollama 대신 `Command = "git"`을 `"git-x"`로 바꿔 같은 관찰을 한다.
3. 다시 실행한다.

```powershell
.\env_check.ps1
```

4. Ollama 행이 `실패`, `명령을 찾을 수 없음`으로 바뀌고 나머지 행은 그대로인지 본다. 힌트 절의 Ollama 문장이 비어 있는데, 힌트 표가 원래 명령 이름으로 찾기 때문이다.
5. 바꾼 한 곳을 원래대로 되돌리고 다시 실행해 `정상`(또는 이 PC의 원래 상태)으로 돌아오는지 확인한다.

**예상 결과** — 스크립트는 멈추지 않고 표를 끝까지 출력한다. 설치가 되어 있어도 "새 창을 열지 않아 PATH에 없는" 상황이 화면에서는 이와 똑같이 보인다.

**확인** — [ ] "설치 프로그램이 성공했다"와 "새 창에서 버전이 나온다"가 왜 다른지 한 문장으로 적었다.

### 단계 6. 계정 확인과 점검표 완성

**할 일**

1. 브라우저에서 GitHub에 로그인하고 자기 프로필 페이지(`https://github.com/<표시 이름>`)를 연다. 실명·전화번호 같은 불필요한 개인정보가 공개되어 있는지 본다.
2. Hugging Face에 로그인한다. 설정 화면의 Access Tokens는 열어 보기만 하고 만들지 않는다.
3. 점검표 템플릿을 복사해 채운다.

```powershell
Copy-Item env_check_template.md env_check.md
code env_check.md
```

4. 도구 표에는 `env_check_raw.md`의 버전 문자열을 옮겨 적고, GPU 표·계정 표·실패 항목과 조치·한 문장 결론을 채운다.

**예상 결과** — `env_check.md`의 도구 표 5행, GPU 표, 계정 표 2행이 모두 채워져 있고 비밀번호·토큰·이메일은 어디에도 없다. 계정 표는 `확인함/미확인`과 표시 이름(`student01` 같은 수업용 값)뿐이다. GPU가 없는 PC는 GPU 표에 "GPU 없음"과 대체 경로(`CPU + qwen3:0.6b`)가 적혀 있다.

**확인** — [ ] [`lab.md`의 1교시 완료 조건](lab.md#1교시-실습--실습환경-점검표-만들기)을 모두 체크했다. 실습 30분 뒤 휴식 10분.

---

## 2교시 — 공개 AI 프로젝트 탐색표

**이어받는 것:** 1교시의 개인 실습 폴더 `C:\classwork\osa-week01`과 브라우저의 GitHub 로그인 상태. 하루가 바뀌었으면 단계 1에서 폴더가 그대로 있는지 먼저 확인한다.

### 단계 1. 템플릿 복사와 예상 적기

**할 일**

```powershell
Set-Location C:\classwork\osa-week01
Copy-Item oss_survey_template.md oss_survey.md
code oss_survey.md
```

조사 대상은 `ollama/ollama`, `huggingface/transformers`, `vllm-project/vllm` 세 저장소다(강의자가 다르게 지정하면 그것을 따른다). 화면을 열기 전에 저장소마다 라이선스 이름과 활동 수준(많다/적다)을 예상해 적는다.

**예상 결과** — `oss_survey.md`에 탐색표(3행), 근거 URL 표, OSAID 판정, 도구와 모델의 라이선스, 살아 있는 프로젝트의 근거 절이 빈 채로 보인다.

**확인** — [ ] 세 저장소의 예상 라이선스를 적었다.

### 단계 2. 라이선스 — About에서 LICENSE 파일까지

**할 일**

1. `https://github.com/ollama/ollama`를 연다.
2. 첫 화면 오른쪽 About 칸의 라이선스 표기를 읽는다.
3. 파일 목록에서 `LICENSE`(또는 `LICENSE.md`)를 열어 첫 줄과 본문 첫 문단을 읽는다.
4. 표에는 SPDX ID 형식(`MIT`, `Apache-2.0`, `BSD-3-Clause` 같은 짧은 식별자)으로 적고, 근거 URL 표에는 `LICENSE` 파일 화면의 주소를 적는다.
5. 나머지 두 저장소도 같은 순서로 읽는다.

**예상 결과** — About의 이름과 `LICENSE` 파일의 이름이 같다. 세 저장소 모두 OSI 승인 라이선스이며 [SPDX 목록](https://spdx.org/licenses/)에서 같은 이름을 찾을 수 있다. About에 `View license`로만 보이면 GitHub이 자동 인식하지 못한 것이므로 파일에서 읽은 이름을 적는다.

**확인** — [ ] 라이선스 3개가 모두 SPDX ID로 적혀 있고 근거 URL이 있다.

### 단계 3. 활동 지표 — 최근 커밋, 열린 이슈, 릴리스

**할 일**

1. 기본 브랜치 파일 목록 위의 마지막 커밋 시각을 읽어 "며칠 전"으로 적는다. 커밋 목록 화면(`/commits/<기본 브랜치>`)의 주소를 근거로 적는다.
2. Issues 탭에서 `Open` 개수를 읽는다. `Closed` 개수도 옆에 적어 두면 비율을 볼 수 있다.
3. Releases(오른쪽 칸)에서 최근 태그 3개의 날짜를 읽고 간격을 "약 N주"로 적는다. Releases가 없으면 Tags 화면으로 대신하고, 둘 다 없으면 "릴리스 없음(커밋으로만 배포)"이라고 적는다.
4. 세 저장소를 같은 순서로 채운다.

**예상 결과** — 세 저장소 모두 마지막 커밋이 며칠 이내이고, 열린 이슈가 수백~수천 개이며, 릴리스가 주 단위로 나온다. 숫자는 조사 당일마다 다르므로 **값과 함께 URL과 조사 날짜**를 적어야 근거가 된다.

**확인** — [ ] 탐색표의 라이선스·최근 커밋·열린 이슈·릴리스 주기 열이 3행 모두 채워졌다.

### 단계 4. 기여 가이드 찾기

**할 일**

1. 저장소 파일 목록에서 `CONTRIBUTING.md`를 찾는다. 루트에 없으면 `docs/` 아래나 `.github/` 아래를 본다.
2. 파일을 열어 첫 절 제목 하나를 표에 적는다.
3. 없으면 "없음"과 그렇게 판단한 파일 목록 화면의 URL을 적는다.

**예상 결과** — 세 저장소 모두 기여 문서가 있으며, 위치는 저장소마다 다르다. "없음"도 근거 URL이 있으면 정답이다.

**확인** — [ ] 기여 가이드 열이 `있음(절 제목)` 또는 `없음(URL)`으로 채워졌다.

### 단계 5. OSAID 판정과 도구·모델 라이선스 구분

**할 일**

1. 슬라이드의 OSAID 세 공개 항목(데이터 정보·코드·파라미터)을 다시 읽는다.
2. 저장소마다 한 문장을 채운다: "이 프로젝트는 OSAID의 ___ 항목을 만족하고, ___ 항목은 프로젝트가 아니라 개별 모델의 문제다."
3. Ollama 라이브러리에서 크기 태그 하나를 열고(`https://ollama.com/library/qwen3:8b`) 파일 목록의 `license` 항목에서 라이선스 이름을 읽는다. 모델 첫 화면(`/library/qwen3`)에는 라이선스가 표시되지 않는다. 다운로드는 하지 않는다.
4. "도구의 라이선스와 그 도구로 실행하는 모델의 라이선스가 같은가"를 한 문장으로 적는다.
5. 셋 중 "살아 있는 프로젝트"라고 판단하는 근거를 활동 지표 2개로 적는다.

**예상 결과** — 세 저장소는 모델이 아니라 소프트웨어라는 사실에서, 세 항목 중 어느 것이 프로젝트의 것이고 어느 것이 그 위에서 돌리는 모델의 것인지가 문장에 구분되어 있다. 도구 라이선스와 모델 라이선스는 서로 다른 문서(저장소의 `LICENSE`와 모델 페이지의 라이선스)에서 정해진다.

**확인** — [ ] 판정 문장 3개, 도구·모델 구분 문장 1개, 활동 지표 2개가 있다.

### 단계 6. 근거 URL 대조

**할 일**

1. 근거 URL 표의 15칸을 하나씩 열어, 열리는 화면이 탐색표의 값을 실제로 보여 주는지 대조한다.
2. 화면에서 찾지 못한 값은 표에서 지우고 "없음"과 이유를 적는다.
3. 파일을 저장한다.

**예상 결과** — 값마다 URL이 있고, URL을 열면 그 값이 보인다. 기억이나 인상으로 적은 칸은 남아 있지 않다.

**확인** — [ ] [`lab.md`의 2교시 완료 조건](lab.md#2교시-실습--공개-ai-프로젝트-탐색표)을 모두 체크했다. 실습 30분 뒤 휴식 10분.

---

## 3교시 — 첫 uv 실행과 첫 commit

**이어받는 것:** 1·2교시에서 만든 `env_check.md`, `oss_survey.md`가 있는 개인 실습 폴더 `C:\classwork\osa-week01`. 두 파일이 없어도 이 교시의 단계는 진행할 수 있으며, 단계 5에서 있는 파일만 `reports\`로 옮긴다.

### 단계 1. first_run 폴더 확인과 예상

**할 일**

```powershell
Set-Location C:\classwork\osa-week01\first_run
Get-ChildItem -Force
Get-Content pyproject.toml
```

실행 전에 예상을 적는다: 보고서 JSON에 GPU 이름이 들어갈지, Python이 어느 폴더의 것일지, `OLLAMA_MODEL` 값은 무엇으로 나올지.

**예상 결과** — `.env.example`, `.gitignore`, `README.md`, `pyproject.toml`, `sysinfo.py` 다섯 항목이 보이고 `.venv`, `outputs`, `.env`는 아직 없다. `pyproject.toml`의 의존성은 `python-dotenv` 하나다.

**확인** — [ ] 예상 세 가지를 적었다.

### 단계 2. 첫 uv run

**할 일**

```powershell
uv run python sysinfo.py
Get-ChildItem -Force
```

**예상 결과** — 첫 실행에서 uv가 `.venv`를 만들고 `python-dotenv`를 설치하는 메시지가 지나간 뒤, 다음 형태의 요약 7줄과 `저장: outputs/sysinfo.json`이 출력된다.

```text
OS       : Windows 11 (AMD64)
CPU      : … / 논리 코어 N
RAM      : NN.N GiB
디스크   : C:\ 여유 NNN.N / NNN.N GiB
GPU      : NVIDIA GeForce RTX 4070 (12282 MiB, driver …)
Python   : 3.x.y @ .venv
모델 설정: OLLAMA_MODEL=qwen3:8b [기본값]
```

폴더에 `.venv`, `outputs`, 그리고 잠금 파일 `uv.lock`이 새로 생겼다. `uv.lock`은 지우지 않는다(역할은 3주차에 다룬다). `outputs\sysinfo.json`을 열면 `python.in_project_venv`가 `true`, `python.venv_location`이 `.venv`다. 두 번째 실행부터는 설치 메시지 없이 바로 요약이 나온다.

**확인** — [ ] GPU 줄에 이름과 VRAM(MiB)이 있거나, GPU 없는 PC라면 `GPU 없음: …` 사유가 있다.

### 단계 3. .env로 값 바꾸기

**할 일**

1. 예측을 적는다: "코드를 고치지 않고 `.env`만 만들면 `OLLAMA_MODEL` 값이 바뀔까?"
2. 실행한다.

```powershell
Copy-Item .env.example .env
code .env
```

3. `.env`에서 `OLLAMA_MODEL=qwen3:8b`를 `OLLAMA_MODEL=qwen3:0.6b`로 바꾸고 저장한다.
4. 다시 실행한다.

```powershell
uv run python sysinfo.py
```

**예상 결과** — 마지막 요약 줄이 `모델 설정: OLLAMA_MODEL=qwen3:0.6b [.env 또는 환경변수]`로 바뀐다. `outputs\sysinfo.json`의 `env.OLLAMA_MODEL.source`도 `.env 또는 환경변수`다. `sysinfo.py`는 한 글자도 바꾸지 않았다.

**확인** — [ ] 값이 어디서 왔는지(`source`)를 보고서에 남기는 이유를 한 문장으로 적었다.

### 단계 4. GPU 없음 경계 경로

**할 일**

```powershell
uv run python sysinfo.py --no-gpu
```

**예상 결과** — 스크립트가 오류 없이 끝나고 GPU 줄이 `GPU 없음: --no-gpu 옵션으로 건너뜀`이다. JSON의 `gpu.available`은 `false`, `reason`이 채워져 있고 `devices`는 빈 목록이다. GPU가 없는 PC에서는 옵션 없이도 같은 형태가 나온다(사유만 다르다).

옵션 없이 한 번 더 실행해 보고서를 정상 값으로 되돌린다.

**확인** — [ ] 정상 실행과 `--no-gpu` 실행의 차이를 한 문장으로 적었다.

### 단계 5. 개인 저장소 만들기와 reports 정리

**할 일**

1. 저장소 루트는 `first_run`이 아니라 개인 실습 폴더다. 수업 자료 저장소 안에서 `git init`하지 않는다.

```powershell
Set-Location C:\classwork\osa-week01
git init
git branch -M main
git status
```

2. 증거를 `reports\`에 모은다. `first_run\outputs\`는 `.gitignore`로 무시되므로 보고서를 복사해 둔다.

```powershell
New-Item -ItemType Directory -Force reports
Copy-Item first_run\outputs\sysinfo.json reports\week01_sysinfo.json
Move-Item env_check.md, oss_survey.md reports\
git check-ignore -v first_run\.venv first_run\outputs first_run\.env
git status
```

**예상 결과** — 첫 `git status`는 `On branch main`, `No commits yet`과 untracked 목록이다. `git check-ignore -v`는 세 경로마다 `first_run/.gitignore:N:패턴` 형태로 어느 줄이 무시했는지 한 줄씩 출력한다. 두 번째 `git status`의 untracked 목록에 `reports/`, `README.md`, `env_check.ps1`, `env_check_raw.md`, 템플릿 2개, `first_run/`이 보인다. identity 오류가 나면 강의자 안내에 따라 수업용 `user.name`/`user.email`을 설정한다(공유 PC에서 전역 설정을 임의로 바꾸지 않는다).

**확인** — [ ] `reports\week01_sysinfo.json`을 열어 사용자 이름·홈 경로가 없는 것을 확인했다.

### 단계 6. 첫 commit과 검증

**할 일**

```powershell
git add .
git status
git commit -m "Add environment report"
git log --oneline -1
git status
```

`git commit` 전의 `git status`에서 `Changes to be committed` 목록을 읽고 `.venv`·`outputs`·`.env`가 없는지 확인한 뒤 commit한다.

**예상 결과** — `Changes to be committed`에는 `first_run/` 아래 여섯 파일(원본 다섯 + 첫 실행이 만든 `uv.lock`), `reports/` 아래 세 파일, 예제 안내 `README.md`, `env_check.ps1`, `env_check_raw.md`, 템플릿 2개, 모두 14개만 있다. `git log --oneline -1`에 해시와 `Add environment report`가 한 줄로 보인다. 마지막 `git status`는 `nothing to commit, working tree clean`이다. 이 commit이 학기 내내 자랄 개인 저장소의 첫 기록이며, 2주차에 GitHub 원격과 연결된다.

**확인** — [ ] [`lab.md`의 3교시 완료 조건](lab.md#3교시-실습--첫-uv-실행과-첫-commit)을 모두 체크했다. 실습 30분 뒤 휴식 10분.

---

## 문제가 생겼을 때

| 증상 | 이 문서에서 돌아갈 단계 |
|---|---|
| `env_check.ps1`이 "스크립트를 실행할 수 없으므로"로 멈춘다 | 1교시 단계 3 (`-ExecutionPolicy Bypass`로 이번 실행만 우회) |
| 설치했는데 도구가 `명령을 찾을 수 없음`이다 | 1교시 단계 4 (PowerShell 창을 완전히 닫고 새로 연다. 그래도 같으면 `Test-Path`로 설치 실패와 PATH 미등록을 구분한다) |
| `ollama`가 `명령을 찾을 수 없음`이다 | 설치하지 않아도 되는 상태다. 점검표에 "미설치 → 4주차 전까지 설치"를 적고 계속. 설치는 [`lab.md`의 숙제](lab.md#숙제--올라마-설치-4주차-전까지) |
| `ollama --version`이 경고 두 줄만 낸다 | 설치는 됐고 서버만 꺼진 것이다. 트레이 또는 시작 메뉴에서 Ollama를 실행하고 다시 확인 |
| `nvidia-smi`만 실패한다 | 1교시 단계 6 (GPU 없는 PC. 점검표에 대체 경로 `CPU + qwen3:0.6b`를 적고 계속) |
| About에 라이선스가 `View license`로만 보인다 | 2교시 단계 2 (`LICENSE` 파일에서 이름을 읽는다) |
| Releases가 비어 있다 | 2교시 단계 3 (Tags로 대신, 둘 다 없으면 "릴리스 없음") |
| `uv run`이 Python을 내려받기 시작한다 | 3교시 단계 2 (네트워크가 열려 있으면 기다린다. 막혀 있으면 조교에게 알리고 단계 5를 먼저 진행) |
| `python-dotenv` 설치가 실패한다(네트워크 없음) | 3교시 단계 2 (`uv run --no-project python sysinfo.py`, 값은 `$env:OLLAMA_MODEL`로 준다) |
| `.env`를 만들었는데 `source`가 `기본값`이다 | 3교시 단계 3 (`.env`가 `first_run` 안에 있는지, 변수 이름 오타·앞뒤 공백이 없는지) |
| `git check-ignore`가 아무것도 출력하지 않는다 | 3교시 단계 5 (`first_run\.gitignore`가 복사되었는지 `Get-ChildItem first_run -Force`로 확인) |
| `Changes to be committed`에 `.venv/`가 보인다 | 3교시 단계 6 (`git restore --staged first_run/.venv` 후 `.gitignore` 확인) |
| commit이 identity 오류로 실패한다 | 3교시 단계 5 (오류 첫 문장을 읽고 강의자 안내에 따라 수업용 설정) |

세부 판정 기준과 힌트는 [`lab.md`](lab.md)에 있다. 정답과 해설은 실습이 끝난 뒤 강의자가 별도로 안내한다.
