---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 내 평가 문항과 실패 분류

---

## 0–3분 · 이번 시간의 작업

문항 세트 → 내용 검사 → 14주차 채점기 → 실패 종류 표 → 고칠 것 하나.

공개 20문항과 내 문항을 같은 채점기로 재고, 잃은 점수를 실패 종류별로 나눈다. 최종 성능은 같은 형식의 비공개 문항으로 잰다. 그래서 공개 20문항에 맞춘 변경이 다른 문장의 질문에서도 점수를 올리는지 내 문항으로 확인한다.

이 시간에 만든 내 문항과 기록표는 2~4교시에도 이어 쓴다.

---

## 3–6분 · 평가 문항과 학습 문항을 나눈다

| `QUESTION_SET` | 파일 | 쓰는 곳 |
|---|---|---|
| `"public"` | 14주차 공개 20문항 | `ex02` 공개 평가와 같은 문항 |
| `"mine"` | `my_questions.json`, `my_answers.json` | 내 평가 문항(예시 20문항) |
| `"train"` | `train_questions.json`, `train_answers.json` | 3교시 학습 문항(예시 40문항) |

평가 문항(`public`, `mine`)은 학습에 넣지 않는다. 학습한 질문으로 다시 재면 외운 답의 점수가 나온다. 공개한 `mine`·`train`은 만드는 방법을 보여 주는 예시이고, 문항을 늘리는 일은 과제에서 한다.

---

## 6–9분 · 질문 파일과 정답 파일에 같은 id로 둔다

`my_questions.json`의 mine-16은 범주가 `composite`이고 질문은 "신입생 퀴즈에 원광초급대학 설립 연도와 원광대학교 교색을 문제로 내려 합니다. 두 정답을 알려 주세요."다. `my_answers.json`에는 같은 `id`로 다음 항목을 둔다.

```json
{"id": "mine-16", "expected": [["1951", "1951년"], ["황금색", "금색"]],
 "sources": ["wku-history", "wku-symbols"], "abstain": false,
 "fact_sources": ["wku-history", "wku-symbols"]}
```

`expected`에는 사실마다 별칭 그룹을 하나씩 두고, `fact_sources`에는 사실마다 근거 문서를 같은 순서로 적는다. 답변 불가 문항은 `expected`·`sources`·`fact_sources`가 비고 `abstain`이 `true`다. [문항 작성 규칙](examples/src/lab_shared/data/README.md)

---

## 9–12분 · ex04는 14주차 채점기를 그대로 부른다

```python
BOT = "student_bot"    # 2교시에는 "rag_bot"
QUESTION_SET = "mine"  # "public", "mine", "train" 가운데 하나
```

`uv run ex04`는 `mine`·`train`을 채점하기 전에 문항 내용을 검사한다. 근거 문서 ID가 `corpus.json`에 없거나, 공개 문항이나 같은 세트의 문항과 같은 질문이 있으면 평가를 시작하지 않는다. 채점은 14주차 `evaluate`가 하므로, 공개 20문항으로 돌리면 같은 프로젝트에 설치된 `uv run ex02`와 점수를 대조할 수 있다.

---

## 12–15분 · 잃은 점수를 일곱 종류로 나눈다

| 종류 | 해당 문항 | 넣는 점수 |
|---|---|---|
| 시간 초과 | `status=timeout` | 100 |
| 실행 오류 | `status=error` | 100 |
| 형식 오류 | `status=invalid_response` | 100 |
| 답변 불가인데 답함 | 정답이 답변 불가인데 100점이 아님 | 100 |
| 답할 수 있는데 거절 | 정답이 있는데 `abstain=true` | 100 |
| 사실 누락·불필요한 답 | 답변 F1이 1보다 낮음 | 80 − `answer_points` |
| 출처 누락·불필요한 출처 | 출처 F1이 1보다 낮음 | 20 − `source_points` |

맞힌 사실이 없으면 출처 점수도 0이 되므로 100점을 모두 '사실 누락·불필요한 답'에 넣는다. 종류별 잃은 점수 합을 전체 문항 수로 나누면 '전체 평균에서 빠진 점수'다. 일곱 줄을 더하면 100에서 전체 평균을 뺀 값이 된다.

---

## 15–18분 · 가장 큰 감점 하나를 같은 조건에서 비교한다

| 원인 가설 | 확인할 곳 |
|---|---|
| 근거 문서가 모델에 가지 않았다 | 2교시 `ex05` 검색 관찰 |
| 문서는 갔는데 답을 잘못 뽑았다 | `SYSTEM_PROMPT`, 3교시 학습 |
| 형식을 어겼거나 시간 초과·실행 오류가 났다 | 4교시 `ex07` 추론 점검 |

'전체 평균에서 빠진 점수'가 가장 큰 종류 하나를 고르고 원인 가설을 하나 적는다. 아무것도 바꾸지 않고 한 번 더 재서 변동을 본다. 이 변동보다 큰 차이만 개선으로 보고, `public`과 `mine` 점수가 함께 오른 변경만 채택한다.

---

## 18–20분 · 실습 인계

1. `QUESTION_SET = "public"`으로 `ex04`와 `ex02`를 실행하고 점수를 대조한다.
2. 내 문항을 몇 개 더하고 `"mine"`으로 실행한다.
3. 실패 종류 표에서 가장 큰 감점 하나를 고르고 원인 가설을 적는다.
4. 같은 설정으로 한 번 더 실행하고 기록표를 채운다.

기록표의 모델 칸에는 이름과 digest 앞 12자리를 적는다. 같은 태그라도 digest가 다르면 다른 빌드다.

[1교시 실습](lab.md#1교시--내-평가-문항과-실패-분류) 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## 임베딩 RAG와 검색 관찰

---

## 0–3분 · 이번 시간의 작업

질문 → 문서 고르기(검색) → 답 만들기(모델) → 채점.

1교시에 나눈 실패 가운데 검색 탓인 것을 따로 떼어 본다. `rag_bot`은 14주차 `student_bot`과 응답 계약·시스템 지시·요청 본문의 값이 같고 검색이 다르다.

---

## 3–6분 · 낱말 겹침 검색은 같은 글자 조각을 센다

```python
terms = search_terms(question)  # 한글 낱말과 두 글자 조각
score = len(terms & search_terms(doc["title"] + " " + doc["text"]))
```

"원광대의 뿌리가 된 학교는 어디인가요?"에서 연혁 문서는 3점으로 위치 문서(4점)보다 낮다. 같은 3점인 문서들 사이에서도 자료 순서에 밀려 4위가 되고, `TOP_K` 3 밖으로 빠진다.

---

## 6–9분 · 임베딩 검색은 뜻이 가까운 문서를 찾는다

```python
vectors = embed([f"{doc['title']}: {doc['text']}" for doc in corpus])
query = embed([question])[0]
ranked = sorted(((cosine(query, v), doc) for doc, v in zip(corpus, vectors)), ...)
```

같은 질문에서 bge-m3(ID `790764642607`, Ollama 0.40.17)는 연혁 문서를 1위로 골랐다. 문서 벡터는 첫 검색 때 한 번 만든다. 채점에서는 준비 질문(최대 120초) 때 만들어진다.

---

## 9–12분 · 6주차 LangChain 예제와 같은 일을 한다

| 6주차 | rag_bot |
|---|---|
| `OllamaEmbeddings(model="bge-m3")` | `EMBED_MODEL`, `embed()`가 `/api/embed` 호출 |
| `InMemoryVectorStore.add_texts` | 첫 검색 때 만드는 `index` |
| `similarity_search_with_score` | `rank()`, `retrieve()` |

`urllib`로 쓴 이유: `student_bot`도 같은 방식이라 추가 패키지가 필요 없고, 과제 폴더의 `student_bot`에 그대로 옮길 수 있다.

---

## 12–16분 · 검색만 따로 잰다

```text
[문항 ID] fact 근거 wku-history
    student_bot 놓침 wku-history | rag_bot 포함(최고 유사도 0.xxx)
rag_bot: 근거 문서를 모두 찾은 문항 n/16, 답변 불가 문항에 보낸 문서 평균 n개
```

`ex05`는 답을 만들지 않는다. 정답의 근거 문서(`fact_sources`)가 검색 결과에 들었는지, 답변 불가 문항에 문서를 몇 개 보냈는지 센다. 위는 출력 형식이다. 문서가 5개뿐이라 `TOP_K` 3이면 평가 문항의 근거는 대부분 들어간다. 차이는 학습 문항(`train`)에서 드러난다.

---

## 16–18분 · 바꿔 볼 두 상수

```python
TOP_K = 3        # 모델에 보낼 문서 수
MIN_SCORE = 0.0  # 이 유사도보다 낮은 문서는 보내지 않는다
```

보낼 문서가 하나도 없으면 모델을 부르지 않고 답변을 보류한다. 문서를 많이 보내면 근거가 들어갈 가능성은 커지지만 입력이 길어지고 관계없는 문서도 함께 간다.

---

## 18–20분 · 실습 인계

1. `uv run ex05`로 두 검색을 비교하고, `SETS`에 `"train"`을 더해 다시 본다.
2. `ex04`의 `BOT`을 `"rag_bot"`으로 바꿔(검색 상수는 기본값) `mine`·`public`을 잰다.
3. `TOP_K`나 `MIN_SCORE` 하나만 바꿔 `ex05`·`ex04`를 다시 실행한다. 두 점수가 함께 오른 변경만 채택한다.
4. 3교시에 쓸 검색 설정 하나를 `rag_bot`에 남긴다.

[2교시 실습](lab.md#2교시--임베딩-rag와-검색-관찰) 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 학습 예시와 LoRA 학습·등록

---

## 0–3분 · 이번 시간의 작업

`ex06` 학습 예시 → `ft01` 학습 → `ft02` 병합 → GGUF 변환 → `ollama create` → `ex04` 채점.

확인할 것: 0.5B 모델이 학습 예시로 응답 계약(JSON 세 키)과 짧은 답 고르기를 따르게 되는가. 학습 전 `wku-base`와 같은 문항으로 비교한다. 학습은 `finetune/`에서, 학습 예시와 채점은 `examples/`에서 한다.

---

## 3–6분 · 학습 예시는 rag_bot이 보낼 대화로 만든다

```python
documents = rag_bot.retrieve(question)
messages = rag_bot.messages(question, documents)
row = {"messages": messages + [{"role": "assistant", "content": target(item)}]}
```

학습 문항(질문·정답 JSON)마다 실제 요청과 같은 대화를 만든다. 평가 문항과 같은 학습 문항이 있으면 모두 보여 주고 멈춘다. 검색이 근거 문서를 놓친 문항은 학습에서 뺀다.

---

## 6–9분 · 7주차와 달리 길이·메모리 때문에 바꾼 설정

| 상수 | 7주차 | 이 특강 |
|---|---|---|
| `MAX_LENGTH` | 256 | 1024 |
| `DTYPE` | float32 | bfloat16 |
| `GRADIENT_CHECKPOINTING` | 없음 | True |
| 패딩 | 없음 | 64토큰 단위 |

검색 문서가 든 예시는 256토큰에 담기지 않는다. 기준 PC(Windows 11)에서는 메모리가 넘쳐도 오류 없이 느려졌다. 학습 전에 Ollama가 올린 모델을 내린다. 전체 차이표는 따라하기에 있다.

---

## 9–12분 · 병합하고 GGUF로 바꾼다

```powershell
uv run ft02
uv run --locked --with sentencepiece==0.2.3 --with protobuf==7.36.2 `
  python tools/llama.cpp/convert_hf_to_gguf.py `
  models/wku-lora-merged --outfile models/wku-lora.gguf --outtype f16
```

Ollama 0.40.17은 병합한 safetensors 폴더를 바로 등록하지 못했다. GGUF로 바꿔 등록한다.

---

## 12–15분 · 등록하고 같은 채점기로 잰다

```text
FROM ./models/wku-lora.gguf
PARAMETER temperature 0
```

`ollama create wku-lora -f Modelfile.lora`로 등록한다. `ex04`의 `BOT`이 `"rag_bot"`인지 확인하고 `rag_bot`의 `MODEL`을 `"wku-lora"`로 바꿔 잰다. 학습 전 모델 `wku-base`도 같은 문항으로 잰다. 7주차 `Modelfile`을 복사하면 신화 안내자 `SYSTEM`과 `num_predict 120`도 함께 등록된다.

---

## 15–18분 · 시연: ft01 출력 읽기

강의자 PC에서 `uv run ft01`을 실행하며 짚는다.

- 시작 부분(`모델:` 줄 다음): 학습 예시 수와 최소·최대 토큰 수
- step마다: loss가 줄어드는지
- 끝부분: `train_runtime`(초)과 `GPU 최대 할당 메모리`

step 시간이 점점 늘면 VRAM이 넘친 것이다.

---

## 18–20분 · 실습 인계

1. (examples/) `ex06` → `ollama stop bge-m3`
2. (finetune/) `ft01` → `ft02` → 변환 → `ollama create wku-lora`
3. (examples/) `ex04`로 `wku-lora`와 `wku-base`를 같은 문항으로 잰다.

답이 이상한 문항은 4교시에 `ex07`로 본다. 공개한 학습 문항은 일부이고 늘리는 일은 과제에서 한다. 평가 문항은 학습 데이터에 넣지 않는다. 과제의 모델 규칙은 강좌 공지를 따른다.

[3교시 실습](lab.md#3교시--학습-예시와-lora-학습등록) 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 4교시 · 설명 20분
## 추론 버그 잡기

---

## 0–3분 · 이번 시간의 작업

실패한 문항 → `ex07`로 재현 → [6]의 증상과 근거 → 고칠 곳 → 버그 심기.

학습과 등록이 끝났는데 답이 이상하면, 모델을 다시 학습하기 전에 봇이 Ollama에 실제로 보낸 요청과 받은 응답부터 본다. 3교시에 등록한 자기 모델과 기준 봇(14주차 `student_bot`)을 같은 질문으로 점검하고, 버그를 일부러 넣어 증상과 원인을 짝짓는다. 명령은 모두 `examples/`에서 실행한다.

---

## 3–6분 · ex07은 봇이 보낸 요청과 받은 응답을 보여 준다

| 구역 | 보는 값 |
|---|---|
| [1] 호출 목록 | 경로, 모델, HTTP 상태, 소요 시간 |
| [2] 생성 호출 | 보낸 설정과 messages, 모델 정보, 컨텍스트, 응답, 시간 |
| [3] 임베딩 호출 | 모델, 입력 수, 벡터 수와 차원 |
| [4] 실행 위치 | `/api/ps`의 GPU 적재 비율과 context_length |
| [5] 최종 판정 | 반환값, 응답 계약, 적재를 뺀 시간, 채점기 status |
| [6] 의심되는 문제와 고칠 곳 | 증상, 근거 값, 고칠 곳. 끝에 참고 줄 |

`ex07`은 봇 코드를 바꾸지 않고, `answer(question)`을 한 번 실행하는 동안 `urllib`로 나간 요청을 가로챈다. 봇 파일을 고쳤으면 `/bye`로 끝내고 다시 실행한다.

---

## 6–9분 · 실패한 문항을 질문 하나로 재현한다

```text
[mine-xx] fact  점수 n  status=…  실패: …
    질문 원광대학교 …
    응답 {"answers": …}
```

`ex04`에서 실패한 문항은 `질문` 줄이 함께 나온다. 이 문장을 `ex07`의 `질문>`에 그대로 넣는다. `ex07`의 `BOT`과 `rag_bot`의 `MODEL`은 `ex04`에서 잴 때와 같게 둔다. 채점기는 문항마다 질문 하나만 보내므로 앞 질문에 기대지 않는다.

| [5]의 status | 채점 | 1교시 실패 종류 |
|---|---|---|
| `ok` | 정답과 비교해 점수를 매긴다 | 답의 내용(사실·출처·거절) |
| `invalid_response`, `timeout`, `error` | 0점 | 형식 오류, 시간 초과, 실행 오류 |

---

## 9–12분 · [6]은 증상, 근거, 고칠 곳 순서로 읽는다

```text
[6] 의심되는 문제와 고칠 곳
  - <증상> | 근거: <[2]~[5]의 값> | 고칠 곳: <바꿀 상수나 요청 값>
  참고: 요청이 덮어쓰지 않은 Modelfile 값 | <모델> <이름>=<값>, … | 영향이 의심되면 …
```

문제 줄은 위에서부터 읽고, 근거 값을 [2]~[5]에서 찾아 대조한다. 증상 이름과 고칠 곳은 [추론 버그 잡기](examples/debugging.md#증상별-확인할-값과-고칠-곳)의 표에 있다. 문제 줄이 없는데 답이 틀렸으면 검색된 문서(`ex05`)와 `SYSTEM_PROMPT`를 본다. 첫 질문의 '모델 새로 적재'는 모델을 올린 시간이고, 채점기는 준비 질문으로 이 시간을 뺀다.

---

## 12–14분 · 요청에 없는 값은 모델이 정한다

```powershell
ollama show <모델>               # capabilities, 생각 모드, 최대 컨텍스트, 템플릿 출처
ollama show <모델> --parameters  # Modelfile의 PARAMETER
```

요청 options에 넣은 값은 그 요청에 쓰이고, 넣지 않은 값은 모델을 등록할 때의 Modelfile이 정한다. 같은 봇 코드라도 `MODEL`만 바꾸면 동작이 달라질 수 있다. [2]의 'Modelfile 기본값'에서 '(요청이 덮어씀)' 표시가 없는 값을 [6] 끝의 참고 줄이 모델마다 모은다. temperature는 '온도를 모델 기본값에 맡김' 규칙이 따로 본다. 참고 줄은 그런 값이 있다는 것만 알려 준다. 답에 주는 영향은 같은 이름의 값을 요청 options에 넣고 `ex04`로 재 봐야 안다.

---

## 14–16분 · 버그를 하나씩 넣고 예상과 비교한다

| 버그 | `rag_bot`에서 바꾸는 값 |
|---|---|
| 1. 생각 모드 켜기 | `"think": False` → `"think": True` |
| 2. 출력 한도 줄이기 | `"num_predict": 512` → 질문 A eval_count의 절반(정수) |
| 3. 없는 모델 이름 | `MODEL` → 지금 이름에서 한 글자를 틀리게 |

질문 A는 '원광대학교를 상징하는 새는 무엇인가요?'다. 넣기 전 `git diff -- src/rag_bot/__init__.py`를 기록한다 → 예상을 적는다 → 버그 하나를 넣는다 → `ex07`에 질문 A, `ex04`로 실패 종류 표 → 넣기 전 값으로 되돌리고 `git diff`가 기록과 같은지 본다. 같은 버그라도 `MODEL`이 가리키는 모델에 따라 결과가 다를 수 있다.

---

## 16–18분 · 시연: ex07 출력 읽기

강의자 PC에서 버그 없이 `uv run ex07`을 실행해 질문 하나를 넣고 위에서부터 짚는다.

- [1]: 호출 순서와 HTTP 상태
- [2]: 보낸 think·stream·options, 모델 정보, 응답의 done_reason·eval_count
- [5]: 소요 시간과 적재를 뺀 시간, 채점기 status
- [6]: 문제 줄과 참고 줄

이어서 `git diff -- src/rag_bot/__init__.py`로 넣기 전 상태를 기록하는 것까지 보인다.

---

## 18–20분 · 실습 인계

1. (examples/) `ex04`에서 실패한 문항의 `질문` 줄을 `ex07`(`BOT = "rag_bot"`, `MODEL`은 자기 모델)에 넣는다.
2. `BOT = "student_bot"`으로 같은 질문을 넣고 두 출력을 비교한다.
3. `ex07`의 `BOT`을 `"rag_bot"`으로 되돌리고 넣기 전 `git diff`와 질문 A 기준값을 적은 뒤, 버그 1~3을 하나씩 넣어 `ex07`·`ex04`로 관찰하고 되돌린다.
4. 증상, 확인한 값, 고칠 곳을 실습지 4교시 표에 적는다.

나머지 버그는 과제 기간에 골라서 해 본다(선택). 학습한 모델의 답이 이상할 때도 [추론 버그 잡기](examples/debugging.md)로 좁힌다.

[4교시 실습](lab.md#4교시--추론-버그-잡기) 30분 뒤 휴식 10분.
