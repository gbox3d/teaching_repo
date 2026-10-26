[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud)

# 12주차 따라하기 — 비교 예제로 원리를 보고 마지막에 조립

이번 주는 새 저장소 `web-week12`를 만든다. 지난주 완성본과 `server.mjs`를 넣고, 비교 예제는 그 안의 `ex/` 폴더에 저장한다. 값·줄을 바꾼 뒤 결과를 화면과 **F12 › Console**, **F12 › Network**에서 본다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.
**이번 주 예제는 서버로 연다.** `fetch`는 두 번 눌러 연 화면(`file://`)에서 막힌다. 작업 중에는 `node server.mjs`로 띄운 `http://localhost:8000/`에서 보고, 확인과 캡처는 공개 주소에서 한다.

비교 예제 6개는 교재 저장소의 [examples/day1](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud/examples/day1)(1일차 ex01~ex03과 고르기 페이지)과 [examples/day2](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud/examples/day2)(2일차 ex04~ex06) 폴더에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다.

## 1일차

### 1. web-week12 폴더 만들고 지난주 완성본 넣기

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-week12`를 만들고 VS Code **File › Open Folder**로 연다.

지난주 완성본을 넣는다. 내 `web-week11` 저장소 GitHub 화면에서 **Code › Download ZIP**을 누르고, 압축을 푼 폴더에서 맨 위 파일(`index.html`·`about.html`·`guestbook.html`·`styles.css`·`app.js`·`guestbook.js`·`README.md`·`server.mjs`)과 `images/`·`screenshots/`를 `web-week12`로 옮긴다. 지난주 `ex/` 폴더는 옮기지 않는다.
ZIP을 못 받았으면 교재 [11주차 `examples/day2/web-week11/`](../week11_auth_rls/examples/day2/web-week11/)의 파일을 2단계와 같은 **Raw** 방법으로 받고, [server.mjs](../../tools/static-server/server.mjs)도 같은 방법으로 받는다.

이어서 `web-week12` 안에 `ex` 폴더를 만든다. 현재 폴더: `web-week12`

```bash
mkdir ex
```

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week12/
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

- 11주차 완성 사이트(홈·내 정보·방명록 세 페이지)가 그대로 있다. 이번 주는 여기서 시작한다.
- 맨 위 파일은 오늘 건드리지 않는다. 2일차 끝에 `data/`·`projects.html`·`projects.js`를 더하고 nav에 한 줄씩 넣는다.

### 2. 비교 예제 가져오기

오늘 파일은 여섯 개다. 고르기 페이지 `index.html` 하나, 예제 코드 `.js` 세 개, ex02·ex03이 읽어 오는 `.json` 두 개다. 세 예제가 같은 화면(글자 자리 하나)을 쓰기 때문에 화면은 `index.html` 하나에 두고 코드만 따로 뗐다.

| 파일 | 비교하는 것 |
|---|---|
| [index.html](examples/day1/index.html) | 고르기 페이지. 맨 아래 `<script src>` 세 줄 중 하나만 켠다. 예제가 쓰는 자리(`#result`)가 여기 있다 |
| [ex01_json_rule.js](examples/day1/ex01_json_rule.js) | JSON 글자: 큰따옴표 / 작은따옴표 / 마지막 쉼표 |
| [ex02_fetch.js](examples/day1/ex02_fetch.js) · [ex02_projects.json](examples/day1/ex02_projects.json) | `await fetch`의 응답 / `await response.json()`의 배열 |
| [ex03_file_http.js](examples/day1/ex03_file_http.js) · [ex03_projects.json](examples/day1/ex03_projects.json) | 서버 주소로 연 페이지 / 두 번 눌러 연 페이지 |

[교재 저장소 examples/day1 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud/examples/day1)에서 파일을 누르고 오른쪽 위 **Raw**를 누른다. 글자만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `web-week12/ex/`에 저장한다. 파일 이름은 교재와 **같게** 둔다. Raw가 열리지 않을 때만 주석 줄까지 그대로 친다.

**예상 결과** — `ex/` 안에 파일 여섯 개가 있다.

```text
ex/
  ex01_json_rule.js
  ex02_fetch.js
  ex02_projects.json
  ex03_file_http.js
  ex03_projects.json
  index.html
```

- 저장한 파일 이름이 `.txt`로 끝나면 이름을 고친다. 이름은 VS Code 탐색기에서 확인한다.
- `ex/index.html`은 예제를 고르는 페이지다. 맨 위 `index.html`(내 사이트)과 이름이 같지만 다른 파일이다. 탭 이름 옆 폴더 경로로 구분한다.

### 3. 서버로 열기와 Network 탭

이번 주 예제는 서버로 연다. 터미널(**Terminal › New Terminal**)을 열고 친다. 현재 폴더: `web-week12`

```bash
node server.mjs
```

**예상 결과** — 터미널에 두 줄이 찍히고 서버가 떠 있다. 폴더 줄은 PC마다 다르다.

```text
폴더: C:\Users\student\web-week12
주소: http://localhost:8000/   (멈추기: Ctrl+C)
```

Chrome 주소창에 `http://localhost:8000/ex/`를 친다. `ex/` 폴더의 `index.html`(고르기 페이지)이 열린다. VS Code에서 `ex/index.html`도 열어 맨 아래를 본다.

```html
<script src="ex01_json_rule.js"></script>
<!-- <script src="ex02_fetch.js"></script> -->
<!-- <script src="ex03_file_http.js"></script> -->
```

지금은 ex01 줄만 켜져 있다. 다른 예제로 바꿀 때는 켜 둔 줄에 커서를 두고 **Ctrl+/**(macOS **⌘+/**)로 주석으로 만들고, 볼 줄에서 다시 **Ctrl+/** 로 주석을 푼다. 저장 → 새로고침한다. 한 번에 한 줄만 켠다.

**예상 결과** — 화면의 "예제가 쓰는 자리"가 `1. 2개 — 첫 제목은 자기소개 페이지`다. F12 › **Console**에 `1. 큰따옴표 :`로 시작하는 줄이 하나 있고, 앞의 ▶를 누르면 객체 두 개가 펼쳐진다. 서버 터미널에는 `200 GET /ex/` 같은 요청 줄이 늘어 있다.
서버로 열면 Console에 `favicon.ico` 404 빨간 줄이, 터미널에 `404 GET /favicon.ico` 줄이 하나 섞일 때가 있다. 브라우저가 탭 아이콘을 찾으려고 스스로 보낸 요청이라 괜찮다(5주차).

이번 주에는 **Network** 탭도 쓴다. DevTools 위쪽 탭에서 **Network**를 누르고, 연 채로 새로고침한다. Network는 열어 둔 뒤에 오간 요청만 적는다.
이제 `ex/index.html`에서 ex01 줄을 끄고 `ex02_fetch.js` 줄을 켠 뒤 저장 → 새로고침한다.

**예상 결과** — 화면이 `2. 3개를 불러왔다 — 첫 제목은 3주차 자기소개`로 바뀐다. Network 목록에 이 페이지가 받은 파일이 한 줄씩 생긴다. 페이지 자체, `ex02_fetch.js`, `ex02_projects.json`이다. `ex02_projects.json` 줄의 **Status**는 `200`, **Type**은 `fetch`다.

- `ex02_projects.json` 줄이 `fetch`가 요청한 파일이다. Status **200**은 "찾아서 보냈다"이다. 2일차 제출 캡처에 이 줄(`projects.json` 200)이 들어간다.
- 줄을 누르고 오른쪽 **Response** 탭을 열면 받은 글자가 보인다. `ex02_projects.json` 파일의 글자와 같다.
- 위쪽 **Fetch/XHR** 단추를 누르면 `fetch`가 보낸 요청만 남는다. 다시 **All**을 누르면 모두 보인다.
- 서버 터미널에도 같은 요청이 한 줄씩 찍힌다(`200 GET /ex/ex02_projects.json`). Network는 브라우저 쪽에서, 터미널은 서버 쪽에서 본 같은 요청이다.

### 4. 값 바꾸는 요령

실험은 늘 같은 순서다. **VS Code에서 고치고 저장**(Ctrl+S, macOS는 ⌘+S) → **브라우저에서 새로고침**(F5, macOS는 ⌘+R) → **화면·Console·Network**를 본다. 서버는 띄운 채로 둔다. 파일을 고쳐도 서버를 다시 띄울 필요가 없다.
바꾸기 전에 무엇이 달라질지 먼저 말해 보고 확인한다.

**두 번 눌러 열어 보기** — `ex/index.html` 맨 아래에서 `ex03_file_http.js` 줄만 켜고 저장한다. 먼저 서버 주소 `http://localhost:8000/ex/`를 새로고침한다. 이어서 VS Code 탐색기에서 `ex/index.html`을 오른쪽 클릭 › **Reveal in File Explorer**(macOS는 **Reveal in Finder**) → 두 번 눌러 연다.

**예상 결과** — 서버 주소 탭은 `3. 2개를 불러왔다`다. 두 번 눌러 연 탭은 주소창이 `file:///`로 시작하고, 화면이 `1. 불러오는 중 — …`에서 멈춰 있다. Console에 빨간 줄이 있다.

```text
Access to fetch at 'file:///…/ex/ex03_projects.json' from origin 'null' has been blocked by CORS policy: …
Failed to load resource: net::ERR_FAILED
Uncaught (in promise) TypeError: Failed to fetch
```

같은 파일인데 주소만 다르다. `file://`로 연 페이지에서는 브라우저가 `fetch`를 막는다. 그래서 `fetch` 줄 아래(3번)가 실행되지 않았다.
가운데 줄은 요청이 실패했다는 브라우저의 줄이다. 이 탭에서 F12를 연 채 새로고침하면 같은 줄이 `GET file:///…/ex/ex03_projects.json net::ERR_FAILED` 모양으로 바뀐다. 세 줄의 표기는 Chrome 버전에 따라 조금 다를 수 있다.

- 값을 원래대로 못 돌리겠으면 교재에서 그 파일을 다시 **Raw**로 받아 덮어쓴다.
- 서버 터미널을 닫거나 **Ctrl+C**를 누르면 서버가 멈춘다. 그때 `http://localhost:8000/`은 `사이트에 연결할 수 없음`이다. 다시 `node server.mjs`로 띄운다.
- 파일마다 무엇을 바꿔 볼지는 [1일차 실습](lab.md#1일차--json-파일과-fetch-60분)에 있다.

### 5. 이번 주 저장소 만들어 올리기

1일차 50–60분에 한다. 세 예제에서 각각 값 하나 이상을 바꿔 봤으면 올린다.

GitHub에서 **New repository**를 누르고 이름 `web-week12`, **Public**으로 만든다. README는 추가하지 않는다.
서버가 떠 있는 터미널은 그대로 두고 **Terminal › New Terminal**로 터미널을 하나 더 연다. 2주차에 배운 순서 그대로 친다. 현재 폴더: `web-week12`

```bash
git init
git add .
git commit -m "12주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week12.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save**를 누른다.

**예상 결과** — GitHub 저장소 화면을 새로고침하면 `ex/`·`images/`·`screenshots/`와 맨 위 파일들이 보인다.
1~3분 뒤 `https://student01.github.io/web-week12/ex/`를 연다. 고르기 페이지의 제목과 "예제가 쓰는 자리"가 보인다. 켜 둔 줄이 ex02면 공개 주소에서도 `ex02_projects.json`을 읽어 와 화면이 2번 글자가 된다(공개 주소는 `https://`라 `fetch`가 된다). 이 화면은 **확인용**이다.
공용 PC라면 서버를 **Ctrl+C**로 멈추고, **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 404가 나면 주소의 `web-week12/ex/`가 저장소·폴더 이름과 글자 단위로 같은지, Pages를 켰는지 본다.
- push가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../week02_github_pages/lab.md#막혔을-때)를 본다.

## 2일차

### 6. 폴더 열고 2일차 예제 아홉 파일 가져오기

같은 PC에 `web-week12` 폴더가 남아 있으면 VS Code로 그대로 연다. 없으면 받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week12.git
```

내려받은 `web-week12`를 **File › Open Folder**로 연다. 터미널(현재 폴더 `web-week12`)에서 `node server.mjs`를 띄운다.

오늘 예제는 세 개이고, 예제마다 `.html`과 `.js`가 한 쌍이다. 예제가 읽는 그림 하나와 `.json` 두 개를 더해 파일은 아홉 개다. 오늘 예제는 화면이 서로 달라서 `.html`을 따로 둔다. [교재 저장소 examples/day2 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud/examples/day2)에서 1일차와 같은 **Raw** → 저장으로 `web-week12/ex/`에 넣는다. 그림 파일도 **Raw**를 누르면 그림만 열린다. 그 화면에서 **Ctrl+S**로 저장한다.

| 파일 | 비교하는 것 |
|---|---|
| [ex04_cards.html](examples/day2/ex04_cards.html) + [ex04_cards.js](examples/day2/ex04_cards.js) · [ex04_picture.png](examples/day2/ex04_picture.png) | 카드 한 장 안의 그림(`img`) / 제목(`h3`) / 설명(`p`) / 링크(`a`) |
| [ex05_try_catch.html](examples/day2/ex05_try_catch.html) + [ex05_try_catch.js](examples/day2/ex05_try_catch.js) · [ex05_projects.json](examples/day2/ex05_projects.json) | `try`를 끝까지 / `catch`로 넘어감 |
| [ex06_response_ok.html](examples/day2/ex06_response_ok.html) + [ex06_response_ok.js](examples/day2/ex06_response_ok.js) · [ex06_projects.json](examples/day2/ex06_projects.json) | 있는 파일(200) / 없는 파일(404)과 `response.ok` |

**예상 결과** — `ex/`에 파일이 열다섯 개 있다(1일차 여섯 + 오늘 아홉).
`http://localhost:8000/ex/ex04_cards.html`을 열면 노란 카드 세 장에 `카드 그림`·제목·설명·`교재 열기`가 차례로 보인다.

- 오늘은 `.html`을 연다. `.js`·그림·`.json`은 같은 폴더에서 `.html`이 불러온다. 하나를 빠뜨리면 그 부분이 동작하지 않는다.
- ex04는 `fetch`가 없어서 두 번 눌러 열어도 된다. ex05·ex06은 서버 주소로 연다. ex05는 두 번 눌러서도 한 번 열어 본다.
- 파일마다 무엇을 바꿔 볼지는 [2일차 실습](lab.md#2일차--카드와-오류-안내-그리고-조립-60분)에 있다.

### 7. 조립표

28분부터 조립한다. 이제 `ex/`가 아니라 `web-week12` 맨 위에서 만든다.
조립하는 줄은 모두 비교 예제와 11주차 완성본에서 본 것이다.

| 조립할 줄 | 출처 |
|---|---|
| `data/projects.json` — 객체 세 개, 이름표 `title`·`description`·`image`·`link` | [ex01](examples/day1/ex01_json_rule.js) 큰따옴표 규칙, [ex02](examples/day1/ex02_projects.json) 파일 모양, [ex04](examples/day2/ex04_cards.js) 이름표 |
| `projects.html`의 head·header·footer | 11주차 완성본 `guestbook.html` |
| `<h2>지금까지 만든 것</h2>` · 안내 문장 `<p>` | 11주차 `guestbook.html`의 `<h2>` 제목 줄과 같은 모양(글자만 새로) |
| `<div id="notice"></div>` · `<div id="project-list"></div>` | [ex05](examples/day2/ex05_try_catch.html)·[ex06](examples/day2/ex06_response_ok.html) 안내 자리, [ex04](examples/day2/ex04_cards.html) 카드 상자 |
| `const projectList`·`const notice` | [ex04](examples/day2/ex04_cards.js), [ex05](examples/day2/ex05_try_catch.js) |
| `function showProjects(projects) { … }` | [ex04](examples/day2/ex04_cards.js) |
| `async function loadProjects() { try { … } catch (error) { … } }` | [ex02](examples/day1/ex02_fetch.js) + [ex05](examples/day2/ex05_try_catch.js) |
| `await fetch('data/projects.json')` · `await response.json()` | [ex02](examples/day1/ex02_fetch.js) 1·2번 |
| `if (!response.ok) { …; return; }` · `notice.textContent = '';` | [ex06](examples/day2/ex06_response_ok.js) |
| `showProjects(projects);` | [ex04](examples/day2/ex04_cards.js) 받은 배열을 넘긴다 |
| `loadProjects();` | [ex02](examples/day1/ex02_fetch.js) |
| nav의 `<a href="projects.html">프로젝트</a>` | 11주차 nav 링크와 같은 모양 |

옮겨 적을 때 출처 ex 파일을 옆에 열어 두고, 같은 줄이 거기서 무엇을 했는지 떠올린다.

### 8. data 폴더와 projects.json 만들기

탐색기에서 `web-week12` 맨 위에 **New Folder**로 `data`를 만들고, 그 안에 **New File**로 `projects.json`을 만든다. 아래 전문을 넣는다.

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

같은 파일이 [examples/day2/web-week12/data/projects.json](examples/day2/web-week12/data/projects.json)에 있다.

**예상 결과** — 저장했을 때 VS Code가 빨간 밑줄을 긋지 않는다.

- 대괄호 `[ ]` 안에 중괄호 `{ }` 객체 세 개를 쉼표로 잇는다. 마지막 객체 뒤에는 쉼표가 없다(ex01 3번).
- 이름표와 문자열 값은 모두 **큰따옴표**다(ex01 1번). 제목·설명은 본인 내용으로 바꿔도 된다. 이름표 네 개(`title`·`description`·`image`·`link`)는 그대로 둔다. `projects.js`가 이 이름으로 꺼내기 때문이다.
- `image`와 `link`의 값은 `projects.html`이 있는 폴더에서 본 **상대 경로**다. `link`는 이미 있는 세 페이지 이름이다.

### 9. 카드 그림 세 장 넣기

교재 [examples/day2/web-week12/images/](examples/day2/web-week12/images/)에서 [project1.png](examples/day2/web-week12/images/project1.png)·[project2.png](examples/day2/web-week12/images/project2.png)·[project3.png](examples/day2/web-week12/images/project3.png)를 **Raw** → 저장으로 `web-week12/images/`에 넣는다. 본인 페이지를 캡처해 같은 이름으로 저장해도 된다.

**예상 결과** — 탐색기의 `images/` 안에 `profile.png`까지 그림 네 장이 보인다.

- 파일 이름의 대소문자를 `data/projects.json`의 `image` 값과 똑같이 맞춘다. 공개 주소는 대소문자가 다르면 그림을 찾지 못한다.

### 10. projects.html 만들기

탐색기에서 `projects.html`을 새로 만들고 아래 전문을 넣는다. 11주차 `guestbook.html`과 뼈대가 같다. 다른 것은 `<title>`, `<script src="projects.js" defer>`, `<h1>`, `<main>` 안, nav의 네 번째 링크다.

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
      <div id="notice"></div>
      <div id="project-list"></div>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

같은 파일이 [examples/day2/web-week12/projects.html](examples/day2/web-week12/projects.html)에 있다.

- `<p>` 한 줄은 읽는 사람에게 하는 실제 문장이다. JS가 채우는 두 자리는 `<div>`다.
- `<div id="notice"></div>`는 안내 문구 자리다(ex05·ex06). 비어 있으면 화면에 보이지 않는다.
- `<div id="project-list"></div>`는 카드를 담을 빈 상자다(ex04). 10주차 `<ul id="list">` 자리와 같은 역할이고, 목록이 아니라 카드를 넣으므로 `div`다.

**예상 결과** — 아직 `projects.js`가 없으므로 `http://localhost:8000/projects.html`을 열면 제목 `프로젝트`·`지금까지 만든 것`과 안내 문장만 보인다. 서버 터미널에 `404 GET /projects.js` 줄이 찍히고, Console에도 `projects.js`를 찾지 못한 404 빨간 줄이 하나 있다. DevTools를 연 채 새로고침하면 `GET http://localhost:8000/projects.js net::ERR_ABORTED 404 (Not Found)` 모양, 나중에 열면 `Failed to load resource: … 404 (Not Found)` 모양이다(Chrome 버전에 따라 표기가 조금 다를 수 있다). 다음 단계에서 파일을 만들면 사라진다.

### 11. projects.js 쓰기

탐색기에서 `projects.js`를 새로 만들고 조립표 순서로 쓴다.

1. 찾아 두기 두 줄 — `#project-list`와 `#notice`를 `querySelector`로 찾아 `const`에 담는다(ex04·ex05).
2. 카드 그리기 `showProjects(projects)` — ex04의 함수를 그대로 옮긴다. 그림 너비는 `240`, 대체 글은 `` `${projects[i].title} 화면 그림` ``, 링크 글자는 `페이지 열기`로 쓴다.
3. 불러오기 `async function loadProjects()` — 안쪽 전체를 `try { } catch (error) { }`로 감싼다(ex05).
4. `try` 안: `await fetch('data/projects.json')`(ex02 1번) → `if (!response.ok) { …; return; }`(ex06) → `await response.json()`(ex02 2번) → `notice.textContent = '';`(ex06) → `showProjects(projects);`(ex04).
5. `catch` 안: 안내 문장 `프로젝트를 불러오지 못했습니다.`(ex05 2번). `!response.ok` 쪽과 같은 문장이다.
6. 마지막 줄 `loadProjects();`(ex02).

**예상 결과** — 저장하고 `http://localhost:8000/projects.html`을 새로고침한다. 카드 세 장에 그림·제목·설명·**페이지 열기**가 차례로 보인다. Console에 `Uncaught` 빨간 줄이 없다(`favicon.ico` 404 한 줄은 탭 아이콘 요청이라 괜찮다).

### 12. projects.js 전문

내 파일과 한 줄씩 비교한다. 글자 단위로 같아야 한다.

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

같은 파일이 [examples/day2/web-week12/projects.js](examples/day2/web-week12/projects.js)에 있다.

- 4~23행 `showProjects`는 ex04와 같은 순서다. 비우기 → `for` → 카드 하나에 `img`·`h3`·`p`·`a` → `append`.
- 27행 경로 `data/projects.json`은 `/`로 시작하지 않는다. 공개 주소의 내 파일은 `/web-week12/` 아래에 있다.
- 28~31행은 404일 때 안내를 쓰고 끝낸다(ex06). 35~37행은 `try` 안에서 오류가 났을 때(요청이 막혔거나 받은 글자를 JSON으로 읽지 못했을 때) 안내를 쓴다(ex05). 두 문장이 같다.
- 33행은 안내 자리를 비운다. 앞에서 안내가 남아 있었다면 지운다(ex06).
- 40행이 없으면 아무 일도 일어나지 않는다(ex02).

### 13. nav에 프로젝트 링크 넣기

`index.html`·`about.html`·`guestbook.html`을 차례로 열어 nav의 `<a href="guestbook.html">방명록</a>` 줄 **바로 아래**에 한 줄을 넣는다.

```html
        <a href="projects.html">프로젝트</a>
```

세 파일의 전문은 아래와 같다. 11주차 파일에서 늘어난 것은 nav의 이 한 줄뿐이다.

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
      <div class="card" id="greeting">인사말을 준비 중입니다.</div>
      <div>
        <button id="hello-button" type="button">인사 바꾸기</button>
        <button id="dark-button" type="button">다크 모드</button>
      </div>
      <div class="card" id="count">클릭 0회</div>
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
      <div id="notice"></div>
      <h3>남긴 글</h3>
      <ul class="card" id="list"></ul>
      <div id="count">아직 남긴 글이 없습니다.</div>
      <div><button id="clear-button" type="button">전체 지우기</button></div>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

같은 파일이 [index.html](examples/day2/web-week12/index.html) · [about.html](examples/day2/web-week12/about.html) · [guestbook.html](examples/day2/web-week12/guestbook.html)에 있다.

**예상 결과** — 네 페이지 어디에서나 nav에 `홈 · 내 정보 · 방명록 · 프로젝트` 네 링크가 보이고 서로 오갈 수 있다.

### 14. 서버 주소와 Network로 확인

서버가 떠 있는지 본다. 멈춰 있으면 현재 폴더 `web-week12`에서 `node server.mjs`를 띄운다. `http://localhost:8000/projects.html`을 열고 **F12 › Network**를 연 채 새로고침한다.

**예상 결과** — 카드 세 장이 보이고 Network의 `projects.json` 줄이 **200**, Type이 `fetch`다. 그림 세 장(`project1.png`~`project3.png`)도 200이다. Console에 `Uncaught` 빨간 줄이 없다(`favicon.ico` 404 한 줄은 괜찮다).

이어서 안내 문구를 확인한다. 탐색기에서 `data/projects.json`의 이름을 잠깐 `project.json`으로 바꾸고 새로고침한다.

**예상 결과** — 카드 대신 `프로젝트를 불러오지 못했습니다.`가 보인다. Network의 `projects.json`은 **404**다. Console에는 그 요청의 404 빨간 줄(연 채 새로고침하면 `GET http://localhost:8000/data/projects.json 404 (Not Found)` 모양. Chrome 버전에 따라 표기가 조금 다를 수 있다)이 있고 `Uncaught` 줄은 없다. 확인했으면 이름을 **반드시** `projects.json`으로 되돌리고 새로고침해 카드가 돌아오는지 본다.

- nav의 네 링크와 카드의 **페이지 열기** 세 개를 모두 눌러 본다. 404가 없으면 된 것이다.
- 서버 사용법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.

### 15. 375·1280 폭으로 확인

DevTools의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)를 켜고 폭을 375와 1280으로 바꿔 가며 `projects.html`을 본다.

**예상 결과** — 두 폭 모두 카드 세 장이 위아래로 쌓인다. 375에서는 메뉴가 세로로 서고(4주차 `@media`), 카드 그림이 화면 밖으로 넘치지 않는다.
확인이 끝나면 서버 터미널에서 **Ctrl+C**로 서버를 멈춘다.

### 16. push와 캡처

현재 폴더: `web-week12`

```bash
git add .
git commit -m "12주차 2일차"
git push
```

1~3분 뒤 `https://student01.github.io/web-week12/projects.html`을 연다. **F12 › Network**를 연 채 새로고침한다.

**예상 결과** — 카드 세 장이 보이고 Network의 `projects.json`이 **200**이다. 카드와 Network 탭, 주소창이 함께 보이게 캡처한다. 이 캡처 한 장이 제출이다.
공용 PC라면 자격 증명을 지우고 나간다.

- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 공개 주소에서만 그림이 깨지면 `image` 값과 그림 파일 이름의 대소문자를 맞춘다.
- 막히면 [실습지의 막혔을 때](lab.md#막혔을-때)를 본다.
