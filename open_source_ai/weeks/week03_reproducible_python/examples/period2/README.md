# 2교시 — greet 다음 sysinfo

[실습지 2교시](../../lab.md#2교시-실습--oss-tool-cli-완성하기)의 **기본 문제 참조본**이다.
기존 개인 저장소를 이어서 편집한다. 교재 참조본을 통째로 덮어쓰지 않는다.

| 실습 시간·단계 | 지금 열 파일 | 이때 있는 기능 |
|---|---|---|
| 5–13분 · 문제 1 | [step1_greet/src/oss_tool/cli.py](step1_greet/src/oss_tool/cli.py), [pyproject.toml](pyproject.toml) | greet 하나 |
| 13–21분 · 문제 2 | [src/oss_tool/cli.py](src/oss_tool/cli.py), [sysinfo.py](src/oss_tool/sysinfo.py) | greet + sysinfo |
| 21–25분 · 실패/README | [pyproject.toml](pyproject.toml) | 엔트리포인트 오타 관찰·복구 |

`step1_greet`는 문제 1 완료 시점의 독립 프로젝트다. 문제 2까지 한 뒤에는 이 폴더 루트가 비교 대상이다.
`sysinfo.py`는 1주차 수집 함수를 옮겨 둔 제공 모듈이다. 이번 시간에는 `collect()` 결과를 CLI에 연결하는 부분을 본다.
설정 로더·HTTP 요청·`config`·`--ping`은 아직 없다. `--verbose`·`--version`은 실습지의 선택 확장으로 직접 추가한다.

참조본을 교재 밖에 복사했다면 `pyproject.toml` 옆에서:
```text
uv sync
uv run oss-tool greet --name student01
uv run oss-tool sysinfo --json
```
인사말에 `student01`이 보이고 JSON의 `os`·`python`·`gpu`가 출력된다.
`outputs/sysinfo-*.json`에 결과가 저장되고 저장 안내는 stderr다. GPU가 없으면 `available: false`가 정상이다.
실습 배포 lock이 있으면 위 명령에 `--locked`를 붙인다. 네트워크 없이 실행하려면 Python·httpx·hatchling을 사전에 캐시한다.
다음 [3교시](../period3/README.md)는 이 코드에 설정 기능만 더한다.

## 실습 시간표

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 상태 확인, 예상표(명령 이름·패키지 이름·실패 시점) |
| greet 서브커맨드 | 5–13분 | `src/oss_tool/` 뼈대, `[project.scripts]`·빌드 백엔드, `uv sync`, greet 실행 |
| sysinfo 서브커맨드 | 13–21분 | `sysinfo.py` 모듈 배치, `--json`, `outputs/` 저장, logging은 stderr |
| 실패 경로·README | 21–25분 | 엔트리포인트 오타 재현·복구, README 실행 절차 3줄 |
| 검증·기록 | 25–30분 | `--help`·파이프 확인, 오류 줄 기록, commit·push |

시간은 설명·시연 20분 뒤 시작하는 **실습 30분 기준**이다. 휴식 10분은 별도다.
