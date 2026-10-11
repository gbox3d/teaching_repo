[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules)

# 7주차 예제 — 비교 예제 7개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   ex01 ~ ex03     폼 제출과 preventDefault, 입력 칸의 value, trim (.html + .js 한 쌍)
  day2/   index.html      고르기 페이지 — 맨 아래 script 줄 하나만 켠다
          ex04 ~ ex07     reset 과 focus, 빈값 검사와 return, input 이벤트, 함수 이름만 맡기기 (.js 파일)
          web-week07/     2일차 끝의 web-week07 — 비교 예제에서 본 줄을 모은 조립
```

`exNN_*` 파일은 **파일 하나 = 개념 하나**다. 같은 일을 다르게 한 **형제**(1·2·3번)를 나란히 놓는다.
결과는 화면과 **주소창**, **F12 › Console** 에서 본다. 이번 주에는 Console 설정 ⚙ › **Preserve log** 를 켜 둔다. 폼이 페이지를 다시 열어도 Console 줄이 남는다. 값이나 줄을 바꾸고 저장 → 새로고침으로 무엇이 달라지는지 본다.
**다른 파일의 개념은 섞지 않는다.** 칸을 비우는 `form.reset()` 은 ex04 의 주제라서 1일차 예제에는 없다. 함수 이름만 맡기는 모양은 ex07 의 주제라서 ex06 은 두 칸 모두 `function () { }` 를 그 자리에 쓴다. 앞 예제의 줄을 빌려 쓸 때는 줄 끝에 `// ex01` 처럼 출처를 적었다.
만들기는 마지막 하나, [`day2/web-week07/`](day2/web-week07/) 뿐이다.

1일차 예제는 화면이 서로 다르다(폼 두 개 / 두 칸과 결과 세 줄 / 한 칸). 그래서 예제마다 `.html` 과 `.js` 를 한 쌍으로 둔다. `.html` 을 연다. 두 파일이 같은 폴더에 있어야 한다.
2일차는 네 예제가 같은 화면(방명록 모양 폼, 안내 자리 `#notice`, 결과 자리 `#last`)을 쓴다. 그래서 코드를 `.js` 파일로 떼어 두고 고르기 페이지 [day2/index.html](day2/index.html) 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 네 줄 중 **하나만** 주석 밖에 둔다(VS Code 에서 줄에 커서를 두고 **Ctrl+/**, macOS **⌘+/**). 처음에는 ex04 줄만 켜져 있다. 5·6주차와 같은 방법이다. 둘 이상 켜면 같은 이름의 `const` 가 겹쳐 둘째 파일이 빨간 줄을 내고 실행되지 않는다.
내려받아 이번 주 저장소 `web-week07` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 내 저장소에서는 날짜 폴더 없이 `ex/` 한 곳에 모은다. 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 예제

| 파일 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/ex01_submit.html](day1/ex01_submit.html) + [ex01_submit.js](day1/ex01_submit.js) | 폼 두 개(칸 하나와 보내기 버튼). 2번을 보내면 주소 그대로, 칸 글자 그대로, 결과 `2. 제출을 받았다`, Console 2번. 1번을 보내면 주소 끝에 `?`, 칸이 비고 두 결과 자리가 처음 글자로 돌아간다 | 폼을 보내면 브라우저는 페이지를 **다시 연다**. 리스너는 실행되지만 바꾼 화면이 함께 사라진다. 리스너 첫 줄 `event.preventDefault()` 가 다시 열기를 막는다. 버튼을 눌러도 칸에서 Enter 를 쳐도 같은 `submit` 이다 | Preserve log 를 켜고 1번 보내기 → Console 1번이 남는다. 17행 앞에 `//` → 2번도 다시 열린다. 17행 `event.` 지우기 → `preventDefault is not defined` |
| [day1/ex02_value.html](day1/ex02_value.html) + [ex02_value.js](day1/ex02_value.js) | 이름·메시지 칸과 남기기. 처음 열고 누르면 1번 `1. 열 때 읽은 이름 : `(빈 글자), 2번 지금 적힌 이름, 3번 지금 적힌 메시지 | `value` 는 칸에 **지금** 적힌 글자다. 11행은 열 때 한 번, 15·16행은 누를 때마다 읽는다(6주차 ex02 와 같은 원리). textarea 도 `value` 로 읽는다 | 이름을 바꿔 다시 누르기 → 2번만 바뀐다. 16행 `value` 를 `textContent` 로 → 3번이 빈다. 15행 `velue` → 2번 `undefined` |
| [day1/ex03_trim.html](day1/ex03_trim.html) + [ex03_trim.js](day1/ex03_trim.js) | 이름 칸 하나. 앞뒤에 빈칸을 넣고 누르면 Console 1번 `[  student01  ]`, 2번 `[student01]` | `trim()` 은 앞뒤 빈칸만 뗀 값을 돌려준다. 빈칸만 친 칸은 빈 글자 `''` 가 되고, 가운데 빈칸은 남는다 | 빈칸만 넣기 → 2번 `[]`. `student 01`. 10행 `trm()` → 빨간 줄, `.trim` (괄호 빠짐) → 함수 글자 |
| [day2/index.html](day2/index.html) | 제목과 안내 두 줄, "예제가 쓰는 자리"(이름·메시지 칸, **남기기**, 빈 안내 자리, `아직 남긴 글이 없습니다.`). Console 은 켜 둔 `script` 줄의 예제 것만 찍힌다 | 같은 화면을 쓰는 예제는 JS 만 파일로 떼어 HTML 이 `<script src>` 로 불러온다. 어느 파일을 불러올지는 `script` 줄 하나로 정해진다 | 켜 둔 줄을 바꿔 가며 새로고침 |
| [day2/ex04_reset_focus.js](day2/ex04_reset_focus.js) | 두 칸을 채우고 누르면 Console 1번 `[student01] [안녕하세요]`, 2번 `[] []`. 칸이 비고 커서가 이름 칸에서 깜박인다(3번) | 다음 입력 준비다. `form.reset()` 은 폼 안의 칸을 모두 비운다. 그래서 값은 비우기 **전에** 읽는다. `focus()` 는 커서를 그 칸으로 옮긴다 | 14행 `form.reset();` 을 2번 `console.log` 줄 아래로 → 2번에도 글자. 19행 `nameInput` → `messageInput`. 14행 `rest` → 빨간 줄 |
| [day2/ex05_empty.js](day2/ex05_empty.js) | 이름이 비면 안내 `이름을 입력하세요.`·Console 1번, 메시지가 비면 `메시지를 입력하세요.`·2번, 둘 다 차면 안내가 지워지고 결과 `student01: 안녕하세요`·3번 | `if` 안의 `return` 은 함수를 그 자리에서 끝낸다. 검사는 위에서부터라 둘 다 비면 1번만 나온다. `trim()` 덕분에 빈칸만 친 칸도 1번이다 | 19행 `return;` 앞에 `//` → 1번 다음 3번, 결과 `: 안녕하세요`. 16행 `===` 를 `=` 로 → 빨간 줄 |
| [day2/ex06_input.js](day2/ex06_input.js) | 열자마자 안내 `안내 문구 — 칸에 글자를 치면 사라진다`. 이름 칸에 칠 때마다 Console 1번, 메시지 칸에 칠 때마다 2번이 한 줄씩. 첫 글자에서 안내가 사라진다 | `'input'` 은 칸의 글자가 바뀔 때마다 일어난다. 한 글자 칠 때도, Backspace 로 지울 때도. 한 줄 칸(`input`)과 여러 줄 칸(`textarea`)이 같다 | 11행 `'input'` 을 `'inptu'` 로 → 이름 칸에 쳐도 1번이 없고 안내가 남는다. 빨간 줄은 없다 |
| [day2/ex07_pass_name.js](day2/ex07_pass_name.js) | 열자마자 안내 `안내 문구 — 칸에 글자를 치면 사라진다`. 이름 칸(1번)이나 메시지 칸(2번)에 한 글자를 치면 안내가 사라진다. Console 은 쓰지 않는다 | 미리 만든 함수 `clearNotice` 는 **이름만** 맡기면 칠 때마다 브라우저가 대신 부른다(2번). `function () { }` 안에서 직접 부를 때는 괄호를 붙인다(1번). 두 모양은 하는 일이 같다 | 18행 `clearNotice` 를 `clearNotice()` 로 → 메시지 칸에 쳐도 안내가 남는다. 14행 `clearNotice();` 를 `clearNotice;` 로 → 이름 칸에 쳐도 안내가 남는다. 빨간 줄은 둘 다 없다 |

### 파일 안의 모양

형제 번호가 주석 첫머리와 화면·Console 글자 앞에 있다. [ex02_value.js](day1/ex02_value.js) 에서 인용:

```js
const atOpen = nameInput.value;              // 1. 열 때 한 번 읽는다 — 그때 칸에 있던 글자(보통 빈 글자)

form.addEventListener('submit', function (event) {
    event.preventDefault();                  // ex01: 다시 열리지 않게 막는다
    const atSubmit = nameInput.value;        // 2. 누를 때마다 다시 읽는다 — 지금 적힌 글자
    const message = messageInput.value;      // 3. textarea 도 value 로 읽는다
```

1번과 2번은 같은 `nameInput.value` 다. 다른 것은 그 줄이 리스너 **밖**에 있느냐 **안**에 있느냐 하나다. `event.preventDefault();` 는 ex01 에서 본 줄을 빌려 쓴 것이라 줄 끝에 출처를 적었다.

## `day2/web-week07/` — 2일차 끝의 web-week07

[`day2/web-week07/`](day2/web-week07/) 는 2일차 끝의 `web-week07` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 9주차의 시작점이다. 비교 예제를 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.

| `day2/web-week07/` 파일 | 내 `web-week07` 의 위치 | 따라하기 단계 |
|---|---|---|
| [guestbook.html](day2/web-week07/guestbook.html) | `guestbook.html` | [2일차 8단계](../walkthrough.md#2일차) — `<head>` 에 `<script src="guestbook.js" defer></script>`, `<form id="guestbook-form">`, 3주차 문장 대신 `#notice` 자리·제목·`#last` 카드 |
| [guestbook.js](day2/web-week07/guestbook.js) | `guestbook.js` | [2일차 9단계](../walkthrough.md#2일차) — 새로 만든다. 조립표 순서로 쓰면 이 파일과 글자 단위로 같아진다 |
| [index.html](day2/web-week07/index.html) | `index.html` | 6주차 그대로. 이번 주에 열지 않는다 |
| [app.js](day2/web-week07/app.js) | `app.js` | 6주차 그대로. `index.html` 만 이 파일을 부른다(페이지마다 자기 js 하나) |
| [styles.css](day2/web-week07/styles.css) | `styles.css` | 6주차 그대로. `#last` 카드도 `.card` 모양을 쓴다 |
| [about.html](day2/web-week07/about.html) | `about.html` | 6주차 그대로 |
| [images/profile.png](day2/web-week07/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |
