실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

# 4주차 예제 — 비교 파일 12개와 조립 하나

이 폴더의 `exNN_*.html` 은 **파일 하나 = 속성 하나**다. 파일마다 같은 상자를 여러 개 놓고 값 하나만 다르게 한 **형제**를 나란히 보여 준다.
첫 형제는 **기본값**이다(ex11 만 1번이 `@media` 가 있는 frame). 주석 처리된 줄은 **대안값**이다. 주석을 풀거나 값을 바꾸고 저장 → 새로고침으로 무엇이 달라지는지 본다.
작년 수업에서 CSS 를 가르친 방식이다. 만들기는 마지막 하나, [`build/`](build/) 뿐이다.

각 파일은 단일 HTML 이고 `<style>` 이 안에 있다. 내려받아 `my-web/week04/` 에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장, 또는 타이핑). 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 파일

| 파일 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_selector.html](ex01_selector.html) | 문단 여섯 줄. 1 파랑, 2·3 빨강, 4 파랑(오타 `Red`), 5 초록(nav 안 a), 6 기본색 | 선택자가 맞아야 적용된다. 클래스가 태그를 이긴다. 같은 선택자를 두 번 쓰면 뒤가 이긴다 | `/* p { color: gray; } */` 주석 풀기 → 1·4번 회색, 2번은 빨강 그대로. 4번의 `class="Red"` 를 `class="red"` 로 고치기 → 4번도 빨강 |
| [ex02_display.html](ex02_display.html) | 노란 상자 네 묶음. div 는 한 줄씩, span 은 옆으로. `display` 를 바꾼 3·4번은 서로 반대 | 줄을 차지하는지는 태그가 아니라 `display` 가 정한다 | `.as-block` 과 `.as-inline` 의 값을 서로 바꾸기 |
| [ex03_box_model.html](ex03_box_model.html) | 흰 frame 다섯 개 안에 하늘색 상자. 2번은 안이 넓고, 3번은 남색 테두리, 4번은 흰 자리가 벌어짐, 5번은 셋 다 | 안쪽 여백·테두리·바깥 여백은 서로 다른 층. 흰 frame 위에서 margin 이 벌린 자리가 보인다 | `.pad`·`.bd`·`.mg` 의 값을 `0` / `16px` / `32px` 로 |
| [ex04_width.html](ex04_width.html) | 연두 상자 네 개. 1번은 창 폭 전부, 2·3번은 640px, 4번은 640px 가운데 | `max-width` 는 창이 좁으면 같이 줄고, `margin: auto` 는 남는 폭을 반씩 나눈다 | 창을 400px 까지 줄이기 → 2번만 삐져나가 가로 스크롤 |
| [ex05_text_align.html](ex05_text_align.html) | 파란 상자 네 개. 글자가 왼쪽 / 가운데 / 오른쪽. 4번 `vertical-align: middle` 은 그대로 위에 | 가로 정렬은 `text-align`. `vertical-align` 은 줄 안에서 글자끼리 맞추는 속성이라 상자 안 세로 가운데는 안 된다 → 답은 ex08 | `.middle` 의 값을 `bottom` 등으로 바꿔도 안 움직임 확인 |
| [ex06_flex_direction.html](ex06_flex_direction.html) | 흰 테두리 frame 일곱 개 안에 파란 상자 1·2·3. 1번은 세로로 쌓임, 2번부터 flex. 6번은 가로 가운데, 7번은 세로 가운데 | `display: flex` 는 부모에 쓴다. `flex-direction` 이 주축을 정한다. 같은 `justify-content: center` 가 row 에선 가로, column 에선 세로 가운데 | 6·7번의 `row`·`column` 을 서로 바꾸기. `.box` 에 `display: flex` 를 잘못 줘 보기(상자 배치는 그대로, 숫자만 왼쪽 끝으로) |
| [ex07_justify_content.html](ex07_justify_content.html) | 가로 frame 다섯 개. 상자 셋이 앞 / 가운데 / 뒤 / 양 끝 / 고르게 | 주축 위에서 남는 공간을 어떻게 나누나 | `.frame` 의 `height` 를 `160px` 로 늘리고 `/* flex-direction: column; */` 주석 풀기 → 다섯 개가 전부 세로로 움직임. `.evenly` 주석 풀고 5번 frame 의 class 를 `evenly` 로 |
| [ex08_align_items.html](ex08_align_items.html) | 높이 120px frame 네 개. 1번은 상자가 위아래로 늘어남, 2·3·4번은 위 / 가운데 / 아래 | 교차축 정렬. ex05 에서 안 되던 세로 가운데가 여기서 된다 | `.frame` 의 `/* flex-direction: column; */` 주석 풀기 → 네 개가 전부 가로로 움직임 |
| [ex09_flex_wrap_gap.html](ex09_flex_wrap_gap.html) | 폭 300px frame 에 64px 상자 여섯 개. 1번은 찌그러짐, 2번은 두 줄, 3번은 두 줄 + 16px 간격 | 주축에 다 안 들어가면 넘길지는 `flex-wrap`, 사이 간격은 `gap`. 둘 다 부모에 쓴다 | 자식 수 6 → 3. `.gap` 의 값을 `0` / `16px` / `32px` 로 |
| [ex10_flex_grow.html](ex10_flex_grow.html) | 가로 frame 세 개: 오른쪽이 빔 / 가운데 상자가 늘어남 / 셋이 똑같이. 4번은 세로 화면, main 이 나머지를 차지 | 주축의 남는 공간을 누가 차지하나. 세로에서도 같다 | `/* flex: 2; */` 주석 풀기 → 변화 없음(셋 다 2). 3번의 한 상자에만 `style="flex: 2"` → 2:1:1. 4번 `.screen` 높이를 `100vh` 로 |
| [ex11_media.html](ex11_media.html) | 메뉴 상자 홈 · 내 정보 · 방명록 frame 두 개. 창을 600px 보다 좁히면 1번만 세로로 | 조건이 맞을 때만 뒤 규칙이 살아난다. 같은 선택자 두 번 → 뒤가 이김(ex01) | `600px` → `900px`. F12 › 기기 모드 375 |
| [ex12_position.html](ex12_position.html) (부록, 설명 없음) | frame 세 개 안에 상자 A·B. 2번 A 는 밀려나고 자리는 남음, 3번 A 는 오른쪽 아래 모서리로 가고 B 가 A 자리로 | 문서 흐름에서 빼는 두 방법 | `.relative` 의 `top`·`left`, `.absolute` 의 `right`·`bottom` |

### 파일 안의 모양

flex 파일(ex06~ex11)은 같은 틀을 쓴다. `.frame` 이 **부모(컨테이너)**, `.box` 가 **자식**이다. 값 하나만 다른 클래스를 frame 에 붙여 형제를 만든다. [ex06_flex_direction.html](ex06_flex_direction.html)에서 인용:

```css
.flex {
    display: flex;              /* 부모에 쓴다. 자식들이 한 줄로 선다 */
}
.row            { flex-direction: row; }            /* 기본값: 주축이 가로 → */
.row-reverse    { flex-direction: row-reverse; }    /* 주축이 가로 ← */
.column         { flex-direction: column; }         /* 주축이 세로 ↓ */
.column-reverse { flex-direction: column-reverse; } /* 주축이 세로 ↑ */
.center         { justify-content: center; }        /* 주축 방향으로 가운데 */
```

```html
<div class="frame flex row center">
    <div class="box">1</div><div class="box">2</div><div class="box">3</div>
</div>
```

주석은 대안값이다. [ex07_justify_content.html](ex07_justify_content.html)의 두 줄처럼, `/* */` 를 지우면 그 규칙이 살아난다.

```css
/* flex-direction: column; */   /* 주석을 풀면 다섯 개가 전부 세로 방향으로 움직인다 */
/* .evenly { justify-content: space-evenly; } */ /* 모든 간격이 같다 */
```

주석에 적힌 "가로"·"세로"는 row 일 때 이야기다. 정확한 낱말은 **주축**·**교차축**이다. `justify-content` 는 주축, `align-items` 는 교차축. `flex-direction: column` 이면 둘 다 방향이 바뀐다.

## `build/` — 2일차 끝의 my-web

[`build/`](build/) 는 2일차 끝의 `my-web` **전체**다. 5주차의 시작점이다(5주차 walkthrough 1단계). 비교 파일을 저장한 `week04/` 실험 파일은 여기 넣지 않는다.

| `build/` 파일 | 내 `my-web` 의 위치 | 따라하기 단계 |
|---|---|---|
| [styles.css](build/styles.css) | `styles.css` | [2일차 6·9단계](../walkthrough.md#2일차) — 조립표 순서로 규칙을 쓴다. 이 파일과 글자 단위로 같아진다 |
| [index.html](build/index.html) | `index.html` | [2일차 7·8·10단계](../walkthrough.md#2일차) — `<head>` 에 `link` 한 줄, `class="card"` 세 곳 |
| [about.html](build/about.html) | `about.html` | [2일차 7·10단계](../walkthrough.md#2일차) — `link` 한 줄만 늘어난다 |
| [guestbook.html](build/guestbook.html) | `guestbook.html` | [2일차 7·10단계](../walkthrough.md#2일차) — `link` 한 줄만 늘어난다 |
| [app.js](build/app.js) | `app.js` | [2일차 11단계](../walkthrough.md#2일차) — 열지 않는다. 5주차에 비우고 다시 쓴다 |
| [images/profile.png](build/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |

### 조립표 — `styles.css` 의 규칙은 어느 ex 에서 본 것인가

`styles.css` 는 새로 배우는 것이 없다. 비교 파일에서 본 규칙을 한 파일에 모은 것이다.

| `styles.css` 규칙 | 어느 ex 에서 본 것 |
|---|---|
| `body { background-color; color; font-family; font-size }` | ex01 태그 선택자. 색·글꼴 네 속성은 3주차 HTML 에 없던 새 속성 |
| `body { max-width: 640px; margin: 0 auto; padding: 16px }` | ex04 (`max-width`·`margin` auto), ex03 (`padding`) |
| `h1` · `h2` `{ color … }` | ex01 태그 선택자 |
| `nav { display: flex; gap: 16px; flex-wrap: wrap }` | ex06 (flex 는 부모에), ex09 (`gap`·`wrap` 도 부모에) |
| `nav a { color }` | ex01 자손 선택자 |
| `.card { background-color; padding; margin: 12px 0; border }` | ex01 클래스 선택자, ex03 세 층 |
| `input, textarea { width: 280px; max-width: 100% }` | ex04 3번 `max-width` 로 좁은 화면 대비. `width: 280px` 은 평소 폭, `max-width: 100%` 는 부모보다 못 커지게 하는 상한. 쉼표 = 두 대상에 같은 규칙 |
| `footer { text-align: center; … }` | ex05 |
| `@media (max-width: 600px) { nav { flex-direction: column } }` | ex11 (조건) + ex06 (`column`) |

마지막 덩어리가 이번 주 질문의 답이다. [build/styles.css](build/styles.css)에서 인용:

```css
nav {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}
```

`nav` 규칙이 두 번이다. 600px 이하에서만 뒤 규칙이 살아나 `flex-direction` 을 `column` 으로 덮는다. 1280px 에서는 가로, 375px 에서는 세로가 되는 이유다.

## 공식 참고 자료

- [CSS 첫걸음 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Styling_basics/Getting_started)
- [CSS 선택자 — MDN](https://developer.mozilla.org/ko/docs/Web/CSS/CSS_selectors)
- [박스 모델 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Styling_basics/Box_model)
- [플렉스박스(Flexbox) — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Flexbox)
- [미디어 쿼리 시작하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Media_queries)
