[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

# 13주차 따라하기 — 비교 예제로 원리를 보고 마지막에 조립

이번 주는 새 저장소 `web-week13`을 만든다. 지난주 완성본을 넣고, 비교 예제는 그 안의 `ex/` 폴더에 저장한다. 값·줄을 바꾼 뒤 결과를 화면과 **F12 › Console**, **F12 › Elements**에서 보고, `.md` 예제는 VS Code **Open Preview**에서 본다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

비교 예제 8개는 교재 저장소의 [examples/day1](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security/examples/day1)(1일차 ex01~ex05와 고르기 페이지, 그림)과 [examples/day2](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security/examples/day2)(2일차 ex06~ex08) 폴더에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다.

**확인·캡처는 공개 주소에서 한다.** 내 PC 에서 볼 때는 `node server.mjs` → `http://localhost:8000/` 로 연다. 방명록 글은 주소마다 따로 저장되고, 프로젝트 카드는 두 번 눌러 연 `file://` 화면에는 나오지 않는다.

## 1일차

### 1. web-week13 폴더 만들고 지난주 완성본 넣기

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-week13`을 만들고 VS Code **File › Open Folder**로 연다.

지난주 완성본을 넣는다. 내 `web-week12` 저장소 GitHub 화면에서 **Code › Download ZIP**을 누르고, 압축을 푼 폴더에서 맨 위 파일(`index.html`·`about.html`·`guestbook.html`·`projects.html`·`styles.css`·`app.js`·`guestbook.js`·`projects.js`·`README.md`·`server.mjs`)과 `images/`·`data/`·`screenshots/` 폴더를 `web-week13`으로 옮긴다. 지난주 `ex/` 폴더는 옮기지 않는다.
ZIP을 못 받았으면 교재 [12주차 `examples/day2/web-week12/`](../week12_persistent_crud/examples/day2/web-week12/)의 파일을 2단계와 같은 **Raw** 방법으로 받고, [server.mjs](../../tools/static-server/server.mjs)도 같은 방법으로 받는다.

이어서 `web-week13` 안에 `ex` 폴더를 만든다. 현재 폴더: `web-week13`

```bash
mkdir ex
```

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week13/
  data/          projects.json
  ex/            ← 아직 비어 있다
  images/        profile.png  project1.png  project2.png  project3.png
  screenshots/   home.png  guestbook.png
  about.html
  app.js
  guestbook.html
  guestbook.js
  index.html
  projects.html
  projects.js
  README.md
  server.mjs
  styles.css
```

- 맨 위 파일은 오늘 건드리지 않는다. 2일차 끝에 `about.html`·`about.js`·`projects.js`·`screenshots/`·`README.md`를 조립한다.
- 터미널에서 `node server.mjs`를 실행하고 `http://localhost:8000/projects.html`을 열면 카드 세 장이 보인다. 이번 주는 이 상태에서 시작한다. 확인했으면 **Ctrl+C**로 서버를 멈춘다.

### 2. 비교 예제 가져오기

오늘 파일은 일곱 개와 그림 하나다. ex01·ex02는 같은 화면(입력 칸·버튼·결과 자리)을 쓰기 때문에 화면은 고르기 페이지 `index.html` 하나에 두고 코드만 `.js`로 뗐다. ex03은 화면이 달라 `.html`과 `.js` 한 쌍이고, ex04·ex05는 JavaScript가 없는 `.html` 하나다.

| 파일 | 비교하는 것 |
|---|---|
| [index.html](examples/day1/index.html) | 고르기 페이지. 맨 아래 `<script src>` 두 줄 중 하나만 켠다. 예제가 쓰는 자리(`#year` 칸·`#btn`·`#result`)가 여기 있다 |
| [ex01_number.js](examples/day1/ex01_number.js) | 글자 + 1 / `Number(글자)` + 1 / `isNaN` |
| [ex02_year.js](examples/day1/ex02_year.js) | 올해 / 올해 - 입학 연도 / + 1 |
| [ex03_text_html.html](examples/day1/ex03_text_html.html) + [ex03_text_html.js](examples/day1/ex03_text_html.js) | `textContent`로 넣기 / `innerHTML`로 넣기 / `innerHTML = ''`로 비우기 |
| [ex04_alt.html](examples/day1/ex04_alt.html) + 그림 [images/profile.png](examples/day1/images/profile.png) | 알맞은 `alt` / `alt` 없음 / `alt="그림"` |
| [ex05_label.html](examples/day1/ex05_label.html) | `for`와 `id`가 같다 / 한 글자 다르다 / `label` 없음 |

[교재 저장소 examples/day1 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security/examples/day1)에서 파일을 누르고 오른쪽 위 **Raw**를 누른다. 코드만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `web-week13/ex/`에 저장한다. 파일 이름은 교재와 **같게** 둔다. Raw가 열리지 않을 때만 주석 줄까지 그대로 친다.
그림은 `ex` 안에 `images` 폴더를 먼저 만들고, 교재의 `images/profile.png`를 눌러 그림만 보이는 화면에서 같은 방법으로 `ex/images/profile.png`로 저장한다.

**예상 결과** — `ex/` 안에 파일 일곱 개와 `images/profile.png`가 있다.

```text
ex/
  images/
    profile.png
  ex01_number.js
  ex02_year.js
  ex03_text_html.html
  ex03_text_html.js
  ex04_alt.html
  ex05_label.html
  index.html
```

- 저장한 파일 이름이 `.txt`로 끝나면 이름을 고친다. 이름은 VS Code 탐색기에서 확인한다.
- `ex/index.html`은 예제를 고르는 페이지다. 맨 위 `index.html`(내 사이트)과 이름이 같지만 다른 파일이다. 탭 이름 옆 폴더 경로로 구분한다.
- `ex/images/`는 ex04와 2일차 ex08이 쓰는 그림 자리다. 맨 위 `images/`와 같은 그림이지만 따로 둔다.

### 3. 고르기 페이지와 여는 법

`ex/index.html`을 Chrome으로 연다(VS Code 탐색기에서 오른쪽 클릭 › **Reveal in File Explorer**, macOS는 **Reveal in Finder** → 두 번 누르기). `.js` 파일은 두 번 누르지 않는다. `.js`는 `index.html`이 불러온다.

VS Code에서 `ex/index.html`도 열어 맨 아래를 본다.

```html
<script src="ex01_number.js"></script>
<!-- <script src="ex02_year.js"></script> -->
```

지금은 ex01 줄만 켜져 있다. ex02로 바꿀 때는 켜 둔 줄에 커서를 두고 **Ctrl+/**(macOS **⌘+/**)로 주석으로 만들고, 볼 줄에서 다시 **Ctrl+/** 로 주석을 푼다. 저장 → 새로고침한다. 한 번에 한 줄만 켠다.

**예상 결과** — 화면에 `입학 연도` 칸(`2023`이 적혀 있다), **눌러 보기** 버튼, `결과 자리 — 버튼을 누르면 바뀐다`가 보인다. Console은 아직 비어 있다. ex01·ex02는 버튼을 눌러야 찍힌다.

ex03부터는 그 예제의 `.html`을 연다. ex04·ex05는 HTML만으로 보는 예제라 Console에 찍히는 것이 없다. 화면과 **Elements** 탭(6주차)에서 본다.

- 이번 주 2일차에는 키보드 **Tab** 키(ex06)를 처음 쓴다. ex07·ex08은 9주차처럼 VS Code 미리 보기(**Ctrl+K** 다음 **V**)로 본다. DevTools는 지금까지 쓴 Console·Elements·기기 모드(4주차)만 쓴다.

### 4. 값 바꾸는 요령

실험은 늘 같은 순서다. **VS Code에서 고치고 저장**(Ctrl+S, macOS는 ⌘+S) → **브라우저에서 새로고침**(F5, macOS는 ⌘+R) → **화면·Console·Elements**를 본다.
바꾸기 전에 무엇이 달라질지 먼저 말해 보고 확인한다.

**눌러 보기** — `ex/index.html`(ex01 줄만 켬)에서 칸에 `2023`이 적힌 채로 **눌러 보기**를 누른다. 이어서 칸을 `이천이십삼`으로 바꾸고 한 번 더 누른다.

**예상 결과** — Console에 세 줄씩 두 번 찍힌다.

```text
1. 글자 + 1 : 20231               ex01_number.js:10
2. Number(글자) + 1 : 2024        ex01_number.js:13
3. isNaN(바꾼 값) : false         ex01_number.js:15
1. 글자 + 1 : 이천이십삼1          ex01_number.js:10
2. Number(글자) + 1 : NaN         ex01_number.js:13
3. isNaN(바꾼 값) : true          ex01_number.js:15
```

화면의 결과 자리는 `숫자로 바꾼 값: 2023` → `숫자로 바꾼 값: NaN`으로 바뀐다. 입력 칸의 값은 숫자를 적어도 글자라서 1번은 뒤에 `1`이 이어 붙는다. `Number()`로 바꿔야 2번처럼 더해진다.

- 값을 원래대로 못 돌리겠으면 교재에서 그 파일을 다시 **Raw**로 받아 덮어쓴다.
- 파일마다 무엇을 바꿔 볼지는 [1일차 실습](lab.md#1일차--숫자와-글자-그리고-접근성-60분)에 있다.

### 5. 이번 주 저장소 만들어 올리기

1일차 50–60분에 한다. 다섯 예제에서 각각 값 하나 이상을 바꿔 봤으면 올린다.

GitHub에서 **New repository**를 누르고 이름 `web-week13`, **Public**으로 만든다. README는 추가하지 않는다.
터미널에서 2주차에 배운 순서 그대로 친다. 현재 폴더: `web-week13`

```bash
git init
git add .
git commit -m "13주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week13.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save**를 누른다.

**예상 결과** — GitHub 저장소 화면을 새로고침하면 `data/`·`ex/`·`images/`·`screenshots/`와 맨 위 파일들이 보이고, 파일 목록 아래에 지난주 `README.md`가 문서로 보인다.
1~3분 뒤 `https://student01.github.io/web-week13/ex/`를 연다. 고르기 페이지의 제목과 "예제가 쓰는 자리"가 보인다. 이 화면은 **확인용**이다.
공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 404가 나면 주소의 `web-week13/ex/`가 저장소·폴더 이름과 글자 단위로 같은지, Pages를 켰는지 본다.
- push가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../week02_github_pages/lab.md#막혔을-때)를 본다.

## 2일차

### 6. 폴더 열고 2일차 예제 가져오기

같은 PC에 `web-week13` 폴더가 남아 있으면 VS Code로 그대로 연다. 없으면 받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week13.git
```

내려받은 `web-week13`을 **File › Open Folder**로 연다.

오늘 예제는 세 개다. ex06은 `.html` 하나, ex07·ex08은 README와 같은 마크다운 `.md` 파일이다. [교재 저장소 examples/day2 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security/examples/day2)에서 1일차와 같은 **Raw** → 저장으로 `web-week13/ex/`에 넣는다. ex08이 쓰는 그림은 1일차에 받은 `ex/images/profile.png`다. 다시 받지 않는다.

| 파일 | 비교하는 것 |
|---|---|
| [ex06_link_text.html](examples/day2/ex06_link_text.html) | 같은 글자 링크 셋 / 목적지를 적은 링크 셋 / 기호 버튼과 글자 버튼 |
| [ex07_line_marks.md](examples/day2/ex07_line_marks.md) | `#` 제목 / `-` 목록 / 기호 없이 줄만 바꿈 / 기호 뒤 띄어쓰기 없음 |
| [ex08_link_image.md](examples/day2/ex08_link_image.md) | 링크 / 그림 / `!`를 뺀 그림 줄 / 대소문자가 다른 경로 |

`.md` 파일은 VS Code에서 열고 **Ctrl+K**를 누르고 손을 뗀 뒤 **V**(macOS **⌘+K** 다음 **V**)를 누른다. 9주차와 같은 미리 보기다. 편집기 오른쪽 위의 미리 보기 아이콘(**Open Preview to the Side**)을 눌러도 된다. 왼쪽에 글자, 오른쪽에 모양이 나란히 보인다. 왼쪽을 고치면 오른쪽이 바로 바뀐다.

**예상 결과** — `ex/`에 1일차 일곱 개와 오늘 세 개, `images/profile.png`가 있다.
`ex/ex06_link_text.html`을 열고 맨 위 제목 글자를 한 번 누른 뒤 **Tab**을 누르면 첫 링크 `페이지 열기`에 테두리가 생긴다. Tab을 누를 때마다 다음 링크·버튼으로 옮겨 간다.
`ex/ex08_link_image.md`의 미리 보기에서는 2번에 프로필 그림이 보이고, 3번은 파란 링크 글자로 보인다.

- ex07·ex08 맨 위의 `<!-- … -->` 두 줄은 주석이라 미리 보기에 나오지 않는다.
- 파일마다 무엇을 바꿔 볼지는 [2일차 실습](lab.md#2일차--readme-와-점검-그리고-조립-60분)에 있다.

### 7. 조립표

17분부터 조립한다. 이제 `ex/`가 아니라 `web-week13` 맨 위의 파일을 연다.
조립하는 줄은 모두 비교 예제와 12주차 완성본에서 본 것이다.
8단계(`about.html`)부터 15단계(`README.md`)까지 차례대로 한다. 45분이 되었는데 README가 남았으면 남은 절은 두고 16단계 점검과 17단계 push·캡처를 먼저 한다. README는 14주차 레포트로 보며 이번 주 채점 대상이 아니다.

| 조립할 줄 | 출처 |
|---|---|
| `about.html`의 `<script src="about.js" defer></script>` | 12주차 `guestbook.html`의 script 줄과 같은 모양 |
| `about.html`의 `<form id="year-form">`·`<label for="year">`·`<input id="year">`·`<button type="submit">계산하기</button>` | [ex05](examples/day1/ex05_label.html) 1번 `for`=`id`, [ex06](examples/day2/ex06_link_text.html) 3번 버튼 글자, 12주차 `guestbook.html`의 폼 |
| `about.html`의 `<div class="card" id="year-result">` | [ex01](examples/day1/ex01_number.js)·[ex02](examples/day1/ex02_year.js)의 결과 자리 |
| `about.js`의 제출 리스너·`preventDefault`·`trim`·`focus`·`return` | 12주차 `guestbook.js`의 폼(7주차) |
| `const year = Number(text);` · `isNaN(year)` | [ex01](examples/day1/ex01_number.js) 2·3번 |
| `const thisYear = new Date().getFullYear();` · `thisYear - year + 1` · 결과 문장 | [ex02](examples/day1/ex02_year.js) 1·3번과 화면 문장 |
| `projects.js`의 `` link.textContent = `${projects[i].title} 열기`; `` | [ex06](examples/day2/ex06_link_text.html) 2번 |
| `README.md`의 `#`·`##`·`- ` | [ex07](examples/day2/ex07_line_marks.md) 1·2번 |
| `README.md`의 링크와 그림 줄 | [ex08](examples/day2/ex08_link_image.md) 1·2·4번 |

옮겨 적을 때 출처 ex 파일을 옆에 열어 두고, 같은 줄이 거기서 무엇을 했는지 떠올린다.

### 8. about.html에 script 줄과 입학 연도 폼 넣기

`web-week13/about.html`을 연다. `about.html`에 자기 `.js`를 붙이는 것은 이번이 처음이다.

1. `<head>`의 `<link rel="stylesheet" href="styles.css">` **바로 아래**에 한 줄을 넣는다.

```html
    <script src="about.js" defer></script>
```

2. `</table>` **바로 아래**에 아홉 줄을 넣는다.

```html
      <h2>몇 년차일까요?</h2>
      <form id="year-form">
        <p>
          <label for="year">입학 연도</label>
          <input id="year" type="text">
          <button type="submit">계산하기</button>
        </p>
      </form>
      <div class="card" id="year-result">입학 연도를 적고 계산하기를 누르세요.</div>
```

- `id`는 세 개다. 폼 `year-form`, 입력 칸 `year`, 결과 자리 `year-result`. `about.js`가 이 이름으로 찾는다.
- `label for="year"`와 `input id="year"`는 글자까지 같아야 한다(ex05 1번). 이름표 글자를 눌러 커서가 칸으로 가면 이어진 것이다.
- 폼 한 줄을 `<p>`로 묶은 것은 `guestbook.html`의 폼 줄과 같은 모양이다. `<div>`로 묶어도 동작은 같고, 아래 결과 카드와의 간격만 조금 좁아진다.
- 버튼 글자는 누르면 하는 일 `계산하기`다(ex06 3번). `type="submit"`이라 누르면 폼이 제출된다(7주차).

**예상 결과** — 저장하고 `about.html`을 새로고침하면 표 아래에 `몇 년차일까요?`, **입학 연도** 칸과 **계산하기** 버튼, `입학 연도를 적고 계산하기를 누르세요.`가 적힌 흰 카드가 보인다. 아직 `about.js`가 없으므로 Console에 그 파일을 못 찾았다는 빨간 줄이 하나 있다. 9단계에서 파일을 만들면 사라진다. 서버로 열었으면 `favicon.ico` 404 줄이 하나 더 보일 수 있다. 탭 아이콘 요청이라 세지 않는다.

### 9. about.js 새로 만들기

`web-week13` 맨 위에 새 파일 `about.js`를 만든다. 순서는 12주차 `guestbook.js`의 제출 리스너와 같다.

1. 찾아 두기 세 줄 — `#year-form`·`#year`·`#year-result`를 `querySelector`로 찾아 `const`에 담는다.
2. 제출 리스너 — `yearForm.addEventListener('submit', function (event) { … });` 첫 줄은 `event.preventDefault();`.
3. 글자 읽기 — `const text = yearInput.value.trim();`
4. 숫자로 바꾸기 — `const year = Number(text);`(ex01 2번).
5. 거르기 — `if (text === '' || isNaN(year)) { … }` 안에서 안내 문장을 쓰고, 칸에 커서를 두고, `return;`(ex01 3번과 빈칸 바꿔 보기).
6. 계산 — `const thisYear = new Date().getFullYear();`, `const years = thisYear - year + 1;`(ex02 1·3번).
7. 화면에 쓰기 — ex02 화면 문장과 같은 템플릿 문자열을 `yearResult.textContent`에 넣고 칸에 커서를 둔다.

**예상 결과** — 저장하고 `about.html`을 새로고침한다. 칸에 `2023`을 적고 **계산하기**를 누르면 카드가 `2023년에 입학했으니 올해 4년차입니다.`로 바뀐다(2026년일 때). `이천이십삼`을 적거나 칸을 비우고 누르면 `입학 연도를 숫자로 적어 주세요.`가 보이고 커서가 칸으로 돌아간다. 화면이 깜빡이지 않고 Console에 빨간 줄이 없다. 서버로 열었으면 `favicon.ico` 404 한 줄은 보여도 된다(탭 아이콘 요청).

### 10. projects.js 링크 글자 한 줄 바꾸기

`web-week13/projects.js` 19행 `link.textContent = '페이지 열기';`를 아래 한 줄로 바꾼다.

```js
    link.textContent = `${projects[i].title} 열기`;
```

- 카드 제목(`projects[i].title`)을 링크 글자에 넣었다. 링크 글자만 읽어도 어디로 가는지 알 수 있다(ex06 2번).
- 작은따옴표가 아니라 백틱(`` ` ``)이다. 5주차 템플릿 문자열이다.

**예상 결과** — 터미널에서 `node server.mjs`를 실행하고 `http://localhost:8000/projects.html`을 연다. 카드 세 장의 링크 글자가 `자기소개 페이지 열기`·`내 정보 표 열기`·`방명록 열기`로 서로 다르다. **Tab**으로 옮겨 다니며 읽어도 셋이 구분된다.

### 11. about.html 전문

8단계까지 마친 `about.html` 전체다. 내 파일과 한 줄씩 비교한다. 12주차 파일에서 늘어난 것은 8단계의 열 줄뿐이다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
    <link rel="stylesheet" href="styles.css">
    <script src="about.js" defer></script>
  </head>
  <body>
    <header>
      <h1>내 정보</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
        <a href="projects.html">프로젝트</a>
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
      <h2>몇 년차일까요?</h2>
      <form id="year-form">
        <p>
          <label for="year">입학 연도</label>
          <input id="year" type="text">
          <button type="submit">계산하기</button>
        </p>
      </form>
      <div class="card" id="year-result">입학 연도를 적고 계산하기를 누르세요.</div>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

같은 파일이 [examples/day2/web-week13/about.html](examples/day2/web-week13/about.html)에 있다.

### 12. about.js 전문

9단계에서 만든 `about.js` 전체다. 글자 단위로 같아야 한다.

```js
const yearForm = document.querySelector('#year-form');
const yearInput = document.querySelector('#year');
const yearResult = document.querySelector('#year-result');

yearForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const text = yearInput.value.trim();
  const year = Number(text);
  if (text === '' || isNaN(year)) {
    yearResult.textContent = '입학 연도를 숫자로 적어 주세요.';
    yearInput.focus();
    return;
  }
  const thisYear = new Date().getFullYear();
  const years = thisYear - year + 1;
  yearResult.textContent = `${year}년에 입학했으니 올해 ${years}년차입니다.`;
  yearInput.focus();
});
```

같은 파일이 [examples/day2/web-week13/about.js](examples/day2/web-week13/about.js)에 있다.

- 1~3행은 찾은 요소를 `const`에 담아 둔다. 12주차 `guestbook.js` 1~7행과 같은 모양이다.
- 8행 `Number(text)`는 글자를 숫자로 바꾼다. 못 바꾸면 `NaN`이다(ex01).
- 9행은 빈칸이거나 숫자가 아니면 안내하고 12행 `return`으로 멈춘다. 빈칸은 `Number()`가 `0`으로 바꾸기 때문에 `text === ''`도 함께 묻는다(ex01 셋째 바꿔 보기).
- 14~15행은 ex02 1·3번이다. 올해를 `2026`이라고 직접 적지 않는다.
- 10·16행 모두 `textContent`로 쓴다. 입력한 글이 섞인 문장은 글자로 넣는다(ex03).

### 13. projects.js 전문

12주차 파일에서 바뀐 것은 19행 하나뿐이다.

```js
const projectList = document.querySelector('#project-list');
const notice = document.querySelector('#notice');

function showProjects(projects) {
  projectList.innerHTML = '';
  for (let i = 0; i < projects.length; i++) {
    const article = document.createElement('article');
    article.classList.add('card');
    const image = document.createElement('img');
    image.src = projects[i].image;
    image.alt = `${projects[i].title} 화면 그림`;
    image.width = 240;
    const title = document.createElement('h3');
    title.textContent = projects[i].title;
    const description = document.createElement('p');
    description.textContent = projects[i].description;
    const link = document.createElement('a');
    link.href = projects[i].link;
    link.textContent = `${projects[i].title} 열기`;
    article.append(image, title, description, link);
    projectList.append(article);
  }
}

async function loadProjects() {
  try {
    const response = await fetch('data/projects.json');
    if (!response.ok) {
      notice.textContent = '프로젝트를 불러오지 못했습니다.';
      return;
    }
    const projects = await response.json();
    notice.textContent = '';
    showProjects(projects);
  } catch (error) {
    notice.textContent = '프로젝트를 불러오지 못했습니다.';
  }
}

loadProjects();
```

같은 파일이 [examples/day2/web-week13/projects.js](examples/day2/web-week13/projects.js)에 있다.

- 5행 `projectList.innerHTML = '';`는 카드를 다시 그리기 전에 비우는 줄이다. 입력한 글이 들어가지 않으므로 그대로 둔다(ex03 3번).
- 11행 `image.alt`는 12주차에 이미 카드 제목을 넣어 두었다(ex04 1번).

### 14. 화면 캡처 세 장 넣기

`node server.mjs`로 띄운 `http://localhost:8000/`에서 세 화면을 찍어 `screenshots/` 폴더에 넣는다. 지난주 완성본의 두 장은 9주차에 찍은 화면이라 지금 페이지와 다르다. 새로 찍어 덮어쓰고 `projects.png`를 더한다.

| 파일 | 찍을 화면 |
|---|---|
| `screenshots/home.png` | `index.html` — 인사말과 클릭 횟수, 소개 |
| `screenshots/guestbook.png` | `guestbook.html` — 한 줄 이상 남긴 목록 |
| `screenshots/projects.png` | `projects.html` — 카드 세 장 |

캡처 도구는 Windows **Win+Shift+S**(찍은 뒤 화면 구석에 뜨는 알림을 눌러 **저장**), macOS **⌘+Shift+4**(바탕화면에 저장된다)다. 저장한 그림을 `web-week13/screenshots/` 로 옮기고, 이름을 위 표와 **글자 하나까지 같게** 바꾼다.

**예상 결과** — VS Code 탐색기의 `screenshots/` 안에 `guestbook.png`·`home.png`·`projects.png` 세 파일이 있다.

- 파일 이름은 소문자로 두고 한글·공백을 쓰지 않는다. `Home.png`로 저장하면 GitHub에서 그림이 깨진다(ex08 4번).
- 캡처에 실명·학번·전화번호·실제 이메일이 보이지 않게 한다. 방명록에는 `student02` 같은 예시 이름으로 남긴다.

### 15. README.md 최종판 쓰기

`web-week13/README.md`를 열고 **Open Preview to the Side**를 켠다. 지난주 README를 아래 일곱 절로 다시 쓴다. 이 README가 그대로 14주차 레포트가 된다.

```text
# 사이트 이름 한 줄            제목. # 하나. 바로 아래에 사이트를 소개하는 문장 한 줄
## 공개 주소                   https://student01.github.io/web-week13/ 링크 한 줄
## 페이지                      네 페이지를 링크 목록으로 네 줄
## 기능                        다섯 줄
## 화면                        screenshots/ 그림 세 장
## 사용 기술                   세 줄 안팎
## 어려움과 해결               세 줄
## 만든 과정                   9주차부터 주차마다 한 줄씩, 다섯 줄 이상
```

쓰는 기호는 네 가지뿐이다. 모두 ex07·ex08에서 본 모양이다.

```text
## 화면                                       절 제목. ## 다음에 띄어쓰기 한 칸 (ex07 1번)
- 방명록에 글을 남기면 목록에 쌓입니다.          목록 한 줄. - 다음에 띄어쓰기 한 칸 (ex07 2번)
[공개 주소](https://student01.github.io/web-week13/)     링크. 대괄호에 보이는 글, 소괄호에 주소 (ex08 1번)
![홈 화면](screenshots/home.png)              그림. 링크 앞에 ! (ex08 2번)
```

예시 전문은 [examples/day2/web-week13/README.md](examples/day2/web-week13/README.md)에 있다. 문장은 본인 사이트에 맞게 쓰고, 예시의 `student01`은 본인 아이디로 바꾼다.

- 소개 한 줄은 제목 바로 아래에 둔다. 예시에서는 `웹프로그래밍 수업에서 한 주씩 늘려 만든 자기소개 사이트입니다.`가 그 줄이다.
- `## 만든 과정`에는 9주차부터 이번 주까지 **주차마다 한 줄**씩, 그 주 실습에서 한 일을 떠올려 `- `를 붙여 쓴다(예: `- 12주차: projects.json 을 불러와 프로젝트 카드 그리기`). 9주차 줄을 맨 위에 두고 주차 순서대로 적는다. **다섯 줄 이상**이어야 한다. 14주차 레포트는 이 줄 수를 본다.
- `## 어려움과 해결`은 세 줄로 쓴다. 이번 학기에 실제로 막혔던 것과 푼 방법이다.
- 그림 줄의 소괄호에는 `screenshots/home.png`처럼 README가 있는 곳부터의 경로를 적는다. 대괄호 글자는 그림이 안 보일 때 대신 읽히는 글이다(ex04의 `alt`).
- 줄을 바꿔도 미리 보기에서 한 줄로 붙으면 그 줄 앞에 `- `를 붙이거나 줄 사이에 빈 줄을 넣는다(ex07 3번).

**예상 결과** — 미리 보기에서 큰 제목 하나와 소개 한 줄, 절 제목 일곱 개, 목록, 파란 링크, 그림 세 장이 보인다. 그림 자리에 깨진 표시나 파란 글자가 없다. `## 만든 과정` 아래 목록이 다섯 줄 이상이다.

### 16. 링크 → Console → 375 점검(+ alt·이름표·개인정보)

순서를 바꾸지 않고 한 번씩 한다. 현재 폴더: `web-week13`

```bash
node server.mjs
```

1. `http://localhost:8000/`에서 nav 링크 네 개를 모두 눌러 본다. `projects.html`에서는 카드 링크 세 개도 누른다. 404가 없어야 한다.
2. 각 페이지에서 **F12 › Console**에 빨간 줄이 없는지 본다. `about.html`은 `2023`으로 한 번, 빈칸으로 한 번 **계산하기**를 누른 뒤에도 본다.
3. 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)를 켜고 폭 **375**에서 네 페이지를 본다. 이어서 폭 **1280**으로 바꿔 한 번 더 본다.
4. 그림마다 **F12 › Elements**에서 `alt`를 읽는다(ex04): 홈 프로필 그림, 프로젝트 카드 그림 셋. 입력 칸마다 이름표 글자를 눌러 커서가 칸으로 가는지 본다(ex05): 방명록 이름·이메일·메시지 칸, 내 정보 입학 연도 칸.
5. `README.md`·`about.html`·`screenshots/` 세 장에 실명·학번·전화번호·실제 이메일·비밀번호가 없는지 본다.

**예상 결과** — 네 페이지가 모두 열리고, 빨간 줄이 없고(`favicon.ico` 404 한 줄은 세지 않는다), 375에서 nav가 세로로 서며(4주차 `@media`) 오른쪽이 잘리거나 옆으로 밀리는 곳이 없다. 1280에서는 nav가 가로로 선다. `about.html`의 입력 칸과 **계산하기** 버튼은 한 줄에 다 들어가지 않으면 다음 줄로 내려간다. 그림 넷 모두 `alt`가 있고, 이름표 넷을 누르면 커서가 그 칸으로 간다.
확인이 끝나면 터미널에서 **Ctrl+C**로 서버를 멈춘다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.

- 404는 주소창의 파일 이름과 실제 파일 이름의 철자·대소문자를 맞춘다. 내 PC 서버는 파일 이름의 대소문자가 달라도 열어 준다(Windows·macOS). 그래서 17단계에서 공개 주소로 링크를 한 번 더 누른다.
- `styles.css`는 이번 주에 고치지 않는다. 375에서 깨지는 곳이 있으면 먼저 강의자에게 보여 준다.

### 17. push와 캡처

현재 폴더: `web-week13`

```bash
git add .
git commit -m "13주차 2일차"
git push
```

GitHub 저장소 화면 `https://github.com/student01/web-week13`을 새로고침한다.

**예상 결과** — 파일 목록 아래에 README 최종판이 문서로 보이고 그림 세 장이 나온다. `ex/ex08_link_image.md`를 눌러 열면 2번 그림은 보이고 4번(대소문자가 다른 경로)만 깨져 있다.

1~3분 뒤 공개 주소 `https://student01.github.io/web-week13/`를 열고 nav 링크 네 개와 프로젝트 카드 링크 세 개를 한 번 더 누른다. 내 PC 서버는 파일 이름의 대소문자가 달라도 열어 주므로, 대소문자 실수는 공개 주소에서만 404로 보인다.

**예상 결과** — 네 페이지와 카드 링크 세 개가 모두 열린다. 404가 나면 그 링크의 `href`(주소창 끝의 파일 이름)와 저장소의 파일 이름을 대소문자까지 맞추고 다시 push한다.

이어서 공개 주소 `https://student01.github.io/web-week13/guestbook.html`을 열고 **F12 › 기기 모드 375**로 바꾼다. 목록이 비어 있으면 이름 `student02`, 메시지 `<b>안녕</b>`으로 한 줄을 남긴다.

**예상 결과** — 목록에 `student02: <b>안녕</b> (남긴 날짜)`가 굵은 글씨가 아니라 **글자 그대로** 보이고, Console에 빨간 줄이 없다(`favicon.ico` 404 한 줄은 세지 않는다). 주소창이 함께 보이게 캡처한다. 이 캡처 한 장이 제출이다.
공용 PC라면 자격 증명을 지우고 나간다.

- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 지난주에 남긴 글이 목록에 보이면 같은 공개 주소(`student01.github.io`)가 저장 칸을 함께 쓰기 때문이다. **전체 지우기**로 비우고 다시 남긴다.
- 막히면 [실습지의 막혔을 때](lab.md#막혔을-때)를 본다.
