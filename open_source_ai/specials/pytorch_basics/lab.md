# PyTorch 선택 특강 실습

## 준비

```powershell
uv init --package --python 3.12 --vcs none pytorch-skeleton
```

생성한 `src/`·`pyproject.toml`·`.python-version`을 확인한 뒤 교재 `examples`를 별도 작업 폴더에 복사한다. 정규 주차의 작업 폴더와 구분한다.

```powershell
$src = "<교재 저장소>\open_source_ai\specials\pytorch_basics\examples"
$dst = "C:\classwork\pytorch-special"
New-Item -ItemType Directory -Force "C:\classwork" | Out-Null
Copy-Item -Recurse $src $dst
Set-Location $dst
uv sync
```

명령은 이 루트에서 실행한다. `main()`을 scripts가 명령으로 연결하고 build-system이 패키지 설치 방법을 정한다. scripts 수정 뒤에는 `uv sync`를 다시 실행한다.

## 1교시 실습 — 텐서 연산과 파일 저장

| 시간 | 활동 |
|---|---|
| 0–5분 | 텐서와 저장·복원 흐름 확인 |
| 5–15분 | ex01로 생성·연산·저장 |
| 15–25분 | ex02로 복원, 다른 값으로 반복 |
| 25–30분 | 없는 파일·잘못된 입력 확인, 기록 |

1. `uv run ex01`에서 `2 3`을 입력한다. `+ 1`은 `[3, 4]`, `* 2`는 `[4, 6]`, 합계는 5다.
2. `outputs/tensor.pt`에는 2배 한 결과가 저장된다. `/bye`로 프로그램을 종료한다.
3. `uv run ex02`에서 파일 경로 `outputs/tensor.pt`를 입력한다. `[4, 6]`을 복원하고 1을 더하면 `[5, 7]`이다.
4. ex01에서 `-1 4`를 저장하고 종료한 뒤 ex02로 읽어 마지막 결과 `[-2, 8]`인지 확인한다.
5. `torch.save`·`torch.load` 줄과 파일 위치를 찾는다. shape `(2,)`는 1차원 숫자 두 개, dtype은 숫자 자료형, device는 계산 장치다.
6. 잘못된 숫자와 없는 파일 경로를 입력해 안내 후 계속 입력할 수 있는지 확인한다.

[1교시의 입력·출력 상세 설명](examples/period1/README.md)을 따른다. 완료 조건은 프로그램 종료 후에도 계산 결과가 파일에 남음을 설명하는 것이다.

## 2교시 실습 — 작은 데이터로 회귀 모델 학습

| 시간 | 활동 |
|---|---|
| 0–5분 | CSV의 입력·정답과 예측 목적 읽기 |
| 5–15분 | 기본 학습과 새 시간 두 개 예측 |
| 15–25분 | epoch 한 값만 변경해 비교 |
| 25–30분 | 식·오차·저장 파일 기록 |

1. [study_scores.csv](examples/src/shared/data/study_scores.csv)를 연다. 공부 시간 1~6시간과 가상 연습 점수 6개다. 실제 학생 성적이 아니다.
2. 목표는 숫자 값을 예측하는 회귀다. 모델은 `점수 = 가중치 × 시간 + 편향`인 `nn.Linear(1, 1)`이다.
3. `uv run ex03`에서 첫·마지막 MSE와 학습한 식을 기록한다. MSE는 예측과 정답의 차이를 제곱해 평균한 값이다.
4. `2.5`, `5.5`를 입력하고 예측한 점수를 읽은 뒤 `/bye`로 종료한다.
5. `EPOCHS`만 1000에서 20으로 바꾸고 다시 실행해 MSE·식·예측을 비교한다. 비교 후 1000으로 복원해 최종 모델을 다시 저장한다.
6. 예측 → 손실 계산 → zero_grad → backward → step을 코드와 연결한다. 학습한 가중치는 `outputs/regression.pt`에 저장된다.

완료 조건은 입력과 정답, 회귀식, 손실의 변화와 저장한 모델을 설명하는 것이다.

## 3교시 실습 — 모델을 불러와 예측

| 시간 | 활동 |
|---|---|
| 0–5분 | state_dict와 모델 구조 확인 |
| 5–15분 | 저장 모델로 같은 입력의 예측 비교 |
| 15–25분 | 새 입력과 학습 범위 밖 입력 관찰 |
| 25–30분 | 한계와 재현 절차 기록 |

1. `uv run ex04`를 실행한다. 학습을 다시 하지 않고 `outputs/regression.pt`의 가중치를 읽는다.
2. `2.5`, `5.5`를 입력하고 ex03 마지막 실행의 예측과 비교한다.
3. `create_regression()`이 같은 모델 구조를 만들고, `load_state_dict`가 저장한 가중치를 채우는 부분을 찾는다.
4. `10`처럼 학습 자료 1~6시간 범위 밖 입력도 관찰한다. 그 값까지 정확하다고 단정하지 않는다.
5. 음수·문자·빈 줄을 입력해 처리 방법을 확인하고 `/bye`로 종료한다.

모델 파일이 없으면 먼저 ex03을 실행한다. `torch.no_grad()`는 예측에서 기울기 기록을 생략한다. 완료 조건은 같은 모델의 예측을 새 실행에서 재현하고 제한을 설명하는 것이다.

## 남길 파일

코드와 `pytorch_note.md`에 두 입력의 저장·복원, 학습 비교, 같은 모델의 예측 재현을 기록한다. `outputs/`와 `.venv/`는 커밋하지 않는다.
