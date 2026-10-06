---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 4주차"
footer: "CSS와 반응형 UI · 부품을 하나씩 비교하고 마지막에 조립"
---

# CSS와 반응형 UI

3주차에 만든 세 페이지는 아직 꾸미지 않았습니다. 이번 주는 CSS 입니다.
이번 주 저장소는 새로 만드는 `web-week04` 입니다. 공개 주소 `https://student01.github.io/web-week04/`

이번 주 방식: **부품 13개를 하나씩 비교**하고(부록 하나 더), 마지막에 `styles.css` 를 **조립**합니다.

- 파일 하나 = 주제 하나. 값 하나만 다른 형제를 나란히 놓고 차이를 봅니다.
- 다른 주제의 속성은 넣지 않았습니다. 상자는 **배경색으로만** 구분합니다.
- 첫 형제는 기본값. 주석은 다른 값. 실습도 **값을 바꿔 보는 것**입니다.
- 만들기는 2일차 끝에 한 번. 어느 규칙이 어느 파일에서 온 것인지 적어 둡니다.

작년 수업(dayNN/exNN 비교 파일 → 마지막에 만들기)과 같은 방식입니다.

---

# 1일차 — 선택자와 박스

`30분 설명·시연 → 60분 실습`

1. ex01 선택자 — 맞아야 적용되고, 겹치면 클래스가 이긴다
2. ex02 display — 줄을 차지하는지는 태그가 아니라 display
3. ex03 박스모델 — padding·border·margin 세 층
4. ex04 width·max-width — 창이 좁아지면 어느 쪽이 줄어드나
5. ex05 margin auto — 남는 폭을 나눠 가운데에 놓는다
6. ex06 text-align — 상자 안 글자를 가로로 어디에 두나

---

## 1일차 · 0–4분 — 이번 주 방식: 부품을 보고 마지막에 조립한다

```css
선택자 {
  속성: 값;
}
```

- 규칙 하나 = 선택자 + 중괄호 + `속성: 값;` 줄들. 비교 파일은 `<style>` 안에, 세 페이지는 `styles.css` + `<link rel="stylesheet" href="styles.css">`.
- 색·글꼴 속성은 이름 그대로입니다: `color` · `background-color` · `font-size` · `font-family`.
- **CSS 는 틀려도 오류 메시지가 없다.** 선택자가 안 맞거나 세미콜론이 빠지면 조용히 무시됩니다.
- 그래서 형제를 나란히 놓고 **눈으로** 비교합니다. 값을 바꿨는데 화면이 안 바뀌면 그것도 결과입니다.

---

## 1일차 · 4–9분 — ex01 선택자: 맞아야 적용되고, 겹치면 클래스가 이긴다

[examples/day1/ex01_selector.html](examples/day1/ex01_selector.html)
형제: `p` / `p.red` / `div.red` / `p.Red`(오타) / `nav a` / nav 밖 `a`

```css
p     { color: blue; }    /* 태그 선택자: 모든 p */
.red  { color: red; }     /* 클래스 선택자: class="red" 만, 태그는 상관없다 */
nav a { color: green; }   /* 자손 선택자: nav 안의 a 만 */
/* p { color: gray; } */
```

- 2번은 `p` 이면서 `.red` → 빨강. 4번 `class="Red"` 는 `.red` 와 다른 이름 → 파랑.
- 바꿔 보기: 주석 풀기 → 1·4번(`.red` 가 안 맞는 p)만 회색, 2번은 빨강 그대로. 4번의 `class="Red"` 를 `class="red"` 로 → 빨강.

**선택자가 맞아야 적용된다. 클래스는 태그보다 좁게 고르니 더 세다. 세기가 같을 때만 뒤가 이긴다.**

---

## 1일차 · 9–13분 — ex02 display: 줄을 차지하는지는 태그가 아니라 display

[examples/day1/ex02_display.html](examples/day1/ex02_display.html)
형제: div 3개 / span 3개 / span + `display: block` / div + `display: inline`

```css
.as-block  { display: block; }   /* 한 줄을 다 차지한다 */
.as-inline { display: inline; }  /* 글자처럼 옆으로 이어진다 */
```

- 1번 div 는 한 줄씩 창 끝까지, 2번 span 은 글자만큼만 옆으로. 색이 바뀌면 다른 상자입니다.
- 바꿔 보기: `.as-block` 을 `inline` 으로, `.as-inline` 을 `block` 으로 → 3번과 4번이 자리를 바꾼다.

**줄을 차지하는지는 태그가 아니라 `display` 가 정한다.**

---

## 1일차 · 13–18분 — ex03 박스모델: padding·border·margin 세 층

[examples/day1/ex03_box_model.html](examples/day1/ex03_box_model.html)
형제: 기본 / `padding` / `border` / `margin` / 셋 다 (회색 frame 안의 하늘색 box)

```css
.pad { padding: 16px; }           /* 테두리 안쪽, 글자와 테두리 사이 */
.bd  { border: 4px solid navy; }  /* 테두리 */
.mg  { margin: 16px; }            /* 테두리 바깥, 이웃과의 거리 */
```

- 하늘색 배경은 `padding` 까지 칠해지고, `margin` 이 벌린 자리는 회색 frame 이 보입니다. F12 › Styles 맨 아래 상자 그림.
- 바꿔 보기: 세 값을 0 / 16 / 32 로 → 5번 상자에서 어느 층이 커지는지.

**안쪽 여백(padding)·테두리(border)·바깥 여백(margin)은 서로 다른 층이다.**

---

## 1일차 · 18–22분 — ex04 width와 max-width: 창이 좁아지면 어느 쪽이 줄어드나

[examples/day1/ex04_width.html](examples/day1/ex04_width.html)
형제: 기본(부모 폭) / `width: 640px` / `max-width: 640px`

```css
.w  { width: 640px; }        /* 창이 좁아져도 640px, 삐져나간다 */
.mw { max-width: 640px; }    /* 640px 까지만, 창이 좁으면 같이 줄어든다 */
```

- 넓은 창에서는 2·3번이 똑같이 640px 입니다. 차이는 창이 640px 보다 좁을 때만 보입니다.
- 바꿔 보기: 창 폭을 400px 까지 천천히 줄이기 → 2번만 삐져나가 가로 스크롤이 생긴다.

**`width` 는 폭을 못박고 `max-width` 는 상한만 둔다. 상한만 두면 창과 함께 준다.**

---

## 1일차 · 22–25분 — ex05 margin auto: 남는 폭을 나눠 가운데에 놓는다

[examples/day1/ex05_margin_auto.html](examples/day1/ex05_margin_auto.html)
형제: 기본(왼쪽) / `margin-left: auto` / 좌우 `auto` / `margin: 0 auto`

```css
.left-auto { margin-left: auto; }                       /* 남는 폭을 왼쪽이 다 → 오른쪽에 붙는다 */
.both-auto { margin-left: auto; margin-right: auto; }   /* 반씩 → 가운데 */
.short     { margin: 0 auto; }                          /* 위아래 0, 좌우 auto. 3번과 같다 */
```

- 상자가 창보다 좁아야 남는 폭이 생깁니다(ex04 의 `max-width`). `auto` 는 그 남는 폭을 가져가는 값입니다.
- 바꿔 보기: 3번의 `margin-right: auto` 지우기 → 2번과 같다. `max-width` 지우기 → 넷이 같다.

**`margin` 의 `auto` 는 남는 폭을 가져간다. 양쪽이 나눠 가지면 상자가 가운데에 선다.**

---

## 1일차 · 25–28분 — ex06 text-align: 상자 안 글자를 가로로 어디에 두나

[examples/day1/ex06_text_align.html](examples/day1/ex06_text_align.html)
형제: 기본(왼쪽) / `text-align: center` / `text-align: right`

```css
.center { text-align: center; }
.right  { text-align: right; }
```

- 상자는 그대로 창 폭 전부이고, 상자 **안의 글자**만 움직입니다. ex05 는 상자 자체를 옮겼습니다.
- 바꿔 보기: 3번의 `right` 를 `center` 로. 조립에서 footer 글자를 가운데로 할 때 이 줄을 씁니다.

**`text-align` 은 상자 안 글자를 가로로 어디에 둘지 정한다. 상자 자체는 움직이지 않는다.**

---

## 1일차 · 28–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--선택자와-박스-60분) · [따라하기](walkthrough.md#1일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css)

1. 새 폴더 `web-week04` 에 지난주 파일을 넣고, `ex/` 에 ex01~ex06 을 저장합니다.
2. 파일마다 값을 하나 이상 바꿔 보고 화면이 어떻게 달라지는지 봅니다.
3. 끝: `web-week04` 저장소에 올리고 Pages 켜기 — 순서는 실습지

화면이 안 바뀌면 오류를 찾지 말고 **선택자 철자**와 **세미콜론**부터 봅니다.

**설명 합계: 4+5+4+5+4+3+3+2 = 30분**

---

# 2일차 — flex, 그리고 조립

`30분 설명·시연 → 60분 실습`

1. flex 원리 다섯 줄 — 부모·주축·교차축
2. ex07·ex08·ex09 — direction 이 주축, justify 는 주축, align 은 교차축
3. ex10·ex11·ex12 — wrap·gap 은 부모에, flex: 1 은 자식에
4. ex13 — @media 는 조건이 맞을 때만
5. 조립 — `styles.css` 를 부품에서 모은다

---

## 2일차 · 0–4분 — flex 원리 다섯 줄: 부모·주축·교차축

```text
부모(컨테이너) display: flex, flex-direction: row
┌──────────────── 주축 → ───────────┐
│ [1] [2] [3]                       │  교차축 ↓
└───────────────────────────────────┘
```

1. `display: flex` 는 **부모**에 쓴다. 자식들이 배치 대상이 된다.
2. `flex-direction` 이 **주축**을 정한다. `row` 면 가로, `column` 이면 세로.
3. `justify-content` 는 **주축** 정렬이다. `row` 면 가로 방향.
4. `align-items` 는 **교차축** 정렬이다. `row` 면 세로 방향.
5. `flex: 1` 은 주축의 **남는 공간**을 그 자식이 차지한다.

ex07~ex12 는 이 다섯 줄을 한 파일에 하나씩 따로 확인합니다. 회색은 부모, 색 상자는 자식입니다.

---

## 2일차 · 4–8분 — ex07 flex-direction: 주축을 정한다

[examples/day2/ex07_flex_direction.html](examples/day2/ex07_flex_direction.html)
형제: flex 없음 / `display: flex`(기본 row) / `row-reverse` / `column` / `column-reverse`

```css
.flex           { display: flex; }                   /* 부모에 쓴다. 기본 방향 row(가로 →) */
.row-reverse    { flex-direction: row-reverse; }     /* 가로 ← */
.column         { flex-direction: column; }          /* 세로 ↓ */
.column-reverse { flex-direction: column-reverse; }  /* 세로 ↑ */
```

- 2번은 상자가 글자만큼만 옆으로 서고 남는 공간이 회색으로 보입니다. 4번 column 은 1번(flex 없음)과 똑같아 보입니다.
- 바꿔 보기: 2번의 `상자 1` 에 class `flex` 를 더하기 → 배치는 그대로. flex 는 부모에 써야 자식들이 움직인다.

**`display: flex` 는 부모에. `flex-direction` 이 자식이 서는 방향(주축)을 정한다.**

---

## 2일차 · 8–12분 — ex08 justify-content: 주축 위의 남는 공간

[examples/day2/ex08_justify_content.html](examples/day2/ex08_justify_content.html)
형제: `flex-start` / `center` / `flex-end` / `space-between` / `space-around`, 주석 `space-evenly`

```css
.start   { justify-content: flex-start; }    /* 기본값: 앞에 모은다 */
.between { justify-content: space-between; } /* 양 끝에 붙이고 사이를 벌린다 */
.around  { justify-content: space-around; }  /* 상자마다 양옆에 같은 여백 */
/* .evenly { justify-content: space-evenly; } */ /* 모든 간격이 같다 */
```

- 회색이 남는 공간입니다. 값마다 그 공간을 앞·뒤·사이 중 어디에 둘지가 다릅니다.
- 바꿔 보기: `.evenly` 주석을 풀고 5번 class 를 `evenly` 로 → around 와 무엇이 다른가.

**`justify-content` 는 주축 위에서 남는 공간을 어떻게 나누는가다.**

---

## 2일차 · 12–16분 — ex09 align-items: 교차축 위의 자리

[examples/day2/ex09_align_items.html](examples/day2/ex09_align_items.html)
형제: `stretch`(기본) / `flex-start` / `center` / `flex-end` — frame 높이 100px

```css
.stretch { align-items: stretch; }     /* 기본값: 높이를 안 정한 자식은 끝까지 늘어난다 */
.start   { align-items: flex-start; }  /* 위 */
.center  { align-items: center; }      /* 세로 가운데 */
.end     { align-items: flex-end; }    /* 아래 */
```

- 1번은 상자에 높이가 없어 frame 높이만큼 늘어납니다. 3번이 세로 가운데입니다.
- 바꿔 보기: `.frame` 의 `height: 100px` 를 지우기 → 세로로 남는 공간이 없어 네 개가 똑같아진다.

**`align-items` 는 교차축 정렬이다. 가로로 선 자식에게는 세로 방향이다.**

---

## 2일차 · 16–18분 — ex10 flex-wrap: 다 안 들어가면 넘기기

[examples/day2/ex10_flex_wrap.html](examples/day2/ex10_flex_wrap.html)
형제: `nowrap`(기본) / `wrap` — 폭 80px 자식 6개, 폭 300px frame

```css
.nowrap { flex-wrap: nowrap; }  /* 기본값: 한 줄에 억지로 넣는다 */
.wrap   { flex-wrap: wrap; }    /* 안 들어가면 다음 줄로 넘긴다 */
```

- 80px × 6 = 480px. 1번은 여섯 개를 50px 씩으로 줄이고, 2번은 셋씩 두 줄로 넘깁니다.
- 바꿔 보기: 자식 수를 6 → 3 으로 → 줄어듦도 넘김도 사라진다.

**다 안 들어갈 때 넘길지는 `flex-wrap` 이 정한다. 부모에 쓴다.**

---

## 2일차 · 18–20분 — ex11 gap: 자식과 자식 사이 간격

[examples/day2/ex11_gap.html](examples/day2/ex11_gap.html)
형제: gap 없음 / `gap: 16px` / `gap: 32px`

```css
.gap16 { gap: 16px; }   /* 자식과 자식 사이를 벌린다. 부모에 쓴다 */
.gap32 { gap: 32px; }
```

- 사이만 벌어지고 맨 앞·맨 뒤는 붙어 있습니다.
- 바꿔 보기: `gap16` 을 frame 에서 빼서 `상자 1` 의 class 에 붙이기 → 아무 일도 없다.

**사이 간격은 자식 하나가 정할 수 없다. 그래서 `gap` 은 부모에 쓴다.**

---

## 2일차 · 20–23분 — ex12 flex: 1 — 남는 공간을 차지한다

[examples/day2/ex12_flex_grow.html](examples/day2/ex12_flex_grow.html)
형제: 기본 / 가운데만 `flex: 1` / 셋 다 `flex: 1`, 주석 `flex: 2`

```css
.grow { flex: 1; }   /* 주축의 남는 공간을 이 자식이 차지한다 */
/* flex: 2; */       /* 둘이 나눠 가질 때 2:1 로 */
```

- 이 속성만 **자식**에 씁니다. "남는 공간을 내가 가진다"는 자식의 말이기 때문입니다.
- 바꿔 보기: 3번 가운데 `<div>` 에만 `style="flex: 2"` → 가운데가 두 배 몫. `.grow` 의 `flex: 2` 주석은 셋 다 2 라 변화 없음.

**`flex: 1` 은 주축의 남는 공간을 그 자식이 차지한다. 여럿이면 숫자 비율로 나눈다.**

---

## 2일차 · 23–26분 — ex13 @media: 조건이 맞을 때만 뒤 규칙이 산다

[examples/day2/ex13_media.html](examples/day2/ex13_media.html)
형제: `@media (max-width: 600px)` 규칙이 있는 상자 / 없는 상자

```css
.with-media { background-color: lightskyblue; }   /* 평소 색 */
@media (max-width: 600px) {                        /* 900px 으로 바꿔 보기 */
    .with-media { background-color: orange; }
}
```

- 600px 이하에서만 안쪽 규칙이 삽니다. 같은 선택자가 두 번이면 뒤가 이깁니다(ex01). 확인은 기기 모드 375.
- 바꿔 보기: 600 → 900 → 보통 창에서도 주황. 콜론을 빼면 오류 없이 덩어리 전체가 무시된다.

**조건이 맞을 때만 안쪽 규칙이 산다. 바꿀 속성은 무엇이든 된다(조립은 `flex-direction`).**

---

## 2일차 · 26–30분 — 조립: web-week04 styles.css, 그리고 실습 인계

```text
body  { max-width: 640px; margin: 0 auto; padding: 16px }      ← ex04 + ex05 + ex03
nav   { display: flex; gap: 16px; flex-wrap: wrap }            ← ex07 + ex11 + ex10 (모두 부모에)
.card { background-color; padding; margin: 12px 0; border }    ← ex01 클래스 + ex03 세 층
@media (max-width: 600px) { nav { flex-direction: column } }   ← ex13 + ex07
```

[2일차 실습](lab.md#2일차--flex와-조립-60분) · [따라하기](walkthrough.md#2일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css)

1. ex07~ex13 일곱 파일을 `ex/` 에 저장하고 값을 바꿔 봅니다(35분까지).
2. 조립: `styles.css` 를 조립표 순서로, 세 페이지에 `link` 줄, `index.html` 에 `class="card"` 세 곳.
3. 1280 과 기기 모드 375 로 확인 → 끝: `web-week04` 에 올리고 캡처 — 순서는 실습지

**설명 합계: 4+4+4+4+2+2+3+3+4 = 30분**

---

## 부록 — ex14 position (선택, 설명 없음)

[examples/day2/ex14_position.html](examples/day2/ex14_position.html)
형제: `static`(기본) / `relative; top: 40px; left: 40px` / `absolute; right: 0; bottom: 0`

```css
.frame    { position: relative; }                           /* absolute 자식의 기준점 */
.relative { position: relative; top: 40px; left: 40px; }    /* 원래 자리에서 밀어낸다. 자리는 남는다 */
.absolute { position: absolute; right: 0; bottom: 0; }      /* 흐름에서 빠져 frame 모서리 기준 */
```

- 수업에서 다루지 않습니다. 먼저 끝났으면 열어서 값을 바꿔 봅니다.
- 2번에서 A 의 원래 자리(맨 위)가 비어 있고, 3번에서 B 가 A 자리로 올라오는 이유: `absolute` 는 A 를 문서 흐름에서 뺐기 때문입니다.

**문서 흐름에서 빼는 두 방법. `relative` 는 자리를 남기고, `absolute` 는 남기지 않는다.**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/web-week04/
DevTools 기기 모드 375px
메뉴: 홈 / 내 정보 / 방명록   ← 세로로 한 줄씩
소개 문단·취미 목록: 테두리 있는 흰 카드
주소창과 폭 375 표시가 함께 보이게 찍습니다
```

1280px 화면과 `ex/` 의 실험 파일은 확인용입니다. 캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

오늘까지 세 페이지는 **보이는 것**만 바뀌었습니다. 버튼도 입력 칸도 아직 아무 동작을 하지 않습니다.

5주차는 새 저장소 `web-week05` 에서, 오늘 파일을 시작점으로 합니다.
그 위에서 `app.js` 를 비우고 다시 써서 JavaScript 를 시작합니다.
`<script src="app.js" defer></script>` 줄을 되살리고, Console 에 값을 찍어 봅니다.
`styles.css` 는 그대로입니다. 오늘 정한 `.card` 색은 6주차 다크 모드에서 다시 씁니다.
