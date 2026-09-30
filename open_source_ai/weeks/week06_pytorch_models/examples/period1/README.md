# 6주차 1교시 — 텐서 이동과 자동미분 관찰

**역할: 1교시 텐서·장치·자동미분 참조 구현.** [실습지의 1교시](../../lab.md#1교시-실습--텐서-이동과-자동미분-관찰)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 문제 1, 크기별 시간·복사 비교 | `tensor_basics.py`의 1~4절 | `outputs/tensor_report*.json`·`tensor_compare.md` |
| 문제 2, 자동미분·no_grad·실패 | `tensor_basics.py`의 5~6절, `runlog.py`의 장치·seed 함수 | 메모리/grad 기록·장치 오류 |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week06_pytorch_models\examples"
$dst = "$HOME\osa-practice\week06"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period1")) { Copy-Item -Recurse "$src\period1" "$dst\period1" }
Set-Location "$dst\period1"
uv sync                    # 수업 전에 설치·캐시한다
```

Python 명령은 현재 `period1` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 1교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | pipeline 한 줄을 열면 |
| 3–6분 | Tensor 세 속성 |
| 6–9분 | CPU↔GPU 이동과 시간 측정 |
| 9–12분 | dtype과 메모리 |
| 12–15분 | 자동미분과 `no_grad` |
| 15–17분 | 모델 = 파라미터 + `forward` |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#1교시-실습--텐서-이동과-자동미분-관찰)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 행렬 크기 3개의 GPU 배속과 `no_grad` 메모리 차이를 예상표에 적기 |
| 기본 실행 | 5–12분 | `tensor_basics.py` 기본 실행, 여섯 절 출력과 `tensor_report.json` 읽기 |
| 크기 비교 | 12–21분 | `--size` 3개로 실행, 시간·복사 비교표 작성, 교차점 찾기 |
| `no_grad` 관찰 | 21–25분 | `--batch`·`--layers`를 키워 활성화 메모리 차이 확인 |
| 검증·기록 | 25–30분 | 실패 경로 재현, `tensor_compare.md` 완성, `evidence/` 복사 |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
uv run python tensor_basics.py
uv run python tensor_basics.py --size 256 --output outputs/tensor_report-256.json
uv run python tensor_basics.py --size 4096 --output outputs/tensor_report-4096.json
uv run python tensor_basics.py --batch 4096 --layers 8 --output outputs/tensor_report-nograd.json
uv run python tensor_basics.py --device cuda:9
```

## 예상 결과와 완료 확인

여섯 절의 텐서 속성·시간·dtype·forward·grad·no_grad가 출력되고 JSON으로 저장된다. 행렬 크기 3개 비교와 없는 장치 실패를 `tensor_compare.md`에 적는다. GPU가 없으면 GPU 수치를 만들지 않는다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

실습지 문제 1·2대로 `--size`, `--batch`, `--layers`만 바꿔 시간과 메모리 차이를 비교한다. `runlog.py`에는 이번 교시에 쓰는 seed·장치·동기화 함수만 있다.

## CPU·네트워크 대체 경로

모델 다운로드가 필요 없다. GPU가 없으면 `--device cpu`, 4096 행렬 대신 `--size 1024 --repeat 1`, no_grad는 grad_fn·requires_grad로 비교한다. torch·numpy를 미리 설치하고 `uv sync --offline`으로 캐시를 확인한다.
