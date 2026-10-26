[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data)

# 10주차 따라하기 — 비교 예제로 원리를 보고 마지막에 조립

이번 주는 새 저장소 `web-week10`을 만든다. 지난주 완성본을 넣고, 비교 예제는 그 안의 `ex/` 폴더에 저장한다. 값·줄을 바꾼 뒤 결과를 화면과 **F12 › Console**, **F12 › Elements**에서 본다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

비교 예제 7개는 교재 저장소의 [examples/day1](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data/examples/day1)(1일차 ex01~ex04와 고르기 페이지)과 [examples/day2](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data/examples/day2)(2일차 ex05~ex07) 폴더에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다.

## 1일차

### 1. web-week10 폴더 만들고 지난주 완성본 넣기

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-week10`을 만들고 VS Code **File › Open Folder**로 연다.

지난주 완성본을 넣는다. 내 `web-week09` 저장소 GitHub 화면에서 **Code › Download ZIP**을 누르고, 압축을 푼 폴더에서 맨 위 파일(`index.html`·`about.html`·`guestbook.html`·`styles.css`·`app.js`·`guestbook.js`·`README.md`·`server.mjs`)과 `images/`·`screenshots/`를 `web-week10`으로 옮긴다. 지난주 `ex/` 폴더는 옮기지 않는다.
ZIP을 못 받았으면 교재 [9주차 `examples/day2/web-week09/`](../week09_architecture_project/examples/day2/web-week09/)의 파일을 2단계와 같은 **Raw** 방법으로 받고, [server.mjs](../../tools/static-server/server.mjs)도 같은 방법으로 받는다.

이어서 `web-week10` 안에 `ex` 폴더를 만든다. 현재 폴더: `web-week10`

```bash
mkdir ex
```

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week10/
  ex/            ← 아직 비어 있다
  images/
  screenshots/
  about.html
  app.js
  guestbook.html
  guestbook.js
  index.html
  README.md
  server.mjs
  styles.css
```

- `guestbook.html`을 두 번 눌러 열면 9주차 방명록이 보인다. 폼 아래 `마지막으로 남긴 글` 카드에는 마지막 글 한 줄만 보인다. 이번 주는 여기서 시작한다.
- `guestbook.html`·`guestbook.js`는 오늘 건드리지 않는다. 2일차 끝에 조립한다.

### 2. 비교 예제 가져오기

오늘 파일은 다섯 개다. 고르기 페이지 `index.html` 하나와 예제 코드 `.js` 네 개다. 네 예제가 같은 화면(글 칸과 **더하기** 버튼, 빈 목록, 개수 자리)을 쓰기 때문에 화면은 `index.html` 하나에 두고 코드만 따로 뗐다.

| 파일 | 비교하는 것 |
|---|---|
| [index.html](examples/day1/index.html) | 고르기 페이지. 맨 아래 `<script src>` 네 줄 중 하나만 켠다. 예제가 쓰는 자리(`#text`·`#add`·`#list`·`#count`)가 여기 있다 |
| [ex01_array.js](examples/day1/ex01_array.js) | 빈 배열 / `push` 세 번 / `items[0]`·`items[2]`·`items[3]` / 처음 값을 넣어 만든 배열 |
| [ex02_for.js](examples/day1/ex02_for.js) | 끝을 `3`으로 적은 `for` / 끝을 `items.length`로 적은 `for` |
| [ex03_create_li.js](examples/day1/ex03_create_li.js) | 만들기만 / 만들고 붙이기 / 하나 더 붙이기 |
| [ex04_push_add.js](examples/day1/ex04_push_add.js) | 누를 때 배열에 넣기 / 화면에 붙이기 / 개수 쓰기 |

[교재 저장소 examples/day1 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data/examples/day1)에서 파일을 누르고 오른쪽 위 **Raw**를 누른다. 코드만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `web-week10/ex/`에 저장한다. 파일 이름은 교재와 **같게** 둔다. Raw가 열리지 않을 때만 주석 줄까지 그대로 친다.

**예상 결과** — `ex/` 안에 파일 다섯 개가 있다.

```text
ex/
  ex01_array.js
  ex02_for.js
  ex03_create_li.js
  ex04_push_add.js
  index.html
```

- 저장한 파일 이름이 `.txt`로 끝나면 이름을 고친다. 이름은 VS Code 탐색기에서 확인한다.
- `ex/index.html`은 예제를 고르는 페이지다. 맨 위 `index.html`(내 사이트)과 이름이 같지만 다른 파일이다. 탭 이름 옆 폴더 경로로 구분한다.

### 3. 고르기 페이지와 Console 입력 칸

`ex/index.html`을 Chrome으로 연다(VS Code 탐색기에서 오른쪽 클릭 › **Reveal in File Explorer**, macOS는 **Reveal in Finder** → 두 번 누르기). `.js` 파일은 두 번 누르지 않는다. `.js`는 `index.html`이 불러온다.

VS Code에서 `ex/index.html`도 열어 맨 아래를 본다.

```html
<script src="ex01_array.js"></script>
<!-- <script src="ex02_for.js"></script> -->
<!-- <script src="ex03_create_li.js"></script> -->
<!-- <script src="ex04_push_add.js"></script> -->
```

지금은 ex01 줄만 켜져 있다. 다른 예제로 바꿀 때는 켜 둔 줄에 커서를 두고 **Ctrl+/**(macOS **⌘+/**)로 주석으로 만들고, 볼 줄에서 다시 **Ctrl+/** 로 주석을 푼다. 저장 → 새로고침한다. 한 번에 한 줄만 켠다.

**예상 결과** — F12 › **Console**에 여섯 줄이 찍혀 있다. 화면의 "예제가 쓰는 자리"는 그대로다(ex01은 Console에만 찍는다).

```text
1. 빈 배열의 개수 : 0                                     ex01_array.js:5
2. push 세 번 뒤의 개수 : 3 (3) ['student01: 안녕하세요', 'student02: 고맙습니다', 'student03: 반갑습니다']   ex01_array.js:10
3. 첫 번째 items[0] : student01: 안녕하세요               ex01_array.js:12
4. 마지막 items[2] : student03: 반갑습니다                ex01_array.js:13
5. 없는 번호 items[3] : undefined                         ex01_array.js:14
6. 처음 값을 넣어 만든 배열의 개수 : 2 (2) ['student01', 'student02']   ex01_array.js:17
```

이번 주에는 Console **입력 칸**도 쓴다. Console 맨 아래 `>` 표시 옆을 누르고 `items`를 친 뒤 Enter를 누른다. 이어서 `items.length`, `items[0]`도 쳐 본다.

**예상 결과** — 입력한 줄 아래에 답이 나온다.

```text
> items
< (3) ['student01: 안녕하세요', 'student02: 고맙습니다', 'student03: 반갑습니다']
> items.length
< 3
> items[0]
< 'student01: 안녕하세요'
```

- 배열 앞의 ▶를 누르면 펼쳐져 `0`·`1`·`2` 번호와 값, 그리고 `length: 3`이 보인다. 번호는 0부터, 개수는 3이다.
- 6번은 `push` 없이 대괄호 안에 값을 쉼표로 나눠 적어 만든 배열이다. ex02·ex05·ex07이 이 모양으로 배열을 시작한다.
- 입력 칸은 파일을 고치지 않고 지금 페이지의 변수를 들여다보는 곳이다. 새로고침하면 파일을 다시 읽어 처음 값으로 돌아간다.
- `items is not defined`가 나오면 켜 둔 예제에 `items`가 없거나, 파일을 아직 불러오지 못한 것이다. 켜 둔 `script` 줄부터 본다.

### 4. 값 바꾸는 요령

실험은 늘 같은 순서다. **VS Code에서 고치고 저장**(Ctrl+S, macOS는 ⌘+S) → **브라우저에서 새로고침**(F5, macOS는 ⌘+R) → **화면·Console·Elements**를 본다.
바꾸기 전에 무엇이 달라질지 먼저 말해 보고 확인한다.

**눌러 보기** — `ex/index.html` 맨 아래에서 ex01 줄을 끄고 `ex04_push_add.js` 줄을 켠 뒤 저장 → 새로고침한다. 글 칸을 `student01: 안녕하세요` → `student02: 고맙습니다` → `student03: 반갑습니다`로 바꿔 가며 **더하기**를 세 번 누른다.

**예상 결과** — 화면의 빈 목록에 세 줄이 쌓이고 개수 자리가 `3개`가 된다.

```text
• student01: 안녕하세요
• student02: 고맙습니다
• student03: 반갑습니다
3개
```

Console에는 누를 때마다 1·2·3번이 한 묶음씩 찍힌다. 3번 개수가 `1`·`2`·`3`으로 오른다. 입력 칸에 `items`를 치면 화면의 세 줄과 같은 값이 배열로 보인다.

- F12 › **Elements**에서 `<ul id="list">`를 펼치면 `<li>` 세 개가 보인다. 페이지 소스 보기(**Ctrl+U**, macOS **⌘+Option+U**)의 `<ul id="list"></ul>`은 비어 있다. JavaScript가 만들어 붙인 줄은 DOM에만 있다(6주차 ex01).
- 새로고침하면 목록이 비고 `0개`로 돌아간다. 브라우저가 파일을 다시 읽어 배열과 DOM을 새로 만들기 때문이다.
- 값을 원래대로 못 돌리겠으면 교재에서 그 파일을 다시 **Raw**로 받아 덮어쓴다.
- 파일마다 무엇을 바꿔 볼지는 [1일차 실습](lab.md#1일차--배열과-목록-한-줄-60분)에 있다.

### 5. 이번 주 저장소 만들어 올리기

1일차 50–60분에 한다. 네 예제에서 각각 값 하나 이상을 바꿔 봤으면 올린다.

GitHub에서 **New repository**를 누르고 이름 `web-week10`, **Public**으로 만든다. README는 추가하지 않는다.
터미널에서 2주차에 배운 순서 그대로 친다. 현재 폴더: `web-week10`

```bash
git init
git add .
git commit -m "10주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week10.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save**를 누른다.

**예상 결과** — GitHub 저장소 화면을 새로고침하면 `ex/`·`images/`·`screenshots/`와 맨 위 파일들이 보이고, 그 아래에 지난주 `README.md` 내용이 보인다.
1~3분 뒤 `https://student01.github.io/web-week10/ex/`를 연다. 고르기 페이지의 제목과 "예제가 쓰는 자리"가 보인다. 이 화면은 **확인용**이다.
공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 404가 나면 주소의 `web-week10/ex/`가 저장소·폴더 이름과 글자 단위로 같은지, Pages를 켰는지 본다.
- push가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../week02_github_pages/lab.md#막혔을-때)를 본다.

## 2일차

### 6. 폴더 열고 비교 예제 여섯 파일 가져오기

같은 PC에 `web-week10` 폴더가 남아 있으면 VS Code로 그대로 연다. 없으면 받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week10.git
```

내려받은 `web-week10`을 **File › Open Folder**로 연다.

오늘 예제는 세 개이고, 예제마다 `.html`과 `.js`가 한 쌍이라 파일은 여섯 개다. 오늘 예제는 화면이 서로 달라서 `.html`을 따로 둔다. [교재 저장소 examples/day2 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data/examples/day2)에서 1일차와 같은 **Raw** → 저장으로 `web-week10/ex/`에 넣는다. 같은 폴더의 `web-week10/`은 조립 결과라서 지금 받지 않는다.

| 파일 | 비교하는 것 |
|---|---|
| [ex05_redraw.html](examples/day2/ex05_redraw.html) + [ex05_redraw.js](examples/day2/ex05_redraw.js) | 비우지 않고 그리기 / 비우고 그리기, 버튼 두 개와 빈 목록 |
| [ex06_show_list.html](examples/day2/ex06_show_list.html) + [ex06_show_list.js](examples/day2/ex06_show_list.js) | 열 때 `showList()` / **더하기** 뒤 `showList()`, 목록·안내 문장·개수 |
| [ex07_delete_button.html](examples/day2/ex07_delete_button.html) + [ex07_delete_button.js](examples/day2/ex07_delete_button.js) | 줄마다 **[삭제]** 버튼 틀, 세 줄로 시작하는 목록과 개수 |

**예상 결과** — `ex/`에 파일이 열한 개 있다(1일차 다섯 개 + 오늘 여섯 개).
`ex/ex07_delete_button.html`을 열면 세 줄마다 **[삭제]** 가 있고 `3개`다. 가운데 **[삭제]** 를 누르면 `student01: 안녕하세요`와 `student03: 반갑습니다` 두 줄과 `2개`가 남는다.

- 오늘은 `.html`을 연다. `.js`는 같은 폴더에서 `.html`이 불러온다. 둘 중 하나를 빠뜨리면 목록이 그려지지 않는다.
- `ex05`는 1번을 누를 때마다 줄이 세 줄씩 늘고, 2번은 몇 번을 눌러도 세 줄이다.
- `ex06`은 열자마자 `아직 남긴 글이 없습니다.`와 `0개`이고, **더하기**를 누르면 안내 문장이 사라진다.
- 파일마다 무엇을 바꿔 볼지는 [2일차 실습](lab.md#2일차--다시-그리기와-삭제-버튼-그리고-조립-60분)에 있다.

### 7. 조립표

29분부터 조립한다. 이제 `ex/`가 아니라 `web-week10` 맨 위의 `guestbook.html`·`guestbook.js`를 연다.
조립하는 줄은 모두 비교 예제와 9주차 완성본에서 본 것이다.

| 조립할 줄 | 출처 |
|---|---|
| `guestbook.html`의 `<h3>남긴 글</h3>` | 9주차 `<h3>마지막으로 남긴 글</h3>`에서 "마지막으로"를 뺀 것 |
| `guestbook.html`의 `<ul class="card" id="list"></ul>` | [ex03](examples/day1/ex03_create_li.js)이 쓰는 빈 `<ul id="list">`(고르기 페이지), 4주차 `.card` |
| `guestbook.html`의 `#empty`·`#count` 두 줄 | [ex06](examples/day2/ex06_show_list.html) 안내 자리와 개수 자리 |
| `const list`·`empty`·`count` | [ex06](examples/day2/ex06_show_list.js) 찾아서 `const`에 담기 |
| `let items = [];` | [ex01](examples/day1/ex01_array.js) 1번 빈 배열 |
| `showList()`의 `list.innerHTML = '';` | [ex05](examples/day2/ex05_redraw.js) 2번 비우고 그리기 |
| `for (let i = 0; i < items.length; i++)` | [ex02](examples/day1/ex02_for.js) 2번 |
| `createElement('li')`·`textContent`·`list.append(li)` | [ex03](examples/day1/ex03_create_li.js) 2번 + [ex05](examples/day2/ex05_redraw.js) |
| 삭제 버튼 틀 일곱 줄 | [ex07](examples/day2/ex07_delete_button.js) 그대로 |
| `` count.textContent = `${items.length}개`; `` | [ex04](examples/day1/ex04_push_add.js) 3번 |
| `if (items.length === 0) { … } else { … }` | [ex06](examples/day2/ex06_show_list.js) |
| submit 안 `` items.push(`${name}: ${message}`); `` | [ex04](examples/day1/ex04_push_add.js) 1번 `push`. 넣는 문장은 9주차 `last.textContent`의 오른쪽 그대로 |
| submit 안 `showList();` · 파일 맨 끝 `showList();` | [ex06](examples/day2/ex06_show_list.js) 2번(넣고 다시 그리기) · 1번(열 때 한 번) |

옮겨 적을 때 출처 ex 파일을 옆에 열어 두고, 같은 줄이 거기서 무엇을 했는지 떠올린다.

### 8. guestbook.html의 두 줄을 네 줄로

`web-week10/guestbook.html`을 열고 `</form>` 아래 `<div id="notice"></div>` **다음** 두 줄을 찾는다.

```html
      <h3>마지막으로 남긴 글</h3>
      <div class="card" id="last">아직 남긴 글이 없습니다.</div>
```

이 두 줄을 지우고 그 자리에 네 줄을 넣는다.

```html
      <h3>남긴 글</h3>
      <ul class="card" id="list"></ul>
      <div id="empty">아직 남긴 글이 없습니다.</div>
      <div id="count">0개</div>
```

- `<ul>` 안은 **비워 둔다.** 목록 줄은 JavaScript가 만들어 붙인다. 손으로 `<li>`를 적지 않는다.
- `id`는 `guestbook.js`가 찾을 이름이다. `list`·`empty`·`count`를 글자 단위로 같게 쓴다.
- `class="card"`는 4주차 카드 모양이다. 비어 있을 때도 테두리 상자가 보인다.

**예상 결과** — 저장하고 `guestbook.html`을 새로고침하면 폼 아래에 `남긴 글` 제목, 빈 카드, `아직 남긴 글이 없습니다.`, `0개`가 차례로 보인다. 아직 `guestbook.js`를 고치지 않았으므로 지금 이름·메시지를 넣고 **남기기**를 누르면 Console에 `Uncaught TypeError: Cannot set properties of null (setting 'textContent')`(`guestbook.js:30`)가 뜨고 입력 칸도 비워지지 않는다. 지운 `#last`를 JavaScript가 아직 쓰고 있기 때문이다. 9~11단계에서 고친다.

### 9. guestbook.js 맨 위 — 찾아 두기와 빈 배열

`web-week10/guestbook.js`를 연다. 맨 위 다섯째 줄 `const last = document.querySelector('#last');`를 지우고 그 자리에 네 줄을 넣는다.

```js
const list = document.querySelector('#list');
const empty = document.querySelector('#empty');
const count = document.querySelector('#count');
let items = [];
```

- 앞 세 줄은 8단계에서 넣은 세 자리를 찾아 `const`에 담는다(ex06).
- `let items = [];`는 남긴 글을 쌓을 빈 배열이다(ex01). 이 줄을 빠뜨려도 지금은 빨간 줄이 없다. 11단계에서 맨 끝 `showList();`를 넣은 뒤에 열자마자 `items is not defined`가 뜬다.

**예상 결과** — 새로고침해 Console에 빨간 줄이 없으면 된다. 아직 **남기기**는 누르지 않는다. submit 안에 `last.textContent = …` 줄이 남아 있어 이름·메시지를 넣고 누르면 `Uncaught ReferenceError: last is not defined`(`guestbook.js:33`)가 뜬다. 11단계에서 바꾼다.

### 10. showList 함수 넣기

`clearNotice` 함수 **아래**에 `showList` 함수를 넣는다. ex06의 함수와 같은 모양이다.

```js
function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    list.append(li);
  }
  count.textContent = `${items.length}개`;
  if (items.length === 0) {
    empty.textContent = '아직 남긴 글이 없습니다.';
  } else {
    empty.textContent = '';
  }
}
```

- 첫 줄은 목록을 비운다(ex05 2번). 이 수업에서 `innerHTML`은 비우기에만 쓴다.
- `for` 안의 세 줄은 배열의 `i`번째 글로 한 줄을 만들어 붙인다(ex02 2번, ex03).
- 개수와 안내 문장은 `for` **밖**에서 한 번 쓴다(ex04 3번, ex06).

**예상 결과** — 새로고침해도 화면은 8단계와 같다. 함수를 만들기만 하고 아직 부르는 곳이 없기 때문이다(5주차 ex08). Console에 빨간 줄이 없으면 된다.

### 11. submit 안 두 줄과 맨 끝 한 줄

submit 리스너 안 `clearNotice();` 아래의 `` last.textContent = `${name}: ${message}`; `` 한 줄을 지우고 두 줄을 넣는다.

```js
  items.push(`${name}: ${message}`);
  showList();
```

이어서 파일 **맨 끝**(input 리스너 두 줄 아래)에 한 줄을 더한다.

```js
showList();
```

- `items.push(…)`는 배열 맨 뒤에 한 줄을 넣는다(ex04 1번). 넣는 문장은 9주차 `last.textContent`의 오른쪽과 같다.
- 넣은 뒤 `showList();`로 목록 전체를 다시 그린다(ex06 2번). 맨 끝 `showList();`는 페이지를 열 때 한 번 그린다(ex06 1번).
- 빈칸 안내·`form.reset()`·`nameInput.focus()`는 7주차 그대로 둔다. 빈칸이면 `return`으로 끝나 배열에 들어가지 않는다.

**예상 결과** — 저장하고 새로고침한다. 이름·메시지를 넣고 **남기기**를 누를 때마다 목록에 한 줄씩 쌓이고 `1개`·`2개`·`3개`로 오른다. 첫 글을 남기면 `아직 남긴 글이 없습니다.`가 사라진다. 이름을 비우고 누르면 `이름을 입력하세요.`만 보이고 목록·개수는 그대로다.

### 12. 삭제 버튼 틀 붙이기

`showList` 안 `li.textContent = items[i];` 줄과 `list.append(li);` 줄 **사이**에 ex07의 일곱 줄을 그대로 옮겨 쓴다.

```js
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      showList();
    });
    li.append(removeButton);
```

- 이 일곱 줄은 **틀**이다. 뜯어보지 않고 그대로 쓴다. `showList()`가 다시 그릴 때 버튼마다 번호를 새로 붙인다.
- 누르면 `items.splice(i, 1);`로 배열에서 하나를 빼고 `showList();`로 다시 그린다. 개수와 안내 문장도 함께 다시 쓴다.
- `li.append(removeButton)`은 버튼을 그 **줄** 안에, `list.append(li)`는 그 줄을 **목록**에 붙인다. 붙이는 상자가 다르다.

**예상 결과** — 줄마다 **[삭제]** 가 생긴다. 글 세 개를 남기고 **가운데** 줄의 **[삭제]** 를 누르면 그 줄만 사라지고 위아래 두 줄과 `2개`가 남는다. 남은 두 줄도 지우면 `아직 남긴 글이 없습니다.`와 `0개`가 보인다.

### 13. guestbook.html 전문

8단계까지 마친 `guestbook.html` 전체다. 내 파일과 한 줄씩 비교한다. 9주차 파일과 다른 곳은 `<div id="notice"></div>` 아래 네 줄뿐이다.

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
      <h3>남긴 글</h3>
      <ul class="card" id="list"></ul>
      <div id="empty">아직 남긴 글이 없습니다.</div>
      <div id="count">0개</div>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

같은 파일이 [examples/day2/web-week10/guestbook.html](examples/day2/web-week10/guestbook.html)에 있다.

### 14. guestbook.js 전문

12단계까지 마친 `guestbook.js` 전체다. 교재 파일은 submit 안의 빈 줄을 뺐다. 내 파일에 빈 줄이 남아 있어도 동작은 같다.

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const empty = document.querySelector('#empty');
const count = document.querySelector('#count');
let items = [];

function clearNotice() {
  notice.textContent = '';
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      showList();
    });
    li.append(removeButton);
    list.append(li);
  }
  count.textContent = `${items.length}개`;
  if (items.length === 0) {
    empty.textContent = '아직 남긴 글이 없습니다.';
  } else {
    empty.textContent = '';
  }
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
  items.push(`${name}: ${message}`);
  showList();
  form.reset();
  nameInput.focus();
});

nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
showList();
```

같은 파일이 [examples/day2/web-week10/guestbook.js](examples/day2/web-week10/guestbook.js)에 있다.

- 5~8행은 목록·안내·개수 자리를 찾아 두고 빈 배열을 만든다(ex06, ex01).
- 14~34행 `showList`는 비우고(ex05) → 배열을 처음부터 끝까지(ex02) → 줄마다 만들고 **[삭제]** 를 붙인 뒤 목록에 붙이고(ex03, ex07) → 개수와 안내 문장을 쓴다(ex04, ex06).
- 51~52행은 배열에 넣고 다시 그린다. 59행은 열 때 한 번 그린다(ex06).
- 나머지는 9주차 그대로(7주차에 만든 폼 코드)다.

`index.html`·`about.html`·`app.js`·`styles.css`·`README.md`와 `images/`·`screenshots/`는 9주차 그대로다. 이번 주에 열지 않는다.

### 15. 375·1280 폭과 서버로 확인

DevTools의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)를 켜고 폭을 375와 1280으로 바꿔 가며 글 하나를 남기고 지워 본다.

**예상 결과** — 두 폭 모두 목록 줄과 **[삭제]** 가 보이고 개수가 맞는다. 375에서는 메뉴가 세로로 선다(4주차 `@media`).

이어서 서버로 연다. 현재 폴더: `web-week10`

```bash
node server.mjs
```

주소창에 `http://localhost:8000/guestbook.html`을 친다. 두 번 눌러 연 것과 결과가 같으면 된 것이다. 터미널에는 브라우저가 받아 간 파일마다 한 줄씩 찍힌다(`200 GET /guestbook.html`·`200 GET /guestbook.js`·`200 GET /styles.css`. `guestbook.js` 와 `styles.css` 줄의 순서는 바뀔 수 있다). `404 GET /favicon.ico` 줄과 Console의 `Failed to load resource: … 404 (Not Found)`(`favicon.ico`) 줄도 하나씩 보일 수 있는데 괜찮다. 탭 아이콘을 찾는 요청이다([서버 사용 안내](../../tools/static-server/README.md#터미널에-찍히는-줄-읽기) 참고). 확인이 끝나면 터미널에서 **Ctrl+C**로 서버를 멈춘다.
쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다. Node가 없는 PC는 `guestbook.html`을 두 번 눌러 연 것으로 대신한다.

### 16. push와 캡처

현재 폴더: `web-week10`

```bash
git add .
git commit -m "10주차 2일차"
git push
```

1~3분 뒤 `https://student01.github.io/web-week10/guestbook.html`을 연다. 이름·메시지를 바꿔 가며 글 세 개를 남기고 **가운데** 줄의 **[삭제]** 를 누른다.

**예상 결과** — 두 줄이 남고 줄마다 **[삭제]**, 목록 아래 `2개`가 보인다. 주소창이 함께 보이게 캡처한다. 이 캡처 한 장이 제출이다.
공용 PC라면 자격 증명을 지우고 나간다.

- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 캡처하기 전에 새로고침하면 목록이 비어 버린다. 글을 남긴 **그 화면**에서 바로 찍는다.
- 막히면 [실습지의 막혔을 때](lab.md#막혔을-때)를 본다.
