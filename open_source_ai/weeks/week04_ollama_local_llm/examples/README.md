# 4주차 예제 — 실습지 교시별 시작점

수업에서는 **실습지의 현재 교시와 같은 `period1` → `period2` → `period3`만** 연다. 각 폴더 README에 실습 단계와 파일 대응, 20분 시연·30분 실습 시간표, 복사·실행·검증 명령이 있다.

| 교시 | 지금 여는 폴더 | 실습지의 목표 | 핵심 파일 |
|---|---|---|---|
| 1교시 | [period1](period1/README.md) | 모델 두 개를 실행하고 측정하기 | `ollama_probe.ps1` |
| 2교시 | [period2](period2/README.md) | REST API로 대화하고 실패를 다루기 | `chat.py`, `stream.py`, `ollama_api.py` |
| 3교시 | [period3](period3/README.md) | 수업 도우미 모델 만들기와 과제 점검 | `Modelfile` |

## 사용 순서

1. [실습지](../lab.md)의 현재 교시 준비 절을 읽는다.
2. 해당 `periodN` 폴더만 개인 주차 실습 폴더에 복사하고, 그 안에서 `uv run`을 실행한다. 각 폴더는 자기 코드·데이터·`pyproject.toml`로 독립 실행한다.
3. 현재 교시의 기본 문제·실패 경로·완료 조건을 마친 뒤 다음 폴더로 이동한다. 이미 작성한 기록을 다시 복사해 덮어쓰지 않는다.
4. 수치·보고서 답안은 직접 채운다. 교시 폴더의 역할은 시작 코드·공개 참조 구현·양식으로 각 README에 표시되어 있다.

패키지·모델은 수업 전에 준비한다. 환경 생성과 실행은 uv를 사용하며 [공통 uv 가이드](../../../uv_guide.md)의 설치·lock·Git 배포 절차를 따른다. 모델·`.venv/`·`.env`·`outputs/`는 복사하거나 커밋하지 않는다.

## 기존 링크 호환용 통합 참조

기존 [ollama_client/](ollama_client/README.md)와 [통합 상세 안내](ollama_client/reference_guide.md)는 전체 코드를 한 번에 비교할 때만 사용한다. 수업 실습의 진입점은 위 교시 표다. 기존 소스·템플릿은 보존했다.
