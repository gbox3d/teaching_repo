# 13주차 실습 — 모델 없이 검사하고, 내 PC 밖에서 검사하고, 남의 변경을 검사한다

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 실습 시간에 모델을 내려받지 않는다. 이번 주 테스트는 모델 서버 없이 돌고, 통합 테스트만 캐시된 기본 모델(`OLLAMA_MODEL`)을 쓴다.
- 실제 토큰·비밀번호를 어디에도 쓰지 않는다. 3교시에 심는 "가짜 토큰"은 커밋하지 않고 검출을 확인한 즉시 지운다.
- 실패 재현(테스트 깨기, 비밀 심기)은 예제 원본이 아니라 **개인 복사본**에서만 한다.

## 1교시 실습 — 가짜 클라이언트로 서비스 테스트 만들기

### 상황

팀원이 12주차 서비스에 기능을 추가한 PR을 올렸다. 리뷰어가 "확인하려면 Ollama를 켜고 손으로 다섯 번 요청해야 한다"고 불평한다. 모델 서버 없이 `uv run pytest` 한 줄로 스키마·서비스·HTTP 계층을 검사하는 테스트를 붙이고, lint·format까지 통과시켜 "내 PC에서는 됨"을 코드로 대신하라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 예제 복사·`uv sync`·기존 테스트 실행, 추가할 테스트 3개의 실패 조건 예상 |
| 테스트 추가 | 5–16분 | 스키마·서비스·HTTP 계층에 테스트 1개씩 추가해 통과 |
| lint·format | 16–22분 | ruff 통과 확인, 일부러 만든 오류를 `--fix`·`format`으로 수정 |
| 느린 테스트 | 22–26분 | `integration` 마커와 `RUN_INTEGRATION` 동작 확인 |
| 검증·기록 | 26–30분 | 출력 정리, commit |

### 준비

교재 주차 폴더의 예제를 개인 실습 폴더로 복사한다. `$src`에는 교재 저장소의 이 주차 `examples` 폴더 경로를 넣는다. 저장 경로는 학기별 환경 기준표를 따른다(아래는 예시).

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week13_test_ci_security\examples"
New-Item -ItemType Directory -Force C:\classwork\week13 | Out-Null
Copy-Item -Recurse "$src\ci_lab" C:\classwork\week13\ci_lab
Set-Location C:\classwork\week13\ci_lab
Copy-Item .env.example .env
uv sync
uv run pytest -q
```

마지막 줄이 `19 passed, 2 deselected`로 끝나야 한다. `tests/conftest.py`를 열어 `FakeOllamaClient`의 네 속성(`reply`·`models`·`fail_with`·`calls`)과 fixture 세 개(`service`·`make_service`·`api_for`)를 확인한다.

`ci_lab`은 12주차 서비스를 줄여 다시 쓴 것이라 요청 필드(`prompt`·`system`)와 예외→상태 코드(503·404·502)가 12주차(502·503·504)와 다르다. 아래 문제는 `ci_lab`의 매핑을 기준으로 풀고, 이 테스트를 팀 저장소로 옮길 때는 팀 코드가 정한 코드값으로 바꾼다.

### 문제 1 · 테스트 3개 추가

실행 전에 예상표를 적는다. "이 테스트가 실패하면 무엇이 잘못된 것인가"를 한 문장으로 쓴다.

| 테스트 | 검사 대상 | 실패하면 잘못된 것 |
|---|---|---|
| 공백만 있는 prompt | `schemas.py`의 validator |  |
| system 프롬프트 순서 | `service.py`의 `build_messages` |  |
| 모델 없음 → 404 | `main.py`의 예외 매핑 |  |

1. `tests/test_schemas.py`에 `test_whitespace_only_prompt_is_rejected`를 추가한다. `ChatRequest(prompt="   ")`가 `ValidationError`를 내야 한다. 먼저 `schemas.py`에서 `prompt_must_have_text` 위의 데코레이터 두 줄(`@field_validator("prompt")`, `@classmethod`)을 주석 처리한 채 실행해 **실패**를 본다. 새 테스트는 `DID NOT RAISE`로, 기존 `test_prompt_is_stripped`는 `assert` 줄로 함께 실패한다 — 공백 제거도 같은 validator가 하기 때문이다. 왜 2건인지 한 문장으로 적고, 주석을 풀어 통과시킨다.
2. `tests/test_service.py`에 `test_system_prompt_goes_first`를 추가한다. `ChatRequest(prompt="안녕", system="너는 수업 도우미다")`로 `service.chat()`을 부른 뒤 `fake_client.calls[-1]["messages"]`가 `system` 역할 → `user` 역할 순서의 두 항목인지 검사한다.
3. `tests/test_api.py`에 `test_missing_model_becomes_404`를 추가한다. `make_service(fail_with=ModelNotFoundError("모델이 서버에 없다: no-such-model"))`로 만든 서비스를 `api_for`에 넣고 `POST /chat`을 보내 상태 코드 404와 `detail`에 `no-such-model`이 들어 있는지 검사한다. `ModelNotFoundError` import를 잊지 않는다.
4. `uv run pytest -q`로 `22 passed, 2 deselected`를 확인하고, `-q` 없이 실행해 어느 파일의 어느 테스트가 추가됐는지 읽는다.

완료 조건:

- [ ] 테스트 3개가 각각 다른 파일에 있고 `22 passed, 2 deselected`다.
- [ ] 1번에서 validator를 끈 상태의 실패 출력(`assert` 줄 또는 `DID NOT RAISE`)을 기록했다.
- [ ] 예상표의 세 번째 열을 채웠다.

### 문제 2 · ruff와 느린 테스트

1. `uv run ruff check .`와 `uv run ruff format --check .`를 실행해 둘 다 통과하는지 확인한다.
2. `tests/test_api.py`의 `from collections.abc import Callable` 바로 위 줄에 `import os`를 추가하고 `ruff check .`를 다시 실행한다. `F401 'os' imported but unused`가 나와야 한다. `from __future__` 줄 바로 아래처럼 다른 자리에 넣으면 `I001`(import 블록 정렬)이 함께 나온다 — 그 경우 두 코드를 모두 적는다. 규칙 코드와 메시지를 적은 뒤 `uv run ruff check . --diff`로 무엇이 지워질지 먼저 보고, `uv run ruff check . --fix`로 고친다.
3. `tests/test_service.py`의 한 `assert` 앞에 공백을 서너 개 더 넣거나 두 줄을 한 줄로 합친다. `ruff format --check .`의 출력(`Would reformat`)을 적고 `uv run ruff format .`로 되돌린다.
4. `uv run pytest -m integration -q`를 실행한다. `RUN_INTEGRATION`이 없으므로 `2 skipped`가 나와야 한다. Ollama가 있는 PC라면 아래로 실제 실행하고 `--durations=3`의 시간을 단위 테스트 전체 시간과 비교한다.

```powershell
$env:RUN_INTEGRATION = "1"
uv run pytest -m integration -q --durations=3
Remove-Item Env:RUN_INTEGRATION
```

5. 개인 실습 폴더를 Git 저장소로 만들고 첫 commit을 남긴다(2교시에서 push한다). `git status`에 `.env`·`outputs/`·`.venv/`가 없어야 한다.

```powershell
git init
git add -A
git status --short
git commit -m "Add unit tests, ruff config and CI workflow"
```

완료 조건:

- [ ] `ruff check .`·`ruff format --check .`가 최종적으로 통과한다.
- [ ] F401(또는 그에 해당하는 코드)와 `Would reformat` 출력을 각각 기록했다.
- [ ] `pytest -m integration`의 `skipped` 출력(또는 실제 실행 시간)을 기록했고 첫 commit이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — <code>ModuleNotFoundError: No module named 'app'</code> 또는 <code>'tests'</code></summary>

`pyproject.toml`과 `app/`, `tests/`가 함께 보이는 폴더에서 실행해야 한다. `pyproject.toml`의 `[tool.pytest.ini_options] pythonpath = ["."]`가 프로젝트 루트를 `sys.path`에 넣어 준다. 다른 폴더에서 `uv run pytest ../ci_lab`처럼 실행하면 이 설정이 적용되지 않는다.
</details>

<details>
<summary>힌트 2 — 404 테스트가 503이나 502로 실패한다</summary>

`fail_with`에 넣은 예외 클래스를 확인한다. `main.py`는 `OllamaUnavailableError`→503, `ModelNotFoundError`→404, 그 밖의 `OllamaError`→502 순서로 잡는다. 부모 클래스 `OllamaError`를 넣으면 502가 된다.
</details>

<details>
<summary>힌트 3 — system 프롬프트 테스트에서 <code>calls</code>가 비어 있다</summary>

`service` fixture와 `fake_client` fixture를 **같은 테스트 함수의 인자**로 함께 받아야 같은 가짜 객체를 본다. `make_service`로 새로 만들었다면 그 함수가 돌려준 두 번째 값(client)의 `calls`를 봐야 한다.
</details>

### 검증

- 정상: `uv run pytest -q`가 `22 passed, 2 deselected`, `ruff check .`·`ruff format --check .`가 통과한다.
- 경계 또는 실패: validator를 끄면 공백 prompt 테스트(`DID NOT RAISE`)와 `test_prompt_is_stripped`(`assert` 줄) 2건만 실패하고 나머지는 통과한다(테스트 1개만 추가한 시점이면 `2 failed, 18 passed, 2 deselected`). `fail_with`를 `OllamaError`로 바꾸면 404 테스트가 502로 실패한다. `service.py`의 `1_000_000`을 `1_000`으로 바꾸면 `test_chat_converts_fake_response` 1건만 실패한다.
- 설명: 테스트가 모델 서버 없이 도는데도 "오류 경로를 검사했다"고 말할 수 있는 이유를 한 문장으로 적는다.

### 확장 문제

1. `FakeOllamaClient`에 `latency_s` 속성을 추가해 `chat()`이 그 시간만큼 `time.sleep`하게 하고, 서비스에 타임아웃이 없다는 사실을 테스트로 드러낸다.
2. `test_api.py`에 `GET /health`가 `ok=False`일 때도 200을 돌려주는지 검사하는 테스트를 쓰고, 12주차 확장 문제(503으로 바꾸기)와 연결해 어느 쪽이 맞는지 두 문장으로 적는다.
3. `uv run pytest --cov`가 왜 동작하지 않는지(허용 의존성 범위) 확인하고, 대신 `-v`로 테스트 이름만으로 무엇이 검사되지 않았는지 목록을 만든다.

## 2교시 실습 — GitHub Actions로 초록불과 빨간불 만들기

### 상황

팀 저장소에 "테스트 다 통과했어요"라는 PR 설명만 있고 아무도 그것을 확인할 수 없다. 저장소에 workflow를 붙여 push·PR마다 GitHub가 깨끗한 머신에서 `ruff`·`pytest`를 돌리게 하고, 리뷰어가 로그 대신 상태 체크를 보게 만들어라. 빨간불이 켜졌을 때 로그에서 첫 오류를 찾는 순서까지 몸에 익힌다.

이어받는 것: 1교시의 `C:\classwork\week13\ci_lab`(테스트 22개 통과, 첫 commit 완료). 없으면 준비 절의 명령으로 예제를 복사하고 `git init`·commit부터 한다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | `ci.yml` 읽기, 각 step과 로컬 명령의 대응표, 실패 지점 예상 |
| 저장소·push | 4–12분 | GitHub 새 저장소, `push`, Actions 첫 실행 확인 |
| PR·초록불 | 12–19분 | 브랜치·배지·PR, 상태 체크 확인, 캐시·시간 기록 |
| 빨간불·수정 | 19–26분 | 단위 변환 버그 commit → 로그 읽기 → 수정 commit → merge |
| 검증·기록 | 26–30분 | 실행 URL·step 이름·첫 오류 줄 기록 |

### 준비

GitHub에 로그인한 뒤 새 저장소 `week13-ci-lab`을 **빈 상태로**(README·.gitignore·라이선스 추가 없이) 만든다. 그다음 로컬에서:

```powershell
Set-Location C:\classwork\week13\ci_lab
git branch -M main
git remote add origin https://github.com/<계정>/week13-ci-lab.git
git push -u origin main
```

브라우저에서 저장소의 **Actions** 탭을 연다. `ci` workflow의 첫 실행이 보여야 한다.

### 문제 1 · 첫 실행과 PR 상태 체크

1. 실행 전에 `.github/workflows/ci.yml`을 읽고 대응표를 적는다.

| step 이름 | 로컬에서 같은 명령 | 실패하면 의심할 것 |
|---|---|---|
| uv 설치 |  |  |
| 의존성 설치 |  |  |
| ruff lint |  |  |
| ruff format 검사 |  |  |
| pytest |  |  |

2. 첫 실행이 끝나면 `test` 잡을 열어 각 step의 소요 시간을 적는다. `audit` 잡의 결과도 적는다(실패해도 workflow는 초록일 수 있다 — 왜인지 `ci.yml`에서 찾는다).
3. 브랜치 `feature/ci-badge`를 만들고 `README.md` 맨 위에 상태 배지를 추가한다.

```markdown
![ci](https://github.com/<계정>/week13-ci-lab/actions/workflows/ci.yml/badge.svg)
```

4. commit·push 후 GitHub에서 PR을 만든다(제목: `Add CI status badge`). PR 하단의 상태 체크가 노란 원 → 초록 체크로 바뀌는 것을 본다. 실행 URL을 적는다.
5. 두 번째 실행의 `uv 설치`·`의존성 설치` 시간을 첫 실행과 비교한다. 로그에서 캐시 관련 줄을 찾아 적는다.

완료 조건:

- [ ] Actions 첫 실행(main push)과 PR 실행이 모두 초록불이고 URL 2개를 적었다.
- [ ] 대응표 5행을 채웠다.
- [ ] 첫 실행과 두 번째 실행의 `uv sync` 시간 차이와 그 이유를 한 문장으로 적었다.

### 문제 2 · 빨간불 만들기와 고치기

1. 같은 브랜치에서 `app/service.py`의 `duration_ns / 1_000_000`을 `duration_ns / 1_000`으로 바꾼다. **push 전에** 어느 step이, 어느 테스트가 실패할지 예상해 적는다. 로컬에서 `uv run pytest -q`로 예상을 확인한다.
2. commit 메시지 `Break duration unit on purpose`로 push한다. PR의 상태 체크가 빨간 X가 될 때까지 기다린다.
3. 실패한 실행을 열어 다음 순서로 기록한다: 빨간 job 이름 → X가 붙은 step 이름 → 로그의 첫 오류 줄(`FAILED …` 또는 `assert …`) → 그 줄이 가리키는 파일·테스트 이름.
4. 로컬에서 되돌리고(`1_000_000`) `uv run pytest -q` 통과를 확인한 뒤 `Fix duration unit`으로 push한다. 초록불이 되면 PR을 merge한다.
5. (선택) Settings → Branches에서 `main` 보호 규칙을 만들고 required status check로 `test`를 지정한다. 규칙 이름과 선택 항목을 적는다.

완료 조건:

- [ ] 빨간불 실행 URL, 실패한 step 이름, 첫 오류 줄, 실패한 테스트 이름을 적었다.
- [ ] 수정 commit으로 초록불이 되어 PR이 merge되었다.
- [ ] 예상(어느 step·어느 테스트)과 실제가 같았는지 적었다.

### 단계별 힌트

<details>
<summary>힌트 1 — Actions 탭에 workflow가 나타나지 않는다</summary>

`.github/workflows/ci.yml`이 **저장소 루트** 기준 경로인지 `git ls-files .github`로 확인한다. `Copy-Item`이 숨김 폴더를 빠뜨렸다면 예제에서 다시 복사한다. 기본 브랜치 이름이 `main`이 아니면 `on.push.branches`와 맞지 않아 push 실행이 생기지 않는다(PR 실행은 생긴다).
</details>

<details>
<summary>힌트 2 — <code>uv sync</code> step에서 실패한다</summary>

로그의 첫 오류 줄을 본다. `requires-python`을 만족하는 Python이 없다는 메시지면 `uv python install` step이 있는지 확인한다. lock 관련 메시지면 `--frozen`·`--locked`를 붙였는데 `uv.lock`을 커밋하지 않았거나, `--locked`인데 lock이 `pyproject.toml`보다 오래된 경우다.
</details>

<details>
<summary>힌트 3 — push가 거부된다</summary>

`git remote -v`로 주소를 확인한다. 인증 창이 뜨면 GitHub 계정으로 로그인한다(비밀번호·토큰을 파일에 적지 않는다). 저장소를 만들 때 README를 추가했다면 원격에 이미 commit이 있으므로 `git pull --rebase origin main` 후 다시 push한다.
</details>

### 검증

- 정상: main push와 PR 실행이 초록불이고, `ruff check`·`ruff format --check`·`pytest` step이 모두 통과 표시다.
- 경계 또는 실패: 단위 변환 버그는 `ruff` step을 통과하고 `pytest` step에서만 실패한다. 로그의 첫 오류 줄이 `test_chat_converts_fake_response`를 가리킨다.
- 설명: 로컬에서 통과한 테스트를 CI에서 다시 돌리는 이유를 "다른 PC"라는 말을 써서 한 문장으로 적는다.

### 확장 문제

1. `test` 잡에 `strategy.matrix`로 `ubuntu-latest`와 `windows-latest`를 추가하고, Windows 러너에서 달라지는 것(경로·줄 끝)을 관찰한다.
2. 기준 PC에서 `uv lock`을 만들어 커밋한 뒤, `pyproject.toml`에만 의존성을 추가하고 lock을 올리지 않은 채 push한다. `uv sync --frozen`은 그대로 통과하고 `uv sync --locked`(또는 `uv lock --check` step)만 실패하는 것을 비교해, 두 옵션의 차이와 CI에 어느 쪽을 둘지 적는다.
3. `audit` 잡의 `continue-on-error`를 지우면 무엇이 달라지는지, 팀 규칙으로 어느 쪽이 맞는지 두 문장으로 적는다.

## 3교시 실습 — 의존성 감사와 비밀 검색, 교차 리뷰

### 상황

릴리스(14주차)를 앞두고 팀 저장소를 외부에 공개하기 전 점검을 맡았다. 의존성에 알려진 취약점이 있는지, 비밀이나 위험한 모델 파일이 저장소에 들어 있지 않은지 도구로 확인하고, 다른 팀의 PR 하나를 체크리스트로 리뷰해 근거 있는 판정을 남겨라.

이어받는 것: 2교시의 `week13-ci-lab` 저장소(초록불, PR merge 완료). 리뷰 대상은 다른 팀 저장소의 열린 PR 1건이다. 없으면 짝이 2교시 저장소에 `docs/readme-run` 브랜치로 README 실행 절을 추가하는 PR을 열어 준다(3분).

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 의존성 개수·취약점 수 예상, 점검 스크립트가 잡을 항목 예상 |
| 의존성 감사 | 4–11분 | `audit_report.py` 실행, 보고서 읽기, 다음 행동 정리 |
| 비밀·모델 파일 검색 | 11–18분 | 깨끗한 결과 → 문제 3종 심기 → 검출 → 제거 |
| 교차 리뷰 | 18–27분 | 다른 팀 PR에 체크리스트 기반 코멘트·판정, 받은 리뷰에 응답 |
| 검증·기록 | 27–30분 | 증거 폴더 복사, 리뷰 기록 표 |

### 준비

```powershell
Set-Location C:\classwork\week13\ci_lab
git switch main
git pull
git status --short          # 비어 있어야 한다
```

### 문제 1 · 감사와 비밀 검색

1. 예상을 적는다: `uv sync`로 들어온 패키지 수, 그중 취약점이 있을 패키지 수, `security_check.ps1`이 깨끗한 저장소에서 지적할 항목 수.
2. 감사를 실행하고 `outputs/audit-*.md`를 읽는다. 검사한 패키지 수, 취약 패키지 수, 취약점이 있다면 ID와 `고친 버전`, 다음 행동을 적는다.

```powershell
uv run python audit_report.py
```

   네트워크가 없어 실패하면 `uv run python audit_report.py --sample`로 보고서 형식을 읽고 그 사실을 기록한다.

3. 점검 스크립트를 실행한다. 깨끗한 저장소에서 `문제 0건`이어야 한다. `outputs/security-*.md`를 `evidence/week13/security-clean.md`로 복사한다.

```powershell
.\security_check.ps1
```

4. 문제 3종을 **스테이지에만** 심는다(commit 금지). 각 단계마다 스크립트를 다시 실행해 무엇이 잡히는지 적는다.

```powershell
git add -f .env                                                  # (a) 비밀 파일 스테이지
Set-Content notes.txt ('HF_TOKEN=hf_' + 'abcdefghijklmnopqrstuvwxyz12345678') # (b) 가짜 토큰(실행 시 조합)
git add notes.txt
New-Item model.pt -ItemType File | Out-Null                      # (c) pickle 계열 모델 파일
git add model.pt
.\security_check.ps1
```

5. 보고서에서 (a)·(b)·(c)가 각각 어느 절에 어떤 문구로 나오는지, (b)가 몇 건으로 잡히는지 적는다. 그 보고서를 `evidence/week13/security-planted.md`로 복사한 뒤 **심은 것을 전부 제거**한다.

```powershell
git rm --cached .env notes.txt model.pt
Remove-Item notes.txt, model.pt
git status --short          # 비어 있어야 한다
.\security_check.ps1        # 다시 문제 0건
```

완료 조건:

- [ ] `evidence/week13/audit-*.md`(또는 `--sample` 결과와 그 사실)에 패키지 수·취약점 수·다음 행동이 있다.
- [ ] `security-clean.md`는 0건, `security-planted.md`는 (a)·(b)·(c)를 모두 잡았다.
- [ ] `git status --short`가 비어 있고 `notes.txt`·`model.pt`가 사라졌으며, 심은 것이 commit 이력에 없다(`git log --stat -3`).

### 문제 2 · 교차 코드리뷰

1. `examples/ci_lab/REVIEW_CHECKLIST.md`를 열고, 리뷰 대상 PR의 설명·연결 Issue·상태 체크를 먼저 본다(0절·1절).
2. 변경 파일을 읽으며 2~4절의 항목 중 **근거가 있는 것만** 골라 코멘트를 남긴다. 코멘트는 `[근거] → [문제] → [제안]` 구조이며 최소 2개다. 좋은 점 1개도 구체적으로 적는다.
3. `Review changes`에서 `Approve` 또는 `Request changes`를 고른다. 수정 요청이면 무엇이 되면 승인할지 함께 적는다.
4. 자기 저장소(또는 팀 저장소)의 PR에 받은 리뷰가 있으면 응답 1개를 남긴다(수용·반박·질문 중 하나, 근거 포함).
5. 개인 저장소 `reviews/week13.md`에 체크리스트 마지막의 표 한 행을 채운다.

완료 조건:

- [ ] 코멘트 2개 이상이 각각 파일·줄 또는 로그를 근거로 가리킨다.
- [ ] 판정(승인/수정 요청)을 남겼고 대표 코멘트 URL을 적었다.
- [ ] 받은 리뷰에 응답 1개를 남겼거나, 받은 리뷰가 없다는 사실을 적었다.

### 단계별 힌트

<details>
<summary>힌트 1 — <code>audit_report.py</code>가 <code>pip_audit</code> 모듈을 찾지 못한다</summary>

`uv sync`가 dev 그룹까지 설치했는지 `uv run python -m pip_audit --version`으로 확인한다. `--no-dev`로 설치했다면 `uv sync`를 다시 실행한다.
</details>

<details>
<summary>힌트 2 — 심은 파일이 검출되지 않는다</summary>

스크립트는 **git이 아는 파일**(추적 + 스테이지)만 본다. `git add`를 했는지 `git status --short`로 확인한다. `notes.txt`의 토큰은 `hf_` 뒤에 영문·숫자 20자 이상이어야 패턴에 걸린다.
</details>

<details>
<summary>힌트 3 — 실행 정책 오류로 <code>.ps1</code>이 실행되지 않는다</summary>

`Get-ExecutionPolicy`가 `Restricted`이면 현재 세션에만 `Set-ExecutionPolicy -Scope Process RemoteSigned`를 적용한다. 공유 PC의 전역 정책은 바꾸지 않는다.
</details>

### 검증

- 정상: 깨끗한 저장소에서 `security_check.ps1`이 종료 코드 0, `audit_report.py`가 보고서를 만든다.
- 경계 또는 실패: 스테이지한 `.env`는 2절, 가짜 토큰은 3절(패턴 2종으로 2건), `.pt`는 4절에 잡히고 종료 코드가 1이다. 제거 후 다시 0이다.
- 설명: 점검 스크립트가 찾은 줄의 **내용을 출력하지 않는** 이유를 한 문장으로 적는다.

### 확장 문제

1. `security_check.ps1`에 `.env.example`이 없을 때를 경고하는 항목을 추가하고, 팀 저장소에서 실행해 결과를 Issue로 등록한다.
2. `.git/hooks/pre-commit`에서 `security_check.ps1`을 호출해 문제가 있으면 commit이 막히게 만든다(`pwsh -File`). 훅은 저장소에 커밋되지 않는다는 점을 README에 어떻게 적을지 두 문장으로 쓴다.
3. 팀 저장소의 `SOURCES.md`에 사용 모델의 파일 형식(safetensors·GGUF 여부)과 revision을 추가하고, `trust_remote_code`를 쓰는 곳이 있는지 `security_check.ps1 -Path`로 확인한다.

## 제출 체크

- `uv run pytest -q` 최종 출력(`22 passed, 2 deselected`)과 추가한 테스트 3개의 commit id
- validator를 끈 실패 출력, F401 출력, `Would reformat` 출력, `pytest -m integration` 결과
- Actions 실행 URL 2개(성공·실패), step 대응표, 실패 step 이름·첫 오류 줄·실패 테스트 이름, merge된 PR URL
- `evidence/week13/audit-*.md`, `security-clean.md`, `security-planted.md`
- `reviews/week13.md`: 리뷰한 PR URL, 판정, 코멘트 URL, 받은 응답 요약
- 선택: 확장 문제 결과
