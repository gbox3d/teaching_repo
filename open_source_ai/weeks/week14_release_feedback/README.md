# 14주차 — 릴리스와 커뮤니티 피드백

## 이번 주 질문

> 처음 보는 사람이 README만 읽고 10분 안에 실행하고, 의견을 남기고 싶어지는 릴리스는 무엇으로 이루어지는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 릴리스 문서 세트(README 8개 절, LICENSE, CONTRIBUTING, CHANGELOG, CITATION.cff, `SOURCES.md`, 어댑터 공개 시 Model Card, AI 도구 사용 내역)를 점검표와 `release_check.py`로 검사하고 빠진 것을 보완한다.
2. 코드·의존성·모델·데이터 라이선스의 호환 여부를 `SOURCES.md`에서 대조하고, 가장 제한적인 조건을 README 「제한」 절에 한 문장으로 적는다.
3. Semantic Versioning에 따라 `v0.1.0` 주석 태그와 GitHub Release를 만들고, CHANGELOG의 `[Unreleased]`를 버전 절로 승격해 릴리스 노트를 쓴다.
4. 다른 팀의 릴리스를 README만 보고 새 폴더에서 10분 안에 재현하고, 막힌 곳을 환경·명령·출력이 있는 Issue로 보고한다.
5. 받은 Issue를 triage 라벨로 분류하고, 재현 시도 결과와 수용·보류·거절 결정을 근거와 함께 `DECISIONS.md`에 기록한다.
6. 문제 → 시연 → 한계 → 다음 순서의 3분 시연을 구성하고 리허설 시간을 측정해 15주차 발표를 준비한다.

## 누적 결과물

이번 주 실습은 4차 종합과제(15주차, 최종 오픈소스 릴리스 패키지)의 "릴리스 태그·문서 세트·출처와 라이선스 목록·피드백 반영 근거" 항목을 채운다. 13주차에 pytest·ruff·CI가 초록불이 된 팀 저장소를 `v0.1.0`으로 릴리스하고, 다른 팀의 교차 재현 Issue와 그에 대한 응답·결정 기록이 15주차 발표와 기말 재현 검증의 재료가 된다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 릴리스 문서 세트: README 8개 절(무엇·왜·설치·실행·예시·제한·라이선스·출처), LICENSE 재확인(의존성·모델·데이터 라이선스 호환), CONTRIBUTING, Model Card(어댑터 공개 시), CHANGELOG(Keep a Changelog), CITATION.cff, AI 도구 사용 내역 표기, `release_check.py` 시연 | 릴리스 문서 세트 보완: 팀 README·Model Card를 점검표로 보완 → `SOURCES.md` 최종화 → CHANGELOG `[Unreleased]` 정리 | `outputs/release-check-*.json`(FAIL 0), `docs/release_checklist.md`, 보완 commit |
| 2교시 | 버전과 릴리스: SemVer, `git tag -a`, GitHub Release와 릴리스 노트, 깨끗한 폴더에서 `uv sync --frozen`으로 재현 절차 검증, 릴리스 후 고칠 때(패치 버전), 모델·어댑터 산출물 배포(Release asset·Hub 업로드 개념) | 릴리스 생성과 교차 재현: `v0.1.0` 태그·릴리스 생성 → 짝 팀 릴리스를 README만 보고 10분 안에 재현 → 재현 실패 항목을 Issue로 등록 | 릴리스 URL, `docs/repro/repro-log-*.md`, 교차 재현 Issue URL |
| 3교시 | 커뮤니티 피드백과 시연 준비: Issue 분류(triage 라벨 5개), 응답 예절·기대 관리, 재현 불가 보고 요청법, 피드백 반영 결정 기록, 3분 시연 구성(문제→시연→한계→다음), 질의 예상 | 피드백 응답과 시연 리허설: 교차 피드백 Issue 2건 작성·응답·라벨 → `DECISIONS.md` 기록 → 3분 시연 리허설 2회 측정 | 피드백 Issue·응답 URL, `DECISIONS.md`, `docs/demo_outline.md` 리허설 시간표 |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- 13주차까지 누적된 팀 저장소 clone본(pytest·ruff·CI 통과 상태). 9주차 템플릿의 LICENSE·CONTRIBUTING·CODE_OF_CONDUCT, 5·8주차의 `SOURCES.md`, 10·11주차의 실험 기록·데이터 카드·평가 결과가 들어 있어야 한다.
- GitHub 계정, 팀 저장소 쓰기 권한, 짝 팀(교차 재현 대상) 지정. 짝 팀 저장소에는 Issue만 남기고 push하지 않는다.
- Git, VS Code, uv, PowerShell. 이번 주 예제는 모델·GPU 없이 동작한다. Ollama와 사전 캐시된 모델은 3교시 시연 리허설에서만 쓴다(`ollama list`로 확인, 실습 시간에 내려받지 않는다).
- 이번 주 [`examples/`](examples/README.md)의 `release_kit/` 템플릿과 `release_check/` 도구 복사본.
- 정확한 도구 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 릴리스 노트·Issue·리허설 기록에 실제 이름, 학번, 토큰, 홈 경로를 넣지 않는다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다. `.env`는 릴리스에 포함하지 않고 `.env.example`만 둔다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): 릴리스 키트 템플릿(README·Model Card·CHANGELOG·CITATION.cff·점검표·교차 재현 절차·피드백 Issue 양식·triage 라벨·시연 개요)과 릴리스 점검 도구 `release_check/`
- 강의 대본: 강의자 별도 관리(비공개)

## 권장 진행 방식

1. 문서를 고치기 전에 `release_check.py`를 먼저 돌려 FAIL 목록을 예상과 비교한다. 도구는 "있다"만 보고 "맞다"는 사람이 본다.
2. README의 설치·실행 명령은 새 PowerShell 창에서 복사·붙여넣기로 한 번 실행해 본 뒤 commit한다.
3. 태그는 push하기 전에만 지운다. push한 태그는 옮기지 않고 고친 뒤 패치 버전을 낸다.
4. 다른 팀 릴리스를 재현할 때는 그 팀에 아무것도 묻지 않는다. 막힌 곳이 README의 결함이며 그것이 Issue가 된다.
5. Issue에는 사람이 아니라 동작에 대해 쓴다. 수용·보류·거절 어느 쪽이든 근거를 `DECISIONS.md`에 남긴다.

## 완료 기준

- [ ] `release_check.py` 결과에 FAIL이 없고, 남은 WARN마다 이유를 `docs/release_checklist.md`에 적었다.
- [ ] README 8개 절과 AI 도구 사용 내역 표가 있으며 설치·실행 명령이 새 창에서 동작했다.
- [ ] `SOURCES.md` 모든 행에 라이선스·SPDX ID·URL이 있고, 가장 제한적인 조건이 README 「제한」 절에 있다.
- [ ] CHANGELOG `[Unreleased]`가 `[0.1.0]` 절로 승격되었고, `pyproject.toml`·CITATION.cff·태그의 버전이 같다.
- [ ] `v0.1.0` 주석 태그가 push되고 GitHub Release에 릴리스 노트가 있다.
- [ ] 짝 팀 릴리스를 새 폴더에서 재현한 `repro-log-*.md`가 있고, 막힌 단계마다 Issue를 등록했다.
- [ ] 받은 Issue 2건 이상에 라벨·재현 시도 결과·응답이 있고 `DECISIONS.md`에 결정과 근거가 있다.
- [ ] 3분 시연 리허설 2회의 구간별 시간이 `docs/demo_outline.md`에 있고 2회차가 3분 30초 이내다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 개인 저장소(또는 팀 저장소 `docs/`)에 누적한다.

1. `outputs/release-check-*.json`과 `docs/release_checklist.md`, 문서 보완 commit id
2. 릴리스 URL, `git show v0.1.0 --stat` 출력 첫 8줄, 태그가 가리키는 commit id
3. `docs/repro/repro-log-*.md`와 짝 팀 저장소에 등록한 Issue URL
4. 우리 팀이 받은 Issue의 응답 URL과 `DECISIONS.md`
5. `docs/demo_outline.md`의 리허설 시간표(2회)

터미널 출력과 기록에는 사용자 홈 경로가 포함될 수 있다. 붙여넣기 전에 개인 식별 정보가 없는지 확인한다.

## 다음 주 연결

15주차(`week15_final_presentation`)에서는 이번 주 릴리스 태그가 가리키는 기준본으로 팀당 시연 3분 + 질의 2분의 최종 발표를 하고, 다른 팀 저장소를 평가자 체크리스트로 검증하며, 4차 종합과제를 제출한다. 교차 재현 Issue 중 수용한 것을 고쳤다면 발표 전에 패치 태그(`v0.1.1`)를 찍어 기준본을 다시 확정한다.

## 참고 자료

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Citation File Format](https://citation-file-format.github.io/)
- [GitHub Docs — About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [GitHub Docs — Managing labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
- [Hugging Face Hub — Model Cards](https://huggingface.co/docs/hub/model-cards)
- [Open Source Guides — Best Practices for Maintainers](https://opensource.guide/best-practices/)
