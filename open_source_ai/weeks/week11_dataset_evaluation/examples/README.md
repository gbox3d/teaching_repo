# 11주차 예제 — 데이터 정제·분할·평가 파이프라인

원시 Q&A 48건을 정제·마스킹·분할하고, 그 test split로 기준선 모델과 10주차 LoRA 어댑터를 정량·정성 비교하는 최소 파이프라인이다. 1교시는 데이터 스크립트 세 개, 2교시는 지표·평가 스크립트, 3교시는 채점표 생성과 양식에 쓴다. 팀 데이터는 `data/raw.jsonl`과 같은 JSONL 형식으로 바꾸면 그대로 흐른다.

```text
data/raw.jsonl ─clean.py─▶ outputs/clean.jsonl ─pii_check.py─▶ outputs/masked.jsonl ─split.py─▶ outputs/split/{train,val,test}.jsonl
                                                                                                             │
data/sample_predictions/*.json ──(모델 없이)──┐                                                             ▼
10주차 어댑터 adapters/run-001 ──(모델 모드)──┴──▶ evaluate.py ──▶ outputs/eval-*.json ──make_sheet.py──▶ outputs/scoring-*.md
```

## 파일 구성

| 경로 | 역할 |
|---|---|
| `eval_lab/pyproject.toml` | uv 프로젝트(numpy, torch(CUDA 인덱스 블록), transformers, peft, datasets, python-dotenv) |
| `eval_lab/.env.example` | `HF_TEXT_MODEL`, `LORA_ADAPTER_DIR`, `HF_HOME`, `HF_HUB_OFFLINE`. 복사해 `.env`로 쓴다 |
| `eval_lab/.gitignore` | `.venv`·`.env`·`outputs`·`adapters`·`models`를 Git 밖에 둔다 |
| `eval_lab/data/raw.jsonl` | 자체 작성 한국어 Q&A 48건(수업 내용, 실제 인물·기관 없음). 정확 중복 2건, 근사 중복 1건, 빈 출력 1건, 가짜 개인정보 3건을 일부러 넣었다 |
| `eval_lab/data/sample_predictions/base.json`, `lora.json` | 교재 검증용 가상 예측 20건씩. 모델·GPU 없이 2·3교시를 진행할 때 쓴다. 실제 모델 출력이 아니다 |
| `eval_lab/clean.py` | NFKC 정규화, 필수 필드·길이 검사, 정확 중복(instruction 키)·근사 중복(문자 2-gram Jaccard) 제거 → `outputs/clean.jsonl`, `clean_report.json` |
| `eval_lab/pii_check.py` | 정규식 3종(PHONE·EMAIL·RRN) 검출. `--action report`(검출만)·`mask`(기본)·`drop` → `outputs/masked.jsonl`, `pii_report.json` |
| `eval_lab/split.py` | `datasets.Dataset.train_test_split` 두 번으로 train/val/test, 누수 검사, `--against`로 외부 학습 파일과 겹침(오염) 검사 → `outputs/split/`, `split_report.json` |
| `eval_lab/metrics.py` | 분류 지표(혼동행렬·accuracy·precision·recall·F1)와 생성 지표(정확 일치·키워드·유사도·형식·한글 비율·반복). `--demo`로 자체 예시 실행 |
| `eval_lab/evaluate.py` | 기준선 vs 어댑터를 test split로 생성·채점(모델 모드) 또는 예측 JSON만 채점(`--predictions`). `--exclude`로 오염 문항 제외 → `outputs/eval-*.json` |
| `eval_lab/make_sheet.py` | `eval-*.json`에서 수동 채점표 Markdown을 만든다(청사진 밖 보조 스크립트, 3교시 시간 절약용) |
| `eval_lab/DATA_CARD_TEMPLATE.md` | 데이터 카드 양식(1교시) |
| `eval_lab/manual_scoring_sheet.md` | 채점 기준·오류 유형 코드·빈 채점표 양식(3교시) |
| `eval_lab/FAILURE_ANALYSIS_TEMPLATE.md` | 실패 분석 보고 양식(3교시) |
| `eval_lab/README.md` | 프로젝트 안 짧은 안내와 기준 PC 측정값 기록 칸 |

모델 ID·양자화·용량은 학기별 환경 기준표에서 확정하며, 코드의 기본값(`HF_TEXT_MODEL=Qwen/Qwen2.5-0.5B-Instruct`)은 교재 검증용 기본값이다. `uv.lock`은 이 폴더에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.

## 실행 방법

원본을 훼손하지 않도록 `eval_lab/`을 개인 실습 폴더에 복사한 뒤 그 안에서 실행한다.

```powershell
Copy-Item -Recurse .\eval_lab C:\classwork\week11\eval_lab
Set-Location C:\classwork\week11\eval_lab
Copy-Item .env.example .env
uv sync
```

1교시 — 데이터 파이프라인(GPU 불필요):

```powershell
uv run python clean.py                                  # 48 → 44건, 제거 사유 출력
uv run python clean.py --near-threshold 0.95            # 근사 중복 판정을 느슨하게
uv run python pii_check.py --action report              # 검출만, 파일은 만들지 않는다
uv run python pii_check.py                              # 마스킹 → outputs/masked.jsonl
uv run python split.py                                  # train 20 / val 4 / test 20, seed 42
uv run python split.py --seed 7 --out-dir outputs/split_seed7 --report outputs/split_report_seed7.json
uv run python split.py --against C:\classwork\week10\lora_lab\data\sample_sft.jsonl   # 10주차 학습 데이터와 겹침 검사
```

2교시 — 평가:

```powershell
uv run python metrics.py --demo                         # 지표 함수 예시 → outputs/metrics_demo.json
uv run python evaluate.py --predictions data/sample_predictions/base.json data/sample_predictions/lora.json
uv run python evaluate.py                               # HF_TEXT_MODEL 기준선(+ LORA_ADAPTER_DIR 어댑터) 실제 생성·채점
uv run python evaluate.py --adapter C:\classwork\week10\lora_lab\adapters\run-001
uv run python evaluate.py --exclude q023 q005 q008      # split.py --against가 보고한 겹침 문항을 빼고 채점
uv run python evaluate.py --device cpu --limit 5 --max-new-tokens 96   # GPU 없을 때
```

3교시 — 채점표:

```powershell
uv run python make_sheet.py --run lora                  # 최근 eval-*.json → outputs/scoring-*.md
uv run python make_sheet.py --eval outputs\eval-<시각>.json   # 특정 파일, 모든 실행
```

### 환경변수

| 변수 | 기본값 | 용도 |
|---|---|---|
| `HF_TEXT_MODEL` | `Qwen/Qwen2.5-0.5B-Instruct` | 기준선 모델. 10주차 LoRA와 같은 모델이어야 어댑터가 붙는다 |
| `LORA_ADAPTER_DIR` | (비어 있음) | 10주차 어댑터 폴더(`adapter_config.json`이 있는 곳). 비어 있으면 기준선만 평가 |
| `HF_HOME` | (설정 시) | Hugging Face 캐시 위치 |
| `HF_HUB_OFFLINE` | (설정 시 `1`) | 네트워크 없이 캐시만 쓴다 |

우선순위는 코드 기본값 → `.env` → 셸 환경변수 → 명령 인자(`--base`, `--adapter`) 순으로 뒤가 앞을 덮는다.

### 데이터 형식

`data/raw.jsonl`의 한 줄:

```json
{"id": "q003", "instruction": ".venv 폴더를 Git에 올려도 되나요?",
 "output": "핵심: .venv는 커밋하지 않고 .gitignore에 넣는다.\n이유: …\n다음 할 일: `git status`에 .venv가 나타나지 않는지 확인한다.",
 "keywords": [".gitignore", "커밋"], "source": "ta-faq"}
```

- `output`은 10주차 `sample_sft.jsonl`과 같은 세 줄 형식(핵심/이유/다음 할 일)이다. `metrics.py`의 형식 준수 판정이 이 형식을 본다.
- `keywords`는 "이 답이 맞다면 반드시 들어갈 말" 1~3개다. 키워드 일치율의 기준이 된다.
- `source`는 출처 분류(`course-notes`, `ta-faq`, `student-qa`)다. 데이터 카드의 출처 절과 편향 점검에 쓴다.
- 예측 JSON(`--predictions`)은 `{"model": "이름", "adapter": null, "predictions": [{"id": "q023", "output": "…"}]}` 형식이다.

## 관찰 지점

1. `clean.py` 출력: 48 → 44. `q009`(정확 중복 ← q003), `q021`(공백만 다른 정확 중복 ← q014), `q033`(근사 중복 ← q027, 유사도 약 0.94), `q040`(빈 output). `--near-threshold 0.95`에서는 q033이 살아남는다.
2. `pii_check.py --action report`: 3건 — `q012` output의 PHONE, `q025` instruction의 EMAIL, `q038` output의 RRN. q038은 "이런 패턴을 찾는다"는 설명용 예시다. 정규식은 이 차이를 모른다 — 오탐으로 볼지, 그래도 마스킹할지는 사람이 정해 데이터 카드에 적는다.
3. `split.py`: train 20 / val 4 / test 20, `leak_count` 0. seed를 바꾸면 test id 목록이 바뀐다(seed 7이면 `q012`, `q044`, … 로 시작). `--against`로 10주차 `sample_sft.jsonl`을 주면 3건이 겹침으로 보고된다: `q023`(유사도 1.0, "torch.no_grad는 언제 쓰나요?"와 같은 질문), `q005`(0.62), `q008`(0.61). `--against-threshold`를 0.7로 올리면 뒤의 두 건은 빠진다. 기준을 어디에 둘지가 곧 판단이다.
4. `evaluate.py --predictions` 표(샘플 기준): base 키워드 일치율 0.400·형식 준수율 0.000·유사도 평균 0.116, lora 0.825·0.850·0.513. `--exclude q023 q005 q008`로 17문항만 채점하면 lora 0.794·0.824로 내려간다. 숫자는 가상 출력에서 나온 값이며 실제 모델과 다르다.
5. `eval-*.json`의 lora `items`: `q043`은 형식 통과·키워드 0·유사도 0.19(환각), `q024`는 거부(키워드 0·형식 위반), `q038`은 반복(형식은 통과), `q035`는 한글 비율 0.60으로 평균 0.78보다 낮다(언어 혼합), `q027`·`q031`은 형식 위반(내용은 맞음). 자동 지표가 무엇을 잡고 무엇을 놓치는지 보여 주는 문항들이다.
6. 모델 모드 첫 줄 `device=…, base=…, adapter=…`와 `eval-*.json`의 `system`: 10주차 `common.py`의 SYSTEM_PROMPT와 같은 문장이어야 공정한 비교다. `elapsed_sec`로 두 실행의 시간을 비교한다.
7. `make_sheet.py`가 만든 채점표: 점수·오류 유형·메모 열이 비어 있다. 자동 지표 열(키워드·형식)을 가리고 출력만 읽으며 채점하는 것이 3교시의 요점이다.

## GPU 없을 때 · 네트워크 없을 때

- **GPU 없음**: 1·3교시는 GPU가 필요 없다. 2교시는 `--predictions` 모드로 지표를 익히고, 모델 모드는 `--device cpu --limit 5 --max-new-tokens 96`으로 기준선만 몇 분 안에 돌린다. 어댑터까지 CPU로 돌리면 시간이 두 배가 되므로 `--skip-base --adapter …`로 어댑터만 따로 돌린다.
- **네트워크 없음**: 데이터는 전부 저장소 안에 있고 외부 다운로드가 없다. `uv sync`는 패키지 캐시가 필요하므로 수업 전에 한 번 실행해 둔다. 모델은 사전 캐시된 것을 `HF_HUB_OFFLINE=1`로 읽는다.
- **10주차 어댑터 없음**: `LORA_ADAPTER_DIR`를 비워 기준선만 생성·채점하고, 샘플 `lora.json`은 "가상 출력"이라고 표시한 채 채점 연습에만 쓴다. 짝의 어댑터 폴더를 복사해 써도 된다(가중치 수 MB, 커밋 금지).
- **datasets import가 느리거나 실패**: `split.py`만 `datasets`를 쓴다. 실패하면 `uv sync`가 끝났는지와 현재 폴더를 확인한다.

## 복사 후 변형

- 팀 데이터를 넣을 때는 `raw.jsonl` 형식(`id`, `instruction`, `output`, `keywords`, `source`)으로 바꾼다. `keywords`가 없으면 키워드 일치율은 항상 1.0이 되어 의미가 없다.
- 답변 형식이 다르면 `metrics.py`의 `FORMAT_HEAD`·`FORMAT_MID`·`FORMAT_TAIL`·`MAX_CHARS`를 바꾼다. 10주차 학습 데이터와 같은 형식이어야 형식 준수율이 "학습이 됐는가"를 잰다.
- 개인정보 패턴을 추가할 때는 `pii_check.py`의 `PATTERNS`에 넣고 `--action report`로 오탐부터 본다. "4자리 이상 숫자" 같은 넓은 패턴은 포트 번호 `11434` 같은 값도 잡는다.
- `outputs/`는 Git에 넣지 않는다. 제출 증거로 쓸 JSON·채점표는 `evidence/week11/`로 복사해 커밋한다.
