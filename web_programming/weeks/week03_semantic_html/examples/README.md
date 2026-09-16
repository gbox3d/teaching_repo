# 3주차 예제 — 세 페이지 자기소개 사이트

2주차 `my-web`에서 이어지는 파일이다. 아래 파일은 해당 날짜 끝의 **`my-web` 전체 파일**이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/index.html](day1/index.html) | [2~5단계](../walkthrough.md#2-indexhtml-비우고-뼈대-만들기) — 2주차 내용을 지우고 뼈대부터 다시 쓴다 | `index.html` |
| [day1/images/profile.png](day1/images/profile.png) | [4단계](../walkthrough.md#4-프로필-그림과-nav-링크-넣기) — 내려받아 `images/`에 넣는다 | `images/profile.png` |
| [day1/about.html](day1/about.html) | [6단계](../walkthrough.md#6-stylescss와-appjs는-그대로-둔다) — 1일차에는 2주차 그대로 둔다 | `about.html` |
| [day1/styles.css](day1/styles.css) · [day1/app.js](day1/app.js) | [6단계](../walkthrough.md#6-stylescss와-appjs는-그대로-둔다) — 열지 않는다. 2주차와 같다 | `styles.css` · `app.js` |
| [day2/about.html](day2/about.html) | [9단계](../walkthrough.md#9-abouthtml을-내-정보-표로-다시-쓰기) — 전체를 지우고 표로 다시 쓴다 | `about.html` |
| [day2/guestbook.html](day2/guestbook.html) | [10단계](../walkthrough.md#10-guestbookhtml-만들기) — 새 파일 | `guestbook.html` |
| [day2/index.html](day2/index.html) | [11단계](../walkthrough.md#11-세-페이지-nav-통일하기) — day1에서 `nav` 한 줄이 늘어난다 | `index.html` |
| [day2/styles.css](day2/styles.css) · [day2/app.js](day2/app.js) | day1과 같다. 이번 주에는 고치지 않는다 | `styles.css` · `app.js` |

`day2/images/profile.png`도 `day1`과 같은 파일이다.

## 1. 1일차 완성 — 자기소개 페이지

`day1/index.html`을 브라우저로 열면 꾸미지 않은 화면이 위에서 아래로 쌓인다.

```text
student01의 웹 연습장      ← header > h1
홈  내 정보                ← header > nav > a 두 개
소개                       ← main > h2
[프로필 그림]              ← img src="images/profile.png" alt="…"
웹프로그래밍을 배우는 student01입니다.   ← p + strong
취미                       ← h2
• 사진 찍기 • 보드게임 • 저녁 산책        ← ul > li 세 개
수업용 연습 페이지 · student01            ← footer > p
```

- `<link rel="stylesheet">`와 `<script src="app.js" defer>` 두 줄이 없다. 그래서 2주차의 카드 모양이 사라진다.
- `styles.css`·`app.js`는 폴더에 그대로 있다. 4·5주차에 비우고 다시 쓴다.
- `day1/about.html`은 2주차 파일 그대로여서 혼자 카드 화면으로 보인다. 2일차에 다시 쓴다.

### 개념별 최소 코드

뼈대 네 개:

```html
<body>
  <header>…</header>
  <main>…</main>
  <footer>…</footer>
</body>
```

상대 경로 링크와 그림:

```html
<a href="about.html">내 정보</a>
<img src="images/profile.png" alt="student01의 프로필 그림" width="160">
```

`href`에 파일 이름만 적으면 같은 폴더의 파일을 연다. `img`의 경로가 틀리면 그림 대신 `alt` 글자가 보인다.

## 2. 2일차 완성 — 내 정보 표와 방명록 form

`day2/`는 day1에 `guestbook.html`이 추가되고, `about.html`이 다시 쓰이고, `index.html`의 `nav`에 한 줄이 늘어난 것이다.

```html
<a href="guestbook.html">방명록</a>
```

`day2/about.html`의 표:

```text
항목      내용            ← th 두 개 (굵게·가운데)
아이디    student01       ← td 두 개
이메일    student01@example.com
관심 분야  웹 페이지 만들기
```

`day2/guestbook.html`의 입력 칸:

```html
<label for="name">이름</label>
<input id="name" type="text">
```

- `label for`와 `input id`가 같아서 `이름`을 누르면 입력 칸에 커서가 들어간다.
- `form`에 `action`·`method`가 없다. **남기기**를 누르면 주소창이 `guestbook.html?`로 바뀌고 화면은 그대로다.
- 여기 쓴 `id`(`name`·`email`·`message`)는 7주차에 JavaScript가 그대로 쓴다. 철자를 바꾸지 않는다.

## 3. 세 페이지와 메뉴

| 페이지 | 제목(`h1`) | 안에 있는 것 |
|---|---|---|
| `index.html` | student01의 웹 연습장 | 그림, 소개 문단, 취미 `ul` |
| `about.html` | 내 정보 | 2열 4행 `table` |
| `guestbook.html` | 방명록 | 쓰는 순서 `ol`, 이름·이메일·메시지 `form` |

세 페이지의 `nav`는 글자 단위로 같다. 한 페이지에서 메뉴를 고치면 나머지 두 페이지도 같이 고친다.

## 공식 참고 자료

- [HTML 문서와 웹사이트 구조 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/Structuring_documents)
- [HTML 표 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/HTML_table_basics)
- [첫 HTML 폼 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Extensions/Forms/Your_first_form)
