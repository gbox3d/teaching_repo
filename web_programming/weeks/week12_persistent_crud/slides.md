---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 12주차"
footer: "fetch로 JSON 불러오기 · data/projects.json, await, try/catch"
---

# fetch로 JSON 불러오기

11주차에는 방명록 항목을 **브라우저 저장 칸**에 넣었습니다.
이번 주에는 화면에 쓸 내용을 **파일**에 적어 두고 읽어 옵니다.

```text
data/projects.json ── fetch ──▶ projects.js ──▶ projects.html
   제목·설명·그림·링크          읽어서 카드로 만들기        카드 3장
```

---

# 1일차 — JSON 파일을 읽어 카드로 그리기

`30분 설명·시연 → 60분 실습`

1. Pages에서 먼저 보기 (오늘 도구 5분)
2. JSON 파일과 큰따옴표 규칙
3. `loadProjects()` 틀 — fetch · json · `console.log`
4. `file://`로 열면 나는 Console 오류

---

## 1일차 · 0–5분 — 오늘 도구 5분: Pages에서 먼저 보기

```text
내 PC ── git push ──▶ GitHub ── Pages ──▶ https://student01.github.io/my-web/
```

- 이번 주 **확인과 캡처의 기준은 공개 주소**입니다. `fetch`는 서버에 올라간 주소에서만 동작합니다.
- 작업 중 미리 보기(선택): VS Code 확장 **Live Server** → 상태줄 **Go Live** → `http://127.0.0.1:5500/`
- 확장이 막히면 터미널에서 `python3 -m http.server 8000`을 씁니다.
- 둘 다 없어도 됩니다. **한 번에 한 가지만 고쳐 push**하고 공개 주소에서 봅니다.

---

## 1일차 · 5–11분 — JSON 파일이란

```json
[
  { "title": "자기소개 페이지", "description": "홈 화면입니다." },
  { "title": "내 정보 표", "description": "아이디와 이메일을 표로 정리했습니다." }
]
```

- 11주차 **Application › Local Storage**에서 본 글자 모양과 같습니다.
- 이름과 문자열 값에는 **큰따옴표 `"`만** 씁니다. 작은따옴표는 오류입니다.
- 마지막 항목 뒤에 쉼표를 남기지 않습니다.
- 파일은 `data/` 폴더 안에 `projects.json`으로 둡니다.

---

## 1일차 · 11–19분 ① — 읽어 온 값을 카드로 그리기

```js
function showProjects(projects) {
  projectList.innerHTML = '';
  for (let i = 0; i < projects.length; i++) {
    const article = document.createElement('article');
    article.classList.add('card');
    const title = document.createElement('h3');
    title.textContent = projects[i].title;
    article.append(title);
    projectList.append(article);
  }
}
```

10주차 `showList()`와 같은 순서입니다: 비우기 → 고전 `for` → 만들어 붙이기.

---

## 1일차 · 11–19분 ② — loadProjects() 틀

```js
async function loadProjects() {
  const response = await fetch('data/projects.json');
  const projects = await response.json();
  console.log(projects);
  showProjects(projects);
}

loadProjects();
```

- `async`와 `await`는 짝입니다. 이번 주에는 **복붙 틀**로 씁니다.
- `await`는 "올 때까지 기다린다"입니다. 두 줄 모두 기다려야 합니다.
- `console.log(projects)`로 배열이 왔는지 먼저 봅니다.

---

## 1일차 · 19–25분 — file://로 열면 카드가 안 나옵니다

```text
Access to fetch at 'file:///…/data/projects.json' from origin 'null'
has been blocked by CORS policy: Cross origin requests are only
supported for protocol schemes: chrome, chrome-extension, …, http, https

Uncaught (in promise) TypeError: Failed to fetch     projects.js:18
```

- 더블클릭해 연 화면은 주소가 `file://`이라 `fetch`가 막힙니다. 페이지는 비어 보입니다.
- **공개 주소(https)** 나 Live Server(`http://127.0.0.1:5500/`)에서는 그대로 나옵니다.
- 오류 줄 끝의 `projects.js:18`이 **파일 이름과 줄 번호**입니다. 5주차 `app.js:6`과 같은 읽는 법입니다.

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--json-파일을-만들어-카드로-그리기-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud

1. `data/projects.json`에 프로젝트 3개를 적습니다.
2. `projects.html`과 `projects.js`를 만들고 `console.log`로 확인합니다.
3. 카드를 그린 뒤 push해서 **공개 주소**에서 봅니다.

**설명 합계: 5+6+8+6+5 = 30분**

막히면 Console의 첫 빨간 줄과 그 끝의 `파일 이름:줄 번호`부터 읽습니다.

---

# 2일차 — 오류 안내와 카드 완성

`30분 설명·시연 → 60분 실습`

1. `try / catch`로 오류를 받아 안내 문구 보여 주기
2. `response.ok`와 404
3. 카드에 그림과 **페이지 열기** 링크 넣기
4. 14주차 최종 과제 공지

---

## 2일차 · 0–6분 — try / catch로 오류 받기

```js
async function loadProjects() {
  try {
    const response = await fetch('data/projects.json');
    const projects = await response.json();
    showProjects(projects);
  } catch (error) {
    notice.textContent = '프로젝트를 불러오지 못했습니다.';
  }
}
```

- `try` 안에서 오류가 나면 멈추지 않고 `catch` 쪽으로 넘어갑니다.
- 화면에 보일 문장은 한 줄로 고정합니다: `프로젝트를 불러오지 못했습니다.`

---

## 2일차 · 6–12분 — response.ok와 404

```js
if (!response.ok) {
  notice.textContent = '프로젝트를 불러오지 못했습니다.';
  return;
}
```

```text
Uncaught (in promise) SyntaxError: Unexpected token '<',
"<!DOCTYPE "... is not valid JSON
```

- 파일 이름을 틀리면 서버가 404와 **HTML 오류 페이지**를 보냅니다.
- `response.json()`이 그 HTML을 읽다가 위 오류를 냅니다. `response.ok`로 먼저 걸러 냅니다.
- 경로를 `/data/projects.json`처럼 `/`로 시작하면 공개 주소에서 404입니다.

---

## 2일차 · 12–19분 ① — 카드에 그림과 링크 넣기

```js
const image = document.createElement('img');
image.src = projects[i].image;
image.alt = `${projects[i].title} 화면 그림`;
image.width = 240;
const link = document.createElement('a');
link.href = projects[i].link;
link.textContent = '페이지 열기';
article.append(image, title, description, link);
```

- `append`에 넣은 **순서대로** 카드 안에 쌓입니다.
- `alt`는 그림이 안 보일 때 대신 읽히는 글입니다. 13주차에 다시 봅니다.

---

## 2일차 · 12–19분 ② — .card를 그대로 씁니다

```css
.card {
  background-color: #ffffff;
  padding: 16px;
  margin: 12px 0;
  border: 1px solid #c3cbe6;
}
```

- 4주차에 만든 규칙입니다. `styles.css`에 **새 규칙을 더하지 않습니다.**
- `article.classList.add('card')` 한 줄이면 같은 모양이 됩니다.
- 카드가 흰 상자로 보이지 않으면 `classList.add`의 철자부터 봅니다.

---

## 2일차 · 19–25분 — 14주차 최종 과제 공지

**필수 기능** (9주차 사이트 + 10~12주차 기능)

1. 세 페이지 + CSS + 클릭 기능 + 폼 입력·빈값 안내
2. 방명록 목록 추가·삭제와 개수 (10주차)
3. 새로고침해도 남는 방명록 (11주차)
4. `data/projects.json`을 읽어 그리는 카드 (12주차)

**README 최종판**: 공개 주소 · 페이지 목록 · 기능 · `screenshots/` 3장 · 배운 것

발표는 3분 시연입니다. 자세한 양식은 13주차에 정리합니다.

---

## 2일차 · 25–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--오류-안내와-카드-완성-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud

1. `projects.html`에 안내 문구 자리를 만들고 `try / catch`·`response.ok`를 넣습니다.
2. 카드에 그림과 **페이지 열기** 링크를 넣습니다.
3. 네 페이지 nav에 `projects.html` 링크를 넣고 push합니다.

**설명 합계: 6+6+7+6+5 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

- 공개 주소 `https://<아이디>.github.io/my-web/projects.html`
- 카드 3개(그림·제목·설명·**페이지 열기**)가 보인다
- **F12 › Network**에 `projects.json`이 **Status 200**으로 보인다
- 주소창이 함께 보이게 찍는다

캡처에 이메일·실명이 보이지 않게 합니다. 아이디는 보여도 됩니다.

---

## 다음 주 미리 보기

이제 화면에 쓸 내용이 HTML 밖의 파일에 있습니다.

13주차에는 네 페이지를 점검합니다. 입력한 글자를 그대로 보여 주는 `textContent`,
그림의 `alt`, 폼의 `label for`를 다시 보고 `about.js`로 입학 연도를 계산합니다.
저장소 `README.md` 최종판과 `screenshots/` 3장도 이때 정리합니다.

---

## 최소 정합 — 수업계획서의 "영속 CRUD와 관계 기능"

| 수업계획서의 말 | 이 수업에서 한 것 |
|---|---|
| 영속(persistent) | 11주차 `localStorage` — 새로고침해도 남는 방명록 |
| CRUD | 10~11주차 방명록 남기기·목록·삭제·전체 지우기 |
| 관계 기능 | 12주차 카드 → 상세 페이지 링크(`link.href`) |

서버 데이터베이스와 로그인은 이 과목의 선택 특강에서 다룹니다.
