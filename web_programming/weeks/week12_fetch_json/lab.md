[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud)

# 12주차 실습 — 값을 바꿔 보고 마지막에 조립하기

이번 주 실습도 코드를 새로 쓰는 것이 아니라 **값을 바꿔 보는 것**이다.
비교 예제 6개를 이번 주 새 저장소 `web-week12` 의 `ex/` 폴더에 저장하고(1일차는 고르기 페이지 `index.html` 하나와 `.js` 세 개·`.json` 두 개, 2일차는 `.html`·`.js` 세 쌍과 그림 하나·`.json` 두 개), 값이나 줄 하나를 바꾼 뒤 결과가 어떻게 달라지는지 본다.
**확인과 캡처는 공개 주소에서 한다.** `fetch` 는 두 번 눌러 연 화면(`file://`)에서 막힌다. 작업 중에는 저장소 맨 위에서 `node server.mjs` 로 띄운 `http://localhost:8000/` 에서 본다.
결과는 화면, **F12 › Console**, 그리고 이번 주에 처음 쓰는 **F12 › Network** 에서 본다. DevTools 는 실습 내내 열어 둔다.
2일차 끝에 그 부품으로 `web-week12` 에 `data/projects.json`·`projects.html`·`projects.js` 를 만들고 네 페이지의 nav 를 맞춘다. 나머지 파일은 지난주 완성본 그대로다. 채점 대상은 2일차 캡처 1장이다.
`student01` 은 예시 아이디이므로 본인 아이디로 바꾼다.

파일을 받는 법, 서버로 여는 법, Network 탭 보는 법은 [따라하기 1일차](walkthrough.md#1일차)에 있다.
"바꿔 보기"는 **무엇이 달라질지 먼저 말해 보고** 저장 → 새로고침으로 확인한다. 확인했으면 원래대로 되돌리고 다음으로 간다.

## 1일차 — JSON 파일과 fetch (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 새 폴더 `web-week12` 를 만들어 VS Code 로 연다(**File › Open Folder**). 지난주 완성본을 넣는다: 내 `web-week11` 저장소 GitHub 화면 › **Code › Download ZIP** → 압축을 풀어 맨 위 파일(`server.mjs` 포함)과 `images/`·`screenshots/` 를 넣는다. 못 받으면 교재 [11주차 `examples/day2/web-week11/`](../week11_auth_rls/examples/day2/web-week11/) 파일과 [server.mjs](../../tools/static-server/server.mjs) 를 **Raw** 로 받는다. `ex` 폴더를 만들고 교재 [`examples/day1/`](examples/day1/) 의 여섯 파일을 **Raw** 로 저장한다. 터미널에서 `node server.mjs` 를 띄운다 |
| 5–18분 | ex01 JSON 글자 규칙 |
| 18–33분 | ex02 fetch 로 JSON 파일 읽기 |
| 33–47분 | ex03 `file://` 과 `http://` |
| 47–50분 | 확인: 여섯 파일이 `ex/` 에 있고, 각 예제에서 값 하나 이상을 바꿨는지. 일부러 낸 오류와 지운 줄은 되돌려 두었는지 |
| 50–60분 | 이번 주 저장소 만들어 올리기: GitHub 에 새 저장소 `web-week12` → [올리기 명령](#이번-주-저장소-만들어-올리기) → **Settings › Pages** → 공개 주소 `https://student01.github.io/web-week12/ex/` 확인 → 공용 PC면 자격 증명 삭제 |

1일차 예제는 모두 `ex/index.html` 하나로 연다. 주소창에 `http://localhost:8000/ex/` 를 친다. 그 파일 맨 아래 `<script src="exNN_….js">` 세 줄 중 **지금 문항의 줄 하나만** 주석 밖에 둔다(줄에서 **Ctrl+/**, macOS **⌘+/**). 코드는 각 `.js` 파일에서 고치고, 저장 → 새로고침으로 본다.
Node 가 없어 서버를 띄울 수 없는 PC 는 50–60분의 올리기를 먼저 하고 공개 주소 `https://student01.github.io/web-week12/ex/` 에서 본다. 고칠 때마다 push 하고 1~3분 기다린다.

### 1. ex01 JSON 글자 규칙 (`JSON.parse` · 큰따옴표 `"`)

[examples/day1/ex01_json_rule.js](examples/day1/ex01_json_rule.js) 를 `ex/ex01_json_rule.js` 로 저장한다. `ex/index.html` 맨 아래에서 `ex01_json_rule.js` 줄만 켠다(처음 받은 상태가 이렇다).

- 바꿔 보기: 화면 글자와 Console 1번은? Console 의 배열 앞 ▶ 를 눌러 펼친다. 객체는 몇 개이고 첫 `title` 은 무엇인가?
- 바꿔 보기: 13~15행 세 줄을 골라 **Ctrl+/** 로 주석을 푼다(2번 켜기). 빨간 줄은 무엇이라고 하나? 문구 끝 `(line 1 column 3)` 은 13행 백틱 안 글자의 몇째 글자인가? 오른쪽 `파일:줄` 이 내 `.js` 의 줄이 아니라 끝이 `:1` 인 까닭도 생각해 본다. 화면의 1번 글자는 왜 그대로 남아 있나? 확인했으면 되돌린다.
- 바꿔 보기: 18~20행의 주석을 푼다(3번 켜기). 빨간 줄 문구가 2번과 같은가? 18행에서 `]` 바로 앞의 `,` 하나를 지우면 어떻게 되나? 확인했으면 되돌린다.
- 바꿔 보기: 7행 글자의 `"title"` 두 곳에서 큰따옴표를 지워 `title` 로 만든다. 11주차 JS 객체 `{ name: name }` 에서는 이름에 따옴표가 없었다. JSON 에서는 어떻게 되나? 확인했으면 되돌린다.
- 흔한 실수: JSON 을 JS 객체처럼 쓴다. JSON 에서는 이름도 큰따옴표로 감싸고, 작은따옴표와 마지막 쉼표를 쓰지 않는다. VS Code 에서 `.json` 파일을 열면 틀린 자리에 빨간 밑줄이 생긴다.

### 2. ex02 fetch 로 JSON 파일 읽기 (`async` · `await fetch` · `await response.json()` · Network 탭)

[examples/day1/ex02_fetch.js](examples/day1/ex02_fetch.js) 와 [ex02_projects.json](examples/day1/ex02_projects.json) 을 `ex/` 에 저장한다. `ex/index.html` 맨 아래에서 ex01 줄을 끄고 `ex02_fetch.js` 줄만 켠다. **F12 › Network** 를 연 채로 새로고침한다.

- 바꿔 보기: 화면 글자와 Console 1·2번은? 1번 `response` 를 펼쳐 `status` 와 `ok` 를 찾는다. Network 에서 `ex02_projects.json` 줄의 **Status** 와 **Type** 은? 그 줄을 누르고 **Response** 탭을 연다. 무엇이 보이나?
- 바꿔 보기: `ex02_projects.json` 의 첫 `"title"` 값을 바꾸고 저장 → 새로고침한다. `.js` 는 그대로인데 화면이 바뀌나? 화면에 쓸 내용은 어느 파일에 있나?
- 바꿔 보기: 9행 `await response.json()` 에서 `await` 만 지운다. Console 2번에는 무엇이 찍히나? 빨간 줄은 무엇이라고 하나? 화면은 왜 원래 글자인가? 확인했으면 되돌린다.
- 바꿔 보기: 맨 아래 14행 `loadProjects();` 를 지운다. 화면·Console·Network 는 어떻게 되나? 확인했으면 되돌린다.
- 흔한 실수: `async` 를 빠뜨린다. `await` 는 `async` 를 붙인 함수 안에서만 쓸 수 있어서 파일 전체가 실행되지 않는다. Console 의 `await is only valid in async functions …` 줄이 그 표시다.

### 3. ex03 `file://` 과 `http://` (주소창 · Console)

[examples/day1/ex03_file_http.js](examples/day1/ex03_file_http.js) 와 [ex03_projects.json](examples/day1/ex03_projects.json) 을 `ex/` 에 저장한다. `ex/index.html` 에서 `ex03_file_http.js` 줄만 켠다.

- 바꿔 보기: 서버 주소 `http://localhost:8000/ex/` 에서 화면은 몇 번 글자인가? 서버를 띄운 터미널에 찍힌 줄 가운데 `ex03_projects.json` 줄의 앞 숫자는?
- 바꿔 보기: 탐색기에서 `ex/index.html` 을 두 번 눌러 연다. 주소창은 무엇으로 시작하나? 화면은 몇 번 글자에서 멈췄나? Console 의 빨간 줄은 무엇이라고 하고, `Uncaught` 로 시작하는 줄의 `파일:줄` 은 몇 행인가? 서버 터미널에는 줄이 늘었나?
- 바꿔 보기: 서버 주소 쪽 탭의 주소창에 `http://localhost:8000/ex/ex03_projects.json` 을 직접 친다. 무엇이 보이나? `fetch` 가 받아 오는 것도 이 글자다.
- 흔한 실수: "코드가 똑같은데 화면이 안 바뀐다"며 코드를 고친다. **주소창**을 먼저 본다. `file:///` 로 시작하면 서버 주소나 공개 주소로 다시 연다.

### 이번 주 저장소 만들어 올리기

GitHub 에서 **New repository** → 이름 `web-week12`, **Public**, README 는 추가하지 않는다. VS Code 터미널(현재 폴더 `web-week12`)에서 2주차에 배운 순서 그대로 친다. 서버가 떠 있는 터미널은 그대로 두고 **Terminal › New Terminal** 로 하나 더 연다.

```bash
git init
git add .
git commit -m "12주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week12.git
git push -u origin main
```

저장소 **Settings › Pages › Branch: main, /(root) › Save** → 1~3분 뒤 `https://student01.github.io/web-week12/ex/` 를 연다. `ex/index.html` 의 화면(제목과 "예제가 쓰는 자리")이 보이면 된 것이다. 켜 둔 줄이 ex02 면 공개 주소에서도 `ex02_projects.json` 을 읽어 온다. 공용 PC면 자격 증명을 지우고 나간다.
오늘 올린 것은 확인용이다. 제출은 2일차에 캡처 한 장만 한다.

## 2일차 — 카드와 오류 안내, 그리고 조립 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC에 `web-week12` 폴더가 남아 있으면 그대로 연다. 없으면 `git clone https://github.com/student01/web-week12.git` 뒤 **File › Open Folder**. 교재 [`examples/day2/`](examples/day2/) 의 아홉 파일(ex04~ex06 의 `.html`·`.js`, `ex04_picture.png`, `ex05_projects.json`, `ex06_projects.json`)을 **Raw** 로 `ex/` 에 저장하고 `node server.mjs` 를 띄운다. 5분 안에 다 못 받았으면 ex04 부터 시작하고, 나머지는 각 문항을 시작할 때 저장한다 |
| 5–14분 | ex04 카드 만들기 |
| 14–21분 | ex05 try / catch |
| 21–28분 | ex06 response.ok |
| 28–48분 | 조립: `data/projects.json` 과 카드 그림 세 장, `projects.html`, `projects.js` 를 만들고 세 페이지 nav 에 한 줄씩 |
| 48–55분 | 확인: 서버 주소 `http://localhost:8000/projects.html` → Network `projects.json` 200 → 파일 이름을 잠깐 바꿔 안내 문구 보기 → 되돌리기 → 375·1280 폭 |
| 55–60분 | 끝 루틴: `git add .` → `git commit -m "12주차 2일차"` → `git push` → 공개 주소 `https://student01.github.io/web-week12/projects.html` 에서 카드와 Network 탭을 함께 **캡처 1장** → 공용 PC면 자격 증명 삭제 |

2일차 예제는 `.html` 과 `.js` 가 한 쌍이다. 두 파일과 그 예제가 읽는 그림·`.json` 을 같은 `ex/` 폴더에 저장하고 `.html` 을 연다. 서버 주소는 `http://localhost:8000/ex/` 뒤에 파일 이름을 붙인다(예: `http://localhost:8000/ex/ex05_try_catch.html`).
파일마다 **바꿔 보기를 하나 이상** 하고 넘어간다. 28분이 되면 남은 것은 두고 조립을 시작한다. 남은 바꿔 보기는 캡처까지 끝낸 뒤 한다.

### 4. ex04 카드 만들기 (`createElement('article')` · `img` · `a` · `append`)

[examples/day2/ex04_cards.html](examples/day2/ex04_cards.html) 과 [ex04_cards.js](examples/day2/ex04_cards.js), 그림 [ex04_picture.png](examples/day2/ex04_picture.png) 를 `ex/` 에 저장하고 `ex04_cards.html` 을 연다. 이 예제는 `fetch` 가 없어서 두 번 눌러 열어도 된다.

- 바꿔 보기: 카드는 몇 장인가? **F12 › Elements** 에서 `<article class="card">` 하나를 펼친다. 안의 요소 네 개는 어떤 순서인가? `.js` 의 몇 행이 그 순서를 정하나?
- 바꿔 보기: 44행을 `article.append(title, image, description, link);` 로 바꾼다. 화면에서 무엇이 달라지나? 확인했으면 되돌린다.
- 바꿔 보기: 32행 `article.classList.add('card');` 앞에 `//` 를 붙인다. 노란 배경은? Elements 의 `article` 줄은 어떻게 보이나? 확인했으면 되돌린다.
- 바꿔 보기: 15행 두 번째 객체의 `image` 값을 `'ex04_nothing.png'`(없는 파일)로 바꾼다. 그 카드의 그림 자리에 무엇이 보이나? 35행 `alt` 에 넣은 글인가? 확인했으면 되돌린다.
- 바꿔 보기: 배열 끝에 네 번째 객체를 하나 더 적는다(세 번째 객체를 복사해 제목만 바꾼다. 앞 객체의 `}` 뒤에 쉼표). 카드는 몇 장이 되나? `for` 는 고쳤나?
- 흔한 실수: `projects[i].titel` 처럼 이름표 철자가 틀린다. 빨간 줄 없이 그 자리만 비어 보인다. 이름표는 데이터의 이름과 글자 단위로 같아야 한다.

### 5. ex05 try / catch (`try` · `catch (error)`)

[examples/day2/ex05_try_catch.html](examples/day2/ex05_try_catch.html) 과 [ex05_try_catch.js](examples/day2/ex05_try_catch.js), [ex05_projects.json](examples/day2/ex05_projects.json) 을 `ex/` 에 저장한다.

- 바꿔 보기: 서버 주소 `http://localhost:8000/ex/ex05_try_catch.html` 에서 화면과 Console 은? 이어서 탐색기에서 `ex05_try_catch.html` 을 두 번 눌러 연다. 화면은 몇 번인가? Console 에 `Uncaught` 로 시작하는 줄이 있나? 1일차 ex03 을 두 번 눌러 열었을 때와 무엇이 다른가?
- 바꿔 보기: `ex05_projects.json` 의 `"title"` 하나를 `'title'`(작은따옴표)로 바꾸고 서버 주소에서 새로고침한다. 화면은 몇 번인가? Console 2번의 오류는 ex01 2번의 빨간 줄과 같은 말인가? 확인했으면 되돌린다.
- 바꿔 보기: 둘째 바꿔 보기처럼 `ex05_projects.json` 에 작은따옴표를 넣은 채로 13·14행 앞에 `//` 를 붙여 `catch` 안을 비운다. 서버 주소에서 새로고침한다. 화면, Console, Network 의 `ex05_projects.json` Status 는? 무엇이 잘못됐는지 알 수 있나? 확인했으면 두 파일을 모두 되돌린다.
- 흔한 실수: `catch` 를 비워 둔다. 받은 오류를 아무 데도 쓰지 않아 화면은 `불러오는 중` 그대로이고, 내 코드가 남긴 오류 줄도 없어 원인을 찾기 어렵다. `catch` 에는 화면 안내 한 줄을 꼭 쓴다.

### 6. ex06 response.ok (`response.ok` · `!` · `return`)

[examples/day2/ex06_response_ok.html](examples/day2/ex06_response_ok.html) 과 [ex06_response_ok.js](examples/day2/ex06_response_ok.js), [ex06_projects.json](examples/day2/ex06_projects.json) 을 `ex/` 에 저장하고 서버 주소 `http://localhost:8000/ex/ex06_response_ok.html` 로 연다. **F12 › Network** 를 열어 둔다.

- 바꿔 보기: 화면, Console 한 줄, Network 의 `ex06_projects.json` Status 는? 처음에 있던 `불러오는 중` 은 어느 줄이 지웠나?
- 바꿔 보기: 6행 앞에 `//` 를 붙이고 7행의 `//` 를 지운다(2번 켜기). 화면, Console, Network Status 는? Console 에 `ex06_project.json` 의 404 빨간 줄이 있다(DevTools 를 연 채 새로고침하면 `GET …/ex/ex06_project.json 404 (Not Found)` 모양, 새로고침한 뒤에 열면 `Failed to load resource: … 404 (Not Found)` 모양이다. 표기는 Chrome 버전에 따라 조금 다를 수 있다). 이 빨간 줄은 내 코드가 남긴 줄인가? 연 채 새로고침했을 때 그 줄 오른쪽 `파일:줄` 은 몇 행이고, 그 행은 무엇을 하는 줄인가?
- 바꿔 보기: 2번을 켠 채 12~15행(`if` 부터 닫는 `}` 까지) 앞에 `//` 를 붙인다. 빨간 줄은 무엇이라고 하나? 그 안의 `<` 는 어디서 왔나(Network 에서 `ex06_project.json` 줄을 누르고 **Response** 탭의 첫 글자를 본다)? 확인했으면 되돌린다.
- 바꿔 보기: 1번으로 되돌리고 6행 파일 이름 앞에 `/` 를 붙인다(`'/ex06_projects.json'`). Network 에 찍힌 요청 주소와 Status 는? `/` 로 시작하는 주소는 어느 폴더에서 찾나? 확인했으면 되돌린다.
- 흔한 실수: `return;` 을 빠뜨린다. 안내를 쓰고도 아래 `response.json()` 으로 내려가 셋째 바꿔 보기와 같은 빨간 줄이 뜬다.

### 7. 조립 — `data/projects.json`·`projects.html`·`projects.js`, nav 네 페이지 (`fetch` · `try / catch` · `response.ok` · 카드)

이제 `ex/` 가 아니라 `web-week12` 맨 위에서 만든다. `ex/` 의 파일은 조립에 쓰지 않는다. 전문과 단계는 [따라하기 2일차](walkthrough.md#2일차)에 있다.

- `data` 폴더를 만들고 `data/projects.json` 에 객체 세 개를 적는다. 이름표는 `title`·`description`·`image`·`link` 네 개다.
- `images/` 에 카드 그림 `project1.png`·`project2.png`·`project3.png` 를 넣는다(교재 [`examples/day2/web-week12/images/`](examples/day2/web-week12/images/) 에서 **Raw**).
- `projects.html` 은 지난주 `guestbook.html` 과 같은 뼈대로 만든다. `<main>` 안에는 제목·안내 문장과 `<div id="notice"></div>`·`<div id="project-list"></div>` 두 자리를 둔다.
- `projects.js` 는 아래 조립표 순서로 쓴다.
- `index.html`·`about.html`·`guestbook.html` 의 nav 끝에 `<a href="projects.html">프로젝트</a>` 를 한 줄씩 넣는다. `projects.html` 의 nav 에도 같은 네 링크가 있다.

| 조립할 줄 | 어느 ex 에서 본 것 |
|---|---|
| `data/projects.json` 의 `[ { "title": …, "description": …, "image": …, "link": … }, … ]` | ex01 1번(큰따옴표), ex02 (`ex02_projects.json` 모양), ex04 (이름표 `image`·`link`) |
| `projects.html` 의 head·header·footer | 지난주 완성본 `guestbook.html` (`<title>`·`<script src="projects.js" defer>`·`<h1>` 의 글자를 바꾸고, nav 에 네 번째 링크를 넣는다) |
| `<h2>지금까지 만든 것</h2>` · `<p>아래 카드는 data/projects.json 파일에서 읽어 옵니다.</p>` | 지난주 `guestbook.html` 의 `<h2>한 줄 남기기</h2>` 와 같은 제목 줄, 읽는 사람에게 하는 실제 문장이라 `<p>`(글자만 새로 쓴다) |
| `<div id="notice"></div>` · `<div id="project-list"></div>` | ex05·ex06 (안내 자리), ex04 (카드 상자) |
| `const projectList = document.querySelector('#project-list');` · `const notice = document.querySelector('#notice');` | ex04, ex05 |
| `function showProjects(projects) { … }` (`innerHTML = ''` · `for` · `article` · `img` · `h3` · `p` · `a` · `append`) | ex04 그대로. `image.width` 와 `alt` 글, 링크 글자 `페이지 열기` 만 다르다 |
| `async function loadProjects() {` · `try {` | ex02 · ex05 |
| `const response = await fetch('data/projects.json');` | ex02 1번. 경로는 3주차 `images/profile.png` 처럼 폴더 이름/파일 이름 |
| `if (!response.ok) { notice.textContent = '프로젝트를 불러오지 못했습니다.'; return; }` | ex06 |
| `const projects = await response.json();` · `notice.textContent = '';` | ex02 2번 · ex06 |
| `showProjects(projects);` | ex04 (받은 배열을 넘긴다) |
| `} catch (error) { notice.textContent = '프로젝트를 불러오지 못했습니다.'; }` | ex05 2번 |
| `loadProjects();` | ex02 |
| nav 의 `<a href="projects.html">프로젝트</a>` | 지난주 nav 의 링크와 같은 모양 |

- 확인: 서버 주소 `http://localhost:8000/projects.html` 에서 카드 3장에 그림·제목·설명·**페이지 열기**가 보이고, Network 의 `projects.json` 이 200 이고, Console 에 `Uncaught` 빨간 줄이 없으면 된 것이다. `favicon.ico` 404 빨간 줄 하나는 브라우저가 탭 아이콘을 찾는 요청이라 괜찮다(5주차).
- 바꿔 보기: `data/projects.json` 의 이름을 잠깐 `project.json` 으로 바꾸고 새로고침한다. 화면과 Network 는? (ex06 2번과 같다.) 확인했으면 반드시 되돌린다.
- 흔한 실수: `fetch('/data/projects.json')` 처럼 `/` 로 시작한다. 내 PC 서버의 맨 위는 `web-week12` 폴더라 되는 것처럼 보이지만, 공개 주소의 맨 위는 `student01.github.io` 라서 404 다(내 파일은 `/web-week12/` 아래에 있다). `data/projects.json` 으로 쓴다.

### 8. 서버와 375·1280 폭으로 확인

- 서버가 멈춰 있으면 터미널(현재 폴더 `web-week12`)에서 `node server.mjs` → `http://localhost:8000/projects.html` 을 연다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.
- nav 의 네 링크와 카드의 **페이지 열기** 세 개를 모두 눌러 본다. 404 가 없으면 된 것이다.
- DevTools 의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)로 폭 375 와 1280 에서 카드를 본다. 375 에서 카드 그림이 화면 밖으로 넘치지 않고 메뉴가 세로로 서면 된 것이다.
- 확인이 끝나면 서버 터미널에서 **Ctrl+C** 로 멈추고 끝 루틴으로 간다. 캡처는 공개 주소에서 찍는다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다 |
| push 가 거부되거나 로그인 창이 안 뜬다 | [2주차 막혔을 때](../week02_github_pages/lab.md#막혔을-때) 표를 본다 |
| 화면이 생각과 다른데 이유를 모르겠다 | **주소창**이 `file:///` 로 시작하는지 먼저 본다. 다음은 **Console** 의 빨간 줄과 오른쪽 `파일:줄`, 그다음 **Network** 의 Status 다 |
| `'node' is not recognized` / `command not found: node` | Node.js 가 없는 PC 다. [서버 사용 안내](../../tools/static-server/README.md#막혔을-때)를 본다. 설치할 수 없으면 저장소를 먼저 만들어 올리고 공개 주소에서 확인한다 |
| `Access to fetch at 'file:///…' from origin 'null' has been blocked by CORS policy` 와 `… net::ERR_FAILED` 줄 | 두 번 눌러 연 화면(`file://`)이다. 코드가 틀린 것이 아니다. 서버 주소나 공개 주소로 연다(ex03) |
| `Uncaught (in promise) TypeError: Failed to fetch` | 위와 같은 원인이다. `try / catch` 를 넣으면 이 줄 대신 화면에 안내가 나온다(ex05) |
| `Uncaught SyntaxError: await is only valid in async functions and the top level bodies of modules` | `function` 앞에 `async` 가 빠졌다(ex02 흔한 실수) |
| Console 에 `Promise {<pending>}` 이 찍힌다 | 그 값을 만든 줄에 `await` 가 빠졌다(ex02 셋째 바꿔 보기) |
| `Uncaught (in promise) SyntaxError: Unexpected token '<', "<!doctype "... is not valid JSON` | 파일을 못 찾아(404) 서버가 보낸 HTML 오류 페이지를 `json()` 이 읽었다. 공개 주소에서는 `"<!DOCTYPE "...` 로 보인다. 이 줄의 오른쪽 `파일:줄` 은 내 `.js` 의 줄이 아니라 끝이 `:1` 이다(받은 글자 안의 자리). 그래서 Network 의 Status 부터 본다. `fetch` 의 경로·파일 이름·`data` 폴더를 본다. `response.ok` 확인이 있는지 본다(ex06) |
| 그 밖의 `SyntaxError` 줄에 `JSON` 이 들어 있다(`Expected property name or '}' in JSON at position …`, `… is not valid JSON` 등) | JSON 글자 규칙을 어겼다. 작은따옴표, 따옴표 없는 이름, 마지막 쉼표를 찾는다(ex01). 자리는 괄호 안 `line 3 column 5` 같은 숫자로 찾는다(JSON 글자 안의 줄과 칸). 오른쪽 `파일:줄` 은 내 `.js` 의 틀린 줄을 가리키지 않는다(`catch` 에 `console.log(error);` 를 넣었으면 그 줄이 찍힌다). 괄호 숫자가 없는 `… is not valid JSON` 문구는 따옴표 안에 보인 글자 조각 근처를 찾는다. VS Code 에서 `.json` 파일을 열면 빨간 밑줄로도 보인다 |
| Network 의 `projects.json` 은 200 인데 화면에 `프로젝트를 불러오지 못했습니다.` 가 보인다 | 파일은 왔다. `catch` 안에 `console.log(error);` 를 잠깐 넣고 새로고침한다. ① 문구가 찍히면 JSON 을 읽거나 카드를 그리다 난 오류를 `catch` 가 받은 것이다. 문구로 원인을 찾는다(JSON 규칙, `#project-list` 의 id 철자). ② 아무것도 찍히지 않으면 `catch` 가 아니라 `if (!response.ok)` 쪽 안내다. `fetch` 줄 앞의 `await` 가 빠졌거나(`response.ok` 가 `undefined`), `if` 의 `!` 가 빠졌다. 원인을 찾았으면 넣은 줄을 지운다 |
| Network 의 `projects.json` 이 404 다 | 파일 이름·폴더 이름·대소문자, `fetch` 경로의 철자를 본다. 서버 주소에서는 되는데 공개 주소에서만 404 면 경로가 `/` 로 시작하는지 본다(조립 흔한 실수) |
| `Uncaught (in promise) TypeError: Cannot set properties of null (setting 'textContent')` | `#notice` 를 찾지 못했다. `projects.js` 의 `querySelector('#notice')` 와 `projects.html` 의 `id="notice"` 철자가 같은지, `<script src="projects.js" defer>` 에 `defer` 가 있는지 본다 |
| 카드도 안내도 빨간 줄도 없다 | 마지막 줄 `loadProjects();` 가 있는지 본다(Network 에 `projects.json` 줄이 없다). 줄이 있으면 `await response.json()` 의 `await` 가 빠졌는지 본다 |
| 카드는 나오는데 그림 대신 글이 보인다 | 그림을 못 찾아 `alt` 글이 보인 것이다. `image` 값과 `images/` 안 파일 이름을 대소문자까지 맞춘다. 공개 주소는 대소문자를 가린다 |
| **페이지 열기**를 누르면 404 다 | `data/projects.json` 의 `link` 값이 실제 파일 이름과 다르다 |
| 카드가 흰 상자로 보이지 않는다 | `article.classList.add('card');` 줄이 빠졌거나 철자가 틀렸다(ex04 셋째 바꿔 보기). `styles.css` 는 고치지 않는다 |
| Network 의 Status 가 200 이 아니라 304 다 | 브라우저가 전에 받아 둔 파일을 다시 쓴다는 뜻이다. Network 탭 위쪽의 **Disable cache** 를 켜고 새로고침한다 |
| `Uncaught SyntaxError: Identifier 'result' has already been declared` | 1일차 `ex/index.html` 맨 아래에서 `script` 줄을 둘 이상 켰다. ex01~ex03 이 모두 같은 이름의 `const result` 를 만들어 둘째 파일이 실행되지 않는다. 한 줄만 켠다 |
| `.js` 이름(`ex02_fetch.js` 등)이 든 404 빨간 줄(DevTools 를 연 채 새로고침하면 `GET …/ex/ex02_fetch.js net::ERR_ABORTED 404 (Not Found)` 모양, 나중에 열면 `Failed to load resource: … 404 (Not Found)` 모양. 표기는 Chrome 버전에 따라 조금 다를 수 있다) | 켠 줄의 `.js` 파일이 `ex/` 에 없다. 파일 이름이 교재와 같은지(`.txt` 로 끝나지 않는지), `ex/` 안에 저장했는지 본다. 서버 터미널에도 `404 GET /ex/ex02_fetch.js` 같은 줄이 찍힌다 |
| 1일차 화면이 `원래 글자 — HTML 파일에 적힌 글자` 그대로이고 Console 에 예제가 찍은 줄이 없다(`favicon.ico` 404 한 줄은 상관없다) | `ex/index.html` 맨 아래에 켠 `script` 줄이 없다(모두 주석). 그 문항의 줄 하나를 켠다. 켠 줄이 ex02 면 `ex02_fetch.js` 맨 아래 `loadProjects();` 가 있는지 본다(ex02 넷째 바꿔 보기) |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 과 Network 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://student01.github.io/web-week12/projects.html` (본인 아이디) 을 열고 **F12 › Network** 를 연 채 새로고침한 뒤, 다음이 한 화면에 보이게 캡처한다.

- 카드 3장에 그림·제목·설명과 **페이지 열기** 링크가 있다.
- **F12 › Network** 에 `projects.json` 이 **Status 200** 으로 보인다.
- **주소창이 함께 보이게** 찍는다.

완료 기준은 공개 주소에서 카드 3장이 JSON 파일에서 읽혀 나오는 것이다. 카드에 제목·설명만 있고 그림·링크가 없으면 부분 통과다.
1일차 push 와 `ex/` 실험 파일은 확인용이며 따로 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- `data/projects.json` 에 네 번째 항목을 더한다. 카드가 4장이 되나? `projects.js` 는 고쳤나?
- 카드 제목 아래에 만든 날짜를 넣는다. `projects.json` 의 세 항목에 `"date"` 를 더하고 `showProjects` 에서 `div` 를 하나 더 만든다(날짜는 문장이 아니라 값 한 칸이라 `div`). `append` 의 어디에 넣나?
- `data/projects.json` 을 `[]`(빈 배열)로 바꾼다. 화면은 어떻게 되나? 빈 화면 대신 `아직 등록한 프로젝트가 없습니다.` 를 보이려면 `if (projects.length === 0)` 을 어디에 넣나? 확인했으면 되돌린다.
- **Network** 에서 `projects.json` 줄을 누르고 **Response** 탭을 연다. 내 파일과 같은 글자인가?

추가 과제는 선택 사항이며 채점하지 않는다.
