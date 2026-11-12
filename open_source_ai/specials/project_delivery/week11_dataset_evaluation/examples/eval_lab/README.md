# eval_lab — 11주차 데이터셋 정제·분할과 모델 평가 예제 프로젝트

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
uv run python clean.py                         # 1교시: data/raw.jsonl → outputs/clean.jsonl (중복·빈 값 제거)
uv run python pii_check.py --action report     # 1교시: 개인정보 패턴 검출만
uv run python pii_check.py                     # 1교시: 마스킹 → outputs/masked.jsonl
uv run python split.py                         # 1교시: train/val/test 분할 + 누수 검사
uv run python metrics.py --demo                # 2교시: 지표 함수 예시
uv run python evaluate.py --predictions data/sample_predictions/base.json data/sample_predictions/lora.json
                                               # 2교시: 모델 없이 예측 JSON만 채점
uv run python evaluate.py --adapter <10주차 어댑터 폴더>   # 2교시: 실제 기준선 vs LoRA 생성·채점 (GPU)
uv run python make_sheet.py                    # 3교시: 최근 eval-*.json → outputs/scoring-*.md 수동 채점표
```

GPU가 없으면 `evaluate.py --device cpu --limit 5 --max-new-tokens 96`으로 문항 수를 줄이거나 `--predictions` 모드만 쓴다.

## 기준 PC 측정값 기록 칸

환경 기준표 확정 후 기준 PC에서 한 번 측정해 채운다. 학생 PC 값과 비교하는 기준이 된다.

| 스크립트 | 조건 | 실행 시간 | 최대 VRAM | 비고 |
|---|---|---:|---:|---|
| `clean.py` → `split.py` | 기본 옵션 | | 해당 없음 | 첫 `split.py`는 `datasets` import로 몇 초 더 걸린다 |
| `evaluate.py --predictions` | 샘플 2개 | | 해당 없음 | |
| `evaluate.py` | base + 어댑터 · 20문항 · max_new_tokens 160 | | | 모델 2회 로드 |
| `evaluate.py --device cpu --limit 5` | base만 | | 해당 없음 | |
