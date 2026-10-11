[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud)

# 12주차 예제 — 비교 예제 6개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   index.html      고르기 페이지 — 맨 아래 script 줄 하나만 켠다
          ex01 ~ ex03     JSON 글자 규칙, fetch 틀, file:// 과 http:// (.js 파일)
          ex02·ex03 의 .json   ex02·ex03 이 fetch 로 읽는 데이터 파일
  day2/   ex04 ~ ex06     카드 만들기, try / catch, response.ok (.html + .js 한 쌍)
          ex04_picture.png · ex05·ex06 의 .json   예제가 쓰는 그림과 데이터 파일
          web-week12/     2일차 끝의 web-week12 — 비교 예제에서 본 줄을 모은 조립
```

`exNN_*` 파일은 **파일 하나 = 개념 하나**다. 같은 일을 다르게 한 **형제**(1·2·3번)를 나란히 놓는다.
결과는 화면과 **F12 › Console**, 그리고 이번 주에 처음 쓰는 **F12 › Network** 탭에서 본다. 값이나 줄을 바꾸고 저장 → 새로고침으로 무엇이 달라지는지 본다.
**다른 파일의 개념은 섞지 않는다.** 오류를 받는 `try / catch` 는 ex05 의 주제라서 ex02·ex03·ex06 에는 없다. ex04 는 `fetch` 없이 JS 안의 배열로 카드만 그린다.
만들기는 마지막 하나, [`day2/web-week12/`](day2/web-week12/) 뿐이다.

**이번 주 예제는 서버로 연다.** `fetch` 는 두 번 눌러 연 화면(`file://`)에서 막힌다(ex03). 저장소 맨 위에서 `node server.mjs` 를 띄우고 `http://localhost:8000/ex/` 로 연다([서버 사용 안내](../../../tools/static-server/README.md)). 공개 주소 `https://student01.github.io/web-week12/ex/` 에서도 된다. `fetch` 가 없는 ex01·ex04 는 두 번 눌러 열어도 결과가 같다(ex03·ex05 는 차이를 보려고 일부러 두 번 눌러서도 연다).
1일차는 세 예제가 같은 화면(글자 자리 하나)을 쓴다. 그래서 코드를 `.js` 파일로 떼어 두고 고르기 페이지 [day1/index.html](day1/index.html) 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 세 줄 중 **하나만** 주석 밖에 둔다(VS Code 에서 줄에 커서를 두고 **Ctrl+/**, macOS **⌘+/**). 처음에는 ex01 줄만 켜져 있다. 6주차 1일차와 같은 방법이다.
2일차 예제는 화면이 서로 다르다. 그래서 예제마다 `.html` 과 `.js` 를 한 쌍으로 둔다. `.html` 을 연다. 두 파일과 그 예제가 읽는 그림·`.json` 이 같은 폴더에 있어야 한다.
내려받아 이번 주 저장소 `web-week12` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 내 저장소에서는 날짜 폴더 없이 `ex/` 한 곳에 모은다. 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 예제

| 파일 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/index.html](day1/index.html) | 제목과 안내 두 줄, "예제가 쓰는 자리"의 글자 한 줄. Console·Network 에는 켜 둔 `script` 줄의 예제 것만 찍힌다(서버로 처음 열거나 새로고침하면 `favicon.ico` 404 한 줄이 섞일 수 있다. 탭 아이콘 요청이다) | JS 를 파일로 떼어 HTML 이 `<script src>` 로 불러온다. 어느 파일을 불러올지는 `script` 줄 하나로 정해진다 | 켜 둔 줄을 바꿔 가며 새로고침 |
| [day1/ex01_json_rule.js](day1/ex01_json_rule.js) | 화면 `1. 2개 — 첫 제목은 자기소개 페이지`. Console 1번에 객체 두 개짜리 배열 | JSON 은 글자다. 이름과 문자열 값을 큰따옴표로 감싸고 마지막 항목 뒤에 쉼표가 없는 글자만 `JSON.parse` 가 배열로 바꾼다(11주차 `JSON.parse` 와 같다) | 13~15행 주석 풀기(작은따옴표) → `Expected property name or '}' in JSON …` 빨간 줄, 18~20행 주석 풀기(마지막 쉼표) → `Unexpected token ']' …` 빨간 줄. 두 줄 모두 오른쪽 `파일:줄` 이 `.js` 의 줄이 아니라 끝이 `:1` 이다(JSON 글자 안의 1행). 7행 `"title"` 의 따옴표 지우기 |
| [day1/ex02_fetch.js](day1/ex02_fetch.js) + [ex02_projects.json](day1/ex02_projects.json) | 화면 `2. 3개를 불러왔다 — 첫 제목은 3주차 자기소개`. Console 1번 `response`, 2번 배열. Network 에 `ex02_projects.json` 200 · `fetch` | `await fetch(…)` 는 파일을 요청하고 응답을 기다린다. `await response.json()` 은 응답의 글자를 배열로 바꾼다. `async` 를 붙인 함수 안에서만 `await` 를 쓴다 | `.json` 의 첫 제목 바꾸기 → `.js` 그대로 화면만 바뀐다. 9행 `await` 지우기 → 2번에 `Promise`, 11행 빨간 줄. 14행 `loadProjects();` 지우기 → 아무 일도 없다 |
| [day1/ex03_file_http.js](day1/ex03_file_http.js) + [ex03_projects.json](day1/ex03_projects.json) | 서버 주소: 화면 `3. 2개를 불러왔다`. 두 번 눌러 연 `file://`: 화면 `1. 불러오는 중 …` 에서 멈추고 Console 에 CORS 줄, `… net::ERR_FAILED` 줄, `Uncaught (in promise) TypeError: Failed to fetch` | 코드는 같고 주소가 다르다. `file://` 로 연 페이지에서는 브라우저가 `fetch` 를 막아 8행에서 멈춘다. 그 아래(3번)는 실행되지 않는다 | 서버 주소와 두 번 눌러 열기를 번갈아. 주소창에 `…/ex/ex03_projects.json` 을 직접 쳐서 받은 글자 보기 |
| [day2/ex04_cards.html](day2/ex04_cards.html) + [ex04_cards.js](day2/ex04_cards.js) | 노란 카드 세 장. 카드마다 `카드 그림`·제목·설명·`교재 열기` 링크 | 배열의 항목 하나가 `article` 카드 한 장이 된다. 카드 안 순서는 44행 `append(image, title, description, link)` 의 순서다. 모양은 `.card` 규칙이 정하고 JS 는 class 만 붙인다(6주차) | 44행 순서 바꾸기, 32행 `classList.add('card')` 주석, 15행 그림 이름을 `'ex04_nothing.png'` 로 → `alt` 글이 보인다, 네 번째 객체 더하기 |
| [day2/ex05_try_catch.html](day2/ex05_try_catch.html) + [ex05_try_catch.js](day2/ex05_try_catch.js) | 서버 주소: `1. try: 2개를 불러왔다`. 두 번 눌러 열면: `2. catch: 프로젝트를 불러오지 못했습니다.`, Console 2번에 받은 오류. `Uncaught` 줄은 없다 | `try` 안에서 오류가 나면 페이지가 멈추지 않고 `catch` 로 가서 화면에 알린다. 1일차 ex03 에서 화면이 멈추던 그 오류다 | `ex05_projects.json` 에 작은따옴표 넣기 → 서버 주소에서도 2번. 작은따옴표를 둔 채 13·14행 주석 → 화면은 `불러오는 중`, Console 은 비고 Network 는 200 이라 원인을 알 수 없다 |
| [day2/ex06_response_ok.html](day2/ex06_response_ok.html) + [ex06_response_ok.js](day2/ex06_response_ok.js) | 1번(있는 파일): `불러오는 중` 이 지워지고 `3개를 불러왔다`, Network 200. 2번(없는 파일): `프로젝트를 불러오지 못했습니다.`, Network 404 | 파일이 없어도 서버는 404 와 HTML 오류 페이지로 답한다. `fetch` 는 멈추지 않으므로 읽기 전에 `response.ok` 로 묻고, `false` 면 안내를 쓰고 `return` 한다 | 6·7행 바꿔 2번 켜기, 2번에서 12~15행 주석 → `Unexpected token '<'` 빨간 줄, 파일 이름 앞에 `/` → 404 |

### 파일 안의 모양

형제 번호가 주석 첫머리와 `console.log` 앞 글자에 있다. [ex01_json_rule.js](day1/ex01_json_rule.js) 에서 인용:

```js
// 1. 큰따옴표 — 11주차 Application 탭에서 본 글자와 같은 모양이다
const text1 = `[{"title": "자기소개 페이지"}, {"title": "방명록"}]`;
const projects1 = JSON.parse(text1);
console.log('1. 큰따옴표 :', projects1);

// 2. 작은따옴표 — 아래 세 줄의 // 를 지우면 빨간 줄이 뜬다. JSON 에는 작은따옴표가 없다
// const text2 = `[{'title': '자기소개 페이지'}, {'title': '방명록'}]`;
// const projects2 = JSON.parse(text2);
// console.log('2. 작은따옴표 :', projects2);
```

1번과 2번은 `JSON.parse` 하는 줄이 똑같다. 다른 것은 글자 안의 따옴표 하나다. 바깥의 `` ` `` 는 JS 의 글자 표시(5주차 템플릿 문자열)이고, JSON 파일에는 그 안쪽 글자만 적는다.

## `day2/web-week12/` — 2일차 끝의 web-week12

[`day2/web-week12/`](day2/web-week12/) 는 2일차 끝의 `web-week12` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 13주차 새 저장소 `web-week13` 의 시작점이다. 비교 예제를 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.
이 폴더도 `fetch` 가 있어서 서버로 연다(`node server.mjs` → `http://localhost:8000/projects.html`).

| `day2/web-week12/` 파일 | 내 `web-week12` 의 위치 | 따라하기 단계 |
|---|---|---|
| [data/projects.json](day2/web-week12/data/projects.json) | `data/projects.json` | [2일차 8단계](../walkthrough.md#2일차) — 새로 만든다. 객체 세 개, 이름표 `title`·`description`·`image`·`link` |
| [images/project1.png](day2/web-week12/images/project1.png) · [project2.png](day2/web-week12/images/project2.png) · [project3.png](day2/web-week12/images/project3.png) | `images/project1.png` 등 | [2일차 9단계](../walkthrough.md#2일차) — 카드 그림 세 장. 새로 넣는다 |
| [projects.html](day2/web-week12/projects.html) | `projects.html` | [2일차 10단계](../walkthrough.md#2일차) — 새로 만든다. `guestbook.html` 과 같은 뼈대에 `#notice`·`#project-list` |
| [projects.js](day2/web-week12/projects.js) | `projects.js` | [2일차 11·12단계](../walkthrough.md#2일차) — 새로 만든다. 조립표 순서로 쓰면 이 파일과 글자 단위로 같아진다 |
| [index.html](day2/web-week12/index.html) · [about.html](day2/web-week12/about.html) · [guestbook.html](day2/web-week12/guestbook.html) | 같은 이름 | [2일차 13단계](../walkthrough.md#2일차) — nav 에 `<a href="projects.html">프로젝트</a>` 한 줄이 늘어난다 |
| [app.js](day2/web-week12/app.js) · [guestbook.js](day2/web-week12/guestbook.js) · [styles.css](day2/web-week12/styles.css) | 같은 이름 | 11주차 그대로. 이번 주에 고치지 않는다. 카드 모양은 4주차 `.card` 규칙을 그대로 쓴다 |
| [README.md](day2/web-week12/README.md) · [screenshots/](day2/web-week12/screenshots/) · [images/profile.png](day2/web-week12/images/profile.png) | 같은 이름 | `README.md` 와 캡처 두 장은 9주차 1차 과제 때 만든 README 1차판과 화면 그대로다. 10·11주차에 이어 이번 주에도 고치지 않는다(프로필 그림도 그대로). 저장소 `README.md` 는 13주차에 최종판으로 다시 쓴다 |
