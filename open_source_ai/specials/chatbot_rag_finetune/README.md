# 특강: 기말 챗봇 개선(평가·RAG·파인튜닝)

14주차 원광대학교 소개 챗봇을 학생이 스스로 채점하면서 고치는 특강이다. 과제 규칙은 14주차와 같고 어떤 방법을 쓸지는 학생이 고른다. 이 특강은 교과서처럼 방법별 예제를 모두 제공한다. 내 평가 문항, 임베딩 RAG, 7주차 방식의 0.5B LoRA 학습, 학습한 모델과 RAG를 합친 챗봇, 추론 점검(`ex07`)이다.

## 목표

- 공개 20문항 밖의 내 평가 문항을 만들고, 채점 결과를 실패 종류별로 나눠 전체 평균에서 빠진 점수가 가장 큰 종류 하나를 고칠 계획을 세운다.
- 낱말 겹침 검색을 bge-m3 임베딩 검색으로 바꾸고, 정답 문서가 검색 결과에 들었는지 문항 세트 전체에서 확인한다.
- 챗봇이 실제로 보내는 메시지로 학습 예시를 만들어 Qwen2.5-0.5B-Instruct를 7주차 절차로 학습하고, GGUF로 바꿔 Ollama에 등록한 뒤 같은 채점기로 잰다.
- 학습은 됐는데 답이 이상할 때 템플릿, 생성 설정, 컨텍스트, 출력 형식 중 어디가 원인인지 좁힌다.

## 네 교시 흐름

| 교시 | 주제 | 예제 | 안내 |
|---|---|---|---|
| 1 | 내 평가 문항과 실패 분류 | `ex04` 내 평가(공개 20문항과 같은 채점기) | [1교시](examples/period1/README.md) |
| 2 | 임베딩 RAG와 검색 관찰 | `rag_bot`, `ex05` 검색 관찰 | [2교시](examples/period2/README.md) |
| 3 | 학습 예시와 LoRA 학습·등록 | `ex06` 학습 예시, `finetune/`의 학습·병합·등록 | [3교시](examples/period3/README.md) |
| 4 | 추론 버그 잡기 | `ex07` 추론 점검, 버그 심기 | [4교시](examples/period4/README.md), [추론 버그 잡기](examples/debugging.md) |

교시마다 설명 20분, 실습 30분, 휴식 10분이다. 30분 실습은 [실습지](lab.md)에, 수업 전 준비와 학습·변환·등록 명령은 [따라하기](walkthrough.md)에 있다.

## 폴더 구성

```text
chatbot_rag_finetune/
├─ README.md, lab.md, walkthrough.md
├─ slides.md, slides_en.md
├─ examples/              uv 프로젝트. 14주차 프로젝트(채점기·기준 봇·참고 자료)를 path 의존성으로 쓴다
│  ├─ period1/ ~ period4/ 교시별 안내
│  ├─ debugging.md        추론 버그 잡기: 증상별 확인할 값, 버그 심기 실습
│  ├─ src/rag_bot/        임베딩 RAG 봇(bge-m3 검색 + 14주차와 같은 응답 계약)
│  ├─ src/lab_shared/     문항 세트 읽기, 평가 워커
│  │  └─ data/            예시 문항(내 평가 문항, 학습 문항)과 작성 규칙
│  ├─ src/ex04_my_eval/   내 평가 문항과 공개 20문항 채점, 실패 종류별 잃은 점수
│  ├─ src/ex05_search/    정답의 근거 문서가 검색 결과에 들었는지 확인
│  ├─ src/ex06_make_sft/  rag_bot이 보낼 대화로 학습 예시 만들기
│  ├─ src/ex07_inspect/   봇의 Ollama 요청과 응답을 보며 추론 설정·컨텍스트·형식 점검
│  └─ tests/              Ollama 없이 도는 시험
├─ finetune/              uv 프로젝트. 7주차와 같은 torch·transformers·peft 버전
│  ├─ src/                prepare(기본 모델 받기), ft01(LoRA 학습), ft02(병합)
│  ├─ Modelfile.base, Modelfile.lora
│  └─ tools/llama.cpp/    GGUF 변환기. 내려받아 쓰고 커밋하지 않는다
└─ outputs/sft/           ex06이 만든 학습 파일. 커밋하지 않는다
```

공개하는 학습 데이터는 `lab_shared/data`의 학습 문항 40건(v0)뿐이다. 학습 문항은 질문·정답 JSON이고, 학습 예시는 `ex06`이 학습 문항으로 만든 대화(`outputs/sft/train.jsonl`)다. 학습 데이터를 늘리고 다듬는 일은 학생의 과업으로 남긴다. 설정을 정하려고 쓴 늘린 학습 데이터는 강의자가 별도로 관리한다(비공개).

명령 이름은 14주차와 겹치지 않게 `ex04`부터 쓴다. `examples/`의 가상 환경에는 14주차 명령(`ex01`~`ex03`, `evaluate`)도 함께 설치되므로, 이 폴더에서 `uv run ex02`를 실행하면 14주차 공식 공개 평가가 그대로 돈다.

`examples/`는 14주차 폴더를 상대 경로로 가리키므로 저장소 전체를 clone한 위치에서 실행한다. 과제 제출용 챗봇은 학생이 따로 복사한 14주차 예제 폴더(개인 사본)에서 고친다. 이 특강이 부르는 `student_bot`은 저장소 14주차의 기준 봇이며 학생이 고친 사본이 아니다.

## 시험

`examples/`에서 실행한다. Ollama 없이 돈다.

```powershell
uv run python -B -m unittest discover -s tests
uv run python -B -m unittest tests.test_my_data -v
```

첫 줄은 전체 시험이고, 둘째 줄은 예시 문항 파일만 검사한다. 내 문항을 고친 뒤에는 둘째 줄로 형식과 규칙을 먼저 확인한다.

## 과제로 옮기기

특강에서 고친 것을 과제 폴더(14주차 예제의 개인 사본)로 옮기는 방법이다.

- 임베딩 RAG: `rag_bot/__init__.py`는 14주차 `shared`만 쓴다. 내용을 과제 폴더의 `student_bot/__init__.py`에 그대로 옮기면 같은 계약으로 돈다. `bge-m3`가 필요하다.
- 내 평가: `lab_shared`와 `ex04_my_eval` 두 폴더를 과제 폴더의 `src/`에 복사하고, `pyproject.toml`의 `[project.scripts]`에 `ex04` 한 줄을, `module-name`에 `lab_shared`·`ex04_my_eval` 두 이름을 더한 뒤 `uv sync`를 다시 실행한다. 자세한 순서는 [1교시 안내](examples/period1/README.md#과제-폴더로-옮기기)에 있다.
- 추론 점검: `src/ex07_inspect`를 과제 폴더의 `src/`에 복사하고 `[project.scripts]`에 `ex07` 줄을, `module-name` 목록에 `"ex07_inspect"`를 더한 뒤 `uv sync`를 다시 실행한다. 과제 폴더에서는 `BOT = "student_bot"`을 그대로 둔다. 자세한 순서는 [추론 버그 잡기](examples/debugging.md#과제-폴더에서-ex07-쓰기)에 있다.
- 학습한 모델: 먼저 임베딩 RAG를 옮겨 과제 폴더의 `student_bot`이 `rag_bot`과 같은 검색을 하게 한다. `EMBED_MODEL`·`TOP_K`·`MIN_SCORE`를 학습 때의 `outputs/sft/settings.json` 값과 맞춘 뒤 `MODEL`을 등록한 이름으로 바꾼다. 검색이 다르면 모델은 학습 때와 다른 입력을 받는다. 기본 모델 ID·revision, GGUF와 `Modelfile`, 등록 명령은 14주차 과제 안내의 '제출물' 1번 실행 안내에 적는다. 모델 제출 방법과 모델 규칙은 강좌 공지를 따른다.

## 실행 환경

예제가 쓰는 Ollama 모델은 이름과 digest로 적는다. 생성 `qwen3.5:2b`(`0689d44085e0`)와 임베딩 `bge-m3`(`790764642607`)이다. 어떤 모델을 쓸지는 학생이 고르고, 과제의 모델 규칙은 강좌 공지를 따른다. Ollama 버전은 업데이트로 바뀔 수 있으므로 모델 이름과 digest를 기준으로 삼고 버전은 기록만 한다. 이 문서들의 실측은 Ollama 0.40.17에서 했다.

기준 PC는 Windows 11, RTX 5060 8GB다. 예제는 이 PC(8GB)에서 도는 설정만 쓴다.

## 완료 기준

- 기록표에 1교시 `student_bot`(`public`, `mine`, 같은 설정으로 다시 잰 줄), 2교시 `rag_bot`(기본값과 바꾼 설정), 3교시 `wku-lora`와 `wku-base` 줄이 있다. 2교시와 3교시는 설정이나 모델마다 `mine`·`public` 두 줄이다.
- 가장 큰 감점 종류의 원인 가설과 다음에 바꿀 것 하나를 적었다.
- 평가 문항(공개 20문항, 내 문항)을 학습 데이터에 넣지 않았다.
- 4교시에 실패한 문항 하나의 [5] status, [6]의 증상(없으면 '없음'), 확인한 값, 고칠 곳과 기준 봇과의 차이를 적었고, 버그 1의 예상과 관찰을 적은 뒤 `git diff` 출력을 넣기 전 기록과 같게 되돌렸다.

자료: [실습지](lab.md) · [따라하기](walkthrough.md) · [슬라이드](slides.md) · [영문 슬라이드](slides_en.md)
