# 1주차 예제 — 실습환경·탐색·첫 실행

[실습지](../lab.md)의 순서대로 **지금 교시의 폴더 하나만** 연다.
각 폴더 README의 시간표는 실습지의 실습 30분 시간표와 같다. 설명·시연 20분과 휴식 10분은 별도다.

| 교시 | 예제 폴더 | 지금 볼 파일·자료 | 실습 |
|---|---|---|---|
| 1교시 · 실습환경 점검표 만들기 | [period1](period1/README.md) | `env_check.ps1 · env_check_template.md` | [실습 1교시](../lab.md#1교시-실습--실습환경-점검표-만들기) |
| 2교시 · 공개 AI 프로젝트 탐색표 | [period2](period2/README.md) | `oss_survey_template.md` | [실습 2교시](../lab.md#2교시-실습--공개-ai-프로젝트-탐색표) |
| 3교시 · 첫 uv 실행과 첫 commit | [period3](period3/README.md) | `sysinfo.py · pyproject.toml · .env.example` | [실습 3교시](../lab.md#3교시-실습--첫-uv-실행과-첫-commit) |

## 사용 순서

1. 실습지의 해당 교시 **준비**부터 진행한다. 예제의 역할(제공 코드·참조 코드·학생용 양식)은 교시 README에 적혀 있다.
2. 파일을 개인 실습 폴더로 복사하거나, 실습지에서 지정한 파일을 자기 코드와 비교한다. 기존 개인 코드·보고서·lock을 통째로 덮어쓰지 않는다.
3. 해당 교시 README에서 **실습 시간 → 파일 → 명령 → 결과**를 확인한다. 뒤 교시 폴더는 그 시간이 되었을 때 연다.
4. Python 예제는 해당 `pyproject.toml` 옆에서 `uv run`으로 실행한다. 교재 원본에는 lock이 없고, 검증된 배포 lock은 `--locked`로 확인한다.

## 기존 경로 안내

이전 배포 링크를 위해 기존 파일은 남겨 두었다. 이번 수업에서는 위 `period1 → period2 → period3` 경로만 따라간다.
