# Streamlit 실행 예제

한 프로젝트 루트에서 `uv sync`를 마친다. 세 앱은 차례로 실행하고 서버를 바꾸기 전에 Ctrl+C로 종료한다.

| 교시 | 코드 | 명령 |
|---|---|---|
| 1 | [첫 위젯](src/ex01_widgets/app.py) | `uv run ex01` |
| 2 | [채팅](src/ex02_chat/app.py) | `uv run ex02` |
| 3 | [문서 RAG](src/ex03_rag/app.py) | `uv run ex03` |

`src/<모듈>/__init__.py`의 `main()`이 공용 실행 함수를 부르고 Streamlit이 같은 패키지의 `app.py`를 실행한다. scripts는 명령 연결, build-system은 설치 방법이다. 수정 뒤 `uv sync`한다. 모델·검색·서버 실행은 [shared](src/shared/__init__.py)에서 공유한다.

## 수업 전 준비

Ollama의 `qwen3.5:2b`와 Hugging Face 임베딩 모델 `intfloat/multilingual-e5-small`을 준비한다. 6주차의 `bge-m3`(Ollama)와는 다른 모델이다. 임베딩 모델이 없다면 수업 전에 다음 명령으로 캐시한다.

```powershell
uv run prepare
```

임베딩 코드는 캐시만 읽는다. 기본 문서는 [library.txt](src/shared/data/library.txt)이며 실제 기관 정보가 아니다. 문단을 빈 줄로 나누는 작은 텍스트 예제다. 파일 형식·분할을 확장하는 일은 기본 앱이 동작한 뒤 진행한다.

각 앱의 현재 상태는 서버 실행과 브라우저 세션에 속한다. 새 세션에서 장기 기억이 유지된다고 가정하지 않는다.
