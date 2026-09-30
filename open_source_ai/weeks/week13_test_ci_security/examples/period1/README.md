# 13주차 1교시 — 모델 없는 테스트

[해당 실습 단계·문제·완료 조건](../../lab.md#1교시-실습--가짜-클라이언트로-서비스-테스트-만들기) · [교시별 색인](../README.md)

스키마·서비스·HTTP 계층의 **19개 테스트 시작 코드**다. lab 문제 1의 세 테스트는 학생이 추가한다. workflow·감사·리뷰 파일은 아직 없다.

## 시간별 파일 대응

| 실습 시간 | 단계 | 이 폴더의 파일·경로 | 확인할 증거 |
|---|---|---|---|
| 0–5분 | 기존 검사·예상 | `tests/conftest.py`, `tests/test_*.py` | 19 passed, 2 deselected |
| 5–16분 | 3개 테스트 추가 | `test_schemas.py`, `test_service.py`, `test_api.py` | 실습 후 22 passed, 2 deselected |
| 16–22분 | lint·format | `pyproject.toml`, `tests/` | F401·Would reformat 후 복구 |
| 22–26분 | 느린 테스트 | `tests/test_integration.py`, `.env.example` | RUN_INTEGRATION 없으면 2 skipped |
| 26–30분 | 검증·기록 | 추가 테스트·터미널 출력 | 실습 후 22개 통과와 개인 commit |

파일명이 짧게 적힌 경우 바로 앞 열의 같은 하위 폴더를 기준으로 읽는다. 시간과 완료 조건은 연결된 실습지를 따른다.

## 실행 위치와 명령

이 `period1/` 폴더를 개인 실습 공간에 **처음 한 번 폴더째** 복사하고 그 안에서 실행한다. 숨김 파일도 포함한다. 이미 개인 교시 폴더가 있으면 다시 복사하지 않고 이어 한다. `.env`와 작성한 기록도 새 양식으로 덮어쓰지 않는다. 실제 준비 명령은 위 실습지 링크를 따른다. Python 명령은 `pyproject.toml` 옆에서 실행한다. `uv.lock`·`.venv/`는 배포하지 않았으므로 최초 `uv sync`로 개인 환경을 만든다.

```powershell
uv sync
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
uv run pytest -m integration -q
```

## 기본 실행과 실습 후 검증

배포된 시작 코드는 19 passed, 2 deselected다. 실습의 세 테스트를 추가한 개인 복사본이 22 passed, 2 deselected가 된다. RUN_INTEGRATION을 설정하지 않은 느린 테스트는 2 skipped다.

## 이전 산출물과 다음 단계

12주차 서비스의 오류 응답 관찰을 이어받는다. 이 예제의 요청 필드와 상태 코드 매핑은 lab 설명대로 12주차와 다르다. 2교시에는 개인 테스트·commit을 유지하고 workflow와 의존성 선언만 추가한다.

## 대체 경로

기본 검사는 GPU·Ollama 없이 실행된다. 네트워크가 없으면 사전 준비한 uv 캐시를 사용하고, 실제 통합 테스트는 skipped로 기록한다.
