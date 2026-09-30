# 4주차 1교시 — 모델 두 개를 실행하고 측정하기

**역할: 1교시 실습 기록 도우미와 보고서 양식.** [실습지의 1교시](../../lab.md#1교시-실습--모델-두-개를-실행하고-측정하기)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 문제 1·2, 기본·소형 모델 실측 | `ollama_probe.ps1` | `outputs/probe-*.txt` |
| 문제 1·2, 예상·비교·계산·결론 | `model_report_template.md` | 상위 폴더의 `model_report.md` 1~4절 |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week04_ollama_local_llm\examples"
$dst = "C:\classwork\week04"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period1")) { Copy-Item -Recurse "$src\period1" "$dst\period1" }
Set-Location "$dst\period1"
if (-not (Test-Path ..\model_report.md)) { Copy-Item model_report_template.md ..\model_report.md }
```

Python 명령은 현재 `period1` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 1교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | 이어받는 것: 설정에서 호출로 |
| 3–6분 | LLM 실행 구조 세 조각 |
| 6–9분 | 양자화: 같은 모델, 다른 바이트 |
| 9–12분 | 파라미터 수 → VRAM 어림 계산 |
| 12–15분 | Ollama의 네 부분 |
| 15–17분 | 오늘 쓰는 CLI 다섯 개 |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#1교시-실습--모델-두-개를-실행하고-측정하기)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 두 모델의 파일 크기·메모리·tokens/s를 예상표에 적기 |
| 기본 모델 실측 | 5–13분 | `ollama show` → `ollama run` + `/set verbose` + 질문 3개 → `ollama ps` |
| 소형 모델 실측 | 13–20분 | 같은 절차를 소형 모델로 반복 |
| 답 비교·계산 | 20–25분 | 질문 3개의 답 차이, 파라미터 수 × 바이트 계산과 실측 대조 |
| 검증·기록 | 25–30분 | `model_report.md` 1~4절 완성, `ollama_probe.ps1` 출력 저장 |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
ollama list
ollama show qwen3:8b
ollama run qwen3:8b
# Ollama 프롬프트에서 /set verbose → 보고서의 질문 3개 → /bye
ollama ps
.\ollama_probe.ps1 -Model qwen3:8b
# qwen3:0.6b로 같은 절차를 반복한다.
```

## 예상 결과와 완료 확인

두 모델의 파라미터·양자화·파일 크기·메모리·tokens/s와 같은 질문 3개의 답 차이를 기록한다. `outputs/probe-*.txt`에는 list/show/ps 결과가 남는다. 실제 숫자는 PC와 실행 조건에 따라 달라진다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

실습지 확장대로 `num_ctx`만 바꿔 `ollama ps`의 메모리 변화를 비교한다. 질문 3개는 그대로 둔다.

## CPU·네트워크 대체 경로

GPU가 없으면 캐시된 소형 모델로 실행하고 CPU 사용 사실을 기록한다. 소형 모델 두 개도 없으면 가능한 모델의 실측과 강의자 제공 비교 기록을 구분한다. 네트워크는 모델·Ollama가 사전 준비되어 있으면 필요 없다. 모델이 없다면 수업 중 다운로드하지 않고 캐시 상태를 확인한다.
