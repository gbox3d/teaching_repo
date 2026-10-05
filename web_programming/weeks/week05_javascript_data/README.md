[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data)

# 5주차 — JavaScript 데이터와 함수

이번 주도 부품을 하나씩 본다. 비교 파일 10개를 열어 값을 바꿔 보고, 마지막에 이번 주 새 저장소 `web-week05`의 `index.html`·`app.js`를 그 부품으로 조립한다.
작년 수업 예제(버튼과 `console.log` → 카운터 → 입력 칸 + 버튼으로 두 수를 더하는 페이지)와 같은 방식이다. 첫 파일부터 입력 칸·버튼·클릭·화면 글자·Console 이 함께 나온다. 파일 하나에 개념 하나. 같은 일을 다르게 한 형제를 나란히 놓고 차이를 본다.
JavaScript 는 브라우저가 실행한다. 결과는 **화면**과 **F12 › Console** 두 곳에서 본다.

## 이번 주 질문

> 버튼을 누르면 글자가 바뀌고, 열 때마다 시각에 맞는 인사가 나오게 하려면 무엇을 알아야 하나?

답은 명령 이름 몇 개가 아니다. 세 가지 원리다.
스크립트는 브라우저가 그 줄을 **읽는 순간** 위에서 아래로 한 번 실행되고, `addEventListener` 안쪽은 등록만 했다가 **클릭할 때** 실행된다.
`if` 는 **처음 참인 한 곳만** 실행한다. 화면은 **먼저 찾고, 그다음 바꾼다.**
이 세 줄을 이해하면 조합은 스스로 만들 수 있다.

## 학습 목표

1. 스크립트는 브라우저가 그 줄을 읽는 순간 실행된다. 아직 읽지 않은 요소는 `null` 이고, `defer` 는 HTML 을 끝까지 읽은 뒤 실행한다. `addEventListener` 안쪽은 클릭할 때마다 실행된다. 화면은 먼저 요소를 찾고 그다음 글자를 바꾼다. 못 찾으면 `null` 이다.
2. `let`·`var` 는 다시 담을 수 있고 `const` 는 안 된다. 다시 담을 일이 없는 값을 `const` 로 두면, 실수로 다시 담을 때 Console 이 알려 준다. 오류는 그 줄이 실행될 때 나고, 오류 난 줄 아래는 실행되지 않는다. Console 빨간 줄 오른쪽의 `파일:줄` 에서 찾기 시작한다. 문법 오류(SyntaxError)는 파일 전체가 실행되지 않고, 표시된 줄보다 위에 실수가 있을 수 있다.
3. `+` 는 둘 다 숫자면 더하고 한쪽이라도 문자열이면 잇는다. 입력 칸의 `value` 는 늘 문자열이다. 백틱(`` ` ``)으로 감싼 문자열만 `${}` 안을 계산해 넣는다. `new Date()` 는 그 줄이 실행된 순간의 시각을 담는다.
4. 비교의 결과는 `true`/`false` 값이다. `if / else if / else` 는 위에서부터 보다가 처음 참인 한 곳만 실행한다. 그래서 조건 순서가 결과를 바꾼다.
5. 함수는 정의만으로는 실행되지 않고, 괄호를 붙여 부를 때 실행된다. `return` 이 부른 곳에 값을 돌려주고, 없으면 `undefined` 가 돌아간다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/web-week05/
         카드 한 줄 ─ 안녕하세요, student01님! 좋은 아침입니다.
         F12 Console ─ 10
                       안녕하세요, student01님! 좋은 아침입니다.
         ← 주소창과 Console 두 줄이 한 화면에 보이게 찍는다
```

- 제출은 이 캡처 **한 장**이다. 12시가 지난 시간에 열면 `좋은 오후입니다.` 가 나온다. 둘 다 정답이다.
- 2일차를 끝내지 못했다면 `https://student01.github.io/web-week05/ex/ex01_click.html` 을 열고 Console 에 A·D·B 가 찍힌 화면으로 대신한다. JavaScript 를 처음 쓰는 주여서 두는 완화다.
- `web-week05/ex/` 에 비교 파일을 저장하고 값을 바꾼 것은 push 로 남긴다. 기록물·표는 없다. 산출물은 push 된 파일과 화면이다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 화면과 Console → ex01 지금 실행 vs 클릭할 때 → ex02 script 위치 → ex03 let·const·var → ex04 `+` → ex05 템플릿 문자열 | 새 폴더 `web-week05` 에 지난주 완성본 넣기 → `ex/` 에 다섯 파일(ex02 는 `.js` 까지 여섯 개) 저장 → 값 바꿔 보기 → 새 저장소 만들어 올리기 · Pages 켜기 | `ex/` 비교 파일(확인용) |
| 2일차 | `file://` 과 `http://localhost`(내 PC 웹 서버) → ex06 비교 → ex07 if / else → ex08 function → ex09 화면에 쓰기 → ex10 `new Date()` → 조립표 | 다섯 파일 값 바꿔 보기 → `index.html` 두 줄, `app.js` 조립 → `node server.mjs` 로 열어 확인 → push | 캡처 1 |

각 수업은 `설명·시연 30분 + 실습 60분` 이다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.

## 준비

- 지난주 완성본. 내 `web-week04` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [4주차 `examples/day2/build/`](../week04_responsive_css/examples/day2/build/) 파일을 **Raw** 로 받는다. 4주차를 옛 저장소 `my-web` 으로 수업한 분반은 내 `my-web` 을 같은 방법으로 받아 맨 위 파일과 `images/` 만 넣는다
- VS Code, Chrome(DevTools), Git (`git --version` 으로 확인)
- Node.js LTS(선택). `node -v` 로 확인한다. 2일차에 [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더에 받아 `node server.mjs` 로 띄운다([사용 안내](../../tools/static-server/README.md)). Node 가 없는 PC 는 파일을 두 번 눌러 열어도 이번 주 결과는 같다
- 개발자 도구를 여는 법(오른쪽 클릭 › **검사**, 또는 **F12**. 노트북에서 안 열리면 Fn+F12, macOS 는 ⌘+Option(⌥)+I)과 **Console** 탭 위치
- 4주차 flex 비교 파일 [ex06](../week04_responsive_css/examples/day2/ex06_flex_direction.html) · [ex07](../week04_responsive_css/examples/day2/ex07_justify_content.html) · [ex08](../week04_responsive_css/examples/day2/ex08_align_items.html) · [ex09](../week04_responsive_css/examples/day2/ex09_flex_wrap_gap.html) · [ex10](../week04_responsive_css/examples/day2/ex10_flex_grow.html) · [ex11](../week04_responsive_css/examples/day2/ex11_media.html) 을 아직 열어 보지 않았다면 **먼저 열어 본다**. 지난주 완성본의 메뉴가 좁은 화면에서 세로로 서는 이유가 거기 있다
- 이번 주에 만드는 것은 새 저장소 `web-week05` 와 그 안의 `ex/` 폴더. 고치는 파일은 `index.html` 두 줄과 `app.js` 전체
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 변수 | variable | 变量 |
| 상수 | const | 常量 |
| 문자열 · 숫자 | string · number | 字符串 · 数字 |
| 템플릿 문자열 | template literal | 模板字符串 |
| 조건문 | if / else | 条件语句 |
| 함수 | function | 函数 |
| 돌려주기 | return | 返回 |
| 이벤트 | event | 事件 |

## 이번 주 비교 파일

모두 HTML 파일 하나에 `<script>` 가 들어 있다(ex02 만 보조 파일 `.js` 가 하나 더 있다). 화면의 번호와 Console 의 번호가 코드의 형제 번호와 같다. 값이나 주석을 바꾸고 저장 → 새로고침으로 차이를 본다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_click.html](examples/day1/ex01_click.html) | Console A(열자마자) / D(A 다음) / B(1번 버튼 `function`) / C(2번 버튼 화살표 `() =>`) | 스크립트는 위에서 아래로 한 번 실행되고, `addEventListener` 안쪽은 등록만 했다가 클릭할 때마다 실행된다. `function () {}` 와 `() => {}` 는 여기서 같은 뜻 | 이름을 넣고 두 버튼 누르기. Console 순서가 A·D → B·C 인지 |
| [ex02_script_position.html](examples/day1/ex02_script_position.html) + [ex02_script_position.js](examples/day1/ex02_script_position.js) | 1. head 안 script / 2. body 끝 script / 3. head 에 `defer` 로 연결한 파일 | 스크립트는 브라우저가 그 줄을 읽는 순간 실행된다. 아직 읽지 않은 요소는 없어서 `null`. `defer` 는 HTML 을 끝까지 읽은 뒤 실행한다 | head script 의 `// document.getElementById('msg').innerText = …` 주석 풀기 → 빨간 오류의 `파일:줄` 읽기. js 연결 줄에서 `defer` 지우기 |
| [ex03_let_const.html](examples/day1/ex03_let_const.html) | 1. `let` / 2. `const` / 3. `var` 에 버튼으로 1 더하기 | `let`·`var` 는 다시 담을 수 있고 `const` 는 안 된다. 오류는 그 줄이 실행될 때(클릭할 때) 나고, 오류 난 줄 아래는 실행되지 않는다 | 2번 버튼 → Console `Assignment to constant variable.`. `const b = 0;` 을 `let b = 0;` 으로 바꿔 다시 |
| [ex04_plus.html](examples/day1/ex04_plus.html) | `1 + 2` / `'1' + '2'` / `'1' + 2` / `Number('1') + 2` / `parseInt('12px') + 1`, 입력 칸 두 개로 6. 그냥 더하기 / 7. `Number` 로 바꿔 더하기 | `+` 는 둘 다 숫자면 더하고 한쪽이라도 문자열이면 잇는다. 입력 칸의 `value` 는 늘 문자열이라 `Number()` 로 바꿔야 더해진다 | 입력 칸 값 바꾸기, 표의 식 바꾸기(표 왼쪽 식 글자도 같이, `typeof` 줄도 같이) |
| [ex05_template.html](examples/day1/ex05_template.html) | 1. `+` 로 잇기 / 2. 백틱 템플릿 / 3. 작은따옴표 안 `${}` / 4. `${hour + 1}` | 백틱으로 감싼 문자열만 `${}` 안을 계산해 넣는다. 따옴표면 글자 그대로 | `name`·`hour` 값 바꾸기, 3번의 `'` 를 백틱으로 |
| [ex06_compare.html](examples/day2/ex06_compare.html) | `1 == '1'` / `1 === '1'` / `12 >= 12` / `12 > 12` / `'10' > '9'` / `Number('10') > Number('9')` | 비교의 결과는 `true`/`false` 값이다. `===` 는 종류(숫자·문자열)까지 같아야 참. 문자열끼리는 첫 글자부터 비교한다 | 식의 숫자·따옴표 바꾸기(표 왼쪽 식 글자도 같이) |
| [ex07_if_else.html](examples/day2/ex07_if_else.html) | 입력한 시각으로 1. `if` 만 / 2. `if / else` / 3. `if / else if / else`(큰 수부터) / 4. 같은 조건, 순서만 거꾸로 | 위에서부터 보다가 처음 참인 한 곳만 실행하고 나머지는 보지 않는다. `else` 는 위가 모두 거짓일 때. 그래서 조건 순서가 결과를 바꾼다 | 9 · 12 · 15 · 20 입력 |
| [ex08_function.html](examples/day2/ex08_function.html) | 1. `return` 없는 `greetLog` / 2. `return` 하는 `greet` / 3. 같은 함수, 다른 값 / 4. 입력한 이름으로 부르기, 정의만 한 `neverCalled` | 정의는 이름을 붙여 두기만 하고, 괄호를 붙여 부를 때 실행된다. `return` 이 부른 곳에 값을 돌려준다. 없으면 `undefined` | 이름 입력, `greetLog` 에 `return` 넣기, `neverCalled()` 부르기 |
| [ex09_dom_write.html](examples/day2/ex09_dom_write.html) | 1. `getElementById` + `innerText` / 2. `querySelector('#p2')` + `textContent` / 3. `textContent` 에 `<b>…</b>` / 4. 입력 칸 `value`, Console 에 없는 id → `null` | 화면을 바꾸려면 먼저 찾고 그다음 바꾼다. 두 찾기 방법은 같은 id 면 같은 요소를 준다. 글자만 바꿀 때 `innerText`·`textContent` 결과는 같다. 넣은 글자는 태그가 아니라 글자 그대로다. 입력 칸은 `value` | `#p9` 에 `.textContent` 를 써서 오류 보기, 찾는 id 바꾸기 |
| [ex10_date.html](examples/day2/ex10_date.html) | `getHours()` · `getMinutes()` · `getFullYear()` · `getMonth()` · `getMonth() + 1` · `getDay()` | `new Date()` 는 그 줄이 실행된 순간의 날짜·시각을 담은 값이고, `.getHours()` 는 그 값에게 "몇 시야?" 묻는 것이다. 월은 0부터 센다 | 새로고침, `getSeconds()` 줄 더하기 |
| [server.mjs](../../tools/static-server/server.mjs)(서버) | 두 번 눌러 연 `file:///…` / `node server.mjs` 로 연 `http://localhost:8000/` | 브라우저는 HTML 을 받은 뒤 그 안의 CSS·JS·그림을 하나씩 따로 요청한다(1주차 요청과 응답). 터미널에 한 줄씩 찍힌다 | 새로고침하며 요청 줄 세기, 없는 파일 이름을 주소창에 쳐서 `404` 보기 |

마지막 줄은 비교 파일이 아니라 2일차 0–4분에 쓰는 정적 서버다. 한 학기 내내 같은 파일을 쓴다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week05_javascript_data/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(ex01~ex05), 2일차 `day2/`(ex06~ex10과 조립 `build/`)
- 2일차 끝의 `web-week05`(조립 결과): [index.html](examples/day2/build/index.html) · [app.js](examples/day2/build/app.js) · [about.html](examples/day2/build/about.html) · [guestbook.html](examples/day2/build/guestbook.html) · [styles.css](examples/day2/build/styles.css) · [images/profile.png](examples/day2/build/images/profile.png)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data

## 완료 기준

- [ ] 새 저장소 `web-week05` 를 만들어 Pages 를 켰고, `ex/` 에 비교 파일이 있고, 각 파일에서 값을 하나 이상 바꿔 push 했다.
- [ ] `index.html` 의 `<head>` 에 `<script src="app.js" defer></script>` 가 있고, `<main>` 첫 줄이 `<p class="card" id="greeting">` 이다.
- [ ] 공개 주소 `https://student01.github.io/web-week05/` 을 열면 카드 한 줄에 본인 아이디와 오전·오후 인사가 함께 보인다.
- [ ] F12 Console 에 빨간 줄이 없고, `console.log` 로 찍은 `hour` 와 인사말 두 줄이 보인다.
- [ ] `node server.mjs` 로 `http://localhost:8000/` 을 열고, 터미널의 요청 줄이 HTML·CSS·JS·그림마다 하나씩인 것을 봤다(Node 가 없는 PC 는 두 번 눌러 열기로 대신한다).
- [ ] 주소창과 Console 이 함께 보이는 캡처 1장을 제출한다.

## 다음 수업 연결

오늘 `app.js` 에 쓴 코드는 페이지를 열 때 **한 번** 실행된다. 6주차에는 새 저장소 `web-week06` 을 만들고, 오늘 `web-week05` 의 파일에서 시작한다(**Code › Download ZIP**, 못 받으면 교재의 이번 주 [`examples/day2/build/`](examples/day2/build/)).
그 위에 ex01 에서 본 `addEventListener` 를 쓴다. 오늘 조립한 `#greeting` 과 `greet(name)`·`hello(hour)` 를 이어받아 "인사 바꾸기" 버튼과 클릭 횟수, 다크 모드를 만든다.
두 함수와 `#greeting` 의 이름은 바꾸지 않는다. 결과는 6주차 공개 주소 `https://student01.github.io/web-week06/` 에서 확인한다. 서버 `server.mjs` 도 새 폴더로 옮겨 그대로 쓴다.

## 공식 참고 자료

- [JavaScript 첫걸음 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/What_is_JavaScript)
- [변수에 필요한 정보 저장하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Variables)
- [문자열 다루기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Strings)
- [템플릿 리터럴 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Template_literals)
- [조건문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Conditionals)
- [함수 — 코드 재사용하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Functions)
- [나만의 함수 만들기(return 포함) — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Build_your_own_function)
- [EventTarget.addEventListener() — MDN](https://developer.mozilla.org/ko/docs/Web/API/EventTarget/addEventListener)
- [Document.querySelector() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/querySelector)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [Date — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Date)
- [console.log() — MDN](https://developer.mozilla.org/ko/docs/Web/API/console/log_static)
- [Console 개요 — Chrome DevTools](https://developer.chrome.com/docs/devtools/console?hl=ko)
- [Node.js 내려받기(LTS)](https://nodejs.org/ko)
