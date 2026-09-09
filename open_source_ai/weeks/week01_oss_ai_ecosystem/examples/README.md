# 1주차 예제 — 실습환경 점검과 첫 uv 실행

## 파일 구성

| 파일 | 역할 |
|---|---|
| `env_check.ps1` | `git`·`code`·`uv`·`ollama`·`nvidia-smi` 버전 문자열을 모아 Markdown 표로 출력하고 실패 항목과 조치 힌트를 표시하는 PowerShell 스크립트 |
| `env_check_template.md` | 1교시 실습환경 점검표 양식. `env_check.md`로 복사해 채운다 |
| `oss_survey_template.md` | 2교시 공개 AI 프로젝트 탐색표 양식. `oss_survey.md`로 복사해 채운다 |
| `first_run/` | 3교시 uv 프로젝트. `sysinfo.py`, `pyproject.toml`, `.env.example`, `.gitignore`, `README.md` |
| `first_run/sysinfo.py` | OS·CPU·RAM·디스크·GPU·Python·환경변수 값을 `outputs/sysinfo.json`으로 남기는 스크립트 |

## 실행 방법

이 폴더를 개인 실습 폴더에 복사한 뒤 복사본에서 실행한다. 원본은 수정하지 않는다.

```powershell
New-Item -ItemType Directory -Force C:\classwork\osa-week01
Copy-Item -Recurse "<교재 폴더>\open_source_ai\weeks\week01_oss_ai_ecosystem\examples\*" C:\classwork\osa-week01\
Set-Location C:\classwork\osa-week01
```

환경 점검(1교시):

```powershell
.\env_check.ps1
.\env_check.ps1 -OutFile env_check_raw.md
```

실행 정책 오류가 나면 정책을 바꾸지 않고 이번 실행만 우회한다.

```powershell
powershell -ExecutionPolicy Bypass -File .\env_check.ps1 -OutFile env_check_raw.md
```

첫 uv 실행(3교시):

```powershell
Set-Location C:\classwork\osa-week01\first_run
uv run python sysinfo.py
uv run python sysinfo.py --no-gpu
uv run python sysinfo.py --print
```

첫 실행에서 uv가 `.venv`를 만들고 `python-dotenv`를 설치한다. 결과는 `first_run\outputs\sysinfo.json`이다. 설정을 바꾸려면 `.env.example`을 `.env`로 복사해 값을 고친다.

## 관찰 지점

1. `env_check.ps1` 출력에서 `실패` 행과 그 아래 조치 힌트. 도구가 있어도 새 창을 열지 않으면 "명령을 찾을 수 없음"이 나온다.
2. `nvidia-smi` 행의 GPU 이름, `memory.total`(MiB), 드라이버 버전.
3. `sysinfo.json`의 `python.in_project_venv`와 `python.venv_location`: uv가 프로젝트 폴더 안의 `.venv`를 썼다는 증거.
4. `sysinfo.json`의 `env.OLLAMA_MODEL.source`: `.env`가 없으면 `기본값`, 있으면 `.env 또는 환경변수`.
5. `--no-gpu`(또는 GPU 없는 PC)에서 `gpu.available`이 `false`이고 `reason`이 채워진다. 스크립트는 오류로 멈추지 않는다.
6. `git status`에서 `.venv/`, `outputs/`, `.env`가 보이지 않는다. `first_run/.gitignore`가 하는 일이다.

## GPU 없을 때·네트워크 없을 때

| 상황 | 대체 경로 |
|---|---|
| NVIDIA GPU 또는 드라이버가 없다 | `env_check.ps1`의 `nvidia-smi` 행은 `실패`가 정상이다. `sysinfo.py`는 `gpu.available: false`와 사유를 기록하고 끝까지 실행된다. 점검표에는 "GPU 없음 → CPU + 소형 모델(`qwen3:0.6b`)"로 적는다 |
| Ollama가 아예 설치되어 있지 않다(개인 노트북) | `실패`와 `명령을 찾을 수 없음`이 정상이다. **이번 주에는 설치하지 않는다.** 점검표에 "미설치 → 4주차 전까지 설치"를 적고 넘어간다. 설치 절차는 [`lab.md`의 숙제](../lab.md#숙제--올라마-설치-4주차-전까지)에 있다 |
| Ollama 서버가 꺼져 있다 | 이번 주는 서버가 필요 없다. `ollama --version`은 `Warning: could not connect to a running Ollama instance`와 `Warning: client version is 0.x.y` **두 줄**을 내고 `ollama version is …` 줄은 나오지 않는다. `env_check.ps1`은 숫자가 들어 있는 첫 줄을 버전으로 고르므로 표에는 `Warning: client version is 0.x.y`가 들어가고 상태는 `정상`이 된다 — 설치는 되어 있다는 뜻이라 실패가 아니다. 점검표에는 그 줄을 그대로 옮기고 조치 칸에 "서버 꺼짐"을 적는다 |
| 네트워크가 막혀 `python-dotenv` 설치가 안 된다 | `uv run --no-project python sysinfo.py`로 실행한다. `.env`는 읽지 않으므로 `$env:OLLAMA_MODEL = "qwen3:0.6b"`처럼 셸 환경변수로 준다 |
| 환경 기준표의 Python이 설치되지 않아 uv가 다운로드를 시작한다 | 네트워크가 열려 있으면 기다린다. 막혀 있으면 조교에게 알리고 3교시 문제 2(`git init`)를 먼저 진행한다 |
| `code` 명령이 없다 | VS Code를 직접 열어 편집한다. 점검표에는 `실패`와 조치(PATH 옵션 확인)를 적는다 |

## 모델·버전 안내

- 이 예제는 모델을 내려받거나 호출하지 않는다. `OLLAMA_HOST`, `OLLAMA_MODEL` 값을 읽어 보고서에 적기만 한다. 실제 호출은 4주차다.
- 모델 ID·양자화·용량은 학기별 [환경 기준표](../../../../environment_baseline_template.md)에서 확정하며, `.env.example`의 값은 교재 검증용 기본값이다.
- `first_run/`에 `uv.lock`은 없다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다. 학생 복사본에서는 첫 `uv run`이 `uv.lock`을 자동으로 만들며, 지우지 않고 그대로 commit한다(잠금 파일의 역할은 3주차에 다룬다).

## 복사 후 변형

- 점검표·탐색표는 템플릿을 복사한 파일(`env_check.md`, `oss_survey.md`)에만 쓴다.
- `sysinfo.py`를 고칠 때는 복사본에서 고친다. `--check-ollama`, `warnings` 같은 확장은 `lab.md`의 확장 문제를 따른다.
- `first_run/outputs/`는 커밋되지 않는다. 남길 보고서는 개인 저장소의 `reports/`로 복사한다.
