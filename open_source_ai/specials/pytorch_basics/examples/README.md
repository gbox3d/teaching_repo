# PyTorch 특강 실행 예제

한 uv 프로젝트의 루트에서 실행한다. 의존성은 torch와 NumPy이며 모델 다운로드 없이 CPU로 진행한다.

| 교시 | 소스 | 명령 |
|---|---|---|
| 1 | [텐서 연산](src/ex01_tensors/__init__.py), [텐서 불러오기](src/ex02_save_load/__init__.py) | `uv run ex01`, `uv run ex02` |
| 2 | [회귀 학습](src/ex03_train/__init__.py), [CSV](src/shared/data/study_scores.csv) | `uv run ex03` |
| 3 | [모델 불러오기·예측](src/ex04_predict/__init__.py) | `uv run ex04` |

`src/<모듈>/__init__.py`의 `main()`을 scripts가 연결한다. `uv_build`는 패키지 설치 방법이며 scripts 수정 뒤에는 `uv sync`를 다시 실행한다. 경로·데이터·예측 입력은 [shared](src/shared/__init__.py)에서 공유한다.

빈 줄은 건너뛰고 `/bye`로 종료한다. ex01은 숫자 두 개, ex02는 저장한 파일 경로, ex03·ex04는 0 이상의 공부 시간을 받는다. 저장 파일은 프로젝트 루트의 `outputs/`에 생긴다. 다른 폴더에서 실행하면 상대 경로도 달라지므로 같은 루트에서 진행한다.

[1교시 상세](period1/README.md) · [2교시](period2/README.md) · [3교시](period3/README.md) · [추가 참고](torch_lab/README.md)
