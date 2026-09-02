# 4주차 예제 — Ollama 클라이언트, 모델 보고서, 커스텀 모델

## 파일 구성

| 파일 | 역할 | 쓰는 교시 |
|---|---|---|
| `model_report_template.md` | 모델 2개 비교 보고서 양식. 3교시 전후 비교표 포함 | 1·3교시 |
| `ollama_probe.ps1` | `ollama list/show/ps` 출력을 `outputs/`에 텍스트로 저장 | 1교시 |
| `ollama_client/` | uv 프로젝트. 아래 파일을 담는다 | 2·3교시 |
| `ollama_client/pyproject.toml` | 의존성 `httpx`, `python-dotenv`. 버전은 고정하지 않는다 | |
| `ollama_client/config.py` | 기본값 < `.env`·환경변수 < 인자 순서의 설정 로더 | 2교시 |
| `ollama_client/ollama_api.py` | 오류 문장, tokens/s 계산, JSON 저장 도우미 | 2교시 |
| `ollama_client/chat.py` | `/api/chat` 비스트리밍. `outputs/chat-*.json` 기록 | 2·3교시 |
| `ollama_client/stream.py` | `/api/chat` 스트리밍(NDJSON). `outputs/stream-*.json` 기록 | 2교시 |
| `ollama_client/Modelfile` | 수업 도우미 커스텀 모델(FROM·SYSTEM·PARAMETER) | 3교시 |
| `ollama_client/.env.example` | 환경변수 예시. `.env`로 복사한다 | 2교시 |
| `ollama_client/.gitignore` | `.venv/`, `.env`, `outputs/` 등 커밋 제외 | |
| `ollama_client/README.md` | 짧은 실행 안내 | |

## 실행 방법

원본을 두고 개인 실습 폴더에 복사한다. `$src`에는 교재 저장소의 이 `examples` 폴더 경로를 넣는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week04_ollama_local_llm\examples"
New-Item -ItemType Directory -Force C:\classwork\week04 | Out-Null
Copy-Item "$src\model_report_template.md" C:\classwork\week04\model_report.md
Copy-Item "$src\ollama_probe.ps1" C:\classwork\week04\
Copy-Item -Recurse "$src\ollama_client" C:\classwork\week04\ollama_client
```

1교시(CLI 실측):

```powershell
Set-Location C:\classwork\week04
ollama list
ollama show qwen3:4b
ollama run qwen3:4b          # 안에서 /set verbose → 질문 3개 → /bye
ollama ps                    # run 을 끝낸 직후
.\ollama_probe.ps1 -Model qwen3:4b
```

2교시(REST API):

```powershell
Set-Location C:\classwork\week04\ollama_client
Copy-Item .env.example .env
uv sync
uv run python config.py
uv run python chat.py --prompt "uv가 무엇인지 두 문장으로 설명해 줘." --tag first
uv run python stream.py --prompt "MIT 라이선스와 GPL의 차이를 표로 정리해 줘."
uv run python chat.py --host http://localhost:11435 --prompt "안녕"   # 연결 실패 재현
uv run python chat.py --model no-such-model --prompt "안녕"           # 모델 없음 재현
$LASTEXITCODE                                                        # 종료 코드 확인
```

3교시(커스텀 모델):

```powershell
Set-Location C:\classwork\week04\ollama_client
ollama create student01-helper -f Modelfile
ollama list
uv run python chat.py --model student01-helper --prompt "uv가 무엇인지 두 문장으로 설명해 줘." --tag helper-1
```

`Modelfile` 머리의 예시 이름은 `osa-helper`다. 공용 PC에서는 `student01-helper`처럼 자기 표시 이름을 붙여 겹치지 않게 한다. 같은 이름으로 다시 `create`하면 덮어쓴다.

`uv run`은 `.venv`가 없으면 만들고 의존성을 설치한다. 수업 전에 `uv sync`를 한 번 실행해 두면 실습 중 네트워크가 필요 없다.

## 관찰 지점

1. `ollama list`의 SIZE(파일)와 `ollama ps`의 SIZE(메모리)가 다르다. 차이는 컨텍스트(KV 캐시)와 실행 버퍼다.
2. `/set verbose`의 `eval rate`와 `chat.py`가 계산한 `tokens_per_second`는 같은 식(`eval_count / eval_duration`)이다.
3. 같은 명령을 두 번 실행하면 두 번째의 `load_seconds`가 0에 가깝다. 모델이 이미 메모리에 있기 때문이다.
4. `stream.py`의 조각은 `done:false` 줄이고 메타는 `done:true` 마지막 줄에만 있다. `first_piece_seconds`가 체감 지연이다.
5. `--num-predict 32`로 줄이면 `done_reason`이 `length`가 된다.
6. 연결 실패는 종료 코드 2, 모델 없음은 3이다. 스택 트레이스 대신 한 문장이 나온다.
7. `ollama create` 뒤 `ollama list`의 SIZE는 기준 모델과 같아 보인다. 가중치 blob을 공유한다.
8. 요청 JSON의 `options`는 Modelfile의 `PARAMETER`보다 우선한다.

## GPU 없을 때·네트워크 없을 때

- GPU가 없거나 인식되지 않으면 `OLLAMA_MODEL=qwen3:0.6b`로 바꾸고, `--num-predict 128`로 줄여 시간을 아낀다. `ollama ps`의 PROCESSOR가 `CPU`로 표시되는 것 자체가 기록할 관찰이다.
- Modelfile의 `FROM`도 캐시된 소형 모델 이름으로 바꾼다. `FROM`에 적은 이름이 캐시에 없으면 `ollama create`가 다운로드를 시도한다.
- 네트워크가 없어도 모델과 `uv sync`가 수업 전에 준비되어 있으면 모든 실습이 오프라인으로 진행된다. 실습 중 `ollama pull`을 실행하지 않는다.
- Ollama 서버가 시작되지 않으면 1교시 보고서의 `ollama show`·`ollama list` 항목은 강의자가 배포하는 기준 PC 측정값으로 채우고, 2교시 실패 경로(연결 실패 메시지)를 먼저 확인한다.

## 복사 후 변형

- `chat.py`에 `--seed` 옵션을 추가한다(2교시 문제 2). `options`에 `seed`를 넣으면 같은 temperature에서 같은 표본 순서를 얻는다.
- `Modelfile`의 `SYSTEM`은 한 번에 한 줄만 바꾸고 같은 이름으로 다시 `ollama create`한다. 같은 이름은 덮어써진다.
- 만든 커스텀 모델은 실습이 끝나면 `ollama rm <이름>`으로 정리해도 된다. 기준 모델은 남는다.
- `outputs/`는 커밋하지 않는다. 증거로 낼 JSON 2~3개는 과제 저장소의 `evidence/`에 복사한다.
- 1차 종합과제에서는 `chat.py`·`stream.py`의 `build_payload()`·오류 처리·저장 로직을 3주차 `oss_tool`의 `chat`·`stream` 서브커맨드로 옮긴다. `config.py`는 3주차 것과 우선순위 규칙이 같으므로 하나만 남긴다.

## 기본값과 환경 기준표

| 환경변수 | 기본값 | 용도 |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama 서버 |
| `OLLAMA_MODEL` | `qwen3:4b` | 기본 생성 모델(RTX 4070 기준). CPU 대체는 `qwen3:0.6b` |
| `OLLAMA_TIMEOUT` | `180` | HTTP 제한 시간(초) |

모델 ID·양자화·용량은 [학기별 환경 기준표](../../../../environment_baseline_template.md)에서 확정하며 위 값은 교재 검증용 기본값이다. `uv.lock`은 만들지 않았다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
