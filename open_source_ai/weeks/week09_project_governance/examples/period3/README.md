# 9주차 3교시 — 팀 저장소와 이슈 분해

팀 저장소의 **시작 템플릿**, 마일스톤·Issue **계획 양식과 검사 도구**다. 1·2교시 도구를 누적하고 이번 교시용 저장소·Issue 파일을 추가했다.

기준: [실습지의 3교시](../../lab.md#3교시-실습--팀-저장소와-이슈-분해). 아래 시간은 실습 30분의 구간이며, 설명 20분·휴식 10분은 기존 시간표를 따른다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–5분 | 마일스톤 3개·Issue 후보 | `milestone_plan_template.md` |
| 5–12분 | 팀 저장소·거버넌스·doctor | `project_template/` |
| 12–22분 | Issue 8~10개 검사·등록 | `issue_plan.sample.json`, `issue_plan_check.py`, `issue_plan_push.py` |
| 22–27분 | 3분 리허설 | `proposal_rubric.md`, `rehearsal_template.md` |
| 27–30분 | URL·Issue·리허설 기록 | 팀 저장소 `docs/` |

## 이전 산출물과 시작 위치

1교시 조사표와 2교시 제안서를 이어받는다. `period3`을 `C:\classwork\week09\period3`에 복사한다. 팀 저장소용 `project_template`는 별도로 `C:\classwork\week09\team-repo`에 복사하고 Git을 초기화한다. 교재 원본에 git init하지 않는다.

## 실행 순서

복사·`.env` 생성·이전 산출물 전달은 **새 실습 폴더에서 최초 1회만** 한다. 이미 작업 중이면 이 명령들을 생략하고 실행 위치 확인부터 이어간다. 기존 개인 코드·설정·결과를 덮어쓰지 않는다. 새 period의 누적 코드와 개인 변경은 비교하여 필요한 수정만 옮긴다.

```powershell
Set-Location C:\classwork\week09\period3
if (-not (Test-Path C:\classwork\week09\team-repo)) { Copy-Item -Recurse project_template C:\classwork\week09\team-repo }
if (-not (Test-Path issue_plan.json)) { Copy-Item issue_plan.sample.json issue_plan.json }
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync
uv run python issue_plan_check.py --plan issue_plan.json
uv run python issue_plan_push.py --plan issue_plan.json --repo team-a/team-a-local-helper --dry-run
Set-Location C:\classwork\week09\team-repo
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv run team-project doctor
```

계획은 팀 값으로 바꾼다. 실제 GitHub 등록은 실습지 순서로 `--dry-run` 결과를 확인한 뒤 진행한다. `docs/proposal.md`와 `docs/milestones.md`에 이전 산출물을 옮긴다.

## 예상 출력과 완료 확인

`outputs/issue_plan_report.md` 경고 0개, 팀 저장소 `outputs/doctor-*.json`, GitHub의 마일스톤 3개·Issue 8~10개, `docs/rehearsal.md`의 소요 시간·빠진 항목·예상 질문 2개를 확인한다.

## 대체 경로

GitHub 등록 권한·토큰이 없으면 브라우저로 등록한다. doctor는 Ollama가 없어도 연결 실패 사유를 남겨야 한다. 모델 다운로드는 하지 않는다.

실측 결과·답안은 개인 실습 폴더에 기록한다. 실제 비밀정보와 환경 폴더를 공개하지 않는다. 학기 기준이 정해지면 기준 PC에서 생성·검증한 lock을 배포하며, 현재 원본에는 lock을 넣지 않았다.
