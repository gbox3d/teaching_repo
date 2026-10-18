# 8주차 실습 — 혼자서 재현하고 설명하기

## 공통 규칙

준비 절의 폴더 복사·설정 생성은 최초 1회만 한다. 대상 폴더에서 이미 실습 중이면 복사를 생략하고 이어서 실행한다. 개인 코드·답안·설정·산출물을 보존한다.

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 모의 실기는 타이머를 켜고 30분을 지킨다. 못 끝낸 항목은 "증상·관찰·시도"를 적고 넘어간다.
- 모델 다운로드는 하지 않는다. 사전 캐시된 `OLLAMA_MODEL`만 쓰고, 실제 토큰·비밀번호는 어떤 파일에도 적지 않는다.
- 1·2교시 모의 실기는 공개 동형 문제다. 3교시 개인 실기는 비공개 패킷을 쓰며 허용 자료·AI 도구 범위·제출 경로는 학교 운영 문서를 따른다.

## 1교시 실습 — 모의 실기 A 프로젝트 복구와 uv·프로젝트 개념 문항

> 이 교시의 파일·시간 대응: [examples/period1](examples/period1/README.md).

### 상황

동료가 "급하게 커밋했는데 `uv sync`가 안 된다"며 프로젝트를 넘겼다. 열어 보니 `pyproject.toml`이 깨져 있고 `.gitignore`가 없으며 `.env`까지 커밋되어 있다. 복구해서 `report.py`가 돌아가게 만든다. 그다음 표준 양식의 uv 프로젝트를 새로 만들어 `uv run hello`를 실행하고 첫 commit까지 남긴다(A-2). 구조·설정 개념 문항(A-3·A-4)은 한두 문장으로 답한다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–3분 | `tasks_A.md`를 읽고 완료 조건에 체크 항목 표시, 오류 순서 예상 |
| 프로젝트 복구 | 3–13분 | `uv sync` 오류를 하나씩 고치고 `.gitignore`·`.env`·`.env.example` 정리 |
| 표준 양식 프로젝트 | 13–22분 | `uv init --package` → `[project.scripts]` → `uv run hello` → `git init`·`add`·`commit`(A-2) |
| 개념 문항 | 22–27분 | 프로젝트 구조(A-3), 설정 파일과 비밀값(A-4) |
| 검증·기록 | 27–30분 | 실행 결과·`git ls-files` 확인, `answers_A.md` 마무리 |

### 준비

`examples/` 원본은 수정하지 않는다. 아래 스크립트가 `broken_project/`를 개인 실습 폴더에 복사하고, `.env`가 커밋된 Git 이력을 만들어 준다.

```powershell
Set-Location <교재 폴더>\open_source_ai\weeks\week08_midterm\examples\period1
.\make_broken_repo.ps1 -Destination $HOME\osa-practice\week08-mock-a
Set-Location $HOME\osa-practice\week08-mock-a
git log --oneline
git ls-files
```

스크립트 실행이 막히면 `powershell -ExecutionPolicy Bypass -File .\make_broken_repo.ps1 -Destination $HOME\osa-practice\week08-mock-a`로 실행한다. 문제는 `examples/period1/tasks_A.md`를 그대로 읽고, 답안은 실습 폴더의 `answers_A.md`에 쓴다.

### 문제 1 · 깨진 프로젝트 복구

`tasks_A.md`의 A-1이다.

1. 시작 전에 예상을 적는다: `uv sync`를 처음 실행하면 어떤 오류가 먼저 보일까? `git ls-files`에 무엇이 있으면 안 되는가?
2. `uv sync`를 실행하고 **첫 오류 메시지의 첫 줄**을 읽어 원인 한 곳만 고친다. 다시 실행한다. 오류가 사라질 때까지 반복하되, 고칠 때마다 무엇을 왜 바꿨는지 `answers_A.md`에 한 줄씩 적는다.
3. `uv run python report.py`가 실행되는지 확인한다. `uv sync`가 성공한 것처럼 보여도 `ModuleNotFoundError`가 나면 아직 설정이 덜 고쳐진 것이다.
4. `.gitignore`를 만들고(`.venv/`, `.env`, `outputs/`, `__pycache__/`), `.env`를 추적에서 뺀 뒤(`git rm --cached .env`), 값을 비운 `.env.example`을 만든다.
5. 한 commit으로 정리하고 `git ls-files`·`git status`로 확인한다. 복구 뒤 `uv sync`가 만든 `uv.lock`은 3주차 원칙대로 같은 commit에 넣는다(`.gitignore`로 감추면 재현성 위반이다).

완료 조건:

- [ ] `uv run python report.py`가 `outputs/report.json`을 만든다(Ollama가 꺼져 있어도 파일은 생기고 `ollama_reachable`이 `false`로 기록된다).
- [ ] `git ls-files`에 `.env`가 없고 `.gitignore`·`.env.example`이 있다.
- [ ] `answers_A.md`에 고친 항목 3개 이상과 각 항목의 증상이 적혀 있다.

### 문제 2 · 표준 양식 프로젝트와 개념 문항

`tasks_A.md`의 A-2(실기), A-3·A-4(개념)다. A-2는 4주차 2교시 문제 0과 같은 순서다.

1. `uv init --package --python 3.12 --vcs none week8-hello` → `__init__.py`의 `main()` 고치기 → `[project.scripts]`에 `hello` 추가 → `uv run hello`. 출력이 나오면 `pyproject.toml`·`__init__.py`·출력을 답안에 붙인다.
2. `.gitignore`에 `__pycache__/`를 적고 `git init` → `git status` → `git add .` → `git status` → `git commit` → `git log --oneline`. 두 `git status`와 `git log` 출력을 붙이고, `.venv`가 보이지 않는 이유를 쓴다.
3. A-3·A-4는 한두 문장으로 답한다. 확신이 없는 물음은 "확인할 명령·문서"를 적는다.

완료 조건:

- [ ] `uv run hello`가 지정한 문장을 출력하고, `pyproject.toml`에 `hello = "week8_hello:main"` 줄이 있다.
- [ ] `git log --oneline`에 commit 1개, `git status` clean, `.venv/`는 보이지 않는다.
- [ ] A-2-(d)에 `git add`(staging area)와 `git commit`의 역할이 한 문장씩 있고, A-3·A-4의 모든 물음에 답이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — `uv sync`가 첫 줄에 TOML parse error를 낸다</summary>

메시지가 가리키는 줄 번호와 열을 본다. 배열 안 항목 사이에 빠진 것이 무엇인지 확인한다. 한 곳만 고치고 다시 실행한다.
</details>

<details>
<summary>힌트 2 — `uv sync`는 되는데 `import httpx`가 실패한다</summary>

`uv sync` 출력에 설치된 패키지 수가 없거나 "No `requires-python` value found in the workspace" 경고가 있으면 uv가 `[project]` 테이블을 찾지 못한 것이다. 테이블 이름의 철자를 한 글자씩 본다.
</details>

<details>
<summary>힌트 3 — `.env`를 지웠는데 `git log -p`에 여전히 보인다</summary>

삭제 commit은 이력을 지우지 않는다. 모의 실기에서는 "이력에 남아 있으므로 토큰을 회전해야 한다"고 적으면 된다. 이력 자체를 다시 쓰는 방법은 GitHub Docs의 민감 데이터 제거 문서를 참고 자료로만 적는다.
</details>

<details>
<summary>힌트 4 — `uv run hello`가 `Failed to spawn: hello`라고 한다</summary>

`pyproject.toml`의 `[project.scripts]`에 `hello = "week8_hello:main"` 줄이 있는지 본다. 형식은 `명령이름 = "패키지:함수"`다. 줄을 넣은 뒤 `uv sync`를 한 번 실행하면 `.venv\Scripts\hello.exe`가 생긴다. `git commit`이 이름을 물으면 `git config user.name student01`·`git config user.email student01@example.com`(수업용 값)을 설정한다.
</details>

### 검증

- 정상: `uv sync` → `uv run python report.py` → `outputs/report.json`에 `host`·`model`·`ollama_reachable`·`model_available`·`hf_token_present`가 있다.
- 경계 또는 실패: Ollama를 끄고 실행하면 사람이 읽을 메시지가 나오고 종료 코드가 `2`다(`$LASTEXITCODE`로 확인).
- 설명: "테이블 이름 오타는 왜 `uv sync`에서 오류로 잡히지 않았는가"를 한 문장으로 쓴다.

### 확장 문제

1. `git log -p -- .env`로 첫 commit에 남은 값을 확인하고, 이 저장소를 공개했을 때 해야 할 일을 두 줄로 쓴다.
2. `report.py`에 `--host` 인자를 추가해 환경변수보다 인자가 우선하도록 만든다(설정 계층: 기본값 < 환경변수 < 인자).

## 2교시 실습 — 모의 실기 B Git 상황 판단과 Ollama 툴 콜링

> 이 교시의 파일·시간 대응: [examples/period2](examples/period2/README.md).

### 상황

실기평가의 두 번째 묶음은 Git과 Ollama다. `git status` 출력을 영역으로 읽는 Git 개념 문항, 모의 A에서 만든 프로젝트를 GitHub에 올리는 실기, Ollama 명령과 메시지 역할·temperature·실패 메시지를 설명하는 개념 문항, 그리고 4주차 툴 콜링 프로젝트에 함수를 하나 추가해 모델이 실제로 부르게 만드는 실기가 한 패킷에 들어 있다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–3분 | `tasks_B.md`를 읽고 완료 조건에 체크 항목 표시 |
| Git 개념 | 3–9분 | B-1 기록 흐름·`git status` 읽기 |
| GitHub 실기 | 9–17분 | B-2 빈 저장소 만들기 → `remote add` → `push -u` → 수정 commit·push |
| Ollama 개념 | 17–22분 | B-3 명령·메시지 역할·temperature·실패 구분 |
| 툴 콜링 실기 | 22–30분 | B-4 함수 추가 → `uv run ex07` → `[함수 실행]` 줄 기록, `answers_B.md` 마무리 |

### 준비

B-1·B-3은 모델 없이 읽고 답한다. B-2는 GitHub 로그인이 필요하므로 2주차에 쓴 계정으로 먼저 로그인해 둔다. B-4는 4주차 3교시에 만든 `period3` 프로젝트에서 한다.

```powershell
Set-Location C:\classwork\week04\period3
ollama show qwen3.5:2b
uv sync
```

`period3`가 없으면 교재 `week04_ollama_local_llm/examples/period3`를 `C:\classwork\week04\period3`로 복사한 뒤 위 명령을 실행한다. `Capabilities`에 `tools`가 보여야 한다. 문제는 `examples/period2/tasks_B.md`를 그대로 읽고, 답안은 실습 폴더의 `answers_B.md`에 쓴다.

### 문제 1 · Git 기록 흐름과 GitHub에 올리기

`tasks_B.md`의 B-1(개념)과 B-2(실기)다.

1. B-1-2의 `git status` 출력을 보고 세 파일이 각각 어느 영역에 있는지 먼저 판정한다. 그다음에 명령을 쓴다.
2. B-1-3은 실행할 명령을 순서대로 쓰고, 각 명령이 바꾸는 영역(working tree / staging area / repository / origin)을 괄호로 붙인다.
3. B-2는 2주차 1교시 문제 1과 같다. GitHub에서 빈 저장소를 만들고 `git remote add origin` → `git push -u origin main` → README 한 줄 수정 → `add`·`commit`·`push`. 브라우저에서 commit 수가 2인지 확인한다.

완료 조건:

- [ ] B-1-2 세 파일의 영역 판정과 B-1-3 명령 순서의 영역 표기가 있다.
- [ ] B-1-4에 `.gitignore`가 막지 못한 이유와 `git restore --staged .env`가 있다.
- [ ] GitHub 저장소에 commit 2개가 보이고, `git remote -v`·`git log --oneline` 출력이 답안에 있다.

### 문제 2 · Ollama 사용법과 툴 콜링 실기

`tasks_B.md`의 B-3과 B-4다.

1. B-3은 4주차 보고서에 적었던 것을 다시 떠올려 쓴다. B-3-4의 표는 세 메시지의 원인이 서로 다르다는 점이 핵심이다.
2. B-4-1에서 함수를 추가할 때 docstring의 `Args:`를 빼먹지 않는다. 라이브러리가 이름·타입·docstring을 읽어 모델에게 설명서로 보낸다.
3. `uv run ex07`로 지정 질문을 입력하고 `[함수 실행]` 줄과 `AI>` 답을 그대로 답안에 붙인다. 함수를 부르지 않으면 질문이나 docstring을 바꿔 다시 시도하고 바꾼 내용을 적는다.
4. 함수 결과와 모델의 최종 답을 비교한다. 다르면 함수 결과가 정답이다.

완료 조건:

- [ ] B-3-4 표의 세 메시지에 서로 다른 원인과 확인 방법이 있다.
- [ ] `answers_B.md`에 새 함수를 부른 `[함수 실행]` 줄이 있다(또는 재시도 기록과 실패 원인).
- [ ] B-4-4에 세 단계와 "함수를 실행하는 것은 내 프로그램"이라는 설명이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — `git status`의 세 묶음이 헷갈린다</summary>

`Changes to be committed`는 staging area에 올라간 것(다음 commit 후보), `Changes not staged for commit`은 working tree에서만 바뀐 것, `Untracked files`는 Git이 아직 추적하지 않는 새 파일이다. 2주차 슬라이드의 세 영역 그림에 그대로 대응시킨다.
</details>

<details>
<summary>힌트 2 — 모델이 새 함수를 부르지 않는다</summary>

`TOOLS` 딕셔너리에 새 함수를 넣었는지 먼저 확인한다. 그다음 질문을 함수 설명(docstring)과 더 가깝게 바꿔 본다. 숫자를 받는 함수가 글자를 받는 함수보다 잘 맞는다. 작은 모델은 함수를 빠뜨리기도 하므로 한 번 더 시도한 기록도 답안이 된다.
</details>

<details>
<summary>힌트 3 — GitHub가 push를 거부한다(rejected)</summary>

원격 저장소를 만들 때 README나 `.gitignore`를 추가했으면 원격에 이미 commit이 있어 거부된다. 빈 저장소로 다시 만들거나 다른 이름으로 만든다. `remote: Repository not found`면 URL의 계정 이름과 저장소 이름을 다시 본다.
</details>

<details>
<summary>힌트 4 — 함수 결과와 `AI>` 답이 다르다</summary>

함수 결과가 정답이다. 모델은 함수 결과를 받아 사람에게 할 말을 만들 뿐이고, 그 과정에서 숫자를 바꿔 말하기도 한다(4주차에 02:07을 "오후 2시"라고 말한 사례). 답안에는 두 값을 모두 적고 어느 쪽을 믿는지 쓴다.
</details>

### 검증

- 정상: `[함수 실행] discount_price({'price': 25000, 'percent': 20}) -> 20000.0` 같은 줄이 보이고 `AI>` 답에 20000원이 들어 있다.
- 경계 또는 실패: `tools=`를 빼고 같은 계산을 물으면 모델이 직접 계산한다. 맞을 수도 틀릴 수도 있다는 점을 적는다. Ollama 앱을 끄고 실행하면 `Failed to connect to Ollama`가 나온다(공용 서버는 끄지 않고 메시지만 적는다).
- 설명: "`.gitignore`에 넣었는데 `git status`에 계속 보이는 이유"와 "첫 push에 `-u`를 붙이는 이유"를 각각 한 문장으로 쓴다.

### 확장 문제

1. `rooms = {"오픈소스 AI 응용": "공학관 301호"}`에서 과목 이름으로 강의실을 찾는 `get_class_room(course: str)`을 추가해 본다. 모델이 다른 글자(`"오픈소스 AI 응용 수업"`)를 넘기면 어디서 틀리는지 관찰하고, 함수 쪽에서 `in`으로 받아 주는 방법을 적는다.
2. 2주차 충돌 해결 저장소에서 `git log --oneline --graph --all`로 두 갈래와 합류점을 다시 확인하고, 각 commit이 사용자에게 준 변화를 한 줄씩 쓴다.

## 3교시 실습 — 개인 실기평가와 대체 운영

> 이 교시의 파일·시간 대응: [examples/period3](examples/period3/README.md).

### 상황

실기평가 당일이다. 비공개 패킷(요구사항·starter·fixture·제출 파일명)을 받으면 1·2교시에 연습한 순서 — 환경 점검 → 완료 조건 표시 → 해결 → 검증 → 제출 — 를 그대로 밟는다. 분반 시간표상 실기가 다른 슬롯에 있으면 같은 30분을 2차 종합과제 최종 점검(문제 2)에 쓴다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 환경 점검 | 0–5분 | `check_env.py`, `git status`, 저장·제출 경로 확인 |
| 문항 해결 | 5–22분 | 요구사항 → 완료 조건 → 해결. 막히면 증상·관찰·시도 기록 |
| 검증 | 22–27분 | 정상·실패 경로 재현, `outputs/` 확인, 답안 다시 읽기 |
| 제출·기록 | 27–30분 | commit, commit id 기록, 제출 파일 다시 열기 |

실제 평가 시간은 기관 시간표에 따라 30분을 넘겨 확장될 수 있다. 확장되면 "문항 해결"과 "검증" 구간을 같은 비율로 늘린다.

### 준비

```powershell
if (-not (Test-Path $HOME\osa-practice\week08-period3)) { Copy-Item -Recurse <교재 폴더>\open_source_ai\weeks\week08_midterm\examples\period3 $HOME\osa-practice\week08-period3 }
Set-Location $HOME\osa-practice\week08-period3
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync
uv run python check_env.py
Get-Content outputs\env-check.json
Set-Location <지정 저장 경로>
git status
ollama list
```

- 비공개 패킷을 지정 폴더에 풀고 파일 목록이 패킷 문서와 같은지 확인한다.
- `check_env.py`는 `period3`에 실제 사본이 있다. 패킷에 별도 점검기가 있으면 우선하고, 없으면 `week08-period3\outputs\env-check.json`이 시작 전 증거다.
- 허용 자료·AI 도구 범위·제출 경로는 시험 공지(학교 운영 문서)를 따른다.

### 문제 1 · 개인 실기 응시 절차

1. 요구사항 문서를 읽고 완료 조건마다 체크 항목을 만든다. 코드는 아직 만지지 않는다.
2. 검증 명령을 먼저 정한다(`uv run ...`, `git ls-files`, 파일 열기).
3. 가장 짧은 한 경로를 끝까지 연결한 뒤 다음 요구사항으로 간다.
4. 22분에 작업을 멈추고 정상·실패 경로를 각각 한 번 재현한다.
5. commit하고 `git log -1 --oneline`의 id를 제출 설명에 적는다. 제출 파일을 다시 열어 같은 내용인지 본다.

완료 조건:

- [ ] `outputs/env-check.json`이 시작 시각과 함께 있고, 시작 시점의 `git status`가 clean이었다.
- [ ] 제출 파일·commit id·짧은 설명(무엇을·왜)이 제출 경로에 있다.
- [ ] 못 끝낸 항목은 증상·관찰·시도 세 줄로 적었다.

### 문제 2 · 대체 운영 — 2차 종합과제 최종 점검

실기가 다른 슬롯에 있는 분반은 이 문제를 수행한다. 시간 배분은 위 표를 그대로 쓰되 "문항 해결"을 "재현 점검"으로 읽는다.

1. `examples/period3/assignment_check.ps1 -RepoPath <내 과제 저장소>`를 실행해 파일 존재·`.gitignore`·추적 파일·비밀 흔적을 훑는다.
2. 새 폴더에 `git clone`하고 README의 명령을 **그대로** 실행한다(`uv sync --frozen` → 인덱스 생성(`chunk.py`·`embed.py`) → `eval.py`). `outputs/`는 커밋하지 않으므로 인덱스는 clone에 없다.
3. README에 없는 조작이 필요했던 지점을 README에 추가한다.
4. [assignment_brief.md](assignment_brief.md)의 제출 전 검사 목록을 순서대로 체크한다.
5. 보완 commit을 만들고 `git log -1 --oneline`을 기록한다.

완료 조건:

- [ ] `assignment_check.ps1` 결과에 FAIL이 없다(또는 FAIL 항목의 조치가 commit되었다).
- [ ] 깨끗한 폴더에서 README만으로 `eval.py`까지 실행되었다.
- [ ] 제출 전 검사 목록의 항목이 모두 체크되었다.

### 단계별 힌트

<details>
<summary>힌트 1 — `check_env.py`가 연결 실패를 보인다</summary>

`ollama list`가 되는지 본다. 되면 `.env`의 `OLLAMA_HOST`가 다른 주소를 가리키는 것이다. 안 되면 Ollama를 한 번 재시작하고, 그래도 안 되면 시각을 적어 감독에게 알린다.
</details>

<details>
<summary>힌트 2 — 시간이 모자란다</summary>

22분이 되면 새 기능을 시작하지 않는다. 지금까지 된 경로 하나를 정상·실패로 재현하고 commit한다. 못 끝낸 항목은 "증상·관찰·시도"로 적는다. 부분 결과도 실행 가능하면 점수가 된다.
</details>

<details>
<summary>힌트 3 — 깨끗한 폴더에서 `uv sync --frozen`이 실패한다</summary>

`uv.lock`이 커밋되지 않았거나 `pyproject.toml`과 어긋난 것이다. 원래 폴더에서 `uv lock`을 다시 만들고 commit한 뒤 clone부터 다시 한다.
</details>

### 검증

- 정상: 제출 경로의 파일을 다시 열었을 때 마지막 commit의 내용과 같다.
- 경계 또는 실패: 장애가 있었다면 `outputs/env-check.json`의 시각과 감독에게 알린 시각이 기록되어 있다.
- 설명: "commit id를 제출물에 함께 적는 이유"를 한 문장으로 쓴다.

### 확장 문제

1. 다른 팀원의 2차 과제 저장소를 README만 보고 재현해 보고, 막힌 지점을 Issue로 남긴다.
2. `assignment_check.ps1`에 "README에 `uv sync --frozen`이 적혀 있는가" 검사를 추가한다.

## 제출 체크

- `answers_A.md`: 모의 A 복구 기록(고친 항목·증상), 표준 양식 프로젝트 실기 A-2(`pyproject.toml`·`uv run hello` 출력·`git status`·`git log`), 개념 문항 A-3·A-4
- 모의 A 저장소: `.gitignore`·`.env.example` commit, `git ls-files`에 `.env` 없음
- `answers_B.md`: Git 개념 B-1(영역 표기 포함), GitHub 올리기 기록 B-2(저장소 URL·`git log`), Ollama 개념 B-3, 툴 콜링 실행 기록 B-4(`[함수 실행]` 줄 포함)
- `week8-hello` 저장소: GitHub에 commit 2개
- 4주차 `period3/src/ex07/tools.py`: 추가한 함수와 `TOOLS` 등록
- 개인 실기: 제출 파일 + commit id + 짧은 설명(비공개 제출 경로)
- 2차 종합과제: 저장소 URL + 최종 commit id + `assignment_check.ps1` 결과([assignment_brief.md](assignment_brief.md) 기준)
