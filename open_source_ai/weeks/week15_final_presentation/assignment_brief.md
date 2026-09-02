# 4차 종합과제 — 최종 오픈소스 릴리스 패키지

## 목적

학기 내내 키운 "로컬 AI 도우미" 팀 저장소를, 처음 보는 사람이 README만 읽고 재현하고 검증하고 기여할 수 있는 오픈소스 릴리스로 완결한다. 13주차 테스트·CI·보안, 14주차 릴리스 문서·태그·교차 재현, 15주차 발표·검증·회고의 결과가 모두 저장소 안의 증거로 남아야 한다. 평가자는 발표를 듣고 믿는 것이 아니라 저장소를 clone해 체크리스트대로 확인한다. 배점·마감은 학교 운영 문서가 정한다.

## 대상 챕터 범위

4장(13~15주차)을 중심으로 1~12주차의 누적 산출물을 포함한다.

| 주차 | 이 과제에서 확인하는 것 |
|---|---|
| 1~4 | 재현 가능한 uv 프로젝트, LICENSE, `.env.example`, 설정 로더, Ollama 클라이언트와 오류 처리 |
| 5~8 | 모델·데이터 라이선스 분석(`SOURCES.md`, 모델 카드 분석), 출처 있는 RAG와 평가셋 |
| 9~12 | 거버넌스 문서(CONTRIBUTING·CoC·이슈 템플릿), LoRA 실험 기록, 데이터 카드·평가·실패 분석, 서비스 베타 |
| 13 | pytest·ruff, GitHub Actions, `pip-audit`, 교차 코드리뷰 |
| 14 | README·Model Card·CHANGELOG, `v0.1.0` 릴리스, 교차 재현 Issue 응답 |
| 15 | 최종 발표 기록, 교차 재현 검증 기록, 회고, 최종 제출 점검 |

## 필수 산출물

1. **실행 가능한 저장소와 재현 절차** — 처음 보는 PC에서 `git clone` → `uv sync --frozen` → README 절차 → `uv run pytest -q`가 통과한다. 모델 ID·용량·다운로드 방법과 GPU 없는 PC용 대체 경로(CPU·소형 모델)를 README에 둔다.
2. **README·LICENSE·CONTRIBUTING** — README는 무엇·왜·설치·실행·예시·제한·라이선스·출처 순서. CODE_OF_CONDUCT.md, CHANGELOG.md(릴리스 버전 항목), 선택으로 CITATION.cff. 어댑터를 공개했다면 Model Card.
3. **출처·라이선스 목록** — `SOURCES.md`에 모델·데이터·코드·의존성의 이름·revision·라이선스(SPDX ID)·용도·변경 내용. 저장소 LICENSE와의 호환 근거 한 문장. 오픈 웨이트와 오픈소스를 구분해 적는다.
4. **협업 근거** — 팀원별 commit·Issue·PR·Review URL, `git shortlog -sn --no-merges` 결과, 14·15주차 교차 재현 Issue에 대한 응답·라벨·반영 결정.
5. **실행 화면 또는 시연 영상** — 3분 이내, 릴리스 기준본에서 실행, 비밀·개인정보 없음. 영상은 저장소 밖 링크여도 되지만 README에서 찾을 수 있어야 한다.
6. **모델 평가 결과와 한계·오류 사례** — 기준선 대비 수치(문항 수·평가셋 출처·학습에 쓰지 않았다는 근거), 실패 사례 3개 이상(`FAILURE_ANALYSIS.md` 등), 데이터 카드.
7. **AI 도구 활용 내역과 직접 검증·수정한 내용** — 어떤 도구를 어느 작업에 썼는지, 채택·거절·수정한 제안과 검증 방법. README 또는 `docs/AI_USAGE.md`.
8. **릴리스 태그** — `v0.1.0` 이상. 릴리스 뒤 고쳤으면 패치 태그(`v0.1.1` 등)와 CHANGELOG 항목. 태그가 가리키는 commit이 제출 commit이다.
9. **15주차 산출물** — 교차 재현 검증 기록(`review-<팀>.md`, 등록한 Issue URL), 발표 기록(`presentation_log.md`), 개인 회고(`retrospective.md`). 개인 저장소 또는 팀 저장소 `docs/`에 둔다.

## 제출 형식

- 저장소 URL
- 릴리스 태그 이름과 그 태그가 가리키는 **최종 commit id**
- README 재현 절차(3~5줄)를 제출 정보에 그대로 옮겨 적는다
- 팀원별 기여 URL, 시연 영상 또는 실행 화면 위치, 받은 Issue와 처리
- 양식은 [examples/submission_checklist.md](examples/submission_checklist.md)의 "제출 정보 양식"을 쓴다

```text
팀: team-a
저장소 URL:
릴리스 태그:
태그가 가리키는 commit id:
재현 절차(3~5줄):
팀원별 기여 URL:
시연 영상 또는 실행 화면 위치:
교차 재현 검증에서 받은 Issue와 처리:
AI 도구 활용 내역 위치:
```

제출 뒤 저장소를 고쳤다면 제출 commit id는 바뀌지 않는다. 고친 내용은 다음 태그로 남긴다.

## 개인 기여 증거

팀 과제이지만 개인별로 다음을 확인한다. 하나라도 없으면 해당 개인의 협업 근거 항목이 부분 충족이다.

- 본인 commit 1개 이상(`git log --author=<표시 이름>`), 의미 있는 변경(오타 수정만은 제외)
- 본인이 만든 Issue 1개 이상(기능·버그·재현 실패 보고 모두 가능)
- 본인이 올린 PR 1개 이상과 리뷰를 받은 흔적
- 본인이 남긴 Review 코멘트 1개 이상(다른 팀 PR 리뷰 포함)
- 15주차 교차 재현 검증 기록과 회고(개인 작성)

## 제출 전 검사 체크리스트

전체 목록은 [examples/submission_checklist.md](examples/submission_checklist.md)다. 최소 확인 항목:

- [ ] 깨끗한 폴더에서 clone → `uv sync --frozen` → README 절차 → pytest가 통과했다.
- [ ] `git describe --tags --exact-match`가 제출 태그를 돌려주고, 그 commit id를 제출 정보에 적었다.
- [ ] `verify_release.py` 결과에 FAIL이 없거나 남은 FAIL의 이유를 적었다.
- [ ] `SOURCES.md`의 라이선스가 저장소 LICENSE와 호환된다는 근거 한 문장이 있다.
- [ ] 팀원 전원의 commit·Issue·PR·Review URL이 있다.
- [ ] 평가 수치·실패 사례·AI 도구 내역이 README 또는 링크된 문서에 있다.
- [ ] `.env`가 추적되지 않고 이력에도 비밀이 없다. 개인정보가 없다.

## 금지 사항

- 실제 토큰·비밀번호·개인정보(실명·학번·전화·이메일)를 저장소·영상·보고서에 넣지 않는다. 표시 이름은 `student01`, 팀명은 `team-a`.
- 재현 불가능한 캡처만으로 실행 증거를 대신하지 않는다. 명령과 출력, commit id가 함께 있어야 한다.
- 라이선스가 없는 코드·모델·데이터를 쓰지 않는다. 라이선스가 없으면 사용 불가로 본다.
- 릴리스 태그 밖의 commit으로 시연·제출하지 않는다.
- 다른 팀 저장소에 Issue 외의 쓰기를 하지 않는다.
- 제출 뒤 태그를 옮기거나(`git tag -f`) 이력을 다시 쓰지 않는다.

학교 적용 시 실제 비율·마감은 학교 운영 문서가 정한다.
