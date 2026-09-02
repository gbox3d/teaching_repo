# lora_lab — 10주차 PEFT/LoRA 예제 프로젝트

상세 설명과 관찰 지점은 상위 [`../README.md`](../README.md)에 있다. 이 파일은 실행 요약이다.

## 준비

```powershell
Copy-Item .env.example .env
uv sync
```

`uv.lock`은 이 저장소에 포함하지 않는다. 학기별 환경 기준표가 확정된 뒤 기준 PC에서 `uv lock`을 생성해 커밋한다.
모델 ID·양자화·용량은 환경 기준표에서 확정하며 `.env.example`의 값은 교재 검증용 기본값이다.

## 실행 순서

```powershell
uv run python lora_setup.py --ranks 4,8,16      # 1교시: 학습 파라미터 비율표 + VRAM 예측표
uv run python train_lora.py --inspect           # 2교시: 템플릿·라벨 마스킹 확인
uv run python train_lora.py                     # 2교시: adapters/run-001/ 학습
uv run python compare.py                        # 3교시: 기본 vs 어댑터 전후 비교
uv run python merge.py --check                  # 3교시 확장: 병합본 저장
```

GPU가 없으면 `--device cpu --max-steps 5 --batch-size 1`로 학습을 짧게 끝낸다.

## 기준 PC 측정값 기록 칸

환경 기준표 확정 후 기준 PC에서 한 번 측정해 채운다. 학생 PC 값과 비교하는 기준이 된다.

| 스크립트 | 조건 | 실행 시간 | 최대 VRAM | 비고 |
|---|---|---:|---:|---|
| `lora_setup.py` | r=4,8,16 · 기본 모델 | | | 모델 3회 로드 |
| `train_lora.py` | 2 epoch · batch 4 · accum 2 · max_len 512 | | | step 수: |
| `train_lora.py` | `--device cpu --max-steps 5 --batch-size 1` | | 해당 없음 | |
| `compare.py` | 프롬프트 5개 · max_new_tokens 120 | | | |
| `merge.py` | `--check` | | | 병합본 용량: |
