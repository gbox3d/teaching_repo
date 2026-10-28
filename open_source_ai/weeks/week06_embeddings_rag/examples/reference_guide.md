# 6주차 옵션·공용 함수 안내

실행 위치와 준비는 [예제 README](README.md)를 따른다. `ex01`~`ex05`는 한 프로젝트의 명령이며 모든 기본 경로는 현재 프로젝트 루트를 기준으로 한다.

## 명령과 비교 옵션

| 명령 | 자주 바꾸는 옵션 | 결과 |
|---|---|---|
| `ex01` | `--docs`, `--size`, `--overlap`, `--hard`, `--out` | 청크 JSON |
| `ex02` | `--chunks`, `--backend st/ollama`, `--device cpu`, `--out` | 인덱스 JSON·NumPy 행렬 |
| `ex03` | `--query`, `--index`, `--top-k`, `--device cpu` | 질문별 검색 결과 JSON |
| `ex04` | `--query`, `--index`, `--top-k`, `--model`, `--num-ctx`, `--show-prompt`, `--no-context` | 질문별 답변·출처 JSON |
| `ex05` | `--evalset`, `--index`, `--top-k`, `--ids`, `--generate`, `--model` | 평가 JSON·Markdown |

각 명령의 `--help`에서 전체 옵션을 확인한다. `ex03`·`ex04`에서 `--query`를 생략하면 직접 질문을 입력한다. 이전 대화는 보내지 않으며 `/bye`로 종료한다.

```powershell
uv run ex01 --size 300 --overlap 0 --hard
uv run ex02 --chunks outputs/chunks-300.json --backend ollama --out outputs/index-ollama
uv run ex03 --index outputs/index-ollama --query "uv.lock은 왜 커밋하는가"
uv run ex04 --query "uv.lock은 왜 커밋하는가" --show-prompt
uv run ex05 --ids q05,q10 --generate
```

`--out`은 `ex01`에서는 JSON 파일명, `ex02`에서는 확장자를 뺀 인덱스 이름이다. 예를 들어 `--out outputs/index-150`은 `index-150.json`과 `index-150.npy`를 만든다.

## 공용 코드

| 위치 | 역할 | 사용하는 예제 |
|---|---|---|
| [shared/__init__.py](src/shared/__init__.py) | 루트 `.env`, `Chunk`, `Embedder`, 인덱스 저장·로드, 코사인 top-k, 입력 반복 | 전체 |
| [shared/retrieval.py](src/shared/retrieval.py) | `load_search_index()`의 모델 일치 확인, `search()` | ex03·ex04·ex05 |
| [shared/generation.py](src/shared/generation.py) | `SYSTEM_PROMPT`, 자료 블록 조립, Ollama 호출, 인용·거부 판정 | ex04·ex05 |

공용 패키지에는 명령을 등록하지 않는다. `pyproject.toml`의 `[tool.uv.build-backend] module-name`에는 예제 패키지와 `shared`를 모두 등록한다.

## 관찰 지점

- `ex01_chunk.split_text()`는 창의 뒤쪽 60% 이후에서 문장·문단 경계를 찾는다. `--hard`는 이 탐색을 건너뛴다.
- 청크 id인 `파일명#번호`를 검색·답변 출처·평가가 그대로 사용한다.
- e5 계열은 질의에 `query:`, 문서에 `passage:`를 붙이고 벡터를 정규화한다. 코사인 유사도는 `vectors @ query`로 계산한다.
- 검색·답변·평가는 인덱스와 현재 설정의 임베딩 모델이 같은지 확인한다. 다른 모델의 벡터는 직접 비교하지 않는다.
- `shared/generation.py`가 `/api/chat`의 `stream: false`, `think: false`, `options`를 구성한다. `--show-prompt`로 실제 자료와 질문을 확인한다.
- `cited`는 답이 인용한 id, `cited_in_retrieved`는 그중 검색 결과에 있는 id, `refused`는 고정 거부 문구의 포함 여부다. 이 필드와 함께 실제 문서·답변을 읽는다.
- `ex05`의 hit rate는 기대 출처 파일을 검색했는지 측정한다. 답변의 정확성과는 별개다. 생성 평가의 출처 일치율은 기대 출처 파일을 인용했는지 잰다.

## 기본값과 사전 준비

| 환경변수 | 기본값 | 용도 |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama 서버 |
| `OLLAMA_MODEL` | `qwen3:8b` | 생성 모델. 4·5주차 모델을 재사용하면 실제 설치한 이름으로 변경 |
| `OLLAMA_EMBED_MODEL` | `bge-m3` | Ollama 임베딩 모델 |
| `HF_EMBED_MODEL` | `intfloat/multilingual-e5-small` | Sentence Transformers 임베딩 모델 |
| `EMBED_BACKEND` | `st` | 기본 임베딩 백엔드 |
| `HF_HOME` | 설정 시 적용 | Hugging Face 캐시 위치 |
| `RAG_OUTPUT_DIR` | `outputs` | 결과 저장 폴더 |

Python은 `.python-version`의 3.12를 사용한다. `uv.lock`으로 의존성을 고정하며 `uv sync --locked`로 설치한다. 모델·장치 기준은 [학기별 환경 기준표](../../../../environment_baseline_template.md)에서 확정한다.

GPU가 없으면 임베딩에 `--device cpu`를 사용한다. Ollama가 없으면 기본 `st` 백엔드의 검색·검색 평가까지 진행할 수 있다. 생성에는 실행 중인 Ollama와 캐시된 생성 모델이 필요하다. 모델을 바꾼 실습은 사용한 모델 이름과 실제 결과를 기록한다.

## 문서 변경과 증거 보존

문서를 바꿨을 때만 `ex01`·`ex02`를 다시 실행한다. 평가 질문을 바꾸어 점수를 올리지 않고, 고정한 평가셋으로 개선 전후를 비교한다. 프롬프트 인젝션 실험은 별도의 `docs_inject/`와 인덱스를 사용한다.

`.env`·`.venv/`·모델 캐시·`outputs/` 전체는 커밋하지 않는다. 남길 증거만 `evidence/week06/`에 복사한다. [2차 종합과제](../../week08_midterm/assignment_brief.md)에서는 자기 문서 10개 이상과 평가셋·실패 분석으로 확장한다.
