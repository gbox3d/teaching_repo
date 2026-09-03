# 5주차 실습 — 공개 자원을 문서와 해시로 판단하라

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 실습 시간에 모델·데이터를 새로 내려받지 않는다. 사전 캐시된 모델과 예제의 로컬 샘플만 쓴다.
- Hugging Face 토큰은 `.env`에만 둔다. gated 모델은 카드만 읽고 파일을 받지 않는다.

## 1교시 실습 — 모델 카드 분석표와 캐시 보고

### 상황

팀이 "로컬 AI 도우미"에 쓸 후보 모델 세 개를 골라 왔다. 팀장은 내려받기 전에 "셋 다 우리 프로젝트(공개 저장소, 수업용)에 써도 되는지, 디스크는 얼마나 필요한지"를 한 장으로 정리해 달라고 한다. 카드를 읽고 판단 근거를 표로 남겨라. 이어받는 것: 4주차 개인 저장소와 `.env` 패턴.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 카드를 열기 전에 모델 3개의 라이선스·fp16 용량·한국어 지원을 예상 |
| 카드 읽기 | 4–16분 | 카드 3개에서 항목을 찾아 `model_cards.md` 분석표 채우기 |
| 캐시 보고 | 16–24분 | `cache_report.py` 실행, 캐시 위치·용량·commit hash 기록, 암산과 비교 |
| 검증·기록 | 24–30분 | 실패 경로 재현, 판정 문장 작성, commit |

### 준비

```powershell
# 교재 저장소 위치는 실습실 안내를 따른다. $src 와 $dst 는 예시다.
$src = "C:\teaching_repo\open_source_ai\weeks\week05_huggingface_hub\examples"
$dst = "$HOME\osa-practice\week05"   # 4주차까지 쓴 개인 저장소 안의 폴더로 바꾼다
New-Item -ItemType Directory -Force $dst | Out-Null
# 이미 있으면 건너뛴다. 하루가 바뀌어 이 블록을 다시 실행해도 채워 둔 문서가 템플릿으로 되돌아가지 않는다.
if (-not (Test-Path "$dst\hf_explore"))     { Copy-Item -Recurse "$src\hf_explore" "$dst\hf_explore" }
if (-not (Test-Path "$dst\model_cards.md")) { Copy-Item "$src\model_cards_template.md" "$dst\model_cards.md" }
if (-not (Test-Path "$dst\SOURCES.md"))     { Copy-Item "$src\SOURCES_template.md" "$dst\SOURCES.md" }
Set-Location "$dst\hf_explore"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv run python cache_report.py --help
```

`uv sync`(첫 실행 시 torch 설치)는 수업 전에 마쳐 둔다. 실습실 공용 캐시를 쓴다면 `.env`의 `HF_HOME` 줄의 주석을 풀고 안내받은 경로를 적는다.

### 문제 1 · 모델 카드 분석표

대상 모델은 `Qwen/Qwen2.5-0.5B-Instruct`, `intfloat/multilingual-e5-small`, 그리고 라이선스 제한이 있는 모델 1개(예: `meta-llama/Llama-3.2-1B-Instruct` 또는 `google/gemma-3-1b-it`, 강의자가 바꿔 지정할 수 있다)다.

1. 카드를 열기 전에 `model_cards.md`의 예상표에 세 모델의 라이선스, fp16 용량(파라미터 수 × 2바이트), 한국어 지원 여부를 예상해 적는다.
2. 브라우저에서 각 모델 페이지를 열고 카드 맨 위 YAML(`license`, `language`, `pipeline_tag`, `base_model`)을 분석표에 옮긴다. 별도 약관 파일이나 "동의" 버튼이 있으면 gated 칸에 표시한다.
3. 카드 본문에서 의도된 용도, 금지·제한 용도, 학습 데이터 공개 여부, 평가·한계·편향 서술을 찾아 **해당 절의 제목**과 함께 적는다. 항목이 없으면 "카드에 없음"이라고 적는다.
4. 라이선스 이름을 SPDX 식별자로 바꾼다. SPDX 목록에 없는 라이선스(Llama, Gemma 등)는 `LicenseRef-이름` 형태로 적고 핵심 조건을 한 줄로 요약한다.
5. 모델마다 "우리 프로젝트(공개 저장소, 수업용, 비상업)에 쓸 수 있는가"를 가능/조건부/불가로 판정하고 근거를 한 문장으로 쓴다.

완료 조건:

- [ ] 세 모델 모두 분석표의 13개 행이 채워졌거나 "카드에 없음"으로 표시되었다.
- [ ] 판정 3개에 각각 카드의 어느 절이 근거인지 적혀 있다.
- [ ] 예상표와 분석표의 차이 중 가장 큰 것 하나를 한 문장으로 설명했다.

### 문제 2 · 캐시 보고와 용량 추정

1. `uv run python cache_report.py`를 실행하고 캐시 위치, 총 용량, 저장소별 용량·파일 수·commit hash(12자리)를 `model_cards.md`의 캐시 보고 절에 옮긴다.
2. `uv run python cache_report.py --params 0.5 --bytes-per-param 2`로 암산값을 얻고, 실제 캐시 용량과 다른 이유를 한 문장으로 적는다.
3. 네트워크가 허용되면 `uv run python cache_report.py --estimate Qwen/Qwen2.5-0.5B-Instruct`로 Hub 파일 합계와 `sha`를 받아, `sha`가 캐시의 commit hash와 같은지 확인한다. 네트워크가 없으면 이 단계를 건너뛰고 그 사실을 적는다.
4. 실패 경로: `uv run python cache_report.py --cache-dir C:\없는폴더`와 `--estimate 없는조직/없는모델`을 각각 실행해 메시지 첫 줄과 종료 코드(`$LASTEXITCODE`)를 기록한다.

완료 조건:

- [ ] `outputs/cache_report-*.json`이 생겼고 commit hash를 문서에 옮겼다.
- [ ] 실패 경로 2개의 메시지를 각각 한 줄로 요약했다.

### 단계별 힌트

<details>
<summary>힌트 1 — 카드 페이지가 열리지 않는다(네트워크 없음)</summary>

`precache.py`로 사전 캐시한 모델은 `HF_HOME/hub/models--조직--이름/snapshots/<commit hash>/README.md`에 카드 원문이 있다. `cache_report.py` 출력의 경로를 따라가 VS Code로 연다. 카드가 없는 모델은 강의자가 나눠 준 사본을 쓴다.
</details>

<details>
<summary>힌트 2 — YAML의 license와 본문의 라이선스가 다르다</summary>

본문과 별도 파일(LICENSE, 약관 페이지)이 우선이다. YAML은 검색용 요약일 뿐이다. 둘이 다르면 분석표에 둘 다 적고 판정 근거는 본문 쪽을 쓴다.
</details>

<details>
<summary>힌트 3 — 캐시 폴더가 없다고 나온다</summary>

`.env`의 `HF_HOME`이 비어 있지 않은지, 경로 철자가 맞는지 본다. `HF_HOME`을 지정하지 않았다면 기본 위치(사용자 홈의 `.cache\huggingface\hub`)를 스캔한다. 아직 아무 모델도 받지 않은 PC라면 그 메시지가 정상이다.
</details>

### 검증

- 정상: `cache_report.py`가 저장소 목록과 commit hash를 출력하고 `outputs/cache_report-*.json`을 남긴다.
- 경계 또는 실패: 없는 폴더·없는 저장소를 지정하면 사람이 읽을 메시지와 종료 코드 1이 나온다.
- 설명: "카드의 `license` 한 줄만 보고 사용 가능 여부를 판정할 수 없는 이유"를 한 문장으로 쓴다.

### 확장 문제

1. `--estimate`의 `largest_files` 목록에서 가중치 파일 형식(safetensors인지 `.bin`인지)을 확인하고, 13주차에 다룰 "모델 파일 안전"과 어떤 관계가 있는지 한 문장으로 적는다.
2. 같은 모델의 다른 revision(브랜치 또는 이전 commit)을 `--estimate REPO --revision 해시`로 조회해 파일 합계가 달라지는지 본다.

## 2교시 실습 — pipeline으로 분류와 생성 실행하기

### 상황

팀원이 "모델은 받아 놨는데 실제로 돌아가는지, GPU가 CPU보다 얼마나 빠른지, 어떤 버전을 썼는지 기록해 달라"고 한다. 두 태스크를 실행하고 조건별 시간과 commit hash를 표로 남겨라. 이어받는 것: 1교시 `model_cards.md`의 모델 ID와 캐시 보고의 commit hash.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 5문장의 라벨, 한국어·영어 문장의 결과 차이, CPU/GPU 시간을 예상 |
| 분류 실행 | 4–12분 | `--task cls`를 CPU와 GPU에서 실행, 라벨·점수·시간 기록 |
| 생성 실행 | 12–20분 | `--task gen` 실행, commit hash로 revision 고정 후 재실행 |
| 실패·비교 | 20–25분 | 잘못된 revision·오프라인 실패 재현, 시간 비교표 작성 |
| 검증·기록 | 25–30분 | `pipeline_report.md` 완성, commit |

### 준비

1교시에 복사한 `hf_explore` 폴더에서 계속한다. 새로 시작하는 날이면 1교시의 준비 명령을 먼저 실행한다.

```powershell
Set-Location "$HOME\osa-practice\week05\hf_explore"
uv run python pipeline_demo.py --help
# -Force 는 이미 있는 파일을 빈 파일로 덮어쓴다. 없을 때만 만든다.
if (-not (Test-Path ..\pipeline_report.md)) { New-Item -ItemType File ..\pipeline_report.md | Out-Null }
```

### 문제 1 · 감성 분류를 두 장치에서

1. `pipeline_demo.py`의 `SAMPLE_SENTENCES` 5문장을 읽고, 각 문장의 라벨(positive/neutral/negative)과 "영어 문장과 한국어 문장 중 어느 쪽 점수가 높을지"를 예상해 적는다.
2. `uv run python pipeline_demo.py --task cls --device cpu`를 실행한다. 출력의 라벨·점수·로드·워밍업·추론 시간을 표에 옮긴다.
3. `uv run python pipeline_demo.py --task cls --device cuda`를 실행한다. GPU가 없는 PC는 `--device cpu`를 한 번 더 실행해 두 번째 실행의 로드 시간이 왜 달라지는지(또는 같은지) 적는다.
4. 출력 JSON의 `commit_hash`를 확인하고 1교시 캐시 보고의 해시와 같은지 비교한다.

완료 조건:

- [ ] 5문장의 라벨·점수가 `outputs/pipeline-*.json` 두 개(장치별)에 남았다.
- [ ] 예상과 다른 라벨이 있으면 카드의 언어 목록·라벨 정의와 연결해 한 문장으로 설명했다.

### 문제 2 · 생성 실행과 revision 고정

1. `uv run python pipeline_demo.py --task gen --device cuda --max-new-tokens 120`을 실행한다(GPU가 없으면 `--device cpu --max-new-tokens 60`). 답, 생성 토큰 수, tokens/s, 최대 VRAM을 기록한다.
2. 출력의 `commit_hash`를 복사해 `--gen-revision <해시>`로 다시 실행한다. `do_sample=False`이므로 답이 같아야 한다. 같은지 확인하고 다르면 그 이유를 적는다.
3. 실패 경로 A: `--gen-revision 0000000`으로 실행해 메시지 첫 줄을 기록한다.
4. 실패 경로 B: `.env`의 `HF_HUB_OFFLINE`을 `1`로 바꾸고 `--cls-model 없는조직/없는모델 --task cls`를 실행해 메시지 첫 줄을 기록한다. 끝나면 `0`으로 되돌린다.
5. `pipeline_report.md`에 아래 표를 채우고, 4주차 Ollama의 tokens/s와 비교한 한 문장을 덧붙인다.

```text
| 장치 | 태스크 | dtype | 로드(s) | 워밍업(s) | 추론(s) | 생성 토큰 | tokens/s | 최대 VRAM | commit hash |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| cpu  | cls | float32 |  |  |  | - | - | - |  |
| cuda | cls | float32 |  |  |  | - | - | - |  |
| cpu  | gen | float32 |  | - |  |  |  | - |  |
| cuda | gen | float16 |  | - |  |  |  |  |  |
```

완료 조건:

- [ ] 생성 답 1건과 revision 고정 재실행 결과가 기록되었다.
- [ ] 실패 경로 A·B의 메시지가 각각 한 줄로 요약되었다.
- [ ] 시간 비교표에서 "로드 시간과 추론 시간 중 어느 쪽이 장치에 더 민감한가"를 한 문장으로 적었다.

### 단계별 힌트

<details>
<summary>힌트 1 — CUDA 장치를 찾지 못했다고 나온다</summary>

`uv run python -c "import torch; print(torch.cuda.is_available(), torch.version.cuda)"`로 확인한다. `False`면 `pyproject.toml`의 CUDA 인덱스 태그와 드라이버가 환경 기준표와 맞는지 조교에게 확인하고, 이번 실습은 `--device cpu`로 진행한다.
</details>

<details>
<summary>힌트 2 — commit_hash가 null이다</summary>

일부 버전에서는 로드된 config에 해시가 남지 않는다. 그럴 때는 1교시 `cache_report.py` 출력의 commit hash를 쓴다. 두 값이 다르면 캐시에 revision이 두 개 있는 것이니 `refs`가 `main`인 쪽을 기록한다.
</details>

<details>
<summary>힌트 3 — 생성 결과가 두 번 실행에서 다르다</summary>

`do_sample=False`여도 장치(CPU/GPU)나 dtype이 다르면 부동소수 연산 순서 차이로 답이 달라질 수 있다. 같은 장치·같은 dtype에서 revision만 고정한 두 실행을 비교한다.
</details>

### 검증

- 정상: 두 태스크 모두 `outputs/pipeline-*.json`에 `commit_hash`, `load_seconds`, `infer_seconds`가 기록된다.
- 경계 또는 실패: 잘못된 revision과 오프라인 상태에서 사람이 읽을 메시지와 종료 코드 1이 나오고, JSON에 `error` 항목이 남는다.
- 설명: "첫 호출 시간을 시간 비교에 쓰지 않는 이유"를 한 문장으로 쓴다.

### 확장 문제

1. `--prompt`를 바꿔 같은 질문을 4주차 Ollama 클라이언트(`chat.py`)에도 보내고, 답의 길이·형식·tokens/s를 한 표로 비교한다.
2. `--max-new-tokens`를 30·120·300으로 바꿔 추론 시간이 토큰 수에 비례하는지 확인한다.

## 3교시 실습 — 데이터셋 살펴보기와 출처 기록표

### 상황

팀의 10주차 LoRA 학습에 쓸 데이터 후보를 찾는 중이다. 팀장이 "데이터 구조와 라이선스를 먼저 확인하고, 지금까지 쓴 모델·데이터의 출처를 한 표로 만들어 두자"고 한다. 자체 샘플과 공개 데이터셋 카드를 살펴보고 `SOURCES.md`를 완성하라. 이어받는 것: 2교시 `pipeline_report.md`의 모델 ID·commit hash.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 파일을 열지 않고 `sample_qa.jsonl`의 필드 구조를 예상 |
| 로컬 데이터 | 4–12분 | `dataset_peek.py` 기본 실행·스트리밍 실행, 구조·건수 기록 |
| 카드 읽기 | 12–20분 | 공개 데이터셋 1개의 Dataset Card 분석, 가능하면 스트리밍으로 5개 확인 |
| 출처 기록 | 20–26분 | `SOURCES.md`에 모델 2개 + 데이터 1개 작성 |
| 검증·기록 | 26–30분 | 실패 경로 재현, 조건 요약, commit |

### 준비

```powershell
Set-Location "$HOME\osa-practice\week05\hf_explore"
uv run python dataset_peek.py --help
```

새로 시작하는 날이면 1교시의 준비 명령을 먼저 실행한다.

### 문제 1 · 로컬 샘플의 구조 기록

1. `data/sample_qa.jsonl`을 열지 않은 채, 파일 이름과 3교시 슬라이드만 보고 필드 이름과 자료형을 예상해 적는다.
2. `uv run python dataset_peek.py`를 실행하고 필드 표, 건수, `info.license` 값, 샘플 5개를 기록한다. 예상과 다른 필드를 표시한다.
3. `uv run python dataset_peek.py --streaming --n 3 --max-chars 40`을 실행하고 건수 칸이 어떻게 달라졌는지, 왜 그런지 한 문장으로 적는다.
4. 실패 경로: `uv run python dataset_peek.py --file data\없음.jsonl`을 실행해 메시지와 종료 코드를 기록한다.

완료 조건:

- [ ] 필드 표에 `Value`와 `Sequence`(또는 `List`) 자료형이 각각 하나 이상 기록되었다.
- [ ] 스트리밍과 일반 로드의 건수 표시 차이를 설명했다.

### 문제 2 · 공개 데이터셋 카드와 SOURCES.md

1. 강의자가 지정한 공개 데이터셋(지정이 없으면 후보: `klue/klue`의 `ynat` 구성, 또는 `HuggingFaceH4/no_robots`) 페이지를 열어 Dataset Card에서 요약·출처, 구조(필드·split·건수), 수집·주석 방법, 개인정보 언급, 라이선스를 찾아 적는다. 라이선스는 카드에서 직접 확인한 값만 적되, 본문 절과 맨 위 YAML 중 **어디에서 찾았는지**를 함께 적는다. 본문 절이 `[Needs More Information]`이면 그 사실도 적는다.
2. 네트워크와 강의자의 허용이 있으면 `uv run python dataset_peek.py --hub-id <ID> --config <구성> --split train --streaming --n 5`로 앞 5개를 보고 카드의 필드·건수와 비교한다. 허용이 없으면 카드 기록만으로 진행하고 그 사실을 적는다.
3. 실패 경로: config가 필요한 데이터셋을 `--config` 없이 실행해 오류 메시지에 나열된 config 이름을 기록한다(오프라인이면 네트워크 오류 메시지를 대신 기록한다).
4. `SOURCES.md`에 2교시에서 쓴 모델 2개(분류·생성)와 데이터 1개(로컬 샘플 또는 공개 데이터셋)를 적는다. 버전 칸에는 commit hash, 라이선스 칸에는 SPDX 식별자, 용도 칸에는 이번 주의 실제 용도를 쓴다.
5. `SOURCES.md`의 조건 요약 절에 출처 표시·같은 조건 공유·상업 이용 제한·gated 여부를 항목별로 적고 commit한다.

완료 조건:

- [ ] Dataset Card 5개 항목 중 카드에 없는 항목이 "카드에 없음"으로 표시되었다.
- [ ] `SOURCES.md` 3행 모두 버전 칸이 commit hash 또는 revision이고 "최신"이라는 말이 없다.
- [ ] commit 메시지가 무엇을 기록했는지 드러낸다(예: `Add week05 model cards and SOURCES`).

### 단계별 힌트

<details>
<summary>힌트 1 — features가 비어 있거나 자료형이 str로만 나온다</summary>

스트리밍 모드에서는 라이브러리가 파일 전체를 읽지 않아 `features`가 비어 있을 수 있다. 예제는 그때 첫 행에서 파이썬 자료형을 추론한다. 정확한 `Value`/`Sequence` 표기가 필요하면 스트리밍 없이 실행한 결과를 쓴다.
</details>

<details>
<summary>힌트 2 — 데이터셋 카드에 라이선스가 두 개 이상 적혀 있다</summary>

원문 데이터와 주석(라벨)의 라이선스가 다른 경우가 있다. `SOURCES.md`에는 둘 다 적고, 더 제한적인 쪽을 기준으로 조건 요약을 쓴다.
</details>

<details>
<summary>힌트 3 — 모델의 commit hash를 어디서 가져와야 할지 모르겠다</summary>

2교시 `outputs/pipeline-*.json`의 `commit_hash`, 또는 1교시 `cache_report.py` 출력의 해시를 쓴다. 둘 다 없으면 브라우저의 Files and versions 탭에서 최신 commit의 해시를 복사하고, 그 사실을 변경 내용 칸에 적는다.
</details>

### 검증

- 정상: `dataset_peek.py`가 필드 표·건수·샘플을 출력하고 `outputs/dataset_peek-*.json`을 남긴다.
- 경계 또는 실패: 없는 파일, config 누락, 오프라인 상태에서 각각 다른 메시지와 종료 코드 1이 나온다.
- 설명: "라이선스가 CC-BY-4.0인 데이터라도 바로 쓸 수 없는 경우"를 한 문장으로 쓴다.

### 확장 문제

1. `data/sample_qa.jsonl`에 같은 형식의 Q&A 3건을 추가하고(실제 인물·기관 없이 수업 내용으로), `dataset_peek.py`의 건수와 `tags` 필드 자료형이 그대로인지 확인한다.
2. `SOURCES.md`에 2주차 `license_matrix.md`의 의존 패키지 행을 옮겨 와 모델·데이터·코드가 한 표에 있는 상태로 만든다.

## 제출 체크

- `model_cards.md`: 예상표, 모델 3개 분석표, 판정 3개, 캐시 보고 요약과 실패 경로 2개
- `pipeline_report.md`: 분류 5문장 결과, 생성 답 1건, revision 고정 재실행 결과, 시간 비교표, 실패 경로 A·B 요약
- `SOURCES.md`: 모델 2개 + 데이터 1개, 조건 요약
- 개인 저장소: 이번 주 commit 3개 이상, `.env`와 `outputs/`가 commit되지 않았음을 `git status`로 확인
- 선택: 확장 문제 결과
