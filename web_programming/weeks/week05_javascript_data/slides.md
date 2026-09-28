---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 5주차"
footer: "JavaScript 데이터와 함수 · 비교 예제로 원리를 보고 마지막에 조립"
---

# JavaScript 데이터와 함수

4주차까지 만든 페이지는 **보이는 것**만 바뀌었습니다. 이번 주는 JavaScript 입니다.

이번 주 방식: **비교 예제 10개**를 하나씩 보고, 마지막에 새 저장소 `web-week05` 의 `index.html`·`app.js` 를 **조립**합니다(지난주 완성본에서 시작).

- JavaScript 는 **브라우저가** 실행합니다. 페이지를 열면 그때 돕니다.
- 결과는 두 곳에서 봅니다: **화면**과 **F12 › Console**.
- 파일 하나 = 개념 하나. 같은 일을 다르게 한 형제를 나란히 놓고 차이를 봅니다.
- 실습은 **값을 바꿔 보는 것**입니다. 무엇이 달라질지 먼저 말해 보고 확인합니다.

작년 수업 예제와 같은 순서입니다: 버튼과 `console.log` → 카운터 → 덧셈기(입력 칸 + 버튼으로 두 수를 더하는 페이지).

---

# 1일차 — 스크립트와 값

`30분 설명·시연 → 60분 실습`

1. ex01 — 열 때 실행되는 줄과 클릭할 때 실행되는 줄
2. ex02 — script 위치: 읽는 순간 실행, `defer` 는 다 읽은 뒤
3. ex03 — `let` · `const` · `var`: 다시 담을 수 있나
4. ex04 — `+` 는 더하기와 잇기, 입력 칸의 `value` 는 문자열
5. ex05 — 템플릿 문자열: 백틱 안의 `${}` 만 계산된다

---

## 1일차 · 0–4분 — JavaScript는 브라우저가 실행한다: 화면과 Console

```text
화면     ← 요소를 찾아 글자를 바꾼다 (innerText · textContent)
Console  ← console.log(값) 이 찍힌다. 오류는 빨간 줄 + 파일:줄
document ← 브라우저가 읽어 들인 이 페이지 전체
  document.getElementById('output')   ← id 가 output 인 요소 찾기
  output.innerText = inputName.value + '님 (function)';   ← 글자 바꾸기
```

- 1주차 세 언어: HTML 은 **내용**, CSS 는 **모양**, JavaScript 는 **동작**.
- `<script>` 안의 코드는 브라우저가 위에서 아래로 한 줄씩 실행합니다.
- `console.log` 는 Console 에만 찍습니다. 화면은 그대로입니다.
- Console: 오른쪽 클릭 › 검사 → Console 탭. 또는 F12(노트북 Fn+F12, macOS ⌘+Option(⌥)+I).

**문법이 틀리거나 없는 것을 쓰면 빨간 줄이 뜬다. 결과만 다른 경우(ex04 12)는 조용하다. 그래서 화면과 Console 을 둘 다 본다.**

---

## 1일차 · 4–10분 — ex01 지금 실행 vs 클릭할 때 실행

[examples/ex01_click.html](examples/ex01_click.html)
형제: Console A(열자마자) / D(A 다음) / B(1번 버튼 `function`) / C(2번 버튼 `() =>`)

```js
console.log('A. 페이지를 열자마자 실행된다');
btn1.addEventListener('click', function () {
    console.log('B. 1번 버튼을 누를 때마다 실행된다');
    output.innerText = inputName.value + '님 (function)';
});
```

- 열면 Console 에 A → D. B·C 는 누를 때마다. 2번 `() => {}` 는 작년 예제 모양, 뜻은 같다.
- 바꿔 보기: 이름 칸에 `student01` → 두 버튼 → 화면 `student01님 (function)` / `(화살표)`.

**스크립트는 위에서 아래로 한 번 실행된다. `addEventListener` 안쪽은 등록만 했다가 클릭할 때 실행된다.**

---

## 1일차 · 10–16분 — ex02 script 위치: 읽는 순간 실행된다, defer는 다 읽은 뒤

[examples/ex02_script_position.html](examples/ex02_script_position.html) · [ex02_script_position.js](examples/ex02_script_position.js)
형제: 1. head 안 script / 2. body 끝 script / 3. head 에 `defer` 로 연결한 파일

```text
head <script> 안     console.log('1. …', document.getElementById('msg'));
head                 <script src="ex02_script_position.js" defer></script>
body                 <p id="msg">p#msg — 이 글자가 바뀌면 …</p>
body 끝 <script> 안  console.log('2. …', document.getElementById('msg'));
```

- Console 순서 1(`null` = 찾은 것이 없다) → 2 → 3. 1번 때는 아직 `<p id="msg">` 를 읽기 전.
- 바꿔 보기: head 주석 줄 풀기 → 빨간 오류, `파일:줄` 읽기. `defer` 지우기 → 3번도 `null`, 순서 1→3→2.

**스크립트는 브라우저가 그 줄을 읽는 순간 실행된다. `defer` 는 HTML 을 끝까지 읽은 뒤 실행한다.**

---

## 1일차 · 16–21분 — ex03 let · const · var: 다시 담을 수 있나

[examples/ex03_let_const.html](examples/ex03_let_const.html)
형제: 1. `let` / 2. `const` / 3. `var` — 버튼마다 1 더하기

```js
const b = 0;    // 한 번 담으면 다시 담을 수 없다 (let a · var c 는 다시 담을 수 있다)
document.getElementById('btn-const').addEventListener('click', function () {
    b = b + 1;  // 누를 때 이 줄이 실행되고 여기서 멈춘다
});
```

- 2번 → `Uncaught TypeError: Assignment to constant variable.` `ex03_let_const.html:30`. 화면은 0.
- 바꿔 보기: `const b` 를 `let b` 로 → 2번도 오른다. 열 때는 오류가 없었다는 것도 봅니다.

**`let`·`var` 는 다시 담을 수 있고 `const` 는 안 된다. 오류는 그 줄이 실행될 때 나고, 그 아래 줄은 실행되지 않는다.**

---

## 1일차 · 21–26분 — ex04 +는 두 가지 일을 한다: 더하기와 잇기

[examples/ex04_plus.html](examples/ex04_plus.html)
형제: `1 + 2` / `'1' + '2'` / `'1' + 2` / `Number('1') + 2` / `parseInt('12px') + 1` / 입력 칸 6·7번

```js
1 + 2                                     // 숫자 + 숫자 → 더한다
'1' + 2                                   // 한쪽만 문자열이어도 잇는다
num1.value + num2.value                   // 입력 칸의 value 는 늘 문자열
Number(num1.value) + Number(num2.value)   // 숫자로 바꿔서 더한다
```

- 표: 3 · 12 · 12 · 3 · 13. 종류: number(숫자) · string(문자열) · string · number · number.
- 바꿔 보기: 입력 칸 1·2 → 6번 `12`, 7번 `3`. 5번을 `Number('12px')` 로 → `NaN`. 숫자로 못 바꿨다는 숫자 값이라 종류는 number.

**`+` 는 둘 다 숫자면 더하고, 한쪽이라도 문자열이면 잇는다. 입력 칸은 친 글자라 `value` 는 늘 문자열.**

---

## 1일차 · 26–28분 — ex05 템플릿 문자열: 백틱 안의 ${}만 계산된다

[examples/ex05_template.html](examples/ex05_template.html)
형제: 1. `+` 로 잇기 / 2. 백틱 / 3. 작은따옴표 안 `${}` / 4. `${hour + 1}`

```js
'안녕하세요, ' + name + '님! 지금은 ' + hour + '시입니다.'   // 1
`안녕하세요, ${name}님! 지금은 ${hour}시입니다.`   // ` 로 감싼다
'안녕하세요, ${name}님!'     // ' 로 감싸면 ${} 가 글자 그대로
`한 시간 뒤는 ${hour + 1}시입니다.`   // ${} 안은 계산된다
```

- 1·2번은 같은 문장. 3번은 `${name}` 이 글자 그대로, 4번은 `10시`.
- 바꿔 보기: 3번의 `'` 를 백틱으로. 백틱은 `Esc` 아래 키. `₩` 가 들어가면 영문 입력으로 바꿔 친다.

**백틱(`` ` ``)으로 감싼 문자열만 `${}` 안을 계산해 넣는다. 따옴표면 글자 그대로.**

---

## 1일차 · 28–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--스크립트와-값-60분) · [따라하기](walkthrough.md#1일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data)

1. 새 폴더 `web-week05` 에 지난주 완성본을 넣고, `ex/` 에 ex01~ex05 를 **Raw** 로 저장합니다(ex02 는 `.js` 까지).
2. 파일마다 값을 하나 이상 바꿔 보고, 화면과 Console 이 어떻게 달라지는지 봅니다.
3. 50–60분: 새 저장소 `web-week05` 를 만들어 2주차에 배운 순서 그대로 올리고, Pages 를 켜서 `…/web-week05/ex/ex01_click.html` 을 엽니다.

결과가 이상하면 **Console 을 먼저** 엽니다. 빨간 줄 오른쪽 `파일:줄` 로 갑니다.

**설명 합계: 4+6+6+5+5+2+2 = 30분**

---

# 2일차 — 조건과 함수, 그리고 조립

`30분 설명·시연 → 60분 실습`

1. 내 PC에서 웹 서버로 열기: file:// 과 http://localhost
2. ex06·ex07 — 비교는 `true`/`false`, `if` 는 처음 맞는 한 곳만
3. ex08 — `function` 정의 · 호출 · `return`
4. ex09·ex10 — 먼저 찾고 바꾼다, `new Date()` 는 지금 시각
5. 조립 — `web-week05` 의 `index.html` 두 줄과 `app.js` 를 ex 에서 모은다

---

## 2일차 · 0–4분 — 내 PC에서 웹 서버로 열기: file:// 과 http://localhost

[server.mjs](../../tools/static-server/server.mjs) 를 `web-week05` 에 저장 → `node server.mjs` → `http://localhost:8000/` · [사용 안내](../../tools/static-server/README.md)

```text
200 GET /
200 GET /styles.css
200 GET /app.js
200 GET /images/profile.png
404 GET /favicon.ico        ← 탭 아이콘 요청. 없어도 된다
```

- 두 번 눌러 열면 `file:///…`. 이번 주 파일은 서버로 열어도 결과가 같습니다. 멈추기는 Ctrl+C.
- 나중에 배우는 `fetch`·`type="module"` 은 서버나 공개 주소가 있어야 돕니다.

**브라우저는 HTML 을 받은 뒤 그 안의 CSS·JS·그림을 하나씩 따로 요청한다(1주차 요청과 응답).**

---

## 2일차 · 4–9분 — ex06 비교: 결과는 true 아니면 false

[examples/ex06_compare.html](examples/ex06_compare.html)
형제: `1 == '1'` / `1 === '1'` / `12 >= 12` / `12 > 12` / `'10' > '9'` / `Number('10') > Number('9')`

```js
1 == '1'                     // 값만 맞춰 보고 같다고 한다
1 === '1'                    // 종류(숫자·문자열)까지 같아야 true
12 >= 12                     // 크거나 같다
'10' > '9'                   // 문자열끼리는 첫 글자부터: '1' < '9'
```

- 결과 true · false · true · false · false · true. `=` 하나는 비교가 아니라 담기(ex03).
- 바꿔 보기: 2번을 `1 === 1` 로, 4번을 `12 > 11` 로 → 무엇이 true 로 바뀌나. 표 왼쪽 글자도 같이.

**비교의 결과는 `true`/`false` 값이다. `===` 는 종류까지 같아야 참. 문자열끼리는 첫 글자부터.**

---

## 2일차 · 9–14분 — ex07 if / else: 처음 맞는 한 곳만 실행된다

[examples/ex07_if_else.html](examples/ex07_if_else.html)
형제: 1. `if` 만 / 2. `if/else` / 3. `else if`(큰 수부터) / 4. 3번과 같은 조건, 순서만 거꾸로

```js
if (hour >= 12) {
    m4 = '오후';     // 20 도 여기서 true → 아래는 보지 않는다
} else if (hour >= 18) {
    m4 = '저녁';     // 이 줄에는 영영 오지 못한다
}
```

- 20시: 3번 **저녁**, 4번 **오후**. 9시: 1번 `(담긴 것 없음)`, `else` 는 위가 모두 false 일 때만.
- 바꿔 보기: 9 · 12 · 15 · 20 입력 → 네 줄이 언제 갈리나.

**위에서부터 보다가 처음 참인 한 곳만 실행한다. 그래서 조건 순서가 결과를 바꾼다.**

---

## 2일차 · 14–19분 — ex08 function: 정의 · 호출 · return

[examples/ex08_function.html](examples/ex08_function.html)
형제: 1. `return` 없는 `greetLog` / 2. `return` 하는 `greet` / 3·4. 다른 값으로 부르기

```js
function greetLog(name) { console.log('안녕하세요, ' + name + '님!'); }  // return 없음
function greet(name) { return `안녕하세요, ${name}님!`; }             // 돌려준다
const a = greetLog('student01');    // 호출: Console 에 찍히고, a 에는 undefined
const b = greet('student01');       // 호출: Console 에는 없고, b 에 문장이 담긴다
```

- 화면 1번 `undefined`(아직 담긴 값이 없다는 값), 2번 문장. 괄호 안 `name` = 부를 때 넣은 값(매개변수).
- 바꿔 보기: `greetLog` 에 `return` 넣기. `neverCalled();` 부르기 → Console 한 줄.

**정의는 이름만 붙이고, 괄호를 붙여 부를 때 실행된다. `return` 이 없으면 `undefined` 가 돌아간다.**

---

## 2일차 · 19–24분 — ex09 화면에 쓰기: 먼저 찾고, 그다음 바꾼다

[examples/ex09_dom_write.html](examples/ex09_dom_write.html)
형제: 1. `getElementById` + `innerText` / 2. `querySelector` + `textContent` / 3. 태그 넣기 / 4. `value`

```js
const p1 = document.getElementById('p1');   // id 로 찾는다('#' 없이)
const p2 = document.querySelector('#p2');   // CSS 선택자로 찾는다
p2.textContent = '2. textContent 로 바꿨다';
p3.textContent = '<b>3. 굵게 될까?</b>';        // 태그가 아니라 글자 그대로 보인다
```

- 버튼 → 1·2번 둘 다 글자가 바뀐다(찾는 법·바꾸는 법만 다르다). `#` 은 id(4주차 ex01). 3번은 `<b>` 까지 글자 그대로, 4번은 `value`.
- 바꿔 보기: 없는 `#p9` 에 `.textContent` 쓰기 → `Cannot set properties of null`.

**먼저 찾고(요소를 받아) 그다음 바꾼다. 없는 것을 찾으면 `null` 이고, `null` 은 바꿀 수 없다.**

---

## 2일차 · 24–27분 — ex10 new Date(): 지금 시각을 담은 값

[examples/ex10_date.html](examples/ex10_date.html)
형제: `getHours()` · `getMinutes()` · `getFullYear()` · `getMonth()` · `getMonth() + 1` · `getDay()`

```js
const now = new Date();     // 이 줄이 실행된 순간의 날짜·시각을 담은 값
now.getHours()              // 값에게 "몇 시야?"를 묻는다
now.getMonth()              // 월 — 0부터 센다(1월이 0)
now.getMonth() + 1          // 사람이 읽는 월
```

- 9월 28일 8시 47분에 열면 8 · 47 · 2026 · 8 · 9 · 1. `getDay()` 는 0 = 일요일.
- 바꿔 보기: 새로고침 → 다시 잰다. `getSeconds()` 줄 더하기. 조립의 `new Date().getHours()` 는 위 두 줄을 이어 쓴 것.

**`new Date()` 는 실행된 순간의 시각을 담은 값이고, `.getHours()` 는 그 값에게 묻는 것이다.**

---

## 2일차 · 27–30분 — 조립: web-week05 app.js, 그리고 실습 인계

```text
<script src="app.js" defer>  <p class="card" id="greeting">  ← ex02 · ex09
const name · const hour = new Date().getHours();  ← ex03 · ex10
function greet(name) { return `안녕하세요, ${name}님!`; }  ← ex08 · ex05
function hello(hour) { if (hour >= 12) … else … }  ← ex07 · ex06
const message = `${greet(name)} ${hello(hour)}`;  ← ex05 · ex08
console.log(hour); console.log(message);  ← ex01
document.querySelector('#greeting').textContent = message;  ← ex09 2번
```

[2일차 실습](lab.md#2일차--조건과-함수-그리고-조립-60분) · [따라하기](walkthrough.md#2일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data)

1. ex06~ex10 을 `ex/` 에 저장하고 값을 바꿔 봅니다(33분까지).
2. 조립: `index.html` 에 두 줄, `app.js` 는 비우고 조립표 순서로.
3. 서버로 열어 확인 → 2주차에 배운 순서 그대로 push → 공개 주소에서 카드·Console 캡처.

**설명 합계: 4+5+5+5+5+3+3 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/web-week05/
카드: 안녕하세요, student01님! 좋은 아침입니다.
F12 Console: console.log 두 줄 (hour 숫자 / message 문장)
주소창·카드·Console 이 한 화면에 보이게 찍습니다
```

12시 이후에 열면 `좋은 오후입니다.` 가 나옵니다. 둘 다 정답입니다.
2일차를 끝내지 못했으면 `…/web-week05/ex/ex01_click.html` 에서 Console 에 A·D·B 가 찍힌 화면으로 대신합니다.
캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

오늘 `app.js` 는 페이지를 열 때 **한 번** 실행됩니다.

6주차에는 새 저장소 `web-week06` 을 오늘 완성본에서 시작하고, ex01 에서 본 `addEventListener` 를 씁니다. 누를 때마다 실행되는 코드입니다.
오늘 조립한 `#greeting`·`greet(name)`·`hello(hour)` 를 이어받아 "인사 바꾸기" 버튼과 클릭 횟수를 만듭니다.
다크 모드도 더합니다. 4주차에 정한 `.card` 색을 그때 다시 씁니다.
