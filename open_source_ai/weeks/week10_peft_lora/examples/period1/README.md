# 10주차 1교시 — 어댑터 붙이고 학습 파라미터 세기

[실습지 1교시](../../lab.md#1교시-실습--어댑터-붙이고-학습-파라미터-세기)에 대응하는 **누적 참조 구현**이다. 이전 교시 코드·입력은 이 폴더에 실제로 들어 있고, 이후 교시 실행 파일은 아직 없다. 모델·개인 실행 결과·어댑터는 포함하지 않는다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–5분 | rank별 예상 | 개인 예상표 |
| 5–13분 | 기본 설정·파라미터 수 | `lora_setup.py`, `common.py`, `.env.example` |
| 13–22분 | target·길이·배치 변형 | `lora_setup.py` 옵션 |
| 22–30분 | VRAM 예측·오류 관찰 | `outputs/setup-*.md`, 개인 예측표 |

## 이전 산출물과 실행 위치

교재의 이 폴더 전체를 개인 `C:\classwork\week10\period1`에 복사한다. 다른 period의 가상환경을 복사하지 않고 이 폴더에서 `uv sync`한다. 패키지·모델은 수업 전에 준비한다.

9주차 제안서의 모델 후보를 이어받는다. 이전 교시 출력은 필요 없다. 학습 데이터·학습 코드·비교 코드는 2·3교시에 추가된다.

## 실행 순서

복사·`.env` 생성·이전 산출물 전달은 **새 실습 폴더에서 최초 1회만** 한다. 이미 작업 중이면 이 명령들을 생략하고 실행 위치 확인부터 이어간다. 기존 개인 코드·설정·결과를 덮어쓰지 않는다. 새 period의 누적 코드와 개인 변경은 비교하여 필요한 수정만 옮긴다.

```powershell
Set-Location C:\classwork\week10\period1
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync
uv run python lora_setup.py --ranks 4,8,16
uv run python lora_setup.py --ranks 8 --target-modules q_proj,v_proj
uv run python lora_setup.py --ranks 8 --seq-len 256
uv run python lora_setup.py --ranks 8 --batch-size 1
```

## 예상 출력과 완료 확인

`outputs/setup-*.md`·JSON에 세 rank의 학습 파라미터·비율과 VRAM 예측이 생긴다. r 비례 관계, 줄인 target의 변화, 12 GB 판정과 2교시 실측값 빈 칸을 남긴다.

## 대체 경로

GPU가 없으면 CPU로 파라미터를 센다. 느리면 `--ranks 8` 하나만 실측하고 다른 행은 계산값임을 적는다. 캐시가 없으면 실습 중 모델을 내려받지 않고 강의자에게 준비 상태를 확인한다.

옵션별 변형·실패 경로·확장은 실습지를 따른다. 모델 ID·revision·장치·조건을 기록하고 실행하지 않은 수치를 만들지 않는다. `.venv/`·`.env`·`outputs/`·가중치는 제외하고, 검증한 기록을 증거 폴더에 골라 보관한다. 현재 원본에는 lock이 없으며 학기 기준 확정 후 기준 PC에서 생성·검증해 배포한다.
