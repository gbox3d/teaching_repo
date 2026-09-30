# 12주차 3교시 — Docker와 재현 절차

[해당 실습 단계·문제·완료 조건](../../lab.md#3교시-실습--dockerfile과-재현-절차-검증) · [교시별 색인](../README.md)

2교시 API·UI에 Dockerfile, 이미지 제외 규칙과 재현 점검 스크립트를 더한 **누적 참조 구현**이다. README 실행 절과 과제 점검표는 실습에서 실제 검증 결과로 작성한다.

## 시간별 파일 대응

| 실습 시간 | 단계 | 이 폴더의 파일·경로 | 확인할 증거 |
|---|---|---|---|
| 0–4분 | 레이어 예상 | `Dockerfile` | 재빌드 레이어 예상 |
| 4–9분 | 외부 설정 | `reproduce_check.ps1`, `.gitignore`, `.dockerignore` | 필수 파일·비밀·실행 경로 점검 |
| 9–20분 | 포장·실행 | `Dockerfile` 또는 `pyproject.toml`, `smoke_test.py` | Docker 또는 깨끗한 uv 환경 |
| 20–26분 | 짝 검증 | 이 폴더 `README.md`의 실행 절 | 막힌 줄·이유·반영 여부 |
| 26–30분 | 과제 점검 | `../../assignment_brief.md` → 개인 `assignment3_checklist.md` | 모든 항목 O/X와 근거 |

파일명이 짧게 적힌 경우 바로 앞 열의 같은 하위 폴더를 기준으로 읽는다. 시간과 완료 조건은 연결된 실습지를 따른다.

## 실행 위치와 명령

이 `period3/` 폴더를 개인 실습 공간에 **처음 한 번 폴더째** 복사하고 그 안에서 실행한다. 숨김 파일도 포함한다. 이미 개인 교시 폴더가 있으면 다시 복사하지 않고 이어 한다. `.env`와 작성한 기록도 새 양식으로 덮어쓰지 않는다. 실제 준비 명령은 위 실습지 링크를 따른다. Python 명령은 `pyproject.toml` 옆에서 실행한다. `uv.lock`·`.venv/`는 배포하지 않았으므로 최초 `uv sync`로 개인 환경을 만든다.

```powershell
uv sync
.\reproduce_check.ps1
# Docker가 없는 경로: 이 폴더의 소스만 복사한 새 폴더에서
uv run uvicorn app.main:app --port 8001
# 다른 터미널
uv run python smoke_test.py --api http://localhost:8001 --skip-stream
```

## 기본 실행과 실습 후 검증

필수 파일과 제외 규칙이 확인되고, 깨끗한 환경에서 /health 및 /chat을 재현한다. Docker 경로는 lab 문제 1의 build/run 명령을 따른다. 응답이 degraded이면 연결 원인을 기록한다.

## 이전 산출물과 다음 단계

개인 2교시 app/·ui/를 이 폴더에 옮겨 GET /models 및 수정한 ERROR_HINTS를 보존한다. outputs는 검증 기록으로 따로 이어받고 .venv는 복사하지 않는다.

## 대체 경로

Docker가 없거나 호스트 Ollama 연결 정책을 바꿀 수 없으면 lab 경로 B(깨끗한 uv 환경)를 수행한다. Docker 부분은 시연과 레이어 설명으로 기록한다.
