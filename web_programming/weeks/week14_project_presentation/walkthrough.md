[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation)

# 14주차 따라하기 — 비교 예제로 확인하고 발표 준비하기

이번 주는 새 저장소 `web-week14` 를 만든다. 지난주 완성본을 넣고, 비교 예제는 그 안의 `ex/` 폴더에 저장한다. 값이나 여는 방법을 바꾼 뒤 결과를 화면, **F12 › Console**, 서버를 띄운 터미널에서 본다.
2일차는 90분 전체가 발표라서 **조립·올리기·리허설을 모두 1일차에 한다.** 2일차에는 발표만 한다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

비교 예제 3개는 교재 저장소의 [examples/day1](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation/examples/day1) 폴더에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다.

## 1일차

### 1. web-week14 폴더 만들고 지난주 완성본 넣기

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-week14` 를 만들고 VS Code **File › Open Folder** 로 연다.

지난주 완성본을 넣는다. 내 `web-week13` 저장소 GitHub 화면에서 **Code › Download ZIP** 을 누르고, 압축을 푼 폴더에서 맨 위 파일과 `data/`·`images/`·`screenshots/` 를 `web-week14` 로 옮긴다. 맨 위 파일에는 `README.md` 와 `server.mjs` 도 있다. 지난주 `ex/` 폴더는 옮기지 않는다.
ZIP 을 못 받았으면 교재 [13주차 `examples/day2/web-week13/`](../week13_release_security/examples/day2/web-week13/) 의 파일을 2단계와 같은 **Raw** 방법으로 받고, [server.mjs](../../tools/static-server/server.mjs) 도 같은 방법으로 받는다.

이어서 `web-week14` 안에 `ex` 폴더를 만든다. 현재 폴더: `web-week14`

```bash
mkdir ex
```

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week14/
  data/          projects.json
  ex/            ← 아직 비어 있다
  images/        profile.png  project1.png  project2.png  project3.png
  screenshots/   guestbook.png  home.png  projects.png
  about.html  about.js  app.js  guestbook.html  guestbook.js
  index.html  projects.html  projects.js  README.md  server.mjs  styles.css
```

- `README.md` 가 지난주에 쓴 레포트 최종판이다. 이번 주에는 세 곳만 고친다.
- `styles.css` 와 `.js` 파일은 이번 주에 한 글자도 고치지 않는다. 고치는 파일은 `index.html`·`about.html`·`README.md` 와 그림 `screenshots/home.png` 뿐이다.

### 2. 비교 예제 가져오기

오늘 파일은 여섯 개다. 예제마다 화면이 서로 달라서 고르기 페이지 없이 따로 연다.

| 파일 | 비교하는 것 |
|---|---|
| [ex01_order_list.html](examples/day1/ex01_order_list.html) | 같은 다섯 줄을 `<ol>` 번호 목록 / `<ul>` 점 목록에 |
| [ex02_server.html](examples/day1/ex02_server.html) + [ex02_server.js](examples/day1/ex02_server.js) + [ex02_message.json](examples/day1/ex02_message.json) | 같은 페이지를 서버로 연다 / 두 번 눌러 연다 |
| [ex03_storage.html](examples/day1/ex03_storage.html) + [ex03_storage.js](examples/day1/ex03_storage.js) | 변수에 담은 수 / 저장 칸(`localStorage`)에 넣은 수 |

[교재 저장소 examples/day1 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation/examples/day1)에서 파일을 누르고 오른쪽 위 **Raw** 를 누른다. 글자만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `web-week14/ex/` 에 저장한다. 파일 이름은 교재와 **같게** 둔다. `.json` 도 같은 방법이다.

**예상 결과** — `ex/` 안에 파일 여섯 개가 있다.

```text
ex/
  ex01_order_list.html
  ex02_message.json
  ex02_server.html
  ex02_server.js
  ex03_storage.html
  ex03_storage.js
```

- 저장한 파일 이름이 `.txt` 로 끝나면 이름을 고친다. 이름은 VS Code 탐색기에서 확인한다.
- `.js`·`.json` 은 두 번 누르지 않는다. 같은 폴더의 `.html` 이 불러온다.

### 3. 여는 법 — 서버로 열기와 두 번 눌러 열기

이번 주에는 같은 파일을 두 가지로 열어 비교한다. 차례는 예제의 형제 번호와 같다. ①이 1번, ②가 2번이다.

① **서버로 열기** — 터미널에서 서버를 띄운다. 현재 폴더: `web-week14`

```bash
node server.mjs
```

주소창에 `http://localhost:8000/ex/ex02_server.html` 을 친다. 서버는 그 터미널에서 **Ctrl+C** 를 누를 때까지 돈다. 터미널을 닫아도 멈춘다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.

② **두 번 눌러 열기** — VS Code 탐색기에서 `ex/ex02_server.html` 을 오른쪽 클릭 › **Reveal in File Explorer**(macOS는 **Reveal in Finder**) → 두 번 누른다. 주소창이 `file:///` 로 시작한다.

**예상 결과** — ①은 화면 글자가 `서버로 열어 JSON 파일에서 읽은 글입니다.` 이고, Console 에 아래 한 줄이 찍힌다(favicon 404 빨간 줄은 세지 않는다).

```text
1. 서버로 열어 읽었다 : 서버로 열어 JSON 파일에서 읽은 글입니다.   ex02_server.js:12
```

서버 터미널에는 브라우저가 요청한 파일이 한 줄씩 찍힌다.

```text
200 GET /ex/ex02_server.html
200 GET /ex/ex02_server.js
200 GET /ex/ex02_message.json
```

- ①의 서버 터미널에 `404 GET /favicon.ico` 한 줄이 섞여도 된다. 그때 Console 에도 `favicon.ico` 의 404 빨간 줄이 하나 보일 수 있다. 탭 아이콘 요청이고 없어도 된다(5주차).

②는 화면 글자가 `읽지 못했습니다.` 이고, Console 에 빨간 줄 두 줄과 `2. 읽지 못했다` 가 찍힌다.

- ②의 첫 빨간 줄은 `Access to fetch at 'file:///…/ex02_message.json' from origin 'null' has been blocked by CORS policy` 로 시작하고, 둘째 줄은 `Failed to load resource: net::ERR_FAILED` 다. 두 번 눌러 연 페이지에서는 `fetch` 가 파일을 읽지 못한다는 뜻이다. 12주차 프로젝트 카드가 같은 이유로 두 번 눌러 연 화면에서 나오지 않는다.
- 이번 주에 새로 쓰는 DevTools 탭은 없다. ex03 에서 11주차의 **Application › Local storage** 를 다시 쓴다.

### 4. 값 바꾸는 요령

실험은 늘 같은 순서다. **VS Code 에서 고치고 저장**(Ctrl+S, macOS는 ⌘+S) → **브라우저에서 새로고침**(F5, macOS는 ⌘+R) → **화면·Console·서버 터미널**을 본다.
바꾸기 전에 무엇이 달라질지 먼저 말해 보고 확인한다.

**새로고침해 보기** — `ex/ex03_storage.html` 을 두 번 눌러 연다. **눌러 보기**를 세 번 누르고 새로고침한다.

**예상 결과** — 누를 때마다 Console 에 두 줄씩 찍히고, 새로고침 뒤 화면은 `1. 변수에 담은 수: 0` 과 `2. 저장한 수: 3` 이다(처음 열었을 때 기준).

```text
1. 변수 : 1     ex03_storage.js:15
2. 저장 : 1     ex03_storage.js:20
1. 변수 : 2     ex03_storage.js:15
2. 저장 : 2     ex03_storage.js:20
1. 변수 : 3     ex03_storage.js:15
2. 저장 : 3     ex03_storage.js:20
```

`+ 1` 하는 줄은 둘이 같다. 다른 것은 담는 곳이다. 1번은 변수라서 새로고침하면 파일을 다시 읽어 0 에서 시작한다. 2번은 브라우저의 저장 칸(`localStorage`, 11주)에 넣어 두었다가, 열 때 9행이 다시 꺼내 온다. 9행은 11주 방명록의 되살리는 줄과 같은 모양이다.

- 같은 파일을 서버 주소 `http://localhost:8000/ex/ex03_storage.html` 로 열면 2번은 0 에서 시작한다. 주소 앞부분(`file://` 과 `http://localhost:8000`)이 다르면 저장 칸도 다르다. 새 시크릿 창도 따로다.
- 거꾸로 앞부분이 같으면 저장 칸을 함께 쓴다. 같은 아이디의 `github.io` 주소는 `web-week13` 과 `web-week14` 가 한 칸을 쓴다(11주). `http://localhost:8000` 도 5주부터 매주 같은 칸이다.
- 값을 원래대로 못 돌리겠으면 교재에서 그 파일을 다시 **Raw** 로 받아 덮어쓴다.
- 파일마다 무엇을 바꿔 볼지는 [1일차 실습](lab.md#1일차--비교-예제-조립-3분-리허설-60분)에 있다.

### 5. 조립표

21분부터 조립한다. 이제 `ex/` 가 아니라 `web-week14` 맨 위의 `index.html`·`about.html`·`README.md` 를 연다.
조립하는 줄은 모두 비교 예제와 13주차 완성본에서 본 것이다. 13주차 완성본은 1단계에서 넣은 내 파일 자체다.

| 조립할 줄 | 출처 |
|---|---|
| `index.html` 에 `<h2>이 사이트에서 할 수 있는 것</h2>` | 13주차 완성본 `index.html` 의 `<h2>취미</h2>` 와 같은 모양 |
| `index.html` 에 `<ol class="card">` 와 `<li>` 다섯 줄 | [ex01](examples/day1/ex01_order_list.html) 1번 + 13주차 `<ul class="card">` 의 `class="card"` |
| `about.html` 표에 `<tr>` 한 행(`<td>` 두 칸) | 13주차 완성본 `about.html` 의 `관심 분야` 행 |
| `README.md` 의 공개 주소 줄과 홈 줄 | 13주차 완성본 `README.md` 의 7행과 11행 |
| `README.md` 의 `## 만든 과정` 맨 아래 한 줄(`- 14주차: …`) | 13주차 완성본 `README.md` 의 같은 절 줄 모양(`- 13주차: …`) |

옮겨 적을 때 출처 파일을 옆에 열어 두고, 같은 줄이 거기서 무엇을 했는지 떠올린다.

### 6. index.html 에 발표 순서 목록 넣기

`web-week14/index.html` 을 연다. `<div class="card" id="count">클릭 0회</div>` **바로 아래**에 여덟 줄을 넣는다.

```html
      <h2>이 사이트에서 할 수 있는 것</h2>
      <ol class="card">
        <li>위 메뉴로 네 페이지를 오갑니다.</li>
        <li>버튼으로 인사말과 배경색을 바꿉니다.</li>
        <li>방명록에 글을 남기고 지웁니다.</li>
        <li>남긴 글은 새로고침해도 그대로 있습니다.</li>
        <li>프로젝트 카드는 JSON 파일에서 읽어 옵니다.</li>
      </ol>
```

- 다섯 줄의 순서가 곧 발표 순서다. [3분 시연 흐름 표](demo_outline.md)의 둘째~일곱째 줄과 같다. 빈값 안내(0:55)와 남기기·삭제(1:15)는 셋째 줄 하나로 묶었다.
- `<ol>` 이라서 번호는 브라우저가 붙인다. 글에 번호를 쓰지 않는다(ex01).
- `class="card"` 를 붙여서 다른 카드처럼 흰 상자 안에 들어간다(4주차 `.card`).
- 문장은 본인 사이트에 맞게 고쳐도 된다. 줄 수와 차례만 지킨다.

### 7. about.html 표에 공개 주소 행 넣기

`web-week14/about.html` 을 연다. 표의 `관심 분야` 행(그 행의 `</tr>` 까지) **아래**에 네 줄을 넣는다. 주소는 내 공개 주소다.

```html
        <tr>
          <td>공개 주소</td>
          <td>https://student01.github.io/web-week14/</td>
        </tr>
```

- 표의 한 행은 `<tr>` 이고 그 안의 칸이 `<td>` 두 개다. 위 `관심 분야` 행과 같은 모양이다(3주차 표).
- 주소는 글자로 적는다. 지금 보고 있는 페이지가 그 주소라서 링크로 만들 필요는 없다.
- `student01` 을 본인 아이디로 바꾼다. 교재 완성본(10단계 전문)의 주소는 예시 아이디 `student01` 의 것이다.

### 8. README.md 세 곳 고치기

`web-week14/README.md` 를 연다. 새로 쓰지 않는다. 세 곳만 고친다.

첫째, `## 공개 주소` 아래 줄의 주소 두 곳을 이번 주 주소로 바꾼다. 대괄호 안은 보이는 글, 소괄호 안은 누르면 가는 주소다.

```markdown
- [https://student01.github.io/web-week14/](https://student01.github.io/web-week14/)
```

둘째, `## 페이지` 의 첫 줄(홈) 설명에 `할 수 있는 것 목록` 을 넣는다. 줄 앞의 링크 부분은 그대로 둔다.

```markdown
- [홈 (index.html)](index.html) — 인사말, 할 수 있는 것 목록, 소개, 취미 목록
```

셋째, `## 만든 과정` 맨 아래(13주차 줄 다음)에 이번 주 한 줄을 더한다. 이번 주 실습에서 한 일을 내 말로 쓴다.

```markdown
- 14주차: 홈에 할 수 있는 것 목록 넣고 내 정보에 공개 주소 적기
```

**예상 결과** — VS Code 에서 `README.md` 를 열고 오른쪽 위 **Open Preview** 를 누르면, 공개 주소가 `web-week14` 가 들어간 파란 링크로 보이고, 홈 줄에 `할 수 있는 것 목록` 이 보이고, `## 만든 과정` 이 9주차부터 14주차까지 여섯 줄이다.

- 만든 과정은 주차마다 한 줄이다. 13주차에 쓴 다섯 줄(9~13주차)은 그대로 둔다. 빠진 주가 있으면 그 주 실습에서 한 일을 떠올려 한 줄로 채운다. 채점표는 9주차부터 14주차까지 여섯 줄을 본다([채점표](rubric.md) "사용 기술·만든 과정").
- 교재 완성본 [README.md](examples/day2/web-week14/README.md) 의 주소는 예시 아이디 `student01` 의 것이다. 내 README 에는 내 아이디의 `web-week14` 주소를 쓴다. 채점자가 이 링크를 눌러 사이트를 연다.
- 맨 위 제목 줄(`# …`)은 사이트 이름이라 그대로 두어도 된다.

### 9. index.html 전문

8단계까지 마친 `index.html` 전체다. 내 파일과 한 줄씩 비교한다. 13주차 파일에서 늘어난 것은 6단계의 여덟 줄(27~34행)뿐이다.

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
      <h2>이 사이트에서 할 수 있는 것</h2>
      <ol class="card">
        <li>위 메뉴로 네 페이지를 오갑니다.</li>
        <li>버튼으로 인사말과 배경색을 바꿉니다.</li>
        <li>방명록에 글을 남기고 지웁니다.</li>
        <li>남긴 글은 새로고침해도 그대로 있습니다.</li>
        <li>프로젝트 카드는 JSON 파일에서 읽어 옵니다.</li>
      </ol>
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

같은 파일이 [examples/day2/web-week14/index.html](examples/day2/web-week14/index.html) 에 있다.

### 10. about.html 전문

13주차 파일에서 늘어난 것은 7단계의 네 줄(40~43행)뿐이다. 42행 주소의 아이디만 내 것으로 다르고, 나머지는 글자 단위로 같아야 한다.

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
        <tr>
          <td>공개 주소</td>
          <td>https://student01.github.io/web-week14/</td>
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
      <div class="card" id="year-result">입학 연도를 적고 계산하기를 누르세요.</div>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

같은 파일이 [examples/day2/web-week14/about.html](examples/day2/web-week14/about.html) 에 있다.

### 11. 375·1280 폭과 서버로 확인 — 로컬 시연 연습

3단계에서 띄운 서버가 그대로 돌고 있으면 주소창에 `http://localhost:8000/` 을 친다. 멈췄으면 다시 띄운다. 현재 폴더: `web-week14`

```bash
node server.mjs
```

**예상 결과** — 홈의 `클릭 0회` 아래에 `이 사이트에서 할 수 있는 것` 과 번호 1~5 의 다섯 줄이 흰 카드에 들어가 보인다. 번호는 카드 왼쪽 테두리에 걸쳐 보인다. 13주차 취미 목록의 점과 같은 자리이고 고장이 아니다. 내 정보 표는 다섯 행이고 마지막 행이 공개 주소다. 프로젝트 페이지에 카드 세 장이 나온다. Console 에 `Uncaught` 빨간 줄이 없다. 서버로 열면 `favicon.ico` 404 한 줄은 보여도 된다(탭 아이콘 요청).

이어서 [3분 시연 흐름 표](demo_outline.md)의 앞 일곱 줄을 이 서버 주소에서 한 번 해 본다. 공개 주소가 안 열릴 때 하는 **로컬 시연**과 같은 화면이다. 여덟째 줄(Commits 탭과 README)은 저장소를 올린 뒤 14·15단계에서 본다.

- 서버 주소의 방명록은 공개 주소의 방명록과 저장 칸이 따로다(ex03). 비어 있거나, 지난 주에 이 PC 의 서버로 연습한 글이 보일 수 있다. `http://localhost:8000` 은 5주부터 같은 주소이고 방명록 키 `guestbook` 도 11주부터 같다. 비어 있으면 두세 줄 남기고 진행한다.
- DevTools 의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)로 폭 375 와 1280 을 오가며 홈을 본다. 375 에서는 메뉴가 세로로 선다(4주차 `@media`). 목록 카드는 두 폭 모두 화면 안에 들어온다.
- **다크 모드**를 누르면 목록 카드도 어두워진다. 목록에도 `class="card"` 를 붙였기 때문이다(6주차 `body.dark .card`).
- 두 번 눌러 연 `index.html` 에서 프로젝트 페이지로 가면 카드가 나오지 않는다(ex02). 로컬 시연은 서버로만 한다.

### 12. 이번 주 저장소 만들어 올리기

31분에 한다. 2일차가 발표라서 오늘 미리 올려 공개 주소를 확인받는다.

GitHub 에서 **New repository** 를 누르고 이름 `web-week14`, **Public** 으로 만든다. README 는 추가하지 않는다. 지난주 `README.md` 를 이미 넣었다.
서버가 돌고 있는 터미널은 그대로 두고 **Terminal › New Terminal** 로 새 터미널을 연다. 2주차에 배운 순서 그대로 친다. 현재 폴더: `web-week14`

```bash
git init
git add .
git commit -m "14주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week14.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save** 를 누른다.

**예상 결과** — GitHub 저장소 화면을 새로고침하면 파일 목록 아래에 `README.md` 가 문서로 보이고 그림 세 장이 나온다. 1~3분 뒤 `https://student01.github.io/web-week14/` 를 열면 홈에 번호 목록이 보인다.

- 404가 나면 주소의 `web-week14` 가 저장소 이름과 글자 단위로 같은지, Pages 를 켰는지 본다.
- push 가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../week02_github_pages/lab.md#막혔을-때)를 본다.

### 13. 공개 주소에서 확인하고 그림 다시 찍기

**새 시크릿 창**(Ctrl+Shift+N, macOS ⌘+Shift+N)에서 공개 주소를 연다. 로그인하지 않은 창이라 채점자가 보는 화면과 같다.

```text
https://student01.github.io/web-week14/
```

| 확인할 것 | 어디서 |
|---|---|
| nav 링크 네 개가 서로 오간다 | 네 페이지 모두 |
| 버튼을 누르면 문장·배경색이 바뀌고 `클릭 N회` 가 오른다 | `index.html` |
| 표 맨 아래에 내 공개 주소가 있다 | `about.html` |
| 칸을 비우고 누르면 안내가 보이고, 넣고 누르면 목록에 쌓이고 지워진다 | `guestbook.html` |
| 새로고침해도 목록이 남아 있다 | `guestbook.html` |
| 카드 세 장이 그려진다 | `projects.html` |

**예상 결과** — 여섯 가지가 모두 공개 주소에서 동작하고 Console 에 `Uncaught` 빨간 줄이 없다. 방명록은 처음에 비어 있다. 새 시크릿 창은 일반 창과 저장 칸을 따로 쓰기 때문이다(ex03). 여기서는 한 줄 남겨 쌓이는지만 본다. 시크릿 창을 닫으면 지워지므로 발표용 두세 줄은 2일차 발표 직전에 발표할 창에서 남긴다(17단계).

이어서 홈에서 **인사 바꾸기**를 한 번 누르고, 13주차와 같은 방법으로 홈 화면을 찍어 `web-week14/screenshots/home.png` 에 덮어쓴다. `guestbook.png`·`projects.png` 는 13주차 것을 그대로 둔다.

- `home.png` 는 버튼을 누른 뒤 찍는다. `클릭 0회` 인 그림은 동작하기 전 화면이다(채점표 "캡처 3장").
- 그림 파일 이름은 `home.png` 그대로 둔다. README 가 이 이름으로 부른다. 대소문자가 다르면 GitHub 에서 깨진다.

### 14. 저장소 첫 화면에서 README 확인하기

저장소 화면 `https://github.com/student01/web-week14` 를 새로고침한다. 파일 목록 아래에 `README.md` 가 문서로 보인다. 이 화면이 레포트이고, 조교가 확인하는 화면이다.

| 확인할 것 | 어디서 |
|---|---|
| 공개 주소 링크를 누르면 내 `web-week14` 사이트가 열린다 | `## 공개 주소` |
| 홈 줄에 `할 수 있는 것 목록` 이 있다 | `## 페이지` |
| 9주차부터 14주차까지 주차마다 한 줄씩, 여섯 줄이다 | `## 만든 과정` |
| 그림 세 장이 깨지지 않고 보인다 | `## 화면` |

**예상 결과** — 네 가지가 모두 보인다. 홈 그림은 아직 31분에 올린 13주차 그림이다. 13단계에서 다시 찍은 `home.png` 는 16단계 끝 루틴에서 올라간다.

- 고칠 것이 있으면 VS Code 에서 고쳐 저장해 둔다. 올리는 것은 16단계에서 한 번에 한다.
- 그림이 깨지거나 글자 링크로만 보이면 [실습지의 막혔을 때](lab.md#막혔을-때)를 본다.

### 15. 3분 리허설

조교는 38분부터 순회하며 먼저 끝낸 사람부터 공개 주소와 README 를 확인한다. 확인받은 사람부터(늦어도 47–55분) 짝과 번갈아 3분을 재며 한 번씩 해 본다.

```text
0:00  공개 주소를 열고 한 줄 소개        1:15  이름·메시지를 넣고 [남기기], 한 줄 [삭제]
0:20  nav 로 네 페이지                   1:45  새로고침 — 목록이 남아 있다
0:40  홈에서 [다크 모드] 클릭            2:05  프로젝트 카드 세 장
0:55  칸을 비우고 [남기기] → 안내        2:35  Commits 탭과 README
```

**예상 결과** — 3분 안에 여덟 줄이 끝난다. 넘치면 어디를 줄일지 정한다. 대개 첫 소개와 카드 설명이 길다.

- 말하면서 누른다. 누르고 나서 설명하면 시간이 두 배가 된다.
- 듣는 짝은 점수를 매기지 않는다. 넘긴 시간과 빠뜨린 줄만 적어 준다.
- 구술 연습: 짝이 버튼 하나를 가리키면 **F12 › Elements** 에서 그 버튼의 `id` 를 읽고, `.js` 파일에서 그 `id` 로 찾은 줄과 `addEventListener` 안에서 부르는 함수를 말한다. 예: **[다크 모드]** → `id="dark-button"` → `app.js` 의 `darkButton.addEventListener('click', …)` → 안에서 `countUp()` 을 부른다.

### 16. push 와 캡처

55분에 한다. 현재 폴더: `web-week14`

```bash
git add .
git commit -m "14주차 1일차 마무리"
git push
```

push 가 끝나면 저장소 화면 `https://github.com/student01/web-week14` 를 새로고침한다. 저장소 화면은 push 가 끝나면 곧 바뀐다. 1~3분 기다리는 것은 공개 주소(Pages)다.

**예상 결과** — 저장소 첫 화면의 README 에서 공개 주소가 `web-week14` 이고, `## 만든 과정` 이 14주차 줄까지 여섯 줄이고, 홈 그림이 새 그림이다. README 와 그림 세 장이 함께 보이게 이 화면을 캡처한다. 이 캡처 한 장이 제출이다.
공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com` 을 지우고 나간다.

- 그림이 옛 그림이면 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 막히면 [실습지의 막혔을 때](lab.md#막혔을-때)를 본다.

## 2일차

### 17. 발표 전 탭 세 개 준비하기

자기 차례 두 사람 앞에서 브라우저 탭 세 개를 연다.

```text
탭 1  https://student01.github.io/web-week14/            ← 발표할 창
탭 2  https://github.com/student01/web-week14
탭 3  https://github.com/student01/web-week14/commits
```

이어서 탭 1 에서 방명록을 열어 발표용 글 두세 줄을 남기고 홈으로 돌아온다.

**예상 결과** — 세 탭이 열려 있고, 탭 1은 홈이 밝은 배경에 `클릭 0회` 인 처음 상태다. 방명록에는 방금 남긴 글 두세 줄이 있다.

- 시크릿 창은 닫으면 저장한 글이 지워진다. 1일차에 시크릿 창에서 남긴 한 줄은 오늘 없다. 그래서 발표용 글은 지금, 발표할 이 창에서 남긴다(ex03).
- 일반 창이면 지난주(`web-week13`)에 같은 PC 에서 남긴 글이 보일 수 있다. 같은 아이디의 `github.io` 주소는 저장 칸을 함께 쓴다(11주). 지우려면 **전체 지우기**를 누르고 다시 남긴다.
- 다크 모드는 꺼 두고 시작한다. 0:40 에 눌러서 바뀌는 것을 보여 준다.
- 다른 사이트나 로그인 화면이 보이는 탭은 닫는다.

### 18. 3분 시연

15단계에서 연습한 여덟 줄을 그대로 한다. 말하면서 누른다.

1. 탭 1을 보이며 "`student01`의 웹 연습장입니다. 네 페이지가 있고, 남긴 글이 새로고침해도 남습니다."
2. nav 로 홈 → 내 정보 → 방명록 → 프로젝트 → 홈. 내 정보 표의 **공개 주소** 행을 한 번 짚는다.
3. 홈에서 **[다크 모드]** 를 누르며 "배경색이 바뀌고 클릭 횟수가 오릅니다."
4. 방명록에서 칸을 비운 채 **[남기기]** → 안내 문장.
5. 이름·메시지를 넣고 **[남기기]**, 한 줄을 **[삭제]**.
6. 같은 페이지를 **새로고침**(F5)한다. 목록이 그대로다.
7. 프로젝트 페이지에서 "카드 세 장은 제가 쓴 `data/projects.json` 에서 읽어 온 것입니다."
8. 탭 3의 **Commits** 탭과 탭 2의 README 를 보이며 마무리한다.

**예상 결과** — 3분 안에 끝나고, 채점자가 여덟 가지를 모두 화면에서 확인한다.

- 코드 파일은 띄우지 않는다. 구술 질문("이 버튼을 누르면 어느 함수가 실행됩니까?")을 받으면 그때 연다.
- 잘 안 되는 기능이 있으면 그 줄을 건너뛰고 되는 것부터 보여 준다.
- 공개 주소가 열리지 않으면 손을 든다. 새 시크릿 창 → 로컬 시연(11단계처럼 `node server.mjs` → `http://localhost:8000/`) 순서로 바꾸며 배점은 같다. 로컬 주소의 방명록은 공개 주소와 저장 칸이 따로라서, 비어 있으면 먼저 두세 줄 남긴다.
- 이 PC 에 `web-week14` 폴더가 없으면 19단계의 `git clone` 으로 받은 뒤 그 폴더에서 `node server.mjs` 를 띄운다. Node 가 없는 PC 면 손을 들어 조교 PC 에서 연다.

### 19. 발표가 끝나면

남의 발표를 들으며 채점표를 본다. 자기 코드는 고치지 않는다.
마지막 10분에 README 를 고칠 것이 있으면 고쳐 올린다. 같은 PC에 `web-week14` 폴더가 없으면 받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week14.git
```

내려받은 `web-week14` 를 **File › Open Folder** 로 열고 고친다. 현재 폴더: `web-week14`

```bash
git add .
git commit -m "14주차 2일차"
git push
```

**예상 결과** — 저장소 첫 화면에 고친 README 가 보인다. 고칠 것이 없으면 올리지 않아도 된다. 제출은 2일차 발표 3분과 1일차 캡처 1장이다.
공용 PC라면 자격 증명을 지우고 나간다.
