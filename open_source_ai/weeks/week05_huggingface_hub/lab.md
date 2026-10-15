# 5주차 실습 — 공개 자원을 문서와 해시로 판단하라

## 공통 규칙

- 모델·데이터는 수업 전에 받아 둔다. 실습 중에는 카드·정보 조회와 스트리밍만 네트워크를 쓴다.
- 현재 교시의 [예제 폴더](examples/README.md)를 `$HOME\osa-practice\week05` 아래에 복사해 그 안에서 `uv run exNN`으로 실행한다.
- 실행하기 전에 무엇이 나올지 한 줄로 예상하고, 실행한 뒤 실제 결과와 비교한다.
- 기록은 상위 폴더의 `model_cards.md`(1교시), `pipeline_report.md`(2교시), `SOURCES.md`(3교시)에 남긴다.
- Hugging Face 토큰은 이번 실습에 필요 없다. gated 모델은 카드만 읽고 파일을 받지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week05_huggingface_hub\examples"
$dst = "$HOME\osa-practice\week05"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\model_cards.md")) { Copy-Item "$src\model_cards_template.md" "$dst\model_cards.md" }
if (-not (Test-Path "$dst\SOURCES.md")) { Copy-Item "$src\SOURCES_template.md" "$dst\SOURCES.md" }
```

## 1교시 실습 — 모델 카드 분석표와 캐시 보고

### 상황

팀이 "로컬 AI 도우미"에 쓸 후보 모델 세 개를 골라 왔다. 팀장은 내려받기 전에 "셋 다 우리 프로젝트(공개 저장소, 수업용, 비상업)에 써도 되는지, 디스크는 얼마나 필요한지"를 한 장으로 정리해 달라고 한다.

대상 모델은 `Qwen/Qwen2.5-0.5B-Instruct`, `intfloat/multilingual-e5-small`, 라이선스 제한이 있는 `meta-llama/Llama-3.2-1B-Instruct`다(강의자가 바꿔 지정할 수 있다).

### 준비

```powershell
Copy-Item -Recurse "$src\period1" "$dst\period1"
Set-Location "$dst\period1"
uv sync
```

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 프로젝트 만들기 | 0–4분 | `uv init --package --python 3.12`로 내 프로젝트 만들고 구조 읽기 |
| 예상 | 4–6분 | 세 모델의 라이선스·fp16 용량·한국어 지원 예상 |
| Hub 정보 | 6–12분 | `uv run ex01`에 세 모델 입력 |
| 카드 읽기 | 12–24분 | `uv run ex02`와 브라우저로 분석표 채우기 |
| 캐시·기록 | 24–30분 | `uv run ex03`, 판정 문장 작성 |

### 문제

0. 교재 폴더를 쓰기 전에 같은 구조의 내 프로젝트를 Python 3.12로 만든다.

   ```powershell
   Set-Location $dst
   uv init --package --python 3.12 --vcs none my-hub
   Set-Location my-hub
   uv add huggingface_hub
   uv run my-hub
   Set-Location "$dst\period1"
   ```

   `Hello from my-hub!`가 나오면 성공이다. `.python-version`, `pyproject.toml`의 `[project.scripts]`·`[build-system]`, `src/my_hub/__init__.py`의 `main()`을 열어 보고, 교재 `period1`이 같은 구조라는 것을 확인한다.

1. 카드를 열기 전에 `model_cards.md`의 예상표에 세 모델의 라이선스, fp16 용량(파라미터 수 × 2바이트), 한국어 지원 여부를 예상해 적는다.
2. `uv run ex01`을 실행하고 `모델>`에 세 모델 ID를 차례로 입력한다. license·task·gated·commit·파일 합계를 분석표 4절에 옮긴다. 잘못된 이름(`없는조직/없는모델`)과 없는 저장소(`noorg/nomodel-xyz`)도 입력해 오류 첫 줄을 적고 `/bye`로 끝낸다.
3. `uv run ex02`로 세 모델의 카드를 읽는다. YAML의 `license`·`language`·`pipeline_tag`·`base_model`을 분석표에 옮기고, 본문 절 제목에서 의도된 용도·학습 데이터·한계 절을 찾는다. 절의 내용은 브라우저의 모델 페이지에서 읽고 **절 제목과 함께** 적는다. 없으면 "카드에 없음"이라고 쓴다.
4. 라이선스 이름을 SPDX 식별자로 바꾼다. SPDX 목록에 없는 라이선스(Llama 등)는 `LicenseRef-이름`으로 적고 핵심 조건을 한 줄로 요약한다. Llama 카드의 `extra_gated_prompt`가 무엇인지도 적는다.
5. 모델마다 "우리 프로젝트에 쓸 수 있는가"를 가능/조건부/불가로 판정하고 근거 절을 적는다.
6. `uv run ex03`으로 캐시 위치·총 용량·저장소별 commit hash를 4절에 옮긴다. `ex02`를 실행하기 전과 비교해 무엇이 캐시에 생겼는지 적는다.

완료 조건:

- [ ] 세 모델의 분석표가 채워졌거나 "카드에 없음"으로 표시되었다.
- [ ] 판정 3개에 근거 절이 적혀 있다.
- [ ] `ex01`의 commit과 `ex03`의 캐시 commit이 같은지 확인했다.
- [ ] 없는 저장소가 404가 아니라 401로 나오는 이유를 한 문장으로 적었다.

<details>
<summary>힌트</summary>

- `gated`가 `False`가 아니면(`manual`, `auto`) 약관 동의 뒤에만 파일을 받을 수 있다. 카드(README.md)는 동의 없이 읽힌다.
- YAML의 `license`와 본문·LICENSE 파일이 다르면 본문 쪽이 우선이다. 둘 다 적는다.
- `ex01`의 파일 합계에는 여러 형식(safetensors·onnx 등)의 가중치가 함께 들어 있을 수 있다. 실제로 받는 크기는 그보다 작을 수 있다.
- `uv init` 뒤에 `Adding my-hub as member of workspace`가 나왔다면 교재 폴더 안에서 실행한 것이다. 교재 `pyproject.toml` 끝에 추가된 `[tool.uv.workspace]` 세 줄을 지우고 `$dst`에서 다시 만든다.

</details>

### 확장

- `uv run hf cache ls`를 실행해 `ex03`과 같은 캐시를 보는지 비교한다.
- `ex01`에 다른 모델(예: 한국어 모델) ID를 넣고 같은 표를 하나 더 채운다.

## 2교시 실습 — pipeline으로 분류와 생성 실행하기

### 상황

팀원이 "모델은 받아 놨는데 실제로 돌아가는지, GPU가 CPU보다 얼마나 빠른지, 어떤 버전을 썼는지 기록해 달라"고 한다.

### 준비

```powershell
Copy-Item -Recurse "$src\period2" "$dst\period2"
Set-Location "$dst\period2"
uv sync
```

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 구조 읽기 | 0–4분 | `pyproject.toml`과 `src/shared/__init__.py` 읽기 |
| 분류 | 4–14분 | `uv run ex04`를 자동 장치와 CPU에서 실행 |
| 생성 | 14–22분 | `uv run ex05`, revision 고정 후 재실행 |
| 실패·기록 | 22–30분 | 잘못된 revision 재현, `pipeline_report.md` 작성 |

### 문제

1. `pyproject.toml`과 `src/shared/__init__.py`를 연다. `ex04`·`ex05`가 `shared`에서 무엇을 가져오는지, `shared`가 왜 `[project.scripts]`에는 없고 `module-name`에만 있는지 보고서에 한 줄로 적는다.
2. `uv run ex04`를 실행하고 `문장>`에 다음을 입력한다. 라벨·점수·시간을 표에 적는다.

   ```text
   이 수업은 정말 재미있고 배울 것이 많다.
   설치가 자꾸 실패해서 시간을 다 날렸다.
   모델 카드에는 라이선스와 학습 데이터 항목이 있다.
   The download was slow and the error message was useless.
   /bye
   ```

3. `src/ex04/__init__.py`의 `DEVICE = pick_device()`를 `DEVICE = "cpu"`로 바꿔 같은 문장으로 다시 실행한다. 로드 시간과 문장당 시간을 비교한다. 비교가 끝나면 되돌린다.
4. `uv run ex05`를 실행하고 `공개 모델을 프로젝트에 쓰기 전에 확인할 것을 세 가지만 말해 줘.`를 입력한다. 답과 시간을 적고, 답이 질문에 맞는지 판단한다.
5. 1교시 `ex01`에서 적은 `Qwen/Qwen2.5-0.5B-Instruct`의 commit hash를 `src/shared/__init__.py`의 `TEXT_REVISION`에 넣고 `ex05`를 다시 실행한다. 같은 질문의 답이 같은지 확인한다.
6. 실패 경로: `TEXT_REVISION`을 `"0000000"`으로 바꿔 실행한다. Traceback의 맨 아래 줄(`OSError: 0000000 is not a valid git identifier ...`)이 실제 이유다. 그 줄을 적고, 위쪽 줄들은 어느 함수에서 났는지 보여 주는 경로라는 점을 확인한다. 끝나면 commit hash로 되돌린다.

완료 조건:

- [ ] `pipeline_report.md`에 아래 표가 채워졌다.
- [ ] 한국어와 영어 문장의 점수 차이, 중립 문장의 라벨을 카드의 언어 목록·라벨과 연결해 한 문장으로 설명했다.
- [ ] revision을 고정하는 이유를 3주차 `uv.lock`과 비교해 한 문장으로 적었다.

```text
| 장치 | 예제 | 로드(s, 두 번째 실행) | 문장/답 하나(s) | revision |
|---|---|---:|---:|---|
| 자동(cuda/mps) | ex04 |  |  | main |
| cpu | ex04 |  |  | main |
| 자동 | ex05 |  |  | main |
| 자동 | ex05 |  |  | (commit hash) |
```

<details>
<summary>힌트</summary>

- 첫 실행의 로드 시간에는 다운로드·파일 확인이 섞인다. 두 번째 실행을 기준으로 잰다.
- `do_sample=False`이므로 같은 장치·같은 revision이면 답이 같아야 한다. 장치가 다르면 계산 순서 차이로 달라질 수 있다.
- 라벨이 `LABEL_0`처럼 나오는 모델은 카드나 `config.json`의 `id2label`에서 뜻을 찾는다.

</details>

### 확장

- `src/shared/__init__.py`의 `CLS_MODEL`을 다른 감성 분류 모델로 바꾸고, 1교시처럼 `ex01`로 그 모델의 license부터 확인한 뒤 실행한다.
- `ex05`의 `max_new_tokens`를 30·120·300으로 바꿔 답 시간이 토큰 수에 비례하는지 본다.

## 3교시 실습 — 데이터셋 살펴보기와 출처 기록표

### 상황

10주차 LoRA 학습에 쓸 데이터 후보를 찾는 중이다. 팀장이 "데이터 구조와 라이선스를 먼저 확인하고, 지금까지 쓴 모델·데이터의 출처를 한 표로 만들어 두자"고 한다.

### 준비

```powershell
Copy-Item -Recurse "$src\period3" "$dst\period3"
Set-Location "$dst\period3"
uv sync
```

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 예상 | 0–3분 | `src/shared/data/sample_qa.jsonl`의 필드 구조 예상 |
| 로컬 데이터 | 3–11분 | `uv run ex06`, 키워드 찾기 |
| Hub 데이터 | 11–20분 | `uv run ex07`, 카드 라이선스 비교 |
| 출처 기록 | 20–28분 | `SOURCES.md`에 모델 2개 + 데이터 1개 |
| 정리 | 28–30분 | 조건 요약, commit |

### 문제

1. 파일을 열지 않고 `sample_qa.jsonl`의 필드 이름과 자료형을 예상해 적는다.
2. `uv run ex06`을 실행해 필드·건수·자료형·카드 license를 기록한다. `찾기>`에 `uv`, `라이선스`, `모델`을 입력해 건수를 적고 `/bye`로 끝낸다. `tags`의 자료형이 다른 필드와 왜 다른지 한 문장으로 적는다. `라이선스`의 건수가 데이터 내용(`answer`·`tags`)과 맞는지 보고, 맞지 않으면 `src/ex06/__init__.py`의 `filter` 줄을 읽어 이유를 적는다.
3. `src/shared/__init__.py`에서 데이터 경로가 `Path(__file__).parent / "data"`로 정해진 이유를 한 문장으로 적는다.
4. `uv run ex07`을 실행하고 빈 줄(기본값 `klue/klue ynat`), `klue/klue`(구성 빠짐), `HuggingFaceH4/no_robots`를 차례로 입력한다. 두 데이터셋의 카드 license와 첫 행의 필드를 기록한다. 구성이 빠졌을 때 오류가 알려 준 구성 이름 목록을 적는다.
5. 브라우저에서 두 데이터셋의 Dataset Card를 열어 수집 방법·개인정보 언급·라이선스 절을 찾아 적는다. 없으면 "카드에 없음"이라고 쓴다.
6. `SOURCES.md`에 2교시 모델 2개와 데이터 1개를 적는다. 버전 칸에는 commit hash, 라이선스 칸에는 SPDX 식별자, 용도 칸에는 이번 주의 실제 용도를 쓴다. 조건 요약 절에 출처 표시·같은 조건 공유·상업 이용 제한·gated 여부를 적고 commit한다.

완료 조건:

- [ ] `ex06` 결과에서 `Value`와 `List` 자료형을 각각 하나 이상 기록했다.
- [ ] `cc-by-sa-4.0`과 `cc-by-nc-4.0`이 우리 프로젝트에 주는 조건 차이를 한 문장으로 적었다.
- [ ] `SOURCES.md` 3행 모두 버전 칸이 commit hash(로컬 파일은 파일 해시)이고 "최신"이라는 말이 없다.

<details>
<summary>힌트</summary>

- 스트리밍(`streaming=True`)은 전부 받지 않으므로 전체 건수를 모른다. 앞에서부터 필요한 만큼만 받는다.
- 원문 데이터와 라벨의 라이선스가 다를 수 있다. 둘 다 적고 더 제한적인 쪽으로 조건을 요약한다.
- 모델의 commit hash는 1교시 `ex01`의 `commit` 줄에서 가져온다.

</details>

### 확장

- `sample_qa.jsonl`에 같은 형식의 Q&A 3건을 추가하고(실제 인물·기관 없이) `ex06`의 건수와 `찾기>` 결과가 바뀌는지 확인한다.
- `src/shared/__init__.py`의 `HUB_DATASET`·`HUB_CONFIG`를 다른 공개 데이터셋으로 바꾸고 `ex07`을 빈 줄로 실행한다.

## 제출 체크

- `model_cards.md`: 예상표, 분석표, 판정, Hub 정보와 캐시 보고
- `pipeline_report.md`: 분류 결과, 생성 답, 시간 비교표, revision 고정·실패 결과
- `SOURCES.md`: 모델 2개 + 데이터 1개, 조건 요약
- 개인 저장소: 이번 주 commit 3개 이상, `.venv/`가 commit되지 않았음을 `git status`로 확인
