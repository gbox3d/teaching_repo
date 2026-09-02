# 4차 종합과제 최종 제출 체크리스트

배점·마감은 학교 운영 문서가 정한다. 이 체크리스트는 제출 전에 팀이 직접 확인하는 용도다. 항목마다 근거 파일·URL을 옆에 적는다. 안내서는 [assignment_brief.md](../assignment_brief.md), 루브릭은 [assignment_rubric.md](../assignment_rubric.md)다.

## 기준본

- [ ] 릴리스 태그가 있고(`git tag --list 'v*'`) 최종 commit을 가리킨다(`git describe --tags --exact-match`).
- [ ] 태그가 가리키는 commit id를 제출 정보에 적었다.
- [ ] 저장소 URL이 로그아웃 상태(또는 다른 브라우저)에서 열린다.
- [ ] 릴리스 뒤 고친 것이 있으면 패치 태그(`v0.1.1` 등)를 다시 찍고 CHANGELOG에 적었다.

## 실행·재현

- [ ] 깨끗한 폴더에서 `git clone` → `uv sync --frozen` → README 절차 → `uv run pytest -q`가 통과했다.
- [ ] `uv.lock`이 커밋되어 있고 `pyproject.toml`과 맞는다.
- [ ] 모델 ID·용량·다운로드 방법이 README에 있고, 실습 PC 사전 캐시 대상과 같다.
- [ ] GPU 없는 PC용 대체 경로(CPU·소형 모델)가 README에 있다.
- [ ] `verify_release.py` 결과에 FAIL이 없거나, 남은 FAIL의 이유를 기록했다.

## 문서 세트

- [ ] README: 무엇·왜·설치·실행·예시·제한·라이선스·출처.
- [ ] LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md.
- [ ] CHANGELOG.md에 릴리스 버전 항목, CITATION.cff(선택).
- [ ] Model Card(어댑터를 공개했다면)와 데이터 카드.

## 출처·라이선스

- [ ] `SOURCES.md`: 모델·데이터·코드·의존성의 이름·revision·라이선스(SPDX)·용도·변경 내용.
- [ ] 저장소 LICENSE와 모델·데이터 라이선스가 호환된다(근거 한 문장).
- [ ] 오픈 웨이트와 오픈소스를 구분해 적었다.

## 협업 근거(개인별)

- [ ] 팀원 각자 commit·Issue·PR·Review URL 1개 이상.
- [ ] `git shortlog -sn --no-merges` 결과가 README 또는 보고서에 있다.
- [ ] 14·15주차 교차 재현 Issue에 응답·라벨·반영 결정이 있다.

## 평가·한계

- [ ] 모델 평가 결과(수치·문항 수·평가셋 출처, 기준선 대비).
- [ ] 한계·오류 사례 3개 이상(`FAILURE_ANALYSIS.md` 등).
- [ ] 실행 화면 또는 3분 이내 시연 영상(비밀·개인정보 없음).

## AI 도구 활용 내역

- [ ] 어떤 도구를 어느 작업에 썼는지.
- [ ] 직접 검증·수정한 내용과 거절한 제안.

## 보안

- [ ] `.env` 미추적, `.env.example`만 있음, 이력에 비밀 없음(`git log -p`로 `token`·`key` 검색).
- [ ] `pip-audit` 결과와 남은 항목의 이유.
- [ ] 실제 이름·학번·전화·이메일 등 개인정보 없음(표시 이름 `student01`).
- [ ] 모델 파일은 safetensors 또는 외부 링크, `trust_remote_code` 사용 여부 명시.

## 제출 정보 양식

```text
팀: team-a
저장소 URL:
릴리스 태그:
태그가 가리키는 commit id:
재현 절차(3~5줄):
  1. git clone <URL>
  2. uv sync --frozen
  3. (README 절차)
  4. uv run pytest -q
팀원별 기여 URL:
  student01 — commit: / Issue: / PR: / Review:
  student02 — commit: / Issue: / PR: / Review:
시연 영상 또는 실행 화면 위치:
교차 재현 검증에서 받은 Issue와 처리:
AI 도구 활용 내역 위치:
```
