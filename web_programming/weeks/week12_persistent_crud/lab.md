# 12주차 실습 — JSON 파일을 읽어 카드로 그리기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud

이번 주에는 화면에 쓸 내용을 `data/projects.json` 파일에 적어 두고, `fetch`로 읽어 `projects.html`에 카드로 그린다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.

**확인과 캡처는 공개 주소 `https://<아이디>.github.io/my-web/`에서만 한다.**
파일을 더블클릭해 연 화면(`file://`)에서는 `fetch`가 막혀 카드가 보이지 않는다.
작업 중 미리 보기가 필요하면 VS Code 확장 **Live Server**(**Go Live** → `http://127.0.0.1:5500/`)를 쓰고,
설치가 막히면 터미널에서 `python3 -m http.server 8000`을 쓴다. 둘 다 없으면 **한 번에 한 가지만 고쳐 push**하고 공개 주소에서 본다.

## 1일차 — JSON 파일을 만들어 카드로 그리기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`. 미리 보기를 쓸 수 있으면 **Go Live**까지 켠다 |
| 5–20분 | `data` 폴더와 `data/projects.json`에 프로젝트 3개를 적고, `images/`에 카드 그림 세 장을 넣는다 |
| 20–35분 | `projects.html`과 `projects.js`를 만들고 `console.log(projects)`까지 넣는다 |
| 35–55분 | `showProjects()`로 카드를 그린다. `file://`에서 나는 Console 오류를 한 번 확인한다 |
| 55–60분 | `git add .` → `git commit` → `git push` → 공개 주소에서 카드 확인 → 확인용 캡처 → 자격 증명 삭제 |

### 1. 데이터 파일 만들기 (`data/projects.json`)

`data` 폴더를 만들고 그 안에 `projects.json`을 만들어 객체 3개를 적는다. [따라하기 2단계](walkthrough.md#2-data-폴더와-projectsjson-만들기)를 본다.

- 이름표는 `title`·`description`·`image`·`link` 네 개로 고정한다. 값은 본인 내용으로 바꿔도 된다.
- 이름과 문자열 값에는 **큰따옴표만** 쓴다. VS Code가 빨간 밑줄을 그으면 따옴표와 마지막 쉼표부터 본다.
- `link`에는 이미 만든 페이지 이름(`index.html`·`about.html`·`guestbook.html`)을 적는다.

### 2. 카드 그림 넣기 (`images/`)

`images/` 폴더에 `project1.png`·`project2.png`·`project3.png`를 넣는다. [따라하기 3단계](walkthrough.md#3-카드-그림-세-장-넣기)를 본다.

- 예제 그림을 내려받아도 되고, 본인 페이지를 캡처해 같은 이름으로 저장해도 된다.
- 파일 이름의 대소문자를 `projects.json`의 `image` 값과 똑같이 맞춘다.

### 3. 페이지와 스크립트 만들기 (`projects.html` · `projects.js`)

`projects.html`에 `<div id="project-list"></div>`와 `<script src="projects.js" defer>`를 두고, `projects.js`에 `loadProjects()` 틀을 넣는다.
[따라하기 4~5단계](walkthrough.md#4-projectshtml-만들기)를 본다.

- `async function`과 `await` 두 줄은 이번 주에 **복붙 틀**로 쓴다. 다만 `fetch`의 경로는 직접 적는다.
- 먼저 `console.log(projects)`까지만 만들고, 배열이 오는지 Console에서 확인한 뒤 카드를 그린다.
- 마지막 줄 `loadProjects();`를 빠뜨리면 아무 일도 일어나지 않는다.

### 4. 카드 그리기 (`createElement` · `append`)

`showProjects(projects)` 안에서 `article`을 만들고 `classList.add('card')`를 한 뒤 `h3`과 `p`를 넣는다.

- 10주차 `showList()`와 순서가 같다: `innerHTML = ''`로 비우기 → 고전 `for` → 만들어 `append`.
- `projects[i].title`처럼 **몇 번째 항목의 어떤 값**인지 적는다.
- `styles.css`는 고치지 않는다. `.card`는 4주차에 만든 것을 그대로 쓴다.

### 5. `file://`에서 나는 오류 한 번 보기

`projects.html`을 더블클릭해서 열고 **F12 › Console**을 본다. [따라하기 6단계](walkthrough.md#6-file로-열어-console-보기)를 본다.

- 빨간 줄 두 개(CORS 안내와 `Failed to fetch`)를 눈으로 확인한다. 코드가 틀린 것이 아니다.
- 오류 줄 끝의 `projects.js:18`이 파일 이름과 줄 번호다. 5주차 `app.js:6`과 같은 읽는 법을 2일차에도 쓴다.

### 6. 오늘 확인할 것

- [ ] `data/projects.json`에 객체가 3개 있고 VS Code에 빨간 밑줄이 없다.
- [ ] push한 뒤 공개 주소 `/my-web/projects.html`에서 카드 3장이 보인다.
- [ ] Console에 `console.log(projects)`가 찍은 배열이 보인다.
- [ ] 확인용 캡처 1장을 저장했다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 오류 안내와 카드 완성 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | `git pull`. 미리 보기를 쓸 수 있으면 **Go Live**까지 켠다 |
| 5–20분 | `projects.html`에 `<p id="notice"></p>`를 넣고 `try / catch`·`response.ok`로 안내 문구를 띄운다 |
| 20–40분 | 카드에 `img`와 **페이지 열기** 링크를 넣고, 네 페이지 nav에 `projects.html` 링크를 넣는다 |
| 40–55분 | 공개 주소에서 카드 3장을 확인하고 **F12 › Network**에서 `projects.json` 200을 확인한다 |
| 55–60분 | `git add .` → `git commit` → `git push` → 공개 주소 새로고침 → 제출 캡처 → 자격 증명 삭제 |

### 1. 안내 문구 자리 만들기 (`<p id="notice">`)

`projects.html`의 안내 문장 아래에 `<p id="notice"></p>`를 넣고, `projects.js` 위쪽에 `const notice = document.querySelector('#notice');`를 넣는다.
[따라하기 8단계](walkthrough.md#8-안내-문구-자리-만들기)를 본다.

- 11주차 방명록의 `#notice`와 같은 방식이다. 비어 있으면 화면에 보이지 않는다.
- 안내 문장은 한 줄로 고정한다: `프로젝트를 불러오지 못했습니다.`

### 2. 오류 받기 (`try / catch`)

`loadProjects()`의 안쪽을 `try { }`로 감싸고 `catch (error) { }`에서 안내 문구를 넣는다. [따라하기 9단계](walkthrough.md#9-try--catch로-오류-받기)를 본다.

- 성공했을 때는 `notice.textContent = '';`로 문구를 지운다. 지우지 않으면 한 번 뜬 안내가 남는다.
- 이 상태로 `file://` 화면을 열면 Console 대신 **화면에** 안내 문구가 보인다. 1일차와 비교해 본다.

### 3. 404 거르기 (`response.ok`)

`fetch` 바로 아래에서 `if (!response.ok)`로 확인하고 안내 문구를 넣은 뒤 `return`한다. [따라하기 10단계](walkthrough.md#10-responseok로-404-거르기)를 본다.

- 확인은 `data/projects.json`의 이름을 잠깐 `project.json`으로 바꿔서 한다. 확인한 뒤 반드시 되돌린다.
- 이 실험 중에는 Console에 404 한 줄이 남는 것이 정상이다. 이름을 되돌리면 사라진다.
- 경로를 `/data/projects.json`처럼 `/`로 시작하면 공개 주소에서 404다. `data/projects.json`으로 쓴다.

### 4. 카드 완성하기 (`img` · `a`)

`for` 안에서 `img`와 `a`를 만들어 `append(image, title, description, link)` 순서로 넣는다. [따라하기 11단계](walkthrough.md#11-카드에-그림과-링크-넣기)를 본다.

- `image.alt`에는 그림이 안 보일 때 읽힐 글을 넣는다(예: `자기소개 페이지 화면 그림`).
- `link.textContent`는 `페이지 열기`로 두고, `link.href`에 `projects[i].link`를 넣는다.

### 5. nav 통일하기 (네 페이지)

`index.html`·`about.html`·`guestbook.html`의 nav에 `<a href="projects.html">프로젝트</a>` 한 줄씩을 넣는다. [따라하기 12단계](walkthrough.md#12-nav에-프로젝트-링크-넣기)를 본다.

- 네 페이지의 nav 링크 순서를 `홈 · 내 정보 · 방명록 · 프로젝트`로 같게 둔다.
- 한 페이지씩 열어 네 링크가 모두 동작하는지 눌러 본다.

### 6. 오늘 확인할 것

- [ ] 공개 주소에서 카드 3장에 그림·제목·설명·**페이지 열기**가 보인다.
- [ ] **F12 › Network**에 `projects.json`이 **200**으로 보인다.
- [ ] 파일 이름을 틀리게 하면 `프로젝트를 불러오지 못했습니다.`가 화면에 보인다(확인 뒤 되돌린다).
- [ ] (파일 이름을 되돌린 뒤) Console에 빨간 줄이 없다.
- [ ] 제출 캡처 1장을 저장했다.

## 막혔을 때

아래 문구는 실제로 재현해 본 Console·화면 문구다.

| 증상 | 확인할 것 |
|---|---|
| push했는데 공개 페이지가 그대로다 | **Pages 반영은 1~3분 늦다.** 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 Pages 확인을 해도 된다 |
| `Access to fetch at 'file:///…/data/projects.json' from origin 'null' has been blocked by CORS policy: Cross origin requests are only supported for protocol schemes: chrome, chrome-extension, chrome-untrusted, data, http, https, isolated-app.` | 파일을 더블클릭해서 연 화면(`file://`)이다. 공개 주소나 Live Server(`http://127.0.0.1:5500/`)에서 연다. 코드 문제가 아니다 |
| `Uncaught (in promise) TypeError: Failed to fetch` (`projects.js:18`) | 위와 같은 원인이다. 2일차에 `try / catch`를 넣으면 이 줄 대신 화면에 안내 문구가 나온다 |
| `Uncaught (in promise) SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON` | 파일을 못 찾아 서버가 HTML 404 페이지를 보냈다. `fetch`의 경로 철자, `data` 폴더 위치, 파일 이름 `projects.json`을 본다. `/`로 시작하는 경로를 썼는지도 본다 |
| `Uncaught (in promise) SyntaxError: Expected property name or '}' in JSON at position 10 (line 3 column 5)` | JSON 안에 작은따옴표를 썼거나 쉼표가 남았다. 괄호 안 `line 3 column 5`가 고칠 자리다 |
| 화면에 `프로젝트를 불러오지 못했습니다.`만 보인다 | 안내가 제대로 동작한 것이다. 원인은 위 두 줄 중 하나다. **Network** 탭에서 `projects.json`의 Status가 200인지 404인지 본다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` | `#notice`나 `#project-list`를 찾지 못했다. `projects.html`의 `id` 철자와 `<script src="projects.js" defer>` 줄을 본다 |
| 카드는 나오는데 그림이 깨진다 | `data/projects.json`의 `image` 값과 `images/` 안 파일 이름의 **대소문자**를 맞춘다. 공개 주소는 대소문자를 구분한다 |
| **페이지 열기**를 누르면 404 | `link` 값이 실제 파일 이름과 다르다. `index.html`·`about.html`·`guestbook.html` 철자를 본다 |
| 카드가 흰 상자로 안 보인다 | `article.classList.add('card')` 줄이 빠졌거나 철자가 틀렸다. `styles.css`는 고치지 않는다 |
| 페이지에 아무 변화가 없다 | `projects.js` 마지막 줄 `loadProjects();`가 있는지 본다 |
| `git push` 뒤 `Permission to student01/my-web.git denied to <다른 아이디>` | 공용 PC에 이전 사용자 로그인이 남아 있다. **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 제거하고 다시 push한다 |

한 번에 한 곳만 고치고 다시 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://<아이디>.github.io/my-web/projects.html`에서 다음이 한 화면에 보이게 찍는다.

1. 카드 3장에 그림·제목·설명과 **페이지 열기** 링크
2. **F12 › Network** 탭의 `projects.json` **Status 200**
3. 주소창(공개 주소가 보여야 한다)

완료 기준은 공개 주소에서 카드 3장이 JSON 파일에서 읽혀 나오는 것이다.
카드가 제목·설명만 있고 그림·링크가 없으면 부분 통과다. 캡처에 이메일·실명이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- `data/projects.json`에 네 번째 항목을 더해 보고, 카드가 저절로 4장이 되는지 본다. 코드는 고치지 않는다.
- 카드 제목 아래에 만든 날짜를 넣어 본다. `projects.json`에 `"date"`를 더하고 `p` 하나를 더 만들면 된다.
- `data/projects.json`의 내용을 `[]`(빈 배열)로 바꿔 보고 화면이 어떻게 되는지 본다. 빈 화면 대신 안내 문장을 넣으려면 어디에 `if`를 넣어야 할지 생각해 본다.
- **Network** 탭에서 `projects.json`을 눌러 **Response** 탭을 열어 보고, 내 파일과 같은 글자인지 확인한다.

추가 과제는 선택 사항이다.
