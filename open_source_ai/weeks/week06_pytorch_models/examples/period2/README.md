# 6주차 2교시 — 소형 MLP 학습 루프와 과적합

**역할: 2교시 MLP 학습 참조 구현과 1교시 텐서 코드.** [실습지의 2교시](../../lab.md#2교시-실습--소형-mlp-학습-루프와-과적합)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 문제 1, 기준 학습·step 계산 | `train_loop.py`의 Dataset·DataLoader·train | `outputs/train-*.json`의 config/history |
| 문제 2, 과적합·seed·실패 | `train_loop.py`의 summarize·옵션 | `overfit_note.md`·summary |
| 앞 교시 장치 대조 | `tensor_basics.py`, `runlog.py` | 동일한 device·seed 기준 |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week06_pytorch_models\examples"
$dst = "$HOME\osa-practice\week06"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period2")) { Copy-Item -Recurse "$src\period2" "$dst\period2" }
Set-Location "$dst\period2"
uv sync                    # 수업 전에 설치·캐시한다
```

Python 명령은 현재 `period2` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 2교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | 학습 루프는 다섯 줄의 반복이다 |
| 3–6분 | Dataset과 DataLoader |
| 6–9분 | 손실 함수와 옵티마이저 |
| 9–12분 | epoch · batch · train/val 분리 |
| 12–15분 | 과적합 신호 (예시 수치) |
| 15–17분 | seed 고정과 곡선 기록 |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#2교시-실습--소형-mlp-학습-루프와-과적합)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 기본 설정의 val loss 최저 epoch과 400 epoch 곡선 모양 예상 |
| 기준 실행 | 4–10분 | 기본 실행, epoch 표와 요약 읽기, 1 epoch의 step 수 계산 |
| 과적합 재현 | 10–19분 | 긴 epoch·큰 모델로 실행, 최저·마지막 값 표, 과적합 시점 문장 |
| seed·실패 | 19–25분 | seed를 바꿔 재실행 비교, `--val-ratio 0` 실패 경로 |
| 검증·기록 | 25–30분 | `overfit_note.md` 완성, `evidence/` 복사 |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
uv run python train_loop.py
uv run python train_loop.py --epochs 400 --hidden 128 --tag overfit
uv run python train_loop.py --epochs 400 --hidden 128 --tag overfit-seed7 --seed 7
uv run python train_loop.py --val-ratio 0
$LASTEXITCODE
```

## 예상 결과와 완료 확인

스크립트가 만든 합성 데이터로 train/val loss·accuracy와 summary를 기록한다. 긴 epoch의 최저·마지막 val loss, seed별 차이를 비교한다. `--val-ratio 0`은 실패하며 이유를 출력한다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

실습지 문제 2의 hidden·epoch·seed를 한 조건씩 바꾸어 최저 epoch와 과적합 신호를 적는다. 확장의 early stopping은 기본 실습 뒤 직접 구현한다.

## CPU·네트워크 대체 경로

모델·외부 데이터 다운로드가 필요 없다. GPU가 없으면 `--device cpu`를 명시한다. 시간이 부족한 CPU는 실습지 대체 경로처럼 epoch을 줄이고 바꾼 값을 기록한다. 패키지 사전 설치가 끝났으면 오프라인 진행이 가능하다.
