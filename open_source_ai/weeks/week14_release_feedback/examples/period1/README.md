# 14주차 1교시 — 릴리스 문서 보완

[해당 실습 단계·문제·완료 조건](../../lab.md#1교시-실습--릴리스-문서-세트-보완) · [교시별 색인](../README.md)

팀 저장소를 읽는 **릴리스 점검 도구와 문서 양식**이다. 이 폴더 자체가 제출할 팀 프로젝트는 아니다. 릴리스 노트 생성·재현 스크립트·피드백 카드는 다음 교시에 추가한다.

## 시간별 파일 대응

| 실습 시간 | 단계 | 이 폴더의 파일·경로 | 확인할 증거 |
|---|---|---|---|
| 0–4분 | FAIL 예상 | `release_check.py`의 검사 항목 | 예상3개와 이유 |
| 4–9분 | 자동 점검 | `release_check.py` | FAIL/WARN 목록 |
| 9–22분 | 문서 보완 | `release_kit/README_TEMPLATE.md`, `CHANGELOG_TEMPLATE.md`, `CITATION.cff`, `MODEL_CARD_TEMPLATE.md` | 팀 저장소 문서·라이선스 근거 |
| 22–26분 | 재점검 | `release_check.py` | FAIL0 또는 남은 WARN 이유 |
| 26–30분 | 결과 정리 | `release_kit/release_checklist.md`의 1·2절 | 팀 docs/release_checklist.md |

파일명이 짧게 적힌 경우 바로 앞 열의 같은 하위 폴더를 기준으로 읽는다. 시간과 완료 조건은 연결된 실습지를 따른다.

## 실행 위치와 명령

이 `period1/` 폴더를 개인 실습 공간에 **처음 한 번 폴더째** 복사하고 그 안에서 실행한다. 숨김 파일도 포함한다. 이미 개인 교시 폴더가 있으면 다시 복사하지 않고 이어 한다. `.env`와 작성한 기록도 새 양식으로 덮어쓰지 않는다. 실제 준비 명령은 위 실습지 링크를 따른다. Python 명령은 `pyproject.toml` 옆에서 실행한다. `uv.lock`·`.venv/`는 배포하지 않았으므로 최초 `uv sync`로 개인 환경을 만든다.

```powershell
uv sync
uv run python release_check.py --repo C:\classwork\team-a-repo --tag v0.1.0
```

## 기본 실행과 실습 후 검증

팀 저장소 상태에 따라 PASS/WARN/FAIL과 outputs/release-check-*.json이 나온다. 처음부터 FAIL0을 가정하지 않는다. 실제 문서를 보완한 뒤 counts.fail=0과 WARN 처리 이유를 남긴다.

## 이전 산출물과 다음 단계

13주차 팀 저장소, 기존 LICENSE·CONTRIBUTING·SOURCES, 실험·평가 기록을 사용한다. 템플릿은 팀 저장소에 복사해 실제 값으로 채우며 기존 문서를 덮어쓰지 않는다.

## 대체 경로

모델·GPU는 필요 없다. 라이선스 출처 접속이 막히면 보유한 카드와 출처 기록으로 확인 가능한 부분만 쓰고 미확인 항목을 표시한다.
