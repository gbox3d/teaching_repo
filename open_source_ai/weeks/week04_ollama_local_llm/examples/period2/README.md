# 4주차 2교시 — REST API로 대화하고 실패를 다루기

처음에는 [Python 라이브러리 실습](../../python_library.md)을 따른다. `hello.py`로 첫 답을 받고 `prompt_chat.py`로 시스템·사용자 프롬프트를 비교한다. 아래 REST API·메타 측정은 이후 선택 심화다.

**역할: 2교시 실습 시작 코드와 1교시 기록 도우미 (`--seed`는 문제 2에서 직접 추가).** [실습지의 2교시](../../lab.md#2교시-실습--rest-api로-대화하고-실패를-다루기)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 문제 1, 응답·메타·스트리밍 | `chat.py`, `stream.py`, `ollama_api.py` | `outputs/chat-*.json`, `outputs/stream-*.json` |
| 준비·문제 2, 설정·실패·seed 추가 | `config.py`, `.env.example`, `chat.py` | `failures.md`, `temperature_compare.md` |
| 1교시까지의 실습 참고 | `ollama_probe.ps1`, `model_report_template.md` | 모델 비교 기록 |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week04_ollama_local_llm\examples"
$dst = "C:\classwork\week04"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period2")) { Copy-Item -Recurse "$src\period2" "$dst\period2" }
Set-Location "$dst\period2"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync                    # 수업 전에 설치·캐시한다
if (-not (Test-Path ..\model_report.md)) { Copy-Item model_report_template.md ..\model_report.md }
```

Python 명령은 현재 `period2` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 2교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | 이어받는 것: 서버는 살아 있는가 |
| 3–6분 | `/api/generate`와 `/api/chat` |
| 6–9분 | 메시지 역할과 이력 |
| 9–12분 | 스트리밍: 줄 단위 JSON |
| 12–15분 | options와 think |
| 15–17분 | 응답 메타와 실패 두 가지 |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#2교시-실습--rest-api로-대화하고-실패를-다루기)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 첫 호출과 둘째 호출의 시간 차이, 실패 두 가지의 메시지·종료 코드 예상 |
| chat.py·메타 읽기 | 5–12분 | 실행 → JSON에서 `eval_count`·`eval_duration` 찾아 tokens/s 손계산 |
| stream.py·실패 경로 | 12–19분 | 스트리밍 관찰 → 포트 오류·모델 이름 오류 재현 |
| seed 추가·temperature 비교 | 19–25분 | `--seed` 옵션 구현 → temperature 0과 1을 각 2회 |
| 검증·기록 | 25–30분 | 실패 메시지 2건, 비교 문단, `outputs/` 확인 |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
uv run python config.py
uv run python chat.py --prompt "uv가 무엇인지 두 문장으로 설명해 줘." --tag first
uv run python chat.py --prompt "uv가 무엇인지 두 문장으로 설명해 줘." --tag second
uv run python stream.py --prompt "MIT 라이선스와 GPL의 차이를 표로 정리해 줘."
uv run python chat.py --prompt "오픈소스의 정의를 설명해 줘." --num-predict 32 --tag short
uv run python chat.py --host http://localhost:11435 --prompt "안녕"
$LASTEXITCODE
uv run python chat.py --model no-such-model --prompt "안녕"
$LASTEXITCODE
```

## 예상 결과와 완료 확인

정상 호출은 답과 메타를 JSON에 저장한다. tokens/s는 `eval_count / (eval_duration / 1e9)`로 검산한다. 연결 실패는 종료 코드 2, 모델 없음은 3이다. 스트리밍 결과의 `final_chunk`에서 최종 메타를 읽는다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

실습지 문제 2의 `--seed`를 먼저 구현한다. 그 뒤 같은 프롬프트로 temperature 0·1을 각각 두 번 실행해 비교한다. 아래 명령은 구현 뒤에만 통과한다.

```powershell
uv run python chat.py --prompt "MIT 라이선스와 GPL의 차이를 표로 정리해 줘." --temperature 0 --seed 7 --tag t0a --show-request
```

## CPU·네트워크 대체 경로

GPU가 없으면 `.env`의 `OLLAMA_MODEL`을 캐시된 `qwen3:0.6b`로 바꾼다. Ollama 서버는 로컬에 켜져 있어야 한다. 네트워크 없이 진행하려면 의존성·모델을 수업 전에 캐시하고 `uv sync --offline`으로 확인한다.
