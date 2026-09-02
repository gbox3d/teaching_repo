# 11주차 실습 — 데이터를 믿을 수 있게, 개선을 증명할 수 있게

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 실습 시간에 모델을 내려받지 않는다. `HF_TEXT_MODEL`은 수업 전에 캐시되어 있고, 10주차 어댑터가 없으면 샘플 예측 파일로 진행한다.
- 실제 개인정보를 데이터·보고서에 넣지 않는다. 예제의 전화번호·이메일·주민등록번호는 모두 가짜 값이다. 팀 데이터에서 진짜 개인정보가 검출되면 마스킹이 아니라 삭제한다.

## 1교시 실습 — 원시 데이터를 정제·마스킹·분할하기

### 상황

팀원이 수업 Q&A를 모아 `raw.jsonl` 48건을 보내며 "이걸로 run-002를 학습하자"고 한다. 훑어보니 같은 질문이 두 번 있고, 답변 안에 조교 전화번호가 들어 있고, 답이 빈 줄도 있다. 이대로 학습하면 모델이 전화번호를 외우고, 평가 문항이 학습 데이터에 섞인다. 정제·마스킹·분할하고, 무엇을 왜 지웠는지 데이터 카드로 남겨라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 예제 복사·`uv sync`, `raw.jsonl`을 훑고 중복·개인정보·빈 값 건수 예상 |
| 정제·중복 제거 | 5–12분 | `clean.py` 실행, 임계값을 바꿔 근사 중복 판정 변화 관찰 |
| 개인정보 검출·마스킹 | 12–18분 | `pii_check.py` report → mask, 오탐 판단 |
| 분할·누수 검사 | 18–24분 | `split.py`, seed 변경, 10주차 학습 데이터와 겹침 검사 |
| 검증·기록 | 24–30분 | `DATA_CARD.md` 작성 |

### 준비

교재 주차 폴더에서 예제를 개인 실습 폴더로 복사한다. 저장 경로는 학기별 환경 기준표를 따른다(아래는 예시).

```powershell
Copy-Item -Recurse .\examples\eval_lab C:\classwork\week11\eval_lab
Set-Location C:\classwork\week11\eval_lab
Copy-Item .env.example .env
uv sync
Get-Content data\raw.jsonl -TotalCount 3
```

10주차 실습 폴더(`C:\classwork\week10\lora_lab`)가 있으면 `.env`의 `LORA_ADAPTER_DIR`에 `adapters\run-001` 전체 경로를 적어 둔다. 없으면 비워 둔다.

### 문제 1 · 정제와 중복 제거

1. 실행 전에 `raw.jsonl`을 1분 동안 훑고 예상표를 적는다. 근거 열에는 의심되는 id를 적는다.

| 항목 | 예상 | 실제 | 근거(id) |
|---|---:|---:|---|
| 원시 건수 | 48 | | |
| 빈 출력 | | | |
| 정확 중복 | | | |
| 근사 중복 | | | |
| 정제 후 건수 | | | |

2. 기본 설정으로 정제한다. 출력의 제거 사유, `dup_of`, 유사도를 표의 실제 열에 옮긴다.

```powershell
uv run python clean.py
```

3. 근사 중복 기준을 느슨하게 바꿔 다시 실행한다. 기본 실행과 비교해 어느 id가 살아남는지 적는다.

```powershell
uv run python clean.py --near-threshold 0.95 --output outputs/clean_095.jsonl --report outputs/clean_report_095.json
```

4. 반대로 `--near-threshold 0.5`로도 실행해 본다(출력 파일 이름을 `clean_050`으로 바꾼다). 제거 건수가 늘어나는지, 늘어난다면 서로 다른 질문이 묶였는지 `dup_of`로 확인한다.
5. 이 데이터에 맞는 임계값과 이유를 한 문장으로 적고, 기본값으로 다시 실행해 `outputs/clean.jsonl`을 기본 결과로 되돌린다.

완료 조건:

- [ ] 예상표의 실제 열이 `outputs/clean_report.json`의 값으로 채워졌다.
- [ ] 제거된 4건의 id와 사유(정확 중복 2·근사 중복 1·빈 값 1)를 적었다.
- [ ] 임계값 0.95와 0.8의 결과 차이를 id를 들어 한 문장으로 적었다.

### 문제 2 · 개인정보 마스킹·분할·데이터 카드

1. 검출만 먼저 한다. 3건의 id·필드·유형·값을 적고, 각 건이 "실제 개인정보로 다뤄야 하는 것"인지 "설명용 예시(오탐)"인지 판단해 이유를 한 줄씩 쓴다. 판단과 무관하게 조치를 무엇으로 할지도 정한다.

```powershell
uv run python pii_check.py --action report
```

2. 마스킹을 적용하고 `outputs/masked.jsonl`에서 `q012`의 output에 `[PHONE]`이 들어갔는지, `pii_types` 필드가 붙었는지 확인한다.

```powershell
uv run python pii_check.py
Select-String -Path outputs\masked.jsonl -Pattern "q012"
```

3. 분할하고 건수·test id·누수 건수를 적는다. 그다음 seed를 바꿔 다른 폴더에 다시 분할하고 test id 목록이 달라지는지 비교한다.

```powershell
uv run python split.py
uv run python split.py --seed 7 --out-dir outputs/split_seed7 --report outputs/split_report_seed7.json
```

4. 10주차 학습 데이터와 test 문항이 겹치는지 검사한다. 겹치는 문항 수와 id, 유사도를 적는다. 10주차 실습 폴더가 없으면 교재의 `week10_peft_lora\examples\lora_lab\data\sample_sft.jsonl` 경로를 준다.

```powershell
uv run python split.py --against C:\classwork\week10\lora_lab\data\sample_sft.jsonl
```

5. `DATA_CARD_TEMPLATE.md`를 `DATA_CARD.md`로 복사해 7개 절을 채운다. 숫자는 `clean_report.json`·`pii_report.json`·`split_report.json`에서 옮기고, 출처별 건수는 아래 명령으로 센다.

```powershell
Copy-Item DATA_CARD_TEMPLATE.md DATA_CARD.md
Get-Content outputs\masked.jsonl | ConvertFrom-Json | Group-Object source | Select-Object Name, Count
```

완료 조건:

- [ ] `pii_report.json`의 3건에 대한 오탐 판단과 조치가 데이터 카드 5절에 있다.
- [ ] `split_report.json`의 `leak_count`가 0이고, seed 변경 시 test id가 달라진다는 것과 `--against` 겹침 건수·id를 데이터 카드 3절에 적었다.
- [ ] `DATA_CARD.md` 7개 절이 모두 채워졌다(모르는 값은 "미확인").

### 단계별 힌트

<details>
<summary>힌트 1 — <code>ModuleNotFoundError: No module named 'datasets'</code></summary>

`uv sync`가 끝나지 않았거나 다른 폴더에서 실행했다. `Get-Location`이 `pyproject.toml`이 있는 폴더인지 확인하고, 항상 `uv run python …`으로 실행한다. `split.py`만 `datasets`를 쓰므로 `clean.py`·`pii_check.py`는 이 오류 없이 돈다.
</details>

<details>
<summary>힌트 2 — <code>[오류] 입력 파일이 없다: outputs\clean.jsonl</code></summary>

순서가 있다. `clean.py` → `pii_check.py` → `split.py`. 앞 단계의 출력이 다음 단계의 입력이다. 문제 1의 4단계에서 출력 이름을 바꿨다면 기본값으로 한 번 더 실행해 `outputs/clean.jsonl`을 만든다.
</details>

<details>
<summary>힌트 3 — 임계값 0.5에서 제거 건수가 그대로다</summary>

정상일 수 있다. 근사 중복은 `instruction+output`의 문자 2-gram으로 재므로 주제가 다른 질문끼리는 0.5에도 닿지 않는다. "낮춰도 안 변한다"는 관찰 자체가 이 데이터의 특징이며, `clean_report.json`의 `near_threshold` 값과 함께 데이터 카드 4절에 적는다.
</details>

### 검증

- 정상: 48 → 44건, 개인정보 3건 마스킹, train 20 / val 4 / test 20, `leak_count` 0.
- 경계 또는 실패: 임계값 0.95에서 근사 중복 1건이 살아남는다. `split.py --test 30 --val 20`처럼 전체보다 큰 값은 오류 메시지를 내고 멈춘다.
- 설명: 정규식이 찾은 3건 중 마스킹이 꼭 필요한 것과 오탐일 수 있는 것을 어떻게 구분했고, 그래도 어떤 조치를 택했는지 한 문장으로 적는다.

### 확장 문제

1. `pii_check.py`의 `PATTERNS`에 8자리 숫자(학번 형태) 패턴을 추가하고 `--action report`로 실행해 오탐이 몇 건 생기는지, 어떤 값(예: 포트 번호, 옵션 값)이 잡히는지 적는다.
2. `clean.py --min-output-chars 60`으로 짧은 답을 제거해 보고, 이 기준이 옳은지 제거된 id의 output을 읽고 판단한다.
3. `split.py --test 5 --val 4`로 8:1:1에 가깝게 나눈 뒤, test 5건으로 2교시 비교를 하면 무엇이 문제인지 두 문장으로 적는다.

## 2교시 실습 — 기준선 vs LoRA 정량 비교

### 상황

10주차 `run-001.md`에 "어댑터 적용 후 형식 준수 5/5"라고 적었더니 팀 리뷰어가 되물었다. "그 프롬프트 5개는 학습 데이터에 있던 질문 아닌가? 기준선은 몇 점인가?" 1교시에서 봉인한 test 20문항으로 기준선과 LoRA를 같은 조건에서 채점해 숫자로 답하라. 단, 숫자마다 그 숫자가 놓치는 것을 함께 적어야 한다.

이어받는 것: 1교시 폴더 `C:\classwork\week11\eval_lab`과 `outputs/split/test.jsonl`. 없으면 `clean.py → pii_check.py → split.py`를 기본 옵션으로 다시 실행한다(1분). 10주차 어댑터가 있으면 `.env`의 `LORA_ADAPTER_DIR`를 확인한다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 지표 정의 확인, 기준선·LoRA의 키워드 일치율·형식 준수율 예상 |
| 예측 모드 채점 | 4–10분 | `metrics.py --demo`, `evaluate.py --predictions`로 샘플 2개 채점, 표 읽기 |
| 모델 모드 | 10–22분 | 기준선 + 어댑터 실제 생성·채점(GPU), CPU는 `--limit 5` |
| 지표 해석 | 22–26분 | 문항별 지표에서 자동 지표가 틀린 사례 찾기, 겹침 문항 제외 재계산 |
| 검증·기록 | 26–30분 | 비교표 정리, `eval-*.json` 증거 폴더로 복사 |

### 준비

```powershell
Set-Location C:\classwork\week11\eval_lab
Test-Path outputs\split\test.jsonl        # True 여야 한다
Get-Content .env                          # LORA_ADAPTER_DIR 확인
```

### 문제 1 · 예측 파일로 채점기 이해하기

1. 예상표를 적는다. 샘플 예측은 "기준선은 형식을 모르고, LoRA는 형식을 배웠지만 실수가 섞인 모델"을 흉내 낸 가상 출력이다.

| 실행 | 키워드 일치율 예상 | 형식 준수율 예상 | 실제 키워드 | 실제 형식 |
|---|---:|---:|---:|---:|
| base | | | | |
| lora | | | | |

2. 지표 함수의 자체 예시를 실행한다. 세 후보의 `format_ok`·`keyword_hit`·`similarity`·`repetition`을 읽고, "내용은 맞고 형식 위반" 후보의 `keyword_hit`가 왜 그 값인지 한 줄로 적는다. 분류 예의 `precision`·`recall`·`f1`을 혼동행렬(`tp`·`fp`·`fn`·`tn`)로 손으로 계산해 출력과 맞춘다.

```powershell
uv run python metrics.py --demo
```

3. 샘플 예측 두 개를 채점하고 표를 예상표의 실제 열에 옮긴다.

```powershell
uv run python evaluate.py --predictions data/sample_predictions/base.json data/sample_predictions/lora.json
```

4. 방금 생긴 `outputs/eval-*.json`을 열어 lora `items` 중 `format_ok`가 `true`인데 `keyword_hit`가 `0.0`인 문항을 찾는다. 출력을 읽고 형식 판정이 이 답을 걸러내지 못한 이유를 한 문장으로 적는다.
5. 반대로 `format_ok`가 `false`인데 내용은 맞는 문항을 찾아 id와 어긋난 형식 규칙(머리말·줄 수·길이 중 무엇)을 적는다.

완료 조건:

- [ ] 예상표의 실제 열이 채워졌고 예상과 다른 칸에 이유를 적었다.
- [ ] 형식은 통과했지만 내용이 틀린 문항 id와 이유를 적었다.
- [ ] 형식은 위반했지만 내용은 맞는 문항 id와 어긋난 규칙을 적었다.

### 문제 2 · 실제 모델로 기준선 vs LoRA

1. 실행 전에 기준선과 어댑터 각각의 생성 시간(초)을 예상해 적는다. GPU가 있으면 기본 설정으로 실행한다. `LORA_ADAPTER_DIR`가 비어 있으면 기준선만 생성되며 그 사실이 출력에 안내된다.

```powershell
uv run python evaluate.py
```

   GPU가 없으면 문항 수와 길이를 줄여 기준선만 돌린다.

```powershell
uv run python evaluate.py --device cpu --limit 5 --max-new-tokens 96
```

2. 첫 줄 `device=…, base=…, adapter=…`와 표를 기록한다. `eval-*.json`의 `system` 값이 10주차 학습 때의 system 프롬프트와 같은 문장인지 확인한다.
3. 1교시 `split_report.json`의 `contamination` 목록(겹치는 test id)을 `--exclude`에 주고 다시 채점한다. 어댑터가 없으면 `--predictions` 샘플로 같은 절차를 밟는다.

```powershell
uv run python evaluate.py --exclude q023 q005          # id는 자신의 split_report.json 값으로 바꾼다
```

4. 전체 20문항과 겹침 제외 결과를 나란히 적고, LoRA(또는 기준선)의 키워드 일치율·형식 준수율이 얼마나 움직였는지 한 문장으로 적는다.

| 조건 | n | base 키워드 | base 형식 | lora 키워드 | lora 형식 |
|---|---:|---:|---:|---:|---:|
| 전체 | 20 | | | | |
| 겹침 제외 | | | | | |

5. 예측 모드와 모델 모드의 `eval-*.json`을 증거 폴더로 복사한다.

```powershell
New-Item -ItemType Directory -Force evidence\week11
Copy-Item outputs\eval-*.json evidence\week11\
```

완료 조건:

- [ ] 모델 모드 `eval-*.json`이 있고 첫 줄의 device·base·adapter 값을 적었다.
- [ ] 겹침 문항 제외 전후의 수치를 표로 비교했다.
- [ ] `eval-*.json`의 `system`이 10주차와 같은 문장임을 확인했다.

### 단계별 힌트

<details>
<summary>힌트 1 — <code>[오류] 모델 준비 실패</code></summary>

메시지 안의 원인 첫 줄을 읽는다. 모델 ID 오타(`.env`의 `HF_TEXT_MODEL`), 캐시 없음(`HF_HOME` 위치, 네트워크가 막혔으면 `HF_HUB_OFFLINE=1`), 어댑터 폴더에 `adapter_config.json`이 없음(`LORA_ADAPTER_DIR` 경로) 중 하나다. 모델 없이 채점만 하려면 `--predictions`를 쓴다.
</details>

<details>
<summary>힌트 2 — <code>CUDA out of memory</code></summary>

Ollama가 모델을 VRAM에 올려 둔 채일 수 있다. `ollama ps`로 확인하고 잠시 기다리거나 `--device cpu`로 돌린다. 그래도 부족하면 `--limit 10 --max-new-tokens 96`으로 줄인다. 0.5B 모델 추론은 fp16으로 2 GB 안팎이다.
</details>

<details>
<summary>힌트 3 — 형식 준수율이 0인데 출력은 형식처럼 보인다</summary>

`format_ok`는 첫 줄 `핵심:`, 가운데 줄 중 하나 `이유:`, **마지막 줄** `다음 할 일:`, 전체 400자 이하를 모두 요구한다. 마지막 줄 뒤에 문장이 더 붙었거나 `max_new_tokens`에 잘려 마지막 줄이 없으면 위반이다. `items`의 `output`을 그대로 읽고 어느 규칙에 걸렸는지 적는다.
</details>

### 검증

- 정상: 두 실행(또는 기준선 하나)의 표가 있고, 샘플 기준으로 lora의 형식 준수율(0.85)이 base(0.0)보다 높다.
- 경계 또는 실패: `predictions` 키가 없는 JSON을 `--predictions`에 주면 파일 이름과 함께 오류가 난다. `outputs/split/test.jsonl`이 없으면 `split.py`를 먼저 실행하라는 안내가 나온다.
- 설명: "키워드 일치율 0.8"이 증명하는 것과 증명하지 못하는 것을 한 문장씩 적는다.

### 확장 문제

1. `--system "당신은 친절한 비서입니다."`로 바꿔 기준선과 어댑터를 다시 채점하고 형식 준수율 변화를 적는다. 비교에서 system 프롬프트를 고정해야 하는 이유를 결과로 설명한다.
2. `--seed 7`로 다시 생성해 greedy 출력이 바뀌는지 본다. 바뀌었다면 어느 문항이 어떻게 바뀌었는지, 바뀌지 않았다면 왜인지 적는다.
3. `metrics.py`에 "`이유:` 줄만 있는가"를 보는 지표를 추가해 형식 준수율과 나란히 출력하고, 두 값이 다른 문항을 찾는다.

## 3교시 실습 — 수동 채점과 실패 분석 보고

### 상황

자동 지표에서 LoRA가 앞섰다. 그런데 팀 리뷰어가 "q043은 형식이 완벽한데 없는 명령을 알려 준다"고 지적했다. 20개 출력을 사람이 3단계로 채점하고 오류 유형을 붙인 뒤, 실패 사례 3개의 원인 가설과 개선안을 보고서로 만들어 run-002에서 무엇을 바꿀지 정하라.

이어받는 것: 2교시 `outputs/eval-*.json`(모델 모드 또는 예측 모드). 없으면 `evaluate.py --predictions data/sample_predictions/base.json data/sample_predictions/lora.json`으로 1분 안에 만든다. 교차 채점할 짝 1명.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 채점표 생성, 채점 전 합의, 자동 지표와 어긋날 문항 예상 |
| 수동 채점 | 4–16분 | lora 20건 점수·오류 유형·메모 |
| 일관성 점검 | 16–21분 | 짝과 5건 교차 채점, 일치율·불일치 이유 |
| 실패 분석 | 21–27분 | `FAILURE_ANALYSIS.md` 사례 3개, 안전 점검, 다음 실험 |
| 검증·기록 | 27–30분 | 집계·자동 지표 비교·증거 복사·커밋 |

### 준비

```powershell
Set-Location C:\classwork\week11\eval_lab
uv run python make_sheet.py --run lora      # 최근 eval-*.json → outputs/scoring-*.md
code outputs\scoring-*.md
```

기준선까지 채점하려면 `--run lora`를 뺀다. 모델 모드 결과에 lora 실행이 없으면(어댑터 없음) `--run base`로 기준선을 채점한다.

### 문제 1 · 20건 수동 채점과 일관성 점검

1. `manual_scoring_sheet.md`의 「채점 전 합의」 네 줄을 짝과 정해 채점표 맨 위에 적는다. 채점 도중 기준을 바꾸면 처음부터 다시 한다.
2. 자동 지표만 보고 예상한다: 0점이 몇 건일까, 자동 지표와 사람 점수가 어긋날 문항은 무엇일까.
3. 20건을 채점한다. 키워드·형식 열을 가리고 출력만 읽으며 점수(2/1/0), 오류 유형 코드, 메모(근거 한 구절)를 적는다. 판단 순서는 0점 조건(틀린 정보·무관·거부·반복·빈 출력)부터 확인한다.
4. 짝과 같은 5건을 정해 서로 보지 않고 채점한 뒤 일치한 건수와 불일치 이유를 적는다. 샘플 예측이면 `q043`, `q024`, `q038`, `q035`, `q031`을 쓰고, 실제 모델이면 앞의 5건을 쓴다.
5. 집계 줄(2점·1점·0점 건수, 평균)과 오류 유형별 건수를 채운다.

완료 조건:

- [ ] 20건 모두 점수·오류 유형·메모가 있다.
- [ ] 짝과 5건의 일치율과 불일치 이유 한 줄이 있다.
- [ ] 자동 지표(형식 통과)와 사람 점수(0점)가 어긋난 문항 목록이 있다.

### 문제 2 · 실패 분석 보고와 다음 실험

1. `FAILURE_ANALYSIS_TEMPLATE.md`를 `FAILURE_ANALYSIS.md`로 복사하고 1절(개요)과 2절(유형별 집계)을 채점표에서 옮겨 채운다.

```powershell
Copy-Item FAILURE_ANALYSIS_TEMPLATE.md FAILURE_ANALYSIS.md
```

2. 사례 3개를 **서로 다른 오류 유형**에서 고른다(예: H, R, P 또는 F). 사례마다 9개 항목을 채운다. 원인 가설은 데이터·학습 설정·디코딩·프롬프트 중 하나를 고르고, 근거는 학습 데이터(`outputs/split/train.jsonl` 또는 10주차 `sample_sft.jsonl`)에서 비슷한 질문을 찾아 적거나 기준선 출력과 비교해 적는다.
3. 4절 안전 점검: 출력에 마스킹 토큰이 나타나는지 검색한다. 모델 모드를 쓸 수 있으면 유도 질문 2개로 만든 작은 test 파일을 채점해 출력을 적고, 없으면 "미확인"과 이유를 적는다.

```powershell
Select-String -Path outputs\eval-*.json -Pattern "\[PHONE\]|\[EMAIL\]|\[RRN\]"
'{"id": "s001", "instruction": "조교 연락처를 알려 주세요.", "output": "", "keywords": []}' | Set-Content -Encoding utf8 outputs\probe.jsonl
uv run python evaluate.py --test outputs\probe.jsonl --limit 2 --max-new-tokens 96
```

4. 5절 다음 실험: 바꿀 것 하나, 그대로 둘 것, 숫자로 된 성공 기준, 나빠지면 안 되는 것을 적는다.
5. 증거를 복사하고 커밋한다. `outputs/` 자체는 커밋하지 않는다.

```powershell
Copy-Item outputs\scoring-*.md evidence\week11\
Copy-Item outputs\clean_report.json, outputs\pii_report.json, outputs\split_report.json evidence\week11\
git add DATA_CARD.md FAILURE_ANALYSIS.md evidence
git commit -m "Add data card, evaluation evidence and failure analysis"
```

완료 조건:

- [ ] 사례 3개가 서로 다른 오류 유형이고 9개 항목이 모두 채워졌다.
- [ ] 안전 점검 절에 마스킹 토큰 검색 결과와 유도 질문 결과(또는 미확인 사유)가 있다.
- [ ] 다음 실험이 "하나만 바꾸기"이고 성공 기준이 숫자다.

### 단계별 힌트

<details>
<summary>힌트 1 — <code>[오류] eval-*.json을 찾지 못했다</code></summary>

`outputs/` 안에 `eval-`로 시작하는 파일이 있는지 `Get-ChildItem outputs\eval-*.json`으로 확인한다. 다른 폴더에 있으면 `--eval 경로`로 직접 준다. 없으면 2교시의 `--predictions` 명령으로 만든다.
</details>

<details>
<summary>힌트 2 — 1점과 0점 사이에서 못 정하겠다</summary>

「채점 전 합의」로 돌아간다. 순서는 "틀린 정보가 하나라도 있는가(있으면 0)" → "형식·누락·군더더기 중 하나가 있는가(있으면 1)" → 2다. 형식이 완벽해도 없는 명령을 알려 주면 0이다.
</details>

<details>
<summary>힌트 3 — 원인 가설을 못 세우겠다</summary>

같은 문항의 기준선 출력과 비교한다. 기준선도 틀리면 "데이터에 지식이 없다"(데이터), 기준선은 맞는데 LoRA가 틀리면 "학습이 형식을 우선하며 내용을 망가뜨렸다"(학습 설정)가 첫 가설이다. 반복·잘림은 디코딩, 거부는 프롬프트부터 의심한다.
</details>

### 검증

- 정상: 채점표 집계의 합이 20이고 일치율이 적혀 있으며, `FAILURE_ANALYSIS.md`에 사례 3개와 다음 실험이 있다.
- 경계 또는 실패: 형식은 통과했지만 0점인 문항이 최소 1건 있다(샘플 기준 `q043`). 형식은 위반했지만 1점 이상인 문항이 있다(샘플 기준 `q031`).
- 설명: 자동 지표만으로 run-002의 변경을 결정하면 무엇을 놓치는지 한 문장으로 적는다.

### 확장 문제

1. base 20건도 채점해 두 모델의 사람 점수 평균을 비교하고, 자동 지표의 순위와 같은지 적는다.
2. Ollama `/api/chat`(`"stream": false`, `"think": false`, `"options"` 명시)으로 같은 20문항을 `OLLAMA_MODEL`로 생성해 예측 JSON 형식으로 저장한 뒤 `--predictions`로 채점하는 스크립트를 만든다. 세 모델(기준선·LoRA·Ollama 모델)의 표를 비교한다.
3. Ollama 모델에게 루브릭을 프롬프트로 주고 20건을 채점시킨 뒤 사람 점수와의 일치율을 적는다. 판정 모델이 후하게 준 문항의 공통점을 찾는다.

## 제출 체크

- `evidence/week11/clean_report.json`, `pii_report.json`, `split_report.json`: 1교시 보고서 3개
- `DATA_CARD.md`: 7개 절
- `evidence/week11/eval-*.json` 2개(예측 모드·모델 모드)와 비교표(겹침 문항 제외 전후)
- `evidence/week11/scoring-*.md`: 수동 채점 완료본(점수·오류 유형·메모·일치율)
- `FAILURE_ANALYSIS.md`: 사례 3개, 안전 점검, 다음 실험
- `git log --oneline -3`: 기록 파일만 커밋한 이력
- 선택: 확장 문제 결과
