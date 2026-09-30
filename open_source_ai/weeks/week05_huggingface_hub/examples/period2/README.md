# 5주차 2교시 — pipeline으로 분류와 생성 실행하기

**역할: 2교시 pipeline 참조 구현과 1교시 카드·캐시 도구.** [실습지의 2교시](../../lab.md#2교시-실습--pipeline으로-분류와-생성-실행하기)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 문제 1, 분류 5문장·장치 비교 | `pipeline_demo.py`의 `--task cls` | 장치별 `outputs/pipeline-*.json` |
| 문제 2, 생성·revision·실패 | `pipeline_demo.py`의 `--task gen`, `hf_env.py` | `pipeline_report.md`·생성/실패 JSON |
| 준비, 이전 모델 ID·commit 확인 | `cache_report.py`, `model_cards_template.md` | 1교시 카드·캐시 기록 |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week05_huggingface_hub\examples"
$dst = "$HOME\osa-practice\week05"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period2")) { Copy-Item -Recurse "$src\period2" "$dst\period2" }
Set-Location "$dst\period2"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync                    # 수업 전에 설치·캐시한다
if (-not (Test-Path ..\model_cards.md)) { Copy-Item model_cards_template.md ..\model_cards.md }
```

Python 명령은 현재 `period2` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 2교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | 이어받는 것: 카드에서 코드로 |
| 3–6분 | task 종류와 모델 명시 |
| 6–9분 | 한국어 모델 고르기 |
| 9–12분 | device와 dtype |
| 12–15분 | 생성 모델 호출 |
| 15–17분 | 경고 메시지 읽기와 시간 재기 |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#2교시-실습--pipeline으로-분류와-생성-실행하기)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 5문장의 라벨, 한국어·영어 문장의 결과 차이, CPU/GPU 시간을 예상 |
| 분류 실행 | 4–12분 | `--task cls`를 CPU와 GPU에서 실행, 라벨·점수·시간 기록 |
| 생성 실행 | 12–20분 | `--task gen` 실행, commit hash로 revision 고정 후 재실행 |
| 실패·비교 | 20–25분 | 잘못된 revision·오프라인 실패 재현, 시간 비교표 작성 |
| 검증·기록 | 25–30분 | `pipeline_report.md` 완성, commit |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
uv run python pipeline_demo.py --task cls --device cpu
uv run python pipeline_demo.py --task gen --device cpu --max-new-tokens 60
# CUDA를 확인한 PC에서는 --device cuda로 같은 태스크를 반복한다.
# 출력의 실제 commit hash를 복사해 --gen-revision 값으로 재실행한다.
uv run python pipeline_demo.py --task gen --device cpu --gen-revision 0000000
```

## 예상 결과와 완료 확인

분류 라벨·점수 5개, 생성 답, 모델·revision·device·dtype·로드/추론 시간과 실패 기록이 JSON에 남는다. CPU/GPU가 없으면 CPU 두 번의 결과를 비교하고 실제 장치명을 적는다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

실습지 문제 2대로 출력된 commit hash를 `--gen-revision`에 넣고 재실행한다. 오프라인 상태에서 없는 모델을 지정해 실패 경로도 기록한다.

## CPU·네트워크 대체 경로

GPU가 없으면 `--device cpu`, 생성은 `--max-new-tokens 60`을 사용한다. 모델·패키지는 수업 전에 캐시한다. 네트워크가 없으면 `.env`의 `HF_HUB_OFFLINE=1`로 두고 캐시만 사용한다. 누락된 모델은 수업 중 다운로드하지 않는다.
