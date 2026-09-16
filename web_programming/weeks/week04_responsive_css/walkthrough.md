# 4주차 따라하기 — 세 페이지를 CSS로 꾸미기

처음에는 그대로 따라 하고, 결과가 나오면 본인 아이디와 색으로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

이번 주에 고치는 파일은 `styles.css` 하나와 세 페이지의 `link` 한 줄씩, 그리고 `index.html`의 `class="card"` 세 곳이다.
`app.js`는 열지 않는다. 동작은 5주차에 한다.

## 1일차

### 1. 저장소 받아오기

지난주에 쓰던 PC라면 폴더를 열고 새 commit만 받아 온다. 현재 폴더: `my-web`

```bash
git pull
git log --oneline
```

**예상 결과** — 집에서 push한 것이 없으면 `Already up to date.` 한 줄이다. `git log --oneline`에는 3주차까지의 commit이 보인다.

```text
9bd9ddb 방명록 페이지 추가
32b2716 자기소개 페이지 만들기
```

처음 쓰는 PC라면 저장소를 통째로 내려받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

- 앞의 일곱 글자는 PC마다 다르다. GitHub 저장소 화면의 **Commits** 탭에서도 같은 목록을 볼 수 있고,
  commit 하나를 누르면 그때 바뀐 줄이 초록·빨강으로 보인다.
- `fatal: destination path 'my-web' already exists and is not an empty directory.`가 나오면 그 자리에 이미 폴더가 있는 것이다. 그 폴더를 열고 `git pull`을 한다.

### 2. styles.css 비우고 body 규칙 쓰기

`styles.css`를 연다. 2주차에 넣어 둔 틀(카드·그림자)이 들어 있다. **전체를 지우고** 아래 규칙 하나를 쓴다.

```css
body {
  background-color: #eef2ff;
  color: #17213a;
  font-family: system-ui, sans-serif;
  font-size: 16px;
}
```

**예상 결과** — 저장하고 브라우저를 새로고침해도 **화면은 그대로**다. 아직 `index.html`이 이 파일을 연결하지 않았기 때문이다.

- 규칙 하나는 `선택자 { 속성: 값; }` 모양이다. 속성 줄 끝에 세미콜론을 붙인다.
- 색은 `#`과 여섯 자리로 적는다. 다른 색을 써도 되지만, 글자색과 배경색이 너무 비슷하면 읽기 어렵다.
- `font-family`의 `system-ui, sans-serif`는 "그 PC의 기본 글꼴, 없으면 아무 고딕"이라는 뜻이다.

### 3. index.html에 link 줄 넣기

`index.html`의 `<title>my-web</title>` 바로 아래에 한 줄을 넣는다. 3주차에 뺐던 줄을 되살리는 것이다.

```html
    <link rel="stylesheet" href="styles.css">
```

**예상 결과** — 새로고침하면 배경이 연한 파랑으로 바뀌고 글꼴이 달라진다. 2단계에서 쓴 규칙이 이제야 화면에 나타난다.

- 규칙을 아무리 잘 써도 **연결하지 않으면 아무 일도 일어나지 않는다.** 이번 주에 가장 자주 나오는 실수다.
- 화면이 안 바뀌면 `href`의 파일 이름을 본다. `style.css`(s 빠짐)로 적으면 파일을 찾지 못한다.
- 앞의 공백은 네 칸이다. 공백 수가 달라도 동작하지만 다른 줄과 맞춰 둔다.

### 4. 제목과 메뉴 색 정하기

`styles.css`의 `body` 규칙 아래에 규칙 세 개를 더한다.

```css
h1 {
  color: #1f3a93;
  font-size: 28px;
}

h2 {
  color: #3157d5;
}

nav a {
  color: #3157d5;
}
```

**예상 결과** — `student01의 웹 연습장`이 진한 남색, `소개`·`취미`가 파랑, 메뉴 링크 세 개가 같은 파랑으로 바뀐다.

- `h1`·`h2`는 태그 선택자다. 그 태그 **전부**가 대상이다.
- `nav a`는 사이를 띄웠다. "`nav` 안에 있는 `a`"라는 뜻이며, `footer` 안에 링크가 생겨도 그것은 바뀌지 않는다.
- 색이 안 바뀌면 선택자 철자를 본다. `H1`·`Nav a`처럼 적어도 동작하지만, 뒤에 나오는 `.card`는 대소문자를 구분한다.

### 5. 카드 class 붙이고 .card 규칙 쓰기

먼저 `index.html`에서 소개 문단 두 개와 취미 목록에 `class="card"`를 붙인다.

```html
      <p class="card">웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p class="card">이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
```

```html
      <ul class="card">
```

여기까지 하면 `index.html` 전체가 아래와 같다. 같은 파일이 [examples/day1/index.html](examples/day1/index.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
    <link rel="stylesheet" href="styles.css">
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

이어서 `styles.css`에 규칙 두 개를 더한다.

```css
.card {
  background-color: #ffffff;
}

footer {
  color: #5a6478;
  text-align: center;
  font-size: 14px;
}
```

**예상 결과** — 문단 두 개와 취미 목록의 배경만 흰색으로 바뀌어 띠처럼 보이고, 맨 아래 한 줄이 회색·가운데로 간다.
아직 테두리도 안여백도 없으므로 카드처럼 보이지는 않는다. 상자로 만드는 일은 2일차다.

여기까지가 1일차 `styles.css`다. 같은 파일이 [examples/day1/styles.css](examples/day1/styles.css)에 있다.

```css
body {
  background-color: #eef2ff;
  color: #17213a;
  font-family: system-ui, sans-serif;
  font-size: 16px;
}

h1 {
  color: #1f3a93;
  font-size: 28px;
}

h2 {
  color: #3157d5;
}

nav a {
  color: #3157d5;
}

.card {
  background-color: #ffffff;
}

footer {
  color: #5a6478;
  text-align: center;
  font-size: 14px;
}
```

- `.card`의 점은 CSS에서만 쓴다. HTML에는 `class="card"`라고 점 없이 적는다.
- `.Card`·`.cards`처럼 한 글자만 달라도 아무 일도 일어나지 않는다. 오류 메시지는 나오지 않는다.
- 흰 배경이 안 보이면 HTML 쪽에 `class="card"`가 들어갔는지부터 본다.

### 6. 나머지 두 페이지에도 link 줄 넣기

`about.html`과 `guestbook.html`의 `<title>` 아래에도 3단계와 **같은 한 줄**을 넣는다.

```html
    <link rel="stylesheet" href="styles.css">
```

`about.html` 전체는 아래와 같다. 3주차 파일에서 이 한 줄만 늘었다. 같은 파일이 [examples/day1/about.html](examples/day1/about.html)에 있다.

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

`guestbook.html`도 마찬가지로 한 줄만 늘었다. 같은 파일이 [examples/day1/guestbook.html](examples/day1/guestbook.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
    <link rel="stylesheet" href="styles.css">
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
      <form>
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
      <p>지금은 눌러도 주소창만 바뀐다. 화면에 띄우는 일은 7주에 한다.</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

**예상 결과** — 세 페이지의 배경색·제목 색·메뉴 색이 같아진다. 메뉴로 오가며 확인한다.
`about.html`의 표와 `guestbook.html`의 입력 칸은 아직 꾸미지 않아 3주차와 같은 모양이다.

- 두 페이지에는 `class="card"`를 붙이지 않는다. 카드는 `index.html`에만 둔다.
- 한 페이지만 안 꾸며지면 그 페이지의 `link` 줄을 본다.

### 7. app.js는 열지 않는다

`app.js`는 이번 주에 **한 글자도 고치지 않는다.** 폴더에 그대로 있는지만 확인한다. 내용은 2주차와 같다.
같은 파일이 [examples/day1/app.js](examples/day1/app.js)에 있다.

```js
const countButton = document.querySelector('#count-button');
const status = document.querySelector('#status');

let clickCount = 0;

countButton.addEventListener('click', () => {
  clickCount += 1;
  status.textContent = `클릭 횟수: ${clickCount}`;
});

console.info('my-web ready');
```

**예상 결과** — 세 페이지 어디에도 `<script>` 줄이 없으므로 이 파일은 실행되지 않는다. 그래서 오류도 나지 않는다.

- 이 파일이 찾는 `#count-button`·`#status`는 3주차에 페이지에서 사라졌다. 5주차에 이 파일을 비우고 다시 쓴다.
- 지우지 않는다. 지운 학생은 2주차 commit에서 되살려야 한다.

### 8. 1일차 끝 루틴

현재 폴더: `my-web`

```bash
git add .
git commit -m "세 페이지에 CSS 연결하고 색 정하기"
git push
```

1. 1분쯤 뒤 `https://student01.github.io/my-web/`을 새로고침한다. 색이 들어간 화면이 보인다. 이 화면은 **확인용**이다.
2. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

**예상 결과**

```text
[main 7c1a0e5] 세 페이지에 CSS 연결하고 색 정하기
 4 files changed, 25 insertions(+), 23 deletions(-)
```

- 앞의 일곱 글자는 PC마다 다르다. 색이나 줄을 교재와 다르게 썼다면 줄 수도 달라진다.
- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.

## 2일차

### 9. 이어서 시작하기

현재 폴더: `my-web`

```bash
git pull
git status
```

**예상 결과** — `Already up to date.`와 `nothing to commit, working tree clean`이 보인다. 오늘도 `styles.css` 한 파일만 고친다.

- 다른 PC라면 1단계의 `git clone`을 한다.
- 1일차 push를 못 했다면 먼저 `git add .` → `git commit` → `git push`를 하고 시작한다.

### 10. 메뉴를 가로로, 카드를 상자로

`styles.css`의 `h2` 규칙과 `nav a` 규칙 사이에 `nav` 규칙을 새로 만든다.

```css
nav {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
```

이어서 `.card` 규칙에 세 줄을 더한다.

```css
.card {
  background-color: #ffffff;
  padding: 16px;
  margin: 12px 0;
  border: 1px solid #c3cbe6;
}
```

**예상 결과** — 메뉴 세 개가 한 줄에 같은 간격(16px)으로 놓이고, 문단과 취미 목록이 **테두리가 있는 흰 상자**가 된다.
상자와 글자 사이가 벌어지고, 상자끼리 위아래로 12px씩 떨어진다.

- `margin: 12px 0`은 위아래 12px, 좌우 0이라는 뜻이다.
- `border: 1px solid #c3cbe6`은 두께·모양·색을 한 줄에 적은 것이다.
- DevTools **Elements › Styles** 맨 아래의 상자 그림에서 `margin`·`border`·`padding` 값을 그대로 볼 수 있다.

### 11. 본문을 가운데로 모으기

`body` 규칙에 세 줄을 더한다.

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
```

**예상 결과** — 넓은 화면에서 본문이 가운데로 모이고 좌우에 빈 공간이 생긴다. 글줄이 640px보다 길어지지 않는다.
화면 가장자리와 글자 사이에도 16px이 생긴다.

- `margin: 0 auto`의 `auto`가 좌우 남는 공간을 반씩 나눠 가진다. 그래서 가운데로 간다.
- `width: 640px`로 적지 않는다. 그러면 640px보다 좁은 화면에서 옆으로 잘려 가로 스크롤이 생긴다.

### 12. @media 세 줄 붙이고 375에서 보기

`styles.css`의 **맨 끝**에 아래 덩어리를 그대로 붙여 넣는다.

```css
@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}
```

그 다음 Chrome에서 확인한다.

1. F12로 DevTools를 연다.
2. **Ctrl+Shift+M**(macOS는 **⌘+⇧+M**)으로 기기 모드를 켠다.
3. 위쪽 폭 칸에 `375`를 치고 Enter를 누른다.

**예상 결과** — 375px에서 메뉴가 `홈`·`내 정보`·`방명록` **세 줄로 세로로 선다.** 폭을 1280으로 되돌리면 다시 한 줄이 된다.
카드 테두리는 두 폭 모두 화면 안에 들어오고 가로 스크롤 막대는 생기지 않는다.

- `@media (max-width: 600px)`는 "화면 폭이 600px 이하일 때만"이라는 뜻이다. 375는 600보다 작으므로 적용된다.
- 괄호 안의 콜론을 빠뜨려 `(max-width 600px)`로 적으면 오류 없이 **이 덩어리 전체가 무시된다.** 375에서도 메뉴가 가로 그대로다.
- 중괄호가 두 겹이다. 맨 끝의 `}`를 빠뜨리지 않는다.

### 13. 입력 칸 폭 정하기

`footer` 규칙 **바로 위**에 규칙 하나를 더한다.

```css
input,
textarea {
  width: 280px;
  max-width: 100%;
}
```

여기까지가 2일차 `styles.css`다. 같은 파일이 [examples/day2/styles.css](examples/day2/styles.css)에 있다.

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
```

**예상 결과** — `guestbook.html`의 이름·이메일 칸과 메시지 칸의 폭이 280px로 같아진다.
기기 모드 375px에서는 `max-width: 100%` 덕분에 칸이 화면 밖으로 나가지 않는다.

- 쉼표로 선택자 두 개를 묶으면 **한 규칙을 두 대상에 함께** 쓴다. 쉼표를 빠뜨리면 `input textarea`가 되어 아무것도 고르지 못한다.
- `width`와 `max-width`를 같이 쓰면 "기본은 280px, 화면이 좁으면 화면에 맞춘다"가 된다.
- `index.html`·`about.html`에는 입력 칸이 없으므로 아무 변화가 없다.

### 14. git restore로 되돌려 보기

일부러 한 줄을 지웠다가 되돌린다. `styles.css`의 `nav` 규칙에서 `gap: 16px;` 한 줄을 지우고 **저장**한다.
새로고침하면 메뉴 사이 간격이 사라진다. 현재 폴더: `my-web`

```bash
git status
git restore styles.css
git status
```

**예상 결과** — 첫 `git status`는 아래와 같다.

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   styles.css

no changes added to commit (use "git add" and/or "git commit -a")
```

`git restore styles.css`는 **아무 말도 하지 않는다.** 두 번째 `git status`가 `nothing to commit, working tree clean`이면 되돌아간 것이다.
VS Code의 `styles.css`로 돌아가면 지웠던 `gap: 16px;`이 다시 있고, 새로고침하면 간격이 돌아온다.

- `git restore <파일>`은 commit하지 않은 수정을 **마지막 commit 상태로** 되돌린다. 되돌린 내용은 돌아오지 않으므로 살릴 것이 없을 때만 쓴다.
- `git add`까지 했다면 `git status`에 `(use "git restore --staged <file>..." to unstage)`가 보인다. `git restore --staged styles.css`로 add만 취소한다(파일 내용은 그대로다).
- `error: pathspec 'style.css' did not match any file(s) known to git`이 나오면 파일 이름을 잘못 적은 것이다.

### 15. 제출하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "박스와 반응형 규칙 넣기"
git push
```

1. 1분쯤 뒤 `https://student01.github.io/my-web/`을 새로고침한다.
2. F12 → 기기 모드(**Ctrl+Shift+M**) → 폭 `375`.
3. 메뉴가 세로로 서고 카드에 테두리가 보이면 **주소창과 폭 375 표시가 함께 보이게** 화면을 캡처한다. 이 한 장이 이번 주 제출물이다.
4. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 아이디는 보여도 된다.

## 오류가 나면

CSS는 틀려도 **빨간 오류 줄이 나오지 않는다.** 그냥 아무 일도 일어나지 않는다. 그래서 순서대로 본다.

1. `index.html`에 `link` 줄이 있는가, 파일 이름이 `styles.css`가 맞는가.
2. 선택자 철자와 대소문자가 HTML과 같은가(`class="card"` ↔ `.card`).
3. 속성 이름과 줄 끝 세미콜론, 중괄호 짝이 맞는가.
4. DevTools **Elements › Styles**에서 그 요소에 내 규칙이 보이는가.

자주 나오는 증상과 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 새로고침하고, 해결되지 않으면 화면을 그대로 보여 주고 도움을 요청한다.
