# 6주차 실행 예제

한 uv 프로젝트에서 여섯 명령을 실행한다. 명령은 복사한 `examples` 루트에서 실행하고, `period1`~`period3` README는 현재 교시의 소스를 안내한다. 자료는 수업용으로 새로 쓴 그리스·로마 신화 요약 50편과 오디세우스 귀향 이야기 한 편이다.

| 교시 | 안내 | 소스 | 실행 | 바꿔 볼 값 |
|---|---|---|---|---|
| 1 | [임베딩과 유사도](period1/README.md) | [ex01_embed](src/ex01_embed/__init__.py) | `uv run ex01` | `SENTENCES` |
| 1 | 신화 검색 | [ex02_search](src/ex02_search/__init__.py) | `uv run ex02` | `TOP_K` |
| 2 | [자료 없이 vs 자료 넣고](period2/README.md) | [ex03_compare](src/ex03_compare/__init__.py) | `uv run ex03` | `TOP_K` |
| 2 | 출처 있는 신화 도우미 | [ex04_rag_chat](src/ex04_rag_chat/__init__.py) | `uv run ex04` | `RULES`, `TOP_K` |
| 3 | [긴 글 나누기](period3/README.md) | [ex05_chunk](src/ex05_chunk/__init__.py) | `uv run ex05` | `CHUNK_SIZE`, `CHUNK_OVERLAP` |
| 3 | 내 문서 도우미 | [ex06_my_docs](src/ex06_my_docs/__init__.py) | `uv run ex06` | `src/shared/data/`의 파일 |

예제에 명령행 옵션은 없다. 바꿀 값은 각 파일 맨 위의 대문자 상수이며, 값을 고치고 같은 명령을 다시 실행해 비교한다.

## 공용 코드와 자료

[shared](src/shared/__init__.py)에 모델 설정과 신화 자료를 읽는 함수를 모았다. 예제는 `from shared import ...`로 가져다 쓴다.

| 이름 | 역할 |
|---|---|
| `MODEL`, `EMBED_MODEL`, `HOST` | 생성 모델 `qwen3.5:2b`, 임베딩 모델 `bge-m3`, Ollama 주소. 환경변수 `OLLAMA_MODEL`·`OLLAMA_EMBED_MODEL`·`OLLAMA_HOST`가 있으면 그 값을 쓴다 |
| `create_model()` | 5주차와 같은 `ChatOllama` (temperature 0, 생각 출력 끔) |
| `create_embeddings()` | 문장을 벡터로 바꾸는 `OllamaEmbeddings` |
| `load_myths()` | `data/myths.md`를 `## 제목` 단위로 나눈 (제목, 본문) 목록 |
| `create_myth_store()` | 신화 50편을 벡터로 저장한 검색 저장소. `ex02`에서 직접 쓴 두 줄과 같다 |

자료 파일은 코드와 함께 `src/shared/data/`에 둔다.

| 파일 | 내용 | 쓰는 예제 |
|---|---|---|
| `myths.md` | 신화 요약 50편. `## 제목` 하나가 검색 단위 한 편 | ex02·ex03·ex04·ex06 |
| `odyssey.md` | `## 제목`으로 나뉘지 않고 한 편으로 이어지는 긴 글(약 3,900자). 조각으로 나누는 연습용 | ex05·ex06 |

`ex06`은 이 폴더의 `.md` 파일을 모두 읽으므로 자기 글을 `.md`로 저장해 넣으면 그 글에 대해 물을 수 있다.

## 구조

```text
examples/
├── pyproject.toml / uv.lock / .python-version
└── src/
    ├── ex01_embed/__init__.py
    ├── ex02_search/__init__.py
    ├── ex03_compare/__init__.py
    ├── ex04_rag_chat/__init__.py
    ├── ex05_chunk/__init__.py
    ├── ex06_my_docs/__init__.py
    └── shared/
        ├── __init__.py
        └── data/myths.md, odyssey.md
```

각 `src/<모듈>/__init__.py`의 `main()`이 실행 시작점이다. `[project.scripts]`가 `ex01` 같은 명령을 그 함수에 연결하고 `[build-system]`의 `uv_build`가 `src/` 패키지를 설치한다. scripts를 바꾸면 `uv sync`를 다시 실행한다. `shared`는 명령이 필요 없으므로 `module-name`에만 있다.

## 수업 전 준비

```powershell
ollama pull bge-m3
ollama list
uv sync
```

생성 모델은 4주차 `qwen3.5:2b`를 그대로 쓴다. 임베딩 모델 `bge-m3`는 글을 벡터로 바꾸는 전용 모델(MIT 라이선스, 약 1.2 GB)로 답을 생성하지 않는다. 두 모델이 `ollama list`에 보여야 한다. 다운로드는 수업 전에 마친다.

패키지는 5주차의 `langchain-core`·`langchain-ollama`에 글을 조각으로 나누는 `langchain-text-splitters`와 유사도 계산에 쓰는 `numpy`를 더했다. PyTorch는 설치하지 않는다.

## 입력

```text
나> 메두사를 죽인 영웅은 누구야?
  0.572  메두사와 고르곤 자매: 고르곤은 머리카락이 뱀이고 눈을 마주친 생물을 돌로 만드는 세 자매...
  0.532  페르세우스와 메두사의 머리: 페르세우스는 황금 비로 변한 제우스와 다나에 사이에서 태어났다...
  0.529  벨레로폰과 페가소스: 코린토스의 영웅 벨레로폰은 아테나의 도움으로 황금 굴레를 얻어 메두사...
나> /bye
```

모든 예제가 `나>`에서 질문을 반복해 받는다. 빈 줄은 건너뛰고 `/bye`로 종료한다. 이번 주 예제는 질문마다 새로 검색하며 이전 대화는 보내지 않는다. 실행할 때마다 처음에 자료 전체를 벡터로 바꾸느라 몇 초 기다린다. 연결 실패는 Ollama 실행 상태를, 모델 오류는 `ollama list`에 두 모델이 있는지 확인한다.
