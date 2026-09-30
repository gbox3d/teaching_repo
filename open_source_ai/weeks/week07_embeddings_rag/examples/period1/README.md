# 7주차 1교시 — 문서를 나누고 임베딩으로 찾기

**역할: 1교시 문서 분할·임베딩·검색 참조 구현.** [실습지의 1교시](../../lab.md#1교시-실습--문서를-나누고-임베딩으로-찾기)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 문제 1, 300자 청크·인덱스·질의 | `docs/`, `chunk.py`, `embed.py`, `search.py`, `ragcore.py` | chunks/index/search JSON·벡터 |
| 문제 2, 150자 비교·경계 | `chunk.py --size/--overlap/--hard`, 같은 검색 코드 | top-3 비교표·`search_note.md` |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week07_embeddings_rag\examples"
$dst = "$HOME\osa-practice\week07"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period1")) { Copy-Item -Recurse "$src\period1" "$dst\period1" }
Set-Location "$dst\period1"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync                    # 수업 전에 설치·캐시한다
```

Python 명령은 현재 `period1` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 1교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | 이어받는 것: 행렬에서 검색으로 |
| 3–6분 | 왜 RAG인가 |
| 6–9분 | 임베딩과 의미 유사도 |
| 9–12분 | 문서 분할: 크기·겹침·경계 |
| 12–15분 | 벡터 검색: 코사인 top-k |
| 15–17분 | 시연: chunk → embed → search |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#1교시-실습--문서를-나누고-임베딩으로-찾기)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 문서 6개를 훑고 청크 수·질의 2개의 1위 파일을 예상표에 적기 |
| 분할·인덱스 | 5–13분 | `chunk.py` 300자 → `embed.py` → 청크 수·인코딩 시간 기록 |
| 검색 | 13–20분 | `search.py` 질의 2개 top-3, 순위·점수·id 기록 |
| chunk 크기 비교 | 20–25분 | 150자 인덱스로 같은 질의 반복, `--hard` 경계 실패 재현 |
| 검증·기록 | 25–30분 | `search_note.md` 완성, `outputs/search-*.json` 확인 |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
uv run python chunk.py --size 300 --overlap 50
uv run python embed.py --chunks outputs/chunks-300.json
uv run python search.py --query "uv.lock은 왜 커밋하는가" --query "Apache-2.0 라이선스가 MIT와 다른 점은?" --top-k 3
uv run python chunk.py --size 150 --overlap 30
uv run python embed.py --chunks outputs/chunks-150.json --out outputs/index-150
uv run python search.py --index outputs/index-150 --query "uv.lock은 왜 커밋하는가" --query "Apache-2.0 라이선스가 MIT와 다른 점은?" --top-k 3
uv run python chunk.py --size 300 --overlap 0 --hard
```

## 예상 결과와 완료 확인

문서 6개가 청크로 나뉘고 300자·150자 인덱스가 각각 생성된다. 질의 2개 × 인덱스 2개의 top-3와 문장 경계 실패를 `search_note.md`에 적는다. 이 폴더에는 답 생성·평가 코드가 없다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

실습지 문제 2대로 청크 크기를 바꿔 순위·본문을 비교한다. 점수만 높다는 이유로 정답이라고 판단하지 않는다.

## CPU·네트워크 대체 경로

GPU가 없으면 embed/search에 `--device cpu`를 붙인다. 네트워크가 없으면 사전 캐시한 HF 모델과 `HF_HUB_OFFLINE=1`을 쓰거나 캐시된 Ollama 임베딩 모델로 `--backend ollama`를 선택한다. 생성 모델은 필요 없다.
