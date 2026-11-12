# 7주차 실습 — 데이터 수정, 학습, 저장, 다시 대화

## 준비

Python 버전과 패키지 구조를 먼저 확인한다. 4~6주차와 같은 구조를 Python 3.12로 직접 만든다. `my-lora` 폴더가 이미 있으면 다른 이름을 쓴다.

```powershell
New-Item -ItemType Directory -Force "C:\classwork" | Out-Null
Set-Location C:\classwork
uv init --package --python 3.12 --vcs none my-lora
Set-Location my-lora
uv add langchain-ollama
uv run my-lora
```

`Hello from my-lora!`가 나오면 성공이다. `.python-version`, `pyproject.toml`의 `[project.scripts]`·`[build-system]`, `src/my_lora/__init__.py`의 `main()`을 열어 본다. `uv add`가 `dependencies`에 패키지를 적어 넣은 것도 확인한다. 교재 예제는 이 구조에 명령 일곱 개(`prepare`, `ex01`~`ex06`)와 `shared` 패키지를 더한 것이다. 기존 프로젝트에 새 명령을 반영한 뒤에는 `uv sync`를 다시 실행한다.

교재의 `examples` 전체를 개인 실습 폴더에 복사하고 그 루트에서 명령을 실행한다. 세 교시는 같은 프로젝트를 이어 쓴다. `C:\classwork\week07`이 이미 있으면 그 안에 `examples` 폴더가 한 겹 더 생기므로 다른 이름을 쓴다.

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

`ollama list`에 `qwen3.5:2b`가 있어야 한다. `uv run prepare`는 학습용 모델 `Qwen/Qwen2.5-0.5B-Instruct`를 내려받고 `모델 준비 완료`를 출력한다. 설치와 모델 다운로드는 수업 전에 마친다. 교시별 `period` 폴더에는 실행 파일이 아니라 소스 안내만 있다. 개인 저장소의 `experiments/run-001.md`에 [기록 양식](examples/EXPERIMENT_TEMPLATE.md)을 복사해 관찰을 적는다.

NVIDIA PC는 [CUDA용 PyTorch 설치 설정](examples/README.md#cuda용-pytorch-설치-설정)을 확인한다. TOML에는 `cu128` 저장소와 `torch` 출처가 이미 지정되어 있다. 위 확인 명령에서 `12.8 True`, `prepare`에서 `장치: cuda`가 나오는지 확인한다. `None False`이면 CPU용 빌드이고, 버전은 있으나 `False`이면 GPU·드라이버 호환성 등을 확인한다. TOML을 바꾸면 `uv lock` → `uv sync`로 잠금 파일도 갱신한다. macOS의 MPS·GPU 없는 PC의 CPU 경로에서는 CUDA가 `False`인 것이 정상이다.

## 1교시 실습 — Ollama 대화와 학습 도구 연결

| 시간 | 활동 |
|---|---|
| 0–8분 | `ex01` 대화와 형식 지시 |
| 8–18분 | `ex02` 대화, `ex01`과 같은 형식 지시 주기, 토큰 변환·생성·디코딩 코드 읽기 |
| 18–25분 | 프롬프트·RAG·학습의 차이 설명 |
| 25–30분 | 비교할 질문 선택과 기록 |

1. `uv run ex01`에서 `아테나를 소개해 줘.`와 `포세이돈은 어떤 신이야?`를 입력한다. `/bye`로 종료한다.
2. [ex01](examples/src/ex01_ollama/__init__.py)의 `PROMPT` 줄을 다음처럼 바꿔 형식 지시를 덧붙인다.

   ```python
   PROMPT = SYSTEM_PROMPT + " 이름, 소개, 기억할 점을 한 줄씩 답하세요."
   ```

   같은 명령과 질문으로 다시 실행하고 답이 이름·소개·기억할 점 세 줄로 나뉘는지 적는다. 지시문만 바꿨고 학습은 하지 않았다. 확인 후 `PROMPT = SYSTEM_PROMPT`로 되돌린다.
3. `ex01`을 `/bye`로 끝낸 뒤 `ollama stop qwen3.5:2b`를 실행한다. 대화를 끝내도 Ollama 모델이 GPU 메모리에 남아 있을 수 있으므로 모델을 내려 메모리를 확보한다. `MODEL`을 바꿨다면 그 모델 이름을 쓴다. 이어서 `uv run ex02`를 실행해 같은 두 질문을 입력한다. 작은 모델로 바뀌었으므로 답변 수준이나 문장이 다를 수 있다. 아직 학습하지 않았다는 점을 적는다. 빈 줄을 입력해 건너뛰는지 확인하고 `/bye`로 종료한다.
4. [ex02](examples/src/ex02_transformers/__init__.py)의 `PROMPT`도 2번과 같은 줄로 바꿔 같은 두 질문을 한다. 2B 모델과 비교해 0.5B 모델이 세 줄 형식을 따르는지 적는다. 따르지 못했다면, 지시 대신 원하는 답변 예시로 형식을 가르치는 것이 2교시의 학습이다. 따랐다면 그 결과를 그대로 적는다. 확인 후 `PROMPT = SYSTEM_PROMPT`로 되돌린다.
5. [shared](examples/src/shared/__init__.py)의 `load_model()`과 `answer()`를 읽는다. `load_model()`은 `AutoTokenizer`와 `AutoModelForCausalLM`으로 토크나이저와 모델을 불러온다. `answer()`에서는 `apply_chat_template`이 대화문을 토큰으로 바꾸고, `generate`가 다음 토큰을 생성하며, `decode`가 생성한 토큰을 글로 바꾼다. 이 세 호출을 소스에서 찾는다.
6. 다음을 자기 말로 설명한다. “4·5주차에는 지시문을, 6주차에는 검색한 자료를 입력에 넣었다. 이번 주에는 예시 답변으로 무엇을 바꾸는가?”
7. 3교시에 다시 물어볼 질문 두 개를 기록한다. `ex01`의 2B 모델과 `ex02`의 0.5B 모델을 학습 전후로 묶지 않는다.

완료 조건: 두 방식으로 질문을 반복하고 종료했다. 같은 형식 지시에 2B와 0.5B가 어떻게 답했는지 적었다. 실행과 학습의 차이를 설명하고, 아직 학습하지 않은 0.5B 모델의 답변을 남겼다.

힌트: Ollama가 모델을 실행하는 일을 맡아 주었다면, Transformers 예제에서는 Python이 모델을 직접 불러온다. 학습할 부분을 붙이기 위해 모델을 Python에서 다룬다. 자세한 텐서 연산은 이번 실습의 선행 조건이 아니다.

## 2교시 실습 — 내 답변 예시로 LoRA 학습

| 시간 | 활동 |
|---|---|
| 0–8분 | 데이터 읽기와 항목 이름 바꾸기 |
| 8–12분 | 학습 코드에서 붙이기·학습·저장 찾기 |
| 12–25분 | 학습 실행, loss와 저장 파일 확인 |
| 25–30분 | 실제 설정과 관찰 기록 |

1. [sample_sft.jsonl](examples/src/shared/data/sample_sft.jsonl)을 연다. 한 줄이 질문 `instruction`과 원하는 답변 `output` 한 쌍이다. `\n`은 답변의 줄바꿈이다. 24건 모두 `이름:`, `소개:`, `기억할 점:` 세 줄로 답한다.
2. 답변 형식을 내 것으로 바꾼다. VS Code에서 이 파일을 연 채 `Ctrl+H`를 누른다. 찾을 내용에 `기억할 점:`, 바꿀 내용에 자기가 정한 항목 이름(예: `한 줄 요약:`)을 넣고 **모두 바꾸기**를 누른다. 끝의 `:`은 남기고, 이름에 큰따옴표(`"`)나 역슬래시(`\`)는 쓰지 않는다. 24곳이 모두 바뀌었는지 확인하고 바꾼 이름과 고른 이유를 기록한다.
3. 선택: 인물 한 명의 답변 내용을 자기가 아는 다른 사실로 고친다. 예를 들어 제우스 답변 마지막 줄에서 항목 이름은 그대로 두고 뒤의 문장만 바꿔 `한 줄 요약: 독수리와 참나무도 제우스의 상징입니다.`처럼 만든다. 3교시에 그 인물을 물어 고친 내용이 나오는지 본다.
4. [ex03](examples/src/ex03_train/__init__.py)에서 `get_peft_model`, `trainer.train()`, `save_pretrained`를 찾는다. 각각 LoRA 붙이기, 학습, 저장에 해당한다. `Trainer`와 마스킹 구현을 새로 작성할 필요는 없다.
5. `uv run ex03`을 실행한다. 처음 출력되는 학습 데이터 답변(제우스)에 바꾼 항목 이름이 보이는지 확인한다. loss는 학습 예시를 얼마나 잘 맞추는지 보는 값이다. loss 줄 하나가 한 step이며 n번째 줄이 step n이다. 줄 끝의 `epoch`는 24건을 몇 바퀴 돌았는지를 나타낸다. 두 지점의 실제 step과 loss를 적되 모든 step에서 감소한다고 가정하지 않는다.
6. `adapters/run-001/`의 `adapter_config.json`과 `adapter_model.safetensors`를 확인한다. 토크나이저 파일도 함께 저장된다. 기본 모델 전체를 저장한 것은 아니다.
7. 기록에 `STEPS`, `LEARNING_RATE`, `RANK`, 모델 ID, 사용 장치와 바꾼 항목 이름을 남긴다. 학습 시간이 길면 강의자가 준비한 CPU 대체 경로를 따른다.

완료 조건: 항목 이름을 바꾼 데이터로 학습을 실행하고 어댑터를 저장했다. loss와 실행 결과를 실제 값으로 기록했다. 어댑터가 기본 모델과 함께 필요하다는 점을 설명했다.

힌트: JSON 오류는 오류가 가리키는 줄의 따옴표·쉼표부터 본다. 바꾸기는 `sample_sft.jsonl` 안에서만 한다. 길이 오류가 나면 답변을 줄인다. CPU 대체는 `ex03`의 `STEPS = 3`, `shared`의 `DEVICE = "cpu"`로 실행한다. 3 step은 실행 경로 확인용이며 형식 학습을 보장하지 않는다. 강의자 어댑터로 비교를 이어 가면 강의자가 알려 준 그 어댑터의 항목 이름이 나오는지로 형식을 판단한다. 이미 저장한 `run-001`은 공용 `ADAPTER_DIR`을 `run-002`로 바꿔 보존한다.

## 3교시 실습 — 저장한 결과로 다시 대화

| 시간 | 활동 |
|---|---|
| 0–5분 | 새 실행에서 어댑터 불러오기 |
| 5–17분 | 같은 질문의 학습 전후 비교 |
| 17–25분 | 기록 작성 또는 병합 모델 Python 대화 선택 실습 |
| 25–30분 | 변화·한계·다음 실험 설명 |

1. `uv run ex04`를 새로 실행한다. 입력 하나마다 `학습 전>`과 `학습 후>`가 나온다. 이는 같은 기본 모델에서 어댑터만 끄고 켠 결과다.
2. 1교시에 고른 두 질문과 [eval_prompts.json](examples/src/shared/data/eval_prompts.json)의 질문 중 세 개를 입력한다. 학습에 없는 인물과 신화 밖 질문을 각각 하나 포함한다. 이 파일은 질문 목록이며 프로그램이 자동으로 읽어 평가하는 파일은 아니다.
3. 적어도 세 질문의 실제 답변을 기록한다. 바꾼 항목 이름으로 세 줄이 나왔는지(형식), 내용이 맞는지(사실), 반복·잘림이 있는지를 따로 적는다. 2교시에 사실을 고쳤다면 그 인물도 물어 고친 내용이 나오는지 적는다. 형식만 맞고 틀린 답을 개선으로 단정하지 않는다.
4. `/bye`로 종료하고 `uv run ex04`를 다시 실행해 같은 질문을 해 본다. 저장된 파일로 다시 동작하는지 확인한다. 학습 이력을 다시 실행할 필요는 없다.
5. 선택: [병합 모델 Python 대화](examples/README.md#병합한-모델로-python에서-대화하기)에 따라 `uv run ex05` → `uv run ex06`을 실행한다. `models/merged-run-001/`에는 작은 어댑터만이 아니라 모델·토크나이저 전체가 저장된다(약 2 GB). 질문 두 개와 빈 줄을 입력하고 `/bye`로 종료한다. 질문마다 독립적으로 답한다는 점을 확인한다. Ollama에서 실행하려면 별도 선택 경로인 [Ollama 가져오기](examples/README.md#ollama로-다시-대화하기)를 따른다.
6. 기록 마지막에 변화가 있었던 부분, 그대로거나 나빠진 부분, 다음에 바꿀 한 가지를 적는다. 형식과 사실 중 학습으로 바뀐 것은 무엇인지, 사실에 맞게 답하게 하려면 6주차의 어떤 방법을 쓸지 한 문장으로 적는다. 기록과 데이터·코드 변경만 커밋한다. 어댑터·병합 모델·가상환경은 제외한다.

완료 조건: 저장한 어댑터로 대화를 다시 실행했다. 같은 조건의 전후 답변과 해석이 있다. 프롬프트 변경·학습·모델 병합·Ollama 등록을 구분한다. 병합 모델 Python 대화와 Ollama 가져오기 성공은 학생 필수 완료 조건에 추가하지 않는다.

## 선택 심화

기본 실습을 마친 경우에만 [심화 안내](examples/advanced.md)에 따라 rank 비교, 메모리 관찰, 답변만 학습하는 마스킹을 살펴본다. 형식이 달라지지 않았다면 데이터를 더 일관되게 만들거나 학습 step을 바꾸되 한 번에 한 조건만 변경한다. 재학습 전에는 새 어댑터 경로를 지정한다.

[추가로 생각해 볼 일: 자료에 없는 질문과 답변 거절](examples/advanced.md#추가로-생각해-볼-일-자료에-없는-질문과-답변-거절)에서는 프롬프트, 거절 예시 학습, RAG와 코드 검사, 고정 답변을 비교한다. 같은 주제라도 자료로 답할 수 없는 질문을 구분하고, 정상 질문을 잘못 거절하는 경우도 기록한다. 구현이나 추가 학습은 필수 과제가 아니다.
