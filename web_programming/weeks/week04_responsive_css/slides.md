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

이번 주 방식: **부품 12개를 하나씩 비교**하고, 마지막에 `styles.css` 를 **조립**합니다.

- 파일 하나 = 속성 하나. 값 하나만 다른 형제를 나란히 놓고 차이를 봅니다.
- 첫 형제는 기본값. 주석은 다른 값. 주석을 풀거나 값을 바꿔 봅니다.
- 실습도 파일을 만드는 것이 아니라 **값을 바꿔 보는 것**입니다.
- 만들기는 2일차 끝에 한 번. 어느 규칙이 어느 파일에서 온 것인지 적어 둡니다.

작년 수업(dayNN/exNN 비교 파일 → 마지막에 만들기)과 같은 방식입니다.

---

# 1일차 — 선택자와 박스

`30분 설명·시연 → 60분 실습`

1. ex01 선택자 — 맞아야 적용되고, 겹치면 클래스가 이긴다
2. ex02 display — 줄을 차지하는지는 태그가 아니라 display
3. ex03 박스모델 — padding·border·margin 세 층
4. ex04 width·max-width — 창이 좁아지면 어느 쪽이 줄어드나
5. ex05 text-align — 가로는 되고 세로 가운데는 안 된다

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

## 1일차 · 4–10분 — ex01 선택자: 맞아야 적용되고, 겹치면 클래스가 이긴다

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

## 1일차 · 10–15분 — ex02 display: 줄을 차지하는지는 태그가 아니라 display

[examples/day1/ex02_display.html](examples/day1/ex02_display.html)
형제: div 3개 / span 3개 / span + `display: block` / div + `display: inline`

```css
.as-block  { display: block; }   /* 한 줄을 다 차지한다 */
.as-inline { display: inline; }  /* 글자처럼 옆으로 이어진다 */
```

- 1번 div 는 세로로 쌓이고 2번 span 은 옆으로 이어집니다. 태그의 기본값이 다를 뿐, 3·4번처럼 바꿀 수 있습니다.
- 바꿔 보기: `.as-block` 을 `inline` 으로, `.as-inline` 을 `block` 으로 → 3번과 4번이 자리를 바꾼다. 내일의 `flex` 도 같은 속성의 다른 값.

**줄을 차지하는지는 태그가 아니라 `display` 가 정한다.**

---

## 1일차 · 15–21분 — ex03 박스모델: padding·border·margin 세 층

[examples/day1/ex03_box_model.html](examples/day1/ex03_box_model.html)
형제: 기본 / `padding` / `border` / `margin` / 셋 다 (흰 frame 위의 하늘색 box)

```css
.pad { padding: 16px; }           /* 테두리 안쪽, 글자와 테두리 사이 */
.bd  { border: 4px solid navy; }  /* 테두리 */
.mg  { margin: 16px; }            /* 테두리 바깥, 이웃과의 거리 */
```

- 하늘색 배경은 `padding` 까지 칠해지고, `margin` 이 벌린 자리는 흰 frame 이 보입니다. F12 › Styles 맨 아래 상자 그림.
- 바꿔 보기: 세 값을 0 / 16 / 32 로 → 5번 상자에서 어느 층이 커지는지.

**안쪽 여백(padding)·테두리(border)·바깥 여백(margin)은 서로 다른 층이다.**

---

## 1일차 · 21–26분 — ex04 width와 max-width, margin auto

[examples/day1/ex04_width.html](examples/day1/ex04_width.html)
형제: 기본(부모 폭) / `width: 640px` / `max-width: 640px` / `max-width` + `margin` 좌우 `auto`

```css
.w      { width: 640px; }        /* 창이 좁아져도 640px, 삐져나간다 */
.mw     { max-width: 640px; }    /* 640px 까지만, 창이 좁으면 같이 줄어든다 */
.center { max-width: 640px; margin-left: auto; margin-right: auto; }
```

- `margin-left: auto; margin-right: auto` → 남는 폭을 왼쪽·오른쪽이 반씩. 합쳐서 `margin: 0 auto`.
- 바꿔 보기: 창 폭을 400px 까지 천천히 줄이기 → 2번만 삐져나가 가로 스크롤이 생긴다.

**`width` 는 폭을 못박고 `max-width` 는 상한만 둔다. 상한만 두면 창과 함께 준다.**

---

## 1일차 · 26–28분 — ex05 text-align, 그리고 안 되는 세로 가운데

[examples/day1/ex05_text_align.html](examples/day1/ex05_text_align.html)
형제: 기본 / `text-align: center` / `right` / `vertical-align: middle`(블록 상자엔 효과 없음)

```css
.center { text-align: center; }
.right  { text-align: right; }
.middle { vertical-align: middle; }  /* 블록 상자에는 아무 일도 일어나지 않는다 */
```

- 가로 정렬은 `text-align` 한 줄. 4번은 값을 뭘로 바꿔도 글자가 위에 붙어 있습니다.
- 바꿔 보기: `.middle` 값을 `bottom` 으로 → 그래도 안 움직인다. 답은 2일차 ex08.

**`vertical-align` 은 줄 안 글자끼리의 정렬이라 상자 안 내용은 못 옮긴다. 세로 정렬은 부모의 일이다 → ex08.**

---

## 1일차 · 28–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--선택자와-박스-60분) · [따라하기](walkthrough.md#1일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css)

1. 새 폴더 `web-week04` 에 지난주 파일을 넣고, `ex/` 에 ex01~ex05 를 저장합니다.
2. 파일마다 값을 하나 이상 바꿔 보고 화면이 어떻게 달라지는지 봅니다.
3. 끝: `web-week04` 저장소에 올리고 Pages 켜기 — 순서는 실습지

화면이 안 바뀌면 오류를 찾지 말고 **선택자 철자**와 **세미콜론**부터 봅니다.

**설명 합계: 4+6+5+6+5+2+2 = 30분**

---

# 2일차 — flex, 그리고 조립

`30분 설명·시연 → 60분 실습`

1. flex 원리 다섯 줄 — 부모·주축·교차축
2. ex06·ex07·ex08 — direction 이 주축, justify 는 주축, align 은 교차축
3. ex09·ex10 — wrap·gap 은 부모에, flex: 1 은 남는 공간
4. ex11 — @media 는 조건이 맞을 때만
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
3. `justify-content` 는 **주축** 정렬이다. "가로" 가 아니다.
4. `align-items` 는 **교차축** 정렬이다. `row` 에선 세로, `column` 에선 가로.
5. `flex: 1` 은 주축의 **남는 공간**을 그 자식이 차지한다.

ex06~ex10 은 이 다섯 줄을 한 줄씩 눈으로 확인하는 파일입니다.

---

## 2일차 · 4–9분 — ex06 flex-direction: 주축을 정한다

[examples/day2/ex06_flex_direction.html](examples/day2/ex06_flex_direction.html)
형제: flex 없음 / row / row-reverse / column / column-reverse / row + center / column + center

```css
.flex   { display: flex; }               /* 부모에 쓴다. 자식들이 한 줄로 선다 */
.column { flex-direction: column; }      /* 주축이 세로 ↓ (기본값 row 는 가로 →) */
.center { justify-content: center; }     /* 주축 방향으로 가운데 */
```

- 6번과 7번은 같은 `justify-content: center`. row 에선 가로, column 에선 세로 가운데.
- 바꿔 보기: 6·7번의 direction 을 서로 바꾸기 → 가운데 방향이 뒤집힌다. 자식에 `display: flex` → 상자 셋은 그대로, 숫자만 왼쪽으로.

**`display: flex` 는 부모에. `flex-direction` 이 주축을 정하고 `justify-content` 는 주축을 따라간다.**

---

## 2일차 · 9–13분 — ex07 justify-content: 주축 위의 남는 공간

[examples/day2/ex07_justify_content.html](examples/day2/ex07_justify_content.html)
형제: `flex-start` / `center` / `flex-end` / `space-between` / `space-around`, 주석 `space-evenly`

```css
.start   { justify-content: flex-start; }    /* 기본값: 앞에 모은다 */
.between { justify-content: space-between; } /* 양 끝에 붙이고 사이를 벌린다 */
.around  { justify-content: space-around; }  /* 상자마다 양옆에 같은 여백 */
/* .evenly { justify-content: space-evenly; } */ /* 모든 간격이 같다 */
```

- 상자 셋 48px, frame 300px. 남는 공간을 어디에 둘지가 값마다 다릅니다.
- 바꿔 보기: `.frame` 의 `height` 를 160px 로 하고 주석 `column` 풀기 → 다섯 개가 전부 세로로. `.evenly` 를 풀고 5번 class 를 `evenly` 로.

**`justify-content` 는 주축 위에서 남는 공간을 어떻게 나누는가다.**

---

## 2일차 · 13–17분 — ex08 align-items: 교차축, ex05의 답

[examples/day2/ex08_align_items.html](examples/day2/ex08_align_items.html)
형제: `stretch`(기본) / `flex-start` / `center` / `flex-end`, frame 주석 `column`

```css
.stretch { align-items: stretch; }     /* 기본값: 높이를 안 정한 자식은 끝까지 늘어난다 */
.start   { align-items: flex-start; }  /* 위 */
.center  { align-items: center; }      /* 세로 가운데 */
.end     { align-items: flex-end; }    /* 아래 */
```

- `.box` 에 높이가 없어 1번은 frame 높이만큼 늘어납니다. ex05 에서 안 되던 세로 가운데가 3번에서 됩니다.
- 바꿔 보기: `.frame` 의 `column` 주석 풀기 → 네 개가 전부 가로로 움직인다. 교차축이 가로가 됐기 때문.

**`align-items` 는 교차축 정렬. row 에선 세로, column 에선 가로.**

---

## 2일차 · 17–21분 — ex09 flex-wrap과 gap: 넘기기와 간격

[examples/day2/ex09_flex_wrap_gap.html](examples/day2/ex09_flex_wrap_gap.html)
형제: `nowrap`(64px×6 이 300px 안에 찌그러짐) / `wrap` / `wrap` + `gap: 16px`

```css
.nowrap { flex-wrap: nowrap; }  /* 기본값: 한 줄에 억지로 넣는다 */
.wrap   { flex-wrap: wrap; }    /* 안 들어가면 다음 줄로 넘긴다 */
.gap    { gap: 16px; }          /* 자식 사이 간격. 부모에 쓴다 */
```

- 64px × 6 = 384px. 300px 에 안 들어가면 1번은 찌그러뜨리고 2번은 넘깁니다. `gap` 은 부모에 — `nav a { gap }` 은 아무 일도 없습니다.
- 바꿔 보기: 자식 수 6 → 3 → 찌그러짐도 넘김도 사라진다. `gap` 을 0 / 16 / 32 로.

**넘길지는 `flex-wrap`, 사이 간격은 `gap`. 사이는 자식 하나가 정할 수 없으니 둘 다 부모에 쓴다.**

---

## 2일차 · 21–24분 — ex10 flex: 1 — 남는 공간을 차지한다

[examples/day2/ex10_flex_grow.html](examples/day2/ex10_flex_grow.html)
형제: 기본 / 가운데만 `flex: 1` / 셋 다 `flex: 1` / column 화면(header · main `flex: 1` · footer)

```css
.grow   { flex: 1; }   /* 주축의 남는 공간을 이 자식이 차지한다.  flex: 2 면 두 배 몫 */
.screen { display: flex; flex-direction: column; height: 200px; }
```

- 이 속성만 **자식**에 씁니다. "남는 공간을 내가 가진다"는 자식의 말이기 때문입니다. 4번은 세로에서도 같다는 것 — 작년 게임 타이틀 화면의 원리.
- 바꿔 보기: 3번 가운데 `<div>` 에만 `style="flex: 2"` → 가운데가 두 배 몫. `.grow` 의 `flex: 2` 주석은 셋 다 2 라 변화 없음.

**`flex: 1` 은 주축의 남는 공간을 그 자식이 차지한다. 여럿이면 숫자 비율로 나눈다.**

---

## 2일차 · 24–27분 — ex11 @media: 조건이 맞을 때만 뒤 규칙이 산다

[examples/day2/ex11_media.html](examples/day2/ex11_media.html)
형제: `@media (max-width: 600px)` 규칙이 있는 frame(`.narrow`) / 없는 frame

```css
.frame { display: flex; flex-direction: row; }   /* 평소에는 가로 */
@media (max-width: 600px) {                      /* 900px 으로 바꿔 보기 */
    .narrow { flex-direction: column; }
}
```

- 600px 이하일 때만 안쪽 규칙이 살아납니다. 그때 `.narrow` 는 `row` 와 `column` 을 둘 다 갖고, 세기가 같으니 뒤가 이깁니다(ex01). 확인은 F12 › 기기 모드 375.
- 바꿔 보기: 600 → 900 → 보통 창에서도 1번이 세로. `(max-width 600px)` 콜론 누락 → 오류 없이 덩어리 전체 무시.

**조건이 맞을 때만 뒤 규칙이 살아난다. 세기가 같으면 뒤가 이긴다.**

---

## 2일차 · 27–30분 — 조립: web-week04 styles.css, 그리고 실습 인계

```text
body  { max-width: 640px; margin: 0 auto; padding: 16px }      ← ex04 + ex03
nav   { display: flex; gap: 16px; flex-wrap: wrap }            ← ex06 + ex09 (부모에)
.card { background-color; padding; margin: 12px 0; border }    ← ex01 클래스 + ex03 세 층
@media (max-width: 600px) { nav { flex-direction: column } }   ← ex11 + ex06
```

[2일차 실습](lab.md#2일차--flex와-조립-60분) · [따라하기](walkthrough.md#2일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css)

1. ex06~ex11 여섯 파일을 `ex/` 에 저장하고 값을 바꿔 봅니다(35분까지).
2. 조립: `styles.css` 를 조립표 순서로, 세 페이지에 `link` 줄, `index.html` 에 `class="card"` 세 곳.
3. 1280 과 기기 모드 375 로 확인 → 끝: `web-week04` 에 올리고 캡처 — 순서는 실습지

**설명 합계: 4+5+4+4+4+3+3+3 = 30분**

---

## 부록 — ex12 position (선택, 설명 없음)

[examples/day2/ex12_position.html](examples/day2/ex12_position.html)
형제: `static`(기본) / `relative; top: 20px; left: 40px` / `absolute; right: 4px; bottom: 4px`

```css
.frame    { position: relative; }                           /* absolute 자식의 기준점 */
.relative { position: relative; top: 20px; left: 40px; }    /* 원래 자리에서 밀어낸다. 자리는 남는다 */
.absolute { position: absolute; right: 4px; bottom: 4px; }  /* 흐름에서 빠져 frame 모서리 기준 */
```

- 수업에서 다루지 않습니다. 먼저 끝났으면 열어서 값을 바꿔 봅니다.
- 3번에서 B 가 A 자리로 올라오는 이유: A 가 문서 흐름에서 빠졌기 때문입니다.

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
