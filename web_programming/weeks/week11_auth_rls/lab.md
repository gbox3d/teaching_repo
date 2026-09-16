# 11주차 실습 — 객체로 바꾸고 브라우저에 저장하기

**11주차부터 확인·캡처는 공개 URL에서만 한다 — 로컬과 공개 주소는 저장소가 다르다.**
내 PC에서 파일을 직접 연 화면(`file://`)에 남긴 글은 공개 주소에 나타나지 않는다. 완료 기준과 제출 캡처는 모두 공개 주소에서 만든다.

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls

10주차 방명록은 한 줄이 `하늘: 안녕하세요`라는 글자 한 덩어리였고, 새로고침하면 목록이 사라졌다.
이번 주에는 항목을 이름·메시지·날짜 **객체**로 바꾸고, 목록을 브라우저 저장소에 저장해 새로고침해도 남게 한다.
고치는 파일은 `guestbook.html`과 `guestbook.js` 둘뿐이다. 모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.
`student01`은 예시 아이디이므로 본인 아이디로 바꾼다. 이번 주에도 브랜치를 만들지 않고 `main`에서 바로 작업한다.

## 1일차 — 항목을 객체로 바꾸기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` |
| 5–30분 | `items.push`에 넣는 값을 객체로 바꾸고, 목록 한 줄을 점 표기로 고친다 |
| 30–45분 | 날짜가 함께 보이는지 확인하고, 빈칸 안내 문구를 한 줄로 합친다 |
| 45–55분 | 빈 목록 안내를 개수 자리로 옮기고, Console에서 `items`를 펼쳐 본다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 확인·확인용 캡처 → 공용 PC면 자격 증명 삭제 |

### 1. 저장소 받아오기 (`git pull` · `git clone`)

지난 시간과 같은 PC면 `git pull`, 다른 PC에서 처음이면 `git clone`부터 한다. [따라하기 1단계](walkthrough.md#1-저장소-받아오기)를 본다.

- 시작 전 `git status`가 `On branch main`, `nothing to commit, working tree clean`이어야 한다.
- `guestbook.html`에 `<p id="empty">`와 `<p id="count">0개</p>` 두 줄이 보이면 10주차 끝 상태가 맞다.
- 파일이 없거나 이어 하기 어려우면 조교에게 10주차 `examples/day2` 폴더를 받아 그 폴더에서 시작한다.

### 2. 남긴 글을 객체로 바꾸기 (`{ name: …, message: …, date: … }`)

submit 리스너 안의 `items.push(\`${name}: ${message}\`);` 한 줄을 날짜 한 줄 + 객체 한 줄로 바꾼다.
[따라하기 2단계](walkthrough.md#2-남긴-글을-객체로-바꾸기)를 본다.

- `{ }` 안에 `이름: 값` 쌍 세 개를 쉼표로 이어 적는다. 이름표는 `name`·`message`·`date` 세 개로 고정한다.
- `name: name`의 왼쪽은 객체의 이름표, 오른쪽은 바로 위에서 만든 변수다. 글자가 같아도 다른 자리다.
- 날짜 줄 `const today = new Date().toLocaleDateString();`은 **복붙 틀**이다. `items.push` 위에 둔다.
- 이 단계까지 하면 목록에 `[object Object]`가 보인다. 오류가 아니며 3번에서 고친다.

### 3. 목록 한 줄을 점 표기로 고치기 (`items[i].name`)

`showList()` 안의 `li.textContent = items[i];` 한 줄만 바꾼다. [따라하기 3단계](walkthrough.md#3-목록-한-줄을-점-표기로-고치기)를 본다.

- 대괄호로 **몇 번째**인지 고르고, 점으로 **무슨 값**인지 고른다. `items[0].name`은 "첫 번째 글의 이름"이다.
- 백틱과 `${ }` 안에 세 값을 넣는다. 날짜는 괄호로 감싼다. 점 앞뒤에 빈칸을 넣지 않는다.
- 삭제 버튼 틀은 10주차 그대로 둔다. 오늘 `showList()`에서 바꾸는 줄은 이 한 줄뿐이다.
- 이름 자리에 `undefined`가 보이면 이름표 철자가 다른 것이다. 오류는 나지 않으니 화면 글자로 찾는다.

### 4. 안내 문구를 한 줄로 합치기 (`||`)

`clearNotice()` 함수와 `input` 리스너 두 줄을 지우고, `if` 두 덩어리를 한 덩어리로 합친다.
[따라하기 4단계](walkthrough.md#4-안내-문구를-한-줄로-합치기)를 본다.

- `if (name === '' || message === '')`의 `||`는 **또는**이다. 둘 중 하나라도 비면 안내를 보여 주고 `return`으로 멈춘다.
- 안내 문구는 `이름과 메시지를 모두 입력하세요.` 한 가지로 통일한다.
- 안내를 지우는 줄 `notice.textContent = '';`은 제출이 성공한 자리 한 곳에만 둔다.
- 지우는 순서는 바꿔도 된다. 다만 `clearNotice`라는 이름이 파일에 **한 군데도 남지 않아야** 한다.

### 5. 빈 목록 안내를 개수 자리로 옮기기 (`#count`)

`guestbook.html`에서 `<p id="empty">` 줄을 지우고, `guestbook.js`에서 `empty`를 없앤 뒤 `showList()` 끝을 다섯 줄로 줄인다.
[따라하기 5단계](walkthrough.md#5-빈-목록-안내를-개수-자리로-옮기기)를 본다.

- 한 자리(`#count`)가 두 가지 일을 한다. 목록이 비면 안내 문장, 아니면 `3개`다.
- `<p id="count">`의 처음 글자도 `0개`에서 `아직 남긴 글이 없습니다.`로 바꾼다.
- `guestbook.js`에 `empty`가 한 줄이라도 남으면 Console에 빨간 줄이 뜬다. 찾기(Ctrl+F)로 확인한다.
- 여기까지 하면 1일차 `guestbook.js`가 47줄이 된다. 줄 수가 크게 다르면 지울 줄이 남은 것이다.

### 6. Console에서 `items` 펼쳐 보기

글을 두세 개 남긴 뒤 Console에 `items`, `items[0]`, `items[0].name`, `items[0].date`를 차례로 쳐 본다.
[따라하기 6단계](walkthrough.md#6-console에서-items-펼쳐-보기)를 본다.

- 배열은 대괄호 `[ ]`, 객체는 중괄호 `{ }`로 보인다. 삼각형을 눌러 세 값이 들어 있는지 본다.
- 없는 이름표를 물으면 `undefined`가 나온다. 오류가 아니다.
- 화면의 한 줄과 `items[0]`의 세 값이 같은지 대조한다.

### 7. 오늘 확인할 것

- [ ] 목록 한 줄이 `하늘: 안녕하세요 (2026. 9. 16.)`처럼 이름·메시지·날짜로 보인다.
- [ ] 이름 칸만 비우거나 메시지 칸만 비우고 눌러도 `이름과 메시지를 모두 입력하세요.`가 보인다.
- [ ] 목록이 비면 개수 자리에 `아직 남긴 글이 없습니다.`가 보이고, 글이 있으면 `2개`처럼 숫자가 보인다.
- [ ] Console에 `items[0].name`을 치면 화면의 이름과 같은 값이 나온다.
- [ ] F12 Console에 빨간 줄이 없다.
- [ ] push한 뒤 공개 주소에서 같은 화면이 되는 것을 확인용으로 한 장 찍어 두었다.

제출 캡처는 2일차 마지막에 한 번만 찍는다.

## 2일차 — 브라우저에 저장하고 되살리기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` |
| 5–25분 | `saveList()`를 만들고 추가한 뒤·삭제한 뒤 두 곳에서 부른다 |
| 25–40분 | `let items = …` 줄을 복원 한 줄로 바꿔 새로고침해도 남게 한다 |
| 40–55분 | **[전체 지우기]** 버튼을 붙이고 새로고침해 비어 있는지 확인한다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소에서 **캡처 1장** → 공용 PC면 자격 증명 삭제 |

### 1. 저장하는 함수 만들기 (`JSON.stringify` · `setItem`)

`function showList() {` 위에 `saveList()` 함수를 만든다. [따라하기 8단계](walkthrough.md#8-저장하는-함수-savelist-만들기)를 본다.

- 저장 칸에는 **문자열만** 들어간다. 그래서 넣기 전에 `JSON.stringify(items)`로 바꾼다.
- 키 이름은 `'guestbook'`으로 고정한다. 철자가 다르면 다른 칸에 저장되고 다음에 열 때 아무것도 못 찾는다.
- 함수 이름은 `saveList`다. `showList`와 한 글자 차이이므로 천천히 읽는다.
- 만들기만 하면 화면은 그대로다. 부르는 곳이 아직 없기 때문이다.

### 2. 추가한 뒤와 삭제한 뒤에 저장하기 (`saveList()`)

`saveList();` 한 줄을 두 곳에 넣는다. [따라하기 9단계](walkthrough.md#9-추가한-뒤와-삭제한-뒤에-저장하기)를 본다.

- 첫 번째는 submit 안 `items.push({ … });` 바로 아래, 두 번째는 삭제 버튼 틀 안 `items.splice(i, 1);` 바로 아래다.
- 저장은 **바뀐 뒤에** 한다. 들여쓰기가 두 곳에서 다르다.
- F12 **Application › Storage › Local Storage**에서 지금 주소를 고르면 `guestbook` 키와 값이 보인다.
- 값이 `[{"name":"하늘","message":"안녕하세요","date":"2026. 9. 16."}]`처럼 보이면 된 것이다. 새로고침하면 아직 사라진다.

### 3. 페이지를 열 때 되살리기 (`JSON.parse` · `getItem` · `|| []`)

`let items = [];` 한 줄을 복원 한 줄로 바꾼다. [따라하기 10단계](walkthrough.md#10-페이지를-열-때-되살리기)를 본다.

- 안에서 밖으로 읽는다. 꺼내기(`getItem`) → 되살리기(`JSON.parse`) → 없으면 빈 배열(`|| []`).
- 이 한 줄은 **복붙 틀**이다. 그대로 옮겨 쓰고 키 이름만 확인한다.
- 글을 세 개 남기고 새로고침해 세 줄과 `3개`가 그대로면 된 것이다. 탭을 닫았다 다시 열어도 남는다.
- 파일 맨 끝의 `showList();`가 되살린 배열을 그린다. 10주차에 넣어 둔 줄이며 지우지 않는다.

### 4. 전체 지우기 버튼 붙이기 (`removeItem`)

`guestbook.html`에 버튼 한 줄, `guestbook.js`에 선언 한 줄과 리스너 다섯 줄을 넣는다.
[따라하기 11단계](walkthrough.md#11-전체-지우기-버튼-붙이기)를 본다.

- **HTML을 먼저 고친다.** JavaScript만 고치면 Console에 빨간 줄이 하나 뜬다.
- 버튼 안에서 두 가지를 한다. `items = [];`로 화면 쪽 배열을 비우고 `removeItem('guestbook')`으로 저장 칸을 지운다.
- 둘 중 하나만 하면 새로고침할 때 목록이 되살아나거나 저장 칸만 남는다.
- 배열을 통째로 바꾸므로 `items`는 `let`이어야 한다. 10주차에 그렇게 선언해 두었다.

### 5. 오늘 확인할 것

- [ ] 글을 남기고 **새로고침**해도 목록과 개수가 그대로 남아 있다.
- [ ] Application 탭에 `guestbook` 키가 있고 값이 `[{"name":…}]` 모양이다.
- [ ] 항목 하나를 **[삭제]**한 뒤 새로고침해도 그 줄이 돌아오지 않는다.
- [ ] **[전체 지우기]**를 누르면 목록이 비고, 새로고침해도 비어 있으며 `guestbook` 키가 사라진다.
- [ ] F12 Console에 빨간 줄이 없다.
- [ ] 공개 주소에서 글 3개 → 새로고침 → Application 탭을 함께 연 화면을 캡처 1장으로 저장했다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 다시 확인해도 된다. `git status`에 `Your branch is ahead of 'origin/main' by 1 commit.`이 있으면 push를 안 한 것이다 |
| 내 PC에서 파일을 직접 열면 목록이 남는데 공개 주소에서는 비어 있다 | 고장이 아니다. 저장 칸은 주소마다 따로 있다. 이번 주 확인과 캡처는 공개 주소에서만 한다 |
| 목록 한 줄이 `[object Object]`로 보인다 | 점 표기를 쓰지 않았다. `li.textContent = items[i];`를 [3단계](walkthrough.md#3-목록-한-줄을-점-표기로-고치기)의 한 줄로 바꾼다. Console은 조용하다 |
| 이름 자리에 `undefined: 안녕하세요 (2026. 9. 16.)`처럼 보인다 | 이름표 철자가 다르다. `items.push`에 적은 `name`·`message`·`date`와 `items[i].name`을 나란히 놓고 비교한다 |
| `Uncaught ReferenceError: today is not defined` | `const today = new Date().toLocaleDateString();` 한 줄이 빠졌다. `items.push` **위**에 넣는다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` | `guestbook.html`에서 `<p id="empty">`를 지웠는데 `guestbook.js`에 `empty`가 남아 있다. [5단계](walkthrough.md#5-빈-목록-안내를-개수-자리로-옮기기)대로 `const empty = …` 줄과 `empty.textContent` 줄을 없앤다 |
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` | `#clear-button`을 못 찾았다. `guestbook.html`에 **[전체 지우기]** 버튼 줄을 먼저 넣는다 |
| `Uncaught TypeError: Cannot read properties of null (reading 'length')` | 복원 줄 끝의 `\|\| []`가 빠졌다. 저장 칸이 비어 있으면 `null`이 들어와 목록을 그리다 멈춘다 |
| `Uncaught SyntaxError: Unexpected token 'h', "hello" is not valid JSON` | 저장 칸에 JSON이 아닌 글자가 들어 있다. Application 탭에서 값을 손으로 고쳤을 때 난다. `guestbook` 키를 지우고 새로고침한다 |
| `Uncaught SyntaxError: "[object Object]" is not valid JSON` | `JSON.stringify` 없이 배열을 그대로 저장했다. `saveList()` 안을 고치고 Application 탭에서 `guestbook` 키를 한 번 지운 뒤 다시 남긴다 |
| 새로고침하면 목록이 사라진다 | 저장만 하고 읽어 오지 않았다. `let items = [];`가 그대로면 [10단계](walkthrough.md#10-페이지를-열-때-되살리기)의 복원 한 줄로 바꾼다 |
| Application 탭에 `guestbook` 키가 아예 없다 | `saveList();`를 부르는 곳이 없다. 제출 자리와 삭제 버튼 안 두 곳을 본다. 키 철자도 함께 확인한다 |
| 삭제했는데 새로고침하면 그 줄이 다시 나온다 | 삭제 버튼 틀 안의 `saveList();`가 빠졌다. `items.splice(i, 1);` 바로 아래에 넣는다 |
| **[전체 지우기]**를 누르면 목록은 비는데 새로고침하면 되살아난다 | `localStorage.removeItem('guestbook');`가 빠졌다. `items = [];`만으로는 저장 칸이 남는다 |
| 앞사람이 남긴 글이 이미 보인다 | 같은 아이디의 `github.io` 주소는 저장 칸을 함께 쓴다. **[전체 지우기]**를 누르고 본인 글만 남겨 캡처한다 |
| 날짜 모양이 옆 사람과 다르다 | 브라우저 언어 설정에 따라 다르다. 날짜가 보이면 통과다. 틀 안을 고치지 않는다 |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시와 `git log --oneline`을 본다 |
| `! [rejected]        main -> main (fetch first)` | GitHub 쪽에 내가 받지 않은 commit이 있다. `git pull` 뒤 다시 `git push`한다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://<아이디>.github.io/my-web/guestbook.html`에서 아래 순서로 만든 화면을 캡처한다.

1. 앞사람 글이 보이면 **[전체 지우기]**를 먼저 누른다.
2. 이름·메시지를 넣어 글 **세 개**를 남긴다.
3. **새로고침**한다. 세 줄과 `3개`가 그대로 남아 있어야 한다.
4. F12 **Application › Storage › Local Storage**에서 내 공개 주소를 고르고 `guestbook` 키를 누른다.
5. 목록과 Application 탭이 한 화면에 보이게 찍는다.

- 목록 한 줄에 이름·메시지·날짜가 함께 보인다.
- 주소창이 함께 보이게 찍는다. 화면이 좁아 한 장에 담기지 않으면 강의자 안내를 따른다.
- 시크릿 창이 아니라 일반 창에서 찍는다.

캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- **다크 모드를 기억하게 한다.** `app.js`의 다크 모드 버튼 안에서 `localStorage.setItem('dark', 'on')`을 하고, 파일 맨 끝에서 `if (localStorage.getItem('dark') === 'on') { document.body.classList.add('dark'); }`로 되살려 본다. 키 이름은 `guestbook`과 겹치지 않게 `dark`로 둔다. 채점에는 넣지 않는다.
- Application 탭에서 `guestbook` 값의 큰따옴표를 하나 지우고 새로고침해 본다. `is not valid JSON` 오류가 어떻게 생기는지 눈으로 본 뒤 그 키를 지운다.
- 이메일 칸도 객체에 넣어 본다. `email: emailInput.value.trim()`을 더하고 목록 한 줄에 `(${items[i].email})`을 붙여 본다. 이메일이 비었을 때 보기 좋은지 확인한다.
- Console에서 `items.push({ name: '직접', message: '넣은 줄', date: '오늘' })` 뒤 `saveList()`와 `showList()`를 차례로 불러 본다. 화면과 저장 칸이 함께 바뀌는 것을 볼 수 있다.
- 저장 칸에 든 글자 수를 세어 본다. `localStorage.getItem('guestbook').length`를 Console에 쳐 보고, 글을 하나 더 남긴 뒤 다시 쳐 본다.

추가 과제는 선택 사항이며 채점하지 않는다.
