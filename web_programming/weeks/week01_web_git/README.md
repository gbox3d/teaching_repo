# 1주차 — 웹 실행 구조와 Git 상태

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week01_web_git

## 이번 주 질문

> 브라우저에 보이는 한 화면은 어떤 파일들로 만들어지며, 내가 고친 파일을 Git에 어떻게 기록할까?

이번 주에는 `index.html`·`styles.css`·`app.js` 세 파일로 작은 페이지를 만들어 브라우저로 열고,
내 PC의 연습 폴더에 `git init`부터 `git commit`까지 기록 세 개를 남긴다.
웹 서버는 설치하지 않는다. 페이지는 파일을 더블클릭해 `file://` 주소로 연다.

## 학습 목표

1. 주소(URL)를 scheme·host·port·path로 나눠 읽고, 내 PC 파일을 여는 `file://` 주소와 구별한다.
2. DevTools **Network**에서 요청 한 줄의 **Status**를 읽고 `200`과 `404`를 구분한다.
3. `index.html`(내용)·`styles.css`(모양)·`app.js`(동작) 세 파일의 역할을 말하고, VS Code에서 고쳐 브라우저에서 확인한다.
4. `git init` → `git config` → `git status` → `git add` → `git commit -m` → `git log --oneline` 순서로 commit 세 개를 남긴다.
5. `git status`에서 **untracked**와 **staged**를 구분해 읽는다.

## 이번 주 결과물

```text
[캡처 1 · 1일차] 왼쪽 창 : file:///…/week01/index.html ─ "안녕하세요, student01입니다"
                오른쪽 창 : 교재 사이트 + DevTools Network ─ Status 200 (document · stylesheet · script)
[캡처 2 · 2일차] 터미널   : git log --oneline ─ commit 3줄
                브라우저  : file:///…/week01-practice/index.html ─ "student01의 Git 연습"
```

`student01`은 예시 별칭이다. 본인 수업용 별칭으로 바꿔 쓴다. 제출물은 **캡처 2장**이며 다른 제출 파일은 없다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | URL 네 부분, 요청·응답과 200·404, 세 파일의 역할, VS Code로 고치기, DevTools 세 탭 | `week01` 폴더에 세 파일 → 브라우저로 열기 → 내 소개로 고치기 → 교재 사이트에서 200·404 보기 → CSS 이름 오류 한 번 | 캡처 1 |
| 2일차 | `git init`·`git branch -M main`, 세 영역과 `git status`, `git config`, `git add`·`git commit -m`, `git log --oneline` | `week01-practice` 폴더에서 commit 3개(제목 → 소개 문단과 링크 → 스타일과 스크립트 연결) | 캡처 2 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 다시 한다.

## 준비

- **VS Code** — **File › Open Folder**로 폴더를 열고, 왼쪽 탐색기의 **New File**로 파일을 만든다.
- **브라우저** — Chrome 등 최신 브라우저. DevTools는 `F12`(macOS는 `⌥⌘I`)로 연다.
- **Git** — 터미널에서 `git --version`으로 설치를 확인한다.
- 웹 서버·확장 프로그램은 이번 주에 쓰지 않는다.
- 실명·학번·전화번호·비밀번호는 파일과 캡처에 넣지 않는다. 표시 이름은 `student01` 같은 수업용 별칭을 쓴다.

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 주소 | URL | 网址 |
| 방식 / 서버 이름 / 창구 번호 / 파일 위치 | scheme / host / port / path | 协议 / 主机 / 端口 / 路径 |
| 내 PC 파일 주소 | `file://` | 本地文件 |
| 요청과 응답 | request / response | 请求与响应 |
| 상태 번호 | status code | 状态码 |
| 내용과 구조 | HTML | 结构 |
| 모양 | CSS | 样式 |
| 동작 | JavaScript | 行为 |

## 이번 주 범위

| 명령·개념 | 이번 주에 알아둘 뜻 |
|---|---|
| 주소 | 브라우저에 넣는 주소. scheme·host·port·path 네 부분으로 읽는다 |
| 방식 / 서버 이름 / 창구 번호 / 파일 위치 | `https://gbox3d.github.io:443/teaching_repo/webprg/index.html`의 네 부분 |
| 내 PC 파일 주소 | 파일을 더블클릭해 열 때의 주소. 서버를 거치지 않는다 |
| 요청과 응답 | 브라우저가 "이 주소의 파일을 주세요"라고 묻고, 서버가 상태 번호와 내용으로 답한다 |
| 상태 번호 | `200`은 찾아서 보냈다, `404`는 그 주소에 파일이 없다 |
| 내용과 구조 | `index.html`. 제목·문단·버튼 같은 내용 |
| 모양 | `styles.css`. 색·간격·카드 모양 |
| 동작 | `app.js`. 버튼을 누를 때 일어나는 일 |
| 개발자 도구 (DevTools) | Elements(화면의 HTML) · Console(메시지·오류) · Network(받은 파일과 Status) |
| 저장소 (repository) | 기록이 쌓이는 곳. `git init`이 만드는 `.git/` 폴더가 본체다 |
| `git init` / `git branch -M main` | 이 폴더를 저장소로 만들고 기본 브랜치 이름을 `main`으로 바꾼다 |
| `git config user.name` / `user.email` | 기록에 남을 이름과 이메일. `--global` 없이 쓰면 이 저장소에만 적용된다 |
| 추적 전 / 담아 둔 (untracked / staged) | `git status`에 나오는 두 상태. 아직 Git이 모르는 파일과 다음 commit에 담긴 내용 |
| `git add` / `git commit -m` | 다음 기록에 넣을 것을 고르고, 설명과 함께 기록으로 확정한다 |
| `git log --oneline` | 지금까지의 commit을 한 줄씩 본다 |

브랜치 **만들기**(`git branch <이름>`)와 `git push`·GitHub는 2주차에 다룬다. `git status`가 알려 주는 되돌리기 명령(`git rm --cached`·`git restore --staged`)은 이번 주에 **이름만 읽고 쓰지는 않는다**. `git branch -M main`은 브랜치 이름을 바꾸는 것이라 이번 주에 쓴다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week01_web_git/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [index.html](examples/day1/index.html) · [styles.css](examples/day1/styles.css) · [app.js](examples/day1/app.js)
- 2일차 완성 코드: [index.html](examples/day2/index.html) · [styles.css](examples/day2/styles.css) · [app.js](examples/day2/app.js)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week01_web_git

## 완료 기준

- [ ] `week01` 폴더의 세 파일이 브라우저에서 한 화면으로 열린다(카드 모양, 버튼을 누르면 숫자가 올라간다).
- [ ] `<h1>`과 소개 문단이 내 소개(수업용 별칭)로 바뀌어 있다.
- [ ] 교재 사이트 DevTools **Network**에서 Status `200`을 찾았고, 없는 주소에서 `404`를 보았다.
- [ ] `week01-practice`에서 `git log --oneline`에 commit 3줄이 보인다.
- [ ] 마지막 `git status`가 `nothing to commit, working tree clean`이다.
- [ ] 캡처 2장을 제출했다.

## 다음 수업 연결

2주차에는 새 폴더 `my-web`에 같은 세 파일을 만들어 GitHub 저장소에 올리고(`git push`) **GitHub Pages**로 누구나 여는 주소를 만든다.
`git config`는 저장소마다 따로 적용되므로 새 폴더에서도 이름·이메일을 다시 적는다.
다음 수업 전에 GitHub 계정에 쓸 이메일을 준비한다. 계정 아이디는 공개 주소에 그대로 들어가므로 실명·학번을 넣지 않는다.

## 공식 참고 자료

- [첫 번째 웹사이트 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Getting_started/Your_first_website)
- [URL이란 무엇인가 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL)
- [HTTP 404 — MDN](https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Status/404)
- [네트워크 활동 검사 — Chrome DevTools](https://developer.chrome.com/docs/devtools/network?hl=ko)
- [git init](https://git-scm.com/docs/git-init) · [git config](https://git-scm.com/docs/git-config) · [git status](https://git-scm.com/docs/git-status)
- [git add](https://git-scm.com/docs/git-add) · [git commit](https://git-scm.com/docs/git-commit) · [git log](https://git-scm.com/docs/git-log)
- [Pro Git (한국어) — 2.1 Git 저장소 만들기](https://git-scm.com/book/ko/v2)
