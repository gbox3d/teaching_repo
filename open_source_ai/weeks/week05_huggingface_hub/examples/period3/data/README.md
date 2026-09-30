---
license: cc-by-4.0
language:
  - ko
pretty_name: 오픈소스 AI 응용 수업 Q&A 샘플
size_categories:
  - n<1K
task_categories:
  - question-answering
tags:
  - education
  - korean
---

# Dataset Card — sample_qa.jsonl

교재 예제용으로 직접 작성한 한국어 Q&A 12건이다. 3교시 `dataset_peek.py`의 기본 입력이며, 이 카드는 학생이 Dataset Card의 항목을 실제 파일과 대조하는 연습 대상이다.

## 요약·출처

- 작성 주체: 교재 작성자. 크롤링·외부 데이터 없이 수업 내용(uv, Git, 라이선스, Ollama, Hugging Face)을 바탕으로 작성했다.
- 실제 인물·기관·연락처는 들어 있지 않다.

## 구조

| 필드 | 자료형 | 설명 |
|---|---|---|
| `id` | string | `qa-001` 형식의 고유 번호 |
| `question` | string | 한국어 질문 한 문장 |
| `answer` | string | 두세 문장의 답 |
| `topic` | string | 주제 분류(`uv`, `git`, `license`, `ollama`, `huggingface`, `data`, `env`) |
| `tags` | list of string | 자유 태그 1~3개 |
| `week` | int | 관련 주차 |

- split: `train` 하나, 12행
- 형식: JSON Lines(한 줄에 객체 하나), UTF-8

## 수집·주석 방법

사람이 직접 작성했다. 라벨 지침은 없고 `topic`·`tags`는 작성자가 붙였다. 자동 생성·번역·필터링 단계는 없다.

## 개인정보·민감 정보

없음. 확장 문제로 행을 추가할 때도 실제 인물·기관·연락처를 넣지 않는다.

## 라이선스

CC-BY-4.0. 출처(이 교재)를 표시하면 수정·재배포·상업적 이용이 가능하다.

## 의도된 용도와 한계

- 용도: `datasets` API 연습, 10주차 LoRA 학습 데이터 형식(`jsonl`)의 예시.
- 한계: 12건뿐이라 학습·평가 데이터로 쓰기에는 너무 작다. 답은 교재 기준이며 최신 도구 동작과 다를 수 있다.
