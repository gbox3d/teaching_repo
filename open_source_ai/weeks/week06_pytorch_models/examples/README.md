# 6주차 예제 — torch_lab: 텐서 관찰, 학습 루프, 임베딩, 실험 기록

## 파일 구성

| 파일 | 역할 | 쓰는 교시 |
|---|---|---|
| `torch_lab/` | uv 프로젝트. 아래 파일을 담는다 | 1·2·3교시 |
| `torch_lab/pyproject.toml` | 의존성 `torch`(CUDA 휠 인덱스 블록 포함), `transformers`, `numpy`, `python-dotenv`. 버전은 고정하지 않는다 | |
| `torch_lab/runlog.py` | 공통 헬퍼. `set_seed`·`pick_device`·`sync`와 실험 기록 클래스 `RunLog`. 단독 실행하면 `outputs/runs/` 기록을 표로 보여 준다 | 1·2·3교시 |
| `torch_lab/tensor_basics.py` | Tensor 세 속성, 행렬곱 CPU/GPU 시간과 복사 시간, dtype 변환, 선형 모델 forward, 자동미분, `no_grad` 메모리 차이 → `outputs/tensor_report.json` | 1교시 |
| `torch_lab/train_loop.py` | 스크립트 안에서 만든 2차원 분류 데이터(반달 2개)로 소형 MLP 학습. epoch별 train/val loss·accuracy와 요약 → `outputs/train-<시각>[-태그].json` | 2교시 |
| `torch_lab/pretrained_embed.py` | `AutoTokenizer`/`AutoModel`로 문장 → 토큰 ID → hidden state → pooling → 임베딩 → 코사인 유사도 행렬 → softmax. 결과 `outputs/embed-<시각>.json`, 실험 기록 `outputs/runs/<시각>-embed.json` | 3교시 |
| `torch_lab/sentences.txt` | 내장 5문장과 같은 내용의 입력 파일 예시. 복사해 자기 문장으로 바꾼다 | 3교시 |
| `torch_lab/.env.example` | `HF_EMBED_MODEL`, `HF_HOME`(주석), `HF_HUB_OFFLINE`(주석), `HF_TOKEN`(비워 둠) 예시. `.env`로 복사한다 | 3교시 |
| `torch_lab/.gitignore` | `.venv/`, `.env`, `outputs/`, `__pycache__/` 등 커밋 제외 | |
| `torch_lab/README.md` | 짧은 실행 안내 | |

1·2교시는 모델 파일이 필요 없다. 3교시만 사전 캐시된 임베딩 모델을 쓴다.

## 실행 방법

원본을 두고 개인 저장소 안의 실습 폴더에 복사한다. `$src`에는 교재 저장소의 이 `examples` 폴더 경로를 넣는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week06_pytorch_models\examples"
$dst = "$HOME\osa-practice\week06"
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item -Recurse "$src\torch_lab" "$dst\torch_lab"
Set-Location "$dst\torch_lab"
Copy-Item .env.example .env
uv sync                                       # 수업 전에 한 번. torch 설치로 오래 걸린다
uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

1교시(텐서·자동미분):

```powershell
uv run python tensor_basics.py
uv run python tensor_basics.py --size 256 --output outputs/tensor_report-256.json
uv run python tensor_basics.py --size 4096 --output outputs/tensor_report-4096.json
uv run python tensor_basics.py --batch 4096 --layers 8 --output outputs/tensor_report-nograd.json
uv run python tensor_basics.py --device cuda:9        # 실패 경로: 없는 장치
```

2교시(학습 루프):

```powershell
uv run python train_loop.py
uv run python train_loop.py --epochs 400 --hidden 128 --tag overfit
uv run python train_loop.py --epochs 400 --hidden 128 --tag overfit-seed7 --seed 7
uv run python train_loop.py --val-ratio 0              # 실패 경로: 검증 데이터 없음
```

3교시(임베딩·실험 기록):

```powershell
uv run python pretrained_embed.py --show-tokens
uv run python pretrained_embed.py --temperature 1.0
Copy-Item sentences.txt my_sentences.txt               # 내용을 자기 문장으로 바꾼다
uv run python pretrained_embed.py --sentences my_sentences.txt
uv run python pretrained_embed.py --sentences my_sentences.txt --pooling cls
uv run python pretrained_embed.py --model no-org/no-model   # 실패 경로: 없는 모델
uv run python runlog.py                                # 기록 표
```

모든 스크립트는 `--help`로 인자를 보여 주고, `--device auto|cpu|cuda`를 받는다. 결과는 `outputs/`에 쌓이며 `.gitignore` 대상이다.

## 관찰 지점

1. `tensor_basics.py` `[2]` 절: 작은 행렬(256)에서는 GPU가 CPU보다 느릴 수 있다. 커널 실행 준비 비용과 복사 비용이 계산보다 크기 때문이다. 2048 이상에서 배속이 커진다.
2. 같은 절의 `speedup`과 "복사 포함 speedup"이 다르다. `.to("cuda")`는 복사이고 시간이 든다. 데이터가 이미 GPU에 있을 때만 앞의 배속이 나온다.
3. `[3]` 절: float16과 bfloat16은 같은 2바이트지만 1/3의 표현이 다르다. bfloat16은 지수 범위가 넓고 소수 정밀도가 낮다.
4. `[5]` 절: `x.grad`가 `2x`다. `y = Σx²`이므로 `dy/dx = 2x`. `no_grad` 안에서 만든 텐서는 `grad_fn`이 `None`이다.
5. `[6]` 절: `no_grad=False`일 때 추가 메모리가 층 수 × 배치 × 은닉 × 4바이트 근처로 늘어난다. 역전파에 쓸 활성화를 저장하기 때문이다. `no_grad=True`면 입력·출력 버퍼 두 장 크기에서 멈추고 층 수를 늘려도 늘지 않는다.
6. `train_loop.py`: train loss는 거의 항상 내려가지만 val loss는 최저점 뒤 다시 오른다. `summary.overfit_suspected`는 "최저 대비 5% 이상 상승 + train loss 하락"이라는 단순 규칙이다. 규칙이 못 잡는 경우도 표에서 찾을 수 있다.
7. 같은 seed·같은 코드로 CPU에서 두 번 실행하면 `history`가 같다. GPU에서는 소수점 아래가 달라질 수 있다.
8. `pretrained_embed.py`: `last_hidden_state`는 `[문장 수, 토큰 수, 은닉 차원]`이고 문장 임베딩은 `[문장 수, 은닉 차원]`이다. pooling이 가운데 축을 없앤다. `attention_mask`를 곱하지 않으면 pad 토큰이 평균에 섞인다.
9. 유사도 행렬은 대각선 1, 대칭이다. 정규화한 벡터의 행렬곱 한 번이 모든 쌍의 코사인이다. `--temperature`는 순위를 바꾸지 않고 softmax 확률의 쏠림만 바꾼다.
10. `outputs/runs/*.json`에는 모델 ID·revision·seed·device·경과 시간·`max_memory_allocated_mb`가 있다. 실패한 실행은 기록을 남기지 않는다.

## GPU 없을 때·네트워크 없을 때

- GPU가 없거나 `torch.cuda.is_available()`가 `False`면 모든 스크립트가 자동으로 CPU에서 돈다(`--device auto`). `tensor_basics.py`의 GPU 시간·복사 시간·추가 메모리는 `null`로 기록되고 `grad_fn`·`requires_grad` 값으로 `no_grad` 차이를 설명한다. 행렬 크기는 `--size 1024 --repeat 1`까지만 쓴다.
- `train_loop.py`는 CPU에서도 400 epoch이 수십 초 안에 끝난다. 시간이 부족하면 `--epochs 200 --print-every 20`으로 줄인다.
- `pretrained_embed.py`는 CPU에서 문장 5개 기준 수 초면 끝난다. `--device cpu`를 명시해 기록의 `device`가 `cpu`로 남게 한다.
- 네트워크가 없어도 `uv sync`와 임베딩 모델 사전 캐시가 수업 전에 끝나 있으면 세 교시 모두 오프라인으로 진행된다. `.env`의 `HF_HUB_OFFLINE=1` 주석을 풀면 캐시 밖 접근을 시도하지 않는다. 실습 중 모델을 내려받지 않는다.
- 임베딩 모델이 캐시에 없는 PC는 `pretrained_embed.py`가 사람이 읽을 메시지로 종료한다. 이 경우 조교가 안내하는 공용 캐시 경로를 `HF_HOME`에 넣거나, 기준 PC 측정값으로 `experiment_note.md`의 표를 채우고 그 사실을 적는다. 1·2교시는 영향이 없다.

## 복사 후 변형

- `tensor_basics.py`의 `time_matmul`에 `dtype` 인자를 추가해 float16 행렬곱을 비교한다(1교시 확장). 함수 하나만 바꾸고 나머지 절은 그대로 둔다.
- `train_loop.py`에 `--patience` 옵션을 추가해 early stopping을 구현한다(2교시 확장). `history`와 `summary` 형식은 바꾸지 않아야 앞선 기록과 비교할 수 있다.
- `sentences.txt`는 `my_sentences.txt`로 복사한 뒤 바꾼다. 원본은 기본 5문장의 대조군으로 남긴다. 실명·학번·기관명을 넣지 않는다.
- `runlog.py`는 자기 프로젝트에 그대로 복사해 쓴다. `RunLog(name, config, device)` → 실험 → `finish(metrics)` 순서만 지키면 된다. 7주차 `ragcore.py`와 10주차 `common.py`는 파일 이름이 다를 뿐 같은 항목(모델·설정·시간·최대 메모리)을 남긴다.
- `outputs/`는 커밋하지 않는다. 증거로 낼 JSON 3~4개는 개인 저장소의 `evidence/week06/`에 복사한다.

## 기본값과 환경 기준표

| 환경변수 | 기본값 | 용도 |
|---|---|---|
| `HF_EMBED_MODEL` | `intfloat/multilingual-e5-small` | 3교시 임베딩 모델(`AutoModel`). 7주차 `mini_rag`와 같은 값 |
| `HF_HOME` | (주석 상태) | Hugging Face 캐시 위치. 공용 캐시를 쓸 때만 주석을 풀고 경로를 적는다. 값 없이 `HF_HOME=`으로 켜 두면 캐시가 현재 폴더의 `hub/`로 잡혀 사전 캐시를 못 찾는다 |
| `HF_HUB_OFFLINE` | (설정 시 `1`) | 캐시만 사용. 네트워크 없는 실습실에서 켠다 |
| `HF_TOKEN` | (비워 둠) | 이 주차 모델은 토큰이 필요 없다. 값은 `.env`에만 둔다 |

모델 ID·양자화·용량은 [학기별 환경 기준표](../../../../environment_baseline_template.md)에서 확정하며 위 값은 교재 검증용 기본값이다(과목 공통 표는 [`weeks/README.md`](../../README.md#교재-검증용-기본값)). `pyproject.toml`의 CUDA 휠 인덱스 태그도 같은 표에서 확정한다. `uv.lock`은 만들지 않았다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
