# 교차 재현 — 처음 보는 사람으로 실행하기

다른 팀의 릴리스를 **README 만 보고** 10분 안에 실행해 보는 절차와 기록 양식이다.
재현하는 사람은 그 팀의 팀원에게 아무것도 묻지 않는다. 막힌 곳이 곧 README 의 결함이며, 그것이 이 절차의 산출물이다.

## 규칙

1. 타이머 10분을 켠다. 시작 시각을 적는다.
2. 대상 팀 저장소의 README 와 릴리스 노트만 읽는다. 코드를 읽어 원인을 찾지 않는다.
3. 새 폴더에서 시작한다. 이전 clone·가상환경을 재사용하지 않는다.
4. 막히면 30초만 시도하고 기록한 뒤 다음 단계로 간다. 고쳐 주지 않는다.
5. 출력을 붙여넣기 전에 홈 경로·계정 이름을 지운다.

## 절차

| 단계 | 할 일 | 성공 기준 |
|---|---|---|
| 1 | `reproduce_by_stranger.ps1 -Source 주소 -Tag v0.1.0` 실행 | clone·checkout·`uv sync --frozen` 이 성공 |
| 2 | `.env` 를 README 가 시키는 대로 채운다 | 필요한 값이 README 에 다 적혀 있다 |
| 3 | README 「실행」 절의 첫 명령을 그대로 실행 | 오류 없이 도움말 또는 첫 응답이 나온다 |
| 4 | README 「예시」 절의 입력을 넣는다 | 예시와 같은 형태의 출력이 나온다 |
| 5 | 테스트(있으면) `uv run pytest -q` | 통과 |
| 6 | 타이머를 멈추고 총 시간을 적는다 | 600초 이내 |

스크립트 없이 손으로 할 때의 명령:

```powershell
New-Item -ItemType Directory -Force C:\classwork\repro | Out-Null
Set-Location C:\classwork\repro
git clone REPO_URL repro-team-b
Set-Location repro-team-b
git checkout v0.1.0
uv sync --frozen
Copy-Item .env.example .env
```

## 기록 양식

`repro-log-<시각>.md` 가 1단계까지의 표를 만들어 준다. 그 아래에 다음을 이어 적는다.

```text
## 재현 기록

- 대상 저장소·태그:
- 재현한 사람(팀명):
- 시작 시각 / 종료 시각 / 총 소요:
- 환경: OS, GPU 유무, Ollama 실행 여부

| 단계 | 소요(초) | 결과 | 막힌 곳 | README 의 어느 절 |
|---|---:|---|---|---|
| 1 clone·sync |  |  |  |  |
| 2 .env |  |  |  |  |
| 3 실행 명령 |  |  |  |  |
| 4 예시 입력 |  |  |  |  |
| 5 테스트 |  |  |  |  |

가장 먼저 막힌 곳 한 문장:
그것이 코드 문제인가 문서 문제인가(근거):
```

## Issue 로 옮길 때

- 막힌 단계마다 Issue 1건. 여러 문제를 한 Issue 에 합치지 않는다.
- 양식은 `feedback_issue_template.md`. 환경·실행한 명령·전체 출력·README 위치 네 가지를 반드시 넣는다.
- 성공했으면 기록 파일을 자기 팀 저장소 `docs/repro/` 에 commit 하고, 대상 팀에 총 소요 시간을 알린다.
