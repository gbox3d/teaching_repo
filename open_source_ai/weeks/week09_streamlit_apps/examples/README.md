# Streamlit 실행 예제

9주차 `examples/` 폴더에서 `uv sync`를 실행한다. 세 앱은 차례로 실행하고 서버를 바꾸기 전에 Ctrl+C로 종료한다.

| 교시 | 코드 | 명령 |
|---|---|---|
| 1 | [첫 위젯](src/ex01_widgets/app.py) | `uv run streamlit run src/ex01_widgets/app.py` |
| 2 | [채팅](src/ex02_chat/app.py) | `uv run streamlit run src/ex02_chat/app.py` |
| 3 | [문서 RAG](src/ex03_rag/app.py) | `uv run streamlit run src/ex03_rag/app.py` |

`uv run`은 프로젝트 환경에서 명령을 실행한다. `streamlit run` 뒤에 지정한 `app.py`가 브라우저에 보이는 화면을 만든다. 채팅과 문서 검색 앱은 [shared](src/shared/__init__.py)의 모델 함수를 함께 사용한다. [Streamlit 공식 실행 안내](https://docs.streamlit.io/develop/concepts/architecture/run-your-app)

## 수업 전 준비

Ollama의 `qwen3.5:2b`와 Hugging Face 임베딩 모델 `intfloat/multilingual-e5-small`을 준비한다. 6주차의 `bge-m3`(Ollama)와는 다른 모델이다. 임베딩 모델이 없다면 수업 전에 다음 명령으로 캐시한다.

```powershell
uv run prepare
```

임베딩 코드는 캐시만 읽는다. 기본 문서는 [library.txt](src/shared/data/library.txt)이며 실제 기관 정보가 아니다. 문단을 빈 줄로 나누는 작은 텍스트 예제다. 파일 형식·분할을 확장하는 일은 기본 앱이 동작한 뒤 진행한다.

각 앱의 현재 상태는 서버 실행과 브라우저 세션에 속한다. 새 세션에서 장기 기억이 유지된다고 가정하지 않는다.

채팅 앱은 이전 메시지를 매 요청에 함께 보낸다. system 지시는 사실만 알려 주면 짧게 확인하고, 수량 질문에는 앞선 정보를 사용한 계산식과 단위를 쓰도록 요청한다. [2교시 안내](period2/README.md)의 세 차례 대화로 이력 전달과 계산의 정확성을 따로 확인한다. 두 AI 앱 모두 본문이 비거나 공백뿐이면 경고를 표시하고 assistant 기록에 넣지 않는다.
