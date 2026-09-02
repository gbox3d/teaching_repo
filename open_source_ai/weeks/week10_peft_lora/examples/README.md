# 10주차 예제 — LoRA 실험 프로젝트 `lora_lab`

## 파일 구성

| 경로 | 역할 | 쓰는 교시 |
|---|---|---|
| `lora_lab/` | uv 프로젝트. 아래 스크립트 5개, 데이터, 실험 기록 양식 | 1·2·3교시 |
| `lora_lab/common.py` | 공통 헬퍼 — 환경변수 읽기, 장치·dtype 선택, JSONL 읽기, `outputs/` 기록, 모델 로드 오류 안내, system 프롬프트·메시지 구성 | 모든 스크립트가 import |
| `lora_lab/lora_setup.py` | `HF_TEXT_MODEL`에 `LoraConfig`를 붙여 rank별 학습 파라미터 수·비율과 VRAM 예측표(가중치·학습 상태·활성화)를 만든다 | 1교시 |
| `lora_lab/train_lora.py` | `data/sample_sft.jsonl`로 LoRA SFT 학습. `--inspect`는 chat template·라벨 마스킹만 보여 주고 종료. `--max-steps`로 짧게 실행 가능 | 2교시 |
| `lora_lab/compare.py` | 같은 프롬프트·greedy·같은 seed로 기본 모델(어댑터 끔)과 어댑터 모델 출력을 나란히 기록. 형식 준수 수 집계, `--tag`로 기록 이름 분리 | 3교시 |
| `lora_lab/merge.py` | `merge_and_unload()`로 어댑터를 기본 가중치에 병합해 `models/merged-<run>/`에 safetensors로 저장. `--check`로 생성 1회 | 3교시 확장 |
| `lora_lab/data/sample_sft.jsonl` | 자체 작성 한국어 Q&A 57건. `{"instruction": …, "output": …}` 형식, 답은 모두 "핵심 · 이유 · 다음 할 일" 세 줄. 수업 내용(uv·Git·라이선스·Ollama·HF·LoRA·평가)만 다루고 실제 인물·기관 정보 없음 | 2교시 |
| `lora_lab/data/eval_prompts.json` | 전후 비교용 프롬프트 5개(`[{id, prompt}]`). p1~p3는 학습 주제 안, p4·p5는 학습 데이터에 없는 주제 | 3교시 |
| `lora_lab/EXPERIMENT_TEMPLATE.md` | 실험 기록 양식 7개 절. 팀 저장소 `experiments/run-NNN.md`로 복사해 채운다. 11·12주차와 3차 종합과제가 같은 양식을 쓴다 | 3교시 |
| `lora_lab/pyproject.toml` | 의존성(torch CUDA 인덱스 블록, transformers, peft, accelerate, datasets, safetensors, huggingface_hub, python-dotenv) | |
| `lora_lab/.env.example`, `.gitignore` | 환경변수 예시(`HF_TEXT_MODEL`, `HF_HOME`, `HF_HUB_OFFLINE`, `HF_TOKEN`), 커밋 제외 목록(`adapters/`, `models/`, `outputs/`, `.env`, `.venv/`) | |
| `lora_lab/README.md` | 실행 요약과 기준 PC 측정값 기록 칸 | 강의자 |

모델 ID·양자화·용량은 학기별 환경 기준표에서 확정하며, `.env.example`의 `HF_TEXT_MODEL=Qwen/Qwen2.5-0.5B-Instruct`는 교재 검증용 기본값이다. `uv.lock`은 이 저장소에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.

## 실행 방법

원본을 훼손하지 않도록 개인 실습 폴더에 복사한 뒤 실행한다. `uv sync`(torch 설치)와 모델 캐시는 수업 전에 끝내 둔다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week10_peft_lora\examples"
Copy-Item -Recurse "$src\lora_lab" C:\classwork\week10\lora_lab
Set-Location C:\classwork\week10\lora_lab
Copy-Item .env.example .env
uv sync
```

교시 순서대로 실행한다.

```powershell
uv run python lora_setup.py --ranks 4,8,16                 # 1교시: 학습 파라미터 비율표 + VRAM 예측표 → outputs/setup-*.md
uv run python lora_setup.py --ranks 8 --target-modules q_proj,v_proj
uv run python train_lora.py --inspect                      # 2교시: chat template·라벨 마스킹 확인(토크나이저만 읽음)
uv run python train_lora.py --run-name run-001             # 2교시: 2 epoch 학습 → adapters/run-001/, outputs/train-run-001.json
uv run python compare.py --adapter adapters/run-001        # 3교시: 전후 비교 → outputs/compare-run-001.md
uv run python compare.py --adapter adapters/run-001 --prompt "오늘 점심 뭐 먹을까?" --tag offtopic
uv run python merge.py --check                             # 3교시 확장: models/merged-run-001/
```

주요 옵션은 `--help`로 본다. 학습 기본값은 r=8, alpha=16, dropout 0.05, target `q_proj,k_proj,v_proj,o_proj`, lr 2e-4(cosine, warmup 5%), 2 epoch, batch 4 × grad accum 2, max_len 512, seed 42다. 결과는 모두 `outputs/`에 JSON 또는 Markdown으로 남고 어댑터는 `adapters/<run-name>/`에 저장된다.

## 관찰 지점

1. `lora_setup.py`: 학습 파라미터 수가 r에 정비례하는가(`r × (in + out)`). `target_modules`를 `q_proj,v_proj`로 줄인 r=8과 네 계층 모두 붙인 r=4의 파라미터 수가 같은가. `--seq-len`·`--batch-size`는 활성화 열만 바꾸고, `--dtype fp32`는 가중치 열만 두 배로 만드는가. `full` 행의 학습 상태(MB)와 LoRA 행의 차이.
2. `train_lora.py --inspect`: system·user 구간 라벨이 모두 -100이고 "학습 대상 토큰만 복원" 문자열이 답변과 종료 토큰만인가. `--max-len 32`로 줄이면 학습 대상이 0이 되는 경계.
3. `train_lora.py`: step 1의 loss(사전학습 모델이므로 한 자릿수)와 마지막 loss. `outputs/train-run-001.json`의 `max_vram_mb`가 1교시 예측 합계와 얼마나 다른가(예측식에 CUDA 컨텍스트·임시 버퍼가 없다). 같은 seed로 다시 돌렸을 때 `loss_history`가 같은가.
4. `compare.py`: 형식 준수 수(기본 vs 어댑터). p4·p5처럼 학습 데이터에 없는 주제에서 형식은 따르되 내용이 부정확한 경우. 반복·언어 혼합·잘림 같은 나빠진 사례. `--tag offtopic`의 무관한 입력에 세 줄 형식을 강요하는지.
5. `merge.py`: 병합본 용량(기본 모델과 같은 크기)과 어댑터 용량(수 MB)의 차이. bf16 병합본과 어댑터 방식의 출력이 완전히 같은지(반올림 차이).
6. 실패 경로: `--target-modules no_such_proj`, `--data data/missing.jsonl`, `--adapter adapters/no-such`, 잘못된 `HF_TEXT_MODEL`이 모두 스택 트레이스가 아니라 한 줄 메시지와 종료 코드 2로 끝나는가.

## GPU 없을 때·네트워크 없을 때

- **GPU 없음**: `lora_setup.py`와 `train_lora.py --inspect`는 CPU에서 그대로 실행된다(로드 시간만 길다). 학습은 `uv run python train_lora.py --run-name run-001 --device cpu --max-steps 5 --batch-size 1 --max-len 256`으로 파이프라인만 확인한다. 이때 전후 비교 차이가 거의 없을 수 있으며, 그 사실을 기록에 적는다. `compare.py`는 `--device cpu --max-new-tokens 60`으로 줄인다. `--device cpu`는 CUDA를 가리므로 GPU PC에서 CPU 경로를 재현할 때도 쓸 수 있다.
- **VRAM 부족(12 GB 미만)**: `--batch-size 2 --grad-accum 4` → `--max-len 256` → `--gradient-checkpointing` 순서로 하나씩 줄인다. 바꾼 값은 `run_config.json`에 자동으로 남는다.
- **네트워크 없음**: 모델이 캐시되어 있으면 `.env`의 `HF_HUB_OFFLINE=1` 주석을 풀어 캐시만 쓴다. 캐시가 없으면 실습 시간에 내려받지 않고 강의자가 배포한 캐시 폴더를 `HF_HOME`으로 지정한다. 데이터는 저장소 안의 파일이라 네트워크가 필요 없다.
- **어댑터 학습 실패로 3교시를 시작할 수 없을 때**: `--max-steps 5`로 짧게 다시 만들거나 강의자가 배포한 `adapters/run-001/`을 복사해 `compare.py`를 진행한다. 기록에 "배포본 사용"이라고 적는다.
- **토큰 없음**: 기본 모델은 gated가 아니므로 토큰이 필요 없다. gated 모델로 바꿀 때만 `.env`의 `HF_TOKEN`에 넣고, 파일과 명령줄에 토큰을 쓰지 않는다.

## 복사 후 변형

- 스크립트는 그대로 두고 인자와 `.env`만 바꾸는 것이 기본이다. 코드를 고쳤다면 어떤 줄을 왜 바꿨는지 실험 기록 6절에 적는다.
- 팀 데이터로 바꿀 때는 `data/sample_sft.jsonl`과 같은 `{"instruction", "output"}` 형식을 지키고, 답변 형식(세 줄)을 바꾸면 `compare.py`의 `FORMAT_MARKERS`도 함께 바꾼다. 실제 인물·기관·개인정보는 넣지 않는다(11주차에 정제·점검한다).
- system 프롬프트(`common.py`의 `SYSTEM_PROMPT`)를 바꾸면 학습과 비교가 같은 문장을 쓰도록 한 곳만 고친다. 바꾼 문장을 실험 기록 2절에 적는다.
- `adapters/`, `models/`, `outputs/`, `.env`는 어느 폴더에서도 커밋하지 않는다. 기록은 `outputs/`에서 개인 저장소 `experiments/run-NNN/`로 복사해 커밋한다.
- 실행 시간·VRAM의 기준값은 `lora_lab/README.md`의 측정값 기록 칸에 강의자가 기준 PC에서 채운다.
