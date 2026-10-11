[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules)

# 7주차 따라하기 — 비교 예제로 원리를 보고 마지막에 조립

이번 주는 새 저장소 `web-week07`을 만든다. 지난주 완성본을 넣고, 비교 예제는 그 안의 `ex/` 폴더에 저장한다. 값·줄을 바꾼 뒤 결과를 화면과 주소창, **F12 › Console**에서 본다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

비교 예제 7개는 교재 저장소의 [examples/day1](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules/examples/day1)(1일차 ex01~ex03)과 [examples/day2](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules/examples/day2)(2일차 고르기 페이지와 ex04~ex07) 폴더에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다.

## 1일차

### 1. web-week07 폴더 만들고 지난주 완성본 넣기

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-week07`을 만들고 VS Code **File › Open Folder**로 연다.

지난주 완성본을 넣는다. 내 `web-week06` 저장소 GitHub 화면에서 **Code › Download ZIP**을 누르고, 압축을 푼 폴더에서 맨 위 파일(`index.html`·`about.html`·`guestbook.html`·`styles.css`·`app.js`·`server.mjs`)과 `images/`를 `web-week07`로 옮긴다. 지난주 `ex/` 폴더는 옮기지 않는다.
ZIP을 못 받았으면 교재 [6주차 `examples/day2/web-week06/`](../week06_dom_crud/examples/day2/web-week06/)의 파일을 2단계와 같은 **Raw** 방법으로 받고, [server.mjs](../../tools/static-server/server.mjs)도 같은 방법으로 받는다.

이어서 `web-week07` 안에 `ex` 폴더를 만든다. 현재 폴더: `web-week07`

```bash
mkdir ex
```

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week07/
  ex/            ← 아직 비어 있다
  images/
  about.html
  app.js
  guestbook.html
  index.html
  server.mjs
  styles.css
```

`guestbook.html`을 두 번 눌러 열고, 이름과 메시지를 아무렇게나 넣어 **남기기**를 누른다.

**예상 결과** — 주소창 끝에 `?`가 붙고(`…/guestbook.html?`) 칸이 모두 빈다. 화면 아래 문장은 3주차에 적어 둔 `지금은 눌러도 주소창만 바뀐다. 화면에 띄우는 일은 7주에 한다.` 그대로다. F12 › Console에 빨간 줄은 없다.

- 오류가 아니다. 브라우저가 폼을 "보내려고" 같은 파일을 다시 연 것이다. 이번 주는 이 폼을 동작하게 한다.
- `guestbook.html`은 오늘 고치지 않는다. 2일차 끝에 조립한다. `index.html`·`about.html`·`styles.css`·`app.js`는 이번 주에 고치지 않는다.

### 2. 비교 예제 가져오기

오늘 파일은 여섯 개다. 예제 세 개가 `.html`과 `.js` 한 쌍씩이다. 세 예제의 화면(폼과 결과 자리)이 서로 달라서 `.html`을 따로 둔다.

| 파일 | 비교하는 것 |
|---|---|
| [ex01_submit.html](examples/day1/ex01_submit.html) + [ex01_submit.js](examples/day1/ex01_submit.js) | 1. 막지 않는 폼 / 2. `event.preventDefault()`로 막는 폼 |
| [ex02_value.html](examples/day1/ex02_value.html) + [ex02_value.js](examples/day1/ex02_value.js) | 1. 열 때 읽은 `value` / 2. 누를 때 읽은 `value` / 3. textarea의 `value` |
| [ex03_trim.html](examples/day1/ex03_trim.html) + [ex03_trim.js](examples/day1/ex03_trim.js) | 1. `value` 그대로 / 2. `trim()` 한 값 |

[교재 저장소 examples/day1 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules/examples/day1)에서 파일을 누르고 오른쪽 위 **Raw**를 누른다. 코드만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `web-week07/ex/`에 저장한다. 파일 이름은 교재와 **같게** 둔다. Raw가 열리지 않을 때만 주석 줄까지 그대로 친다.

**예상 결과** — `ex/` 안에 파일 여섯 개가 있다.

```text
ex/
  ex01_submit.html
  ex01_submit.js
  ex02_value.html
  ex02_value.js
  ex03_trim.html
  ex03_trim.js
```

- 저장한 파일 이름이 `.txt`로 끝나면 이름을 고친다. 이름은 VS Code 탐색기에서 확인한다.
- `.html`과 `.js`는 짝이다. `.html`이 같은 폴더의 `.js`를 불러온다. `.js`를 빠뜨리면 막는 코드가 없어서, 어느 폼이든 보내면 페이지가 다시 열린다.

### 3. 여는 법과 Preserve log

`ex/ex01_submit.html`을 Chrome으로 연다(VS Code 탐색기에서 오른쪽 클릭 › **Reveal in File Explorer**, macOS는 **Reveal in Finder** → 두 번 누르기). `.js` 파일은 두 번 누르지 않는다.

F12 › **Console**을 연다. 이번 주에는 Console 설정을 하나 켠다. Console 위쪽 오른편의 ⚙(**Console settings**)를 누르고 **Preserve log**에 체크한다. 페이지가 다시 열려도 Console 줄이 지워지지 않고 남는다. 이번 주에는 폼이 페이지를 다시 여는 일이 많아서 켜 둔다.

2번 칸에 `abc`를 넣고 **2. 보내기**를 누른다.

**예상 결과** — 주소창은 그대로다. 2번 칸의 `abc`도 그대로고, 2번 결과 자리가 `2. 제출을 받았다`로 바뀐다. Console에 한 줄이 찍힌다.

```text
2. form2 에서 submit          ex01_submit.js:19
```

이어서 1번 칸에 `xyz`를 넣고 **1. 보내기**를 누른다.

**예상 결과** — 주소창 끝에 `?`가 붙는다(`…/ex01_submit.html?`). 두 칸이 모두 비고(2번 칸의 `abc`도 사라진다), 1번·2번 결과 자리가 모두 처음 글자(`1번 결과 자리`·`2번 결과 자리`)로 돌아간다. Preserve log를 켰으므로 Console에 `1. form1 에서 submit`(`ex01_submit.js:12`) 줄이 남아 있다.

- 1번 리스너도 실행됐다. 그런데 곧바로 페이지가 통째로 다시 열려 바꾼 글자가 사라졌다. 2번 결과까지 돌아간 것이 그 증거다.
- 2번은 리스너 첫 줄 `event.preventDefault();`가 "다시 열기"를 막았다. 막아야 바꾼 화면이 남는다.
- 줄이 너무 쌓이면 Console에서 오른쪽 클릭 › **Clear console**로 지운다. Preserve log는 이번 주 내내 켜 둔다.

### 4. 값 바꾸는 요령

실험은 늘 같은 순서다. **VS Code에서 고치고 저장**(Ctrl+S, macOS는 ⌘+S) → **브라우저에서 새로고침**(F5, macOS는 ⌘+R) → **화면·주소창·Console**을 본다.
바꾸기 전에 무엇이 달라질지 먼저 말해 보고 확인한다.

**입력해 보기** — `ex/ex02_value.html`을 연다. 이름 `student01`, 메시지 `안녕하세요`를 넣고 **남기기**를 누른다.

**예상 결과** — 아래 세 줄이 화면에 보인다. 1번은 콜론 뒤가 비어 있다.

```text
1. 열 때 읽은 이름 : 
2. 누를 때 읽은 이름 : student01
3. 누를 때 읽은 메시지 : 안녕하세요
```

이름을 `student02`로 바꿔 한 번 더 누르면 2번만 `student02`로 바뀐다. 11행 `const atOpen = nameInput.value;`는 열 때 한 번, 15행 `const atSubmit = nameInput.value;`는 누를 때마다 실행되기 때문이다(6주차 ex02와 같은 원리).

- `value`는 칸에 **지금** 적혀 있는 글자다. 그래서 누를 때 읽는다.
- 값을 원래대로 못 돌리겠으면 교재에서 그 파일을 다시 **Raw**로 받아 덮어쓴다.
- 파일마다 무엇을 바꿔 볼지는 [1일차 실습](lab.md#1일차--폼-제출과-입력-값-60분)에 있다.

### 5. 이번 주 저장소 만들어 올리기

1일차 50–60분에 한다. 세 예제에서 각각 값 하나 이상을 바꿔 봤으면 올린다.

GitHub에서 **New repository**를 누르고 이름 `web-week07`, **Public**으로 만든다. README는 추가하지 않는다.
터미널에서 2주차에 배운 순서 그대로 친다. 현재 폴더: `web-week07`

```bash
git init
git add .
git commit -m "7주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week07.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save**를 누른다.

**예상 결과** — GitHub 저장소 화면을 새로고침하면 `ex/`·`images/`와 맨 위 파일들이 보인다.
1~3분 뒤 `https://student01.github.io/web-week07/ex/ex01_submit.html`을 연다. 두 폼이 보이고 **2. 보내기**는 주소를 바꾸지 않는다. 이 화면은 **확인용**이다.
공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 주소는 파일 이름까지 쓴다. 1일차 `ex/`에는 `index.html`이 없어서 `…/web-week07/ex/`까지만 치면 보여 줄 페이지가 없다. 404 화면이 나오면 [막혔을 때](lab.md#막혔을-때)의 마지막 줄을 본다.
- push가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../week02_github_pages/lab.md#막혔을-때)를 본다.

## 2일차

### 6. 폴더 열고 2일차 예제 다섯 파일 가져오기

같은 PC에 `web-week07` 폴더가 남아 있으면 VS Code로 그대로 연다. 없으면 받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week07.git
```

내려받은 `web-week07`을 **File › Open Folder**로 연다.

오늘 파일은 다섯 개다. 고르기 페이지 `index.html` 하나와 예제 코드 `.js` 네 개다. 네 예제가 같은 화면(방명록 모양 폼, 안내 자리, 결과 자리)을 쓰기 때문에 화면은 `index.html` 하나에 두고 코드만 따로 뗐다. [교재 저장소 examples/day2 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules/examples/day2)에서 1일차와 같은 **Raw** → 저장으로 `web-week07/ex/`에 넣는다. `web-week07/` 하위 폴더는 받지 않는다.

| 파일 | 비교하는 것 |
|---|---|
| [index.html](examples/day2/index.html) | 고르기 페이지. 맨 아래 `<script src>` 네 줄 중 하나만 켠다. 폼 `#form`·이름 칸 `#name`·메시지 칸 `#message`·안내 자리 `#notice`·결과 자리 `#last`가 여기 있다 |
| [ex04_reset_focus.js](examples/day2/ex04_reset_focus.js) | 다음 입력 준비 — 비우기 전에 읽은 값 / `form.reset()` 뒤에 읽은 값 / `focus()` 로 커서 옮기기 |
| [ex05_empty.js](examples/day2/ex05_empty.js) | 이름이 빔 / 메시지가 빔 / 둘 다 찼음 — `if` 안의 `return` |
| [ex06_input.js](examples/day2/ex06_input.js) | `'input'` 이벤트 — 이름 칸(`input`) / 메시지 칸(`textarea`) |
| [ex07_pass_name.js](examples/day2/ex07_pass_name.js) | 함수 맡기기 — `function () { clearNotice(); }` / 이름만 맡긴 `clearNotice` |

`ex/index.html`을 Chrome으로 열고, VS Code에서도 열어 맨 아래를 본다.

```html
<script src="ex04_reset_focus.js"></script>
<!-- <script src="ex05_empty.js"></script> -->
<!-- <script src="ex06_input.js"></script> -->
<!-- <script src="ex07_pass_name.js"></script> -->
```

지금은 ex04 줄만 켜져 있다. 다른 예제로 바꿀 때는 켜 둔 줄에 커서를 두고 **Ctrl+/**(macOS **⌘+/**)로 주석으로 만들고, 볼 줄에서 다시 **Ctrl+/** 로 주석을 푼다. 저장 → 새로고침한다. 한 번에 한 줄만 켠다.

**예상 결과** — `ex/`에 파일이 열한 개 있다(1일차 여섯 개 + 오늘 다섯 개). `ex/index.html`에서 이름 `student01`, 메시지 `안녕하세요`를 넣고 **남기기**를 누르면 두 칸이 비고 커서가 이름 칸에서 깜박인다. Console에 두 줄이 찍힌다.

```text
1. 비우기 전 : [student01] [안녕하세요]     ex04_reset_focus.js:12
2. 비운 뒤 : [] []                          ex04_reset_focus.js:17
```

- 줄을 둘 이상 켜면 둘째 파일이 `Uncaught SyntaxError: Identifier '…' has already been declared` 빨간 줄을 내고 실행되지 않는다. 두 파일이 같은 이름의 `const`를 만들기 때문이다. 한 줄만 켠다.
- 파일마다 무엇을 바꿔 볼지는 [2일차 실습](lab.md#2일차--빈값-안내와-다음-입력-그리고-조립-60분)에 있다.

### 7. 조립표

29분부터 조립한다. 이제 `ex/`가 아니라 `web-week07` 맨 위의 `guestbook.html`을 열고, 그 옆에 `guestbook.js`를 새로 만든다.
조립하는 줄은 모두 비교 예제와 6주차 완성본에서 본 것이다.

| 조립할 줄 | 출처 |
|---|---|
| `guestbook.html`의 `<script src="guestbook.js" defer></script>` | 6주차 완성본 `index.html`의 `<script src="app.js" defer></script>`, 파일 이름만 바꾼다 |
| `<form id="guestbook-form">` | [ex01](examples/day1/ex01_submit.html)·[ex02](examples/day1/ex02_value.html) 폼에 `id` 붙이기 |
| `#notice` 자리·`<h3>마지막으로 남긴 글</h3>`·`#last` 카드 | [고르기 페이지](examples/day2/index.html)의 `#notice`·`#last`, 6주차 `.card`·`<h3>` |
| `const form`·`nameInput`·`messageInput`·`notice`·`last` | [ex02](examples/day1/ex02_value.js)·[ex05](examples/day2/ex05_empty.js) 찾아서 `const`에 담기 |
| `function clearNotice() { notice.textContent = ''; }` | [ex07](examples/day2/ex07_pass_name.js) 안내를 지우는 함수(본문까지 같다) |
| `form.addEventListener('submit', function (event) { event.preventDefault(); …` | [ex01](examples/day1/ex01_submit.js) 2번 |
| `const name = nameInput.value.trim();`·`const message = messageInput.value.trim();` | [ex02](examples/day1/ex02_value.js) 2·3번 + [ex03](examples/day1/ex03_trim.js) 2번 |
| `if (name === '') { … nameInput.focus(); return; }`·`if (message === '') { … messageInput.focus(); return; }` | [ex05](examples/day2/ex05_empty.js) 1·2번 + [ex04](examples/day2/ex04_reset_focus.js) `focus()` |
| `clearNotice();`·`` last.textContent = `${name}: ${message}`; `` | [ex07](examples/day2/ex07_pass_name.js) 1번 괄호를 붙여 부르기 · [ex05](examples/day2/ex05_empty.js) 3번 |
| `form.reset();`·`nameInput.focus();` | [ex04](examples/day2/ex04_reset_focus.js) |
| `nameInput.addEventListener('input', clearNotice);`·`messageInput.addEventListener('input', clearNotice);` | [ex06](examples/day2/ex06_input.js) `'input'` 이벤트 + [ex07](examples/day2/ex07_pass_name.js) 2번 이름만 맡기기 |

옮겨 적을 때 출처 ex 파일을 옆에 열어 두고, 같은 줄이 거기서 무엇을 했는지 떠올린다.

### 8. guestbook.html 네 곳 고치기

`web-week07/guestbook.html`을 연다. 3주차에 만든 폼은 그대로 두고 **찾을 이름과 결과 자리만** 만든다.

1. `<head>`의 `<link rel="stylesheet" href="styles.css">` **바로 아래**에 한 줄을 넣는다.

```html
    <script src="guestbook.js" defer></script>
```

2. `<form>`을 `<form id="guestbook-form">`으로 바꾼다.
3. `</form>` 아래의 `<p>지금은 눌러도 주소창만 바뀐다. 화면에 띄우는 일은 7주에 한다.</p>` 한 줄을 지운다.
4. 지운 자리에 세 줄을 넣는다.

```html
      <div id="notice"></div>
      <h3>마지막으로 남긴 글</h3>
      <div class="card" id="last">아직 남긴 글이 없습니다.</div>
```

- `defer`는 HTML을 끝까지 읽은 뒤 `guestbook.js`를 실행하라는 뜻이다(5주차 ex02). 빠뜨리면 폼을 찾지 못한다.
- `index.html`은 `app.js`를, `guestbook.html`은 `guestbook.js`를 부른다. **페이지마다 자기 js 하나**다.
- `id`는 `guestbook-form`·`notice`·`last` 세 개를 새로 붙인다. 이름·메시지 칸의 `id`(`name`·`message`)는 3주차에 붙여 둔 것을 그대로 쓴다.
- `<div id="notice"></div>`는 **비어 있는 자리**다. 안내할 일이 있을 때만 글자가 들어간다.

**예상 결과** — 저장하고 Console에서 오른쪽 클릭 › **Clear console**로 지운 뒤 `guestbook.html`을 새로고침하면 폼 아래에 **마지막으로 남긴 글** 제목과 `아직 남긴 글이 없습니다.` 카드가 보인다. Console에는 `guestbook.js`를 불러오지 못했다는 빨간 줄이 하나 있다(`guestbook.js`와 `net::ERR_FILE_NOT_FOUND`가 들어 있는 줄). 아직 파일을 만들지 않아서다. 9단계에서 파일을 만들면 이 줄은 더 나지 않는다.

### 9. guestbook.js 새로 만들기

VS Code 탐색기에서 `web-week07` 맨 위(`guestbook.html` 옆)에 **New File**로 `guestbook.js`를 만든다. 조립표 순서로 쓴다.

1. 찾아 두기 다섯 줄 — `#guestbook-form`·`#name`·`#message`·`#notice`·`#last`를 `querySelector`로 찾아 `const`에 담는다(ex02·ex05).
2. 함수 `clearNotice` — 안내 자리를 비운다(ex07).
3. 제출 리스너 — 폼의 `'submit'`에 맡기고 첫 줄에서 `event.preventDefault();`(ex01 2번).
4. 값 두 개 — 이름·메시지를 리스너 **안**에서 `.value.trim()`으로 읽는다(ex02·ex03).
5. 이름 검사 — 비었으면 `이름을 입력하세요.`, 커서를 이름 칸으로, `return`(ex05 1번·ex04).
6. 메시지 검사 — 비었으면 `메시지를 입력하세요.`, 커서를 메시지 칸으로, `return`(ex05 2번·ex04).
7. 다 찼을 때 — 안내 지우기(`clearNotice();`, ex07 1번), 결과 한 줄 쓰기, 칸 비우기, 커서를 이름 칸으로(ex05 3번·ex04).
8. 맨 끝 두 줄 — 두 칸의 `'input'`(ex06)에 `clearNotice`를 이름만 맡긴다(ex07 2번).

**예상 결과** — 저장하고 Console을 다시 **Clear console**로 지운 뒤 `guestbook.html`을 새로고침한다. 빨간 줄이 새로 나지 않는다(Preserve log를 켜 두었으므로 지우지 않으면 8단계의 줄이 그대로 남아 있다). 이름 `student01`, 메시지 `안녕하세요`로 **남기기**를 누르면 주소가 그대로이고, 카드가 `student01: 안녕하세요`로 바뀌고, 세 칸이 비고, 커서가 이름 칸에 있다.
이름을 비우고 누르면 폼 아래에 `이름을 입력하세요.`가 나타나고 커서가 이름 칸으로 간다. 이름 칸에 한 글자를 치면 안내가 사라진다.

### 10. guestbook.html 전문

8단계까지 마친 `guestbook.html` 전체다. 내 파일과 한 줄씩 비교한다. 6주차 파일과 다른 곳은 8단계의 네 곳뿐이다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
    <link rel="stylesheet" href="styles.css">
    <script src="guestbook.js" defer></script>
  </head>
  <body>
    <header>
      <h1>방명록</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <h2>한 줄 남기기</h2>
      <h3>쓰는 순서</h3>
      <ol>
        <li>이름을 적는다.</li>
        <li>메시지를 적는다.</li>
        <li>남기기 버튼을 누른다.</li>
      </ol>
      <form id="guestbook-form">
        <p>
          <label for="name">이름</label>
          <input id="name" type="text">
        </p>
        <p>
          <label for="email">이메일</label>
          <input id="email" type="email">
        </p>
        <p>
          <label for="message">메시지</label>
          <textarea id="message" rows="4"></textarea>
        </p>
        <button type="submit">남기기</button>
      </form>
      <div id="notice"></div>
      <h3>마지막으로 남긴 글</h3>
      <div class="card" id="last">아직 남긴 글이 없습니다.</div>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

같은 파일이 [examples/day2/web-week07/guestbook.html](examples/day2/web-week07/guestbook.html)에 있다.

### 11. guestbook.js 전문

새로 만든 파일 전체다. 글자 단위로 같아야 한다.

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const last = document.querySelector('#last');

function clearNotice() {
  notice.textContent = '';
}

form.addEventListener('submit', function (event) {
  event.preventDefault();

  const name = nameInput.value.trim();
  const message = messageInput.value.trim();

  if (name === '') {
    notice.textContent = '이름을 입력하세요.';
    nameInput.focus();
    return;
  }

  if (message === '') {
    notice.textContent = '메시지를 입력하세요.';
    messageInput.focus();
    return;
  }

  clearNotice();
  last.textContent = `${name}: ${message}`;
  form.reset();
  nameInput.focus();
});

nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
```

같은 파일이 [examples/day2/web-week07/guestbook.js](examples/day2/web-week07/guestbook.js)에 있다.

- 1~5행은 찾은 요소를 `const`에 담아 둔다. 리스너 안과 맨 끝에서 이름으로 쓴다.
- 7~9행 `clearNotice`는 안내를 지우는 일이다(ex07). 29행(다 찼을 때)과 35~36행(다시 칠 때) 세 곳에서 쓴다. 고칠 일이 생기면 여기 한 곳만 고친다(6주차 ex06).
- 12행 `event.preventDefault();`가 리스너 첫 줄이다. 이 줄이 없으면 아래가 다 맞아도 페이지가 다시 열린다(ex01).
- 14~15행은 리스너 **안**에서 읽는다. 누를 때마다 그때의 글자를 읽는다(ex02 2번).
- 17~27행은 위에서부터 차례로 본다. 이름이 비면 20행 `return`에서 끝나 메시지 검사까지 가지 않는다(ex05).
- 29~32행은 두 칸이 다 찼을 때만 온다. 30행에서 결과를 쓴 **뒤** 31행에서 비운다. 이름과 메시지는 14~15행에서 이미 읽어 두었다(ex04).
- 35~36행은 함수 이름만 맡긴다. `clearNotice()`처럼 괄호를 붙이면 맡기는 순간 한 번 실행되고 끝난다(ex07).
- `index.html`·`about.html`·`app.js`·`styles.css`·`images/profile.png`는 6주차 완성본과 글자 하나까지 같다.

### 12. 375·1280 폭과 서버로 확인

DevTools의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)를 켜고 폭을 375와 1280으로 바꿔 가며 `guestbook.html`에서 글을 남겨 본다.

**예상 결과** — 두 폭 모두 폼과 카드가 화면 안에 들어오고 결과 줄이 같게 나온다. 375에서는 메뉴가 세로로 선다(4주차 `@media`). 입력 칸(폭 280px)은 375 폭 안에 그대로 들어간다. 4주차 `max-width: 100%`는 칸이 담긴 상자보다 넓어지지 않게 막는 규칙이라, 375에서는 칸을 줄이지 않는다.

이어서 서버로 연다. 현재 폴더: `web-week07`

```bash
node server.mjs
```

주소창에 `http://localhost:8000/guestbook.html`을 친다. 두 번 눌러 연 것과 결과가 같으면 된 것이다. 터미널에는 브라우저가 받아 간 파일마다 한 줄씩 찍힌다(`guestbook.html`·`guestbook.js`·`styles.css`). **남기기**를 눌러도 새 줄이 생기지 않는다. 페이지를 다시 열지 않았기 때문이다. `404 GET /favicon.ico` 줄도 보일 수 있는데 괜찮다([서버 사용 안내](../../tools/static-server/README.md#터미널에-찍히는-줄-읽기) 참고). 그때 Console에도 `favicon.ico`를 받지 못했다는 빨간 줄(404)이 하나 보일 수 있다. 브라우저가 탭 아이콘을 찾은 것이라 내 코드와 관계없다. 확인이 끝나면 터미널에서 **Ctrl+C**로 서버를 멈춘다.
쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다. Node가 없는 PC는 `guestbook.html`을 두 번 눌러 연 것으로 대신한다.

### 13. push와 캡처

현재 폴더: `web-week07`

```bash
git add .
git commit -m "7주차 2일차"
git push
```

1~3분 뒤 `https://student01.github.io/web-week07/guestbook.html`을 연다. 이름 `student01`, 메시지 `안녕하세요`를 넣고 **남기기**를 누른다.

**예상 결과** — 주소는 그대로이고, **마지막으로 남긴 글** 아래 카드에 `student01: 안녕하세요`가 보인다. 주소창이 함께 보이게 캡처한다. 이 캡처 한 장이 제출이다.
공용 PC라면 자격 증명을 지우고 나간다.

- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 이메일 칸은 비워 둔다. 캡처에 실제 이메일이 보이지 않게 한다.
- 막히면 [실습지의 막혔을 때](lab.md#막혔을-때)를 본다.
