[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data)

# 10주차 실습 — 값을 바꿔 보고 마지막에 조립하기

이번 주 실습도 코드를 새로 쓰는 것이 아니라 **값을 바꿔 보는 것**이다.
비교 예제 7개를 이번 주 새 저장소 `web-week10` 의 `ex/` 폴더에 저장하고(1일차는 고르기 페이지 `index.html` 하나와 `.js` 네 개, 2일차는 `.html`·`.js` 세 쌍), 값이나 줄 하나를 바꾼 뒤 결과가 어떻게 달라지는지 본다.
결과는 화면, **F12 › Console**, **F12 › Elements** 에서 본다. DevTools 는 실습 내내 열어 둔다. Console 아래 입력 칸(`>` 표시)에 `items` 를 치고 Enter 하면 지금 배열이 보인다.
2일차 끝에 그 부품으로 `web-week10` 맨 위의 `guestbook.html`·`guestbook.js` 를 조립한다. 두 파일은 지난주 완성본에서 가져온다. 채점 대상은 2일차 캡처 1장이다.
`student01` 은 예시 아이디이므로 본인 아이디로 바꾼다.

파일을 받는 법, 고르기 페이지 쓰는 법, Console 에 `items` 를 쳐 보는 법은 [따라하기 1일차](walkthrough.md#1일차)에 있다.
"바꿔 보기"는 **무엇이 달라질지 먼저 말해 보고** 저장 → 새로고침으로 확인한다. 확인했으면 원래대로 되돌리고 다음으로 간다.

## 1일차 — 배열과 목록 한 줄 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 새 폴더 `web-week10` 을 만들어 VS Code 로 연다(**File › Open Folder**). 지난주 완성본을 넣는다: 내 `web-week09` 저장소 GitHub 화면 › **Code › Download ZIP** → 압축을 풀어 맨 위 파일과 `images/`·`screenshots/` 를 넣는다. 못 받으면 교재 [9주차 `examples/day2/web-week09/`](../week09_architecture_project/examples/day2/web-week09/) 파일을 **Raw** 로 받는다. `ex` 폴더를 만들고 교재 [`examples/day1/`](examples/day1/) 의 다섯 파일(고르기 페이지 `index.html` 과 ex01~ex04 의 `.js`)을 **Raw** 로 저장한다 |
| 5–14분 | ex01 배열 |
| 14–23분 | ex02 for |
| 23–35분 | ex03 목록 한 줄 만들기 |
| 35–47분 | ex04 누를 때마다 쌓기 |
| 47–50분 | 확인: 다섯 파일이 `ex/` 에 있고, 각 예제에서 값 하나 이상을 바꿨는지. 주석으로 만든 줄과 바꾼 값은 되돌려 두었는지 |
| 50–60분 | 이번 주 저장소 만들어 올리기: GitHub 에 새 저장소 `web-week10` → [올리기 명령](#이번-주-저장소-만들어-올리기) → **Settings › Pages** → 공개 주소 `https://student01.github.io/web-week10/ex/` 확인 → 공용 PC면 자격 증명 삭제 |

1일차 예제는 모두 `ex/index.html` 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 네 줄 중 **지금 문항의 줄 하나만** 주석 밖에 둔다(줄에서 **Ctrl+/**, macOS **⌘+/**). 코드는 각 `.js` 파일에서 고치고, 저장 → `ex/index.html` 새로고침으로 본다.

### 1. ex01 배열 (`[]` · `push` · `length` · `items[i]` · `['…', '…']`)

[examples/day1/ex01_array.js](examples/day1/ex01_array.js) 를 `ex/ex01_array.js` 로 저장한다. `ex/index.html` 맨 아래에서 `ex01_array.js` 줄만 켠다(처음 받은 상태가 이렇다).

- 바꿔 보기: Console 의 1번과 2번 개수는? 2번 줄 끝의 `(3) [...]` 앞 ▶ 를 눌러 펼친다. 번호 `0`·`1`·`2` 옆에 무엇이 있나? 4번 `items[2]` 가 마지막인 이유는?
- 바꿔 보기: Console 아래 입력 칸에 `items` 를 치고 Enter, 이어서 `items.length`, `items[1]` 을 친다. 파일을 고치지 않고 배열을 보는 방법이다. 입력 칸에서 `items.push('student04: 또 왔습니다')` 를 친 뒤 `items.length` 는?
- 바꿔 보기: 8행 앞에 `//` 를 붙여 `push` 를 하나 뺀다. 2번 개수와 4번 `items[2]` 는? 확인했으면 되돌린다.
- 바꿔 보기: 12행 `items[0]` 을 `items[1]` 로 바꾼다. 3번에 무엇이 찍히나? 첫 번째 값의 번호는 몇인가? 확인했으면 되돌린다.
- 바꿔 보기: 6번은 `push` 없이 대괄호 안에 값을 적어 만든 배열이다. 16행 `'student02'` 뒤에 `, 'student03'` 을 더한다. 6번 개수는? 이어서 방금 넣은 쉼표만 지운다. 빨간 줄은 무엇이라고 하나? 1~5번은 찍히나? 확인했으면 되돌린다. 2일차 ex05·ex06 의 바꿔 보기에서 이 모양을 직접 쓴다.
- 흔한 실수: 첫 번째 값을 `items[1]` 로 꺼낸다. 번호는 **0 부터** 센다. 값이 세 개면 번호는 0·1·2 이고 `items[3]` 은 `undefined` 다(빨간 줄은 뜨지 않는다).

### 2. ex02 for (`for (let i = 0; i < items.length; i++)`)

[examples/day1/ex02_for.js](examples/day1/ex02_for.js) 를 `ex/ex02_for.js` 로 저장한다. `ex/index.html` 맨 아래에서 ex01 줄을 끄고 `ex02_for.js` 줄만 켠다.

- 바꿔 보기: 1번은 몇 줄, 2번은 몇 줄인가? 1번이 빠뜨린 값은 무엇인가? 두 `for` 에서 다른 곳은 어디 하나인가?
- 바꿔 보기: 5행 앞에 `//` 를 붙여 넷째 값을 넣지 않는다. 1번과 2번은 각각 몇 줄인가? 언제 두 `for` 의 결과가 같아지나? 확인했으면 되돌린다.
- 바꿔 보기: 14행 `i < items.length` 를 `i <= items.length` 로 바꾼다. 2번 마지막 줄의 번호와 값은? 확인했으면 되돌린다.
- 바꿔 보기: 14행 `let i` 를 `const i` 로 바꾼다. 2번이 몇 줄 찍히고 멈추나? 빨간 줄은 무엇이라고 하고 `파일:줄` 은 몇 행인가? 6주차 ex03 의 `const count` 와 같은 이유다. 확인했으면 되돌린다.
- 흔한 실수: 끝을 숫자로 적는다(1번). 배열에 값이 늘거나 줄면 빠뜨리거나 없는 번호까지 간다. 끝은 `items.length` 로 적는다. `i` 는 한 바퀴마다 바뀌므로 `let` 이다.

### 3. ex03 목록 한 줄 만들기 (`createElement` · `textContent` · `append`)

[examples/day1/ex03_create_li.js](examples/day1/ex03_create_li.js) 를 `ex/ex03_create_li.js` 로 저장한다. `ex/index.html` 에서 `ex03_create_li.js` 줄만 켠다.

- 바꿔 보기: 화면 목록에 몇 줄이 보이나? Console 1번에는 만든 `<li>` 가 찍혀 있다. **F12 › Elements** 에서 `<ul id="list">` 를 펼친다. 1번 줄은 거기 있나?
- 바꿔 보기: 파일 맨 끝(21행 아래)에 `list.append(li1);` 한 줄을 더한다. 1번 줄은 목록의 어디에 나타나나? 왜 맨 위가 아닌가? 확인했으면 되돌린다.
- 바꿔 보기: 7행 `createElement('li')` 의 `'li'` 를 `'<li>'` 로 바꾼다. 빨간 줄은 무엇이라고 하나? 그 아래 2·3번은 실행되나? 확인했으면 되돌린다.
- 흔한 실수: `list.append(…)` 를 빠뜨린다(1번). 빨간 줄 없이 화면에 아무것도 없다. **만들기 → 글자 넣기 → 붙이기** 세 줄이 한 묶음이다.

### 4. ex04 누를 때마다 쌓기 (`push` · `append` · `` `${items.length}개` ``)

[examples/day1/ex04_push_add.js](examples/day1/ex04_push_add.js) 를 `ex/ex04_push_add.js` 로 저장한다. `ex/index.html` 에서 `ex04_push_add.js` 줄만 켠다.

- 바꿔 보기: 칸의 글을 `student01: 안녕하세요` → `student02: 고맙습니다` → `student03: 반갑습니다` 로 바꿔 가며 **더하기**를 세 번 누른다. 화면의 줄, `N개`, Console 3번은? Console 입력 칸에 `items` 를 쳐서 화면의 줄과 비교한다.
- 바꿔 보기: 12행 `items.push(text);` 앞에 `//` 를 붙이고 세 번 누른다. 화면의 줄과 `N개` 는? 왜 서로 맞지 않나? 확인했으면 되돌린다.
- 바꿔 보기: 16행 `list.append(li);` 앞에 `//` 를 붙이고 세 번 누른다. 이번에는 무엇이 맞지 않나? 확인했으면 되돌린다.
- 바꿔 보기: 18행의 백틱(`` ` ``) 두 개를 작은따옴표(`'`)로 바꾼다. 개수 자리에 무엇이 보이나? 5주차 템플릿 문자열을 떠올린다. 확인했으면 되돌린다.
- 흔한 실수: 칸을 비우고 누르면 빈 줄이 쌓이고 개수도 오른다. 이 예제에는 빈칸 확인이 없다. 조립하는 방명록에는 7주차의 빈칸 안내(`if … return`)가 이미 있다.

### 이번 주 저장소 만들어 올리기

GitHub 에서 **New repository** → 이름 `web-week10`, **Public**, README 는 추가하지 않는다. VS Code 터미널(현재 폴더 `web-week10`)에서 2주차에 배운 순서 그대로 친다.

```bash
git init
git add .
git commit -m "10주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week10.git
git push -u origin main
```

저장소 **Settings › Pages › Branch: main, /(root) › Save** → 1~3분 뒤 `https://student01.github.io/web-week10/ex/` 를 연다. `ex/index.html` 의 화면(제목과 "예제가 쓰는 자리")이 보이면 된 것이다. 공용 PC면 자격 증명을 지우고 나간다.
지난주 완성본에 `README.md` 가 있으므로 GitHub 저장소 첫 화면에 그 내용이 보인다. 오늘 올린 것은 확인용이다. 제출은 2일차에 캡처 한 장만 한다.

## 2일차 — 다시 그리기와 삭제 버튼, 그리고 조립 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC에 `web-week10` 폴더가 남아 있으면 그대로 연다. 없으면 `git clone https://github.com/student01/web-week10.git` 뒤 **File › Open Folder**. 교재 [`examples/day2/`](examples/day2/) 의 여섯 파일(ex05~ex07 의 `.html`·`.js`)을 **Raw** 로 `ex/` 에 저장한다 |
| 5–13분 | ex05 비우고 다시 그리기 |
| 13–21분 | ex06 showList |
| 21–29분 | ex07 삭제 버튼 틀 |
| 29–48분 | 조립: `guestbook.html` 의 두 줄을 네 줄로, `guestbook.js` 는 조립표 순서로 고치기 |
| 48–55분 | 확인: 375·1280 폭에서 남기기·삭제, `node server.mjs` → `http://localhost:8000/guestbook.html`. Node 가 없으면 `guestbook.html` 을 두 번 눌러 연다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit -m "10주차 2일차"` → `git push` → 공개 주소 `https://student01.github.io/web-week10/guestbook.html` 에서 글 3개 → 가운데 삭제 → `2개` **캡처 1장** → 공용 PC면 자격 증명 삭제 |

2일차 예제는 `.html` 과 `.js` 가 한 쌍이다. 두 파일을 같은 `ex/` 폴더에 저장하고 `.html` 을 연다. 코드는 `.js` 에 있다.
파일마다 **바꿔 보기를 하나 이상** 하고 넘어간다. 29분이 되면 남은 것은 두고 조립을 시작한다. 남은 바꿔 보기는 캡처까지 끝낸 뒤 한다.

### 5. ex05 비우고 다시 그리기 (`list.innerHTML = ''`)

[examples/day2/ex05_redraw.html](examples/day2/ex05_redraw.html) 과 [ex05_redraw.js](examples/day2/ex05_redraw.js) 를 `ex/` 에 저장하고 `ex05_redraw.html` 을 연다.

- 바꿔 보기: **1. 비우지 않고 그리기**를 두 번, **2. 비우고 그리기**를 한 번 누른다. 누를 때마다 화면은 몇 줄인가? Console 의 배열 개수는 늘 몇 개인가?
- 바꿔 보기: 19행 `list.innerHTML = '';` 앞에 `//` 를 붙이고 2번을 세 번 누른다. 1번과 무엇이 같아졌나? 확인했으면 되돌린다.
- 바꿔 보기: 5행 배열의 `'student03: 반갑습니다'` 뒤에 `, 'student04: 또 왔습니다'` 를 더한다. 2번을 누르면 몇 줄인가? 그리는 코드는 고쳤나? 확인했으면 되돌린다.
- 흔한 실수: 다시 그리기 전에 비우지 않는다. 앞에 그린 줄이 남아 누를 때마다 목록이 늘어난다. 이 수업에서 `innerHTML` 은 **비우기(`= ''`)에만** 쓴다. 남긴 글을 넣을 때는 `textContent` 를 쓴다.

### 6. ex06 showList (`function showList()` · 열 때 · 바꾼 뒤)

[examples/day2/ex06_show_list.html](examples/day2/ex06_show_list.html) 과 [ex06_show_list.js](examples/day2/ex06_show_list.js) 를 `ex/` 에 저장하고 `ex06_show_list.html` 을 연다.

- 바꿔 보기: 열자마자 목록·안내 문장·개수는? **더하기**를 세 번 누른다. 무엇이 사라지고 무엇이 바뀌나? Console 1번은 몇 번, 2번은 몇 번 찍혔나?
- 바꿔 보기: 8행을 `let items = ['student02: 고맙습니다'];` 로 바꾸고 새로고침한다. 열자마자 화면은? 이어서 26행 `showList();` 앞에 `//` 를 붙이고 새로고침한다. 화면의 개수와 Console 1번의 개수는 각각 몇인가? 열 때도 한 번 그려야 하는 이유는? 확인했으면 둘 다 되돌린다.
- 바꿔 보기: 32행 `showList();` 앞에 `//` 를 붙이고 **더하기**를 두 번 누른다. 화면과 Console 2번은? Console 입력 칸에 `items` 를 친다. 확인했으면 되돌린다.
- 흔한 실수: 개수 줄(17행)을 `for` 안에 넣는다. 배열이 비면 `for` 안이 한 번도 실행되지 않아 개수가 바뀌지 않는다. 조립한 방명록에서 모두 지웠는데 `1개` 가 남는 원인이다. 개수와 안내 문장은 `for` **밖**에서 한 번 쓴다.

### 7. ex07 삭제 버튼 틀 (`createElement('button')` · `splice(i, 1)` · `showList()`)

[examples/day2/ex07_delete_button.html](examples/day2/ex07_delete_button.html) 과 [ex07_delete_button.js](examples/day2/ex07_delete_button.js) 를 `ex/` 에 저장하고 `ex07_delete_button.html` 을 연다.

14~20행 일곱 줄은 **삭제 버튼 틀**이다. 뜯어보지 않고 그대로 옮겨 쓴다. `showList()` 가 다시 그릴 때 버튼마다 번호를 새로 붙인다.

- 바꿔 보기: 가운데 줄 `student02: 고맙습니다` 의 **[삭제]** 를 누른다. 남은 줄과 `N개` 는? Console 의 `그린 뒤 items :` 는 몇 번 찍혔나? 이어서 맨 위 **[삭제]** 를 두 번 더 누른다. 마지막 화면은?
- 바꿔 보기: 17행 `items.splice(i, 1);` 의 `1` 을 `2` 로 바꾸고 새로고침한 뒤 맨 위 **[삭제]** 를 누른다. 몇 줄이 지워지나? `splice` 의 둘째 값은 무엇을 정하나? 확인했으면 되돌린다.
- 바꿔 보기: 18행 `showList();` 앞에 `//` 를 붙이고 가운데 **[삭제]** 를 누른다. 화면과 `N개` 는? Console 입력 칸에 `items` 를 치면 몇 개인가? 확인했으면 되돌린다.
- 흔한 실수: 틀 안의 `showList();` 를 빠뜨린다. 배열에서는 빠졌는데 화면은 그대로라 빨간 줄 없이 "안 지워진다"고 느낀다. Console 에 `items` 를 쳐서 배열과 화면을 따로 확인한다.

### 8. 조립 — `guestbook.html` 네 줄, `guestbook.js` (`push` · `showList` · 삭제 버튼 틀)

이제 `ex/` 가 아니라 `web-week10` 맨 위의 `guestbook.html`·`guestbook.js` 를 연다. `ex/index.html` 은 1일차 예제 고르기 페이지라서 조립에 쓰지 않는다. 전문과 단계는 [따라하기 2일차](walkthrough.md#2일차)에 있다.

- `guestbook.html` 의 `<h3>마지막으로 남긴 글</h3>` 과 `<div class="card" id="last">아직 남긴 글이 없습니다.</div>` 두 줄을 지우고 네 줄을 넣는다: `<h3>남긴 글</h3>`, `<ul class="card" id="list"></ul>`, `<div id="empty">아직 남긴 글이 없습니다.</div>`, `<div id="count">0개</div>`.
- `guestbook.js` 는 9주차 파일을 고친다. 맨 위 `const last = …` 한 줄을 네 줄로, `clearNotice` 아래에 `showList()` 함수, submit 안의 `last.textContent = …` 한 줄을 두 줄로, 파일 맨 끝에 `showList();` 한 줄.
- 7주차에 만든 줄(폼·입력 칸 찾기, `clearNotice`, submit 안의 빈칸 안내·`form.reset()`·`focus()`, input 리스너 두 줄)은 그대로 둔다(교재 완성본은 submit 안의 빈 줄만 뺐다. 남아 있어도 동작은 같다).

| 조립할 줄 | 어느 ex 에서 본 것 |
|---|---|
| `guestbook.html` 의 `<h3>남긴 글</h3>` | 9주차 완성본의 `<h3>마지막으로 남긴 글</h3>` 에서 "마지막으로" 를 뺀 것 |
| `guestbook.html` 의 `<ul class="card" id="list"></ul>` | ex03 (빈 `<ul id="list">`), 4주차 `.card` |
| `guestbook.html` 의 `<div id="empty">아직 남긴 글이 없습니다.</div>` · `<div id="count">0개</div>` | ex06 (안내 자리와 개수 자리) |
| `const list = document.querySelector('#list');` · `const empty = …('#empty');` · `const count = …('#count');` | ex06 (찾아서 `const` 에 담기, 6주차 ex01) |
| `let items = [];` | ex01 1번 (빈 배열) |
| `function showList() { … }` 의 `list.innerHTML = '';` | ex05 2번 (비우고 그리기) |
| `for (let i = 0; i < items.length; i++) { … }` | ex02 2번 (끝을 `items.length` 로) |
| `const li = document.createElement('li');` · `li.textContent = items[i];` · `list.append(li);` | ex03 2번 + ex05 (배열의 `i` 번째 글로 한 줄) |
| 삭제 버튼 틀 일곱 줄(`const removeButton = …` 부터 `li.append(removeButton);` 까지) | ex07 (그대로 옮겨 쓴다) |
| `` count.textContent = `${items.length}개`; `` | ex04 3번 (개수는 배열의 `length`) |
| `if (items.length === 0) { empty.textContent = '아직 남긴 글이 없습니다.'; } else { empty.textContent = ''; }` | ex06 (5주차 ex07 `if / else`) |
| submit 안 `` items.push(`${name}: ${message}`); `` | ex04 1번 (`push`). 넣는 문장은 9주차 `last.textContent` 오른쪽 그대로 |
| submit 안 `showList();` | ex06 2번 (넣고 다시 그리기) |
| 파일 맨 끝 `showList();` | ex06 1번 (열 때 한 번) |

- 확인: 저장하고 `guestbook.html` 을 새로고침한다. 열자마자 목록은 비어 있고 `아직 남긴 글이 없습니다.` 와 `0개` 가 보인다. 이름·메시지를 넣고 **남기기**를 세 번 누르면 세 줄이 쌓이고 줄마다 **[삭제]**, `3개`, 안내 문장은 사라진다. 가운데 **[삭제]** 를 누르면 두 줄과 `2개` 가 남으면 된 것이다.
- 바꿔 보기: 글 두 개를 남긴 뒤 새로고침한다. 목록과 개수는 어떻게 되나? 왜 그런가? (새로고침하면 파일을 다시 읽어 배열을 `[]` 로 새로 만든다. 남기는 법은 11주차다.)
- 흔한 실수: `guestbook.html` 만 고치고 `guestbook.js` 의 `last.textContent = …` 줄이 남아 있다. 이름·메시지를 넣고 **남기기**를 누르면 `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` 가 뜨고 목록에 아무것도 쌓이지 않는다. 입력 칸도 비워지지 않는다. 지운 `#last` 를 아직 쓰고 있는 것이다.

### 9. 375·1280 폭과 서버로 확인

- DevTools 의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)로 폭 375 와 1280 에서 글 하나를 남기고 지워 본다. 두 폭 모두 목록과 **[삭제]** 가 보이고 개수가 맞으면 된 것이다.
- 1일차에 넣어 둔 `server.mjs` 가 없으면 [server.mjs](../../tools/static-server/server.mjs) 를 **Raw** 로 받아 `web-week10` 맨 위에 둔다. 터미널(현재 폴더 `web-week10`)에서 `node server.mjs` → `http://localhost:8000/guestbook.html` 을 연다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.
- 확인이 끝나면 터미널에서 **Ctrl+C** 로 서버를 멈추고 끝 루틴으로 간다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다 |
| push 가 거부되거나 로그인 창이 안 뜬다 | [2주차 막혔을 때](../week02_github_pages/lab.md#막혔을-때) 표를 본다 |
| 화면이 생각과 다른데 이유를 모르겠다 | **Console 을 먼저 연다.** 빨간 줄 오른쪽 `파일:줄` 로 간다. 빨간 줄이 없으면 Console 입력 칸에 `items` 를 쳐서 **배열**을 보고, 화면의 **줄**과 따로 비교한다 |
| 1일차 예제를 열었는데 Console 에 예제 줄이 하나도 없다 | `ex/index.html` 맨 아래에서 그 문항의 `script` 줄을 켰는지(주석 밖인지), `.js` 파일이 같은 `ex/` 폴더에 있는지 본다. `Failed to load resource: net::ERR_FILE_NOT_FOUND` 줄이 있으면 `script` 줄의 파일 이름 철자가 틀렸거나 그 파일이 `ex/` 에 없다 |
| `Uncaught SyntaxError: Identifier '…' has already been declared`(`'items'`·`'list'`), 또는 두 예제의 Console 줄이 섞여 찍힌다 | 고르기 페이지에서 `script` 줄을 둘 이상 켰다. 빨간 줄의 `파일:줄` 은 `index.html` 에서 더 아래에 있는 `script` 줄 파일의 1행을 가리킨다. 켠 순서와는 상관없다. ex01·ex02·ex04 는 모두 `items` 를, ex03·ex04 는 둘 다 `list` 를 만든다. 이름이 겹치지 않으면(ex01·ex03) 빨간 줄 없이 두 예제가 함께 실행된다. 한 줄만 켠다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'innerHTML')` | 목록 `<ul>` 을 못 찾았다. `guestbook.html` 의 `id="list"` 와 `guestbook.js` 의 `querySelector('#list')` 를 글자 단위로 비교한다. 파일 맨 끝 `showList();` 때문에 페이지를 **열자마자** 뜬다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` | 열자마자 뜨면 `#empty` 나 `#count` 를 못 찾았다(**남기기** 때도 다시 뜬다). `guestbook.html` 에 네 줄을 넣었는지, id 철자가 같은지 본다. 열 때는 없다가 **남기기**를 누를 때 처음 뜨면 지운 `#last` 를 쓰는 `last.textContent = …` 줄이 남아 있다 |
| `Uncaught ReferenceError: last is not defined` | `const last = …` 줄은 지웠는데 submit 안의 `last.textContent = …` 줄이 남아 있다. 그 줄을 `items.push(…)` 와 `showList();` 두 줄로 바꾼다 |
| `Uncaught ReferenceError: showList is not defined` | 함수 이름과 부른 이름이 다르다. `function showList()` 와 `showList();` 의 대소문자까지 비교한다 |
| `Uncaught ReferenceError: items is not defined` | `let items = [];` 줄이 없거나 이름이 다르다(`item`). 맨 위 찾아 두기 줄 아래에 있는지 본다 |
| `Uncaught TypeError: document.creatElement is not a function` | `createElement` 철자가 틀렸다. 글을 남길 때 처음 뜬다. 목록이 비어 있으면 `for` 안이 실행되지 않기 때문이다 |
| `Uncaught TypeError: Assignment to constant variable.` | `for (const i = 0; …)` 로 썼다. `i` 는 한 바퀴마다 바뀌므로 `let` 이다(ex02 넷째 바꿔 보기) |
| 개수가 `undefined개` 로 보인다 | `items.lenght` 처럼 `length` 철자가 틀렸다. 빨간 줄이 없으니 화면 글자로 찾는다 |
| **남기기**를 눌러도 목록과 개수가 그대로다. 빨간 줄도 없다 | submit 안에 `showList();` 가 없다. 입력 칸은 비워지고 배열에는 들어갔다. Console 에 `items` 를 쳐 본다(ex06 셋째 바꿔 보기) |
| **[삭제]** 를 눌러도 화면과 개수가 그대로다 | 삭제 버튼 틀 안의 `showList();` 가 빠졌다. 배열만 줄었다(ex07 셋째 바꿔 보기) |
| 남기거나 지울 때마다 목록이 늘어난다 | `showList()` 첫 줄 `list.innerHTML = '';` 가 빠졌다. 비우지 않고 다시 그리면 앞의 줄이 남는다(ex05) |
| 모두 지웠는데 `1개` 가 남는다 | 개수 줄이 `for` 안에 있다. `for` 밖으로 옮긴다(ex06 흔한 실수) |
| 목록 맨 끝에 글 없이 **[삭제]** 만 있는 줄이 하나 더 생긴다(열자마자도 보인다) | `for` 의 조건을 `i <= items.length` 로 썼다. 마지막 번호는 `items.length - 1` 이다(ex02 셋째 바꿔 보기) |
| 새로고침하면 목록이 사라진다 | 정상이다. 새로고침하면 파일을 다시 읽어 배열을 `[]` 로 새로 만든다. 남기는 법은 11주차에 배운다 |
| 공개 주소 `…/web-week10/ex/` 가 404 다 | ① 폴더 이름이 `ex` 인지 ② 그 안에 `index.html` 이 있는지 ③ 저장소 이름이 `web-week10` 이고 **Settings › Pages** 가 켜져 있는지 본다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://student01.github.io/web-week10/guestbook.html` (본인 아이디) 을 열고 글 **세 개**를 남긴 뒤 **가운데** 줄의 **[삭제]** 를 누른 화면을 캡처한다.

- 목록에 두 줄이 남아 있고 각 줄에 **[삭제]** 버튼이 보인다.
- 목록 아래 숫자가 `2개` 다.
- **주소창이 함께 보이게** 찍는다.

1일차 push 와 `ex/` 실험 파일은 확인용이며 따로 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 전체 지우기: `guestbook.html` 의 `<div id="count">0개</div>` 아래에 `<div><button id="clear-button" type="button">전체 지우기</button></div>` 를 넣는다. `guestbook.js` 의 `const count = …` 줄 아래에서 그 버튼을 찾아 두고, 누르면 `items = [];` 와 `showList();` 두 줄을 실행하게 한다. `items` 를 `let` 으로 만든 이유가 여기서 보인다. `const` 였다면 누를 때 무슨 빨간 줄이 뜨나?
- 버튼 여백: `styles.css` 맨 아래에 `.card button { margin-left: 8px; }` 를 더한다. 글과 **[삭제]** 사이가 띄워지나? 왜 `.card` 안의 버튼에만 맞나?
- 이메일도 함께: submit 안에서 이메일 칸의 값도 읽어 `` `${name}(${email}): ${message}` `` 로 넣어 본다. 이메일 칸을 찾는 줄은 맨 위에 하나 더 둔다. 이메일을 비우고 남기면 어떻게 보이나?
- Console 에서 직접: 방명록을 연 채 Console 입력 칸에 `items.push('직접 넣은 줄')` 을 치고, 이어서 `showList()` 를 친다. 화면이 언제 바뀌나?

추가 과제는 선택 사항이며 채점하지 않는다.
해 본 것은 확인한 뒤 모두 되돌려 교재 완성본과 같게 둔다. 이미 push 했다면 되돌린 뒤 `git add .` → `git commit -m "10주차 2일차"` → `git push` 를 한 번 더 한다.
11주차는 내 `web-week10` 에서 시작해 같은 **[전체 지우기]** 를 조립한다. 남겨 두면 그때 같은 줄이 두 번 들어가 `Uncaught SyntaxError: Identifier 'clearButton' has already been declared` 가 뜨고 `guestbook.js` 전체가 실행되지 않는다.
