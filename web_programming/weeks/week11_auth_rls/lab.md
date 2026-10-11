[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls)

# 11주차 실습 — 값을 바꿔 보고 마지막에 조립하기

**11주부터 확인·캡처는 공개 URL에서만 한다**(로컬과 공개 주소는 저장소가 다르다).
내 PC 에서 연 화면(두 번 눌러 연 `file://`, 서버로 연 `http://localhost:8000/`)에 남긴 글은 공개 주소 `https://student01.github.io/…` 에 나타나지 않는다. 값 바꿔 보기와 조립 중 미리 보기는 내 PC 에서 하고, 완료 확인과 제출 캡처는 공개 주소에서 만든다.

이번 주 실습도 코드를 새로 쓰는 것이 아니라 **값을 바꿔 보는 것**이다.
비교 예제 7개를 이번 주 새 저장소 `web-week11` 의 `ex/` 폴더에 저장하고(날마다 고르기 페이지 `index.html` 하나와 `.js` 여러 개. 1일차는 `.js` 세 개, 2일차는 네 개), 값이나 줄 하나를 바꾼 뒤 결과가 어떻게 달라지는지 본다.
결과는 화면, **F12 › Console**, 그리고 2일차에 처음 쓰는 **F12 › Application** 에서 본다. DevTools 는 실습 내내 열어 둔다.
2일차 끝에 그 부품으로 `web-week11` 맨 위의 `guestbook.html`·`guestbook.js` 를 조립한다. 두 파일은 지난주 완성본에서 가져온다. 채점 대상은 2일차 캡처 1장이다.
`student01` 은 예시 아이디이므로 본인 아이디로 바꾼다.

파일을 받는 법, 고르기 페이지 쓰는 법, Application 탭 여는 법은 [따라하기](walkthrough.md)에 있다.
"바꿔 보기"는 **무엇이 달라질지 먼저 말해 보고** 저장 → 새로고침으로 확인한다. 확인했으면 원래대로 되돌리고 다음으로 간다.

## 1일차 — 객체와 점 표기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 새 폴더 `web-week11` 을 만들어 VS Code 로 연다(**File › Open Folder**). 지난주 완성본을 넣는다: 내 `web-week10` 저장소 GitHub 화면 › **Code › Download ZIP** → 압축을 풀어 맨 위 파일과 `images/`·`screenshots/` 를 넣는다. 못 받으면 교재 [10주차 `examples/day2/web-week10/`](../week10_supabase_data/examples/day2/web-week10/) 파일을 **Raw** 로 받는다. `ex` 폴더를 만들고 교재 [`examples/day1/`](examples/day1/) 의 네 파일(고르기 페이지 `index.html` 과 ex01~ex03 의 `.js`)을 **Raw** 로 저장한다 |
| 5–20분 | ex01 객체와 점 표기 |
| 20–33분 | ex02 배열 안의 객체와 날짜 |
| 33–47분 | ex03 객체를 목록 한 줄로 |
| 47–50분 | 확인: 네 파일이 `ex/` 에 있고, 각 예제에서 값 하나 이상을 바꿨는지. 일부러 낸 오류는 되돌려 두었는지 |
| 50–60분 | 이번 주 저장소 만들어 올리기: GitHub 에 새 저장소 `web-week11` → [올리기 명령](#이번-주-저장소-만들어-올리기) → **Settings › Pages** → 공개 주소 `https://student01.github.io/web-week11/ex/` 확인 → 공용 PC면 자격 증명 삭제 |

1일차 예제는 모두 `ex/index.html` 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 세 줄 중 **지금 문항의 줄 하나만** 주석 밖에 둔다(줄에서 **Ctrl+/**, macOS **⌘+/**). 코드는 각 `.js` 파일에서 고치고, 저장 → `ex/index.html` 새로고침으로 본다.
Console 에 객체·배열이 찍힌 줄은 그 값(`{…}`·`[…]`) 바로 앞의 ▶ 를 눌러 펼칠 수 있다.

### 1. ex01 객체와 점 표기 (`{ 이름표: 값 }` · `item.name`)

[examples/day1/ex01_object.js](examples/day1/ex01_object.js) 를 `ex/ex01_object.js` 로 저장한다. `ex/index.html` 맨 아래에서 `ex01_object.js` 줄만 켠다(처음 받은 상태가 이렇다).

- 바꿔 보기: Console 1번 줄 `{name: …}` 앞의 ▶ 를 눌러 펼친다. 이름표 몇 개와 값이 보이나? `[[Prototype]]` 줄이 보이면 그것은 내가 적은 이름표가 아니다. 2·3번은 그중 어느 값인가? 4번은 왜 `undefined` 인가?
- 바꿔 보기: 4행 객체에서 `'하늘'` 뒤의 쉼표를 지운다. Console 에 무엇이 뜨나? 1~5번 중 찍히는 줄이 있나? 확인했으면 되돌린다.
- 바꿔 보기: 14행 `name: name` 의 오른쪽 `name` 에 따옴표를 붙여 `name: 'name'` 으로 바꾼다. 5번은 무엇인가? 따옴표가 없을 때 오른쪽 `name` 은 무엇이었나? 확인했으면 되돌린다.
- 흔한 실수: 이름표 철자를 틀린다(4번 `item.nmae`). 빨간 줄 없이 `undefined` 가 나온다. Console 이 조용하니 찍힌 값을 읽어서 찾는다.

### 2. ex02 배열 안의 객체와 날짜 (`items[0].name` · `toLocaleDateString()`)

[examples/day1/ex02_array_objects.js](examples/day1/ex02_array_objects.js) 를 `ex/ex02_array_objects.js` 로 저장한다. `ex/index.html` 맨 아래에서 ex01 줄을 끄고 `ex02_array_objects.js` 줄만 켠다.

- 바꿔 보기: Console 1번과 3번 줄을 펼쳐 비교한다. 1번 한 칸에는 무엇이, 3번 한 칸에는 무엇이 들었나? 2번 글자에서 이름 `하늘` 만 따로 꺼낼 수 있나? 4번은?
- 바꿔 보기: 17행 쉼표 뒤(따옴표 밖)의 `items[0].name` 을 `items[1].name` 으로 바꾼다. 4번은? 되돌린 뒤 `items[0].name` 을 `items.name[0]` 으로(대괄호와 점의 순서를 바꿔) 바꾼다. 빨간 줄과 `파일:줄` 은? 5번은 찍히나? 확인했으면 되돌린다.
- 바꿔 보기: 12행 끝의 `.toLocaleDateString()` 을 지워 `new Date();` 만 남긴다. 5번은 어떤 모양인가? 목록 한 줄에 넣기 좋은 쪽은? 확인했으면 되돌린다.
- 흔한 실수: 배열 `[ ]` 과 객체 `{ }` 를 헷갈린다. 여러 개를 순서대로 담으면 `[ ]`, 이름표를 붙여 한 묶음으로 담으면 `{ }` 다. 꺼낼 때는 대괄호(몇 번째)가 먼저, 점(무슨 값)이 다음이다.

### 3. ex03 객체를 목록 한 줄로 (`[object Object]` · 점 표기 템플릿)

[examples/day1/ex03_list_line.js](examples/day1/ex03_list_line.js) 를 `ex/ex03_list_line.js` 로 저장한다. `ex/index.html` 에서 `ex03_list_line.js` 줄만 켠다.

- 바꿔 보기: 화면의 1번 목록과 2번 목록을 읽는다. 1번 줄의 글자는 무엇인가? Console 에 빨간 줄이 있나?
- 바꿔 보기: 16행 `items[i].name` 을 `items[i].nmae` 로 바꾼다. 2번 목록은? 빨간 줄은? 확인했으면 되돌린다.
- 바꿔 보기: 16행의 백틱(`` ` ``) 두 개를 작은따옴표(`'`)로 바꾼다. 2번 목록은 어떻게 보이나? 5주차 ex05 의 몇 번과 같은가? 확인했으면 되돌린다.
- 바꿔 보기: 12행 `items[i]` 를 `items[i].message` 로 바꾼다. 1번 목록은? 확인했으면 되돌린다.
- 흔한 실수: `li.textContent = items[i];` 를 그대로 둔다. 화면에 `[object Object]` 가 보이고 Console 은 조용하다. 점 표기로 값을 하나씩 꺼내 넣는다.

### 이번 주 저장소 만들어 올리기

GitHub 에서 **New repository** → 이름 `web-week11`, **Public**, README 는 추가하지 않는다. VS Code 터미널(현재 폴더 `web-week11`)에서 2주차에 배운 순서 그대로 친다.

```bash
git init
git add .
git commit -m "11주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week11.git
git push -u origin main
```

저장소 **Settings › Pages › Branch: main, /(root) › Save** → 1~3분 뒤 `https://student01.github.io/web-week11/ex/` 를 연다. `ex/index.html` 의 화면(제목과 "ex03 이 쓰는 자리")이 보이면 된 것이다. 공용 PC면 자격 증명을 지우고 나간다.
오늘 올린 것은 확인용이다. 제출은 2일차에 캡처 한 장만 한다.

## 2일차 — 저장 칸에 남기고 되살리기, 그리고 조립 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC에 `web-week11` 폴더가 남아 있으면 그대로 연다. 없으면 `git clone https://github.com/student01/web-week11.git` 뒤 **File › Open Folder**. 교재 [`examples/day2/`](examples/day2/) 의 다섯 파일(고르기 페이지 `index.html` 과 ex04~ex07 의 `.js`)을 **Raw** 로 `ex/` 에 저장한다. `index.html` 은 1일차 고르기 페이지를 덮어쓴다(바꿀지 물으면 바꾼다). 5분 안에 다 못 받으면 `index.html` 과 ex04 부터 시작하고 나머지는 그 문항을 시작할 때 받는다 |
| 5–11분 | ex04 저장 칸 localStorage |
| 11–17분 | ex05 JSON |
| 17–23분 | ex06 `\|\|` 또는 |
| 23–29분 | ex07 removeItem |
| 29–48분 | 조립: `guestbook.html` 두 곳, `guestbook.js` 를 조립표 순서로 고친다. 내 PC 에서 미리 보며 고친다 |
| 48–55분 | 올리고 확인: `git add .` → `git commit -m "11주차 2일차"` → `git push` → 1~3분 뒤 공개 주소 `https://student01.github.io/web-week11/guestbook.html` 에서 글 남기기·새로고침·375·1280 폭 확인 |
| 55–60분 | 끝 루틴: 공개 주소에서 **캡처 1장**(전체 지우기 → 글 세 개 → 새로고침 → Application 탭) → 고친 것이 있으면 `git add .` → `git commit -m "11주차 2일차"` → `git push` → 공용 PC면 **[전체 지우기]** 를 누르고 자격 증명 삭제 |

2일차 예제도 `ex/index.html` 하나로 연다. 오늘 받은 `index.html` 이 1일차 고르기 페이지를 덮어쓴다. 1일차 `.js` 세 개는 그대로 남으므로 코드는 VS Code 에서 계속 열어 볼 수 있다.
그 파일 맨 아래 `<script src="exNN_….js">` 네 줄 중 **지금 문항의 줄 하나만** 주석 밖에 둔다(줄에서 **Ctrl+/**, macOS **⌘+/**). 코드는 각 `.js` 파일에서 고치고, 저장 → `ex/index.html` 새로고침으로 본다. ex04 의 **저장하기** 버튼은 `index.html` 의 "ex04 가 쓰는 자리"에 있다. 다른 줄을 켜 두었을 때는 눌러도 아무 일이 없다.
오늘은 **F12 › Application** 탭을 연다. 왼쪽 **Local Storage** 아래의 주소 한 줄을 누르면 오른쪽 표에 Key(키)와 Value(값)가 보인다. 예제의 키는 `ex04-memo` 처럼 예제 번호로 시작한다. 완성본의 `guestbook` 키와 섞이지 않게 하려는 것이다.
파일마다 **바꿔 보기를 하나 이상** 하고 넘어간다. 29분이 되면 남은 것은 두고 조립을 시작한다. 남은 바꿔 보기는 캡처까지 끝낸 뒤 한다.

### 4. ex04 저장 칸 localStorage (`setItem` · `getItem` · Application 탭)

[examples/day2/ex04_storage.js](examples/day2/ex04_storage.js) 를 `ex/ex04_storage.js` 로 저장한다. `ex/index.html` 맨 아래에서 `ex04_storage.js` 줄만 켠다(처음 받은 상태가 이렇다). Application 탭 여는 법은 [따라하기 6단계](walkthrough.md#6-폴더-열고-2일차-예제-다섯-파일-가져오기)에 있다.

- 바꿔 보기: **저장하기**를 누르기 전에 새로고침한다. Console 1·2번은? 이제 **저장하기**를 누르고 새로고침한다. 1번과 2번 중 어느 쪽이 남았나? Application › Local Storage 표에 무엇이 생겼나?
- 바꿔 보기: 표에 `ex04-memo` 가 있는 상태에서 8행 `getItem` 의 키를 `'ex04-Memo'`(대문자 M)로 바꾸고 새로고침한다. 2번은? Application 표의 키는 무엇인가? 확인했으면 되돌린다.
- 바꿔 보기: Application 표에서 `ex04-memo` 줄을 오른쪽 클릭 › **Delete** 로 지우고 새로고침한다. 2번은?
- 바꿔 보기: 12행 값 자리의 `'안녕하세요'` 를 `['하늘', '바다']` 로 바꾸고 **저장하기** → 새로고침한다. 2번은 어떤 글자인가? 저장 칸에는 무엇만 들어가나? 확인했으면 되돌린다.
- 흔한 실수: 적을 때(`setItem`)와 꺼낼 때(`getItem`)의 키 철자가 다르다. 빨간 줄 없이 `null` 이 나온다.

### 5. ex05 JSON (`JSON.stringify` · `JSON.parse`)

[examples/day2/ex05_json.js](examples/day2/ex05_json.js) 를 `ex/ex05_json.js` 로 저장한다. `ex/index.html` 맨 아래에서 ex04 줄을 끄고 `ex05_json.js` 줄만 켠다.

- 바꿔 보기: Application 표에서 `ex05-raw` 와 `ex05-json` 의 값을 비교한다. 이름 `하늘` 이 남은 쪽은? 2번 글자에서 이름표를 감싼 것은 큰따옴표인가 작은따옴표인가?
- 바꿔 보기: 22행 맨 앞의 `// ` 를 지워 주석을 푼다. 빨간 줄은 무엇이라고 하나? 오른쪽 `파일:줄` 은 `ex05_json.js` 의 22행을 가리키나? 1~3번은 찍히나? 확인했으면 되돌린다.
- 바꿔 보기: 13행 `const text = JSON.stringify(items);` 를 잘라 6행(둘째 `items.push`) **위**에 붙인다. 2번 글자에 이름이 몇 개인가? 3번 개수는? 확인했으면 되돌린다.
- 흔한 실수: `setItem` 할 때 `JSON.stringify` 를 빠뜨린다. 저장 칸에 `[object Object]` 같은 글자가 적히고, 다음에 열 때 `JSON.parse` 에서 빨간 줄이 뜬다.

### 6. ex06 `||` 또는 (if 안 · 값 자리)

[examples/day2/ex06_or.js](examples/day2/ex06_or.js) 를 `ex/ex06_or.js` 로 저장한다. `ex/index.html` 에서 `ex06_or.js` 줄만 켠다.

- 바꿔 보기: 5행 `const message = '';` 를 `const message = '잘 봤습니다';` 로 바꾼다. 1번은? 이어서 4행 `'하늘'` 을 `''` 로 바꾼다. 1번은? 확인했으면 되돌린다.
- 바꿔 보기: 23행 맨 앞의 `// ` 를 지운다. 빨간 줄은? 2번에서 본 `saved` 는 무엇이었나? 확인했으면 되돌린다.
- 바꿔 보기: Application 표의 빈 줄을 두 번 눌러 키 `ex06-none`, 값 `["하늘"]` 을 만든 뒤 새로고침한다. 2번과 3번은? `||` 뒤의 `[]` 가 쓰였나? 확인했으면 그 키를 지운다.
- 흔한 실수: 되살리는 줄 끝의 `|| []` 를 빠뜨린다. 저장 칸에 값이 있는 내 PC 에서는 멀쩡하고, 저장 칸이 빈 사람(처음 여는 사람)에게만 빨간 줄이 뜬다.

### 7. ex07 removeItem (`localStorage.removeItem` · `items = []`)

[examples/day2/ex07_remove.js](examples/day2/ex07_remove.js) 를 `ex/ex07_remove.js` 로 저장한다. `ex/index.html` 에서 `ex07_remove.js` 줄만 켠다.

- 바꿔 보기: 1번과 2번 줄의 "저장 칸" 값을 비교한다. 배열을 비운 1번 뒤에도 저장 칸에 무엇이 남았나? Application 표에는 어느 키가 남았나?
- 바꿔 보기: 13행 `localStorage.removeItem('ex07-list');` 앞에 `//` 를 붙인다. 2번은? 전체 지우기에서 이 줄을 빠뜨리면 새로고침할 때 어떻게 되겠나? 확인했으면 되돌린다.
- 바꿔 보기: 13행의 키를 `'ex07-other'` 로 바꾼다. 2번과 3번은? 확인했으면 되돌린다.
- 흔한 실수: 전체 지우기에서 `items = [];` 만 쓴다. 화면은 비지만 저장 칸은 그대로여서 새로고침하면 목록이 되살아난다.

### 8. 조립 — `guestbook.html` 두 곳, `guestbook.js` (`saveList` · `JSON.parse` · `removeItem`)

이제 `ex/` 가 아니라 `web-week11` 맨 위의 `guestbook.html`·`guestbook.js` 를 연다. 전문과 단계는 [따라하기 2일차](walkthrough.md#2일차)에 있다.

- `guestbook.html`: `<div id="empty">…</div>` 줄을 지우고, `<div id="count">` 의 처음 글자를 `아직 남긴 글이 없습니다.` 로 바꾸고, 그 아래에 **[전체 지우기]** 버튼 줄을 넣는다.
- `guestbook.js`: 지난주 파일을 고쳐 쓴다. 지울 줄은 `const empty …` 한 줄, `function clearNotice() { … }` 세 줄, 맨 아래 `input` 리스너 두 줄, 두 번째 `if (message === '') { … }` 덩어리, `clearNotice();` 한 줄이다. 넣고 바꿀 줄은 아래 조립표 순서대로다.

| 조립할 줄 | 어느 ex 에서 본 것 |
|---|---|
| `guestbook.html` 의 `<div id="count">아직 남긴 글이 없습니다.</div>`(`#empty` 줄은 지운다)와 `showList()` 끝의 `if (items.length === 0) { … } else { … }` — 안내 문장과 개수를 모두 `count` 에 쓴다 | 10주 완성본의 빈 목록 문장과 `if / else` 그대로. 쓰는 자리만 `empty` → `count` |
| `if (name === '' \|\| message === '') { notice.textContent = '이름과 메시지를 모두 입력하세요.'; … }` | ex06 1번 |
| `notice.textContent = '';` | 10주 완성본 `clearNotice()` 안의 줄 |
| `const today = new Date().toLocaleDateString();` | ex02 (날짜 틀) |
| `items.push({ name: name, message: message, date: today });` | ex01 5번 (값 자리에 변수) · ex02 3번 (배열에 객체 쌓기) |
| `` li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`; `` | ex03 2번 |
| `function saveList() { localStorage.setItem('guestbook', JSON.stringify(items)); }` | ex05 2번 (+ ex04 `setItem`) |
| `items.push(…)` 바로 아래와 삭제 버튼 틀 안 `items.splice(i, 1);` 바로 아래의 `saveList();` | ex05 셋째 바꿔 보기(저장은 배열이 바뀐 뒤에) |
| `let items = JSON.parse(localStorage.getItem('guestbook')) \|\| [];` | ex06 3번 (+ ex04 `getItem`, ex05 `JSON.parse`) |
| `guestbook.html` 의 `<div><button id="clear-button" type="button">전체 지우기</button></div>` 와 `const clearButton = document.querySelector('#clear-button');` | ex04 (고르기 페이지 `index.html` 의 버튼 줄 `<div><button id="save-button">`, 찾아 두기 `const saveButton = …`). `type="button"` 은 10주 완성본 `index.html` 의 버튼과 같다 |
| `clearButton.addEventListener('click', function () { items = []; localStorage.removeItem('guestbook'); showList(); });` | ex04 (버튼 클릭 등록) + ex07 1·2번 + 10주 완성본 `showList()` |

- 확인(미리 보기): 저장하고 내 PC 에서 `guestbook.html` 을 연다(두 번 눌러 열기, 또는 `node server.mjs` → `http://localhost:8000/guestbook.html`). 앞 단계에서 남긴 글이 보이면 **[전체 지우기]** 를 먼저 누른다. 글을 하나 남기면 `하늘: 안녕하세요 (…)` 한 줄과 `1개` 가 보이고, 새로고침해도 그대로면 된 것이다. 이 화면의 저장 칸은 내 PC 의 것이다. 완료 확인은 9번에서 공개 주소로 한다.
- 바꿔 보기: **[전체 지우기]** 를 누르고 새로고침한다. 목록과 Application 표의 `guestbook` 키는 어떻게 되나?
- 흔한 실수: `guestbook.html` 에 버튼 줄을 넣지 않고 `guestbook.js` 만 고친다. `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` 가 뜨고, 그 줄 아래 맨 끝 `showList();` 가 실행되지 않아 열 때 목록이 그려지지 않는다. **HTML 을 먼저 고친다.**

### 9. 공개 주소에서 확인 (375·1280 폭)

- 48분이 되면 `git add .` → `git commit -m "11주차 2일차"` → `git push` 한다. 1~3분 뒤 `https://student01.github.io/web-week11/guestbook.html` 을 연다.
- 글을 두 개 남기고 새로고침한다. 두 줄과 `2개` 가 그대로이고, Application › Local Storage › `https://student01.github.io` 에 `guestbook` 키가 있으면 된 것이다.
- DevTools 의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)로 폭 375 와 1280 에서 본다. 375 에서는 메뉴가 세로로 선다(4주차 `@media`).
- 내 PC 에서 남긴 글은 여기 없다. 저장 칸이 주소마다 따로이기 때문이다. 고장이 아니다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다 |
| push 가 거부되거나 로그인 창이 안 뜬다 | [2주차 막혔을 때](../week02_github_pages/lab.md#막혔을-때) 표를 본다 |
| 내 PC 에서는 목록이 남는데 공개 주소에서는 비어 있다 | 고장이 아니다. 저장 칸은 주소마다 따로 있다. 이번 주 확인과 캡처는 공개 주소에서만 한다 |
| 화면이 생각과 다른데 이유를 모르겠다 | **Console 을 먼저 연다.** 빨간 줄 오른쪽 `파일:줄` 로 간다. 오류 난 줄 아래는 실행되지 않으므로 그 줄부터 본다. 빨간 줄이 없으면 화면(목록)·배열(Console 에 `items`)·저장 칸(Application 표) 세 곳을 나란히 본다 |
| 예제를 열었는데 Console 에 아무것도 없다 | `ex/index.html` 맨 아래에서 그 문항의 `script` 줄을 켰는지(주석 밖인지), `.js` 파일이 같은 `ex/` 폴더에 있는지 본다. `Failed to load resource` 줄이 `.js` 파일 이름과 함께 보이면 그 파일 이름 철자가 틀린 것이다(`favicon.ico` 와 함께 보이는 줄은 바로 아래 줄을 본다). 2일차에 1일차 줄이 보이면 2일차 `index.html` 을 아직 받지 않은 것이다 |
| Console 에 `Failed to load resource: the server responded with a status of 404 (Not Found)` 빨간 줄이 `favicon.ico` 와 함께 보인다 | 서버(`node server.mjs`)로 열면 브라우저가 탭 아이콘 `favicon.ico` 를 찾는데, 폴더에 그 파일이 없어서 생긴 줄이다. 내 코드의 오류가 아니다(공개 주소에서도 보일 수 있다). `Uncaught` 로 시작하는 빨간 줄만 본다 |
| `ex/` 예제에서 `Uncaught SyntaxError: Identifier 'items' has already been declared` | 고르기 페이지에서 `script` 줄을 둘 켰다. 한 줄만 켠다 |
| 목록 한 줄이 `[object Object]` 로 보인다 | `li.textContent = items[i];` 를 그대로 두었다. 점 표기로 값을 꺼내 넣는다(ex03 2번). Console 은 조용하다 |
| 목록이 `undefined: 안녕하세요 (…)` 처럼 보인다 | 이름표 철자가 다르다. `items.push({ … })` 에 적은 `name`·`message`·`date` 와 `items[i].name` 을 나란히 놓고 비교한다(ex01 4번) |
| `Uncaught ReferenceError: today is not defined` | `const today = new Date().toLocaleDateString();` 줄이 빠졌다. `items.push` 바로 **위**에 넣는다 |
| `Uncaught ReferenceError: Cannot access 'today' before initialization` | `const today …` 줄이 `items.push` 보다 **아래**에 있다. 만들기 전에 썼다는 뜻이다. `items.push` 위로 옮긴다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` | `guestbook.html` 에서 `<div id="empty">` 를 지웠는데 `guestbook.js` 에 `empty` 가 남아 있다. `const empty …` 줄을 지우고, `showList()` 끝의 여섯 줄(`count.textContent = …` 한 줄과 `if / else`)을 [따라하기 8단계](walkthrough.md#8-빈-목록-안내를-개수-자리로)의 다섯 줄로 바꾼다(목록이 비면 안내 문장, 아니면 개수를 `count` 에 쓴다). `empty` 줄만 지우면 빈 목록에서도 `0개` 가 남는다. 찾기(Ctrl+F)로 `empty` 가 한 군데도 없는지 본다 |
| `Uncaught ReferenceError: clearNotice is not defined` | `function clearNotice() { … }` 를 지웠는데 그 이름을 쓰는 줄이 남았다. 맨 아래 `input` 리스너 두 줄은 지우고, submit 안의 `clearNotice();` 는 `notice.textContent = '';` 로 바꾼다([따라하기 9단계](walkthrough.md#9-안내-문구를-하나로)). 그 줄이 있어야 제대로 제출했을 때 안내 문구가 지워진다. 찾기(Ctrl+F)로 `clearNotice` 가 한 군데도 없는지 본다. `input` 두 줄이 남았으면 열자마자 그 줄에서 멈춰 맨 끝 `showList();` 도 실행되지 않는다 |
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` | `#clear-button` 을 못 찾았다. `guestbook.html` 에 **[전체 지우기]** 버튼 줄이 있는지, `id` 철자가 같은지 본다. 이 줄 아래 맨 끝 `showList();` 가 실행되지 않아 열 때 목록이 그려지지 않는다 |
| `Uncaught SyntaxError: Identifier 'clearButton' has already been declared` | 10주차 "먼저 끝났다면"의 **[전체 지우기]** 를 남겨 둔 채 같은 줄을 또 넣었다. 이 빨간 줄이 뜨면 `guestbook.js` 전체가 실행되지 않는다. 10주에 더한 버튼 줄(`guestbook.html`)·`const clearButton` 줄·클릭 등록 덩어리(`removeItem` 이 없는 쪽)를 지워 한 벌만 남긴다 |
| `Uncaught TypeError: Cannot read properties of null (reading 'length')` | 되살리는 줄 끝의 `\|\| []` 가 빠졌다. 저장 칸이 비어 있으면 `null` 이 들어와 목록을 그리다 멈춘다(ex06 4번) |
| `Uncaught SyntaxError: Unexpected token 'h', "hello" is not valid JSON` | 저장 칸에 JSON 이 아닌 글자가 들어 있다. Application 탭에서 값을 손으로 고쳤을 때 난다. `guestbook` 키를 지우고 새로고침한다. 이 빨간 줄의 `파일:줄` 은 `guestbook.js` 의 줄이 아니다(JSON 글자를 읽다가 났다). 되살리는 줄(`JSON.parse`)과 Application 표의 값을 본다 |
| `Uncaught SyntaxError: … is not valid JSON` — 저장한 글이 하나면 `"[object Object]" is not valid JSON`, 둘 이상이면 `Unexpected token 'o', "[object Obj"... is not valid JSON` | `JSON.stringify` 없이 배열을 그대로 저장했다(ex05 1번). `saveList()` 안을 고치고, Application 탭에서 `guestbook` 키를 한 번 지운 뒤 다시 남긴다. 바로 위 줄처럼 `파일:줄` 이 `guestbook.js` 를 가리키지 않으니 Application 표의 값을 본다 |
| 새로고침하면 목록이 사라진다 | 저장만 하고 되살리지 않았다. `let items = [];` 가 그대로면 되살리는 한 줄로 바꾼다(ex06 3번). 되살리는 줄이 있는데도 사라지면 `getItem` 의 키 철자가 `setItem` 의 `'guestbook'` 과 같은지 본다(빨간 줄 없이 빈 목록이 된다) |
| Application 표에 `guestbook` 키가 없다 | `saveList();` 를 부르는 곳이 없거나 키 철자가 다르다. 왼쪽 **Local Storage** 아래에서 지금 주소를 골랐는지도 본다 |
| 삭제했는데 새로고침하면 그 줄이 다시 나온다 | 삭제 버튼 틀 안의 `saveList();` 가 빠졌다. `items.splice(i, 1);` 바로 아래에 넣는다 |
| **[전체 지우기]** 를 누르면 비는데 새로고침하면 되살아난다 | `localStorage.removeItem('guestbook');` 가 빠졌다. `items = [];` 만으로는 저장 칸이 남는다(ex07 1번) |
| **[전체 지우기]** 를 누르면 `Uncaught TypeError: Assignment to constant variable.` | `items` 를 `const` 로 만들었다. 통째로 다시 담는 변수는 `let` 이다 |
| 공개 주소를 열었는데 글이 이미 있다 | 대개 9번에서 남긴 내 글이다. 같은 아이디의 `github.io` 주소는 저장소가 달라도 저장 칸을 함께 쓰므로, 다른 저장소의 방명록에 남긴 글일 수도 있다. **[전체 지우기]** 를 누르고 다시 남긴다 |
| 내 PC 미리 보기에 모르는 글이 있다 | 이 PC 를 먼저 쓴 사람이 같은 Chrome 으로 남긴 글이다. 미리 보기의 저장 칸은 이 PC 의 Chrome 에 있다. `http://localhost:8000` 은 앞사람과 주소가 같고, 두 번 눌러 연 파일(`file://`)은 폴더가 달라도 칸 하나를 함께 쓴다. **[전체 지우기]** 를 누른다. 확인과 캡처는 공개 주소에서 하므로 제출과는 상관없다 |
| 날짜 모양이 옆 사람과 다르다 | 브라우저 언어 설정에 따라 다르다. 날짜가 보이면 된 것이다. 틀 안은 고치지 않는다 |
| 공개 주소 `…/web-week11/ex/` 가 404 다 | ① 폴더 이름이 `ex` 인지 ② 그 안에 `index.html` 이 있는지 ③ 저장소 이름이 `web-week11` 이고 **Settings › Pages** 가 켜져 있는지 본다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://student01.github.io/web-week11/guestbook.html` (본인 아이디) 에서 아래 순서로 만든 화면을 캡처한다.

1. 이미 남긴 글(9번에서 남긴 글 등)이 보이면 **[전체 지우기]** 를 먼저 누른다.
2. 이름·메시지를 넣어 글 **세 개**를 남긴다.
3. **새로고침**한다. 세 줄과 `3개` 가 그대로 남아 있어야 한다.
4. F12 **Application › Local Storage** 에서 내 공개 주소를 고르고 `guestbook` 키를 누른다.
5. 목록과 Application 탭이 한 화면에 보이게 찍는다.

- 목록 한 줄에 이름·메시지·날짜가 함께 보인다.
- **주소창이 함께 보이게** 찍는다. 화면이 좁아 한 장에 담기지 않으면 강의자 안내를 따른다.
- 시크릿 창이 아니라 일반 창에서 찍는다.

1일차 push 와 `ex/` 실험 파일은 확인용이며 따로 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 다크 모드 기억하기: `app.js` 의 다크 모드 버튼 안에서 `toggle` 다음에 다크 모드가 켜졌으면 `localStorage.setItem('dark', 'on')`, 꺼졌으면 `localStorage.removeItem('dark')` 를 한다. 파일 맨 끝에서 `localStorage.getItem('dark') === 'on'` 이면 `document.body.classList.add('dark')` 로 되살린다. 켜졌는지는 6주차 "먼저 끝났다면"의 `document.body.classList.contains('dark')` 로 안다. 키는 `guestbook` 과 겹치지 않게 `dark` 로 둔다.
- 값 깨뜨려 보기: Application 표에서 `guestbook` 의 값을 두 번 눌러 `hello` 로 고치고 새로고침한다. 어느 줄에서 어떤 빨간 줄이 뜨나? 확인했으면 그 키를 지운다.
- 이메일도 담기: `guestbook.js` 에서 `#email` 을 찾아 두고, 객체에 `email: emailInput.value.trim()` 을 더하고, 목록 한 줄 끝에 `` ` · ${items[i].email}` `` 을 붙인다. 이메일을 넣기 **전에** 남긴 글은 어떻게 보이나? 왜 그런가?

추가 과제는 선택 사항이며 채점하지 않는다.
