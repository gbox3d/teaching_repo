[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud)

# 6주차 — DOM·이벤트·브라우저 CRUD

이번 주도 부품을 하나씩 본다. 비교 예제 6개를 열어 값을 바꿔 보고, 마지막에 이번 주 새 저장소 `web-week06` 의 `index.html`·`styles.css`·`app.js` 를 그 부품으로 조립한다.
5주차 코드는 페이지를 열 때 **한 번** 실행됐다. 이번 주에는 **버튼을 누를 때마다** 화면이 바뀌게 한다. 글자를 바꾸고, 누른 횟수를 세고, class 하나로 다크 모드를 켜고 끈다.
결과는 화면과 **F12 › Console**, 그리고 이번 주에 처음 쓰는 **F12 › Elements** 탭에서 본다. 파일 하나에 개념 하나. 다른 파일의 개념은 섞지 않는다.

## 이번 주 질문

> 버튼을 누를 때마다 글자가 바뀌고 횟수가 늘고 화면이 어두워지게 하려면 무엇을 알아야 하나?

답은 세 가지 원리다.
브라우저는 HTML 파일을 읽어 요소 상자(**DOM**)를 만들고, JavaScript 는 그 상자를 **찾아서 바꾼다**. 파일은 그대로다.
바꾸는 줄을 `addEventListener` 안에 넣으면 **누를 때마다** 실행된다. 누를 때마다 이어서 세려면 변수를 함수 **밖**에 둔다.
모양은 CSS 규칙에 미리 적어 두고, JavaScript 는 **class 이름만** 붙였다 뗀다.

## 학습 목표

1. HTML 파일과 브라우저가 만든 DOM 의 차이를 말한다. DevTools **Elements** 탭은 지금의 DOM 을, 페이지 소스 보기는 파일을 보여 준다는 것을 확인한다.
2. `document.querySelector('#id')` 로 요소를 찾아 `const` 에 담고 `textContent` 로 글자를 바꾼다. 못 찾으면 `null` 이고 `null` 에 쓰면 빨간 줄이 뜬다.
3. 바꾸는 줄을 `addEventListener('click', function () { })` 안에 넣어 누를 때마다 실행되게 한다. 횟수는 함수 밖의 `let count` 에 담아 센다.
4. `classList.add / remove / toggle` 의 차이를 말하고, `body.dark` CSS 규칙과 `document.body.classList.toggle('dark')` 로 다크 모드를 켜고 끈다.
5. 두 버튼이 같은 일을 하면 그 일을 함수 하나에 적고 두 곳에서 부른다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/web-week06/
         배경이 어두운 화면 ─ [인사 바꾸기] [다크 모드]
         카드 한 줄 ─ 반갑습니다. 오늘도 좋은 하루 되세요.
         카드 한 줄 ─ 클릭 3회
         ← 주소창이 함께 보이게 찍는다
```

- 제출은 이 캡처 **한 장**이다. 클릭 횟수는 몇 번이든 된다. `클릭 0회` 가 아니라 **1 이상**이면 눌러 본 것이 보인다.
- `web-week06/ex/` 에 비교 예제를 저장하고 값을 바꾼 것은 push 로 남긴다. 기록물·표는 없다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 고르기 페이지 쓰는 법 → ex01 HTML 파일과 DOM(Elements 탭) → ex02 클릭할 때 바꾸기 → ex03 클릭 횟수 | 새 폴더 `web-week06` 에 지난주 완성본 넣기 → `ex/` 에 네 파일 저장 → 값 바꿔 보기 → 새 저장소 만들어 올리기 · Pages 켜기 | `ex/` 비교 예제(확인용) |
| 2일차 | ex04 classList → ex05 다크 모드 → ex06 함수 하나를 두 버튼에 → 8주차 중간 실기 안내 → 조립표 | 여섯 파일 값 바꿔 보기 → `index.html`·`styles.css`·`app.js` 조립 → 375·1280 폭과 서버로 확인 → push | 캡처 1 |

각 수업은 `설명·시연 30분 + 실습 60분` 이다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.

## 준비

- 지난주 완성본. 내 `web-week05` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [5주차 `examples/day2/web-week05/`](../week05_javascript_data/examples/day2/web-week05/) 파일을 **Raw** 로 받는다
- VS Code, Chrome(DevTools), Git (`git --version` 으로 확인)
- Node.js LTS(선택). 5주차에 받은 [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더에도 둔다([사용 안내](../../tools/static-server/README.md)). Node 가 없는 PC 는 파일을 두 번 눌러 열어도 이번 주 결과는 같다
- 개발자 도구의 **Console** 탭과 **Elements** 탭 위치(오른쪽 클릭 › **검사**, 또는 **F12**)
- 5주차 비교 예제 [ex01](../week05_javascript_data/examples/day1/ex01_click.html)(클릭할 때 실행)·[ex09](../week05_javascript_data/examples/day2/ex09_dom_write.js)(먼저 찾고 그다음 바꾼다)를 기억해 둔다. 이번 주가 그 두 파일에서 이어진다
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 문서 객체 모델 | DOM (Document Object Model) | 文档对象模型 |
| 요소 | element | 元素 |
| 요소 찾기 | querySelector | 查找元素 |
| 글자 내용 | textContent | 文本内容 |
| 이벤트 | event | 事件 |
| 클릭 이벤트 등록 | addEventListener | 添加事件监听 |
| 클래스 목록 | classList | 类列表 |
| 다크 모드 | dark mode | 深色模式 |

## 이번 주 비교 예제

1일차 ex01~ex03 은 같은 화면을 쓰므로 코드만 `.js` 파일에 두고, 고르기 페이지 [day1/index.html](examples/day1/index.html) 맨 아래 `<script src>` 세 줄 중 하나만 켜서 연다. 2일차 ex04~ex06 은 화면이 서로 달라서 `.html` 과 `.js` 를 한 쌍으로 둔다. Console 의 번호가 코드의 형제 번호와 같다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_dom.js](examples/day1/ex01_dom.js) | 화면 · Elements 탭 · 페이지 소스 보기의 글자 | 브라우저는 HTML 파일을 읽어 DOM 을 만들고 화면은 DOM 을 보여 준다. JS 가 바꾸는 것은 DOM 이고 파일은 그대로다 | 찾는 id 를 틀리게 → `null` 과 빨간 줄 |
| [ex02_click_write.js](examples/day1/ex02_click_write.js) | 1. 열 때 바꾸기 / 2. 클릭할 때 바꾸기 | 바꾸는 줄을 `addEventListener` 안에 넣으면 누를 때마다 실행된다 | 바꾸는 줄을 `});` 밖으로 옮기기 |
| [ex03_counter.js](examples/day1/ex03_counter.js) | 1. 함수 밖의 `let count` / 2. 함수 안의 `let inside` | 함수 밖 변수는 열 때 한 번만 0 이 되어 누를 때마다 이어서 는다. 안의 변수는 누를 때마다 다시 0 이 된다 | `let count = 0;` 을 함수 안으로 옮기기 |
| [ex04_classlist.html](examples/day2/ex04_classlist.html) + [.js](examples/day2/ex04_classlist.js) | 1. `classList.add` / 2. `remove` / 3. `toggle` | 모양은 CSS 규칙이 정하고 JS 는 class 이름만 붙였다 뗀다 | `.on` 색 바꾸기, class 이름의 대소문자 |
| [ex05_dark.html](examples/day2/ex05_dark.html) + [.js](examples/day2/ex05_dark.js) | 1. `body.dark` 규칙 / 2. `body.dark .card` 규칙 | 색은 CSS 에 미리 적고 JS 는 `document.body.classList.toggle('dark')` 한 줄 | 카드 규칙 지우기, `toggle` 을 `add` 로 |
| [ex06_reuse.html](examples/day2/ex06_reuse.html) + [.js](examples/day2/ex06_reuse.js) | 1. A 버튼 / 2. B 버튼이 같은 `countUp()` 을 부른다 | 같은 일은 함수 하나에 적고 여러 곳에서 부른다. 부를 때는 괄호를 붙인다 | `countUp();` 의 괄호 빼기 |

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week06_dom_crud/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(고르기 페이지 `index.html`, ex01~ex03 의 `.js`), 2일차 `day2/`(ex04~ex06 의 `.html`·`.js`, 조립 `web-week06/`)
- 2일차 끝의 `web-week06`(조립 결과): [index.html](examples/day2/web-week06/index.html) · [styles.css](examples/day2/web-week06/styles.css) · [app.js](examples/day2/web-week06/app.js) · [about.html](examples/day2/web-week06/about.html) · [guestbook.html](examples/day2/web-week06/guestbook.html) · [images/profile.png](examples/day2/web-week06/images/profile.png)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud

## 완료 기준

- [ ] 새 저장소 `web-week06` 을 만들어 Pages 를 켰고, `ex/` 에 비교 예제가 있고, 각 예제에서 값을 하나 이상 바꿔 push 했다.
- [ ] `index.html` 의 `#greeting` 카드 아래에 **인사 바꾸기**·**다크 모드** 버튼과 `id="count"` 카드가 있다.
- [ ] `styles.css` 맨 아래에 `body.dark, body.dark .card { … }` 규칙이 있다.
- [ ] 공개 주소 `https://student01.github.io/web-week06/` 에서 **인사 바꾸기**를 누르면 인사 문장이 바뀌고, 두 버튼 어느 쪽을 눌러도 `클릭 N회` 가 하나씩 는다.
- [ ] **다크 모드**를 누르면 배경과 카드가 어두워지고, 다시 누르면 돌아온다. F12 Console 에 빨간 줄이 없다.
- [ ] 다크 모드가 켜진 화면과 주소창이 함께 보이는 캡처 1장을 제출한다.

## 다음 수업 연결

오늘은 버튼을 눌렀을 때 **정해 둔 글자**를 띄웠다. 7주차에는 새 저장소 `web-week07` 을 오늘 `web-week06` 의 파일에서 시작하고(**Code › Download ZIP**, 못 받으면 교재의 이번 주 [`examples/day2/web-week06/`](examples/day2/web-week06/)), 방명록 폼에 **사용자가 입력한 글자**를 읽어 화면에 띄운다.
오늘 쓴 `addEventListener` 와 `textContent` 를 그대로 쓰고, `click` 대신 폼의 `submit` 을 듣는다. 결과는 7주차 공개 주소 `https://student01.github.io/web-week07/` 에서 확인한다.
8주차는 중간 개인 실기다. 1~7주 실습 제출로 만든 문제 은행에서 값을 바꿔 출제한다. 문제 은행은 [8주차 예제](../week08_midterm/examples/README.md)에 있다.

## 공식 참고 자료

- [DOM 소개 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document_Object_Model/Introduction)
- [Document.querySelector() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/querySelector)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [EventTarget.addEventListener() — MDN](https://developer.mozilla.org/ko/docs/Web/API/EventTarget/addEventListener)
- [이벤트 입문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Events)
- [Element.classList — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/classList)
- [Document.body — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/body)
- [함수 — 코드 재사용하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Functions)
- [DOM 보기와 바꾸기(Elements 패널) — Chrome DevTools](https://developer.chrome.com/docs/devtools/dom?hl=ko)
