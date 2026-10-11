[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data)

# 10주차 — 배열 데이터를 목록으로 그리기

이번 주도 부품을 하나씩 본다. 비교 예제 7개를 열어 값을 바꿔 보고, 마지막에 이번 주 새 저장소 `web-week10` 의 `guestbook.html`·`guestbook.js` 를 그 부품으로 조립한다.
7주차 방명록은 글을 남기면 카드 한 줄(`#last`)에 마지막 글만 보였다. 이번 주에는 남긴 글을 **배열**에 쌓아 **목록**으로 그리고, 줄마다 **[삭제]** 버튼을 붙인다.
결과는 화면과 **F12 › Console**, **F12 › Elements** 에서 본다. Console 아래 입력 칸에 `items` 를 쳐서 배열을 직접 보는 것도 이번 주에 처음 한다. 파일 하나에 개념 하나다.

## 이번 주 질문

> 방명록에 남긴 글이 사라지지 않고 목록으로 쌓이고, 줄마다 지울 수 있게 하려면 무엇을 알아야 하나?

답은 세 가지 원리다.
값 여러 개는 **배열** 하나에 순서대로 담는다. `push` 로 뒤에 더하고, 번호(`items[i]`)는 0 부터 세며, 개수는 `items.length` 다. 처음부터 끝까지 훑을 때는 `for` 를 쓴다.
화면의 한 줄은 `createElement` 로 **만들고** `textContent` 로 글자를 넣은 뒤 `append` 로 **붙여야** 보인다.
화면은 배열을 비춘 것이다. 배열을 바꾼 뒤에는 `showList()` 가 목록을 **비우고 배열 전체를 다시 그린다**. [삭제]도 배열에서 하나 빼고(`splice`) 다시 그린다.

## 학습 목표

1. `let items = []` 에 `push` 로 값을 쌓고, `items.length`(개수)와 `items[i]`(번호는 0 부터)로 꺼내 쓴다. Console 입력 칸에 `items` 를 쳐 배열을 본다.
2. `for (let i = 0; i < items.length; i++)` 로 배열을 처음부터 끝까지 훑는다. 끝을 숫자 대신 `items.length` 로 적는 이유를 말한다.
3. `document.createElement('li')`·`textContent`·`append` 로 목록에 한 줄을 붙인다. 붙이지 않은 요소는 화면에도 Elements 탭에도 없다는 것을 확인한다.
4. `list.innerHTML = ''` 로 비운 뒤 배열 전체를 다시 그리는 함수 `showList()` 를 쓰고, 그 안에서 개수(`N개`)와 빈 목록 안내도 함께 쓴다.
5. 삭제 버튼 틀(`createElement('button')`·`splice(i, 1)`·`showList()`)을 그대로 붙여 가운데 줄을 지우고, 개수가 함께 줄어드는 것을 확인한다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/web-week10/guestbook.html
         글 3개를 남긴 뒤 가운데 줄의 [삭제]를 누른 화면
         남긴 글
         · student01: 안녕하세요 [삭제]
         · student03: 반갑습니다 [삭제]
         2개                     ← 3개에서 하나를 지워 2개
         ← 주소창이 함께 보이게 찍는다
```

- 제출은 이 캡처 **한 장**이다. 목록에 두 줄이 남고, 줄마다 **[삭제]** 가 있고, 목록 아래가 `2개` 이면 된다.
- `web-week10/ex/` 에 비교 예제를 저장하고 값을 바꾼 것은 push 로 남긴다. 기록물·표는 없다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | ex01 배열 → ex02 for → ex03 목록 한 줄 만들기 → ex04 누를 때마다 쌓기 → 데이터가 가는 세 곳 | 새 폴더 `web-week10` 에 지난주 완성본 넣기 → `ex/` 에 다섯 파일 저장 → 값 바꿔 보기 → 새 저장소 만들어 올리기 · Pages 켜기 | `ex/` 비교 예제(확인용) |
| 2일차 | 지우려면 두 곳을 바꿔야 한다 → ex05 비우고 다시 그리기 → ex06 showList → ex07 삭제 버튼 틀 → 조립표 | 여섯 파일 값 바꿔 보기 → `guestbook.html`·`guestbook.js` 조립 → 375·1280 폭과 서버로 확인 → push | 캡처 1 |

각 수업은 `설명·시연 30분 + 실습 60분` 이다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.

## 준비

- 지난주 완성본. 내 `web-week09` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [9주차 `examples/day2/web-week09/`](../week09_architecture_project/examples/day2/web-week09/) 파일을 **Raw** 로 받는다
- VS Code, Chrome(DevTools), Git (`git --version` 으로 확인)
- Node.js LTS(선택). 5주차부터 쓴 [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더에도 둔다([사용 안내](../../tools/static-server/README.md)). Node 가 없는 PC 는 파일을 두 번 눌러 열어도 이번 주 결과는 같다
- 개발자 도구의 **Console** 탭과 **Elements** 탭 위치(오른쪽 클릭 › **검사**, 또는 **F12**)
- 7주차에 만든 방명록의 submit 코드(`event.preventDefault()`·`value`·`trim()`·빈칸 안내)를 기억해 둔다. 이번 주에는 그 코드를 그대로 두고 **결과를 쓰는 곳**만 바꾼다
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 배열 | array | 数组 |
| 뒤에 더하기 | push | 追加 |
| 개수 | length | 长度 |
| 번호(인덱스) | index | 索引 |
| 반복문 | for loop | for 循环 |
| 요소 만들기 | createElement | 创建元素 |
| 붙이기 | append | 添加 |
| 하나 빼기 | splice | 删除一项 |

## 이번 주 비교 예제

1일차 ex01~ex04 는 같은 화면을 쓰므로 코드만 `.js` 파일에 두고, 고르기 페이지 [day1/index.html](examples/day1/index.html) 맨 아래 `<script src>` 네 줄 중 하나만 켜서 연다. 2일차 ex05~ex07 은 화면이 서로 달라서 `.html` 과 `.js` 를 한 쌍으로 둔다. Console 의 번호가 코드의 형제 번호와 같다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_array.js](examples/day1/ex01_array.js) | 1. 빈 배열 / 2. `push` 세 번 / 3·4·5. `items[0]`·`items[2]`·`items[3]` / 6. 처음 값을 넣어 만들기 | 배열은 값을 순서대로 담는다. 번호는 0 부터라서 마지막 번호는 개수보다 하나 작다. 없는 번호는 `undefined` 다. 처음부터 값을 넣을 때는 대괄호 안에 쉼표로 나눠 적는다 | `push` 한 줄 빼기, `items[0]` 을 `items[1]` 로, 6번 배열에 값 하나 더 |
| [ex02_for.js](examples/day1/ex02_for.js) | 1. 끝을 `3` 으로 적은 `for` / 2. 끝을 `items.length` 로 적은 `for` | `for` 는 `i` 를 0 부터 하나씩 올린다. 끝을 `items.length` 로 적으면 몇 개가 들어 있든 끝까지 간다 | `push` 줄 빼기, `<` 를 `<=` 로, `let i` 를 `const i` 로 |
| [ex03_create_li.js](examples/day1/ex03_create_li.js) | 1. 만들기만 / 2. 만들고 붙이기 / 3. 하나 더 붙이기 | 만든 요소는 `append` 로 붙여야 화면에 보인다. `append` 는 맨 뒤에 붙인다 | 맨 끝에 `list.append(li1);` 더하기, `'li'` 를 `'<li>'` 로 |
| [ex04_push_add.js](examples/day1/ex04_push_add.js) | 누를 때 1. 배열에 넣기 / 2. 화면에 붙이기 / 3. 개수 쓰기 | 배열과 화면은 따로다. 둘 다 넣어야 맞는다. 개수는 화면의 줄이 아니라 `items.length` 로 쓴다 | `push` 줄 주석, `append` 줄 주석, 백틱을 작은따옴표로 |
| [ex05_redraw.html](examples/day2/ex05_redraw.html) + [.js](examples/day2/ex05_redraw.js) | 1. 비우지 않고 그리기 / 2. 비우고 그리기 | 다시 그릴 때는 `list.innerHTML = ''` 로 먼저 비운다. 비우지 않으면 앞에 그린 줄이 남는다 | `innerHTML` 줄 주석, 배열에 한 줄 더 |
| [ex06_show_list.html](examples/day2/ex06_show_list.html) + [.js](examples/day2/ex06_show_list.js) | 1. 열 때 `showList()` / 2. [더하기] 뒤 `showList()` | 화면(목록·안내 문장·개수)은 모두 배열에서 다시 만든다. 배열을 바꿀 때마다, 그리고 열 때 한 번 부른다 | 처음 배열에 값 넣기, 열 때 부르는 줄 주석, 누를 때 부르는 줄 주석 |
| [ex07_delete_button.html](examples/day2/ex07_delete_button.html) + [.js](examples/day2/ex07_delete_button.js) | 삭제 버튼 틀: 1. `splice(i, 1)` / 2. `showList()` / 3. `li.append(removeButton)` | 틀을 그대로 옮겨 쓴다. `showList()` 가 다시 그릴 때 버튼마다 번호를 새로 붙인다 | `splice(i, 1)` 의 `1` 을 `2` 로, 틀 안 `showList();` 주석 |

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week10_supabase_data/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(고르기 페이지 `index.html`, ex01~ex04 의 `.js`), 2일차 `day2/`(ex05~ex07 의 `.html`·`.js`, 조립 `web-week10/`)
- 2일차 끝의 `web-week10`(조립 결과): [guestbook.html](examples/day2/web-week10/guestbook.html) · [guestbook.js](examples/day2/web-week10/guestbook.js) · [index.html](examples/day2/web-week10/index.html) · [about.html](examples/day2/web-week10/about.html) · [styles.css](examples/day2/web-week10/styles.css) · [app.js](examples/day2/web-week10/app.js) · [README.md](examples/day2/web-week10/README.md)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data

## 완료 기준

- [ ] 새 저장소 `web-week10` 을 만들어 Pages 를 켰고, `ex/` 에 비교 예제가 있고, 각 예제에서 값을 하나 이상 바꿔 push 했다.
- [ ] `guestbook.html` 의 폼 아래에 `<ul class="card" id="list"></ul>`·`<div id="empty">`·`<div id="count">0개</div>` 가 있다.
- [ ] 공개 주소 `https://student01.github.io/web-week10/guestbook.html` 에서 **남기기**를 누를 때마다 목록에 한 줄씩 쌓이고, 목록 아래 `N개` 가 하나씩 오른다.
- [ ] 줄마다 **[삭제]** 가 있고, 가운데 줄을 지우면 그 줄만 사라지며 개수가 함께 줄어든다. 모두 지우면 `아직 남긴 글이 없습니다.` 와 `0개` 가 보인다.
- [ ] F12 Console 에 `Uncaught` 로 시작하는 빨간 줄이 없다(서버로 열 때 `favicon.ico` 404 한 줄이 보여도 탭 아이콘 요청이라 괜찮다).
- [ ] 글 3개를 남기고 가운데 줄을 지워 `2개` 가 보이는 화면을 주소창과 함께 캡처 1장으로 제출한다.

## 다음 수업 연결

이번 주 목록은 **화면에만** 있다. 새로고침하면 배열과 화면을 새로 만들어 `아직 남긴 글이 없습니다.` 로 돌아간다.
11주차에는 새 저장소 `web-week11` 을 오늘 `web-week10` 의 파일에서 시작하고(**Code › Download ZIP**, 못 받으면 교재의 이번 주 [`examples/day2/web-week10/`](examples/day2/web-week10/)), 한 줄짜리 글을 이름·메시지·날짜를 담은 **객체**로 바꾼 뒤 브라우저 저장소 `localStorage` 에 남겨 **새로고침해도 목록이 남게** 한다.
오늘 만든 `items`·`showList()`·삭제 버튼 틀을 그대로 쓴다. 11주차부터 확인과 캡처는 공개 주소에서만 한다.

## 공식 참고 자료

- [배열 — MDN 입문](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Arrays)
- [Array — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array)
- [Array.prototype.push() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/push)
- [Array.prototype.splice() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/splice)
- [for — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/for)
- [Document.createElement() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/createElement)
- [Element.append() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/append)
- [Element.innerHTML — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/innerHTML)
- [Console 에서 JavaScript 실행하기 — Chrome DevTools](https://developer.chrome.com/docs/devtools/console/javascript?hl=ko)
