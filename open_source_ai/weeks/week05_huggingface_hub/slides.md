---
marp: true
theme: default
paginate: true
header: "오픈소스 AI 응용 · 5주차"
footer: "Hugging Face Hub와 공개 자원 분석"
---

# 5주차
## Hugging Face Hub와 공개 자원 분석

**60분 블록 × 3**<br>
매 블록 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분

---

## 이번 주 세 블록

| 교시 | 설명·시연 20분 | 직접 해결 실습 30분 |
|---|---|---|
| 1교시 | Hub 구조와 모델 카드 | 모델 카드 분석표와 캐시 보고 |
| 2교시 | Transformers pipeline 첫 추론 | pipeline으로 분류와 생성 실행하기 |
| 3교시 | datasets와 출처 기록 | 데이터셋 살펴보기와 출처 기록표 |

이번 주 질문: **공개된 모델과 데이터가 정말 내 프로젝트에 쓸 수 있는 것인지 어떤 문서와 정보로 판단하는가?**

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## Hub 구조와 모델 카드

---

## 0–3분 · 이어받는 것: Ollama 라이브러리 밖으로

4주차 `OLLAMA_MODEL`은 Ollama 라이브러리 안의 이름이었다. 오늘은 그 원본이 있는 곳으로 간다.

```text
huggingface.co/
 ├─ models/    Qwen/Qwen2.5-0.5B-Instruct   가중치 + 토크나이저 + 모델 카드
 ├─ datasets/  조직/이름                     데이터 파일 + 데이터 카드
 └─ spaces/    조직/앱이름                   데모 앱
```

- 저장소 하나 = **Git 저장소**(큰 파일은 LFS). 주소는 `조직/이름`
- 오늘 쓸 모델은 수업 전에 캐시되어 있다. 실습 중 새로 받지 않는다

**질문:** `ollama pull qwen3:4b`가 받는 GGUF 파일의 원본 가중치는 어디에 있는가?

---

## 3–6분 · Model Card 읽는 순서

| 순서 | 항목 | 찾는 질문 |
|---|---|---|
| 1 | 라이선스 | 상업적 이용·재배포·수정이 되는가 |
| 2 | 의도된 용도·금지 용도 | 내 용도가 허용 범위 안인가 |
| 3 | 학습 데이터 | 무엇으로 배웠고 공개되어 있는가 |
| 4 | 평가·한계·편향 | 어떤 입력에서 약한가 |
| 5 | 언어·크기·형식 | 한국어, VRAM, safetensors 여부 |

카드가 비어 있으면 **"모른다"가 답**이지 "괜찮다"가 아니다.

---

## 6–9분 · 카드 메타데이터가 곧 검색 조건이다

```yaml
license: apache-2.0
language:
  - en
  - ko
pipeline_tag: text-generation
base_model: Qwen/Qwen2.5-0.5B
```

- 카드(README.md) 맨 위 `---` 두 줄 사이의 YAML이 Hub 검색 필터·라이선스 표시·태스크 배지의 원천이다
- `license: other`와 별도 약관 파일은 조건을 **직접 읽어야** 하는 신호다
- `base_model`은 출처 사슬. 파생 모델은 원본의 조건을 이어받는다

**질문:** `language`에 `ko`가 없는 모델을 한국어에 쓰면 어떤 일이 생기는가?

---

## 9–12분 · gated 모델과 토큰

```text
카드 열람      ── 누구나
파일 내려받기  ── 약관 동의(gated) → 계정 토큰 → .env 의 HF_TOKEN
```

- Llama Community License, Gemma Terms of Use: **오픈 웨이트**지만 조건이 붙는다
- SPDX 목록에 없는 라이선스는 `LicenseRef-이름`으로 적고 조건을 한 줄 요약한다
- 토큰은 `.env`에만 둔다. 코드·슬라이드·커밋에 넣지 않는다
- 토큰이 없어도 카드는 읽을 수 있다. 분석은 토큰 없이 시작한다

**핵심:** 동의 버튼은 조건을 **읽었다는 서명**이다.

---

## 12–14분 · revision으로 고정하기

```python
from transformers import pipeline

clf = pipeline("text-classification", model=MODEL_ID,
               revision="a1b2c3d4e5f6")  # commit hash
```

- `main`은 움직인다. 카드가 바뀌고 가중치가 교체되기도 한다
- 재현 가능한 기록 = 모델 ID + **commit hash**
- 해시는 저장소의 Files and versions 탭, 또는 캐시의 snapshots 폴더 이름에 있다

**질문:** 3주차 `uv.lock`과 같은 역할을 하는 것은 무엇인가?

---

## 14–17분 · 캐시 구조, 용량, 오프라인

```text
HF_HOME/hub/models--Qwen--Qwen2.5-0.5B-Instruct/
 ├─ blobs/                    실제 파일(내용 해시 이름)
 ├─ refs/main                 → commit hash
 └─ snapshots/COMMIT_HASH/    config.json, model.safetensors → blobs 링크
```

- `HF_HOME`을 바꾸면 캐시 위치가 바뀐다. 실습실은 공용 위치를 쓸 수 있다
- 용량 감: 파라미터 0.5B × 2바이트(fp16) ≈ 1 GB. 토크나이저·설정 파일은 덤
- `HF_HUB_OFFLINE=1`이면 네트워크 없이 캐시만 쓴다. 없는 모델은 즉시 실패한다
- `scan_cache_dir()`가 이 구조를 표로 돌려준다

---

## 17–20분 · 실습 인계

[1교시 실습 — 모델 카드 분석표와 캐시 보고](lab.md#1교시-실습--모델-카드-분석표와-캐시-보고)

완료 조건:

1. 모델 3개의 라이선스·SPDX·용도·학습 데이터 공개 여부·한계를 `model_cards.md`에 채웠다
2. `cache_report.py` 출력에서 캐시 위치·총 용량·commit hash를 기록했다
3. "셋 중 우리 프로젝트에 못 쓰는 것과 이유"를 한 문장으로 적었다

실습 30분 뒤 휴식 10분. 휴식 후 2교시.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## Transformers pipeline 첫 추론

---

## 0–3분 · 이어받는 것: 카드에서 코드로

1교시에서 고른 모델 ID와 commit hash가 이제 코드의 인자가 된다.

```text
"이 수업은 재미있다"
   ─ 토크나이저 ─▶ [101, 9302, …]
   ─ 모델 ──────▶ logits
   ─ 후처리 ────▶ {"label": "positive", "score": 0.93}
```

```python
from transformers import pipeline
clf = pipeline("text-classification", model=MODEL_ID, revision=COMMIT)
clf("이 수업은 재미있다")
```

task 이름 하나가 전처리·모델 클래스·후처리를 한 벌로 고른다. 6주차에 이 세 단계를 직접 쪼갠다.

---

## 3–6분 · task 종류와 모델 명시

| task | 입력 → 출력 | 이번 주 |
|---|---|---|
| `text-classification` | 문장 → 라벨·점수 | 감성 분류 |
| `text-generation` | 프롬프트 → 이어 쓴 글 | 수업 도우미 답변 |
| `feature-extraction` | 문장 → 벡터 | 7주차 |
| `token-classification` | 문장 → 단어별 태그 | 비교만 |
| `image-classification` | 이미지 → 라벨 | 비교만 |

`pipeline("text-classification")`처럼 모델을 생략하면 라이브러리가 기본 모델을 골라 준다. 편하지만 라이선스도 revision도 내가 고른 것이 아니다.

**핵심:** `model=`과 `revision=`은 항상 쓴다.

---

## 6–9분 · 한국어 모델 고르기

카드에서 확인할 세 줄:

1. `language:`에 `ko` 또는 `multilingual`이 있는가
2. 학습 데이터에 한국어가 **실제로** 들어 있는가 (태그만 있는 경우가 있다)
3. 라벨의 이름과 뜻 — `LABEL_0`인가, `positive/negative`인가

- 다국어 토크나이저는 한국어를 자를 수는 있다. 잘 아는 것과는 다르다
- 결과가 이상하면 모델 탓 전에 카드의 언어 목록을 다시 본다

**질문:** 라벨이 `LABEL_0`, `LABEL_1`로만 나오면 어디에서 뜻을 찾는가?

---

## 9–12분 · device와 dtype

```python
pipeline(task, model=MODEL_ID, device=0)      # 0: 첫 GPU, -1: CPU
model.to(device="cuda:0", dtype=torch.float16)
```

| dtype | 파라미터당 | 0.5B 모델 | 특징 |
|---|---|---|---|
| float32 | 4바이트 | 약 2 GB | CPU 기본값 |
| float16 | 2바이트 | 약 1 GB | GPU 기본값, 표현 범위 좁음 |
| bfloat16 | 2바이트 | 약 1 GB | 범위 넓음, 최신 GPU |

- `device_map="auto"`(accelerate)는 여러 장치에 나눌 때 쓴다. 12 GB 한 장이면 `device=0`이면 된다
- dtype 인자 이름은 버전에 따라 `dtype` 또는 `torch_dtype`이다. 예제는 `.to()`로 통일했다

---

## 12–15분 · 생성 모델 호출

```python
messages = [{"role": "system", "content": "수업 도우미다. 한국어로 짧게 답한다."},
            {"role": "user", "content": "모델을 쓰기 전에 확인할 것은?"}]
prompt = gen.tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True)
out = gen(prompt, max_new_tokens=120, do_sample=False,
          return_full_text=False)
out[0]["generated_text"]
```

- chat template이 4주차의 system/user 역할을 모델 고유의 특수 토큰 형식으로 바꾼다
- `do_sample=False`는 temperature 0과 같다. 비교 실험의 기준값이다
- Ollama의 `think` 옵션 같은 스위치는 없다. 모델이 생각을 출력하면 그것도 답의 일부다

---

## 15–17분 · 경고 메시지 읽기와 시간 재기

| 메시지 | 뜻 | 조치 |
|---|---|---|
| `Some weights ... were not used` | 헤드 불일치 | task와 모델 짝을 확인 |
| `Setting pad_token_id to eos_token_id` | 패딩 토큰 미정의 | 생성에는 대개 무해 |
| `sequence length is longer than` | 입력 잘림 | 입력을 줄이거나 나눈다 |
| `401`/`gated repo` | 약관·토큰 | 카드에서 동의, `.env` |

- 첫 호출은 워밍업이다. **두 번째 호출부터** 시간을 잰다
- GPU 시간은 `torch.cuda.synchronize()` 뒤에 멈춰야 정확하다

---

## 17–20분 · 실습 인계

[2교시 실습 — pipeline으로 분류와 생성 실행하기](lab.md#2교시-실습--pipeline으로-분류와-생성-실행하기)

완료 조건:

1. 분류 5문장·생성 1건의 출력이 `outputs/pipeline-*.json`에 남았다
2. CPU와 GPU(또는 CPU 두 번)의 로드·워밍업·추론 시간을 표로 비교했다
3. 잘못된 revision 또는 오프라인 상태의 실패 메시지를 한 줄로 요약했다

실습 30분 뒤 휴식 10분. 휴식 후 3교시.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## datasets와 출처 기록

---

## 0–3분 · 이어받는 것: 모델에서 데이터로

2교시 JSON의 commit hash는 `SOURCES.md`의 한 행이 된다. 이제 데이터 행을 채운다.

```python
from datasets import load_dataset

ds = load_dataset("조직/이름", "구성이름", split="train")
ds                 # Dataset({features: [...], num_rows: N})
ds[0]              # 첫 행 dict
ds.features        # 필드 이름 → 자료형
ds.info.license    # 카드의 license가 여기로 들어온다
```

- Hub 데이터셋도 저장소다: 파일(parquet·jsonl·csv) + Dataset Card
- `split`은 train/validation/test 같은 나눔. `config`는 한 저장소 안의 하위 데이터셋

---

## 3–6분 · 로컬 파일도 같은 API

```python
ds = load_dataset("json", data_files="data/sample_qa.jsonl", split="train")
```

- `json`·`csv`·`parquet`·`text`: 내 파일을 Hub 데이터셋과 **같은 객체**로 다룬다
- 이번 주 예제는 자체 작성 한국어 Q&A 12건이다. 네트워크 없이 3교시가 돈다
- 10주차 LoRA 학습 데이터도 같은 형식(`jsonl`)으로 만든다

**질문:** `features`에서 `Value('string')`으로 나온 필드와 `Sequence`로 나온 필드는 무엇이 다른가?

---

## 6–9분 · 스트리밍 — 전부 내려받지 않고 보기

```python
from itertools import islice

ds = load_dataset("조직/이름", split="train", streaming=True)
for row in islice(ds, 5):
    print(row)
```

- `streaming=True` → `IterableDataset`. 인덱싱과 `num_rows`가 없다
- 수십 GB 말뭉치의 앞 5개만 보고 구조·라이선스를 판단할 때 쓴다
- 캐시에 남지 않으므로 실습실 디스크를 아낀다

**핵심:** 구조를 모르는 데이터는 먼저 5개만 본다.

---

## 9–12분 · Dataset Card 읽기

| 항목 | 찾는 질문 |
|---|---|
| 요약·출처 | 누가 어디서 모았나 (크롤링, 사람 작성, 합성) |
| 구조 | 필드·split·건수가 카드와 실제에서 같은가 |
| 수집·주석 방법 | 라벨을 누가 붙였나, 지침이 있나 |
| 개인정보·민감 정보 | 이름·연락처·계정이 들어 있나 |
| 라이선스 | 데이터 자체와 주석의 라이선스가 다른가 |

카드의 건수와 `dataset_peek.py`의 건수가 다르면 **버전이 다르거나** 카드가 낡은 것이다.

---

## 12–15분 · 데이터 라이선스와 위험

| 라이선스 | 상업 이용 | 조건 |
|---|---|---|
| CC0-1.0 | 가능 | 없음 |
| CC-BY-4.0 | 가능 | 출처 표시 |
| CC-BY-SA-4.0 | 가능 | 출처 표시 + 같은 조건으로 공유 |
| CC-BY-NC-4.0 | **불가** | 비상업만 |
| 연구 전용·`other` | 대개 불가 | 조건문을 직접 읽는다 |

- 크롤링 데이터는 라이선스가 있어도 **원저작자의 권리**가 남는다
- 개인정보가 섞인 데이터는 라이선스와 무관하게 쓸 수 없다. 11주차 PII 점검으로 이어진다

**질문:** CC-BY-SA 데이터로 학습한 모델은 어떤 조건을 이어받는가? (정해진 답이 하나가 아니다)

---

## 15–17분 · SOURCES.md — 출처 기록표

```text
| 이름 | 종류 | 출처 URL | 버전/revision | 라이선스(SPDX) | 용도 | 변경 내용 |
```

- 모델·데이터·코드 조각까지 **한 표**에 모은다
- 버전 칸에는 commit hash 또는 데이터셋 revision을 적는다. "최신"이라고 쓰지 않는다
- 변경 내용 칸: 필터링·정제·번역·병합 등 내가 손댄 것
- 8주차 2차 종합과제의 라이선스 분석 보고가 이 표에서 시작한다

**핵심:** 기록하지 않은 출처는 나중에 **찾을 수 없다**.

---

## 17–20분 · 실습 인계

[3교시 실습 — 데이터셋 살펴보기와 출처 기록표](lab.md#3교시-실습--데이터셋-살펴보기와-출처-기록표)

완료 조건:

1. `dataset_peek.py` 출력으로 필드 구조·건수·샘플 5개를 기록했다
2. 공개 데이터셋 1개의 Dataset Card에서 라이선스·수집 방법·개인정보 항목을 찾았다
3. `SOURCES.md`에 모델 2개 + 데이터 1개를 revision·라이선스·용도와 함께 적었다

실습 30분 뒤 휴식 10분. 다음 주는 pipeline 안쪽의 텐서와 학습 루프다.

---

## 이번 주 정리

```text
카드 읽기 → 라이선스·용도·데이터 판단 → revision 고정 → 캐시·오프라인
pipeline(model=, revision=, device=) → 시간·경고·commit hash 기록
load_dataset(streaming=) → 5개 보기 → Dataset Card → SOURCES.md
```

공개되어 있다는 것과 **써도 된다**는 것은 다르다. 판단의 근거는 문서와 해시다.
