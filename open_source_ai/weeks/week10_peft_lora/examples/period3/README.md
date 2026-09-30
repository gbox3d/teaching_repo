# 10주차 3교시 — 전후 비교와 실험 기록 run-001

[실습지 3교시](../../lab.md#3교시-실습--전후-비교와-실험-기록-run-001)에 대응하는 **누적 참조 구현**이다. 이전 교시 코드·입력은 이 폴더에 실제로 들어 있고, 이후 교시 실행 파일은 아직 없다. 모델·개인 실행 결과·어댑터는 포함하지 않는다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–4분 | 형식 준수·주제 밖 결과 예상 | `data/eval_prompts.json` |
| 4–12분 | 기본·어댑터 동일 조건 비교 | `compare.py`, `common.py` |
| 12–24분 | 실험 기록 7개 절 | `EXPERIMENT_TEMPLATE.md`, 이전 setup·train 출력 |
| 24–30분 | 주제 밖 경계·기록 commit | `compare.py --prompt ... --tag offtopic` |
| 기본 완료 후 | 선택 확장: 병합 | `merge.py` |

## 이전 산출물과 실행 위치

교재의 이 폴더 전체를 개인 `C:\classwork\week10\period3`에 복사한다. 다른 period의 가상환경을 복사하지 않고 이 폴더에서 `uv sync`한다. 패키지·모델은 수업 전에 준비한다.

2교시 `adapters/run-001/`과 `outputs/`(1교시 setup 기록 포함), `.env`를 이 폴더에 복사한다. 실험 기록의 데이터 해시는 실제 학습에 사용한 2교시 파일로 계산한다. `--data`를 바꿨거나 여기서 재학습했다면 해당 실행의 입력 파일을 사용한다. 학습 코드도 누적되어 다시 짧게 학습할 수 있다. `$repo`는 기록을 커밋할 개인 저장소다.

## 실행 순서

복사·`.env` 생성·이전 산출물 전달은 **새 실습 폴더에서 최초 1회만** 한다. 이미 작업 중이면 이 명령들을 생략하고 실행 위치 확인부터 이어간다. 기존 개인 코드·설정·결과를 덮어쓰지 않는다. 새 period의 누적 코드와 개인 변경은 비교하여 필요한 수정만 옮긴다.

```powershell
Set-Location C:\classwork\week10\period3
if (-not (Test-Path .env)) { Copy-Item ..\period2\.env .env }
if ((Test-Path ..\period2\outputs) -and -not (Test-Path outputs)) { Copy-Item -Recurse ..\period2\outputs outputs }
if ((Test-Path ..\period2\adapters) -and -not (Test-Path adapters)) { Copy-Item -Recurse ..\period2\adapters adapters }
New-Item -ItemType Directory -Force outputs, adapters | Out-Null
uv sync
uv run python compare.py --adapter adapters/run-001
$repo = "<개인 저장소 경로>"
New-Item -ItemType Directory -Force "$repo\experiments\run-001" | Out-Null
if (-not (Test-Path "$repo\experiments\run-001.md")) { Copy-Item EXPERIMENT_TEMPLATE.md "$repo\experiments\run-001.md" }
```

## 예상 출력과 완료 확인

`outputs/compare-run-001.md`·JSON에 프롬프트 5개의 기본·어댑터 출력이 생긴다. 개선·악화 근거, 형식 준수 수, 데이터 해시·조건·실패·다음 실험을 적는다. 모델 가중치는 개인 저장소에도 커밋하지 않는다.

## 대체 경로

CPU 비교는 `--device cpu --max-new-tokens 60`을 붙인다. 어댑터가 없으면 이 폴더의 `train_lora.py`로 실습지의 짧은 학습을 하거나 강의자 배포 어댑터를 쓰고 출처를 기록한다.

옵션별 변형·실패 경로·확장은 실습지를 따른다. 모델 ID·revision·장치·조건을 기록하고 실행하지 않은 수치를 만들지 않는다. `.venv/`·`.env`·`outputs/`·가중치는 제외하고, 검증한 기록을 증거 폴더에 골라 보관한다. 현재 원본에는 lock이 없으며 학기 기준 확정 후 기준 PC에서 생성·검증해 배포한다.
