# 6주차 — PyTorch 모델 활용

## 이번 주 질문

> pipeline 한 줄 뒤에서 텐서가 GPU로 옮겨져 어떻게 계산되며, 학습 루프는 무엇을 반복하는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. Tensor의 shape·dtype·device를 읽고, CPU와 GPU 사이에서 옮긴 뒤 동기화해 계산 시간을 측정한다.
2. `requires_grad`·`backward`·`torch.no_grad`의 역할을 grad 값과 메모리 차이로 설명한다.
3. Dataset·DataLoader·손실 함수·옵티마이저로 학습 루프를 구성하고 epoch별 train/val loss를 기록한다.
4. 학습 곡선에서 과적합 신호를 찾아 시점을 근거 수치와 함께 말한다.
5. `AutoTokenizer`·`AutoModel`로 토큰 ID → hidden state → pooling → 문장 임베딩을 직접 계산하고 코사인 유사도 행렬을 만든다.
6. 모델 ID·revision·seed·device·실행 시간·최대 GPU 메모리를 실험 로그 JSON으로 남긴다.

## 누적 결과물

이번 주 임베딩 스크립트와 실험 기록 습관은 7주차 RAG 답변기, 곧 2차 종합과제(8주차)의 검색 부분을 채운다. 학습 루프와 seed·학습 곡선 기록은 10주차 LoRA 실험 기록, 곧 3차 종합과제(12주차)의 바탕이 된다. 세 실습의 `outputs/` 기록과 비교 문장을 개인 저장소에 누적한다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 텐서 이동과 자동미분 관찰: Tensor 세 속성, CPU↔GPU 이동과 동기화, dtype과 메모리, `requires_grad`·`backward`·`no_grad`, 모델 = 파라미터 + `forward`, TensorFlow 개념 대응 | `tensor_basics.py`로 행렬곱 CPU/GPU 시간, dtype 변환, 선형 모델 forward, `no_grad` 메모리 차이를 관찰하고 행렬 크기를 바꿔 비교한다 | `outputs/tensor_report.json`, 크기별 시간·메모리 비교표 |
| 2교시 | 소형 MLP 학습 루프와 과적합: Dataset/DataLoader, 손실 함수·옵티마이저, epoch·batch, train/val 분리, 과적합 신호, seed 고정, 학습 곡선 기록 | `train_loop.py`로 합성 2차원 분류 데이터를 학습하고, epoch을 늘려 val loss가 다시 오르는 시점을 찾는다 | `outputs/train-*.json`, 과적합 시점 문장 |
| 3교시 | 문장 임베딩과 실험 기록: `AutoTokenizer`/`AutoModel`, 토큰 ID → hidden state → pooling → 임베딩, logits → softmax, 실험 기록 습관 | `pretrained_embed.py`로 문장 5개의 유사도 행렬을 만들고 `runlog.py`로 남은 실험 기록을 확인한다 | 유사도 행렬, `outputs/runs/*.json` |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Git, VS Code, uv, PowerShell. NVIDIA GPU가 있으면 `nvidia-smi`가 동작해야 한다(없어도 CPU 경로로 진행한다).
- 3교시 임베딩 모델(`HF_EMBED_MODEL`, 교재 검증용 기본값 `intfloat/multilingual-e5-small`)이 수업 전에 Hugging Face 캐시에 들어 있어야 한다. 실습 시간에 내려받지 않는다.
- `examples/torch_lab`을 개인 저장소에 복사한 폴더에서 `uv sync`를 수업 전에 마쳐 둔다(첫 sync는 torch 설치로 오래 걸린다). 1·2교시는 모델 파일이 필요 없다.
- 5주차 산출물: `model_cards.md`·`SOURCES.md`의 임베딩 모델 행(모델 ID·commit hash·라이선스), `pipeline_report.md`의 CPU/GPU 시간 비교표.
- 정확한 도구 버전과 CUDA 태그는 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 실제 이름, 학번, 토큰, 비밀번호를 실습 파일과 공개 저장소에 넣지 않는다. `.env`는 커밋하지 않고 `.env.example`만 둔다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): `torch_lab/` uv 프로젝트 — 텐서 관찰, 학습 루프, 임베딩, 실험 기록 헬퍼
- 강의 대본: 강의자 별도 관리(비공개)

## 권장 진행 방식

1. 스크립트를 실행하기 전에 시간·메모리·유사도 순위를 먼저 예상해 적는다.
2. 실행 결과 JSON을 열어 예상과 다른 값을 찾고, 왜 다른지 한 문장으로 쓴다.
3. 옵션(`--size`, `--epochs`, `--pooling`)을 하나씩만 바꿔 다시 실행하고 변화를 비교한다.
4. GPU가 없거나 인식되지 않으면 `--device cpu`로 같은 절차를 진행하고 device 값을 기록에 남긴다.
5. 기본 문제를 마친 뒤에만 확장 문제를 한다. 실험 기록이 없는 실행은 하지 않은 것과 같다.

## 완료 기준

- [ ] `uv sync` 후 `torch.__version__`과 `torch.cuda.is_available()`을 확인했다.
- [ ] `tensor_basics.py`를 세 가지 행렬 크기로 실행해 CPU/GPU 시간과 복사 시간을 표로 만들었다.
- [ ] `no_grad` 유무의 차이를 `grad_fn` 또는 메모리 수치로 설명했다.
- [ ] `train_loop.py`를 기본 설정과 긴 epoch 설정으로 실행해 val loss 최저 epoch을 찾았다.
- [ ] 과적합이 시작된 시점을 근거 수치와 함께 한 문장으로 썼다.
- [ ] `pretrained_embed.py`로 문장 5개의 유사도 행렬을 만들고 예상 순위와 비교했다.
- [ ] `outputs/runs/`에 실험 기록이 2건 이상 있고 `runlog.py` 표에서 확인했다.
- [ ] 기록에 토큰·개인정보가 없다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 개인 저장소에 누적한다. `outputs/`는 `.gitignore`에 들어 있으므로 남길 JSON은 `evidence/week06/`로 복사해 커밋한다.

1. `tensor_compare.md`: 크기별 CPU/GPU 시간·복사 시간 비교표와 교차점 문장
2. `overfit_note.md`: 기준·긴 epoch·seed 변경 실행의 val loss 최저 epoch 표와 과적합 시점 문장
3. `experiment_note.md`: 임베딩 실행 3건의 모델·pooling·최고 유사 쌍·경과 시간·최대 메모리 표
4. `evidence/week06/`: `tensor_report.json`, `train-*.json` 1건, `runs/*.json` 1건

## 다음 주 연결

`week07_embeddings_rag`에서는 오늘 만든 임베딩과 유사도 행렬을 수업용 한국어 문서 여러 개로 확장해 chunk 분할, top-k 검색, 출처 있는 RAG 답변기를 만든다. `runlog.py`의 기록 습관은 그대로 이어지며, `HF_EMBED_MODEL` 환경변수도 같은 값을 쓴다.

## 참고 자료

- [PyTorch 튜토리얼 — Tensors](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)
- [PyTorch 튜토리얼 — Automatic Differentiation](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
- [PyTorch 튜토리얼 — Datasets & DataLoaders](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html)
- [PyTorch 튜토리얼 — Optimizing Model Parameters](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
- [PyTorch 문서 — CUDA semantics](https://docs.pytorch.org/docs/stable/notes/cuda.html)
- [Transformers 문서 — Auto Classes](https://huggingface.co/docs/transformers/model_doc/auto)
