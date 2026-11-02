[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_form_input)

# 7주차 — 폼 입력 읽기와 결과 표시

이번 주도 부품을 하나씩 본다. 비교 예제 8개를 열어 값을 바꿔 보고, 마지막에 그 부품으로 이번 주 새 저장소 `web-week07` 의 `guestbook.html` 을 고치고 `guestbook.js` 를 조립한다.
6주차에는 버튼을 누르면 **정해 둔 글자**를 띄웠다. 이번 주에는 방명록 폼에 **사용자가 입력한 글자**를 읽어, 남길 때마다 아래 목록에 **한 줄씩 붙인다**. 칸이 비어 있으면 안내 문구를 보이고 커서를 그 칸으로 옮긴다.
결과는 화면과 **주소창**, **F12 › Console** 에서 본다. 예제 하나에 개념 하나. 다른 예제의 개념은 섞지 않는다.

## 이번 주 질문

> 3주차에 만든 방명록 폼은 **남기기**를 누르면 주소창 끝에 `?` 만 붙고 처음 화면으로 돌아갔다. 입력한 이름과 메시지를 읽어, 남길 때마다 화면 목록에 한 줄씩 쌓으려면 무엇을 알아야 하나?

답은 네 가지 원리다.
폼을 보내면 브라우저는 페이지를 **다시 연다**. 폼의 `submit` 을 듣고 첫 줄에서 `event.preventDefault()` 로 그 일을 막아야 내 코드가 바꾼 화면이 남는다.
입력 칸의 글자는 `value` 다. 누를 **때** 읽어야 그때 적힌 글자가 나온다. `trim()` 으로 앞뒤 빈칸을 떼면 빈칸만 친 칸도 빈 칸으로 볼 수 있다.
칸이 비었으면 안내 문구를 쓰고 `focus()` 로 커서를 옮긴 뒤 `return` 으로 **거기서 멈춘다**. 다 채워졌으면 목록에 한 줄을 붙이고 `form.reset()` 으로 칸을 비운다.
목록에 한 줄을 더하려면 `document.createElement('li')` 로 줄을 **새로 만들고** `textContent` 로 글자를 넣은 뒤 `append` 로 목록 맨 뒤에 **붙인다**. 자리 하나의 `textContent` 를 바꾸기만 하면 늘 마지막 한 줄만 남는다.

## 학습 목표

1. 폼을 보내면 페이지가 다시 열리는 것(주소 끝 `?`)을 보고, `addEventListener('submit', function (event) { })` 의 첫 줄 `event.preventDefault()` 로 막는다. Enter 로 보내도 같은 `submit` 이다.
2. `input.value`·`textarea.value` 로 칸에 지금 적힌 글자를 읽는다. 읽는 줄은 리스너 **안**에 둔다.
3. `trim()` 으로 앞뒤 빈칸을 떼고, `if (name === '') { … return; }` 로 빈 칸이면 안내하고 멈춘다. 검사는 위에서부터 차례로 한다.
4. `form.reset()` 으로 칸을 비우고 `focus()` 로 커서를 옮겨 다음 입력을 준비한다. 값은 비우기 **전에** 읽는다.
5. `'input'` 이벤트는 칸의 글자가 바뀔 때마다 일어난다. 다시 입력하면 안내 문구를 지우는 데 쓴다.
6. 미리 만든 함수를 맡길 때는 이름만 쓴다(`addEventListener('input', clearNotice)`). 괄호는 부를 때만 붙인다(`clearNotice();`).
7. `document.createElement('li')`·`textContent`·`append` 로 남길 때마다 목록 `<ul>` 에 한 줄씩 붙인다. 자리 하나의 `textContent` 를 바꾸면 늘 한 줄뿐인 것과 비교한다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/web-week07/guestbook.html
         글 두 개를 차례로 남긴 화면
         남긴 글
         · student01: 안녕하세요
         · student02: 반갑습니다     ← 남길 때마다 한 줄씩 쌓인다
         ← 주소창이 함께 보이게 찍는다
```

- 제출은 이 캡처 **한 장**이다. 빈값 안내 문구(`이름을 입력하세요.`)는 실습 중에 확인하는 것이고 캡처에는 없어도 된다.
- `web-week07/ex/` 에 비교 예제를 저장하고 값을 바꾼 것은 push 로 남긴다. 기록물·표는 없다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 3주차 폼 다시 보기(주소 끝 `?`) → ex01 폼 제출과 preventDefault → ex02 입력 칸의 value → ex03 trim | 새 폴더 `web-week07` 에 지난주 완성본 넣기 → `ex/` 에 예제 폴더 세 개(파일 여섯 개) 저장 → 값 바꿔 보기 → 새 저장소 만들어 올리기 · Pages 켜기 | `ex/` 비교 예제(확인용) |
| 2일차 | 예제 폴더 하나에 파일 두 개 → ex04 reset 과 focus → ex05 빈값 검사와 return → ex06 input 이벤트 → ex07 함수 이름만 맡기기 → ex08 바꾸기 vs 붙이기 → 조립표 | `ex/` 에 예제 폴더 다섯 개 저장 → 다섯 예제 값 바꿔 보기 → `guestbook.html`·`guestbook.js` 조립 → 375·1280 폭과 서버로 확인 → push | 캡처 1 |

각 수업은 `설명·시연 30분 + 실습 60분` 이다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.

## 준비

- 지난주 완성본. 내 `web-week06` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [6주차 `examples/day2/web-week06/`](../week06_dom_events/examples/day2/web-week06/) 파일을 **Raw** 로 받는다
- VS Code, Chrome(DevTools), Git (`git --version` 으로 확인)
- Node.js LTS(선택). 5주차에 받은 [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더에도 둔다([사용 안내](../../tools/static-server/README.md)). Node 가 없는 PC 는 파일을 두 번 눌러 열어도 이번 주 결과는 같다
- 개발자 도구의 **Console** 탭. 이번 주에는 Console 설정 ⚙ › **Preserve log** 를 켠다(폼이 페이지를 다시 열어도 Console 줄이 남는다. [따라하기 3단계](walkthrough.md#3-여는-법과-preserve-log))
- 6주차 비교 예제 [ex02](../week06_dom_events/examples/day1/ex02/app.js)(열 때 vs 클릭할 때)·[ex06](../week06_dom_events/examples/day2/ex06/app.js)(함수 하나를 두 곳에서 부르기)를 기억해 둔다. 이번 주가 그 두 파일에서 이어진다. 3주차에 만든 방명록 폼(`guestbook.html`)이 이번 주에 동작한다
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 폼 제출 | submit | 提交表单 |
| 기본 동작 막기 | preventDefault | 阻止默认行为 |
| 입력 값 | value | 输入值 |
| 앞뒤 빈칸 떼기 | trim | 去除首尾空格 |
| 안내 문구 | notice | 提示文字 |
| 커서 옮기기 | focus | 聚焦 |
| 폼 비우기 | reset | 重置表单 |
| 입력 이벤트 | input event | 输入事件 |
| 요소 만들기 | createElement | 创建元素 |
| 붙이기 | append | 添加 |

## 이번 주 비교 예제

예제마다 폴더 하나에 내 사이트와 같은 이름의 두 파일(`index.html` 화면 · `app.js` 동작)을 둔다. `index.html` 을 열고, 원리는 `app.js` 에서 본다. `index.html` 에는 그 예제가 쓰는 자리만 있다(1일차는 폼과 결과 자리, 2일차는 방명록 모양 폼·안내 자리·결과 자리 가운데 그 예제가 쓰는 것, ex08 은 글 칸·버튼·목록). 화면과 Console 의 번호가 코드의 형제 번호와 같다. ex07 은 Console 에 찍지 않고 안내 자리만 본다. 아래 `N행` 은 모두 그 폴더 `app.js` 의 줄 번호다.

| 예제 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01/index.html](examples/day1/ex01/index.html) + [app.js](examples/day1/ex01/app.js) | 1. 막지 않는 폼 / 2. `event.preventDefault()` 로 막는 폼 | 폼을 보내면 브라우저는 페이지를 다시 연다(주소 끝 `?`). 리스너 첫 줄에서 막아야 바꾼 화면이 남는다. 버튼을 눌러도 Enter 를 쳐도 같은 `submit` 이다 | 17행 `event.preventDefault();` 앞에 `//` → 2번도 다시 열린다 |
| [ex02/index.html](examples/day1/ex02/index.html) + [app.js](examples/day1/ex02/app.js) | 1. 열 때 읽은 `value` / 2. 누를 때 읽은 `value` / 3. textarea 의 `value` | `value` 는 칸에 **지금** 적힌 글자다. 읽는 줄이 리스너 안에 있어야 누를 때의 글자가 나온다(6주차 ex02 와 같은 원리) | 이름을 바꿔 다시 누르기 → 2번만 바뀐다. 16행 `value` 를 `textContent` 로 → 3번이 빈다 |
| [ex03/index.html](examples/day1/ex03/index.html) + [app.js](examples/day1/ex03/app.js) | 1. `value` 그대로 / 2. `trim()` 한 값 | `trim()` 은 앞뒤 빈칸만 뗀 값을 돌려준다. 빈칸만 친 칸은 빈 글자 `''` 가 된다. 가운데 빈칸은 남는다 | 빈칸만 넣기 → 2번 `[]`. 10행 `trim()` 을 `trm()` 으로 → 빨간 줄 |
| [ex04/index.html](examples/day2/ex04/index.html) + [app.js](examples/day2/ex04/app.js) | 1. 비우기 전에 읽은 값 / 2. `form.reset()` 뒤에 읽은 값 / 3. `focus()` 로 커서 옮기기 | 다음 입력 준비다. `reset()` 은 폼 안의 칸을 모두 비운다. 그래서 값은 비우기 전에 읽는다. `focus()` 는 커서를 그 칸으로 옮긴다 | 14행 `form.reset();` 을 2번 `console.log` 줄 아래로 → 2번에도 글자가 있다. 19행 `nameInput` 을 `messageInput` 으로 → 커서가 메시지 칸으로 |
| [ex05/index.html](examples/day2/ex05/index.html) + [app.js](examples/day2/ex05/app.js) | 1. 이름이 빔 / 2. 메시지가 빔 / 3. 둘 다 찼음 | `if` 안의 `return` 은 함수를 그 자리에서 끝낸다. 검사는 위에서부터라 둘 다 비면 1번 안내만 나온다 | 19행 `return;` 앞에 `//` → 결과에 `: 안녕하세요` 가 남는다 |
| [ex06/index.html](examples/day2/ex06/index.html) + [app.js](examples/day2/ex06/app.js) | 1. 이름 칸(`input`)의 `'input'` / 2. 메시지 칸(`textarea`)의 `'input'` | `'input'` 은 칸의 글자가 바뀔 때마다(칠 때도, 지울 때도) 일어난다. 한 줄 칸과 여러 줄 칸이 같다 | `abc` 를 한 글자씩 → 1번이 세 줄. 11행 `'input'` 을 `'inptu'` 로 → 이름 칸에 쳐도 빨간 줄 없이 아무 일도 없다 |
| [ex07/index.html](examples/day2/ex07/index.html) + [app.js](examples/day2/ex07/app.js) | 1. `function () { clearNotice(); }` 를 맡김 / 2. 이름만 맡긴 `clearNotice` | 미리 만든 함수는 이름만 맡기면 칠 때마다 브라우저가 대신 부른다. 괄호는 부를 때만 붙인다. 두 모양은 하는 일이 같다 | 18행 `clearNotice` 를 `clearNotice()` 로 → 메시지 칸에 쳐도 안내가 남는다. 14행 `clearNotice();` 를 `clearNotice;` 로 → 이름 칸에 쳐도 안내가 남는다 |
| [ex08/index.html](examples/day2/ex08/index.html) + [app.js](examples/day2/ex08/app.js) | 1. `textContent` 로 바꾸기 / 2. `createElement`·`append` 로 붙이기 | 바꾸기는 같은 자리의 글자를 갈아 끼워 늘 한 줄이다. 붙이기는 누를 때마다 새 `<li>` 를 **만들고** 글자를 넣어 목록 맨 뒤에 **붙이므로** 앞 줄이 남는다 | 20행 `list.append(li);` 앞에 `//` → 2번을 눌러도 목록이 빈다(빨간 줄 없음). 18행을 리스너 밖(8행 아래)으로 → 목록이 늘 한 줄 |

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week07_form_input/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(예제 폴더 `ex01/`~`ex03/`), 2일차 `day2/`(예제 폴더 `ex04/`~`ex08/`, 조립 `web-week07/`). 폴더마다 `index.html`·`app.js`
- 2일차 끝의 `web-week07`(조립 결과): [guestbook.html](examples/day2/web-week07/guestbook.html) · [guestbook.js](examples/day2/web-week07/guestbook.js) · [index.html](examples/day2/web-week07/index.html) · [about.html](examples/day2/web-week07/about.html) · [app.js](examples/day2/web-week07/app.js) · [styles.css](examples/day2/web-week07/styles.css) · [images/profile.png](examples/day2/web-week07/images/profile.png)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_form_input

## 완료 기준

- [ ] 새 저장소 `web-week07` 을 만들어 Pages 를 켰고, `ex/` 에 비교 예제가 있고, 각 예제에서 값을 하나 이상 바꿔 push 했다.
- [ ] `guestbook.html` 의 `<head>` 에 `<script src="guestbook.js" defer></script>` 가 있고, `<form id="guestbook-form">` 아래에 `#notice` 자리와 `<ul class="card" id="list">` 목록이 있다.
- [ ] 공개 주소 `https://student01.github.io/web-week07/guestbook.html` 에서 이름·메시지를 넣고 **남기기**를 누르면 주소가 그대로이고, 목록에 `이름: 메시지` 한 줄이 붙고, 칸이 비고 커서가 이름 칸에 있다. 한 번 더 남기면 앞 줄 아래에 한 줄이 더 붙는다.
- [ ] 이름이나 메시지를 비우고 누르면 그 칸의 안내 문구가 보이고 커서가 그 칸으로 간다. 그 칸에 한 글자를 치면 안내가 사라진다.
- [ ] Console 을 비우고(오른쪽 클릭 › **Clear console**) `guestbook.html` 을 새로고침한 뒤 글을 남겨 봐도 F12 Console 에 빨간 줄이 없다(브라우저가 탭 아이콘을 찾다 낸 `favicon.ico` 404 줄은 괜찮다).
- [ ] 목록에 두 줄이 쌓인 화면과 주소창이 함께 보이는 캡처 1장을 제출한다.

## 다음 수업 연결

이번 주로 8주차 중간 실기 범위(1~7주 실습 제출)가 모두 채워졌다. 6주차 2일차에 안내한 대로 8주차는 [문제 은행](../week08_midterm/examples/README.md)에서 값을 바꿔 출제한다. 폼 문제 [w07_form_line](../week08_midterm/examples/w07_form_line/README.md)은 이번 주 실습에서 나왔다.
이번 주 목록은 **화면에만** 있다. 한 줄만 지우거나 개수를 세려면 글을 배열에 모아 두고 목록을 다시 그려야 한다. 그것이 10주차이고, 새로고침해도 남게 하는 것은 11주차다. 9주차는 오늘 `web-week07` 의 파일에서 시작한다(**Code › Download ZIP**, 못 받으면 교재의 이번 주 [`examples/day2/web-week07/`](examples/day2/web-week07/)).

## 공식 참고 자료

- [첫 번째 폼 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Extensions/Forms/Your_first_form)
- [HTMLFormElement: submit 이벤트 — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLFormElement/submit_event)
- [Event.preventDefault() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Event/preventDefault)
- [HTMLInputElement — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLInputElement)
- [String.prototype.trim() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/String/trim)
- [HTMLElement.focus() — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLElement/focus)
- [HTMLFormElement.reset() — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLFormElement/reset)
- [Element: input 이벤트 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/input_event)
- [Document.createElement() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/createElement)
- [Element.append() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/append)
- [Console 기능 참고(로그 보존 Preserve log) — Chrome DevTools](https://developer.chrome.com/docs/devtools/console/reference?hl=ko#persist)
