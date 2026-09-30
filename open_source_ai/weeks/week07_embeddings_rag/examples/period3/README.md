# 7주차 3교시 — 평가셋으로 품질 재기와 실패 분석

**역할: 3교시 평가 참조 구현·평가셋과 앞 교시 전체 코드.** [실습지의 3교시](../../lab.md#3교시-실습--평가셋으로-품질-재기와-실패-분석)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 준비, 두 인덱스 재생성 | `docs/`, `chunk.py`, `embed.py` | 이 폴더의 `outputs/index.*`, `outputs/index-150.*` |
| 문제 1, 조건별 hit rate | `eval.py`, `evalset.json`, `search.py`, `ragcore.py` | 조건 3개의 `outputs/eval-*.md/json` |
| 문제 2, 실패 분석·생성 평가 | `search.py`, `eval.py --generate`, `rag_answer.py` | `eval_note.md`·실패 2건·과제 점검 |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week07_embeddings_rag\examples"
$dst = "$HOME\osa-practice\week07"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period3")) { Copy-Item -Recurse "$src\period3" "$dst\period3" }
Set-Location "$dst\period3"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync                    # 수업 전에 설치·캐시한다
```

이 교시 폴더만 복사해도 시작할 수 있다. 실습 30분을 시작하기 전에 아래 준비 명령으로 **이 폴더의** 인덱스를 만든다. 앞 교시의 `outputs/`를 가져오거나 다른 폴더를 import하지 않는다. 문서를 수정했다면 그 내용을 이 폴더의 `docs/`에도 반영한 뒤 다시 만든다.

```powershell
uv run python chunk.py --size 300 --overlap 50
uv run python embed.py --chunks outputs/chunks-300.json
uv run python chunk.py --size 150 --overlap 30
uv run python embed.py --chunks outputs/chunks-150.json --out outputs/index-150
```

Python 명령은 현재 `period3` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 3교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | 이어받는 것: 그럴듯한 답의 함정 |
| 3–6분 | 검색 실패 유형 세 가지 |
| 6–9분 | 환각 점검: 근거 확인 세 필드 |
| 9–12분 | 소형 평가셋과 hit rate |
| 12–15분 | 시연: eval.py와 결과표 읽기 |
| 15–17분 | 2차 종합과제 안내 |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#3교시-실습--평가셋으로-품질-재기와-실패-분석)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | `evalset.json` 10문항 훑기, 조건별 hit rate 예상 |
| hit rate 측정 | 4–12분 | `eval.py` top-k 3 · top-k 1 · 150자 인덱스, 결과표 옮기기 |
| 실패 분석 | 12–20분 | 실패(또는 순위 낮은) 문항 2개의 top-5 확인, 유형 분류, 개선 시도 |
| 생성 포함 평가 | 20–24분 | `--ids`로 2~3문항 `--generate`, 키워드·출처 일치·거부 확인 |
| 검증·기록 | 24–30분 | `eval_note.md` 완성, 2차 과제 "제출 전 검사" 표시 |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
uv run python eval.py --evalset evalset.json --top-k 3
uv run python eval.py --evalset evalset.json --top-k 1
uv run python eval.py --evalset evalset.json --index outputs/index-150 --top-k 3
uv run python search.py --query "uv.lock은 왜 커밋하는가" --top-k 5
uv run python eval.py --evalset evalset.json --ids q05,q10 --generate
```

## 예상 결과와 완료 확인

10문항의 hit·rank·top과 조건 3개의 hit rate를 남긴다. 실패 또는 순위가 낮은 문항 2개를 lab의 세 유형으로 분석하고, 생성 2문항의 keyword_ok·source_ok·refused를 기록한다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

평가 질문은 고정하고 top-k·청크·문서 표현 중 개선안 하나만 바꿔 전후 순위를 잰다. 모두 1위라면 실습지의 점수 차 대체 기준을 적용한다.

## CPU·네트워크 대체 경로

검색 평가는 캐시된 임베딩 모델만 있으면 CPU에서 가능하며 Ollama 생성 서버는 `--generate`에서만 필요하다. 생성은 소형 모델과 `--ids` 2문항으로 줄인다. 오프라인 모드에서는 사전 캐시만 사용한다.
