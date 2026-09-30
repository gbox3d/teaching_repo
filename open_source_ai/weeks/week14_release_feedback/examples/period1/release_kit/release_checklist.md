# 릴리스 점검표 — v0.1.0 전에 확인할 것

복사해서 팀 저장소 `docs/release_checklist.md` 로 쓴다. 「확인 방법」의 명령을 실제로 실행한 뒤 「결과」를 채운다.
`release_check.py` 가 자동으로 보는 항목은 ★ 표시다. 나머지는 사람이 본다.

## 1. 문서 세트

| 항목 | 확인 방법 | 결과 |
|---|---|---|
| ★ README 8개 절(소개·왜·설치·실행·예시·제한·라이선스·출처) | `uv run python release_check.py --repo 경로` 의 `readme.sections` | |
| ★ AI 도구 사용 내역 | README 절 또는 `AI_USAGE.md` | |
| ★ LICENSE | 파일 첫 줄에 라이선스 이름 | |
| ★ CONTRIBUTING.md | Issue 양식·브랜치·PR 규칙이 적혀 있는가 | |
| ★ CHANGELOG.md `[Unreleased]` | 항목이 사용자 관점으로 3개 이상 | |
| ★ CITATION.cff | 필수 `cff-version`·`message`·`title`·`authors` + `version` | |
| ★ SOURCES.md | 모든 행에 라이선스·URL | |
| ★ MODEL_CARD.md (어댑터 공개 팀만) | `--require-model-card` 로 점검 | |
| CODE_OF_CONDUCT.md | 9주차 템플릿이 그대로 있는가 | |

## 2. 라이선스·출처 호환

| 항목 | 확인 방법 | 결과 |
|---|---|---|
| 코드 라이선스와 의존 패키지 라이선스가 충돌하지 않는다 | `SOURCES.md` 표에서 copyleft 항목 확인 | |
| 기반 모델 라이선스가 어댑터 공개를 허용한다 | 모델 카드의 license 필드 | |
| 데이터 라이선스의 NC·SA 조건을 README 제한 절에 적었다 | README 「제한」 | |


나머지 재현·릴리스·응답 점검은 다음 교시 자료에서 이어간다.
