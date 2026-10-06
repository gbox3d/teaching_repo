[15주 문제 은행](../README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam)

# w09_readme_links — README 1차판

출처: [9주차 실습 제출](../../../week09_architecture_project/lab.md#제출--캡처-한-장과-발표) · 권장 9분 · 기말 A(화면(HTML·CSS·README))

9주차에 쓴 README 1차판을 다른 값으로 다시 쓴다. 사이트는 완성되어 있고, 이 폴더에 `README.md` 한 장만 새로 만든다. 마크다운은 제목 `#`, 목록 `-`, 링크 `[보이는 글](주소)` 세 가지만 쓴다.

## 시작 파일

| 파일 | 지금 상태 |
|---|---|
| `index.html` · `about.html` · `guestbook.html` | 완성된 세 페이지다. nav 로 서로 오간다. 고치지 않는다 |
| `styles.css` · `app.js` · `guestbook.js` | 완성본이다. 고치지 않는다 |
| `screenshots/home.png` · `screenshots/guestbook.png` | 버튼을 누른 뒤와 글을 남긴 뒤에 찍은 화면 그림 두 장이다. 고치지 않는다 |
| `README.md` | 없다. 이 문제에서 새로 만든다 |

## 할 일

1. 이 문제 폴더 안(`index.html` 옆)에 `README.md` 를 만든다. 저장소에서 보면 `w09_readme_links/README.md` 다. 맨 첫 줄에 제목 `# 나의 웹 연습장` 한 줄을 쓴다. 홈 페이지 맨 위의 사이트 이름과 같다.
2. 제목 아래에 `##` 절 다섯을 이 순서로 쓴다. `##` 절은 이 다섯 개뿐이고, 절 안의 줄은 모두 목록 `- ` 으로 쓴다.
   - `## 공개 주소` — 이 폴더의 공개 주소를 링크 한 줄로 쓴다. 주소는 `https://<아이디>.github.io/web-week15/w09_readme_links/` 다.
   - `## 페이지` — `index.html` · `about.html` · `guestbook.html` 을 이 순서로 한 줄에 하나씩 링크로 쓰고, 링크 뒤에 그 페이지 설명을 붙인다.
   - `## 기능` — 사이트에서 할 수 있는 일을 2줄 쓴다.
   - `## 화면` — `screenshots/home.png` · `screenshots/guestbook.png` 를 이 순서로 한 줄에 하나씩 링크로 쓴다.
   - `## 이번에 배운 것` — 수업에서 배운 것을 3줄 쓴다.
3. 같은 폴더의 파일은 소괄호에 경로만 쓴다(그림은 `screenshots/` 부터). 파일 이름은 대소문자까지 그대로 쓴다. 굵게 `**` 와 그림 `![]()` 문법은 쓰지 않는다.

## 확인할 것

- [ ] 서버로 연 이 폴더 주소 뒤에 `README.md` 를 붙여 열면 404 가 아니라 쓴 글이 그대로 보인다.
- [ ] VS Code 에서 `README.md` 를 열고 Open Preview 를 누르면 큰 제목 `나의 웹 연습장` 아래에 작은 제목이 `공개 주소` → `페이지` → `기능` → `화면` → `이번에 배운 것` 순서로 보인다. `#` 이 글자로 남은 줄이 없다.
- [ ] `공개 주소` 절의 링크 한 줄이 `https://` 로 시작하는 `github.io` 주소를 가리킨다.
- [ ] `페이지` 절의 세 줄이 차례로 `index.html` · `about.html` · `guestbook.html` 을 가리키고 줄마다 설명이 붙어 있다. `화면` 절의 두 줄이 차례로 `screenshots/home.png` · `screenshots/guestbook.png` 를 가리킨다.
- [ ] 페이지 링크 셋과 그림 링크 둘을 누르면 모두 열린다. 올린 뒤 GitHub 에서 이 폴더를 열면 파일 목록 아래에 README 가 문서로 보이고, 그 링크를 눌러도 404 가 나지 않는다.
- [ ] `기능` 절은 목록 2줄, `이번에 배운 것` 절은 목록 3줄이다. README 어디에도 `**` 와 `![` 가 없다.
- [ ] 세 페이지를 열어도 F12 › Console 에 빨간 줄이 없다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| README 제목 | `나의 웹 연습장` |
| 절 제목(순서대로) | `공개 주소` · `페이지` · `기능` · `화면` · `이번에 배운 것` |
| 페이지 파일(순서대로) | `index.html` · `about.html` · `guestbook.html` |
| 둘째 페이지 이름(nav 글자) | `내 정보` |
| 셋째 페이지 이름(nav 글자) | `방명록` |
| 그림 파일(순서대로) | `screenshots/home.png` · `screenshots/guestbook.png` |
| 셋째 절 목록 줄 수 | `2` |
| 다섯째 절 목록 줄 수 | `3` |

시험에서는 같은 문제를 이 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다.

## 받기와 올리기

- 이번 주 저장소(`web-week15`) 맨 위에 [server.mjs](../../../../tools/static-server/server.mjs) 가 없으면 먼저 **Raw** 로 받아 둔다.
- 저장소 안에 `w09_readme_links/` 폴더를 만든다. 교재의 이 문제 폴더에 있는 시작 파일을 하나씩 열어 **Raw** 를 누르고 Ctrl+S(macOS ⌘+S)로 같은 이름으로 저장한다. 그림도 Raw 를 누르면 그림만 보이는 화면이 열리고, 거기서 같은 방법으로 저장한다. 하위 폴더(그림·데이터)는 GitHub 에서 그 폴더를 눌러 들어가 받고, 내 폴더에도 같은 이름으로 만든다. 저장한 이름 끝에 `.txt` 가 붙었으면 지운다. 이 `README.md`(지금 읽는 문제 문장)는 받지 않는다.
- 저장소 맨 위에서 `node server.mjs` 로 열면 주소는 `http://localhost:8000/w09_readme_links/` 이다. Node 가 없는 PC 는 두 번 눌러 연다.
- `node server.mjs` 로 연 주소나 공개 주소에서는 `favicon.ico` 404 한 줄이 Console·Network 에 보여도 괜찮다(빨간 줄로 세지 않는다). 공개 주소에서 새로고침하면 Status 가 `304` 로 보일 수 있다. 이미 받은 파일을 다시 쓴다는 뜻이다.
- 올린 뒤 공개 주소는 `https://student01.github.io/web-week15/w09_readme_links/`이다.
- 해답은 공개하지 않는다. 위 "확인할 것"이 모두 맞으면 된 것이다.
