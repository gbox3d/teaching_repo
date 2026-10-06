실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

# 4주차 — CSS와 반응형 UI

이번 주는 부품을 하나씩 본다. 비교 파일 13개(부록 ex14 는 선택)를 열어 값을 바꿔 보고, 마지막에 `styles.css`를 그 부품으로 조립한다.
작년 수업과 같은 방식이다. 파일 하나에 주제 하나. 값 하나만 다른 형제를 나란히 놓고 차이를 눈으로 본다. 다른 주제의 속성은 섞지 않고, 상자는 배경색으로만 구분한다.
이번 주부터 주마다 새 저장소를 만든다. 이번 주 저장소는 `web-week04` 이고, 지난주 완성본에서 시작한다.

## 이번 주 질문

> 메뉴 세 개를 가로로 놓고, 좁은 화면에서는 세로로 세우려면 무엇을 알아야 하나?

답은 속성 이름 몇 개가 아니다. 세 가지 원리다.
`display: flex` 는 **부모**에 쓴다. `flex-direction` 이 **주축**을 정한다. `@media` 는 조건이 맞을 때만 뒤 규칙을 살린다.
이 세 줄을 이해하면 조합은 스스로 만들 수 있다.

## 학습 목표

1. 선택자가 맞아야 규칙이 적용된다. 겹치면 클래스가 태그를 이기고, 같은 선택자를 두 번 쓰면 뒤가 이긴다.
2. 줄을 차지하는지는 태그가 아니라 `display` 가 정한다. `padding`·`border`·`margin` 은 서로 다른 층이다.
3. `max-width` 는 창이 좁으면 같이 줄고, `margin` 의 `auto` 는 남는 폭을 가져간다(양쪽이면 반씩 → 가운데). `text-align` 은 상자가 아니라 상자 안 글자를 옮긴다.
4. flex 는 부모·주축·교차축으로 설명한다. `justify-content` 는 주축, `align-items` 는 교차축이다. `flex-wrap`·`gap` 은 부모에, `flex: 1` 은 자식에 쓴다.
5. `@media (max-width: 600px)` 안의 규칙은 조건이 맞을 때만 살아나 앞 규칙을 덮는다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/web-week04/
         DevTools 기기 모드 375px
         메뉴 홈 / 내 정보 / 방명록 이 세로로 한 줄씩
         소개 문단과 취미 목록이 테두리 있는 흰 카드
         ← 주소창과 폭 375 표시가 함께 보이게 찍는다
```

- 제출은 이 캡처 **한 장**이다. 1280px 화면은 확인용이다.
- 이번 주 저장소 `web-week04` 의 모양은 아래와 같다. 비교 파일은 `ex/` 에 저장하고 값을 바꾼 채로 올린다. 기록물·표는 없다. 산출물은 올린 파일과 화면이다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

```text
web-week04/
  index.html  about.html  guestbook.html  styles.css  app.js  images/   ← 지난주 완성본에서 시작, 2일차에 조립
  ex/                                                                  ← 비교 파일(값을 바꿔 보는 실험)
```

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 이번 주 방식 → ex01 선택자 → ex02 display → ex03 박스모델 → ex04 width·max-width → ex05 margin auto → ex06 text-align | `web-week04` 폴더에 지난주 파일 넣기 → `ex/` 에 여섯 파일 저장 → 값 바꿔 보기 → 새 저장소 `web-week04` 에 올리고 Pages 켜기 | 공개 주소와 `ex/` 여섯 파일(확인용) |
| 2일차 | flex 원리 다섯 줄 → ex07 direction → ex08 justify → ex09 align → ex10 wrap → ex11 gap → ex12 flex: 1 → ex13 @media → 조립표 | 일곱 파일 값 바꿔 보기 → `styles.css` 조립 → 1280·375 확인 → 올리기 | 캡처 1 |

각 수업은 `설명·시연 30분 + 실습 60분` 이다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.

## 준비

- 지난주 완성본. 내 3주차 저장소(`my-web`) GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [3주차 examples/day2/](../week03_semantic_html/examples/day2/) 파일을 쓴다
- VS Code, Chrome(DevTools), Git, GitHub 계정
- 이번 주에 만드는 폴더는 `web-week04` 하나. 고치는 파일은 `styles.css` 와 세 페이지의 `link` 한 줄씩, `index.html` 의 `class="card"` 세 곳
- `app.js` 는 열지 않는다. 5주차에 비우고 다시 쓴다
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 선택자 | selector | 选择器 |
| 규칙 | rule | 规则 |
| 박스모델 | box model | 盒模型 |
| 컨테이너 · 자식 | container · item | 容器 · 子项 |
| 주축 | main axis | 主轴 |
| 교차축 | cross axis | 交叉轴 |
| 줄 넘김 | wrap | 换行 |
| 화면 폭 조건 | media query | 媒体查询 |

## 이번 주 비교 파일

첫 형제는 기본값이다(ex13 만 1번이 `@media` 규칙이 있는 상자). 주석은 대안값이다. 주석을 풀거나 값을 바꾸고 저장 → 새로고침으로 차이를 본다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_selector.html](examples/day1/ex01_selector.html) | `p` / `p.red` / `div.red` / `p.Red`(오타) / `nav a` / nav 밖 `a` | 선택자가 맞아야 적용된다. 클래스가 태그를 이긴다. 같은 선택자 두 번이면 뒤가 이긴다 | `/* p { color: gray; } */` 주석 풀기, 4번의 `class="Red"` 를 `class="red"` 로 |
| [ex02_display.html](examples/day1/ex02_display.html) | div 3 / span 3 / span + `display: block` / div + `display: inline` | 줄을 차지하는지는 태그가 아니라 `display` 가 정한다 | `block` ↔ `inline` |
| [ex03_box_model.html](examples/day1/ex03_box_model.html) | 기본 / `padding` / `border` / `margin` / 셋 다 | 안쪽 여백·테두리·바깥 여백은 서로 다른 층. 회색 frame 안에서 margin 이 벌린 자리가 보인다 | 세 값을 `0` / `16px` / `32px` 로 |
| [ex04_width.html](examples/day1/ex04_width.html) | 기본(부모 폭) / `width: 640px` / `max-width: 640px` | `width` 는 폭을 못박고, `max-width` 는 상한만 둬서 창이 좁으면 같이 준다 | 창을 400px 로 줄여 2번만 삐져나가는지 |
| [ex05_margin_auto.html](examples/day1/ex05_margin_auto.html) | 기본(왼쪽) / `margin-left: auto` / 좌우 `auto` / `margin: 0 auto` | `auto` 는 남는 폭을 가져간다. 양쪽이 나눠 가지면 상자가 가운데에 선다 | 3번의 `margin-right: auto` 지우기, `.box` 의 `max-width` 지우기 |
| [ex06_text_align.html](examples/day1/ex06_text_align.html) | 기본(왼쪽) / `center` / `right` | 상자 안 글자의 가로 자리를 정한다. 상자 자체는 움직이지 않는다 | `right` → `center` |
| [ex07_flex_direction.html](examples/day2/ex07_flex_direction.html) | flex 없음 / `display: flex`(row) / `row-reverse` / `column` / `column-reverse` | `display: flex` 는 부모에 쓴다. `flex-direction` 이 자식이 서는 방향(주축)을 정한다 | 2번의 `상자 1` 에 class `flex` 를 더해 보기(배치는 그대로) |
| [ex08_justify_content.html](examples/day2/ex08_justify_content.html) | `flex-start` / `center` / `flex-end` / `space-between` / `space-around` | 주축 위에서 남는 공간(회색)을 어떻게 나누나 | `.evenly` 주석 풀고 5번 frame 의 class 를 `evenly` 로 |
| [ex09_align_items.html](examples/day2/ex09_align_items.html) | `stretch`(기본) / `flex-start` / `center` / `flex-end` | 교차축(세로)에서 자식을 어디에 두나. frame 에 높이가 있어야 보인다 | `.frame` 의 `height: 100px` 지우기 |
| [ex10_flex_wrap.html](examples/day2/ex10_flex_wrap.html) | `nowrap`(기본) / `wrap` | 주축에 다 안 들어갈 때 넘길지는 `flex-wrap`. 부모에 쓴다 | 자식 수 6 → 3 |
| [ex11_gap.html](examples/day2/ex11_gap.html) | gap 없음 / `gap: 16px` / `gap: 32px` | 자식과 자식 사이 간격. 사이는 자식 하나가 정할 수 없으니 부모에 쓴다 | `gap16` 을 frame 에서 빼서 자식에 붙여 보기(아무 일도 없다) |
| [ex12_flex_grow.html](examples/day2/ex12_flex_grow.html) | 기본 / 가운데만 `flex: 1` / 셋 다 `flex: 1` | 주축의 남는 공간을 그 자식이 차지한다. 이 속성만 자식에 쓴다 | `flex: 2` 주석 풀기, 3번 가운데에만 `style="flex: 2"` |
| [ex13_media.html](examples/day2/ex13_media.html) | `@media (max-width: 600px)` 규칙이 있는 상자 / 없는 상자 | 조건이 맞을 때만 안쪽 규칙이 살아난다. 같은 선택자 두 번 → 뒤가 이김(ex01) | `600px` → `900px`, 기기 모드 375 |
| [ex14_position.html](examples/day2/ex14_position.html) (부록, 설명 없음) | `static` / `relative; top; left` / `absolute; right; bottom` | 문서 흐름에서 빼는 두 방법 | `top`·`left`·`right`·`bottom` 값 바꾸기 |

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week04_responsive_css/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(ex01~ex06), 2일차 `day2/`(ex07~ex14와 조립 `build/`)
- 2일차 끝의 `web-week04`(조립 결과): [styles.css](examples/day2/build/styles.css) · [index.html](examples/day2/build/index.html) · [about.html](examples/day2/build/about.html) · [guestbook.html](examples/day2/build/guestbook.html) · [app.js](examples/day2/build/app.js) · [images/profile.png](examples/day2/build/images/profile.png)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

## 완료 기준

- [ ] GitHub 에 `web-week04` 저장소가 있고 Pages 가 켜져 있다.
- [ ] `ex/` 에 비교 파일이 있고, 각 파일에서 값을 하나 이상 바꿔 올렸다.
- [ ] 세 페이지의 `<head>` 에 `<link rel="stylesheet" href="styles.css">` 가 있다.
- [ ] 공개 주소 `https://student01.github.io/web-week04/` 에서 배경색·제목 색·메뉴 색이 보이고, 소개 문단과 취미 목록이 테두리 있는 흰 카드로 보인다.
- [ ] 1280px 에서 메뉴 세 개가 가로 한 줄이고, 가로 스크롤 막대가 생기지 않는다.
- [ ] DevTools 기기 모드 375px 에서 메뉴 세 개가 세로로 선다.
- [ ] 375px 화면 캡처 1장을 제출한다.

## 다음 수업 연결

이번 주까지 세 페이지는 **보이는 것**만 바뀌었다. 버튼도 입력 칸도 아직 아무 동작을 하지 않는다.
5주차에는 새 저장소 `web-week05` 를 만든다. 시작점은 이번 주 `web-week04` 의 파일이다.
그 위에서 `app.js` 를 비우고 다시 써서 JavaScript 를 시작한다. `index.html` 에 `<script src="app.js" defer></script>` 줄을 되살린다.
`styles.css` 는 그대로 가져간다. `.card` 의 색은 6주차 다크 모드에서 다시 쓴다. 결과는 새 공개 주소 `https://student01.github.io/web-week05/` 에서 확인한다.

## 공식 참고 자료

- [CSS 첫걸음 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Styling_basics/Getting_started)
- [CSS 선택자 — MDN](https://developer.mozilla.org/ko/docs/Web/CSS/CSS_selectors)
- [박스 모델 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Styling_basics/Box_model)
- [플렉스박스(Flexbox) — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Flexbox)
- [미디어 쿼리 시작하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Media_queries)
- [기기 모드로 모바일 기기 시뮬레이션 — Chrome DevTools](https://developer.chrome.com/docs/devtools/device-mode)
