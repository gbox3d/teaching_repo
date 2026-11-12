# 7주차 따라하기

## 실행 폴더와 모델 준비

[예제 준비](examples/README.md#수업-전-준비)를 마친 개인 복사본에서 시작한다. 세 교시 모두 같은 프로젝트 루트다.

```powershell
Set-Location C:\classwork\week07
uv sync --locked
uv run python -c "import torch; print(torch.__version__); print(torch.version.cuda, torch.cuda.is_available())"
uv run prepare
```

모델 준비 완료가 출력되면 Hugging Face 모델을 사용할 수 있다. Ollama 모델은 `ollama list`에서 별도로 확인한다. 다운로드는 수업 전에 끝낸다.

NVIDIA PC에서는 CUDA 확인 결과가 `12.8 True`인지, `prepare`가 `장치: cuda`를 출력하는지 확인한다. TOML의 저장소·출처 설정과 결과 해석은 [CUDA용 PyTorch 설치 설정](examples/README.md#cuda용-pytorch-설치-설정)을 따른다. `DEVICE = "auto"`만으로 CPU용 PyTorch가 CUDA용으로 바뀌지는 않는다. macOS는 MPS, GPU가 없는 PC는 CPU 경로로 이어 간다.

## 1교시: 질문 입력을 유지하며 도구를 바꾼다

`uv run ex01`에서 `아테나를 소개해 줘.`를 입력한다. 답이 끝나면 다른 질문을 입력한다. 종료는 `/bye`다. `PROMPT`에 세 줄 형식 지시를 덧붙여 같은 질문을 하고 결과를 기록한 뒤 원래 지시로 되돌린다.

`/bye`로 대화를 끝내도 Ollama 모델은 GPU 메모리에 남아 있을 수 있다. `ex02`로 넘어가기 전에 `ollama stop qwen3.5:2b`로 모델을 내려 GPU 메모리를 확보한다. `ex01`의 `MODEL`을 바꿨다면 그 모델 이름을 쓴다.

`uv run ex02`를 실행하면 학습용 모델 ID와 장치가 먼저 나온다. 같은 질문을 입력하고 `/bye`로 종료한다. 여기까지는 학습이 아니다. 2B 모델에서 0.5B 모델로 바뀐 이유는 짧은 실습에서 학습을 실행하기 위해서다.

`ex02`의 `PROMPT`에도 `ex01`과 같은 형식 지시를 덧붙여 같은 질문을 한다. 교재 검증 PC(macOS)에서 2B는 이름·소개·기억할 점 세 줄로 답했고, 0.5B는 형식 없이 한두 문장으로 답했다. 학생 PC에서는 결과가 다를 수 있으므로 자기 화면의 답을 적는다. 지시를 따르지 못하는 작은 모델에 답변 예시로 형식을 가르치는 것이 2교시의 학습이다. 확인 후 `PROMPT = SYSTEM_PROMPT`로 되돌린다.

## 2교시: 항목 이름 바꾸기와 학습

`src/shared/data/sample_sft.jsonl`을 VS Code로 열고 `Ctrl+H`로 `기억할 점:`을 자기가 정한 항목 이름(예: `한 줄 요약:`)으로 모두 바꾼다. 한 줄에 JSON 하나이며 `\n`은 출력에서 줄바꿈이 된다. `uv run ex03`을 실행하면 첫 학습 답변(제우스), 학습 가능한 파라미터 수, step별 loss가 나온다. 첫 답변의 마지막 줄이 새 항목 이름으로 시작하면 바꾼 파일로 학습하는 것이다. 마지막에 어댑터 저장 경로가 출력된다.

예상 파일은 `adapters/run-001/adapter_config.json`과 `adapter_model.safetensors`다. loss 값과 소요 시간은 실행 환경과 수정 데이터에 따라 달라지므로 교재의 고정 정답으로 비교하지 않는다.

## 3교시: 어댑터를 새로 불러와 비교

`uv run ex04`를 실행해 같은 질문을 입력한다. `학습 전>`은 어댑터를 끈 답변, `학습 후>`는 켠 답변이다. 양쪽은 같은 모델·system 지시·생성 길이·greedy 생성 조건을 사용한다.

`다이달로스를 소개해 줘.`와 `uv.lock 파일은 어떤 역할을 해?`도 입력한다. 형식을 따르더라도 내용이 틀리거나 신화 형식을 억지로 적용할 수 있다. 이를 그대로 기록한다. `/bye`로 종료한 뒤 다시 실행해 저장·복원을 확인한다.

교재 검증 PC에서 `한 줄 요약:`은 학습 후 모든 비교 질문의 답에 나왔다. 이름에 따라 결과가 달라서 `퀴즈 힌트:`는 uv.lock 질문과 `올림포스에서 번개를 다루는 신을 소개해 줘.`의 답에서 빠졌다. 모델은 학습 데이터에 있는 `아테나를 소개해 줘.`에도 틀린 설명을 했고, 제우스의 사실 한 줄을 고친 실험에서도 고친 내용은 답에 나오지 않았다. 이번 실습의 관찰 대상은 답변 형식의 변화이며, 형식이 바뀌어도 사실의 정확성을 보장하지 않는다. 6주차 RAG로 자료를 넣을 때도 필요한 근거가 검색됐는지, 답변이 그 근거와 맞는지 확인해야 한다.

## 선택 시연: 병합 모델로 Python 대화

```powershell
uv sync
uv run ex05
uv run ex06
```

기존 프로젝트에 `ex06` 소스와 scripts 변경을 반영한 뒤에는 `uv sync`를 다시 실행한다. `ex05`가 어댑터를 기본 모델에 합쳐 `models/merged-run-001/`에 저장하면, `ex06`이 같은 폴더의 모델·토크나이저를 읽는다. 이 폴더는 전체 모델을 담으며 어댑터만 있는 `adapters/run-001/`과 다르다. Ollama 서버나 GGUF 변환 없이 Python에서 실행한다.

`아테나를 소개해 줘.`를 입력하고 답이 끝나면 `포세이돈은 어떤 신이야?`를 입력한다. 빈 줄은 건너뛰고 `/bye`로 종료한다. 각 질문은 독립적이며 앞 대화를 기억하지 않는다. `uv run ex06`을 다시 실행해도 저장한 병합 폴더를 읽으므로 다시 학습하거나 병합할 필요가 없다. 학습 전후 비교 기록은 `ex04`를 기준으로 남긴다. 이 시연은 필수 완료 조건이 아니다.

## 별도 선택: Ollama 연결

위에서 저장한 병합 모델을 Ollama로 가져오고 싶을 때 실행한다. 병합한 폴더를 이어 쓰므로 `ex05`를 다시 실행하지 않는다.

```powershell
# examples/ollama_import.md의 준비된 변환기로 GGUF 생성
ollama create week07-lora -f Modelfile
ollama run week07-lora
```

[변환 준비](examples/ollama_import.md)를 먼저 마치고 `models/week07-lora.gguf`를 만든다. 질문을 입력하고 답변을 확인한다. Ollama 대화를 끝낸 뒤 `src/ex01_ollama/__init__.py`의 `MODEL = "week07-lora"`로 고쳐 `uv run ex01`을 실행하면 처음과 같은 코드로 대화한다. `Modelfile`의 system 지시는 학습·비교와 같게 유지한다.

## 막혔을 때 확인할 부분

| 증상 | 확인과 다음 행동 |
|---|---|
| Ollama 연결 실패·모델 없음 | Ollama 실행 상태와 `ollama list`, `ex01`의 모델 이름 확인 |
| Transformers 모델을 찾지 못함 | 준비 때와 같은 사용자·캐시 환경에서 `uv run prepare` 실행 |
| NVIDIA GPU가 있는데 `장치: cpu` | CUDA 확인 명령의 버전·`True/False`, TOML의 `torch` 출처, `nvidia-smi`와 `shared`의 `DEVICE` 확인. TOML 변경 시 `uv lock` → `uv sync` |
| JSON 오류 | 수정한 줄의 따옴표·쉼표·줄바꿈 확인, 새 항목 이름에 `"`나 `\`가 들어갔는지 확인 |
| 답변이 길다는 오류 | 데이터의 질문·답변을 줄여 256토큰 이내로 유지 |
| 학습이 느림·메모리 부족 | 기준 PC 사용 또는 CPU 대체 3 step으로 경로 확인 |
| 어댑터가 이미 있음 | 기존 기록을 보존하고 `ADAPTER_DIR`을 새 이름으로 변경 |
| 어댑터가 없음 | `ex03` 저장 경로와 `ADAPTER_DIR` 일치 여부 확인 |
| `ex06` 명령을 찾지 못함 | 개인 프로젝트에 `ex06` 소스와 `[project.scripts]` 변경을 반영했는지 확인하고 프로젝트 루트에서 `uv sync` 재실행 |
| 병합 모델이 없음 | `uv run ex05`의 저장 완료 여부와 공용 `MERGED_DIR` 확인. `models/merged-run-001/`에 `config.json`·모델 가중치·토크나이저 파일이 함께 있어야 한다 |
| Qwen인데 Mistral의 `incorrect regex pattern` 경고가 나옴 | Transformers 4.57.6의 로컬 Qwen 판별 오탐. `shared.load_model()`의 `fix_mistral_regex=False` 설정을 반영하고 재실행한다. [원인과 적용 범위](examples/README.md#병합한-모델로-python에서-대화하기)를 확인하고 `True`를 무조건 적용하지 않는다 |
| 학습 후 새 항목 이름이 나오지 않음 | 24곳이 모두 바뀌었는지, `ex03` 첫 출력에 새 이름이 있었는지 확인. 첫 출력에 있었는데 일부 질문에서만 빠지면 데이터 오류가 아니므로 질문별 결과로 기록 |
| Ollama 가져오기 실패 | 병합 폴더·Modelfile 경로·지원 버전 확인, 필수 비교는 `ex04`로 완료 |

자세한 문제와 완료 조건은 [실습지](lab.md), 기록 항목은 [양식](examples/EXPERIMENT_TEMPLATE.md)을 따른다.
