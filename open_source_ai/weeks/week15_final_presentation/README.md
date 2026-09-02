# 15주차 — 기말평가와 프로젝트 발표

## 이번 주 질문

> 우리 프로젝트는 다른 사람이 재현·검증·기여할 수 있는 오픈소스 릴리스인가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 문제 → 시연 → 한계 → 다음 순서로 3분 안에 프로젝트를 실제로 실행해 보이고, 2분 질의에 파일·commit·수치를 근거로 답한다.
2. 평가자 체크리스트(clone → `uv sync --frozen` → 실행 → 테스트 → 문서·라이선스·출처 → 비밀 검사)로 다른 팀의 릴리스를 검증하고 결과를 재현 가능하게 기록한다.
3. 재현 실패를 환경 문제·릴리스 결함·설계 한계로 구분해 Issue 양식으로 보고한다.
4. 기말평가·발표·4차 종합과제 루브릭의 항목을 자기 저장소의 파일과 대응시켜 빠진 증거를 찾는다.
5. 잘된 것·어려웠던 것·다음에 다르게 할 것을 근거와 함께 회고하고, 동료에게 실행 가능한 피드백을 남긴다.
6. 릴리스 이후의 유지 책임(라이선스·출처·Issue 응답)과 포트폴리오로서의 다음 행동 3개를 계획한다.

## 누적 결과물

이번 주는 4차 종합과제(최종 오픈소스 릴리스 패키지)를 마감하고 제출하는 주다. 1교시 발표 기록, 2교시 교차 재현 검증 기록, 3교시 회고와 제출 점검이 그대로 4차 과제의 "협업 근거·평가 결과와 한계·AI 도구 활용 내역" 항목을 채운다. 14주차 `v0.1.0` 릴리스에서 발견된 결함을 고쳤다면 패치 태그(`v0.1.1` 등)로 최종 기준본을 확정한다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 발표 규칙과 평가자의 시선: 팀당 시연 3분 + 질의 2분, 순서·장비 점검, 평가자가 보는 것(문제·시연·한계·재현), 질문 카드 예시 | 최종 발표 라운드: 기준본에서 시연·질의, 청중은 발표 기록(팀 수에 따라 학교 시간표로 확장) | `presentation_log.md` |
| 2교시 | 재현성 검증 절차와 기말평가 항목: 평가자 체크리스트 6단계, 실패 구분, 검증 도구 시연, 기말평가 루브릭 | 교차 재현 검증: 다른 팀 저장소를 체크리스트로 검증·기록, 재현 실패 Issue 등록 | `review-<팀>.md`, `outputs/verify-*.md`, Issue URL |
| 3교시 | 회고와 오픈소스 이후: 회고 방법, 동료 피드백 원칙, 기여 지속·포트폴리오·라이선스 유지 책임, 4차 과제 제출 점검 | 회고와 최종 제출 점검: 동료 피드백·개인 회고 작성, `submission_checklist.md`로 최종 제출 점검 | `peer_feedback-<팀>.md`, `retrospective.md`, `submission.md` |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- 팀 저장소의 14주차 릴리스(`v0.1.0` 태그)와 열린 Issue 목록. 결함을 고쳤다면 패치 태그까지 찍은 상태.
- Git, VS Code, uv, Ollama, PowerShell. 시연·검증에 쓰는 모델은 발표 PC와 검증 PC에 사전 캐시되어 있어야 한다(`ollama list`로 확인). 실습 시간에 모델을 내려받지 않는다.
- 발표 PC 연결과 장애 대체 자료: 사전 실행 결과 `outputs/`, 화면 녹화, 시연 명령 파일.
- 이번 주 [`examples/`](examples/README.md)의 템플릿과 `release_verify/` 검증 도구 복사본.
- 정확한 도구 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 발표 화면·검증 기록·회고에 실제 이름, 학번, 토큰, 개인정보를 넣지 않는다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): 시연 개요·질문 카드·리뷰어 체크리스트·동료 피드백·회고·제출 체크리스트 템플릿과 릴리스 검증 도구 `release_verify/`
- 강의 대본: 강의자 별도 관리(비공개)
- [4차 종합과제 안내](assignment_brief.md) · [4차 종합과제 루브릭](assignment_rubric.md)
- [기말평가 루브릭](final_review_rubric.md) · [최종 발표 루브릭](presentation_rubric.md)

## 권장 진행 방식

1. 발표 전에 세 루브릭을 읽고 "평가자가 무엇을 보는가"를 팀에서 한 문장씩 정리한다.
2. 발표는 릴리스 태그가 가리키는 기준본에서만 한다. 발표 중 코드를 고치지 않는다.
3. 다른 팀 저장소를 검증할 때는 처음 보는 사람처럼 README만 읽고 시작하며, 막히면 재시도 1회 뒤 기록한다.
4. 재현 실패는 "환경 문제 / 릴리스 결함 / 설계 한계"로 분류하고 릴리스 결함만 Issue로 보낸다.
5. 회고와 피드백은 근거(commit·Issue·수치)를 붙인 문장만 쓴다. 점수를 매기지 않는다.

## 완료 기준

- [ ] 릴리스 태그 기준본에서 시연 3분 + 질의 2분을 마쳤다(장애가 났다면 fallback으로 마치고 원인을 기록했다).
- [ ] 다른 팀 발표를 `presentation_log.md`에 팀마다 한 행씩 기록했다.
- [ ] 다른 팀 저장소를 clone → `uv sync --frozen` → 실행 → 테스트 → 문서·라이선스·출처 → 비밀 순으로 검증하고 `review-<팀>.md`를 작성했다.
- [ ] 재현 실패를 분류해 릴리스 결함 Issue를 1건 이상 등록했다(없으면 "결함 없음"과 근거를 적었다).
- [ ] 동료 피드백 1건을 대상 팀에 전달하고 개인 회고 `retrospective.md`를 작성했다.
- [ ] 자기 팀 저장소에 `verify_release.py`를 실행해 FAIL이 없거나 남은 FAIL의 이유를 기록했다.
- [ ] `submission_checklist.md`를 모두 확인하고 `submission.md`에 저장소 URL·태그·commit id·재현 절차·팀원별 기여 URL을 적었다.

## 제출 증거

이번 주는 4차 종합과제 제출 주다. 제출 형식은 [4차 종합과제 안내](assignment_brief.md)를 따르고, 아래 증거를 개인 저장소(또는 팀 저장소 `docs/`)에 누적한다.

1. 팀 저장소 URL, 릴리스 태그, 태그가 가리키는 commit id
2. `presentation_log.md`: 다른 팀 발표 기록
3. `review-<팀>.md`: 교차 재현 검증 체크리스트, 등록한 Issue URL, `outputs/verify-<팀>-*.md`
4. `peer_feedback-<팀>.md`, `retrospective.md`
5. `submission.md`: 제출 정보 양식과 체크리스트 확인 결과

터미널 출력과 보고서에는 사용자 홈 경로가 포함될 수 있다. 제출 전에 개인 식별 정보가 없는지 확인한다.

## 다음 주 연결

이번 주로 학기가 끝난다. 다음 주차 폴더는 없다. 대신 저장소를 닫지 말고 다음 세 가지를 한다.

1. 교차 재현 검증에서 받은 Issue 중 하나를 닫고 패치 릴리스(`v0.1.1`)를 낸다.
2. 수업 밖의 오픈소스 프로젝트(문서 오타·재현 실패 보고라도 좋다)에 작은 Issue 또는 PR을 하나 보낸다.
3. 사용한 모델·데이터·의존성의 라이선스를 한 학기 뒤에 다시 확인하고 `SOURCES.md`를 갱신한다. 라이선스는 릴리스 순간이 아니라 유지하는 동안의 책임이다.

## 참고 자료

- [GitHub Docs — About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [uv — Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [Open Source Initiative — Licenses](https://opensource.org/licenses)
- [OSI — Open Source AI Definition](https://opensource.org/ai)
- [Keep a Changelog](https://keepachangelog.com/)
- [Contributor Covenant](https://www.contributor-covenant.org/)
