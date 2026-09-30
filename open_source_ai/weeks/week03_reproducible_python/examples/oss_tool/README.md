# oss-tool — 3주차 예제 프로젝트

이 폴더는 선택 확장을 포함한 **기존 통합 참조본**이다. 기본 실습은 [교시별 예제](../README.md)의 period1 → period2 → period3를 사용한다.


3주차 교재의 참조 구현이다. 파일 설명, 관찰 지점, 대체 경로는 [상위 README](../README.md)에 있다.

## 실행

이 폴더(`pyproject.toml`이 있는 `oss_tool/`)에서 실행한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)에 있다.

1. `uv sync` — 사전 설치. 현재 배포 예제에는 lock이 없어 새 `uv.lock`·`.venv/`가 만들어지고 `oss-tool` 명령이 설치된다.
2. `uv run oss-tool greet --name student01`
3. `uv run oss-tool sysinfo --json` — 결과는 `outputs/`에도 저장된다.

`uv run`도 필요한 환경을 자동 준비하므로 activate와 사전 `uv sync`가 필수는 아니다. 위 sync는 수업 전 캐시를 위한 단계다.

`uv run oss-tool --help`로 서브커맨드 목록을, `uv run oss-tool config`로 현재 설정과 출처를 본다.

## 설정

`Copy-Item .env.example .env` 뒤 값을 바꾼다. `.env`는 커밋하지 않는다.

## uv.lock

이 폴더에는 `uv.lock`을 두지 않았다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다. 그 배포본을 clone한 사람은 `uv sync --locked` → `uv run --locked oss-tool greet --name student01`로 검증한다. `--locked`가 실패하면 lock 누락·변경 원인을 먼저 확인한다. `--frozen`은 선언과 lock의 일치 검사를 생략하므로 오류를 피하는 대안으로 쓰지 않는다.

`pyproject.toml`, `uv.lock`, `.python-version`(사용 시), 소스, `.env.example`은 공유하고 `.venv/`, `.env`, `outputs/`, 캐시는 제외한다. 이미 추적된 파일에는 `.gitignore`만 추가해도 적용되지 않으므로 push 전에 `git diff --cached`와 `git ls-files`를 확인한다.
