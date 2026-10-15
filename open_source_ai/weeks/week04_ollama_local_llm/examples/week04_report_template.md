# 4주차 실습 보고서

- 이름: student01
- 모델: qwen3.5:2b
- PC: (GPU 이름 또는 CPU만)

## 1. 터미널에서 읽은 숫자

| 항목 | 예상 | 실제 |
|---|---|---|
| 파라미터 수 | | |
| 양자화 | | |
| Capabilities | | |
| eval rate (tokens/s) | | |
| `ollama ps` SIZE | | |
| PROCESSOR | | |

- 두 질문의 답이 맞았는가:
- `ollama list` SIZE와 `ollama ps` SIZE가 다른 이유:

## 2. Python에서 대화하기

- `uv init --package --python 3.12`가 만든 파일과 `uv run my-ollama`가 부르는 함수:
- `messages`는 무엇인가:
- `response.message.content`는 무엇인가:
- 내가 만든 시스템 프롬프트와 답:
- stream 과 일반 호출의 차이:
- temperature 0 과 1 의 차이:

| | 보내는 메시지 개수(두 번째 질문) | 색을 맞혔는가 |
|---|---|---|
| 기억 켜기 | | |
| 기억 끄기 | | |

- "모델이 기억한다"의 실제 뜻:

## 3. 이미지 인식, 툴 콜링, 내 도우미 모델

- 예제 그림 결과:
- 내 그림과 질문, 결과:
- 툴 콜링 세 단계를 내 말로:
- 내가 추가한 함수와 `[함수 실행]` 줄:
- 내 모델(`ollama create`)과 기준 모델의 답 비교:
