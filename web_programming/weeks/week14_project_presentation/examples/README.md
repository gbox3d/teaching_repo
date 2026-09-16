# 14주차 예제 — 발표할 사이트와 README 최종판

13주차 `my-web`에서 이어지는 파일이다. 아래 파일은 해당 날짜 끝의 **`my-web` 전체 파일**이다.
이번 주에는 CSS와 JavaScript를 고치지 않는다. 바뀌는 것은 `index.html`·`about.html`·`README.md` 세 파일뿐이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/index.html](day1/index.html) | [3단계](../walkthrough.md#3-홈에-할-수-있는-것-목록-넣기) — `<h2>`와 `<ol>` 다섯 줄을 더한다 | `index.html` |
| [day1/about.html](day1/about.html) | [4단계](../walkthrough.md#4-내-정보-표에-공개-주소-한-줄-넣기) — 표에 `<tr>` 한 행을 더한다 | `about.html` |
| [day1/README.md](day1/README.md) | [5단계](../walkthrough.md#5-readme-최종판-마무리하기) — 13주차 최종판에 두 곳을 고친다 | `README.md` |
| [day1/screenshots/home.png](day1/screenshots/home.png) | [5단계](../walkthrough.md#5-readme-최종판-마무리하기) — 홈이 바뀌었으므로 다시 찍는다 | `screenshots/home.png` |
| [day1/screenshots/guestbook.png](day1/screenshots/guestbook.png) · [day1/screenshots/projects.png](day1/screenshots/projects.png) | 13주차에 찍은 것 그대로 둔다 | `screenshots/` |
| [day1/styles.css](day1/styles.css) · [day1/app.js](day1/app.js) · [day1/about.js](day1/about.js) · [day1/guestbook.js](day1/guestbook.js) · [day1/projects.js](day1/projects.js) · [day1/guestbook.html](day1/guestbook.html) · [day1/projects.html](day1/projects.html) · [day1/data/projects.json](day1/data/projects.json) | [이번 주에 고치지 않는 파일](../walkthrough.md#이번-주에-고치지-않는-파일) — 열어서 동작만 확인한다 | 그대로 |
| [day2/](day2/)의 모든 파일 | day1과 같다. 2일차는 발표뿐이라 파일이 바뀌지 않는다 | 그대로 |

`day1/images/`의 네 그림은 3주차·12주차에 넣은 것 그대로다.

## 1. 1일차에 바뀌는 세 곳

### 홈 — 할 수 있는 것 목록 (`index.html`, 42줄 → 50줄)

`<p class="card" id="count">` 줄 아래에 여덟 줄을 더한다.

```html
<h2>이 사이트에서 할 수 있는 것</h2>
<ol class="card">
  <li>위 메뉴로 네 페이지를 오갑니다.</li>
  <li>버튼으로 인사말과 배경색을 바꿉니다.</li>
  <li>방명록에 글을 남기고 지웁니다.</li>
  <li>남긴 글은 새로고침해도 그대로 있습니다.</li>
  <li>프로젝트 카드는 JSON 파일에서 읽어 옵니다.</li>
</ol>
```

- 다섯 줄의 **순서가 곧 발표 순서**다. [3분 시연 흐름 표](demo_outline.md)의 **둘째 줄부터 일곱째 줄**과 같다.
- 0:55 빈값 안내와 1:15 남기기·삭제가 "방명록에 글을 남기고 지웁니다" 한 줄로 묶여 여섯 줄이 다섯 줄이 된다.
- 발표 중에 다음에 할 일을 화면에서 볼 수 있다. 종이를 들고 읽지 않아도 된다.
- 쓰는 태그는 `h2`·`ol`·`li`뿐이다. 모두 3주차에 배운 것이고 `class="card"`는 4주차 것이다.

### 내 정보 — 공개 주소 행 (`about.html`, 55줄 → 59줄)

표의 `관심 분야` 행 아래에 네 줄을 더한다.

```html
<tr>
  <td>공개 주소</td>
  <td>https://student01.github.io/my-web/</td>
</tr>
```

- 발표 첫 20초에 채점자가 여는 주소를 화면으로 보여 주기 위한 것이다.
- 링크로 만들지 않고 글자로 적는다. 자기 페이지를 자기 페이지로 다시 여는 링크는 필요 없다.

### README — 두 곳 (`README.md`, 51줄 → 52줄)

- `## 페이지`의 홈 설명에 `할 수 있는 것 목록`을 넣는다.
- `## 만든 과정 (git log --oneline)`의 맨 위에 이번 주 commit 한 줄을 더한다.

```markdown
- 9b2f7c1 홈에 할 수 있는 것 목록 넣고 내 정보에 공개 주소 적기
```

앞의 일곱 글자는 PC마다 다르다. `git log --oneline`에서 **본인 값**을 옮겨 적는다.

## 2. 발표에서 보여 줄 화면

`day1/screenshots/home.png`가 **[인사 바꾸기]**를 한 번 누른 뒤의 홈 화면이다.

```text
student01의 웹 연습장
홈  내 정보  방명록  프로젝트
반갑습니다. 오늘도 좋은 하루 되세요.     ← 버튼을 눌러 바뀐 문장
[인사 바꾸기] [다크 모드]
클릭 1회                                 ← 눌러 본 것이 보인다
이 사이트에서 할 수 있는 것 1~5          ← 이번 주에 넣은 목록 = 발표 순서
소개 · 프로필 그림 · 취미 세 줄
```

`day1/screenshots/guestbook.png`는 글 세 줄이 쌓인 방명록, `day1/screenshots/projects.png`는 카드가 그려진 프로젝트 화면이다(창 높이에 카드 세 장 중 위 두 장까지 들어왔다).
세 장 모두 **동작한 뒤의 화면**이다. `클릭 0회`·`아직 남긴 글이 없습니다.`인 채로 찍지 않는다.

- 방명록 목록과 프로젝트 카드는 공개 주소에서 찍는다. 파일을 더블클릭해 연 화면은 저장되는 곳이 다르고, 카드는 그려지지도 않는다.
- 캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 아이디는 보여도 된다.

## 3. 두 날의 파일 비교

| | 13주차 끝 | 14주차 1일차 끝 | 14주차 2일차 끝 |
|---|---|---|---|
| `index.html` | 42줄 | **50줄** (할 수 있는 것 목록) | 같음 |
| `about.html` | 55줄 | **59줄** (공개 주소 행) | 같음 |
| `README.md` | 51줄 | **52줄** (commit 한 줄 추가) | 같음 |
| `screenshots/home.png` | 13주차 것 | **다시 찍음** | 같음 |
| 그 밖의 파일 | 있음 | 같음 (고치지 않음) | 같음 |

`day2/`는 `day1/`과 파일이 모두 같다. 2일차는 90분 전체가 발표이므로 `my-web`에 바뀌는 파일이 없다.

## 공식 참고 자료

- [ol 요소 — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/ol)
- [table 요소 — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/table)
- [README 정보 — GitHub Docs](https://docs.github.com/ko/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
