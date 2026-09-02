# 3주차 — 재현 가능한 Python 오픈소스 프로젝트

## 이번 주 질문

> 다른 PC에서 내 코드를 같은 결과로 실행하게 만들려면 무엇을 저장소에 넣고 무엇을 빼야 하는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 전역 `pip install`과 "내 PC에서는 됨"이 재현성을 깨뜨리는 이유를 가상환경 개념으로 설명한다.
2. `uv init` → `uv add` → `uv lock` → `uv sync` → `uv run` 흐름으로 프로젝트를 만들고, `pyproject.toml`(의도)과 `uv.lock`(결과)의 역할 차이를 구분한다.
3. 깨끗한 폴더에 clone한 뒤 `uv sync --frozen`으로 같은 환경을 재현하고, `.venv/`가 커밋되지 않았음을 확인한다.
4. src 레이아웃과 `[project.scripts]` 엔트리포인트로 `oss-tool` 명령을 만들고 argparse 서브커맨드와 logging을 붙인다.
5. 설정을 코드에서 분리해 기본값 < `.env` < 환경변수 < 명령 인자 순서로 읽는 설정 로더를 구현한다.
6. 실수로 스테이지된 `.env`를 `git restore --staged`로 되돌리고 Git 이력에 비밀이 남지 않았는지 검사한다.

## 누적 결과물

이번 주 실습은 4주차 **1차 종합과제**(협업 저장소 + Ollama 로컬 API 클라이언트 CLI)의 뼈대를 채운다. 1교시의 uv 프로젝트(`pyproject.toml`·`uv.lock`)와 2교시의 `oss-tool` CLI 구조 위에 4주차의 `chat`·`stream` 서브커맨드가 얹히고, 3교시의 `config.py`·`.env.example`은 1차 과제 루브릭의 재현성·보안 항목에 그대로 쓰인다. 여기서 만든 저장소 골격은 9주차 팀 저장소 템플릿과 14주차 릴리스까지 이어진다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 재현성 실패 사례(전역 pip, 버전 충돌), 가상환경 개념, uv가 맡는 일과 `init/add/lock/sync/run` 흐름, `pyproject.toml`과 `uv.lock`의 관계, 커밋할 것과 뺄 것 | uv 프로젝트를 만들고 깨끗한 폴더에서 재현하기 — `uv init` → `uv add httpx` → commit → clone → `uv sync --frozen`, `uv.lock`이 없을 때의 실패 관찰 | `pyproject.toml`·`uv.lock` commit, 깨끗한 폴더 재현 로그 |
| 2교시 | src 레이아웃과 패키지·모듈, `[project.scripts]` 엔트리포인트, argparse 서브커맨드 설계, `logging` 기본, README의 실행 절차 | oss-tool CLI 완성하기 — `uv run oss-tool greet --name student01`, `uv run oss-tool sysinfo --json`(1주차 sysinfo 재사용), README 실행 절차 3줄 | CLI 실행 출력, `outputs/sysinfo-*.json`, README |
| 3교시 | 설정과 코드의 분리, `.env`와 `.env.example`, python-dotenv와 `os.environ`, 설정 계층(기본값 < `.env` < 환경변수 < 인자), `.gitignore`의 한계와 이미 커밋된 비밀의 위험(토큰 회전) | 설정 로더와 비밀정보 분리 — `config.py` 구현, `.env.example` 작성, `.env`를 실수로 add한 상황 재현 후 `git restore --staged`, `git log`로 이력 검사 | `config.py`, `.env.example`, 이력 검사 결과 문장 |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- 2주차까지 쓴 개인 저장소(GitHub 원격 연결, `LICENSE` 포함)와 1주차의 `sysinfo.py`. 개인 저장소 폴더 이름은 각자 다를 수 있으며 이 주차 문서에서는 `osa-practice`라고 부른다.
- Git, VS Code, uv, PowerShell(PowerShell 7 권장). 전역 `pip install`은 쓰지 않는다.
- 예제 의존성(`httpx`, `python-dotenv`)과 빌드 백엔드(`hatchling`)는 수업 전에 [실행 예제](examples/README.md)의 `uv sync`를 한 번 실행해 캐시해 둔다. 실습 시간에 새 패키지를 내려받지 않는다.
- Ollama 서버는 이번 주 필수가 아니다. 3교시 확장 문제(`config --ping`)에서만 쓴다.
- 정확한 도구 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 실제 토큰, 비밀번호, 개인정보를 `.env`·산출물·공개 저장소에 넣지 않는다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): `oss_tool/` uv 프로젝트(`cli.py`·`sysinfo.py`·`config.py`·`.env.example`)와 깨끗한 폴더 재현 스크립트 `reproduce_check.ps1`, 기록 양식 `week03_notes_template.md`
- [따라하기 절차](walkthrough.md): 시연·실습을 단계대로 재현하는 절차서
- 강의 대본: 강의자 별도 관리(비공개)

## 권장 진행 방식

1. 실습 문제의 완료 조건을 먼저 읽고, 명령을 실행하기 전에 "무엇이 생기고 무엇이 없을지"를 예상표에 적는다.
2. 예제 `examples/oss_tool`은 참조 구현이다. 개인 저장소에 직접 만들다가 막혔을 때만 열어 비교한다.
3. 매 교시 실패·경계 경로(`uv.lock` 없음, 엔트리포인트 오타, `.env` 스테이지)를 한 번씩 재현하고 오류의 첫 줄을 기록한다.
4. `git status`를 commit 직전마다 읽는다. `.venv/`·`.env`·`outputs/`가 보이면 `.gitignore`부터 고친다.
5. 3교시가 끝나면 4주차에서 `config.py`가 그대로 쓰인다는 전제로 `uv run oss-tool config`가 기본값을 출력하는지 마지막으로 확인한다.

## 완료 기준

- [ ] 개인 저장소에 `pyproject.toml`, `uv.lock`, `.python-version`이 commit되어 있고 `git status`에 `.venv/`가 나타나지 않는다.
- [ ] 깨끗한 폴더에 clone해 `uv sync --frozen` → `import httpx`가 성공한 재현 로그(`notes/week03_reproduce.md`)가 있다.
- [ ] `uv.lock`이 없을 때 `uv sync --frozen`이 실패하는 이유를 한 문장으로 적었다.
- [ ] `uv run oss-tool greet --name student01`과 `uv run oss-tool sysinfo --json`이 동작하고 `outputs/sysinfo-*.json`이 생긴다.
- [ ] README에 처음 보는 사람이 복사해 실행할 수 있는 실행 절차 3줄이 있다.
- [ ] `uv run oss-tool config`가 `OLLAMA_HOST`·`OLLAMA_MODEL`의 값과 출처(default/.env/env/arg)를 출력한다.
- [ ] `.env.example`은 commit되고 `.env`는 `.gitignore`로 막혀 있다.
- [ ] `git log`로 검사해 `.env`와 가짜 토큰 문자열이 이력에 없다는 문장을 `notes/week03.md`에 적었다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 개인 저장소에 누적한다.

1. `git log --oneline -5` 결과(uv 프로젝트, CLI, 설정 로더 commit이 보이는지)
2. 재현 로그 요약(clone 위치, `uv sync --frozen` 결과, 확인 명령 출력)과 `uv.lock` 없을 때의 오류 첫 줄
3. `uv run oss-tool greet --name student01`, `uv run oss-tool sysinfo --json`, `uv run oss-tool config` 출력
4. `notes/week03.md`(예상표, 실패 경로 오류 줄 3개, 출처 관찰표, 이력 검사 결과 문장)와 `notes/week03_reproduce.md`(재현 로그)

터미널 출력에는 사용자 홈 경로가 포함될 수 있다. 제출 전에 개인 식별 정보와 토큰이 없는지 확인한다.

## 다음 주 연결

4주차 `week04_ollama_local_llm`에서는 이번 주 `config.py`가 읽는 `OLLAMA_HOST`·`OLLAMA_MODEL`로 실제 로컬 모델을 호출하는 `chat`·`stream` 서브커맨드를 `oss-tool`에 추가한다. 1교시의 `uv sync --frozen` 재현 절차와 3교시의 `.env.example`은 4주차 1차 종합과제의 재현성·보안 항목으로 그대로 평가된다. 다음 수업 전에 기본 모델이 캐시되어 있는지 `ollama list`로 확인한다.

## 참고 자료

- [uv — Working on projects](https://docs.astral.sh/uv/guides/projects/)
- [uv — Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [Python Packaging User Guide — Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [Python 문서 — argparse](https://docs.python.org/3/library/argparse.html)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [GitHub Docs — Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
