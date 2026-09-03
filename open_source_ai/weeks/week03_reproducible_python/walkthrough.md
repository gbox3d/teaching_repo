# 3주차 따라하기 — uv 프로젝트, oss-tool CLI, 설정 로더

이 문서는 3주차 시연·실습을 **순서대로 그대로 재현**하기 위한 절차서다.
강의자는 각 교시의 20분 시연을 이 순서로 진행하고, 학생은 실습·복습 때 같은 순서로 따라 한다.
각 단계는 `할 일 → 예상 결과 → 확인` 순서로 되어 있다. 예상 결과가 다르면 다음 단계로 넘어가지 않는다.

## 시작 전 준비

- Git, VS Code, uv, PowerShell(7 권장)이 설치되어 있다. 정확한 버전은 환경 기준표가 정한다. 전역 `pip install`은 쓰지 않는다.
- 2주차까지 쓴 개인 저장소가 GitHub와 연결되어 있고 `git status`가 clean이다. 이 문서는 그 폴더를 `C:\classwork\osa-practice`로 적는다(1주차 이름이 `osa-week01`이면 그 경로).
- 수업 전에 [`examples/oss_tool`](examples/README.md)에서 `uv sync`를 한 번 실행해 `httpx`·`python-dotenv`·`hatchling`을 캐시해 둔다. 실습 중 새 패키지를 내려받지 않는다.
- 예제는 개인 실습 폴더 `C:\classwork\week03`에 **복사**해서 쓴다. 수업 자료 원본은 수정하지 않는다.
- 터미널 명령은 현재 경로를 먼저 확인하고 실행한다. 이번 주는 GPU·모델·Ollama 서버가 필요 없다.

---

## 1교시 — uv 프로젝트를 만들고 깨끗한 폴더에서 재현하기

### 단계 1. 저장소 상태 확인과 예제 복사

**할 일**

```powershell
Set-Location C:\classwork\osa-practice
git status
git remote -v
$src = "<교재 저장소>\open_source_ai\weeks\week03_reproducible_python\examples"
New-Item -ItemType Directory -Force C:\classwork\week03 | Out-Null
Copy-Item "$src\reproduce_check.ps1" C:\classwork\week03\
New-Item -ItemType Directory -Force notes | Out-Null
Copy-Item "$src\week03_notes_template.md" notes\week03.md
```

**예상 결과** — `nothing to commit, working tree clean`과 `origin` 두 줄이 보인다. `notes\week03.md`가 생기고 `git status`에 `notes/`가 untracked로 나타난다.

**확인** — [ ] `notes\week03.md` 1절 예상표를 실행 전에 채웠다.

### 단계 2. `uv init`과 `uv add httpx`

**할 일**

```powershell
uv init
git status --short
Remove-Item main.py
uv add httpx
Get-ChildItem -Force
git status --short
Get-Content .venv\.gitignore
```

**예상 결과** — `uv init`이 `Initialized project`를 출력하고 `.python-version`, `main.py`, `pyproject.toml` 세 파일이 untracked로 생긴다(`README.md`·`LICENSE`는 그대로). `uv add httpx`가 `Resolved …`, `Installed …`와 `+ httpx==<버전>` 줄을 출력하고 `.venv\`와 `uv.lock`이 생긴다. `git status`에 `.venv/`는 보이지 않는다. `.venv\.gitignore`의 내용이 `*` 한 줄이기 때문이다.

**확인** — [ ] `pyproject.toml`의 `dependencies`에 `"httpx"`가 들어갔고 `uv.lock`에 `httpx` 외에 함께 끌려온 패키지들이 `[[package]]`로 적혀 있다.

### 단계 3. 루트 `.gitignore`와 첫 commit, `uv lock` 다시 실행

**할 일**

1. `code .gitignore`로 루트 `.gitignore`를 만들고 네 줄을 적는다: `.venv/`, `__pycache__/`, `*.pyc`, `outputs/`. `.env`는 3교시에 넣는다.
2. 네 파일만 stage하고 commit한 뒤 `uv lock`을 한 번 더 실행한다.

```powershell
git add .gitignore .python-version pyproject.toml uv.lock
git status
git commit -m "Add uv project"
uv lock
git status
```

**예상 결과** — stage 목록에 네 파일만 있고 `first_run/`·`reports/`는 바뀌지 않는다. commit 뒤 `uv lock`은 `Resolved N packages`만 출력하고 `git status`에는 tracked 변경 없이 단계 1에서 만든 `notes/`만 untracked로 남는다(같은 입력이면 lock은 바뀌지 않는다).

**확인** — [ ] `git log -1 --stat`에 네 파일이 보인다.

### 단계 4. `reproduce_check.ps1`로 깨끗한 폴더 재현

**할 일**

```powershell
Set-Location C:\classwork\week03
.\reproduce_check.ps1 -Source C:\classwork\osa-practice -Dest C:\classwork\_repro\osa-practice -Check 'uv run python -c "import httpx; print(httpx.__version__)"' -Keep
Get-Content (Get-ChildItem outputs\reproduce-*.md | Select-Object -Last 1)
```

**예상 결과** — 화면에 `[OK] 1. git clone`, `[OK] 2. 복제본 점검 …`, `[OK] 3. uv sync --frozen`, `[OK] 4. 확인 명령 …`이 차례로 나오고 종료 코드는 0이다. 로그의 2단계 표에 `.venv 존재: False`, `.env 존재: False`, `uv.lock 존재: True`, 3단계에 `Creating virtual environment`와 설치 목록, 4단계에 `httpx` 버전 문자열이 있다.

**확인** — [ ] 로그를 `C:\classwork\osa-practice\notes\week03_reproduce.md`로 복사했다. 홈 경로가 들어 있으면 지웠다.

### 단계 5. `uv.lock` 없이 `--frozen`

**할 일**

```powershell
Set-Location C:\classwork\_repro\osa-practice
Remove-Item uv.lock
uv sync --frozen
$LASTEXITCODE
uv sync
git status --short
git diff --stat
Set-Location C:\classwork\osa-practice
git push
```

**예상 결과** — `uv sync --frozen`이 `uv.lock`(lockfile)을 찾을 수 없다는 오류 한 줄을 내고 종료 코드는 0이 아니다. 플래그 없는 `uv sync`는 다시 해석해 `uv.lock`을 만든다. 같은 날 같은 인덱스면 `git diff --stat`이 비어 있거나 줄 끝 차이만 보인다. push 뒤 GitHub에 `pyproject.toml`·`uv.lock`이 보인다.

**확인** — [ ] 오류 첫 줄과 종료 코드를 `notes\week03.md`에 적었다. [`lab.md`](lab.md) 1교시 완료 조건을 모두 표시했다. 실습 30분 뒤 휴식 10분.

---

## 2교시 — oss-tool CLI 완성하기

### 단계 1. 패키지 뼈대와 greet

**할 일**

1. `src\oss_tool\__init__.py`를 만들고 `__version__ = "0.1.0"`을 적는다.
2. `src\oss_tool\cli.py`를 만든다. `build_parser()`(`ArgumentParser(prog="oss-tool")`, `add_subparsers(dest="command", required=True)`, `greet` 서브파서와 `--name` 기본값 `student01`), `cmd_greet(args)`(인사말 출력, `0` 반환), `main()`(`parse_args()` 뒤 `args.func(args)` 반환), 파일 끝의 `if __name__ == "__main__": sys.exit(main())`.
3. 엔트리포인트 없이 먼저 모듈로 실행해 본다.

```powershell
Set-Location C:\classwork\osa-practice
uv run python src\oss_tool\cli.py greet --name student01
```

**예상 결과** — 인사말 한 줄이 나온다. 아직 `uv run oss-tool`은 없다.

**확인** — [ ] `notes\week03.md` 2절 예상표를 실행 전에 채웠다.

### 단계 2. `[project.scripts]`와 `uv sync`

**할 일** — `pyproject.toml`에 `[project.scripts] oss-tool = "oss_tool.cli:main"`, `[build-system]`(hatchling), `[tool.hatch.build.targets.wheel] packages = ["src/oss_tool"]` 세 블록을 추가하고 실행한다.

```powershell
uv sync
Get-ChildItem .venv\Scripts\oss-tool*
uv run oss-tool greet --name student01
uv run oss-tool --help
```

**예상 결과** — `uv sync`가 `Building osa-practice @ file:///…`와 `+ osa-practice==0.1.0 (from file:///…)`를 출력한다. `.venv\Scripts\oss-tool.exe`가 생기고 `uv run oss-tool greet --name student01`이 단계 1과 같은 인사말을 낸다. `--help`에 `{greet}`가 보인다.

**확인** — [ ] `git diff --stat`에 `uv.lock`도 바뀐 것이 보인다(프로젝트 자신이 lock에 들어갔다).

### 단계 3. sysinfo 서브커맨드와 stdout/stderr 분리

**할 일**

1. `src\oss_tool\sysinfo.py`를 만든다. 1주차 `first_run\sysinfo.py`의 수집 함수를 옮겨 `collect()`로 정리하거나 예제 `$src\oss_tool\src\oss_tool\sysinfo.py`를 복사한다.
2. `cli.py`에 `sysinfo` 서브파서(`--json`)와 `cmd_sysinfo`를 추가한다. 결과는 `print`로 stdout에, `outputs\sysinfo-<시각>.json` 저장 경로는 `logging`으로 stderr에. `main()`에 `logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(levelname)s %(name)s: %(message)s")`를 넣는다.
3. 실행한다.

```powershell
uv run oss-tool sysinfo
uv run oss-tool sysinfo --json
uv run oss-tool sysinfo --json | Out-String | ConvertFrom-Json | Select-Object os, python
uv run oss-tool sysinfo --json 2>$null | Out-String | ConvertFrom-Json | Select-Object gpu
Get-ChildItem outputs
git status --short
```

**예상 결과** — 첫 명령은 OS·CPU·RAM·Python·GPU 요약 다섯 줄과 stderr의 `INFO oss_tool: 저장: outputs\sysinfo-….json`을 낸다. `--json`은 JSON 전체를 내고, 파이프를 거친 결과는 `os`·`python` 두 속성을 가진 객체다. `2>$null`로 로그를 버려도 `gpu` 객체가 나온다. GPU가 없는 PC에서는 `available: False`와 이유가 보인다. `outputs\`에 JSON이 쌓이지만 `git status`에는 없다.

**확인** — [ ] 로그가 stdout에 섞이지 않는다(섞이면 `ConvertFrom-Json`이 실패한다).

### 단계 4. 엔트리포인트 오타 재현

**할 일** — `pyproject.toml`의 `oss_tool.cli:main`을 `oss_tool.cli:mian`으로 바꾸고 실행한 뒤 되돌린다.

```powershell
uv run oss-tool greet
```

**예상 결과** — `uv run`이 바뀐 프로젝트를 다시 설치하는 줄(`~ osa-practice==0.1.0`)을 낸 뒤 실행 단계에서 `ImportError: cannot import name 'mian' from 'oss_tool.cli'`로 끝난다. 설치는 통과하고 실행이 실패한다. `main`으로 되돌리고 다시 실행하면 인사말이 나온다.

**확인** — [ ] 오류 마지막 줄과 실패 시점을 `notes\week03.md`에 적었다.

### 단계 5. README 세 줄과 commit

**할 일** — `README.md`에 `## 실행` 절과 세 줄(`uv sync --frozen`, `uv run oss-tool greet --name student01`, `uv run oss-tool sysinfo --json`)을 적고 commit·push한다.

```powershell
git add src pyproject.toml uv.lock README.md
git status
git commit -m "Add oss-tool CLI with greet and sysinfo"
git push
```

**예상 결과** — stage 목록에 `src/oss_tool/` 세 파일, `pyproject.toml`, `uv.lock`, `README.md`가 있고 `outputs/`·`.venv/`는 없다.

**확인** — [ ] [`lab.md`](lab.md) 2교시 완료 조건을 모두 표시했다. 실습 30분 뒤 휴식 10분.

---

## 3교시 — 설정 로더와 비밀정보 분리

### 단계 1. `uv add python-dotenv`와 config.py

**할 일**

```powershell
Set-Location C:\classwork\osa-practice
uv add python-dotenv
git diff --stat
```

이어서 `src\oss_tool\config.py`를 만든다. `DEFAULTS`(`OLLAMA_HOST`, `OLLAMA_MODEL`), `load_settings(overrides, env_file=".env")`(기본값 → `dotenv_values` → `os.environ` → `overrides` 순서로 덮어쓰며 출처 기록), 비밀 키 가리기. 예제 `config.py`를 가져와도 된다.

**예상 결과** — `git diff --stat`에 `pyproject.toml`과 `uv.lock`이 함께 보인다.

**확인** — [ ] `notes\week03.md` 3절 예상표를 실행 전에 채웠다.

### 단계 2. config 서브커맨드 첫 실행

**할 일** — `cli.py`에 `config` 서브파서(`--host`, `--model`, `--json`)와 `cmd_config`를 추가하고 실행한다.

```powershell
uv run oss-tool config
```

**예상 결과** — `OLLAMA_HOST = http://localhost:11434 [default]`, `OLLAMA_MODEL = qwen3:8b [default]`처럼 값과 출처가 한 줄씩 나온다. `HF_TOKEN`을 선택 키로 넣었다면 `(비어 있음) [default]`다.

**확인** — [ ] 출처 열이 모두 `default`다.

### 단계 3. `.env.example` → `.env` → 셸 변수 → 인자

**할 일**

1. `.env.example`을 VS Code로 만들고(`OLLAMA_HOST`, `OLLAMA_MODEL`, `HF_TOKEN=` 세 키와 설명 주석) commit한다.
2. `.env`로 복사해 `OLLAMA_MODEL=qwen3:0.6b`, `HF_TOKEN=hf_fake_token_for_class_only`로 바꾸고 세 가지 방법으로 실행한다.

```powershell
git add .env.example
git commit -m "Add .env.example"
Copy-Item .env.example .env
code .env
uv run oss-tool config
$env:OLLAMA_MODEL = "qwen3:1.7b"
uv run oss-tool config
uv run oss-tool config --model qwen3:14b
Remove-Item Env:OLLAMA_MODEL
```

**예상 결과** — 첫 실행은 `OLLAMA_MODEL = qwen3:0.6b [.env]`와 `HF_TOKEN = (설정됨, 가려짐) [.env]`. 둘째는 `qwen3:1.7b [env]`. 셋째는 `qwen3:14b [arg]`. `OLLAMA_HOST`는 `.env` 값이 기본값과 같아도 출처가 `.env`로 바뀐다.

**확인** — [ ] `notes\week03.md`의 출처 관찰표 네 행을 채웠다.

### 단계 4. `.env` 실수 재현과 복구

**할 일**

```powershell
git add .
git status
git restore --staged .env
git status
code .gitignore
git status
git check-ignore -v .env
```

`code .gitignore`에서 `.env` 한 줄을 추가한다(`.env*` 패턴은 쓰지 않는다).

**예상 결과** — 첫 `git status`에 `new file:   .env`가 staged로 보인다. `restore --staged` 뒤에는 untracked로 내려온다. `.gitignore`에 `.env`를 넣으면 `git status`에서 사라지고, `git check-ignore -v .env`가 `.gitignore:<줄>:.env	.env`를 출력한다. `.env.example`은 여전히 tracked다.

**확인** — [ ] 세 시점의 `git status` 줄을 `notes\week03.md`에 적었다.

### 단계 5. 이력 검사와 commit·push

**할 일**

```powershell
git log --all --oneline -- .env
git log --all --oneline -S "hf_fake_token"
git add .gitignore pyproject.toml uv.lock src notes
git status
git commit -m "Add config loader and ignore .env"
git push
uv run oss-tool config --json
```

**예상 결과** — 두 검사 명령이 아무것도 출력하지 않는다(`.env`도 가짜 토큰도 이력에 없다). stage 목록에 `.env`가 없다. `config --json`이 키마다 `value`·`source`·`secret`을 가진 JSON을 낸다. 4주차 클라이언트는 이 로더를 그대로 쓴다.

**확인** — [ ] 검사 결과를 문장으로 `notes\week03.md`에 적었다. [`lab.md`](lab.md) 3교시 완료 조건을 모두 표시했다. 실습 30분 뒤 휴식 10분. 이번 주 종료.

---

## 문제가 생겼을 때

| 증상 | 이 문서에서 돌아갈 단계 |
|---|---|
| `uv init`이 이미 프로젝트가 있다고 거부한다 | 1교시 단계 2 (루트 `pyproject.toml` 확인. `first_run/`은 원인이 아님) |
| `uv add httpx`가 다운로드하려다 실패한다 | 1교시 단계 2 (`--offline` 추가. 수업 전 캐시 전제) |
| `git status`에 `.venv/`가 보인다 | 1교시 단계 3 (루트 `.gitignore`의 `.venv/` 줄, 다른 도구로 만든 venv인지 확인) |
| `reproduce_check.ps1`이 열리지 않거나 한글이 깨진다 | 1교시 단계 4 (`pwsh -ExecutionPolicy Bypass -File`, PowerShell 7) |
| 재현 검사 2단계가 FAIL이다 | 1교시 단계 3 (`uv.lock`이 commit되었는지, `.env`·`.venv`가 tracked인지) |
| `uv run oss-tool`이 명령을 찾지 못한다 | 2교시 단계 2 (`[project.scripts]`·`[build-system]`·hatch `packages` 세 블록, `uv sync`) |
| `No module named 'oss_tool'` | 2교시 단계 1·2 (`src\oss_tool\__init__.py` 존재, hatch `packages` 경로) |
| `ConvertFrom-Json`이 깨진다 | 2교시 단계 3 (로그를 stderr로, `Out-String` 사용) |
| `.env` 값을 바꿨는데 `[default]`다 | 3교시 단계 3 (현재 폴더의 `.env`인지, `KEY=value` 형식) |
| 셸 변수를 지웠는데 `[env]`다 | 3교시 단계 3 (`Remove-Item Env:OLLAMA_MODEL`, 새 터미널) |
| `.gitignore`에 넣었는데 `.env`가 계속 보인다 | 3교시 단계 4 (`restore --staged` 또는 `rm --cached`; push되었으면 토큰 회전) |
| `.env.example`까지 사라졌다 | 3교시 단계 4 (`.env*` 패턴을 `.env`로) |

세부 판정 기준과 힌트는 [`lab.md`](lab.md)에 있다. 정답과 해설은 실습이 끝난 뒤 강의자가 별도로 안내한다.
