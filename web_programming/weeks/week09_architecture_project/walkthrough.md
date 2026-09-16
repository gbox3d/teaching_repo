# 9주차 따라하기 — 발표 준비와 README 1차판

처음에는 그대로 따라 하고, 결과가 나오면 본인 아이디와 문구로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

이번 주에는 `my-web`의 HTML·CSS·JavaScript를 **고치지 않는다.** 새로 만드는 것은 `README.md`와 `screenshots/` 폴더의 캡처 두 장이다.
1일차 작업은 `readme` 브랜치에 쌓았다가 main에 합친다. 2일차는 발표다.

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

- `fatal: destination path 'my-web' already exists and is not an empty directory.`가 나오면 이미 받아 둔 것이다. 그 폴더를 열고 `git pull`을 한다.
- 8주차에 만든 `exam/` 폴더도 함께 받아진다. 이번 주에는 열지 않는다.

### 2. readme 브랜치 만들기

오늘 작업할 브랜치를 만들면서 그 브랜치로 옮겨 간다. 현재 폴더: `my-web`

```bash
git status
git switch -c readme
git branch
```

**예상 결과**

```text
Switched to a new branch 'readme'
  main
* readme
```

- 시작 전 `git status`가 `nothing to commit, working tree clean`이어야 한다. 아니면 먼저 commit한다.
- `-c`는 "만들면서 옮겨 가라"는 뜻이다. 3주차 `guestbook`, 6주차 `dark-mode`와 같은 명령이다.
- `git branch`는 이름을 알파벳 순으로 보여 준다. 줄 앞의 `*`가 지금 있는 브랜치다.
- `fatal: a branch named 'readme' already exists`가 나오면 이미 만든 것이다. `git switch readme`로 옮겨 간다.
- 지금부터의 commit이 `readme`에 쌓인다. main과 공개 페이지는 그대로다.

### 3. 홈 화면 세 파일 확인하기

발표에서 가장 먼저 보여 줄 화면이다. `index.html`을 더블클릭해 열고 **[인사 바꾸기]**를 눌러 본다.
문장이 바뀌고 `클릭 1회`가 되면 다음 단계로 간다.

아래는 7주차 끝의 완성본이고 9주차에는 **한 글자도 고치지 않는다.** 내 파일이 이것과 달라도 화면과 동작이 같으면 그대로 발표하면 된다.
파일이 없거나 열리지 않는 학생만 아래 내용을 그대로 넣어 오늘 발표를 준비한다.

`index.html` (같은 파일이 [examples/day1/index.html](examples/day1/index.html)에 있다):

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

`styles.css` (같은 파일이 [examples/day1/styles.css](examples/day1/styles.css)에 있다):

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

`app.js` (같은 파일이 [examples/day1/app.js](examples/day1/app.js)에 있다):

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

**예상 결과** — 카드 안에 인사말이 보이고, **[인사 바꾸기]**를 누르면 `반갑습니다. 오늘도 좋은 하루 되세요.`로 바뀌며 `클릭 1회`가 된다.
**[다크 모드]**를 누르면 배경이 어두워진다. F12 **Console**에 빨간 줄이 없다.

- 인사말은 시각에 따라 `좋은 아침입니다.`나 `좋은 오후입니다.`로 달라진다. 정상이다.
- 발표에서는 **[인사 바꾸기]** 하나만 눌러도 된다. 다크 모드는 선택이다.
- 눌러도 아무 일이 없으면 Console 첫 빨간 줄을 읽는다. 6주차에 본 `null` 오류가 대부분이다.

### 4. 내 정보와 방명록 확인하기

나머지 두 페이지도 열어 본다. 방명록에서는 이름과 메시지를 넣고 **[남기기]**를 눌러 한 줄이 보이는지,
이름을 비우고 누르면 안내가 보이는지 두 가지를 모두 해 본다.

`about.html` (같은 파일이 [examples/day1/about.html](examples/day1/about.html)에 있다):

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

`guestbook.html` (같은 파일이 [examples/day1/guestbook.html](examples/day1/guestbook.html)에 있다):

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
      <h3>마지막으로 남긴 글</h3>
      <p class="card" id="last">아직 남긴 글이 없습니다.</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`guestbook.js` (같은 파일이 [examples/day1/guestbook.js](examples/day1/guestbook.js)에 있다):

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const last = document.querySelector('#last');

function clearNotice() {
  notice.textContent = '';
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
  last.textContent = `${name}: ${message}`;
  form.reset();
  nameInput.focus();
});

nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
```

**예상 결과** — `about.html`에 4행짜리 표가 보인다. `guestbook.html`에서 이름 `student01`, 메시지 `첫 방명록입니다.`를 넣고
**[남기기]**를 누르면 **마지막으로 남긴 글** 아래에 `student01: 첫 방명록입니다.`가 보이고 입력 칸이 비워진다.
이름을 비우고 누르면 `이름을 입력하세요.`가 보인다.

- nav 링크 세 개로 세 페이지를 모두 오갈 수 있어야 한다. 404가 나면 파일 이름의 대소문자를 본다.
- 이메일 칸은 비워 두어도 된다. 빈값 안내는 이름과 메시지 두 칸에만 있다.
- 새로고침하면 남긴 글이 사라진다. 정상이다. 남게 하는 것은 11주차다.

### 5. 화면 두 장 캡처해 screenshots 폴더에 넣기

1. VS Code 탐색기에서 `my-web` 아래에 새 폴더 `screenshots`를 만든다.
2. 브라우저에서 `index.html`을 열고 **[인사 바꾸기]**를 한 번 누른 뒤 화면을 캡처한다.
   - Windows: **Win+Shift+S** → 영역을 끌어 선택 → 그림판 등에 붙여 넣고 저장
   - macOS: **⌘+Shift+4** → 영역을 끌어 선택하면 바탕화면에 저장
3. 저장한 파일을 `screenshots/home.png`로 옮긴다.
4. `guestbook.html`에서 한 줄 남긴 뒤 화면을 같은 방법으로 캡처해 `screenshots/guestbook.png`로 옮긴다.

**예상 결과** — 탐색기의 `my-web/screenshots/` 안에 `home.png`와 `guestbook.png` 두 개가 보인다.
같은 자리에 있는 예시가 [examples/day1/screenshots/home.png](examples/day1/screenshots/home.png)와
[examples/day1/screenshots/guestbook.png](examples/day1/screenshots/guestbook.png)다.

- **동작한 뒤의 화면**을 찍는다. `클릭 0회`나 `아직 남긴 글이 없습니다.`인 캡처는 눌러 보지 않은 것으로 보인다.
- 파일 이름은 영문 소문자로 한다. 한글이나 공백이 들어간 이름은 README 링크에서 깨지기 쉽다.
- 캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 브라우저 탭에 다른 사이트가 보이면 닫고 다시 찍는다.

### 6. README 1차판 쓰기

저장소 맨 위(`my-web` 폴더 바로 아래)에 `README.md`를 만든다. 7주차에 GitHub 웹에서 만든 짧은 README가 있으면 **내용을 모두 지우고** 다시 쓴다.
다섯 항목을 아래 순서로 쓴다.

```text
# my-web — student01의 웹 연습장     사이트 이름 한 줄
## 공개 주소                         Pages 주소를 링크로 한 줄
## 페이지                            세 페이지를 링크 목록으로 세 줄
## 기능                              버튼 한 줄, 폼 한 줄
## 화면                              캡처 두 장을 링크로 두 줄
## 이번에 배운 것                    세 줄
```

전체 예시(29줄)는 [examples/day1/README.md](examples/day1/README.md)에 있다. GitHub 파일 화면의 **Raw**를 눌러 그대로 복사한 뒤
`student01`과 주소를 본인 것으로 바꾼다. 쓰는 마크다운은 세 가지뿐이다.

```text
# 제목                                            제목. #과 글자 사이를 한 칸 띄운다
- 항목                                            목록 한 줄
[공개 주소](https://student01.github.io/my-web/)  링크. 소괄호 안이 주소다
```

**예상 결과** — VS Code에서 `README.md`를 열고 오른쪽 위 미리 보기 아이콘(**Open Preview**)을 누르면 제목·목록·링크가 렌더된 화면이 보인다.

- 소괄호 안에는 인터넷 주소도 넣고, 같은 저장소 안의 파일이면 `index.html`이나 `screenshots/home.png`처럼 **파일 이름만** 넣는다.
- `#` 뒤에는 **띄어쓰기 한 칸**이 있어야 한다. `#제목`은 그냥 글자로 보인다.
- `student01`과 주소를 그대로 두면 예시를 베낀 것으로 보아 레포트 점수가 깎인다.
- 실명·학번·전화번호·실제 이메일을 쓰지 않는다.

### 7. commit하고 readme 브랜치 push 하기

현재 폴더: `my-web`

```bash
git status
git add .
git commit -m "README 1차판과 화면 캡처 2장"
git push -u origin readme
```

**예상 결과** — `git status`에 아직 올리지 않은 것 두 가지가 보인다. `README.md`는 7주차에 만들어 둔 파일을 고친 것이라 `modified`로,
`screenshots/`는 오늘 새로 만든 폴더라 `Untracked files`로 나온다.

```text
On branch readme
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	screenshots/

no changes added to commit (use "git add" and/or "git commit -a")
```

commit과 push는 아래와 같다.

```text
[readme 1f74687] README 1차판과 화면 캡처 2장
 3 files changed, 26 insertions(+), 5 deletions(-)
 create mode 100644 screenshots/guestbook.png
 create mode 100644 screenshots/home.png
```

```text
 * [new branch]      readme -> readme
branch 'readme' set up to track 'origin/readme'.
```

- 앞의 일곱 글자(`1f74687`)와 줄 수는 PC마다 다르다. 파일이 세 개면 맞다.
- `create mode`는 **새로 생긴 파일**에만 붙는다. `README.md`는 7주차에 만든 파일을 고쳐 쓴 것이라 그 줄이 없고, 지운 8줄이 `deletions(-)`로 함께 세어진다.
- 7주차에 README를 만들지 않았다면 `README.md`도 새 파일이라 `create mode` 줄이 하나 더 나오고 `deletions(-)`가 없다. 둘 다 정상이다.
- 처음 올리는 브랜치라 `-u`를 붙인다. 빠뜨리면 `fatal: The current branch readme has no upstream branch.`가 나고,
  git이 바로 아래 줄에 `git push --set-upstream origin readme`를 알려 준다. `-u`가 그것과 같은 뜻이다.
- 지금 GitHub 저장소의 브랜치 드롭다운에 `readme`가 생긴다. 공개 페이지는 아직 그대로다.

### 8. main에 합치고 저장소 첫 화면 확인하기

현재 폴더: `my-web`

```bash
git switch main
git merge readme
git push
```

**예상 결과** — `git switch main` 직후 탐색기에서 `screenshots/`가 사라지고 `README.md`는 7주차에 만든 8줄판으로 돌아간다. 정상이다. merge하면 1차판이 돌아온다.

```text
Updating cf4dee7..1f74687
Fast-forward
 README.md                 |  31 ++++++++++++++++++++++++++-----
 screenshots/guestbook.png | Bin 0 -> 32691 bytes
 screenshots/home.png      | Bin 0 -> 44474 bytes
 3 files changed, 26 insertions(+), 5 deletions(-)
 create mode 100644 screenshots/guestbook.png
 create mode 100644 screenshots/home.png
```

1. `https://github.com/student01/my-web`을 새로고침한다.
2. 파일 목록 아래에 README가 렌더되어 보인다. 이 화면이 **제출 캡처 1장**이다.
3. `## 화면`의 링크 두 개를 눌러 캡처가 열리는지 확인한다.

- `Bin 0 -> 32691 bytes`는 그림 파일이라 줄 수 대신 크기가 나오는 것이다. 숫자는 캡처마다 다르다.
- README가 첫 화면에 안 보이면 파일이 저장소 맨 위에 있는지, 이름이 `README.md`인지 본다.
- 캡처 링크가 404면 `screenshots/` 폴더가 push되지 않았거나 파일 이름의 대소문자가 다른 것이다.

### 9. 브랜치 지우기

합친 브랜치는 내 PC와 GitHub 두 곳에서 각각 지운다. 현재 폴더: `my-web`

```bash
git branch -d readme
git push origin --delete readme
git branch
```

**예상 결과**

```text
Deleted branch readme (was 1f74687).
```

```text
 - [deleted]         readme
```

```text
* main
```

- `git branch -d`는 **내 PC**, `git push origin --delete`는 **GitHub**다. 한쪽만 하면 다른 쪽에 이름이 남는다.
- 지워도 commit은 main에 남아 있다. 지우는 것은 이름표뿐이다. 저장소 첫 화면의 README가 그대로 있는 것을 확인한다.
- `error: the branch 'readme' is not fully merged`가 나오면 7단계 push도 8단계 merge도 하지 않은 것이다. `-D`(대문자)는 쓰지 않는다.
- 7단계 push를 이미 했다면 지우기가 그냥 되고 `warning: deleting branch 'readme' that has been merged to 'refs/remotes/origin/readme', but not yet merged to HEAD`만 나온다. 이때는 `git branch readme origin/readme`로 되살린 뒤 8단계를 한다.
- 같은 `--delete` 명령을 두 번 치면 `error: unable to delete 'readme': remote ref does not exist`가 난다. 이미 지워진 것이다.

### 10. 2분 리허설 해 보기

짝과 번갈아 한 번씩 2분을 재며 해 본다. 순서는 아래와 같다.

```text
0:00  공개 주소를 열고 한 줄 소개
0:20  nav로 세 페이지 이동
0:50  홈에서 [인사 바꾸기] 클릭
1:10  방명록에 이름·메시지를 넣고 [남기기]
1:30  이름을 비우고 [남기기] → 안내 문장
1:40  GitHub Commits 탭과 README
```

**예상 결과** — 2분 안에 여섯 줄이 모두 끝난다. 넘치면 어디를 줄일지 정한다. 대개 첫 소개가 길다.

- 말하면서 누른다. 누르고 나서 설명하면 시간이 두 배가 된다.
- 주소를 치는 시간도 2분에 들어간다. 탭을 미리 열어 두는 이유다.

## 2일차

### 11. 발표 전 탭 세 개 준비하기

자기 차례 두 사람 앞에서 브라우저 탭 세 개를 연다.

```text
탭 1  https://student01.github.io/my-web/
탭 2  https://github.com/student01/my-web
탭 3  https://github.com/student01/my-web/commits
```

**예상 결과** — 세 탭이 모두 열려 있고, 탭 1은 홈 화면이 처음 상태(`클릭 0회`)다.

- 방명록은 비워 둔 상태로 시작한다. 발표 중에 직접 한 줄 남기는 것이 폼 점수다.
- 다크 모드를 켜 두었으면 끄고 시작한다. 첫 화면이 밝아야 글씨가 잘 보인다.
- 다른 사이트나 로그인 화면이 보이는 탭은 닫는다.

### 12. 2분 시연 순서대로 해 보기

10단계에서 연습한 여섯 줄을 그대로 한다. 말하면서 누른다.

1. 탭 1을 보이며 "`student01`의 웹 연습장입니다. 세 페이지가 있습니다."
2. nav로 홈 → 내 정보 → 방명록 → 홈.
3. **[인사 바꾸기]**를 누르며 "버튼을 누르면 문장이 바뀌고 클릭 횟수가 오릅니다."
4. 방명록에서 이름·메시지를 넣고 **[남기기]**.
5. 이름을 비우고 **[남기기]** → 안내 문장.
6. 탭 3의 **Commits** 탭과 탭 2의 README를 보이며 마무리.

**예상 결과** — 2분 안에 끝나고, 채점자가 여섯 가지를 모두 화면에서 확인한다.

- 코드 파일은 띄우지 않는다. 구술 질문("이 버튼을 누르면 어느 파일이 실행됩니까?")을 받으면 그때 연다.
- 잘 안 되는 기능이 있으면 되는 것부터 보여 주고 남은 시간에 말한다.
- 공개 주소가 열리지 않으면 탭 3의 **Commits** 탭과 내 PC 화면으로 대신한다. 손을 들어 알린다.

### 13. 발표가 끝나면

1. 남의 발표를 들으며 채점표를 본다. 자기 코드는 고치지 않는다.
2. 마지막 5분에 README를 고칠 것이 있으면 고쳐 올린다. 현재 폴더: `my-web`

```bash
git add .
git commit -m "README 다듬기"
git push
```

3. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

**예상 결과** — `git status`가 `nothing to commit, working tree clean`이고, 저장소 첫 화면에 최종 README가 보인다.

- 고칠 것이 없으면 `nothing to commit, working tree clean`이 나온다. 그것도 정상이다.
- 제출은 발표 2분과 캡처 1장(저장소 첫 화면)이다. 제출 위치와 마감은 수업 공지를 따른다.

## 오류가 나면

터미널에서는 첫 `error:` 또는 `fatal:` 줄을 읽는다. `hint:` 줄은 git이 알려 주는 해결 방법이다.
브라우저에서는 F12 **Console**의 첫 빨간 줄을 읽는다. 줄 끝의 `app.js:7`이 파일 이름과 줄 번호다.
자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 실행하고, 해결되지 않으면 화면을 그대로 보여 주고 도움을 요청한다.
