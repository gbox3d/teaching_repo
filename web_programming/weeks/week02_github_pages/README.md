# 2주차 — GitHub와 공개 배포

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week02_github_pages

## 이번 주 작업

내 컴퓨터의 commit을 GitHub에 올리고 공개 주소를 만든다. 소개 페이지는 about 브랜치에서 작업한 뒤 main에 합친다.

1주차에는 `index.html`·`styles.css`·`app.js` 세 파일을 만들고 내 컴퓨터에서 `git init → git add → git commit`까지 해 보았다.
이번 주에는 그 저장소를 GitHub에 올리고(push) GitHub Pages로 공개 주소를 만든다.
2일차에는 브랜치를 만들어 소개 페이지를 따로 올린 뒤 main에 합친다.

## 학습 목표

1. 사전 준비한 GitHub 계정에서 빈 저장소 `my-web`을 만들고, 내 저장소에 `git remote add origin <HTTPS URL>`로 주소를 적는다.
2. `git push -u origin main`으로 commit을 올리고, 인증이 필요하면 브라우저 로그인을 마친다.
3. 파일을 고쳐 `add → commit → push` 하면 GitHub 화면이 바뀌는 것을 확인한다.
4. **Settings › Pages**에서 main 브랜치를 배포해 `https://<아이디>.github.io/my-web/`을 연다.
5. `git branch about`·`git switch about`으로 브랜치를 만들어 `about.html`을 따로 push하고, main에서 `git merge about`으로 합쳐 공개 페이지에 반영한다.

## 이번 주 결과물

```text
[캡처 1] github.com/student01/my-web ─ app.js · index.html · styles.css
[캡처 2] https://student01.github.io/my-web/ ─ "내 첫 GitHub 페이지"
[캡처 3] github.com/student01/my-web 의 브랜치 목록 ─ main · about
[캡처 4] https://student01.github.io/my-web/about.html ─ "소개"
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 마지막에는 캡처 4장을 제출한다.

## 2일 수업 흐름

| 일차 | 강의·시연 60분 | 개별 실습 30분 | 결과 |
|---|---|---|---|
| 1일차 | 준비 5, GitHub·remote 15, 첫 push 15, Pages 15, 공개 경로 5, 안내 5 | `my-web` 준비 5, push 10, 제목 변경·push 5, Pages·캡처 10 | 캡처 1·2 |
| 2일차 | 준비 5, branch·switch 15, 파일 추가 10, merge 15, Pages 비교 10, 안내 5 | about 브랜치 5, 제공 HTML의 소개·왕복 링크 10, commit·push·merge 10, 확인 5 | 캡처 3·4 |

Git과 Pages 자체가 학습 목표인 2주는 push·branch·merge를 수업 안에서 수행한다. 강의자는 먼저 완성 파일과 명령 결과를 시연하고, 학생은 뒤의 30분에 아래 필수 범위만 수행한다. 시간은 설계값이며 학생 실측값이 아니다.

## 준비와 실습 범위

사전 준비는 VS Code·Git·브라우저 설치와 GitHub 계정·이메일 확인, 1주 세 파일과 이번 주 제공 파일 확보다. 새 저장소 생성·첫 push·Pages 설정은 수업 안에서 한다. 강의 첫 5분에 파일과 로그인 가능 여부를 확인한다. 계정 문제는 강의자의 준비 지원으로 처리한다.

| 구분 | 수행 범위 |
|---|---|
| 학생 필수 1일차 | 1주 파일 또는 배부한 세 파일을 `my-web`에 복사하고 로컬 commit, 빈 원격 저장소·push, 제목 한 줄 변경·push, Pages 확인 |
| 학생 필수 2일차 | about 브랜치 생성, 제공 `about.html`의 소개 한 줄 수정·왕복 링크 확인, commit·push·merge, 두 페이지 확인 |
| 강의자 시연 | 전체 HTML/CSS/JS 읽기, remote·인증·배포 지연, merge 전후 파일 비교 |
| 선택·수업 뒤 연습 | 브랜치 삭제, clone·pull, SSH, 추가 페이지·CSS 변경 |

세 파일과 소개 HTML을 처음부터 모두 타이핑하지 않는다. [따라하기](walkthrough.md)의 전문은 복구·비교용이다. 방문 횟수 JS와 기초 CSS는 제공 코드이며 이번 주 작성 대상이 아니다. W3.CSS는 7주에 소개한다.

공개 저장소와 페이지에는 실명·학번·전화번호를 넣지 않는다. 예시 아이디는 `student01`, 저장소 이름은 `my-web`이다. commit 이메일에는 GitHub의 비공개 이메일 설정에서 확인한 noreply 주소를 쓸 수 있다.

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 저장소 | repository | 仓库 |
| 원격 저장소 | remote (origin) | 远程仓库 |
| 올리기 | push | 推送 |
| 받아오기 | pull | 拉取 |
| 복제하기 | clone | 克隆 |
| 브랜치 | branch | 分支 |
| 합치기 | merge | 合并 |
| 공개 웹 주소 | GitHub Pages | GitHub Pages（网页发布） |

## 이번 주 범위

| 명령·용어 | 이번 주에 알아둘 뜻 |
|---|---|
| GitHub | Git 저장소를 인터넷에 올려 두는 서비스. Git(도구)과 다른 것이다 |
| remote / `origin` | 내 저장소가 기억하는 인터넷 저장소 주소. 첫 remote의 이름은 관례로 `origin` |
| `git remote add origin <URL>` | GitHub 저장소 주소를 `origin`이라는 이름으로 적어 둔다. 아직 아무것도 보내지 않는다 |
| `git remote -v` | 적어 둔 주소를 확인한다 |
| `git add .` | 폴더 안에서 바뀐 파일을 모두 다음 commit에 넣는다 |
| `git push -u origin main` | main 브랜치의 commit을 `origin`으로 올린다. `-u`는 다음부터 `git push`만 쳐도 되게 기억한다 |
| 브라우저 로그인 | Git Credential Manager가 설정된 PC에서는 인증이 필요할 때 브라우저 로그인을 진행한다. 비밀번호나 토큰을 명령에 적지 않는다 |
| GitHub Pages | 저장소의 HTML 파일을 그대로 웹 주소로 보여 주는 기능. 주소는 `https://<아이디>.github.io/<저장소>/` |
| 브랜치(branch) | 다른 내용을 따로 올리는 작업선. 이번 실습은 `git branch -M main`으로 기본 브랜치 이름을 정한다 |
| `git branch about` / `git switch about` | about 브랜치를 만든다 / about 브랜치로 옮겨 간다 |
| `git branch` | 브랜치 목록. `*`가 지금 있는 브랜치 |
| `git push -u origin about` | about 브랜치를 GitHub에 따로 올린다. main에는 아직 없다 |
| `git merge about` | 지금 있는 브랜치(main)에 about의 commit을 가져와 합친다 |
| `git branch -d about` | 합친 뒤 필요 없는 브랜치를 지운다 |
| `git clone <URL>` / `git pull` (확장) | 다른 PC에서 이어 할 때 저장소를 내려받는다 / 새 commit을 가져온다 |

충돌(conflict), fork와 Pull Request, SSH 키, GitHub Actions는 이번 주에 다루지 않는다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week02_github_pages/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [index.html](examples/day1/index.html) · [styles.css](examples/day1/styles.css) · [app.js](examples/day1/app.js)
- 2일차 완성 코드: [index.html](examples/day2/index.html) · [about.html](examples/day2/about.html) · [styles.css](examples/day2/styles.css) · [app.js](examples/day2/app.js)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week02_github_pages

## 완료 기준

- [ ] GitHub 저장소 `my-web`에 `index.html`·`styles.css`·`app.js` 세 파일이 보인다.
- [ ] `https://<아이디>.github.io/my-web/`에서 `내 첫 GitHub 페이지`가 열린다.
- [ ] merge 전에 main에는 `about.html`이 없고 about에는 있는 것을 비교하고 캡처 3을 저장했다.
- [ ] main에 merge한 뒤 공개 페이지의 `소개 페이지 보기` 링크가 동작한다.
- [ ] 캡처 4장을 제출한다. 2주는 일반 주차와 달리 네 장을 유지한다. Pages가 실습 중 배포되지 않으면 로컬 화면과 GitHub commit 증거로 먼저 확인하고, 배포 뒤 공개 화면을 보완한다.

## 다음 수업 연결

3주 시작 자료는 이번 주 `day2/`와 같은 `index.html`·`about.html`·`styles.css`·`app.js`다. main에 합친 상태와 왕복 링크를 보존한다. 3주에는 main에서 시맨틱 HTML과 정적 방명록 폼을 수정하며 새 브랜치 학습을 반복하지 않는다. CSS·JS 파일은 보존하고 HTML의 연결만 해제한다.

3주부터 배부 파일·새 주차 폴더 준비는 수업 전에 마치고, 학생 실습 30분은 코드 수정·로컬 확인·캡처에 쓴다. GitHub 업로드는 수업 뒤 정리다. `my-web` 공개 주소는 유지한다.

## 공식 참고 자료

2026-11-18에 공식 문서의 저장소 생성·GCM 인증·Pages 게시 원본을 확인했다. UI 문구는 언어·화면 버전에 따라 달라질 수 있다. Pages 반영에는 최대 10분이 걸릴 수 있으며 1분 완료를 보장하지 않는다.

- [commit 이메일과 noreply 주소 설정 — GitHub Docs](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address)
- [GitHub 계정 만들기 — GitHub Docs](https://docs.github.com/ko/get-started/start-your-journey/creating-an-account-on-github)
- [새 리포지토리 만들기 — GitHub Docs](https://docs.github.com/ko/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [원격 리포지토리 정보 — GitHub Docs](https://docs.github.com/ko/get-started/git-basics/about-remote-repositories)
- [원격 리포지토리 관리 — GitHub Docs](https://docs.github.com/ko/get-started/git-basics/managing-remote-repositories)
- [Git에서 GitHub 자격 증명 캐싱 — GitHub Docs](https://docs.github.com/ko/get-started/git-basics/caching-your-github-credentials-in-git)
- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [GitHub Pages 게시 원본 구성 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [리포지토리의 브랜치 보기 — GitHub Docs](https://docs.github.com/ko/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/viewing-branches-in-your-repository)
- [리포지토리 내에서 분기 관리(브랜치 삭제) — GitHub Docs](https://docs.github.com/ko/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository)
- [비빠른 선행 오류 처리 — GitHub Docs](https://docs.github.com/ko/get-started/using-git/dealing-with-non-fast-forward-errors) (다른 PC에서 이어 할 때)
- [새 SSH 키 생성 및 ssh-agent에 추가 — GitHub Docs](https://docs.github.com/ko/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) (강의자 시연·선택)
