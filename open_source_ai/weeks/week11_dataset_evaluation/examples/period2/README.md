# 11주차 2교시 — 기준선 vs LoRA 정량 비교

[실습지 2교시](../../lab.md#2교시-실습--기준선-vs-lora-정량-비교)에 대응하는 **누적 참조 구현**이다. 이전 교시 코드·입력은 이 폴더에 실제로 들어 있고, 이후 교시 실행 파일은 아직 없다. 모델·개인 실행 결과·어댑터는 포함하지 않는다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–4분 | 지표·예상표 | `metrics.py`, 실습지 표 |
| 4–10분 | 지표 예시·샘플 2개 채점 | `evaluate.py`, `data/sample_predictions/` |
| 10–22분 | 모델 모드 또는 CPU 소형 실행 | `evaluate.py`, `.env.example` |
| 22–26분 | 자동 지표 오류·겹침 제외 | `outputs/eval-*.json`, `split_report.json` |
| 26–30분 | 비교표·증거 보관 | `evidence/week11/` |

## 이전 산출물과 실행 위치

교재의 이 폴더 전체를 개인 `C:\classwork\week11\period2`에 복사한다. 다른 period의 가상환경을 복사하지 않고 이 폴더에서 `uv sync`한다. 패키지·모델은 수업 전에 준비한다.

1교시 `outputs/`(split과 보고서), `DATA_CARD.md`, `.env`를 복사한다. 10주차 어댑터 경로는 `.env`의 `LORA_ADAPTER_DIR`에 적는다. 앞 교시 코드·데이터가 포함되어 산출물이 없으면 재생성할 수 있다.

## 실행 순서

복사·`.env` 생성·이전 산출물 전달은 **새 실습 폴더에서 최초 1회만** 한다. 이미 작업 중이면 이 명령들을 생략하고 실행 위치 확인부터 이어간다. 기존 개인 코드·설정·결과를 덮어쓰지 않는다. 새 period의 누적 코드와 개인 변경은 비교하여 필요한 수정만 옮긴다.

```powershell
Set-Location C:\classwork\week11\period2
if ((Test-Path ..\period1\outputs) -and -not (Test-Path outputs)) { Copy-Item -Recurse ..\period1\outputs outputs }
if ((Test-Path ..\period1\DATA_CARD.md) -and -not (Test-Path DATA_CARD.md)) { Copy-Item ..\period1\DATA_CARD.md DATA_CARD.md }
if (-not (Test-Path .env)) {
    if (Test-Path ..\period1\.env) { Copy-Item ..\period1\.env .env } else { Copy-Item .env.example .env }
}
New-Item -ItemType Directory -Force outputs | Out-Null
uv sync
uv run python metrics.py --demo
uv run python evaluate.py --predictions data/sample_predictions/base.json data/sample_predictions/lora.json
# 모델·어댑터가 준비된 PC에서 실습지 문제 2 수행
uv run python evaluate.py
```

## 예상 출력과 완료 확인

샘플 채점은 `outputs/eval-*.json`과 표를 만든다. 가상 출력은 모델 실측과 구분한다. 형식 통과·내용 오류와 반대 사례를 찾고 contamination id를 제외한 지표도 비교한다.

## 대체 경로

앞 결과가 없으면 로컬 `clean.py → pii_check.py → split.py`를 실행한다. GPU·어댑터·모델이 없으면 샘플 채점과 겹침 제외를 진행하고 모델 미실행을 적는다. CPU 모델은 `--device cpu --limit 5 --max-new-tokens 96`이다.

옵션별 변형·실패 경로·확장은 실습지를 따른다. 모델 ID·revision·장치·조건을 기록하고 실행하지 않은 수치를 만들지 않는다. `.venv/`·`.env`·`outputs/`·가중치는 제외하고, 검증한 기록을 증거 폴더에 골라 보관한다. 현재 원본에는 lock이 없으며 학기 기준 확정 후 기준 PC에서 생성·검증해 배포한다.
