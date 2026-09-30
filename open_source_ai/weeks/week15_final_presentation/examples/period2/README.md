# 15주차 2교시 — 교차 재현 검증

[해당 실습 단계·문제·완료 조건](../../lab.md#2교시-실습--교차-재현-검증) · [교시별 색인](../README.md)

발표 카드에 **교차 검증 도구와 리뷰 체크리스트**를 추가했다. 코드·설치 환경은 이 폴더 안에 모두 있으며 다른 period를 import하지 않는다. 이전 발표 기록은 사람이 이어받는다.

## 시간별 파일 대응

| 실습 시간 | 단계 | 이 폴더의 파일·경로 | 확인할 증거 |
|---|---|---|---|
| 0–4분 | README 예상 | 대상 팀 README, `reviewer_checklist.md` | 예상 결과·실패 지점 |
| 4–14분 | clone·실행 | `cross_review.ps1` | 태그·동기화·핵심 기능 |
| 14–22분 | 테스트·문서·비밀 | `verify_release.py`, `checks.py` | FAIL/WARN·라이선스 대조 |
| 22–30분 | 분류·보고 | `reviewer_checklist.md` → `review-team-b.md` | 0~9단계·Issue·실패 분류 |

파일명이 짧게 적힌 경우 바로 앞 열의 같은 하위 폴더를 기준으로 읽는다. 시간과 완료 조건은 연결된 실습지를 따른다.

## 실행 위치와 명령

이 `period2/` 폴더를 개인 실습 공간에 **처음 한 번 폴더째** 복사하고 그 안에서 실행한다. 숨김 파일도 포함한다. 이미 개인 교시 폴더가 있으면 다시 복사하지 않고 이어 한다. `.env`와 작성한 기록도 새 양식으로 덮어쓰지 않는다. 실제 준비 명령은 위 실습지 링크를 따른다. Python 명령은 `pyproject.toml` 옆에서 실행한다. `uv.lock`·`.venv/`는 배포하지 않았으므로 최초 `uv sync`로 개인 환경을 만든다.

```powershell
uv sync
if (-not (Test-Path .\review-team-b.md)) { Copy-Item .\reviewer_checklist.md .\review-team-b.md }
# 파일·Git 상태만 읽는 점검
uv run python verify_release.py --repo C:\classwork\team-b-repo --team team-b
# 수업에서 서로 공개한 팀 저장소를 자동 재현할 때
.\cross_review.ps1 -RepoUrl C:\classwork\team-b-repo -Team team-b -Tag v0.1.0
```

## 기본 실행과 실습 후 검증

outputs/verify-team-b-*.md와 .json, 자동 경로에서는 cross-review 로그가 생긴다. 실제 기능 실행·WARN 판단·0~9단계 기록·Issue 보고는 lab대로 직접 수행한다.

## 이전 산출물과 다음 단계

1교시 presentation_log.md에 적은 대상URL·태그를 사용한다. 체크리스트에서 발표와 실제 출력이 같은지 대조한다.

## 대체 경로

네트워크가 없으면 -RepoUrl에 로컬 저장소 경로를 쓴다. 모델이 없으면 환경 문제로 기록하고 다운받지 않는다. --frozen은 lock 선언 불일치를 검사하지 않으므로 uv lock --check로 별도 진단한다.
