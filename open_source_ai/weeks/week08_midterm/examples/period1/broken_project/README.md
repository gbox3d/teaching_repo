# broken_project — 모의 실기 A 복구 대상

이 폴더는 **일부러 깨진** uv 프로젝트다. 여기서 직접 고치지 말고 `../make_broken_repo.ps1`로 개인 실습 폴더에 복사한 뒤 그곳에서 복구한다.

## 상황 설명

동료가 이 프로젝트를 급하게 커밋해서 넘겼다. 공개 교재 저장소에는 `.env`를 넣을 수 없으므로, "`.env`까지 커밋된 상태"는 `make_broken_repo.ps1`이 재현한다. 스크립트는 다음을 한다.

1. 이 폴더를 지정 위치로 복사한다.
2. 가짜 값이 든 `.env`를 만든다(실제 토큰이 아니다).
3. `git init` 뒤 `.env`를 포함해 모든 파일을 한 commit에 넣는다.

복사본에서 만나게 될 문제:

- `pyproject.toml`에 세 가지 오류가 있다(문법, 테이블 이름, 버전 표기). 어떤 것인지는 `uv sync`와 `uv run`의 메시지가 순서대로 알려 준다.
- `.gitignore`가 없다.
- `.env`가 Git 이력에 들어 있다.
- `.env.example`이 없다.

`report.py` 자체에는 오류가 없다. 설정을 고치면 `uv run python report.py`가 `outputs/report.json`을 만든다.

## 이 폴더에서 하지 않는 것

- 원본에서 `uv sync`를 실행하지 않는다(교재 폴더에 `.venv`가 생긴다).
- 고쳐진 `pyproject.toml`이나 `.gitignore`를 이 폴더에 커밋하지 않는다. 문제가 사라진다.
