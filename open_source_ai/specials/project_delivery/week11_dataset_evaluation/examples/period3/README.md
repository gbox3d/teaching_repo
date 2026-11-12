# 11주차 3교시 — 수동 채점과 실패 분석 보고

[실습지 3교시](../../lab.md#3교시-실습--수동-채점과-실패-분석-보고)에 대응하는 **누적 참조 구현**이다. 이전 교시 코드·입력은 이 폴더에 실제로 들어 있고, 이후 교시 실행 파일은 아직 없다. 모델·개인 실행 결과·어댑터는 포함하지 않는다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–4분 | 채점표 생성·기준 합의 | `make_sheet.py`, `manual_scoring_sheet.md` |
| 4–16분 | 20건 점수·오류·메모 | `outputs/scoring-*.md` |
| 16–21분 | 5건 교차 채점 | 같은 채점표, 실습지 지정 id |
| 21–27분 | 실패 3개·안전·다음 실험 | `FAILURE_ANALYSIS_TEMPLATE.md` |
| 27–30분 | 집계·비교·증거 commit | `DATA_CARD.md`, `FAILURE_ANALYSIS.md`, `evidence/` |

## 이전 산출물과 실행 위치

교재의 이 폴더 전체를 개인 `C:\classwork\week11\period3`에 복사한다. 다른 period의 가상환경을 복사하지 않고 이 폴더에서 `uv sync`한다. 패키지·모델은 수업 전에 준비한다.

2교시 `outputs/`(eval과 1교시 보고서·split), `DATA_CARD.md`, `.env`, `evidence/`를 넘긴다. 이전 결과가 없으면 이 폴더의 누적 코드·샘플로 재생성할 수 있다. 교차 채점할 짝 1명이 필요하다.

## 실행 순서

복사·`.env` 생성·이전 산출물 전달은 **새 실습 폴더에서 최초 1회만** 한다. 이미 작업 중이면 이 명령들을 생략하고 실행 위치 확인부터 이어간다. 기존 개인 코드·설정·결과를 덮어쓰지 않는다. 새 period의 누적 코드와 개인 변경은 비교하여 필요한 수정만 옮긴다.

```powershell
Set-Location C:\classwork\week11\period3
if ((Test-Path ..\period2\outputs) -and -not (Test-Path outputs)) { Copy-Item -Recurse ..\period2\outputs outputs }
if ((Test-Path ..\period2\DATA_CARD.md) -and -not (Test-Path DATA_CARD.md)) { Copy-Item ..\period2\DATA_CARD.md DATA_CARD.md }
if (-not (Test-Path .env)) { Copy-Item ..\period2\.env .env }
if ((Test-Path ..\period2\evidence) -and -not (Test-Path evidence)) { Copy-Item -Recurse ..\period2\evidence evidence }
New-Item -ItemType Directory -Force outputs, evidence\week11 | Out-Null
uv sync
uv run python make_sheet.py --run lora
if (-not (Test-Path FAILURE_ANALYSIS.md)) { Copy-Item FAILURE_ANALYSIS_TEMPLATE.md FAILURE_ANALYSIS.md }
```

## 예상 출력과 완료 확인

채점표는 **빈 채점 양식**이며 점수·오류·메모는 학생이 채운다. 20건 합계, 5건 일치율, 다른 실패 유형 3개와 다음 실험의 수치 기준을 확인한다. 실제 출력이 5건뿐이면 범위를 명시하고 20건 실습은 샘플을 사용한다.

## 대체 경로

어댑터 없는 실제 결과는 `--run base`를 쓴다. eval이 없으면 이 폴더에서 전처리 후 샘플 `--predictions`를 실행한다. 모델로 안전 유도 질문을 확인할 수 없으면 미확인과 사유를 적는다.

옵션별 변형·실패 경로·확장은 실습지를 따른다. 모델 ID·revision·장치·조건을 기록하고 실행하지 않은 수치를 만들지 않는다. `.venv/`·`.env`·`outputs/`·가중치는 제외하고, 검증한 기록을 증거 폴더에 골라 보관한다. 현재 원본에는 lock이 없으며 학기 기준 확정 후 기준 PC에서 생성·검증해 배포한다.
