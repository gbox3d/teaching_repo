# 6주차 실습 — pipeline 안쪽을 숫자로 확인하라

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 실습 시간에 모델을 새로 내려받지 않는다. 3교시 임베딩 모델은 수업 전 사전 캐시가 전제이며, 1·2교시는 모델 파일이 필요 없다.
- GPU가 없거나 인식되지 않으면 `--device cpu`로 같은 절차를 진행하고, 기록의 `device` 값이 `cpu`인 채로 남긴다. 없는 값을 지어내지 않는다.
- `outputs/`는 커밋하지 않는다. 증거로 남길 JSON은 개인 저장소의 `evidence/week06/`에 복사한다.

## 1교시 실습 — 텐서 이동과 자동미분 관찰

### 상황

팀원이 "5주차 pipeline이 GPU에서 빠르긴 한데, 짧은 문장 하나를 넣으면 CPU와 별 차이가 없거나 오히려 느린 것 같다"고 한다. 행렬 크기를 바꿔 가며 CPU/GPU 시간과 복사 시간을 재고, 어느 크기부터 GPU가 이득인지 숫자로 답하라. 덧붙여 추론 코드에 `torch.no_grad()`를 빼먹으면 무엇이 달라지는지도 근거를 대야 한다. 이어받는 것: 5주차 `pipeline_report.md`의 CPU/GPU 시간 비교표.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 행렬 크기 3개의 GPU 배속과 `no_grad` 메모리 차이를 예상표에 적기 |
| 기본 실행 | 5–12분 | `tensor_basics.py` 기본 실행, 여섯 절 출력과 `tensor_report.json` 읽기 |
| 크기 비교 | 12–21분 | `--size` 3개로 실행, 시간·복사 비교표 작성, 교차점 찾기 |
| `no_grad` 관찰 | 21–25분 | `--batch`·`--layers`를 키워 활성화 메모리 차이 확인 |
| 검증·기록 | 25–30분 | 실패 경로 재현, `tensor_compare.md` 완성, `evidence/` 복사 |

### 준비

원본 `examples/`를 훼손하지 않도록 개인 저장소 안의 실습 폴더에 복사한다. `$src`·`$dst`는 예시이며 실습실 안내에 따라 바꾼다.

```powershell
$src = "C:\teaching_repo\open_source_ai\weeks\week06_pytorch_models\examples"
$dst = "$HOME\osa-practice\week06"   # 5주차까지 쓴 개인 저장소 안의 폴더로 바꾼다
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item -Recurse "$src\torch_lab" "$dst\torch_lab"
Set-Location "$dst\torch_lab"
Copy-Item .env.example .env
uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
uv run python tensor_basics.py --help
```

`uv sync`(첫 실행 시 torch 설치)는 수업 전에 마쳐 둔다. 위 확인 명령이 `True`를 출력하면 GPU 경로, `False`면 CPU 경로로 진행한다. 두 경우 모두 같은 문제를 푼다.

### 문제 1 · 행렬 크기에 따른 CPU/GPU 시간

1. 실행 전에 예상표를 적는다. 행렬 크기 256·2048·4096에 대해 "GPU가 CPU보다 몇 배 빠를지", "CPU→GPU 복사 시간이 계산 시간보다 길지 짧을지"를 각각 예상한다.
2. `uv run python tensor_basics.py`를 실행한다. 출력의 `[1]`~`[6]` 여섯 절을 위에서부터 읽고, `[2]` 행렬곱 절의 `cpu`·`cuda`·복사 시간·`speedup`을 적는다. GPU가 없으면 `cpu` 값만 나온다.
3. `outputs/tensor_report.json`을 열어 `matmul` 항목의 `cpu_s`·`gpu_s`·`h2d_copy_s`·`speedup`이 화면 출력과 같은 값인지 확인한다.
4. 크기를 바꿔 두 번 더 실행한다. GPU가 없는 PC는 4096 대신 `--size 1024 --repeat 1`을 쓴다.

   ```powershell
   uv run python tensor_basics.py --size 256 --output outputs/tensor_report-256.json
   uv run python tensor_basics.py --size 4096 --output outputs/tensor_report-4096.json
   ```

5. 세 결과를 아래 표에 옮기고, "어느 크기부터 GPU가 이득인가"와 "복사 시간을 포함하면 배속이 얼마나 줄어드는가"를 각각 한 문장으로 쓴다.

   ```text
   | size | cpu ms | gpu ms | 복사 ms | speedup | 복사 포함 speedup |
   |-----:|-------:|-------:|--------:|--------:|------------------:|
   |  256 |        |        |         |         |                   |
   | 2048 |        |        |         |         |                   |
   | 4096 |        |        |         |         |                   |
   ```

완료 조건:

- [ ] `outputs/tensor_report*.json`이 세 개 있고 `matmul.size`가 서로 다르다.
- [ ] 비교표 3행이 채워졌고 예상표와 가장 크게 어긋난 칸 하나를 골라 이유를 적었다.
- [ ] GPU가 이득이 되기 시작하는 크기(또는 "이 PC에서는 GPU 없음")를 한 문장으로 적었다.

### 문제 2 · `no_grad`와 활성화 메모리

1. 기본 실행 출력의 `[5]` 자동미분 절에서 `x.grad`가 `[2.0, 4.0, 6.0]`인 이유를 수식 한 줄로 적는다.
2. `[6]` 절의 두 줄(`no_grad=False`·`no_grad=True`)에서 `requires_grad`·`grad_fn`·추가 메모리를 비교한다. 기본 설정(hidden 1024 · batch 256 · layers 4)에서는 차이가 작으므로 크기를 키워 다시 실행한다.

   ```powershell
   uv run python tensor_basics.py --batch 4096 --layers 8 --output outputs/tensor_report-nograd.json
   ```

3. `no_grad.with_grad.peak_extra_mb`와 `no_grad.no_grad.peak_extra_mb`, `theory_activation_mb`를 표로 적는다. GPU가 없으면 메모리 칸은 "측정 불가(CPU)"로 두고 `grad_fn` 값의 차이로 설명한다.
4. 실패 경로: `uv run python tensor_basics.py --device cuda:9`를 실행하고 출력의 첫 줄과 마지막 줄, `$LASTEXITCODE`를 기록한다. GPU가 없는 PC는 사람이 읽을 안내문이, GPU가 있는 PC는 장치 번호 오류가 나온다. 둘 중 무엇이 나왔는지와 그 이유를 한 줄로 적는다.

완료 조건:

- [ ] `with_grad`와 `no_grad`의 차이를 메모리 수치 또는 `grad_fn`으로 한 문장 설명했다.
- [ ] 실패 경로의 첫 줄·마지막 줄과 종료 코드를 기록했다.

### 단계별 힌트

<details>
<summary>힌트 1 — uv run이 torch를 새로 설치하려 한다</summary>

수업 전 `uv sync`가 끝나지 않은 PC다. 실습실 네트워크가 허용되면 그대로 두고 기다리되 수 분이 걸린다. 허용되지 않으면 조교가 안내하는 공용 `.venv` 사본을 쓰거나, 옆 사람 PC에서 측정값만 얻어 표를 채우고 그 사실을 적는다.
</details>

<details>
<summary>힌트 2 — GPU 시간이 CPU보다 느리거나 실행마다 크게 다르다</summary>

256 같은 작은 크기에서는 커널 실행 준비 비용이 계산 시간보다 커서 GPU가 느린 것이 정상이다. 값이 흔들리면 `--repeat 10`으로 평균 횟수를 늘린다. 스크립트는 첫 호출을 예열로 버리고 `torch.cuda.synchronize()` 뒤에 시간을 재므로, 직접 코드를 고쳐 잴 때도 같은 순서를 지킨다.
</details>

<details>
<summary>힌트 3 — 추가 메모리가 0.0이거나 두 값이 같다</summary>

`peak_extra_mb`는 forward 동안 늘어난 최대치다. 모델이 너무 작으면 반올림 자리에서 사라진다. `--batch 4096 --layers 8`처럼 활성화(배치 × 은닉 × 층 수)가 커지도록 인자를 키운다. CPU에서는 항상 `null`이 나오며 이는 오류가 아니다.
</details>

### 검증

- 정상: `outputs/tensor_report.json`에 `tensor_info`·`matmul`·`dtype`·`linear_model`·`autograd`·`no_grad` 여섯 항목이 있고 `autograd.grad`가 `[2.0, 4.0, 6.0]`이다.
- 경계 또는 실패: `--size 256`에서는 `speedup`이 1 아래로 내려갈 수 있다. `--device cuda:9`는 GPU가 없는 PC에서는 안내문 한 줄로, GPU가 있는 PC에서는 마지막 줄이 `AssertionError: Invalid device id`인 스택 트레이스로 끝난다(둘 다 종료 코드 1).
- 설명: "`.to("cuda")`가 이동이 아니라 복사인 것이 시간 측정과 메모리에 어떤 영향을 주는가"를 한 문장으로 쓴다.

### 확장 문제

1. `--repeat 10`과 `--repeat 1`의 평균 시간을 비교하고, 예열 없이 첫 호출까지 포함해 재면 값이 어떻게 달라지는지 `time_matmul`을 복사본에서 고쳐 확인한다.
2. 복사본의 `time_matmul`에 `dtype` 인자를 추가해 float32와 float16 행렬곱 시간을 GPU에서 비교한다. `[3]` 절의 dtype 표와 함께 "메모리 절반이 시간 절반을 뜻하는가"에 답한다.
3. `[5]` 절의 계산을 TensorFlow의 `tf.GradientTape`로 쓰면 어떤 세 줄이 되는지 의사코드로 적는다(설치하지 않는다). 두 프레임워크에서 "무엇을 기록하는가"가 같은 점을 한 문장으로 쓴다.

## 2교시 실습 — 소형 MLP 학습 루프와 과적합

### 상황

팀 회의에서 "epoch을 많이 돌릴수록 모델이 좋아지는 것 아니냐"는 의견이 나왔다. 외부 데이터 없이 스크립트가 만드는 2차원 분류 데이터로 소형 MLP를 학습해 val loss가 다시 오르는 시점을 찾고, "몇 epoch에서 멈춰야 하는가"를 곡선 수치로 답하라. 이어받는 것: 1교시 `torch_lab` 폴더와 `tensor_report.json`의 `device` 값(이번 교시 기록에도 같은 값이 남아야 한다).

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 기본 설정의 val loss 최저 epoch과 400 epoch 곡선 모양 예상 |
| 기준 실행 | 4–10분 | 기본 실행, epoch 표와 요약 읽기, 1 epoch의 step 수 계산 |
| 과적합 재현 | 10–19분 | 긴 epoch·큰 모델로 실행, 최저·마지막 값 표, 과적합 시점 문장 |
| seed·실패 | 19–25분 | seed를 바꿔 재실행 비교, `--val-ratio 0` 실패 경로 |
| 검증·기록 | 25–30분 | `overfit_note.md` 완성, `evidence/` 복사 |

### 준비

1교시에 복사한 `torch_lab` 폴더에서 계속한다. 새로 시작하는 날이면 1교시의 준비 명령을 먼저 실행한다.

```powershell
Set-Location "$HOME\osa-practice\week06\torch_lab"
uv run python train_loop.py --help
New-Item -ItemType File -Force ..\overfit_note.md | Out-Null
```

### 문제 1 · 기준 학습 곡선

1. 실행 전에 예상을 적는다. 기본 설정(60 epoch, hidden 32, 300개 중 val 30%)에서 val loss가 최저가 되는 epoch, 마지막 val accuracy, 그리고 400 epoch까지 돌리면 val loss가 "계속 내려간다/평평해진다/다시 오른다" 중 무엇일지 고른다.
2. `uv run python train_loop.py`를 실행한다. 10 epoch마다 찍히는 표에서 train loss와 val loss가 함께 내려가는 구간을 확인하고, 마지막 요약의 다섯 값(val loss 최저와 그 epoch, 마지막 val loss, 마지막 train loss, val-train 차이)을 `overfit_note.md`에 적는다.
3. `outputs/train-<시각>.json`을 열어 `config`에 인자 전부, `history`에 60개 항목, `summary.overfit_suspected`가 들어 있는지 확인한다.
4. 출력 첫 줄의 `train N개`와 `--batch-size 32`로 1 epoch의 step 수를 계산해 적는다(마지막 배치는 32보다 작을 수 있다).

완료 조건:

- [ ] 기준 실행의 JSON이 있고 요약 다섯 값을 옮겨 적었다.
- [ ] 1 epoch의 step 수를 계산식과 함께 적었다.

### 문제 2 · 과적합 재현과 seed

1. 모델을 키우고 epoch을 늘려 실행한다. 태그를 붙여 파일 이름으로 구분한다.

   ```powershell
   uv run python train_loop.py --epochs 400 --hidden 128 --tag overfit
   ```

2. 기준 실행과 이번 실행을 아래 표로 비교한다.

   ```text
   | 실행 | val loss 최저(epoch) | 마지막 val loss | 마지막 train loss | val−train | overfit_suspected |
   |---|---:|---:|---:|---:|---|
   | 기준(60, h32) | | | | | |
   | overfit(400, h128) | | | | | |
   | overfit seed 7 | | | | | |
   ```

3. `history`에서 최저 epoch 이후 val loss가 최저값의 1.05배를 처음 넘는 epoch을 찾는다(힌트 3의 한 줄 명령을 써도 된다). "과적합은 epoch N부터 시작했다. 근거: val loss 최저 a(epoch M) → epoch N에서 b, 같은 구간 train loss는 c → d"의 형태로 한 문장을 쓴다.
4. seed만 바꿔 다시 실행하고 표의 세 번째 행을 채운다. 최저 epoch이 달라졌는지, 과적합 판정이 같은지 비교한다.

   ```powershell
   uv run python train_loop.py --epochs 400 --hidden 128 --tag overfit-seed7 --seed 7
   ```

5. 실패 경로: `uv run python train_loop.py --val-ratio 0`을 실행하고 메시지 첫 줄과 `$LASTEXITCODE`를 기록한다. 왜 val 없이 학습을 시작하면 안 되는지 한 줄로 적는다.

완료 조건:

- [ ] `outputs/train-*-overfit.json`과 `outputs/train-*-overfit-seed7.json`이 있다.
- [ ] 비교표 3행과 "과적합 시작 시점" 문장에 근거 수치가 들어 있다.
- [ ] 실패 경로의 메시지와 종료 코드를 기록했다.

### 단계별 힌트

<details>
<summary>힌트 1 — 400 epoch을 돌려도 val loss가 다시 오르지 않는다</summary>

모델이 외울 만큼 크지 않거나 라벨 잡음이 적은 경우다. `--hidden 256`으로 키우거나 `--label-noise 0.2`로 잡음을 늘리면 뒤집힌 라벨까지 외우기 시작하면서 val loss가 오른다. 데이터를 `--n-samples 120`으로 줄여도 같은 효과가 난다. 무엇을 바꿨는지 표에 함께 적는다.
</details>

<details>
<summary>힌트 2 — 같은 명령인데 실행마다 곡선이 다르다</summary>

`--seed`가 같은지 먼저 본다. seed가 같아도 GPU에서는 일부 연산이 비결정적이라 소수점 아래가 달라질 수 있다. `--device cpu`로 두 번 실행하면 `history`가 완전히 같아야 한다. 이 차이 자체를 `overfit_note.md`에 적는다.
</details>

<details>
<summary>힌트 3 — history에서 시점을 손으로 찾기 어렵다</summary>

한 줄 명령으로 최저 이후 처음 1.05배를 넘는 항목을 찾는다. 파일 이름은 자기 것으로 바꾼다.

```powershell
uv run python -c "import json,sys; r=json.load(open(sys.argv[1],encoding='utf-8')); s=r['summary']; hit=[h for h in r['history'] if h['epoch']>s['val_loss_min_epoch'] and h['val_loss']>s['val_loss_min']*1.05]; print(s['val_loss_min_epoch'], hit[0] if hit else '없음')" outputs\train-XXXXXXXX-XXXXXX-overfit.json
```
</details>

### 검증

- 정상: 기준 실행에서 마지막 val loss가 1 epoch의 val loss보다 낮고 마지막 val accuracy가 0.75 이상이다. JSON의 `history` 길이가 `--epochs`와 같다.
- 경계 또는 실패: `--val-ratio 0`(또는 `1`)은 학습을 시작하지 않고 사람이 읽을 메시지와 종료 코드 1로 끝난다.
- 설명: "val loss는 오르는데 train loss는 계속 내려가는 것이 왜 좋아지는 게 아니라 과적합인가"를 한 문장으로 쓴다.

### 확장 문제

1. `--lr 0.3`으로 실행해 loss가 커지거나 `nan`이 되는 발산을 관찰하고, `--lr 0.0001`과 비교해 "학습률이 곡선 모양을 어떻게 바꾸는가"를 두 문장으로 쓴다.
2. 복사본 `train_loop.py`에 `--patience N` 옵션을 추가해 val loss가 N epoch 동안 개선되지 않으면 멈추게 만든다(early stopping). 멈춘 epoch과 문제 2의 최저 epoch을 비교한다.
3. `--n-samples 3000`으로 데이터를 10배 늘려 같은 400 epoch을 돌리고, 과적합 시점이 늦어지는지(또는 사라지는지) 표에 한 행을 더한다.

## 3교시 실습 — 문장 임베딩과 실험 기록

### 상황

다음 주에 문서 검색기를 만들 팀이 "임베딩 모델이 우리 한국어 문장을 정말 의미로 구분하는지, pooling은 무엇을 써야 하는지, 실행 조건을 어떻게 남겨야 나중에 비교가 되는지" 미리 확인해 달라고 한다. 문장 5개의 유사도 행렬을 만들고 실험 기록을 3건 이상 남겨라. 이어받는 것: 5주차 `SOURCES.md`의 임베딩 모델 행(모델 ID·commit hash·라이선스)과 2교시 `outputs/train-*.json`의 기록 항목.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 내장 5문장 중 가장 비슷한 쌍과 가장 동떨어진 문장을 예상 |
| 기본 실행 | 4–12분 | `pretrained_embed.py` 실행, shape 세 개와 유사도 행렬 읽기, 예상과 비교 |
| 변형 실행 | 12–21분 | 자기 문장 5개, `--pooling cls`, `--prefix ""` 중 두 가지로 재실행 |
| 실패·기록 | 21–25분 | 없는 모델 ID 실패 경로, `runlog.py` 표 확인 |
| 검증·기록 | 25–30분 | `experiment_note.md` 완성, `evidence/` 복사 |

### 준비

```powershell
Set-Location "$HOME\osa-practice\week06\torch_lab"
Get-Content .env                      # HF_EMBED_MODEL, HF_HOME 값 확인
uv run python pretrained_embed.py --help
New-Item -ItemType File -Force ..\experiment_note.md | Out-Null
```

`.env`의 `HF_EMBED_MODEL`은 5주차 `SOURCES.md`에 적은 임베딩 모델 ID와 같아야 한다. 실습실 공용 캐시를 쓴다면 `HF_HOME` 줄에 안내받은 경로를 적는다. 모델은 이미 캐시에 있어야 하며 실습 중 내려받지 않는다.

### 문제 1 · 유사도 행렬 읽기

1. `sentences.txt`의 다섯 문장을 읽고, 가장 비슷한 쌍 하나, 나머지와 가장 동떨어진 문장 하나, 그리고 첫 문장(s1)에서 본 나머지 네 문장의 순위를 예상해 적는다.
2. `uv run python pretrained_embed.py --show-tokens`를 실행한다. 출력에서 `input_ids`·`last_hidden_state`·문장 임베딩의 shape 세 개, 문장별 실제 토큰 수, 첫 문장의 토큰 분할(서브워드로 쪼개진 곳)을 `experiment_note.md`에 적는다.
3. 코사인 유사도 행렬에서 가장 비슷한 쌍과 점수, s1 행의 순위를 읽고 예상과 비교한다. 다른 곳이 있으면 어떤 문장이 왜 가까웠는지 한 문장으로 쓴다.
4. 마지막 줄의 softmax 확률을 적은 뒤 `--temperature 1.0`으로 다시 실행해, 순위는 그대로인데 확률의 쏠림이 어떻게 달라지는지 비교한다.
5. 출력의 `revision=` 값을 5주차 `SOURCES.md`의 commit hash와 비교해 같은지 적는다.

완료 조건:

- [ ] `outputs/embed-*.json`과 `outputs/runs/*-embed.json`이 각각 1개 이상 있다.
- [ ] shape 세 개와 가장 비슷한 쌍을 예상과 비교한 문장을 적었다.
- [ ] revision이 5주차 기록과 같은지(또는 다른 이유)를 적었다.

### 문제 2 · 변형 실행과 실험 기록

1. `sentences.txt`를 `my_sentences.txt`로 복사해 자기 문장 5개로 바꾼다. 수업 내용 문장 3개, 그중 하나를 다른 말로 바꾼 문장 1개, 전혀 무관한 문장 1개로 구성하고 실명·학번·기관명을 넣지 않는다. `--sentences my_sentences.txt`로 실행해 바꿔 쓴 두 문장이 가장 비슷한 쌍으로 잡히는지 확인한다.
2. 같은 문장으로 `--pooling cls`를 실행해 가장 비슷한 쌍과 점수가 mean pooling과 어떻게 다른지 적는다. 모델 카드가 권하는 pooling이 무엇인지 5주차 `model_cards.md`에서 찾아 근거로 붙인다.
3. `--prefix ""`로 접두어 없이 실행해 점수가 어떻게 움직이는지 본다. e5 계열이 `query: ` 접두어를 요구하는 이유를 카드의 문장으로 한 줄 인용한다.
4. 실패 경로: `uv run python pretrained_embed.py --model no-org/no-model`을 실행해 메시지 첫 줄과 `$LASTEXITCODE`를 기록한다. 메시지가 안내하는 세 가지 확인 사항 중 이 PC에 해당하는 것을 고른다.
5. `uv run python runlog.py`로 지금까지의 기록 표를 보고, 아래 표를 `experiment_note.md`에 채운다. 값은 `outputs/runs/*.json`의 `config`·`metrics`·`elapsed_s`·`max_memory_allocated_mb`에서 가져온다.

   ```text
   | 실행 | 모델 | pooling | prefix | 가장 비슷한 쌍(점수) | 경과(s) | 최대 메모리(MB) |
   |---|---|---|---|---|---:|---:|
   | 기본 | | mean | query: | | | |
   | 내 문장 | | mean | query: | | | |
   | cls 또는 prefix 없음 | | | | | | |
   ```

완료 조건:

- [ ] `outputs/runs/`에 기록이 3건 이상 있고 `runlog.py` 표에 모두 보인다.
- [ ] 실험 기록 표 3행을 채웠고 pooling 또는 prefix 변경의 효과를 한 문장으로 적었다.
- [ ] 실패 경로의 첫 줄과 종료 코드를 기록했다.

### 단계별 힌트

<details>
<summary>힌트 1 — 모델을 불러오지 못했다는 메시지가 나온다</summary>

`.env`의 `HF_EMBED_MODEL` 철자, `HF_HOME`이 사전 캐시 위치를 가리키는지, 네트워크가 없는 실습실이면 `HF_HUB_OFFLINE=1`이 켜져 있는지 순서대로 본다. 캐시에 없는 모델을 실습 중에 내려받지 않는다. 캐시가 없는 PC는 조교 안내에 따라 공용 캐시 경로를 `HF_HOME`에 넣는다.
</details>

<details>
<summary>힌트 2 — 모든 문장 쌍의 유사도가 0.8 이상으로 비슷비슷하다</summary>

e5 계열은 코사인 값이 전체적으로 높게 나오는 특성이 있다. 절대값이 아니라 행 안의 순위와 차이로 읽고, softmax 확률(`--temperature`)로 쏠림을 본다. 무관한 문장(점심 식사)이 그래도 가장 낮은지 확인하면 된다.
</details>

<details>
<summary>힌트 3 — runlog.py 표가 비어 있다</summary>

`RunLog.finish()`는 현재 폴더 기준 `outputs/runs/`에 쓴다. `Get-Location`으로 `torch_lab` 안인지 확인하고, 다른 곳에서 실행했다면 `--run-dir`로 그 경로를 가리킨다. `pretrained_embed.py`가 실패로 끝난 실행은 기록을 남기지 않는다.
</details>

### 검증

- 정상: 유사도 행렬의 대각선이 `1.000`이고 대칭이며, 수업 내용 문장끼리의 값이 무관한 문장과의 값보다 높다.
- 경계 또는 실패: 없는 모델 ID는 사람이 읽을 메시지와 종료 코드 1로 끝나고 `outputs/runs/`에 기록을 남기지 않는다. `--pooling cls`는 mean과 순위가 달라질 수 있다.
- 설명: "`attention_mask`를 pooling에 넣지 않으면 무엇이 잘못되는가"를 한 문장으로 쓴다.

### 확장 문제

1. `--max-length 8`로 실행해 긴 문장이 잘렸을 때 유사도가 어떻게 바뀌는지 보고, 다음 주 chunk 크기 선택과 어떤 관계가 있는지 한 문장으로 쓴다.
2. `outputs/embed-*.json`의 `similarity`를 numpy로 읽어 "질의 문장 s1에 가장 가까운 문장 1개"를 돌려주는 함수 `top1(sim, i)`를 짧은 스크립트로 만든다. 7주차 `search.py`의 뼈대가 된다.
3. 같은 명령을 `--device cpu`로 한 번 더 실행해 `runlog.py` 표에서 경과 시간과 `max_memory_allocated_mb` 칸이 어떻게 달라지는지(무엇이 `-`가 되는지) 적는다.

## 제출 체크

- `tensor_compare.md`: 예상표, 크기 3개의 CPU/GPU·복사 시간 비교표와 교차점 문장, `no_grad` 메모리 표, 실패 경로 첫 줄
- `overfit_note.md`: 기준·overfit·seed 7 실행의 비교표, 과적합 시작 시점 문장(근거 수치 포함), step 수 계산, 실패 경로 첫 줄
- `experiment_note.md`: shape 세 개, 예상 vs 실제 비교 문장, 실험 기록 표 3행, pooling·prefix 효과 문장, revision 비교
- `evidence/week06/`: `tensor_report.json`, `train-*-overfit.json` 1건, `runs/*-embed.json` 1건
- 개인 저장소: 이번 주 commit 3개 이상, `.env`와 `outputs/`가 commit되지 않았음을 `git status`로 확인
- 선택: 확장 문제 결과
