# 특강 예제: 평가·검색·학습 예시·추론 점검

한 uv 프로젝트에서 내 평가 문항 채점, 임베딩 RAG, 학습 예시 만들기, 추론 점검을 실행한다. 학습·병합·GGUF 변환은 옆 폴더 [finetune](../finetune/README.md)에서 한다.

| 교시 | 안내 | 진입점 | 실행 |
|---|---|---|---|
| 1 | [내 평가 문항과 실패 분류](period1/README.md) | [ex04_my_eval](src/ex04_my_eval/__init__.py) | `uv run ex04` |
| 2 | [임베딩 RAG와 검색 관찰](period2/README.md) | [rag_bot](src/rag_bot/__init__.py), [ex05_search](src/ex05_search/__init__.py) | `uv run ex05` |
| 3 | [학습 예시와 LoRA 학습·등록](period3/README.md) | [ex06_make_sft](src/ex06_make_sft/__init__.py), [finetune](../finetune/README.md) | `uv run ex06` |
| 4 | [추론 버그 잡기](period4/README.md) | [ex07_inspect](src/ex07_inspect/__init__.py) | `uv run ex07` |

명령은 `pyproject.toml`이 있는 이 폴더에서 실행한다. `period1`~`period4`에는 안내만 있으며 교시마다 프로젝트를 복사하지 않는다. 답이 이상할 때 확인할 값은 [추론 버그 잡기](debugging.md)에 있다.

## 설치와 프로젝트 구조

```powershell
uv sync
ollama list
```

`qwen3.5:2b`와 `bge-m3`가 없다면 수업 전에 `ollama pull`로 받는다. 이 프로젝트는 14주차 예제 프로젝트를 `[tool.uv.sources]`의 상대 경로로 설치한다(path 의존성). 14주차의 채점기(`shared.evaluation`), 기준 봇(`student_bot`), 참고 자료(`shared/data`)를 복사하지 않고 그대로 쓰므로, 저장소 전체를 clone한 위치에서 실행한다.

같은 가상 환경에 14주차 명령(`ex01`~`ex03`, `evaluate`)도 함께 설치된다. 그래서 이 특강의 명령은 `ex04`부터 쓴다. 이 폴더에서 `uv run ex02`를 실행하면 14주차 공식 공개 평가가 그대로 돈다.

각 패키지의 `main()`이 명령의 시작점이고, `[project.scripts]`가 명령 이름을 `패키지:main`에 연결한다. `[tool.uv.build-backend]`의 `module-name`에 공용 패키지 `lab_shared`와 봇 패키지 `rag_bot`도 함께 등록했다. scripts나 `module-name`을 바꾸면 `uv sync`를 다시 실행한다.

## 시험

```powershell
uv run python -B -m unittest discover -s tests
```

Ollama 없이 돈다. 예시 문항 파일만 검사할 때는 `uv run python -B -m unittest tests.test_my_data -v`를 실행한다.
