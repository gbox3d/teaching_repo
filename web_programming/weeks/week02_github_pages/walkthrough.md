# 2주차 따라하기 — GitHub에 올리고 브랜치로 나눠 올리기

각 차시는 강의·시연 60분과 개별 실습 30분이다. 제공 파일을 복사한 뒤 본인 아이디와 문구로 바꾼다. 아래 전문은 비교·복구용이며 전체 타이핑은 필수가 아니다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

## 1일차

사전 준비: VS Code·Git·브라우저와 GitHub 계정·이메일 확인, 1주 세 파일·이번 주 배부본 확보. 계정 가입 설명은 준비 지원용이다. 강의는 준비 5, GitHub·remote 15, 첫 push 15, Pages 15, 공개 경로 5, 안내 5분이다.

학생 실습은 `my-web` 준비 5분 → push 10분 → 제목 변경·push 5분 → Pages·캡처 10분이다. 새 저장소 생성과 Git 명령은 수업 안에서 수행한다.

### 1. 연습 폴더 만들기

1주차 폴더가 있어도 이번 주는 새 폴더 `my-web`에서 시작한다. GitHub 저장소 이름과 폴더 이름을 같게 두기 위해서다.

1. VS Code에서 **Terminal › New Terminal**을 연다. 현재 폴더: 문서(Documents) 폴더 등 원하는 위치 (PowerShell, macOS 터미널 공통)

```bash
mkdir my-web
cd my-web
```

2. **File › Open Folder**로 방금 만든 `my-web` 폴더를 연다. VS Code가 다시 열리면 **Terminal › New Terminal**을 다시 연다.

**예상 결과** — 프롬프트 끝이 `my-web>`이다 (macOS는 `my-web %`). 이제부터 모든 명령은 이 폴더에서 실행한다.

### 2. 세 파일 만들기

1주 세 파일 또는 배부한 `examples/day1/`의 세 파일을 복사한다. 누락된 파일은 VS Code의 **New File**로 만들고 아래 전문을 붙여 넣어 복구한다. CSS·JS는 제공 코드 그대로 쓴다.
`index.html`의 `<h1>`은 일부러 `내 첫 페이지`로 둔다. 8단계에서 한 줄만 고칠 것이다.

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
    <main class="card">
      <p class="eyebrow">Week 02 · GitHub Pages</p>
      <h1>내 첫 페이지</h1>
      <p>내 컴퓨터에서 만든 페이지를 GitHub에 올려 공개합니다.</p>
      <button id="count-button" type="button">방문 버튼</button>
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
  box-sizing: border-box;
  width: min(36rem, calc(100% - 2rem));
  padding: 2rem;
  border-radius: 1rem;
  background: white;
  box-shadow: 0 1rem 2.5rem rgb(30 50 100 / 12%);
}

h1 {
  word-break: keep-all;
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

`app.js` (같은 파일이 [examples/day1/app.js](examples/day1/app.js)에 있다):

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

예상 결과 — 탐색기에서 `index.html`을 오른쪽 클릭 → Reveal in File Explorer(macOS는 Reveal in Finder)로 폴더를 열고 `index.html`을 더블클릭하면
카드 한 장에 `내 첫 페이지`, **방문 버튼**, `클릭 횟수: 0`이 보인다. 버튼을 누르면 숫자가 올라간다.

### 3. 로컬 저장소 만들고 첫 commit 하기 (1주차 복습)

현재 폴더: `my-web`

```bash
git init
git branch -M main
git config user.name "student01"
git config user.email "본인 noreply 이메일"
git add .
git commit -m "첫 페이지 만들기"
git log --oneline
```

**예상 결과**

```text
[main (root-commit) 0be6182] 첫 페이지 만들기
 3 files changed
 create mode 100644 app.js
 create mode 100644 index.html
 create mode 100644 styles.css
```

`git log --oneline`에는 `0be6182 첫 페이지 만들기` 한 줄이 보인다. 해시는 실행마다 다르며 줄 수는 복사한 파일에 따라 달라진다.

- `git add .`: 폴더 안에서 바뀐 파일을 모두 다음 commit에 넣는다. 1주차의 `git add index.html`을 세 파일에 한 번에 한 것이다.
- `git config` 두 줄은 **저장소마다 따로** 적용된다. 1주차 폴더에서 적었어도 새 폴더에서 다시 적어야 내 별칭으로 기록된다.
  기존 Git 설정이 있으면 그 이름·이메일로 기록될 수 있고, 설정이 없으면 commit이 중단될 수 있다. `git config user.name`·`git config user.email`로 확인한다. GitHub 비공개 이메일 설정에서 본인 noreply 주소를 확인해 쓸 수 있다. 공용 PC에서는 `--global`을 붙이지 않는다.

### 4. GitHub 계정 만들기

이미 계정이 있으면 로그인만 하고 5단계로 간다.

1. 브라우저에서 https://github.com/signup 을 연다.
2. 이메일, 비밀번호, 아이디(Username)를 입력한다. 아이디는 공개 주소 `https://<아이디>.github.io/`에 들어가므로
   소문자·숫자·하이픈만 쓰고 실명·학번을 넣지 않는다.
3. 확인 메일에 온 코드를 입력한다.

**예상 결과** — 본인 계정으로 로그인되어 있다. 수업 전 이메일 확인까지 마치고, 화면의 인증 안내가 남으면 강의자에게 준비 지원을 요청한다.

### 5. 빈 저장소 만들기

1. 오른쪽 위 **+ › New repository**를 누른다.
2. **Repository name**에 `my-web`을 적는다. Description은 비워 둔다.
3. **Public**을 고른다.
4. Add a README file은 체크하지 않는다. Add .gitignore와 Choose a license는 None으로 둔다.
5. **Create repository**를 누른다.

**예상 결과** — "Quick setup" 화면이 열린다. **HTTPS**가 선택된 상태에서 `https://github.com/student01/my-web.git` 주소가 보이고,
그 아래 "…or push an existing repository from the command line"에 명령 세 줄이 있다.

```text
git remote add origin https://github.com/student01/my-web.git
git branch -M main
git push -u origin main
```

이 세 줄이 6·7단계의 명령이다. 가운데 줄은 3단계에서 이미 했다. 이 화면을 닫지 않는다.
README를 자동 생성했다면 원격에 별도 commit이 생겨 첫 push가 거부될 수 있다. 삭제·강제 push 대신 [실습지의 복구 안내](lab.md#막혔을-때)를 따른다. 새 이름의 빈 저장소로 연결했다면 이 문서의 저장소 이름과 Pages 주소도 함께 바꾼다.

### 6. remote 연결하기

현재 폴더: `my-web`

```bash
git remote add origin https://github.com/student01/my-web.git
git remote -v
```

**예상 결과**

```text
origin	https://github.com/student01/my-web.git (fetch)
origin	https://github.com/student01/my-web.git (push)
```

- `git remote add origin <URL>`은 주소를 `origin`이라는 이름으로 적어 둘 뿐이다. 아직 아무것도 보내지 않았다.
- `error: remote origin already exists.`가 나오면 이미 적혀 있는 것이다. `git remote -v`의 주소가 맞으면 그대로 7단계로 간다.
  주소가 틀렸으면 `git remote remove origin`을 한 뒤 다시 `git remote add origin <URL>`을 한다.

### 7. 첫 push 하기

현재 폴더: `my-web`

```bash
git push -u origin main
```

1. Git Credential Manager가 설정되어 있고 인증이 필요하면 브라우저 로그인 안내가 열린다. 화면의 **Sign in with your browser** 등 브라우저 로그인 항목을 선택한다.
2. 본인 GitHub 계정인지 확인하고 요청된 인증·권한 확인을 마친다. 문구는 GCM 버전에 따라 달라질 수 있다.
3. 인증 성공 후 터미널에서 push 결과를 확인한다. 기존 인증이 있으면 로그인 창이 생략될 수 있다.

**예상 결과** — `Enumerating objects` 같은 줄 몇 개 뒤에 아래가 보인다.

```text
To https://github.com/student01/my-web.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

4. 브라우저에서 저장소 화면 `https://github.com/student01/my-web`을 새로고침한다.
   `app.js`, `index.html`, `styles.css` 세 파일과 commit 메시지 `첫 페이지 만들기`가 보인다. 이 화면이 **캡처 1**이다.

- 인증 정보가 이 PC에 저장되면 이후 push에서 다시 묻지 않을 수 있다. 비밀번호나 토큰을 명령에 적지 않는다.
- 로그인 창 대신 터미널에 `Username for 'https://github.com':`가 나오면 (GCM 설정 확인이 필요한 환경) 강의자 안내를 따른다.
- `-u`는 "다음부터 `git push`만 쳐도 `origin`의 `main`으로 보낸다"는 뜻이다. 8단계부터는 `git push`만 쓴다.

### 8. 제목 한 줄 고치고 push 하기

1. `index.html`에서 `<h1>내 첫 페이지</h1>`을 `<h1>내 첫 GitHub 페이지</h1>`로 바꾸고 저장한다.
   전체 파일은 아래와 같다. 같은 파일이 [examples/day1/index.html](examples/day1/index.html)에 있다.

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
    <main class="card">
      <p class="eyebrow">Week 02 · GitHub Pages</p>
      <h1>내 첫 GitHub 페이지</h1>
      <p>내 컴퓨터에서 만든 페이지를 GitHub에 올려 공개합니다.</p>
      <button id="count-button" type="button">방문 버튼</button>
      <p id="status">클릭 횟수: 0</p>
    </main>
  </body>
</html>
```

2. 현재 폴더: `my-web`

```bash
git status
git add index.html
git commit -m "제목을 내 첫 GitHub 페이지로 바꾸기"
git push
```

**예상 결과** — `git status`에 `modified:   index.html`, commit에 `1 file changed, 1 insertion(+), 1 deletion(-)`, push에 아래가 보인다.

```text
To https://github.com/student01/my-web.git
   0be6182..911638a  main -> main
```

3. GitHub 저장소 화면을 새로고침하고 제목 변경 commit과 `index.html`의 `<h1>내 첫 GitHub 페이지</h1>`을 확인한다. 새 폴더에서 이 순서로 시작했다면 commit은 2개이며, 기존 파일·기록을 이어 썼다면 개수와 행 번호는 다를 수 있다.

- 1주차의 `add → commit` 뒤에 `push` 한 줄이 붙었다. 저장만 하고 push하지 않으면 GitHub는 그대로다.
- 7단계에서 `-u`를 썼기 때문에 이번에는 `git push`만으로 된다.

### 9. GitHub Pages 켜기

1. 저장소 화면 위쪽 **Settings** 탭 → 왼쪽 메뉴 **Pages**를 누른다.
2. **Build and deployment › Source**가 **Deploy from a branch**인지 확인한다.
3. **Branch**에서 `None`을 `main`으로 바꾸고, 폴더는 `/(root)` 그대로 두고 **Save**를 누른다.
4. Pages의 배포 상태를 확인한다. 배포가 끝나면 공개 주소와 **Visit site**에서 사이트를 연다. 최대 10분이 걸릴 수 있다.
5. **Visit site**를 누르거나 새 탭에 주소를 직접 친다.

예상 결과 — `https://student01.github.io/my-web/`에서 `내 첫 GitHub 페이지` 카드가 열리고 방문 버튼이 동작한다. 이 화면이 캡처 2다.

- 주소는 `https://` + 아이디 + `.github.io/` + 저장소 이름 + `/`이다. 끝의 `/`를 빼지 않는다.
- 404가 보이면 저장소 이름·`index.html`·배포 상태를 확인한다. [GitHub 공식 문서](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)는 push 뒤 최대 10분의 반영 시간을 안내한다.
- 실습 시간이 끝나면 로컬 화면과 GitHub commit을 먼저 캡처하고 공개 배포 화면을 나중에 보완한다. 대기 중인 배포를 완료로 표시하지 않는다.

## 2일차

강의·시연: 준비 5, branch·switch 15, 파일 추가 10, merge 15, Pages 비교 10, 안내 5분. 학생 실습: about 브랜치 5분 → 제공 HTML의 소개·왕복 링크 10분 → commit·push·merge 10분 → 확인 5분이다. 16단계 브랜치 삭제와 문서 끝의 clone·pull은 수업 뒤 선택이다.

### 10. 저장소 다시 열기

VS Code **File › Open Folder**로 1일차의 `my-web`을 열고 **Terminal › New Terminal**을 연다. 현재 폴더: `my-web`

```bash
git status
git log --oneline
```

**예상 결과**

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

`git log --oneline`에 1일차의 commit 두 줄이 보인다. 집에서 push한 commit이 있으면 [다른 PC에서 이어 할 때](#다른-pc에서-이어-할-때)를 먼저 본다.

### 11. about 브랜치 만들고 옮겨 가기

현재 폴더: `my-web`

```bash
git branch about
git switch about
git branch
```

**예상 결과**

```text
Switched to branch 'about'
```

```text
* about
  main
```

- `git branch about`은 브랜치를 만들기만 한다. 만든 직후에는 아직 `main`에 있다.
- `git switch about`으로 옮겨 간다. `git branch`의 `*`가 지금 있는 브랜치다.
- 폴더의 파일은 그대로다. 지금부터 하는 commit이 `about`에 쌓인다.
- `fatal: invalid reference: about`이 나오면 `git branch about`을 아직 하지 않은 것이다.

### 12. about.html 추가하고 링크 넣기

1. 제공 `about.html`을 복사하고 소개 문장 한 줄을 본인 별칭·소개로 바꾼다. 아래는 수정 전 전문이다. 같은 파일이 [examples/day2/about.html](examples/day2/about.html)에 있다.

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

2. `index.html`의 `<p id="status">` 줄 아래에 `<p><a href="about.html">소개 페이지 보기</a></p>` 한 줄을 추가한다.
   전체 파일은 아래와 같다. 같은 파일이 [examples/day2/index.html](examples/day2/index.html)에 있다.

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
    <main class="card">
      <p class="eyebrow">Week 02 · GitHub Pages</p>
      <h1>내 첫 GitHub 페이지</h1>
      <p>내 컴퓨터에서 만든 페이지를 GitHub에 올려 공개합니다.</p>
      <button id="count-button" type="button">방문 버튼</button>
      <p id="status">클릭 횟수: 0</p>
      <p><a href="about.html">소개 페이지 보기</a></p>
    </main>
  </body>
</html>
```

**예상 결과** — 폴더의 `index.html`을 더블클릭해 열면 카드 아래에 **소개 페이지 보기** 링크가 있고, 누르면 `소개` 카드가 열린다.
**첫 페이지로 돌아가기**를 누르면 돌아온다. 두 파일이 같은 폴더에 있으므로 `href`에는 파일 이름만 적는다.

### 13. about 브랜치에서 commit 하기

현재 폴더: `my-web`

```bash
git status
git add .
git commit -m "소개 페이지 추가"
git log --oneline
```

**예상 결과** — `git status`의 첫 줄이 `On branch about`이고 `modified:   index.html`과 `Untracked files: about.html`이 보인다. commit 뒤:

```text
[about c5fdc17] 소개 페이지 추가
 2 files changed, 18 insertions(+)
 create mode 100644 about.html
```

`git log --oneline`에 세 줄이 보인다. 맨 위가 `소개 페이지 추가`다.

### 14. about 브랜치 push 하기

현재 폴더: `my-web`

```bash
git push -u origin about
```

**예상 결과**

```text
To https://github.com/student01/my-web.git
 * [new branch]      about -> about
branch 'about' set up to track 'origin/about'.
```

1. GitHub 저장소 화면을 새로고침한다. 왼쪽 위 브랜치 드롭다운 `main ▾`을 누르면 `main`과 `about` 두 개가 보인다.
2. `about`을 고르면 파일 목록에 `about.html`이 있다. 다시 `main`을 고르면 없다. **main에는 없고 about에만 있다.**
3. 브랜치 드롭다운의 **View all branches**로 전체 목록을 연다. 이 화면이 **캡처 3**이다.
4. 저장소 화면 위에 노란 배너와 초록 **Compare & pull request** 버튼이 보여도 누르지 않는다. 합치는 것은 15단계에서 내 PC에서 한다.

- `git push`만 치면 `fatal: The current branch about has no upstream branch.`가 나온다. 처음 올리는 브랜치는 `-u origin about`을 붙인다.

### 15. main으로 돌아가 merge 하고 push 하기

현재 폴더: `my-web`

```bash
git switch main
git merge about
git push
```

**예상 결과** — `git switch main` 직후 탐색기에서 `about.html`이 사라지고 `index.html`의 링크 줄도 없어진다. 정상이다. merge 뒤 다시 나타난다.

```text
Updating 911638a..c5fdc17
Fast-forward
 about.html | 17 +++++++++++++++++
 index.html |  1 +
 2 files changed, 18 insertions(+)
 create mode 100644 about.html
```

push 뒤에는 `911638a..c5fdc17  main -> main`이 보인다.

1. GitHub 저장소 화면(`main`)을 새로고침하면 `about.html`이 보인다.
2. Pages 배포 완료 뒤 `https://student01.github.io/my-web/`을 새로고침한다. 카드 아래에 **소개 페이지 보기** 링크가 생긴다.
3. 링크를 누르면 `https://student01.github.io/my-web/about.html`에서 `소개` 카드가 열린다. 이 화면이 **캡처 4**다.

- 옛 화면이 그대로면 배포 상태를 확인한 뒤 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- `Fast-forward`는 main에 새 commit이 없어서 about의 commit을 그대로 이어 붙였다는 뜻이다.

### 16. 브랜치 정리하기 (선택)

캡처 3을 저장하고 merge가 끝난 뒤의 수업 후 선택 작업이다. 브랜치를 지워도 commit은 main에 남는다. 지우지 않아도 된다. 현재 폴더: `my-web`

```bash
git branch -d about
git push origin --delete about
```

**예상 결과**

```text
Deleted branch about (was c5fdc17).
```

```text
 - [deleted]         about
```

`git branch`에 `* main`만 남는다. GitHub에서는 브랜치 목록 페이지(**Branches**)에서 `about` 옆 휴지통 아이콘으로도 지울 수 있다.

### 17. 제출하기

2주는 일반 주차와 달리 캡처 4장을 모아 제출한다.

1. 저장소 `my-web`에 세 파일이 보이는 화면 (7단계)
2. `https://student01.github.io/my-web/`이 열린 화면 (9단계)
3. 브랜치 목록에 `about`이 보이는 화면 (14단계)
4. 공개 페이지에서 **소개 페이지 보기**를 눌러 `about.html`이 열린 화면 (15단계)

배포 지연 때는 로컬 화면·GitHub commit으로 우선 확인하고 공개 화면을 보완한다. 캡처에 이메일·실명이 보이지 않게 한다. 아이디는 보여도 된다.

3주에는 day2의 네 파일을 main에서 이어 쓴다. 새 브랜치를 만들지 않고 시맨틱 HTML·정적 방명록을 수정하며 CSS·JS는 연결만 해제한다. 3주부터 파일 준비는 사전, 업로드는 수업 뒤 정리다.

## 다른 PC에서 이어 할 때

집에서 이어 하려면 GitHub의 저장소를 내려받는다. 현재 폴더: 저장소를 둘 위치

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

이미 받아 둔 폴더가 있고 다른 PC에서 push한 commit이 있으면 먼저 가져온다. 현재 폴더: `my-web`

```bash
git pull
```

**예상 결과** — clone은 `Cloning into 'my-web'...`로 시작해 폴더가 생긴다. pull은 새 commit이 없으면 `Already up to date.`,
있으면 `Fast-forward`와 바뀐 파일 목록이 보인다. push할 때는 처음 한 번 브라우저 로그인 창이 다시 뜬다.

## 오류가 나면

먼저 터미널의 **첫 `error:` 또는 `fatal:` 줄**을 읽는다. `hint:` 줄은 git이 알려 주는 해결 방법이다.
자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 실행하고, 해결되지 않으면 터미널 화면을 그대로 보여 주고 도움을 요청한다.
