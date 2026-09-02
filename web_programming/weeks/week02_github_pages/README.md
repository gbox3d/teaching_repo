# 2주차 — GitHub와 GitHub Pages

## 이번 주 질문

> 내 컴퓨터의 commit은 원격 저장소와 어떻게 연결되며, 로컬에서 보이던 페이지가 공개 URL에서 깨지는 이유는 무엇인가?

## 학습 목표

1. local repository, remote repository, branch, upstream의 관계를 설명한다.
2. `fetch`, `pull`, `push`가 어느 방향으로 어떤 참조를 바꾸는지 구분한다.
3. 두 branch의 독립 변경을 merge하고 conflict marker를 읽어 해결한다.
4. GitHub Pages의 publishing source와 entry file을 확인한다.
5. project site URL의 repository base path를 고려해 상대경로를 작성한다.
6. 404, 대소문자, 캐시, 배포 지연 문제를 Network와 Actions 기록으로 진단한다.

## 수업 흐름

| 일차 | 설명·시연 30분 | 직접 해결 실습 60분 | 결과물 |
|---|---|---|---|
| 1일차 | remote, tracking branch, branch·merge·conflict | 두 branch를 만들고 충돌을 해결한 뒤 push | branch 이력과 merge/conflict commit |
| 2일차 | Pages source, project URL, 경로 진단 | 랜딩 페이지를 배포하고 의도적 오류를 수정 | 공개 URL과 오류 해결표 |

## 준비와 안전

- GitHub 계정, Git, 브라우저, 편집기
- 공개 저장소에는 수업용 가상 데이터만 사용한다.
- 비밀번호, personal access token, API secret, 실제 개인정보를 파일·캡처·commit에 남기지 않는다.
- GitHub Pages는 공개 웹사이트다. 저장소 공개 범위와 무관하게 민감 정보를 게시하지 않는다.
- 인증이 필요하면 브라우저 또는 강의자가 정한 credential manager를 사용하고 토큰을 명령에 직접 적지 않는다.

## 자료 안내

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습지](lab.md)
- [배포 예제](examples/README.md)

## 핵심 상태도

```text
working tree → stage → local commit ── push ──▶ origin의 branch
                                      ◀─ fetch ── origin 추적 참조

main ──┬── layout-a ── commit A ──┐
       └── layout-b ── commit B ──┴── merge 또는 conflict 해결
```

## 완료 기준

- [ ] `git remote -v`의 fetch/push 대상을 설명했다.
- [ ] 두 branch가 같은 기준 commit에서 갈라진 것을 log graph로 확인했다.
- [ ] conflict marker의 ours/theirs 내용을 비교해 의도적으로 결과를 작성했다.
- [ ] Pages publishing source를 `main`의 `/(root)`로 설정했다.
- [ ] 공개 project site URL에서 HTML, CSS, JS, 이미지가 모두 200이다.
- [ ] 로컬에서는 보이지만 Pages에서는 실패하는 경로 오류 한 개를 재현·수정했다.
- [ ] 저장소 URL, Pages URL, 해결 commit, 오류 원인표를 제출할 수 있다.

## 공식 참고

- [GitHub Pages 사이트 만들기](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [Publishing source 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GitHub Pages 개요](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

GitHub의 화면 이름과 무료 정책은 바뀔 수 있다. 개강 시점에는 위 공식 문서와 실제 강의용 새 계정에서 다시 확인한다.

## 다음 주 연결

배포한 랜딩 페이지를 3주차부터 프로젝트의 목록·상세·작성 화면으로 발전시킨다. 다음 수업 전에 프로젝트 후보 주제 2개와 사용할 텍스트·이미지의 출처 후보를 정리한다.
