# 10주차 실습 — 남긴 글을 목록으로 쌓고 지우기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data

7주차 방명록은 두 번째 글을 남기면 앞 글이 사라졌다. 이번 주에는 남긴 글을 배열에 쌓아 목록으로 그리고, 항목마다 **[삭제]** 버튼을 붙인다.
고치는 파일은 `guestbook.html`과 `guestbook.js` 둘뿐이다. 모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.
`student01`은 예시 아이디이므로 본인 아이디로 바꾼다. 이번 주에는 브랜치를 만들지 않고 `main`에서 바로 작업한다.

## 1일차 — 배열에 쌓아 목록으로 그리기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` |
| 5–25분 | `guestbook.html`에 목록 자리를 만들고, `let items = []`에 쌓아 `<li>`를 목록에 붙인다 |
| 25–40분 | 목록 아래에 `N개`를 표시한다 |
| 40–55분 | 이름을 비우고 눌러 안내만 나오는지 보고, Console에서 `items`를 확인한다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 확인·확인용 캡처 → 공용 PC면 자격 증명 삭제 |

### 1. 저장소 받아오기 (`git pull` · `git clone`)

지난 시간과 같은 PC면 `git pull`, 다른 PC에서 처음이면 `git clone`부터 한다. [따라하기 1단계](walkthrough.md#1-저장소-받아오기)를 본다.

- 시작 전 `git status`가 `On branch main`, `nothing to commit, working tree clean`이어야 한다.
- 9주차 `readme` 브랜치가 남아 있으면 `git switch main` 뒤 `git merge readme`부터 끝낸다.
- 파일이 없거나 이어 하기 어려우면 조교에게 9주차 `examples/day2` 폴더를 받아 그 폴더에서 시작한다.

### 2. 목록 자리 만들기 (`<ul id="list">` · `<p id="count">`)

`guestbook.html`에서 마지막 글 두 줄을 지우고 목록 자리 세 줄을 넣는다. [따라하기 2단계](walkthrough.md#2-목록-자리-만들기)를 본다.

- 지우는 것은 `<h3>마지막으로 남긴 글</h3>`과 `<p class="card" id="last">…</p>` 두 줄이다.
- 넣는 것은 `<h3>남긴 글</h3>`, `<ul class="card" id="list"></ul>`, `<p id="count">0개</p>` 세 줄이다.
- `<ul>` 안은 **비워 둔다.** 목록 줄은 JavaScript가 만들어 넣는다. 손으로 `<li>`를 적지 않는다.
- 이 단계까지 하고 **[남기기]**를 누르면 Console에 빨간 줄이 하나 뜬다. 3번에서 `guestbook.js`를 고치면 사라진다.

### 3. 배열에 쌓고 목록에 붙이기 (`push` · `createElement` · `append`)

`guestbook.js` 맨 위에서 `#last`를 찾던 줄을 지우고 `#list`·`#count`와 `let items = []`를 만든 뒤,
리스너 안의 `last.textContent = …` 한 줄을 다섯 줄로 바꾼다. [따라하기 3~5단계](walkthrough.md#3-배열과-목록-상자-찾아-두기)를 본다.

- `let items = [];`는 `let`으로 쓴다. 2일차 확장에서 통째로 바꾸기 때문이다.
- 같은 문장을 배열과 화면 두 곳에 넣으므로 `const text = \`${name}: ${message}\`;`로 한 번만 만든다.
- 화면에 붙이는 것은 **만들기 → 글자 넣기 → 붙이기** 세 줄이다. `list.append(li);`를 빠뜨리면 아무것도 보이지 않는다.
- 한 줄을 고칠 때마다 새로고침해 Console을 본다. 세 번 남겨 세 줄이 쌓이면 다음으로 간다.

### 4. 항목 수 보여 주기 (`length`)

`list.append(li);` 아래에 항목 수 한 줄을 더한다. [따라하기 6단계](walkthrough.md#6-항목-수-보여-주기)를 본다.

- 화면의 줄을 세지 않는다. `count.textContent = \`${items.length}개\`;`처럼 **배열의 개수**를 그대로 쓴다.
- 백틱(`` ` ``)과 `${ }`는 5주차 템플릿 문자열이다. 작은따옴표로 쓰면 글자 그대로 `${items.length}개`가 보인다.
- 세 번 남기면 `3개`가 되어야 한다. `undefined개`가 보이면 `length` 철자를 본다.

### 5. 빈값 확인과 Console에서 `items` 보기

이름을 비우고 눌러 7주차 안내가 그대로 동작하는지 보고, Console에서 배열을 직접 확인한다.
[따라하기 7단계](walkthrough.md#7-빈-이름으로-눌러-보기)를 본다.

- 이름을 비우면 `이름을 입력하세요.`, 메시지를 비우면 `메시지를 입력하세요.`가 보이고 목록과 숫자는 그대로여야 한다.
- 이름 칸에 **공백만** 넣고 눌러도 안내가 떠야 한다. 뜨지 않으면 `.trim()`이 빠진 것이다.
- Console에 `items`를 치면 지금까지 쌓인 값이 배열로 보인다. `items.length`와 화면의 숫자가 같은지 대조한다.
- `items[0]`은 첫 번째 값이다. 번호는 **0부터** 센다.

### 6. 오늘 확인할 것

- [ ] **[남기기]**를 누를 때마다 목록에 한 줄씩 쌓이고 앞 글이 사라지지 않는다.
- [ ] 목록 아래 숫자가 `1개`·`2개`·`3개`로 오른다.
- [ ] 이름이나 메시지를 비우고 누르면 안내만 나오고 목록·숫자가 그대로다.
- [ ] Console에 `items`를 치면 화면의 줄과 같은 값이 배열로 보인다.
- [ ] F12 Console에 빨간 줄이 없다.
- [ ] push한 뒤 공개 주소에서 같은 동작이 되는 것을 확인용으로 한 장 찍어 두었다.

제출 캡처는 2일차 마지막에 한 번만 찍는다.

## 2일차 — 다시 그리기와 삭제 버튼 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` |
| 5–25분 | 목록을 그리는 일을 `showList()` 함수로 옮기고 submit 안을 두 줄로 줄인다 |
| 25–45분 | 삭제 버튼 틀을 붙여 가운데 항목을 지워 본다 |
| 45–55분 | 항목 수가 함께 줄어드는지 보고, 목록이 비면 안내 문장이 나오게 한다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 새로고침 → **캡처 1장** → 공용 PC면 자격 증명 삭제 |

### 1. `showList()`로 교체하기 (`innerHTML = ''` · `for`)

목록을 비우고 배열 전체를 다시 그리는 함수를 만들고, submit 안을 두 줄로 줄인다.
[따라하기 9~10단계](walkthrough.md#9-다시-그리는-함수-showlist-만들기)를 본다.

- 함수 이름은 `showList`로 통일한다. 첫 줄은 `list.innerHTML = '';`이며 이 수업에서 `innerHTML`은 **비우기에만** 쓴다.
- `for (let i = 0; i < items.length; i++)`로 훑는다. `<=`로 쓰면 없는 번호까지 가서 빈 줄이 하나 더 그려진다.
- 안의 세 줄은 어제 쓴 것과 같고 글자만 `items[i]`에서 가져온다.
- 함수를 만든 직후에는 화면이 그대로다. 부르는 곳이 없기 때문이다. submit 안을 `items.push(…)` + `showList()` 두 줄로 바꾸면 어제와 똑같이 동작한다.

### 2. 삭제 버튼 붙이기 (`createElement('button')` · `splice`)

`li.textContent` 줄과 `list.append(li)` 줄 **사이**에 삭제 버튼 틀 일곱 줄을 그대로 옮겨 쓴다.
[따라하기 11단계](walkthrough.md#11-삭제-버튼-붙이기)를 본다.

- 이 일곱 줄은 **틀**이다. 안을 뜯어보지 않고 그대로 쓴다. `showList()`가 다시 그릴 때 버튼마다 번호를 새로 붙인다.
- 버튼 안에서 하는 일은 두 가지다. `items.splice(i, 1);`로 배열에서 하나 빼고, `showList();`로 다시 그린다.
- `showList();`를 빠뜨리면 눌러도 화면이 그대로다. 오류는 나지 않으니 Console이 아니라 순서를 읽는다.
- `li.append(removeButton)`은 버튼을 그 줄 안에, `list.append(li)`는 그 줄을 목록에 붙인다. 상자가 다르다.
- 글 세 개를 남기고 **가운데** 줄을 지워 본다. 위아래 두 줄이 남고 번호가 밀리지 않으면 된 것이다.

### 3. 항목 수 갱신과 빈 목록 안내 (`items.length === 0`)

항목 수가 함께 줄어드는지 보고, 목록이 비었을 때 보여 줄 문장을 넣는다.
[따라하기 12~13단계](walkthrough.md#12-빈-목록-안내-넣기)를 본다.

- 항목 수 줄은 함수 안 `for` **밖**에 둔다. 안에 두면 한 줄 그릴 때마다 다시 쓴다.
- `guestbook.html`에 `<p id="empty">아직 남긴 글이 없습니다.</p>` 한 줄을 넣고, `guestbook.js` 위쪽에서 `#empty`를 찾아 둔다.
- 함수 끝에 `if (items.length === 0) { … } else { … }`로 문장을 넣거나 지운다. `===`는 5주차에 배운 비교다.
- 파일 **맨 끝**에 `showList();` 한 줄을 더해 페이지를 열 때 한 번 그린다.
- 항목을 모두 지웠을 때 `0개`와 안내 문장이 함께 보이면 완성이다.

### 4. 오늘 확인할 것

- [ ] 글을 남기면 목록에 쌓이고 줄마다 **[삭제]** 버튼이 보인다.
- [ ] 가운데 줄의 **[삭제]**를 누르면 그 줄만 사라지고 숫자가 하나 줄어든다.
- [ ] 항목을 모두 지우면 `아직 남긴 글이 없습니다.`와 `0개`가 보인다.
- [ ] 페이지를 새로 열었을 때도 같은 화면이다.
- [ ] F12 Console에 빨간 줄이 없다.
- [ ] 공개 주소에서 글 3개 → 가운데 삭제 → `2개` 화면을 캡처 1장으로 저장했다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 다시 확인해도 된다. `git status`에 `Your branch is ahead of 'origin/main' by 1 commit.`이 있으면 push를 안 한 것이다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'innerHTML')` | `<ul>`을 못 찾았다. `guestbook.html`에 `id="list"`가 있는지 보고, `guestbook.js`의 `document.querySelector('#list')` 철자를 비교한다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` | 아직 `guestbook.js`가 지워진 `#last`를 쓰고 있다. `const last = …` 줄과 `last.textContent = …` 줄을 [따라하기 3~4단계](walkthrough.md#3-배열과-목록-상자-찾아-두기)대로 바꾼다 |
| `Uncaught TypeError: document.creatElement is not a function` | `createElement` 철자가 틀렸다. 오류 줄 끝의 `guestbook.js:17`로 줄을 먼저 찾는다 |
| `Uncaught TypeError: Assignment to constant variable.` | `for (const i = 0; …)`로 썼다. `i`가 하나씩 올라가야 하므로 `for (let i = 0; …)`이다 |
| 항목 수가 `undefined개`로 보인다 | `items.lenght`처럼 `length` 철자가 틀렸다. 오류는 나지 않으니 화면 글자로 찾는다 |
| 눌러도 목록에 아무것도 안 보이고 Console도 조용하다 | 배열에는 들어갔는데 화면에 붙이지 않았다. 1일차면 `list.append(li);`(숫자만 `3개`로 오르고 목록은 비어 있다), 2일차면 submit 안의 `showList();`(숫자도 `0개` 그대로다)가 있는지 본다. Console에 `items`를 쳐 값이 쌓였는지 먼저 확인한다 |
| 화면에는 쌓이는데 숫자가 `0개` 그대로다 | `items.push(text);`가 빠졌다. 화면만 만들고 배열에 넣지 않은 것이다 |
| **[삭제]**를 눌러도 화면과 숫자가 그대로다 | `items.splice(i, 1);` 뒤의 `showList();`가 빠졌다. 배열만 줄고 화면은 그대로인 상태다. Console에 `items`를 쳐 두 값이 다른 것을 확인한다 |
| 지울 때마다 목록이 늘어난다 (줄은 8개인데 `2개`) | `list.innerHTML = '';`가 빠졌다. 다시 그리기 전에 비우지 않으면 앞의 줄이 남는다 |
| 목록 맨 끝에 빈 줄이 하나 더 그려진다 | `for`의 조건을 `i <= items.length`로 썼다. 마지막 번호는 `items.length - 1`이다 |
| 빈 이름으로 눌렀는데 `: 안녕하세요`가 쌓인다 | 7주차 `if (name === '') { … return; }`의 `return`이 빠졌다 |
| 새로고침하면 목록이 사라진다 | 정상이다. 오늘 목록은 화면에만 있다. 새로고침해도 남게 하는 것은 11주차다 |
| 다른 PC에서 열었더니 목록이 비어 있다 | 정상이다. 목록은 저장되지 않는다. 캡처는 글을 남긴 **그 화면**에서 바로 찍는다 |
| `! [rejected]        main -> main (fetch first)` / `hint: Updates were rejected because the remote contains work that you do not` | GitHub 쪽에 내가 받지 않은 commit이 있다. `git pull` 뒤 다시 `git push`한다 |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시와 `git log --oneline`을 본다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://<아이디>.github.io/my-web/guestbook.html`을 열고 글 **세 개**를 남긴 뒤 **가운데** 줄의 **[삭제]**를 누른 화면을 캡처한다.

- 목록에 두 줄이 남아 있고 각 줄에 **[삭제]** 버튼이 보인다.
- 목록 아래 숫자가 `2개`다.
- 주소창이 함께 보이게 찍는다.

캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- **전체 지우기** 버튼을 만들어 본다. `guestbook.html`에 `<button id="clear-button" type="button">전체 지우기</button>` 한 줄을 넣고, `guestbook.js`에서 찾아 둔 뒤 클릭 리스너 안에서 `items = [];`와 `showList();` 두 줄을 쓴다. 배열을 통째로 바꾸기 때문에 `items`를 `let`으로 선언한 것이다. 채점에는 넣지 않는다.
- 목록이 몇 자인지 함께 보여 준다. `` `${items.length}개` `` 대신 `` `${items.length}개 · 마지막 ${items[items.length - 1]}` ``처럼 써 보고, 목록이 비었을 때 어떻게 되는지 본다.
- `styles.css`에 `.card button { margin-left: 8px; }` 한 줄을 더해 버튼과 글자 사이를 띄워 본다.
- 이메일 칸도 함께 쌓아 본다. `` `${name}(${email}): ${message}` `` 형태로 바꾸면 한 줄에 세 값이 들어간다. 이메일이 비었을 때 보기 좋은지 확인한다.
- Console에서 `items.push('직접 넣은 줄')`을 친 뒤 `showList()`를 불러 본다. 화면이 배열을 그대로 비춘다는 것을 눈으로 확인할 수 있다.

추가 과제는 선택 사항이며 채점하지 않는다.
