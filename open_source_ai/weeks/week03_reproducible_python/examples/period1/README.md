# 1교시 — uv 프로젝트와 재현

[실습지 1교시](../../lab.md#1교시-실습--uv-프로젝트를-만들고-깨끗한-폴더에서-재현하기)에 대응하는 **프로젝트 설정 참조본**이다.
아직 `src/`나 `oss-tool` 명령은 없다. 개인 저장소에서는 실습지대로 `uv init`·`uv add httpx`를 실행한다.

## 먼저 uv 설치·업데이트 확인

uv가 없는 Windows PC에서는 PowerShell로 설치한다.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

공식 설치 프로그램으로 설치한 uv를 최신 버전으로 갱신할 때는:

```powershell
uv self update
```

WinGet 설치본은 대신 `winget upgrade --id astral-sh.uv -e`를 사용한다.
수업 PC에 지정된 기준 버전이 있으면 그 버전을 유지한다. 설치 후 터미널을 새로 열고 확인한다.

```powershell
uv --version
Get-Command uv -All
```

VS Code 통합 터미널이면 VS Code도 다시 시작한다. 버전과 실행 파일 위치를 확인한 뒤 실습을 시작한다.
macOS·Linux 설치와 Homebrew 업데이트는 [주차별 설치 안내](../../README.md#시작-전-uv-설치와-최신-버전-업데이트)에 있다.
`uv self update`는 uv 자체의 갱신이며, 아래 `uv sync`는 프로젝트 패키지를 설치하는 명령이다.

## 프로젝트 파일과 실행

| 실습 단계 | 파일 | 비교할 것 |
|---|---|---|
| 문제 1 · init/add | [pyproject.toml](pyproject.toml), [.python-version](.python-version) | httpx 선언·Python 선택 |
| 문제 1 · 제외 규칙 | [.gitignore](.gitignore) | `.venv`·`.env` 제외, lock 유지 |
| 문제 2 · clone 검증 | [reproduce_check.ps1](reproduce_check.ps1) | 실습지의 네 단계 OK |

이 폴더를 교재 밖으로 복사해 설정 결과만 확인하려면:
```text
uv sync
uv run python -c "import sys, httpx; print(sys.executable); print(httpx.__version__)"
```
실행 파일은 복사본의 `.venv`에 있고 httpx 버전이 출력된다.
교재 원본에는 lock이 없다. 기준 PC에서 생성·검증한 lock을 포함한 배포본은 `--locked`로 실행한다.
`.python-version`의 3.12는 교재 요구사항에 맞춘 예시다. 개인 저장소에서는 환경 기준표 버전을 선택한다.
재현 스크립트는 실습지의 `C:\classwork\week03`에 따로 복사하며, `-Source`는 commit된 개인 저장소를 가리킨다.
이번 교시는 모델·GPU가 필요 없고 네트워크가 없으면 사전 캐시를 사용한다.
다음 [2교시](../period2/README.md)에서 같은 개인 저장소에 CLI를 추가한다.

## 실습 시간표

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 저장소 상태 확인, 예제 복사, 예상표 작성 |
| 프로젝트 만들기 | 5–13분 | `uv init` → `uv add httpx` → 루트 `.gitignore` → commit → `uv lock` |
| 깨끗한 폴더 재현 | 13–20분 | `reproduce_check.ps1`로 clone → `uv sync --locked` → `import httpx` |
| 실패 경로 | 20–25분 | 복제본에서 `uv.lock` 삭제 → `--locked` 실패 → 플래그 없는 `uv sync` |
| 검증·기록 | 25–30분 | 재현 로그를 `notes/`로 복사, 오류 첫 줄·설명 문장 기록, push |

시간은 설명·시연 20분 뒤 시작하는 **실습 30분 기준**이다. 휴식 10분은 별도다.
