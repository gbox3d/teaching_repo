# hf_explore — 5주차 예제 uv 프로젝트

Hugging Face 캐시를 스캔하고(`cache_report.py`), Transformers `pipeline`으로 분류·생성을 실행하고(`pipeline_demo.py`), `datasets`로 로컬 파일과 Hub 데이터셋을 같은 API로 여는(`dataset_peek.py`) 최소 예제다. 설명과 관찰 지점은 상위 [`../README.md`](../README.md)에 있다.

## 실행

```powershell
Copy-Item .env.example .env      # 값은 그대로 두어도 된다
uv sync                          # 의존성 설치(수업 전 한 번, torch 때문에 오래 걸린다)
uv run python precache.py        # 수업 전 강의자·조교가 모델을 미리 받는다
uv run python cache_report.py
uv run python pipeline_demo.py --task cls --device cpu
uv run python pipeline_demo.py --task gen --device cuda --max-new-tokens 120
uv run python dataset_peek.py
```

결과는 `outputs/cache_report-*.json`, `outputs/pipeline-*.json`, `outputs/dataset_peek-*.json`에 쌓인다(`.gitignore` 대상).

## 파일

| 파일 | 역할 |
|---|---|
| `hf_env.py` | `.env` 읽기, 캐시 위치 결정, commit hash 조회, 오류 문장, JSON 저장 도우미 |
| `precache.py` | 수업 전 모델 스냅샷·데이터셋 카드 사전 캐시(강의자·조교용) |
| `cache_report.py` | `scan_cache_dir()` 캐시 보고, 파라미터 수 → 용량 암산, Hub 파일 합계·sha 조회 |
| `pipeline_demo.py` | 감성 분류·텍스트 생성. `model=`·`revision=`·`device=` 명시, 로드·워밍업·추론 시간 기록 |
| `dataset_peek.py` | `load_dataset`으로 로컬 jsonl·Hub 데이터셋 열기, 필드·건수·샘플·카드 라이선스 기록 |
| `data/sample_qa.jsonl` | 자체 작성 한국어 Q&A 12건(수업 내용). 외부 다운로드 없음 |
| `data/README.md` | 위 샘플의 Dataset Card(YAML 메타데이터 포함) |
| `.env.example` | 환경변수 예시. `.env`로 복사해서 쓴다 |

## 기본값

`HF_TEXT_MODEL`(`Qwen/Qwen2.5-0.5B-Instruct`)·`HF_CLS_MODEL`(`lxyuan/distilbert-base-multilingual-cased-sentiments-student`)·`HF_EMBED_MODEL`(`intfloat/multilingual-e5-small`)은 교재 검증용 기본값이다. 모델 ID·revision·용량은 학기별 환경 기준표에서 확정한다. `uv.lock`은 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
