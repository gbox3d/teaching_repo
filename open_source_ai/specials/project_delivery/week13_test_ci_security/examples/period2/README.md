# 13주차 2교시 — GitHub Actions

[해당 실습 단계·문제·완료 조건](../../lab.md#2교시-실습--github-actions로-초록불과-빨간불-만들기) · [교시별 색인](../README.md)

1교시 시작 코드에 **CI 참조 workflow**를 더했다. 실습에서 이미 audit 잡도 관찰하므로 의존성 감사 도구 선언은 이 교시에 포함한다. 감사 보고서·비밀 검색·리뷰 양식은 3교시에서 추가한다.

## 시간별 파일 대응

| 실습 시간 | 단계 | 이 폴더의 파일·경로 | 확인할 증거 |
|---|---|---|---|
| 0–4분 | step 대응 | `.github/workflows/ci.yml` | 5행 대응표 |
| 4–12분 | 저장소·push | 개인 저장소 루트의 `.github/` | Actions 첫 실행 URL |
| 12–19분 | PR·초록불 | `README.md`, workflow | PR URL·캐시·실행 시간 |
| 19–26분 | 빨간불·수정 | `app/service.py`, `tests/test_service.py` | 단위 변환 버그 실패·수정 |
| 26–30분 | 검증·기록 | Actions 로그 | step·첫 오류·테스트 이름 |

파일명이 짧게 적힌 경우 바로 앞 열의 같은 하위 폴더를 기준으로 읽는다. 시간과 완료 조건은 연결된 실습지를 따른다.

## 실행 위치와 명령

실습을 이어갈 때는 [실습지 준비 절](../../lab.md)에 따라 기존 `ci_lab` Git 저장소에 CI 파일을 추가하고 `uv add --dev pip-audit`를 실행한다. 아래 명령도 그 저장소에서 실행한다. 독립 실행을 확인할 때만 이 폴더 전체를 별도 새 폴더로 복사한다. Python 명령은 `pyproject.toml` 옆에서 실행한다. `uv.lock`·`.venv/`는 배포하지 않았으므로 최초 `uv sync`로 개인 환경을 만든다.

```powershell
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

## 기본 실행과 실습 후 검증

폴더만 새로 복사해 실행하면 원본 19개 테스트가 통과한다. lab을 이어가는 개인 저장소는 1교시에 추가한 테스트를 보존하여 22개가 통과해야 한다. 실제 Actions 실행과 PR 상태는 lab의 GitHub 절차로 확인한다.

## 이전 산출물과 다음 단계

기존 개인 ci_lab Git 저장소에 .github/workflows/ci.yml을 추가하고 uv 명령으로 dev 의존성을 갱신한다. pyproject.toml 전체를 덮어쓰지 않는다. app/·tests/·.git/·README와 증거는 덮어쓰지 않는다. .github는 Git 저장소 루트에 있어야 한다.

## 대체 경로

GitHub 연결이 없으면 같은 순서로 로컬 ruff·pytest를 실행해 초록/빨강 출력을 기록한다. Actions URL·PR·merge는 접속 복구 후 수행하며 로컬 결과를 Actions 성공이라고 적지 않는다.
