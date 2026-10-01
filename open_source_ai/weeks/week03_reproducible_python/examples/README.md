# 3주차 예제 — uv 프로젝트 → CLI → 설정

[실습지](../lab.md)의 순서대로 **지금 교시의 폴더 하나만** 연다.
각 폴더 README의 시간표는 실습지의 실습 30분 시간표와 같다. 설명·시연 20분과 휴식 10분은 별도다.

| 교시 | 예제 폴더 | 지금 볼 파일·자료 | 실습 |
|---|---|---|---|
| 1교시 · uv 프로젝트와 재현 | [period1](period1/README.md) | `pyproject.toml · .gitignore · reproduce_check.ps1` | [실습 1교시](../lab.md#1교시-실습--uv-프로젝트를-만들고-깨끗한-폴더에서-재현하기) |
| 2교시 · greet 다음 sysinfo | [period2](period2/README.md) | README의 greet 시작 코드 → 같은 `src/oss_tool/cli.py`에 sysinfo 추가 | [실습 2교시](../lab.md#2교시-실습--oss-tool-cli-완성하기) |
| 3교시 · 설정 로더와 비밀정보 분리 | [period3](period3/README.md) | `src/oss_tool/config.py · .env.example` | [실습 3교시](../lab.md#3교시-실습--설정-로더와-비밀정보-분리) |

## 사용 순서

1. 실습지의 해당 교시 **준비**부터 진행한다. 예제의 역할(제공 코드·참조 코드·학생용 양식)은 교시 README에 적혀 있다.
2. 파일을 개인 실습 폴더로 복사하거나, 실습지에서 지정한 파일을 자기 코드와 비교한다. 기존 개인 코드·보고서·lock을 통째로 덮어쓰지 않는다.
3. 해당 교시 README에서 **실습 시간 → 파일 → 명령 → 결과**를 확인한다. 뒤 교시 폴더는 그 시간이 되었을 때 연다.
4. Python 예제는 해당 `pyproject.toml` 옆에서 `uv run`으로 실행한다. 교재 원본에는 lock이 없고, 검증된 배포 lock은 `--locked`로 확인한다.

## 2교시 안의 코드 구분

- **5–13분, 문제 1:** [README의 greet 시작 코드](period2/README.md#문제-1--greet만-작성하기). 개인 프로젝트의 `src/oss_tool/cli.py`를 작성한다.
- **13–21분, 문제 2:** [sysinfo를 더한 cli.py](period2/src/oss_tool/cli.py). JSON·저장·logging을 연결한다.
- **3교시 5–13분:** [config를 더한 cli.py](period3/src/oss_tool/cli.py). 설정 로더를 추가한다.

[기록 양식](week03_notes_template.md)은 개인 저장소의 `notes/week03.md`로 복사한다.

## 기존 경로 안내

`oss_tool/`은 `--repeat`·`--verbose`·`--ping` 등 선택 확장을 모은 기존 통합 참조본이다. 기본 실습의 시작 파일은 위의 `period1 → period2 → period3`다.
