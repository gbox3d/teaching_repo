[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data)

# 5주차 예제 — 비교 파일 10개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   ex01 ~ ex05     스크립트와 값 (ex02 는 보조 파일 ex02_script_position.js 까지)
  day2/   ex06 ~ ex10     조건과 함수, 화면에 쓰기, 날짜
          build/          2일차 끝의 web-week05 — 비교 파일에서 본 줄을 모은 조립
```

`exNN_*.html` 은 **파일 하나 = 개념 하나**다. 파일마다 같은 일을 다르게 한 **형제**(1·2·3번…)를 나란히 놓는다.
결과는 **F12 › Console** 에서 본다. Console 의 번호와 코드의 형제 번호가 같다. 값이나 주석을 바꾸고 저장 → 새로고침으로 무엇이 달라지는지 본다.
**다른 파일의 개념은 섞지 않는다.** 화면 글자를 바꾸는 것(찾고 → 바꾸기)은 ex09 의 주제라서 ex01~ex08·ex10 은 화면에 쓰지 않고 `console.log` 로만 결과를 보인다. 버튼을 찾아 클릭을 등록하는 한 줄(`document.getElementById('…').addEventListener(…)`)만은 클릭을 보이는 데 꼭 필요해 ex01 부터 쓴다.
작년 수업에서 JavaScript 를 시작한 순서다. 첫날은 버튼 + 클릭 + `console.log`, 다음은 버튼으로 숫자 바꾸기(`innerText`), 그다음은 `parseInt` 덧셈기(입력 칸 + 버튼으로 두 수를 더하는 페이지)였다.
만들기는 마지막 하나, [`day2/build/`](day2/build/) 뿐이다.

각 파일은 단일 HTML 이고 `<script>` 가 안에 있다. ex02 만 보조 파일 [ex02_script_position.js](day1/ex02_script_position.js) 를 같은 폴더에서 불러온다.
내려받아 이번 주 저장소 `web-week05` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장. Raw 가 열리지 않을 때만 주석 줄까지 타이핑). 내 저장소에서는 날짜 폴더 없이 `ex/` 한 곳에 모은다. 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 파일

| 파일 | 열면 보이는 것(Console) | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_click.html](day1/ex01_click.html) | 버튼 하나. 열자마자 Console 에 A·C 두 줄. 버튼을 누를 때마다 B 한 줄 | 스크립트는 위에서 아래로 한 번 실행되고, `addEventListener` 안쪽은 **등록만** 했다가 클릭할 때마다 실행된다. 작년 예제의 `() => {}` 도 여기서는 `function () {}` 와 같은 뜻이다(주석) | 버튼을 여러 번 누르기 → B 만 늘고 A·C 는 그대로. 새로고침 → A·C 가 다시 찍힌다 |
| [ex02_script_position.html](day1/ex02_script_position.html) + [ex02_script_position.js](day1/ex02_script_position.js) | Console 세 줄이 1 → 2 → 3 순서. 셋 다 `document.body` 를 찍는데 1번은 `null`(없다는 값), 2·3번은 `<body>` | 스크립트는 브라우저가 그 줄을 **읽는 순간** 실행된다. head 를 읽는 동안에는 body 가 아직 없어서 `null`. `defer` 는 HTML 을 끝까지 읽은 뒤 실행한다 | `<script src="ex02_script_position.js" defer>` 에서 `defer` 지우기 → 3번도 `null`, 순서가 1 → 3 → 2 로 바뀐다(`defer` 없는 script 는 head 에서 읽는 순간 실행) |
| [ex03_let_const.html](day1/ex03_let_const.html) | 버튼 셋. 열자마자 `처음 값 : 0 0 0`. let 두 번 → `1. let a = 1`·`= 2`, var 한 번 → `3. var c = 1`, const → 빨간 줄 `Uncaught TypeError: Assignment to constant variable.` 만 | `let`·`var` 는 다시 담을 수 있고 `const` 는 안 된다. 다시 담을 일이 없는 값을 `const` 로 두면, 실수로 다시 담을 때 Console 이 알려 준다. 오류는 열 때가 아니라 **그 줄이 실행될 때**(클릭할 때) 나고, 오류 난 줄 아래는 실행되지 않는다 | 빨간 줄 오른쪽 `ex03_let_const.html:24` 로 가 보기. `const b = 0;` 을 `let b = 0;` 으로 바꿔 다시 누르기 |
| [ex04_plus.html](day1/ex04_plus.html) | Console 1~5번 `3 number` · `12 string` · `12 string` · `3 number` · `13 number`. 입력 칸 1 과 2 로 6번 → `12`, 7번 → `3` | `+` 는 둘 다 숫자면 더하고 한쪽이라도 문자열이면 잇는다. 입력 칸의 `value` 는 **늘 문자열**이라 `Number()` 로 바꿔야 더해진다(작년 `parseInt` 덧셈기) | 입력 칸 값을 `10`·`5` 로(6번 `105`, 7번 `15`). 3번의 `'1' + 2` 를 `1 + '2'` 로(값과 `typeof` 괄호 안, 줄 앞 글자도 같이) |
| [ex05_template.html](day1/ex05_template.html) | 1·2번 같은 문장 `안녕하세요, student01님! 지금은 9시입니다.`, 3번은 `안녕하세요, ${name}님!` 글자 그대로, 4번 `한 시간 뒤는 10시입니다.` | 백틱(`` ` ``)으로 감싼 문자열만 `${}` 안을 **계산해** 넣는다. 작은따옴표면 글자 그대로다 | `name`·`hour` 값 바꾸기. 3번의 작은따옴표를 백틱으로 |
| [ex06_compare.html](day2/ex06_compare.html) | Console 1~6번 `true` · `false` · `true` · `false` · `false` · `true` | 비교의 결과는 `true`/`false` **값**이다. `===` 는 종류(숫자·문자열)까지 같아야 참. 문자열끼리는 첫 글자부터 비교해 `'10' < '9'` | `12 > 12` 를 `12 > 11` 로. `'10' > '9'` 를 `'10' > '09'` 로(줄 앞 글자도 같이) |
| [ex07_if_else.html](day2/ex07_if_else.html) | `hour = 20` 으로 1~4번 오후 / 오후 / **저녁** / **오후**. 9 로 바꾸면 (담긴 것 없음) / 오전 / 아침 / 아침 | 위에서부터 보다가 **처음 참인 한 곳만** 실행하고 나머지는 보지 않는다. `else` 는 위가 모두 거짓일 때. 그래서 조건 순서가 결과를 바꾼다 | 맨 위 `const hour = 20;` 을 9 · 12 · 15 로 바꿔 새로고침. 3번과 4번이 언제 같고 언제 다른지 |
| [ex08_function.html](day2/ex08_function.html) | 맨 위에 `안녕하세요, student01님!`(greetLog 가 찍은 것), 1번 `undefined`, 2번 `안녕하세요, student01님!`, 3번 student02 / student03. `이 줄은 찍히지 않는다` 는 없다 | 정의는 이름을 붙여 두기만 하고, 괄호를 붙여 **부를 때** 실행된다. `return` 이 부른 곳에 값을 돌려준다. 없으면 `undefined` | 13행 `console.log(…)` 를 `return …` 으로 바꾸기. 21행 `const a = greetLog('student01');` 위에 `neverCalled();` 한 줄 더하기 |
| [ex09_dom_write.html](day2/ex09_dom_write.html) | 열자마자 Console 에 찾은 요소 두 개와 `null`. 바꾸기 버튼 → 1·2번 글자 바뀜, 3번은 `<b>3. 굵게 될까?</b>` 글자 그대로(굵어지지 않음), 입력 칸 값 바뀜 | 화면을 바꾸려면 **먼저 찾고(요소 값을 받아) 그다음 바꾼다**. 두 찾기 방법은 같은 id 면 같은 요소를 준다(`querySelector` 는 CSS 선택자를 받는다. `#` 은 id 를 뜻한다). 넣은 글자는 태그가 아니라 글자 그대로다. 입력 칸은 `value` | 23행 `console.log(document.querySelector('#p9'));` 아래에 `document.querySelector('#p9').textContent = '…';` 한 줄 더하기 → null 오류, 바꾸기 버튼도 동작하지 않는다. `querySelector('#p2')` 에서 `#` 을 빼 보기 → Console 에 `null`, 버튼을 누르면 27행 오류, 3·4번은 안 바뀐다 |
| [ex10_date.html](day2/ex10_date.html) | Console 에 `now` 한 줄과 1~6번 시 · 분 · 연도 · 월(0부터) · 월 + 1 · 요일(0 = 일요일). 화면에는 여섯 식의 뜻 목록 | `new Date()` 는 그 줄이 실행된 순간의 날짜·시각을 담은 **값**이고, `.getHours()` 는 그 값에게 "몇 시야?" 묻는 것이다. 월은 0부터 센다 | 새로고침 → 분이 다시 잰 값. `now.getSeconds()` 를 찍는 줄 더하기 |

### 파일 안의 모양

형제 번호가 주석 첫머리와 `console.log` 앞 글자에 있다. [ex02_script_position.html](day1/ex02_script_position.html)에서 인용:

```html
<script>
    // 1. head 안의 script: 아직 body 를 읽기 전이다 → document.body 가 없다(null)
    console.log('1. head 안 script :', document.body);
</script>
<!-- 3. defer: 파일을 받아 두었다가 HTML 을 끝까지 읽은 뒤에 실행한다 -->
<script src="ex02_script_position.js" defer></script>
```

주석은 설명과 실험 거리다. `defer` 한 단어를 지우면 3번 파일이 head 에서 읽는 순간 실행되어 1번처럼 `null` 을 찍는다.

같은 조건, 다른 순서는 [ex07_if_else.html](day2/ex07_if_else.html)의 3·4번이다.

```js
if (hour >= 12) {
    m4 = '오후';                 // 20 도 여기서 true → 아래는 보지 않는다
} else if (hour >= 18) {
    m4 = '저녁';                 // 이 줄에는 영영 오지 못한다
} else {
    m4 = '아침';
}
```

3번은 `hour >= 18` 을 먼저 본다. 그래서 20시에 3번은 `저녁`, 4번은 `오후` 다. 큰 수부터 물어야 하는 이유다.

## `day2/build/` — 2일차 끝의 web-week05

[`day2/build/`](day2/build/) 는 2일차 끝의 `web-week05` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 6주차 새 저장소 `web-week06` 의 시작점이다. 비교 파일을 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.

| `day2/build/` 파일 | 내 `web-week05` 의 위치 | 따라하기 단계 |
|---|---|---|
| [index.html](day2/build/index.html) | `index.html` | [2일차 8·10단계](../walkthrough.md#2일차) — `<head>` 에 `<script src="app.js" defer></script>`, `<main>` 첫 줄에 `#greeting` 카드. 두 줄만 늘어난다 |
| [app.js](day2/build/app.js) | `app.js` | [2일차 9·11단계](../walkthrough.md#2일차) — 2주차 카운터 코드를 지우고 조립표 순서로 쓴다. 1행의 아이디(`student01` 자리)만 다르고 나머지는 이 파일과 글자 단위로 같아진다 |
| [about.html](day2/build/about.html) | `about.html` | 4주차 그대로. 이번 주에 열지 않는다 |
| [guestbook.html](day2/build/guestbook.html) | `guestbook.html` | 4주차 그대로. 이번 주에 열지 않는다 |
| [styles.css](day2/build/styles.css) | `styles.css` | 4주차 그대로. `.card` 가 인사말 카드에도 쓰인다 |
| [images/profile.png](day2/build/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |

`app.js` 에 남아 있던 2주차 카운터 코드를 지우는 이유: 그 코드가 찾던 버튼은 3주차에 `index.html` 에서 사라졌다. 찾으면 `null` 이 오고, `null` 에 `addEventListener` 를 쓰면 빨간 오류가 나서 그 아래 줄이 실행되지 않는다(없으면 `null` 은 ex02·ex09, 오류 난 줄 아래가 멈추는 것은 ex03 에서 본 것).

### 조립표 — `web-week05` 의 줄은 어느 ex 에서 본 것인가

`index.html` 두 줄과 `app.js` 21줄은 새로 배우는 것이 없다. 비교 파일에서 본 것을 한 곳에 모은 것이다.

| `web-week05` 의 줄 | 어느 ex 에서 본 것 |
|---|---|
| `index.html` `<head>` 의 `<script src="app.js" defer></script>` | ex02 3번. HTML 을 다 읽은 뒤 실행하므로 아래의 `#greeting` 을 찾을 수 있다 |
| `index.html` 의 `<p class="card" id="greeting">인사말을 준비 중입니다.</p>` | ex09 (찾을 자리에 `id`), 4주차 ex01 (클래스 선택자, `.red` 와 같은 원리), `.card` 규칙은 4주차 `styles.css` |
| `const name = 'student01';` | ex03 (`const`) |
| `const hour = new Date().getHours();` | ex10 (지금 시각 → 시) + ex03 |
| `` function greet(name) { return `안녕하세요, ${name}님!`; } `` | ex08 (정의 · `return`) + ex05 (템플릿 문자열) |
| `function hello(hour) { if (hour >= 12) { return … } else { return … } }` | ex07 (`if / else`) + ex06 (`>=`) + ex08 (`return`) |
| `` const message = `${greet(name)} ${hello(hour)}`; `` | ex05 (`${}` 안은 계산된다 — 함수 호출도) + ex08 (호출) |
| `console.log(hour);` · `console.log(message);` | ex01 (Console) |
| `document.querySelector('#greeting').textContent = message;` | ex09 2번 (찾고 → 바꾼다) |

마지막 두 덩어리가 이번 주 질문의 답이다. [day2/build/app.js](day2/build/app.js)에서 인용:

```js
function hello(hour) {
  if (hour >= 12) {
    return '좋은 오후입니다.';
  } else {
    return '좋은 아침입니다.';
  }
}

const message = `${greet(name)} ${hello(hour)}`;

console.log(hour);
console.log(message);

document.querySelector('#greeting').textContent = message;
```

`hello(hour)` 는 처음 참인 한 갈래의 문장을 돌려준다. 백틱 안의 `${}` 가 두 함수를 부르고, 돌아온 두 문장을 이어 `message` 에 담는다. 마지막 줄이 `#greeting` 을 찾아 그 글자를 바꾼다.
그래서 `day2/build/index.html` 을 열면 카드 글자가 `인사말을 준비 중입니다.` 에서 `안녕하세요, student01님! 좋은 아침입니다.` 로 바뀐다. 12시가 지나면 `좋은 오후입니다.` 다. 둘 다 정답이다.
카드 글자가 `인사말을 준비 중입니다.` 그대로면 마지막 줄까지 가지 못한 것이다. Console 의 빨간 줄과 오른쪽 `app.js:줄` 을 먼저 본다.

## 공식 참고 자료

- [변수에 필요한 정보 저장하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Variables)
- [템플릿 리터럴 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Template_literals)
- [조건문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Conditionals)
- [나만의 함수 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Build_your_own_function)
- [EventTarget.addEventListener() — MDN](https://developer.mozilla.org/ko/docs/Web/API/EventTarget/addEventListener)
- [Document.querySelector() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/querySelector)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [Date — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Date)
