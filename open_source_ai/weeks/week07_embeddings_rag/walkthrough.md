# 7주차 따라하기 — 문서 분할, 임베딩 검색, 출처 있는 답, 평가셋

이 문서는 7주차 시연·실습을 **순서대로 그대로 재현**하기 위한 절차서다.
강의자는 각 교시의 20분 시연을 이 순서로 진행하고, 학생은 실습·복습 때 같은 순서로 따라 한다.
각 단계는 `할 일 → 예상 결과 → 확인` 순서로 되어 있다. 예상 결과가 다르면 다음 단계로 넘어가지 않는다.

## 시작 전 준비

- uv, Git, VS Code, PowerShell을 사용한다. Ollama 서버가 켜져 있다(`ollama list`가 오류 없이 출력된다).
- 임베딩 모델(`HF_EMBED_MODEL`)과 생성 모델(`OLLAMA_MODEL`)이 수업 전에 캐시되어 있다. 이 문서의 `intfloat/multilingual-e5-small`·`qwen3:8b`·`qwen3:0.6b`는 교재 검증용 기본값이며 실제 이름은 환경 기준표가 정한다. 실습 중 모델을 내려받지 않는다.
- [`examples/mini_rag`](examples/README.md)를 개인 저장소 안의 폴더(`$HOME\osa-practice\week07\mini_rag`)에 **복사**해서 사용한다. 수업 자료 원본은 수정하지 않는다. `uv sync`는 수업 전에 한 번 실행해 둔다.
- 터미널 명령은 복사한 `mini_rag` 폴더 안에서 실행한다. 현재 경로를 먼저 확인하는 습관을 들인다.

---

## 1교시 — 문서를 나누고 임베딩으로 찾기

### 단계 1. 프로젝트 복사와 실행 확인

**할 일**

```powershell
$src = "C:\teaching_repo\open_source_ai\weeks\week07_embeddings_rag\examples"
$dst = "$HOME\osa-practice\week07"
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item -Recurse "$src\mini_rag" "$dst\mini_rag"
Set-Location "$dst\mini_rag"
Copy-Item .env.example .env
uv sync
uv run python chunk.py --help
Get-ChildItem docs
```

**예상 결과** — `uv sync`가 `.venv`를 만들고(수업 전에 했다면 몇 초 안에 끝난다), `--help`에 `--docs`·`--size`·`--overlap`·`--hard`·`--out` 옵션이 보인다. `docs/`에 `.md` 파일 6개가 있다.

**확인** — [ ] `docs/` 파일 6개의 제목을 읽고 "uv.lock은 왜 커밋하는가"의 답이 어느 파일에 있을지 적었다.

### 단계 2. 300자 청크로 분할

**할 일** — `uv run python chunk.py --size 300 --overlap 50`을 실행하고 `outputs/chunks-300.json`을 연다.

**예상 결과** — 파일별 글자 수·청크 수 표와 `합계 청크 N개, 평균 M자 → outputs\chunks-300.json` 줄이 나온다. 문서 하나에 청크가 1~3개씩, 전체 10~20개 안팎이다. JSON의 청크마다 `id`(`파일명#번호`)·`source`·`start`·`end`·`text`가 있고, `text`는 대부분 문장 끝(`다.`)에서 끝난다.

**확인** — [ ] 이웃한 청크 두 개의 `start`·`end`를 비교해 50자 겹침이 있는 것을 보았다.

### 단계 3. 임베딩 인덱스 만들기

**할 일** — `uv run python embed.py --chunks outputs/chunks-300.json`을 실행한다.

**예상 결과** — `청크 N개 로드`, `백엔드 st · 모델 intfloat/multilingual-e5-small · 장치 cuda:0`(GPU 없는 PC는 `cpu`), `벡터 N × 384 · 모델 로드 …s · 인코딩 …s`, `저장 → outputs\index.json, outputs\index.npy`가 차례로 나온다. 인코딩은 수 초 안에 끝난다.

모델 로드가 실패하면 메시지가 `.env`의 `HF_EMBED_MODEL`·캐시·`HF_HUB_OFFLINE=1`·`--backend ollama` 순으로 확인할 것을 알려 준다. 네트워크가 없으면 `.env`의 `HF_HUB_OFFLINE=1` 주석을 풀고 다시 실행한다.

**확인** — [ ] `outputs/index.json`의 `backend`·`model`·`device`·`encode_sec`를 기록했다.

### 단계 4. 질의 2개로 top-3 검색

**할 일**

```powershell
uv run python search.py --query "uv.lock은 왜 커밋하는가" --query "Apache-2.0 라이선스가 MIT와 다른 점은?" --top-k 3
```

**예상 결과** — 질의마다 `순위·점수·id·미리보기` 3행이 나온다. 질의 A의 1위는 `uv_basics.md#…`, 질의 B의 1위는 `oss_license.md#…`이고 점수는 0.8 안팎이다. 마지막 줄에 `저장 → outputs\search-<시각>.json`이 나온다.

**확인** — [ ] 1위 청크의 `text`(JSON)에 질문에 답하는 문장이 실제로 들어 있는지 확인했다. 점수의 절대값이 아니라 순위와 1·2위 차이를 보았다.

### 단계 5. 150자 인덱스로 같은 질의 반복

**할 일**

```powershell
uv run python chunk.py --size 150 --overlap 30
uv run python embed.py --chunks outputs/chunks-150.json --out outputs/index-150
uv run python search.py --index outputs/index-150 --query "uv.lock은 왜 커밋하는가" --query "Apache-2.0 라이선스가 MIT와 다른 점은?" --top-k 3
```

**예상 결과** — 청크 수가 300자의 약 2.5배가 된다(13개 → 33개). 1위 파일은 대체로 같지만 청크 번호가 바뀌고, 같은 파일의 이웃 청크가 top-3에 함께 들어오거나 답 문장이 두 청크에 나뉘어 1위 본문만으로는 답이 완성되지 않는 경우가 보인다.

**확인** — [ ] 두 인덱스의 1위 청크 `text`를 나란히 놓고 "답 문장이 온전히 들어 있는 쪽"을 적었다.

### 단계 6. 경계 실패 재현과 기록

**할 일** — `uv run python chunk.py --size 300 --overlap 0 --hard`를 실행하고 `outputs/chunks-300-hard.json`에서 문장 중간에서 끊긴 청크를 찾는다.

**예상 결과** — 청크의 `text`가 `…GPL은 수정한 코드를 배포할 때 같은`(`oss_license.md#0`)처럼 정확히 300자에서, 문장 중간에서 끝난다. 이런 청크는 임베딩해도 뜻이 흐려져 점수가 낮아진다.

**확인** — [ ] [`lab.md`](lab.md) 1교시 완료 조건을 모두 표시하고 `search_note.md`에 청크 표·top-3 비교표·비교 문장을 적었다. 실습 30분 뒤 휴식 10분.

---

## 2교시 — 출처 있는 답 생성과 거부 경로

1교시 폴더에서 계속한다. 새로 시작하는 날이면 1교시 단계 1~3을 먼저 실행해 `outputs/index.json`을 만든다.

### 단계 1. 서버·모델·인덱스 확인

**할 일**

```powershell
Set-Location "$HOME\osa-practice\week07\mini_rag"
Invoke-RestMethod http://localhost:11434/api/tags | Select-Object -ExpandProperty models | Format-Table name, size
Test-Path outputs\index.npy
```

**예상 결과** — 캐시된 모델 이름과 크기가 표로 나오고 `.env`의 `OLLAMA_MODEL`이 그 안에 있다. `Test-Path`가 `True`다. GPU가 없는 PC는 `.env`의 `OLLAMA_MODEL`을 캐시된 소형 모델로 바꾼다.

**확인** — [ ] 서버를 잠시 끄거나 `.env`의 `OLLAMA_HOST` 포트를 비어 있는 값으로 바꿔 `rag_answer.py`를 실행하면 스택 트레이스 대신 `오류: Ollama 서버에 연결할 수 없다…` 한 문장이 나오는 것을 보았다(본 뒤 원래대로 되돌린다).

### 단계 2. 출처 있는 답 첫 건

**할 일** — `uv run python rag_answer.py --query "uv.lock은 왜 커밋하는가" --top-k 3`을 실행한다.

**예상 결과** — `질문:`, `검색: ['uv_basics.md#…', …]`, `답:` 아래에 두세 문장과 마지막 줄 `[출처: uv_basics.md#1]`(번호는 다를 수 있다), 이어서 `인용 ['uv_basics.md#1'] · 검색 결과 안의 인용 ['uv_basics.md#1'] · 거부 False`, `프롬프트 …자 · 토큰 {'prompt_eval_count': …, 'eval_count': …, 'total_duration_ms': …}`, `저장 → outputs\rag-<시각>.json`이 나온다.

**확인** — [ ] `인용`과 `검색 결과 안의 인용`이 같다. 다르면 인용된 id가 `outputs/index.json`에 존재하는지 확인했다.

### 단계 3. 프롬프트 구조 보기와 두 번째 답

**할 일**

```powershell
uv run python rag_answer.py --query "uv.lock은 왜 커밋하는가" --show-prompt
uv run python rag_answer.py --query "Apache-2.0 라이선스가 MIT와 다른 점은?" --top-k 3
```

**예상 결과** — 첫 명령은 `--- system ---` 아래 규칙 4개, `--- user ---` 아래 `[자료 시작]`·`[1] 출처: …`·본문·`[자료 끝]`·`[질문] …`을 보여 준 뒤 답을 낸다. 두 번째 명령의 답은 "특허" 관련 문장을 담고 `[출처: oss_license.md#…]`로 끝난다.

**확인** — [ ] 규칙이 system에, 자료와 질문이 user에 있는 이유를 한 문장으로 적었다.

### 단계 4. 자료 밖 질문의 거부와 `--no-context` 비교

**할 일**

```powershell
uv run python rag_answer.py --query "LoRA의 rank는 무엇인가" --top-k 3
uv run python rag_answer.py --query "LoRA의 rank는 무엇인가" --no-context
```

**예상 결과** — 첫 명령은 검색이 관련 없는 청크 3개를 돌려주지만(검색은 항상 무언가를 돌려준다) 답은 `제공된 자료에서 찾을 수 없습니다.`이고 `거부 True`다. 두 번째 명령은 `검색: (컨텍스트 없음)`이고 모델이 사전 지식으로 답을 지어내거나 거부한다. 소형 모델은 첫 명령에서도 거부하지 않고 답할 수 있다. 어느 쪽이든 그대로 기록한다.

**확인** — [ ] 두 답의 차이를 "출처"와 "검증 가능성"으로 적었다. 거부하지 않았다면 "근거 없는 답(환각)"으로 분류했다.

### 단계 5. 컨텍스트 창 경계

**할 일** — `uv run python rag_answer.py --query "uv.lock은 왜 커밋하는가" --top-k 3 --num-ctx 256`을 실행한다.

**예상 결과** — `prompt_eval_count`가 256을 넘지 않는다. 단계 2와 같은 답이 나오거나, 거부로 바뀌거나, 출처 형식이 사라진 답이 나온다. 잘려 나간 부분에 system 규칙이 포함되면 규칙이 지켜지지 않는 것이 관찰 포인트다.

**확인** — [ ] [`lab.md`](lab.md) 2교시 완료 조건을 모두 표시하고 `rag_note.md`에 답 2건·거부 결과·비교 문장을 적었다. 실습 30분 뒤 휴식 10분.

---

## 3교시 — 평가셋으로 품질 재기와 실패 분석

1교시 인덱스 2개(`outputs/index`, `outputs/index-150`)가 필요하다. 새로 시작하는 날이면 1교시 단계 1~3과 단계 5의 앞 두 명령을 먼저 실행한다.

### 단계 1. 평가셋 읽기와 첫 측정

**할 일** — `evalset.json`을 열어 10문항의 `question`·`expected_source`·`keywords`를 훑은 뒤 `uv run python eval.py --evalset evalset.json --top-k 3`을 실행한다.

**예상 결과** — 문항마다 `q01 hit=True rank=1 top=[…]` 형태의 줄이 나오고 마지막에 `hit rate 0.9`처럼 요약과 `저장 → outputs\eval-<시각>.md`가 나온다. Ollama 없이도 돌아간다. 값은 환경에 따라 0.7~1.0 사이 어딘가다.

**확인** — [ ] `outputs/eval-*.md`의 표를 열어 hit이 X이거나 rank가 2 이상인 문항 id를 적었다. 전부 hit이고 전부 1위이면 "없음"이라고 그대로 적는다.

### 단계 2. 조건을 바꿔 두 번 더 측정

**할 일**

```powershell
uv run python eval.py --evalset evalset.json --top-k 1
uv run python eval.py --evalset evalset.json --index outputs/index-150 --top-k 3
```

**예상 결과** — top-k 1의 hit rate는 top-k 3보다 같거나 낮다(rank 2·3이던 문항이 X로 바뀐다). 150자 인덱스는 문항에 따라 오르거나 내린다. 결과 파일이 3건이 된다.

**확인** — [ ] 세 조건의 hit rate를 한 표에 놓고 조건에 따라 hit이 바뀐 문항 id를 적었다.

### 단계 3. 실패 문항의 원인 찾기

**할 일** — 실패(또는 순위가 낮은) 문항 하나를 고르고 `uv run python search.py --query "<그 문항의 question>" --top-k 5`를 실행한다. `outputs/index.json`에서 기대 출처 파일의 청크 본문도 읽는다.

**예상 결과** — 기대 출처의 청크가 4~5위에 있거나(top-k 부족), 정답 문장이 두 청크에 나뉘어 있거나(chunk 경계), 질문의 낱말이 문서에 없고 다른 표현으로 적혀 있다(용어 불일치). 1위 청크는 질문의 낱말과 겹치는 다른 문서인 경우가 많다.

**확인** — [ ] 원인을 세 유형 중 하나로 분류하고 근거 문장을 적었다. 두 번째 문항도 같은 절차로 분류했다.

### 단계 4. 개선 시도와 생성 포함 평가

**할 일**

1. 문항마다 개선안 하나를 실제로 시도한다(예: 150자 인덱스로 재검색, `--top-k 5`, `docs/`의 해당 문단을 한 문장 보강 후 `chunk.py`·`embed.py` 재실행). 시도 전후의 순위를 적는다.
2. `uv run python eval.py --evalset evalset.json --ids q05,q10 --generate`를 실행한다.

**예상 결과** — 1에서 순위가 오르거나 그대로다(그대로면 원인 분류를 다시 본다). 2에서는 문항마다 `q05 hit=True keyword=True source=True refused=False` 형태의 줄이 나오고 요약에 `keyword`·`source` 비율이 붙는다. 한 문항에 수 초~수십 초가 걸린다.

**확인** — [ ] 질문을 문서 표현으로 바꾸는 방법은 쓰지 않았다. `--generate` 결과의 세 필드를 기록했다.

### 단계 5. 2차 종합과제 점검

**할 일** — [`../week08_midterm/assignment_brief.md`](../week08_midterm/assignment_brief.md)의 "제출 전 검사" 목록을 열어 자기 저장소 기준으로 하나씩 표시하고, 비어 있는 항목과 다음 수업 전까지 채울 계획을 `eval_note.md`에 적는다.

**예상 결과** — `pyproject.toml`·`.env.example`·`.gitignore`·`evalset.json`은 이미 있고, 자기 문서 10개·`SOURCES.md` 확장·README 재현 절차·실패 사례 2건 정리·`uv.lock`이 남은 항목으로 드러난다.

**확인** — [ ] [`lab.md`](lab.md) 3교시 완료 조건을 모두 표시했다. `git status`에 `.env`·`outputs/`가 없다. 실습 30분 뒤 휴식 10분. 이번 주 종료.

---

## 문제가 생겼을 때

| 증상 | 이 문서에서 돌아갈 단계 |
|---|---|
| `uv sync`가 실패한다 | 1교시 단계 1 (네트워크·uv 캐시 확인. 수업 전 sync 여부, `pip install` 금지) |
| 임베딩 모델을 불러올 수 없다 | 1교시 단계 3 (`.env`의 `HF_EMBED_MODEL`, `HF_HUB_OFFLINE=1`, `--backend ollama`) |
| `search.py`가 "인덱스 모델과 현재 설정이 다르다"고 한다 | 1교시 단계 3 (`.env`를 되돌리거나 `embed.py` 재실행) |
| 점수가 전부 비슷해 차이가 안 보인다 | 1교시 단계 4 (절대값 대신 순위와 1·2위 차이, 본문 확인) |
| "파일이 없다: outputs\…"가 나온다 | 1교시 단계 2~3 (chunk → embed 순서로 앞 단계 실행) |
| Ollama 연결 실패·모델 없음 | 2교시 단계 1 (`ollama list`, `.env`의 `OLLAMA_HOST`·`OLLAMA_MODEL` 이름 일치) |
| 답에 `[출처: …]`가 없다 | 2교시 단계 2 (`--temperature 0` 재실행. 그래도 없으면 형식 위반으로 기록) |
| 자료 밖 질문에 거부하지 않는다 | 2교시 단계 4 (검색된 청크 본문 확인 → 환각으로 분류·기록) |
| 답 앞에 생각 텍스트가 섞인다 | 2교시 단계 2 (요청 JSON의 `think:false` 확인. `ollama run`은 섞일 수 있음) |
| "인덱스에 없는 기대 출처" 경고 | 3교시 단계 1 (`evalset.json`의 파일명과 `docs/` 대조, 문서 변경 후 재인덱스) |
| hit rate가 1.0이라 실패가 없다 | 3교시 단계 2~3 (top-k 1·150자 조건의 실패 문항 → 그래도 전부 1위면 `--top-k 5`로 1위와 다른 파일 첫 청크의 점수 차가 가장 작은 문항 2개) |
| `--generate`가 너무 느리다 | 3교시 단계 4 (`--ids`로 2문항, 소형 모델로 전환) |

세부 판정 기준과 힌트는 [`lab.md`](lab.md)에 있다. 정답과 해설은 실습이 끝난 뒤 강의자가 별도로 안내한다.
