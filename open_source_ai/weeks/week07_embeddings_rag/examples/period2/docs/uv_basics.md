# uv로 재현 가능한 Python 프로젝트 만들기

uv는 Python 설치, 가상환경 생성, 의존성 관리, lock 파일 생성을 한 도구로 처리한다. 프로젝트는 `uv init`으로 시작하고 `uv add httpx`처럼 패키지를 추가하면 `pyproject.toml`에 의존성이 기록된다.

`uv lock`은 의존성을 해석한 패키지 버전과 해시를 `uv.lock`에 기록한다. 다른 PC에서는 `uv sync --locked`로 선언과 lock의 일치를 검사하고 해당 PC에 맞는 패키지를 설치한다. 그래서 `pyproject.toml`과 `uv.lock`은 반드시 커밋한다. Python 선택은 `.python-version`에, GPU·모델 조건은 환경 기준표에 따로 기록한다.

반대로 `.venv` 폴더는 PC마다 다시 만들 수 있고 용량이 크므로 `.gitignore`에 넣고 커밋하지 않는다. 스크립트는 `uv run python script.py`로 실행하면 가상환경을 따로 활성화하지 않아도 된다.

의존성은 `uv add`로 추가한다. 배포 검증에서는 `uv run --locked python script.py`로 실행 중 lock 변경을 막는다. uv 자체 업데이트, Python 설치, 프로젝트 패키지 업데이트는 각각 별도 작업이다.
