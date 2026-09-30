# 12주차 1교시 — 앱 서버와 오류 응답

[해당 실습 단계·문제·완료 조건](../../lab.md#1교시-실습--앱-서버-세우기와-오류-응답-확인) · [교시별 색인](../README.md)

기존 서비스에서 이 교시에 쓰는 비스트리밍 API와 점검 코드를 분리한 **시작 코드**다. `GET /models`는 실습 문제 2에서 직접 추가한다. 스트리밍·UI·Docker 파일은 다음 교시에서 제공한다.

## 시간별 파일 대응

| 실습 시간 | 단계 | 이 폴더의 파일·경로 | 확인할 증거 |
|---|---|---|---|
| 0–5분 | 예상·준비 | `pyproject.toml`, `.env.example`, `app/schemas.py` | 실패 4종 예상표 |
| 5–12분 | 정상 경로 | `app/main.py`, `smoke_test.py` | /health·/chat 응답과 초당 토큰 수 |
| 12–21분 | 실패 4종 | `app/ollama_client.py`, `app/schemas.py` | 502·503·504·422 기록 |
| 21–26분 | GET /models 추가 | `app/main.py` | 목록 또는 502 응답 |
| 26–30분 | 검증·기록 | `outputs/requests.jsonl`, `outputs/smoke-*.json` | 실습 완료 조건 확인 |

파일명이 짧게 적힌 경우 바로 앞 열의 같은 하위 폴더를 기준으로 읽는다. 시간과 완료 조건은 연결된 실습지를 따른다.

## 실행 위치와 명령

이 `period1/` 폴더를 개인 실습 공간에 **처음 한 번 폴더째** 복사하고 그 안에서 실행한다. 숨김 파일도 포함한다. 이미 개인 교시 폴더가 있으면 다시 복사하지 않고 이어 한다. `.env`와 작성한 기록도 새 양식으로 덮어쓰지 않는다. 실제 준비 명령은 위 실습지 링크를 따른다. Python 명령은 `pyproject.toml` 옆에서 실행한다. `uv.lock`·`.venv/`는 배포하지 않았으므로 최초 `uv sync`로 개인 환경을 만든다.

```powershell
uv sync
uv run uvicorn app.main:app --port 8000 --reload
# 다른 터미널도 이 폴더에서
uv run python smoke_test.py
```

## 기본 실행과 실습 후 검증

사전 캐시 모델과 Ollama가 준비되면 /health의 status=ok, /chat은 200과 reply를 반환한다. 실습 후 직접 추가한 /models까지 /docs에서 확인한다. 이 교시 smoke_test.py에는 스트리밍 옵션이 없다.

## 이전 산출물과 다음 단계

11주차 개인 저장소와 캐시 모델을 사용한다. 2교시로 넘어갈 때 이 폴더의 outputs와 본인이 구현한 GET /models를 보존한다.

## 대체 경로

GPU가 없으면 사전 캐시된 CPU 모델로 .env를 바꾼다. 모델·서버가 없으면 502 등 실패 경로까지만 기록하고 정상 응답 완료로 표시하지 않는다.
