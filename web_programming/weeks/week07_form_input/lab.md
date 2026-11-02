[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_form_input)

# 7주차 실습 — 방명록 폼이 남긴 글을 보여 주게 만들기

## 이번 주에 만드는 것

3주차에 만든 `guestbook.html` 폼은 아직 아무 일도 하지 않는다. 이름·메시지를 넣고 **남기기**를 누르면 주소창 끝에 `?` 가 붙고 칸이 빈 채로 처음 화면이 다시 열린다.
이번 주가 끝나면 같은 폼이 이렇게 동작한다.

```text
이름 [student01]   메시지 [안녕하세요]   [남기기]
                     │ 누를 때마다
                     ▼
남긴 글
┌─────────────────────────┐
│ • student01: 안녕하세요  │   ← 주소창은 그대로, 두 칸은 비고, 커서는 이름 칸
│ • student02: 반갑습니다  │   ← 한 번 더 남기면 아래에 한 줄이 더 붙는다
└─────────────────────────┘

이름을 비우고 누르면 → "이름을 입력하세요." 가 보이고 커서가 이름 칸으로 간다
이름 칸에 다시 치면   → 안내가 사라진다
```

이렇게 만들려면 아래 일곱 가지를 알아야 한다. 비교 예제 하나가 하나씩 보여 주고, 2일차 끝에 그 줄들을 모아 `guestbook.js` 를 만든다.

| 알아야 할 것 | 보는 예제 | 완성본 `guestbook.js` 에서 쓰는 줄 |
|---|---|---|
| 폼을 보내면 페이지가 다시 열린다. 그래서 막는다 | 1일차 ex01 | `event.preventDefault();` |
| 칸에 적힌 글자는 누를 **때** 읽는다 | 1일차 ex02 | `nameInput.value` |
| 앞뒤 빈칸을 떼야 빈칸만 친 칸도 빈 칸이 된다 | 1일차 ex03 | `.trim()` |
| 다 쓴 뒤 칸을 비우고 커서를 옮긴다 | 2일차 ex04 | `form.reset();` · `nameInput.focus();` |
| 칸이 비었으면 안내하고 거기서 멈춘다 | 2일차 ex05 | `if (name === '') { …; return; }` |
| 다시 치면 안내를 지운다 | 2일차 ex06·ex07 | `nameInput.addEventListener('input', clearNotice);` |
| 남길 때마다 목록에 줄을 새로 만들어 붙인다 | 2일차 ex08 | `document.createElement('li')` · `list.append(li);` |

예제에서 할 일은 **줄 하나를 바꿔 보고 화면이 어떻게 달라지는지 보는 것**이다. 무엇이 달라질지 먼저 말해 보고, 저장 → 새로고침으로 확인하고, 확인했으면 원래대로 되돌린다.
결과는 화면, **주소창**, **F12 › Console** 에서 본다. 이번 주에는 Console 위쪽 ⚙(**Console settings**) › **Preserve log** 를 켜 둔다. 페이지가 다시 열려도 Console 줄이 지워지지 않는다(켜는 법은 [따라하기 1일차](walkthrough.md#1일차)).
채점 대상은 2일차 캡처 1장이다. `student01` 은 예시 아이디이므로 본인 아이디로 바꾼다.

## 1일차 — 폼 제출과 입력 값 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 새 폴더 `web-week07` 을 만들어 VS Code 로 연다(**File › Open Folder**). 지난주 완성본을 넣는다: 내 `web-week06` 저장소 GitHub 화면 › **Code › Download ZIP** → 압축을 풀어 맨 위 파일과 `images/` 를 넣는다. 못 받으면 교재 [6주차 `examples/day2/web-week06/`](../week06_dom_events/examples/day2/web-week06/) 파일을 **Raw** 로 받는다. `ex` 폴더와 그 안에 `ex01`·`ex02`·`ex03` 폴더를 만든다. 예제 파일은 문항마다 교재 [`examples/day1/`](examples/day1/) 의 같은 이름 폴더에서 받는다 |
| 5–20분 | ex01 폼 제출과 preventDefault |
| 20–34분 | ex02 입력 칸의 value |
| 34–47분 | ex03 trim |
| 47–50분 | 확인: `ex/` 안에 예제 폴더 세 개가 있고 폴더마다 `index.html`·`app.js` 가 있는지, 각 예제에서 값 하나 이상을 바꿨는지. 일부러 낸 오류와 옮긴 줄은 되돌려 두었는지 |
| 50–60분 | 이번 주 저장소 만들어 올리기: GitHub 에 새 저장소 `web-week07` → [올리기 명령](#이번-주-저장소-만들어-올리기) → **Settings › Pages** → 공개 주소 `https://student01.github.io/web-week07/ex/ex01/` 확인 → 공용 PC면 자격 증명 삭제 |

예제는 폴더마다 따로 연다. 문항의 폴더에서 `index.html` 을 Chrome 으로 열고, 코드는 같은 폴더의 `app.js` 에서 고친 뒤 저장 → 새로고침으로 본다. 아래 문항의 `N행` 은 모두 그 폴더 `app.js` 의 줄 번호다("완성본 N행"만 `guestbook.js` 의 줄이다).
시작하기 전에 지난주 완성본의 `guestbook.html` 을 열어 이름·메시지를 넣고 **남기기**를 눌러 본다. 주소창 끝에 `?` 가 붙고 칸이 빈다. 이것이 이번 주에 고칠 문제다.

### 1. ex01 폼 제출과 preventDefault (`submit` · `event.preventDefault()`)

**이 예제로 알 것:** 폼을 보내면 브라우저는 페이지를 다시 연다. 그래서 내 코드가 바꾼 화면이 남지 않는다. `submit` 을 듣고 첫 줄에서 `event.preventDefault()` 로 막는다. → 완성본 11·12행.

교재 [index.html](examples/day1/ex01/index.html) · [app.js](examples/day1/ex01/app.js) 를 **Raw** 로 받아 `ex/ex01/` 에 저장하고(따라하기 2단계에서 받았으면 건너뛴다) `ex/ex01/index.html` 을 연다. 고치는 파일은 `ex/ex01/app.js` 다. 폼이 두 개 있다. 1번은 막지 않고, 2번은 막는다.

- 바꿔 보기: 2번 칸에 글자를 넣고 **2. 보내기**를 누른다. 주소창과 2번 칸의 글자는 그대로인가? 이어서 1번 칸에 글자를 넣고 **1. 보내기**를 누른다. 주소창 끝에 무엇이 붙었나? 두 칸의 글자와 2번 결과 자리는 왜 처음으로 돌아갔나?
- 바꿔 보기: 2번 칸에서 버튼 대신 **Enter** 를 친다. 버튼을 누른 것과 같은가? (그래서 버튼의 `click` 이 아니라 폼의 `submit` 을 듣는다.)
- 바꿔 보기: `app.js` 17행 `event.preventDefault();` 앞에 `//` 를 붙이고 2번을 보낸다. 2번도 1번처럼 되나? 확인했으면 되돌린다.
- 흔한 실수: `event.preventDefault()` 를 `preventDefault()` 로 쓴다(`event.` 빠짐). 빨간 줄이 나고 막지 못해 페이지가 다시 열린다. Preserve log 를 켜야 그 빨간 줄이 남아 보인다.

### 2. ex02 입력 칸의 value (`input.value` · `textarea.value`)

**이 예제로 알 것:** 칸에 적힌 글자는 `value` 다. 누를 **때** 읽어야 그때 적힌 글자가 나온다. 페이지를 열 때 읽으면 빈 글자다. → 완성본 14·15행(리스너 안).

교재 [index.html](examples/day1/ex02/index.html) · [app.js](examples/day1/ex02/app.js) 를 **Raw** 로 받아 `ex/ex02/` 에 저장하고(따라하기 2단계에서 받았으면 건너뛴다) `ex/ex02/index.html` 을 연다. 고치는 파일은 `ex/ex02/app.js` 다.

- 바꿔 보기: 이름 `student01`, 메시지 `안녕하세요` 를 넣고 **남기기**를 누른다. 1·2·3번 자리에 무엇이 나오나? 1번은 왜 비어 있나?
- 바꿔 보기: 이름을 `student02` 로 바꿔 다시 누른다. 1번과 2번 중 무엇이 바뀌나? 11행과 15행은 같은 `nameInput.value` 인데 왜 결과가 다른가? (6주차 ex02 의 "열 때"와 "클릭할 때"와 같다.)
- 흔한 실수: 값을 읽는 줄을 리스너 밖(파일 위쪽)에 둔다. 1번처럼 열 때 한 번만 읽으므로 언제 눌러도 그때의 빈 글자다.

### 3. ex03 trim (`trim()`)

**이 예제로 알 것:** `trim()` 은 앞뒤 빈칸(스페이스)을 뗀 값을 준다. 빈칸만 친 칸은 빈 글자가 된다. 그래서 다음 날 빈 칸 검사에 쓴다. → 완성본 14·15행의 `.trim()`.

교재 [index.html](examples/day1/ex03/index.html) · [app.js](examples/day1/ex03/app.js) 를 **Raw** 로 받아 `ex/ex03/` 에 저장하고(따라하기 2단계에서 받았으면 건너뛴다) `ex/ex03/index.html` 을 연다. 고치는 파일은 `ex/ex03/app.js` 다.

- 바꿔 보기: 이름 칸에 스페이스 두 번, `student01`, 스페이스 두 번을 넣고 누른다. Console 1·2번의 `[ ]` 안은 어떻게 다른가?
- 바꿔 보기: 스페이스만 세 번 넣고 누른다. 2번은 무엇인가? 빈칸만 친 칸을 "비었다"고 보려면 1·2번 중 어느 값을 써야 하나?
- 흔한 실수: `trim` 뒤의 괄호를 빠뜨린다(`.trim;`). 빨간 줄은 없지만 2번 `[ ]` 안에 이름이 아니라 함수의 글자(`function trim() …`)가 들어간다. 6주차 ex06 처럼 **부를 때는 괄호**다.

### 이번 주 저장소 만들어 올리기

GitHub 에서 **New repository** → 이름 `web-week07`, **Public**, README 는 추가하지 않는다. VS Code 터미널(현재 폴더 `web-week07`)에서 2주차에 배운 순서 그대로 친다.

```bash
git init
git add .
git commit -m "7주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week07.git
git push -u origin main
```

저장소 **Settings › Pages › Branch: main, /(root) › Save** → 1~3분 뒤 `https://student01.github.io/web-week07/ex/ex01/` 를 연다. `ex/ex01/index.html` 의 두 폼이 보이고 **2. 보내기**가 주소를 바꾸지 않으면 된 것이다. 공용 PC면 자격 증명을 지우고 나간다.
오늘 올린 것은 확인용이다. 제출은 2일차에 캡처 한 장만 한다.

## 2일차 — 빈값 안내와 다음 입력, 그리고 조립 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC에 `web-week07` 폴더가 남아 있으면 그대로 연다. 없으면 `git clone https://github.com/student01/web-week07.git` 뒤 **File › Open Folder**. `ex/` 안에 `ex04`~`ex08` 폴더 다섯 개를 만든다. 예제 파일은 문항마다 교재 [`examples/day2/`](examples/day2/) 의 같은 이름 폴더에서 받는다 |
| 5–10분 | ex04 reset 과 focus |
| 10–15분 | ex05 빈값 검사와 return |
| 15–19분 | ex06 input 이벤트 |
| 19–23분 | ex07 함수 이름만 맡기기 |
| 23–29분 | ex08 바꾸기 vs 붙이기 |
| 29–48분 | 조립: `guestbook.html` 네 곳 고치기, `guestbook.js` 를 조립표 순서로 새로 쓰기 |
| 48–55분 | 확인: 375·1280 폭, `node server.mjs` → `http://localhost:8000/guestbook.html`. Node 가 없으면 `guestbook.html` 을 두 번 눌러 연다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit -m "7주차 2일차"` → `git push` → 공개 주소 `https://student01.github.io/web-week07/guestbook.html` 에서 글 두 개를 남겨 목록에 두 줄이 보이는 **캡처 1장** → 공용 PC면 자격 증명 삭제 |

2일차 예제도 폴더마다 따로 연다. `ex/ex04/index.html` 처럼 문항의 폴더에서 `index.html` 을 열고, 같은 폴더의 `app.js` 를 고친 뒤 저장 → 새로고침으로 본다. `N행` 은 그 폴더 `app.js` 의 줄 번호다. 화면에는 그 예제가 쓰는 칸과 자리만 있다(ex04 폼, ex05 폼·안내 자리·결과 자리, ex06·ex07 두 칸과 안내 자리, ex08 글 칸·버튼 둘·1번 자리·목록).
파일마다 **바꿔 보기를 하나 이상** 하고 넘어간다. 29분이 되면 남은 것은 두고 조립을 시작한다. 남은 바꿔 보기는 캡처까지 끝낸 뒤 한다.

### 4. ex04 reset 과 focus (`form.reset()` · `focus()`)

**이 예제로 알 것:** `form.reset()` 은 폼의 칸을 모두 비우고, `focus()` 는 커서를 그 칸으로 옮긴다. 값은 비우기 **전에** 읽는다. → 완성본 33·34행.

교재 [index.html](examples/day2/ex04/index.html) · [app.js](examples/day2/ex04/app.js) 를 **Raw** 로 받아 `ex/ex04/` 에 저장하고(따라하기 6단계에서 받았으면 건너뛴다) `ex/ex04/index.html` 을 연다. 고치는 파일은 `ex/ex04/app.js` 다.

- 바꿔 보기: 두 칸을 채우고 **남기기**를 누른다. Console 1·2번의 `[ ]` 안은? 두 칸은 어떻게 됐나? 커서는 어느 칸에서 깜박이나(3번)?
- 바꿔 보기: 14행 `form.reset();` 을 잘라 2번 `console.log` 줄(`2. 비운 뒤 …` 를 찍는 줄) 바로 아래에 붙인다. 2번은 어떻게 바뀌나? 읽는 일과 비우는 일 중 무엇을 먼저 해야 하나? 확인했으면 되돌린다.
- 흔한 실수: `form.reset()` 을 값을 읽기 **전**에 둔다. 읽을 때 칸이 이미 비어 빈 글자를 읽는다. 읽고 → 쓰고 → 비운다.

### 5. ex05 빈값 검사와 return (`if` · `=== ''` · `return`)

**이 예제로 알 것:** 칸이 비었으면 안내를 쓰고 `return` 으로 그 자리에서 멈춘다. 검사는 위에서부터 차례로 한다. → 완성본 17~27행.

교재 [index.html](examples/day2/ex05/index.html) · [app.js](examples/day2/ex05/app.js) 를 **Raw** 로 받아 `ex/ex05/` 에 저장하고 `ex/ex05/index.html` 을 연다. 고치는 파일은 `ex/ex05/app.js` 다. 이 예제는 칸을 비우지 않으므로 칸은 직접 지우며 해 본다.

- 바꿔 보기: 이름만 비우고, 메시지만 비우고, 둘 다 비우고, 둘 다 채워서 각각 누른다. 안내 자리와 결과 자리는 어떻게 되나? 둘 다 비었을 때 어느 안내가 나오나? 왜 그런가?
- 바꿔 보기: 19행 `return;` 앞에 `//` 를 붙인다. 이름은 비우고 메시지는 `안녕하세요` 로 누른다. 결과 자리는? 1번이 쓴 안내는 왜 사라졌나? 확인했으면 되돌린다.
- 바꿔 보기: 메시지 칸은 `안녕하세요` 로 채운 채 이름 칸에 스페이스만 넣고 누른다. 1번 안내가 나오나? 12행의 `.trim()` 을 지우고 같은 값으로 다시 누르면? 확인했으면 되돌린다.
- 흔한 실수: `return` 을 빠뜨린다. 안내를 쓴 뒤에도 아랫줄이 실행되어 결과 자리에 `: 안녕하세요` 처럼 이름 없는 줄이 남는다.

### 6. ex06 input 이벤트 (`'input'`)

**이 예제로 알 것:** `'input'` 은 칸의 글자가 바뀔 때마다(칠 때도 지울 때도) 일어난다. 다시 입력하기 시작하면 안내를 지우는 데 쓴다. → 완성본 37·38행.

교재 [index.html](examples/day2/ex06/index.html) · [app.js](examples/day2/ex06/app.js) 를 **Raw** 로 받아 `ex/ex06/` 에 저장하고 `ex/ex06/index.html` 을 연다. 고치는 파일은 `ex/ex06/app.js` 다. 폼을 보내지 않는 예제라 칸 두 개와 안내 자리만 있다.

- 바꿔 보기: 열자마자 안내 자리에 무엇이 보이나? 이름 칸에 `abc` 를 한 글자씩 친다. Console 1번은 몇 줄인가? 안내는 언제 사라지나?
- 바꿔 보기: 새로고침하고 메시지 칸에 친다. 2번이 찍히나? 한 줄 칸(`input`)과 여러 줄 칸(`textarea`)에서 같은 `'input'` 이 일어나나?
- 흔한 실수: 이벤트 이름의 철자를 틀린다(`'inptu'`). 빨간 줄도 없이 아무 일도 일어나지 않는다. 이벤트 이름은 따옴표 안에 소문자 그대로 쓴다.

### 7. ex07 함수 이름만 맡기기 (`addEventListener('input', clearNotice)`)

**이 예제로 알 것:** 미리 만든 함수를 리스너로 맡길 때는 이름만 쓴다. 괄호는 부를 때만 붙인다. → 완성본 7~9행(`clearNotice`)과 37·38행.

교재 [index.html](examples/day2/ex07/index.html) · [app.js](examples/day2/ex07/app.js) 를 **Raw** 로 받아 `ex/ex07/` 에 저장하고 `ex/ex07/index.html` 을 연다. 고치는 파일은 `ex/ex07/app.js` 다. 이 예제는 Console 에 찍지 않는다. 안내 자리를 본다.

- 바꿔 보기: 열자마자 안내가 보인다. 이름 칸에 한 글자를 치면 안내는? 새로고침하고 이번에는 메시지 칸에 한 글자를 친다. 1번과 2번은 맡기는 모양이 다른데 하는 일은 같은가?
- 바꿔 보기: 18행 `clearNotice` 를 `clearNotice()` 로(괄호를 붙여) 바꾸고 새로고침한다. 메시지 칸에 쳐도 안내가 사라지나? 빨간 줄은? 확인했으면 되돌린다.
- 흔한 실수: 함수를 맡길 때 괄호를 붙인다(`clearNotice()`). 그 줄이 실행될 때 한 번 불리고 끝나서, 칠 때는 아무 일이 없고 빨간 줄도 없다. **맡길 때는 이름만, 부를 때는 괄호**다(6주차 ex06 의 `countUp();`).

### 8. ex08 바꾸기 vs 붙이기 (`createElement` · `textContent` · `append`)

**이 예제로 알 것:** 같은 자리의 `textContent` 를 바꾸면 늘 마지막 한 줄만 남는다. 쌓으려면 누를 때마다 `document.createElement('li')` 로 줄을 **새로 만들고**, `textContent` 로 글자를 넣고, `append` 로 목록 맨 뒤에 **붙인다**. → 완성본 30~32행.

교재 [index.html](examples/day2/ex08/index.html) · [app.js](examples/day2/ex08/app.js) 를 **Raw** 로 받아 `ex/ex08/` 에 저장하고 `ex/ex08/index.html` 을 연다. 고치는 파일은 `ex/ex08/app.js` 다. 글 칸에는 `student01: 안녕하세요` 가 미리 들어 있다.

- 바꿔 보기: **1. 바꾸기**와 **2. 붙이기**를 한 번씩 누른다. 글 칸을 `student02: 반갑습니다` 로 바꿔 다시 한 번씩 누른다. 1번 자리와 목록은 각각 몇 줄인가? **F12 › Elements** 에서 `<ul id="list">` 를 펼치면 `<li>` 가 몇 개인가?
- 바꿔 보기: 20행 `list.append(li);` 앞에 `//` 를 붙이고 2번을 두 번 누른다. 목록은 어떻게 되나? Console 2번은 찍히나? 빨간 줄은? 확인했으면 되돌린다.
- 바꿔 보기: 18행 `const li = document.createElement('li');` 를 잘라 8행(`const list = …`) 바로 아래에 붙인다. 글을 바꿔 가며 2번을 세 번 누른다. 목록은 몇 줄인가? 왜 그런가? 확인했으면 되돌린다.
- 흔한 실수: 결과 자리 하나의 `textContent` 에 쓴다(1번). 두 번째 글이 첫 글을 덮어 늘 한 줄이다. 쌓으려면 누를 때마다 줄을 **새로 만들어 붙인다**. 3주차에 `<ul>` 안에 손으로 적던 `<li>` 를 JavaScript 가 만드는 것이다.

### 9. 조립 — `guestbook.html` 네 곳, `guestbook.js` 새로 쓰기 (`submit` · `value` · `trim` · `return` · `reset` · `input` · `append`)

이제 `ex/` 가 아니라 `web-week07` 맨 위의 `guestbook.html` 을 연다.
`guestbook.js` 는 세 덩어리다. ① 쓸 요소를 찾아 둔다 ② **남기기**를 누르면 막고 → 읽고 → 비었는지 검사하고 → 목록에 한 줄을 만들어 붙이고 → 칸을 비운다 ③ 다시 치면 안내를 지운다. 아래 조립표의 줄이 이 순서다.
`guestbook.js` 는 그 옆(맨 위)에 새로 만든다. `ex/ex04/` 같은 예제 폴더의 `index.html`·`app.js` 는 이름만 같은 예제 파일이라 조립에 쓰지 않는다. 전문과 단계는 [따라하기 2일차](walkthrough.md#2일차)에 있다.

- `guestbook.html`: `<link>` 줄 아래에 `<script src="guestbook.js" defer></script>` 를 넣고, `<form>` 에 `id="guestbook-form"` 을 붙인다. 3주차 문장 `<p>지금은 눌러도 주소창만 바뀐다. 화면에 띄우는 일은 7주에 한다.</p>` 를 지우고 그 자리에 안내 자리·제목·빈 목록 세 줄을 넣는다.
- `guestbook.js`: 아래 조립표 순서로 쓴다. `index.html`·`app.js`·`styles.css`·`about.html` 은 6주차 그대로 두고 열지 않는다.

| 조립할 줄 | 어느 ex 에서 본 것 |
|---|---|
| `guestbook.html` 의 `<script src="guestbook.js" defer></script>` | 6주차 완성본 `index.html` 의 `<script src="app.js" defer></script>`. 파일 이름만 바꾼다(페이지마다 자기 js 하나) |
| `<form id="guestbook-form">` | ex01·ex02 (폼에 `id` 를 붙여 찾는다) |
| `<div id="notice"></div>` · `<ul class="card" id="list"></ul>` | ex05 의 안내 자리 `#notice`, ex08 의 빈 목록 `<ul id="list">`, 6주차 `#count` 카드의 `.card` |
| `<h3>남긴 글</h3>` | 6주차 완성본 `guestbook.html` 의 `<h3>쓰는 순서</h3>` 와 같은 모양의 제목 |
| `const form = …('#guestbook-form');` · `nameInput` · `messageInput` · `notice` · `list` | ex02·ex05·ex08 (찾아서 `const` 에 담기) |
| `function clearNotice() { notice.textContent = ''; }` | ex07 (안내를 지우는 함수. 본문까지 같다) |
| `form.addEventListener('submit', function (event) { event.preventDefault(); …` | ex01 2번 |
| `const name = nameInput.value.trim();` · `const message = messageInput.value.trim();` | ex02 2·3번 (누를 때 읽기) + ex03 2번 (`trim()`) |
| `if (name === '') { notice.textContent = '이름을 입력하세요.'; nameInput.focus(); return; }` | ex05 1번 + ex04 (`focus()`) |
| `if (message === '') { notice.textContent = '메시지를 입력하세요.'; messageInput.focus(); return; }` | ex05 2번 + ex04 |
| `clearNotice();` | ex07 1번 (함수 안에서 괄호를 붙여 부르기) |
| `const li = document.createElement('li');` · `` li.textContent = `${name}: ${message}`; `` · `list.append(li);` | ex08 2번 (줄을 새로 만들고, 글자를 넣고, 목록 맨 뒤에 붙이기). 넣는 글자 `` `${name}: ${message}` `` 는 ex05 3번 |
| `form.reset();` · `nameInput.focus();` | ex04 |
| `nameInput.addEventListener('input', clearNotice);` · `messageInput.addEventListener('input', clearNotice);` | ex06 (`'input'` 이벤트) + ex07 2번 (이름만 맡기기). 한 함수를 여러 곳에서 쓰는 것은 6주차 ex06 |

- 확인: 저장하고 `guestbook.html` 을 새로고침한다. 이름 `student01`, 메시지 `안녕하세요` 로 **남기기**를 누르면 주소가 그대로이고, 목록에 `student01: 안녕하세요` 한 줄이 붙고, 칸이 비고, 커서가 이름 칸에 있다. 이어서 이름 `student02`, 메시지 `반갑습니다` 로 한 번 더 남기면 그 아래에 한 줄이 더 붙어 두 줄이 되면 된 것이다.
- 바꿔 보기: 이름을 비우고 누른 뒤 이름 칸에 한 글자를 친다. 안내는 언제 나타나고 언제 사라지나? 이번에는 메시지만 비우고 해 본다.
- 바꿔 보기: 글 두 개를 남긴 뒤 새로고침한다. 목록은 어떻게 되나? (목록은 화면에만 있다. 새로고침하면 파일을 다시 읽어 빈 목록으로 돌아간다. 새로고침해도 남게 하는 것은 11주차다.)
- 흔한 실수: `<script src="guestbook.js" defer>` 의 `defer` 를 빠뜨린다. 열자마자 `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')`(`guestbook.js:11`)가 뜨고 그 아래가 실행되지 않아, **남기기**를 누르면 페이지가 다시 열린다. 폼 `id` 철자가 틀려도 같은 문구다.

### 10. 375·1280 폭과 서버로 확인

- DevTools 의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)로 폭 375 와 1280 에서 `guestbook.html` 을 연다. 두 폭 모두 폼과 목록이 화면 안에 들어오고 **남기기**가 같게 동작하면 된 것이다.
- 1일차에 넣어 둔 `server.mjs` 가 없으면 [server.mjs](../../tools/static-server/server.mjs) 를 **Raw** 로 받아 `web-week07` 맨 위에 둔다. 터미널(현재 폴더 `web-week07`)에서 `node server.mjs` → `http://localhost:8000/guestbook.html` 을 연다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.
- 확인이 끝나면 터미널에서 **Ctrl+C** 로 서버를 멈추고 끝 루틴으로 간다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다 |
| push 가 거부되거나 로그인 창이 안 뜬다 | [2주차 막혔을 때](../week02_github_pages/lab.md#막혔을-때) 표를 본다 |
| 화면이 생각과 다른데 이유를 모르겠다 | **Console 을 먼저 연다.** 빨간 줄 오른쪽 `파일:줄` 로 간다. 오류 난 줄 아래는 실행되지 않으므로 그 줄부터 본다 |
| **남기기**를 누르면 주소 끝에 `?` 가 붙고 칸이 빈다. Console 에 새 빨간 줄이 없다 | 페이지가 다시 열린 것이다(오류가 아니라 폼의 원래 동작). ① `guestbook.html` 에 `<script src="guestbook.js" defer></script>` 줄이 있는지 ② 리스너 첫 줄에 `event.preventDefault();` 가 있는지 ③ `event.` 를 빠뜨리지 않았는지 본다. Console ⚙ › **Preserve log** 를 켜고 다시 누르면 빨간 줄이 있었는지 보인다 |
| 열자마자 `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` (`guestbook.js:11`) | 폼을 못 찾았다. `'#guestbook-form'` 과 `<form id="guestbook-form">` 의 글자를 비교하고, `script` 줄에 `defer` 가 있는지 본다 |
| `Uncaught ReferenceError: preventDefault is not defined` | `event.` 를 빠뜨렸다. `event.preventDefault();` 로 쓴다(ex01 흔한 실수) |
| `Uncaught TypeError: Cannot read properties of undefined (reading 'trim')` (`guestbook.js:14`) | `.value` 철자가 틀렸다(`velue`). 없는 이름이라 `undefined` 이고, 그 뒤 `.trim()` 에서 멈췄다(ex02 와 같은 철자 실수) |
| `Uncaught TypeError: nameInput.value.trm is not a function` | `trim` 철자가 틀렸다(ex03 `trim` 철자) |
| `Uncaught TypeError: form.rest is not a function` | `reset` 철자가 틀렸다. 목록에는 이미 한 줄이 붙고 칸만 안 비워진다(ex04 `reset` 철자) |
| `Uncaught TypeError: Cannot read properties of null (reading 'append')` (`guestbook.js:32`) | 목록을 못 찾았다. `guestbook.html` 의 `<ul class="card" id="list">` 와 `querySelector('#list')` 의 글자를 비교한다. 이때 칸도 비워지지 않는다(33행까지 못 간다) |
| `Uncaught TypeError: Assignment to constant variable.` | `if (name === '')` 를 `if (name = '')` 로 썼다. 비교는 `=` 세 개다(ex05) |
| 이름을 비웠는데 목록에 `: 안녕하세요` 줄이 붙는다 | 이름 검사 안의 `return;` 이 없다(ex05 둘째 바꿔 보기) |
| 이름 칸에 스페이스만 넣었는데 통과한다 | `.trim()` 이 빠졌다. `nameInput.value.trim()` 으로 읽는다(ex03) |
| 채워서 눌러도 늘 `이름을 입력하세요.` 가 나온다 | `const name = …` 줄이 리스너 **밖**에 있거나(ex02 1번), `form.reset();` 이 값을 읽는 줄보다 **위**에 있다(ex04) |
| 안내 문구가 다시 쳐도 사라지지 않는다 | 맨 끝 두 줄의 `'input'` 철자를 보고(ex06 흔한 실수), `clearNotice` 에 괄호를 붙이지 않았는지 본다(ex07 둘째 바꿔 보기) |
| **남기기**를 누르면 이메일 칸 옆에 메일 주소를 고치라는 말풍선이 뜨고(문구는 친 글자에 따라 다르다), 커서가 이메일 칸에 남고, 결과·안내는 그대로다. Console 에 새 줄도 없다 | 이메일 칸에 메일 주소 모양이 아닌 글자가 있다. `type="email"` 칸이라 브라우저가 보내기 전에 막았다(제출 리스너까지 가지 않는다). 이메일 칸은 비워 두거나 `student01@example.com` 모양으로 쓴다 |
| 남겼는데 목록에 아무것도 없다. 칸은 비고 빨간 줄도 없다 | `list.append(li);` 가 빠졌다. 만든 줄은 붙여야 보인다(ex08 둘째 바꿔 보기) |
| 남길 때마다 목록이 늘 한 줄이고 글자만 바뀐다 | `const li = document.createElement('li');` 가 리스너 밖(맨 위 찾아 두기 줄 옆)에 있다. 줄은 누를 때마다 리스너 안에서 새로 만든다(ex08 셋째 바꿔 보기) |
| 예제를 열었는데 아무 일도 없다. ex01·ex02·ex03·ex04·ex05 는 보내면 주소 끝에 `?` 가 붙고 Console 에 번호 줄이 없다. ex06·ex07 은 안내 문구가 나오지 않는다. ex08 은 눌러도 그대로다 | `app.js` 가 그 `index.html` 과 같은 폴더(`ex/ex04/` 등)에 있는지 본다. Console 에 `Failed to load resource` 줄이 있으면 그 폴더에 `app.js` 가 없거나 파일 이름 철자가 틀린 것이다(Preserve log 를 켜 두어야 다시 열린 뒤에도 보인다) |
| 두 번째 글을 남기면 앞 글이 사라진다 | 결과 자리 하나의 `textContent` 를 바꾸고 있다. 줄(`li`)을 새로 만들어 `list.append(li)` 로 붙인다(ex08 1번과 2번의 차이) |
| 새로고침하면 남긴 글이 사라진다 | 정상이다. 새로고침하면 파일을 다시 읽어 화면을 새로 만든다. 남기는 법은 11주차에 배운다 |
| 공개 주소 `…/web-week07/ex/ex01/` 가 404 다 | ① 주소가 `ex/` 에서 끝나지 않고 `ex/ex01/` 까지 있는지 본다(`ex/` 바로 아래에는 `index.html` 이 없어서 `…/ex/` 만 열면 늘 404 다. `ex/` 에 `index.html` 을 만들거나 옮기지 않는다) ② 폴더 이름이 `ex`·`ex01` 이고 `ex01` 안에 `index.html` 이 있는지 ③ 저장소 이름이 `web-week07` 이고 **Settings › Pages** 가 켜져 있는지 본다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://student01.github.io/web-week07/guestbook.html` (본인 아이디) 을 열고 이름과 메시지를 바꿔 가며 **남기기**를 두 번 누른 화면을 캡처한다.

- **남긴 글** 아래 목록에 `이름: 메시지` 줄이 **두 줄 이상** 보인다(예: `student01: 안녕하세요`, `student02: 반갑습니다`).
- **주소창이 함께 보이게** 찍는다.
- 빈값 안내(`이름을 입력하세요.`)는 실습 중에 확인하는 것이고 캡처에는 없어도 된다.

1일차 push 와 `ex/` 실험 파일은 확인용이며 따로 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다(이메일 칸은 비워 둔다). 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 이메일 칸도 검사한다: 비어 있으면 `이메일을 입력하세요.` 를 쓰고 커서를 이메일 칸으로 옮긴다. ex05 2번과 같은 모양의 `if` 를 메시지 검사 아래에 하나 더 둔다. 이메일 칸을 찾아 두는 줄과 읽는 줄은 어디에 더하나? 다시 치면 안내가 사라지게 하려면 맨 끝에 무엇을 한 줄 더하나?
- 안내 문구 색: `styles.css` 맨 아래에 `#notice { color: #b3261e; }` 규칙을 더한다(4주차 `#` 선택자). JavaScript 는 고치지 않는다.
- 남긴 글 수 세기: 목록 아래에 `<div id="total">남긴 글 0개</div>` 를 두고, 글을 남길 때마다 `남긴 글 N개` 로 바꾼다. 횟수 변수는 함수 안과 밖 중 어디에 두나(6주차 ex03)? 두 칸이 비어 막혔을 때는 늘지 않아야 한다.
- 서버로 ex01 열기: 터미널(현재 폴더 `web-week07`)에서 `node server.mjs` → `http://localhost:8000/ex/ex01/` 을 연다. 열 때 터미널에 어떤 줄들이 찍히나? 1번을 보낼 때는 어떤 줄들이 더 찍히나? 2번을 보낼 때는? "페이지를 다시 연다"는 것이 서버 쪽에서는 어떻게 보이나(1주차 요청과 응답)? 줄 읽는 법은 [서버 사용 안내](../../tools/static-server/README.md#터미널에-찍히는-줄-읽기)에 있다. 확인이 끝나면 **Ctrl+C**.
- 8주차 문제 은행의 [w07_form_line](../week08_midterm/examples/w07_form_line/README.md) 을 풀어 본다. 이번 주와 같은 일을 다른 값으로 한다. 해답은 공개하지 않는다. 문제의 "확인할 것"이 모두 맞으면 된 것이다.

추가 과제는 선택 사항이며 채점하지 않는다.
