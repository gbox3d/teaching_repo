# 14주차 3교시 — 피드백·리허설

[해당 실습 단계·문제·완료 조건](../../lab.md#3교시-실습--피드백-응답과-시연-리허설) · [교시별 색인](../README.md)

앞선 도구·양식에 **Issue 분류 카드, 결정 기록 양식과 3분 시연 개요**를 더했다. 미래 평가 결과를 만들어 주지 않으며 실제 받은 피드백과 리허설 시간을 기록한다.

## 시간별 파일 대응

| 실습 시간 | 단계 | 이 폴더의 파일·경로 | 확인할 증거 |
|---|---|---|---|
| 0–3분 | 라벨 예상 | `release_kit/triage_labels.md` | 5개 라벨 기준 |
| 3–13분 | Issue·응답 | `feedback_issue_template.md`, `triage_labels.md` | 제안·응답·재현 근거 |
| 13–18분 | 결정 | `release_kit/DECISIONS_TEMPLATE.md` | 팀 DECISIONS.md |
| 18–26분 | 리허설 | `release_kit/demo_outline.md` | 3분 리허설2회 |
| 26–30분 | 검증·기록 | `release_checklist.md` 6절·팀 docs/demo_outline.md | URL·구간별 시간·fallback |

파일명이 짧게 적힌 경우 바로 앞 열의 같은 하위 폴더를 기준으로 읽는다. 시간과 완료 조건은 연결된 실습지를 따른다.

## 실행 위치와 명령

이 `period3/` 폴더를 개인 실습 공간에 **처음 한 번 폴더째** 복사하고 그 안에서 실행한다. 숨김 파일도 포함한다. 이미 개인 교시 폴더가 있으면 다시 복사하지 않고 이어 한다. `.env`와 작성한 기록도 새 양식으로 덮어쓰지 않는다. 실제 준비 명령은 위 실습지 링크를 따른다. Python 명령은 `pyproject.toml` 옆에서 실행한다. `uv.lock`·`.venv/`는 배포하지 않았으므로 최초 `uv sync`로 개인 환경을 만든다.

```powershell
Get-Content .\release_kit\triage_labels.md
# 팀 저장소 docs 폴더에서 쓸 양식을 복사한 뒤 채운다.
New-Item -ItemType Directory -Force C:\classwork\team-a-repo\docs | Out-Null
if (-not (Test-Path C:\classwork\team-a-repo\docs\demo_outline.md)) {
    Copy-Item .\release_kit\demo_outline.md C:\classwork\team-a-repo\docs\demo_outline.md
}
# DECISIONS.md가 이미 있으면 양식의 열만 참고하여 이어 쓴다.
```

## 기본 실행과 실습 후 검증

Issue마다 라벨·응답·결정·근거·반영 버전이 남는다. 리허설2회 기록과 실제 fallback 경로를 적고 2회차는 3분30초 이내인지 확인한다.

## 이전 산출물과 다음 단계

2교시 Release URL·보낸/받은 Issue·docs/repro 로그를 이어받는다. 템플릿은 빈 양식이며 답을 미리 채우지 않는다.

## 대체 경로

받은 Issue가 부족하면 lab의 역할 교대 경로를 사용하고 연습임을 적는다. Ollama·모델이 없으면 사전 출력 JSON·CLI·로컬 파일로 리허설한다.
