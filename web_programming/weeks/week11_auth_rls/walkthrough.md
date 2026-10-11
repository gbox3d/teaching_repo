[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls)

# 11주차 따라하기 — 비교 예제로 원리를 보고 마지막에 조립

이번 주는 새 저장소 `web-week11`을 만든다. 지난주 완성본을 넣고, 비교 예제는 그 안의 `ex/` 폴더에 저장한다. 값·줄을 바꾼 뒤 결과를 화면과 **F12 › Console**, 2일차부터는 **F12 › Application**에서 본다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.
**이번 주부터 확인·캡처는 공개 주소에서만 한다.** 내 PC 에서 연 화면(`file://`·`http://localhost:8000/`)과 공개 주소는 저장 칸이 따로다. 내 PC 에서는 값 바꿔 보기와 미리 보기만 한다.

비교 예제 7개는 교재 저장소의 [examples/day1](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls/examples/day1)(1일차 ex01~ex03과 고르기 페이지)과 [examples/day2](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls/examples/day2)(2일차 ex04~ex07과 고르기 페이지) 폴더에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다.

## 1일차

### 1. web-week11 폴더 만들고 지난주 완성본 넣기

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-week11`을 만들고 VS Code **File › Open Folder**로 연다.

지난주 완성본을 넣는다. 내 `web-week10` 저장소 GitHub 화면에서 **Code › Download ZIP**을 누르고, 압축을 푼 폴더에서 맨 위 파일(`index.html`·`about.html`·`guestbook.html`·`guestbook.js`·`styles.css`·`app.js`·`README.md`·`server.mjs`)과 `images/`·`screenshots/`를 `web-week11`으로 옮긴다. 지난주 `ex/` 폴더는 옮기지 않는다.
ZIP을 못 받았으면 교재 [10주차 `examples/day2/web-week10/`](../week10_supabase_data/examples/day2/web-week10/)의 파일을 2단계와 같은 **Raw** 방법으로 받고, [server.mjs](../../tools/static-server/server.mjs)도 같은 방법으로 받는다.

이어서 `web-week11` 안에 `ex` 폴더를 만든다. 현재 폴더: `web-week11`

```bash
mkdir ex
```

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week11/
  ex/            ← 아직 비어 있다
  images/
  screenshots/
  README.md
  about.html
  app.js
  guestbook.html
  guestbook.js
  index.html
  server.mjs
  styles.css
```

- `guestbook.html`을 두 번 눌러 열면 10주차 완성 화면이 보인다. 글 남기기 폼이 있고, "남긴 글" 아래에 `아직 남긴 글이 없습니다.`와 `0개`가 보인다. 글을 남기면 줄마다 **[삭제]** 버튼이 붙는다. 이번 주는 여기서 시작한다.
- `guestbook.html`·`guestbook.js`는 오늘 건드리지 않는다. 2일차 끝에 조립한다.

### 2. 비교 예제 가져오기

오늘 파일은 네 개다. 고르기 페이지 `index.html` 하나와 예제 코드 `.js` 세 개다. 세 예제가 같은 화면을 쓰기 때문에 화면은 `index.html` 하나에 두고 코드만 따로 뗐다.

| 파일 | 비교하는 것 |
|---|---|
| [index.html](examples/day1/index.html) | 고르기 페이지. 맨 아래 `<script src>` 세 줄 중 하나만 켠다. ex03 이 쓰는 목록 두 개(`#list1`·`#list2`)가 여기 있다 |
| [ex01_object.js](examples/day1/ex01_object.js) | 객체 통째로 / 점 표기로 값 하나 / 없는 이름표 / 값 자리에 변수 |
| [ex02_array_objects.js](examples/day1/ex02_array_objects.js) | 글자를 쌓은 배열 / 객체를 쌓은 배열, 날짜 틀 |
| [ex03_list_line.js](examples/day1/ex03_list_line.js) | 객체를 그대로 넣은 줄 / 점 표기로 꺼내 넣은 줄 |

[교재 저장소 examples/day1 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls/examples/day1)에서 파일을 누르고 오른쪽 위 **Raw**를 누른다. 코드만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `web-week11/ex/`에 저장한다. 파일 이름은 교재와 **같게** 둔다. Raw가 열리지 않을 때만 주석 줄까지 그대로 친다.

**예상 결과** — `ex/` 안에 파일 네 개가 있다.

```text
ex/
  ex01_object.js
  ex02_array_objects.js
  ex03_list_line.js
  index.html
```

- 저장한 파일 이름이 `.txt`로 끝나면 이름을 고친다. 이름은 VS Code 탐색기에서 확인한다.
- `ex/index.html`은 예제를 고르는 페이지다. 맨 위 `index.html`(내 사이트)과 이름이 같지만 다른 파일이다. 탭 이름 옆 폴더 경로로 구분한다. 2일차에는 이 파일을 같은 이름의 2일차 고르기 페이지로 덮어쓴다.

### 3. 고르기 페이지와 Console 에서 펼쳐 보기

`ex/index.html`을 Chrome으로 연다(VS Code 탐색기에서 오른쪽 클릭 › **Reveal in File Explorer**, macOS는 **Reveal in Finder** → 두 번 누르기). `.js` 파일은 두 번 누르지 않는다. `.js`는 `index.html`이 불러온다.

VS Code에서 `ex/index.html`도 열어 맨 아래를 본다.

```html
<script src="ex01_object.js"></script>
<!-- <script src="ex02_array_objects.js"></script> -->
<!-- <script src="ex03_list_line.js"></script> -->
```

지금은 ex01 줄만 켜져 있다. 다른 예제로 바꿀 때는 켜 둔 줄에 커서를 두고 **Ctrl+/**(macOS **⌘+/**)로 주석으로 만들고, 볼 줄에서 다시 **Ctrl+/** 로 주석을 푼다. 저장 → 새로고침한다. 한 번에 한 줄만 켠다.

**예상 결과** — F12 › **Console**에 다섯 줄이 찍혀 있다. 줄 끝의 `ex01_object.js:6`이 그 줄을 찍은 파일과 줄 번호다.

```text
1. item : {name: '하늘', message: '안녕하세요', date: '2026. 11. 11.'}   ex01_object.js:6
2. item.name : 하늘                                                    ex01_object.js:7
3. item.date : 2026. 11. 11.                                           ex01_object.js:8
4. item.nmae : undefined                                               ex01_object.js:9
5. item5.name : 바다                                                   ex01_object.js:15
```

이번 주에는 Console 에 찍힌 객체·배열을 **펼쳐** 본다. 1번 줄에서 `1. item :` 뒤, `{name: …}` 바로 앞의 ▶를 누른다.

**예상 결과** — 1번 줄 아래로 이름표 세 개와 값이 한 줄씩 펼쳐진다. `[[Prototype]]` 줄이 함께 보이면 그것은 내가 적은 이름표가 아니다. 펼친 목록의 순서는 코드에 적은 순서와 다를 수 있다. 순서가 아니라 이름표와 값의 짝을 본다.

- 객체는 중괄호 `{ }`, 배열은 대괄호 `[ ]`로 찍힌다. ex02 에서 둘이 섞인 모양(`[{…}, {…}]`)을 본다.
- 4번 `undefined`는 오류가 아니다. 없는 이름표를 물었다는 뜻이다. 빨간 줄이 없어서 찍힌 값을 읽어야 찾는다.

### 4. 값 바꾸는 요령

실험은 늘 같은 순서다. **VS Code에서 고치고 저장**(Ctrl+S, macOS는 ⌘+S) → **브라우저에서 새로고침**(F5, macOS는 ⌘+R) → **화면·Console**을 본다.
바꾸기 전에 무엇이 달라질지 먼저 말해 보고 확인한다.

**목록에 써 보기** — `ex/index.html` 맨 아래에서 ex01 줄을 끄고 `ex03_list_line.js` 줄을 켠 뒤 저장 → 새로고침한다.

**예상 결과** — "ex03 이 쓰는 자리"의 두 목록이 아래처럼 채워진다. Console 에 빨간 줄이 없다.

```text
1. 객체를 그대로 넣은 줄
   • [object Object]
   • [object Object]
2. 점 표기로 꺼내 넣은 줄
   • 하늘: 안녕하세요 (2026. 11. 11.)
   • 바다: 잘 봤습니다 (2026. 11. 11.)
```

같은 객체를 넣었는데 1번은 내용이 사라졌다. 글자 자리에 객체를 통째로 넣으면 `[object Object]`라는 글자가 된다. 2번은 점 표기로 값을 하나씩 꺼내 백틱 문장(5주차 템플릿 문자열)에 넣었다.

- 값을 원래대로 못 돌리겠으면 교재에서 그 파일을 다시 **Raw**로 받아 덮어쓴다.
- 파일마다 무엇을 바꿔 볼지는 [1일차 실습](lab.md#1일차--객체와-점-표기-60분)에 있다.

### 5. 이번 주 저장소 만들어 올리기

1일차 50–60분에 한다. 세 예제에서 각각 값 하나 이상을 바꿔 봤으면 올린다.

GitHub에서 **New repository**를 누르고 이름 `web-week11`, **Public**으로 만든다. README는 추가하지 않는다.
터미널에서 2주차에 배운 순서 그대로 친다. 현재 폴더: `web-week11`

```bash
git init
git add .
git commit -m "11주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week11.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save**를 누른다.

**예상 결과** — GitHub 저장소 화면을 새로고침하면 `ex/`·`images/`·`screenshots/`와 맨 위 파일들이 보인다.
1~3분 뒤 `https://student01.github.io/web-week11/ex/`를 연다. 고르기 페이지의 제목과 "ex03 이 쓰는 자리"가 보인다. 이 화면은 **확인용**이다.
공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 404가 나면 주소의 `web-week11/ex/`가 저장소·폴더 이름과 글자 단위로 같은지, Pages를 켰는지 본다.
- push가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../week02_github_pages/lab.md#막혔을-때)를 본다.

## 2일차

### 6. 폴더 열고 2일차 예제 다섯 파일 가져오기

같은 PC에 `web-week11` 폴더가 남아 있으면 VS Code로 그대로 연다. 없으면 받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week11.git
```

내려받은 `web-week11`을 **File › Open Folder**로 연다.

오늘 파일은 다섯 개다. 고르기 페이지 `index.html` 하나와 예제 코드 `.js` 네 개다. 네 예제 모두 결과를 Console과 Application 탭에서 보므로, 1일차처럼 화면은 `index.html` 하나에 두고 코드만 뗐다. ex04가 쓰는 **저장하기** 버튼도 `index.html`의 "ex04 가 쓰는 자리"에 있다.

| 파일 | 비교하는 것 |
|---|---|
| [index.html](examples/day2/index.html) | 고르기 페이지. 맨 아래 `<script src>` 네 줄 중 하나만 켠다. ex04가 쓰는 **저장하기** 버튼이 여기 있다 |
| [ex04_storage.js](examples/day2/ex04_storage.js) | 변수 `memo` / 저장 칸 `ex04-memo` |
| [ex05_json.js](examples/day2/ex05_json.js) | 배열을 그대로 저장 / `JSON.stringify` 해서 저장 / `JSON.parse` 로 되살리기 |
| [ex06_or.js](examples/day2/ex06_or.js) | if 안의 `\|\|` / `\|\|` 없이 되살리기 / `\|\| []` 붙여 되살리기 |
| [ex07_remove.js](examples/day2/ex07_remove.js) | `items = []` / `removeItem` / 다른 키 |

[교재 저장소 examples/day2 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls/examples/day2)에서 1일차와 같은 **Raw** → 저장으로 `web-week11/ex/`에 넣는다. `index.html`은 1일차 고르기 페이지와 이름이 같다. 바꿀지 물으면 바꾼다(덮어쓴다).

**예상 결과** — `ex/` 안에 파일 여덟 개가 있다. 1일차 `.js` 세 개는 그대로 남고 `index.html`만 2일차 것으로 바뀌었다.

```text
ex/
  ex01_object.js
  ex02_array_objects.js
  ex03_list_line.js
  ex04_storage.js
  ex05_json.js
  ex06_or.js
  ex07_remove.js
  index.html          ← 2일차 고르기 페이지
```

- `ex/index.html` 맨 아래는 처음에 `ex04_storage.js` 줄만 켜져 있다. 문항이 바뀌면 1일차처럼 **Ctrl+/**(macOS **⌘+/**)로 켤 줄을 바꾸고 저장 → 새로고침한다. 한 번에 한 줄만 켠다.
- **저장하기** 버튼은 ex04 줄을 켰을 때만 일을 한다. 다른 줄을 켜 두었을 때는 눌러도 아무 일이 없다.
- 조립할 때 ex01~ex03은 VS Code에서 코드만 열어 본다.

이번 주에는 **Application** 탭을 처음 쓴다. `ex/index.html`을 Chrome으로 열고(ex04 줄만 켜진 상태) F12 › 위쪽 탭 줄에서 **Application**을 누른다(안 보이면 `>>`를 눌러 고른다). 왼쪽 **Local Storage**를 펼쳐 그 아래의 주소 한 줄을 누르면, 오른쪽 표에 Key(키)와 Value(값)가 보인다. 이 표가 브라우저의 저장 칸이다.

**예상 결과** — 처음 열면 Console 이 아래와 같고, Application 표에 `ex04-memo`가 없다.

```text
1. 변수 memo : (처음 값)            ex04_storage.js:7
2. 저장 칸 ex04-memo : null         ex04_storage.js:8
```

**저장하기**를 누르고 새로고침하면 2번만 바뀐다. Application 표에 Key `ex04-memo`, Value `안녕하세요` 한 줄이 생긴다(표가 그대로면 표 위의 새로고침 단추를 누른다).

```text
1. 변수 memo : (처음 값)            ex04_storage.js:7
2. 저장 칸 ex04-memo : 안녕하세요   ex04_storage.js:8
```

- 변수는 페이지를 열 때마다 처음 값으로 다시 시작한다. 저장 칸에 적은 것은 새로고침해도 남는다.
- 저장 칸은 **주소마다** 따로 있다. 두 번 눌러 연 `file://` 의 칸, `http://localhost:8000/` 의 칸, 공개 주소의 칸이 모두 다르다.
- 예제의 키는 `ex04-memo`·`ex05-json` 처럼 예제 번호로 시작한다. 같은 주소의 저장 칸은 함께 쓰므로, 완성본의 `guestbook` 키와 섞이지 않게 했다.
- 파일마다 무엇을 바꿔 볼지는 [2일차 실습](lab.md#2일차--저장-칸에-남기고-되살리기-그리고-조립-60분)에 있다.

### 7. 조립표

29분부터 조립한다. 이제 `ex/`가 아니라 `web-week11` 맨 위의 `guestbook.html`·`guestbook.js`를 연다.
조립하는 줄은 모두 비교 예제와 10주차 완성본에서 본 것이다. 아래 순서대로 한 단계씩 고치고, 단계마다 저장 → 새로고침으로 확인한다.

| 단계 | 조립할 줄 | 출처 |
|---|---|---|
| 8 | `#empty` 줄 지우기, 빈 목록 문장과 개수를 모두 `#count` 에 | 10주차 완성본의 `if / else` |
| 9 | `if (name === '' \|\| message === '')`, `notice.textContent = '';` | [ex06](examples/day2/ex06_or.js) 1번, 10주차 완성본 `clearNotice()` 안의 줄 |
| 10 | `const today = new Date().toLocaleDateString();` | [ex02](examples/day1/ex02_array_objects.js) 날짜 틀 |
| 10 | `items.push({ name: name, message: message, date: today });` | [ex01](examples/day1/ex01_object.js) 5번, [ex02](examples/day1/ex02_array_objects.js) 3번 |
| 10 | `` li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`; `` | [ex03](examples/day1/ex03_list_line.js) 2번 |
| 11 | `function saveList() { localStorage.setItem('guestbook', JSON.stringify(items)); }` | [ex05](examples/day2/ex05_json.js) 2번, [ex04](examples/day2/ex04_storage.js) `setItem` |
| 11 | `push` 다음·`splice` 다음의 `saveList();` | [ex05](examples/day2/ex05_json.js) 셋째 바꿔 보기 — 저장은 배열이 바뀐 뒤에 |
| 12 | `let items = JSON.parse(localStorage.getItem('guestbook')) \|\| [];` | [ex06](examples/day2/ex06_or.js) 3번, [ex05](examples/day2/ex05_json.js) 3번, [ex04](examples/day2/ex04_storage.js) `getItem` |
| 13 | **[전체 지우기]** 버튼 줄, `const clearButton`, `clearButton.addEventListener('click', …)` | ex04: 고르기 페이지 [index.html](examples/day2/index.html)의 버튼 줄·[찾아 두기와 클릭 등록](examples/day2/ex04_storage.js) |
| 13 | `items = []; localStorage.removeItem('guestbook'); showList();` | [ex07](examples/day2/ex07_remove.js) 1·2번, 10주차 완성본 `showList()` |

옮겨 적을 때 출처 ex 파일을 옆에 열어 두고, 같은 줄이 거기서 무엇을 했는지 떠올린다.
조립 중 미리 보기는 `guestbook.html`을 두 번 눌러 열거나 서버(16단계)로 연다. 이 미리 보기의 저장 칸은 내 PC 의 것이다.

### 8. 빈 목록 안내를 개수 자리로

`guestbook.html`을 열고 `<main>` 끝의 아래 두 줄을 찾는다.

```html
      <div id="empty">아직 남긴 글이 없습니다.</div>
      <div id="count">0개</div>
```

첫 줄을 지우고, 둘째 줄의 처음 글자를 바꾼다.

```html
      <div id="count">아직 남긴 글이 없습니다.</div>
```

이어서 `guestbook.js` 위쪽의 `const empty = document.querySelector('#empty');` 한 줄을 지운다. 그다음 `showList()` 끝의 아래 여섯 줄을 지우고

```js
  count.textContent = `${items.length}개`;
  if (items.length === 0) {
    empty.textContent = '아직 남긴 글이 없습니다.';
  } else {
    empty.textContent = '';
  }
```

아래 다섯 줄을 넣는다.

```js
  if (items.length === 0) {
    count.textContent = '아직 남긴 글이 없습니다.';
  } else {
    count.textContent = `${items.length}개`;
  }
```

**예상 결과** — 페이지를 열면 목록 아래에 `아직 남긴 글이 없습니다.` 한 줄만 보인다. 글을 남기면 그 자리가 `1개`로 바뀌고, 모두 지우면 안내 문장이 돌아온다. Console 에 `Uncaught` 로 시작하는 빨간 줄이 없다(서버로 열면 `favicon.ico` 404 한 줄은 상관없다).

- 한 자리(`#count`)가 두 가지 일을 한다. 목록이 비면 안내 문장, 아니면 개수다. `if / else`는 10주차 완성본 그대로이고 쓰는 자리만 `empty`에서 `count`로 바꿨다.
- HTML 에서 `#empty`를 지우고 `guestbook.js`에 `empty`가 남으면 `Cannot set properties of null (setting 'textContent')` 빨간 줄이 뜬다. 찾기(Ctrl+F)로 `empty`가 한 군데도 없는지 본다.

### 9. 안내 문구를 하나로

`guestbook.js` 위쪽의 `clearNotice()` 함수 세 줄과 그 아래 빈 줄을 지운다.

```js
function clearNotice() {
  notice.textContent = '';
}
```

파일 맨 아래 `showList();` 위의 두 줄도 지운다.

```js
nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
```

마지막으로 submit 리스너 안의 아래 열한 줄을 지우고

```js
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
```

아래 여섯 줄을 넣는다.

```js
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    nameInput.focus();
    return;
  }
  notice.textContent = '';
```

**예상 결과** — 이름 칸만 비우고 눌러도, 메시지 칸만 비우고 눌러도 `이름과 메시지를 모두 입력하세요.`가 보인다. 두 칸을 채워 누르면 안내 문구가 사라지고 목록에 한 줄이 는다.
메시지 칸만 비웠을 때도 커서는 **이름 칸**으로 간다. 안내가 하나가 되어 `nameInput.focus()` 한 줄만 남았기 때문이다. 고장이 아니다.

- `||`는 ex06 1번의 **또는**이다. 둘 중 하나라도 비면 안내를 보여 주고 `return`으로 멈춘다.
- 안내를 지우는 일은 제출에 성공한 자리 한 곳(`notice.textContent = '';`)에서만 한다. 그래서 `clearNotice()` 함수와 `input` 두 줄이 필요 없다. 이 줄은 10주차 `clearNotice()` 안에 있던 줄이다. 이제 칸에 글자를 쳐도 안내가 바로 지워지지 않고, 다음에 제대로 제출할 때 지워진다.
- `clearNotice`라는 이름이 파일에 **한 군데도 남지 않아야** 한다. 남으면 `Uncaught ReferenceError: clearNotice is not defined` 빨간 줄이 뜬다. 맨 아래 `input` 두 줄이 남았으면 열자마자 그 줄에서 멈추고, 그 아래 맨 끝 `showList();`도 실행되지 않는다. 찾기(Ctrl+F)로 `clearNotice`가 없는지 본다.

### 10. 한 줄을 객체로

submit 리스너 안에서 아래 한 줄을 찾는다.

```js
  items.push(`${name}: ${message}`);
```

이 한 줄을 지우고 두 줄을 넣는다.

```js
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
```

그리고 `showList()` 안의 `li.textContent = items[i];` 한 줄을 아래 한 줄로 바꾼다.

```js
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
```

**예상 결과** — 이름 `하늘`, 메시지 `안녕하세요`를 넣고 **[남기기]** 를 누르면 목록에 `하늘: 안녕하세요 (2026. 11. 11.)`처럼 이름·메시지·오늘 날짜가 한 줄로 보인다. 줄마다 붙는 **[삭제]** 버튼은 그대로다. 새로고침하면 아직 사라진다.

- `{ name: name, … }`의 왼쪽은 이름표, 오른쪽은 바로 위에서 만든 변수다(ex01 5번).
- `new Date().toLocaleDateString()`은 ex02 의 날짜 틀이다. 그대로 옮겨 쓴다. 날짜 모양은 브라우저 언어 설정에 따라 다르다.
- `push`만 바꾸고 `li.textContent`를 그대로 두면 목록에 `[object Object]`가 보인다(ex03 1번). 오류가 아니므로 화면 글자로 찾는다.

### 11. 저장하기 — saveList

`guestbook.js`의 `function showList() {` **위**에 함수 하나와 빈 줄 하나를 넣는다.

```js
function saveList() {
  localStorage.setItem('guestbook', JSON.stringify(items));
}
```

그리고 `saveList();` 한 줄을 두 곳에 넣는다. 먼저 submit 리스너 안 `items.push({ … });` 바로 아래다.

```js
  saveList();
```

다음은 삭제 버튼 틀 안 `items.splice(i, 1);` 바로 아래다. 들여쓰기가 더 깊다.

```js
      saveList();
```

**예상 결과** — 글을 하나 남기고 Application › Local Storage 에서 지금 주소를 누르면 Key `guestbook`에 `[{"name":"하늘","message":"안녕하세요","date":"2026. 11. 11."}]` 같은 값이 보인다. 다만 새로고침하면 목록은 아직 사라진다. 12단계에서 되살린다.

- 저장 칸에는 글자만 들어가므로 `JSON.stringify`로 배열을 글자로 바꿔 넣는다(ex05 2번). 키 이름은 `guestbook`으로 둔다.
- 저장은 배열이 **바뀐 뒤에** 한다. `push` 다음, `splice` 다음이다(ex05 셋째 바꿔 보기).
- 함수 이름은 `saveList`다. `showList`와 한 글자 차이이므로 천천히 읽는다.

### 12. 열 때 되살리기

`guestbook.js` 위쪽의 `let items = [];` 한 줄을 아래 한 줄로 바꾼다.

```js
let items = JSON.parse(localStorage.getItem('guestbook')) || [];
```

**예상 결과** — 저장하고 새로고침하면 11단계에서 남긴 글이 다시 보인다(글 하나였으면 그 한 줄과 `1개`). 저장 칸에서 되살린 것이다. 11단계와 같은 방법(두 번 눌러 열기 또는 서버)으로 연 화면이어야 같은 저장 칸이다. 글을 더 남겨 세 줄로 만들고 **새로고침**해도 세 줄과 `3개`가 그대로 남아 있다.

- 안에서 밖으로 읽는다. 꺼내기(`getItem`, ex04) → 되살리기(`JSON.parse`, ex05) → 없으면 빈 배열(`|| []`, ex06 3번).
- 저장 칸이 빈 사람(처음 여는 사람)은 `null`을 받는다. `|| []`가 없으면 목록을 그리다 `Cannot read properties of null (reading 'length')` 빨간 줄이 뜬다.
- 파일 맨 끝의 `showList();`가 되살린 배열을 그린다. 10주차에 넣어 둔 줄이며 지우지 않는다.

### 13. 전체 지우기

**HTML 을 먼저 고친다.** `guestbook.html`의 `<div id="count">…</div>` 줄 **아래**에 한 줄을 넣는다.

```html
      <div><button id="clear-button" type="button">전체 지우기</button></div>
```

이어서 `guestbook.js`의 `const count = document.querySelector('#count');` 줄 아래에 한 줄을 넣는다.

```js
const clearButton = document.querySelector('#clear-button');
```

그리고 파일 맨 끝 `showList();` **위**에 다섯 줄과 빈 줄 하나를 넣는다.

```js
clearButton.addEventListener('click', function () {
  items = [];
  localStorage.removeItem('guestbook');
  showList();
});
```

**예상 결과** — 목록 아래에 **[전체 지우기]** 버튼이 보인다. 누르면 목록이 비고 `아직 남긴 글이 없습니다.`가 보이며, 새로고침해도 비어 있다. Application 표에서 `guestbook` 키도 사라진다.

- `items = [];`는 배열을 비우고 `removeItem('guestbook')`은 저장 칸을 지운다(ex07 1·2번). 둘 다 해야 새로고침 뒤에도 비어 있다.
- `items`를 통째로 다시 담으므로 `let`이어야 한다. 10주차부터 `let`으로 선언해 두었다.
- 버튼 줄을 HTML 에 넣지 않고 `guestbook.js`만 고치면 `Cannot read properties of null (reading 'addEventListener')` 빨간 줄이 뜬다.

### 14. guestbook.html 전문

13단계까지 마친 `guestbook.html` 전체다. 내 파일과 한 줄씩 비교한다. 10주차 파일과 다른 곳은 `#count` 줄과 그 아래 버튼 줄뿐이다(`#empty` 줄은 없다).

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
      <div id="notice"></div>
      <h3>남긴 글</h3>
      <ul class="card" id="list"></ul>
      <div id="count">아직 남긴 글이 없습니다.</div>
      <div><button id="clear-button" type="button">전체 지우기</button></div>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

같은 파일이 [examples/day2/web-week11/guestbook.html](examples/day2/web-week11/guestbook.html)에 있다.

### 15. guestbook.js 전문

글자 단위로 같아야 한다.

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const count = document.querySelector('#count');
const clearButton = document.querySelector('#clear-button');
let items = JSON.parse(localStorage.getItem('guestbook')) || [];

function saveList() {
  localStorage.setItem('guestbook', JSON.stringify(items));
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      saveList();
      showList();
    });
    li.append(removeButton);
    list.append(li);
  }
  if (items.length === 0) {
    count.textContent = '아직 남긴 글이 없습니다.';
  } else {
    count.textContent = `${items.length}개`;
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    nameInput.focus();
    return;
  }
  notice.textContent = '';
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
  saveList();
  showList();
  form.reset();
  nameInput.focus();
});

clearButton.addEventListener('click', function () {
  items = [];
  localStorage.removeItem('guestbook');
  showList();
});

showList();
```

같은 파일이 [examples/day2/web-week11/guestbook.js](examples/day2/web-week11/guestbook.js)에 있다.

- 8행은 열 때 저장 칸에서 되살린다(ex04·ex05·ex06). 10~12행 `saveList()`는 배열을 글자로 바꿔 적는다(ex05).
- 18행이 목록 한 줄이다. 이름·메시지·날짜를 점 표기로 꺼냈다(ex03).
- 23행과 48행이 `saveList();`를 부르는 두 곳이다. 둘 다 배열이 바뀐 바로 다음이다.
- 40행 `||`는 "둘 중 하나라도 비면"이다(ex06 1번). 46~47행이 오늘 날짜와 객체 한 개다(ex01·ex02).
- 54~58행이 전체 지우기다. 배열과 저장 칸을 모두 비운 뒤 다시 그린다(ex07).

### 16. 내 PC 에서 미리 보기

1일차에 넣어 둔 `server.mjs`가 없으면 [server.mjs](../../tools/static-server/server.mjs)를 **Raw**로 받아 `web-week11` 맨 위에 둔다. 현재 폴더: `web-week11`

```bash
node server.mjs
```

주소창에 `http://localhost:8000/guestbook.html`을 친다. Node가 없는 PC는 `guestbook.html`을 두 번 눌러 연다.

**예상 결과** — 글을 두 개 남기고 새로고침해도 두 줄과 `2개`가 남는다. Console 에 `Uncaught` 로 시작하는 빨간 줄이 없다. 서버로 열면 `favicon.ico` 404 한 줄은 보여도 된다(탭 아이콘 요청).

- 이 화면의 저장 칸은 `http://localhost:8000` 의 것이다. 여기 남긴 글은 공개 주소에 없다. 그래서 이 화면은 미리 보기이고, 확인과 캡처는 다음 단계에서 공개 주소로 한다.
- 확인이 끝나면 터미널에서 **Ctrl+C**로 서버를 멈춘다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.

### 17. push 하고 공개 주소에서 확인

2일차 48–55분에 한다. 현재 폴더: `web-week11`

```bash
git add .
git commit -m "11주차 2일차"
git push
```

1~3분 뒤 `https://student01.github.io/web-week11/guestbook.html`을 연다. 글을 두 개 남기고 새로고침한다. 이어서 DevTools의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)를 켜고 폭을 375와 1280으로 바꿔 본다.

**예상 결과** — 새로고침해도 두 줄과 `2개`가 남는다. Application › Local Storage › `https://student01.github.io` 에 `guestbook` 키가 있다. 375 폭에서는 메뉴가 세로로 서고(4주차 `@media`), 1280 폭에서는 가운데 640px 안에 보인다.

- 16단계에서 내 PC 에 남긴 글은 여기 보이지 않는다. 저장 칸이 주소마다 따로이기 때문이다. 고장이 아니다.
- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.

### 18. 캡처

2일차 55–60분에 한다. 공개 주소에서 아래 순서로 만든 화면을 캡처한다.

1. 17단계에서 남긴 글이 보이면 **[전체 지우기]** 를 먼저 누른다.
2. 이름·메시지를 넣어 글 세 개를 남기고 **새로고침**한다. 세 줄과 `3개`가 그대로여야 한다.
3. F12 **Application › Local Storage**에서 내 공개 주소를 고르고 `guestbook` 키를 누른다.
4. 목록과 Application 탭, 주소창이 한 화면에 보이게 캡처한다. 이 캡처 한 장이 제출이다.

**예상 결과** — 목록 세 줄이 `하늘: 안녕하세요 (2026. 11. 11.)`처럼 보이고, Application 표의 `guestbook` 값이 `[{"name":"하늘",…},…]` 모양이다.
캡처 뒤에 고친 것이 있으면 `git add .` → `git commit -m "11주차 2일차"` → `git push`를 한 번 더 한다. 공용 PC라면 **[전체 지우기]** 를 누르고 자격 증명을 지우고 나간다.

- 시크릿 창이 아니라 일반 창에서 찍는다. 실명·학번·실제 이메일이 보이지 않게 한다.
- 막히면 [실습지의 막혔을 때](lab.md#막혔을-때)를 본다.
