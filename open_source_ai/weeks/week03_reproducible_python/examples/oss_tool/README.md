# oss-tool — 3주차 예제 프로젝트

3주차 교재의 참조 구현이다. 파일 설명, 관찰 지점, 대체 경로는 [상위 README](../README.md)에 있다.

## 실행

1. `uv sync` — 처음 한 번. `.venv/`가 만들어지고 `oss-tool` 명령이 설치된다.
2. `uv run oss-tool greet --name student01`
3. `uv run oss-tool sysinfo --json` — 결과는 `outputs/`에도 저장된다.

`uv run oss-tool --help`로 서브커맨드 목록을, `uv run oss-tool config`로 현재 설정과 출처를 본다.

## 설정

`Copy-Item .env.example .env` 뒤 값을 바꾼다. `.env`는 커밋하지 않는다.

## uv.lock

이 폴더에는 `uv.lock`을 두지 않았다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
