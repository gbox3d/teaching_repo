[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

# 13주차 실습 — 값을 바꿔 보고 마지막에 조립하기

이번 주 실습도 코드를 새로 쓰는 것이 아니라 **값을 바꿔 보는 것**이다.
비교 예제 8개를 이번 주 새 저장소 `web-week13` 의 `ex/` 폴더에 저장하고(1일차는 고르기 페이지 `index.html` 과 `.js`·`.html` 여섯 개와 그림 하나, 2일차는 `.html` 하나와 `.md` 둘), 값이나 줄 하나를 바꾼 뒤 결과가 어떻게 달라지는지 본다.
결과는 화면, **F12 › Console**, **F12 › Elements** 에서 보고, `.md` 파일은 VS Code **Open Preview** 에서 본다.
2일차 끝에 그 부품으로 `web-week13` 맨 위의 `about.html`·`about.js`·`projects.js`·`README.md`·`screenshots/` 를 조립한다. 나머지 파일은 지난주 완성본 그대로다. 채점 대상은 2일차 캡처 1장이다.
`student01` 은 예시 아이디이므로 본인 아이디로 바꾼다.

**확인·캡처는 공개 주소에서 한다.** 방명록 글은 주소마다 따로 저장되고(11주차), 프로젝트 카드는 두 번 눌러 연 `file://` 화면에는 나오지 않는다(12주차). 내 PC 에서 볼 때는 `node server.mjs` → `http://localhost:8000/` 로 연다.
파일을 받는 법, 고르기 페이지 쓰는 법은 [따라하기 1일차](walkthrough.md#1일차)에 있다.
"바꿔 보기"는 **무엇이 달라질지 먼저 말해 보고** 저장 → 새로고침으로 확인한다. 확인했으면 원래대로 되돌리고 다음으로 간다.

## 1일차 — 숫자와 글자, 그리고 접근성 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 새 폴더 `web-week13` 을 만들어 VS Code 로 연다(**File › Open Folder**). 지난주 완성본을 넣는다: 내 `web-week12` 저장소 GitHub 화면 › **Code › Download ZIP** → 압축을 풀어 맨 위 파일과 `images/`·`data/`·`screenshots/` 를 넣는다. 못 받으면 교재 [12주차 `examples/day2/web-week12/`](../week12_persistent_crud/examples/day2/web-week12/) 파일을 **Raw** 로 받는다. `ex` 폴더를 만들고 교재 [`examples/day1/`](examples/day1/) 의 일곱 파일과 그림 `images/profile.png` 를 **Raw** 로 저장한다 |
| 5–14분 | ex01 `Number` 와 `isNaN` |
| 14–22분 | ex02 올해와 몇 년차 |
| 22–34분 | ex03 `textContent` 와 `innerHTML` |
| 34–41분 | ex04 `alt` |
| 41–47분 | ex05 `label for` |
| 47–50분 | 확인: 일곱 파일과 `ex/images/profile.png` 가 있고, 각 예제에서 값 하나 이상을 바꿨는지. 일부러 낸 오류와 바꾼 경로는 되돌려 두었는지 |
| 50–60분 | 이번 주 저장소 만들어 올리기: GitHub 에 새 저장소 `web-week13` → [올리기 명령](#이번-주-저장소-만들어-올리기) → **Settings › Pages** → 공개 주소 `https://student01.github.io/web-week13/ex/` 확인 → 공용 PC면 자격 증명 삭제 |

ex01·ex02 는 `ex/index.html` 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 두 줄 중 **지금 문항의 줄 하나만** 주석 밖에 둔다(줄에서 **Ctrl+/**, macOS **⌘+/**). 코드는 각 `.js` 파일에서 고치고, 저장 → `ex/index.html` 새로고침으로 본다. ex03 부터는 그 예제의 `.html` 을 연다.

### 1. ex01 `Number` 와 `isNaN` (`Number()` · `isNaN()`)

[examples/day1/ex01_number.js](examples/day1/ex01_number.js) 를 `ex/ex01_number.js` 로 저장한다. `ex/index.html` 맨 아래에서 `ex01_number.js` 줄만 켠다(처음 받은 상태가 이렇다).

- 바꿔 보기: 칸에 `2023` 이 적힌 채로 **눌러 보기**를 누른다. Console 1번과 2번은 무엇인가? 둘 다 `+ 1` 인데 왜 다른가?
- 바꿔 보기: 칸에 `이천이십삼` 을 적고 누른다. 2번·3번과 화면 글자는? 이어서 `2023년` 은?
- 바꿔 보기: 칸을 **비우고** 누른다. 2번은 무엇이고 3번은 `true` 인가 `false` 인가? 빈칸은 `Number()` 가 숫자 `0` 으로 바꾼다. 그래서 조립할 `about.js` 는 `isNaN` 과 함께 `text === ''` 도 묻는다.
- 흔한 실수: 15행처럼 `isNaN(year)` 로 묻지 않고 `year === NaN` 으로 묻는다. `NaN` 은 자기 자신과도 같지 않아서 이 비교는 늘 `false` 다. Console 에 `NaN === NaN` 을 직접 쳐 본다. 숫자가 아닌지는 `isNaN()` 으로 묻는다.

### 2. ex02 올해와 몇 년차 (`new Date().getFullYear()`)

[examples/day1/ex02_year.js](examples/day1/ex02_year.js) 를 `ex/ex02_year.js` 로 저장한다. `ex/index.html` 맨 아래에서 ex01 줄을 끄고 `ex02_year.js` 줄만 켠다.

- 바꿔 보기: 칸에 `2023` 을 적고 누른다. Console 1·2·3번과 화면 문장은? 2번과 3번은 왜 1 차이가 나나?
- 바꿔 보기: 11행 `const thisYear = new Date().getFullYear();` 를 `const thisYear = 2026;` 으로 바꾼다. 지금은 결과가 같다. 내년에 이 페이지를 열면 어느 쪽이 맞나? 확인했으면 되돌린다.
- 바꿔 보기: 칸에 `이천이십삼` 을 적고 누른다. 화면 문장은? 조립할 `about.js` 가 계산하기 전에 `isNaN` 으로 먼저 거르는 이유다.
- 흔한 실수: `getFullYear` 뒤의 괄호를 빠뜨린다(`new Date().getFullYear;`). 오류는 나지 않는데 1번에 함수 모양의 글자가 찍히고 화면이 `NaN년차` 가 된다. 6주차 ex06 처럼 **부를 때는 괄호**다.

### 3. ex03 `textContent` 와 `innerHTML` (`textContent` · `innerHTML` · `innerHTML = ''`)

[examples/day1/ex03_text_html.html](examples/day1/ex03_text_html.html) 과 [ex03_text_html.js](examples/day1/ex03_text_html.js) 를 `ex/` 에 저장하고 `ex03_text_html.html` 을 연다.

- 바꿔 보기: **1 → 2 → 3** 순서로 누르며 결과 자리와 Console 을 본다. 1번 뒤와 2번 뒤 Console 의 글자는 각각 무엇인가? 2번 뒤에 `<b>` 와 `</b>` 는 어디로 갔나? **F12 › Elements** 에서 `<div id="output">` 를 펼쳐 본다.
- 바꿔 보기: 칸의 글을 `<button>가짜 버튼</button>` 으로 바꾸고 1, 2 를 차례로 누른다. 2 에서는 결과 자리에 무엇이 생기나? 이 글을 다른 사람이 방명록에 남겼다면 어떻게 되나?
- 바꿔 보기: 3 을 누른 뒤 Elements 의 `<div id="output">` 안은 어떤가? 비울 때는 왜 `innerHTML` 을 써도 되나?
- 흔한 실수: 방명록처럼 남이 적는 글을 `innerHTML` 로 넣는다. 지금은 굵은 글씨뿐이어도, 남이 적은 태그가 내 페이지의 진짜 요소가 된다. 입력한 글은 `textContent` 로 넣는다.

### 4. ex04 `alt` (`img alt`)

[examples/day1/ex04_alt.html](examples/day1/ex04_alt.html) 을 `ex/` 에 저장한다. 그림 [examples/day1/images/profile.png](examples/day1/images/profile.png) 는 `ex` 안에 `images` 폴더를 만들어 `ex/images/profile.png` 로 저장한다. `ex04_alt.html` 을 연다.

- 바꿔 보기: 세 그림은 눈으로 보면 같은가? **F12 › Elements** 에서 `img` 세 줄의 `alt` 를 읽는다.
- 바꿔 보기: 13·15·17행의 `src` 를 모두 `images/nothing.png` 로 바꾸고 새로고침한다. 1·2·3번 자리에 각각 무엇이 남나? Console 의 빨간 줄은 무엇을 찾지 못했다고 하나? 확인했으면 되돌린다.
- 바꿔 보기: 3번 `alt="그림"` 을 1번처럼 무슨 그림인지 적은 글로 바꾼다. 그림이 안 보일 때 어느 쪽이 도움이 되나?
- 흔한 실수: `alt` 에 `그림`·`사진`·파일 이름만 적는다. 그림이 안 보이는 사람은 그 글만 듣는다. 무슨 그림인지 적는다.

### 5. ex05 `label for` (`label for` · `id`)

[examples/day1/ex05_label.html](examples/day1/ex05_label.html) 을 `ex/` 에 저장하고 연다.

- 바꿔 보기: 세 줄의 `입학 연도` 글자를 하나씩 누른다. 커서가 옆 칸으로 들어가는 줄은 몇 번인가? 1번과 3번은 눈으로 보면 같은데 무엇이 다른가?
- 바꿔 보기: 20행 `id="years2"` 를 `id="year2"` 로 고치고 새로고침한 뒤 2번 글자를 다시 누른다.
- 바꿔 보기: 24행의 `입학 연도` 를 `<label for="year3">입학 연도</label>` 로 감싸고 다시 누른다.
- 흔한 실수: `for="#year1"` 처럼 `#` 을 붙인다. `for` 에는 `id` 이름만 쓴다. `#` 은 CSS 선택자와 `querySelector` 에서만 붙인다.

### 이번 주 저장소 만들어 올리기

GitHub 에서 **New repository** → 이름 `web-week13`, **Public**, README 는 추가하지 않는다. VS Code 터미널(현재 폴더 `web-week13`)에서 2주차에 배운 순서 그대로 친다.

```bash
git init
git add .
git commit -m "13주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week13.git
git push -u origin main
```

저장소 **Settings › Pages › Branch: main, /(root) › Save** → 1~3분 뒤 `https://student01.github.io/web-week13/ex/` 를 연다. `ex/index.html` 의 화면(제목과 "예제가 쓰는 자리")이 보이면 된 것이다. 공용 PC면 자격 증명을 지우고 나간다.
오늘 올린 것은 확인용이다. 제출은 2일차에 캡처 한 장만 한다.

## 2일차 — README 와 점검, 그리고 조립 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC에 `web-week13` 폴더가 남아 있으면 그대로 연다. 없으면 `git clone https://github.com/student01/web-week13.git` 뒤 **File › Open Folder**. 교재 [`examples/day2/`](examples/day2/) 의 세 파일(`ex06_link_text.html`·`ex07_line_marks.md`·`ex08_link_image.md`)을 **Raw** 로 `ex/` 에 저장한다. 그림은 1일차에 받은 `ex/images/profile.png` 를 그대로 쓴다 |
| 5–9분 | ex06 링크·버튼 글자 |
| 9–13분 | ex07 `#` 과 `-` |
| 13–17분 | ex08 링크와 그림 |
| 17–45분 | 조립(이 순서로): `about.html` 두 군데 → `about.js` 새로 쓰기 → `projects.js` 한 줄 → `screenshots/` 세 장 → `README.md` 최종판 |
| 45–55분 | 점검: `node server.mjs` → `http://localhost:8000/` 에서 링크 → Console → 375 순서. 이어서 그림 `alt`·이름표, 저장소에 개인정보가 없는지 |
| 55–60분 | 끝 루틴: `git add .` → `git commit -m "13주차 2일차"` → `git push` → 저장소 첫 화면에서 README 와 그림 세 장 확인 → 공개 주소에서 nav 네 개·카드 링크 세 개 다시 누르기 → 공개 주소 방명록을 기기 모드 375 로 열어 **캡처 1장** → 공용 PC면 자격 증명 삭제 |

ex06 은 `.html` 을 연다. ex07·ex08 은 VS Code 에서 `.md` 파일을 열고 **Ctrl+K** 다음 **V**(macOS **⌘+K** 다음 **V**, Open Preview to the Side)로 왼쪽 글자와 오른쪽 모양을 나란히 본다. 9주차에 README 1차판을 쓸 때와 같은 미리 보기다.
파일마다 **바꿔 보기를 하나 이상** 하고 넘어간다. 17분이 되면 남은 것은 두고 조립을 시작한다. 남은 바꿔 보기는 캡처까지 끝낸 뒤 한다.
조립은 시간표의 순서대로 한다. 45분이 되었는데 README 가 남았으면 남은 절은 두고 점검과 끝 루틴(제출 캡처)을 먼저 한다. README 는 14주차 레포트로 보며 이번 주 채점 대상이 아니다. 남은 절은 14주차 발표 전까지 채운다.

### 6. ex06 링크·버튼 글자 (**Tab** 키)

[examples/day2/ex06_link_text.html](examples/day2/ex06_link_text.html) 을 `ex/` 에 저장하고 연다.

- 바꿔 보기: 맨 위 제목 글자를 한 번 누르고 **Tab** 키를 한 번씩 누른다. 테두리가 생긴 것의 글자만 소리 내어 읽는다. 1번 세 링크는 각각 어디로 가는지 알 수 있나? 2번은?
- 바꿔 보기: **Shift+Tab** 을 누르면 테두리가 어느 쪽으로 가나? 키보드만 쓰는 사람은 이렇게 페이지를 옮겨 다닌다.
- 바꿔 보기: 16행 셋째 링크의 글자 `페이지 열기` 를 `a 설명 열기` 로 바꾸고 Tab 으로 다시 읽는다.
- 흔한 실수: 링크 글자를 `여기`·`클릭`·`페이지 열기` 로 쓴다. 12주차 카드 세 장의 링크가 모두 `페이지 열기` 였다. 오늘 조립에서 고친다.

### 7. ex07 `#` 과 `-` (마크다운 줄 맨 앞 기호)

[examples/day2/ex07_line_marks.md](examples/day2/ex07_line_marks.md) 를 `ex/ex07_line_marks.md` 로 저장한다. VS Code 에서 열고 미리 보기를 옆에 띄운다. 9주차 ex01·ex02 에서 본 `#`·`-` 를 README 최종판 전에 다시 본다.

- 바꿔 보기: 4행 `# 1번 큰 제목` 앞에 `#` 을 하나 더 붙인다. 미리 보기의 글자 크기는 어느 줄과 같아지나?
- 바꿔 보기: 11행과 12행 사이에 빈 줄을 하나 넣는다. 미리 보기에서 두 줄로 나뉘나? 빈 줄을 지우고 두 줄 앞에 `- ` 를 붙이면?
- 바꿔 보기: 14행과 16행의 기호 뒤에 띄어쓰기를 한 칸 넣는다.
- 흔한 실수: `#제목` 처럼 기호 뒤 띄어쓰기를 빠뜨린다. 미리 보기에서 `#` 이 글자 그대로 보인다.

### 8. ex08 링크와 그림 (`[보이는 글](주소)` · `!`)

[examples/day2/ex08_link_image.md](examples/day2/ex08_link_image.md) 를 `ex/ex08_link_image.md` 로 저장한다. 그림은 1일차의 `ex/images/profile.png` 를 쓴다. VS Code 에서 열고 미리 보기를 옆에 띄운다. 1번 링크는 9주차 ex03 에서 본 모양이고, 이번에 새로 보는 것은 링크 앞의 `!`(2·3번)와 경로의 대소문자(4번)다.

- 바꿔 보기: 10행 맨 앞의 `!` 를 지운다. 미리 보기의 그림이 무엇으로 바뀌나? 14행과 같아졌나? 확인했으면 되살린다.
- 바꿔 보기: 10행의 경로를 `images/nothing.png` 로 바꾼다. 그림 자리에 무엇이 보이나? 대괄호 글자는 1일차 ex04 의 무엇과 같은 일을 하나? 확인했으면 되돌린다.
- 바꿔 보기: 18행(대소문자가 다른 경로)이 내 PC 미리 보기에서 보이나? 2일차 끝에 push 한 뒤 GitHub 에서 `ex/ex08_link_image.md` 를 열어 4번을 다시 본다.
- 흔한 실수: 그림 파일 이름은 `home.png` 인데 README 에 `Home.png` 로 적는다. Windows·macOS 미리 보기에서는 보이고 GitHub 에 올리면 깨진다. 파일 이름을 소문자로 두고 글자 그대로 옮겨 적는다.

### 9. 조립 — `about.html`·`about.js`·`projects.js`·`screenshots/`·`README.md` (`Number` · `isNaN` · `getFullYear` · `label for` · 링크 글자 · 마크다운)

이제 `ex/` 가 아니라 `web-week13` 맨 위의 파일을 연다. `ex/index.html` 은 1일차 예제 고르기 페이지라서 조립에 쓰지 않는다. 전문과 단계는 [따라하기 2일차](walkthrough.md#2일차)에 있다.

- `about.html` 의 `<head>` 에 `<script src="about.js" defer></script>` 한 줄, 표 아래에 제목·폼·결과 자리 아홉 줄을 넣는다.
- `about.js` 를 새로 만든다. 제출 리스너 하나다. 순서는 12주차 `guestbook.js` 의 폼과 같다.
- `projects.js` 19행 `link.textContent = '페이지 열기';` 를 카드 제목이 들어간 글자로 바꾼다.
- `screenshots/` 에 홈·방명록·프로젝트 화면 세 장을 `home.png`·`guestbook.png`·`projects.png` 로 넣는다(지난주 두 장은 새로 찍어 덮어쓴다).
- `README.md` 를 최종판 일곱 절로 다시 쓴다.

| 조립할 줄 | 어느 ex 에서 본 것 |
|---|---|
| `about.html` 의 `<script src="about.js" defer></script>` | 12주차 완성본 `guestbook.html` 8행과 같은 모양(페이지마다 자기 js 하나) |
| `<h2>몇 년차일까요?</h2>` · `<form id="year-form">` | 12주차 완성본 `about.html` 의 `<h2>`, `guestbook.html` 의 `<form id="guestbook-form">` |
| `<label for="year">입학 연도</label>` · `<input id="year" type="text">` | ex05 1번(`for` 와 `id` 를 같게). 한 줄을 `<p>` 로 묶는 것은 12주차 `guestbook.html` 의 폼 줄과 같다 |
| `<button type="submit">계산하기</button>` | ex06 3번(하는 일을 적은 버튼 글자), 12주차 `guestbook.html` 의 `남기기` 버튼 |
| `<div class="card" id="year-result">입학 연도를 적고 계산하기를 누르세요.</div>` | ex01·ex02 의 결과 자리 `#result`, 4주차 `.card` |
| `const yearForm = …('#year-form');` · `yearInput` · `yearResult` | 12주차 `guestbook.js` 1~7행(찾아서 `const` 에 담기) |
| `yearForm.addEventListener('submit', function (event) { event.preventDefault();` | 12주차 `guestbook.js` 36~37행(7주차 폼) |
| `const text = yearInput.value.trim();` | 12주차 `guestbook.js` 38행 |
| `const year = Number(text);` | ex01 2번 |
| `if (text === '' \|\| isNaN(year)) {` | ex01 3번과 빈칸 바꿔 보기, 12주차 `guestbook.js` 40행의 `\|\|` |
| `yearResult.textContent = '입학 연도를 숫자로 적어 주세요.';` · `yearInput.focus();` · `return;` | 12주차 `guestbook.js` 41~43행, ex03 1번(글자로 넣기) |
| `const thisYear = new Date().getFullYear();` | ex02 1번 |
| `const years = thisYear - year + 1;` | ex02 3번 |
| `` yearResult.textContent = `${year}년에 입학했으니 올해 ${years}년차입니다.`; `` · `yearInput.focus();` | ex02 18행(화면 문장), 12주차 `guestbook.js` 51행 |
| `projects.js` 19행 `` link.textContent = `${projects[i].title} 열기`; `` | ex06 2번(어디로 가는지 적은 링크 글자), 12주차 `projects.js` 의 `projects[i].title` |
| `README.md` 의 `#` 제목과 `##` 절 제목 | ex07 1번 |
| `README.md` 의 `- ` 목록 줄 | ex07 2번 |
| `README.md` 의 링크 `[보이는 글](주소)` | ex08 1번 |
| `README.md` 의 그림 줄 세 개 `![홈 화면](screenshots/home.png)` … | ex08 2번(링크 앞에 `!`), 4번(대소문자까지 같게). 지난주 README 의 `[홈 화면 캡처](…)` 링크 줄이 그림 줄로 바뀐다 |

README 최종판의 절은 일곱이다. 이 README 가 그대로 14주차 레포트가 되므로 14주차 레포트 기준(소개 한 줄, 기능 다섯 줄, 그림 세 장, 어려움과 해결 세 줄, 만든 과정은 9주차부터 주차마다 한 줄씩 다섯 줄 이상)에 맞춰 쓴다.
예시 전문은 [examples/day2/web-week13/README.md](examples/day2/web-week13/README.md) 에 있다. 문장은 본인 사이트에 맞게 쓰고, 예시의 `student01` 은 본인 아이디로 바꾼다.

| 절 | 넣을 것 |
|---|---|
| `# 사이트 이름` | 첫 줄 제목 하나. 그 바로 아래에 사이트가 무엇인지 소개하는 문장 한 줄 |
| `## 공개 주소` | `https://student01.github.io/web-week13/` 링크 한 줄(본인 아이디) |
| `## 페이지` | 네 페이지 링크와 한 줄 설명 |
| `## 기능` | 다섯 줄 |
| `## 화면` | `screenshots/` 그림 세 장 |
| `## 사용 기술` | 세 줄 안팎 |
| `## 어려움과 해결` | 세 줄. 이번 학기에 실제로 막혔던 것과 푼 방법 |
| `## 만든 과정` | 9주차부터 이번 주까지 **주차마다 한 줄**, 다섯 줄 이상. 각 주 실습에서 한 일을 떠올려 `- ` 를 붙여 쓴다. 예: `- 12주차: projects.json 을 불러와 프로젝트 카드 그리기`. 9주차 줄을 맨 위에 두고 주차 순서대로 적는다 |

- 확인: `node server.mjs` → `http://localhost:8000/about.html` 에서 `2023` 을 적고 **계산하기**를 누르면 `2023년에 입학했으니 올해 4년차입니다.`(2026년 기준), `이천이십삼` 이면 `입학 연도를 숫자로 적어 주세요.` 가 보인다. `projects.html` 카드 링크가 `자기소개 페이지 열기`·`내 정보 표 열기`·`방명록 열기` 로 서로 다르다. VS Code 미리 보기에서 README 의 그림 세 장이 보이고 `## 만든 과정` 이 주차마다 한 줄씩 다섯 줄 이상이다.
- 흔한 실수: `about.js` 를 만들고 `about.html` 에 `script` 줄을 넣지 않는다. **계산하기**를 누르면 화면이 깜빡이고 주소창 끝에 `?` 가 붙는다. 폼이 원래 동작대로 보내졌다는 뜻이다(7주차).
- 흔한 실수: 스크린샷을 `Home.png` 처럼 대문자로 저장하고 README 에는 `home.png` 로 적는다. ex08 4번과 같다. GitHub 에서만 깨진다.

### 10. 점검 — 링크 → Console → 375 (+ alt·이름표·개인정보)

순서를 바꾸지 않는다. 링크가 깨진 채로 Console 을 보면 원인이 섞인다. `node server.mjs` → `http://localhost:8000/` 에서 한다.

1. 네 페이지의 nav 링크 네 개와 프로젝트 카드 링크 세 개를 **모두 눌러 본다.** 404 가 없어야 한다.
2. 각 페이지에서 **F12 › Console** 에 빨간 줄이 없는지 본다. `about.html` 은 **계산하기**를 누른 뒤에도 본다. 버튼을 눌러야 나는 빨간 줄도 있다. `favicon.ico` 를 못 찾았다는 404 한 줄은 세지 않는다. 브라우저가 탭 아이콘을 찾으려고 스스로 보낸 요청이다(5주차).
3. 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)로 폭 **375** 에서 네 페이지를 본다. 오른쪽이 잘리거나 가로로 밀리는 곳이 없어야 한다. 폭 **1280** 으로 바꿔 한 번 더 본다.
4. 그림마다 **F12 › Elements** 에서 `alt` 를 읽는다(ex04): 홈 프로필 그림, 프로젝트 카드 그림 셋. 입력 칸마다 이름표 글자를 눌러 커서가 칸으로 가는지 본다(ex05): 방명록 이름·이메일·메시지 칸, 내 정보 입학 연도 칸.
5. `README.md`·`about.html`·`screenshots/` 세 장에 실명·학번·전화번호·실제 이메일·비밀번호가 없는지 본다.

- 내 PC 서버는 파일 이름의 대소문자가 달라도 연다(Windows·macOS). 그래서 push 한 뒤 끝 루틴에서 **공개 주소**의 nav 네 개와 카드 링크 세 개를 한 번 더 누른다.
- 404 는 파일 이름의 철자와 **대소문자**부터 본다. 공개 주소에서는 대소문자가 다르면 404 다.
- 빨간 줄은 끝의 `파일:줄` 부터 읽는다. 대개 `id` 철자이거나 `script` 줄이다.
- 확인이 끝나면 터미널에서 **Ctrl+C** 로 서버를 멈추고 끝 루틴으로 간다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다 |
| push 가 거부되거나 로그인 창이 안 뜬다 | [2주차 막혔을 때](../week02_github_pages/lab.md#막혔을-때) 표를 본다 |
| 화면이 생각과 다른데 이유를 모르겠다 | **Console 을 먼저 연다.** 빨간 줄 오른쪽 `파일:줄` 로 간다. 오류 난 줄 아래는 실행되지 않으므로 그 줄부터 본다 |
| ex01·ex02 를 열었는데 Console 에 아무것도 없다 | 두 예제는 **눌러 보기**를 눌러야 찍힌다. 눌러도 없으면 `ex/index.html` 맨 아래에서 그 문항의 `script` 줄을 켰는지, `.js` 파일이 같은 `ex/` 폴더에 있는지 본다 |
| `Uncaught SyntaxError: Identifier 'yearInput' has already been declared` | 고르기 페이지에서 `script` 줄을 둘 다 켰다. ex01·ex02 가 같은 이름의 `const` 를 만들어서 둘째 파일이 실행되지 않는다. 한 줄만 켠다 |
| ex04 의 그림이 처음부터 안 보이고 깨진 그림 표시와 글자만 있다 | `ex/images/profile.png` 가 없다. `ex` 안에 `images` 폴더를 만들고 그림을 그 이름으로 저장한다. 글자가 보인 것은 `alt` 가 대신 나온 것이다 |
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` (`about.js:5`) | `#year-form` 을 찾지 못했다. `about.html` 의 `<form id="year-form">` 철자와 `about.js` 의 `querySelector('#year-form')` 을 맞춘다. `<script src="about.js" defer>` 에 `defer` 가 있는지도 본다 |
| **계산하기**를 누르자 `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` (`about.js:16`, 빈칸·숫자가 아니면 `about.js:10`) | `#year-result` 를 찾지 못했다. 결과 자리 `<div class="card" id="year-result">` 의 `id` 철자를 본다. 누르기 전에는 빨간 줄이 없다 |
| **계산하기**를 누르면 화면이 깜빡이고 주소창 끝에 `?` 가 붙는다 | `about.html` 에 `<script src="about.js" defer></script>` 줄이 없거나, `about.js` 에서 `event.preventDefault();` 가 빠졌다. Console 에 `about.js:5` 빨간 줄도 있으면 위 `reading 'addEventListener'` 줄처럼 `defer` 와 폼 `id` 를 본다 |
| 숫자를 적었는데 `입학 연도를 숫자로 적어 주세요.` 가 나온다 | `2023년` 처럼 글자가 섞여 있으면 `Number()` 가 `NaN` 을 만든다. 숫자만 적는다 |
| 화면에 `NaN년차` 가 보인다 | 계산 전에 거르는 `if (text === '' \|\| isNaN(year))` 가 빠졌거나, `getFullYear` 뒤 괄호가 빠졌다(ex02 흔한 실수) |
| 이름표를 눌러도 커서가 칸으로 가지 않는다 | `label` 의 `for` 와 `input` 의 `id` 를 글자 하나씩 비교한다. `for` 에 `#` 을 붙이지 않는다(ex05) |
| 방명록 목록에서 `<b>안녕</b>` 이 **굵게** 보인다 | `guestbook.js` 에서 목록 한 줄을 만드는 줄이 `li.innerHTML = …` 이다. `li.textContent = …` 로 되돌린다. `innerHTML` 은 `list.innerHTML = '';` 에만 남긴다(ex03) |
| 카드 링크에 `${projects[i].title} 열기` 가 글자 그대로 보인다 | 템플릿 문자열의 백틱(`` ` ``)을 작은따옴표로 적었다. 오류는 나지 않는다. 따옴표를 백틱으로 바꾼다 |
| 카드 링크 글자가 그대로 `페이지 열기` 다 | `projects.js` 를 저장하지 않았거나 push 전이다. 공개 주소는 Pages 반영 뒤 **Ctrl+F5**(macOS ⌘+Shift+R)로 새로고침한다 |
| 프로젝트 카드가 하나도 안 보인다 | `projects.html` 을 두 번 눌러 `file://` 로 열었다. `node server.mjs` → `http://localhost:8000/projects.html` 이나 공개 주소에서 연다(12주차) |
| 링크를 눌렀더니 **404** 화면이 나온다 | 주소창의 파일 이름을 본다. 철자와 **대소문자**가 저장소의 파일 이름과 같아야 한다. 공개 주소에서는 `About.html` 과 `about.html` 이 다른 파일이다(내 PC 서버는 둘 다 연다 — 아래 줄) |
| 내 PC 서버에서는 열리던 링크가 공개 주소에서만 **404** 다 | 내 PC 서버는 대소문자가 달라도 연다(Windows·macOS). 링크의 `href` 와 저장소의 파일 이름을 대소문자까지 맞추고 다시 push 한다 |
| 저장소 첫 화면의 README 에서 그림만 깨진다 | README 에 적은 경로와 `screenshots/` 안 파일 이름의 대소문자를 맞춘다(ex08 4번). 저장소의 `screenshots` 폴더를 눌러 그림 세 장이 올라갔는지 본다 |
| README 의 그림 자리에 파란 글자 링크가 보인다 | 그 줄 맨 앞의 `!` 가 빠졌다(ex08 3번) |
| README 의 `#`·`-` 가 글자 그대로 보인다 | 기호 다음에 띄어쓰기 한 칸이 빠졌다(ex07 4번) |
| 공개 주소 방명록에 지난주에 남긴 글이 보인다 | 같은 아이디의 공개 주소(`student01.github.io`)는 저장 칸을 함께 쓴다(11주차). **전체 지우기**로 비우고 다시 남긴다 |
| 방명록 목록이 강의자 화면과 다르다 | 정상이다. 방명록은 **내 브라우저, 그 주소**에만 저장된다(11주차) |
| 기기 모드 375 에서 오른쪽이 잘려 보이거나 화면이 옆으로 밀린다 | 폭을 정한 그림(`width`)·표·긴 글자가 원인인지 **Elements** 에서 본다. `styles.css` 는 이번 주에 고치지 않으므로 먼저 강의자에게 보여 준다 |
| 공개 주소 `…/web-week13/ex/` 가 404 다 | ① 폴더 이름이 `ex` 인지 ② 그 안에 `index.html` 이 있는지 ③ 저장소 이름이 `web-week13` 이고 **Settings › Pages** 가 켜져 있는지 본다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

제출 캡처는 **2일차 끝 루틴**(55–60분)에서 찍는다. [따라하기 2일차 마지막 단계](walkthrough.md#2일차)를 본다.
공개 주소 `https://student01.github.io/web-week13/guestbook.html`(본인 아이디)을 **F12 › 기기 모드 375px** 로 열고 다음이 한 화면에 보이게 찍는다.
목록이 비어 있으면 이름 `student02`, 메시지 `<b>안녕</b>` 으로 한 줄을 남긴 뒤 찍는다.

1. 이름 `student02`, 메시지 `<b>안녕</b>` 으로 남긴 한 줄이 **글자 그대로** 보인다
2. **F12 › Console** 에 빨간 줄이 없다(`favicon.ico` 404 한 줄은 세지 않는다)
3. 주소창(공개 주소가 보여야 한다)

완료 기준은 입력한 글이 태그가 아니라 글자로 보이고 Console 이 깨끗한 것이다.
`about.html` 의 `…년차입니다.` 화면과 1일차 push, `ex/` 실험 파일은 확인용이며 따로 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 입학 연도에 올해보다 큰 수(예: `2030`)를 적어 본다. 어떤 문장이 나오나? `입학 연도가 올해보다 늦습니다.` 같은 안내를 하나 더 넣으려면 `about.js` 의 어디에 `if` 를 넣어야 하나?
- ex03 칸에 `<a href="https://developer.mozilla.org/ko/">MDN</a>` 을 적고 1, 2 를 눌러 본다. 2 에서 생긴 것을 눌러 보면? 내 방명록 메시지 칸에 같은 글을 남기면 어떻게 보이나?
- 내 `web-week13` 의 네 페이지를 **Tab** 키로만 옮겨 다녀 본다. 링크·버튼·입력 칸마다 글자만 읽어도 무엇인지 알 수 있나?
- README 에 여덟째 절 `## 앞으로 해 보고 싶은 것` 을 두 줄로 더해 본다. 14주차 발표 마무리에 쓸 수 있다.
- 기기 모드에서 폭을 320 으로 더 줄여 네 페이지를 본다. 가로로 밀리는 페이지가 있나? 있으면 어느 요소 때문인지 Elements 에서 찾아본다. 고치지는 않는다.
- 짝과 14주차 3분 시연을 한 번 해 본다: 공개 주소 → nav 로 페이지 이동 → 다크 모드 → 폼 빈값 안내 → 방명록 추가·삭제 → 새로고침해도 남는 목록 → 프로젝트 카드 → Commits 탭과 README.

추가 과제는 선택 사항이며 채점하지 않는다.
