# 5주차 3교시 — 데이터셋 살펴보기와 출처 기록표

**역할: 3교시 datasets 참조 구현·출처 양식과 앞 교시 공개 코드.** [실습지의 3교시](../../lab.md#3교시-실습--데이터셋-살펴보기와-출처-기록표)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 문제 1, 로컬/스트리밍 구조·샘플 | `dataset_peek.py`, `data/sample_qa.jsonl`, `data/README.md` | `outputs/dataset_peek-*.json`·데이터 구조 기록 |
| 문제 2, Dataset Card·출처 | `SOURCES_template.md`, `hf_env.py` | 상위 `SOURCES.md` 모델 2개·데이터 1개 |
| 앞 교시 기록 대조 | `cache_report.py`, `pipeline_demo.py`, `model_cards_template.md` | 실제 모델 ID·revision 대조 |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week05_huggingface_hub\examples"
$dst = "$HOME\osa-practice\week05"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period3")) { Copy-Item -Recurse "$src\period3" "$dst\period3" }
Set-Location "$dst\period3"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync                    # 수업 전에 설치·캐시한다
if (-not (Test-Path ..\model_cards.md)) { Copy-Item model_cards_template.md ..\model_cards.md }
if (-not (Test-Path ..\SOURCES.md)) { Copy-Item SOURCES_template.md ..\SOURCES.md }
```

Python 명령은 현재 `period3` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 3교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | 이어받는 것: 모델에서 데이터로 |
| 3–6분 | 로컬 파일도 같은 API |
| 6–9분 | 스트리밍 — 전부 내려받지 않고 보기 |
| 9–12분 | Dataset Card 읽기 |
| 12–15분 | 데이터 라이선스와 위험 |
| 15–17분 | SOURCES.md — 출처 기록표 |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#3교시-실습--데이터셋-살펴보기와-출처-기록표)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 파일을 열지 않고 `sample_qa.jsonl`의 필드 구조를 예상 |
| 로컬 데이터 | 4–12분 | `dataset_peek.py` 기본 실행·스트리밍 실행, 구조·건수 기록 |
| 카드 읽기 | 12–20분 | 공개 데이터셋 1개의 Dataset Card 분석, 가능하면 스트리밍으로 5개 확인 |
| 출처 기록 | 20–26분 | `SOURCES.md`에 모델 2개 + 데이터 1개 작성 |
| 검증·기록 | 26–30분 | 실패 경로 재현, 조건 요약, commit |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
uv run python dataset_peek.py
uv run python dataset_peek.py --streaming --n 3 --max-chars 40
uv run python dataset_peek.py --file data\없음.jsonl
$LASTEXITCODE
# Hub 실습은 lab의 허용 조건에서만 실행한다.
# uv run python dataset_peek.py --hub-id klue/klue --config ynat --split train --streaming --n 5
```

## 예상 결과와 완료 확인

로컬 데이터의 필드 구조·건수·샘플 5개와 스트리밍의 차이가 JSON에 남는다. 파일 없음은 종료 코드 1과 error 기록을 남긴다. `SOURCES.md`에는 카드에서 확인한 라이선스·revision·용도·변경 내용을 직접 쓴다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

실습지의 `--n`·`--max-chars`·`--streaming` 비교를 수행하고, 출처 표를 공개 모델 2개와 데이터 1개로 채운다. 예제 데이터의 실제 개인정보 여부도 카드와 함께 확인한다.

## CPU·네트워크 대체 경로

데이터 탐색은 CPU로 충분하다. 네트워크가 없어도 포함된 로컬 JSONL과 카드로 기본 실습을 진행한다. 공개 Dataset Card는 사전 제공 사본을 사용하고 Hub 스트리밍을 하지 못한 이유를 적는다. 이 교시의 데이터 명령은 모델을 불러오지 않는다.
