# 8주차 예제 — 공개 동형 모의 실기 starter

이 폴더는 1·2교시 모의 실기의 시작 자료와 3교시 2차 과제 점검 스크립트다. 실제 실기 패킷의 문항·값·정답은 들어 있지 않다.

## 파일 구성

| 경로 | 역할 |
|---|---|
| `mock_exam/README.md` | 모의 실기 폴더 안내 |
| `mock_exam/tasks_A.md` | 모의 A: 깨진 프로젝트 복구 + 라이선스 3문항 + Git 상황 1문항, 답안 양식 |
| `mock_exam/tasks_B.md` | 모의 B: 클라이언트 기능 추가 + pipeline 결과 해석 3문항, 답안 양식 |
| `mock_exam/make_broken_repo.ps1` | `broken_project/`를 개인 폴더에 복사하고 `.env`가 커밋된 Git 이력을 만드는 스크립트 |
| `mock_exam/broken_project/` | 의도적으로 깨진 uv 프로젝트(`pyproject.toml` 오류 3곳, `.gitignore` 없음, `report.py`) |
| `mock_exam/client_starter/` | 기능 추가용 최소 Ollama 클라이언트(uv 프로젝트: `config.py`, `chat.py`, `check_env.py`) |
| `mock_exam/fixtures/pipeline_output.json` | 해석 문항용 자체 작성 샘플(실제 실행 결과가 아님) |
| `assignment_check.ps1` | 2차 종합과제 제출 전 파일 존재·`.gitignore`·추적 파일·비밀 흔적 검사 |

## 실행 방법

원본을 수정하지 않는다. 아래 명령은 교재 폴더의 `examples/mock_exam`에서 시작한다.

모의 A(깨진 프로젝트):

```powershell
.\make_broken_repo.ps1 -Destination $HOME\osa-practice\week08-mock-a
Set-Location $HOME\osa-practice\week08-mock-a
uv sync
uv run python report.py
```

모의 B(클라이언트 시작 코드):

```powershell
Copy-Item -Recurse .\client_starter $HOME\osa-practice\week08-mock-b
Set-Location $HOME\osa-practice\week08-mock-b
Copy-Item .env.example .env
uv sync
uv run python check_env.py
uv run python chat.py --prompt "uv sync 가 하는 일을 한 문장으로 설명하라."
```

2차 과제 점검:

```powershell
..\assignment_check.ps1 -RepoPath $HOME\osa-practice\my-rag-project
```

스크립트 실행이 막히면 `powershell -ExecutionPolicy Bypass -File <스크립트> <인자>` 형태로 실행한다.

## 관찰 지점

1. 모의 A `uv sync`: 첫 실행은 TOML parse error, 고친 뒤에는 경고만 있고 패키지가 설치되지 않는 "조용한 실패", 그다음 `requires-python` 오류. 순서대로 한 번에 하나씩 나타난다.
2. 모의 A `git ls-files`: 복구 전에는 `.env`가 보이고, `git rm --cached` 뒤에도 `git log -p -- .env`에는 값이 남는다.
3. 모의 B `outputs/chat-*.json`: 시작 코드는 `model`·`host`·`prompt`·`content`만 기록한다. 기능 추가 뒤 `system`·`eval_count`·`eval_duration`·`total_duration`·`tokens_per_sec`가 늘어난다.
4. 모의 B 실패 경로: Ollama를 끄면 `ConnectError` 메시지, 켠 상태에서 없는 모델이면 HTTP 404 메시지. 두 문장이 달라야 한다.
5. `check_env.py`: `outputs/env-check.json`의 `ollama_reachable`·`model_available`. 3교시 시작 전 증거로 쓴다.

## GPU 없을 때·네트워크 없을 때

- GPU가 없으면 `.env`의 `OLLAMA_MODEL`을 `qwen3:0.6b`(CPU 대체)로 바꾼다. `tokens_per_sec`가 낮게 나오는 것은 정상이며 답안에 환경을 적는다.
- 네트워크가 없으면 `uv sync --offline`을 쓴다. 3·4주차에서 같은 패키지(`httpx`, `python-dotenv`)를 설치했다면 uv 캐시로 해결된다.
- Ollama가 없어도 모의 A는 끝까지 할 수 있다(`report.py`는 연결 실패를 기록하고 종료 코드 2로 끝난다). 모의 B의 기능 추가는 코드까지 작성하고, 실행 확인은 서버가 있는 PC에서 한다.
- 해석 문항(`fixtures/pipeline_output.json`)은 모델·GPU·네트워크 없이 푼다.

## 복사 후 변형

- `broken_project/`는 반드시 `make_broken_repo.ps1`로 복사본을 만들어 고친다. 원본에서 `uv sync`를 실행하면 교재 폴더에 `.venv`가 생긴다.
- `client_starter/`는 복사한 뒤 `TODO(B-1)`만 채운다. 시작 코드의 `stream: false`·`think: false`·`options`는 지우지 않는다.
- 고친 `pyproject.toml`이나 완성한 `chat.py`를 교재 폴더에 커밋하지 않는다.

## 환경 기준표와 lock 파일

- 모델 ID·양자화·용량은 [학기별 환경 기준표](../../../../environment_baseline_template.md)에서 확정하며, 코드의 `qwen3:4b`·`qwen3:0.6b`는 교재 검증용 기본값이다.
- 예제 프로젝트에 `uv.lock`은 포함하지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
