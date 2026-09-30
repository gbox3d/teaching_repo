# 8주차 2교시 — 모의 실기 B 클라이언트 기능 추가와 결과 해석

공개 모의 실기 B의 **기능 추가 시작 코드와 해석용 fixture**다. `chat.py`의 `TODO(B-1)`은 학생이 채우며, 완성 답안은 포함하지 않는다.

기준: [실습지의 2교시](../../lab.md#2교시-실습--모의-실기-b-클라이언트-기능-추가와-결과-해석). 아래 시간은 실습 30분의 구간이며, 설명 20분·휴식 10분은 기존 시간표를 따른다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–5분 | 요구사항과 원본 1회 실행 | `tasks_B.md`, `client_starter/` |
| 5–18분 | system·응답 메타 기능 추가 | `client_starter/chat.py` |
| 18–24분 | pipeline 출력 해석 | `fixtures/pipeline_output.json` |
| 24–30분 | 실패 2종·답안 확인 | `check_env.py`, 개인 `answers_B.md` |

## 이전 산출물과 시작 위치

1교시 답안을 이어받지 않아도 시작할 수 있다. `examples/period2`에서 `client_starter`를 개인 `week08-mock-b`로 복사한다. 모델은 사전 캐시본만 사용한다.

## 실행 순서

복사·`.env` 생성·이전 산출물 전달은 **새 실습 폴더에서 최초 1회만** 한다. 이미 작업 중이면 이 명령들을 생략하고 실행 위치 확인부터 이어간다. 기존 개인 코드·설정·결과를 덮어쓰지 않는다. 새 period의 누적 코드와 개인 변경은 비교하여 필요한 수정만 옮긴다.

```powershell
if (-not (Test-Path $HOME\osa-practice\week08-mock-b)) { Copy-Item -Recurse .\client_starter $HOME\osa-practice\week08-mock-b }
Set-Location $HOME\osa-practice\week08-mock-b
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync
uv run python check_env.py
uv run python chat.py --prompt "uv sync 가 하는 일을 한 문장으로 설명하라."
```

`tasks_B.md`를 따라 기능을 추가한 뒤 같은 prompt로 system 유무 2회를 비교한다. `--model nonexistent-model`과 `--host http://localhost:1`로 두 실패를 구분한다.

## 예상 출력과 완료 확인

시작 코드는 기본 응답만 저장한다. 실습 후 JSON에 응답 메타·tokens_per_sec가 들어가야 한다. fixture는 자체 작성 샘플이며 실제 추론 성능으로 보고하지 않는다.

## 대체 경로

GPU가 없으면 사전 캐시한 소형 모델을 쓴다. 서버가 없으면 구현과 fixture 해석을 먼저 하고 모델 실행 확인은 가능한 PC에서 한다. 없는 실행 결과를 답안에 쓰지 않는다.

실측 결과·답안은 개인 실습 폴더에 기록한다. 실제 비밀정보와 환경 폴더를 공개하지 않는다. 학기 기준이 정해지면 기준 PC에서 생성·검증한 lock을 배포하며, 현재 원본에는 lock을 넣지 않았다.
