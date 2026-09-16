# 13주차 따라하기 — 페이지 점검하고 README 최종판 쓰기

처음에는 그대로 따라 하고, 결과가 나오면 본인 내용으로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 주소와 글자의 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

**이번 주에도 확인과 캡처는 공개 주소에서 한다.** 방명록에 남긴 글은 브라우저마다 따로 저장되고,
프로젝트 카드는 `file://`에서 읽히지 않는다. 고칠 때마다 push하고 공개 주소를 새로고침한다.

## 1일차

### 1. 저장소 열고 시작 루틴

VS Code **File › Open Folder**로 `my-web`을 열고 **Terminal › New Terminal**을 연다. 현재 폴더: `my-web`

```bash
git pull
git log --oneline
```

다른 PC에서 처음 시작한다면 `git pull` 대신 아래를 먼저 한다. 현재 폴더: 저장소를 둘 위치

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

**예상 결과** — `Already up to date.`가 나오거나 12주차에 push한 commit을 받아 온다.
탐색기에 `index.html`·`about.html`·`guestbook.html`·`projects.html`과 `app.js`·`guestbook.js`·`projects.js`·`styles.css`,
`data/` 폴더와 `images/` 폴더가 보인다. 이 여덟 파일이 오늘 점검할 대상이다.

### 2. about.html에 입학 연도 폼 넣기

1. `about.html`의 `<head>`에 스크립트 줄을 넣는다. `about.html`에 자기 `.js`를 붙이는 것은 이번이 처음이다.

```html
<script src="about.js" defer></script>
```

2. 표 아래에 제목 하나와 폼, 결과가 보일 자리를 넣는다.

```html
<h2>몇 년차일까요?</h2>
<form id="year-form">
  <p>
    <label for="year">입학 연도</label>
    <input id="year" type="text">
    <button type="submit">계산하기</button>
  </p>
</form>
<p class="card" id="year-result">입학 연도를 적고 계산하기를 누르세요.</p>
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day1/about.html](examples/day1/about.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
    <link rel="stylesheet" href="styles.css">
    <script src="about.js" defer></script>
  </head>
  <body>
    <header>
      <h1>내 정보</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
        <a href="projects.html">프로젝트</a>
      </nav>
    </header>
    <main>
      <h2>한눈에 보기</h2>
      <p>수업용 가상 정보입니다.</p>
      <table>
        <tr>
          <th>항목</th>
          <th>내용</th>
        </tr>
        <tr>
          <td>아이디</td>
          <td>student01</td>
        </tr>
        <tr>
          <td>이메일</td>
          <td>student01@example.com</td>
        </tr>
        <tr>
          <td>관심 분야</td>
          <td>웹 페이지 만들기</td>
        </tr>
      </table>
      <h2>몇 년차일까요?</h2>
      <form id="year-form">
        <p>
          <label for="year">입학 연도</label>
          <input id="year" type="text">
          <button type="submit">계산하기</button>
        </p>
      </form>
      <p class="card" id="year-result">입학 연도를 적고 계산하기를 누르세요.</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

**예상 결과** — 공개 주소 `/my-web/about.html`을 새로고침하면 표 아래에 **입학 연도** 칸과 **계산하기** 버튼,
그리고 `입학 연도를 적고 계산하기를 누르세요.`가 적힌 흰 상자가 보인다. 아직 버튼을 눌러도 아무 일도 일어나지 않는다.

- `label for="year"`의 `year`는 바로 아래 `input`의 `id`와 같아야 한다. **입학 연도** 글자를 눌렀을 때 입력 칸에 커서가 가면 맞게 연결된 것이다.
- `<script src="about.js" defer></script>`를 넣었는데 `about.js` 파일이 아직 없으면 Console에 빨간 줄이 하나 뜬다. 3단계에서 파일을 만들면 사라진다.

### 3. about.js로 몇 년차인지 계산하기

`about.js`를 새로 만들고 아래 내용을 넣는다. 같은 파일이 [examples/day1/about.js](examples/day1/about.js)에 있다.

```js
const yearForm = document.querySelector('#year-form');
const yearInput = document.querySelector('#year');
const yearResult = document.querySelector('#year-result');

yearForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const text = yearInput.value.trim();
  const year = Number(text);
  if (text === '' || isNaN(year)) {
    yearResult.textContent = '입학 연도를 숫자로 적어 주세요.';
    yearInput.focus();
    return;
  }
  const thisYear = new Date().getFullYear();
  const years = thisYear - year + 1;
  yearResult.textContent = `${year}년에 입학했으니 올해 ${years}년차입니다.`;
  yearInput.focus();
});
```

**예상 결과** — 입력 칸에 `2023`을 적고 **계산하기**를 누르면 아래 상자가
`2023년에 입학했으니 올해 4년차입니다.`로 바뀐다(올해가 2026년일 때).
`이천이십삼`처럼 숫자가 아닌 글자를 적고 누르면 `입학 연도를 숫자로 적어 주세요.`가 보이고 커서가 입력 칸으로 돌아간다.

- `Number('2023')`은 숫자 `2023`이 되고 `Number('이천이십삼')`은 `NaN`(숫자가 아님)이 된다. `NaN`인지 묻는 함수가 `isNaN()`이다.
- `new Date().getFullYear()`는 오늘 날짜의 연도만 꺼낸다. 2026년이면 `2026`이다.
- 7주차 방명록 폼과 순서가 같다: `preventDefault` → `value.trim()` → 빈칸·오류면 안내하고 `return` → 정상이면 화면에 쓰기.

### 4. 글자로 넣기와 HTML로 넣기 비교하기

이 두 파일은 강의자가 보여 주는 **시연용 예제**다. 내 `my-web` 폴더에는 넣지 않는다.
교재 저장소의 [examples/security-demo.html](examples/security-demo.html)을 내려받아 바탕화면 등 다른 폴더에서 열어 본다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>글자로 넣기와 HTML로 넣기</title>
    <script src="security-demo.js" defer></script>
  </head>
  <body>
    <main>
      <h1>글자로 넣기와 HTML로 넣기</h1>
      <p>입력 칸에는 b 태그로 감싼 글이 적혀 있습니다. 두 버튼을 차례로 눌러 결과를 비교합니다.</p>
      <p>
        <label for="input">입력</label>
        <input id="input" type="text">
      </p>
      <p>
        <button id="text-button" type="button">textContent로 넣기</button>
        <button id="html-button" type="button">innerHTML로 넣기</button>
      </p>
      <h2>결과</h2>
      <p id="output">아직 아무것도 넣지 않았습니다.</p>
      <h2>무엇이 다른가</h2>
      <ul>
        <li>textContent로 넣으면 적은 글자가 그대로 보입니다.</li>
        <li>innerHTML로 넣으면 태그가 HTML로 실행되어 굵은 글씨가 됩니다.</li>
        <li>다른 사람이 쓴 글을 innerHTML로 넣으면 그 사람이 적은 HTML이 내 페이지에서 실행됩니다.</li>
        <li>그래서 방명록은 textContent로 넣습니다. innerHTML은 목록을 비울 때만 씁니다.</li>
      </ul>
    </main>
  </body>
</html>
```

같은 폴더에 [examples/security-demo.js](examples/security-demo.js)를 함께 둔다.

```js
const input = document.querySelector('#input');
const output = document.querySelector('#output');
const textButton = document.querySelector('#text-button');
const htmlButton = document.querySelector('#html-button');

input.value = '<b>안녕</b>';

textButton.addEventListener('click', function () {
  output.textContent = input.value;
});

htmlButton.addEventListener('click', function () {
  output.innerHTML = input.value;
});
```

**예상 결과** — 입력 칸에 `<b>안녕</b>`이 적혀 있다.
**textContent로 넣기**를 누르면 결과 자리에 `<b>안녕</b>`이 **글자 그대로** 보이고,
**innerHTML로 넣기**를 누르면 같은 글이 **굵은 안녕**으로 바뀐다.

- 두 버튼의 차이는 한 단어뿐이다. `output.textContent = …`와 `output.innerHTML = …`.
- 내가 적은 글은 괜찮지만, 다른 사람이 적은 글을 `innerHTML`로 넣으면 그 사람이 적은 HTML이 내 페이지에서 실행된다.
- 그래서 입력한 글을 보여 줄 때는 `textContent`를 쓴다. `innerHTML`은 10주차처럼 **목록을 비울 때(`innerHTML = ''`)만** 쓴다.

### 5. 방명록에 `<b>안녕</b>` 남겨 보기

공개 주소 `/my-web/guestbook.html`을 열고 이름에 `student02`, 메시지에 `<b>안녕</b>`을 적어 **남기기**를 누른다.

**예상 결과** — 목록에 `student02: <b>안녕</b> (2026. 9. 16.)`이 **글자 그대로** 한 줄로 보인다. 굵은 글씨가 되지 않는다.

내 `guestbook.js`가 `textContent`를 쓰고 있어서 그렇다. 아래 파일을 열어 `li.textContent = …` 줄을 눈으로 확인한다.
같은 파일이 [examples/day1/guestbook.js](examples/day1/guestbook.js)에 있고, 이번 주에는 **고치지 않는다**.

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const count = document.querySelector('#count');
const clearButton = document.querySelector('#clear-button');
let items = JSON.parse(localStorage.getItem('guestbook')) || [];

function saveList() {
  localStorage.setItem('guestbook', JSON.stringify(items));
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      saveList();
      showList();
    });
    li.append(removeButton);
    list.append(li);
  }
  if (items.length === 0) {
    count.textContent = '아직 남긴 글이 없습니다.';
  } else {
    count.textContent = `${items.length}개`;
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    nameInput.focus();
    return;
  }
  notice.textContent = '';
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
  saveList();
  showList();
  form.reset();
  nameInput.focus();
});

clearButton.addEventListener('click', function () {
  items = [];
  localStorage.removeItem('guestbook');
  showList();
});

showList();
```

- 만약 목록 글자가 굵게 보인다면 그 줄이 `li.innerHTML = …`로 되어 있는 것이다. `textContent`로 바꾼다.
- 확인이 끝나면 **전체 지우기**를 눌러 목록을 비운다. 제출 캡처는 2일차 15단계에서 한 줄을 다시 남겨 찍는다.

### 6. 그림의 alt와 폼의 label 점검하기

네 페이지를 차례로 열어 두 가지만 본다. 고칠 곳이 없으면 그대로 두고 다음 단계로 간다.

| 페이지 | 볼 것 | 이번 주 상태 |
|---|---|---|
| `index.html` | `<img src="images/profile.png" alt="…">`에 `alt`가 있는가 | 3주차에 넣어 두었다. 그대로 둔다 |
| `about.html` | 입력 칸마다 `<label for="…">`가 있는가 | 2단계에서 넣은 `label for="year"`가 마지막 한 개다 |
| `guestbook.html` | 이름·이메일·메시지 세 칸에 `label for`가 있는가 | 3주차에 넣어 두었다. 그대로 둔다 |
| `projects.html` | 카드 그림의 `alt`와 링크 글자는 어디서 만들어지는가 | HTML이 아니라 `projects.js`에서 만든다. 7단계에서 고친다 |

**예상 결과** — 브라우저에서 **입학 연도**, **이름**, **이메일**, **메시지** 글자를 하나씩 눌러 본다.
누를 때마다 바로 옆 입력 칸에 커서가 생기면 `label for`가 모두 맞게 연결된 것이다.

- `alt`는 그림이 안 보일 때 대신 읽히는 글이다. 비워 두지 않는다.
- `for`의 값과 `input`의 `id`는 **글자가 같아야** 한다. `for="years"`처럼 한 글자만 달라도 연결이 끊긴다.

### 7. 카드 링크 글자 고치기 (`projects.js`)

`projects.js`의 `link.textContent = '페이지 열기';` 한 줄을 아래처럼 바꾼다.

```js
link.textContent = `${projects[i].title} 열기`;
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day1/projects.js](examples/day1/projects.js)에 있다.

```js
const projectList = document.querySelector('#project-list');
const notice = document.querySelector('#notice');

function showProjects(projects) {
  projectList.innerHTML = '';
  for (let i = 0; i < projects.length; i++) {
    const article = document.createElement('article');
    article.classList.add('card');
    const image = document.createElement('img');
    image.src = projects[i].image;
    image.alt = `${projects[i].title} 화면 그림`;
    image.width = 240;
    const title = document.createElement('h3');
    title.textContent = projects[i].title;
    const description = document.createElement('p');
    description.textContent = projects[i].description;
    const link = document.createElement('a');
    link.href = projects[i].link;
    link.textContent = `${projects[i].title} 열기`;
    article.append(image, title, description, link);
    projectList.append(article);
  }
}

async function loadProjects() {
  try {
    const response = await fetch('data/projects.json');
    if (!response.ok) {
      notice.textContent = '프로젝트를 불러오지 못했습니다.';
      return;
    }
    const projects = await response.json();
    notice.textContent = '';
    showProjects(projects);
  } catch (error) {
    notice.textContent = '프로젝트를 불러오지 못했습니다.';
  }
}

loadProjects();
```

**예상 결과** — 공개 주소 `/my-web/projects.html`을 새로고침하면 카드 세 장의 링크 글자가
`자기소개 페이지 열기`·`내 정보 표 열기`·`방명록 열기`로 서로 다르게 보인다.

- 12주차에는 세 장 모두 **페이지 열기**였다. 링크 글자만 읽어서는 어디로 가는지 알 수 없었다.
- 링크·버튼 글자는 **그것만 읽어도 어디로 가는지 알 수 있게** 적는다. `여기를 누르세요`는 쓰지 않는다.
- 템플릿 문자열 `` `${projects[i].title} 열기` ``는 5주차에 배운 모양이다. 따옴표가 아니라 백틱이다.

### 8. 링크·Console·375 점검하기

순서를 바꾸지 않고 위에서 아래로 한 번씩 한다.

1. 네 페이지의 nav 링크 네 개를 **모두 눌러 본다.** 404가 나오는 링크가 없어야 한다.
2. 각 페이지에서 **F12 › Console**을 열고 빨간 줄이 없는지 본다.
3. **F12 › 기기 모드**(왼쪽 위 휴대전화 아이콘)에서 폭을 **375**로 두고 네 페이지를 본다. 가로로 밀리는 곳이 없어야 한다.

**예상 결과** — nav가 세로로 접히고(4주차 `@media`), 입력 칸과 버튼이 줄을 바꿔 들어가며, 가로 스크롤 막대가 생기지 않는다.

- 404가 나오면 주소창의 파일 이름과 실제 파일 이름의 **철자·대소문자**를 맞춘다. 공개 주소는 대소문자를 구분한다.
- Console의 빨간 줄은 끝의 `파일 (줄 번호)`부터 읽는다. 5주차부터 하던 것과 같다.
- `styles.css`는 이번 주에 고치지 않는다. 375에서 깨지는 곳이 있으면 먼저 강의자에게 보여 준다.

### 9. push하고 공개 주소에서 캡처하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "방명록 글자 확인하고 alt·label 고치기"
git push
```

**예상 결과** — 1분쯤 뒤 공개 주소가 바뀐다. 기기 모드 **375**로 `/my-web/guestbook.html`을 열고
이름 `student02`, 메시지 `<b>안녕</b>`으로 한 줄을 남긴다. 목록에 `<b>안녕</b>`이 글자 그대로 보이고
**F12 › Console**에 빨간 줄이 없으면 오늘 몫은 끝났다. 그 화면을 **확인용 캡처**로 한 장 저장한다.

1. 주소창이 함께 보이게 찍는다.
2. 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 제거한다.
3. 제출 캡처는 내일 끝에 같은 화면을 다시 찍는다(15단계).

## 2일차

### 10. 화면 캡처 세 장 넣기

공개 주소에서 세 화면을 찍어 `screenshots/` 폴더에 넣는다. 파일 이름은 소문자로 둔다.

| 파일 | 찍을 화면 |
|---|---|
| `screenshots/home.png` | `/my-web/` — 인사말과 클릭 횟수, 소개, 취미 |
| `screenshots/guestbook.png` | `/my-web/guestbook.html` — 남긴 글 목록과 개수 |
| `screenshots/projects.png` | `/my-web/projects.html` — 카드 세 장 |

**예상 결과** — 9주차에 만든 `screenshots/` 폴더에 파일 세 개가 있다. 9주차에 찍은 두 장은 nav가 세 페이지였으므로 **새로 찍어 덮어쓴다**.

- 캡처에 실명·학번·전화번호·실제 이메일이 보이지 않게 한다.
- 파일 이름에 한글·공백·대문자를 쓰지 않는다. 대문자로 저장하면 README에서 그림이 깨진다(11단계).

### 11. README.md 최종판 쓰기

저장소의 `README.md`를 아래 순서로 다시 쓴다. 9주차에 쓴 1차판을 지우고 새로 쓰는 것이다.

```text
# my-web — student01의 웹 연습장   사이트 이름 한 줄
## 공개 주소                       Pages 주소를 링크로 한 줄
## 페이지                          네 페이지를 링크 목록으로 네 줄
## 기능                            다섯 줄
## 화면                            캡처 세 장을 그림으로 세 줄
## 사용 기술                       HTML·CSS·JavaScript·GitHub Pages 네 줄
## 어려움과 해결                   세 줄
## 만든 과정                       git log --oneline 다섯 줄
```

전체 예시(51줄)는 [examples/day2/README.md](examples/day2/README.md)에 있다. GitHub 파일 화면의 **Raw**를 눌러 그대로 복사한 뒤
`student01`과 주소, 화면 설명을 본인 것으로 바꾼다. 쓰는 마크다운은 네 가지뿐이다.

```text
# 제목                                            제목. #과 글자 사이를 한 칸 띄운다
- 항목                                            목록 한 줄
[공개 주소](https://student01.github.io/my-web/)  링크. 소괄호 안이 주소다
!                                                 링크 앞에 느낌표를 붙이면 그림
```

**예상 결과** — VS Code에서 `README.md`를 열고 오른쪽 위 **Open Preview**(돋보기 아이콘)를 누르면
제목·목록·링크·그림이 들어간 문서로 보인다. 그림 세 장이 모두 나와야 한다.

- 소괄호 안에는 인터넷 주소도 넣고, 같은 저장소 안의 파일이면 `index.html`이나 `screenshots/home.png`처럼 **파일 이름만** 넣는다.
- 그림 줄은 링크 앞에 `!`를 붙인 것이다. `!`가 없으면 그림 대신 파란 링크가 된다.
- `#` 뒤에는 **띄어쓰기 한 칸**이 있어야 한다. `#제목`은 그냥 글자로 보인다.
- 마지막 절의 일곱 글자(`8f31c4a` 등)는 12단계의 `git log --oneline`에서 본인 것을 옮겨 적는다.

### 12. commit 기록을 README에 붙이기

현재 폴더: `my-web`

```bash
git log --oneline
```

**예상 결과** — 지금까지 한 commit이 한 줄씩 보인다. 맨 위가 가장 최근이다.

```text
8f31c4a 방명록 글자 확인하고 alt·label 고치기
5c0b7e2 프로젝트 카드 안내 문장 넣기
2a94d16 projects.json 불러와 카드 그리기
7e12b05 방명록을 localStorage에 저장하기
4d6a893 방명록 목록 추가·삭제 만들기
```

위 다섯 줄을 README 마지막 절에 `- `를 붙여 옮겨 적는다. 앞의 일곱 글자는 PC마다 다르므로 **본인 화면의 값**을 쓴다.

- 줄이 다섯 줄보다 많으면 최근 다섯 줄만 적는다.
- `q`를 눌러 목록에서 빠져나온다.

### 13. 저장소 첫 화면에서 README 확인하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "README 최종판과 캡처 3장 넣기"
git push
```

**예상 결과** — GitHub 저장소 화면 `https://github.com/student01/my-web`을 새로고침하면
파일 목록 **아래**에 README가 문서로 보인다. 제목이 크게 나오고 그림 세 장이 보인다.

- 그림 자리에 깨진 아이콘이 보이면 `screenshots/` 안 파일 이름과 README에 적은 이름의 **대소문자**를 맞춘다.
- 그림 파일을 `git add .`로 함께 올렸는지 본다. 저장소 화면에서 `screenshots` 폴더를 눌러 세 파일이 있는지 확인한다.
- README의 링크(`index.html` 등)는 저장소 화면에서는 파일로, 공개 주소에서는 페이지로 열린다.

### 14. Pages 주소가 만들어지는 두 가지 방식 보기

실습은 없다. **Settings › Pages › Build and deployment**를 열어 지금 설정만 확인한다.

| 방식 | Source | 우리 수업 |
|---|---|---|
| `main` · `/(root)` | Deploy from a branch | **수업 표준**. 2주차부터 이 방식이다 |
| `gh-pages` 브랜치 | Deploy from a branch | `gh-pages`라는 브랜치를 따로 만들어 그 안의 파일만 공개한다. 2주차 부록에서 한 줄로 본 방식이다 |

**예상 결과** — Branch가 `main`, 폴더가 `/(root)`로 되어 있고 위쪽에 `Your site is live at …`가 보인다. 아무것도 바꾸지 않는다.

- 두 방식 모두 결과는 같은 공개 주소다. 어느 브랜치의 파일을 공개할지만 다르다.
- 바꾸면 공개 주소가 1~10분 동안 404가 될 수 있다. 14주차 발표 전에는 건드리지 않는다.

### 15. 제출 캡처 찍고 마무리하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "README 문구 다듬기"
git push
```

고친 곳이 없으면 `nothing to commit, working tree clean`이 나온다. 그대로 다음으로 넘어간다.
공개 주소 `/my-web/guestbook.html`을 **F12 › 기기 모드 375px**로 열고, 목록이 비어 있으면
이름 `student02`, 메시지 `<b>안녕</b>`으로 한 줄을 다시 남긴다.

**예상 결과** — 목록에 `<b>안녕</b>`이 **글자 그대로** 보이고 **F12 › Console**에 빨간 줄이 없다.
이 화면이 **이번 주 제출 캡처**다.

1. 주소창이 함께 보이게 찍는다.
2. 캡처에 실명·학번·전화번호·실제 이메일이 보이지 않게 한다.
3. 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 제거한다.

## 이번 주에 고치지 않는 파일

아래 여섯 파일은 12주차와 같다. 내 파일이 예제와 다르면 여기서 한 줄씩 비교한다.

`index.html`:

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <header>
      <h1>student01의 웹 연습장</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
        <a href="projects.html">프로젝트</a>
      </nav>
    </header>
    <main>
      <p class="card" id="greeting">인사말을 준비 중입니다.</p>
      <p>
        <button id="hello-button" type="button">인사 바꾸기</button>
        <button id="dark-button" type="button">다크 모드</button>
      </p>
      <p class="card" id="count">클릭 0회</p>
      <h2>소개</h2>
      <img src="images/profile.png" alt="student01의 프로필 그림" width="160">
      <p class="card">웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p class="card">이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
      <h2>취미</h2>
      <ul class="card">
        <li>사진 찍기</li>
        <li>보드게임</li>
        <li>저녁 산책</li>
      </ul>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`guestbook.html`:

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
        <a href="projects.html">프로젝트</a>
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
      <p id="notice"></p>
      <h3>남긴 글</h3>
      <ul class="card" id="list"></ul>
      <p id="count">아직 남긴 글이 없습니다.</p>
      <p><button id="clear-button" type="button">전체 지우기</button></p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`projects.html`:

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 프로젝트</title>
    <link rel="stylesheet" href="styles.css">
    <script src="projects.js" defer></script>
  </head>
  <body>
    <header>
      <h1>프로젝트</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
        <a href="projects.html">프로젝트</a>
      </nav>
    </header>
    <main>
      <h2>지금까지 만든 것</h2>
      <p>아래 카드는 data/projects.json 파일에서 읽어 옵니다.</p>
      <p id="notice"></p>
      <div id="project-list"></div>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`app.js`:

```js
const name = 'student01';
const hour = new Date().getHours();
const greeting = document.querySelector('#greeting');
const countBox = document.querySelector('#count');
const helloButton = document.querySelector('#hello-button');
const darkButton = document.querySelector('#dark-button');
let count = 0;

function greet(name) {
  return `안녕하세요, ${name}님!`;
}

function hello(hour) {
  if (hour >= 12) {
    return '좋은 오후입니다.';
  } else {
    return '좋은 아침입니다.';
  }
}

function countUp() {
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
}

greeting.textContent = `${greet(name)} ${hello(hour)}`;

helloButton.addEventListener('click', function () {
  greeting.textContent = '반갑습니다. 오늘도 좋은 하루 되세요.';
  countUp();
});

darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
  countUp();
});
```

`data/projects.json`:

```json
[
  {
    "title": "자기소개 페이지",
    "description": "홈 화면입니다. 이름과 소개, 취미 목록을 적었습니다.",
    "image": "images/project1.png",
    "link": "index.html"
  },
  {
    "title": "내 정보 표",
    "description": "아이디와 이메일, 관심 분야를 표로 정리했습니다.",
    "image": "images/project2.png",
    "link": "about.html"
  },
  {
    "title": "방명록",
    "description": "이름과 메시지를 남기면 목록에 저장되는 페이지입니다.",
    "image": "images/project3.png",
    "link": "guestbook.html"
  }
]
```

`styles.css`:

```css
body {
  background-color: #eef2ff;
  color: #17213a;
  font-family: system-ui, sans-serif;
  font-size: 16px;
  max-width: 640px;
  margin: 0 auto;
  padding: 16px;
}

h1 {
  color: #1f3a93;
  font-size: 28px;
}

h2 {
  color: #3157d5;
}

nav {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

nav a {
  color: #3157d5;
}

.card {
  background-color: #ffffff;
  padding: 16px;
  margin: 12px 0;
  border: 1px solid #c3cbe6;
}

input,
textarea {
  width: 280px;
  max-width: 100%;
}

footer {
  color: #5a6478;
  text-align: center;
  font-size: 14px;
}

@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}

body.dark,
body.dark .card {
  background-color: #222222;
  color: #eeeeee;
}
```

## 오류가 나면

먼저 **F12 › Console**의 첫 빨간 줄과 그 끝의 `파일 (줄 번호)`를 읽는다.
자주 나오는 문구와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 새로고침하고, 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 요청한다.
