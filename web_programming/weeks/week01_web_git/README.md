# 1주차 — 웹 실행 구조와 Git 상태

## 이번 주 질문

> 브라우저에 보이는 한 화면은 어디에서 왔으며, 내가 수정한 파일은 지금 Git의 어느 상태에 있는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. URL을 구성하는 scheme, host, port, path를 구분한다.
2. HTTP 요청과 응답을 브라우저 DevTools의 Network 탭에서 찾는다.
3. HTML, CSS, JavaScript의 역할을 각각 구조, 표현, 동작으로 설명한다.
4. working tree, staging area(index), commit(HEAD)의 차이를 파일 상태로 설명한다.
5. `status → diff → add → diff --staged → commit → log` 순환을 직접 수행한다.
6. 한 커밋에 한 가지 의도를 담고, 결과와 실패 원인을 짧게 기록한다.

## 수업 흐름

| 일차 | 설명·시연 30분 | 직접 해결 실습 60분 | 핵심 증거 |
|---|---|---|---|
| 1일차 | URL·HTTP, HTML/CSS/JS, DevTools | 최소 페이지를 실행하고 요청·요소·콘솔을 관찰 | 관찰표와 오류 설명 |
| 2일차 | Git의 세 영역과 diff 읽기 | 페이지를 세 의도로 나누어 변경·커밋 | commit 3개와 상태 회고 |

## 준비물

- 최신 Chromium 계열 브라우저
- Git (`git --version`으로 확인)
- Node.js LTS (`node --version`으로 확인)
- VS Code 또는 다른 텍스트 편집기
- 터미널에서 현재 경로를 확인하는 습관

실제 이름, 학번, 전화번호, 비밀번호나 API key는 실습 파일과 공개 저장소에 넣지 않는다. 표시 이름은 `student01` 같은 수업용 값을 사용한다.

## 자료 안내

- [PT 원고](slides.md): 두 번의 30분 설명·시연용 Marp 자료
- [따라하기 절차](walkthrough.md): 시연·실습을 단계대로 재현하는 절차서
- 강의 대본: 강의자 별도 관리(비공개)
- [실습지](lab.md): 1·2일차 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): 작은 웹 페이지와 로컬 HTTP 서버

## 권장 진행 방식

1. 실습 문제의 완료 조건을 먼저 읽는다.
2. 코드를 실행하기 전에 결과와 Git 상태를 예상한다.
3. DevTools 또는 Git 명령으로 예상과 실제를 비교한다.
4. 오류 메시지를 복사하기보다 어느 계층의 문제인지 설명한다.
5. 기본 문제를 완료한 뒤에만 확장 문제를 수행한다.

## 완료 기준

- [ ] `http://localhost:8000/`에서 예제를 열었다.
- [ ] Network 탭에서 문서, CSS, JavaScript 요청을 각각 찾았다.
- [ ] Elements에서 HTML 요소와 적용된 CSS를 찾았다.
- [ ] Console에서 JavaScript 실행 결과와 의도적인 오류를 구분했다.
- [ ] 별도의 개인 연습 저장소에 의미 있는 commit 3개를 만들었다.
- [ ] `git status`가 최종적으로 `working tree clean`임을 확인했다.
- [ ] working tree, stage, commit을 자기 말로 설명한 5문장을 작성했다.

## 제출 증거

1. 개인 연습 저장소 경로 또는 저장소 URL
2. `git log --oneline --decorate -3` 결과
3. DevTools 관찰표
4. 상태 변화 5문장 회고

터미널 출력에는 사용자 홈 경로가 포함될 수 있다. 제출 캡처 전에 개인 식별 정보가 없는지 확인한다.

## 다음 주 연결

이번 주의 local repository와 commit을 다음 주 remote, push, branch, GitHub Pages로 확장한다. 다음 수업 전 GitHub 계정을 확인하고 공개 프로필에 불필요한 개인정보가 없는지 점검한다.

## 참고 자료

- [Git `status` 공식 문서](https://git-scm.com/docs/git-status)
- [Git `diff` 공식 문서](https://git-scm.com/docs/git-diff)
- [Git `restore` 공식 문서](https://git-scm.com/docs/git-restore)
