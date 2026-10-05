# 4주차 실습 — 부품을 바꿔 보고 마지막에 조립하기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

이번 주 실습은 파일을 새로 만드는 것이 아니라 **값을 바꿔 보는 것**이다.
이번 주부터 주마다 새 저장소를 만든다. 이번 주 저장소는 `web-week04` 이고, 지난주 완성본에서 시작한다.
비교 파일 11개(부록 ex12 는 선택)를 `web-week04/ex/` 에 저장하고, 값 하나를 바꾼 뒤 화면이 어떻게 달라지는지 본다.
2일차 끝에 그 부품으로 `web-week04` 의 `styles.css` 를 조립한다. 채점 대상은 2일차 캡처 1장이다.
`student01` 은 예시 아이디이므로 본인 아이디로 바꾼다. `app.js` 는 이번 주에 열지 않는다.

파일을 받는 법과 값을 바꾸는 요령은 [따라하기 1일차](walkthrough.md#1일차)에 있다.
"바꿔 보기"는 **무엇이 달라질지 먼저 말해 보고** 저장 → 새로고침으로 확인한다.

## 1일차 — 선택자와 박스 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 새 폴더 `web-week04` 를 만들어 **File › Open Folder** 로 연다. 지난주 완성본을 넣는다: 내 3주차 저장소 GitHub 화면 › **Code › Download ZIP**, 못 하면 교재 [3주차 examples/day2/](../week03_semantic_html/examples/day2/) 를 **Raw** 로. `ex/` 폴더를 만들고 교재 [`examples/day1/`](examples/day1/) 의 ex01~ex05 를 **Raw** 로 저장한다(다 못 받으면 ex01 부터 시작하고 나머지는 문항을 시작할 때) |
| 5–14분 | ex01 선택자 — 저장하고 값 바꿔 보기 |
| 14–22분 | ex02 display |
| 22–31분 | ex03 박스모델 |
| 31–40분 | ex04 width·max-width |
| 40–47분 | ex05 text-align |
| 47–50분 | 확인: 다섯 파일이 `ex/` 에 있고, 각각 값 하나 이상을 바꿨는지 |
| 50–60분 | [이번 주 저장소 만들어 올리기](#이번-주-저장소-만들어-올리기): GitHub 에 새 저장소 `web-week04` → 터미널 여섯 줄 → **Settings › Pages** → 공개 주소 확인 → 공용 PC면 자격 증명 삭제 |

### 1. ex01 선택자 (`p` · `.red` · `nav a`)

[examples/day1/ex01_selector.html](examples/day1/ex01_selector.html) 을 `ex/ex01_selector.html` 로 저장한다. [따라하기 1일차](walkthrough.md#1일차)의 2단계를 본다.

- 바꿔 보기: 주석 `/* p { color: gray; } */` 를 푼다. 1번만 바뀌나, 2번도 바뀌나? 파랑 규칙이 위에 있는데 왜 그런가?
- 바꿔 보기: 4번의 `class="Red"` 를 `class="red"` 로 고친다. 고치기 전에는 왜 파랑이었나?
- 바꿔 보기: `.red` 규칙을 `p { color: blue; }` 보다 **위로** 옮긴다. 2번 색이 바뀌는가?
- 흔한 실수: 선택자가 안 맞으면 오류 없이 그 규칙만 조용히 버려진다. `.Red` 와 `.red` 는 다른 이름이다.

### 2. ex02 display (`display: block` · `display: inline`)

[examples/day1/ex02_display.html](examples/day1/ex02_display.html) 을 `ex/ex02_display.html` 로 저장한다.

- 바꿔 보기: `.as-block` 의 `block` 을 `inline` 으로, `.as-inline` 의 `inline` 을 `block` 으로 바꾼다. 3번·4번이 각각 어느 모양이 되나?
- 바꿔 보기: 1번 `div` 세 개에 `class="box as-inline"` 을 준다. `div` 인데도 옆으로 붙는가?
- 흔한 실수: "div 는 세로, span 은 가로"라고 정리하면 3번·4번을 설명할 수 없다. 줄을 차지하는지는 `display` 값이 정한다.

### 3. ex03 박스모델 (`padding` · `border` · `margin`)

[examples/day1/ex03_box_model.html](examples/day1/ex03_box_model.html) 을 `ex/ex03_box_model.html` 로 저장한다.

- 바꿔 보기: `.pad` 의 `16px` 을 `0` → `32px` 로 바꾼다. 하늘색이 어디까지 칠해지나?
- 바꿔 보기: `.mg` 의 `16px` 을 `0` → `32px` 로 바꾼다. 흰 frame 위에서 벌어지는 자리는 하늘색인가, 흰색인가?
- 바꿔 보기: 5번 상자를 F12 › **Elements** 에서 고르고 **Styles** 맨 아래 상자 그림의 네 값을 읽는다.
- 흔한 실수: `padding` 과 `margin` 을 같은 것으로 본다. 배경이 칠해지는 쪽이 `padding` 이다.

### 4. ex04 width (`width` · `max-width` · `margin: 0 auto`)

[examples/day1/ex04_width.html](examples/day1/ex04_width.html) 을 `ex/ex04_width.html` 로 저장한다.

- 바꿔 보기: 창 폭을 400px 까지 천천히 줄인다. 네 상자 중 어느 것만 삐져나가나? 가로 스크롤 막대는 언제 생기나?
- 바꿔 보기: `.center` 의 `margin-right: auto` 한 줄을 지운다. 4번 상자가 어느 쪽에 붙나?
- 바꿔 보기: `.mw` 의 `640px` 을 `300px` 로 바꾼다. 창이 넓을 때와 좁을 때 각각 어떻게 되나?
- 흔한 실수: 본문 폭을 `width: 640px` 로 정하면 폰 화면에서 삐져나간다. `max-width` 는 창이 좁으면 같이 줄어든다.

### 5. ex05 text-align (`text-align` · `vertical-align`)

[examples/day1/ex05_text_align.html](examples/day1/ex05_text_align.html) 을 `ex/ex05_text_align.html` 로 저장한다.

- 바꿔 보기: `.middle` 의 `middle` 을 `bottom` → `top` 으로 바꾼다. 4번 글자가 움직이는가?
- 바꿔 보기: `.right` 의 `right` 을 `center` 로 바꾼다. 3번이 어떻게 되나?
- 흔한 실수: 블록 상자 안의 세로 가운데를 `vertical-align` 으로 맞추려 한다. 이 방법으로는 안 된다. 답은 2일차 ex08 이다.

### 이번 주 저장소 만들어 올리기

50분이 되면 문항을 멈추고 올린다. 2주차에 배운 순서 그대로다.

1. GitHub 에서 새 저장소 `web-week04` 를 만든다. **Public**, README 는 추가하지 않는다.
2. VS Code 터미널에서 친다. 현재 폴더: `web-week04`

```bash
git init
git add .
git commit -m "4주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week04.git
git push -u origin main
```

3. 저장소 **Settings › Pages › Branch: main, /(root) › Save**.
4. 1~3분 뒤 `https://student01.github.io/web-week04/` 과 `https://student01.github.io/web-week04/ex/ex01_selector.html` 을 연다.
5. 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com` 을 지운다.

오늘 올린 것은 확인용이다. 두 주소가 열리면 된 것이다. 제출은 2일차에 캡처 한 장만 한다.

## 2일차 — flex와 조립 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC에 `web-week04` 폴더가 남아 있으면 **File › Open Folder** 로 연다. 없으면 `git clone https://github.com/student01/web-week04.git` 뒤 **File › Open Folder**. 교재 [`examples/day2/`](examples/day2/) 의 여섯 파일(ex06~ex11)을 **Raw** 로 `ex/` 에 먼저 저장한다 |
| 5–11분 | ex06 flex-direction |
| 11–16분 | ex07 justify-content |
| 16–21분 | ex08 align-items |
| 21–26분 | ex09 flex-wrap·gap |
| 26–30분 | ex10 flex: 1 |
| 30–35분 | ex11 @media |
| 35–50분 | 조립: `styles.css` 규칙을 조립표 순서로 쓰기, 세 페이지 `link` 줄, `index.html` 의 `class="card"` 세 곳 |
| 50–55분 | 1280 과 기기 모드 375 에서 확인 |
| 55–60분 | 올리기(2주차 순서 그대로): `git add .` → `git commit -m "4주차 2일차"` → `git push` → 공개 주소 `https://student01.github.io/web-week04/` 새로고침 → 375 **캡처 1장** → 공용 PC면 자격 증명 삭제 |

팁: 실험하다 비교 파일을 망쳤으면 교재에서 그 파일을 **Raw** 로 다시 받는다.

flex 는 세 낱말로 읽는다. **부모**(`display: flex` 를 쓰는 곳), **주축**(`flex-direction` 이 정하는 방향), **교차축**(주축과 직각). `justify-content` 는 주축, `align-items` 는 교차축이다. "가로·세로"로 부르지 않는다. `column` 에서 뒤집히기 때문이다.
여섯 파일을 받는 법은 [따라하기 2일차](walkthrough.md#2일차)에 있다.
파일마다 첫 번째 바꿔 보기만 하고 다음 파일로 넘어가도 된다. 둘째·셋째는 조립이 끝난 뒤 한다.

### 6. ex06 flex-direction (`display: flex` · `flex-direction`)

[examples/day2/ex06_flex_direction.html](examples/day2/ex06_flex_direction.html) 을 `ex/ex06_flex_direction.html` 로 저장한다.

- 바꿔 보기: 6번 frame 의 `row` 를 `column` 으로, 7번의 `column` 을 `row` 로 바꾼다. 같은 `justify-content: center` 인데 상자가 어느 방향으로 움직이나?
- 바꿔 보기: 1번 frame 은 그대로 두고, 그 안의 `.box` 세 개에 `style="display: flex"` 를 준다. 무엇이 달라지나?
- 바꿔 보기: 2번 frame 에 `row-reverse` 를 주면 숫자 순서가 어떻게 되나? 상자는 어느 쪽 끝에서 시작하나?
- 흔한 실수: `display: flex` 를 자식에 준다. 아무 일도 없다. 부모에 쓴다.

### 7. ex07 justify-content (`justify-content`)

[examples/day2/ex07_justify_content.html](examples/day2/ex07_justify_content.html) 을 `ex/ex07_justify_content.html` 로 저장한다.

- 바꿔 보기: `.frame` 안의 주석 `/* flex-direction: column; */` 을 푼다. 다섯 frame 의 상자가 어느 방향으로 움직이나? `.frame` 의 `height` 를 `160px` 로 늘리면 더 잘 보인다.
- 바꿔 보기: 4번 `space-between` 과 5번 `space-around` 에서 양 끝 여백을 비교한다. 어느 쪽이 벽에 붙나?
- 바꿔 보기: 마지막 주석 `.evenly` 를 풀고 5번 frame 의 class 를 `evenly` 로 바꾼다. `space-around` 와 무엇이 다른가?
- 흔한 실수: "justify 는 가로"라고 정리한다. 주석을 푼 순간 다섯 개가 전부 세로로 움직인다. 주축이다.

### 8. ex08 align-items (`align-items`)

[examples/day2/ex08_align_items.html](examples/day2/ex08_align_items.html) 을 `ex/ex08_align_items.html` 로 저장한다.

- 바꿔 보기: `.frame` 의 주석 `/* flex-direction: column; */` 을 푼다. 네 frame 의 상자가 어느 방향으로 움직이나? ex07 과 반대인가?
- 바꿔 보기: `.box` 에 `height: 32px;` 한 줄을 더한다. 1번 `stretch` 가 어떻게 되나? 왜 늘어나지 않나?
- 바꿔 보기: 3번 frame 의 `class` 에서 `center` 를 지운다(`stretch` 기본값으로). 상자가 어떻게 되나? 다시 넣으면 ex05 4번이 못 하던 세로 가운데가 되는가? 그 한 줄이 부모에 있는지 자식에 있는지 본다.
- 흔한 실수: `align-items: center` 를 자식에 쓴다. 부모에 쓴다.

### 9. ex09 flex-wrap과 gap (`flex-wrap` · `gap`)

[examples/day2/ex09_flex_wrap_gap.html](examples/day2/ex09_flex_wrap_gap.html) 을 `ex/ex09_flex_wrap_gap.html` 로 저장한다.

- 바꿔 보기: 1번 frame 의 자식을 6개에서 3개로 줄인다. 찌그러짐이 사라지나? 왜 그런가?
- 바꿔 보기: `.gap` 의 `16px` 을 `0` → `32px` 로 바꾼다. 3번 frame 에서 한 줄에 들어가는 상자 수가 달라지나?
- 바꿔 보기: `gap: 16px;` 을 `.gap` 이 아니라 `.box` 로 옮긴다. 간격이 생기나?
- 흔한 실수: `gap` 을 자식(`nav a`)에 쓴다. 아무 일도 없다. `flex-wrap` 도 `gap` 도 부모에 쓴다.

### 10. ex10 flex: 1 (`flex`)

[examples/day2/ex10_flex_grow.html](examples/day2/ex10_flex_grow.html) 을 `ex/ex10_flex_grow.html` 로 저장한다.

- 바꿔 보기: `.grow` 안의 주석 `/* flex: 2; */` 를 푼다. 3번 frame 의 세 상자 폭이 어떻게 되나? 2번은?
- 바꿔 보기: 4번 `.screen` 에서 `main` 의 `class="grow"` 를 `header` 로 옮긴다. 어느 칸이 커지나?
- 바꿔 보기: `.screen` 의 `height` 를 `400px` 로 늘린다. `header`·`footer` 는 커지나?
- 흔한 실수: `flex: 1` 을 부모에 쓴다. 이것은 자식에 쓰는 몇 안 되는 속성이다. "남는 공간을 이 자식이 차지한다"는 뜻이다.

### 11. ex11 @media (`@media (max-width: 600px)`)

[examples/day2/ex11_media.html](examples/day2/ex11_media.html) 을 `ex/ex11_media.html` 로 저장한다.

- 바꿔 보기: F12 › 기기 모드(**Ctrl+Shift+M**, macOS **⌘+⇧+M**) 에서 폭을 `375` 로 한다. 1번·2번 중 어느 것이 세로로 서나?
- 바꿔 보기: `600px` 을 `900px` 으로 바꾼다. 기기 모드 폭 `800` 에서 무엇이 달라지나?
- 바꿔 보기: `@media` 덩어리를 파일 **위쪽**, `.frame` 규칙보다 앞으로 옮긴다. 375 에서도 세로로 서나? ex01 의 "뒤가 이긴다"와 연결해 본다.
- 흔한 실수: `(max-width 600px)` 처럼 콜론을 빠뜨린다. 오류 없이 덩어리 전체가 무시된다.

### 12. 조립 — `styles.css` (`link` · `class="card"`)

`web-week04` 의 `styles.css` 를 비우고, 아래 조립표 순서로 규칙을 쓴다. 규칙마다 "어느 ex 에서 본 것"인지 적혀 있다. 전문과 세 페이지 코드는 [따라하기 2일차](walkthrough.md#2일차)에 있다.

| `styles.css` 규칙 | 어느 ex 에서 본 것 |
|---|---|
| `body { background-color; color; font-family; font-size }` | ex01 태그 선택자. 색·글꼴은 3주차 HTML 에 없던 새 속성 4개 |
| `body { max-width: 640px; margin: 0 auto; padding: 16px }` | ex04 (`max-width`·`margin` auto), ex03 (`padding`) |
| `h1`·`h2` `{ color … }` | ex01 태그 선택자 |
| `nav { display: flex; gap: 16px; flex-wrap: wrap }` | ex06 (flex 는 부모에), ex09 (`gap`·`wrap` 도 부모에) |
| `nav a { color }` | ex01 자손 선택자 |
| `.card { background-color; padding; margin: 12px 0; border }` | ex01 클래스 선택자, ex03 세 층 |
| `input, textarea { width: 280px; max-width: 100% }` | ex04 3번 `max-width` 로 좁은 화면 대비. `width: 280px` 은 평소 폭, `max-width: 100%` 는 부모보다 못 커지게 하는 상한. 쉼표 = 두 대상에 같은 규칙 |
| `footer { text-align: center; … }` | ex05 |
| `@media (max-width: 600px) { nav { flex-direction: column } }` | ex11 (조건) + ex06 (`column`) |

- 세 페이지(`index.html`·`about.html`·`guestbook.html`)의 `<head>` 에 `<link rel="stylesheet" href="styles.css">` 가 있어야 규칙이 적용된다. 없는 페이지는 3주차 화면 그대로다.
- `index.html` 의 소개 문단 두 개와 취미 `ul` 에 `class="card"` 를 붙인다. HTML 은 점 없이 `card`, CSS 는 점을 붙여 `.card`.
- 바꿔 보기: 조립이 끝나면 `nav` 의 `gap` 을 `32px` 로, `body` 의 `max-width` 를 `480px` 로 바꿔 본다. 어느 ex 의 결과와 같은가? 확인 뒤 원래 값으로 돌린다.
- 흔한 실수: `nav` 규칙을 빠뜨리고 `@media` 만 쓴다. `flex-direction` 은 `display: flex` 인 부모에서만 뜻이 있다.

확인: 1280 에서 메뉴 세 개가 가로 한 줄, 기기 모드 375 에서 세로 세 줄. 두 폭 모두 가로 스크롤 막대가 없어야 한다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 올린 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub `web-week04` 저장소의 **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 다시 확인해도 된다. 새 저장소라 **Settings › Pages** 에서 Branch 가 `main` 으로 저장됐는지도 본다 |
| push 가 거부되거나 로그인 창이 안 뜬다 | [2주차 막혔을 때 표](../week02_github_pages/lab.md#막혔을-때)를 본다. 올리는 순서는 2주차와 같다 |
| 규칙을 썼는데 아무 반응이 없고 오류도 없다 | **CSS 는 오류 메시지가 없다.** 틀린 줄이나 덩어리는 조용히 무시되고 나머지는 그대로 적용된다. F12 › **Elements** 에서 그 요소를 고르고 **Styles** 에 규칙이 보이는지, 취소선이 그어져 있는지 본다 |
| `display: flex` 를 줬는데 자식이 한 줄로 안 선다 | `display: flex` 를 자식(`.box`·`nav a`)에 줬는지 본다. 자식에 주면 아무 일도 없다. 부모(`.frame`·`nav`)에 쓴다 |
| `gap` 을 줬는데 간격이 안 생긴다 | `gap` 을 `nav a` 에 줬는지 본다. 아무 일도 없다. `gap` 은 부모 `nav` 에 쓴다 |
| 한 규칙만 통째로 안 먹는다 | 클래스 오타·대소문자를 본다. `.Red`·`.Card`·`.cards` 는 다른 선택자다. HTML 의 `class="…"` 와 CSS 의 `.…` 를 나란히 비교한다 |
| 375 에서도 메뉴가 가로다 | `@media (max-width: 600px)` 의 **콜론**을 본다. `(max-width 600px)` 로 적으면 오류 없이 덩어리 통째로 무시된다. 그 다음 `nav` 에 `display: flex` 가 있는지, 기기 모드 폭이 600 이하인지 본다 |
| 두 줄이 한꺼번에 안 먹는다 | 바로 위 줄 끝의 세미콜론을 본다. `color: #17213a` 뒤에 `;` 가 없으면 그 줄과 다음 줄이 함께 무시된다 |
| 규칙을 더했는데 그 아래 규칙들이 전부 이상해졌다 | 중괄호 짝을 본다. `}` 를 빠뜨리면 다음 규칙이 앞 규칙 안으로 들어간 것으로 읽힌다. VS Code 에서 `{` 에 커서를 두면 짝이 되는 `}` 가 함께 표시된다 |
| 화면 아래에 가로 스크롤 막대가 생긴다 | `width: 640px` 으로 적지 않았는지 본다. ex04 의 2번이 그 모습이다. `max-width` 로 고친다 |
| 꾸미기가 하나도 안 먹고 3주차 화면 그대로다 | `<head>` 에 `link` 줄이 있는지, `href` 가 `styles.css` 인지 본다. `style.css`(s 빠짐)는 다른 이름이다. F12 › **Network** 에서 새로고침하면 그 줄이 빨간 **404** 로 보인다 |
| 공개 주소 `…/web-week04/ex/ex01_selector.html` 이 404 다 | ① 폴더 이름이 `ex` 인지(`Ex`·`examples` 는 다른 이름) ② 파일 이름이 교재와 같은지 ③ GitHub 의 `web-week04` 저장소 화면에 `ex/` 폴더와 그 파일이 보이는지 본다. 안 보이면 아직 올리지 않은 것이다 |

한 번에 한 곳만 고치고 다시 새로고침한다. 해결되지 않으면 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

`https://student01.github.io/web-week04/` (본인 아이디) 을 열고 F12 → 기기 모드(**Ctrl+Shift+M**) → 폭 `375` 로 맞춘 화면을 캡처한다.

- 메뉴 `홈`·`내 정보`·`방명록` 이 **세로로 한 줄씩** 보인다.
- 소개 문단과 취미 목록이 테두리 있는 흰 카드로 보인다.
- **주소창과 폭 375 표시가 함께 보이게** 찍는다.

1일차에 올린 것과 `ex/` 실험 파일은 확인용이며 따로 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- ex07: 주석 `.evenly` 를 풀어 `space-evenly` 를 써 본다. `space-around` 와 양 끝 여백을 비교한다.
- ex10: `/* flex: 2; */` 주석을 풀고 2번·3번 frame 의 폭 비율을 본다.
- ex06: 한 frame 에 `column-reverse` 와 `center` 를 같이 준다. 숫자 순서와 위치가 어떻게 되나?
- ex12: [examples/day2/ex12_position.html](examples/day2/ex12_position.html) 을 열어 `top`·`left`·`right`·`bottom` 값을 바꿔 본다. 부록이며 설명하지 않는다.
- ex10 의 4번 `.screen` 을 `width: 100%; height: 100vh` 로 바꿔 창 전체를 header·main·footer 로 나누는 타이틀 화면을 만들어 본다.
- 선택: 정적 서버 [`server.mjs`](../../tools/static-server/README.md) 를 `web-week04` 에 받아 `http://localhost:8000/` 으로 열어 본다. 설명은 5주차에 한다.

추가 과제는 선택 사항이며 채점하지 않는다.
