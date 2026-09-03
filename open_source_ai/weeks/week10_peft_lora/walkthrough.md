# 10주차 따라하기 — LoRA 설정, 학습, 전후 비교와 기록

이 문서는 10주차 시연·실습을 **순서대로 그대로 재현**하기 위한 절차서다.
강의자는 각 교시의 20분 시연을 이 순서로 진행하고, 학생은 실습·복습 때 같은 순서로 따라 한다.
각 단계는 `할 일 → 예상 결과 → 확인` 순서로 되어 있다. 예상 결과가 다르면 다음 단계로 넘어가지 않는다.

## 시작 전 준비

- uv, Git, VS Code, PowerShell을 사용한다. GPU 실습은 NVIDIA GPU(기준 12 GB VRAM)가 전제이며, 없으면 각 단계의 CPU 대체 명령을 쓴다.
- `HF_TEXT_MODEL`(교재 검증용 기본값 `Qwen/Qwen2.5-0.5B-Instruct`)이 수업 전에 캐시되어 있다. 실제 모델 ID·revision은 환경 기준표가 정한다. 실습 중 모델을 내려받지 않는다.
- [`examples/`](examples/README.md)의 `lora_lab/`을 개인 실습 폴더(`C:\classwork\week10\lora_lab`)에 **복사**해서 사용한다. 수업 자료 원본은 수정하지 않는다. `uv sync`는 수업 전에 한 번 실행해 둔다.
- 이 문서의 숫자(파라미터 수, MB, loss)는 기본 모델·기본 옵션 기준의 예다. 모델이나 옵션이 다르면 값이 달라지며, 그 값을 기록하는 것이 실습이다.
- 터미널 명령은 복사한 폴더 안에서 실행한다. 현재 경로를 먼저 확인하는 습관을 들인다.

---

## 1교시 — 어댑터 붙이고 학습 파라미터 세기

### 단계 1. 복사·환경·캐시 확인

**할 일**

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week10_peft_lora\examples"
New-Item -ItemType Directory -Force C:\classwork\week10 | Out-Null
Copy-Item -Recurse "$src\lora_lab" C:\classwork\week10\lora_lab
Set-Location C:\classwork\week10\lora_lab
Copy-Item .env.example .env
uv sync
uv run python -c "import torch, transformers, peft; print('cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu')"
uv run python -c "from huggingface_hub import scan_cache_dir; print([r.repo_id for r in scan_cache_dir().repos])"
```

**예상 결과** — `uv sync`가 이미 되어 있으면 몇 초 안에 끝난다. 첫 출력은 GPU PC에서 `cuda True <GPU 이름>`, 없는 PC에서 `cuda False cpu`다. 두 번째 출력의 목록에 `.env`의 `HF_TEXT_MODEL` 값이 들어 있다.

**확인** — [ ] 캐시 목록에 기본 모델이 있다. 없으면 강의자에게 캐시 배포를 요청하고 실습 중 내려받지 않는다.

### 단계 2. rank 세 개로 학습 파라미터 세기

**할 일** — 실행 전에 "r=8일 때 비율은 0.1%·1%·10% 중 어디에 가까운가"를 적고 실행한다.

```powershell
uv run python lora_setup.py --ranks 4,8,16
```

**예상 결과** — `모델: … · 장치: cuda · dtype: torch.bfloat16`(CPU는 `cpu · torch.float32`) 뒤에 rank마다 한 줄씩 나온다. 기본 모델·기본 target 기준으로 r=8은 `trainable params: 1,081,344 || all params: 495,114,112 || trainable%: 0.2184`이고, r=4는 그 절반(약 54만, 0.11%), r=16은 두 배(약 216만, 0.44%)다. 이어서 표가 출력되고 `기록: outputs\setup-<시각>.json · outputs\setup-<시각>.md`가 찍힌다. 모델을 rank마다 다시 읽으므로 CPU에서는 수십 초가 걸린다.

**확인** — [ ] 학습 파라미터 수가 r에 정비례한다는 것을 표에서 확인하고 `r × (in + out)`으로 설명했다.

### 단계 3. target_modules를 줄여 보기

**할 일**

```powershell
uv run python lora_setup.py --ranks 8 --target-modules q_proj,v_proj
```

**예상 결과** — r=8인데 학습 파라미터가 단계 2의 r=4(네 계층)와 같은 약 54만 개다. `q_proj`와 `o_proj`의 `in + out`이 같고 `k_proj`와 `v_proj`의 `in + out`이 같아, 네 계층에서 `q_proj,v_proj`만 남기면 계층 합이 정확히 절반이 되고 r을 두 배로 올린 것과 상쇄되기 때문이다.

**확인** — [ ] "붙이는 계층을 줄이는 것과 r을 줄이는 것 중 어느 쪽이 파라미터를 더 줄이는가"를 이 모델 기준으로 한 문장 적었다.

### 단계 4. VRAM 예측표 읽기

**할 일** — `outputs/setup-*.md`(가장 최근 파일)를 열어 r=8 행과 `full` 행의 가중치·학습 상태·활성화·예측 합계 열을 예측표로 옮긴다.

```powershell
Get-ChildItem outputs\setup-*.md | Sort-Object LastWriteTime | Select-Object -Last 1 | Get-Content
```

**예상 결과** — 기본 조건(seq 512, batch 4, bf16)에서 r=8 행은 가중치 약 940 MB, 학습 상태 약 17 MB, 활성화 약 3,100 MB, 합계 약 4 GB다. `full` 행은 학습 상태만 약 7.5 GB라 합계가 10 GB를 넘는다. 표 아래에 "예측은 경험식이다 … 실측과 비교" 문장이 있다.

**확인** — [ ] LoRA 행과 `full` 행 각각에 12 GB 판정("여유 / 배치 줄이면 가능 / 불가")을 적었다.

### 단계 5. 활성화 조건을 하나씩 바꾸기

**할 일**

```powershell
uv run python lora_setup.py --ranks 8 --seq-len 256
uv run python lora_setup.py --ranks 8 --batch-size 1
```

**예상 결과** — 두 실행 모두 가중치·학습 상태 열은 그대로이고 활성화 열만 줄어든다(seq 256은 약 1/3, batch 1은 약 1/4). 활성화 예측식이 `seq × batch`에 비례하기 때문이다.

**확인** — [ ] 예측표에 "2교시 실측값" 빈 칸을 만들었다.

### 단계 6. 실패 경로와 정리

**할 일**

```powershell
uv run python lora_setup.py --ranks 8 --target-modules no_such_proj
$LASTEXITCODE
```

**예상 결과** — 스택 트레이스 없이 `[오류] target_modules `no_such_proj` 를 모델에서 찾지 못했다: …`와 안내 한 줄이 나오고 종료 코드가 `2`다.

**확인** — [ ] [`lab.md`](lab.md) 1교시 완료 조건을 모두 표시했다. 실습 30분 뒤 휴식 10분.

---

## 2교시 — 수업 도우미 말투로 LoRA 학습하기

### 단계 1. 템플릿과 라벨 마스킹 확인

**할 일** — 실행 전에 "첫 샘플에서 가려지는 토큰이 절반보다 많은가"를 적고 실행한다.

```powershell
Set-Location C:\classwork\week10\lora_lab
uv run python train_lora.py --inspect
```

**예상 결과** — 모델 가중치를 읽지 않으므로 몇 초 안에 끝난다. `<|im_start|>system … <|im_end|>`, `<|im_start|>user … <|im_end|>`, `<|im_start|>assistant … <|im_end|>` 세 블록이 출력되고, `=== 토큰 수 N · 라벨 가림 M · 학습 대상 N-M ===` 줄이 나온다. 마지막 줄 "학습 대상 토큰만 복원"은 `'핵심: uv는 …'`로 시작해 `<|im_end|>`로 끝나며 system·user 문장은 없다.

**확인** — [ ] 토큰 수·가림·학습 대상 세 값을 적었다.

### 단계 2. 경계 — 프롬프트보다 짧은 max_len

**할 일**

```powershell
uv run python train_lora.py --inspect --max-len 32
```

**예상 결과** — 토큰 수가 32로 잘리고 학습 대상이 `0`이다. 복원 문자열은 빈 문자열 `''`이다. 이 상태로 학습하면 손실을 계산할 라벨이 없어 loss가 `nan`이 되거나 학습이 일어나지 않는다.

**확인** — [ ] "max_len은 가장 긴 프롬프트+답변보다 커야 한다"를 기록했다. 실제 학습은 기본값 512로 돌린다.

### 단계 3. run-001 학습

**할 일** — 첫 loss와 마지막 loss를 예상해 적고 실행한다.

```powershell
uv run python train_lora.py --run-name run-001
```

GPU가 없으면:

```powershell
uv run python train_lora.py --run-name run-001 --device cpu --max-steps 5 --batch-size 1 --max-len 256
```

**예상 결과** — `데이터 57건`, `토큰 길이: 최소 … 최대 … 평균 …`, `trainable params: 1,081,344 …`가 차례로 나온 뒤 step마다 `{'loss': …, 'learning_rate': …, 'epoch': …}` 로그가 찍힌다. 기본 조건(57건, batch 4 × accum 2, 2 epoch)이면 16 step 안팎이고 기준 PC에서 수 분 안에 끝난다. 첫 loss는 한 자릿수(사전학습 모델이므로 무작위 초기화보다 훨씬 낮다), 마지막 loss는 그보다 낮다. 마지막에 `학습 완료: 16 step · …s · 최대 VRAM … MB`, `loss A → B`, `어댑터: adapters\run-001 · 기록: outputs\train-run-001.json`이 나온다. CPU 5 step은 loss가 조금만 움직이며 그것이 정상이다.

**확인** — [ ] `학습 완료` 줄의 step 수·시간·최대 VRAM과 `loss A → B`를 적었다.

### 단계 4. 어댑터 폴더와 기록 파일 확인

**할 일**

```powershell
Get-ChildItem adapters\run-001
Get-Content outputs\train-run-001.json | Select-Object -First 40
```

**예상 결과** — `adapters\run-001`에 `adapter_config.json`, `adapter_model.safetensors`(r=8 기준 약 4 MB), 토크나이저 파일들, `run_config.json`이 있다. 기본 모델 가중치 파일은 없다. JSON에는 `lora`, `train`, `env`, `result`(`first_loss`, `last_loss`, `elapsed_sec`, `max_vram_mb`), `loss_history`가 있다.

**확인** — [ ] `max_vram_mb`를 1교시 예측표의 "2교시 실측값" 칸에 옮기고 차이 이유 후보(예측식에 CUDA 컨텍스트·임시 버퍼가 없음)를 한 문장 적었다. CPU는 `null`이므로 "실측 없음"이라고 적는다.

### 단계 5. 실패 경로와 저장소 상태

**할 일**

```powershell
uv run python train_lora.py --data data/missing.jsonl
$LASTEXITCODE
git status
```

**예상 결과** — `[오류] 데이터 파일이 없다: data\missing.jsonl` 한 줄과 종료 코드 `2`. `git status`(실습 폴더가 저장소 안이라면)에 `adapters/`·`outputs/`·`.env`가 untracked로도 나타나지 않는다(`.gitignore`).

**확인** — [ ] [`lab.md`](lab.md) 2교시 완료 조건을 모두 표시했다. 실습 30분 뒤 휴식 10분.

---

## 3교시 — 전후 비교와 실험 기록 run-001

`adapters/run-001/`이 없으면(하루가 바뀌었거나 학습 실패) `uv run python train_lora.py --run-name run-001 --max-steps 5`로 다시 만들거나 강의자가 배포한 어댑터를 복사한 뒤 시작한다.

### 단계 1. 같은 조건으로 전후 비교

**할 일** — 형식 준수 수(기본/어댑터)와 p4·p5의 결과를 예상해 적고 실행한다.

```powershell
Set-Location C:\classwork\week10\lora_lab
Get-ChildItem adapters\run-001\adapter_config.json
uv run python compare.py --adapter adapters/run-001
```

GPU가 없으면 `--device cpu --max-new-tokens 60`을 붙인다.

**예상 결과** — `모델: … · 어댑터: adapters\run-001 · 장치: … · 프롬프트 5개` 뒤에 프롬프트마다 `기본  :`·`어댑터:` 첫 80자가 찍힌다. GPU 2 epoch 기준으로 어댑터 쪽은 대부분 `핵심:`으로 시작하고 기본 모델은 자유로운 문장이다. 마지막에 `형식 준수: 기본 a/5 · 어댑터 b/5`(b가 a보다 크다)와 `기록: outputs\compare-run-001.json · outputs\compare-run-001.md`가 나온다. CPU 5 step이면 a와 b가 비슷할 수 있다.

**확인** — [ ] 형식 준수 수를 예상과 비교해 적었다.

### 단계 2. 좋아진 것과 나빠진 것 읽기

**할 일** — `outputs\compare-run-001.md`를 열어 프롬프트 5개의 기본·어댑터 출력을 읽는다. p4(GitHub Actions)·p5(발표 구성)는 학습 데이터에 없는 주제다.

**예상 결과** — 머리 줄에 모델·어댑터·`greedy(do_sample=False) · max_new_tokens 120 · seed 42 · 장치`가 있고, 프롬프트마다 **기본 모델**·**어댑터 적용(형식 준수: 예/아니오)** 두 코드 블록이 있다. p4·p5에서 어댑터는 세 줄 형식을 따르지만 내용이 일반론이거나 부정확할 수 있다. 같은 문장 반복이나 잘린 출력이 보이면 그것이 나빠진 사례다.

**확인** — [ ] 나빠진 사례 1개 이상(없으면 "없음"과 근거)을 적었다.

### 단계 3. 경계 — 무관한 입력과 잘못된 어댑터 경로

**할 일**

```powershell
uv run python compare.py --adapter adapters/run-001 --prompt "오늘 점심 뭐 먹을까?" --tag offtopic
uv run python compare.py --adapter adapters/no-such
$LASTEXITCODE
```

**예상 결과** — 첫 실행은 `outputs\compare-run-001-offtopic.md`에 따로 기록되어 기본 기록을 덮어쓰지 않는다. 어댑터는 무관한 질문에도 `핵심: … 이유: … 다음 할 일: …` 형식을 강요할 가능성이 크다. 두 번째 실행은 `[오류] 어댑터 폴더에 adapter_config.json이 없다: adapters\no-such`와 종료 코드 `2`다.

**확인** — [ ] "형식 준수 5/5가 좋은 모델의 증거가 아닌 이유"를 한 문장 적었다.

### 단계 4. 실험 기록 run-001 작성

**할 일**

```powershell
$repo = "<개인 저장소 경로>"
New-Item -ItemType Directory -Force "$repo\experiments\run-001" | Out-Null
Copy-Item EXPERIMENT_TEMPLATE.md "$repo\experiments\run-001.md"
(Get-FileHash data\sample_sft.jsonl -Algorithm SHA256).Hash.Substring(0, 12)
Get-Content adapters\run-001\run_config.json
```

`$repo\experiments\run-001.md`의 7개 절을 `run_config.json`, `outputs\train-run-001.json`, `outputs\compare-run-001.json`, `outputs\setup-*.md`의 값으로 채운다. 2절 데이터 버전에 위 해시 12자리를, 모델 ID·revision에 5주차 `SOURCES.md`의 값을 쓴다.

**예상 결과** — 1절 목적 한 문장, 2절 고정한 것(모델·데이터 해시·system·seed 42·장치·dtype), 3절 설정(r 8 / alpha 16 / dropout 0.05, target 4개, 2 epoch, lr 2e-4 cosine, 4×2), 4절 결과(step·시간·VRAM 예측 vs 실측·loss 처음→마지막·학습 파라미터·어댑터 용량), 5절 샘플 3개 이상과 형식 준수율, 6절 관찰·실패(단계 2 경계, 실패 실행의 오류 첫 줄), 7절 다음 실험(바꿀 변수 하나·성공 기준)이 모두 채워져 있다. 직접 실행하지 않은 값은 없다.

**확인** — [ ] 빈 칸이 없고, 없는 값은 "해당 없음"과 이유로 채웠다.

### 단계 5. 기록 사본 복사와 commit

**할 일**

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

**예상 결과** — `git status`에 `experiments/` 아래 파일만 새로 보인다. commit 뒤 `git log`의 첫 줄이 `Add LoRA experiment record run-001`이고, 마지막 명령은 아무것도 출력하지 않는다(어댑터 가중치를 커밋하지 않았다).

**확인** — [ ] [`lab.md`](lab.md) 3교시 완료 조건을 모두 표시했다. 실습 30분 뒤 휴식 10분. 이번 주 종료.

### 단계 6. (확장) 병합본 만들기

**할 일**

```powershell
Set-Location C:\classwork\week10\lora_lab
uv run python merge.py --check
Get-ChildItem models\merged-run-001
```

**예상 결과** — `병합 완료: models\merged-run-001 · <용량> MB · <초>s · dtype …`와 짧은 생성 결과 한 단락이 나온다. 병합본 용량은 기본 모델 가중치와 같은 크기(bf16 기준 약 1 GB)이고 어댑터(약 4 MB)보다 훨씬 크다. `outputs\merge-run-001.json`에 `note`로 bf16 반올림 안내가 있다.

**확인** — [ ] 병합본은 `models/`에 있어 커밋되지 않는다는 것을 `git status`로 확인했다.

---

## 문제가 생겼을 때

| 증상 | 이 문서에서 돌아갈 단계 |
|---|---|
| `[오류] 모델을 불러오지 못했다` | 1교시 단계 1 (캐시 목록·`.env`의 `HF_TEXT_MODEL`·`HF_HUB_OFFLINE` 확인, 실습 중 다운로드 금지) |
| `uv sync`가 실패하거나 torch를 못 찾는다 | 1교시 단계 1 (네트워크·CUDA 인덱스 확인, `pip install` 금지, 강의자에게 문의) |
| `[오류] target_modules … 찾지 못했다` | 1교시 단계 6 (모델 구조에서 계층 이름 확인, `lab.md` 1교시 힌트 2) |
| `lora_setup.py`가 CPU에서 너무 느리다 | 1교시 단계 2 (`--ranks 8` 하나만 실행, 나머지는 비례식으로) |
| `--inspect` 학습 대상이 0이다 | 2교시 단계 2 (`--max-len`이 프롬프트보다 짧다. 기본값 512로) |
| CUDA out of memory | 2교시 단계 3 (`--batch-size 2 --grad-accum 4` → `--max-len 256` → `--gradient-checkpointing` 순서로 하나씩) |
| loss가 nan이거나 움직이지 않는다 | 2교시 단계 1·3 (`trainable params` 0 여부, 학습 대상 토큰 수, `--dtype bf16`, `--lr 1e-4`) |
| `adapters/run-001`이 없다 | 3교시 도입 (`--max-steps 5`로 재학습 또는 배포본 사용, 기록에 명시) |
| 기본과 어댑터 출력이 똑같다 | 3교시 단계 1 (CPU 5 step이면 정상 관찰. GPU면 `run_config.json`의 `last_loss`와 `--adapter` 경로 확인) |
| 출력이 잘려 세 줄이 다 안 나온다 | 3교시 단계 1 (`--max-new-tokens 160`, 바꾼 조건을 기록 5절에 명시) |
| commit에 `.safetensors`가 들어갔다 | 3교시 단계 5 (`git restore --staged`로 내리고 `.gitignore`에 `adapters/`·`models/` 확인) |

세부 판정 기준과 힌트는 [`lab.md`](lab.md)에 있다. 정답과 해설은 실습이 끝난 뒤 강의자가 별도로 안내한다.
