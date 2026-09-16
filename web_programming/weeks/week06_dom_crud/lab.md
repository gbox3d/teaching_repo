# 6주차 실습 — 클릭 카운터와 다크 모드

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud

5주차까지 만든 `my-web`의 `index.html`에 버튼 두 개를 붙이고, `app.js`에서 그 버튼이 눌렸을 때 화면을 바꾼다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.
이번 주 작업은 **`dark-mode` 브랜치**에서 한다. main과 공개 페이지는 2일차 마지막에 한 번만 바뀐다.

## 1일차 — 클릭하면 바뀌는 페이지 만들기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` 뒤 `git switch -c dark-mode` |
| 5–20분 | `index.html`에 `[인사 바꾸기]` 버튼을 넣고, 누르면 `#greeting`의 글자가 바뀌게 만든다 |
| 20–38분 | `<p id="count">`를 넣고 누를 때마다 `클릭 1회`·`클릭 2회`로 숫자가 오르게 만든다 |
| 38–50분 | `null` 오류 두 가지(선택자 오타·`defer` 누락)를 일부러 만들어 보고 고친다 |
| 50–55분 | `git add .` → `git commit` → `git push -u origin dark-mode` |
| 55–60분 | GitHub 브랜치 목록에서 `dark-mode`를 확인한다(공개 페이지는 아직 그대로다) → 공용 PC면 자격 증명 삭제 |

### 1. 브랜치 만들기 (`git switch -c dark-mode`)

받아온 뒤 오늘 작업할 브랜치를 만든다. [따라하기 1~2단계](walkthrough.md#1-저장소-받아오기)를 본다.

- 시작 전 `git status`가 `nothing to commit, working tree clean`이어야 한다. 아니면 먼저 commit한다.
- `Switched to a new branch 'dark-mode'`가 보이고 `git branch`에 `* dark-mode`가 있으면 된다.
- 폴더의 파일은 그대로 보인다. 지금부터의 commit이 `dark-mode`에 쌓인다.

### 2. 버튼 자리와 요소 찾기 (`querySelector`)

`index.html`의 `#greeting` 카드 **바로 아래**에 버튼 문단과 `<p id="count">` 문단을 넣고, `app.js` 맨 위에서 세 요소를 찾아 둔다.
[따라하기 3~4단계](walkthrough.md#3-버튼과-카운터-자리-만들기)를 본다.

- 버튼에는 `type="button"`을 붙인다. 지금은 폼 밖이라 붙이지 않아도 새로고침되지 않지만, 7주차 폼 안의 버튼과 습관을 맞춰 둔다.
- `id`는 `hello-button`·`count` 두 개다. 한 페이지에 같은 `id`를 두 번 쓰지 않는다.
- `const greeting = document.querySelector('#greeting');`처럼 찾은 것을 `const`에 담는다.
- `console.log(greeting)`으로 찍어 보면 요소가 통째로 보인다. `null`이면 철자가 틀린 것이다.

### 3. 클릭하면 인사말 바꾸기 (`addEventListener('click')` · `textContent`)

`helloButton`에 클릭 리스너를 붙이고, 그 안에서 `greeting.textContent`를 다른 문장으로 바꾼다.
[따라하기 5~6단계](walkthrough.md#5-5주차-두-줄을-한-줄로-합치기)를 본다.

- 리스너는 `function () { }` 모양으로 쓴다. 화살표 함수(`() =>`)는 이 과목에서 쓰지 않는다.
- 맡겨 두는 줄은 페이지를 열 때 **한 번** 실행되고, 중괄호 안은 **누를 때마다** 실행된다.
- 바뀐 글자는 새로고침하면 HTML에 적힌 글자로 돌아간다. 그것이 정상이다.

### 4. 클릭 횟수 세기 (`let count`)

`let count = 0;`을 리스너 **밖**에 두고, 리스너 안에서 1씩 올려 `` `클릭 ${count}회` ``로 표시한다.
[따라하기 7단계](walkthrough.md#7-클릭-횟수-세기)를 본다.

- `count`를 리스너 안에 만들면 누를 때마다 0으로 다시 시작해 계속 `클릭 1회`만 나온다.
- 숫자를 문장에 넣을 때는 5주차의 템플릿 문자열을 쓴다. 백틱은 영문 입력 상태에서 친다.
- 세 번 눌러 `클릭 3회`까지 확인한다.

### 5. `null` 오류 두 가지 만들어 보고 고치기 (Console)

두 가지를 차례로 만들어 Console의 빨간 줄을 읽고 되돌린다. [따라하기 8단계](walkthrough.md#8-null-오류-두-가지-만들어-보기)를 본다.

| 일부러 만드는 것 | 나오는 줄 |
|---|---|
| `'#hello-button'`을 `'#hello-buton'`으로 | `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` |
| `index.html`의 `script` 줄에서 `defer`만 지우기 | `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` |

- 둘 다 원인은 하나다. **찾지 못해서 `null`이 나왔다.** 선택자 철자와 `defer`를 차례로 본다.
- `defer`가 없으면 HTML을 다 읽기 전에 찾으러 가므로 아직 만들어지지 않은 요소를 못 찾는다.
- 확인했으면 **반드시 원래대로 되돌린다.** 오류가 있는 채로 commit하지 않는다.

### 6. 오늘 확인할 것

- [ ] `git branch`에 `* dark-mode`가 있다.
- [ ] 버튼을 누르면 인사말이 바뀌고 `클릭 N회`의 숫자가 오른다.
- [ ] Console에 빨간 줄이 없다.
- [ ] `git push -u origin dark-mode` 뒤 GitHub 브랜치 목록에 `dark-mode`가 보인다.

공개 페이지는 오늘 바뀌지 않는다. Pages는 `main`만 배포하기 때문이며 정상이다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 다크 모드와 함수 재사용 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone …` 뒤 `git switch dark-mode` |
| 5–25분 | `[다크 모드]` 버튼과 `body.dark` 규칙을 만들어 `classList.toggle('dark')`로 켜고 끈다 |
| 25–40분 | 두 버튼이 `countUp()` 한 함수를 쓰게 정리한다 |
| 40–50분 | `git commit` → `git push` → `git switch main` → `git merge dark-mode` → `git push` → `git branch -d dark-mode` |
| 50–55분 | 기기 모드 375px와 1280px에서 다크 모드를 확인한다 |
| 55–60분 | 끝 루틴: 공개 주소 새로고침 → **캡처 1장** → 공용 PC면 자격 증명 삭제 |

### 1. 다크 모드 버튼과 CSS 규칙 (`body.dark`)

`index.html`의 같은 문단 안에 버튼을 하나 더 넣고, `styles.css` **맨 아래**에 규칙 하나를 더한다.
[따라하기 10~12단계](walkthrough.md#10-저장소-받아와-브랜치로-돌아가기)를 본다.

- 버튼 두 개를 같은 `<p>` 안에 둔다. 앞의 버튼과 한 줄에 나란히 보인다.
- `body.dark`는 붙여 쓰고, `body.dark .card`는 띄어 쓴다. 띄우면 "그 안에 있는"이라는 뜻이 된다.
- 4주차에 쓴 53줄은 그대로 두고 아래에 더한다. 위의 규칙을 지우지 않는다.

### 2. 켜고 끄기 (`classList.toggle`)

`darkButton`에 클릭 리스너를 붙이고 `document.body.classList.toggle('dark');` 한 줄을 쓴다.
[따라하기 13단계](walkthrough.md#13-classlisttoggle로-다크-모드-켜고-끄기)를 본다.

- 누를 때마다 켜졌다 꺼진다. `add`만 쓰면 한 번 켜진 뒤 꺼지지 않는다.
- 색이 안 바뀌면 DevTools **Elements**에서 `<body class="dark">`로 바뀌는지 먼저 본다.
  - class는 붙는데 색이 그대로면 `styles.css`의 규칙 철자를, class가 안 붙으면 `app.js`를 본다.
- `classList.toggle`의 철자를 틀리면 `Uncaught TypeError: … is not a function`이 뜬다.

### 3. 두 버튼이 한 함수를 쓰게 정리 (`countUp()`)

클릭 횟수를 올리는 두 줄을 `function countUp() { }`으로 빼내고, 두 리스너에서 `countUp();`으로 부른다.
[따라하기 14단계](walkthrough.md#14-두-버튼이-한-함수를-쓰게-정리하기)를 본다.

- 함수는 리스너보다 **위**에 둔다. 5주차 `greet`·`hello`와 같은 자리다.
- 부를 때는 괄호를 붙인다. `countUp;`이라고만 쓰면 아무 일도 일어나지 않는다.
- 돌려줄 값이 없으므로 `return`은 쓰지 않는다.
- 정리한 뒤에도 두 버튼 클릭 합계가 그대로 세어지는지 확인한다. `[인사 바꾸기]` 2번 + `[다크 모드]` 1번 = `클릭 3회`.

### 4. main에 합치기 (`merge` · `branch -d`)

`dark-mode`를 먼저 push하고, main으로 돌아가 합친 뒤 브랜치를 지운다. [따라하기 15~16단계](walkthrough.md#15-오늘-작업-commit하고-push-하기)를 본다.

- **push를 먼저 한다.** 1일차에 push해 두었으므로, 2일차 commit을 push하지 않은 채 `git branch -d`를 하면 `error: the branch 'dark-mode' is not fully merged`가 뜬다.
- **`git merge dark-mode`를 건너뛰고 지우지 않는다.** merge 전에 지우면 거절되지 않고 경고만 뜬 뒤 그냥 지워진다(아래 「막혔을 때」 표).
- `git switch main` 직후 화면이 5주차로 돌아간다. merge하면 돌아온다. 정상이다.
- merge 출력에 `Fast-forward`와 세 파일 이름이 보이면 맞다.
- merge 뒤 push해야 공개 페이지가 바뀐다. 1분쯤 기다렸다가 새로고침한다.

### 5. 375px와 1280px에서 확인

DevTools 기기 모드(**Ctrl+Shift+M**)로 375px과 1280px에서 다크 모드를 켜 본다.

- 375px에서는 4주차 `@media` 규칙이 살아 있어 nav가 세로로 접힌다. 다크 모드와 함께 확인한다.
- 카드 색과 글자 색이 둘 다 바뀌어야 읽을 수 있다. 글자가 안 보이면 `color` 줄을 확인한다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 다시 확인해도 된다. `git status`에 `Your branch is ahead`가 있으면 push를 안 한 것이다 |
| 1일차에 push했는데 공개 페이지가 그대로다 | 정상이다. `dark-mode` 브랜치에 올렸고 Pages는 `main`만 배포한다. GitHub 브랜치 목록에 `dark-mode`가 보이면 된 것이다 |
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` | 버튼을 못 찾았다. `#hello-button`·`#dark-button` 철자와 `index.html`의 `id`를 비교한다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` | `#greeting`·`#count`를 못 찾았다. 철자를 보고, 그다음 `script` 줄에 `defer`가 있는지 본다 |
| `Uncaught TypeError: document.body.classList.tggle is not a function` | `toggle` 철자가 틀렸다. `add`·`remove`·`toggle` 셋 중 하나여야 한다 |
| `Uncaught TypeError: helloButton.addEventListner is not a function` | `addEventListener` 철자가 틀렸다. `Listener`의 `e`를 빠뜨리기 쉽다 |
| 버튼을 눌러도 아무 일도 안 일어난다 | Console에 빨간 줄이 있는지 먼저 본다. 없으면 `addEventListener`를 맡긴 줄이 있는지, 버튼의 `id`가 맞는지 본다 |
| 계속 `클릭 1회`만 나온다 | `let count = 0;`이 리스너 **안**에 있다. 밖(맨 위)으로 옮긴다 |
| 새로고침하면 `클릭 0회`로 돌아간다 | 정상이다. 새로고침하면 브라우저가 파일을 다시 읽는다. 새로고침해도 남게 하는 것은 11주차다 |
| 다크 모드 버튼을 눌러도 색이 안 바뀐다 | Elements에서 `<body class="dark">`가 되는지 본다. class가 붙는데 색이 그대로면 `styles.css`의 `body.dark` 철자, 안 붙으면 `app.js`를 본다 |
| 한 번 어두워지면 다시 밝아지지 않는다 | `classList.add`를 썼다. `toggle`로 바꾼다 |
| 카드는 그대로 흰색이다 | `body.dark .card` 줄이 빠졌다. `body.dark`만으로는 카드 배경이 바뀌지 않는다 |
| `error: the branch 'dark-mode' is not fully merged` | 1일차에 push해 둔 브랜치인데, 2일차 commit을 push하지 않은 채 지우려 한 것이다. `git push` 뒤 `git switch main` → `git merge dark-mode` → `git push` 순서로 하고 마지막에 지운다. 1일차에 push한 적이 없으면 이 줄 없이 그냥 지워지는데 그것도 정상이다 |
| merge를 건너뛰고 `git branch -d dark-mode`부터 쳤다 | 거절되지 않는다. `warning: deleting branch 'dark-mode' that has been merged to` / `'refs/remotes/origin/dark-mode', but not yet merged to HEAD`만 뜨고 브랜치는 그대로 지워진다. 경고를 지나치면 오늘 작업이 main에 없는 채로 끝난다. `git branch dark-mode origin/dark-mode`로 되살린 뒤 `git merge dark-mode`부터 다시 한다 |
| `error: cannot delete branch 'dark-mode' used by worktree at '…'` | 지금 그 브랜치에 있다. `git switch main`을 먼저 한다 |
| `fatal: The current branch dark-mode has no upstream branch.` | 처음 올리는 브랜치에 `git push`만 쳤다. `git push -u origin dark-mode` |
| `Already up to date.` | main이 아니라 `dark-mode`에서 merge했다. `git branch`로 `*` 위치를 보고 `git switch main` |
| `fatal: invalid reference: dark-mode` | 브랜치를 아직 만들지 않았다. `git switch -c dark-mode` |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시와 `git log --oneline`을 본다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://<아이디>.github.io/my-web/`을 열고 **다크 모드를 켠 뒤** 한 화면을 캡처한다.

- 배경과 카드가 어둡다.
- 카드 한 줄이 `반갑습니다. 오늘도 좋은 하루 되세요.`로 바뀌어 있다.
- `클릭 N회`의 `N`이 **1 이상**이다.
- 주소창이 함께 보이게 찍는다.

캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- nav를 열고 닫는 버튼을 만들어 본다. `index.html`의 버튼 문단에 `<button id="menu-button" type="button">메뉴</button>`를 하나 더 두고, `styles.css`에 아래 규칙을 더한 뒤 `app.js` 맨 위에서 그 버튼을 찾아 두고 `classList.toggle('open')`을 쓴다.

```css
nav.open {
  display: none;
}
```

- `[다크 모드]` 버튼의 글자를 상태에 따라 바꿔 본다(`darkButton.textContent = '밝은 모드';`).
- `클릭 ${count}회`를 `클릭 ${count}번`으로 바꿔 보고, 고칠 곳이 `countUp()` 한 곳뿐인 것을 확인한다.
- `about.html`에도 다크 모드를 넣으려면 무엇이 필요할지 생각해 본다(페이지마다 자기 js가 필요하다. 7주차에 `guestbook.js`로 해 본다).

추가 과제는 선택 사항이며 채점하지 않는다.
