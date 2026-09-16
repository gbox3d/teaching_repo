# 1주차 실습 — 내 소개 페이지와 첫 commit 세 개

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week01_web_git

1일차에는 세 파일로 내 소개 페이지를 만들고, 2일차에는 연습 폴더에 commit 세 개를 남긴다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 별칭이므로 본인 수업용 별칭으로 바꾼다.
제출물은 **캡처 2장**이다. 보고서나 표는 제출하지 않는다.

## 1일차 — 세 파일로 내 소개 페이지 만들기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 폴더 `week01`을 만들어 VS Code로 열고 세 파일을 만든다 |
| 10–20분 | `index.html`을 브라우저로 열어 버튼을 눌러 보고, 주소창의 `file:///…`을 읽는다 |
| 20–30분 | `<h1>`과 소개 문단을 내 소개로 고치고 저장·새로고침한다 |
| 30–40분 | DevTools **Elements**에서 `<h1>`, **Console**에서 `week01 ready`를 확인한다 |
| 40–50분 | 교재 사이트에서 Network의 `200`과 없는 주소의 `404`를 본다 |
| 50–60분 | `styles.css` 이름을 한 번 틀리게 했다가 되돌리고 캡처 1을 저장한다 |

### 1. 폴더와 세 파일

`week01` 폴더를 만들어 VS Code로 열고 `index.html`·`styles.css`·`app.js`를 만든다.
[따라하기 1~2단계](walkthrough.md#1-연습-폴더-만들고-vs-code로-열기)에 전체 코드가 있다.

- 파일 이름은 한 글자도 다르면 안 된다. `styles.css`의 `s`를 빠뜨리지 않는다.
- 세 파일은 모두 같은 폴더에 둔다. 폴더를 더 만들지 않는다.
- `app.js`는 붙여 넣고 읽기만 한다. 이번 주에는 고치지 않는다.

### 2. 브라우저로 열고 내 소개로 고치기

`index.html`을 더블클릭해 열고 `<h1>`과 소개 문단을 본인 소개로 고친다.
[따라하기 3~5단계](walkthrough.md#3-브라우저로-열어-보기)를 본다.

- 주소창이 `file:///`로 시작하는지 본다. 내 PC의 파일을 그대로 여는 주소다.
- 저장(`Ctrl+S`) 뒤 새로고침(`F5`)해야 화면이 바뀐다.
- 실명·학번·전화번호는 쓰지 않는다. `student01` 같은 수업용 별칭을 쓴다.

### 3. Elements와 Console

`F12`로 DevTools를 열고 두 탭을 본다. [따라하기 6단계](walkthrough.md#6-devtools-elements와-console-보기)를 본다.

- **Elements**: 내가 고친 `<h1>` 문장이 그대로 있는지 확인한다.
- **Console**: `week01 ready` 한 줄이 있다. `app.js`가 남긴 메시지다.
- 버튼을 두 번 누르고 `<p id="status">`의 글자가 `클릭 횟수: 2`로 바뀌는 것을 본다.

### 4. 교재 사이트에서 200과 404

새 탭에서 교재 사이트를 열고 **Network** 탭을 본다. [따라하기 7단계](walkthrough.md#7-교재-사이트에서-200과-404-보기)를 본다.

| 주소 | Type | Status |
|---|---|---|
| https://gbox3d.github.io/teaching_repo/webprg/ | document | 200 |
| `…/assets/library.css` · `…/assets/course.css` | stylesheet | 200 |
| `…/assets/course.js` | script | 200 |
| https://gbox3d.github.io/teaching_repo/webprg/nothing.html | document | 404 |

- DevTools를 연 채로 `F5`를 눌러야 목록이 채워진다. 필터는 **All**로 둔다.
- `404`는 "그 주소에 파일이 없다"는 뜻이다. 화면에는 GitHub의 `404 File not found` 페이지가 나온다.
- 목록에 `catalog.json`이나 `favicon.svg` 같은 줄도 보인다. 사이트가 스스로 더 받아 오는 파일이다.

### 5. 오류 하나만 따라 해 보기

`index.html`의 `href="styles.css"`를 `style.css`로 한 번 바꿔 저장하고 새로고침한다.
[따라하기 8단계](walkthrough.md#8-css-이름을-한-번-틀리게-해-보기)를 본다.

1. 화면: 카드 모양과 색이 사라지고 글자만 위에서 아래로 나열된다. 제목·버튼은 그대로이고 버튼도 동작한다.
2. Console: 빨간 줄 `Failed to load resource: net::ERR_FILE_NOT_FOUND`가 생긴다.
3. `href="styles.css"`로 되돌리고 저장·새로고침하면 원래 모양으로 돌아온다.

고치는 곳은 `href` 한 군데다. 화면이 이상할 때 여러 파일을 동시에 고치지 않는다.

### 6. 오늘 확인할 것

- [ ] 주소창이 `file:///…/week01/index.html`이다.
- [ ] 제목과 소개 문단이 내 소개로 바뀌어 있다.
- [ ] 버튼을 누르면 `클릭 횟수`가 올라간다.
- [ ] 교재 사이트 Network에서 `200`을, 없는 주소에서 `404`를 보았다.
- [ ] 캡처 1을 저장했다.

`week01` 폴더는 2일차에도 쓴다. 지우지 않는다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — Git으로 commit 3개 남기기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 폴더 `week01-practice`를 만들어 VS Code로 열고 `git init` → `git branch -M main` |
| 10–15분 | `git config user.name`·`user.email`을 이 저장소에 적는다 |
| 15–28분 | commit 1 — 제목을 만들고 `status → add → commit → log` |
| 28–40분 | commit 2 — 소개 문단·링크·버튼을 추가하고 같은 순서로 commit |
| 40–52분 | commit 3 — `styles.css`·`app.js`를 복사하고 두 줄로 연결해 commit |
| 52–60분 | `git log --oneline`의 3줄과 연습 페이지를 한 화면에 캡처한다 |

### 1. 저장소 만들기

`week01`과 같은 위치에 새 폴더 `week01-practice`를 만들고 VS Code로 연 뒤 터미널에서 `git init` → `git branch -M main` → `git status`.
[따라하기 10~11단계](walkthrough.md#10-연습-폴더-만들고-터미널-열기)를 본다.

- **1일차 폴더에서 `git init`을 하지 않는다.** 새 폴더에서 한다.
- `git status`의 첫 줄이 `On branch main`이어야 한다. `master`면 `git branch -M main`을 다시 친다.
- `hint: Using 'master' as the name for the initial branch.` 여러 줄은 오류가 아니다.

### 2. 이름과 이메일

`git config user.name "student01"`, `git config user.email "본인 이메일"`을 친다.
[따라하기 12단계](walkthrough.md#12-이-저장소에-이름과-이메일-적기)를 본다.

- 적지 않아도 commit은 된다. 대신 Git이 **PC 계정 이름과 PC 이름**으로 자동으로 채워 기록에 남긴다. 그래서 첫 commit 전에 적는다.
- `--global`을 붙이지 않는다. 이 저장소에만 적용된다.
- 이름은 commit마다 기록에 남는다. 실명 대신 수업용 별칭을 쓴다.
- 이 설정은 **저장소마다 따로** 적용된다. 다음 주 새 폴더에서도 첫 commit 전에 다시 친다.
- `git config user.name`만 다시 쳐서 방금 적은 이름이 나오는지 확인한다.

### 3. commit 1 — 제목 만들기

`index.html`을 만들어 제목 `<h1>`까지만 쓰고 `git status` → `git add index.html` → `git commit -m "제목 만들기"` → `git log --oneline`.
[따라하기 13단계](walkthrough.md#13-commit-1--제목-만들기)를 본다.

- `git add` 전에는 `Untracked files:`, add 뒤에는 `Changes to be committed:`에 파일이 보인다. 두 번 다 읽고 넘어간다.
- commit 메시지에 띄어쓰기가 있으므로 반드시 따옴표로 감싼다.
- `git log --oneline`에 한 줄이 보이면 성공이다.

### 4. commit 2 — 소개 문단과 링크 추가

`<h1>` 아래에 소개 문단, 교재 사이트 링크, 버튼, `<p id="status">` 네 줄을 추가하고 같은 순서로 commit한다.
[따라하기 14단계](walkthrough.md#14-commit-2--소개-문단과-링크-추가)를 본다.

- 브라우저에서 새로고침해 문단과 링크가 보이는지 먼저 확인한다.
- 이 시점에는 **버튼을 눌러도 아무 일도 없다.** `app.js`를 아직 연결하지 않았기 때문이다.
- 메시지는 `소개 문단과 링크 추가`처럼 무엇이 바뀌었는지 보이게 쓴다.

### 5. commit 3 — 스타일과 스크립트 연결

1일차 폴더의 `styles.css`·`app.js`를 복사해 넣고, `index.html` 머리에 `<link>`·`<script>` 두 줄을 추가한 뒤 commit한다.
[따라하기 15단계](walkthrough.md#15-commit-3--스타일과-스크립트-연결)를 본다.

- commit 전에 브라우저에서 카드 모양이 생기고 버튼이 동작하는지 확인한다.
- `git status`에 `modified: index.html`과 새 파일 두 개(`app.js`, `styles.css`)가 함께 보인다. `git add .`로 한 번에 담는다.
- commit 뒤 `git log --oneline`이 세 줄, `git status`가 `nothing to commit, working tree clean`이면 끝이다.

### 6. 마지막 확인

- [ ] `git log --oneline`에 commit이 세 줄 있고 메시지가 서로 다르다.
- [ ] `git status`가 `nothing to commit, working tree clean`이다.
- [ ] 연습 페이지가 카드 모양으로 열리고 버튼이 동작한다.
- [ ] 캡처 2를 저장했다.

## 막혔을 때

| 메시지·증상 | 확인할 것 |
|---|---|
| 고쳤는데 화면이 그대로다 | VS Code 탭 제목의 ●(저장 안 됨)을 본다. `Ctrl+S`로 저장하고 브라우저에서 `F5`. 주소창의 폴더가 내 폴더가 맞는지도 본다 |
| 카드 모양·색이 사라지고 글자만 보인다 / Console에 `Failed to load resource: net::ERR_FILE_NOT_FOUND` | `<link href="…">`의 이름과 실제 파일 이름(`styles.css`)을 한 글자씩 비교한다. 두 파일이 같은 폴더에 있는지 본다 |
| 버튼을 눌러도 숫자가 안 바뀐다 | Console에 `week01 ready`가 있는지 본다. 없으면 `<script src="app.js" defer></script>`의 이름을, 있으면 버튼 줄의 `id="count-button"`을 본다 |
| Network 목록이 비어 있다 | DevTools를 연 채로 `F5`를 누른다. 필터를 **All**로 둔다 |
| 교재 사이트에서 `404 File not found` 화면이 나온다 | 없는 주소를 열었을 때의 정상 결과다. Console에는 `Failed to load resource: the server responded with a status of 404 ()`가 남는다 |
| `fatal: not a git repository …` | 그 폴더에서 `git init`을 하지 않았거나 다른 폴더에 있다. 프롬프트의 폴더 이름을 보고 `week01-practice`에서 다시 한다 |
| `fatal: not in a git directory` | `git config`를 `git init`보다 먼저 쳤다. 2일차 1번부터 다시 한다 |
| commit은 됐는데 `Your name and email address were configured automatically …` 안내가 나온다 | 이름·이메일을 적지 않아 PC 계정 이름이 기록에 남은 것이다. 2일차 2번을 한 뒤 `git commit --amend --reset-author`를 한 번 친다 |
| `Author identity unknown` / `*** Please tell me who you are.` | 이름·이메일이 없고 자동 추정도 막힌 PC다. 2일차 2번의 `git config user.name`·`user.email`을 `--global` 없이 치고 commit을 다시 한다 |
| `nothing added to commit but untracked files present (use "git add" to track)` | `git add index.html`을 건너뛰었다. add 뒤에 commit한다 |
| `fatal: pathspec 'inedx.html' did not match any files` | 파일 이름 오타이거나 파일을 아직 만들지 않았다. 탐색기의 실제 이름과 비교한다 |
| `error: pathspec '문단과' did not match any file(s) known to git` | commit 메시지를 따옴표로 감싸지 않았다. `git commit -m "소개 문단과 링크 추가"` |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. 탭의 ●과 `git log --oneline`을 본다 |
| `Aborting commit due to empty commit message.` | `-m "메시지"`를 빠뜨려 편집기가 열렸다가 닫힌 것이다. `-m`을 붙여 다시 commit한다 |
| `fatal: your current branch 'main' does not have any commits yet` | 아직 commit이 하나도 없다. `git add` → `git commit`을 먼저 한다 |
| `git status`의 첫 줄이 `On branch master` | `git branch -M main`을 건너뛰었다. 지금 쳐도 된다 |
| `git`을 찾을 수 없다는 메시지 | Git이 설치되지 않았거나 설치 후 터미널을 다시 열지 않았다. VS Code를 껐다 켜고 `git --version`을 친다 |

한 번에 한 곳만 고치고 다시 해 본다. 해결되지 않으면 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 두 장

1. **1일차**: 내 소개 페이지(`file:///…/week01/index.html`)와 교재 사이트 DevTools **Network**의 `200`이 한 화면에 보이는 캡처
2. **2일차**: 터미널의 `git log --oneline` 3줄과 연습 페이지가 한 화면에 보이는 캡처

두 창을 나란히 놓고 화면을 캡처한다(Windows `Win + Shift + S`, macOS `⌘ + Shift + 4`).
캡처에 실명·학번·이메일이 보이지 않게 한다. 폴더 경로에 이름이 들어 있으면 그 부분을 가린다.
제출 위치와 마감은 수업 공지를 따른다. 다른 제출 파일은 없다.

## 먼저 끝났다면

- 1일차: `styles.css`의 `background: #eef2ff`를 다른 색으로 바꿔 저장·새로고침한다. HTML을 고치지 않아도 화면이 바뀐다.
- 1일차: Elements에서 `<h1>` 글자를 직접 고쳐 보고 새로고침한다. 파일은 그대로이므로 고친 내용이 사라진다.
- 2일차: commit 전에 `git diff`를 쳐서 `+`로 시작하는 줄을 눈으로 본다.
- 2일차: `styles.css`의 색을 바꾸고 네 번째 commit(`카드 색 바꾸기`)을 만들어 `git log --oneline`에 네 줄이 되는지 본다.

추가 과제는 선택이며 채점하지 않는다.
