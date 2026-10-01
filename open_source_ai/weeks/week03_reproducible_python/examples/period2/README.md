# 2교시 — greet 다음 sysinfo

[실습지 2교시](../../lab.md#2교시-실습--oss-tool-cli-완성하기)의 **기본 문제 참조본**이다.
기존 개인 저장소를 이어서 편집한다. 교재 참조본을 통째로 덮어쓰지 않는다.

| 실습 시간·단계 | 지금 열 파일 | 이때 있는 기능 |
|---|---|---|
| 5–13분 · 문제 1 | [아래 greet 시작 코드](#문제-1--greet만-작성하기), [pyproject.toml](pyproject.toml) | greet 하나 |
| 13–21분 · 문제 2 | [src/oss_tool/cli.py](src/oss_tool/cli.py), [sysinfo.py](src/oss_tool/sysinfo.py) | greet + sysinfo |
| 21–25분 · 실패/README | [pyproject.toml](pyproject.toml) | 엔트리포인트 오타 관찰·복구 |

2교시의 예제 프로젝트는 `period2` 하나다. 실습은 1교시에 만든 개인 프로젝트에서 같은 `src/oss_tool/cli.py`를 이어서 편집한다.
이 폴더의 `src/`는 문제 2까지 완료한 참조 코드이며, 문제 1의 시작 코드는 아래에 따로 제시한다.
`sysinfo.py`는 1주차 수집 함수를 옮겨 둔 제공 모듈이다. 이번 시간에는 `collect()` 결과를 CLI에 연결하는 부분을 본다.
설정 로더·HTTP 요청·`config`·`--ping`은 아직 없다. `--verbose`·`--version`은 실습지의 선택 확장으로 직접 추가한다.

## 문제 1 · greet만 작성하기

**5–13분:** 개인 프로젝트 `C:\classwork\osa-practice`에서 `src/oss_tool/__init__.py`에 `__version__ = "0.1.0"`을 적고,
처음 만드는 `src/oss_tool/cli.py`를 아래 코드와 비교한다.

```python
import argparse
import sys

from oss_tool import __version__


def cmd_greet(args):
    print(f"안녕하세요, {args.name}. oss-tool {__version__} 입니다.")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="oss-tool")
    sub = parser.add_subparsers(dest="command", required=True)
    greet = sub.add_parser("greet", help="인사말 출력")
    greet.add_argument("--name", default="student01")
    greet.set_defaults(func=cmd_greet)
    return parser


def main():
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
```

[실습지 문제 1](../../lab.md#문제-1--greet-서브커맨드와-엔트리포인트)의 `[project.scripts]`, `[build-system]`,
`[tool.hatch.build.targets.wheel]` 세 블록을 개인 `pyproject.toml`에 추가한 뒤, 그 파일이 있는 프로젝트 루트에서 실행한다.

```powershell
Set-Location C:\classwork\osa-practice
uv sync
uv run oss-tool greet --name student01
uv run oss-tool --help
```

이름이 들어간 인사말이 출력되고, 이 단계의 `--help`에는 `greet`만 보인다.

## 문제 2 · 같은 CLI에 sysinfo 추가하기

**13–21분:** 같은 개인 프로젝트에 [sysinfo.py](src/oss_tool/sysinfo.py)를 추가하고,
[cli.py 참조본](src/oss_tool/cli.py)과 비교해 `sysinfo` 서브커맨드·JSON 저장·logging을 연결한다.
실행 위치는 계속 개인 프로젝트 루트다.

```text
uv run oss-tool greet --name student01
uv run oss-tool sysinfo --json
```

문제 2 완료 참조본을 따로 실행해 비교하려면, 교재 밖에 복사한 `period2`의 `pyproject.toml` 옆에서:
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
