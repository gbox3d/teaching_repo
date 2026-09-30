# 10주차 2교시 — 수업 도우미 말투로 LoRA 학습하기

[실습지 2교시](../../lab.md#2교시-실습--수업-도우미-말투로-lora-학습하기)에 대응하는 **누적 참조 구현**이다. 이전 교시 코드·입력은 이 폴더에 실제로 들어 있고, 이후 교시 실행 파일은 아직 없다. 모델·개인 실행 결과·어댑터는 포함하지 않는다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–4분 | loss·마스킹 예상 | `data/sample_sft.jsonl` |
| 4–10분 | 토큰·라벨과 짧은 길이 경계 | `train_lora.py --inspect`, `common.py` |
| 10–24분 | run-001 학습 | `train_lora.py`, `data/sample_sft.jsonl` |
| 24–30분 | 어댑터·loss·VRAM 확인 | `adapters/run-001/`, `outputs/train-run-001.json` |

## 이전 산출물과 실행 위치

교재의 이 폴더 전체를 개인 `C:\classwork\week10\period2`에 복사한다. 다른 period의 가상환경을 복사하지 않고 이 폴더에서 `uv sync`한다. 패키지·모델은 수업 전에 준비한다.

1교시의 `outputs/setup-*.md`와 개인 예측표·`.env`를 이어받는다. setup 코드도 포함되어 다시 확인할 수 있다. 예측을 못 했다면 실측 기록에 “예측 없음”이라고 적는다.

## 실행 순서

복사·`.env` 생성·이전 산출물 전달은 **새 실습 폴더에서 최초 1회만** 한다. 이미 작업 중이면 이 명령들을 생략하고 실행 위치 확인부터 이어간다. 기존 개인 코드·설정·결과를 덮어쓰지 않는다. 새 period의 누적 코드와 개인 변경은 비교하여 필요한 수정만 옮긴다.

```powershell
Set-Location C:\classwork\week10\period2
if (-not (Test-Path .env)) { Copy-Item ..\period1\.env .env }
if ((Test-Path ..\period1\outputs) -and -not (Test-Path outputs)) { Copy-Item -Recurse ..\period1\outputs outputs }
New-Item -ItemType Directory -Force outputs | Out-Null
uv sync
uv run python train_lora.py --inspect
uv run python train_lora.py --inspect --max-len 32
uv run python train_lora.py --run-name run-001
```

1교시 폴더가 없으면 `.env.example`을 `.env`로 복사하고 setup 출력 복사는 생략한다.

## 예상 출력과 완료 확인

마스킹 토큰과 답변 토큰을 확인한다. 학습 후 `adapters/run-001`의 설정·가중치·run_config, `outputs/train-run-001.json`의 loss 이력·시간·최대 VRAM을 확인하고 1교시 예측과 비교한다.

## 대체 경로

CPU는 학습 명령에 `--device cpu --max-steps 5 --batch-size 1 --max-len 256`을 붙인다. 목적은 저장과 기록 흐름 확인이며 loss 하락·형식 향상을 보장하지 않는다. 캐시가 없으면 다운로드 없이 준비를 확인한다.

옵션별 변형·실패 경로·확장은 실습지를 따른다. 모델 ID·revision·장치·조건을 기록하고 실행하지 않은 수치를 만들지 않는다. `.venv/`·`.env`·`outputs/`·가중치는 제외하고, 검증한 기록을 증거 폴더에 골라 보관한다. 현재 원본에는 lock이 없으며 학기 기준 확정 후 기준 PC에서 생성·검증해 배포한다.
