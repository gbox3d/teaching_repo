# 7주차 실습 — 폼을 제출하면 화면에 한 줄 남기기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules

3주차에 만들어 둔 `guestbook.html`의 폼이 이번 주에 동작한다. **[남기기]**를 누르면 입력한 이름과 메시지를 읽어
페이지 아래 카드에 `이름: 메시지` 한 줄로 띄우고, 칸이 비어 있으면 안내 문구를 보여 준다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.
이번 주에는 브랜치를 만들지 않고 `main`에서 바로 작업한다.

## 1일차 — 폼 제출을 받아 화면에 표시하기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` |
| 5–18분 | `guestbook.html`에 `id`와 결과 자리를 만들고 `guestbook.js`를 연결해 submit 리스너를 붙인다 |
| 18–32분 | 입력한 값을 읽어 `#last` 카드에 `이름: 메시지` 한 줄로 표시한다 |
| 32–42분 | 이름이 비면 `이름을 입력하세요.`를 띄우고 커서를 이름 칸으로 옮긴다 |
| 42–48분 | `form.reset()`으로 폼을 비우고 커서를 이름 칸에 돌려 둔다 |
| 48–55분 | 8주차 리허설 starter 세 파일을 받아 `file://`로 열어 본다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 확인·확인용 캡처 → 공용 PC면 자격 증명 삭제 |

### 1. 저장소 받아오기 (`git pull` · `git clone`)

지난 시간과 같은 PC면 `git pull`, 다른 PC에서 처음이면 `git clone`부터 한다. [따라하기 1단계](walkthrough.md#1-저장소-받아오기)를 본다.

- 시작 전 `git status`가 `On branch main`, `nothing to commit, working tree clean`이어야 한다.
- 6주차 `dark-mode` 브랜치가 아직 남아 있으면 `git switch main` 뒤 `git merge dark-mode`부터 끝낸다.
- 3주차에 `guestbook.html`을 만들지 못했으면 조교에게 6주차 `examples/day2` 폴더를 받아 그 폴더에서 시작한다.

### 2. 결과 자리 만들고 `guestbook.js` 연결하기 (`id` · `script defer`)

`guestbook.html`을 세 곳 고치고, 새 파일 `guestbook.js`를 만들어 맨 위에서 요소 다섯 개를 찾아 둔다.
[따라하기 2~3단계](walkthrough.md#2-guestbookhtml에-결과-자리-만들기)를 본다.

- `<head>`의 `<link>` 줄 아래에 `<script src="guestbook.js" defer></script>`를 넣는다. `defer`를 빠뜨리지 않는다.
- `<form>`에 `id="guestbook-form"`을 붙인다. 이름·이메일·메시지 칸의 `id`는 3주차에 붙여 둔 것을 그대로 쓴다.
- 3주차에 적어 둔 `지금은 눌러도 주소창만 바뀐다…` 문단을 지우고 그 자리에 `<p id="notice"></p>`와 `마지막으로 남긴 글` 제목, `<p class="card" id="last">`를 넣는다.
- `index.html`은 `app.js`를, `guestbook.html`은 `guestbook.js`를 부른다. 한 페이지에 자기 js 하나다.
- 이메일 칸은 이번 주에 읽지 않는다. `guestbook.js`에서 찾아 두지 않는다.

### 3. 제출 받기와 값 읽기 (`submit` · `preventDefault` · `value` · `trim`)

폼에 `'submit'` 리스너를 맡기고 첫 줄에서 새로고침을 막은 뒤, 두 칸의 값을 읽는다.
[따라하기 4~5단계](walkthrough.md#4-제출을-받아-새로고침-막기)를 본다.

- 리스너는 버튼이 아니라 **폼**에 맡긴다. 입력 칸에서 Enter를 쳐도 제출이 일어나기 때문이다.
- 첫 줄은 `event.preventDefault();`다. 이 줄이 없으면 주소 끝에 `?`가 붙고 화면이 처음으로 돌아간다.
- 값을 읽는 `const name = nameInput.value.trim();`은 리스너 **안**에 둔다. 밖에 두면 언제 눌러도 빈 값이다.
- `console.log(name, message);`로 먼저 Console에 찍어 보고, 값이 맞으면 다음으로 간다.

### 4. 한 줄로 표시하기 (`textContent`)

읽은 값을 템플릿 문자열로 만들어 `#last` 카드에 넣는다. [따라하기 6단계](walkthrough.md#6-마지막-글-한-줄로-표시하기)를 본다.

- `last.textContent = ` 다음에 백틱으로 `` `${name}: ${message}` ``를 쓴다. 사이는 **콜론과 공백**이다.
- 6주차 `textContent`와 같다. 바뀌는 것은 화면이고 HTML 파일은 그대로다.
- 확인했으면 `console.log` 줄은 지운다.

### 5. 빈값 안내와 커서 옮기기 (`if` · `return` · `focus`)

이름이 비었으면 안내만 하고 멈춘다. [따라하기 7단계](walkthrough.md#7-이름이-비면-안내하고-커서-옮기기)를 본다.

- `if (name === '') { … }` 안에 안내 문구·`nameInput.focus()`·`return` 세 줄을 넣는다.
- `return`이 없으면 안내를 띄운 **뒤에도** 아랫줄이 실행되어 `: 안녕하세요`가 표시된다.
- 이름 칸에 **공백만** 넣고 눌러도 안내가 떠야 한다. 뜨지 않으면 `.trim()`이 빠진 것이다.
- 성공했을 때 `notice.textContent = '';`로 지난 안내를 지운다. 이 줄이 없으면 문구가 계속 남는다.

### 6. 폼 비우기와 리허설 starter 열어 보기 (`reset`)

표시한 **뒤에** 폼을 비우고 커서를 이름 칸에 돌려 둔다. 그다음 8주차 리허설 파일을 받아 둔다.
[따라하기 8~9단계](walkthrough.md#8-폼-비우고-다음-입력-준비하기)를 본다.

- `form.reset();` → `nameInput.focus();` 순서다. 먼저 비우면 읽을 값이 없어진다.
- [8주차 리허설 starter](../week08_midterm/examples/rehearsal_starter) 세 파일을 `my-web` **밖**의 새 폴더 `midterm-practice`에 넣는다.
- `index.html`을 더블클릭해 열고 Console에 `리허설 starter 준비 완료`가 보이면 된다. 오늘은 풀지 않는다.
- [8주차 채점표](../week08_midterm/rubric.md)의 `폼 입력·빈값 안내 3` 줄이 오늘 만든 것이다.

### 7. 오늘 확인할 것

- [ ] **[남기기]**를 눌러도 주소가 그대로고 화면이 처음으로 돌아가지 않는다.
- [ ] 카드에 `student01: 안녕하세요`처럼 `이름: 메시지`가 보인다.
- [ ] 누른 뒤 입력 칸이 비워지고 커서가 이름 칸에 있다.
- [ ] 이름을 비우고 누르면 `이름을 입력하세요.`가 보이고 글은 표시되지 않는다.
- [ ] F12 Console에 빨간 줄이 없다.
- [ ] push한 뒤 공개 주소에서 같은 동작이 되는 것을 확인용으로 한 장 찍어 두었다.

제출 캡처는 2일차 마지막에 한 번만 찍는다.

## 2일차 — 두 칸 검사와 안내 문구 다듬기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` |
| 5–15분 | GitHub 웹에서 `README.md`를 만들고 `git pull`로 받아 온다 |
| 15–35분 | 메시지 칸 빈값 안내를 더하고, 다시 입력하면 안내 문구가 지워지게 한다 |
| 35–50분 | 8주차 리허설 문항 하나(폼)를 풀어 본다 |
| 50–55분 | 두 번째 글을 남겨 보고 Console에 빨간 줄이 없는지 확인한다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 새로고침 → **캡처 1장** → 공용 PC면 자격 증명 삭제 |

### 1. GitHub 웹에서 README 만들고 받아오기 (`Add file` · `git pull`)

저장소 화면에서 `README.md`를 만들고 `git pull`로 내 PC에 받아 온다. [따라하기 11단계](walkthrough.md#11-github-웹에서-readme-만들고-받아오기)를 본다.

- **Add file › Create new file** → 파일 이름 `README.md` → 내용 입력 → **Commit changes…** → **Commit changes**.
- 내용은 다섯 줄이면 된다. 저장소 이름, 공개 주소, 페이지 세 개. 실명·학번은 넣지 않는다.
- 만든 직후 내 폴더에는 없다. `git pull`을 해야 생긴다. 탐색기에 `README.md`가 보이면 된 것이다.
- **pull을 먼저 한다.** 오늘 작업을 commit한 뒤에 pull하면 합치는 commit이 하나 더 생기고, pull을 건너뛰면 push가 거부된다.

### 2. 메시지 칸도 검사하기 (`if` · `focus`)

이름 검사 블록 아래에 메시지 검사 블록을 같은 모양으로 넣는다. [따라하기 12단계](walkthrough.md#12-메시지-칸도-검사하기)를 본다.

- 안내 문구는 `메시지를 입력하세요.`로 이름 쪽과 다르게 쓴다. 문구만 보고 어느 칸인지 알 수 있어야 한다.
- 커서는 `messageInput.focus()`로 메시지 칸에 둔다.
- 이름과 메시지를 **둘 다** 비우고 눌러 이름 안내가 먼저 나오는지 본다. 위에서부터 차례로 검사하기 때문이다.

### 3. 다시 입력하면 안내 문구 지우기 (`function` · `'input'`)

안내를 지우는 한 줄을 함수로 묶고, 두 입력 칸에 맡긴다. [따라하기 13단계](walkthrough.md#13-다시-입력하면-안내-문구-지우기)를 본다.

- `function clearNotice() { … }`를 요소를 찾아 둔 다섯 줄 **아래**에 만든다.
- 리스너 안의 `notice.textContent = '';`를 `clearNotice();`로 바꾼다. 같은 일을 두 곳에서 하므로 함수로 묶는다.
- 파일 **맨 끝**에 `nameInput.addEventListener('input', clearNotice);`와 `messageInput.addEventListener('input', clearNotice);` 두 줄을 더한다.
- 맡길 때 `clearNotice`에 **괄호를 붙이지 않는다.** 붙이면 맡기는 순간 한 번 실행되고 만다.
- 안내가 뜬 상태에서 한 글자만 쳐도 문구가 사라지면 된 것이다.

### 4. 리허설 문항 하나 풀어 보기 (8주차 대비)

1일차에 받아 둔 `midterm-practice` 폴더의 `app.js`에서 **문제 4-1·4-2** 주석 자리만 채운다.
[따라하기 15단계](walkthrough.md#15-리허설-문항-하나-풀어-보기)를 본다.

- 오늘 만든 `guestbook.js`와 같은 모양이고 이름만 `joinForm`·`nameInput`·`reasonInput`·`result`로 다르다.
- 신청 이유까지 넣고 누르면 `#result`에 `이름: 신청 이유`가 보이고, 이름을 비우면 안내가 보이며 커서가 이름 칸으로 간다.
- 막히면 `guestbook.js`를 옆에 두고 이름만 바꿔 읽는다. [해답](../week08_midterm/examples/rehearsal_solution)은 다 푼 뒤에 연다.
- 이 폴더는 `my-web`에 넣지 않는다. 채점하지 않는다.

### 5. 두 번째 글 남겨 보기

글을 하나 남긴 뒤 다른 이름·메시지로 한 번 더 남긴다. [따라하기 14단계](walkthrough.md#14-두-번째-글을-남겨-보기)를 본다.

- 카드에는 **마지막 글 하나만** 남는다. 지금 단계에서 정상이므로 고치지 않는다.
- 글을 쌓아 목록으로 보여 주는 것은 10주차, 새로고침해도 남게 하는 것은 11주차다.

### 6. 오늘 확인할 것

- [ ] 저장소 첫 화면에 README 내용이 보이고 내 폴더에도 `README.md`가 있다.
- [ ] 이름 칸, 메시지 칸을 각각 비우고 누르면 서로 다른 안내 문구가 보인다.
- [ ] 안내가 뜬 뒤 그 칸에 한 글자를 치면 문구가 사라진다.
- [ ] 이름과 메시지를 채워 누르면 카드에 `이름: 메시지`가 보이고 칸이 비워진다.
- [ ] F12 Console에 빨간 줄이 없다.
- [ ] 공개 주소에서 결과가 보이는 화면을 캡처 1장으로 저장했다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 다시 확인해도 된다. `git status`에 `Your branch is ahead`가 있으면 push를 안 한 것이다 |
| **[남기기]**를 누르면 화면이 처음으로 돌아가고 주소가 `…/guestbook.html?`로 바뀐다 | `event.preventDefault();`가 없거나, `guestbook.html`에 `<script src="guestbook.js" defer></script>` 줄이 없다. 이때 **Console에는 빨간 줄이 없다.** 오류가 아니라 브라우저가 폼을 보내려고 페이지를 다시 연 것이다 |
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` | 폼을 못 찾았다. `#guestbook-form` 철자와 `<form>`의 `id`를 비교하고, 그다음 `script` 줄에 `defer`가 있는지 본다 |
| `Uncaught ReferenceError: preventDefault is not defined` | `event.`를 빠뜨렸다. `event.preventDefault();`로 쓴다 |
| `Uncaught TypeError: Cannot read properties of undefined (reading 'trim')` | `.value` 철자가 틀렸다(`velue`). 오류 줄 끝의 `guestbook.js:10`으로 줄을 먼저 찾는다 |
| `Uncaught TypeError: nameInput.value.trm is not a function` | `trim` 철자가 틀렸다 |
| `Uncaught TypeError: form.rest is not a function` | `reset` 철자가 틀렸다 |
| `Uncaught TypeError: Assignment to constant variable.` | `if (name === '')`를 `if (name = '')`로 썼다. `=`가 세 개여야 비교다 |
| 이름을 비웠는데 `: 안녕하세요`가 표시된다 | `if` 블록 안에 `return`이 없다. 안내만 하고 멈춰야 한다 |
| 이름 칸에 공백만 넣었는데 그대로 통과된다 | `.trim()`이 빠졌다. `nameInput.value.trim()`으로 읽는다 |
| 안내 문구가 계속 남아 있다 | 1일차라면 성공했을 때 `notice.textContent = '';`가 빠진 것이다. 2일차라면 `'input'` 철자를 보고, `clearNotice`에 괄호를 붙이지 않았는지 본다 |
| 눌러도 아무 일도 안 일어나고 Console도 조용하다 | `guestbook.html`에 `script` 줄이 없거나 파일 이름이 다르다. 대소문자까지 `guestbook.js`로 같아야 한다 |
| 눌러도 아무 일도 안 일어나고 Console도 조용한데 커서가 이메일 칸으로 간다 | 이메일 칸에 적은 값이 메일 주소 모양인지 본다. `type="email"`이라 모양이 맞지 않으면 브라우저가 제출 자체를 막는다. 이번 주에는 이메일 칸을 비워 두면 된다 |
| 값은 보이는데 입력 칸이 안 비워진다 | `form.reset();`이 빠졌다. `last.textContent = …` 줄 **아래**에 둔다 |
| 표시되는 값이 늘 비어 있다 | `const name = …` 줄이 리스너 **밖**에 있거나 `form.reset()`이 값을 읽기 **전**에 있다 |
| 두 번째 글을 남기면 앞 글이 사라진다 | 정상이다. 카드가 한 줄이다. 쌓는 것은 10주차다 |
| 새로고침하면 남긴 글이 사라진다 | 정상이다. 바뀐 것은 화면이고 HTML 파일은 그대로다. 남게 하는 것은 11주차다 |
| `! [rejected]        main -> main (fetch first)` / `hint: Updates were rejected because the remote contains work that you do not` | GitHub 웹에서 만든 README를 받지 않고 push했다. `git pull` 뒤 다시 `git push`한다 |
| `error: The following untracked working tree files would be overwritten by merge:` / `README.md` / `Please move or remove them before you merge.` / `Aborting` | 웹에서 만든 README를 로컬에도 따로 만들어 두었다. 로컬 `README.md`를 지우거나 이름을 바꾼 뒤 다시 `git pull`한다 |
| 파일을 고쳐 저장만 한 채 `git pull`했다 | 오늘처럼 바뀐 파일이 서로 다르면(`guestbook.js` ↔ `README.md`) 그대로 `Fast-forward`로 성공한다. 같은 파일을 GitHub 웹에서도 고쳤을 때만 `error: Your local changes to the following files would be overwritten by merge:`가 나오고, 그때는 `git add .` → `git commit` 뒤에 `git pull`한다 |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시와 `git log --oneline`을 본다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://<아이디>.github.io/my-web/guestbook.html`을 열고 이름과 메시지를 넣어 **[남기기]**를 누른 화면을 캡처한다.

- **마지막으로 남긴 글** 아래 카드에 `이름: 메시지`가 한 줄로 보인다.
- 주소창이 함께 보이게 찍는다.
- 빈값 안내(`이름을 입력하세요.`)는 실습 중에 확인하는 것이고 캡처에는 없어도 된다.

캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 이메일 칸도 검사해 본다. 비어 있으면 `이메일을 입력하세요.`를 띄우고 `emailInput.focus()`로 커서를 옮긴다. 채점에는 넣지 않는다.
- 안내 문구가 보일 때 글자 색을 바꿔 본다. `styles.css`에 `#notice { color: #b3261e; }` 한 줄을 더하면 된다.
- 남긴 글 아래에 글자 수를 함께 보여 준다. `message.length`를 템플릿 문자열에 넣어 `` `${name}: ${message} (${message.length}자)` ``로 써 본다.
- **[남기기]** 대신 **이름 칸**에서 **Enter**를 쳐 보고 같은 동작이 되는지 확인한다. 폼에 맡겼기 때문에 둘 다 잡힌다. 메시지 칸(`textarea`)에서는 Enter가 줄바꿈이라 제출되지 않는다.
- 리허설 starter의 문제 3(버튼 두 개)까지 풀어 본다. 6주차에 한 것과 같다.

추가 과제는 선택 사항이며 채점하지 않는다.
