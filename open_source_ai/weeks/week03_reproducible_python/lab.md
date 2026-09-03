# 3주차 실습 — 넣을 것과 뺄 것을 가려 재현하라

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 실습 시간에 새 패키지를 찾아 추가하지 않는다. 이번 주에 쓰는 `httpx`·`python-dotenv`·`hatchling`은 수업 전 예제 `uv sync`로 캐시되어 있다. 전역 `pip install`은 쓰지 않는다.
- 실제 토큰·비밀번호는 `.env`에도 쓰지 않는다. 실습에서 쓰는 가짜 토큰은 `hf_fake_token_for_class_only`처럼 가짜임이 드러나는 문자열만 쓴다.
- `git push --force`, `git reset --hard`처럼 기록을 지우는 명령은 쓰지 않는다. 막히면 힌트를 읽고, 그래도 안 되면 강의자를 부른다.

## 1교시 실습 — uv 프로젝트를 만들고 깨끗한 폴더에서 재현하기

**이어받는 것:** 2주차까지 쓴 개인 저장소(GitHub 원격 연결, `LICENSE`, 1주차의 `first_run/`·`reports/` 포함). 이 문서는 그 폴더를 `C:\classwork\osa-practice`로 적는다. 1주차에 만든 이름이 `osa-week01`이면 그 경로를 그대로 쓴다.

### 상황

2주차에 짝이 내 저장소를 clone해 `first_run/sysinfo.py`를 돌리려다 "무엇을 어떻게 설치하라는 것인지 모르겠다"고 했다. 저장소 루트를 uv 프로젝트로 바꾸고, 다른 폴더에 clone해도 같은 환경이 만들어지는지 검사하라. 검사가 통과한 뒤에는 `uv.lock`을 지워 보고 무엇이 달라지는지 관찰하라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 저장소 상태 확인, 예제 복사, 예상표 작성 |
| 프로젝트 만들기 | 5–13분 | `uv init` → `uv add httpx` → 루트 `.gitignore` → commit → `uv lock` |
| 깨끗한 폴더 재현 | 13–20분 | `reproduce_check.ps1`로 clone → `uv sync --frozen` → `import httpx` |
| 실패 경로 | 20–25분 | 복제본에서 `uv.lock` 삭제 → `--frozen` 실패 → 플래그 없는 `uv sync` |
| 검증·기록 | 25–30분 | 재현 로그를 `notes/`로 복사, 오류 첫 줄·설명 문장 기록, push |

### 준비

개인 저장소로 이동해 상태를 확인한다. `git status`가 clean이고 `git remote -v`에 원격이 보여야 시작한다.

```powershell
Set-Location C:\classwork\osa-practice
git status
git remote -v
git log --oneline -3
uv --version
```

저장소가 없거나 다른 PC라면 2주차 실습지의 준비 절차대로 만들고 GitHub와 연결한다. 수업 자료 저장소 안에서 `uv init`이나 `git init`을 하지 않는다.

예제는 원본을 두고 복사한다. `$src`에는 교재 저장소의 이 주차 `examples` 폴더 경로를 넣는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week03_reproducible_python\examples"
New-Item -ItemType Directory -Force C:\classwork\week03 | Out-Null
Copy-Item "$src\reproduce_check.ps1" C:\classwork\week03\
New-Item -ItemType Directory -Force C:\classwork\osa-practice\notes | Out-Null
Copy-Item "$src\week03_notes_template.md" C:\classwork\osa-practice\notes\week03.md
```

### 문제 1 · 저장소 루트를 uv 프로젝트로 바꾸기

1. 실행 전에 `notes/week03.md` 1절의 예상표를 채운다.

| 관찰 대상 | 예상 | 실제 |
|---|---|---|
| `uv init` 뒤 새로 생기는 파일 |  |  |
| `uv add httpx` 뒤 새로 생기는 파일·폴더 |  |  |
| `uv add httpx` 뒤 `git status`에 `.venv/`가 보이는가 |  |  |
| clone한 복제본에 있는 것과 없는 것 |  |  |
| 복제본에서 `uv.lock`을 지우고 `uv sync --frozen`하면 |  |  |

2. 저장소 루트에서 `uv init`을 실행하고 `git status --short`로 새로 생긴 파일을 확인한다. `README.md`와 `LICENSE`는 그대로 남는다. 샘플 스크립트 `main.py`는 지운다(2교시에서 `src/` 아래에 진짜 코드를 만든다).

```powershell
uv init
git status --short
Remove-Item main.py
Get-Content pyproject.toml
```

3. `uv add httpx`를 실행한다. `Get-ChildItem -Force`로 `.venv\`와 `uv.lock`이 생겼는지 보고, `git status --short`에 `.venv/`가 보이는지 확인한다. 보이지 않는다면 그 이유를 `Get-Content .venv\.gitignore`로 찾아 예상표에 적는다.

```powershell
uv add httpx
Get-ChildItem -Force
git status --short
Get-Content .venv\.gitignore
```

4. 루트 `.gitignore`를 VS Code로 만든다(`code .gitignore`). PowerShell의 `Out-File`·`Set-Content`는 BOM·줄 끝 문제가 생길 수 있으므로 편집기로 만든다. `.env`는 3교시에서 실수를 재현한 뒤 넣는다.

```text
.venv/
__pycache__/
*.pyc
outputs/
```

5. 네 파일만 stage하고 stage 목록을 읽은 뒤 commit한다. commit 뒤 `uv lock`을 한 번 더 실행해 tracked 파일이 그대로인지 본다(준비 절에서 복사한 `notes/`는 아직 untracked로 남아 있는 것이 정상이다).

```powershell
git add .gitignore .python-version pyproject.toml uv.lock
git status
git commit -m "Add uv project"
uv lock
git status
```

완료 조건:

- [ ] `git log -1 --stat`에 `.gitignore`, `.python-version`, `pyproject.toml`, `uv.lock` 네 파일이 있다.
- [ ] commit 뒤 `uv lock`을 다시 실행해도 tracked 파일에 변경이 없다(`git status --short`에 `?? notes/`만 남는다).
- [ ] `.venv/`가 `git status`에 보이지 않는 이유를 예상표에 한 문장으로 적었다.

### 문제 2 · 깨끗한 폴더에서 재현하고, lock을 지워 보기

1. 재현 검사를 실행한다. `-Keep`을 주어 복제본을 남긴다(실패 경로에서 쓴다).

```powershell
Set-Location C:\classwork\week03
.\reproduce_check.ps1 -Source C:\classwork\osa-practice -Dest C:\classwork\_repro\osa-practice -Check 'uv run python -c "import httpx; print(httpx.__version__)"' -Keep
```

2. `C:\classwork\week03\outputs\reproduce-<시각>.md`를 열어 네 단계가 모두 OK인지, 2단계 표에서 복제본에 `.venv`·`.env`가 없고 `uv.lock`이 있는지, 3단계에 설치된 패키지 목록이 있는지, 4단계에 `httpx` 버전이 찍혔는지 확인한다. 로그를 저장소의 `notes/`로 복사한다(사용자 홈 경로가 들어 있으면 지운다).

```powershell
Copy-Item (Get-ChildItem outputs\reproduce-*.md | Select-Object -Last 1) C:\classwork\osa-practice\notes\week03_reproduce.md
```

3. 실패 경로. 복제본에서 `uv.lock`을 지우고 `--frozen`으로 sync한다. 오류 첫 줄과 종료 코드를 `notes/week03.md`에 적는다.

```powershell
Set-Location C:\classwork\_repro\osa-practice
Remove-Item uv.lock
uv sync --frozen
$LASTEXITCODE
```

4. 같은 폴더에서 플래그 없이 `uv sync`를 실행한다. `uv.lock`이 다시 생기는지, `git status --short`·`git diff --stat`으로 내용이 commit된 것과 같은지 본다. 같은 날 같은 인덱스에서 해석하면 내용이 같을 수 있다(줄 끝 차이만 보일 수 있다). 몇 달 뒤 같은 명령은 다른 버전을 고를 수 있다는 것이 lock을 커밋하는 이유다.

```powershell
uv sync
git status --short
git diff --stat
```

5. 원본 저장소로 돌아가 push한다. 복제본은 지워도 된다.

```powershell
Set-Location C:\classwork\osa-practice
git push
Remove-Item -Recurse -Force C:\classwork\_repro
```

완료 조건:

- [ ] `notes/week03_reproduce.md`에 네 단계가 모두 OK인 로그가 있다.
- [ ] `uv.lock`이 없을 때 `uv sync --frozen`의 오류 첫 줄과 종료 코드를 적었다.
- [ ] `--frozen`이 `pyproject.toml`이 아니라 `uv.lock`을 읽는다는 것을 한 문장으로 적었다.

### 단계별 힌트

<details>
<summary>힌트 1 — `uv init`이 이미 프로젝트가 있다고 거부한다</summary>

저장소 루트에 `pyproject.toml`이 이미 있다. 1주차의 `first_run/pyproject.toml`은 하위 폴더이므로 원인이 아니다. `Get-ChildItem pyproject.toml`로 루트 파일을 확인하고, 이전 시도의 흔적이면 내용을 읽은 뒤 지우고 다시 실행한다. `name`은 폴더 이름에서 오므로 `osa-week01`처럼 나와도 된다.
</details>

<details>
<summary>힌트 2 — `uv add httpx`가 다운로드하려다 실패한다(네트워크 없음)</summary>

캐시에 있는 것만 쓰도록 `--offline`을 붙인다. 수업 전에 예제 `oss_tool`에서 `uv sync`를 했다면 `httpx`와 그 의존성은 캐시에 있다.

```powershell
uv add --offline httpx
uv sync --frozen --offline
```

캐시에도 없으면 조교에게 알리고, 기다리는 동안 `.gitignore`와 예상표를 먼저 끝낸다.
</details>

<details>
<summary>힌트 3 — `reproduce_check.ps1`이 열리지 않거나 한글이 깨진다</summary>

실행 정책 오류면 `pwsh -ExecutionPolicy Bypass -File .\reproduce_check.ps1 -Source ...`처럼 실행한다. 한글 메시지가 깨지면 Windows PowerShell 5.1이다. 판정(OK/FAIL)과 로그 파일은 정상이므로 그대로 써도 되고, `pwsh`(PowerShell 7)로 다시 실행해도 된다. `-Dest` 폴더가 이미 있으면 스크립트가 멈추므로 `Remove-Item -Recurse -Force C:\classwork\_repro` 뒤 재실행한다.
</details>

### 검증

- 정상: 복제본에서 `uv run python -c "import httpx"`가 성공하고 로그의 네 단계가 모두 OK다. 복제본에는 `.venv`가 없었다가 `uv sync --frozen` 뒤 생긴다.
- 경계 또는 실패: 복제본에서 `uv.lock`을 지우면 `--frozen`이 0이 아닌 종료 코드로 실패하고, 플래그 없는 `uv sync`는 새 lock을 만든다.
- 설명: "`pyproject.toml`만 커밋하면 왜 재현이 아닌가"를 한 문장으로 적는다.

### 확장 문제

1. `pyproject.toml`의 `dependencies`에 `"python-dotenv"`를 손으로 추가하고 `uv sync --locked`를 실행해 lock이 낡았다는 오류를 관찰한다. `uv lock` 뒤 다시 실행해 통과하는지 본 다음 `git restore pyproject.toml uv.lock`으로 되돌린다(3교시에서 `uv add`로 제대로 추가한다).
2. `uv tree`로 `httpx`가 끌어온 패키지 트리를 보고 `uv.lock`의 `[[package]]` 개수와 비교한다.
3. `uv python list`로 이 PC에 있는 Python과 `.python-version`이 가리키는 것을 대조하고, `.python-version`을 커밋하는 이유를 적는다.

## 2교시 실습 — oss-tool CLI 완성하기

**이어받는 것:** 1교시의 uv 프로젝트(`pyproject.toml`, `uv.lock`, 루트 `.gitignore`)와 1주차 `first_run/sysinfo.py`. 하루가 바뀌었으면 `uv sync`를 한 번 실행하고 시작한다.

### 상황

팀 저장소 README에 "실행 방법: `python first_run/sysinfo.py`"라고 적었더니 "어느 폴더에서? 어떤 Python으로?"라는 질문이 돌아왔다. 1주차 스크립트를 이름 있는 명령 `oss-tool`의 서브커맨드로 바꾸고, 처음 보는 사람이 복사해 붙여넣기만 하면 되는 세 줄 실행 절차를 README에 적어라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 상태 확인, 예상표(명령 이름·패키지 이름·실패 시점) |
| greet 서브커맨드 | 5–13분 | `src/oss_tool/` 뼈대, `[project.scripts]`·빌드 백엔드, `uv sync`, greet 실행 |
| sysinfo 서브커맨드 | 13–21분 | `sysinfo.py` 모듈 배치, `--json`, `outputs/` 저장, logging은 stderr |
| 실패 경로·README | 21–25분 | 엔트리포인트 오타 재현·복구, README 실행 절차 3줄 |
| 검증·기록 | 25–30분 | `--help`·파이프 확인, 오류 줄 기록, commit·push |

### 준비

```powershell
Set-Location C:\classwork\osa-practice
git status
uv run python -c "import httpx; print('ok')"
$src = "<교재 저장소>\open_source_ai\weeks\week03_reproducible_python\examples"
```

`ok`가 출력되면 시작한다. 예제 `oss_tool`은 참조 구현이다. 막혔을 때 파일 단위로 열어 비교하고, 통째로 복사하지 않는다.

### 문제 1 · greet 서브커맨드와 엔트리포인트

1. `notes/week03.md` 2절의 예상표를 채운다. `[project.scripts]`에 함수 이름 오타(`mian`)가 있으면 `uv sync`가 실패하는가 실행이 실패하는가, `uv sync` 뒤 `.venv\Scripts`에 무엇이 생기는가, `uv run oss-tool greet`와 `uv run python src\oss_tool\cli.py greet`는 무엇이 다른가.
2. 패키지 뼈대를 만든다. `__init__.py`에는 `__version__ = "0.1.0"` 한 줄을 둔다.

```text
src/oss_tool/__init__.py
src/oss_tool/cli.py
```

3. `cli.py`에 argparse 서브커맨드 구조를 만든다. `build_parser()`가 `ArgumentParser(prog="oss-tool")`와 `add_subparsers(dest="command", required=True)`를 만들고, `greet` 서브파서에 `--name`(기본 `student01`)을 둔다. `cmd_greet(args)`는 이름이 들어간 인사말을 출력하고 `0`을 돌려준다. `main()`은 `parse_args()` 뒤 `args.func(args)`의 반환값을 돌려주고, 파일 끝에 `if __name__ == "__main__": sys.exit(main())`을 둔다.
4. `pyproject.toml`에 세 블록을 추가한다. 프로젝트 이름(`osa-practice`)과 패키지 이름(`oss_tool`)이 다르므로 마지막 블록이 필요하다.

```toml
[project.scripts]
oss-tool = "oss_tool.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/oss_tool"]
```

5. 설치하고 실행한다. `uv sync` 출력에 프로젝트 자신이 `(from file:///...)`로 설치되는 줄이 보여야 한다.

```powershell
uv sync
Get-ChildItem .venv\Scripts\oss-tool*
uv run oss-tool greet --name student01
uv run oss-tool --help
```

완료 조건:

- [ ] `uv run oss-tool greet --name student01`이 이름이 들어간 인사말을 출력한다.
- [ ] `.venv\Scripts\oss-tool.exe`가 생겼고, 그것을 만든 `pyproject.toml`의 줄을 예상표에 적었다.
- [ ] `uv run oss-tool --help`에 `greet`이 보인다.

### 문제 2 · sysinfo 서브커맨드, 실패 경로, README

1. `src/oss_tool/sysinfo.py`를 만든다. 1주차 `first_run/sysinfo.py`에서 수집 함수들을 옮기고 `argparse`·`main()`을 빼서 `collect() -> dict` 하나로 정리하거나, 예제 `$src\oss_tool\src\oss_tool\sysinfo.py`를 그대로 복사한다. GPU가 없으면 예외 대신 `available: false`와 이유를 담아 돌려줘야 한다.
2. `cli.py`에 `sysinfo` 서브커맨드를 추가한다. `--json`이 있으면 `json.dumps(info, ensure_ascii=True, indent=2)`를 stdout에, 없으면 사람이 읽을 요약을 출력한다. 결과는 항상 `outputs/sysinfo-<시각>.json`에 저장하고, 저장 경로는 `print`가 아니라 `logging`으로 남긴다. `main()`에서 `logging.basicConfig(level=logging.INFO, stream=sys.stderr, ...)`를 설정한다.
3. 실행하고 stdout과 stderr가 분리되는지 확인한다. Windows PowerShell 5.1은 여러 줄 입력을 바로 받지 못하므로 `Out-String`으로 한 문자열로 합쳐 넘긴다.

```powershell
uv run oss-tool sysinfo
uv run oss-tool sysinfo --json
uv run oss-tool sysinfo --json | Out-String | ConvertFrom-Json | Select-Object os, python
Get-ChildItem outputs
git status --short
```

`outputs/`가 `git status`에 보이면 1교시 `.gitignore`를 확인한다.

4. 실패 경로. `pyproject.toml`의 `oss_tool.cli:main`을 `oss_tool.cli:mian`으로 바꾸고 `uv run oss-tool greet`를 실행한다(`uv run`이 바뀐 프로젝트를 다시 설치한다). 오류의 마지막 줄과 "언제 실패했는가(sync 때인가 실행 때인가)"를 적고 되돌린 뒤 다시 실행한다.
5. `README.md`에 `## 실행` 절을 만들고 세 줄을 적는다. 옵션 설명은 `--help`에 맡긴다.

```markdown
## 실행

1. `uv sync --frozen`
2. `uv run oss-tool greet --name student01`
3. `uv run oss-tool sysinfo --json` (결과는 `outputs/`에 저장된다)
```

6. `git diff --stat`으로 `uv.lock`도 바뀌었는지 본 뒤 commit·push한다. 빌드 백엔드를 추가하면 프로젝트 자신이 lock에 들어간다.

```powershell
git add src pyproject.toml uv.lock README.md
git status
git commit -m "Add oss-tool CLI with greet and sysinfo"
git push
```

완료 조건:

- [ ] `uv run oss-tool sysinfo --json | Out-String | ConvertFrom-Json`이 오류 없이 객체를 만든다(결과는 stdout, 로그는 stderr).
- [ ] `outputs/sysinfo-*.json`이 생겼고 `git status`에 `outputs/`가 없다.
- [ ] 엔트리포인트 오타 때의 오류 마지막 줄과 실패 시점을 적었다.
- [ ] README에 실행 절차 3줄이 있고 commit·push했다.

### 단계별 힌트

<details>
<summary>힌트 1 — `uv run oss-tool`이 명령을 찾지 못한다(Failed to spawn, program not found)</summary>

`[project.scripts]`가 없거나 `[build-system]`이 없어 프로젝트가 `.venv`에 설치되지 않은 것이다. `uv sync` 출력에 `osa-practice==0.1.0 (from file:///...)` 줄이 있어야 하고, 그 뒤 `.venv\Scripts\oss-tool.exe`가 생긴다. 세 블록을 모두 넣었는지 확인하고 `uv sync`를 다시 실행한다.
</details>

<details>
<summary>힌트 2 — `uv sync`가 wheel에 넣을 파일을 정할 수 없다고 하거나, 실행하면 `No module named 'oss_tool'`이 난다</summary>

프로젝트 이름과 패키지 폴더 이름이 달라 hatchling이 패키지를 찾지 못한 것이다. `[tool.hatch.build.targets.wheel] packages = ["src/oss_tool"]`이 있는지, `src/oss_tool/__init__.py`가 실제로 있는지(빈 파일이라도 있어야 패키지다) 확인한다.
</details>

<details>
<summary>힌트 3 — `ConvertFrom-Json`이 깨진다</summary>

stdout에 JSON 외의 글자가 섞였다. 진행 메시지를 `print`로 쓰지 않았는지, `logging.basicConfig(stream=sys.stderr)`인지 확인한다. `uv run oss-tool sysinfo --json 2>$null`로 stderr를 버려도 JSON이 온전해야 한다. JSON 출력에 `ensure_ascii=True`를 주면 콘솔 인코딩 문제도 피한다.
</details>

### 검증

- 정상: `greet`·`sysinfo`가 동작하고 `--help`에 두 서브커맨드가 보인다. `outputs/`에 JSON이 쌓이지만 `git status`에는 나타나지 않는다.
- 경계 또는 실패: 엔트리포인트 오타를 재현했고 되돌렸다. `2>$null`로 stderr를 버려도 JSON이 온전하다.
- 설명: "`python sysinfo.py`와 `oss-tool sysinfo`의 차이는 무엇이 어디에 설치되었는가의 차이"임을 한 문장으로 적는다.

### 확장 문제

1. 최상위 옵션 `-v/--verbose`를 추가해 DEBUG 로그를 켜고, 파싱된 인자를 `log.debug`로 남긴다. 켜지 않았을 때 stderr에 아무것도 늘지 않는지 확인한다.
2. `--version` 옵션이 `__init__.py`의 `__version__`을 출력하게 한다.
3. `Set-Location C:\classwork` 뒤 `uv run --project C:\classwork\osa-practice oss-tool greet`를 실행하고, 저장소 밖에서도 동작하는 이유를 적는다.

## 3교시 실습 — 설정 로더와 비밀정보 분리

**이어받는 것:** 2교시의 `oss-tool`(`greet`·`sysinfo`)과 루트 `.gitignore`(아직 `.env`가 없다). 하루가 바뀌었으면 `uv sync` 뒤 `uv run oss-tool greet`로 확인하고 시작한다.

### 상황

4주차부터 `oss-tool`이 Ollama 서버를 호출한다. 강의실 PC와 집 PC의 서버 주소·모델이 다르고, 5주차에는 Hugging Face 토큰도 필요하다. 코드를 고치지 않고 PC마다 다른 값을 쓰게 만들고, 토큰이 저장소에 들어가지 않도록 막아라. 그리고 실수로 `.env`를 stage했을 때 어떻게 되돌리는지 한 번 재현하라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | `uv add python-dotenv`, 예상표(이기는 출처, 토큰 표시, staged `.env`) |
| 설정 로더 | 5–13분 | `config.py`(기본값 < `.env` < 환경변수 < 인자, 출처 기록), `config` 서브커맨드 |
| 계층 확인 | 13–19분 | `.env.example` commit → `.env` → 셸 변수 → `--model`로 출처 변화 관찰 |
| 실수 재현·복구 | 19–25분 | 가짜 토큰 `.env` → `git add .` → `restore --staged` → `.gitignore` → 이력 검사 |
| 검증·기록 | 25–30분 | 검사 결과 문장, commit·push, `config --json`으로 4주차 연결 확인 |

### 준비

```powershell
Set-Location C:\classwork\osa-practice
git status
uv add python-dotenv
git diff --stat
```

`pyproject.toml`과 `uv.lock`이 함께 바뀌어야 한다. 의존성을 추가하는 일은 곧 lock을 바꾸는 일이다.

### 문제 1 · config.py와 config 서브커맨드

1. `notes/week03.md` 3절의 예상표를 채운다. `.env`에 `OLLAMA_MODEL=qwen3:0.6b`, 셸에 `$env:OLLAMA_MODEL="qwen3:1.7b"`, 인자로 `--model qwen3:14b`를 동시에 주면 무엇이 이기는가. `HF_TOKEN` 값은 화면에 그대로 보여야 하는가. `.gitignore`에 `.env`가 없을 때 `git add .`를 하면 `.env`는 어디에 가는가.
2. `src/oss_tool/config.py`를 만든다. 예제 `$src\oss_tool\src\oss_tool\config.py`를 읽고 가져와도 되지만, 우선순위 4단계를 자기 말로 설명할 수 있어야 한다.
   - `DEFAULTS = {"OLLAMA_HOST": "http://localhost:11434", "OLLAMA_MODEL": "qwen3:8b"}`. 교재 검증용 기본값이며 실제 값은 환경 기준표가 정한다.
   - `load_settings(overrides, env_file=".env")`: 키마다 기본값 → `dotenv_values(env_file)` → `os.environ` → `overrides`(명령 인자) 순서로 덮어쓰고, 값과 함께 출처(`default`·`.env`·`env`·`arg`)를 기록한다. `load_dotenv()` 대신 `dotenv_values()`를 쓰는 이유는 `.env` 값과 셸 변수를 구분하기 위해서다.
   - 키 이름에 `TOKEN`·`KEY`·`SECRET`·`PASSWORD`가 들어가면 값을 가려서 표시한다(`(설정됨, 가려짐)`). 파일로 저장할 때도 가린 값만 저장한다.
3. `cli.py`에 `config` 서브커맨드를 추가한다. `--host`, `--model` 인자를 `overrides`로 넘기고, 키마다 `키 = 값 [출처]` 한 줄을 출력한다. `--json`이 있으면 JSON으로 출력한다.
4. 실행한다. `.env`가 아직 없으므로 모두 `[default]`여야 한다.

```powershell
uv run oss-tool config
```

완료 조건:

- [ ] `uv run oss-tool config`가 `OLLAMA_HOST`·`OLLAMA_MODEL`을 `[default]`로 출력한다.
- [ ] `git diff --stat`에 `pyproject.toml`과 `uv.lock`이 함께 보인다.
- [ ] `HF_TOKEN`처럼 비밀로 보이는 키의 값이 화면과 `outputs/` JSON에 그대로 나오지 않는다.

### 문제 2 · .env.example, 계층 확인, 실수 복구

1. `.env.example`을 VS Code로 만들고 commit한다. 키 이름·기본값·설명만 있고 실제 값은 없다.

```text
# oss-tool 설정. Copy-Item .env.example .env 로 복사한 뒤 값만 바꾼다. .env 는 커밋하지 않는다.
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3:8b
HF_TOKEN=
```

```powershell
git add .env.example
git commit -m "Add .env.example"
```

2. `.env`를 만들어 값을 바꾸고 출처가 바뀌는지 본다. `.env`의 `OLLAMA_MODEL`을 `qwen3:0.6b`로, `HF_TOKEN`을 `hf_fake_token_for_class_only`로 바꾼다.

```powershell
Copy-Item .env.example .env
code .env
uv run oss-tool config
```

3. 셸 환경변수와 명령 인자를 차례로 얹는다. 세 번의 출력에서 `OLLAMA_MODEL`의 값과 출처를 예상표 옆에 적는다. 끝나면 셸 변수를 지운다. `config`는 값과 출처만 보여 줄 뿐 모델을 내려받거나 호출하지 않으므로, 내 PC에 없는 태그를 써도 된다.

```powershell
$env:OLLAMA_MODEL = "qwen3:1.7b"
uv run oss-tool config
uv run oss-tool config --model qwen3:14b
Remove-Item Env:OLLAMA_MODEL
```

4. 실수를 재현한다. `.gitignore`에 아직 `.env`가 없으므로 `git add .`는 `.env`를 stage한다. `git status`에서 `new file: .env`를 확인한 뒤 stage에서 내리고, `.gitignore`에 `.env` 줄을 VS Code로 추가하고(`Add-Content`는 마지막 줄에 개행이 없으면 앞 줄에 붙는다), `git status`에서 `.env`가 사라졌는지 본다.

```powershell
git add .
git status
git restore --staged .env
git status
code .gitignore
git status
git check-ignore -v .env
```

5. 이력을 검사한다. 두 명령이 모두 아무것도 출력하지 않으면 `.env`도 가짜 토큰도 이력에 없다. 결과를 문장으로 `notes/week03.md`에 적는다.

```powershell
git log --all --oneline -- .env
git log --all --oneline -S "hf_fake_token"
```

6. commit·push한다. stage 목록에 `.env`가 없는지 `git status`로 읽은 뒤 commit한다. 마지막으로 `uv run oss-tool config --json`이 4주차 클라이언트가 읽을 JSON을 내는지 확인한다.

```powershell
git add .gitignore pyproject.toml uv.lock src notes
git status
git commit -m "Add config loader and ignore .env"
git push
uv run oss-tool config --json
```

완료 조건:

- [ ] 같은 키를 `.env`, 셸 환경변수, `--model` 인자로 주었을 때 출처가 `.env` → `env` → `arg`로 바뀌는 것을 보았다.
- [ ] `.env`가 staged → `restore --staged` → `.gitignore` 추가 순으로 `git status`에서 사라졌고, `git check-ignore -v .env`가 `.gitignore`의 줄을 가리킨다.
- [ ] 이력 검사 두 명령이 비어 있다는 문장을 `notes/week03.md`에 적었고, `.env.example`만 commit·push되었다.

### 단계별 힌트

<details>
<summary>힌트 1 — `.env` 값을 바꿨는데 계속 `[default]`로 나온다</summary>

`dotenv_values(".env")`는 현재 작업 폴더의 `.env`를 읽는다. `Get-Location`이 저장소 루트인지, `Get-Content .env`에 `KEY=value` 형식으로 공백·따옴표 없이 적혔는지 확인한다. 값이 비어 있으면(`HF_TOKEN=`) 기본값으로 남는 것이 정상이다.
</details>

<details>
<summary>힌트 2 — 셸 변수를 지웠는데 계속 `[env]`다</summary>

`$env:OLLAMA_MODEL = ""`는 빈 값을 넣는 것이고 지우는 것은 `Remove-Item Env:OLLAMA_MODEL`이다. 새 터미널을 열면 사라진다. `.env` 파일과 셸 변수는 다른 통로이며 로더는 셸 변수를 더 우선한다.
</details>

<details>
<summary>힌트 3 — `.gitignore`에 `.env`를 넣었는데 `git status`에 여전히 보이거나, 반대로 `.env.example`까지 사라졌다</summary>

여전히 보이면 이미 stage되었거나 commit된 것이다. staged면 `git restore --staged .env`, 이미 commit되었으면 `git rm --cached .env` 뒤 commit한다. push까지 되었다면 이력에 남으므로 그 토큰은 폐기하고 새로 발급한다(이력 재작성은 강의자와 상의). `.env.example`까지 사라졌다면 `.env*` 같은 패턴을 쓴 것이다. 정확히 `.env` 한 줄만 쓴다.
</details>

### 검증

- 정상: `config`의 출처가 `default` → `.env` → `env` → `arg`로 바뀌고, `.env.example`은 tracked, `.env`는 ignored다.
- 경계 또는 실패: `git add .`로 `.env`가 staged된 상태를 실제로 보고 되돌렸다. 이력 검사 두 명령이 비어 있다.
- 설명: "`.gitignore`가 막지 못하는 경우"를 한 문장으로 적는다.

### 확장 문제

1. 로컬 전용 브랜치 `exp/leak`에서 `git add -f .env`로 `.env`를 일부러 commit한 뒤 `git rm --cached .env`로 지우고 다시 commit한다. `git log -p -- .env`에 가짜 토큰이 여전히 보이는 것을 확인하고 `git switch main`, `git branch -D exp/leak`으로 정리한다. 이 브랜치는 push하지 않는다.
2. `OLLAMA_TIMEOUT`(초, 기본 `180`) 키를 로더에 추가한다. 숫자가 아니면 기본값으로 돌아가고 경고 로그를 남긴다. 4주차 클라이언트가 이 값을 쓴다.
3. `config --ping` 옵션을 추가해 `OLLAMA_HOST`의 `/api/tags`에 GET 요청을 보낸다. Ollama가 꺼져 있으면 스택 트레이스 대신 사람이 읽을 연결 실패 문장과 종료 코드 2를 내야 한다. 켜져 있으면 모델 이름 목록을 출력한다.

## 제출 체크

- 개인 저장소 `main`: `pyproject.toml`, `uv.lock`, `.python-version`, `.gitignore`(`.venv/`·`outputs/`·`.env`), `src/oss_tool/`(`__init__.py`·`cli.py`·`sysinfo.py`·`config.py`), `.env.example`, README의 실행 절차 3줄
- `notes/week03.md`: 예상표 3개(예상과 실제), 실패 경로 오류 줄 3개(`uv.lock` 없음, 엔트리포인트 오타, staged `.env`), 출처 관찰표, 이력 검사 결과 문장, 설명 문장 3개
- `notes/week03_reproduce.md`: `reproduce_check.ps1` 로그(네 단계 OK)
- `uv run oss-tool greet --name student01`, `uv run oss-tool sysinfo --json`, `uv run oss-tool config` 출력
- 선택: 확장 문제 결과
