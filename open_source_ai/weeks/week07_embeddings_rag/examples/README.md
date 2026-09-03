# 7주차 예제 — mini_rag: 분할·임베딩·검색·출처 있는 답·평가

## 파일 구성

| 파일 | 역할 | 쓰는 교시 |
|---|---|---|
| `mini_rag/` | uv 프로젝트. 아래 파일을 담는다 | 1·2·3교시 |
| `mini_rag/pyproject.toml` | 의존성 `sentence-transformers`, `torch`(CUDA 인덱스 블록), `numpy`, `httpx`, `python-dotenv`. 버전은 고정하지 않는다 | |
| `mini_rag/docs/` | 1~5주 수업 내용을 정리한 자체 작성 한국어 문서 6개(각 300~600자). 실제 인물·기관 없음 | 1교시 |
| `mini_rag/ragcore.py` | 공통 모듈: 환경변수 + 기본값, `Chunk`, Ollama 연결·모델 확인, `Embedder`(st / ollama), 인덱스 저장·로드, 코사인 top-k | 전체 |
| `mini_rag/chunk.py` | 문서를 크기·겹침·문장 경계로 분할. `--hard`는 경계 무시. `outputs/chunks-<size>.json` | 1교시 |
| `mini_rag/embed.py` | 청크를 임베딩해 `outputs/index.json`(메타 + 청크) + `index.npy`(벡터). `--backend ollama` 선택 | 1교시 |
| `mini_rag/search.py` | 질의 임베딩 → 코사인 top-k. 여러 `--query` 가능. `outputs/search-*.json` | 1·3교시 |
| `mini_rag/rag_answer.py` | 검색 결과를 system·context·question 프롬프트로 조립해 `/api/chat` 호출. 출처 파싱·거부 판정. `outputs/rag-*.json` | 2교시 |
| `mini_rag/eval.py` | 평가셋으로 retrieval hit rate, `--generate` 시 키워드·출처 일치율. `outputs/eval-*.json`·`.md` | 3교시 |
| `mini_rag/evalset.json` | 10문항(질문·기대 출처 파일·정답 키워드). 문서 표현 그대로와 바꿔 말한 문항이 섞여 있다 | 3교시 |
| `mini_rag/.env.example` | 환경변수 예시. `.env`로 복사한다 | 1교시 |
| `mini_rag/.gitignore` | `.venv/`, `.env`, `outputs/` 등 커밋 제외 | |
| `mini_rag/README.md` | 짧은 실행 안내 | |

`ragcore.py`는 스크립트가 아니라 모듈이며 직접 실행하지 않는다. 각 스크립트는 `argparse`·`main()`을 갖고, 연결 실패·모델 없음·앞 단계 결과 없음을 사람이 읽을 한 문장으로 알린 뒤 0이 아닌 종료 코드로 끝난다.

## 실행 방법

원본을 두고 개인 저장소 안의 폴더에 복사한다. `$src`·`$dst`는 예시이며 교재 저장소 위치는 실습실 안내를 따른다.

```powershell
$src = "C:\teaching_repo\open_source_ai\weeks\week07_embeddings_rag\examples"
$dst = "$HOME\osa-practice\week07"
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item -Recurse "$src\mini_rag" "$dst\mini_rag"
Set-Location "$dst\mini_rag"
Copy-Item .env.example .env
uv sync
```

1교시(분할 → 임베딩 → 검색):

```powershell
uv run python chunk.py --size 300 --overlap 50
uv run python embed.py --chunks outputs/chunks-300.json
uv run python search.py --query "uv.lock은 왜 커밋하는가" --query "Apache-2.0 라이선스가 MIT와 다른 점은?" --top-k 3
uv run python chunk.py --size 150 --overlap 30
uv run python embed.py --chunks outputs/chunks-150.json --out outputs/index-150
uv run python search.py --index outputs/index-150 --query "uv.lock은 왜 커밋하는가" --top-k 3
uv run python chunk.py --size 300 --overlap 0 --hard        # 문장 경계 무시(실패 관찰용)
```

2교시(출처 있는 답 생성):

```powershell
uv run python rag_answer.py --query "uv.lock은 왜 커밋하는가" --top-k 3
uv run python rag_answer.py --query "uv.lock은 왜 커밋하는가" --show-prompt
uv run python rag_answer.py --query "LoRA의 rank는 무엇인가"               # 자료 밖 → 거부 기대
uv run python rag_answer.py --query "LoRA의 rank는 무엇인가" --no-context  # 검색 없이(비교용)
uv run python rag_answer.py --query "uv.lock은 왜 커밋하는가" --num-ctx 256  # 컨텍스트 창 경계
```

3교시(평가):

```powershell
uv run python eval.py --evalset evalset.json --top-k 3
uv run python eval.py --evalset evalset.json --top-k 1
uv run python eval.py --evalset evalset.json --index outputs/index-150 --top-k 3
uv run python eval.py --evalset evalset.json --ids q05,q10 --generate
```

`uv run`은 `.venv`가 없으면 만들고 의존성을 설치한다. 수업 전에 `uv sync`를 한 번 실행해 두면 실습 중 네트워크가 필요 없다. 실행 순서는 `chunk → embed → search/rag_answer/eval`이며, 앞 단계 결과가 없으면 스크립트가 어느 명령을 먼저 실행할지 알려 준다.

## 관찰 지점

1. `chunk.py`의 청크 경계는 창의 뒤쪽(size의 0.6배 지점 이후)에서 문장·문단 끝을 찾아 자른다. `--hard`를 주면 글자 수로만 잘라 문장이 중간에서 끊긴다.
2. 청크 id는 `파일명#번호`다. `rag_answer.py`의 출처 표시와 `eval.py`의 출처 일치율이 모두 이 id를 그대로 쓴다.
3. `embed.py`는 정규화된 float32 벡터를 저장하므로 `search.py`의 코사인 유사도는 행렬곱 한 줄(`vectors @ query`)이다. 벡터 DB 없이 numpy로 충분한 규모다.
4. 6주차 `pretrained_embed.py`에서 손으로 한 토큰화 → hidden state → mean pooling → 정규화를 `SentenceTransformer.encode(..., normalize_embeddings=True)` 한 줄이 대신한다(`ragcore.Embedder`). 라이브러리가 바뀌었을 뿐 계산 절차는 6주차와 같고, 접두어만 질의·청크로 나뉜다(다음 항목).
5. e5 계열 모델은 `query:`·`passage:` 접두어를 붙여 인코딩한다(`ragcore.Embedder.encode`). 질의와 청크에 다른 접두어를 쓰는 것이 의도된 동작이다.
6. `search.py`는 인덱스에 기록된 백엔드·모델과 현재 `.env`가 다르면 실행을 막는다. 같은 모델로 만든 벡터끼리만 비교할 수 있기 때문이다.
7. `rag_answer.py`의 요청 JSON에는 `stream:false`, `think:false`(Qwen3 계열의 생각 출력이 답에 섞이지 않게), `options.num_ctx`·`temperature`·`num_predict`가 명시된다. `--show-prompt`로 system·user 메시지 전체를 볼 수 있다.
8. 결과의 `cited`(답이 인용한 id), `cited_in_retrieved`(그중 검색 결과 안에 있는 것), `refused`(고정 거부 문구가 나왔는가)는 답을 읽기 전에 볼 판정 필드다.
9. `--num-ctx`를 프롬프트보다 작게 주면 `prompt_eval_count`가 그 값을 넘지 않는다. 잘린 부분에 system 규칙이 포함되면 거부·출처 형식이 깨질 수 있다.
10. `eval.py`의 hit rate는 검색만으로 계산되므로 Ollama 없이 돌아간다. `--generate`를 붙여야 생성 모델을 호출하고 키워드율·출처 일치율이 추가된다.
11. `evalset.json`의 `expected_source`가 인덱스에 없는 파일명이면 결과에 경고가 붙는다. 평가셋 오타를 잡는 장치다.
12. `embed.py`가 남기는 `backend`·`model`·`device`·`load_sec`·`encode_sec`는 6주차 실험 기록 습관을 이어받은 항목이다. 인덱스 파일마다 어떤 조건으로 만들었는지 남는다.

## GPU 없을 때·네트워크 없을 때

- GPU가 없거나 인식되지 않으면 sentence-transformers가 자동으로 CPU를 쓴다. 명시하려면 `embed.py --device cpu`. 청크가 300자 13개·150자 33개라 CPU에서도 수 초면 끝난다. `index.json`의 `device` 값이 `cpu`인 것 자체가 기록할 관찰이다.
- 임베딩 모델 로드가 실패하면(캐시 없음·네트워크 없음) `embed.py --backend ollama`로 Ollama 임베딩 모델(`OLLAMA_EMBED_MODEL`, 기본값 `bge-m3`)을 쓴다. 이후 `search.py`·`rag_answer.py`·`eval.py`는 인덱스에 기록된 백엔드를 자동으로 따른다.
- 네트워크가 없는 실습실에서는 `.env`의 `HF_HUB_OFFLINE=1` 줄의 주석을 풀어 캐시된 모델만 쓰게 한다. 모델과 `uv sync`가 수업 전에 준비되어 있으면 모든 실습이 오프라인으로 진행된다.
- 생성 모델은 GPU가 없으면 `.env`의 `OLLAMA_MODEL`을 캐시된 소형 모델(`qwen3:0.6b`)로 바꾼다. 소형 모델은 출처 형식을 덜 지키거나 자료 밖 질문에 거부하지 않을 수 있으며, 그 결과를 그대로 기록하는 것이 이번 주 관찰이다.
- Ollama 서버가 시작되지 않으면 1교시 전체와 3교시의 hit rate 측정은 그대로 진행할 수 있다. 2교시는 연결 실패 메시지(사람이 읽을 한 문장, 종료 코드 1)를 먼저 확인하고, 답 생성 결과는 강의자가 배포하는 기준 PC 실행 기록으로 대신한다.

## 복사 후 변형

- `docs/`에 자기 문서를 추가할 때는 수업 내용을 다룬 300~600자 한국어 문서로 하고 실제 인물·기관·연락처를 넣지 않는다. 문서를 바꾸면 `chunk.py`·`embed.py`를 다시 실행해야 인덱스에 반영된다.
- `evalset.json`에 문항을 추가할 때는 `expected_source`를 `docs/` 파일명과 글자 단위로 맞춘다. 질문을 문서 표현으로 바꿔 hit rate를 올리는 것은 개선이 아니다.
- 프롬프트 인젝션 실험은 `docs/`를 복사한 별도 폴더(`docs_inject/`)에서 하고, `--docs`·`--out`·`--index` 옵션으로 원래 인덱스와 분리한다.
- `outputs/`는 커밋하지 않는다. 증거로 낼 JSON·MD 몇 개는 개인 저장소의 `evidence/week07/`에 복사한다.
- 2차 종합과제에서는 이 프로젝트를 자기 문서 10개 이상, 평가셋 10문항, 실패 분석 2건으로 확장한다. 안내는 [`../../week08_midterm/assignment_brief.md`](../../week08_midterm/assignment_brief.md)에 있다.

## 기본값과 환경 기준표

| 환경변수 | 기본값 | 용도 |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama 서버 |
| `OLLAMA_MODEL` | `qwen3:8b` | 답 생성 모델(RTX 4070 기준). CPU 대체는 `qwen3:0.6b` |
| `OLLAMA_EMBED_MODEL` | `bge-m3` | `--backend ollama`일 때 임베딩 모델 |
| `HF_EMBED_MODEL` | `intfloat/multilingual-e5-small` | sentence-transformers 임베딩 모델(6주차와 같음) |
| `EMBED_BACKEND` | `st` | 기본 임베딩 백엔드(`st` 또는 `ollama`) |
| `HF_HOME` | (설정 시) | Hugging Face 캐시 위치 |
| `RAG_OUTPUT_DIR` | `outputs` | 결과 파일 폴더 |

모델 ID·양자화·용량은 [학기별 환경 기준표](../../../../environment_baseline_template.md)에서 확정하며 위 값은 교재 검증용 기본값이다. `uv.lock`은 만들지 않았다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다. Ollama 호출은 `/api/tags`(모델 확인), `/api/embed`(임베딩), `/api/chat`(생성)만 쓴다.
