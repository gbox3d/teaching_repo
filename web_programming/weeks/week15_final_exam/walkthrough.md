# 15주차 따라하기 — 기말 실기 리허설과 제출

처음에는 그대로 따라 하고, 결과가 나오면 본인 아이디와 문구로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

1일차는 시험과 **같은 형태의 리허설**이다(점수에 들어가지 않는다). 2일차는 본시험 절차다.
확인의 기준은 **공개 주소**다. `localStorage`와 `fetch`는 `file://`로 열면 결과가 달라진다.

## 1일차

### 1. 시험용 저장소 web-final 만들기

`my-web`은 그대로 두고 **새 저장소**를 만든다. 시험 당일에는 이 절차를 하지 않는다.

1. github.com에서 **+ › New repository**
2. Repository name: `web-final` · **Public**
3. **Add a README file**, .gitignore, license는 모두 **끄기**
4. **Create repository**

현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-final.git
cd web-final
```

**예상 결과**

```text
Cloning into 'web-final'...
warning: You appear to have cloned an empty repository.
done.
```

- `warning:`으로 시작하지만 오류가 아니다. 빈 저장소를 받았다는 뜻이다.
- **File › Open Folder**로 `web-final` 폴더를 연다. 그다음 **Terminal › New Terminal**을 다시 연다.
- `fatal: destination path 'web-final' already exists and is not an empty directory.`가 나오면 그 폴더를 열고 다음 단계로 간다.

### 2. starter 네 파일 넣기

탐색기의 **New File**로 파일 세 개를 만들고, `data` 폴더를 만들어 그 안에 `items.json`을 만든다.
네 파일 모두 [examples/rehearsal_starter](examples/rehearsal_starter)에 있다. 내용을 고치지 않고 그대로 넣는다.

`index.html` — 같은 파일이 [examples/rehearsal_starter/index.html](examples/rehearsal_starter/index.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>web-final · 읽은 책 기록</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <header>
      <h1>읽은 책 기록</h1>
      <button id="mode-button" type="button">다크 모드</button>
    </header>
    <main>
      <h2>한 권 남기기</h2>
      <form id="book-form">
        <label for="title">제목</label>
        <input id="title" type="text">
        <button type="submit">추가</button>
      </form>
      <p id="notice"></p>
      <ul id="book-list"></ul>
      <h2>추천 목록</h2>
      <p id="load-status">불러오는 중…</p>
      <ul id="recommend-list"></ul>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`styles.css` — 같은 파일이 [examples/rehearsal_starter/styles.css](examples/rehearsal_starter/styles.css)에 있다.

```css
body {
  margin: 0;
  font-family: system-ui, sans-serif;
  color: #17213a;
  background: #eef2ff;
}

body.dark {
  color: #eeeeee;
  background: #222222;
}

header {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
}

main {
  max-width: 40rem;
  margin: 0 auto;
  padding: 0 1rem 2rem;
}

form {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

button {
  padding: 0.5rem 1rem;
  border: 0;
  border-radius: 0.5rem;
  color: white;
  background: #3157d5;
}

li {
  margin-bottom: 0.5rem;
}

#notice {
  color: #c02b2b;
}

@media (max-width: 600px) {
  form {
    flex-direction: column;
    align-items: stretch;
  }
}
```

`app.js` — 같은 파일이 [examples/rehearsal_starter/app.js](examples/rehearsal_starter/app.js)에 있다. TODO 네 자리가 오늘 할 일이다.

```js
const form = document.querySelector('#book-form');
const titleInput = document.querySelector('#title');
const notice = document.querySelector('#notice');
const list = document.querySelector('#book-list');
const modeButton = document.querySelector('#mode-button');
const loadStatus = document.querySelector('#load-status');
const recommendList = document.querySelector('#recommend-list');

// TODO 3: 페이지를 열 때 'final-items'에 저장해 둔 목록을 복원한다.
let books = [];

function saveList() {
  // TODO 3: books를 'final-items' 키로 localStorage에 저장한다.
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < books.length; i++) {
    const row = document.createElement('li');
    row.textContent = `${books[i].title} (${books[i].date})`;
    // TODO 2: 이 줄을 지우는 [지우기] 버튼을 만들어 row에 붙인다.
    list.append(row);
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  // TODO 1: 제목이 비었으면 notice에 '제목을 입력하세요'를 쓰고 멈춘다.
  // TODO 1: 비지 않았으면 books에 { title, date }를 넣고 showList()·saveList()를 부른다.
});

modeButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
});

async function loadRecommend() {
  // TODO 4: data/items.json을 불러와 recommendList에 li로 그린다.
  // TODO 4: 실패하면 loadStatus에 '불러오지 못했습니다.'를 쓴다.
}

showList();
loadRecommend();
```

`data/items.json` — 같은 파일이 [examples/rehearsal_starter/data/items.json](examples/rehearsal_starter/data/items.json)에 있다.

```json
[
  {
    "title": "처음 만나는 웹",
    "comment": "HTML과 CSS를 그림으로 설명한다."
  },
  {
    "title": "브라우저는 어떻게 동작하나",
    "comment": "주소를 넣으면 무슨 일이 생기는지 따라간다."
  },
  {
    "title": "작은 자바스크립트",
    "comment": "버튼 하나로 시작하는 연습이 많다."
  }
]
```

**예상 결과** — `index.html`을 더블클릭하면 제목과 폼, `추천 목록`, `불러오는 중…`이 보인다.
**[다크 모드]** 버튼을 누르면 배경이 어두워진다. **[추가]**를 눌러도 아무 일이 없다. 여기까지가 정상이다.

- 폴더 구조는 `web-final/index.html`, `web-final/styles.css`, `web-final/app.js`, `web-final/data/items.json`이다.
- `data` 폴더 이름과 `items.json` 파일 이름을 한 글자도 바꾸지 않는다. `app.js`가 이 이름으로 부른다.

### 3. 첫 push와 Pages 켜기

현재 폴더: `web-final`

```bash
git add .
git commit -m "기말 실기 리허설 시작"
git push -u origin main
```

**예상 결과**

```text
[main (root-commit) dd80e4c] 기말 실기 리허설 시작
 4 files changed, 142 insertions(+)
 create mode 100644 app.js
 create mode 100644 data/items.json
 create mode 100644 index.html
 create mode 100644 styles.css
```

```text
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

이어서 **Settings › Pages › Build and deployment**에서 Source **Deploy from a branch**, Branch **main** · **/(root)** · **Save**.

**예상 결과** — 1분쯤 뒤 새로고침하면 "Your site is live at `https://student01.github.io/web-final/`"가 보인다. **Visit site**로 연다.

- 앞의 `dd80e4c`는 예시다. commit 번호는 PC마다 다르다.
- 여기까지가 **시험 전날 끝내야 하는 준비**다. 시험 당일에는 저장소 만들기도 Pages 켜기도 하지 않는다.

### 4. TODO 1 — 폼으로 한 권 추가하기

`app.js`의 `form.addEventListener('submit', …)` 안에 있는 주석 두 줄을 지우고 아래를 넣는다.

```js
  const title = titleInput.value.trim();
  if (title === '') {
    notice.textContent = '제목을 입력하세요';
    titleInput.focus();
    return;
  }
  notice.textContent = '';
  books.push({ title: title, date: new Date().toLocaleDateString() });
  showList();
  saveList();
  form.reset();
  titleInput.focus();
```

**예상 결과** — 제목에 `처음 만나는 웹`을 넣고 **[추가]**를 누르면 아래에 `처음 만나는 웹 (2026. 9. 16.)` 한 줄이 생긴다.
빈 칸인 채로 누르면 빨간 글씨 `제목을 입력하세요`가 나오고 커서가 입력 칸으로 돌아간다.

- `trim()`은 공백만 넣은 경우도 빈값으로 본다. 7주차와 같다.
- `saveList()`는 아직 비어 있어 아무 일도 하지 않는다. 6단계에서 채운다.
- `Uncaught TypeError: Cannot read properties of null` 오류가 나면 `index.html`의 `id` 철자를 본다.

### 5. TODO 2 — 지우기 버튼 붙이기

`showList()`의 `for` 안, TODO 2 주석 자리에 아래 여덟 줄을 넣는다. 10주차에 쓴 틀과 같다.

```js
    const removeButton = document.createElement('button');
    removeButton.textContent = '지우기';
    removeButton.addEventListener('click', function () {
      books.splice(i, 1);
      showList();
      saveList();
    });
    row.append(removeButton);
```

**예상 결과** — 줄마다 오른쪽에 **[지우기]** 버튼이 생기고, 누르면 그 줄만 사라진다.

- `showList()`가 다시 그릴 때 버튼마다 번호를 새로 붙인다. 그래서 가운데 줄을 지워도 번호가 밀리지 않는다.
- 버튼을 눌러도 목록이 그대로면 `splice` 뒤에 `showList()`를 부르지 않은 것이다.

### 6. TODO 3 — localStorage로 남기기

두 줄이 짝이다. 먼저 `let books = [];` 줄을 아래로 바꾼다(TODO 3 주석은 지운다).

```js
let books = JSON.parse(localStorage.getItem('final-items')) || [];
```

그리고 `saveList()` 안의 주석을 지우고 한 줄을 넣는다.

```js
function saveList() {
  localStorage.setItem('final-items', JSON.stringify(books));
}
```

**예상 결과** — 두 권을 넣고 **공개 주소에서** 새로고침해도 두 줄이 그대로 있다.
DevTools **Application › Local Storage**에서 키 `final-items`와 값 `[{"title":"…","date":"…"}]`이 보인다.

- **확인은 공개 주소에서 한다.** `file://`로 연 화면과 공개 주소는 저장소가 서로 달라서, 로컬에서 넣은 항목은 공개 페이지에 나타나지 않는다.
- 키 이름은 `final-items`다. `my-web`의 `guestbook`과 다른 이름이어야 두 페이지의 목록이 섞이지 않는다.

### 7. TODO 4 — 추천 목록 불러오기

`loadRecommend()` 안의 주석 두 줄을 지우고 아래를 넣는다.

```js
  try {
    const response = await fetch('data/items.json');
    if (!response.ok) {
      loadStatus.textContent = '불러오지 못했습니다.';
      return;
    }
    const data = await response.json();
    for (let i = 0; i < data.length; i++) {
      const row = document.createElement('li');
      row.textContent = `${data[i].title} — ${data[i].comment}`;
      recommendList.append(row);
    }
    loadStatus.textContent = `추천 ${data.length}권`;
  } catch (error) {
    loadStatus.textContent = '불러오지 못했습니다.';
  }
```

여기까지 하면 `app.js` 전체가 아래와 같다. 같은 파일이 [examples/rehearsal_solution/app.js](examples/rehearsal_solution/app.js)에 있다.

```js
const form = document.querySelector('#book-form');
const titleInput = document.querySelector('#title');
const notice = document.querySelector('#notice');
const list = document.querySelector('#book-list');
const modeButton = document.querySelector('#mode-button');
const loadStatus = document.querySelector('#load-status');
const recommendList = document.querySelector('#recommend-list');

let books = JSON.parse(localStorage.getItem('final-items')) || [];

function saveList() {
  localStorage.setItem('final-items', JSON.stringify(books));
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < books.length; i++) {
    const row = document.createElement('li');
    row.textContent = `${books[i].title} (${books[i].date})`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '지우기';
    removeButton.addEventListener('click', function () {
      books.splice(i, 1);
      showList();
      saveList();
    });
    row.append(removeButton);
    list.append(row);
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const title = titleInput.value.trim();
  if (title === '') {
    notice.textContent = '제목을 입력하세요';
    titleInput.focus();
    return;
  }
  notice.textContent = '';
  books.push({ title: title, date: new Date().toLocaleDateString() });
  showList();
  saveList();
  form.reset();
  titleInput.focus();
});

modeButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
});

async function loadRecommend() {
  try {
    const response = await fetch('data/items.json');
    if (!response.ok) {
      loadStatus.textContent = '불러오지 못했습니다.';
      return;
    }
    const data = await response.json();
    for (let i = 0; i < data.length; i++) {
      const row = document.createElement('li');
      row.textContent = `${data[i].title} — ${data[i].comment}`;
      recommendList.append(row);
    }
    loadStatus.textContent = `추천 ${data.length}권`;
  } catch (error) {
    loadStatus.textContent = '불러오지 못했습니다.';
  }
}

showList();
loadRecommend();
```

**예상 결과** — 공개 주소에서 `불러오는 중…`이 `추천 3권`으로 바뀌고 아래에 책 세 줄이 보인다.
`data/items.json`을 `data/item.json`으로 바꿔 보면 `불러오지 못했습니다.`가 나오고 위쪽 목록은 그대로 동작한다. 확인한 뒤 이름을 되돌린다.

- `if (!response.ok)`는 파일을 못 찾았을 때(404) 안내 문구를 쓰고 `return`으로 멈춘다. 그 밖의 실패는 아래 `catch`가 받는다.
- 경로는 `'data/items.json'`처럼 **상대 경로**로 쓴다. `'/data/items.json'`로 쓰면 공개 주소에서 404가 난다.
- `file://`로 열면 추천 목록이 항상 `불러오지 못했습니다.`가 된다. 오류가 아니라 브라우저가 막는 것이다. 공개 주소에서 본다.

### 8. 1일차 끝 루틴

현재 폴더: `web-final`

```bash
git add .
git commit -m "리허설 TODO 네 개 채우기"
git push
```

1. 1분쯤 뒤 `https://student01.github.io/web-final/`을 새로고침하고 네 기능을 차례로 눌러 본다.
2. 화면을 캡처한다(확인용. 제출은 내일 한 장이다).
3. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 공개 주소가 옛 화면이면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- `git status`에 `Your branch is ahead of 'origin/main' by 1 commit.`이 있으면 push를 안 한 것이다.

## 2일차

### 9. 본시험 시작 전 3분

어제 쓰던 PC라 `web-final` 폴더가 그대로 있으면 그 폴더를 열고 `git pull`을 한다.
폴더가 없는 PC면 어제 만든 저장소를 다시 받는다. 저장소와 Pages는 어제 그대로 살아 있다.

현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-final.git
cd web-final
```

**File › Open Folder**로 `web-final`을 열고 **Terminal › New Terminal**을 다시 연다.
그다음 감독이 나눠 준 시험 파일 네 개를 `web-final` 폴더에 **덮어쓴다**. 폴더와 파일 이름은 어제와 같다.

현재 폴더: `web-final`

```bash
git status
```

**예상 결과**

```text
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   app.js
	modified:   data/items.json
	modified:   index.html
```

1. `index.html`을 브라우저로 한 번 열어 화면이 뜨고 Console 오류가 0인지 본다.
2. 문항을 끝까지 읽고 어느 TODO 자리를 고치는지 표시한다.

- 바뀐 파일 수는 문항에 따라 다르다. 네 파일 중 몇 개가 `modified:`로 보이면 정상이다.
- 어제 리허설은 commit으로 남아 있다. 덮어써도 사라지지 않는다.
- 여기서 오류가 나면 **구현을 시작하기 전에** 손을 든다.
- Pages는 어제 켜 두었다. 다시 켜지 않는다.

### 10. 60분 동안의 순서

| 시간 | 할 일 |
|---|---|
| 0–5분 | 문항 읽기·starter 실행 확인 |
| 5–15분 | HTML·CSS 문항 |
| 15–35분 | 폼·목록 추가·삭제 |
| 35–45분 | localStorage |
| 45–52분 | fetch·오류 안내 |
| 52–57분 | push와 제출 |
| 57–60분 | 예비(Pages 반영 대기) |

- 한 문항에서 막히면 다음 문항으로 넘어간다. 문항끼리 서로 막지 않는다.
- 한 번에 한 곳만 고치고 브라우저에서 확인한다. 여러 곳을 동시에 고치면 어디가 원인인지 알 수 없다.
- 중간에 한 번 `git add .` → `git commit`을 해 두면 마지막에 급하지 않다.

### 11. 마지막 5분 — push와 제출 세 가지

현재 폴더: `web-final`

```bash
git add .
git commit -m "기말 실기 제출"
git push
git log -1 --format=%H
```

**예상 결과** — 40자짜리 commit 번호 한 줄이 나온다.

```text
dd80e4cede6c4a6a4b527634d7319a8ce6561761
```

1. 공개 주소를 새로고침해 방금 고친 내용이 보이는지 확인한다. **여기 보이는 것이 제출본이다.**
2. 주소창이 함께 보이게 캡처 1장을 찍는다.
3. 공개 주소·저장소 주소·commit 번호 세 가지와 캡처를 제출한다.
4. 공용 PC면 자격 증명을 지우고 나간다.

- 공개 주소가 5분 넘게 옛 화면이면 손을 들어 시각을 기록받고, 로컬 화면 캡처와 commit 번호로 제출한다.
- commit 번호는 `git log --oneline` 첫 줄의 짧은 번호가 아니라 위 명령의 40자를 적는다.
