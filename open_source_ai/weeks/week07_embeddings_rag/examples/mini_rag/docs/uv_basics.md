# uv로 재현 가능한 Python 프로젝트 만들기

uv는 Python 설치, 가상환경 생성, 의존성 관리, lock 파일 생성을 한 도구로 처리한다. 프로젝트는 `uv init`으로 시작하고 `uv add httpx`처럼 패키지를 추가하면 `pyproject.toml`에 의존성이 기록된다.

`uv lock`은 실제로 설치될 모든 패키지의 정확한 버전과 해시를 `uv.lock`에 고정한다. 다른 PC에서는 `uv sync --frozen`을 실행하면 lock 파일 그대로 같은 환경이 재현된다. 그래서 `pyproject.toml`과 `uv.lock`은 반드시 커밋한다.

반대로 `.venv` 폴더는 PC마다 다시 만들 수 있고 용량이 크므로 `.gitignore`에 넣고 커밋하지 않는다. 스크립트는 `uv run python script.py`로 실행하면 가상환경을 따로 활성화하지 않아도 된다.

전역 `pip install`은 프로젝트마다 다른 버전 요구를 한 곳에 섞어 버리므로 이 수업에서는 사용하지 않는다.
