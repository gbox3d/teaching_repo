---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 12주차"
footer: "fetch로 JSON 불러오기 · 비교 예제로 원리를 보고 마지막에 조립"
---

# fetch로 JSON 불러오기

11주차에는 방명록 글을 **브라우저 저장소**에 넣었습니다. 이번 주에는 화면에 쓸 내용을 **파일**에 적어 두고 `fetch` 로 읽어 와 카드로 그립니다.

이번 주 방식도 같습니다: **비교 예제 6개**를 하나씩 보고, 마지막에 새 저장소 `web-week12` 에 `data/projects.json`·`projects.html`·`projects.js` 를 **조립**합니다(지난주 완성본에서 시작).

- JSON 은 **글자**입니다. 큰따옴표 규칙을 지킨 글자만 배열이 됩니다.
- `fetch` 는 파일을 **요청**합니다. 두 번 눌러 연 `file://` 화면에서는 막히고 서버 주소에서 됩니다.
- 결과는 화면, **Console**, 그리고 새로 쓰는 **Network** 탭에서 봅니다.

---

# 1일차 — JSON 파일과 fetch

`30분 설명·시연 → 60분 실습`

1. 고르기 페이지와 서버 — 이번 주 예제는 `http://localhost:8000/ex/` 로 연다
2. ex01 — JSON 글자 규칙: 큰따옴표와 마지막 쉼표
3. ex02 — fetch 틀: `await fetch` → `await response.json()`, Network 탭
4. ex03 — `file://` 과 `http://`: 두 번 눌러 열면 막힌다

---

## 1일차 · 0–4분 — 고르기 페이지와 서버로 열기

[examples/day1/index.html](examples/day1/index.html) — 세 예제가 같은 화면(글자 자리 하나)을 씁니다. 서버: [server.mjs](../../tools/static-server/server.mjs)

```html
<script src="ex01_json_rule.js"></script>
<!-- <script src="ex02_fetch.js"></script> -->
<!-- <script src="ex03_file_http.js"></script> -->
```

- 맨 아래 `script` 줄 중 **한 줄만** 켭니다(Ctrl+/). 6주차와 같은 방법입니다.
- `node server.mjs` 로 띄운 `http://localhost:8000/ex/` 에서 엽니다. `fetch` 가 파일을 요청하기 때문입니다(ex03).
- 확인과 캡처는 **공개 주소**에서 합니다. 서버는 push 전에 미리 보는 도구입니다.

**fetch 가 있는 페이지는 서버 주소나 공개 주소로 연다.**

---

## 1일차 · 4–11분 — ex01 JSON 글자 규칙

[ex01_json_rule.js](examples/day1/ex01_json_rule.js) — 7~8행(1번) · 13~14행(2번) · 18~19행(3번)

```js
const text1 = `[{"title": "자기소개 페이지"}, {"title": "방명록"}]`;
const projects1 = JSON.parse(text1);
// const text2 = `[{'title': '자기소개 페이지'}, {'title': '방명록'}]`;
// const projects2 = JSON.parse(text2);
// const text3 = `[{"title": "자기소개 페이지"}, {"title": "방명록"},]`;
// const projects3 = JSON.parse(text3);
```

- JSON 은 **글자**입니다. 1번은 이름과 값이 **큰따옴표**, 2번은 작은따옴표, 3번은 끝 `}` 뒤에 쉼표.
- 2·3번 주석을 풀면 `JSON.parse` 가 읽지 못하고 빨간 줄이 뜹니다. 위의 1번 화면은 남습니다.

**규칙을 지킨 글자만 배열이 된다.**

---

## 1일차 · 11–19분 — ex02 fetch 틀과 Network 탭

[examples/day1/ex02_fetch.js](examples/day1/ex02_fetch.js) · [ex02_projects.json](examples/day1/ex02_projects.json)

```js
async function loadProjects() {   // await 는 async 함수 안에서만 쓴다
    const response = await fetch('ex02_projects.json');  // 1. 요청하고 기다린다
    const projects = await response.json();              // 2. 글자 → 배열
    result.textContent = `2. ${projects.length}개를 불러왔다 …`;
}
loadProjects();                   // 이 줄이 없으면 아무 일도 없다
```

- **F12 › Network**: `ex02_projects.json` 한 줄, Status **200**, Type `fetch`.
- `await` 를 빼면 아직 오지 않은 값(`Promise`)이 담깁니다.

**fetch 는 파일을 요청하고, json() 은 받은 글자를 배열로 바꾼다.**

---

## 1일차 · 19–26분 — ex03 file:// 과 http://

[examples/day1/ex03_file_http.js](examples/day1/ex03_file_http.js) · [ex03_projects.json](examples/day1/ex03_projects.json)

```text
http://localhost:8000/ex/   → 화면 3. 2개를 불러왔다
file:///…/ex/index.html     → 화면 1. 불러오는 중 … (멈춤)
  Access to fetch at 'file:///…' … has been blocked by CORS policy …
  Uncaught (in promise) TypeError: Failed to fetch
```

- 코드는 같고 **주소**가 다릅니다. `file://` 로 연 페이지에서는 브라우저가 요청을 막습니다.
- 오류 난 줄(2번) 아래는 실행되지 않아 화면이 1번에 멈춥니다.
- "코드가 똑같은데 안 돼요" → **주소창부터** 봅니다.

**fetch 는 서버 주소(http·https)에서만 된다.**

---

## 1일차 · 26–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--json-파일과-fetch-60분) · [따라하기](walkthrough.md#1일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud)

1. 새 폴더 `web-week12` 에 지난주 완성본과 `server.mjs`, `ex/` 에 오늘 여섯 파일.
2. `node server.mjs` → ex01~ex03 줄 하나만 켜고 값 바꿔 보기. 무엇이 달라질지 먼저 말해 봅니다.
3. 새 저장소 `web-week12` 만들어 올리기 · Pages 켜기 → 공개 주소 `…/ex/` 에서도 열어 보기.

**설명 합계: 4+7+8+7+4 = 30분**

---

# 2일차 — 카드와 오류 안내, 그리고 조립

`30분 설명·시연 → 60분 실습`

1. ex04 — 카드 만들기: `article` 에 `img`·`h3`·`p`·`a`
2. ex05 — `try / catch`: 오류를 받아 화면에 알린다
3. ex06 — `response.ok`: 404 는 오류가 아니다
4. 14주차 최종 과제 안내
5. 조립 — `web-week12` 의 `data/projects.json`·`projects.html`·`projects.js`

---

## 2일차 · 0–7분 — ex04 카드 만들기

[examples/day2/ex04_cards.html](examples/day2/ex04_cards.html) · [ex04_cards.js](examples/day2/ex04_cards.js) · [ex04_picture.png](examples/day2/ex04_picture.png)

```js
const article = document.createElement('article');  // 카드 한 장
article.classList.add('card');                       // .card 규칙(6주차)
const image = document.createElement('img');         // 1. src · alt · width
const title = document.createElement('h3');          // 2. 제목
const description = document.createElement('p');     // 3. 설명 — 실제 문장이라 p
const link = document.createElement('a');            // 4. href
article.append(image, title, description, link);     // 넣은 순서대로
```

- 10주차 `showList` 와 같은 순서입니다: 비우기 → `for` → 만들어 붙이기.
- `alt` 는 그림을 못 찾을 때 대신 보이는 글입니다. 13주차에 다시 봅니다.

**배열의 항목 하나가 카드 한 장이 된다.**

---

## 2일차 · 7–13분 — ex05 try / catch: 오류를 받아 화면에 알리기

[ex05_try_catch.html](examples/day2/ex05_try_catch.html) · [ex05_try_catch.js](examples/day2/ex05_try_catch.js) · [ex05_projects.json](examples/day2/ex05_projects.json)

```js
try {   // 이 안에서 오류가 나면 아래 줄은 건너뛰고 catch 로 간다
    const response = await fetch('ex05_projects.json');
    const projects = await response.json();
    notice.textContent = `1. try: ${projects.length}개를 불러왔다`;
} catch (error) {
    notice.textContent = '2. catch: 프로젝트를 불러오지 못했습니다.';
}
```

- 서버로 열면 1번, `file://` 로 열면 2번. 1일차 ex03 의 `Uncaught` 빨간 줄이 사라집니다.

**오류를 catch 로 받아 화면에 알린다.**

---

## 2일차 · 13–19분 — ex06 response.ok: 404 는 오류가 아니다

[ex06_response_ok.html](examples/day2/ex06_response_ok.html) · [ex06_response_ok.js](examples/day2/ex06_response_ok.js) · [ex06_projects.json](examples/day2/ex06_projects.json)

```js
const response = await fetch(fileName);
if (!response.ok) {                 // 404 면 ok 는 false
    notice.textContent = '프로젝트를 불러오지 못했습니다.';
    return;                         // 아래 json() 으로 가지 않는다
}
const projects = await response.json();
```

- 없는 파일에도 서버는 **답합니다**(404 와 HTML 페이지). `fetch` 는 멈추지 않습니다.
- 묻지 않고 읽으면 `json()` 이 HTML 을 읽다가 `Unexpected token '<'` 를 냅니다.

**읽기 전에 response.ok 로 정상인지 묻는다.**

---

## 2일차 · 19–24분 — 14주차 최종 과제 안내

14주차는 **최종 발표**입니다. 새로 만들 것은 없고, 지금까지 만든 사이트를 시연합니다. 필수 기능은 셋입니다.

1. 세 페이지 + CSS + 클릭 기능 + 폼 입력·빈값 안내
2. 방명록 목록 추가·삭제와 개수(10주차) · 새로고침해도 남는 방명록(11주차)
3. `data/projects.json` 을 읽어 그리는 카드(12주차)

- 레포트는 저장소 `README.md` 최종판입니다. 양식은 13주차에 함께 씁니다.
- 수업계획서의 "영속 CRUD와 관계 기능" = 11주차 `localStorage`(영속) + 카드의 **페이지 열기** 링크(관계).
- 서버 데이터베이스와 로그인은 선택 특강에서 다룹니다.

**매주 완성본이 쌓여 최종 과제가 된다.**

---

## 2일차 · 24–30분 — 조립: web-week12, 그리고 실습 인계

```text
data/projects.json  객체 3개 · 큰따옴표        ← ex01 · ex02 · ex04
projects.html       #notice · #project-list     ← 지난주 guestbook.html · ex04 · ex05
projects.js         showProjects(projects)      ← ex04
                    loadProjects: try · fetch   ← ex02 · ex05
                    if (!response.ok) … return  ← ex06
                    catch → 안내 · loadProjects(); ← ex05 · ex02
nav 네 페이지       <a href="projects.html">    ← 지난주 nav
```

[2일차 실습](lab.md#2일차--카드와-오류-안내-그리고-조립-60분) · [따라하기](walkthrough.md#2일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud)

1. ex04~ex06 아홉 파일을 `ex/` 에 저장, 값 바꾸기(28분까지).
2. 조립 → 서버·375·1280 확인 → push → 공개 주소에서 카드와 Network 캡처.

**설명 합계: 7+6+6+5+6 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/web-week12/projects.html
카드 3장 ─ 그림 · 제목 · 설명 · 페이지 열기
F12 › Network ─ projects.json   200
주소창이 함께 보이게 찍습니다
```

확인과 캡처는 공개 주소에서 합니다. 캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

오늘은 HTML 밖의 파일에서 내용을 읽어 카드로 그렸습니다.

13주차에는 새 저장소 `web-week13` 을 오늘 완성본에서 시작하고, 지금까지 만든 네 페이지를 점검합니다.
입력한 글을 `textContent` 로 넣는지(보안), 그림의 `alt` 와 입력 칸의 `label for` 가 있는지(접근성) 보고, `README.md` 를 최종판으로 씁니다.
