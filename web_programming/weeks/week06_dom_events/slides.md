---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 6주차"
footer: "DOM·이벤트 · 비교 예제로 원리를 보고 마지막에 조립"
---

# DOM과 클릭 이벤트

5주차 코드는 페이지를 열 때 **한 번** 실행됐습니다. 이번 주는 **누를 때마다** 바뀌는 페이지입니다.

이번 주 방식도 같습니다: **비교 예제 6개**를 하나씩 보고, 마지막에 새 저장소 `web-week06` 의 `index.html`·`styles.css`·`app.js` 를 **조립**합니다(지난주 완성본에서 시작).

- 브라우저는 HTML 파일을 읽어 **DOM**(요소 상자)을 만들고, JS 는 그 상자를 찾아서 바꿉니다.
- 결과는 화면, **Console**, 그리고 새로 쓰는 **Elements** 탭에서 봅니다.
- 필수는 1차시 카운터 여섯 줄, 2차시 색 두 곳과 함수 연결 세 줄입니다. 비교 예제의 추가 수정은 선택입니다.

---

# 1일차 — DOM 과 클릭

`강의·시연 60분 → 학생 실습 30분`

1. 예제 폴더 — `index.html`·`styles.css`·`app.js` 세 파일
2. ex01 — HTML 파일과 DOM: Elements 와 페이지 소스
3. ex02 — 열 때 바꾸기 vs 클릭할 때 바꾸기
4. ex03 — 클릭 횟수: 변수는 함수 밖에

---

## 1일차 · 0–5분 — 예제 폴더 하나에 파일 세 개

사전에 준비한 폴더·서버를 첫 5분에 확인합니다. 예제마다 같은 이름의 세 파일을 둡니다.

```text
ex01/
  index.html   화면 — 예제가 쓰는 자리
  styles.css   모양 — 자리에 배경색(.card)
  app.js       동작 — 이번 주 원리는 여기
```

- 여는 것은 `index.html`. `<head>` 의 `<link>` 와 `<script src … defer>` 가 두 파일을 불러옵니다.
- 코드는 `app.js` 에서 고치고, 결과는 `index.html` 을 새로고침해 봅니다.
- 맨 위 내 사이트 파일과 이름이 같습니다. 편집기 위쪽 경로 줄(`ex › ex01`)로 구분합니다.

**화면은 HTML, 모양은 CSS, 동작은 JS — 세 파일을 한 폴더에.**

---

## 1일차 · 5–20분 — ex01 HTML 파일과 DOM

[examples/day1/ex01/index.html](examples/day1/ex01/index.html) · [styles.css](examples/day1/ex01/styles.css) · [app.js](examples/day1/ex01/app.js)

```text
HTML 파일(페이지 소스)  ──읽기──▶  요소 상자들(DOM)  ──▶  화면
     그대로                       JS 가 찾아서 바꾼다
```

```js
const message = document.querySelector('#message');
message.textContent = '3. JavaScript 가 바꾼 글자';
```

- **Elements** 탭: 지금의 DOM. 바뀐 글자가 보입니다.
- **페이지 소스**(Ctrl+U): 파일. 원래 글자 그대로입니다.
- 바꿔 보기: `'#message'` 를 `'#msg'` 로 → `null`, 빨간 줄.

**JS 가 바꾸는 것은 파일이 아니라 브라우저가 만든 DOM 이다.**

---

## 1일차 · 20–35분 — ex02 열 때 바꾸기 vs 클릭할 때 바꾸기

[examples/day1/ex02/index.html](examples/day1/ex02/index.html) · [styles.css](examples/day1/ex02/styles.css) · [app.js](examples/day1/ex02/app.js)

```js
message.textContent = '1. 열자마자 바꾼 글자';        // 1. 열 때 한 번

btn.addEventListener('click', function () {
    message.textContent = '2. 버튼을 눌러 바꾼 글자';  // 2. 누를 때마다
});
```

- 열자마자 1번, 누를 때마다 2번. 5주차 ex01 의 A·C 와 B 와 같습니다.
- 바꿔 보기: 2번 줄을 `});` 아래로 옮기면? 열자마자 2번 글자, 버튼은 Console 만 찍고 화면은 그대로입니다.

**바꾸는 줄을 `addEventListener` 안에 넣으면 누를 때마다 실행된다.**

---

## 1일차 · 35–50분 — ex03 클릭 횟수: 변수는 함수 밖에

[examples/day1/ex03/index.html](examples/day1/ex03/index.html) · [styles.css](examples/day1/ex03/styles.css) · [app.js](examples/day1/ex03/app.js)

```js
let count = 0;                     // 1. 함수 밖
btn.addEventListener('click', function () {
    count = count + 1;
    countBox.textContent = `클릭 ${count}회`;
    let inside = 0;                // 2. 함수 안
    inside = inside + 1;
});
```

- 세 번 누르면 1번 1·2·3, 2번은 1·1·1. `+ 1` 하는 줄은 같습니다.
- 새로고침하면 `클릭 0회`. 파일을 다시 읽어 DOM 과 변수를 새로 만듭니다.

**누를 때마다 이어서 세려면 변수를 함수 밖에 둔다.**

---

## 1일차 · 50–60분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차) · [따라하기](walkthrough.md#1일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_events)

50~55분은 잘못된 ID·함수 안 count 오류 시연, 55~60분은 실습 안내입니다.

1. 버튼 ID 대조 5분.
2. [ex03 시작 틀](examples/day1/ex03/app.start.js)의 count·textContent 여섯 줄 작성 15분.
3. 세 번 클릭해 3회, 새로고침해 0회 확인 10분.

완성 예제의 inside와 console 로그는 시연 코드입니다. 파일·저장소는 사전 준비, 업로드는 수업 뒤입니다.

**강의 5+15+15+15+5+5 = 60분, 실습 5+15+10 = 30분**

---

# 2일차 — class 와 함수, 그리고 조립

`강의·시연 60분 → 학생 실습 30분`

1. ex04 — `classList.add / remove / toggle`
2. ex05 — 다크 모드: `body.dark` 규칙과 `toggle('dark')`
3. ex06 — 함수 하나를 두 버튼에
4. 8주차 중간 실기 안내
5. 조립 — `web-week06` 의 `index.html`·`styles.css`·`app.js`

---

## 2일차 · 0–20분 — 준비 5분과 ex04 시연 15분

[examples/day2/ex04/index.html](examples/day2/ex04/index.html) · [styles.css](examples/day2/ex04/styles.css) · [app.js](examples/day2/ex04/app.js)

```css
.on { background-color: gold; }
```

```js
box.classList.add('on');      // 1. 붙인다. 이미 있으면 그대로
box.classList.remove('on');   // 2. 뗀다. 없으면 그대로
box.classList.toggle('on');   // 3. 있으면 떼고, 없으면 붙인다
```

- Elements 의 `<div id="box">` 줄에 `class="on"` 이 생겼다 사라집니다.
- 바꿔 보기: `styles.css` 의 `.on` 색만 바꾸면? `app.js` 는 그대로인데 색이 바뀝니다.

**모양은 CSS 규칙이 정하고, JS 는 class 이름만 붙였다 뗀다.**

---

## 2일차 · 20–35분 — ex05 다크 모드: body 에 class 하나

[examples/day2/ex05/index.html](examples/day2/ex05/index.html) · [styles.css](examples/day2/ex05/styles.css) · [app.js](examples/day2/ex05/app.js)

```css
body.dark { background-color: #222222; color: #eeeeee; }   /* 1 */
body.dark .card { background-color: #222222; }             /* 2 */
```

```js
darkButton.addEventListener('click', function () {
    document.body.classList.toggle('dark');
});
```

- `document.body` 는 `<body>` 요소입니다. 찾지 않고 바로 씁니다.
- 바꿔 보기: `styles.css` 의 2번 규칙을 지우면? 카드만 흰 채로 남습니다(4주차 `nav a` 같은 자손 선택자).

홈의 h1·h2·nav a에는 `body.dark` 선택자로 `#a7c5ff`, footer에는 `#c8d4eb`를 지정합니다. 자체 color가 있으면 body 글자색을 그대로 상속하지 않습니다.

---

## 2일차 · 35–50분 — ex06 함수 하나를 두 버튼에

[examples/day2/ex06/index.html](examples/day2/ex06/index.html) · [styles.css](examples/day2/ex06/styles.css) · [app.js](examples/day2/ex06/app.js)

```js
function countUp() {
    count = count + 1;
    countBox.textContent = `클릭 ${count}회`;
}
// A 버튼과 B 버튼의 클릭 함수 안에서 둘 다
countUp();
```

- A·B 를 섞어 눌러도 횟수는 하나로 이어집니다. 고칠 일이 생기면 함수 한 곳만 고칩니다.
- 바꿔 보기: `countUp;`(괄호 없음) → 오류도 없이 아무 일도 안 합니다. 부를 때는 괄호.

**같은 일은 함수 하나에 적고, 여러 곳에서 부른다.**

---

## 2일차 · 50–55분 — 8주차 중간 실기 안내

- 8주차는 중간 개인 실기입니다. 1~7주 실습 제출을 정리한 문제 은행에서 값을 바꿔 출제합니다.
- 문제 은행은 미리 공개되어 있습니다: [8주차 예제](../week08_midterm/examples/README.md). 문제마다 시작 파일·할 일·확인할 것이 있습니다.
- 해답은 공개하지 않습니다. 매주 실습을 **직접** 해 본 것이 연습입니다.
- 시험 중 교재 열람은 됩니다. 범위는 Pages·HTML·CSS·DOM·W3.CSS(7주차까지)입니다.
- 목록 추가·삭제는 10주차, 새로고침해도 남기기는 11주차입니다.

**매주 실습이 곧 시험 준비다.**

---

## 2일차 · 55–60분 — 조립: web-week06, 그리고 실습 인계

```text
index.html  버튼 두 개 · #count 카드             ← ex02 · ex03
styles.css  body.dark, body.dark .card { … }     ← ex05
app.js      const … = querySelector('#…') 네 줄   ← ex01
            let count = 0;                        ← ex03 1번
            function countUp() { … }              ← ex06
            greeting.textContent = `…`;           ← ex02 1번
            hello 버튼: 문장 바꾸기 + countUp()   ← ex02 2번 · ex06
            dark 버튼: toggle('dark') + countUp() ← ex05 · ex06
```

[2일차 실습](lab.md#2일차) · [따라하기](walkthrough.md#2일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_events)

1. 제공 CSS의 다크 배경·글자 두 값 변경 5분.
2. [홈 시작 틀](examples/day2/web-week06/app.start.js)의 toggle·countUp 세 줄 연결 10분.
3. 두 버튼과 375/1280px 확인 10분, 캡처 5분.

HTML·greet·hello·countUp·리스너 틀은 제공됩니다. app.js 전체를 다시 쓰지 않습니다.

**강의 5+15+15+15+5+5 = 60분, 실습 5+10+10+5 = 30분**

---

## 제출하기

수업 안에서는 localhost 또는 파일 주소의 캡처 **한 장**을 제출합니다. 수업 뒤 commit·push하고 아래 공개 주소에서 확인합니다.

```text
https://student01.github.io/web-week06/
어두운 화면 ─ [인사 바꾸기] [다크 모드]
카드: 반갑습니다. 오늘도 좋은 하루 되세요.
카드: 클릭 2회 (1 이상이면 됩니다)
주소창이 함께 보이게 찍습니다
```

캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

오늘은 버튼을 눌렀을 때 **정해 둔 글자**를 띄웠습니다.

7주차에는 오늘의 방명록 화면을 W3.CSS로 바꿉니다. CDN과 입력창·버튼·카드·메뉴 클래스를 배웁니다.
폼 동작은 제공 코드로 확인합니다. JavaScript가 사용하는 id를 유지하고 class로 모양을 바꿉니다.
