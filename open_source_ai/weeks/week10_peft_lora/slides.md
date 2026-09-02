---
marp: true
theme: default
paginate: true
header: "오픈소스 AI 응용 · 10주차"
footer: "PEFT/LoRA 경량 파인튜닝"
---

# 10주차
## PEFT/LoRA 경량 파인튜닝

**60분 블록 × 3**<br>
매 블록 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분

---

## 이번 주 세 블록

| 교시 | 설명·시연 20분 | 직접 해결 실습 30분 |
|---|---|---|
| 1교시 | 전체를 다시 배우지 않고 일부만 바꾸기 | 어댑터 붙이고 학습 파라미터 세기 |
| 2교시 | 데이터가 모델에 들어가는 길: 템플릿·마스킹·Trainer | 수업 도우미 말투로 LoRA 학습하기 |
| 3교시 | 어댑터를 저장·비교·기록하기 | 전후 비교와 실험 기록 run-001 |

이번 주 질문: **무엇을 고정하고 무엇을 기록해야 몇 분짜리 학습이 재현되는가?**

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 전체를 다시 배우지 않고 일부만 바꾸기

---

## 0–3분 · 세 가지 적응 방법

```text
프롬프트     : 가중치 그대로, 지시문만 바꾼다        (4주차 Modelfile)
전체 파인튜닝: 모든 가중치를 다시 학습한다             (수십 GB VRAM)
PEFT         : 가중치는 얼리고 작은 부품만 학습한다    (이번 주)
```

- 사전학습 모델의 지식을 **재사용**하는 것이 전이학습
- 문제는 "무엇을 바꿀 것인가"가 아니라 **"무엇을 얼릴 것인가"**

**질문:** 4주차의 system 프롬프트로 안 되던 일은 무엇이었는가?

---

## 3–6분 · 전체 파인튜닝 vs PEFT

| 항목 | 전체 파인튜닝 | PEFT(LoRA) |
|---|---|---|
| 학습 파라미터 | 100% | 0.1~2% |
| 옵티마이저 상태 | 파라미터 수 × 8바이트 | 학습 파라미터만 |
| 저장 산출물 | 모델 전체 복사본 | 어댑터 수십 MB |
| 원본 되돌리기 | 별도 보관 필요 | 어댑터만 떼면 된다 |

**같은 기본 모델 위에 어댑터를 여러 개** 바꿔 끼울 수 있다.

---

## 6–10분 · LoRA 직관: ΔW = BA

```text
원래 계층:   y = W x                 W: (out × in), 얼림
LoRA 계층:   y = W x + (alpha / r) · B A x
             A: (r × in)  B: (out × r)   r ≪ in, out
```

- `r`(rank): 안쪽 차원. 커지면 표현력과 파라미터가 함께 는다
- `alpha`: 어댑터 출력 배율. 관례는 `alpha = 2r`
- `target_modules`: 붙일 선형 계층 이름 — 보통 `q_proj, k_proj, v_proj, o_proj`

학습이 끝나면 `W + (alpha/r)·BA`로 **병합**해 원래 모양으로 돌아간다.

---

## 10–13분 · 학습 메모리 네 덩어리

```text
가중치        파라미터 수 × 2바이트(bf16)
그래디언트    학습 파라미터 × 4바이트
옵티마이저    학습 파라미터 × 8바이트(Adam 1차·2차)
활성화        배치 × 시퀀스 길이 × hidden × 층 수 × (상수)
```

- 전체 파인튜닝은 위 세 줄이 **모든** 파라미터에 걸린다
- LoRA는 두·세 번째 줄이 1% 안팎으로 줄고, **활성화는 그대로**

**질문:** 0.5B 모델을 전체 파인튜닝하면 옵티마이저 상태만 몇 GB인가?

---

## 13–16분 · 12 GB에 무엇이 들어가는가

| 모델 크기 | 방식 | 대략의 VRAM | 12 GB 판정 |
|---|---|---|---|
| 0.5B | LoRA · bf16 · seq 512 | 3~5 GB | 여유 |
| 1.5B | LoRA · bf16 · seq 512 | 6~10 GB | 배치 줄이면 가능 |
| 7B | LoRA · bf16 | 16 GB 이상 | 불가 |
| 7B | 4비트 양자화 + LoRA(QLoRA) | 6~10 GB | 가능(이 수업 범위 밖) |

값은 **예측표를 만들고 실측으로 고치는** 것이 이번 주 태도다.

---

## 16–18분 · 프롬프트로 될 일, LoRA가 필요한 일

- 프롬프트로 충분: 역할 지시, 출력 언어, 한두 가지 형식 규칙
- LoRA가 필요: 매번 지키지 못하는 **일관된 형식·말투**, 도메인 용어, 긴 지시문을 짧게 줄이기
- LoRA로도 안 됨: 모델이 모르는 사실 추가(→ 7주차 RAG)

시연: `uv run python lora_setup.py --ranks 4,8,16`

```text
trainable params: 1,081,344 || all params: 495,114,112 || trainable%: 0.2184
```

---

## 18–20분 · 실습 인계

[1교시 실습 — 어댑터 붙이고 학습 파라미터 세기](lab.md#1교시-실습--어댑터-붙이고-학습-파라미터-세기)

완료 조건:

1. r=4·8·16의 학습 파라미터 수와 비율(%) 표
2. 가중치·학습 상태·활성화·합계로 나눈 VRAM 예측표
3. `target_modules`를 줄였을 때 비율이 어떻게 변하는지 한 문장

실습 30분 뒤 휴식 10분, 휴식 후 2교시.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## 데이터가 모델에 들어가는 길: 템플릿·마스킹·Trainer

---

## 0–3분 · SFT 데이터: 질문과 답 한 쌍

```json
{"instruction": "uv.lock 파일을 왜 커밋해야 하나요?",
 "output": "핵심: …\n이유: …\n다음 할 일: …"}
```

- `data/sample_sft.jsonl`: 수업 내용에 대한 한국어 Q&A 50여 건, 자체 작성
- 모든 답이 **핵심 · 이유 · 다음 할 일** 세 줄 형식 — 바꾸려는 "말투"
- 실제 인물·기관 정보 없음. 팀 데이터도 같은 원칙

**질문:** 50건으로 무엇까지 배우고 무엇은 못 배우는가?

---

## 3–7분 · chat template: 문자열이 입력이 되는 길

```text
<|im_start|>system
당신은 오픈소스 AI 응용 수업의 도우미입니다. …<|im_end|>
<|im_start|>user
uv.lock 파일을 왜 커밋해야 하나요?<|im_end|>
<|im_start|>assistant
핵심: uv.lock은 …<|im_end|>
```

- `tokenizer.apply_chat_template(messages)`가 모델별 특수 토큰을 붙인다
- 학습 때 쓴 템플릿과 **추론 때 템플릿이 같아야** 한다
- system 프롬프트도 학습·비교에서 **같은 문장**으로 고정한다

---

## 7–10분 · 라벨 마스킹: 답만 배운다

```text
토큰:   [system…] [user…] [assistant\n] [핵심: …] [<|im_end|>]
라벨:    -100 …    -100 …   -100          그대로     그대로
```

- 손실은 라벨이 `-100`이 아닌 위치에서만 계산된다
- 프롬프트까지 학습하면 모델이 **질문을 흉내 내는 데** 용량을 쓴다
- 시연: `uv run python train_lora.py --inspect`

**질문:** 라벨이 전부 `-100`이면 loss는 어떻게 되는가?

---

## 10–14분 · Trainer 구조

```text
TrainingArguments  ─ lr, epoch, batch, accumulation, seed, bf16, 로그 주기
Dataset            ─ input_ids · attention_mask · labels
DataCollator       ─ 배치마다 길이를 맞춰 패딩(labels는 -100)
Trainer.train()    ─ forward → loss → backward → optimizer.step() 반복
```

```python
trainer = Trainer(model=model, args=training_args,
                  train_dataset=dataset, data_collator=collator)
trainer.train()
trainer.state.log_history   # step별 loss
```

6주차에 직접 쓴 학습 루프를 **설정으로** 바꾼 것이다.

---

## 14–17분 · 하이퍼파라미터 다섯 개

| 이름 | 기본값 | 바꾸면 |
|---|---|---|
| `--lr` | 2e-4 | 크면 loss가 튀고, 작으면 변화 없음 |
| `--epochs` | 2 | 많으면 외운다(11주차 평가에서 드러남) |
| `--batch-size` | 4 | VRAM에 비례 |
| `--grad-accum` | 2 | 유효 배치 = batch × accum |
| `--rank` | 8 | 1교시 표 참고 |

**한 번에 하나만** 바꾸고 run 이름을 새로 붙인다.

---

## 17–18분 · seed와 재현

```powershell
uv run python train_lora.py --seed 42 --run-name run-001
```

- `set_seed(42)`: 초기화·셔플·드롭아웃의 난수를 고정
- 같은 seed·데이터·설정이면 loss 곡선이 **거의 같다**(GPU 커널 차이는 남는다)
- `adapters/run-001/run_config.json`에 설정 전체가 자동 저장된다

---

## 18–20분 · 실습 인계

[2교시 실습 — 수업 도우미 말투로 LoRA 학습하기](lab.md#2교시-실습--수업-도우미-말투로-lora-학습하기)

완료 조건:

1. `--inspect` 출력에서 가려진 토큰 수와 학습 대상 토큰 수를 기록
2. `adapters/run-001/`에 어댑터·`run_config.json`이 생성
3. `outputs/train-run-001.json`의 첫 loss와 마지막 loss, 최대 VRAM 실측을 기록

실습 30분 뒤 휴식 10분, 휴식 후 3교시.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 어댑터를 저장·비교·기록하기

---

## 0–3분 · 어댑터 폴더 안에는 무엇이 있는가

```text
adapters/run-001/
├─ adapter_config.json          r, alpha, target_modules, 기본 모델 이름
├─ adapter_model.safetensors    B·A 행렬만 (수 MB)
├─ tokenizer*.json, …           비교·서비스 때 같은 토크나이저
└─ run_config.json              이 예제가 남기는 학습 설정·loss 이력
```

- 기본 모델 가중치는 **없다** — 같은 기본 모델이 있어야 다시 붙는다
- 저장소에는 어댑터가 아니라 **기록**을 커밋한다(`adapters/`는 `.gitignore`)

---

## 3–7분 · 로드·끄기·병합 세 경로

```python
model = PeftModel.from_pretrained(base, "adapters/run-001")
with model.disable_adapter():     # 같은 객체로 기본 모델 출력
    base_text = generate(...)
lora_text = generate(...)         # 어댑터 켠 출력
merged = model.merge_and_unload() # W + (alpha/r)·BA → 단독 모델
```

- 비교에는 `disable_adapter()` — 모델을 두 번 올리지 않는다
- 서비스·변환에는 `merge_and_unload()` 후 `save_pretrained()`

**질문:** 병합본과 어댑터 방식 중 저장 용량이 큰 쪽은?

---

## 7–11분 · 공정한 전후 비교 설계

| 고정할 것 | 값 |
|---|---|
| 프롬프트 | 같은 5개(`data/eval_prompts.json`) |
| system 프롬프트 | 학습 때와 같은 문장 |
| 디코딩 | greedy(`do_sample=False`), 같은 `max_new_tokens` |
| seed · dtype · 장치 | 같은 값 |

- 5개 중 **학습 주제 밖 질문**을 섞는다(p4, p5)
- 좋아진 것과 **나빠진 것**(반복, 근거 없는 내용)을 같이 본다

---

## 11–15분 · 실험 기록 양식: 재현에 필요한 것만

```text
1 목적            무엇을 확인하려는 실험인가
2 고정한 것       모델 ID·revision, 데이터 버전, system, seed, 장치
3 설정            r/alpha/dropout, target, lr, epoch, batch×accum
4 결과            step, 시간, VRAM 예측 vs 실측, loss 처음→마지막
5 샘플 출력       전후 3개 이상 + 형식 준수율
6 관찰과 실패     예상과 다른 점, 오류 첫 줄
7 다음 실험       바꿀 변수 하나
```

`EXPERIMENT_TEMPLATE.md`를 복사해 `experiments/run-001.md`로 만든다. **11·12주차와 3차 과제가 이 양식을 그대로 쓴다.**

---

## 15–17분 · 실패도 기록이다

| 증상 | 먼저 볼 것 |
|---|---|
| loss가 전혀 안 내려감 | `trainable params`가 0인가, 라벨이 전부 -100인가 |
| loss가 NaN | lr 절반, fp16이면 bf16으로 |
| CUDA out of memory | batch 절반 + accum 두 배, `--max-len` 축소 |
| 전후 출력이 똑같음 | 어댑터 경로, `disable_adapter()` 위치 |
| 답이 무한 반복 | epoch 과다, `max_new_tokens`·eos 확인 |

**질문:** 실패한 run을 기록에서 지우면 무엇을 잃는가?

---

## 17–18분 · 확장: GGUF·Ollama 가져오기

```text
merge.py  →  models/merged-run-001/ (safetensors)
          →  Ollama Modelfile의 FROM 으로 가져오기   (공식 import 문서)
          →  또는 GGUF 변환 뒤 FROM ./model.gguf
```

- 4주차 `ollama create`와 같은 흐름 — 12주차 서비스에서 재사용
- 절차와 지원 아키텍처는 Ollama 공식 문서를 기준으로 확인한다

---

## 18–20분 · 실습 인계

[3교시 실습 — 전후 비교와 실험 기록 run-001](lab.md#3교시-실습--전후-비교와-실험-기록-run-001)

완료 조건:

1. `outputs/compare-run-001.md`에 프롬프트 5개의 전후 출력과 형식 준수 수
2. `experiments/run-001.md` 7개 절을 실측값으로 채움
3. 어댑터 가중치가 아닌 기록 파일만 커밋한 `git log`

실습 30분 뒤 휴식 10분. 이번 주 정리로 이어진다.

---

## 이번 주 정리

```text
고정: 모델 ID·revision, 데이터 버전, system 프롬프트, seed, 디코딩 조건
기록: 학습 파라미터 비율, VRAM 예측 vs 실측, loss 곡선, 전후 출력, 실패
```

- LoRA는 **얼린 가중치 옆에 작은 행렬**을 붙여 배우는 방법이다
- 학습이 되었다는 증거는 loss가 아니라 **같은 조건의 전후 비교**다
- 다음 주(11주차): 이 데이터를 정제·분할하고 전후 모델을 정량·정성 평가한다
