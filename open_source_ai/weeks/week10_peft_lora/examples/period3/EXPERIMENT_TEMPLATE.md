# 실험 기록 — run-NNN

> 이 파일을 팀 저장소의 `experiments/run-NNN.md`로 복사해 채운다. 값은 직접 실행한 결과만 적는다.
> `outputs/train-run-NNN.json`, `outputs/compare-run-NNN.json`, `adapters/run-NNN/run_config.json`에서 옮겨 적는다.

## 1. 목적

- 이 실험으로 확인하려는 것 한 문장:
- 비교 대상(이전 run 또는 기본 모델):

## 2. 고정한 것

| 항목 | 값 | 근거 파일 |
|---|---|---|
| 기본 모델 ID · revision | | `SOURCES.md` |
| 학습 데이터 파일 · 건수 · 버전(commit id) | | `data/` |
| system 프롬프트 | | `common.py` |
| seed | | `run_config.json` |
| 장치 · dtype | | `run_config.json` |

## 3. LoRA·학습 설정

| 항목 | 값 |
|---|---|
| r / alpha / dropout | |
| target_modules | |
| epochs 또는 max_steps | |
| learning rate · scheduler | |
| batch_size × grad_accum (유효 배치) | |
| max_len | |

## 4. 결과

| 항목 | 값 |
|---|---|
| 총 step | |
| 학습 시간(초) | |
| 최대 VRAM(MB) — 실측 | |
| 최대 VRAM(MB) — 1교시 예측 | |
| loss 처음 → 마지막 | |
| 학습 파라미터 수 · 비율(%) | |
| 어댑터 폴더 용량(MB) | |

loss 곡선(step: loss)을 5~10개 점만 옮겨 적는다.

```text
step 1: ...
step 5: ...
```

## 5. 샘플 출력(전후 비교)

같은 프롬프트, greedy, 같은 seed. 3개 이상.

| 프롬프트 | 기본 모델(요약) | 어댑터 적용(요약) | 형식 준수 |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

형식 준수율: 기본 __/5 · 어댑터 __/5

## 6. 관찰과 실패

- 예상과 다른 점:
- 나빠진 것(반복, 언어 혼합, 근거 없는 내용 등):
- 실패한 실행과 원인(오류 메시지 첫 줄):

## 7. 다음 실험

- 바꿀 변수 하나:
- 그대로 둘 것:
- 성공 기준:
