[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud)

# 6주차 예제 — 비교 예제 6개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   index.html      고르기 페이지 — 맨 아래 script 줄 하나만 켠다
          ex01 ~ ex03     DOM, 클릭할 때 바꾸기, 클릭 횟수 (.js 파일)
  day2/   ex04 ~ ex06     classList, 다크 모드, 함수 하나를 두 버튼에 (.html + .js 한 쌍)
          web-week06/     2일차 끝의 web-week06 — 비교 예제에서 본 줄을 모은 조립
```

`exNN_*` 파일은 **파일 하나 = 개념 하나**다. 같은 일을 다르게 한 **형제**(1·2·3번)를 나란히 놓는다.
결과는 화면과 **F12 › Console**, 그리고 이번 주에 처음 쓰는 **F12 › Elements** 탭에서 본다. 값이나 줄을 바꾸고 저장 → 새로고침으로 무엇이 달라지는지 본다.
**다른 파일의 개념은 섞지 않는다.** class 를 붙이고 떼는 것은 ex04 의 주제라서 1일차 예제에는 없다.
만들기는 마지막 하나, [`day2/web-week06/`](day2/web-week06/) 뿐이다.

1일차는 세 예제가 같은 화면(글자 자리 하나, 버튼 하나, 횟수 자리 하나)을 쓴다. 그래서 코드를 `.js` 파일로 떼어 두고 고르기 페이지 [day1/index.html](day1/index.html) 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 세 줄 중 **하나만** 주석 밖에 둔다(VS Code 에서 줄에 커서를 두고 **Ctrl+/**, macOS **⌘+/**). 처음에는 ex01 줄만 켜져 있다. 5주차 2일차와 같은 방법이다.
2일차 예제는 화면이 서로 다르다. 그래서 예제마다 `.html` 과 `.js` 를 한 쌍으로 둔다. `.html` 을 연다. 두 파일이 같은 폴더에 있어야 한다.
내려받아 이번 주 저장소 `web-week06` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 내 저장소에서는 날짜 폴더 없이 `ex/` 한 곳에 모은다. 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 예제

| 파일 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/index.html](day1/index.html) | 제목과 안내 두 줄, "예제가 쓰는 자리"(글자 한 줄·**눌러 보기** 버튼·`클릭 0회`). Console 은 켜 둔 `script` 줄의 예제 것만 찍힌다 | JS 를 파일로 떼어 HTML 이 `<script src>` 로 불러온다. 어느 파일을 불러올지는 `script` 줄 하나로 정해진다 | 켜 둔 줄을 바꿔 가며 새로고침 |
| [day1/ex01_dom.js](day1/ex01_dom.js) | 화면 글자가 `3. JavaScript 가 바꾼 글자`. Console 1번 `#document`, 2번 `<div id="message">` 요소 | 브라우저는 HTML 파일을 읽어 요소 상자(**DOM**)를 만들고, 화면은 DOM 을 보여 준다. JS 가 바꾸는 것은 DOM 이다. Elements 탭은 바뀐 DOM 을, 페이지 소스 보기는 바뀌지 않은 파일을 보여 준다 | Elements 의 글자와 페이지 소스(Ctrl+U)의 글자 비교. 4행 `'#message'` 를 `'#msg'` 로 → 2번 `null`, 10행 빨간 줄 |
| [day1/ex02_click_write.js](day1/ex02_click_write.js) | 열자마자 화면 `1. 열자마자 바꾼 글자`, Console 1번 한 줄. 버튼을 누를 때마다 화면 `2. 버튼을 눌러 바꾼 글자`, Console 2번 한 줄씩 | 바꾸는 줄을 `addEventListener` 안에 넣으면 **누를 때** 실행된다. 밖에 두면 열 때 한 번 실행된다(5주차 ex01 과 같은 원리) | 13행을 `});` 아래로 옮기기 → 열자마자 2번 글자 |
| [day1/ex03_counter.js](day1/ex03_counter.js) | 버튼을 누를 때마다 화면 `클릭 1회`·`2회`·`3회`, Console 1번 1·2·3, 2번은 늘 1 | 횟수를 담는 변수는 함수 **밖**에 둔다. 밖의 `let count` 는 열 때 한 번 0 이 되고, 안의 `let inside` 는 누를 때마다 다시 0 이 된다 | 7행 `let count = 0;` 을 함수 안 첫 줄로 옮기기 → 늘 `클릭 1회`. 새로고침 → `클릭 0회` |
| [day2/ex04_classlist.html](day2/ex04_classlist.html) + [ex04_classlist.js](day2/ex04_classlist.js) | 상자 하나와 버튼 셋. 1 add → 노란 배경, 2 remove → 배경 없음, 3 toggle → 누를 때마다 번갈아. Elements 의 `<div id="box">` 줄에 `class="on"` 이 생겼다 사라진다 | 모양은 CSS 규칙(`.on`)이 정하고, JS 는 class 이름만 붙였다 뗀다. `add` 는 이미 있으면 그대로, `remove` 는 없으면 그대로, `toggle` 은 있으면 떼고 없으면 붙인다 | `.on` 의 색 바꾸기(JS 는 그대로). 15행 `'on'` 을 `'On'` 으로 → class 는 붙는데 색이 안 바뀐다 |
| [day2/ex05_dark.html](day2/ex05_dark.html) + [ex05_dark.js](day2/ex05_dark.js) | **다크 모드** 버튼을 누를 때마다 배경과 글자색, 카드까지 어둡게 ↔ 원래대로. Elements 의 `<body>` 줄에 `class="dark"` | 색은 CSS 의 `body.dark` 규칙에 미리 적어 두고 JS 는 `document.body.classList.toggle('dark')` 한 줄만 쓴다. `body.dark .card` 는 "어두운 body 안의 카드"(4주차 `nav a` 와 같은 자손 선택자) | `body.dark .card` 규칙 지우기 → 카드만 흰 채로. `toggle` 을 `add` 로 → 한 번 켜면 꺼지지 않는다 |
| [day2/ex06_reuse.html](day2/ex06_reuse.html) + [ex06_reuse.js](day2/ex06_reuse.js) | A·B 어느 버튼이든 `클릭 N회` 가 하나로 이어서 는다. Console 에 1번(A)·2번(B) | 두 버튼이 같은 일을 하면 그 일을 함수 `countUp()` 하나에 적고 두 곳에서 부른다. 고칠 때 한 곳만 고친다 | 14행 `countUp();` 을 `countUp;` 으로(괄호 빠짐) → 오류 없이 횟수만 안 는다 |

### 파일 안의 모양

형제 번호가 주석 첫머리와 `console.log` 앞 글자에 있다. [ex03_counter.js](day1/ex03_counter.js) 에서 인용:

```js
let count = 0;                     // 1. 함수 밖: 열 때 한 번만 0 이 된다

btn.addEventListener('click', function () {
    count = count + 1;             // 누를 때마다 1 씩 는다
    countBox.textContent = `클릭 ${count}회`;
    console.log('1. 밖에 둔 count :', count);

    let inside = 0;                // 2. 함수 안: 누를 때마다 다시 0 이 된다
    inside = inside + 1;
    console.log('2. 안에 둔 inside :', inside);
});
```

1번과 2번은 `+ 1` 하는 줄이 똑같다. 다른 것은 `let` 줄이 함수 **밖**에 있느냐 **안**에 있느냐 하나다.

## `day2/web-week06/` — 2일차 끝의 web-week06

[`day2/web-week06/`](day2/web-week06/) 는 2일차 끝의 `web-week06` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 7주차 새 저장소 `web-week07` 의 시작점이다. 비교 예제를 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.

| `day2/web-week06/` 파일 | 내 `web-week06` 의 위치 | 따라하기 단계 |
|---|---|---|
| [index.html](day2/web-week06/index.html) | `index.html` | [2일차 8단계](../walkthrough.md#2일차) — `#greeting` 카드 아래에 버튼 줄과 `#count` 카드가 늘어난다 |
| [styles.css](day2/web-week06/styles.css) | `styles.css` | [2일차 9단계](../walkthrough.md#2일차) — 맨 아래에 `body.dark` 규칙 하나가 늘어난다(ex05) |
| [app.js](day2/web-week06/app.js) | `app.js` | [2일차 10단계](../walkthrough.md#2일차) — 조립표 순서로 다시 쓴다. 1행의 아이디(`student01` 자리)만 다르고 나머지는 이 파일과 글자 단위로 같아진다 |
| [about.html](day2/web-week06/about.html) | `about.html` | 5주차 그대로. 이번 주에 열지 않는다 |
| [guestbook.html](day2/web-week06/guestbook.html) | `guestbook.html` | 5주차 그대로. 그 폼이 동작하는 것은 7주차다 |
| [images/profile.png](day2/web-week06/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |
