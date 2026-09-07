---
marp: true
theme: default
paginate: true
header: "오픈소스 AI 응용 · 6주차"
footer: "PyTorch 모델 활용"
---

# 6주차
## PyTorch 모델 활용

**60분 블록 × 3**<br>
매 블록 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분

---

## 이번 주 세 블록

| 교시 | 설명·시연 20분 | 직접 해결 실습 30분 |
|---|---|---|
| 1교시 | 텐서 이동과 자동미분 관찰 | `tensor_basics.py` 시간·메모리 비교 |
| 2교시 | 소형 MLP 학습 루프와 과적합 | `train_loop.py` 학습 곡선과 과적합 시점 |
| 3교시 | 문장 임베딩과 실험 기록 | `pretrained_embed.py` 유사도 행렬과 실험 로그 |

지난주 `pipeline` 한 줄을 이번 주에 **열어서** 본다.

---

## 이번 주 질문

> pipeline 한 줄 뒤에서 텐서가 GPU로 옮겨져 어떻게 계산되며, 학습 루프는 무엇을 반복하는가?

- 5주차: `pipeline(...)`의 결과만 보았다
- 6주차: 텐서 → 모델 → loss → backward 를 손으로 만진다
- 7주차: 오늘의 임베딩으로 문서 검색과 RAG를 만든다

**질문:** 지난주 pipeline을 실행했을 때 GPU 메모리는 어느 순간에 늘어났는가?

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 텐서 이동과 자동미분 관찰

---

## 0–3분 · pipeline 한 줄을 열면

```text
"문장" ─tokenizer─▶ input_ids [1, T] ─model─▶ logits [1, C] ─softmax─▶ label
문자열              정수 텐서              실수 텐서              확률
```

- 모든 단계의 입력과 출력은 **Tensor**다
- 텐서는 CPU 메모리 또는 GPU 메모리 한 곳에 있다
- 모델도 텐서(파라미터)의 묶음이다

이어받는 것: 5주차 `pipeline_demo.py`의 CPU/GPU 시간 비교표.

---

## 3–6분 · Tensor 세 속성

```python
import torch
x = torch.tensor([[1.0, 2.0, 3.0]])
x.shape    # torch.Size([1, 3])  — 몇 개가 어떤 모양으로
x.dtype    # torch.float32       — 원소 하나가 몇 바이트
x.device   # device(type='cpu')  — 어느 메모리에
```

- 오류 메시지 대부분은 이 셋 중 하나가 어긋난 것이다
- `shape` 불일치 → 행렬곱 실패, `dtype` 불일치 → 연산 거부, `device` 불일치 → same device 오류

**핵심: 텐서를 보면 세 속성부터 읽는다.**

---

## 6–9분 · CPU↔GPU 이동과 시간 측정

```python
a = torch.randn(2048, 2048)     # CPU
a_gpu = a.to("cuda")            # 복사 — 원본은 그대로 CPU에
c = a_gpu @ a_gpu               # GPU 커널 실행(비동기)
torch.cuda.synchronize()        # 끝날 때까지 기다린 뒤 시간을 잰다
```

- `.to()`는 이동이 아니라 **복사**다. 시간이 들고 두 곳에 존재한다
- GPU 연산은 비동기다. `synchronize()` 없이 잰 시간은 거짓이다
- 작은 행렬은 복사·커널 준비 비용 때문에 CPU가 빠를 수 있다

**질문:** 256×256 행렬곱은 GPU가 몇 배 빠를까, 아니면 오히려 느릴까?

---

## 9–12분 · dtype과 메모리

| dtype | 바이트 | 1/3의 표현 | 쓰임 |
|---|---:|---|---|
| float32 | 4 | 0.33333334 | 기본 학습·계산 |
| float16 | 2 | 0.33325195 | 추론, 메모리 절반 |
| bfloat16 | 2 | 0.33398438 | 학습용 절반 정밀도 |
| int64 | 8 | (정수) | 토큰 ID, 라벨 |

- VRAM = 파라미터 수 × 바이트 + 활성화 + grad + 옵티마이저 상태
- 0.5B 모델: float32 2 GB, float16 1 GB — 1주차 계산이 여기서 다시 나온다
- 변환은 `x.to(torch.float16)`. 소수 → 정수는 반올림이 아니라 **버림**이다

---

## 12–15분 · 자동미분과 `no_grad`

```python
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = (x ** 2).sum()      # 계산 그래프가 기록된다
y.backward()            # dy/dx 를 x.grad 에 채운다
x.grad                  # tensor([2., 4., 6.])

with torch.no_grad():   # 추론: 그래프를 만들지 않는다
    z = (x ** 2).sum()  # z.grad_fn is None
```

- `requires_grad=True`인 텐서가 낀 연산은 **역전파용 중간값을 저장**한다
- 추론만 할 때 `no_grad`를 빼먹으면 메모리가 배로 든다

**질문:** `x.grad`가 `2x`인 이유를 한 줄로 쓰면?

---

## 15–17분 · 모델 = 파라미터 + `forward`

```python
model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 2))
sum(p.numel() for p in model.parameters())   # 4*8+8 + 8*2+2 = 58
out = model(torch.randn(3, 4))               # forward → [3, 2]
```

| PyTorch | TensorFlow(비교만) |
|---|---|
| `torch.Tensor` | `tf.Tensor` |
| `nn.Parameter` | `tf.Variable` |
| `backward()` | `tf.GradientTape` |
| `nn.Module` | `keras.Model` |

`nn.Module`은 파라미터를 들고 있고 `forward`가 계산 순서다. `.to(device)`는 파라미터 전부를 옮긴다.

---

## 17–20분 · 실습 인계

[1교시 실습 — 텐서 이동과 자동미분 관찰](lab.md#1교시-실습--텐서-이동과-자동미분-관찰)

완료 조건:

1. `outputs/tensor_report.json`이 생겼고 행렬곱 CPU/GPU 시간(GPU가 없으면 CPU만)을 읽었다
2. `--size`를 세 값으로 바꾼 비교표를 만들었다
3. `no_grad` 유무의 차이를 메모리 수치 또는 `grad_fn`으로 한 문장 설명했다

실행 전에 예상부터 적는다. **실습 30분 뒤 휴식 10분.**

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## 소형 MLP 학습 루프와 과적합

---

## 0–3분 · 학습 루프는 다섯 줄의 반복이다

```text
for epoch in range(E):
    for x, y in loader:             # 1 배치 하나를 꺼낸다
        logits = model(x)           # 2 forward
        loss = criterion(logits, y) # 3 얼마나 틀렸나
        loss.backward()             # 4 어느 방향으로 고칠까 (grad)
        optimizer.step()            # 5 조금 고친다
```

- 1교시의 `backward()`가 4번이고, `no_grad`는 검증 단계에서 쓴다
- 남은 질문: 무엇을 꺼내고, 무엇으로 틀림을 재고, 언제 멈추는가

이어받는 것: 1교시 `tensor_report.json`의 device 값.

---

## 3–6분 · Dataset과 DataLoader

```python
class MoonDataset(Dataset):
    def __len__(self):         return len(self.y)
    def __getitem__(self, i):  return self.x[i], self.y[i]

loader = DataLoader(ds, batch_size=32, shuffle=True)
```

- Dataset은 **길이**와 **i번째 항목** 두 질문에만 답한다
- DataLoader가 섞고, 묶고(batch), 필요하면 병렬로 읽는다
- 이번 주 데이터는 스크립트가 만든 2차원 점 300개 — 다운로드 없음

**질문:** `shuffle=True`를 검증 데이터에도 켜야 하는가?

---

## 6–9분 · 손실 함수와 옵티마이저

```python
criterion = nn.CrossEntropyLoss()                 # logits + 정수 라벨
optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
optimizer.zero_grad()   # 지난 배치의 grad를 비운다 — 안 비우면 누적된다
```

- `CrossEntropyLoss`는 **softmax를 안에 포함**한다 → 모델 출력은 logits 그대로
- 옵티마이저는 `grad`를 보고 파라미터를 `lr` 만큼 움직인다
- `lr`이 크면 발산하고 작으면 느리다 — 곡선으로 판단한다

**핵심: `zero_grad → backward → step` 순서를 바꾸지 않는다.**

---

## 9–12분 · epoch · batch · train/val 분리

```text
300개 ─┬─ train 210개  → 학습에 사용, loss·acc 기록
       └─ val    90개  → 학습에 절대 쓰지 않음, loss·acc만 기록
```

- 1 epoch = 학습 데이터 한 바퀴. 배치 32면 7 step
- val 점수는 "본 적 없는 데이터에서 얼마나 맞히는가"의 유일한 근거
- val을 학습에 섞으면(누수) 점수는 오르고 의미는 사라진다

**질문:** val loss가 낮은 모델과 train loss가 낮은 모델 중 무엇을 고르는가?

---

## 12–15분 · 과적합 신호 (예시 수치)

| epoch | train loss | val loss | 읽기 |
|---:|---:|---:|---|
| 10 | 0.45 | 0.48 | 둘 다 내려간다 — 학습 중 |
| 40 | 0.31 | 0.47 | val 최저 근처 |
| 200 | 0.18 | 0.90 | train만 내려간다 — **과적합** |
| 400 | 0.10 | 1.80 | 잡음 라벨까지 외웠다 |

- 신호: val loss가 최저점을 찍고 **다시 오른다**. train과 val 차이가 벌어진다
- 처방: 최저 시점에서 멈춤(early stopping), 데이터 추가, 모델 축소, 규제
- 실습에서는 epoch을 늘려 이 표를 직접 만든다

---

## 15–17분 · seed 고정과 곡선 기록

```python
torch.manual_seed(42)          # 초기 가중치·shuffle 순서 고정
history.append({"epoch": e, "train_loss": tl, "val_loss": vl})
json.dump({"config": vars(args), "history": history}, f)
```

- 같은 seed·같은 코드 → 같은 곡선(CPU). GPU는 미세하게 다를 수 있다
- 기록 없는 실험은 재현도 비교도 못 한다 — 설정과 곡선을 **한 파일에**
- 파일 이름에 시각과 태그(`train-…-overfit.json`)를 넣어 덮어쓰지 않는다

---

## 17–20분 · 실습 인계

[2교시 실습 — 소형 MLP 학습 루프와 과적합](lab.md#2교시-실습--소형-mlp-학습-루프와-과적합)

완료 조건:

1. 기본 설정과 긴 epoch 설정의 `outputs/train-*.json`이 각각 있다
2. val loss 최저 epoch과 마지막 epoch의 값을 표로 적었다
3. "과적합이 시작된 시점"을 근거 수치와 함께 한 문장으로 썼다

**실습 30분 뒤 휴식 10분.**

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 문장 임베딩과 실험 기록

---

## 0–3분 · pipeline 없이 세 줄

```python
from transformers import AutoTokenizer, AutoModel
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id).to(device).eval()
out = model(**tok(sentences, padding=True, return_tensors="pt").to(device))
```

- `AutoModel`은 분류 헤드 없는 **몸통**만 준다 → `last_hidden_state`
- `eval()`은 dropout을 끄고, `no_grad`는 그래프를 끈다 — 둘 다 필요하다
- 모델 ID는 `HF_EMBED_MODEL` 환경변수로 읽는다(값은 환경 기준표)

이어받는 것: 5주차 `model_cards.md`의 임베딩 모델 라이선스 행.

---

## 3–6분 · 토큰 ID → hidden state

```text
input_ids          [5, 18]        문장 5개 × 최대 토큰 18개 (짧은 문장은 pad)
attention_mask     [5, 18]        1 = 실제 토큰, 0 = pad
last_hidden_state  [5, 18, 384]   토큰마다 384차원 벡터
```

- 문장마다 길이가 다르므로 **padding**으로 맞추고 mask로 구분한다
- hidden state는 "토큰의 벡터"다. 아직 문장 하나의 벡터가 아니다

**질문:** pad 토큰의 벡터를 평균에 넣으면 무엇이 달라지는가?

---

## 6–9분 · pooling → 문장 임베딩 → 코사인 유사도

```python
m = mask.unsqueeze(-1).float()
emb = (hidden * m).sum(1) / m.sum(1)   # mean pooling — pad 제외
emb = F.normalize(emb, dim=1)          # 길이 1로
sim = emb @ emb.T                      # 코사인 유사도 행렬 [5, 5]
```

- mean pooling: 실제 토큰 벡터의 평균. cls pooling: 첫 토큰만
- 정규화한 벡터의 내적 = 코사인 → 행렬곱 한 번이 **모든 쌍**의 유사도
- e5 계열은 문장 앞에 `query: ` 접두어를 붙이라고 모델 카드가 권한다

---

## 9–12분 · logits → softmax

```python
scores = sim[0, 1:]                          # s1이 본 나머지 4문장 점수
probs = torch.softmax(scores / 0.05, dim=0)  # 합이 1인 확률
```

- 분류 모델의 마지막도 같다: `logits [1, C]` → softmax → 확률 → argmax
- 온도(나누는 값)가 작을수록 1등에 확률이 쏠린다 — 순위는 그대로
- 5주차 pipeline이 보여 준 `score`가 바로 이 확률이다

**질문:** softmax 확률 0.9는 "90% 맞다"는 뜻인가?

---

## 12–15분 · 실험 기록의 습관

| 항목 | 예 | 없으면 |
|---|---|---|
| 모델 ID·revision | `intfloat/multilingual-e5-small`, commit hash | 어느 가중치였는지 모른다 |
| seed·device·dtype | 42, cuda, float32 | 재현 불가 |
| 입력 버전 | `sentences.txt` 5문장 | 결과 비교 불가 |
| 시간·최대 메모리 | 1.2 s, 310 MB | 다음 실험 크기를 못 정한다 |
| 결과 파일 경로 | `outputs/embed-….json` | 표를 다시 만들어야 한다 |

- `torch.cuda.max_memory_allocated()`로 최대 메모리를 기록한다.
- 10주차 LoRA 실험 기록 양식이 이 표에서 자란다

---

## 15–17분 · `runlog.py` — 기록을 코드로

```python
from runlog import RunLog, pick_device, set_seed
set_seed(42); device = pick_device("auto")
run = RunLog("embed", config={"model": model_id, "seed": 42}, device=device)
...                                  # 실험
run.finish({"infer_ms": 12.3})       # outputs/runs/시각-embed.json
```

- 생성 시 시작 시각과 GPU 최대 메모리 카운터를 초기화하고, `finish`가 파일을 쓴다
- `uv run python runlog.py`로 지금까지의 기록을 표로 본다
- 7주차 `ragcore.py`, 10주차 `common.py`도 같은 항목을 남긴다 — 내 프로젝트엔 이 파일을 복사한다

**핵심: 결과보다 먼저 기록 코드를 넣는다.**

---

## 17–20분 · 실습 인계

[3교시 실습 — 문장 임베딩과 실험 기록](lab.md#3교시-실습--문장-임베딩과-실험-기록)

완료 조건:

1. 5문장 유사도 행렬을 출력했고 가장 비슷한 쌍이 예상과 맞는지 적었다
2. 자기 문장 5개와 pooling(또는 접두어) 변경으로 두 번 더 실행했다
3. `outputs/runs/`에 기록 3건 이상이 있고 `runlog.py` 표에서 확인했다

**실습 30분 뒤 휴식 10분.** 휴식 후에는 다음 주로 이어진다.

---

## 이번 주 정리

```text
텐서:   shape·dtype·device → .to(device) → synchronize 후 측정
학습:   zero_grad → forward → loss → backward → step, val은 보기만 한다
임베딩: 토큰 ID → hidden [B,T,H] → pooling → normalize → 행렬곱 = 유사도
기록:   모델·revision·seed·device·시간·최대 메모리를 JSON 한 파일로
```

다음 주(`week07_embeddings_rag`)는 오늘의 유사도 행렬을 **문서 검색**으로 키운다.
