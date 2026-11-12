# 7주차 예제 — 대화에서 학습으로

5주차처럼 `examples/` 하나가 uv 프로젝트다. 모든 명령은 이 폴더의 개인 복사본에서 실행한다. 교시가 바뀌어도 프로젝트·가상환경·어댑터를 이어 쓴다.

## 프로젝트 구조

```text
examples/
├── pyproject.toml / uv.lock / .python-version
├── Modelfile
├── src/
│   ├── ex01_ollama/__init__.py
│   ├── ex02_transformers/__init__.py
│   ├── ex03_train/__init__.py
│   ├── ex04_compare/__init__.py
│   ├── ex05_merge/__init__.py
│   └── shared/
│       ├── __init__.py
│       ├── training.py
│       └── data/   # sample_sft.jsonl, eval_prompts.json
└── period1~3/README.md
```

`[project.scripts]`가 `uv run ex01`을 `ex01_ollama`의 `main()`과 연결한다. `[build-system]`의 `uv_build`는 이 소스를 설치 가능한 패키지로 만든다. `shared`에는 여러 예제가 함께 쓰는 모델 설정·대화 함수·데이터만 둔다. scripts를 고쳤으면 `uv sync`를 다시 실행한다. 예제끼리 직접 import하지 않는다.

## 수업 전 준비

빈 연습 프로젝트로 Python 버전과 패키지 구조를 확인한다. 이미 같은 이름의 폴더가 있으면 새 이름을 쓴다.

```powershell
New-Item -ItemType Directory -Force "C:\classwork" | Out-Null
Set-Location C:\classwork
uv init --package --python 3.12 --vcs none my-lora
Set-Location my-lora
uv add langchain-ollama
uv run my-lora
```

`.python-version`, `src/my_lora/__init__.py`의 `main()`, `pyproject.toml`의 scripts·build-system과 `uv add`가 적어 넣은 `dependencies`를 연다. 이어서 교재 `examples/` 전체를 **새 개인 폴더** `C:\classwork\week07`에 한 번만 복사한다. 이 폴더가 이미 있으면 그 안에 `examples`가 한 겹 더 생기므로 다른 이름을 쓴다. 교재 저장소의 `examples` 안에 `.venv`나 실행 산출물이 있으면 복사본에서 지운다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week07_peft_lora\examples"
$dst = "C:\classwork\week07"
Copy-Item -Recurse $src $dst
Set-Location $dst
uv sync --locked
uv run python -c "import torch; print(torch.__version__); print(torch.version.cuda, torch.cuda.is_available())"
ollama list
uv run prepare
```

Ollama에는 앞 주차의 `qwen3.5:2b`가 필요하다. `prepare`는 별도의 학습용 모델 `Qwen/Qwen2.5-0.5B-Instruct`와 토크나이저를 다운로드·로드한다. Ollama의 모델 캐시와 Hugging Face 캐시는 서로 다르다. 작은 모델도 다운로드와 메모리가 필요하므로 수업 시간에 처음 준비하지 않는다.

## CUDA용 PyTorch 설치 설정

Ollama에서 GPU를 쓰고 있어도 Python 프로젝트의 PyTorch가 CUDA용이라는 뜻은 아니다. `shared`의 `DEVICE = "auto"`는 **설치된 PyTorch가 사용할 수 있는 장치**를 고르며, CPU용 PyTorch를 CUDA용으로 바꾸지는 않는다.

교재 [pyproject.toml](pyproject.toml)에는 `[project]`의 `dependencies`에 `"torch>=2.6,<3"`과 아래 설정이 이미 들어 있다. 복사본에는 중복해서 추가하지 않는다. 새 프로젝트에서 같은 설정을 만들 때는 의존성 선언과 저장소 설정을 함께 넣는다.

```toml
[[tool.uv.index]]
name = "pytorch-cuda"
url = "https://download.pytorch.org/whl/cu128"
explicit = true

[tool.uv.sources]
torch = [
  { index = "pytorch-cuda", marker = "sys_platform == 'win32' or sys_platform == 'linux'" },
]
```

| 항목 | 의미 |
|---|---|
| `[[tool.uv.index]]` | 패키지 설치 파일을 받을 저장소를 등록한다. `pytorch-cuda`는 이 프로젝트에서 붙인 이름이다. |
| URL의 `cu128` | CUDA 12.8용 PyTorch 빌드를 뜻한다. 교재의 기존 예시이며 모든 PC에 맞는 최신 권장값이라는 뜻은 아니다. GPU·드라이버·PyTorch의 지원 조합을 확인해 학기별 환경 기준표에서 정한다. |
| `explicit = true` | `sources`에서 이 저장소를 명시한 패키지만 여기서 받는다. 나머지 일반 패키지는 기본 PyPI에서 받는다. |
| `[tool.uv.sources]`의 `torch` | 의존성 `torch`의 다운로드 출처를 위 저장소에 연결한다. 저장소 등록만으로는 이 연결이 생기지 않는다. |
| `marker` | Windows(`win32`)·Linux에만 CUDA 저장소를 적용한다. GPU 유무를 검사하는 조건은 아니다. macOS에서는 PyPI 패키지를 설치하고 실행 시 MPS 또는 CPU를 고른다. |

배포된 TOML과 `uv.lock`을 그대로 쓰면 `uv sync --locked`로 설치한다. 강의자가 GPU·드라이버에 맞춰 저장소 URL 등을 **변경했다면** 다음 순서로 잠금 파일을 갱신하고 설치한다. `--locked`는 설정 변경을 반영해 잠금 파일을 고치는 옵션이 아니며, 갱신이 필요하면 오류로 멈춘다. 새 프로젝트에는 `uv lock`이 잠금 파일을 생성한다.

```powershell
uv lock
uv sync
```

변경한 `pyproject.toml`과 `uv.lock`은 함께 배포한다. 별도의 `pip install torch`로 가상환경만 바꾸면 다음 `uv sync`에서 프로젝트 설정에 따른 설치로 돌아갈 수 있다.

### NVIDIA GPU에서 설치와 실행 확인

프로젝트 루트에서 실행한다. GPU가 없는 PC와 macOS에서는 `nvidia-smi` 단계를 건너뛴다.

```powershell
nvidia-smi
uv run python -c "import torch; print(torch.__version__); print(torch.version.cuda, torch.cuda.is_available())"
uv run prepare
```

`nvidia-smi`에서는 GPU와 드라이버를 확인한다. 여기에 표시되는 `CUDA Version`은 드라이버가 지원하는 CUDA 상한이며, 설치된 PyTorch의 CUDA 버전과 반드시 같아야 하는 값은 아니다. PyTorch 빌드는 `torch.version.cuda`로, GPU 사용 가능 여부는 `torch.cuda.is_available()`로 확인한다.

| 확인 결과 | 해석과 다음 행동 |
|---|---|
| `12.8 True` | 이 예시의 CUDA 빌드를 설치했고 GPU를 사용할 수 있다. `uv run prepare`에도 `장치: cuda`가 나오는지 확인한다. |
| `None False` | CPU용 PyTorch다. 현재 프로젝트의 TOML·잠금 파일·`uv sync --locked` 실행 위치를 확인한다. |
| `12.8 False`처럼 버전은 있으나 `False` | CUDA용 패키지는 설치했지만 GPU를 사용할 수 없다. NVIDIA GPU 유무, 드라이버·GPU와 해당 빌드의 호환성, GPU 접근 설정을 확인한다. |
| `True`인데 `prepare`에 `장치: cpu` | `src/shared/__init__.py`의 `DEVICE`를 `"cpu"`로 바꿨는지 확인한다. 자동 선택은 `"auto"`다. |

`True`만으로 모델 로드·학습까지 검증한 것은 아니다. `prepare`에서 장치와 모델 로드를 확인한 뒤 `ex03`의 실제 학습 결과를 확인한다. macOS에서는 CUDA가 `False`여도 MPS를 사용할 수 있으며, GPU가 없는 환경에서는 기존 CPU 대체 경로를 따른다.

공식 근거: [uv의 PyTorch 설치 설정](https://docs.astral.sh/uv/guides/integration/pytorch/) · [PyTorch 설치와 GPU 확인](https://pytorch.org/get-started/locally/) · [NVIDIA SMI의 CUDA Version 설명](https://docs.nvidia.com/deploy/nvidia-smi/index.html)

## 실행 순서

| 명령 | 하는 일 | 학생이 할 일 |
|---|---|---|
| `uv run ex01` | 기존 Ollama 모델과 대화 | [ex01](src/ex01_ollama/__init__.py)의 `PROMPT`에 형식 지시 덧붙이기 |
| `uv run ex02` | Transformers로 작은 모델과 대화 | [ex02](src/ex02_transformers/__init__.py)의 `PROMPT`에 같은 지시 덧붙이기, [shared](src/shared/__init__.py)의 생성 과정 읽기 |
| `uv run ex03` | LoRA 학습·어댑터 저장 | [학습 데이터](src/shared/data/sample_sft.jsonl)의 `기억할 점:`을 자기 항목 이름으로 바꾸기 |
| `uv run ex04` | 저장한 어댑터를 끄고 켜며 전후 비교 | [비교 질문](src/shared/data/eval_prompts.json) 입력 |
| `uv run ex05` | 기본 모델에 어댑터를 합쳐 저장 | 시연 보기, 원하면 직접 실행 |

`ex01`, `ex02`, `ex04`는 빈 줄을 건너뛰고 `/bye`·입력 종료로 끝난다. 질문마다 독립적으로 답하므로 앞 대화를 기억하지 않는다. `ex04`는 질문 하나에 학습 전·후 답을 모두 출력한다. 긴 질문이나 답변이 잘리면 공용 `MAX_NEW_TOKENS`를 확인한다.

바꿀 값은 소스 위쪽의 상수로 둔다. `.env`와 명령행 옵션은 없다. 실행 결과 JSON을 따로 만들지 않고 관찰을 [실험 기록 양식](EXPERIMENT_TEMPLATE.md)에 적는다.

## 학습과 저장

원본 가중치를 고정하고 LoRA 부분만 학습한다. 기본은 24건, 30 step, rank 8이다. 이는 저장·복원과 형식 변화를 관찰하는 작은 실험이며 품질 개선을 보장하는 설정은 아니다. 교재 검증 PC에서는 `기억할 점:`을 바꾼 새 항목 이름이 학습 뒤 대부분의 답에 나왔고(이름에 따라 일부 질문에서는 빠졌다), 답변 내용을 고친 부분은 답에 나오지 않았다. 느린 CPU에서는 [ex03](src/ex03_train/__init__.py)의 `STEPS = 3`, [shared](src/shared/__init__.py)의 `DEVICE = "cpu"`로 실행할 수 있다.

`adapters/run-001/`에 `adapter_config.json`과 `adapter_model.safetensors`가 생긴다. 어댑터는 기본 모델 전체가 아니므로 같은 기본 모델이 필요하다. 다시 학습할 때는 기존 어댑터를 덮어쓰지 않도록 공용 `ADAPTER_DIR`을 `adapters/run-002`로 바꾼다. 학습·비교·병합이 모두 이 경로를 쓴다.

## Ollama로 다시 대화하기

3교시 설명 시간에 강의자가 병합·GGUF 변환·가져오기를 시연한다. 학생은 전후 비교를 마친 뒤 선택해서 따라 한다. 변환 도구는 [강의자 준비 순서](ollama_import.md)에 따라 수업 전에 설치한다. 프로젝트 루트에서 실행한다.

```powershell
uv run ex05
# ollama_import.md의 변환 명령으로 models/week07-lora.gguf 생성
ollama create week07-lora -f Modelfile
ollama run week07-lora
```

`Modelfile`의 `FROM`은 `models/week07-lora.gguf`를 가리킨다. 병합은 학습한 변화를 기본 가중치에 합치는 작업이고, GGUF 변환은 실행할 파일 형식을 바꾸는 작업이다. `ollama create`는 그 결과를 Ollama에 등록한다. `SYSTEM`만 바꿔 모델을 만드는 것은 학습이 아니다.

병합 폴더는 float32 기본 모델 전체를 담으므로 약 2 GB이고, GGUF(f16) 파일에 약 1 GB가 더 필요하다. `ollama create`로 등록하면 GGUF가 Ollama 저장소에 한 번 더 저장된다. 어댑터 가중치 파일(약 2 MB)보다 훨씬 크므로 디스크 여유 공간을 먼저 확인한다.

등록 후 [ex01](src/ex01_ollama/__init__.py)의 `MODEL`을 `"week07-lora"`로 바꾸면 `uv run ex01`의 같은 입력 반복문으로 대화할 수 있다. Ollama의 자체 대화 명령과 달리 이 예제는 이전 질문을 누적하지 않는다. 실행기·정밀도가 달라질 수 있으므로 학습 효과의 비교 근거는 `ex04`로 남긴다.

가져오기에는 해당 구조를 지원하는 Ollama 버전이 필요하다. 강의자는 기준 PC에서 병합 → 변환 → 등록 → 질문 응답까지 사전에 확인한다. 실습 중 변환 도구 설치로 시간을 쓰지 않고 필수 비교는 `ex04`까지 완료한다. Safetensors 직접 가져오기는 모든 모델 구조를 지원하는 경로가 아니므로 이 모델은 안내한 GGUF 경로를 사용한다.

## 데이터와 다음 단계

신화 자료는 공개 영역의 이야기를 교재용으로 새로 요약한 24건이다. 특정 번역본을 복사하지 않았다. 기본 목표 답변은 `이름:`, `소개:`, `기억할 점:` 세 줄이며, 2교시에 `기억할 점:`을 각자 정한 이름으로 바꾼다. 비교 질문은 학습 문장과 표현을 달리했지만 주제가 겹친다. 독립된 일반화 성능 시험으로 부르지 않는다.

rank·VRAM·마스킹 구현은 [선택 심화](advanced.md)에서 다룬다. 필수 실습의 완료 조건은 [실습지](../lab.md)를 따른다.
