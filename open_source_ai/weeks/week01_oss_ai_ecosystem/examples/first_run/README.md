# first_run — 첫 uv 실행

3주차에 uv 프로젝트를 본격적으로 다루기 전에 "복사 → `uv run` → 결과 파일 → commit" 한 바퀴를 돌려 보는 최소 예제다. 실행 방법·관찰 지점·대체 경로는 상위 [`../README.md`](../README.md)가 기준이다.

`pyproject.toml`과 `sysinfo.py`가 있는 **이 폴더로 이동한 뒤** 실행한다. `uv run`은 프로젝트 `.venv`를 만들고 의존성을 맞춘 후 실행하므로 가상환경을 따로 활성화하지 않아도 된다.

```powershell
uv run python sysinfo.py
uv run python sysinfo.py --no-gpu
uv run python sysinfo.py --print
uv run python --version
```

- Python: `requires-python = ">=3.12"`는 허용 범위다. 실행 버전은 [환경 기준표](../../../../../environment_baseline_template.md)를 따르며, 새 Python이 나왔다고 수업 프로젝트를 임의로 바꾸지 않는다.
- 결과: `outputs/sysinfo.json` (OS·CPU·RAM·디스크·GPU·Python·환경변수)
- 설정: `.env.example`을 `.env`로 복사해 `OLLAMA_HOST`, `OLLAMA_MODEL`을 바꾼다. `.env`는 커밋하지 않는다.
- 의존성: `python-dotenv` 하나. 없어도 실행되며 `.env`만 읽지 않는다.
- `uv.lock`은 아직 없다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
- 학생 복사본의 첫 실행은 `uv.lock`을 만든다. `.venv/`·`.env`·`outputs/`는 Git에서 제외하고 `pyproject.toml`·`uv.lock`·`.env.example`은 보관한다.

설치·갱신과 실행 명령 차이는 [uv 사용 가이드](../../../../uv_guide.md), `.gitignore` 확인과 새 clone 재현은 [GitHub 소스 배포 가이드](../../../../github_distribution.md)를 참고한다.
