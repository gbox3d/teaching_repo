# 2주차 — GitHub와 공개 배포

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week02_github_pages

## 이번 주 질문

> 내 컴퓨터에만 있는 페이지를 GitHub에 올려 누구나 여는 주소를 만들고, 다른 내용은 브랜치로 따로 올릴 수 있을까?

1주차에는 `index.html`·`styles.css`·`app.js` 세 파일을 만들고 내 컴퓨터에서 `git init → git add → git commit`까지 해 보았다.
이번 주에는 그 저장소를 GitHub에 올리고(push) GitHub Pages로 공개 주소를 만든다.
2일차에는 브랜치를 만들어 소개 페이지를 따로 올린 뒤 main에 합친다.

## 학습 목표

1. GitHub 계정과 빈 저장소 `my-web`을 만들고, 내 저장소에 `git remote add origin <HTTPS URL>`로 주소를 적는다.
2. `git push -u origin main`으로 commit을 올리고, 처음 push 때 브라우저 로그인을 마친다.
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

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | GitHub 계정·빈 저장소, remote와 `origin`, 첫 push와 브라우저 로그인, 고치고 push, Pages 켜기 | 세 파일 준비 → 빈 저장소 → push → 제목 고쳐 push → Pages → 공개 URL | 캡처 1·2 |
| 2일차 | 브랜치는 따로 올리는 작업선, `branch`·`switch`, about.html commit, `push -u origin about`, `merge` → push, 브랜치 삭제 | about 브랜치 → about.html·링크 → push → GitHub에서 브랜치 비교 → merge → 공개 페이지 확인 | 캡처 3·4 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 새 폴더 `my-web`에 [따라하기 2단계](walkthrough.md#2-세-파일-만들기)의 세 파일을 만든다 (1주차 파일을 복사해 와도 되지만 `<h1>`은 `내 첫 페이지`로 둔다)
- Git (`git --version`으로 확인), VS Code, 브라우저
- 이메일 주소 (GitHub 계정 만들기와 확인 메일에 쓴다)
- 공개 저장소와 공개 페이지에는 실명·학번·전화번호를 넣지 않는다. 예시 아이디는 `student01`, 저장소 이름은 `my-web`이다.

## 이번 주 범위

| 명령·용어 | 이번 주에 알아둘 뜻 |
|---|---|
| GitHub | Git 저장소를 인터넷에 올려 두는 서비스. Git(도구)과 다른 것이다 |
| remote / `origin` | 내 저장소가 기억하는 인터넷 저장소 주소. 첫 remote의 이름은 관례로 `origin` |
| `git remote add origin <URL>` | GitHub 저장소 주소를 `origin`이라는 이름으로 적어 둔다. 아직 아무것도 보내지 않는다 |
| `git remote -v` | 적어 둔 주소를 확인한다 |
| `git add .` | 폴더 안에서 바뀐 파일을 모두 다음 commit에 넣는다 |
| `git push -u origin main` | main 브랜치의 commit을 `origin`으로 올린다. `-u`는 다음부터 `git push`만 쳐도 되게 기억한다 |
| 브라우저 로그인 | 처음 push 때 Git Credential Manager가 브라우저를 열어 GitHub 로그인을 받는다. 비밀번호나 토큰을 명령에 적지 않는다 |
| GitHub Pages | 저장소의 HTML 파일을 그대로 웹 주소로 보여 주는 기능. 주소는 `https://<아이디>.github.io/<저장소>/` |
| 브랜치(branch) | 다른 내용을 따로 올리는 작업선. `main`은 처음부터 있는 기본 브랜치 |
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
- [ ] GitHub 브랜치 목록에 `about`이 보이고, about 브랜치에만 `about.html`이 있다.
- [ ] main에 merge한 뒤 공개 페이지의 `소개 페이지 보기` 링크가 동작한다.
- [ ] 캡처 4장을 제출한다.

## 다음 수업 연결

이제 `git add → commit → push` 한 번이면 공개 페이지가 바뀐다. 3주차부터는 이 `my-web` 저장소에 페이지를 늘려 가며
시맨틱 HTML과 form을 배운다. 매주 결과는 같은 공개 주소 `https://<아이디>.github.io/my-web/`에서 확인한다.

## 공식 참고 자료

- [GitHub 계정 만들기 — GitHub Docs](https://docs.github.com/ko/get-started/start-your-journey/creating-an-account-on-github)
- [새 리포지토리 만들기 — GitHub Docs](https://docs.github.com/ko/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [원격 리포지토리 정보 — GitHub Docs](https://docs.github.com/ko/get-started/git-basics/about-remote-repositories)
- [원격 리포지토리 관리 — GitHub Docs](https://docs.github.com/ko/get-started/git-basics/managing-remote-repositories)
- [Git에서 GitHub 자격 증명 캐싱 — GitHub Docs](https://docs.github.com/ko/get-started/git-basics/caching-your-github-credentials-in-git)
- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [GitHub Pages 사이트에 대한 게시 원본 구성 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [리포지토리의 브랜치 보기 — GitHub Docs](https://docs.github.com/ko/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/viewing-branches-in-your-repository)
- [리포지토리 내에서 분기 관리(브랜치 삭제) — GitHub Docs](https://docs.github.com/ko/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository)
- [비빠른 선행 오류 처리 — GitHub Docs](https://docs.github.com/ko/get-started/using-git/dealing-with-non-fast-forward-errors) (다른 PC에서 이어 할 때)
- [새 SSH 키 생성 및 ssh-agent에 추가 — GitHub Docs](https://docs.github.com/ko/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) (강의자 시연·선택)
