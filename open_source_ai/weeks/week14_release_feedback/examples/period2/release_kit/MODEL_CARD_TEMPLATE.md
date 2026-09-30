---
license: apache-2.0
base_model: Qwen/Qwen2.5-0.5B-Instruct
language:
  - ko
tags:
  - lora
  - peft
library_name: peft
---

<!--
Hub 의 모델 카드는 모델 저장소의 `README.md` 다. 이 파일을 그 이름으로 올려야 카드로 렌더링되고 위 frontmatter 가 메타데이터가 된다.
값은 SOURCES.md 와 같아야 한다. 기반 모델 ID 는 환경 기준표에서 확정한 값으로 바꾼다.
어댑터를 공개하지 않는 팀은 이 파일을 만들지 않아도 된다.
-->

# 모델 카드 — 어댑터 이름

## 모델 설명

- 종류: LoRA 어댑터 (기반 모델 가중치는 포함하지 않는다)
- 기반 모델: `Qwen/Qwen2.5-0.5B-Instruct` (revision: 커밋 해시를 적는다)
- 목적: (예: 수업 도우미 말투·형식으로 답하게 함)
- 만든 팀: team-a
- 저장 형식: safetensors (`adapter_model.safetensors`, `adapter_config.json`)

## 의도된 용도와 금지 용도

- 의도: (예: 로컬 PC 에서 수업 자료 질의응답 데모)
- 금지: (예: 사실 확인 없이 외부 공개 답변 생성, 개인정보가 담긴 입력)

## 학습 데이터

| 이름 | 건수 | 라이선스 | 출처 | 변경 |
|---|---:|---|---|---|
| (예: `data/sample_sft.jsonl`) | (예: 48) | (예: CC-BY-4.0, 자체 작성) | (예: 팀 작성) | (예: PII 마스킹, 중복 제거) |

데이터 카드: `DATA_CARD.md`

## 학습 절차

| 항목 | 값 |
|---|---|
| LoRA r / alpha / target modules | (예: 8 / 16 / q_proj,k_proj,v_proj,o_proj) |
| epoch / learning rate / batch | (예: 2 / 2e-4 / 4) |
| seed | (예: 42) |
| 소요 시간 / 최대 VRAM | 기준 PC 측정값을 적는다 |
| 실험 기록 | `experiments/run-001.md` |

## 평가

| 지표 (test 20문항) | 기준 모델 | 어댑터 적용 |
|---|---:|---:|
| 키워드 일치율 | | |
| 형식 준수율 | | |

평가셋은 학습에 쓰지 않았다. 측정 스크립트: (예: `evaluate.py`)

## 한계와 편향

- (예: 학습 데이터가 수업 도메인에 한정되어 다른 주제에서는 형식만 따라 한다.)
- (예: 형식은 따르지만 사실 오류가 남는다. 사례는 `FAILURE_ANALYSIS.md`.)

## 라이선스

- 기반 모델: (예: Apache-2.0 — 기반 모델 카드에 적힌 값)
- 학습 데이터: 위 표
- 어댑터: 기반 모델과 데이터 조건을 모두 만족하는 라이선스 (예: Apache-2.0, 데이터가 NC 면 비상업 조건을 명시)

## 인용

`CITATION.cff` 를 따른다.
