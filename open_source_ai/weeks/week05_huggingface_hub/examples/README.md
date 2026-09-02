# 5주차 예제 — Hub 캐시 보고, pipeline 첫 추론, datasets 살펴보기

## 파일 구성

| 파일 | 역할 | 쓰는 교시 |
|---|---|---|
| `model_cards_template.md` | 모델 3개 예상표·분석표(13행)·판정·캐시 보고 양식. `model_cards.md`로 복사한다 | 1교시 |
| `SOURCES_template.md` | 출처 기록표(이름·종류·URL·revision·SPDX·용도·변경 내용)와 조건 요약. `SOURCES.md`로 복사한다 | 3교시 |
| `hf_explore/` | uv 프로젝트. 아래 파일을 담는다 | 1·2·3교시 |
| `hf_explore/pyproject.toml` | 의존성 `torch`(CUDA 인덱스), `transformers`, `datasets`, `huggingface_hub`, `python-dotenv`. 버전은 고정하지 않는다 | |
| `hf_explore/hf_env.py` | `.env` 읽기(빈 값 정리), 캐시 위치 결정, 캐시의 commit hash 조회, Hub 오류 문장, JSON 저장 도우미 | 공통 |
| `hf_explore/precache.py` | 수업 전 모델 스냅샷(카드 포함)·데이터셋 카드 사전 캐시. 강의자·조교용 | 수업 전 |
| `hf_explore/cache_report.py` | `scan_cache_dir()` 캐시 보고, 파라미터 수 → 용량 암산, Hub 파일 합계·sha 조회와 캐시 비교. `outputs/cache_report-*.json` | 1교시 |
| `hf_explore/pipeline_demo.py` | 감성 분류(`--task cls`)·텍스트 생성(`--task gen`). `model=`·`revision=`·`device=` 명시, 로드·워밍업·추론 시간과 commit hash 기록. `outputs/pipeline-*.json` | 2교시 |
| `hf_explore/dataset_peek.py` | `load_dataset`으로 로컬 jsonl과 Hub 데이터셋을 같은 API로 열어 필드·건수·샘플·카드 라이선스 기록. `outputs/dataset_peek-*.json` | 3교시 |
| `hf_explore/data/sample_qa.jsonl` | 자체 작성 한국어 Q&A 12건(수업 내용). 필드 `id`·`question`·`answer`·`topic`·`tags`(목록)·`week`(정수) | 3교시 |
| `hf_explore/data/README.md` | 위 샘플의 Dataset Card(YAML `license: cc-by-4.0` 포함). 카드와 실제 파일을 대조하는 연습 대상 | 3교시 |
| `hf_explore/.env.example` | 환경변수 예시. `.env`로 복사한다 | 1교시 |
| `hf_explore/.gitignore` | `.venv/`, `.env`, `outputs/` 등 커밋 제외 | |
| `hf_explore/README.md` | 짧은 실행 안내 | |

## 실행 방법

원본을 두고 개인 저장소 안의 실습 폴더에 복사한다. `$src`에는 교재 저장소의 이 `examples` 폴더 경로를 넣는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week05_huggingface_hub\examples"
$dst = "$HOME\osa-repo\week05"
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item -Recurse "$src\hf_explore" "$dst\hf_explore"
Copy-Item "$src\model_cards_template.md" "$dst\model_cards.md"
Copy-Item "$src\SOURCES_template.md" "$dst\SOURCES.md"
Set-Location "$dst\hf_explore"
Copy-Item .env.example .env
uv sync                          # 수업 전 한 번. torch 설치로 오래 걸린다
```

수업 전(강의자·조교, 기준 PC에서 먼저):

```powershell
uv run python hf_env.py          # 기본값·캐시 위치·오프라인 여부 확인
uv run python precache.py        # HF_CLS_MODEL·HF_TEXT_MODEL·HF_EMBED_MODEL 스냅샷(카드 포함)
uv run python precache.py --dataset klue/klue     # 3교시 카드 분석용 데이터셋 카드만(선택)
uv run python cache_report.py    # 받은 것과 commit hash 확인
```

1교시(캐시 보고):

```powershell
uv run python cache_report.py
uv run python cache_report.py --params 0.5 --bytes-per-param 2
uv run python cache_report.py --estimate Qwen/Qwen2.5-0.5B-Instruct        # 네트워크 허용 시
uv run python cache_report.py --cache-dir C:\없는폴더                        # 실패 경로
$LASTEXITCODE
uv run python cache_report.py --estimate 없는조직/없는모델                   # 실패 경로
```

2교시(pipeline):

```powershell
uv run python pipeline_demo.py --task cls --device cpu --tag cpu
uv run python pipeline_demo.py --task cls --device cuda --tag gpu
uv run python pipeline_demo.py --task gen --device cuda --max-new-tokens 120 --tag gpu
uv run python pipeline_demo.py --task gen --device cuda --gen-revision <출력의 commit_hash> --tag pinned
uv run python pipeline_demo.py --task gen --gen-revision 0000000             # 실패 경로 A
# .env 의 HF_HUB_OFFLINE=1 로 바꾼 뒤
uv run python pipeline_demo.py --task cls --cls-model 없는조직/없는모델       # 실패 경로 B, 끝나면 0 으로 되돌린다
```

3교시(datasets):

```powershell
uv run python dataset_peek.py
uv run python dataset_peek.py --streaming --n 3 --max-chars 40
uv run python dataset_peek.py --file data\없음.jsonl                          # 실패 경로
uv run python dataset_peek.py --hub-id klue/klue --config ynat --split train --streaming --n 5   # 네트워크·허용 시
uv run python dataset_peek.py --hub-id klue/klue --split train --streaming   # config 누락 실패 경로
```

`uv run`은 `.venv`가 없으면 만들고 의존성을 설치한다. 수업 전에 `uv sync`와 `precache.py`를 마쳐 두면 실습 중 네트워크 없이 1·2교시와 3교시 로컬 부분이 진행된다.

## 관찰 지점

1. `cache_report.py`의 저장소 폴더 이름은 `models--조직--이름`이고 그 아래 `snapshots/<commit hash>/`가 실제로 불러오는 파일이다. `refs`의 `main`이 어느 commit을 가리키는지 본다.
2. 암산(0.5B × 2바이트 ≈ 1 GB)과 실제 캐시 용량이 다르다. 가중치 형식(fp32·bf16), 토크나이저·설정 파일, 중복 형식(`.bin`과 `.safetensors`)이 차이를 만든다.
3. `--estimate`의 `sha`가 캐시의 commit hash와 같으면 "지금 캐시가 main과 같은 상태"라는 뜻이다. 다르면 캐시가 낡았거나 다른 revision을 받은 것이다.
4. `pipeline_demo.py`는 첫 호출(워밍업)과 두 번째 호출(추론)의 시간을 따로 적는다. 로드 시간은 디스크·메모리, 추론 시간은 장치에 더 민감하다.
5. 분류 결과의 `id2label`이 `positive/neutral/negative`인지 `LABEL_0`인지 본다. 라벨 이름은 모델 config가 정하며 카드에서 뜻을 찾는다.
6. 생성 결과는 `do_sample=False`라서 같은 장치·dtype·revision이면 같은 답이 나온다. 장치나 dtype이 바뀌면 답이 달라질 수 있다.
7. 실패 경로는 스택 트레이스 대신 한 문장과 종료 코드 1을 내고, `outputs/`에 `error` 항목이 있는 JSON을 남긴다.
8. `dataset_peek.py`에서 `info.license`는 비어 있어도 `data/README.md` 카드의 `license`는 읽힌다. 라이선스는 `load_dataset` 객체가 아니라 카드가 갖고 있다.
9. `--streaming`이면 건수가 "알 수 없음"이고 `features`가 첫 행에서 추론될 수 있다. 큰 데이터의 앞 5개만 볼 때 쓰는 모드다.

## GPU 없을 때·네트워크 없을 때

- GPU가 없거나 `torch.cuda.is_available()`이 `False`면 `--device cpu`로 같은 절차를 진행한다. 2교시의 "CPU vs GPU" 비교는 "CPU 첫 실행 vs 두 번째 실행"으로 바꾸고, 생성은 `--max-new-tokens 60`으로 줄인다.
- `--device cuda`를 GPU 없는 PC에서 실행하면 한 문장 메시지와 종료 코드 1이 나온다. 이것도 기록할 실패 경로다.
- 네트워크가 없어도 `uv sync`와 `precache.py`가 수업 전에 끝났으면 1교시(`--estimate` 제외), 2교시 전체, 3교시 로컬 부분이 돈다. `.env`의 `HF_HUB_OFFLINE=1`로 두면 캐시만 쓴다.
- 카드 페이지를 열 수 없으면 `cache_report.py` 출력의 `snapshot_path` 아래 `README.md`(precache가 받은 카드 원문)를 VS Code로 연다.
- 3교시 공개 데이터셋 부분은 네트워크가 없으면 강의자가 나눠 준 카드 사본으로 진행하고, `dataset_peek.py --hub-id`는 실패 메시지만 기록한다.
- 실습실 공용 캐시를 쓰면 `.env`의 `HF_HOME` 줄의 주석을 풀고 안내받은 경로를 적는다. 빈 값은 "설정하지 않음"으로 처리된다.

## 복사 후 변형

- `pipeline_demo.py`의 `SAMPLE_SENTENCES`에 문장을 추가하거나 `--prompt`를 바꿔 4주차 Ollama 클라이언트(`chat.py`)와 같은 질문으로 비교한다.
- `--max-new-tokens`를 30·120·300으로 바꿔 추론 시간이 토큰 수에 비례하는지 본다.
- `data/sample_qa.jsonl`에 같은 형식의 Q&A 3건을 추가하고(실제 인물·기관 없이 수업 내용으로) `dataset_peek.py`의 건수·`tags` 자료형이 그대로인지 확인한다. `data/README.md`의 건수도 함께 고친다.
- `SOURCES.md`에 2주차 `license_matrix.md`의 의존 패키지 행을 옮겨 와 모델·데이터·코드가 한 표에 있게 만든다.
- `outputs/`는 커밋하지 않는다. 증거로 낼 값은 `model_cards.md`·`pipeline_report.md`·`SOURCES.md`에 옮겨 적는다.

## 기본값과 환경 기준표

| 환경변수 | 기본값 | 용도 |
|---|---|---|
| `HF_TEXT_MODEL` | `Qwen/Qwen2.5-0.5B-Instruct` | 2교시 텍스트 생성. 6·10주차에도 같은 값 |
| `HF_CLS_MODEL` | `lxyuan/distilbert-base-multilingual-cased-sentiments-student` | 2교시 감성 분류. 소형 다국어, 라벨 `positive/neutral/negative` |
| `HF_EMBED_MODEL` | `intfloat/multilingual-e5-small` | 6·7주차 임베딩. 이번 주에는 사전 캐시·카드 분석 대상 |
| `HF_HOME` | (설정 시) | Hugging Face 캐시 위치. 캐시는 `HF_HOME/hub` |
| `HF_HUB_OFFLINE` | `0` | `1`이면 네트워크 없이 캐시만 쓴다 |
| `HF_TOKEN` | (비움) | gated 모델 파일 접근 시에만. 값은 `.env`에만 둔다 |

모델 ID·revision·양자화·용량은 [학기별 환경 기준표](../../../../environment_baseline_template.md)에서 확정하며 위 값은 교재 검증용 기본값이다. 분류 모델은 카드의 `language` 목록에 한국어가 명시되어 있지 않을 수 있다. 한국어 문장의 점수가 영어보다 낮게 나오는 것 자체가 2교시 "카드의 언어 목록을 다시 본다"의 관찰 대상이며, 기준표에서 한국어 지원 모델로 바꿔도 코드는 그대로 동작한다. `uv.lock`은 만들지 않았다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.

## 자체 샘플 데이터

- `hf_explore/data/sample_qa.jsonl`: 교재 작성자가 수업 내용으로 직접 쓴 한국어 Q&A 12건. 라이선스 CC-BY-4.0(`data/README.md`). 실제 인물·기관·연락처 없음. 용도는 `datasets` API 연습과 10주차 LoRA 데이터 형식 예시.
- 3교시 공개 데이터셋 카드 분석 후보(강의자가 바꿔 지정할 수 있다): `klue/klue`의 `ynat` 구성, `HuggingFaceH4/no_robots`. 라이선스는 카드 본문에서 직접 확인한 값만 기록한다.
