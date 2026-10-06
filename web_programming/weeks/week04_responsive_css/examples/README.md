실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

# 4주차 예제 — 비교 파일 14개(부록 포함)와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   ex01 ~ ex06     선택자와 박스
  day2/   ex07 ~ ex14     flex 와 @media (ex14 는 부록)
          build/          2일차 끝의 web-week04 — 비교 파일에서 본 규칙을 모은 조립
```

`exNN_*.html` 은 **파일 하나 = 주제 하나**다. 파일마다 같은 상자를 여러 개 놓고 그 주제의 값 하나만 다르게 한 **형제**를 나란히 보여 준다.
**다른 주제의 속성은 넣지 않는다.** 상자는 배경색으로만 구분한다(색이 바뀌면 다른 상자, 회색은 부모). 주제를 보이는 데 꼭 필요한 앞 예제의 속성만 쓰고(예: ex09 frame 의 높이, ex10 의 폭), 그 줄에는 주석으로 이유를 적었다.
첫 형제는 **기본값**이다(ex13 만 1번이 `@media` 규칙이 있는 상자). 주석 처리된 줄은 **대안값**이다. 주석을 풀거나 값을 바꾸고 저장 → 새로고침으로 무엇이 달라지는지 본다.
작년 수업에서 CSS 를 가르친 방식이다. 만들기는 마지막 하나, [`day2/build/`](day2/build/) 뿐이다.

각 파일은 단일 HTML 이고 `<style>` 이 안에 있다. 내려받아 이번 주 저장소 폴더의 `web-week04/ex/` 에 파일 이름을 바꾸지 않고 저장한다(교재 저장소에서 **Raw** → 저장, 또는 타이핑). 내 저장소에서는 날짜 폴더 없이 `ex/` 한 곳에 모은다. 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 파일

| 파일 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_selector.html](day1/ex01_selector.html) | 문단 여섯 줄. 1 파랑, 2·3 빨강, 4 파랑(오타 `Red`), 5 초록(nav 안 a), 6 기본색 | 선택자가 맞아야 적용된다. 클래스가 태그를 이긴다. 같은 선택자를 두 번 쓰면 뒤가 이긴다 | `/* p { color: gray; } */` 주석 풀기 → 1·4번 회색, 2번은 빨강 그대로. 4번의 `class="Red"` 를 `class="red"` 로 고치기 → 4번도 빨강 |
| [ex02_display.html](day1/ex02_display.html) | 금색·하늘색·연두 상자 네 묶음. 1번 div 는 한 줄씩 창 끝까지, 2번 span 은 글자만큼 옆으로. `display` 를 바꾼 3·4번은 서로 반대 | 줄을 차지하는지는 태그가 아니라 `display` 가 정한다 | `.as-block` 과 `.as-inline` 의 값을 서로 바꾸기 |
| [ex03_box_model.html](day1/ex03_box_model.html) | 회색 frame 다섯 개(위아래에 `frame` 글자 줄) 안에 하늘색 box. 2번은 안이 넓고, 3번은 남색 테두리, 4번은 둘레에 회색 자리가 벌어짐, 5번은 셋 다 | 안쪽 여백·테두리·바깥 여백은 서로 다른 층. 배경색은 padding 까지 칠해지고, margin 자리에는 부모(회색)가 보인다 | `.pad`·`.bd`·`.mg` 의 값을 `0` / `16px` / `32px` 로 |
| [ex04_width.html](day1/ex04_width.html) | 연두 상자 세 개. 1번은 창 폭 전부, 2·3번은 640px | `width` 는 폭을 못박고 `max-width` 는 상한만 둔다. 창이 640px 보다 좁으면 3번만 같이 준다 | 창을 400px 까지 줄이기 → 2번만 삐져나가 가로 스크롤 |
| [ex05_margin_auto.html](day1/ex05_margin_auto.html) | 폭 300px 연두 상자 네 개. 1번 왼쪽, 2번 오른쪽, 3·4번 가운데 | `margin` 의 `auto` 는 남는 폭을 가져간다. 한쪽이면 반대편에 붙고, 양쪽이면 반씩 나눠 가운데. `margin: 0 auto` 는 3번을 한 줄로 쓴 것 | 3번의 `margin-right: auto` 지우기 → 2번과 같아짐. `.box` 의 `max-width` 지우기 → 남는 폭이 없어 넷이 같아짐 |
| [ex06_text_align.html](day1/ex06_text_align.html) | 창 폭 하늘색 상자 세 개. 글자가 왼쪽 / 가운데 / 오른쪽 | 상자 안 글자를 가로로 어디에 둘지 정한다. 상자 자체는 움직이지 않는다(상자를 옮기는 것은 ex05) | `.right` 의 값을 `center` 로 |
| [ex07_flex_direction.html](day2/ex07_flex_direction.html) | 회색 frame 다섯 개 안에 색 상자 1·2·3. 1번은 세로로 쌓임, 2번은 가로로 서고 오른쪽이 회색, 3번은 오른쪽 끝부터 3·2·1, 4번은 1번과 같은 모양, 5번은 위부터 3·2·1 | `display: flex` 는 부모에 쓴다. `flex-direction` 이 자식이 서는 방향(주축)을 정한다 | 2번의 `상자 1` 에 class `flex` 를 더해 보기 → 배치는 그대로(flex 는 부모에 써야 한다) |
| [ex08_justify_content.html](day2/ex08_justify_content.html) | 회색 frame 다섯 개. 상자 셋이 앞 / 가운데 / 뒤 / 양 끝 / 고르게 | 주축 위에서 남는 공간(회색)을 어떻게 나누나 | `.evenly` 주석 풀고 5번 frame 의 class 를 `evenly` 로 → 모든 간격이 같아짐 |
| [ex09_align_items.html](day2/ex09_align_items.html) | 높이 100px 회색 frame 네 개. 1번은 상자가 위아래로 늘어남, 2·3·4번은 위 / 가운데 / 아래 | 교차축(세로) 정렬. 높이를 안 정한 자식은 기본값 stretch 로 늘어난다 | `.frame` 의 `height: 100px` 지우기 → 남는 세로 공간이 없어 넷이 같아짐 |
| [ex10_flex_wrap.html](day2/ex10_flex_wrap.html) | 폭 300px frame 에 80px 상자 여섯 개(금색·하늘색 번갈아). 1번은 50px 씩으로 줄어 한 줄, 2번은 셋씩 두 줄 | 주축에 다 안 들어갈 때 넘길지는 `flex-wrap` 이 정한다. 부모에 쓴다 | 자식 수 6 → 3 → 줄어듦도 넘김도 사라짐 |
| [ex11_gap.html](day2/ex11_gap.html) | 회색 frame 세 개. 상자 셋이 붙어 있음 / 16px 씩 / 32px 씩 벌어짐 | 자식과 자식 사이만 벌린다. 맨 앞·맨 뒤는 붙어 있다. 사이는 자식 하나가 정할 수 없으니 부모에 쓴다 | `gap16` 을 frame 에서 빼서 `상자 1` 의 class 에 붙이기 → 간격이 사라지고 아무 일도 없다 |
| [ex12_flex_grow.html](day2/ex12_flex_grow.html) | 회색 frame 세 개: 오른쪽이 회색으로 빔 / 가운데 상자가 늘어남 / 셋이 똑같이 | 주축의 남는 공간을 `flex: 1` 인 자식이 차지한다. 이 속성만 자식에 쓴다 | `/* flex: 2; */` 주석 풀기 → 변화 없음(셋 다 2). 3번 가운데 상자에만 `style="flex: 2"` → 1:2:1 |
| [ex13_media.html](day2/ex13_media.html) | 하늘색 상자 두 개. 창을 600px 보다 좁히면 1번만 주황 | 조건이 맞을 때만 안쪽 규칙이 살아난다. 같은 선택자 두 번 → 뒤가 이김(ex01) | `600px` → `900px`. F12 › 기기 모드 375 |
| [ex14_position.html](day2/ex14_position.html) (부록, 설명 없음) | 높이 100px 회색 frame 세 개 안에 A·B. 2번 A 는 B 아래로 밀려나고 맨 위 자리는 빔, 3번 A 는 오른쪽 아래 모서리로 가고 B 가 A 자리로 | 문서 흐름에서 빼는 두 방법 | `.relative` 의 `top`·`left`, `.absolute` 의 `right`·`bottom` |

### 파일 안의 모양

flex 파일(ex07~ex12)은 같은 틀을 쓴다. 회색 `.frame` 이 **부모(컨테이너)**, 색 상자 `.c1`·`.c2`·`.c3` 이 **자식**이다. 값 하나만 다른 클래스를 frame 에 붙여 형제를 만든다. [ex07_flex_direction.html](day2/ex07_flex_direction.html)에서 인용:

```css
.frame {
    background-color: lightgray;    /* 부모(컨테이너). 회색이 보이면 남는 공간이다 */
}
.flex {
    display: flex;              /* 부모에 쓴다. 자식들이 한 줄로 선다. flex-direction 을 안 쓰면 row(가로 →) */
}
.row-reverse    { flex-direction: row-reverse; }    /* 주축이 가로 ← */
.column         { flex-direction: column; }         /* 주축이 세로 ↓ */
.column-reverse { flex-direction: column-reverse; } /* 주축이 세로 ↑ */
```

```html
<div class="frame flex column">
    <div class="c1">상자 1</div><div class="c2">상자 2</div><div class="c3">상자 3</div>
</div>
```

`class` 에 이름을 띄어 여러 개 쓰면(`frame flex column`) 그 클래스들의 규칙이 모두 붙는다.

주석은 대안값이다. [ex08_justify_content.html](day2/ex08_justify_content.html)의 이 줄처럼, `/* */` 를 지우면 그 규칙이 살아난다.

```css
/* .evenly { justify-content: space-evenly; } */ /* 모든 간격이 같다 */
```

주석에 적힌 "가로"·"세로"는 자식이 가로로 서는(row) 경우의 이야기다. 정확한 낱말은 **주축**·**교차축**이다. `justify-content` 는 주축, `align-items` 는 교차축에서 정렬한다.

## `day2/build/` — 2일차 끝의 web-week04

[`day2/build/`](day2/build/) 는 2일차 끝의 `web-week04` 저장소 **루트 전체**다. 5주차 새 저장소 `web-week05` 의 시작점이다. 비교 파일을 저장한 `ex/` 폴더는 여기 넣지 않는다.

| `day2/build/` 파일 | 내 `web-week04` 의 위치 | 따라하기 단계 |
|---|---|---|
| [styles.css](day2/build/styles.css) | `styles.css` | [2일차 6·9단계](../walkthrough.md#2일차) — 조립표 순서로 규칙을 쓴다. 이 파일과 글자 단위로 같아진다 |
| [index.html](day2/build/index.html) | `index.html` | [2일차 7·8·10단계](../walkthrough.md#2일차) — `<head>` 에 `link` 한 줄, `class="card"` 세 곳 |
| [about.html](day2/build/about.html) | `about.html` | [2일차 7·10단계](../walkthrough.md#2일차) — `link` 한 줄만 늘어난다 |
| [guestbook.html](day2/build/guestbook.html) | `guestbook.html` | [2일차 7·10단계](../walkthrough.md#2일차) — `link` 한 줄만 늘어난다 |
| [app.js](day2/build/app.js) | `app.js` | [2일차 11단계](../walkthrough.md#2일차) — 열지 않는다. 5주차에 비우고 다시 쓴다 |
| [images/profile.png](day2/build/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |

### 조립표 — `styles.css` 의 규칙은 어느 ex 에서 본 것인가

`styles.css` 는 새로 배우는 것이 없다. 비교 파일에서 본 규칙을 한 파일에 모은 것이다.

| `styles.css` 규칙 | 어느 ex 에서 본 것 |
|---|---|
| `body { background-color; color; font-family; font-size }` | ex01 태그 선택자. 색·글꼴 네 속성은 3주차 HTML 에 없던 새 속성 |
| `body { max-width: 640px; margin: 0 auto; padding: 16px }` | ex04 (`max-width`), ex05 (`margin: 0 auto`), ex03 (`padding`) |
| `h1` · `h2` `{ color … }` | ex01 태그 선택자 |
| `nav { display: flex; gap: 16px; flex-wrap: wrap }` | ex07 (flex 는 부모에), ex11 (`gap`), ex10 (`flex-wrap`) — 셋 다 부모에 |
| `nav a { color }` | ex01 자손 선택자 |
| `.card { background-color; padding; margin: 12px 0; border }` | ex01 클래스 선택자, ex03 세 층 |
| `input, textarea { width: 280px; max-width: 100% }` | ex04 의 `width` 와 `max-width` 를 함께 쓴 것. `width: 280px` 은 평소 폭, `max-width: 100%` 는 부모보다 못 커지게 하는 상한. 쉼표 = 두 대상에 같은 규칙 |
| `footer { text-align: center; … }` | ex06 |
| `@media (max-width: 600px) { nav { flex-direction: column } }` | ex13 (조건) + ex07 (`column`) |

마지막 덩어리가 이번 주 질문의 답이다. [day2/build/styles.css](day2/build/styles.css)에서 인용:

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
