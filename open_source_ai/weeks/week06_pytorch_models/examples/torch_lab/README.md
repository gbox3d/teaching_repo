# torch_lab — 6주차 예제 uv 프로젝트

pipeline 한 줄 안쪽을 세 스크립트로 나눈 최소 예제다. 텐서·자동미분 관찰(`tensor_basics.py`), 소형 MLP 학습 루프(`train_loop.py`), 사전학습 모델 직접 호출과 문장 임베딩(`pretrained_embed.py`), 그리고 셋이 함께 쓰는 실험 기록 헬퍼(`runlog.py`)로 구성된다. 설명과 관찰 지점, 대체 경로는 상위 [`../README.md`](../README.md)에 있다.

## 실행

```powershell
Copy-Item .env.example .env      # 값은 그대로 두어도 된다
uv sync                          # 의존성 설치(수업 전 한 번, torch 설치로 오래 걸린다)
uv run python tensor_basics.py
uv run python train_loop.py --epochs 400 --hidden 128 --tag overfit
uv run python pretrained_embed.py --show-tokens
uv run python runlog.py          # outputs/runs/ 기록 표
```

결과는 `outputs/tensor_report*.json`, `outputs/train-*.json`, `outputs/embed-*.json`, `outputs/runs/*.json`에 쌓인다(`.gitignore` 대상).

## 파일

| 파일 | 역할 |
|---|---|
| `runlog.py` | `set_seed`·`pick_device`·`sync` 헬퍼와 `RunLog` 실험 기록 클래스. 단독 실행 시 기록 표 |
| `tensor_basics.py` | Tensor 세 속성, 행렬곱 CPU/GPU 시간, dtype, 선형 모델, 자동미분, `no_grad` 메모리 |
| `train_loop.py` | 합성 2차원 분류 데이터로 MLP 학습, epoch별 train/val 기록, 과적합 요약 |
| `pretrained_embed.py` | `AutoTokenizer`/`AutoModel` → pooling → 코사인 유사도 행렬 → softmax, `RunLog` 기록 |
| `sentences.txt` | 입력 문장 파일 예시(한 줄에 한 문장, `#` 주석 무시) |
| `.env.example` | `HF_EMBED_MODEL`, `HF_HOME`, `HF_HUB_OFFLINE`, `HF_TOKEN` 예시 |

## 기본값

`HF_EMBED_MODEL`(`intfloat/multilingual-e5-small`)은 교재 검증용 기본값이다. 모델 ID·양자화·용량과 `pyproject.toml`의 CUDA 휠 태그는 학기별 환경 기준표에서 확정한다. `uv.lock`은 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다. 실습 중 모델을 내려받지 않는다.
