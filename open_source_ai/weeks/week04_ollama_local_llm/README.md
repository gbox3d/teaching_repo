# 4주차 — Ollama와 로컬 LLM

## 처음 시작하는 순서

1. [Windows 설치와 첫 채팅](windows_setup.md): 설치 파일 다운로드부터 모델 준비, PowerShell에서 직접 대화하기까지 수업 전에 진행한다.
2. [실습지](lab.md): 1교시 터미널 → 2교시 Python 대화 → 3교시 이미지 인식·툴 콜링·Modelfile 순서로 진행한다.

## 이번 주 질문

> 공개된 오픈소스 모델을 내 PC에서 돌리고, 내 Python 프로그램에서 가져다 쓰려면 무엇이 필요한가?

이번 주는 모델이나 서버를 만드는 주가 아니다. 오픈소스 실행기 **Ollama**(MIT)와 오픈 가중치 모델 **Qwen3.5 2B**(Apache-2.0), 공식 Python 라이브러리 **`ollama`**를 그대로 가져다 쓴다.

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. `ollama show`·`ollama run --verbose`·`ollama ps`로 모델의 파라미터 수, 양자화, 기능(Capabilities), 속도, 메모리 사용량을 읽는다.
2. `ollama.chat()`으로 질문하고 system·user·assistant 메시지의 역할을 설명한다.
3. `stream`, `temperature`, 대화 기억(메시지 쌓기)이 답에 주는 영향을 같은 질문으로 비교한다.
4. 이미지를 함께 보내 VLM에게 그림 속 내용을 묻는다.
5. 툴 콜링으로 모델이 혼자 못 하는 일(현재 시각, 정확한 계산)을 Python 함수에 맡기고, 함수를 실행하는 쪽이 내 프로그램임을 설명한다.
6. Modelfile로 시스템 프롬프트가 들어간 내 도우미 모델을 만들고 기준 모델과 비교한다.

## 누적 결과물

이번 주는 1장(1~4주)을 마무리하는 **1차 종합과제** 주차다. 2주차의 협업 저장소와 3주차의 uv 프로젝트 위에 이번 주 예제를 바탕으로 한 대화·이미지·툴 콜링 기능, 실습 보고서(`week04_report.md`), `Modelfile`이 얹혀 1차 과제 저장소가 완성된다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 모델은 어떻게 실행되는가 — 가중치·토크나이저·컨텍스트, 양자화와 크기, Ollama 구조(서버·CLI·Python 라이브러리·Modelfile) | 터미널에서 모델 실행하고 숫자 읽기 — `ollama show`·`run --think=false`·`/set verbose`·`ps` | 보고서 1절(숫자표) |
| 2교시 | Python 라이브러리로 대화하기 — `ollama.chat()`, 메시지 역할, `stream`, `temperature`, 기억은 메시지 쌓기 | `ex01_hello.py` ~ `ex05_memory.py` 실행하고 바꿔 보기 | 내 시스템 프롬프트, 기억 켜기·끄기 비교 |
| 3교시 | 이미지 인식과 툴 콜링, Modelfile, 1차 종합과제 | `ex06_vision.py`·`ex07_tools.py` 실행, 함수 하나 추가, `ollama create` | 내 그림 결과, 내가 추가한 함수의 호출 기록, 내 모델 비교 |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Ollama가 설치되어 있고 `ollama list`에 `qwen3.5:2b`가 보인다. 모델(약 2.7 GB)은 **수업 전에** 받아 둔다. 여러 PC가 같은 네트워크에서 동시에 받지 않도록 조교가 시간을 나눈다.
- uv, VS Code, PowerShell. 예제 의존성은 `ollama` 하나이며 수업 전 `uv sync`로 받아 둔다.
- GPU가 없어도 된다. 2B 모델은 CPU에서도 느리지만 동작한다. `ollama ps`의 PROCESSOR로 어디서 도는지 확인한다.
- 실명·개인정보를 보고서와 대화에 넣지 않는다. 표시 이름은 `student01` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 확장
- [실행 예제](examples/README.md): `period1`(명령만) → `period2`(`ex01`~`ex05`) → `period3`(`ex06`·`ex07`·`Modelfile`)
- [따라하기 절차](walkthrough.md): 시연·실습을 단계대로 재현하는 절차서
- 강의 대본: 강의자 별도 관리(비공개)
- [1차 종합과제 안내](assignment_brief.md) · [1차 종합과제 루브릭](assignment_rubric.md)

## 완료 기준

- [ ] `ollama show`·`/set verbose`·`ollama ps`에서 파라미터 수, 양자화, Capabilities, eval rate, SIZE, PROCESSOR를 옮겨 적었다.
- [ ] `ex02_system_prompt.py`에 내 역할을 추가하고 답의 차이를 적었다.
- [ ] temperature 0과 1의 차이, 기억 켜기·끄기의 차이를 같은 질문으로 비교했다.
- [ ] 예제 그림과 내 그림으로 이미지 인식 결과를 적었다.
- [ ] `ex07_tools.py`에 함수를 하나 추가하고 모델이 그 함수를 부른 기록을 남겼다.
- [ ] `ollama create`로 내 모델을 만들고 기준 모델과 답을 비교했다.

## 제출 증거

이번 주는 1차 종합과제 주차다. 아래 증거를 개인 저장소에 누적하고, 과제 제출은 [1차 종합과제 안내](assignment_brief.md)를 따른다.

1. `week04_report.md`(1~3절)
2. 내 역할을 추가한 `ex02_system_prompt.py`, 내 함수를 추가한 `ex07_tools.py`
3. 팀명을 넣은 `Modelfile`

## 다음 주 연결

5주차 `week05_huggingface_hub`에서는 Ollama 라이브러리 밖의 Hugging Face Hub에서 모델과 데이터를 찾고, 모델 카드와 라이선스를 읽어 "정말 내 프로젝트에 쓸 수 있는 것인지"를 판단한다. 이번 주에 `ollama show --license`로 본 라이선스가 그 출발점이다.

## 참고 자료

- [Ollama 공식 문서](https://docs.ollama.com/)
- [Ollama Python 라이브러리](https://github.com/ollama/ollama-python)
- [Ollama 이미지 입력(Vision)](https://docs.ollama.com/capabilities/vision)
- [Ollama 툴 콜링](https://docs.ollama.com/capabilities/tool-calling)
- [Ollama Modelfile 문서](https://docs.ollama.com/modelfile)
- [Qwen3.5 모델 페이지](https://ollama.com/library/qwen3.5)
