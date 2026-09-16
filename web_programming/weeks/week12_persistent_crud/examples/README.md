# 12주차 예제 — JSON 파일을 읽어 그리는 프로젝트 카드

`day1/`·`day2/`는 그날 수업이 끝났을 때의 **`my-web` 폴더 전체**다. 그 주에 고치지 않은 파일도 함께 들어 있다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

**이 예제는 파일을 더블클릭해서 열면 카드가 보이지 않는다.** `fetch`는 `file://`에서 막힌다.
공개 주소(GitHub Pages)나 로컬 서버(Live Server, `python3 -m http.server 8000`)로 열어야 한다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/data/projects.json](day1/data/projects.json) | [2단계](../walkthrough.md#2-data-폴더와-projectsjson-만들기) | `data/projects.json` |
| [day1/images/project1.png](day1/images/project1.png) · [project2.png](day1/images/project2.png) · [project3.png](day1/images/project3.png) | [3단계](../walkthrough.md#3-카드-그림-세-장-넣기) | `images/project1.png` · `project2.png` · `project3.png` |
| [day1/projects.html](day1/projects.html) | [4단계](../walkthrough.md#4-projectshtml-만들기) | `projects.html` |
| [day1/projects.js](day1/projects.js) | [5단계](../walkthrough.md#5-projectsjs로-json-불러오기) | `projects.js` |
| [day2/projects.html](day2/projects.html) | [8단계](../walkthrough.md#8-안내-문구-자리-만들기) — day1에 `<p id="notice">`와 nav 링크가 늘어난다 | `projects.html` |
| [day2/projects.js](day2/projects.js) | [9~11단계](../walkthrough.md#11-카드에-그림과-링크-넣기) | `projects.js` |
| [day2/index.html](day2/index.html) · [about.html](day2/about.html) · [guestbook.html](day2/guestbook.html) | [12단계](../walkthrough.md#12-nav에-프로젝트-링크-넣기) — nav에 한 줄씩만 늘어난다 | `index.html` · `about.html` · `guestbook.html` |
| [day1/app.js](day1/app.js) · [day1/guestbook.js](day1/guestbook.js) · [day1/styles.css](day1/styles.css) · [day1/README.md](day1/README.md) · [day1/screenshots/](day1/screenshots) · [day1/images/profile.png](day1/images/profile.png) | 이번 주에 고치지 않는다 (11주차와 같다) | `app.js` · `guestbook.js` · `styles.css` · `README.md` · `screenshots/` · `images/profile.png` |

저장소 `README.md`와 `screenshots/`는 13주차 최종판에서 프로젝트 페이지를 포함해 다시 쓴다. 이번 주에는 그대로 둔다.

## 1. 데이터 파일 — data/projects.json

```json
[
  {
    "title": "자기소개 페이지",
    "description": "홈 화면입니다. 이름과 소개, 취미 목록을 적었습니다.",
    "image": "images/project1.png",
    "link": "index.html"
  }
]
```

- 대괄호 `[ ]` 안에 중괄호 `{ }` 객체를 쉼표로 이어 **3개** 적는다.
- 이름(`"title"`)과 문자열 값에 **큰따옴표만** 쓴다. 작은따옴표·마지막 쉼표는 오류다.
- `image`와 `link`의 값은 `projects.html`이 있는 곳에서 본 **상대 경로**다.

## 2. 1일차 완성 — 제목과 설명만 있는 카드

`day1/projects.js`는 파일을 읽어 카드를 그리는 가장 작은 모양이다.

```js
async function loadProjects() {
  const response = await fetch('data/projects.json');
  const projects = await response.json();
  console.log(projects);
  showProjects(projects);
}
```

공개 주소나 로컬 서버에서 `projects.html`을 열면 이렇게 보인다.

```text
지금까지 만든 것
아래 카드는 data/projects.json 파일에서 읽어 옵니다.

┌ 자기소개 페이지 ────────────────────────┐
│ 홈 화면입니다. 이름과 소개, 취미 목록을… │
└─────────────────────────────────────────┘
(같은 모양의 카드가 3장)
```

Console에는 `console.log(projects)`가 찍은 배열이 한 줄로 보이고, 펼치면 `title`·`description`·`image`·`link`가 들어 있다.

## 3. 2일차 완성 — 그림·링크와 안내 문구

`day2/projects.js`는 day1에 세 가지가 늘어난 것이다.

| 늘어난 것 | 코드 |
|---|---|
| 그림 | `image.src = projects[i].image;` · `image.alt = ...` · `image.width = 240;` |
| 링크 | `link.href = projects[i].link;` · `link.textContent = '페이지 열기';` |
| 오류 안내 | `try { } catch (error) { }`와 `if (!response.ok) { … return; }` |

```js
if (!response.ok) {
  notice.textContent = '프로젝트를 불러오지 못했습니다.';
  return;
}
```

`data/projects.json`의 이름을 일부러 `project.json`으로 바꿔 두고 열면 카드 대신 이 문장이 보인다.

```text
지금까지 만든 것
아래 카드는 data/projects.json 파일에서 읽어 옵니다.
프로젝트를 불러오지 못했습니다.
```

day1 코드로 같은 실험을 하면 화면에는 아무 안내도 없고 Console에만 빨간 줄이 남는다. 그 차이가 2일차의 목표다.

## 4. day1과 day2의 차이

| 파일 | day1 | day2 |
|---|---|---|
| `projects.html` | nav 세 링크, `<div id="project-list">` | nav 네 링크, `<p id="notice">`가 늘어난다 |
| `projects.js` | 24줄. fetch → json → 카드(제목·설명) | 40줄. `try / catch`·`response.ok`·그림·링크 |
| `index.html` · `about.html` · `guestbook.html` | 11주차와 같다 | nav에 `<a href="projects.html">프로젝트</a>` 한 줄씩 |
| `app.js` · `guestbook.js` · `styles.css` | 11주차와 같다 | day1과 같다 |

`styles.css`에는 이번 주에 규칙을 더하지 않았다. 카드는 4주차에 만든 `.card`를 그대로 쓴다.

## 공식 참고 자료

- [Fetch API 사용하기 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- [Response.ok — MDN](https://developer.mozilla.org/ko/docs/Web/API/Response/ok)
- [JSON — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/JSON)
