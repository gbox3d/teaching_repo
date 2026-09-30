# 15주차 3교시 — 회고·최종 제출

[해당 실습 단계·문제·완료 조건](../../lab.md#3교시-실습--회고와-최종-제출-점검) · [교시별 색인](../README.md)

교차 검증 도구에 **동료 피드백·회고·최종 제출 양식**을 더했다. 앞선 기록을 근거로 빈칸을 채우며 실제 받지 않은 리뷰나 실행하지 않은 검증을 만들어 적지 않는다.

## 시간별 파일 대응

| 실습 시간 | 단계 | 이 폴더의 파일·경로 | 확인할 증거 |
|---|---|---|---|
| 0–8분 | 동료 피드백 | `peer_feedback_form.md` | 근거4칸·전달URL |
| 8–18분 | 개인 회고 | `retrospective_template.md` | 근거·기여URL·다음행동3개 |
| 18–26분 | 제출 점검 | `submission_checklist.md`, `verify_release.py` | 자기팀 FAIL/WARN·태그 |
| 26–30분 | 기록 확정 | 개인 `submission.md`와 앞선 증거 | commit id·기여URL·증거 commit |

파일명이 짧게 적힌 경우 바로 앞 열의 같은 하위 폴더를 기준으로 읽는다. 시간과 완료 조건은 연결된 실습지를 따른다.

## 실행 위치와 명령

이 `period3/` 폴더를 개인 실습 공간에 **처음 한 번 폴더째** 복사하고 그 안에서 실행한다. 숨김 파일도 포함한다. 이미 개인 교시 폴더가 있으면 다시 복사하지 않고 이어 한다. `.env`와 작성한 기록도 새 양식으로 덮어쓰지 않는다. 실제 준비 명령은 위 실습지 링크를 따른다. Python 명령은 `pyproject.toml` 옆에서 실행한다. `uv.lock`·`.venv/`는 배포하지 않았으므로 최초 `uv sync`로 개인 환경을 만든다.

```powershell
uv sync
if (-not (Test-Path .\peer_feedback-team-b.md)) { Copy-Item .\peer_feedback_form.md .\peer_feedback-team-b.md }
if (-not (Test-Path .\retrospective.md)) { Copy-Item .\retrospective_template.md .\retrospective.md }
if (-not (Test-Path .\submission.md)) { Copy-Item .\submission_checklist.md .\submission.md }
uv run python verify_release.py --repo C:\classwork\team-a-repo --team team-a
```

## 기본 실행과 실습 후 검증

검증 보고서를 읽어 FAIL을 고치거나 남은 이유를 submission.md에 적는다. 발표·교차검증 기록과 받은 Issue를 근거로 회고를 작성하고 태그의 commit id와 제출값을 맞춘다.

## 이전 산출물과 다음 단계

1교시 presentation_log.md, 2교시 review-team-b.md·Issue, 우리 팀이 받은 Issue를 함께 본다. 빈 양식 복사는 최초1회만 하고 이후 기록을 보존한다.

## 대체 경로

Ollama가 준비된 경우에만 검증 명령에 --check-ollama를 추가한다. 준비되지 않았으면 모델 항목을 환경 문제로 기록하고 파일 검증을 진행한다. 전달·push가 불가능하면 초안을 남겨 접속 복구 후 수행한다.
