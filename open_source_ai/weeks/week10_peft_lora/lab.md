# 10주차 실습 — 어댑터를 학습하고 실험을 기록하라

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 이번 주는 모델을 내려받지 않는다. `HF_TEXT_MODEL`(기본값 `Qwen/Qwen2.5-0.5B-Instruct`)은 수업 전에 캐시되어 있어야 하며, 로드 실패 메시지가 나오면 힌트를 따라 캐시·`.env`를 확인한다.
- 조건은 한 번에 하나만 바꾸고 run 이름을 새로 붙인다. 실패한 실행도 지우지 않고 기록에 남긴다.
- Hugging Face 토큰은 `.env`에만 둔다. 어댑터(`adapters/`)·병합본(`models/`)은 저장소에 커밋하지 않는다. 학습 데이터와 기록에 실제 인물·기관 정보를 넣지 않는다.

## 1교시 실습 — 어댑터 붙이고 학습 파라미터 세기

### 상황

9주차 제안서에서 모델 후보를 골랐더니 팀원이 "12 GB GPU로 이 모델에 LoRA 학습이 되느냐"고 물었다. 감으로 답하지 말고, 실제로 어댑터를 붙여 rank별 학습 파라미터 비율표와 VRAM 예측표를 만들어 근거와 함께 답하라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | r=4·8·16의 학습 파라미터 비율과 r을 2배로 했을 때의 변화를 예상 |
| 기본 실행 | 5–13분 | 복사·`.env` 확인 후 `lora_setup.py --ranks 4,8,16` 실행, 표 읽기 |
| 변형 실행 | 13–22분 | `--target-modules`, `--seq-len`, `--batch-size`를 한 번에 하나씩 바꿔 재실행 |
| 검증·기록 | 22–30분 | 예측표 정리, 실패 경로 재현, 예상과 실제 비교 문장 작성 |

### 준비

원본 `examples/`를 훼손하지 않도록 개인 실습 폴더에 복사한다. `uv sync`는 수업 전에 한 번 실행해 두었다는 전제다(torch 설치에 네트워크가 필요하다).

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week10_peft_lora\examples"
New-Item -ItemType Directory -Force C:\classwork\week10 | Out-Null
Copy-Item -Recurse "$src\lora_lab" C:\classwork\week10\lora_lab
Set-Location C:\classwork\week10\lora_lab
Copy-Item .env.example .env
uv sync
uv run python -c "import torch; print('cuda', torch.cuda.is_available())"
```

GPU가 없는 PC는 `cuda False`가 정상이다. 이 교시의 스크립트는 학습하지 않으므로 CPU에서도 끝난다(모델을 rank마다 한 번씩 읽으므로 수십 초가 걸릴 수 있다).

### 문제 1 · rank별 학습 파라미터 비율표

1. 실행 전에 예상을 적는다. r=8일 때 학습 파라미터 비율이 0.1%·1%·10% 중 어디에 가까운가. r을 4→8→16으로 올리면 학습 파라미터 수는 몇 배가 되는가.
2. 기본 조건으로 실행한다.

```powershell
uv run python lora_setup.py --ranks 4,8,16
```

3. 콘솔의 `trainable params: … || all params: … || trainable%: …` 세 줄과 `outputs/setup-*.md`의 표를 읽고, r=4·8·16 행의 학습 파라미터 수와 비율(%)을 옮겨 적는다.
4. 학습 파라미터 수가 r에 정비례하는 이유를 LoRA 계층 하나의 파라미터 수 `r × (in + out)`으로 설명한다.
5. 붙이는 계층을 줄여 다시 실행하고, 비율이 어떻게 변하는지 적는다.

```powershell
uv run python lora_setup.py --ranks 8 --target-modules q_proj,v_proj
```

완료 조건:

- [ ] r=4·8·16 세 행의 학습 파라미터 수와 비율(%)이 표에 있다.
- [ ] r과 학습 파라미터 수의 관계를 식 하나로 설명했다.
- [ ] `target_modules`를 `q_proj,v_proj`로 줄였을 때의 비율 변화를 한 문장으로 적었다.

### 문제 2 · VRAM 예측표

1. `outputs/setup-*.md`의 r=8 행에서 가중치·학습 상태·활성화·예측 합계 네 값을 예측표로 옮긴다. `full` 행(전체 파인튜닝)도 옮긴다.
2. 활성화 예측 조건을 한 번에 하나씩 바꿔 재실행하고, 어느 열이 변하는지 확인한다.

```powershell
uv run python lora_setup.py --ranks 8 --seq-len 256
uv run python lora_setup.py --ranks 8 --batch-size 1
```

3. 예측 합계를 12 GB와 비교해 LoRA 행과 `full` 행에 각각 "여유 / 배치 줄이면 가능 / 불가" 판정을 한 줄씩 적는다.
4. 예측표에 "2교시 실측값" 빈 칸을 남긴다. 2교시 학습이 끝나면 `max_vram_mb`를 옮겨 적고 차이 이유를 쓴다.

완료 조건:

- [ ] r=8의 네 덩어리와 합계, `full` 행이 예측표에 있다.
- [ ] `--seq-len`·`--batch-size` 변경이 어느 열만 바꾸는지 적었다.
- [ ] LoRA와 전체 파인튜닝 각각의 12 GB 판정이 한 줄씩 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — "[오류] 모델을 불러오지 못했다"가 나온다</summary>

`.env`의 `HF_TEXT_MODEL` 철자를 확인하고, 캐시가 있는지 본다. 네트워크가 막힌 실습실이면 `.env`에서 `HF_HUB_OFFLINE=1`의 주석을 푼다. 실습 시간에 모델을 내려받지 않는다. 캐시 목록은 다음으로 본다.

```powershell
uv run python -c "from huggingface_hub import scan_cache_dir; print([r.repo_id for r in scan_cache_dir().repos])"
```
</details>

<details>
<summary>힌트 2 — "[오류] target_modules … 를 모델에서 찾지 못했다"가 나온다</summary>

모델마다 선형 계층 이름이 다르다. 모델 구조를 출력해 `Linear` 계층 이름을 확인한 뒤 `--target-modules`를 고친다.

```powershell
uv run python -c "import os; from transformers import AutoModelForCausalLM; print(AutoModelForCausalLM.from_pretrained(os.environ.get('HF_TEXT_MODEL', 'Qwen/Qwen2.5-0.5B-Instruct')))"
```
</details>

<details>
<summary>힌트 3 — CPU에서 너무 오래 걸린다</summary>

rank마다 모델을 한 번씩 읽는다. `--ranks 8`처럼 하나만 주면 1회 로드로 끝난다. 세 rank의 값은 `r × (in + out)` 관계로 계산해 표를 채우고, 그렇게 채웠다고 표에 적는다.
</details>

### 검증

- 정상: 세 rank 행에서 학습 파라미터 수가 r에 비례하고, 비율은 모두 1% 미만이다. `full` 행의 학습 상태(MB)가 LoRA 행보다 수백 배 크다.
- 경계 또는 실패: `--target-modules no_such_proj`로 실행해 스택 트레이스가 아니라 한 줄 오류 메시지가 나오고 종료 코드가 2인지 확인한다(`$LASTEXITCODE`).
- 설명: "r을 16에서 32로 올려도 12 GB 판정이 바뀌지 않는 이유"를 예측표의 열 이름을 써서 한 문장으로 적는다.

### 확장 문제

1. `--ranks 32,64,128`로 실행해 학습 파라미터 비율이 1%를 넘는 r을 찾고, 그때 학습 상태(MB)가 얼마인지 적는다.
2. `--dtype fp32`로 실행해 가중치 열이 두 배가 되는 것을 확인하고, 활성화 예측이 16비트 기준 경험식이라는 점을 예측표 각주에 적는다.

## 2교시 실습 — 수업 도우미 말투로 LoRA 학습하기

### 상황

팀 도우미가 항상 "핵심 · 이유 · 다음 할 일" 세 줄 형식으로 답하게 만들고 싶다. 4주차의 system 프롬프트만으로는 형식이 자주 깨졌다. 자체 작성 Q&A 57건으로 LoRA 어댑터를 학습해 `adapters/run-001/`로 저장하고 step별 loss를 기록하라.

이어받는 것: 1교시 `outputs/setup-*.md`의 r=8 예측 합계(실측과 비교할 값). 없으면 예측 없이 진행하고 3교시 기록에 "예측 없음"이라고 적는다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 첫 loss와 마지막 loss, 첫 샘플에서 가려질 토큰 비율을 예상 |
| 마스킹 확인 | 4–10분 | `--inspect`로 템플릿·라벨 마스킹 확인, 경계(`--max-len 32`) 재현 |
| 학습 실행 | 10–24분 | `train_lora.py --run-name run-001` 실행(GPU 수 분, CPU는 `--max-steps 5`) |
| 검증·기록 | 24–30분 | `outputs/train-run-001.json` 읽기, 어댑터 폴더 확인, 예측 vs 실측, `git status` |

### 준비

1교시와 같은 폴더에서 진행한다.

```powershell
Set-Location C:\classwork\week10\lora_lab
Get-Location
uv run python train_lora.py --help
```

### 문제 1 · 템플릿과 라벨 마스킹 확인

1. 실행 전에 예상을 적는다. 첫 샘플의 전체 토큰 중 라벨이 가려지는(-100) 토큰은 절반보다 많은가 적은가.
2. 토크나이저만 읽어 첫 샘플을 확인한다(모델을 읽지 않으므로 CPU에서도 바로 끝난다).

```powershell
uv run python train_lora.py --inspect
```

3. 출력에서 `<|im_start|>system`, `user`, `assistant` 세 블록을 찾고 `토큰 수 · 라벨 가림 · 학습 대상` 세 값을 적는다.
4. "학습 대상 토큰만 복원" 문자열이 답변(`핵심: …`)과 종료 토큰만으로 이루어졌는지 확인한다. system·user 문장이 섞여 있으면 마스킹이 잘못된 것이다.
5. 경계를 재현한다. `--inspect --max-len 32`로 다시 실행해 학습 대상 토큰이 0이 되는 것을 확인하고, 이 상태로 학습하면 무엇이 일어나는지 한 문장으로 적는다.

완료 조건:

- [ ] 토큰 수·라벨 가림·학습 대상 수를 기록했다.
- [ ] 학습 대상 복원 문자열이 답변만임을 확인했다.
- [ ] `--max-len 32`에서 학습 대상이 0이 되는 경계를 재현하고 그 의미를 적었다.

### 문제 2 · run-001 학습

1. 첫 loss(사전학습 모델이므로 무작위 초기화보다 훨씬 낮다)와 마지막 loss를 예상해 적는다.
2. 학습한다. 기본값은 r=8, alpha=16, lr 2e-4, 2 epoch, batch 4 × accum 2, max_len 512, seed 42다.

```powershell
uv run python train_lora.py --run-name run-001
```

GPU가 없으면 파이프라인 확인이 목적이므로 짧게 끝낸다.

```powershell
uv run python train_lora.py --run-name run-001 --device cpu --max-steps 5 --batch-size 1 --max-len 256
```

3. 콘솔에 step마다 찍히는 `loss`를 지켜보고, 끝에 나오는 `학습 완료: N step · Ns · 최대 VRAM … MB`와 `loss 처음 → 마지막` 줄을 옮겨 적는다.
4. 어댑터 폴더와 기록 파일을 확인한다.

```powershell
Get-ChildItem adapters\run-001
Get-Content outputs\train-run-001.json | Select-Object -First 40
```

5. `outputs/train-run-001.json`의 `first_loss`, `last_loss`, `elapsed_sec`, `max_vram_mb`를 1교시 예측표의 "2교시 실측값" 칸에 옮기고, 예측과 실측의 차이 이유 후보를 한 문장으로 적는다.
6. `git status`를 실행해 `adapters/`·`outputs/`가 untracked 목록에도 나타나지 않는지(`.gitignore`) 확인한다.

완료 조건:

- [ ] `adapters/run-001/`에 `adapter_config.json`, `adapter_model.safetensors`, `run_config.json`이 있다.
- [ ] `first_loss`보다 `last_loss`가 낮고 두 값을 기록했다.
- [ ] 최대 VRAM 예측 vs 실측 차이와 이유 후보를 한 문장으로 적었다(CPU는 "실측 없음").

### 단계별 힌트

<details>
<summary>힌트 1 — CUDA out of memory</summary>

한 번에 하나씩 줄인다. 먼저 `--batch-size 2 --grad-accum 4`(유효 배치는 그대로 8), 그래도 부족하면 `--max-len 256`, 마지막으로 `--gradient-checkpointing`을 켠다. 바꾼 값을 run 이름과 함께 기록한다.
</details>

<details>
<summary>힌트 2 — loss가 nan이거나 전혀 내려가지 않는다</summary>

`trainable params`가 0이면 `--target-modules` 이름이 틀린 것이다. 문제 1처럼 `--inspect`로 학습 대상 토큰이 0이 아닌지 본다. `--dtype fp16`을 썼다면 `bf16`(또는 `auto`)으로 바꾼다. 그래도 튀면 `--lr 1e-4`로 절반으로 줄인다.
</details>

<details>
<summary>힌트 3 — CPU에서 한 step에 수십 초가 걸린다</summary>

정상이다. `--max-steps 5 --batch-size 1 --max-len 256`이면 몇 분 안에 끝난다. 이 실행의 목적은 loss 하락이 아니라 어댑터 저장과 기록 파일 생성이므로, 3교시 기록에 "CPU 5 step"이라고 적는다.
</details>

### 검증

- 정상: `outputs/train-run-001.json`의 `loss_history`가 step 1부터 이어지고 `last_loss < first_loss`다. `adapters/run-001/run_config.json`의 `seed`가 42, `lora.r`이 8이다.
- 경계 또는 실패: `--data data/missing.jsonl`로 실행해 "[오류] 데이터 파일이 없다" 한 줄과 종료 코드 2가 나오는지 확인한다. 문제 1의 `--max-len 32`는 학습 대상 0인 경계다.
- 설명: "loss가 내려갔다는 사실이 '말투를 배웠다'의 충분한 증거가 아닌 이유"를 한 문장으로 적는다.

### 확장 문제

1. 같은 설정으로 `--run-name run-001b`를 한 번 더 학습하고 두 `loss_history`를 나란히 놓는다. 같은 seed인데 값이 완전히 같은지, 다르면 어느 자리부터 다른지 적는다.
2. `--rank 16 --alpha 32 --run-name run-002`로 학습해 학습 파라미터·시간·최대 VRAM·마지막 loss를 run-001과 표로 비교한다(바꾼 변수는 rank 하나다).

## 3교시 실습 — 전후 비교와 실험 기록 run-001

### 상황

팀 리뷰어가 "어댑터가 정말 효과가 있느냐, 다음 주에 같은 결과를 다시 낼 수 있느냐"고 물었다. 같은 프롬프트 5개로 기본 모델과 어댑터 모델을 나란히 비교하고, 3차 종합과제의 첫 실험 기록 `experiments/run-001.md`를 작성해 개인 저장소에 커밋하라.

이어받는 것: 2교시의 `adapters/run-001/`. 하루가 바뀌어 폴더가 없거나 학습에 실패했다면 `uv run python train_lora.py --run-name run-001 --max-steps 5`로 다시 만들거나 강의자가 배포한 어댑터 폴더를 쓰고, 기록에 그 사실을 적는다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 5개 프롬프트의 형식 준수 수(기본/어댑터)와 주제 밖 문항(p4·p5)의 결과 예상 |
| 비교 실행 | 4–12분 | `compare.py` 실행, `outputs/compare-run-001.md` 읽기, 나빠진 것 찾기 |
| 기록 작성 | 12–24분 | `EXPERIMENT_TEMPLATE.md`를 `experiments/run-001.md`로 복사해 7개 절 채우기 |
| 검증·기록 | 24–30분 | 주제 밖 입력 경계 재현, 기록 사본 복사, commit, `git log` 확인 |

### 준비

`$repo`는 3주차부터 키워 온 개인 저장소 경로다. 기록은 실습 폴더가 아니라 개인 저장소의 `experiments/`에 둔다.

```powershell
Set-Location C:\classwork\week10\lora_lab
Get-ChildItem adapters\run-001
$repo = "<개인 저장소 경로>"
New-Item -ItemType Directory -Force "$repo\experiments\run-001" | Out-Null
Copy-Item EXPERIMENT_TEMPLATE.md "$repo\experiments\run-001.md"
```

### 문제 1 · 같은 조건 전후 비교

1. 실행 전에 예상을 적는다. 기본 모델과 어댑터 모델이 각각 5개 중 몇 개에서 "핵심·이유·다음 할 일" 형식을 지킬 것인가. 학습 데이터에 없는 주제인 p4·p5는 형식과 내용 중 무엇이 달라질 것인가.
2. 비교를 실행한다. greedy 디코딩, 같은 system 프롬프트, 같은 seed로 기본 모델(어댑터 끔)과 어댑터 모델을 한 객체로 번갈아 생성한다.

```powershell
uv run python compare.py --adapter adapters/run-001
```

GPU가 없으면 `--device cpu --max-new-tokens 60`을 붙인다.

3. 콘솔 마지막 줄의 `형식 준수: 기본 __/5 · 어댑터 __/5`를 적고 예상과 비교한다.
4. `outputs/compare-run-001.md`를 열어 프롬프트 5개마다 좋아진 점과 나빠진 점(같은 문장 반복, 언어 혼합, 근거 없는 내용, 잘린 출력)을 한 줄씩 표시한다. p4·p5에서 형식은 따르지만 내용이 부정확한지 특히 본다.

완료 조건:

- [ ] `outputs/compare-run-001.md`에 프롬프트 5개의 기본·어댑터 출력이 모두 있다.
- [ ] 형식 준수 수(기본/어댑터)를 적고 예상과 비교했다.
- [ ] 나빠진 사례 1개 이상을 근거와 함께 적었다(없으면 "없음"과 그 판단 근거).

### 문제 2 · 실험 기록 run-001

1. `$repo\experiments\run-001.md`의 7개 절을 채운다. 값은 `adapters/run-001/run_config.json`, `outputs/train-run-001.json`, `outputs/compare-run-001.json`, `outputs/setup-*.md`에서 옮기고 직접 실행하지 않은 값은 적지 않는다.
2. 2절 「고정한 것」의 데이터 버전은 파일 해시로 적는다. 모델 ID·revision은 5주차 `SOURCES.md`의 값을 쓴다.

```powershell
(Get-FileHash data\sample_sft.jsonl -Algorithm SHA256).Hash.Substring(0, 12)
```

3. 4절 「결과」에 1교시 VRAM 예측과 2교시 실측을 나란히 적고, 6절 「관찰과 실패」에 2교시 경계(`--max-len 32`)와 실패한 실행의 오류 첫 줄을 적는다.
4. 7절 「다음 실험」에 바꿀 변수 하나(예: rank 16, epoch 3, 데이터 추가)와 성공 기준(형식 준수 수 또는 11주차 평가 지표)을 적는다.
5. 기록 사본을 개인 저장소로 복사하고 커밋한다. 어댑터 가중치는 복사하지 않는다.

```powershell
Copy-Item outputs\setup-*.md "$repo\experiments\run-001\"
Copy-Item outputs\train-run-001.json "$repo\experiments\run-001\"
Copy-Item outputs\compare-run-001.md "$repo\experiments\run-001\"
Set-Location $repo
git status
git add experiments
git commit -m "Add LoRA experiment record run-001"
git log --oneline -3
git ls-files | Select-String safetensors
```

완료 조건:

- [ ] 7개 절에 모두 값이 있고, 없는 값은 빈칸 대신 "해당 없음"과 이유가 적혀 있다.
- [ ] 데이터 해시, 모델 ID, seed, 장치·dtype이 「고정한 것」에 있다.
- [ ] commit에 기록 파일만 있고 `git ls-files | Select-String safetensors`가 아무것도 출력하지 않는다.

### 단계별 힌트

<details>
<summary>힌트 1 — "[오류] 어댑터 폴더에 adapter_config.json이 없다"</summary>

`--adapter` 경로와 2교시 `--run-name`이 같은지 확인한다. 2교시 학습이 실패했으면 `train_lora.py --run-name run-001 --max-steps 5`로 짧게 다시 만든다. 강의자가 배포한 어댑터를 쓸 때는 기록에 "배포본 사용"이라고 적는다.
</details>

<details>
<summary>힌트 2 — 기본과 어댑터 출력이 거의 같다</summary>

CPU에서 5 step만 학습했다면 정상적인 관찰이다. 그 사실 자체를 6절에 적는다. GPU 2 epoch인데도 같다면 `adapters/run-001/run_config.json`의 `last_loss`가 내려갔는지, `--adapter` 경로가 맞는지 확인한다.
</details>

<details>
<summary>힌트 3 — 출력이 중간에 잘려 세 줄이 다 안 나온다</summary>

`--max-new-tokens 160`으로 늘려 다시 실행한다. 조건을 바꿨으므로 기록 5절의 조건 줄에 바뀐 값을 적는다. 잘린 출력은 형식 준수 "아니오"로 세는 것이 기본이다.
</details>

### 검증

- 정상: `outputs/compare-run-001.md`의 머리 줄에 모델·어댑터·greedy·seed·장치가 있고, 프롬프트 5개 × 기본·어댑터 출력 10개가 있다.
- 경계 또는 실패: 학습 주제와 무관한 입력을 `--tag`를 붙여 실행해(기본 기록을 덮어쓰지 않는다) 어댑터가 무관한 질문에도 세 줄 형식을 강요하는지 관찰한다. `--adapter adapters/no-such`로 실행해 한 줄 오류와 종료 코드 2를 확인한다.

```powershell
uv run python compare.py --adapter adapters/run-001 --prompt "오늘 점심 뭐 먹을까?" --tag offtopic
```

- 설명: "형식 준수 5/5가 '좋은 모델'의 증거가 아닌 이유와 11주차 평가에서 무엇을 더 재야 하는지"를 한 문장으로 적는다.

### 확장 문제

1. `uv run python merge.py --check`로 병합본을 만들고, `models/merged-run-001/`의 용량과 `adapters/run-001/`의 용량을 비교한다. 병합본 출력이 어댑터 출력과 같은지, 다르면 dtype(bf16 반올림) 때문인지 `--dtype fp32` 병합으로 확인한다.
2. 병합본을 Ollama로 가져오는 절차를 공식 import 문서에서 읽고 Modelfile `FROM` 줄 초안을 기록에 적는다(실행은 수업 시간 밖, 변환 도구가 필요할 수 있다).
3. 2교시 확장의 `run-002`(rank 16)를 `compare.py --adapter adapters/run-002`로 비교하고 `experiments/run-002.md`를 쓴다. 바뀐 변수가 하나뿐인지 확인한다.

## 제출 체크

- `experiments/run-001.md`: 7개 절(목적·고정한 것·설정·결과·샘플 출력·관찰과 실패·다음 실험)이 실측값으로 채워진 실험 기록
- `experiments/run-001/setup-*.md`: r=4·8·16 학습 파라미터 비율표와 VRAM 예측표(2교시 실측값 칸 포함)
- `experiments/run-001/train-run-001.json`: 설정·loss 이력·시간·최대 VRAM
- `experiments/run-001/compare-run-001.md`: 프롬프트 5개 전후 출력과 형식 준수 수
- `git log --oneline -3`: 기록 파일만 커밋한 이력(`safetensors` 파일 없음)
- 선택: 확장 문제 결과(`run-001b`·`run-002` 비교, 병합본 용량, Modelfile 초안)
