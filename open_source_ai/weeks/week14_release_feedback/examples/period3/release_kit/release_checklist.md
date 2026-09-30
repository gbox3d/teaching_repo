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

## 3. 재현

| 항목 | 확인 방법 | 결과 |
|---|---|---|
| ★ `uv.lock` 이 커밋되어 있다 | `git ls-files uv.lock` | |
| 새 폴더에서 `uv sync --frozen` 이 성공한다 | `reproduce_by_stranger.ps1` | |
| README 「실행」 명령이 복사·붙여넣기로 동작한다 | 새 폴더에서 실행 | |
| 테스트가 통과한다 | `uv run pytest -q` | |
| CI 가 초록불이다 | GitHub Actions 최근 실행 | |

## 4. 보안

| 항목 | 확인 방법 | 결과 |
|---|---|---|
| ★ `.env` 가 추적되지 않는다 | `git ls-files .env` 가 비어 있다 | |
| ★ `.env.example` 이 있다 | 파일 존재, 값은 비어 있거나 예시 | |
| 이력에 토큰이 없다 | 13주차 `security_check.ps1` | |
| 출력·로그에 홈 경로·계정 이름이 없다 | `outputs/` 샘플 확인 | |

## 5. 버전·태그·릴리스

| 항목 | 확인 방법 | 결과 |
|---|---|---|
| ★ `pyproject.toml` version = 태그 번호 | `--tag v0.1.0` 으로 점검 | |
| CITATION.cff version 이 같다 | 파일 확인 | |
| 주석 태그(`-a`)로 만들었다 | `git show v0.1.0` 에 Tagger 가 있다 | |
| GitHub Release 에 릴리스 노트가 있다 | 릴리스 URL: | |
| 첨부 파일(있다면)에 비밀·개인정보가 없다 | 첨부 목록 확인 | |

## 6. 피드백 통로

| 항목 | 확인 방법 | 결과 |
|---|---|---|
| Issue 를 누구나 만들 수 있다 | 저장소 설정 Issues 켜짐 | |
| 라벨 5개가 있다 | `triage_labels.md` | |
| 첫 응답 담당자가 정해져 있다 | CONTRIBUTING 또는 팀 규칙 | |
