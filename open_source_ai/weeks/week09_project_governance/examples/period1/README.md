# 9주차 1교시 — 거버넌스 문서 분석표

거버넌스 조사에 쓰는 **분석표 양식과 수치 확인 참조 도구**다. 조사 결과나 팀 규칙의 정답을 채워 놓지 않았다.

기준: [실습지의 1교시](../../lab.md#1교시-실습--거버넌스-문서-분석표). 아래 시간은 실습 30분의 구간이며, 설명 20분·휴식 10분은 기존 시간표를 따른다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–5분 | 문서·수치 예상 | `governance_survey_template.md` |
| 5–11분 | 저장소 1 조사 | GitHub·조사표 |
| 11–17분 | 저장소 2 조사 | GitHub·조사표 |
| 17–24분 | 수치 보강·규칙 3개 | `repo_health.py` |
| 24–30분 | URL 대조·commit | 개인 `governance_survey.md` |

## 이전 산출물과 시작 위치

8주차까지 개인 저장소와 GitHub 로그인, 사전에 정한 팀을 이어받는다. `period1` 전체를 `C:\classwork\week09\period1`에 복사한다. 조사 결과는 그 안의 `governance_survey.md`에 쓰고 개인 저장소에 옮겨 커밋한다.

## 실행 순서

복사·`.env` 생성·이전 산출물 전달은 **새 실습 폴더에서 최초 1회만** 한다. 이미 작업 중이면 이 명령들을 생략하고 실행 위치 확인부터 이어간다. 기존 개인 코드·설정·결과를 덮어쓰지 않는다. 새 period의 누적 코드와 개인 변경은 비교하여 필요한 수정만 옮긴다.

```powershell
Set-Location C:\classwork\week09\period1
if (-not (Test-Path governance_survey.md)) { Copy-Item governance_survey_template.md governance_survey.md }
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync
uv run python repo_health.py
```

## 예상 출력과 완료 확인

두 저장소의 문서·활동 수치와 근거 URL, 가져올 규칙 3개 및 제외할 규칙 1개를 적는다. 스크립트의 `outputs/health-*.json`은 브라우저 관찰과 대조한다.

## 대체 경로

API 제한·네트워크 오류면 브라우저에서 확인 가능한 근거로 표를 채우고 미확인 값은 표시한다. 토큰은 `.env`에만 두며 모델이나 GPU는 필요 없다.

실측 결과·답안은 개인 실습 폴더에 기록한다. 실제 비밀정보와 환경 폴더를 공개하지 않는다. 학기 기준이 정해지면 기준 PC에서 생성·검증한 lock을 배포하며, 현재 원본에는 lock을 넣지 않았다.
