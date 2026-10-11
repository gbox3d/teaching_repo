[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

# 13주차 — 보안·접근성·릴리스 점검

이번 주도 부품을 하나씩 본다. 비교 예제 8개를 열어 값을 바꿔 보고, 마지막에 이번 주 새 저장소 `web-week13` 에 입학 연도 폼·`about.js`·카드 링크 글자·README 최종판을 조립한다.
12주차까지 네 페이지(홈·내 정보·방명록·프로젝트)가 생겼다. 이번 주에는 새 기능보다 **내놓기 전 점검**이 중심이다. 입력한 글을 글자로 넣는지, 그림·입력 칸·링크에 무엇인지 알려 주는 글자가 붙어 있는지, 링크·Console·좁은 화면이 괜찮은지 본다.
결과는 화면과 **F12 › Console**·**Elements**, 마크다운은 VS Code **Open Preview** 에서 본다. 파일 하나에 개념 하나. 다른 파일의 개념은 섞지 않는다.

## 이번 주 질문

> 다른 사람이 글을 남기고, 누구나 읽을 수 있고, 어느 화면에서 열어도 괜찮은 페이지로 내놓으려면 무엇을 확인해야 하나?

답은 세 가지 원리다.
입력한 글은 `textContent` 로 넣는다. `innerHTML` 은 받은 글을 HTML 로 읽어서, 남이 적은 태그가 내 페이지의 진짜 요소가 된다. `innerHTML = ''` 은 비울 때만 쓴다.
그림·입력 칸·링크·버튼에는 **무엇인지 알려 주는 글자**가 붙어 있어야 한다. 그림은 `alt`, 입력 칸은 `label for`, 링크·버튼은 그 안의 글자다.
내놓기 전에는 **링크 → Console → 375 폭** 순서로 점검한다. README 는 `#`·`-`·링크·그림 네 가지 기호로 쓴다.

## 학습 목표

1. `Number()` 로 입력 칸의 글자를 숫자로 바꾸고, 숫자로 못 바꾸면 `NaN` 이 된다는 것을 `isNaN()` 으로 확인한다. `new Date().getFullYear()` 로 올해를 꺼내 몇 년차인지 계산한다.
2. 같은 글을 `textContent` 와 `innerHTML` 로 넣었을 때의 차이를 말하고, 입력한 글은 `textContent` 로 넣는다. 공개 저장소와 캡처에 실명·학번·전화번호·실제 이메일·비밀번호를 넣지 않는다.
3. 그림의 `alt`, 입력 칸의 `label for`, 링크·버튼 글자를 점검한다. 이름표를 눌러 커서가 칸으로 가는지, **Tab** 키로 옮겨 다니며 글자만 읽어도 무엇인지 아는지 본다.
4. README 를 `#` 제목·`-` 목록·`[보이는 글](주소)` 링크·`![대체 글](경로)` 그림 네 가지로 쓰고, 그림 경로의 대소문자를 파일 이름과 맞춘다.
5. 모든 링크 404 없음 → Console 빨간 줄 0 → 기기 모드 375 순서로 이번 주 사이트를 점검한다. push 한 뒤 공개 주소에서 링크를 한 번 더 누르고(내 PC 서버는 대소문자를 가리지 않는다), 공개 주소에서 캡처한다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/web-week13/guestbook.html   (F12 기기 모드 375px)
         방명록
         홈 · 내 정보 · 방명록 · 프로젝트   ← 375 에서는 세로로 선다
         … 한 줄 남기기 폼 …
         남긴 글
         · student02: <b>안녕</b> (남긴 날짜) [삭제]
         1개
         F12 › Console — 빨간 줄 없음(favicon.ico 404 한 줄은 세지 않는다)
         ← 주소창이 함께 보이게 찍는다
```

- 제출은 이 캡처 **한 장**이다. `<b>안녕</b>` 이 굵은 글씨가 아니라 **글자 그대로** 보이는 것이 핵심이다.
- 입학 연도 폼·카드 링크 글자·`README.md` 최종판·`screenshots/` 세 장도 이번 주 저장소에 함께 올린다. README 는 그대로 14주차 발표의 레포트가 되므로 소개 한 줄·기능 다섯 줄·그림 세 장·어려움과 해결 세 줄·만든 과정(9주차부터 주차마다 한 줄, 다섯 줄 이상)을 갖춘다. 이번 주 캡처 대상은 아니다.
- `web-week13/ex/` 에 비교 예제를 저장하고 값을 바꾼 것은 push 로 남긴다. 기록물·표는 없다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 고르기 페이지 → ex01 `Number`·`isNaN` → ex02 `getFullYear` → ex03 `textContent` 와 `innerHTML` → 공개 저장소에 넣지 않는 것 → ex04 `alt` → ex05 `label for` | 새 폴더 `web-week13` 에 지난주 완성본 넣기 → `ex/` 에 1일차 파일 저장 → 값 바꿔 보기 → 새 저장소 만들어 올리기 · Pages 켜기 | `ex/` 비교 예제(확인용) |
| 2일차 | ex06 링크·버튼 글자 → ex07 `#`·`-` → ex08 링크와 그림 → 내놓기 전 점검 순서 → 14주차 발표·15주차 문제 은행 안내 → 조립표 | 세 파일 값 바꿔 보기 → `about.html`·`about.js`·`projects.js`·`screenshots/`·`README.md` 조립 → 링크·Console·375 점검과 `alt`·이름표 → push → 공개 주소에서 링크 다시 누르기 → 공개 주소 캡처 | 캡처 1 |

각 수업은 `설명·시연 30분 + 실습 60분` 이다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.

## 준비

- 지난주 완성본. 내 `web-week12` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [12주차 `examples/day2/web-week12/`](../week12_persistent_crud/examples/day2/web-week12/) 파일을 **Raw** 로 받는다
- VS Code, Chrome(DevTools), Git (`git --version` 으로 확인)
- Node.js LTS. 지난주 폴더의 [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더에도 둔다([사용 안내](../../tools/static-server/README.md)). `projects.html` 카드는 두 번 눌러 연 `file://` 화면에는 나오지 않는다(12주차). `node server.mjs` → `http://localhost:8000/` 이나 공개 주소에서 본다
- **확인·캡처는 공개 주소에서 한다.** 방명록 글은 주소마다 따로 저장된다(11주차)
- VS Code 마크다운 미리 보기(9주차): `.md` 파일을 열고 **Ctrl+K** 다음 **V**(macOS **⌘+K** 다음 **V**)로 옆에 띄운다
- 화면 캡처 도구: Windows **Win+Shift+S**, macOS **⌘+Shift+4**
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 글자로 넣기 | textContent | 按文本插入 |
| HTML로 넣기 | innerHTML | 按 HTML 插入 |
| 대체 글 | alt text | 替代文本 |
| 이름표 연결 | label for | 标签关联 |
| 접근성 | accessibility | 无障碍 |
| 개인정보 | personal information | 个人信息 |
| 내놓기 전 점검 | release check | 发布前检查 |
| 마크다운 | Markdown | Markdown 标记语言 |

## 이번 주 비교 예제

1일차 ex01·ex02 는 같은 화면(입력 칸 하나·버튼 하나·결과 자리 하나)을 쓰므로 코드만 `.js` 파일에 두고, 고르기 페이지 [day1/index.html](examples/day1/index.html) 맨 아래 `<script src>` 두 줄 중 하나만 켜서 연다. ex03 은 화면이 달라서 `.html` 과 `.js` 를 한 쌍으로 둔다. ex04·ex05·ex06 은 JavaScript 없이 HTML 만으로 보는 예제라 `.html` 하나다. ex07·ex08 은 README 와 같은 마크다운 `.md` 파일이고 9주차처럼 VS Code 미리 보기로 본다. ex07 의 `#`·`-` 와 ex08 1번 링크는 9주차 ex01~ex03 에서 본 것이고, README 최종판을 쓰기 전에 다시 본다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_number.js](examples/day1/ex01_number.js) | 1. 글자 + 1 / 2. `Number(글자)` + 1 / 3. `isNaN` | 입력 칸의 값은 늘 글자다. `Number()` 로 숫자로 바꾸고, 못 바꾸면 `NaN` 이다. `isNaN()` 은 `NaN` 이면 `true` | 칸에 `이천이십삼`·`2023년`·빈칸 |
| [ex02_year.js](examples/day1/ex02_year.js) | 1. 올해 / 2. 올해 - 입학 연도 / 3. + 1 | `new Date().getFullYear()` 는 버튼을 누른 순간 컴퓨터 시계의 연도다. 입학한 해를 1년차로 세려고 1 을 더한다 | `2026` 을 직접 적기, 괄호 빼기 |
| [ex03_text_html.html](examples/day1/ex03_text_html.html) + [.js](examples/day1/ex03_text_html.js) | 1. `textContent` / 2. `innerHTML` / 3. `innerHTML = ''` | 입력한 글은 글자로 넣는다. `innerHTML` 은 받은 글을 HTML 로 읽어 태그가 진짜 요소가 된다. 비울 때만 `innerHTML` | 칸에 `<button>가짜 버튼</button>` |
| [ex04_alt.html](examples/day1/ex04_alt.html) | 1. 무슨 그림인지 적은 `alt` / 2. `alt` 없음 / 3. `alt="그림"` | `alt` 는 그림이 안 보일 때 대신 읽히는 글이다. 그림이 무엇인지 적는다 | 세 `src` 를 `images/nothing.png` 로 |
| [ex05_label.html](examples/day1/ex05_label.html) | 1. `for` = `id` / 2. 한 글자 다름 / 3. `label` 없음 | 이름표의 `for` 와 칸의 `id` 가 같아야 이어진다. 이어지면 이름표를 눌러도 커서가 칸으로 간다 | 2번 `id` 고치기, `for="#year1"` |
| [ex06_link_text.html](examples/day2/ex06_link_text.html) | 1. 같은 글자 링크 셋 / 2. 목적지를 적은 링크 셋 / 3. 기호 버튼과 글자 버튼 | 링크·버튼 글자는 그것만 읽어도 어디로 가는지·무엇을 하는지 알게 쓴다 | **Tab** 키로 옮겨 다니며 읽기 |
| [ex07_line_marks.md](examples/day2/ex07_line_marks.md) | 1. `#` 제목 / 2. `-` 목록 / 3. 기호 없이 줄만 바꿈 / 4. 띄어쓰기 없음 | 줄 맨 앞 기호와 띄어쓰기 한 칸이 그 줄의 모양을 정한다(9주차 ex01·ex02) | `#` 하나 더, 빈 줄 넣기 |
| [ex08_link_image.md](examples/day2/ex08_link_image.md) | 1. 링크 / 2. 그림 / 3. `!` 를 뺀 그림 줄 / 4. 대소문자가 다른 경로 | 링크(9주차 ex03) 앞에 `!` 를 붙이면 그림이다. 대괄호 글자가 `alt` 다. 경로는 대소문자까지 같아야 GitHub 에서 보인다 | `!` 지웠다 되살리기 |

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week13_release_security/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(고르기 페이지 `index.html`, ex01·ex02 의 `.js`, ex03 의 `.html`·`.js`, ex04·ex05 의 `.html`, 그림 `images/profile.png`), 2일차 `day2/`(ex06 의 `.html`, ex07·ex08 의 `.md`, 같은 그림, 조립 `web-week13/`)
- 2일차 끝의 `web-week13`(조립 결과): [about.html](examples/day2/web-week13/about.html) · [about.js](examples/day2/web-week13/about.js) · [projects.js](examples/day2/web-week13/projects.js) · [README.md](examples/day2/web-week13/README.md) · [screenshots/home.png](examples/day2/web-week13/screenshots/home.png) · [guestbook.png](examples/day2/web-week13/screenshots/guestbook.png) · [projects.png](examples/day2/web-week13/screenshots/projects.png)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security

## 완료 기준

- [ ] 새 저장소 `web-week13` 을 만들어 Pages 를 켰고, `ex/` 에 비교 예제가 있고, 각 예제에서 값을 하나 이상 바꿔 push 했다.
- [ ] 공개 주소 `https://student01.github.io/web-week13/about.html` 에서 입학 연도를 적고 **계산하기**를 누르면 `…년차입니다.` 가 보이고, 숫자가 아니면 `입학 연도를 숫자로 적어 주세요.` 가 보인다.
- [ ] `projects.html` 카드 세 장의 링크 글자가 서로 다르다.
- [ ] 네 페이지의 nav 링크가 공개 주소에서도 모두 열리고(404 없음), 각 페이지 Console 에 빨간 줄이 없고(`favicon.ico` 404 는 세지 않는다), 기기 모드 375 에서 가로로 밀리지 않는다.
- [ ] 그림 넷(홈 프로필, 프로젝트 카드 셋)에 `alt` 가 있고, 이름표 넷(방명록 세 칸, 입학 연도 칸)을 누르면 커서가 그 칸으로 간다.
- [ ] 저장소 첫 화면에 `README.md` 최종판(일곱 절, 제목 아래 소개 한 줄, `## 만든 과정` 은 9주차부터 주차마다 한 줄씩 다섯 줄 이상)이 보이고 `screenshots/` 그림 세 장이 깨지지 않는다.
- [ ] 기기 모드 375 공개 주소 방명록에서 `<b>안녕</b>` 이 글자 그대로 보이고 Console 이 깨끗한(`favicon.ico` 404 한 줄은 세지 않는다) 화면을 캡처 1장으로 제출한다.

## 다음 수업 연결

이번 주로 네 페이지가 내놓을 수 있는 상태가 되었다. 14주차에는 새 저장소 `web-week14` 를 오늘 `web-week13` 의 파일에서 시작하고(**Code › Download ZIP**, 못 받으면 교재의 이번 주 [`examples/day2/web-week13/`](examples/day2/web-week13/)), 그 공개 주소로 **3분 시연**을 한다.
레포트는 오늘 쓴 `README.md` 최종판이다. 시연 순서는 공개 주소 → 페이지 이동 → 다크 모드 → 폼 빈값 안내 → 방명록 추가·삭제 → 새로고침해도 남는 목록 → JSON 카드 → Commits 탭과 README 다.
15주차 기말 실기는 1~14주 실습 제출로 만든 [문제 은행](../week15_final_exam/examples/README.md)에서 나온다. 이번 주 제출(`<b>안녕</b>` 이 글자 그대로 보이는 화면)도 그 안에 [w13_text_safe](../week15_final_exam/examples/w13_text_safe/) 문제로 들어 있다.

## 공식 참고 자료

- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [Element.innerHTML — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/innerHTML)
- [Number() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Number/Number)
- [isNaN() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/isNaN)
- [Date.prototype.getFullYear() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Date/getFullYear)
- [img 요소의 alt — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/img)
- [label 요소 — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/label)
- [접근성 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Accessibility)
- [기본 작성 및 서식 구문 — GitHub Docs](https://docs.github.com/ko/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [리포지토리 README 정보 — GitHub Docs](https://docs.github.com/ko/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [기기 모드로 모바일 기기 시뮬레이션 — Chrome DevTools](https://developer.chrome.com/docs/devtools/device-mode?hl=ko)
