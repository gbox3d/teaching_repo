# 5주차 1교시 — 모델 카드 분석표와 캐시 보고

**역할: 1교시 모델 카드 분석 양식과 캐시 보고 참조 구현.** [실습지의 1교시](../../lab.md#1교시-실습--모델-카드-분석표와-캐시-보고)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 문제 1, 카드 3개 분석 | `model_cards_template.md` | 상위 `model_cards.md` |
| 문제 2, 용량·revision·실패 | `cache_report.py`, `hf_env.py`, `.env.example` | `outputs/cache_report-*.json`·캐시 보고 요약 |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week05_huggingface_hub\examples"
$dst = "$HOME\osa-practice\week05"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period1")) { Copy-Item -Recurse "$src\period1" "$dst\period1" }
Set-Location "$dst\period1"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync                    # 수업 전에 설치·캐시한다
if (-not (Test-Path ..\model_cards.md)) { Copy-Item model_cards_template.md ..\model_cards.md }
```

Python 명령은 현재 `period1` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 1교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | 이어받는 것: Ollama 라이브러리 밖으로 |
| 3–6분 | Model Card 읽는 순서 |
| 6–9분 | 카드 메타데이터가 곧 검색 조건이다 |
| 9–12분 | gated 모델과 토큰 |
| 12–14분 | revision으로 고정하기 |
| 14–17분 | 캐시 구조, 용량, 오프라인 |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#1교시-실습--모델-카드-분석표와-캐시-보고)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 카드를 열기 전에 모델 3개의 라이선스·fp16 용량·한국어 지원을 예상 |
| 카드 읽기 | 4–16분 | 카드 3개에서 항목을 찾아 `model_cards.md` 분석표 채우기 |
| 캐시 보고 | 16–24분 | `cache_report.py` 실행, 캐시 위치·용량·commit hash 기록, 암산과 비교 |
| 검증·기록 | 24–30분 | 실패 경로 재현, 판정 문장 작성, commit |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
uv run python cache_report.py
uv run python cache_report.py --params 0.5 --bytes-per-param 2
uv run python cache_report.py --cache-dir C:\없는폴더
$LASTEXITCODE
# 네트워크가 허용될 때만 카드의 파일 메타데이터를 조회한다.
uv run python cache_report.py --estimate Qwen/Qwen2.5-0.5B-Instruct
```

## 예상 결과와 완료 확인

캐시 위치·용량·저장소별 commit hash를 표시하고 JSON을 저장한다. 없는 캐시 경로는 종료 코드 1이다. 모델 카드 3개의 근거와 판정은 `model_cards.md`에 직접 작성한다. 캐시가 비어 있는 사실도 관찰이며 모델을 임의로 받지 않는다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

실습지 문제 2·확장대로 파라미터 수·바이트 또는 이미 기록된 revision만 바꿔 추정값을 비교한다. Hub 조회와 로컬 캐시 실측을 구분한다.

## CPU·네트워크 대체 경로

GPU·torch·모델 실행이 필요 없다. 네트워크가 없으면 사전 제공 카드 원문과 로컬 캐시만 읽고 `--estimate`는 건너뛴 사실을 적는다. 빈 캐시는 조교에게 준비 상태를 확인한다.
