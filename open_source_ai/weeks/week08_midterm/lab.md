# 8주차 실습 — 혼자서 재현하고 설명하기

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 모의 실기는 타이머를 켜고 30분을 지킨다. 못 끝낸 항목은 "증상·관찰·시도"를 적고 넘어간다.
- 모델 다운로드는 하지 않는다. 사전 캐시된 `OLLAMA_MODEL`만 쓰고, 실제 토큰·비밀번호는 어떤 파일에도 적지 않는다.
- 1·2교시 모의 실기는 공개 동형 문제다. 3교시 개인 실기는 비공개 패킷을 쓰며 허용 자료·AI 도구 범위·제출 경로는 학교 운영 문서를 따른다.

## 1교시 실습 — 모의 실기 A 프로젝트 복구와 판별 문항

### 상황

동료가 "급하게 커밋했는데 `uv sync`가 안 된다"며 프로젝트를 넘겼다. 열어 보니 `pyproject.toml`이 깨져 있고 `.gitignore`가 없으며 `.env`까지 커밋되어 있다. 복구해서 `report.py`가 돌아가게 만들고, 같은 패킷의 라이선스·Git 판별 문항에 판단과 근거를 적는다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | `tasks_A.md`를 읽고 완료 조건에 체크 항목 표시, 오류 순서 예상 |
| 프로젝트 복구 | 5–17분 | `uv sync` 오류를 하나씩 고치고 `.gitignore`·`.env`·`.env.example` 정리 |
| 판별 문항 | 17–24분 | 라이선스 3문항, Git 상황 1문항 답안 작성 |
| 검증·기록 | 24–30분 | 실행 결과·`git ls-files` 확인, `answers_A.md` 마무리 |

### 준비

`examples/` 원본은 수정하지 않는다. 아래 스크립트가 `broken_project/`를 개인 실습 폴더에 복사하고, `.env`가 커밋된 Git 이력을 만들어 준다.

```powershell
Set-Location <교재 폴더>\open_source_ai\weeks\week08_midterm\examples\mock_exam
.\make_broken_repo.ps1 -Destination $HOME\osa-practice\week08-mock-a
Set-Location $HOME\osa-practice\week08-mock-a
git log --oneline
git ls-files
```

스크립트 실행이 막히면 `powershell -ExecutionPolicy Bypass -File .\make_broken_repo.ps1 -Destination $HOME\osa-practice\week08-mock-a`로 실행한다. 문제는 `examples/mock_exam/tasks_A.md`를 그대로 읽고, 답안은 실습 폴더의 `answers_A.md`에 쓴다.

### 문제 1 · 깨진 프로젝트 복구

`tasks_A.md`의 A-1이다.

1. 시작 전에 예상을 적는다: `uv sync`를 처음 실행하면 어떤 오류가 먼저 보일까? `git ls-files`에 무엇이 있으면 안 되는가?
2. `uv sync`를 실행하고 **첫 오류 메시지의 첫 줄**을 읽어 원인 한 곳만 고친다. 다시 실행한다. 오류가 사라질 때까지 반복하되, 고칠 때마다 무엇을 왜 바꿨는지 `answers_A.md`에 한 줄씩 적는다.
3. `uv run python report.py`가 실행되는지 확인한다. `uv sync`가 성공한 것처럼 보여도 `ModuleNotFoundError`가 나면 아직 설정이 덜 고쳐진 것이다.
4. `.gitignore`를 만들고(`.venv/`, `.env`, `outputs/`, `__pycache__/`), `.env`를 추적에서 뺀 뒤(`git rm --cached .env`), 값을 비운 `.env.example`을 만든다.
5. 한 commit으로 정리하고 `git ls-files`·`git status`로 확인한다.

완료 조건:

- [ ] `uv run python report.py`가 `outputs/report.json`을 만든다(Ollama가 꺼져 있어도 파일은 생기고 `ollama_reachable`이 `false`로 기록된다).
- [ ] `git ls-files`에 `.env`가 없고 `.gitignore`·`.env.example`이 있다.
- [ ] `answers_A.md`에 고친 항목 3개 이상과 각 항목의 증상이 적혀 있다.

### 문제 2 · 라이선스·Git 판별 문항

`tasks_A.md`의 A-2(라이선스 3문항)와 A-3(Git 상황 1문항)이다.

1. 문항마다 **판단 → 근거 → 출처(있으면)** 세 줄 이내로 답한다.
2. A-3는 실행할 명령을 순서대로 쓰고, 각 명령이 바꾸는 영역(working tree / stage / commit / remote)을 괄호로 붙인다.
3. 확신이 없는 문항은 "확인할 문서"를 적는다. 빈칸보다 낫다.

완료 조건:

- [ ] `answers_A.md`에 A-2 세 문항 각각 판단과 근거가 있다.
- [ ] A-3 명령 순서에 `.env`가 이력에 남는 문제에 대한 판단이 포함된다.

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

### 검증

- 정상: `uv sync` → `uv run python report.py` → `outputs/report.json`에 `host`·`model`·`ollama_reachable`·`model_available`·`hf_token_present`가 있다.
- 경계 또는 실패: Ollama를 끄고 실행하면 사람이 읽을 메시지가 나오고 종료 코드가 `2`다(`$LASTEXITCODE`로 확인).
- 설명: "테이블 이름 오타는 왜 `uv sync`에서 오류로 잡히지 않았는가"를 한 문장으로 쓴다.

### 확장 문제

1. `git log -p -- .env`로 첫 commit에 남은 값을 확인하고, 이 저장소를 공개했을 때 해야 할 일을 두 줄로 쓴다.
2. `report.py`에 `--host` 인자를 추가해 환경변수보다 인자가 우선하도록 만든다(설정 계층: 기본값 < 환경변수 < 인자).

## 2교시 실습 — 모의 실기 B 클라이언트 기능 추가와 결과 해석

### 상황

팀의 최소 Ollama 클라이언트에 사용자가 "역할을 지정하는 system 프롬프트를 넣고 싶다"와 "답이 느린지 숫자로 알고 싶다"는 요청을 보냈다. 시작 코드의 `TODO(B-1)`을 채워 두 기능을 추가하고, 같은 패킷에 들어 있는 pipeline 실행 결과 샘플을 해석한다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | `tasks_B.md` 읽기, 시작 코드 그대로 1회 실행, 예상 적기 |
| 기능 추가 | 5–18분 | `--system` 인자, 응답 메타·`tokens_per_sec` 기록 |
| 결과 해석 | 18–24분 | `fixtures/pipeline_output.json` 3문항 답안 |
| 검증·기록 | 24–30분 | 실패 경로 2가지 재현, `answers_B.md` 마무리 |

### 준비

```powershell
Copy-Item -Recurse <교재 폴더>\open_source_ai\weeks\week08_midterm\examples\mock_exam\client_starter $HOME\osa-practice\week08-mock-b
Set-Location $HOME\osa-practice\week08-mock-b
Copy-Item .env.example .env
uv sync
uv run python check_env.py
uv run python chat.py --prompt "uv sync 가 하는 일을 한 문장으로 설명하라."
```

`check_env.py`가 `[실패]`를 보이면 `ollama serve`와 `ollama list`를 먼저 확인한다. GPU가 없는 PC는 `.env`의 `OLLAMA_MODEL`을 `qwen3:0.6b`로 바꾼다. 해석 문항의 샘플은 `examples/mock_exam/fixtures/pipeline_output.json`을 그대로 읽는다.

### 문제 1 · 클라이언트 기능 추가

`tasks_B.md`의 B-1이다.

1. 예상을 적는다: `--system "모든 답을 한 문장으로만 한다."`를 주면 답 길이와 `eval_count`는 어떻게 달라질까?
2. `chat.py`의 `build_messages`에서 system 메시지를 맨 앞에 넣고, `build_parser`에 `--system` 인자를 추가한다.
3. `summarize`에 `system`, `eval_count`, `eval_duration`, `total_duration`, `tokens_per_sec`를 추가한다. 계산식은 `tasks_B.md`에 있다.
4. 같은 `--prompt`로 `--system` 유무 2회 실행하고 `outputs/chat-*.json` 두 개를 나란히 비교한다.
5. `--model nonexistent-model`로 실행해 메시지와 종료 코드를 본다.

완료 조건:

- [ ] `--system` 유무에 따라 답이 달라지고 그 차이를 `answers_B.md`에 한 문장으로 적었다.
- [ ] `outputs/chat-*.json`에 `eval_count`·`eval_duration`·`tokens_per_sec`가 숫자로 기록된다.
- [ ] 없는 모델 이름으로 실행하면 사람이 읽을 메시지가 나오고 종료 코드가 0이 아니다.

### 문제 2 · pipeline 결과 해석

`tasks_B.md`의 B-2다. `fixtures/pipeline_output.json`을 열고 세 문항에 판단과 근거를 적는다.

1. 감성 분류의 세 번째 결과(`score` 0.51대)를 보고 이 값의 뜻과 그대로 쓰면 안 되는 이유를 적는다.
2. 텍스트 생성 결과가 반복되는 현상에서 확인할 생성 인자 2개와 `stderr` 메시지의 성격(오류인가 안내인가)을 적는다.
3. 생성이 `cpu`에서 6초 넘게 걸린 결과를 보고 GPU를 쓰게 하는 방법과 실제로 GPU에서 돌았는지 확인하는 방법을 적는다.

완료 조건:

- [ ] 세 문항 모두 판단과 근거가 있다.
- [ ] 각 근거가 JSON의 어느 키를 보고 내린 것인지 적혀 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — `--system`을 넣었는데 답이 그대로다</summary>

`build_messages`가 system 메시지를 `messages[0]`에 넣는지, `main`이 `args.system`을 `build_messages`에 넘기는지 순서대로 확인한다. `outputs/chat-*.json`의 `system` 키가 `null`이면 인자가 전달되지 않은 것이다.
</details>

<details>
<summary>힌트 2 — `tokens_per_sec`가 0이거나 나누기 오류가 난다</summary>

`eval_duration`은 나노초다. `eval_count / (eval_duration / 1e9)`로 계산하고, `eval_duration`이 0이면 `None`을 넣는다. 응답 JSON에 키가 없으면 `data.get("eval_count")`로 안전하게 읽는다.
</details>

<details>
<summary>힌트 3 — 없는 모델인데 연결 실패 메시지가 나온다</summary>

서버가 켜져 있으면 없는 모델은 `httpx.HTTPStatusError`(404)로 온다. `ConnectError`와 `HTTPStatusError`를 따로 잡고, 404일 때는 `ollama list`를 안내하는 문장을 만든다.
</details>

### 검증

- 정상: `--system` 유무 두 실행의 `outputs/chat-*.json`에 `tokens_per_sec`가 숫자로 있고, 두 `content`가 다르다.
- 경계 또는 실패: Ollama를 끄고 실행하면 연결 실패 문장이, 켜고 없는 모델로 실행하면 모델 없음 문장이 나온다. 두 문장이 서로 달라야 한다.
- 설명: "`stream: false`와 `think: false`를 요청에 명시하는 이유"를 각각 한 문장으로 쓴다.

### 확장 문제

1. `--stream` 플래그를 추가해 NDJSON 응답을 줄 단위로 출력하고, 마지막 줄(`done: true`)에서만 메타를 기록한다.
2. `outputs/`의 JSON 두 개를 읽어 `tokens_per_sec`를 비교하는 `compare.py`를 만든다.

## 3교시 실습 — 개인 실기평가와 대체 운영

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
Set-Location $HOME\osa-practice\week08-mock-b
uv run python check_env.py
Get-Content outputs\env-check.json
Set-Location <지정 저장 경로>
git status
ollama list
```

- 비공개 패킷을 지정 폴더에 풀고 파일 목록이 패킷 문서와 같은지 확인한다.
- `check_env.py`는 2교시 `client_starter` 복사본(`week08-mock-b`)의 것을 그대로 쓴다. 패킷에 별도 점검 스크립트가 있으면 그것을 우선하고, 없으면 `week08-mock-b\outputs\env-check.json`이 시작 전 점검 증거다.
- 허용 자료·AI 도구 범위·제출 경로는 시험 공지(학교 운영 문서)를 따른다.

### 문제 1 · 개인 실기 응시 절차

1. 요구사항 문서를 읽고 완료 조건마다 체크 항목을 만든다. 코드는 아직 만지지 않는다.
2. 검증 명령을 먼저 정한다(`uv run ...`, `git ls-files`, 파일 열기).
3. 가장 짧은 한 경로를 끝까지 연결한 뒤 다음 요구사항으로 간다.
4. 22분에 작업을 멈추고 정상·실패 경로를 각각 한 번 재현한다.
5. commit하고 `git log -1 --oneline`의 id를 제출 설명에 적는다. 제출 파일을 다시 열어 같은 내용인지 본다.

완료 조건:

- [ ] `outputs/env-check.json`이 시작 시각과 함께 있다.
- [ ] 제출 파일·commit id·짧은 설명(무엇을·왜)이 제출 경로에 있다.
- [ ] 못 끝낸 항목은 증상·관찰·시도 세 줄로 적었다.

### 문제 2 · 대체 운영 — 2차 종합과제 최종 점검

실기가 다른 슬롯에 있는 분반은 이 문제를 수행한다. 시간 배분은 위 표를 그대로 쓰되 "문항 해결"을 "재현 점검"으로 읽는다.

1. `examples/assignment_check.ps1 -RepoPath <내 과제 저장소>`를 실행해 파일 존재·`.gitignore`·추적 파일·비밀 흔적을 훑는다.
2. 새 폴더에 `git clone`하고 README의 명령을 **그대로** 실행한다(`uv sync --frozen` → 실행 → `eval.py`).
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

- `answers_A.md`: 모의 A 복구 기록(고친 항목·증상), 라이선스 3문항, Git 1문항
- 모의 A 저장소: `.gitignore`·`.env.example` commit, `git ls-files`에 `.env` 없음
- `answers_B.md`: 기능 추가 전후 비교 문장, 실패 경로 두 문장, pipeline 해석 3문항
- `outputs/chat-*.json` 2개: `--system` 유무, `tokens_per_sec` 포함
- 개인 실기: 제출 파일 + commit id + 짧은 설명(비공개 제출 경로)
- 2차 종합과제: 저장소 URL + 최종 commit id + `assignment_check.ps1` 결과([assignment_brief.md](assignment_brief.md) 기준)
