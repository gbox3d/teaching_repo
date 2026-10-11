[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation)

# 14주차 예제 — 비교 예제 3개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다. 이번 주는 2일차가 발표라서 비교 예제는 1일차 폴더에만 있다.

```text
examples/
  day1/   ex01            순서 목록 — ol 과 ul (.html 하나)
          ex02            로컬 시연은 서버로 — fetch (.html + .js + .json)
          ex03            새로고침해도 남는 것 — localStorage (.html + .js)
  day2/   web-week14/     2일차 끝의 web-week14 — 지난주 완성본에 홈 목록·공개 주소 행·README 를 더한 조립
```

`exNN_*` 파일은 **파일 하나 = 개념 하나**다. 같은 일을 다르게 한 **형제**(1·2번)를 나란히 놓는다.
결과는 화면과 **F12 › Console** 에서 보고, ex02 는 서버를 띄운 터미널에서도 본다. 값이나 여는 방법을 바꾸고 저장 → 새로고침으로 무엇이 달라지는지 본다.
**다른 파일의 개념은 섞지 않는다.** 저장(`localStorage`)은 ex03 의 주제라서 ex02 에는 없다.
만들기는 마지막 하나, [`day2/web-week14/`](day2/web-week14/) 뿐이다.

세 예제는 화면이 서로 달라서 고르기 페이지 없이 파일마다 따로 연다. ex01 은 `.html` 하나다(JavaScript 가 없다). ex02·ex03 은 `.html` 과 `.js` 한 쌍이고, ex02 에는 `.js` 가 읽어 올 `ex02_message.json` 이 하나 더 있다. `.html` 을 연다. 짝 파일이 같은 폴더에 있어야 한다.
내려받아 이번 주 저장소 `web-week14` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 가져오는 방법과 서버로 여는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 예제

| 파일 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/ex01_order_list.html](day1/ex01_order_list.html) | 같은 다섯 줄이 노란 상자(1. `<ol>`)에는 1~5 번호와, 하늘색 상자(2. `<ul>`)에는 점과 함께 보인다 | 번호는 파일에 쓰지 않는다. 브라우저가 `<li>` 의 차례대로 붙인다. 발표 순서처럼 차례가 뜻을 가지면 `<ol>`, 아니면 `<ul>` | 24·25행 맞바꾸기 → 번호는 1·2 그대로이고 글만 자리를 바꾼다. 23·29행 `ol` 을 `ul` 로. 29행 `</ol>` 지우기 → 2번 제목과 목록이 1번 상자 안으로 들어간다 |
| [day1/ex02_server.html](day1/ex02_server.html) + [ex02_server.js](day1/ex02_server.js) + [ex02_message.json](day1/ex02_message.json) | `node server.mjs` 로 열면(`http://localhost:8000/ex/…`) JSON 의 글과 Console 1번, 터미널에 `200 GET` 세 줄. 두 번 눌러 열면(`file:///…`) `읽지 못했습니다.`, Console 에 빨간 줄 두 줄(`… blocked by CORS policy …`·`net::ERR_FAILED`)과 2번 | 12주 ex05 복습. `fetch` 는 서버나 공개 주소로 연 페이지에서만 파일을 읽는다. 두 번 눌러 연 `file://` 페이지는 막힌다. 그래서 로컬 시연은 서버로 한다 | 서버로 열기 → 두 번 눌러 열기. 8행 파일 이름을 `ex02_massage.json` 으로 → 서버에서도 `읽지 못했습니다.` 이고 터미널에 `404 GET` |
| [day1/ex03_storage.html](day1/ex03_storage.html) + [ex03_storage.js](day1/ex03_storage.js) | 누를 때마다 1번과 2번이 함께 는다. 새로고침하면 1번은 0, 2번은 그대로 | 11주 ex04 복습 + 주소·창 비교. 변수는 새로고침하면 처음으로 돌아가고, 저장 칸(`localStorage`)에 넣은 값은 남는다. 저장 칸은 주소 앞부분(`file://`·`http://localhost:8000`)마다 따로이고 시크릿 창도 따로라, 서버 주소나 새 시크릿 창에서는 2번이 0 에서 시작한다. 같은 아이디의 `github.io` 주소(`web-week13`·`web-week14`)는 저장 칸을 함께 쓴다(11주) | 세 번 누르고 새로고침. 9행을 `let countSaved = 0;` 으로 → 저장값은 남아 있는데 2번은 0. 서버 주소·새 시크릿 창으로 열기 |

### 파일 안의 모양

형제 번호가 주석 첫머리와 `console.log` 앞 글자에 있다. [ex03_storage.js](day1/ex03_storage.js) 에서 인용:

```js
let countVar = 0;                                                       // 1. 변수: 열 때마다 0 에서 시작한다
let countSaved = JSON.parse(localStorage.getItem('ex03-count')) || 0;   // 2. 저장 칸에서 꺼낸다. 처음 여는 주소는 null 이라 || 0 (11주 ex06)
savedBox.textContent = `2. 저장한 수: ${countSaved}`;

btn.addEventListener('click', function () {
    countVar = countVar + 1;
    varBox.textContent = `1. 변수에 담은 수: ${countVar}`;
    console.log('1. 변수 :', countVar);

    countSaved = countSaved + 1;
    localStorage.setItem('ex03-count', JSON.stringify(countSaved));   // 11주 방명록 saveList 와 같은 모양
    savedBox.textContent = `2. 저장한 수: ${countSaved}`;
    console.log('2. 저장 :', countSaved);
});
```

1번과 2번은 `+ 1` 하는 줄이 똑같다. 다른 것은 담는 곳 하나다. 1번은 변수, 2번은 브라우저의 저장 칸(`localStorage`)이다.
9행과 18행은 11주 방명록의 되살리는 줄(`JSON.parse(…) || []`)·`saveList()` 와 같은 모양이다. 목록이 아니라 수 하나라서 `|| []` 대신 `|| 0` 을 붙였다.

## `day2/web-week14/` — 2일차 끝의 web-week14

[`day2/web-week14/`](day2/web-week14/) 는 2일차 끝의 `web-week14` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 2일차는 발표만 하므로 1일차 끝과 같다. 15주차 문제 은행 `w14_readme_images` 의 출처다. 비교 예제를 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.
13주차 완성본에서 바뀐 것은 `index.html`·`about.html`·`README.md`·`screenshots/home.png` 넷이다. 나머지는 13주차와 글자 단위로 같다.
이 폴더의 `about.html` 42행과 `README.md` 의 공개 주소는 예시 아이디의 `https://student01.github.io/web-week14/` 다. 내 파일에는 본인 아이디의 이번 주 공개 주소를 쓴다.

| `day2/web-week14/` 파일 | 내 `web-week14` 의 위치 | 따라하기 단계 |
|---|---|---|
| [index.html](day2/web-week14/index.html) | `index.html` | [6·9단계](../walkthrough.md#6-indexhtml-에-발표-순서-목록-넣기) — `#count` 카드 아래에 `<h2>` 와 `<ol class="card">` 다섯 줄이 늘어난다(ex01) |
| [about.html](day2/web-week14/about.html) | `about.html` | [7·10단계](../walkthrough.md#7-abouthtml-표에-공개-주소-행-넣기) — 표에 공개 주소 행(`<tr>` 네 줄)이 늘어난다 |
| [README.md](day2/web-week14/README.md) | `README.md` | [8·14단계](../walkthrough.md#8-readmemd-세-곳-고치기) — 공개 주소 줄과 홈 줄을 고치고 `## 만든 과정` 맨 아래에 `- 14주차: …` 한 줄을 더한다(9~14주차 여섯 줄). 14단계는 저장소 첫 화면에서 확인 |
| [screenshots/home.png](day2/web-week14/screenshots/home.png) | `screenshots/home.png` | [13단계](../walkthrough.md#13-공개-주소에서-확인하고-그림-다시-찍기) — 인사 바꾸기를 누른 뒤 목록이 보이는 홈을 다시 찍는다 |
| [screenshots/guestbook.png](day2/web-week14/screenshots/guestbook.png) · [screenshots/projects.png](day2/web-week14/screenshots/projects.png) | `screenshots/` | 13주차 그대로 |
| [styles.css](day2/web-week14/styles.css) · [app.js](day2/web-week14/app.js) · [about.js](day2/web-week14/about.js) · [guestbook.html](day2/web-week14/guestbook.html) · [guestbook.js](day2/web-week14/guestbook.js) · [projects.html](day2/web-week14/projects.html) · [projects.js](day2/web-week14/projects.js) · [data/projects.json](day2/web-week14/data/projects.json) | 같은 이름 | 13주차 그대로. 동작하지 않으면 내 파일과 한 줄씩 비교한다 |
| [images/](day2/web-week14/images/) 의 그림 네 장 | `images/` | 3·12주차에 넣은 것 그대로 |
