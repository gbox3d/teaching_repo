# 3주차 따라하기 — 세 페이지 자기소개 사이트 만들기

처음에는 그대로 따라 하고, 결과가 나오면 본인 아이디와 문구로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

이번 주에는 HTML만 쓴다. `styles.css`와 `app.js`는 폴더에 그대로 두고 `index.html`에서 연결 줄만 뺀다.
화면이 꾸며지지 않은 채로 보이는 것이 정상이다. 꾸미기는 4주차, 동작은 5주차에 한다.

## 1일차

### 1. 저장소 받아오기

지난주에 쓰던 PC라면 폴더를 열고 새 commit만 받아 온다. 현재 폴더: `my-web`

```bash
git pull
```

**예상 결과** — 집에서 push한 것이 없으면 `Already up to date.` 한 줄이다.

처음 쓰는 PC라면 저장소를 통째로 내려받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

**예상 결과** — `Cloning into 'my-web'...`로 시작하고 `my-web` 폴더가 생긴다. **File › Open Folder**로 그 폴더를 연다.

- `fatal: destination path 'my-web' already exists and is not an empty directory.`가 나오면 그 자리에 이미 폴더가 있는 것이다. 그 폴더를 열고 `git pull`을 한다.
- 로그인이 막혀 clone이 안 되면 조교에게 2주차 `examples/day2` 파일을 받아 새 폴더에서 작업하고, 끝 루틴에서 `git remote add origin <URL>` 뒤에 push한다.

### 2. index.html 비우고 뼈대 만들기

`index.html`을 열면 2주차 내용이 들어 있다. **`<body>` 안을 모두 지우고**, `<head>` 안의 아래 두 줄도 지운다.

```html
<link rel="stylesheet" href="styles.css">
<script src="app.js" defer></script>
```

지운 자리에 뼈대 네 개를 만든다. 아직 글자는 넣지 않는다.

```html
<body>
  <header>
  </header>
  <main>
  </main>
  <footer>
  </footer>
</body>
```

**예상 결과** — 브라우저에서 새로고침하면 **아무것도 없는 흰 화면**이다. 카드와 버튼이 사라졌으면 제대로 지운 것이다.

- `styles.css`와 `app.js` **파일 자체는 지우지 않는다.** 연결 줄만 뺐다.
- `<title>my-web</title>`과 `<meta>` 두 줄은 그대로 둔다.

### 3. 제목과 소개 문단 쓰기

`header` 안에 `h1`을, `main` 안에 `h2`와 문단을 넣는다.

```html
    <header>
      <h1>student01의 웹 연습장</h1>
    </header>
    <main>
      <h2>소개</h2>
      <p>웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p>이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
    </main>
```

**예상 결과** — 큰 글씨 제목 한 줄, 그 아래 조금 작은 `소개`, 문단 두 줄이 보인다. `student01`만 굵게 보인다.

- `h1`은 페이지에 하나만 둔다. 그 아래 묶음이 `h2`다.
- 글자를 크게 하려고 `h1`을 더 쓰지 않는다. 크기는 4주차에 CSS로 정한다.

### 4. 프로필 그림과 nav 링크 넣기

1. `my-web` 폴더 안에 `images` 폴더를 만들고, 그 안에 [examples/day1/images/profile.png](examples/day1/images/profile.png)를 내려받아 넣는다.
   (파일 화면 오른쪽 위 **Download raw file**을 누른다. 파일 이름은 `profile.png` 그대로 둔다.)
2. `h1` 아래에 `nav`를, `h2 소개` 아래에 `img`를 넣는다.

```html
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
      </nav>
```

```html
      <img src="images/profile.png" alt="student01의 프로필 그림" width="160">
```

**예상 결과** — 제목 아래에 파란 링크 두 개(`홈`·`내 정보`)가 나란히 보이고, `소개` 아래에 동그란 사람 그림이 보인다.
`내 정보`를 누르면 2주차에 만든 `about.html`(카드 화면)이 열린다.

- 그림 자리에 `student01의 프로필 그림`이라는 **글자만** 보이면 경로가 틀린 것이다. `images/profile.png`의 철자와 폴더 위치를 본다.
- 같은 폴더의 파일은 파일 이름만 적는다. 2주차 `about.html` 링크와 같은 방식이다.

### 5. 취미 목록과 footer 넣기

문단 아래에 `h2`와 목록을, `footer` 안에 한 줄을 넣는다.

```html
      <h2>취미</h2>
      <ul>
        <li>사진 찍기</li>
        <li>보드게임</li>
        <li>저녁 산책</li>
      </ul>
```

```html
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
```

여기까지 하면 `index.html` 전체가 아래와 같다. 같은 파일이 [examples/day1/index.html](examples/day1/index.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
  </head>
  <body>
    <header>
      <h1>student01의 웹 연습장</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
      </nav>
    </header>
    <main>
      <h2>소개</h2>
      <img src="images/profile.png" alt="student01의 프로필 그림" width="160">
      <p>웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p>이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
      <h2>취미</h2>
      <ul>
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

**예상 결과** — 제목 · 링크 두 개 · `소개` · 그림 · 문단 두 줄 · `취미` · 점 세 개 목록 · 맨 아래 한 줄이 차례로 보인다.
취미 세 줄 앞에 점(•)이 붙으면 `ul`·`li`가 맞게 들어간 것이다.

### 6. styles.css와 app.js는 그대로 둔다

두 파일은 이번 주에 **한 글자도 고치지 않는다.** 폴더에 그대로 있는지만 확인한다. 내용은 2주차와 같다.

`styles.css` — 같은 파일이 [examples/day1/styles.css](examples/day1/styles.css)에 있다.

```css
body {
  min-height: 100vh;
  margin: 0;
  display: grid;
  place-items: center;
  font-family: system-ui, sans-serif;
  color: #17213a;
  background: #eef2ff;
}

.card {
  width: min(36rem, calc(100% - 2rem));
  padding: 2rem;
  border-radius: 1rem;
  background: white;
  box-shadow: 0 1rem 2.5rem rgb(30 50 100 / 12%);
}

.eyebrow {
  color: #3157d5;
  font-weight: 700;
}

button {
  padding: 0.7rem 1rem;
  border: 0;
  border-radius: 0.5rem;
  color: white;
  background: #3157d5;
}
```

`app.js` — 같은 파일이 [examples/day1/app.js](examples/day1/app.js)에 있다.

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

`about.html`도 아직 2주차 그대로다. 이 파일은 2일차에 다시 쓴다. 같은 파일이 [examples/day1/about.html](examples/day1/about.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 소개</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <main class="card">
      <p class="eyebrow">Week 02 · about 브랜치</p>
      <h1>소개</h1>
      <p>student01의 웹프로그래밍 연습 페이지입니다.</p>
      <p><a href="index.html">첫 페이지로 돌아가기</a></p>
    </main>
  </body>
</html>
```

**예상 결과** — `index.html`은 꾸며지지 않은 화면, `about.html`은 2주차의 카드 화면이다. 두 화면이 달라 보이는 것이 정상이다.

- `index.html`에서 `link` 줄을 뺐기 때문에 `styles.css`가 `index.html`에는 적용되지 않는다. `about.html`에는 아직 연결이 남아 있다.
- 4주차에 `styles.css`를 비우고 다시 써서 세 페이지에 모두 연결한다.

### 7. 1일차 끝 루틴

현재 폴더: `my-web`

```bash
git add .
git commit -m "자기소개 페이지 만들기"
git push
```

**예상 결과**

```text
[main 32b2716] 자기소개 페이지 만들기
 2 files changed, 21 insertions(+), 9 deletions(-)
 create mode 100644 images/profile.png
```

1. 1분쯤 뒤 `https://student01.github.io/my-web/`을 새로고침한다. 방금 만든 자기소개 화면이 보인다. 이 화면은 **확인용**이다.
2. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- `nothing to commit, working tree clean`이 나오면 파일을 저장하지 않은 것이다. VS Code 탭 제목의 ● 표시를 본다.

## 2일차

### 8. guestbook 브랜치 만들기

현재 폴더: `my-web`

```bash
git pull
git switch -c guestbook
```

**예상 결과**

```text
Switched to a new branch 'guestbook'
```

- `git switch -c <이름>`은 2주차의 `git branch <이름>` + `git switch <이름>`을 한 줄로 한 것이다.
- `fatal: a branch named 'guestbook' already exists`가 나오면 이미 만든 것이다. `-c`를 빼고 `git switch guestbook`만 한다.
- `git branch`를 치면 `* guestbook`이 보인다. 지금부터의 commit은 이 브랜치에 쌓인다.

### 9. about.html을 내 정보 표로 다시 쓰기

`about.html`을 열고 **전체를 지운 뒤** 아래 내용을 넣는다. 2주차 카드 내용과 `link` 줄은 남기지 않는다.
같은 파일이 [examples/day2/about.html](examples/day2/about.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
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

**예상 결과** — `내 정보` 제목, 링크 세 개, `한눈에 보기` 아래에 2열 4행 표가 보인다.
첫 줄의 `항목`·`내용`은 굵은 글씨에 가운데 정렬로 보이고, 나머지 줄은 보통 글씨다. `th`와 `td`의 차이다.

- 표에 선이 없는 것이 정상이다. 선은 4주차에 CSS로 그린다.
- 표에 실제 이메일·학번·전화번호를 넣지 않는다. 수업용 가상 정보를 쓴다.
- `방명록` 링크는 아직 파일이 없어 눌러도 열리지 않는다. 10단계에서 만든다.

### 10. guestbook.html 만들기

탐색기의 **New File** 아이콘으로 `guestbook.html`을 만들고 아래 내용을 넣는다.
같은 파일이 [examples/day2/guestbook.html](examples/day2/guestbook.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
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

**예상 결과** — `방명록` 제목, `쓰는 순서` 아래 1·2·3 번호 목록, 그 아래 `이름`·`이메일`·`메시지` 입력 칸과 **남기기** 버튼이 보인다.
`이름`이라는 글자를 눌러 보면 옆 입력 칸에 커서가 들어간다. `label`의 `for`와 `input`의 `id`가 같기 때문이다.

- **남기기**를 누르면 화면은 그대로이고 주소창만 `…/guestbook.html?`로 바뀐다. 아직 아무 일도 일어나지 않는 것이 정상이다.
  적은 글을 화면에 띄우는 일은 7주차에 JavaScript로 한다.
- 커서가 들어가지 않으면 `for="name"`과 `id="name"`의 철자를 대소문자까지 비교한다.

### 11. 세 페이지 nav 통일하기

`index.html`의 `nav`에 `방명록` 한 줄을 더해 세 페이지의 메뉴를 같게 만든다.

```html
        <a href="guestbook.html">방명록</a>
```

`index.html` 전체는 아래와 같다. 1일차 파일에서 이 한 줄만 늘었다. 같은 파일이 [examples/day2/index.html](examples/day2/index.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
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
      <p>웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p>이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
      <h2>취미</h2>
      <ul>
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

**예상 결과** — 세 페이지 어디서나 `홈`·`내 정보`·`방명록`이 같은 자리에 보이고, 눌러서 세 페이지를 오갈 수 있다.

- 링크가 404면 파일 이름의 철자와 대소문자를 본다. 내 PC에서는 `Guestbook.html`로 적어도 열리지만, 공개 주소(GitHub Pages)에서는 404가 된다.
- `about.html`과 `guestbook.html`의 `nav`는 9·10단계에서 이미 세 줄로 넣었다.

### 12. main에 merge하고 push 하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "방명록 페이지 추가"
git switch main
git merge guestbook
git push
```

**예상 결과**

```text
[guestbook 9bd9ddb] 방명록 페이지 추가
 3 files changed, 80 insertions(+), 7 deletions(-)
 create mode 100644 guestbook.html
```

`git switch main`은 먼저 `Switched to branch 'main'`과 `Your branch is up to date with 'origin/main'.` 두 줄을 보여 준다. 이어서 merge 결과가 나온다.

```text
Updating 32b2716..9bd9ddb
Fast-forward
 about.html     | 40 +++++++++++++++++++++++++++++++++-------
 guestbook.html | 46 ++++++++++++++++++++++++++++++++++++++++++++++
 index.html     |  1 +
 3 files changed, 80 insertions(+), 7 deletions(-)
 create mode 100644 guestbook.html
```

- `git switch main` 직후 탐색기에서 `guestbook.html`이 잠시 사라진다. 2주차와 같다. merge 뒤 돌아온다.
- 앞의 일곱 글자(`9bd9ddb`)는 PC마다 다르다.
- 합친 브랜치는 `git branch -d guestbook`으로 지워도 되고 두어도 된다.

### 13. 제출하기

1. 1분쯤 뒤 `https://student01.github.io/my-web/guestbook.html`을 새로고침한다.
2. 메뉴에 `홈`·`내 정보`·`방명록` 세 링크가 보이고 입력 칸과 **남기기** 버튼이 보이면 된다.
3. **주소창이 함께 보이게** 화면 전체를 캡처한다. 이 한 장이 이번 주 제출물이다.

캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 아이디는 보여도 된다.

## 오류가 나면

먼저 터미널의 **첫 `error:` 또는 `fatal:` 줄**을 읽는다. `hint:` 줄은 git이 알려 주는 해결 방법이다.
브라우저 화면이 이상하면 그림·링크의 경로부터 본다. 자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 실행하고, 해결되지 않으면 화면을 그대로 보여 주고 도움을 요청한다.
