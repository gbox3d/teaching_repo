---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 5주차"
footer: "JavaScript 데이터와 함수 · 변수, if, 함수"
---

# JavaScript 데이터와 함수

4주차까지는 HTML과 CSS로 **보이는 것**을 만들었습니다.
이번 주에는 `app.js`를 되살려 **값을 만들고 문장을 조립**합니다.

```text
my-web/
  index.html   ← script 줄 되살리기 (+ 2일차에 <p id="greeting">)
  app.js       ← 비우고 다시 쓴다 (변수 · 템플릿 문자열 · if · 함수)
  styles.css   ← 4주차 그대로
```

1일차는 **Console만** 봅니다. 화면에 띄우는 것은 2일차입니다.

---

# 1일차 — 값을 만들고 Console에서 확인하기

`30분 설명·시연 → 60분 실습`

1. `script` 줄 되살리기와 `console.log`
2. Console의 빨간 오류 줄 읽기 (`app.js:6`)
3. `const`·`let`에 문자열·숫자 담기
4. 템플릿 문자열로 문장 만들기

---

## 1일차 · 0–5분 — JS는 어디서 실행되나, script 줄 되살리기

```html
<link rel="stylesheet" href="styles.css">
<script src="app.js" defer></script>
```

- 1주차 세 언어: HTML은 **내용**, CSS는 **모양**, JavaScript는 **동작**입니다.
- JavaScript는 **브라우저 안에서** 실행됩니다. 페이지를 열면 그때 돕니다.
- 3주차에 뺐던 `script` 줄을 `index.html`의 `</head>` 앞에 되살립니다.
- `defer`는 "HTML을 다 읽은 **뒤에** 실행하라"는 뜻입니다.
- 2주차 `app.js`의 카운터 코드는 **전부 지우고** 오늘 새로 씁니다.

---

## 1일차 · 5–12분 — console.log와 Console 오류 줄

```js
console.log('app.js가 실행되었습니다');
```

```text
Uncaught ReferenceError: nmae is not defined      app.js:6
```

- `console.log(값)`은 괄호 안의 값을 **Console 탭**에 찍습니다. 화면은 바뀌지 않습니다.
- Console은 **F12**(또는 우클릭 › 검사) → **Console** 탭입니다.
- 빨간 줄 오른쪽의 `app.js:6`이 **파일 이름과 줄 번호**입니다. 거기부터 봅니다.
- `is not defined`는 "그런 이름이 없다"는 뜻이며 대개 오타입니다.
- 오류가 난 줄에서 멈춥니다. 그 아래 `console.log`는 찍히지 않습니다.

---

## 1일차 · 12–20분 — let과 const, 숫자와 문자열

```js
const name = 'student01';
let hour = 9;

hour = 15;
```

- 변수는 값에 이름을 붙여 두는 것입니다. `const`로 시작하고, 다시 넣어야 할 때만 `let`.
- 다시 넣을 때는 `let`을 또 쓰지 않습니다. 이름만 적고 `=` 오른쪽에 새 값을 둡니다.
- `const`에 다시 넣으면 `Uncaught TypeError: Assignment to constant variable.`
- 따옴표 안은 문자열, 따옴표 없는 것은 숫자입니다. `'9'`와 `9`는 다릅니다.
- `=`는 "같다"가 아니라 **"넣는다"**입니다.

---

## 1일차 · 20–27분 — 템플릿 문자열로 문장 만들기

```js
const greeting = `안녕하세요, ${name}님!`;
console.log(greeting);
console.log(`지금은 ${hour}시입니다.`);
```

```text
안녕하세요, student01님!
지금은 15시입니다.
```

- **백틱**(`` ` ``)으로 감싸면 문장 안에 `${변수}`를 끼워 넣을 수 있습니다.
- 작은따옴표로 감싸면 `${name}`이 **글자 그대로** 찍힙니다. 따옴표 종류를 먼저 봅니다.
- 백틱은 키보드 `1` 왼쪽, `Esc` 아래 키입니다. 한글 입력 상태에서는 다른 글자가 들어갑니다.

---

## 1일차 · 27–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--값을-만들어-console에-찍기-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data

1. `index.html`에 `script` 줄을 되살리고 `app.js`를 비웁니다.
2. `console.log`, `const name`, `let hour`를 만들어 Console에서 확인합니다.
3. 템플릿 문자열로 인사 문장을 만들고, 일부러 오타를 내 빨간 줄을 읽어 봅니다.

**설명 합계: 5+7+8+7+3 = 30분**

오늘은 **화면을 건드리지 않습니다.** 확인은 모두 Console에서 합니다.

---

# 2일차 — if와 함수로 인사말 만들기

`30분 설명·시연 → 60분 실습`

1. 되돌리기 `git revert HEAD`
2. `if / else`와 비교 `>=`·`===`
3. `function` 정의·호출과 `return`
4. 화면 한 줄 틀로 `#greeting`에 띄우기

---

## 2일차 · 0–5분 — 오늘 Git 5분: git revert HEAD

```bash
git revert HEAD
```

```text
[main a519cac] Revert "인사말 문구 바꾸기"
 Date: Wed Sep 16 10:24:31 2026 +0900
 1 file changed, 1 insertion(+), 1 deletion(-)
```

- 가운데 `Date:` 줄은 `git revert`가 늘 붙이는 줄입니다. 날짜·시각과 해시는 각자 다릅니다.
- 잘못 commit했을 때 **되돌리는 commit을 새로 하나 더** 만드는 명령입니다.
- 되돌릴 것이 한 줄이 되도록 **오늘 작업을 먼저 commit**하고, 틀린 문장은 그 뒤에 따로 commit합니다.
- 편집기 창이 뜨면 기본 메시지 `Revert "…"` 그대로 저장하고 닫습니다.
- `git log --oneline`에 원래 commit과 되돌린 commit이 **둘 다** 남습니다.
- `git reset HEAD^`는 기록 자체를 지웁니다. **push해서 공유한 commit엔 쓰지 않습니다.**

---

## 2일차 · 5–12분 — if / else와 비교 연산

```js
const hour = new Date().getHours();

if (hour >= 12) {
  console.log('좋은 오후입니다.');
} else {
  console.log('좋은 아침입니다.');
}
```

- `if (조건) { } else { }`: 조건이 맞으면 위, 아니면 아래 중괄호 안이 실행됩니다.
- 비교: `>=` 크거나 같다 · `<=` 작거나 같다 · `===` 값이 같다. `=` 하나는 "넣는다"입니다.
- `new Date().getHours()`는 **오늘 복붙 틀 한 줄**입니다. 지금 시각을 0~23 숫자로 줍니다.
- 두 갈래를 다 보려면 `const hour = 9;`처럼 숫자를 직접 넣어 확인합니다.

---

## 2일차 · 12–19분 — function 정의와 호출

```js
function hello(hour) {
  if (hour >= 12) {
    return '좋은 오후입니다.';
  } else {
    return '좋은 아침입니다.';
  }
}

console.log(hello(15));
```

- `function 이름(매개변수) { }`로 하는 일에 이름을 붙입니다. 정의만으로는 실행되지 않습니다.
- `hello(15)`처럼 이름 뒤에 괄호를 붙여야 **그때** 실행됩니다(호출).
- 괄호 안의 `hour`는 함수가 받는 값입니다. 호출할 때 준 값이 그 자리에 들어갑니다.

---

## 2일차 · 19–25분 — return과 greet(name)

```js
function greet(name) {
  return `안녕하세요, ${name}님!`;
}

const message = `${greet(name)} ${hello(hour)}`;
console.log(message);
```

```text
안녕하세요, student01님! 좋은 아침입니다.
```

- `return`은 함수가 **돌려주는 값**입니다. 돌려받은 값은 변수에 담아 다시 씁니다.
- `return` 없이 `console.log`만 한 함수의 결과는 `undefined`입니다.
- 함수 두 개의 결과를 템플릿 문자열로 이어 붙여 한 문장을 만듭니다.

---

## 2일차 · 25–28분 — 화면 한 줄 틀

```html
<p class="card" id="greeting">인사말을 준비 중입니다.</p>
```

```js
document.querySelector('#greeting').textContent = message;
```

- `index.html`의 `<main>` 첫 줄에 `id="greeting"` 문단을 하나 둡니다.
- 마지막 줄은 **복붙 틀**입니다. "`#greeting`인 자리의 글자를 `message`로 바꿔라".
- 이 줄이 무엇인지는 **6주차**에 배웁니다. 오늘은 모양 그대로 씁니다.
- 글자가 안 바뀌고 `인사말을 준비 중입니다.`가 남아 있으면 그 위 줄에서 오류가 난 것입니다.

---

## 2일차 · 28–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--if와-함수로-인사말-만들기-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data

1. `index.html`에 `#greeting` 문단을 넣고 `if`로 오전·오후 인사를 고릅니다.
2. `greet(name)`·`hello(hour)` 두 함수를 만들어 문장을 조립합니다.
3. 틀 한 줄로 화면에 띄워 commit하고, 틀린 문장을 다시 commit한 뒤 `git revert HEAD`로 되돌립니다.

**설명 합계: 5+7+7+6+3+2 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/my-web/
카드 한 줄: 안녕하세요, student01님! 좋은 아침입니다.
F12 Console: 10 / 안녕하세요, student01님! 좋은 아침입니다.
주소창과 Console이 함께 보이게 찍습니다
```

12시 이후에 열면 `좋은 오후입니다.`가 나옵니다. 둘 다 정답입니다.
2일차를 끝내지 못했으면 1일차 Console 캡처로 인정합니다.

---

## 다음 주 미리 보기

오늘 코드는 페이지를 열 때 **한 번** 실행됩니다.

6주차에는 **버튼을 눌렀을 때** 실행되는 코드를 씁니다.
오늘 복붙 틀로 쓴 `document.querySelector`와 `textContent`가 정식 항목이 되고,
`#greeting`과 `greet(name)`·`hello(hour)`를 그대로 이어받아 클릭 횟수와 다크 모드를 만듭니다.
