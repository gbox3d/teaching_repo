# 6주차 실행 예제

5주차처럼 **한 uv 프로젝트**에서 예제별 명령을 실행한다. 세 교시 모두 복사한 `examples/`의 `pyproject.toml` 옆에서 작업한다.

| 교시 | 명령 | 여는 소스 | 역할 |
|---|---|---|---|
| 1 | `uv run ex01` | [ex01_chunk](src/ex01_chunk/__init__.py) | 문서 분할 |
| 1 | `uv run ex02` | [ex02_embed](src/ex02_embed/__init__.py) | 임베딩 인덱스 생성 |
| 1 | `uv run ex03` | [ex03_search](src/ex03_search/__init__.py) | 질문을 입력해 검색 |
| 2 | `uv run ex04` | [ex04_rag](src/ex04_rag/__init__.py) | 검색 근거로 출처 있는 답변 |
| 3 | `uv run ex05` | [ex05_eval](src/ex05_eval/__init__.py) | 평가셋으로 검색·답변 점검 |

[1교시 안내](period1/README.md) · [2교시 안내](period2/README.md) · [3교시 안내](period3/README.md) · [옵션·공용 함수 안내](reference_guide.md)

## 폴더 구조

```text
examples/
├── pyproject.toml / uv.lock / .python-version
├── .env.example / .gitignore
├── src/
│   ├── ex01_chunk/__init__.py
│   ├── ex02_embed/__init__.py
│   ├── ex03_search/__init__.py
│   ├── ex04_rag/__init__.py
│   ├── ex05_eval/__init__.py
│   └── shared/
│       ├── __init__.py     # 설정·임베딩·인덱스·입력
│       ├── retrieval.py    # 검색·모델 일치 확인
│       └── generation.py   # 프롬프트·Ollama 호출·출처 판정
├── docs/                  # 직접 읽고 수정할 문서 6개
├── evalset.json           # 세 교시가 함께 쓰는 평가셋
└── period1~3/README.md     # 교시별 안내만 둔다
```

예제마다 `main()`이 실행 시작점이다. `[project.scripts]`가 `ex01` 같은 명령을 해당 함수에 연결하고 `[build-system]`의 `uv_build`가 `src/` 패키지를 설치한다. scripts를 바꾸면 `uv sync`를 다시 실행한다.

공용 기능은 `from shared import ...`, `from shared.retrieval import search`처럼 가져온다. 예제끼리 직접 import하지 않는다. `docs/`·`evalset.json`·`.env`·`outputs/`는 프로젝트에 한 벌만 두고 계속 사용한다.

## 수업 전 준비

새 프로젝트 구조를 직접 만드는 명령은 다음과 같다. `.python-version`·`pyproject.toml`·`src/`가 생기는지 확인한다. 교재를 아래처럼 복사하는 경우에는 이미 이 구조가 있으므로 `uv init`을 다시 실행하지 않는다.

```powershell
uv init --package --python 3.12 --vcs none week06-rag
```

실습은 교재의 `examples/` 전체를 한 번 복사해 시작한다. 이미 작업 중인 폴더는 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week06_embeddings_rag\examples"
$dst = "$HOME\osa-practice\week06"
New-Item -ItemType Directory -Force "$HOME\osa-practice" | Out-Null
if (-not (Test-Path $dst)) { Copy-Item -Recurse $src $dst }
Set-Location $dst
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync --locked
ollama list
```

원본에 `.venv/`·`.env`·`outputs/`가 이미 있다면 제외하고 교재 파일만 복사한다. 환경·lock 배포는 [공통 uv 가이드](../../../uv_guide.md)를 따른다.

임베딩 모델은 `.env`의 `HF_EMBED_MODEL`, 생성 모델은 `OLLAMA_MODEL`에 지정한다. 4·5주차 모델을 재사용할 때는 `ollama list`에 있는 정확한 이름으로 맞춘다. 패키지와 모델 다운로드는 수업 전에 마친다. 오프라인 수업에서는 준비한 캐시와 `HF_HUB_OFFLINE=1`을 사용한다.

## 실행 순서

```powershell
uv run ex01 --size 300 --overlap 50
uv run ex02 --chunks outputs/chunks-300.json
uv run ex03
uv run ex04
uv run ex05 --top-k 3
```

`ex03`을 `/bye`로 종료한 뒤 `ex04`를 실행하고, `ex04`도 종료한 뒤 평가한다. 2·3교시에는 1교시 인덱스를 그대로 쓴다. 문서를 바꿨거나 인덱스가 없을 때만 `ex01`·`ex02`를 다시 실행한다.

```text
나> uv.lock은 왜 커밋하는가
(검색 결과 또는 출처를 붙인 답변)
나> Apache-2.0 라이선스가 MIT와 다른 점은?
(다음 결과)
나> /bye
```

빈 입력은 건너뛴다. 각 질문은 독립적으로 검색하며 앞 대화를 모델에 보내지 않는다. 같은 조건을 명령으로 재현하려면 `uv run ex03 --query "질문"`, `uv run ex04 --query "질문"`을 사용한다. `--query`는 여러 번 지정할 수 있다.

결과는 루트 `outputs/`에 생긴다. 검색은 한 실행의 질문들을 JSON 하나에 누적하고, 답변은 질문마다 JSON을 남긴다. 제출할 증거만 골라 `evidence/week06/`에 복사한다.
