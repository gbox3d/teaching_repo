# 12주차 — fetch로 JSON 불러오기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud

## 이번 주 질문

> 화면에 쓸 내용을 HTML 안에 직접 적지 않고, **따로 만든 파일에서 읽어 와** 카드로 그릴 수 있을까?

11주차에는 방명록 항목을 객체로 만들고 `JSON.stringify`로 문자열로 바꿔 `localStorage`에 저장했다.
그 저장 칸에 들어 있던 글자 모양(`[{"name":"하늘",…}]`)을 이번에는 **파일**로 만든다.
`data/projects.json`에 프로젝트 3개를 적어 두고, `fetch`로 그 파일을 읽어 `projects.html`에 카드로 그린다.

**이번 주도 확인과 캡처는 공개 주소에서만 한다.** 내 PC에서 파일을 직접 연 화면(`file://`)에서는 `fetch`가 막혀 카드가 하나도 보이지 않는다.

## 학습 목표

1. `data/projects.json` 파일에 `{ "title": …, "description": … }` 객체 3개를 적고 **큰따옴표 규칙**을 지킨다.
2. `async function loadProjects()` 안에서 `await fetch('data/projects.json')`로 파일을 읽는다.
3. `await response.json()`으로 읽어 온 값을 배열로 바꾸고 `console.log`로 확인한다.
4. 10주차의 고전 `for`와 `createElement`로 `article` 카드를 만들어 그림·제목·설명·링크를 넣는다.
5. `try / catch`와 `response.ok`로 파일을 못 읽었을 때 `프로젝트를 불러오지 못했습니다.`를 보여 준다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/my-web/projects.html
         카드 3개가 보이고 F12 › Network 탭에 projects.json 200이 함께 보이는 화면

         지금까지 만든 것
         ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
         │ [그림]        │  │ [그림]        │  │ [그림]        │
         │ 자기소개 페이지 │  │ 내 정보 표     │  │ 방명록        │
         │ 홈 화면입니다… │  │ 아이디와 이메일… │  │ 이름과 메시지… │
         │ 페이지 열기    │  │ 페이지 열기    │  │ 페이지 열기    │
         └──────────────┘  └──────────────┘  └──────────────┘
         Name: projects.json   Status: 200   Type: fetch
         ← 주소창이 함께 보이게 찍는다
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 제출은 이 캡처 **한 장**이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 오늘 도구 5분(Pages에서 먼저 보기), JSON 파일과 큰따옴표, `loadProjects()` 틀, `file://`에서 나는 Console 오류 | `data/projects.json` 3개 → `projects.html`·`projects.js` → `console.log` → 카드 그리기 → push해서 공개 주소에서 확인 | 확인용 캡처 |
| 2일차 | `try / catch`와 안내 문구, `response.ok`와 404, 카드에 `img`·`a`와 `.card` 재사용, 14주 최종 과제 공지 | 안내 문구 → 카드 완성 → nav에 프로젝트 링크 → Network 탭 확인 → push·캡처 | 캡처 1 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 11주차까지 push한 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 이번 주에 새로 만드는 파일은 `projects.html`·`projects.js`·`data/projects.json`과 카드 그림 세 장이다
- 브라우저 개발자 도구의 **Console** 탭과 **Network** 탭 (**F12** 또는 우클릭 › 검사)
- 본인 GitHub Pages 공개 주소. **확인과 캡처는 이 주소에서만 한다**
- (선택) 로컬 미리보기용 VS Code 확장 **Live Server**. 설치가 막히면 미리보기 없이 push해서 공개 주소로 확인해도 이번 주 실습은 그대로 끝난다
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 데이터 파일 | JSON file | JSON 文件 |
| 불러오기 | fetch | 获取 |
| 기다리기 | await | 等待 |
| 응답 | response | 响应 |
| 응답이 정상인가 | response.ok | 响应是否正常 |
| 오류를 받아 두기 | try / catch | 捕获错误 |
| 카드 | card (article) | 卡片 |
| 로컬 서버 | local server | 本地服务器 |

## 이번 주 범위

| 태그·API | 이번 주에 알아둘 뜻 |
|---|---|
| `data/projects.json` | 화면에 쓸 내용만 따로 적어 둔 **데이터 파일**. 11주차 Application 탭에서 본 글자 모양과 같다 |
| JSON의 큰따옴표 | 이름과 문자열 값에 **큰따옴표 `"`만** 쓴다. 작은따옴표와 마지막 쉼표는 오류가 된다 |
| `async function loadProjects() { }` | 안에서 `await`를 쓸 수 있는 함수. **복붙 틀**이며 `async`와 `await`는 짝으로 쓴다 |
| `await fetch('data/projects.json')` | 그 파일을 달라고 요청하고 **응답이 올 때까지 기다린다**. 경로는 `projects.html`이 있는 곳 기준의 상대 경로다 |
| `await response.json()` | 응답의 내용을 배열·객체로 바꾼다. 여기서도 기다려야 한다 |
| `console.log(projects)` | 읽어 온 값을 Console에 찍어 배열인지, 몇 개인지 눈으로 본다 |
| `response.ok` | 응답이 정상(200)이면 `true`, 404 같으면 `false`다 |
| `try { } catch (error) { }` | 안쪽에서 오류가 나면 멈추지 않고 `catch` 쪽으로 넘어간다. 안내 문구를 여기서 보여 준다 |
| `<div id="project-list"></div>` | 카드를 담아 둘 **빈 상자**. 10주차 `<ul id="list">` 자리와 같은 역할이고, 목록이 아니라 카드를 넣으므로 `div`를 쓴다 |
| `document.createElement('article')` | 카드 한 장이 될 요소를 만든다. `classList.add('card')`로 4주차 `.card` 모양을 그대로 쓴다 |
| `image.src` · `image.alt` · `image.width` | 만든 `img`에 그림 주소·대체 글·너비를 넣는다 |
| `link.href` · `link.textContent` | 만든 `a`에 이동할 주소와 보일 글자(`페이지 열기`)를 넣는다 |
| **F12 › Network** | 페이지가 어떤 파일을 받아 왔는지 보는 탭. `projects.json`의 **Status 200**이 제출 캡처에 함께 들어간다 |

`file://`로 연 화면에서는 `fetch`가 막힌다. 서버에 올라간 주소(공개 주소·Live Server)에서만 동작한다.
서버에 저장해 여러 사람이 함께 고치는 것(데이터베이스·로그인)은 이 과목의 선택 특강이다. `Promise.then`·`import`/`export`는 쓰지 않는다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week12_persistent_crud/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [projects.html](examples/day1/projects.html) · [projects.js](examples/day1/projects.js) · [data/projects.json](examples/day1/data/projects.json) · [index.html](examples/day1/index.html) · [styles.css](examples/day1/styles.css)
- 2일차 완성 코드: [projects.html](examples/day2/projects.html) · [projects.js](examples/day2/projects.js) · [index.html](examples/day2/index.html) · [about.html](examples/day2/about.html) · [guestbook.html](examples/day2/guestbook.html)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud

## 완료 기준

- [ ] 공개 주소 `https://<아이디>.github.io/my-web/projects.html`이 열린다.
- [ ] 카드 3개에 그림·제목·설명과 **페이지 열기** 링크가 보이고, 링크를 누르면 그 페이지로 간다.
- [ ] 네 페이지(`index.html`·`about.html`·`guestbook.html`·`projects.html`)의 nav에 링크 네 개가 모두 있다.
- [ ] **F12 › Network**에 `projects.json`이 **200**으로 보인다.
- [ ] `data/projects.json` 파일 이름을 일부러 틀리게 하면 `프로젝트를 불러오지 못했습니다.`가 화면에 보인다.
- [ ] (파일 이름을 되돌린 뒤) F12 Console에 빨간 줄이 없다.
- [ ] 카드 3개와 Network 탭이 함께 보이는 화면을 캡처 1장으로 제출한다.

## 다음 수업 연결

이제 화면에 쓸 내용이 HTML 밖의 파일에 있고, 그 파일을 읽어 카드로 그린다.
13주차에는 지금까지 만든 네 페이지를 점검한다. 입력한 글자를 그대로 보여 주는 `textContent`, 그림의 `alt`, 폼의 `label for`를 다시 보고
`about.js`로 입학 연도를 계산해 넣은 뒤 저장소 `README.md` 최종판과 `screenshots/` 3장을 정리한다.

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
- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
