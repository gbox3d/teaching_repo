# 8주차 1교시 — 모의 실기 A 프로젝트 복구와 판별 문항

공개 모의 실기 A의 **시작 자료**다. `broken_project`의 의도적 오류와 가짜 `.env` 이력을 그대로 재현하며, 복구된 정답은 제공하지 않는다.

기준: [실습지의 1교시](../../lab.md#1교시-실습--모의-실기-a-프로젝트-복구와-판별-문항). 아래 시간은 실습 30분의 구간이며, 설명 20분·휴식 10분은 기존 시간표를 따른다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–5분 | A 요구사항·오류 순서 예상 | `tasks_A.md` |
| 5–17분 | 프로젝트 복구 | `make_broken_repo.ps1`, `broken_project/` |
| 17–24분 | 라이선스·Git 판별 | `tasks_A.md` A-2·A-3 |
| 24–30분 | 실행·추적 확인, 답안 기록 | 개인 복사본 `report.py`, `answers_A.md` |

## 이전 산출물과 시작 위치

이전 교시 산출물은 필요 없다. 교재의 `examples/period1`에서 준비 스크립트를 실행하면 개인 폴더에 별도 Git 저장소가 생긴다. 이미 같은 대상이 있으면 새 이름을 사용한다.

## 실행 순서

복사·`.env` 생성·이전 산출물 전달은 **새 실습 폴더에서 최초 1회만** 한다. 이미 작업 중이면 이 명령들을 생략하고 실행 위치 확인부터 이어간다. 기존 개인 코드·설정·결과를 덮어쓰지 않는다. 새 period의 누적 코드와 개인 변경은 비교하여 필요한 수정만 옮긴다.

```powershell
.\make_broken_repo.ps1 -Destination $HOME\osa-practice\week08-mock-a
Set-Location $HOME\osa-practice\week08-mock-a
uv sync
# 오류를 tasks_A.md에 따라 직접 복구한 뒤
uv run python report.py
git ls-files
```

## 예상 출력과 완료 확인

첫 `uv sync`의 실패는 문제의 일부다. 복구 후 `outputs/report.json`, `.gitignore`, `.env.example`, 복구 기록 3개 이상과 판별 답안을 확인한다. `.env`의 과거 이력은 삭제 commit만으로 없어지지 않는다는 판단도 적는다.

## 대체 경로

Ollama가 없어도 연결 실패를 보고서에 기록하며 진행할 수 있다(종료 코드 2). 실행 정책 오류는 실습지의 일회 실행 방법을 따른다. 원본 broken_project에 `.gitignore`나 고친 manifest를 추가하지 않는다.

실측 결과·답안은 개인 실습 폴더에 기록한다. 실제 비밀정보와 환경 폴더를 공개하지 않는다. 학기 기준이 정해지면 기준 PC에서 생성·검증한 lock을 배포하며, 현재 원본에는 lock을 넣지 않았다.
