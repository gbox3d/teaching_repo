실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

# 4주차 예제 — 비교 13개와 선택 부록

각 비교 폴더는 `index.html`과 `styles.css`로 독립 실행한다. 폴더를 사전에 `web-week04/ex/`에 배부하고 HTML을 Chrome으로 연다. 코드의 값과 짧은 비교 라벨은 화면에, 설명·실험 순서는 이 문서에 둔다. 상자는 배경색으로 구분한다.

| 범위 | 학생 필수 | 강의자 시연·선택 |
|---|---|---|
| 1일차 | ex01 색 1값, ex03 여백 1값, 제공 사이트 CSS 3값 | ex02·ex04·ex05·ex06, 추가 값 실험 |
| 2일차 | ex07 방향 1값, ex08 정렬 1값, 사이트 nav·media 3줄 | ex09~ex13 비교·전체 조립, ex14 선택 |

각 차시는 강의·시연 60분과 학생 실습 30분이다. 모든 예제의 값 변경이나 파일 재입력을 요구하지 않는다. 파일·저장소 준비는 수업 전, 공개 업로드는 수업 뒤다. [실습지](../lab.md)의 값과 완료 조건을 따른다.

`day2/web-week04/`는 자체 CSS를 연결한 제공 완성본이다. `app.js`는 2주차에서 보존한 파일이고 HTML의 script 연결이 없어 실행되지 않는다. `images/profile.png`도 3주차와 같은 그림이다. HTML 세 페이지는 CSS 연결을 공유하고 홈만 카드 클래스 세 곳을 사용한다.

방명록의 긴 입력 순서 설명은 이 문서로 옮겼다. 이름·이메일·메시지의 label 연결을 확인하고 남기기를 누른다. 잘못된 이메일은 브라우저 기본 검사가 막는다. 유효한 입력은 기본 GET으로 현재 문서를 다시 열며, 글 추가·저장 없이 입력이 초기화된다. 7주차에 글 추가 동작을 연결한다.

ex04의 고정 폭 상자는 375px에서 의도적으로 넘친다. 나머지 비교와 완성 사이트는 375/1280px에서 확인한다. ex13의 `max-width: 600px`은 600px도 포함한다. ex14의 `relative`는 원래 공간을 유지하고 `absolute`만 흐름에서 빠진다.

## 비교 예제

| 예제 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/ex01/index.html](day1/ex01/index.html) + [styles.css](day1/ex01/styles.css) | 문단 여섯 줄. 1 파랑, 2·3 빨강, 4 파랑(오타 `Red`), 5 초록(nav 안 a), 6 기본색 | 선택자가 맞아야 적용된다. 클래스가 태그를 이긴다. 같은 선택자를 두 번 쓰면 뒤가 이긴다 | `styles.css` 의 `/* p { color: gray; } */` 주석 풀기 → 1·4번 회색, 2번은 빨강 그대로. `index.html` 4번의 `class="Red"` 를 `class="red"` 로 고치기 → 4번도 빨강 |
| [day1/ex02/index.html](day1/ex02/index.html) + [styles.css](day1/ex02/styles.css) | 금색·하늘색·연두 상자 네 묶음. 1번 div 는 한 줄씩 창 끝까지, 2번 span 은 글자만큼 옆으로. `display` 를 바꾼 3·4번은 서로 반대 | 줄을 차지하는지는 태그가 아니라 `display` 가 정한다 | `.as-block` 과 `.as-inline` 의 값을 서로 바꾸기 |
| [day1/ex03/index.html](day1/ex03/index.html) + [styles.css](day1/ex03/styles.css) | 회색 frame 다섯 개(위아래에 `frame` 글자 줄) 안에 하늘색 box. 2번은 안이 넓고, 3번은 남색 테두리, 4번은 둘레에 회색 자리가 벌어짐, 5번은 셋 다 | 안쪽 여백·테두리·바깥 여백은 서로 다른 층. 배경색은 padding 까지 칠해지고, margin 자리에는 부모(회색)가 보인다 | `.pad`·`.bd`·`.mg` 의 값을 `0` / `16px` / `32px` 로 |
| [day1/ex04/index.html](day1/ex04/index.html) + [styles.css](day1/ex04/styles.css) | 연두 상자 세 개. 1번은 창 폭 전부, 2·3번은 640px | `width` 는 폭을 못박고 `max-width` 는 상한만 둔다. 부모의 사용 가능 폭이 640px보다 좁으면 3번만 같이 준다 | 창을 400px 까지 줄이기 → 2번만 삐져나가 가로 스크롤 |
| [day1/ex05/index.html](day1/ex05/index.html) + [styles.css](day1/ex05/styles.css) | 폭 300px 연두 상자 네 개. 1번 왼쪽, 2번 오른쪽, 3·4번 가운데 | `margin` 의 `auto` 는 남는 폭을 가져간다. 한쪽이면 반대편에 붙고, 양쪽이면 반씩 나눠 가운데. `margin: 0 auto` 는 3번을 한 줄로 쓴 것 | 3번의 `margin-right: auto` 지우기 → 2번과 같아짐. `.box` 의 `max-width` 지우기 → 남는 폭이 없어 넷이 같아짐 |
| [day1/ex06/index.html](day1/ex06/index.html) + [styles.css](day1/ex06/styles.css) | 창 폭 하늘색 상자 세 개. 글자가 왼쪽 / 가운데 / 오른쪽 | 상자 안 글자를 가로로 어디에 둘지 정한다. 상자 자체는 움직이지 않는다(상자를 옮기는 것은 ex05) | `.right` 의 값을 `center` 로 |
| [day2/ex07/index.html](day2/ex07/index.html) + [styles.css](day2/ex07/styles.css) | 회색 frame 다섯 개 안에 색 상자 1·2·3. 1번은 세로로 쌓임, 2번은 가로로 서고 오른쪽이 회색, 3번은 오른쪽 끝부터 3·2·1, 4번은 1번과 같은 모양, 5번은 위부터 3·2·1 | `display: flex` 는 부모에 쓴다. `flex-direction` 이 자식이 서는 방향(주축)을 정한다 | `index.html` 2번의 `상자 1` 에 class `flex` 를 더해 보기 → 배치는 그대로(flex 는 부모에 써야 한다) |
| [day2/ex08/index.html](day2/ex08/index.html) + [styles.css](day2/ex08/styles.css) | 회색 frame 다섯 개. 상자 셋이 앞 / 가운데 / 뒤 / 양 끝 / 고르게 | 주축 위에서 남는 공간(회색)을 어떻게 나누나 | `styles.css` 의 `.evenly` 주석 풀고 `index.html` 5번 frame 의 class 를 `evenly` 로 → 모든 간격이 같아짐 |
| [day2/ex09/index.html](day2/ex09/index.html) + [styles.css](day2/ex09/styles.css) | 높이 100px 회색 frame 네 개. 1번은 상자가 위아래로 늘어남, 2·3·4번은 위 / 가운데 / 아래 | 교차축(세로) 정렬. 높이를 안 정한 자식은 기본값 stretch 로 늘어난다 | `.frame` 의 `height: 100px` 지우기 → 남는 세로 공간이 없어 넷이 같아짐 |
| [day2/ex10/index.html](day2/ex10/index.html) + [styles.css](day2/ex10/styles.css) | 폭 300px frame 에 80px 상자 여섯 개(금색·하늘색 번갈아). 1번은 50px 씩으로 줄어 한 줄, 2번은 셋씩 두 줄 | 주축에 다 안 들어갈 때 넘길지는 `flex-wrap` 이 정한다. 부모에 쓴다 | `index.html` 의 자식 수 6 → 3 → 줄어듦도 넘김도 사라짐 |
| [day2/ex11/index.html](day2/ex11/index.html) + [styles.css](day2/ex11/styles.css) | 회색 frame 세 개. 상자 셋이 붙어 있음 / 16px 씩 / 32px 씩 벌어짐 | 자식과 자식 사이만 벌린다. 첫 상자 앞과 마지막 상자 뒤에 gap은 없다. 사이는 자식 하나가 정할 수 없으니 부모에 쓴다 | `index.html` 에서 `gap16` 을 frame 에서 빼서 `상자 1` 의 class 에 붙이기 → 간격이 사라지고 아무 일도 없다 |
| [day2/ex12/index.html](day2/ex12/index.html) + [styles.css](day2/ex12/styles.css) | 회색 frame 세 개: 오른쪽이 회색으로 빔 / 가운데 상자가 늘어남 / 셋이 똑같이 | 주축의 남는 공간을 `flex: 1` 인 자식이 차지한다. 이 속성만 자식에 쓴다 | `styles.css` 의 `/* flex: 2; */` 주석 풀기 → 변화 없음(셋 다 2). `index.html` 3번 가운데 상자에만 `style="flex: 2"` → 1:2:1 |
| [day2/ex13/index.html](day2/ex13/index.html) + [styles.css](day2/ex13/styles.css) | 하늘색 상자 두 개. 창이 600px 이하이면 1번만 주황 | 조건이 맞을 때만 안쪽 규칙이 살아난다. 같은 선택자 두 번 → 뒤가 이김(ex01) | `600px` → `900px`. F12 › 기기 모드 375 |
| [day2/ex14/index.html](day2/ex14/index.html) + [styles.css](day2/ex14/styles.css) (부록, 설명 없음) | 높이 100px 회색 frame 세 개 안에 A·B. 2번 A 는 B 아래로 밀려나고 맨 위 자리는 빔, 3번 A 는 오른쪽 아래 모서리로 가고 B 가 A 자리로 | 흐름을 유지하는 relative와 흐름에서 빠지는 absolute | `.relative` 의 `top`·`left`, `.absolute` 의 `right`·`bottom` |

### 파일 안의 모양

flex 예제(ex07~ex12)는 같은 틀을 쓴다. 회색 `.frame` 이 **부모(컨테이너)**, 색 상자 `.c1`·`.c2`·`.c3` 이 **자식**이다. 값 하나만 다른 클래스를 frame 에 붙여 형제를 만든다. 규칙은 [ex07/styles.css](day2/ex07/styles.css), 상자는 [ex07/index.html](day2/ex07/index.html)에서 인용:

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

주석은 대안값이다. [ex08/styles.css](day2/ex08/styles.css)의 이 줄처럼, `/* */` 를 지우면 그 규칙이 살아난다.

```css
/* .evenly { justify-content: space-evenly; } */ /* 모든 간격이 같다 */
```

주석에 적힌 "가로"·"세로"는 자식이 가로로 서는(row) 경우의 이야기다. 정확한 낱말은 **주축**·**교차축**이다. `justify-content` 는 주축, `align-items` 는 교차축에서 정렬한다.

## `day2/web-week04/` — 2일차 끝의 web-week04

[`day2/web-week04/`](day2/web-week04/) 는 사전 배부하는 `web-week04` 저장소 루트의 완성 예시다. 5주차 새 저장소 `web-week05` 의 시작점이다. 비교 예제를 저장한 `ex/` 폴더는 여기 넣지 않는다. 예제 폴더에도 같은 이름의 `index.html`·`styles.css` 가 있지만 조립에 쓰는 것은 이 폴더(내 저장소 맨 위)의 파일이다.

| `day2/web-week04/` 파일 | 내 `web-week04` 의 위치 | 따라하기 단계 |
|---|---|---|
| [styles.css](day2/web-week04/styles.css) | `styles.css` | [조립 전문](../walkthrough.md#2일차) — 제공 CSS에서 필수 지정값만 수정한다. 전문은 시연·복습용이다 |
| [index.html](day2/web-week04/index.html) | `index.html` | [조립 전문](../walkthrough.md#2일차) — `<head>` 에 `link` 한 줄, `class="card"` 세 곳 |
| [about.html](day2/web-week04/about.html) | `about.html` | [조립 전문](../walkthrough.md#2일차) — `link` 한 줄만 늘어난다 |
| [guestbook.html](day2/web-week04/guestbook.html) | `guestbook.html` | [조립 전문](../walkthrough.md#2일차) — `link` 한 줄만 늘어난다 |
| [app.js](day2/web-week04/app.js) | `app.js` | [조립 전문](../walkthrough.md#2일차) — 열지 않는다. 5주차에 비우고 다시 쓴다 |
| [images/profile.png](day2/web-week04/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |

### 조립표와 예제 출처

비교 예제에서 본 규칙을 한 파일에 모은 제공본이다. 입력의 `box-sizing: border-box`와 제목의 `word-break: keep-all`은 폭·줄바꿈 보정용 제공 규칙이며 필수 재작성 대상이 아니다.

| `styles.css` 규칙 | 어느 ex 에서 본 것 |
|---|---|
| `body { background-color; color; font-family; font-size }` | ex01 태그 선택자. 색·글꼴 네 속성은 3주차 HTML 에 없던 새 속성 |
| `body { max-width: 640px; margin: 0 auto; padding: 16px }` | ex04 (`max-width`), ex05 (`margin: 0 auto`), ex03 (`padding`) |
| `h1` · `h2` `{ color … }` | ex01 태그 선택자 |
| `nav { display: flex; gap: 16px; flex-wrap: wrap }` | ex07 (flex 는 부모에), ex11 (`gap`), ex10 (`flex-wrap`) — 셋 다 부모에 |
| `nav a { color }` | ex01 자손 선택자 |
| `.card { background-color; padding; margin: 12px 0; border }` | ex01 클래스 선택자, ex03 세 층 |
| `input, textarea { box-sizing: border-box; width: 280px; max-width: 100% }` | ex04 의 `width` 와 `max-width` 를 함께 쓴 것. `width: 280px` 은 평소 폭, `max-width: 100%` 는 부모보다 못 커지게 하는 상한. 쉼표 = 두 대상에 같은 규칙 |
| `footer { text-align: center; … }` | ex06 |
| `@media (max-width: 600px) { nav { flex-direction: column } }` | ex13 (조건) + ex07 (`column`) |

마지막 규칙은 좁은 화면의 메뉴 방향을 바꾼다. [day2/web-week04/styles.css](day2/web-week04/styles.css)에서 인용:

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
