# 9주차 — 프로젝트 제안과 오픈소스 거버넌스

## 이번 주 질문

> 우리 팀이 만들 오픈소스 AI 프로젝트는 어떤 문제를 누구를 위해 어떤 규칙으로 만들 것인가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 오픈소스 프로젝트의 역할(사용자·기여자·커미터·메인테이너)과 의사결정 모델(BDFL·위원회·재단)을 구분한다.
2. 공개 저장소의 CODE_OF_CONDUCT·CONTRIBUTING·이슈 템플릿·릴리스 주기를 읽고 프로젝트 건강 지표(첫 응답 시간·버스 팩터)를 근거와 함께 기록한다.
3. 사용자·상황·기존 해법의 한계로 문제를 한 문장으로 정의하고 Must/Should/Could로 범위를 나눈다.
4. 모델·데이터 후보를 라이선스·VRAM·재현성·확보 가능성 기준으로 비교하고 위험과 완화책을 적는다.
5. 10~15주 일정을 역산해 마일스톤 3개와 검증 가능한 Issue 8~10개로 분해하고 팀원별 역할을 정한다.
6. 팀 저장소에 거버넌스 문서를 배치하고 3분 제안 발표를 구성한다.

## 누적 결과물

이번 주는 3장(9~12주)의 출발점이다. 팀 제안서(`proposal.md`), 거버넌스 문서를 갖춘 팀 저장소, 마일스톤·Issue 목록은 12주차 **3차 종합과제**(LoRA 실험 기록·AI 서비스 베타)의 저장소 골격이 되고, 15주차 **4차 종합과제**(최종 오픈소스 릴리스 패키지)와 최종 발표까지 그대로 이어진다. 1교시 거버넌스 조사에서 고른 규칙 3개는 팀 저장소의 `CONTRIBUTING.md`에 들어간다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 오픈소스 거버넌스 — 역할·규칙·건강 지표 | 거버넌스 문서 분석표 | `governance_survey.md` 2행 표 + "우리 팀이 가져올 규칙 3개" |
| 2교시 | 문제 정의와 기술 선정 근거 | 팀 제안서 초안 | `proposal.md` 초안(문제·사용자·Must 3개·모델 후보 2개·데이터 후보·위험 2개) |
| 3교시 | 마일스톤·역할·제안 발표 | 팀 저장소와 이슈 분해 | 팀 저장소 URL, Issue 8~10개·마일스톤 3개, 발표 리허설 기록 |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Git, VS Code, uv, PowerShell, 브라우저. GitHub 계정(2주차에 확인한 것)과 팀원 2~3명(팀명은 `team-a` 같은 수업용 값).
- 8주차까지의 개인 저장소(LICENSE, `license_matrix.md`, `model_cards.md`, `SOURCES.md`, RAG 미니프로젝트). 2교시 모델·데이터 후보 표는 이 문서들을 재사용한다.
- Ollama 서버가 켜져 있고 기본 모델이 사전 캐시되어 있으면 3교시 저장소 골격 검사(`doctor`)에 쓴다. 없어도 이번 주 실습은 진행된다.
- 정확한 도구 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 실명·학번·전화번호·비밀번호·API 토큰을 제안서, 팀 저장소, 캡처에 넣지 않는다. GitHub 토큰은 `.env`에만 두고 `.env.example`만 커밋한다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): 팀 저장소 뼈대(`project_template/`), 제안 도구(`proposal_tools/`: VRAM 추정·저장소 건강 조사·이슈 계획 검사·이슈 등록), 조사표·마일스톤 템플릿
- 강의 대본: 강의자 별도 관리(비공개)
- [제안서 양식](proposal_template.md): 팀 제안서 `proposal.md`의 항목과 작성 기준
- [제안 발표 채점표](proposal_rubric.md): 3분 제안 발표 100점 상대 배점

## 권장 진행 방식

1. 1교시 조사표는 브라우저로 저장소를 직접 읽으며 채우고, 수치 항목만 `repo_health.py`로 보강한다. 스크립트 출력만 옮겨 적지 않는다.
2. 2교시 제안서는 문제 문장 한 줄을 먼저 확정한 뒤 나머지 항목을 채운다. 문제가 흔들리면 모델·데이터 선택도 흔들린다.
3. 모델 후보의 VRAM은 `vram_estimate.py`로 계산한 값과 4주차 `model_report.md`의 실측값을 나란히 적는다.
4. 3교시 Issue는 GitHub에 올리기 전에 `issue_plan_check.py`로 완료 조건·담당·마일스톤 누락을 잡는다.
5. 발표 리허설은 타이머를 켜고 3분을 재며, 넘긴 시간과 빠진 항목을 기록한다.

## 완료 기준

- [ ] `governance_survey.md`에 공개 프로젝트 2개의 CoC·CONTRIBUTING·이슈 템플릿·릴리스 간격·메인테이너 수를 근거 URL과 함께 적었다.
- [ ] "우리 팀이 가져올 규칙 3개"를 출처 프로젝트와 적용 방식으로 적었다.
- [ ] `proposal.md`에 문제 한 문장, 사용자 한 명, Must 3개가 있다.
- [ ] 모델 후보 2개에 라이선스(SPDX 또는 약관 이름)와 VRAM 추정 근거가 있고, 데이터 후보에 확보 방법과 라이선스가 있다.
- [ ] 위험 2개에 각각 완화책이 있다.
- [ ] 팀 저장소에 LICENSE, CODE_OF_CONDUCT.md, CONTRIBUTING.md, 이슈·PR 템플릿이 있고 `uv run team-project doctor`가 실행된다.
- [ ] 마일스톤 3개와 Issue 8~10개가 등록되었고 각 Issue에 완료 조건·담당·마일스톤이 있다.
- [ ] 3분 발표 리허설 기록(소요 시간, 빠진 항목, 예상 질문 2개)이 있다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 팀 저장소와 개인 저장소에 누적한다. 제안 발표의 평가는 [제안 발표 채점표](proposal_rubric.md)를 기준으로 하며, 발표 시각과 실제 반영 비율은 학교 운영 문서가 정한다.

1. 개인 저장소: `governance_survey.md`
2. 팀 저장소 URL과 `docs/proposal.md` 초안의 commit id
3. 팀 저장소의 Issue 목록(마일스톤별)과 본인이 등록한 Issue URL 1개 이상
4. 발표 리허설 기록(`docs/rehearsal.md`: 소요 시간, 빠진 항목, 예상 질문 2개)

터미널 출력과 저장소 설정 화면에는 사용자 홈 경로나 이메일이 포함될 수 있다. 제출 전에 개인 식별 정보가 없는지 확인한다.

## 다음 주 연결

`week10_peft_lora`에서 팀 제안서의 모델 후보 1개를 실제로 LoRA 학습한다. 그 첫 실험 기록(`experiments/run-001.md`)이 이번 주 마일스톤 M1의 첫 Issue를 닫는 증거가 되고, 12주차 3차 종합과제의 첫 재료가 된다. 다음 수업 전에 팀 저장소를 clone하고 `uv sync`가 되는지 확인해 둔다.

## 참고 자료

- [GitHub Docs — 커뮤니티 프로필과 건강 파일](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories)
- [GitHub Docs — 이슈 템플릿 구성](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [GitHub Docs — 마일스톤](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)
- [Contributor Covenant](https://www.contributor-covenant.org/)
- [Open Source Guides — Leadership and Governance](https://opensource.guide/leadership-and-governance/)
- [Choose a License](https://choosealicense.com/)
