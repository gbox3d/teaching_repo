[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud)

# 12주차 — fetch로 JSON 불러오기

이번 주도 부품을 하나씩 본다. 비교 예제 6개를 열어 값을 바꿔 보고, 마지막에 이번 주 새 저장소 `web-week12` 에 `data/projects.json`·`projects.html`·`projects.js` 를 그 부품으로 조립한다.
11주차에는 방명록 글을 브라우저 저장소에 넣었다. 이번 주에는 화면에 쓸 내용을 **파일**에 적어 두고, `fetch` 로 그 파일을 읽어 와 카드로 그린다.
결과는 화면과 **F12 › Console**, 그리고 이번 주에 처음 쓰는 **F12 › Network** 탭에서 본다. 파일 하나에 개념 하나. 다른 파일의 개념은 섞지 않는다.

## 이번 주 질문

> 화면에 쓸 내용을 HTML 에 직접 적지 않고, 따로 둔 파일에서 읽어 와 카드로 그리려면 무엇을 알아야 하나?

답은 세 가지 원리다.
JSON 은 **글자**다. 이름과 문자열 값을 큰따옴표로 감싸는 규칙을 지킨 글자만 배열·객체로 바뀐다(11주차 `JSON.parse` 와 같다).
`fetch` 는 파일을 **요청**하고 응답을 기다린다. 요청을 받아 줄 서버가 있는 주소(`http://`·`https://`)에서만 된다. 두 번 눌러 연 화면(`file://`)에서는 막힌다.
파일을 못 읽는 길은 둘이다. 요청이 막히거나 받은 글자를 JSON 으로 읽지 못하면 `catch` 로 가고, 파일이 없어 404 가 오면 `response.ok` 가 `false` 다. 둘 다 화면에 알린다.

## 학습 목표

1. JSON 글자 규칙(이름과 문자열 값은 큰따옴표, 마지막 항목 뒤에 쉼표 없음)을 지켜 `data/projects.json` 에 객체 3개를 적는다. 규칙을 어기면 빨간 줄이 뜨는 것을 확인한다.
2. `async function loadProjects()` 안에서 `await fetch('…')` 로 파일을 요청하고 `await response.json()` 으로 배열을 받는다. **Network** 탭에서 요청 한 줄과 Status 200 을 본다.
3. 두 번 눌러 연 화면(`file://`)에서는 `fetch` 가 막히고, 서버 주소(`http://localhost:8000/`)와 공개 주소에서는 된다는 것을 주소창과 Console 문구로 구분한다.
4. 10주차 `for` 와 `createElement` 로 `article` 카드를 만들어 `img`·`h3`·`p`·`a` 를 넣고 `.card` class 를 붙인다.
5. `try / catch` 와 `response.ok` 로 파일을 못 읽었을 때 화면에 `프로젝트를 불러오지 못했습니다.` 를 보여 준다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/web-week12/projects.html
         프로젝트 ─ 지금까지 만든 것
         카드 ─ [그림] 자기소개 페이지 · 홈 화면입니다. … · 페이지 열기
         카드 ─ [그림] 내 정보 표 · 아이디와 이메일, … · 페이지 열기
         카드 ─ [그림] 방명록 · 이름과 메시지를 남기면 … · 페이지 열기
         F12 › Network ─ projects.json   200   fetch
         ← 주소창이 함께 보이게 찍는다
```

- 제출은 이 캡처 **한 장**이다. 카드 3장과 Network 탭의 `projects.json` **200** 이 한 화면에 보여야 한다.
- 확인과 캡처는 **공개 주소에서** 한다. `web-week12/ex/` 에 비교 예제를 저장하고 값을 바꾼 것은 push 로 남긴다. 기록물·표는 없다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 고르기 페이지와 서버로 열기 → ex01 JSON 글자 규칙 → ex02 fetch 틀과 Network 탭 → ex03 `file://` 과 `http://` | 새 폴더 `web-week12` 에 지난주 완성본과 `server.mjs` 넣기 → `ex/` 에 여섯 파일 저장 → 서버로 열어 값 바꿔 보기 → 새 저장소 만들어 올리기 · Pages 켜기 | `ex/` 비교 예제(확인용) |
| 2일차 | ex04 카드 만들기 → ex05 `try / catch` → ex06 `response.ok` → 14주차 최종 과제 안내 → 조립표 | 아홉 파일 값 바꿔 보기 → `data/projects.json`·`projects.html`·`projects.js` 조립, nav 네 페이지 → 서버와 375·1280 폭으로 확인 → push → 공개 주소에서 Network 200 | 캡처 1 |

각 수업은 `설명·시연 30분 + 실습 60분` 이다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.

## 준비

- 지난주 완성본. 내 `web-week11` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [11주차 `examples/day2/web-week11/`](../week11_auth_rls/examples/day2/web-week11/) 파일을 **Raw** 로 받는다
- VS Code, Chrome(DevTools), Git (`git --version` 으로 확인)
- Node.js LTS(`node -v` 로 확인)와 [server.mjs](../../tools/static-server/server.mjs)([사용 안내](../../tools/static-server/README.md)). 이번 주 예제는 `fetch` 가 있어서 **서버로 연다**. Node 가 없는 PC 는 저장소를 먼저 올리고 공개 주소에서 확인한다(push 할 때마다 1~3분 기다린다)
- 개발자 도구의 **Console** 탭과 **Network** 탭 위치(오른쪽 클릭 › **검사**, 또는 **F12**)
- 11주차에 **Application › Local Storage** 에서 본 `guestbook` 값의 모양(`[{"name":…}]`)을 기억해 둔다. 이번 주 JSON 파일이 같은 모양이다
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| JSON 파일 | JSON file | JSON 文件 |
| 파일 요청하기 | fetch | 获取（请求文件） |
| 기다리기 | await | 等待 |
| 비동기 함수 | async function | 异步函数 |
| 응답 | response | 响应 |
| 정상 응답인가 | response.ok | 响应是否正常 |
| 오류 받기 | try / catch | 捕获错误 |
| 네트워크 탭 | Network panel | 网络面板 |

## 이번 주 비교 예제

1일차 ex01~ex03 은 같은 화면(글자 자리 하나)을 쓰므로 코드만 `.js` 파일에 두고, 고르기 페이지 [day1/index.html](examples/day1/index.html) 맨 아래 `<script src>` 세 줄 중 하나만 켜서 연다. 2일차 ex04~ex06 은 화면이 서로 달라서 `.html` 과 `.js` 를 한 쌍으로 둔다. `fetch` 가 읽는 `.json` 파일과 ex04 의 그림은 같은 폴더에 둔다. Console 의 번호가 코드의 형제 번호와 같다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_json_rule.js](examples/day1/ex01_json_rule.js) | 1. 큰따옴표 / 2. 작은따옴표 / 3. 마지막 쉼표 | JSON 은 글자다. 규칙을 지킨 글자만 `JSON.parse` 가 배열로 바꾼다 | 2·3번 주석 풀기 → 빨간 줄, `"title"` 의 따옴표 지우기 |
| [ex02_fetch.js](examples/day1/ex02_fetch.js) + [ex02_projects.json](examples/day1/ex02_projects.json) | 1. `await fetch` 의 응답 / 2. `await response.json()` 의 배열 | `fetch` 는 파일을 요청해 응답을 받고, `json()` 은 그 글자를 배열로 바꾼다. 두 줄 모두 기다린다 | `.json` 의 제목 바꾸기, `await` 하나 지우기, 마지막 줄 `loadProjects();` 지우기 |
| [ex03_file_http.js](examples/day1/ex03_file_http.js) + [ex03_projects.json](examples/day1/ex03_projects.json) | 서버 주소로 연 페이지 / 두 번 눌러 연 페이지 | 코드는 같고 주소가 다르다. `file://` 에서는 `fetch` 가 막혀 그 줄 아래가 실행되지 않는다 | 두 가지로 열어 화면 번호와 Console 비교 |
| [ex04_cards.html](examples/day2/ex04_cards.html) + [.js](examples/day2/ex04_cards.js) | 카드 안의 1. `img` / 2. `h3` / 3. `p` / 4. `a` | 배열의 항목 하나가 `article` 카드 한 장이 된다. `append` 에 넣은 순서대로 쌓인다 | `append` 순서, `classList.add('card')` 지우기, 없는 그림 이름 |
| [ex05_try_catch.html](examples/day2/ex05_try_catch.html) + [.js](examples/day2/ex05_try_catch.js) | 1. `try` 를 끝까지 / 2. `catch` 로 넘어감 | `try` 안에서 오류가 나면 페이지가 멈추지 않고 `catch` 로 가서 화면에 알린다 | 두 가지로 열기, `.json` 에 작은따옴표 넣기, `catch` 비우기 |
| [ex06_response_ok.html](examples/day2/ex06_response_ok.html) + [.js](examples/day2/ex06_response_ok.js) | 1. 있는 파일(200) / 2. 없는 파일(404) | 파일이 없어도 서버는 404 를 답한다. 그래서 읽기 전에 `response.ok` 로 묻는다 | 2번 줄 켜기, `if` 블록 지우기, 파일 이름 앞에 `/` |

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week12_persistent_crud/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(고르기 페이지 `index.html`, ex01~ex03 의 `.js`, ex02·ex03 의 `.json`), 2일차 `day2/`(ex04~ex06 의 `.html`·`.js`, 그림과 `.json`, 조립 `web-week12/`)
- 2일차 끝의 `web-week12`(조립 결과): [projects.html](examples/day2/web-week12/projects.html) · [projects.js](examples/day2/web-week12/projects.js) · [data/projects.json](examples/day2/web-week12/data/projects.json) · [index.html](examples/day2/web-week12/index.html) · [about.html](examples/day2/web-week12/about.html) · [guestbook.html](examples/day2/web-week12/guestbook.html) · [images/](examples/day2/web-week12/images/)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud

## 완료 기준

- [ ] 새 저장소 `web-week12` 를 만들어 Pages 를 켰고, `ex/` 에 비교 예제가 있고, 각 예제에서 값을 하나 이상 바꿔 push 했다.
- [ ] `data/projects.json` 에 객체 3개가 있고 이름표가 `title`·`description`·`image`·`link` 다. VS Code 에 빨간 밑줄이 없다.
- [ ] `projects.html` 에 `<div id="notice">` 와 `<div id="project-list">` 가 있고, 네 페이지(`index.html`·`about.html`·`guestbook.html`·`projects.html`)의 nav 에 링크 네 개가 있다.
- [ ] 공개 주소 `https://student01.github.io/web-week12/projects.html` 에서 카드 3장에 그림·제목·설명·**페이지 열기**가 보이고, **F12 › Network** 에 `projects.json` 이 **200** 이다. Console 에 `Uncaught` 빨간 줄이 없다.
- [ ] `data/projects.json` 의 이름을 잠깐 틀리게 하면 화면에 `프로젝트를 불러오지 못했습니다.` 가 보인다(확인한 뒤 되돌렸다).
- [ ] 카드 3장과 Network 탭이 함께 보이고 주소창이 보이는 캡처 1장을 제출한다.

## 다음 수업 연결

오늘은 HTML 밖의 파일에서 내용을 읽어 카드로 그렸다. 13주차에는 새 저장소 `web-week13` 을 오늘 `web-week12` 의 파일에서 시작하고(**Code › Download ZIP**, 못 받으면 교재의 이번 주 [`examples/day2/web-week12/`](examples/day2/web-week12/)), 지금까지 만든 네 페이지를 점검한다.
입력한 글을 `textContent` 로 넣는지(보안), 그림의 `alt` 와 입력 칸의 `label for` 가 있는지(접근성)를 보고, 저장소 `README.md` 를 최종판으로 정리한다. 오늘 카드에 넣은 `alt` 를 13주차에 다시 본다.
14주차는 최종 발표다. 2일차에 안내한 필수 기능이 그대로 발표 내용이 된다.

## 공식 참고 자료

- [Fetch API 사용하기 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- [fetch() 전역 함수 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Window/fetch)
- [Response.json() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Response/json)
- [Response.ok — MDN](https://developer.mozilla.org/ko/docs/Web/API/Response/ok)
- [async function — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/async_function)
- [await — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/await)
- [try...catch — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/try...catch)
- [JSON — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/JSON)
- [CORS 오류: Cross origin requests are only supported for HTTP — MDN](https://developer.mozilla.org/ko/docs/Web/HTTP/Guides/CORS/Errors/CORSRequestNotHttp)
- [네트워크 활동 검사(Network 패널) — Chrome DevTools](https://developer.chrome.com/docs/devtools/network?hl=ko)
