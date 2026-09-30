# uv 실습 가이드 — 설치부터 실행·재현까지

## 목차

- [수업에서 uv를 쓰는 이유](#수업에서-uv를-쓰는-이유)
- [설치와 최신 버전 업데이트](#설치와-최신-버전-업데이트)
- [Python 버전과 가상환경](#python-버전과-가상환경)
- [새 프로젝트로 uv run 익히기](#새-프로젝트로-uv-run-익히기)
- [기존 수업 예제 실행하기](#기존-수업-예제-실행하기)
- [의존성 추가와 업데이트](#의존성-추가와-업데이트)
- [다른 PC에서 환경 재현하기](#다른-pc에서-환경-재현하기)
- [한 파일짜리 예제와 도구 실행](#한-파일짜리-예제와-도구-실행)
- [문제 해결과 확인 과제](#문제-해결과-확인-과제)

1주차에는 설치·첫 실행, 3주차에는 프로젝트·lock·배포 재현 부분을 사용한다.
소스를 공개할 때는 [GitHub 배포와 Git 제외 가이드](github_distribution.md)를 함께 확인한다.

## 수업에서 uv를 쓰는 이유

uv는 Python 인터프리터 준비, 프로젝트별 패키지 설치, 의존성 기록, 실행을 한 도구로 연결한다.
프로젝트마다 환경을 만들고, 동료가 같은 패키지 구성을 복원할 자료를 남긴다.

| 구성 요소 | 역할 | Git에 포함 |
|---|---|---|
| uv 실행 파일 | 환경을 준비하는 도구 | 아니요. 설치 방법과 검증한 버전을 기록 |
| `pyproject.toml` | 필요한 패키지·Python 허용 범위·명령 정의 | 예 |
| `.python-version` | 이 프로젝트에서 선택할 Python 버전 | 예. 팀이 사용할 버전 문자열로 기록 |
| `uv.lock` | 의존성을 해석한 버전·출처·해시 | 예 |
| `.venv/` | 이 PC에 설치된 프로젝트 환경 | 아니요. 다시 생성 |
| uv 캐시 | 여러 프로젝트가 재사용하는 다운로드·빌드 자료 | 아니요. `uv cache dir`로 위치 확인 |

프로젝트 안에서 `uv run`은 필요한 환경을 준비하고 명령을 실행한다. 기본 설정에서는 lock도 필요에 따라 갱신하므로,
제출·배포 검증 때는 아래의 `--locked`를 사용한다. 파일 역할은 [uv 프로젝트 문서](https://docs.astral.sh/uv/guides/projects/)를 기준으로 한다.

## 설치와 최신 버전 업데이트

### 최초 설치

공식 독립 설치 프로그램은 uv를 설치한다. 미리 Python을 설치할 필요가 없다.
자기 운영체제에 해당하는 명령 **하나**를 실행한다.

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS·Linux 터미널:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

위 명령은 공식 사이트의 설치 스크립트를 내려받아 실행한다. 학교 PC의 설치 정책이 있으면 그 절차를 따른다.
완료 후 터미널을 새로 열고, VS Code 통합 터미널이면 VS Code도 다시 시작해 PATH 변경을 반영한다.

```text
uv --version
uv --help
```

대체 설치 방법은 macOS의 `brew install uv`, Windows의 `winget install --id astral-sh.uv -e`다.
여러 방식으로 중복 설치하면 서로 다른 uv가 실행될 수 있으므로 사용한 설치 방식을 기록한다.

### 설치 방식에 맞춰 업데이트

| 설치 방식 | 업데이트 명령 |
|---|---|
| 위의 공식 독립 설치 프로그램 | `uv self update` |
| Homebrew | `brew update` 다음 `brew upgrade uv` |
| WinGet | `winget upgrade --id astral-sh.uv -e` |

업데이트 후 `uv --version`을 다시 확인한다. Homebrew·WinGet 설치본의 업데이트는 해당 패키지 관리자로 한다.
실행 파일이 의심되면 Windows에서는 `Get-Command uv -All`, macOS·Linux에서는 `command -v uv`로 위치를 확인한다.

"최신" 버전 번호를 교재에 고정해 두지 않는다. 설치·업데이트 시점에 [공식 설치 안내](https://docs.astral.sh/uv/getting-started/installation/)와
[공식 릴리스](https://github.com/astral-sh/uv/releases/latest)를 확인하고, 실제 검증한 `uv --version` 값을 환경 기준표에 적는다.
uv 갱신은 기준 PC에서 먼저 검증하고 수업 기준에 반영한다. 프로젝트 폴더를 나눠도 같은 uv 실행 파일을 사용한다.

## Python 버전과 가상환경

### 최신 Python과 수업 Python은 따로 선택한다

```text
uv python list
```

최신 Python을 시험하려면 uv를 업데이트한 뒤 목록에서 지원하는 최신 안정 버전을 확인하고,
`uv python install <확인한 버전>`으로 명시해 설치한다. 꺾쇠 부분은 실제 버전 번호로 바꾼다.
버전 인자 없는 `uv python install`은 버전 파일·환경변수·기존 관리 Python 상태의 영향을 받으므로
항상 최신 버전으로 업그레이드하는 명령으로 해석하지 않는다. 설치만으로 기존 프로젝트의 버전 선택이 바뀌지도 않는다.
세부 선택 규칙은 [Python 설치 명령 참조](https://docs.astral.sh/uv/reference/cli/#uv-python-install)에 있다.

수업에서는 [환경 기준표](../environment_baseline_template.md)의 버전과 예제의 `requires-python`을 먼저 확인한다.
아래의 `3.12`는 현재 교재 예제의 `>=3.12` 조건에 맞춘 **명령 예시**이며 최신 버전 번호라는 뜻이 아니다.
수업 기준이 다르면 그 값으로 바꾼다. `3.11`로 실행하려면 프로젝트 요구사항과 사용하는 AI 패키지부터 호환되는지 확인해야 한다.

```text
uv python install 3.12
```

프로젝트 폴더에서 사용할 Python을 선택한다.

```text
uv python pin 3.12
uv run python --version
uv run python -c "import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)"
```

프로젝트 환경의 실행 파일은 Windows에서 `.venv\Scripts\python.exe`, macOS·Linux에서 `.venv/bin/python`이다.
마지막 출력이 `True`면 가상환경에서 실행 중이다. `requires-python = ">=3.12"`는 허용 범위이고,
`.python-version`의 `3.12`는 사용할 계열이다. 패치 버전까지 같아야 하면 기준 PC에서 확인한 전체 버전을 pin한다.
Python 설치 파일 자체가 Git이나 `uv.lock`에 들어가는 것은 아니다.

필요한 Python이 없을 때 uv는 기본적으로 자동 다운로드할 수 있다. 학교망·오프라인 실습에서는 수업 전에 설치해 둔다.
Python 패치 업그레이드 등 세부 기능은 [공식 Python 관리 문서](https://docs.astral.sh/uv/guides/install-python/)에서 현재 지원 상태를 확인한다.

### activate와 IDE 설정

`uv run`을 쓸 때는 `activate`가 필요 없다. 명시적으로 `uv venv`를 먼저 만들 필요도 없다.
직접 `python`만 실행하면 셸 PATH의 전역 Python을 고를 수 있으므로 실행 결과가 달라질 수 있다.

VS Code에서는 `Python: Select Interpreter`로 해당 예제의 `.venv` Python을 고른다.
편집기의 실행 버튼·디버거는 uv와 별도로 인터프리터를 선택할 수 있다.
PowerShell에서 활성화 스크립트 실행이 막히더라도 수업 명령인 `uv run ...`은 활성화 스크립트 없이 실행한다.

## 새 프로젝트로 uv run 익히기

교재 저장소 밖의 개인 실습 폴더에서 시작한다. 아래 공통 명령은 PowerShell과 macOS·Linux 셸에서 사용할 수 있다.
`--bare`는 자동 생성 파일을 최소화하고, `--vcs none`은 이 단계에서 Git 저장소를 자동 생성하지 않게 한다.

```text
mkdir uv-hello
cd uv-hello
uv init --bare --python 3.12 --vcs none
uv python pin 3.12
uv add httpx
```

VS Code로 **직접** `hello.py` 파일을 만들고 다음 내용을 저장한다. `uv init`이 특정 이름의 파일을 만들어 줄 것이라고 가정하지 않는다.

```python
import sys

import httpx

print("Python:", sys.version.split()[0])
print("실행 파일:", sys.executable)
print("httpx:", httpx.__version__)
print("가상환경:", sys.prefix != sys.base_prefix)
```

```text
uv run hello.py
uv run python hello.py
uv run python -c "import httpx; print(httpx.__version__)"
uv tree
```

앞의 두 명령은 이 예제에서는 같은 출력을 낸다. `httpx`는 버전 확인만 하므로 외부 API나 모델 서버가 필요 없다.
첫 패키지 설치에는 인터넷이나 사전 캐시가 필요하다. 실행 파일 경로에 `.venv`가 있는지 확인하고,
`pyproject.toml`·`.python-version`·`uv.lock`이 각각 무엇을 기록했는지 열어 본다.

여기까지는 Git 저장소를 만들지 않았다. 이후의 브랜치·`git diff`·clone 실습 전에
[배포 가이드](github_distribution.md)를 따라 `.gitignore`와 실행 README를 작성하고,
이 개인 실습 폴더에서 `git init` 후 환경 파일·`hello.py`를 지정해 첫 커밋을 만든다.
GitHub에서 clone하려면 해당 개인 저장소에 커밋을 push해 두어야 한다.

### 실행 형태를 구분하기

| 형태 | 용도 | 전제 |
|---|---|---|
| `uv run hello.py` | Python 파일 실행 | 파일이 현재 경로에 있음 |
| `uv run python hello.py` | Python 인터프리터를 명시해 파일 실행 | 위와 같음 |
| `uv run python -m oss_tool.cli greet` | 설치된 패키지의 모듈 실행 | 3주차 `period3` 프로젝트에서 실행 |
| `uv run oss-tool greet` | 등록된 CLI 실행 | `[project.scripts]`와 빌드 설정이 있음 |

uv 옵션은 실행할 명령 앞에 둔다. 예를 들어 `uv run --locked oss-tool greet --name student01`에서
`--locked`는 uv 옵션, `--name`은 `oss-tool` 옵션이다.
[프로젝트 명령 실행](https://docs.astral.sh/uv/concepts/projects/run/) 문서에서 추가 실행 방식을 확인할 수 있다.

## 기존 수업 예제 실행하기

교재에는 하나의 공용 Python 환경이 아니라 **예제별 `pyproject.toml`**이 있다.
`teaching_repo` 최상위에서 바로 실행하지 말고 해당 예제 폴더로 이동한다.

```text
cd open_source_ai/weeks/week03_reproducible_python/examples/period3
uv sync
uv run oss-tool greet --name student01
uv run oss-tool sysinfo --json
uv run oss-tool config
```

위 명령은 `teaching_repo`에서 시작하는 경우다. 이미 예제 폴더에 있다면 `cd`를 반복하지 않는다.
현재 교재 원본 예제에는 아직 배포용 `uv.lock`이 없으므로 첫 `uv sync`로 해석한다.
강의자는 환경 기준표 확정 후 기준 PC에서 lock을 생성·검증해 배포본에 커밋한다.
lock이 포함된 배포본을 받았다면 첫 설치부터 `uv sync --locked`, 실행도 `uv run --locked ...`로 바꾼다.

프로젝트를 다른 위치에서 지정할 때, 다음 명령은 `teaching_repo` 최상위에서 실행한다.

```text
uv run --project open_source_ai/weeks/week03_reproducible_python/examples/period3 oss-tool greet
```

`--project`는 프로젝트를 선택하지만 **현재 작업 디렉터리는 바꾸지 않는다**.
`.env`, `docs/`, `outputs/`처럼 상대 경로를 쓰는 예제는 그 폴더로 `cd`한 뒤 실행하는 편이 명확하다.
`uv run`만 붙인다고 `.env`가 자동으로 로드되지는 않는다. 예제 코드가 `python-dotenv`로 읽거나,
의도적으로 `uv run --env-file .env ...`를 사용해야 한다. 3주차는 설정 출처를 관찰하기 위해 코드의 설정 로더를 사용한다.

## 의존성 추가와 업데이트

새 프로젝트 `uv-hello` 폴더에서 다음 명령을 비교한다.

| 할 일 | 명령 | 관찰할 변화 |
|---|---|---|
| 실행 의존성 추가 | `uv add httpx` | 선언·lock·환경에 반영 |
| 개발 도구 추가 | `uv add --dev ruff` | 개발 의존성에 기록, `uv run ruff check hello.py`로 실행 |
| 개발 도구 제거 | `uv remove --dev ruff` | 선언과 lock을 함께 갱신 |
| 현재 선언을 해석 | `uv lock` | lock 생성·갱신. 패키지 설치는 하지 않음 |
| 패키지 하나 업데이트 | `uv lock --upgrade-package httpx` | 허용 범위 내 새 버전을 lock에 반영 |
| 전체 의존성 업데이트 | `uv lock --upgrade` | 모든 의존성의 호환되는 새 버전을 검토 |
| lock대로 설치 | `uv sync --locked` | lock 정합성 확인 후 환경 동기화 |

`uv self update`는 **uv 도구**, `uv python install`은 **Python 인터프리터**,
`uv lock --upgrade`는 **프로젝트 패키지**를 다룬다. 하나를 실행했다고 다른 둘까지 업데이트되지 않는다.
`uv sync`나 `uv run`은 매번 모든 패키지를 최신으로 올리는 명령이 아니다. 유효한 lock이 있으면 기존 해석을 우선한다.

업데이트는 별도 브랜치에서 수행한다. `uv lock --upgrade-package httpx` 뒤 `uv sync --locked`와 예제 실행을 확인하고,
`git diff -- pyproject.toml uv.lock`으로 변경을 검토한다. 제약 때문에 버전이 그대로일 수 있고,
한 패키지를 올리면서 전이 의존성도 바뀔 수 있다. 성공한 lock을 팀에 공유한다.
명령 동작은 [lock·동기화 안내](https://docs.astral.sh/uv/concepts/projects/sync/)를 따른다.

프로젝트에 필요한 패키지는 `uv add`로 선언과 lock에 함께 기록한다.
선언하지 않은 패키지는 다음 `uv sync`에서 제거될 수 있고, 동료의 clone에는 전달되지 않는다.

## 다른 PC에서 환경 재현하기

| 명령 | lock 처리 | 사용할 상황 |
|---|---|---|
| `uv sync` / `uv run ...` | 필요하면 lock 생성·갱신 | 새 예제 준비, 개발 중 선언 반영 |
| `uv sync --locked` / `uv run --locked ...` | lock이 없거나 선언과 맞지 않으면 실패 | 제출·배포·CI에서 상태 검증 |
| `uv sync --frozen` / `uv run --frozen ...` | 기존 lock 사용, 선언과의 정합성 검사는 생략 | 이미 따로 정합성을 확인한 절차 |

`--frozen`도 lock 파일은 필요하다. "더 엄격한 검사"라는 뜻이 아니다.
깨끗한 clone에서 `uv sync --locked` 후 `uv run --locked`로 실행하면 실행 단계에서 lock이 다시 바뀌는 것도 막을 수 있다.
`--locked`는 다운로드를 금지하는 옵션은 아니다. 오프라인 실행에는 `--offline`과 필요한 Python·패키지 캐시가 별도로 필요하다.

프로젝트 루트의 기본 배포물은 다음과 같다. [배포 가이드](github_distribution.md)의 `.gitignore`와 점검 절차도 적용한다.

```text
uv-hello/
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
├── hello.py
└── README.md          # 설치·실행 위치·명령·검증한 환경
```

GitHub에서 clone한 뒤 이 폴더로 이동하여 실행한다.

```text
uv sync --locked
uv run --locked python hello.py
git status --short
```

`.venv/`는 보내지 않고 각 PC에서 만든다. macOS 환경 폴더를 Windows로 복사해도 재현 방법이 되지 않는다.
`uv.lock`은 Python 패키지 재현의 기준이며 GPU 드라이버·CUDA·Ollama 모델 가중치까지 담지 않는다.
AI 결과를 비교하려면 모델 ID·revision/태그·설정·하드웨어 조건도 환경 기준표와 README에 기록한다.

## 한 파일짜리 예제와 도구 실행

과제와 팀 프로젝트는 위의 `pyproject.toml` 방식을 기본으로 한다. 짧은 예제 한 파일을 나눌 때는
PEP 723 메타데이터로 의존성을 파일 안에 적을 수 있다. 다음 내용을 `one_file.py`로 저장한다.

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx"]
# ///

import httpx

print("httpx:", httpx.__version__)
```

```text
uv run one_file.py
uv lock --script one_file.py
uv run --locked one_file.py
```

이 방식은 프로젝트와 별도의 환경을 사용한다. 프로젝트 안에 파일을 두어도 프로젝트 의존성을 자동 상속하지 않는다.
재현용 배포에는 `one_file.py`와 생성된 `one_file.py.lock`을 함께 넣고, `*.lock`으로 제외하지 않는다.
[단일 스크립트 공식 안내](https://docs.astral.sh/uv/guides/scripts/)에 생성·의존성 추가 명령도 있다.

단발 실험은 `uv run --no-project --with httpx python -c "import httpx; print(httpx.__version__)"`처럼 실행할 수도 있다.
`--with`는 의존성을 프로젝트에 기록하지 않으므로 제출할 코드의 설치 방법으로 남발하지 않는다.
도구만 잠깐 실행하려면 `uvx ruff --version`을 쓸 수 있다. 팀이 도구 버전까지 공유하려면
개발 의존성에 추가하고 `uv run ruff ...`로 실행한다.

## 문제 해결과 확인 과제

| 증상 | 먼저 확인할 것 |
|---|---|
| `uv`를 찾을 수 없음 | 설치 완료 여부, 새 터미널·VS Code 재시작, 실행 파일 PATH |
| 패키지를 설치했는데 import 실패 | 현재 폴더의 `pyproject.toml`, `uv run python -c "import sys; print(sys.executable)"` |
| Python 요구 버전 오류 | `requires-python`, `.python-version`, `uv python list` |
| `--locked`가 실패 | lock 누락·선언 변경 확인. 배포자에게 확인하거나 의도한 변경이면 `uv lock` 후 재검증 |
| `oss-tool` 명령을 찾지 못함 | 예제 폴더인지, `[project.scripts]`·`[build-system]`이 있는지, `uv sync` 성공 여부 |
| `.env` 또는 입력 파일을 못 찾음 | 현재 작업 디렉터리, 예제 코드의 설정 로드 방식 |
| 설치한 적 없는 GPU 패키지 조합 오류 | 환경 기준표와 [PyTorch용 uv 안내](https://docs.astral.sh/uv/guides/integration/pytorch/) |

가상환경이 꼬였을 때는 인터프리터·선언·lock 상태를 먼저 진단한다. 정말 재생성이 필요하면
작업 중인 파일이 `.venv` 안에 없는지 확인한 뒤 **그 프로젝트의 `.venv`만** 제거하고 `uv sync --locked`로 만든다.
lock 파일까지 지워서 오류를 숨기면 기존 배포 환경과 달라질 수 있다.

복습 때 다음 증거를 남긴다.

1. `uv --version`, `uv run python --version`, 실행 파일 경로를 기록한다.
2. 새 프로젝트에서 `hello.py`를 두 실행 형태로 실행하고, 활성화 없이 동작한 이유를 적는다.
3. `uv add --dev ruff` 후 `uv run ruff check hello.py`를 실행하고 선언·lock 변경을 비교한다.
4. 배포한 저장소를 새 폴더에 clone해 `uv sync --locked`와 `uv run --locked`가 성공하는지 확인한다.
5. [Git 제외 점검](github_distribution.md)을 따라 `.venv`·실제 `.env`는 빠지고 lock·예제 설정·입력 자료는 포함되는지 확인한다.
