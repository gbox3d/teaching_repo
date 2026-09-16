# 12주차 따라하기 — JSON 파일을 읽어 카드로 그리기

처음에는 그대로 따라 하고, 결과가 나오면 본인 내용으로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 주소와 글자의 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

**이번 주 확인은 공개 주소에서 한다.** 파일을 더블클릭해서 연 화면(`file://`)에서는 `fetch`가 막혀 카드가 보이지 않는다.
이것은 고장이 아니라 브라우저의 규칙이며, 6단계에서 그 화면을 일부러 한 번 본다.

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

**예상 결과** — `Already up to date.`가 나오거나 11주차에 push한 commit을 받아 온다.
탐색기에 `index.html`·`about.html`·`guestbook.html`·`app.js`·`guestbook.js`·`styles.css`와 `images/` 폴더가 보인다.

### 2. data 폴더와 projects.json 만들기

1. 탐색기의 **New Folder** 아이콘으로 폴더 `data`를 만든다.
2. `data` 폴더 안에 **New File**로 `projects.json`을 만들고 아래 내용을 넣는다.

같은 파일이 [examples/day1/data/projects.json](examples/day1/data/projects.json)에 있다.

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

**예상 결과** — 저장했을 때 VS Code가 빨간 밑줄을 긋지 않는다.
빨간 밑줄이 보이면 큰따옴표(`"`)가 아닌 작은따옴표를 썼거나, 마지막 항목 뒤에 쉼표가 남아 있는 것이다.

- 이름(`"title"`)과 문자열 값에는 **큰따옴표만** 쓴다. JSON에는 작은따옴표가 없다.
- `link`의 값은 우리가 이미 만든 페이지 파일 이름이다. 카드에서 그 페이지로 가는 링크가 된다.
- 제목·설명은 본인 내용으로 바꿔도 된다. 다만 **이름표(`title`·`description`·`image`·`link`)는 그대로** 둔다.

### 3. 카드 그림 세 장 넣기

`images/` 폴더에 `project1.png`·`project2.png`·`project3.png` 세 장을 넣는다.
[examples/day1/images/project1.png](examples/day1/images/project1.png) · [project2.png](examples/day1/images/project2.png) · [project3.png](examples/day1/images/project3.png)를 내려받아 써도 되고,
본인 페이지를 캡처해 같은 이름으로 저장해도 된다.

**예상 결과** — 탐색기의 `images/` 안에 `profile.png`까지 네 장이 보인다.
파일 이름의 대소문자가 `data/projects.json`에 적은 것과 같아야 한다. 공개 주소에서는 대소문자가 다르면 그림이 나오지 않는다.

### 4. projects.html 만들기

탐색기에서 `projects.html`을 새로 만들고 아래 내용을 넣는다. 같은 파일이 [examples/day1/projects.html](examples/day1/projects.html)에 있다.

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
      </nav>
    </header>
    <main>
      <h2>지금까지 만든 것</h2>
      <p>아래 카드는 data/projects.json 파일에서 읽어 옵니다.</p>
      <div id="project-list"></div>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

**예상 결과** — 아직 `projects.js`가 없으므로 페이지를 열면 제목 `프로젝트`와 안내 문장만 보이고 카드 자리는 비어 있다.
nav는 아직 세 링크다. 네 번째 링크는 12단계에서 넣는다.

- `<div id="project-list"></div>`는 카드를 담아 둘 **빈 상자**다. 10주차 `<ul id="list">` 자리와 같은 역할이고, 목록이 아니라 카드를 넣으므로 `div`를 쓴다.

### 5. projects.js로 JSON 불러오기

탐색기에서 `projects.js`를 새로 만들고 아래 내용을 넣는다. 같은 파일이 [examples/day1/projects.js](examples/day1/projects.js)에 있다.

```js
const projectList = document.querySelector('#project-list');

function showProjects(projects) {
  projectList.innerHTML = '';
  for (let i = 0; i < projects.length; i++) {
    const article = document.createElement('article');
    article.classList.add('card');
    const title = document.createElement('h3');
    title.textContent = projects[i].title;
    const description = document.createElement('p');
    description.textContent = projects[i].description;
    article.append(title, description);
    projectList.append(article);
  }
}

async function loadProjects() {
  const response = await fetch('data/projects.json');
  const projects = await response.json();
  console.log(projects);
  showProjects(projects);
}

loadProjects();
```

**예상 결과** — 저장하면 VS Code에 오류 표시가 없다. 화면 확인은 다음 두 단계에서 한다.

- 위쪽 `showProjects(projects)`는 10주차 `showList()`와 같은 순서다. 비우기 → 고전 `for` → 만들어 붙이기.
- 아래쪽 `loadProjects()`가 이번 주의 새 틀이다. `async`와 `await`는 짝으로 쓴다.
- 마지막 줄 `loadProjects();`가 있어야 페이지를 열 때 한 번 실행된다.

### 6. file://로 열어 Console 보기

탐색기에서 `projects.html`을 오른쪽 클릭 → **Reveal in File Explorer**(macOS는 **Reveal in Finder**) → 더블클릭해서 연다.
**F12**로 개발자 도구를 열고 **Console** 탭을 본다.

**예상 결과** — 카드가 하나도 보이지 않고 Console에 빨간 줄 두 개가 있다.

```text
Access to fetch at 'file:///…/my-web/data/projects.json' from origin 'null' has been blocked by CORS policy: Cross origin requests are only supported for protocol schemes: chrome, chrome-extension, chrome-untrusted, data, http, https, isolated-app.

Uncaught (in promise) TypeError: Failed to fetch          projects.js:18
```

- 주소창이 `file://`로 시작하는 화면에서는 `fetch`가 막힌다. 코드가 틀린 것이 아니다.
- 오른쪽 끝 `projects.js:18`은 **파일 이름과 줄 번호**다. 18행이 `await fetch(...)` 줄이다.
- 로컬에서 미리 보고 싶으면 VS Code 확장 **Live Server**를 설치하고 상태줄 **Go Live**를 누른다(주소가 `http://127.0.0.1:5500/`으로 바뀐다).
  확장 설치가 막히면 터미널에서 `python3 -m http.server 8000`을 실행하고 `http://127.0.0.1:8000/projects.html`을 연다.
  둘 다 없으면 그대로 7단계로 가서 공개 주소에서 확인한다.

### 7. push하고 공개 주소에서 확인하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "프로젝트 페이지와 projects.json 추가"
git push
```

**예상 결과** — push 뒤 1분쯤 기다렸다가 `https://student01.github.io/my-web/projects.html`을 연다.
카드 3장에 제목과 설명이 보인다. **F12 › Console**에는 `console.log(projects)`가 찍은 배열이 한 줄로 보이고, 펼치면 `title`·`description`·`image`·`link`가 들어 있다.

- **F12 › Network** 탭을 열고 새로고침하면 `projects.json`이 **Status 200**으로 보인다. 이 화면이 2일차 제출 캡처에 들어간다.
- 카드가 보이지 않으면 Console의 첫 빨간 줄을 읽는다. 자주 나오는 문구는 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
- 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 제거하고 자리를 정리한다.

## 2일차

### 8. 안내 문구 자리 만들기

`projects.html`에 두 줄을 더한다. nav에 `<a href="projects.html">프로젝트</a>`, 안내 문장 아래에 `<p id="notice"></p>`다.
전체 파일은 아래와 같다. 같은 파일이 [examples/day2/projects.html](examples/day2/projects.html)에 있다.

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

**예상 결과** — 화면은 아직 그대로다. `<p id="notice"></p>`는 안이 비어 있어서 보이지 않는다.
9단계부터 이 자리에 안내 문장이 들어간다.

### 9. try / catch로 오류 받기

`projects.js` 맨 위에 안내 문구 자리를 한 줄 추가한다.

```js
const notice = document.querySelector('#notice');
```

`loadProjects()`의 안쪽을 `try { } catch (error) { }`로 감싼다.

```js
async function loadProjects() {
  try {
    const response = await fetch('data/projects.json');
    const projects = await response.json();
    notice.textContent = '';
    showProjects(projects);
  } catch (error) {
    notice.textContent = '프로젝트를 불러오지 못했습니다.';
  }
}
```

**예상 결과** — 이 상태로 `projects.html`을 더블클릭해서 열면(`file://`) 화면에 `프로젝트를 불러오지 못했습니다.`가 보인다.
6단계에서 보았던 `Uncaught (in promise) TypeError: Failed to fetch` 줄은 사라지고 CORS 안내 줄만 남는다.
`try` 안에서 난 오류를 `catch`가 받았기 때문이다.

### 10. response.ok로 404 거르기

`await fetch(...)` 바로 아래에 세 줄을 넣는다.

```js
if (!response.ok) {
  notice.textContent = '프로젝트를 불러오지 못했습니다.';
  return;
}
```

**예상 결과** — 확인해 보려면 `data/projects.json`의 이름을 잠깐 `project.json`으로 바꾸고 공개 주소(또는 Live Server)에서 새로고침한다.
화면에 `프로젝트를 불러오지 못했습니다.`가 보이고 **Network** 탭의 `projects.json`은 **404**다. 확인했으면 파일 이름을 되돌린다.

- 이 세 줄이 없으면 Console에 `Uncaught (in promise) SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON`이 난다.
  파일이 없을 때 서버가 HTML로 된 404 페이지를 보내는데, `response.json()`이 그 HTML을 읽다가 나는 오류다.
- 경로를 `/data/projects.json`처럼 `/`로 시작하게 쓰면 공개 주소에서 404가 난다. 공개 주소는 `/my-web/` 아래에 있기 때문이다. `data/projects.json`으로 쓴다.

### 11. 카드에 그림과 링크 넣기

`showProjects`의 `for` 안에 `img`와 `a`를 만들어 넣고, `append`의 순서를 바꾼다.
전체 파일은 아래와 같다. 같은 파일이 [examples/day2/projects.js](examples/day2/projects.js)에 있다.

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
    link.textContent = '페이지 열기';
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

**예상 결과** — 카드 한 장에 그림 → 제목 → 설명 → **페이지 열기** 링크가 차례로 들어간다.
`append(image, title, description, link)`에 넣은 순서대로 쌓이므로 순서를 바꾸면 화면도 바뀐다.

- 그림이 깨져 보이면 `data/projects.json`의 `image` 값과 `images/` 안의 파일 이름을 비교한다.
- `페이지 열기`를 눌렀을 때 404가 나면 `link` 값의 파일 이름을 본다.
- `styles.css`는 고치지 않는다. `article.classList.add('card')` 한 줄로 4주차의 `.card` 모양을 그대로 쓴다.

### 12. nav에 프로젝트 링크 넣기

`index.html`·`about.html`·`guestbook.html`의 nav에 `<a href="projects.html">프로젝트</a>` 한 줄씩을 넣어 네 페이지의 nav를 같게 만든다.
전체 파일은 아래와 같다. 같은 파일이 [examples/day2/index.html](examples/day2/index.html) · [about.html](examples/day2/about.html) · [guestbook.html](examples/day2/guestbook.html)에 있다.

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

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
    <link rel="stylesheet" href="styles.css">
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
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

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

**예상 결과** — 네 페이지 어디에서나 nav에 `홈 · 내 정보 · 방명록 · 프로젝트` 네 링크가 보이고 서로 오갈 수 있다.

### 13. 공개 주소에서 확인하고 캡처하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "카드에 그림과 링크 넣고 오류 안내 추가"
git push
```

**예상 결과** — 1분쯤 뒤 `https://student01.github.io/my-web/projects.html`을 새로고침하면
그림·제목·설명·**페이지 열기**가 있는 카드 3장이 보인다.

1. **F12 › Network** 탭을 열고 새로고침한다. `projects.json`의 **Status**가 **200**이다.
2. 카드 3장과 Network 탭이 함께 보이게, 주소창을 포함해 **캡처 1장**을 찍는다. 이 캡처가 이번 주 제출물이다.
3. 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 제거한다.

- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 5분이 지나도 반영되지 않으면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 함께 제출한다.

## 이번 주에 고치지 않는 파일

아래 여섯 파일은 11주차와 같다. 내 파일이 예제와 다르면 여기서 비교한다.
`index.html`·`about.html`·`guestbook.html`은 12단계에서 nav 한 줄만 늘어난다.
예제 폴더에는 이 여섯 파일 말고 `README.md`·`screenshots/`·`images/profile.png`도 11주차 그대로 들어 있다. 저장소 `README.md`와 `screenshots/`는 13주차 최종판에서 다시 쓴다.

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

`about.html`:

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <header>
      <h1>내 정보</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
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

`guestbook.js`:

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

먼저 **F12 › Console**의 첫 빨간 줄과 그 끝의 `파일 이름:줄 번호`를 읽는다.
자주 나오는 문구와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 새로고침하고, 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 요청한다.
