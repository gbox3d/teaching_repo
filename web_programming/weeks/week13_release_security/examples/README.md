[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

# 13주차 예제 — 비교 예제 8개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   index.html      고르기 페이지 — 맨 아래 script 줄 하나만 켠다
          ex01 · ex02     Number·isNaN, 올해와 몇 년차 (.js 파일)
          ex03            textContent 와 innerHTML (.html + .js 한 쌍)
          ex04 · ex05     alt, label for (.html 하나)
          images/         ex04 가 쓰는 그림 profile.png
  day2/   ex06            링크·버튼 글자 (.html 하나)
          ex07 · ex08     마크다운 # 과 -, 링크와 그림 (.md 파일)
          images/         ex08 이 쓰는 그림 profile.png (1일차와 같은 그림)
          web-week13/     2일차 끝의 web-week13 — 비교 예제에서 본 줄을 모은 조립
```

`exNN_*` 파일은 **파일 하나 = 개념 하나**다. 같은 일을 다르게 한 **형제**(1·2·3번)를 나란히 놓는다.
결과는 화면과 **F12 › Console**·**Elements** 에서 본다. `.md` 파일은 VS Code 에서 열고 미리 보기를 옆에 띄워(**Ctrl+K** 다음 **V**, macOS **⌘+K** 다음 **V**. 9주차와 같다) 왼쪽 글자와 오른쪽 모양을 비교한다. 값이나 줄을 바꾸고 저장 → 새로고침(미리 보기는 바로 바뀐다)으로 무엇이 달라지는지 본다.
**다른 파일의 개념은 섞지 않는다.** 고르기 페이지와 ex03 의 입력 칸 이름표(`label for`)는 3주차 폼에서 쓴 모양이다. 이름표가 칸에 이어지는지는 ex05 에서 따로 본다. 그래서 두 파일의 이름표 줄에는 그 뜻의 주석만 붙였다.
만들기는 마지막 하나, [`day2/web-week13/`](day2/web-week13/) 뿐이다.

1일차 ex01·ex02 는 같은 화면(입력 칸 하나, 버튼 하나, 결과 자리 하나)을 쓴다. 그래서 코드를 `.js` 파일로 떼어 두고 고르기 페이지 [day1/index.html](day1/index.html) 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 두 줄 중 **하나만** 주석 밖에 둔다(VS Code 에서 줄에 커서를 두고 **Ctrl+/**, macOS **⌘+/**). 처음에는 ex01 줄만 켜져 있다. 6주차 1일차와 같은 방법이다.
ex03 은 화면이 달라서 `.html` 과 `.js` 를 한 쌍으로 둔다. `.html` 을 연다. 두 파일이 같은 폴더에 있어야 한다. ex04·ex05·ex06 은 JavaScript 없이 HTML 만으로 보는 예제라 `.html` 하나다.
ex04 와 ex08 은 같은 폴더의 `images/profile.png` 를 쓴다. 내 저장소에서는 `ex/images/profile.png` 하나를 두 예제가 함께 쓴다.
내려받아 이번 주 저장소 `web-week13` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 내 저장소에서는 날짜 폴더 없이 `ex/` 한 곳에 모은다. 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 예제

| 파일 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/index.html](day1/index.html) | 제목과 안내 두 줄, "예제가 쓰는 자리"(`입학 연도` 칸에 `2023`, **눌러 보기** 버튼, 결과 자리). Console 은 켜 둔 `script` 줄의 예제 것만, 버튼을 누를 때 찍힌다 | JS 를 파일로 떼어 HTML 이 `<script src>` 로 불러온다. 어느 파일을 불러올지는 `script` 줄 하나로 정해진다 | 켜 둔 줄을 바꿔 가며 새로고침 |
| [day1/ex01_number.js](day1/ex01_number.js) | `2023` 으로 누르면 Console 1번 `20231`, 2번 `2024`, 3번 `false`, 화면 `숫자로 바꾼 값: 2023`. `이천이십삼` 이면 2번 `NaN`, 3번 `true` | 입력 칸의 값은 숫자를 적어도 글자다. `Number()` 로 숫자로 바꾸고, 못 바꾸면 `NaN`(숫자가 아님)이다. `isNaN()` 은 `NaN` 이면 `true` | 칸에 `이천이십삼`·`2023년`·빈칸. 빈칸은 `0` 이 되어 3번이 `false` 다 |
| [day1/ex02_year.js](day1/ex02_year.js) | `2023` 으로 누르면 Console 1번 올해(2026년이면 `2026`), 2번 `3`, 3번 `4`, 화면 `2023년에 입학했으니 올해 4년차입니다.` | `new Date().getFullYear()` 는 버튼을 누른 순간 컴퓨터 시계의 연도다(5주차 ex10). 입학한 해를 1년차로 세려고 1 을 더한다 | 11행을 `const thisYear = 2026;` 으로. 괄호를 뺀 `getFullYear;` → `NaN년차` |
| [day1/ex03_text_html.html](day1/ex03_text_html.html) + [ex03_text_html.js](day1/ex03_text_html.js) | 칸에 `<b>안녕</b>`. 1 → 결과 자리에 `<b>안녕</b>` 이 글자 그대로, 2 → 굵은 `안녕`, 3 → 결과 자리가 빈다. Console 1번 `<b>안녕</b>`, 2번 `안녕`, 3번 `0` | 입력한 글은 `textContent` 로 넣는다. `innerHTML` 은 받은 글을 HTML 로 읽어 태그가 진짜 요소가 된다. 입력한 글이 들어가지 않는 비우기(`innerHTML = ''`)에만 쓴다 | 칸에 `<button>가짜 버튼</button>` → 2 에서 진짜 버튼이 생긴다 |
| [day1/ex04_alt.html](day1/ex04_alt.html) | 같은 프로필 그림 세 장. 눈으로는 같다. Elements 의 `img` 세 줄은 `alt` 가 다르다 | `alt` 는 그림이 안 보일 때 대신 읽히는 글이다. 그림이 무엇인지 적는다. `그림` 한 낱말로는 알 수 없다 | 세 `src` 를 `images/nothing.png` 로 → 그림 자리에 남는 것이 다르다 |
| [day1/ex05_label.html](day1/ex05_label.html) | `입학 연도` 칸 세 줄. 글자를 누르면 1번만 커서가 칸으로 들어간다 | `label` 의 `for` 와 `input` 의 `id` 가 같아야 이어진다. 이어진 이름표는 눌러도 칸으로 간다. 1번과 3번은 눈으로는 같다 | 20행 `years2` 를 `year2` 로. `for="#year1"` |
| [day2/ex06_link_text.html](day2/ex06_link_text.html) | 같은 글자 `페이지 열기` 링크 셋, 목적지를 적은 링크 셋, `▶` 버튼과 `계산하기` 버튼. **Tab** 키를 누르면 링크·버튼에 차례로 테두리가 생긴다 | 링크·버튼 글자는 그것만 읽어도 어디로 가는지·무엇을 하는지 알게 쓴다. 키보드만 쓰는 사람은 Tab 으로 옮겨 다니며 그 글자만 읽는다 | 16행 글자를 `a 설명 열기` 로. **Shift+Tab** |
| [day2/ex07_line_marks.md](day2/ex07_line_marks.md) | 미리 보기에서 1번은 큰 제목과 작은 제목, 2번은 목록 두 줄, 3번은 두 줄이 한 줄로 붙고, 4번은 `#`·`-` 가 글자 그대로 | 줄 맨 앞 기호와 띄어쓰기 한 칸이 그 줄의 모양을 정한다. 기호 없이 줄만 바꾸면 한 줄로 붙는다(9주차 ex01·ex02) | 4행 앞에 `#` 하나 더, 11·12행 사이에 빈 줄 |
| [day2/ex08_link_image.md](day2/ex08_link_image.md) | 미리 보기에서 1번은 파란 링크, 2번은 프로필 그림, 3번은 그림 파일로 가는 파란 링크, 4번은 내 PC 에서는 그림이 보이지만 GitHub 에서는 깨진다 | `[보이는 글](주소)`(9주차 ex03) 앞에 `!` 를 붙이면 그림이다. 대괄호 글자가 그림의 `alt` 다. 경로는 대소문자까지 파일 이름과 같아야 GitHub 에서 보인다 | 10행의 `!` 지우기, 경로를 `images/nothing.png` 로 |

### 파일 안의 모양

형제 번호가 주석 첫머리와 `console.log` 앞 글자에 있다. [ex03_text_html.js](day1/ex03_text_html.js) 에서 인용:

```js
// 1. textContent: 받은 글을 글자 그대로 넣는다. 태그도 글자로 보인다
textButton.addEventListener('click', function () {
    output.textContent = input.value;
    console.log('1. 결과 자리의 글자 :', output.textContent);
});

// 2. innerHTML: 받은 글을 HTML 로 읽어 넣는다. 태그가 진짜 요소가 된다
htmlButton.addEventListener('click', function () {
    output.innerHTML = input.value;
    console.log('2. 결과 자리의 글자 :', output.textContent);
});
```

1번과 2번은 넣는 글과 자리가 똑같다. 다른 것은 `textContent` 와 `innerHTML` 단어 하나다.
`.md` 예제는 Console 이 없으므로 형제 번호를 절 제목이나 줄 첫머리의 `1번`·`2번` 으로 적었다. 마크다운에서 줄 맨 앞의 `1.` 은 번호 목록이 되기 때문이다.

## `day2/web-week13/` — 2일차 끝의 web-week13

[`day2/web-week13/`](day2/web-week13/) 는 2일차 끝의 `web-week13` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 14주차 새 저장소 `web-week14` 의 시작점이다. 비교 예제를 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.
`projects.html` 의 카드는 `fetch` 로 읽으므로 두 번 눌러 연 `file://` 화면에는 나오지 않는다. `node server.mjs` 로 연 주소나 공개 주소에서 본다(12주차와 같다).

| `day2/web-week13/` 파일 | 내 `web-week13` 의 위치 | 따라하기 단계 |
|---|---|---|
| [about.html](day2/web-week13/about.html) | `about.html` | [2일차 8단계](../walkthrough.md#2일차) — `<head>` 에 `about.js` script 줄, 표 아래에 입학 연도 폼과 결과 카드가 늘어난다(ex05·ex06) |
| [about.js](day2/web-week13/about.js) | `about.js` | [2일차 9단계](../walkthrough.md#2일차) — 이번 주에 새로 만드는 파일. 제출 리스너 하나다(ex01·ex02, 12주차 `guestbook.js` 의 폼) |
| [projects.js](day2/web-week13/projects.js) | `projects.js` | [2일차 10단계](../walkthrough.md#2일차) — 19행 링크 글자 한 줄이 카드 제목을 넣은 글자로 바뀐다(ex06) |
| [screenshots/home.png](day2/web-week13/screenshots/home.png) · [guestbook.png](day2/web-week13/screenshots/guestbook.png) · [projects.png](day2/web-week13/screenshots/projects.png) | `screenshots/` 세 장 | [2일차 14단계](../walkthrough.md#2일차) — 지난주 두 장을 새로 찍고 `projects.png` 를 더한다 |
| [README.md](day2/web-week13/README.md) | `README.md` | [2일차 15단계](../walkthrough.md#2일차) — 최종판 일곱 절. 화면 절의 링크 줄이 그림 줄로 바뀐다(ex07·ex08). 공개 주소와 아이디는 본인 것으로 쓴다. `## 만든 과정` 은 9주차부터 주차마다 한 줄씩 다섯 줄이다 |
| [index.html](day2/web-week13/index.html) · [guestbook.html](day2/web-week13/guestbook.html) · [projects.html](day2/web-week13/projects.html) · [app.js](day2/web-week13/app.js) · [guestbook.js](day2/web-week13/guestbook.js) · [styles.css](day2/web-week13/styles.css) · [data/projects.json](day2/web-week13/data/projects.json) · [images/](day2/web-week13/images/) | 같은 이름의 파일 | 12주차 그대로. 이번 주에 점검만 하고 고치지 않는다 |
