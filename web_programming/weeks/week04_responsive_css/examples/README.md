# 4주차 예제 — CSS로 꾸민 세 페이지

3주차 `my-web`에서 이어지는 파일이다. 아래 파일은 해당 날짜 끝의 **`my-web` 전체 파일**이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

이번 주에 실제로 바뀌는 것은 `styles.css` 한 파일과, 세 페이지의 `link` 한 줄씩, `index.html`의 `class="card"` 세 곳뿐이다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/styles.css](day1/styles.css) | [2·4·5단계](../walkthrough.md#2-stylescss-비우고-body-규칙-쓰기) — 2주차 내용을 전부 지우고 규칙 여섯 개를 쓴다 | `styles.css` |
| [day1/index.html](day1/index.html) | [3·5단계](../walkthrough.md#3-indexhtml에-link-줄-넣기) — `link` 한 줄 + `class="card"` 세 곳 | `index.html` |
| [day1/about.html](day1/about.html) | [6단계](../walkthrough.md#6-나머지-두-페이지에도-link-줄-넣기) — `link` 한 줄만 늘어난다 | `about.html` |
| [day1/guestbook.html](day1/guestbook.html) | [6단계](../walkthrough.md#6-나머지-두-페이지에도-link-줄-넣기) — `link` 한 줄만 늘어난다 | `guestbook.html` |
| [day1/app.js](day1/app.js) | [7단계](../walkthrough.md#7-appjs는-열지-않는다) — 열지 않는다. 2주차와 같다 | `app.js` |
| [day2/styles.css](day2/styles.css) | [10~13단계](../walkthrough.md#10-메뉴를-가로로-카드를-상자로) — day1에 네 묶음이 늘어난다 | `styles.css` |
| [day2/index.html](day2/index.html) · [day2/about.html](day2/about.html) · [day2/guestbook.html](day2/guestbook.html) | day1과 글자 단위로 같다. 2일차에는 HTML을 고치지 않는다 | 세 페이지 |

`day1/images/profile.png`와 `day2/images/profile.png`는 3주차와 같은 파일이다.

## 1. 1일차 완성 — 색과 글꼴

`day1`의 `index.html`을 브라우저로 열면 3주차와 같은 순서 그대로, 색만 입은 화면이 보인다.

```text
연한 파랑 배경                         ← body { background-color: #eef2ff }
student01의 웹 연습장 (진한 남색·28px)  ← h1
홈  내 정보  방명록 (파랑, 거의 붙어 있다) ← nav a
소개 (파랑)                             ← h2
[프로필 그림]
흰 띠 위의 문단 두 개                    ← p.card { background-color: #ffffff }
취미 (파랑) / 흰 띠 위의 목록 세 개       ← ul.card
수업용 연습 페이지 · student01 (회색·가운데·14px)  ← footer
```

- 아직 `padding`·`border`가 없어서 흰 배경이 **띠처럼** 보인다. 카드 모양은 2일차에 만든다.
- `nav`는 아직 보통 블록이다. 링크 세 개가 공백 한 칸(약 4px)만 두고 거의 붙어 보인다.
- `about.html`·`guestbook.html`도 같은 `styles.css`를 쓰므로 배경·제목·메뉴 색이 같다. 표와 입력 칸은 3주차 모양 그대로다.

### 개념별 최소 코드

연결 한 줄(세 페이지 공통, `<title>` 아래):

```html
<link rel="stylesheet" href="styles.css">
```

규칙의 모양과 선택자 세 가지:

```css
h1 { color: #1f3a93; }
nav a { color: #3157d5; }
.card { background-color: #ffffff; }
```

`h1`은 태그 전부, `nav a`는 `nav` 안의 `a`, `.card`는 HTML에 `class="card"`라고 적어 둔 것만 고른다.
선택자가 한 글자라도 다르면 오류 없이 그 규칙만 통째로 무시된다.

## 2. 2일차 완성 — 박스와 반응형

`day2/styles.css`는 `day1/styles.css`에 네 묶음이 늘어난 것이다. HTML 세 개는 day1과 같다.

| 더한 것 | 어디에 | 화면에서 보이는 것 |
|---|---|---|
| `max-width: 640px` · `margin: 0 auto` · `padding: 16px` | `body` | 본문이 가운데로 모이고 좌우에 여백이 생긴다 |
| `display: flex` · `gap: 16px` · `flex-wrap: wrap` | `nav`(새 규칙) | 메뉴가 한 줄에 16px 간격으로 놓인다 |
| `padding: 16px` · `margin: 12px 0` · `border: 1px solid #c3cbe6` | `.card` | 흰 띠가 테두리 있는 상자가 된다 |
| `width: 280px` · `max-width: 100%` | `input, textarea`(새 규칙) | 방명록 입력 칸 폭이 같아진다 |

파일 맨 끝에는 화면 폭 조건 한 덩어리가 붙는다.

```css
@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}
```

```text
1280px: 홈   내 정보   방명록      ← 한 줄
 375px: 홈
        내 정보
        방명록                     ← 세 줄
```

- 600px이 갈림길이다. 폭을 천천히 줄이면 그 지점에서 메뉴가 바뀐다.
- `input, textarea`처럼 쉼표로 묶으면 한 규칙을 두 대상에 함께 쓴다.
- 두 폭 모두에서 가로 스크롤 막대가 생기지 않는다. `width` 대신 `max-width`를 썼기 때문이다.

## 3. 세 페이지와 규칙

| 페이지 | 이 페이지에만 있는 것 | 이번 주에 바뀐 줄 |
|---|---|---|
| `index.html` | 그림, 소개 문단, 취미 목록 | `link` 1줄 + `class="card"` 3곳 |
| `about.html` | 2열 4행 표 | `link` 1줄 |
| `guestbook.html` | 쓰는 순서 목록, 이름·이메일·메시지 폼 | `link` 1줄 |

`styles.css`의 선택자는 `body`·`h1`·`h2`·`nav`·`nav a`·`.card`·`input, textarea`·`footer` 여덟 개다.
`class`는 `card` 하나뿐이고, 세 페이지에서 쓰는 CSS 파일은 하나다. 한 파일을 고치면 세 페이지가 함께 바뀐다.

## 공식 참고 자료

- [CSS 첫걸음 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Styling_basics/Getting_started)
- [박스 모델 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Styling_basics/Box_model)
- [플렉스박스(Flexbox) — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Flexbox)
- [미디어 쿼리 시작하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Media_queries)
