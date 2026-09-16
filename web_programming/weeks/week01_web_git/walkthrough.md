# 1주차 따라하기 — 세 파일 만들기와 첫 commit 세 개

처음에는 그대로 따라 하고, 결과가 나오면 본인 소개 문구로 바꾼다.
각 단계의 **예상 결과**가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 예시 별칭이다. 파일과 캡처에 실명·학번·전화번호를 넣지 않는다.
이번 주에는 서버를 켜지 않는다. 페이지는 파일을 더블클릭해 `file://` 주소로 연다.
2일차 명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.

## 1일차

### 1. 연습 폴더 만들고 VS Code로 열기

1. 문서(Documents)처럼 찾기 쉬운 위치에 새 폴더 `week01`을 만든다.
2. VS Code에서 **File › Open Folder**로 `week01` 폴더를 연다.

**예상 결과** — 왼쪽 탐색기(EXPLORER) 맨 위에 `WEEK01`이 보이고 그 아래는 비어 있다.

### 2. 세 파일 만들기

탐색기의 **New File** 아이콘으로 `index.html`, `styles.css`, `app.js`를 만들고 아래 내용을 그대로 넣는다.
파일 이름은 한 글자도 다르면 안 된다. 붙여 넣은 뒤 `Ctrl+S`(macOS `⌘S`)로 저장한다.

`index.html` — `<h1>`과 소개 문단은 5단계에서 내 소개로 고친다:

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>week01</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <main class="card">
      <p class="eyebrow">Week 01 · HTML · CSS · JavaScript</p>
      <h1>여기에 내 소개 제목을 씁니다</h1>
      <p>여기에 나를 소개하는 한 문장을 씁니다.</p>
      <button id="count-button" type="button">눌러 보기</button>
      <p id="status">클릭 횟수: 0</p>
    </main>
  </body>
</html>
```

`styles.css` (같은 파일이 [examples/day1/styles.css](examples/day1/styles.css)에 있다):

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

`app.js` (같은 파일이 [examples/day1/app.js](examples/day1/app.js)에 있다). 붙여 넣고 **읽기만** 한다:

```js
const countButton = document.querySelector('#count-button');
const status = document.querySelector('#status');

let clickCount = 0;

countButton.addEventListener('click', () => {
  clickCount += 1;
  status.textContent = `클릭 횟수: ${clickCount}`;
});

console.info('week01 ready');
```

**예상 결과** — 탐색기에 세 파일이 나란히 보이고, 탭 제목의 ●(저장 안 됨) 표시가 모두 사라진다.

### 3. 브라우저로 열어 보기

1. 탐색기에서 `index.html`을 오른쪽 클릭 → **Reveal in File Explorer**(macOS는 **Reveal in Finder**).
2. 열린 폴더에서 `index.html`을 더블클릭한다.

**예상 결과** — 연한 파란 배경에 흰 카드 한 장이 열린다. 제목과 문단, **눌러 보기** 버튼, `클릭 횟수: 0`이 보인다.
버튼을 두 번 누르면 `클릭 횟수: 2`가 된다.

**확인** — 새로고침(`F5`)하면 다시 `클릭 횟수: 0`이다. 숫자는 페이지를 다시 읽으면 처음부터 시작한다.

### 4. 주소창 읽기 — file://

주소창을 한 번 클릭해 주소 전체를 본다.

```text
file:///C:/Users/student01/Documents/week01/index.html   (Windows)
file:///Users/student01/Documents/week01/index.html      (macOS)
```

- 맨 앞 `file`이 scheme이다. 내 PC의 파일을 그대로 여는 방식이라 서버를 거치지 않는다.
- 교재 사이트 주소 `https://gbox3d.github.io/teaching_repo/webprg/`와 비교한다.
  `https`는 인터넷의 서버(`gbox3d.github.io`)에서 받아 온다는 뜻이고, 그 뒤가 서버 안에서의 위치(path)다.

**예상 결과** — 내 주소는 `file:///`로 시작하고 폴더 이름 `week01`과 파일 이름 `index.html`이 그대로 들어 있다.

### 5. 내 소개로 고치고 저장하기

1. `index.html`의 `<h1>`과 바로 아래 `<p>`를 본인 소개로 바꾼다. 실명 대신 `student01` 같은 수업용 별칭을 쓴다.
2. `Ctrl+S`로 저장하고 브라우저에서 `F5`로 새로고침한다.

전체 파일은 아래와 같다. 같은 파일이 [examples/day1/index.html](examples/day1/index.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>week01</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <main class="card">
      <p class="eyebrow">Week 01 · HTML · CSS · JavaScript</p>
      <h1>안녕하세요, student01입니다</h1>
      <p>웹프로그래밍 수업에서 만든 첫 페이지입니다.</p>
      <button id="count-button" type="button">눌러 보기</button>
      <p id="status">클릭 횟수: 0</p>
    </main>
  </body>
</html>
```

**예상 결과** — 카드의 제목과 문단이 내가 쓴 내용으로 바뀐다.
그대로면 저장(탭의 ●)과 새로고침을 확인한다. 저장하지 않으면 브라우저는 옛 내용을 계속 보여 준다.

### 6. DevTools Elements와 Console 보기

1. 브라우저에서 `F12`(macOS는 `⌥⌘I`)로 DevTools를 연다.
2. **Elements** 탭에서 `<h1>`을 찾아 내가 쓴 문장이 들어 있는지 본다.
3. **Console** 탭을 연다.
4. 버튼을 누르고 Elements에서 `<p id="status">`의 글자가 바뀌는 것을 본다.

**예상 결과** — Console에 `week01 ready` 한 줄이 있다(`app.js`가 남긴 메시지다).
버튼을 누르면 Elements의 `<p id="status">` 안 글자가 `클릭 횟수: 1`, `클릭 횟수: 2`로 바뀐다.
`index.html` 파일 자체는 그대로다. 화면에 보이는 HTML만 바뀐 것이다.

### 7. 교재 사이트에서 200과 404 보기

1. 새 탭에서 https://gbox3d.github.io/teaching_repo/webprg/ 를 연다.
2. `F12` → **Network** 탭 → `F5`로 새로고침한다.
3. 목록에서 맨 위 줄(Type이 `document`)과 `.css`·`.js` 줄의 **Status**를 본다.
4. 주소창에 https://gbox3d.github.io/teaching_repo/webprg/nothing.html 을 넣고 Enter를 누른다.

**예상 결과** — 3에서 `document`·`stylesheet`·`script` 줄의 Status가 모두 `200`이다.
4에서는 Status `404`인 줄 하나가 남고 화면에는 GitHub의 **404** 안내 페이지가 나온다.

- Network 목록이 비어 있으면 DevTools를 연 채로 다시 새로고침한다. 필터는 **All**로 둔다.
- `200`·`404`는 **서버가 보내는 번호**다. 내 PC 파일(`file://`)은 서버를 거치지 않으므로 이 번호는 교재 사이트에서 확인한다.
- 목록에는 `catalog.json`(Type `fetch`)이나 `favicon.svg`처럼 우리가 적지 않은 줄도 보인다. 사이트가 스스로 더 받아 오는 파일이다.

### 8. CSS 이름을 한 번 틀리게 해 보기

1. `index.html`의 `href="styles.css"`를 `href="style.css"`로 바꾸고 저장한다(`s` 하나를 뺀 것이다).
2. 브라우저에서 새로고침하고 화면을 본다.
3. **Console**의 빨간 줄을 읽는다.
4. 다시 `href="styles.css"`로 되돌리고 저장·새로고침한다.

**예상 결과** — 2에서 카드 모양과 색이 사라지고 글자만 위에서 아래로 나열된다.
제목·문단·버튼은 그대로 있고 버튼도 동작한다. HTML과 JavaScript는 멀쩡하고 CSS만 못 찾은 것이다.
3에서 Console에 빨간 줄이 하나 생긴다.

```text
Failed to load resource: net::ERR_FILE_NOT_FOUND
```

그 줄 오른쪽에 못 찾은 파일 이름 `style.css`가 함께 표시된다.
4에서 카드 모양이 돌아오고 빨간 줄이 사라진다.

**확인** — 고친 곳은 `href` 한 군데뿐이다. 화면이 이상할 때 파일을 여러 개 동시에 고치지 않는다.

### 9. 캡처 1 저장하기

브라우저 창 두 개를 나란히 놓는다.

- 왼쪽: 내 소개 페이지(`file:///…/week01/index.html`)
- 오른쪽: 교재 사이트와 DevTools **Network**(Status `200`이 보이게)

Windows는 `Win + Shift + S`, macOS는 `⌘ + Shift + 4`로 화면을 캡처한다.

**예상 결과** — 한 장에 내 소개 페이지와 Status `200`이 함께 보인다. 이 화면이 **캡처 1**이다.

## 2일차

### 10. 연습 폴더 만들고 터미널 열기

1일차 폴더와 **별도의 새 폴더**에서 한다. 1일차 폴더에서 `git init`을 하지 않는다.

1. 탐색기(Finder)에서 `week01`과 **같은 위치**에 새 폴더 `week01-practice`를 만든다.
2. VS Code **File › Open Folder**로 `week01-practice`를 연다.
3. **Terminal › New Terminal**을 열고 아래를 친다.

```bash
git --version
```

**예상 결과** — 프롬프트 끝이 `week01-practice>`(Windows) 또는 `week01-practice %`(macOS)이고,
`git version 2.x.x` 같은 줄이 나온다. `git`을 찾을 수 없다는 메시지가 나오면 Git이 설치되지 않은 것이다.

### 11. 저장소 만들고 브랜치 이름 정하기

현재 폴더: `week01-practice`

```bash
git init
git branch -M main
git status
```

**예상 결과** — `git init`의 마지막 줄:

```text
Initialized empty Git repository in …/week01-practice/.git/
```

그 위에 `hint: Using 'master' as the name for the initial branch.`로 시작하는 여러 줄이 함께 나올 수 있다. 오류가 아니다.
바로 다음 줄의 `git branch -M main`이 브랜치 이름을 `main`으로 바꾼다(출력 없음). `git status`는 이렇게 나온다.

```text
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

- 폴더에 보이는 파일은 없지만 숨김 폴더 `.git/`이 생겼다. 이 폴더가 기록 전체다. 지우거나 옮기지 않는다.

### 12. 이 저장소에 이름과 이메일 적기

현재 폴더: `week01-practice`

```bash
git config user.name "student01"
git config user.email "student01@example.com"
git config user.name
```

**예상 결과** — 앞의 두 줄은 아무것도 출력하지 않고, 마지막 줄이 `student01`을 보여 준다.

- `--global`을 붙이지 않았으므로 **이 저장소에만** 적용된다. 공용 PC에서 남의 설정을 바꾸지 않는다.
- 이름은 commit마다 기록에 남는다. 실명 대신 수업용 별칭을 쓴다. 이메일은 다음 주 GitHub 가입에 쓸 주소면 된다.
- 이 설정은 **이 저장소에만** 적용된다. 다음 주 새 폴더에서도 `git init` 뒤에 같은 두 줄을 다시 친다.
- `fatal: not in a git directory`가 나오면 11단계의 `git init`을 하지 않았거나 다른 폴더에 있는 것이다.

### 13. commit 1 — 제목 만들기

1. 탐색기 **New File**로 `index.html`을 만들고 아래를 넣어 저장한다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>week01-practice</title>
  </head>
  <body>
    <main class="card">
      <h1>student01의 Git 연습</h1>
    </main>
  </body>
</html>
```

2. 현재 폴더: `week01-practice`

```bash
git status
git add index.html
git status
git commit -m "제목 만들기"
git log --oneline
```

**예상 결과** — 첫 `git status`에는 `Untracked files:` 아래에 `index.html`이 있고
마지막 줄이 `nothing added to commit but untracked files present (use "git add" to track)`이다.
`git add` 뒤의 `git status`에는 `Changes to be committed:` 아래에 `new file:   index.html`이 있다. commit 출력은 이렇다.

```text
[main (root-commit) 708c9ec] 제목 만들기
 1 file changed, 13 insertions(+)
 create mode 100644 index.html
```

`git log --oneline`에 `708c9ec (HEAD -> main) 제목 만들기` 한 줄이 보인다. 앞의 일곱 글자는 commit 번호이며 PC마다 다르고,
`(HEAD -> main)`은 지금 이 브랜치에 있다는 표시다.

- commit 출력에 `Your name and email address were configured automatically …`가 보이면 12단계를 건너뛴 것이다.
  commit은 되지만 **PC 계정 이름과 PC 이름**이 기록에 남는다. 12단계를 한 뒤 `git commit --amend --reset-author`를 치면 방금 commit의 이름이 바뀐다.
- 이 파일을 브라우저로 열면 흰 배경에 제목만 보인다. 아직 CSS가 없으니 정상이다.

### 14. commit 2 — 소개 문단과 링크 추가

1. `<h1>` 줄 **아래**에 네 줄을 추가하고 저장한다.

```html
      <p>commit을 하나씩 쌓아 가며 만든 연습 페이지입니다.</p>
      <p><a href="https://gbox3d.github.io/teaching_repo/webprg/">웹프로그래밍 교재 사이트</a></p>
      <button id="count-button" type="button">눌러 보기</button>
      <p id="status">클릭 횟수: 0</p>
```

2. 브라우저에서 새로고침한다. 문단·링크·버튼이 보인다. **버튼을 눌러도 아직 아무 일도 없다.** `app.js`가 없기 때문이다.
3. 현재 폴더: `week01-practice`

```bash
git status
git add index.html
git commit -m "소개 문단과 링크 추가"
git log --oneline
```

**예상 결과** — `git status`에 `modified:   index.html`이 보이고, commit 출력은 이렇다.

```text
[main cfa0792] 소개 문단과 링크 추가
 1 file changed, 4 insertions(+)
```

`git log --oneline`에 두 줄이 쌓이고 맨 윗줄이 `cfa0792 (HEAD -> main) 소개 문단과 링크 추가`다. 위가 방금 만든 commit이다.

### 15. commit 3 — 스타일과 스크립트 연결

1. 1일차 `week01` 폴더의 `styles.css`와 `app.js`를 `week01-practice` 폴더로 복사한다.
   탐색기에서 복사·붙여 넣거나, **New File**로 만들어 1일차 파일 내용을 그대로 붙여 넣는다([examples/day1](examples/day1)에 같은 파일이 있다).
2. `index.html`의 `<title>` 줄 **아래**에 두 줄을 추가하고 저장한다.

```html
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day2/index.html](examples/day2/index.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>week01-practice</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <main class="card">
      <h1>student01의 Git 연습</h1>
      <p>commit을 하나씩 쌓아 가며 만든 연습 페이지입니다.</p>
      <p><a href="https://gbox3d.github.io/teaching_repo/webprg/">웹프로그래밍 교재 사이트</a></p>
      <button id="count-button" type="button">눌러 보기</button>
      <p id="status">클릭 횟수: 0</p>
    </main>
  </body>
</html>
```

3. 브라우저에서 새로고침한다. 카드 모양이 생기고 버튼을 누르면 숫자가 올라간다.
4. 현재 폴더: `week01-practice`

```bash
git status
git add .
git commit -m "스타일과 스크립트 연결"
git log --oneline
git status
```

**예상 결과** — 첫 `git status`에 `modified:   index.html`과 `Untracked files:` 아래 `app.js`, `styles.css`가 보인다.
`git add .`는 이 세 개를 한 번에 담는다. commit 출력은 이렇다.

```text
[main 2041aef] 스타일과 스크립트 연결
 3 files changed, 43 insertions(+)
 create mode 100644 app.js
 create mode 100644 styles.css
```

`git log --oneline`에 세 줄이 보이고 맨 윗줄이 `2041aef (HEAD -> main) 스타일과 스크립트 연결`이다.
마지막 `git status`는 `nothing to commit, working tree clean`이다.

### 16. 캡처 2 저장하기

터미널 창과 브라우저 창을 나란히 놓고 한 장으로 캡처한다.

- 터미널: `git log --oneline`의 commit 3줄
- 브라우저: `week01-practice/index.html`(카드 모양의 연습 페이지)

**예상 결과** — 한 장에 commit 3줄과 연습 페이지가 함께 보인다. 이 화면이 **캡처 2**다.

## 오류가 나면

터미널의 첫 `fatal:` 또는 `error:` 줄, 브라우저 Console의 **첫 빨간 줄**을 먼저 읽는다.
자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 번에 한 곳만 고치고 다시 해 본다. 해결되지 않으면 화면을 그대로 보여 주고 도움을 요청한다.
