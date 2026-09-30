# 14주차 2교시 — 릴리스 생성·교차 재현

[해당 실습 단계·문제·완료 조건](../../lab.md#2교시-실습--릴리스-생성과-교차-재현) · [교시별 색인](../README.md)

1교시 점검 도구·양식에 **릴리스 노트 및 교차 재현 도구**를 더했다. tag_notes.py는 기본 실행에서 노트만 쓰고, --promote를 명시하면 대상 CHANGELOG를 변경한다. Git 태그·push·Release·Issue는 lab에서 사람이 수행한다.

## 시간별 파일 대응

| 실습 시간 | 단계 | 이 폴더의 파일·경로 | 확인할 증거 |
|---|---|---|---|
| 0–3분 | 재현 실패 예상 | 팀 README | 먼저 막힐 곳1개 |
| 3–12분 | 태그·릴리스 | `tag_notes.py`, `release_kit/CHANGELOG_TEMPLATE.md` | 노트·태그·Release URL |
| 12–24분 | 교차 재현 | `release_kit/reproduce_by_stranger.ps1`, `reproduce_by_stranger.md` | 10분 재현 로그 |
| 24–30분 | 보고·정리 | `release_kit/feedback_issue_template.md`, `release_checklist.md` | 단계별 Issue·docs/repro 기록 |

파일명이 짧게 적힌 경우 바로 앞 열의 같은 하위 폴더를 기준으로 읽는다. 시간과 완료 조건은 연결된 실습지를 따른다.

## 실행 위치와 명령

이 `period2/` 폴더를 개인 실습 공간에 **처음 한 번 폴더째** 복사하고 그 안에서 실행한다. 숨김 파일도 포함한다. 이미 개인 교시 폴더가 있으면 다시 복사하지 않고 이어 한다. `.env`와 작성한 기록도 새 양식으로 덮어쓰지 않는다. 실제 준비 명령은 위 실습지 링크를 따른다. Python 명령은 `pyproject.toml` 옆에서 실행한다. `uv.lock`·`.venv/`는 배포하지 않았으므로 최초 `uv sync`로 개인 환경을 만든다.

```powershell
uv sync
uv run python tag_notes.py --repo C:\classwork\team-a-repo --version 0.1.0
# 먼저 outputs/release-notes-v0.1.0.md를 읽는다.
# 교차 재현은 lab 문제 2의 별도 빈 작업 폴더에서 실행한다.
```

## 기본 실행과 실습 후 검증

노트 초안과 제안 Git 명령이 출력된다. --promote 없이 대상 CHANGELOG는 바뀌지 않는다. 교차 재현 도구는 단계·초·결과를 로그에 남기며 README 기능 실행과 Issue 작성은 사람이 한다.

## 이전 산출물과 다음 단계

1교시 FAIL0 팀 저장소와 작성된 docs/release_checklist.md 1·2절을 이어받는다. 여기의 3~5절만 추가해 기존 결과를 보존한다.

## 대체 경로

GitHub가 없으면 로컬 저장소 경로로 재현하고 릴리스 노트·Issue 초안을 파일로 기록한다. 모델은 사전 캐시만 사용한다. --frozen은 lock 내용으로 설치하되 선언 일치는 검사하지 않으므로 그 진단은 대상 폴더의 uv lock --check로 구분한다.
