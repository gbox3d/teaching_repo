# 2교시 실습 5–13분 — greet까지
[실습 문제 1](../../../lab.md#문제-1--greet-서브커맨드와-엔트리포인트)에 대응한다.
이 폴더는 greet까지 작성했을 때의 독립 참조 프로젝트다. sysinfo·설정 로더는 아직 없다.

개인 복사본의 이 폴더(`pyproject.toml` 옆)에서:
```text
uv sync
uv run oss-tool greet --name student01
uv run oss-tool --help
```
첫 명령은 환경 준비, 다음은 `안녕하세요, student01.`이 포함된 인사말이다.
`--help`에는 `greet`만 보인다. `--name student02`로 바꾸면 이름만 달라진다.
13분부터는 [period2의 src](../src/oss_tool/cli.py)를 보고 자기 코드에 sysinfo를 추가한다.
원본 lock은 기준 PC에서 생성하므로 첫 실행은 `uv sync`, 배포 lock이 있으면 `--locked`를 사용한다.
