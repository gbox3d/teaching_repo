# 2주차 — Git/GitHub 협업과 라이선스

## 이번 주 질문

> 내 변경을 다른 사람의 저장소에 안전하게 제안하고, 그 코드를 어떤 조건으로 쓰고 나눌 수 있는지 어떻게 판단하는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 로컬 저장소를 GitHub 원격과 연결하고 `push`, `fetch`, `pull`이 각각 어떤 참조를 바꾸는지 구분한다.
2. branch에서 작업한 변경을 merge하고, 같은 줄이 충돌했을 때 마커를 읽어 결과를 직접 작성한다.
3. Fork → Issue → Branch → Pull Request → Review → Merge 순서로 쓰기 권한이 없는 저장소에 변경을 제안한다.
4. PR 템플릿을 채우고, 코드에 대한 구체적인 리뷰 코멘트를 남기며, 수정 요청에 commit으로 답한다.
5. permissive와 copyleft 라이선스의 의무를 구분하고 호환성 방향을 판단한다.
6. 코드·모델·데이터의 라이선스를 SPDX ID와 출처 URL로 표에 기록하고 개인 저장소의 LICENSE를 고른다.

## 누적 결과물

이번 주에 만드는 GitHub 원격 저장소, Issue·PR·리뷰 코멘트 URL, `LICENSE`, `license_matrix.md`는 4주차 **1차 종합과제**(협업 저장소 + Ollama 클라이언트)의 "협업 근거"와 "라이선스·출처" 항목을 직접 채운다. `license_matrix.md`는 8주차 2차 종합과제에서 모델·데이터 항목을 늘려 라이선스 분석 보고로 확장한다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 브랜치·원격·충돌 해결 — Git 세 영역 복습, branch·merge·충돌, clone/push/pull/fetch, 커밋 메시지 규약 | 원격 연결과 충돌 1회 해결 — 개인 저장소 push, `feature/readme` 브랜치, 같은 줄 충돌 재현·해결, graph 확인 | 해결된 충돌 merge commit, `git log --graph --oneline --all` 출력 |
| 2교시 | GitHub 협업 흐름과 리뷰 — Fork → Issue → Branch → PR → Review → Merge, 작은 PR, PR 설명 양식, 리뷰 예절, Draft PR, 이슈 템플릿 | 짝 저장소에 제안하고 리뷰 받기 — Issue 등록, fork, 브랜치, 템플릿 채운 PR, 리뷰 코멘트·수정 요청, 수정 push, merge | 본인이 올린 PR URL, 본인이 남긴 리뷰 코멘트 URL |
| 3교시 | 라이선스 읽기와 고르기 — 저작권과 라이선스, permissive·copyleft, 특허 조항, 호환성 방향, 모델·데이터 라이선스, 라이선스 없음 = 사용 불가 | 라이선스 판별과 LICENSE 추가 — 판별 카드 10문항, `LICENSE` 선택·commit, `license_matrix.md` 작성 | `LICENSE` commit, `license_matrix.md` |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- 1주차 3교시에 만든 개인 연습 저장소(첫 commit이 있는 로컬 Git 저장소. 1주차 실습지의 예시 경로는 `C:\classwork\osa-week01`). 폴더 이름은 각자 달라도 되며, 이번 주부터 문서는 이 저장소를 `osa-practice`라고 부른다. 없으면 실습지의 준비 절차대로 새로 만든다.
- GitHub 계정(이메일 인증 완료)과 브라우저 로그인. 2교시는 2인 1조이므로 짝의 GitHub 계정 이름을 미리 확인한다.
- Git, VS Code, PowerShell. 이번 주는 GPU·모델·Python 실행이 필요 없다.
- Git 인증은 브라우저 로그인 또는 강의자가 정한 credential manager로 한다. 토큰을 명령이나 URL에 직접 적지 않는다.
- 정확한 도구 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 저장소·Issue·PR·표·캡처에 학번, 전화번호, 비밀번호, 토큰을 넣지 않는다. commit 작성자와 저작권자 표기는 GitHub 계정 이름으로 충분하다. 실습 문서의 표시 이름은 `student01`, 짝은 `student02` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): PR·Issue 템플릿, CONTRIBUTING 예시, 라이선스 판별 카드, 라이선스 표 양식, 충돌 재현 스크립트
- 강의 대본: 강의자 별도 관리(비공개)

## 권장 진행 방식

1. 각 교시 실습의 완료 조건을 먼저 읽고, 명령을 실행하기 전에 결과(graph 모양, PR 상태, 판별 결과)를 예상해 적는다.
2. Git 명령은 `git status`로 현재 branch와 상태를 확인한 뒤 실행한다. 되돌리는 명령(`--abort`, `restore`)은 대상과 범위를 말할 수 있을 때만 쓴다.
3. 2교시는 짝과 제안자·리뷰어 역할을 동시에 수행한다. 한쪽이 기다리게 되면 상대의 PR을 리뷰한다.
4. 라이선스 판단은 "가능·조건부·불가" 중 하나를 고르고 근거가 되는 조항의 핵심 단어와 출처 URL을 적는다. 검색 결과 요약이 아니라 라이선스 원문·모델 카드를 근거로 삼는다.
5. 기본 문제를 완료한 뒤에만 확장 문제를 수행한다.

## 완료 기준

- [ ] 개인 저장소가 GitHub 원격과 연결되어 `git branch -vv`에서 `main`이 `origin/main`을 추적한다.
- [ ] 같은 줄을 다르게 고친 두 branch를 merge해 충돌을 재현하고, 마커 없는 결과로 merge commit을 만들었다.
- [ ] 짝 저장소에 Issue 1개와 PR 템플릿을 채운 PR 1개를 올렸다.
- [ ] 짝의 PR에 줄 단위 리뷰 코멘트 1개 이상과 수정 요청을 남기고, 수정 push 뒤 merge를 확인했다.
- [ ] 라이선스 판별 카드 10문항에 판단과 근거를 적었다.
- [ ] 개인 저장소에 `LICENSE`(MIT 또는 Apache-2.0)와 선택 이유 1문장을 commit·push했다.
- [ ] `license_matrix.md`에 코드·모델·데이터 항목 5개 이상을 SPDX ID·상업적 이용·재배포 조건·출처 URL로 채웠다.
- [ ] 저장소·Issue·PR·표에 비밀번호, 토큰, 학번, 전화번호가 없다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 개인 저장소에 누적한다.

1. 개인 저장소 URL과 `git log --graph --oneline --all` 출력(충돌 해결 merge commit 포함)
2. 본인이 올린 Issue·PR URL과 본인이 남긴 리뷰 코멘트 URL(`notes/week02_links.md`에 기록)
3. `LICENSE` 파일과 README의 선택 이유 1문장
4. `license_matrix.md`(5행 이상)
5. `license_cards_answers.md`(10문항 판단·근거·출처)

## 다음 주 연결

3주차 `week03_reproducible_python`에서는 이번 주에 GitHub와 연결하고 LICENSE를 넣은 이 개인 저장소를 uv 기반의 재현 가능한 Python 프로젝트 구조(`pyproject.toml`, `uv.lock`, `.gitignore`, `.env.example`)로 바꾼다. 다음 수업 전에 `uv --version`이 동작하는지 확인하고, 이번 주 Issue·PR·리뷰 URL이 `notes/week02_links.md`에 정리되어 있는지 점검한다.

## 참고 자료

- [Git — git-merge](https://git-scm.com/docs/git-merge)
- [GitHub Docs — About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- [Choose a License](https://choosealicense.com/)
- [OSI — Licenses](https://opensource.org/licenses)
- [SPDX License List](https://spdx.org/licenses/)
- [Creative Commons — About CC Licenses](https://creativecommons.org/share-your-work/cclicenses/)
