# 4주차 3교시 — 수업 도우미 모델 만들기와 과제 점검

먼저 [Python 라이브러리 실습의 대화 기억 단계](../../python_library.md#3-이전-대화를-기억하게-만들기)를 따른다. `memory_chat.py`로 대화 저장·재시작·기억 끄기를 비교한다. 아래 Modelfile 내용은 이후 선택 심화다.

**역할: 3교시 Modelfile 실습 시작 코드와 1·2교시 공개 참조 코드.** [실습지의 3교시](../../lab.md#3교시-실습--수업-도우미-모델-만들기와-과제-점검)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 문제 1, FROM·SYSTEM·create | `Modelfile` | 커스텀 모델·`ollama list/show` |
| 문제 1·2, 기준·v1·v2·충돌 비교 | `chat.py`, `config.py`, `ollama_api.py` | `outputs/chat-*.json` 6개 이상 |
| 문제 1·2, 비교 기록 | `custom_model_report_section.md`, `model_report_template.md` | 상위 `model_report.md` 5절·`assignment_check.md` |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week04_ollama_local_llm\examples"
$dst = "C:\classwork\week04"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period3")) { Copy-Item -Recurse "$src\period3" "$dst\period3" }
Set-Location "$dst\period3"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync                    # 수업 전에 설치·캐시한다
if (-not (Test-Path ..\model_report.md)) { Copy-Item model_report_template.md ..\model_report.md }
```

기존 보고서의 1~4절은 보존하고 `custom_model_report_section.md`의 5절을 상위 `model_report.md`에 추가한다. 이미 5절이 있으면 다시 붙이지 않는다.

Python 명령은 현재 `period3` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 3교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | 이어받는 것: 역할은 어디에 두는가 |
| 3–6분 | Modelfile 네 지시어 |
| 6–9분 | `ollama create`는 복사가 아니다 |
| 9–12분 | 시스템 프롬프트 설계 |
| 12–14분 | 프롬프트로 되는 것과 안 되는 것 |
| 14–17분 | 1차 종합과제 |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#3교시-실습--수업-도우미-모델-만들기와-과제-점검)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | create 뒤 `ollama list` SIZE, 답 길이 변화 예상 |
| Modelfile 수정·create | 4–11분 | FROM 확인, SYSTEM에 팀명 한 줄 추가, `ollama create`, `show` |
| 전후 비교 | 11–19분 | 질문 3개를 기준 모델과 커스텀 모델로 `chat.py` 실행, 표 채우기 |
| SYSTEM 한 줄 변경·재비교 | 19–24분 | 한 줄만 바꿔 재생성, 같은 질문 재실행, `--system` 충돌 관찰 |
| 증거 정리 | 24–30분 | 1차 과제 체크리스트 점검, 빈 항목과 계획 기록, `outputs/` JSON 6개 이상 확인 |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
Get-Content Modelfile
ollama show qwen3:8b --modelfile | Select-Object -First 30
# FROM은 캐시된 모델, SYSTEM은 자기 팀명으로 수정한 뒤 실행한다.
ollama create student01-helper -f Modelfile
ollama list
ollama show student01-helper
uv run python chat.py --prompt "uv가 무엇인지 두 문장으로 설명해 줘." --tag base-1
uv run python chat.py --model student01-helper --prompt "uv가 무엇인지 두 문장으로 설명해 줘." --tag helper-1
# 보고서의 Q2·Q3도 같은 방식으로 실행한다.
```

## 예상 결과와 완료 확인

커스텀 모델이 목록에 보이고 질문 3개 × 기준·커스텀 모델의 JSON 6개 이상이 생긴다. SYSTEM 한 줄 변경 후 v2와 요청 `--system` 충돌 결과까지 보고서에 적는다. 모델 답이 지시와 다르면 그대로 관찰로 남긴다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

실습지 문제 2대로 SYSTEM 한 줄만 바꿔 다시 create하고 같은 질문을 재실행한다. 2교시에 만든 `--seed` 구현을 이어 쓰려면 자신이 수정한 `period2/chat.py`를 이 폴더의 복사본에 반영한다. 기본 문제 실행에는 다른 교시 코드가 필요 없다.

## CPU·네트워크 대체 경로

GPU가 없으면 Modelfile의 FROM과 `.env` 모두 같은 캐시된 소형 모델을 가리키게 한다. create가 다운로드하려 하면 중단하고 FROM 이름을 확인한다. 네트워크 없이도 로컬 모델과 의존성이 준비되어 있으면 진행할 수 있다.
