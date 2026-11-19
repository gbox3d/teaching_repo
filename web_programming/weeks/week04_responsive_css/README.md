실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

# 4주차 — CSS와 반응형 UI

3주차의 세 페이지에 자체 CSS를 연결한다. 비교 예제 13개와 선택 부록 ex14는 그대로 제공한다. 강의자가 비교와 조립을 시연하고 학생은 제공 파일의 지정된 값만 바꾼다. W3.CSS는 7주차에 도입한다.

## 학습 목표

선택자와 박스모델을 읽고 색·여백·최대 폭을 바꾼다. flex의 부모·주축·교차축을 구분하고, 600px 이하에서 메뉴를 세로로 배치한다. `max-width`와 `margin: 0 auto`의 역할을 화면에서 확인한다.

## 수업 전 준비

- 새 폴더와 저장소 `web-week04`는 수업 전에 준비한다. 3주차 `my-web` 파일을 `.git` 없이 복사한다. 받지 못한 학생에게는 [3주차 완성본](../week03_semantic_html/examples/day2/)을 배부한다.
- 강의자는 이번 주 [제공 완성본](examples/day2/web-week04/)의 CSS·세 HTML을 배부한다. 학생의 소개·취미·가상 정보는 보존하고, CSS 연결과 홈의 `class="card"` 세 곳을 미리 반영한다. 전체 조립은 강의자 시연이다.
- 비교 폴더 ex01~ex14도 `web-week04/ex/`에 미리 배부한다. 수업 중 파일별 Raw 다운로드·새 저장소 생성은 하지 않는다.
- VS Code·Chrome과 파일 또는 준비된 localhost 주소를 확인한다. `app.js`는 보존하지만 HTML에서 연결하지 않는다.
- 실명·학번·전화번호·실제 이메일 대신 별칭과 `student01@example.com`을 쓴다. Git 작업은 2주차에 배운 순서를 반복한다.

## 2일 수업 흐름

| 차시 | 강의·시연 60분 | 학생 실습 30분 | 확인 결과 |
|---|---|---|---|
| 4-1 | 준비 5, 선택자 15, 박스모델 15, max-width·margin 15, 비교 시연 5, 안내 5 | ex01·ex03 각 1값 10, 기존 CSS 색·여백·폭 3곳 15, 확인 5 | 기존 HTML을 꾸민 화면 |
| 4-2 | 준비 5, flex 부모·축 20, gap·정렬 10, media 15, 조립 시연 5, 안내 5 | flex 방향·정렬 2값 10, nav·media 5줄 이내 12, 375/1280px 확인·캡처 8 | 좁은 폭에서 세로 메뉴 |

첫 5분에는 파일과 실행 상태만 확인한다. 학생은 [실습지](lab.md)의 필수 항목을 수행하고 로컬 화면으로 확인한다. 공개 업로드와 Pages 확인은 수업 뒤 정리다. 비교 예제 전부 수정과 CSS 전문 재입력은 필수가 아니다.

## 결과물과 완료 기준

- 1일차는 ex01·ex03의 지정 값과 사이트 CSS의 색·여백·폭을 바꿔 본 화면을 확인한다.
- 2일차는 1280px의 가로 메뉴와 375px의 세로 메뉴를 확인한다. 세 페이지 모두 가로 넘침이 없어야 한다.
- 375px 홈 화면 캡처 한 장을 제출한다. 주소창과 기기 모드 폭이 보이게 찍는다. 파일 주소 또는 localhost도 인정한다.
- 수업 뒤 `web-week04`에 업로드하고 `https://student01.github.io/web-week04/`를 확인한다. `student01`은 본인 아이디로 바꾼다.

```text
web-week04/
  index.html  about.html  guestbook.html  styles.css  app.js  images/
  ex/ex01/ … ex/ex14/   ← 제공 비교 파일, 지정 항목만 수정
```

## 비교 예제와 시연 범위

ex01·ex03은 1일차 필수, ex07·ex08은 2일차 필수 비교다. 나머지는 강의자 시연이고 추가 값 변경은 선택이다. ex14는 선택 부록이다.

예제마다 폴더 하나에 내 사이트와 같은 이름의 두 파일(`index.html` 화면 · `styles.css` 규칙)을 둔다. `index.html` 을 열고, 규칙은 `styles.css` 에서 본다. `styles.css` 는 `index.html` 의 `<link rel="stylesheet" href="styles.css">` 한 줄이 불러온다.
첫 형제는 기본값이다(ex13 만 1번이 `@media` 규칙이 있는 상자). 주석은 대안값이다. 주석을 풀거나 값을 바꾸고 저장 → 새로고침으로 차이를 본다.

| 예제 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01/index.html](examples/day1/ex01/index.html) + [styles.css](examples/day1/ex01/styles.css) | `p` / `p.red` / `div.red` / `p.Red`(오타) / `nav a` / nav 밖 `a` | 선택자가 맞아야 적용된다. 클래스가 태그를 이긴다. 같은 선택자 두 번이면 뒤가 이긴다 | `/* p { color: gray; } */` 주석 풀기, 4번의 `class="Red"` 를 `class="red"` 로 |
| [ex02/index.html](examples/day1/ex02/index.html) + [styles.css](examples/day1/ex02/styles.css) | div 3 / span 3 / span + `display: block` / div + `display: inline` | 줄을 차지하는지는 태그가 아니라 `display` 가 정한다 | `block` ↔ `inline` |
| [ex03/index.html](examples/day1/ex03/index.html) + [styles.css](examples/day1/ex03/styles.css) | 기본 / `padding` / `border` / `margin` / 셋 다 | 안쪽 여백·테두리·바깥 여백은 서로 다른 층. 회색 frame 안에서 margin 이 벌린 자리가 보인다 | 세 값을 `0` / `16px` / `32px` 로 |
| [ex04/index.html](examples/day1/ex04/index.html) + [styles.css](examples/day1/ex04/styles.css) | 기본(부모 폭) / `width: 640px` / `max-width: 640px` | `width` 는 폭을 못박고, `max-width` 는 상한만 둬서 창이 좁으면 같이 준다 | 창을 400px 로 줄여 2번만 삐져나가는지 |
| [ex05/index.html](examples/day1/ex05/index.html) + [styles.css](examples/day1/ex05/styles.css) | 기본(왼쪽) / `margin-left: auto` / 좌우 `auto` / `margin: 0 auto` | `auto` 는 남는 폭을 가져간다. 양쪽이 나눠 가지면 상자가 가운데에 선다 | 3번의 `margin-right: auto` 지우기, `.box` 의 `max-width` 지우기 |
| [ex06/index.html](examples/day1/ex06/index.html) + [styles.css](examples/day1/ex06/styles.css) | 기본(왼쪽) / `center` / `right` | 상자 안 글자의 가로 자리를 정한다. 상자 자체는 움직이지 않는다 | `right` → `center` |
| [ex07/index.html](examples/day2/ex07/index.html) + [styles.css](examples/day2/ex07/styles.css) | flex 없음 / `display: flex`(row) / `row-reverse` / `column` / `column-reverse` | `display: flex` 는 부모에 쓴다. `flex-direction` 이 자식이 서는 방향(주축)을 정한다 | 2번의 `상자 1` 에 class `flex` 를 더해 보기(배치는 그대로) |
| [ex08/index.html](examples/day2/ex08/index.html) + [styles.css](examples/day2/ex08/styles.css) | `flex-start` / `center` / `flex-end` / `space-between` / `space-around` | 주축 위에서 남는 공간(회색)을 어떻게 나누나 | `.evenly` 주석 풀고 5번 frame 의 class 를 `evenly` 로 |
| [ex09/index.html](examples/day2/ex09/index.html) + [styles.css](examples/day2/ex09/styles.css) | `stretch`(기본) / `flex-start` / `center` / `flex-end` | 교차축(세로)에서 자식을 어디에 두나. frame 에 높이가 있어야 보인다 | `.frame` 의 `height: 100px` 지우기 |
| [ex10/index.html](examples/day2/ex10/index.html) + [styles.css](examples/day2/ex10/styles.css) | `nowrap`(기본) / `wrap` | 주축에 다 안 들어갈 때 넘길지는 `flex-wrap`. 부모에 쓴다 | 자식 수 6 → 3 |
| [ex11/index.html](examples/day2/ex11/index.html) + [styles.css](examples/day2/ex11/styles.css) | gap 없음 / `gap: 16px` / `gap: 32px` | 자식과 자식 사이 간격. 사이는 자식 하나가 정할 수 없으니 부모에 쓴다 | `gap16` 을 frame 에서 빼서 자식에 붙여 보기(아무 일도 없다) |
| [ex12/index.html](examples/day2/ex12/index.html) + [styles.css](examples/day2/ex12/styles.css) | 기본 / 가운데만 `flex: 1` / 셋 다 `flex: 1` | 주축의 남는 공간을 그 자식이 차지한다. 이 속성만 자식에 쓴다 | `flex: 2` 주석 풀기, 3번 가운데에만 `style="flex: 2"` |
| [ex13/index.html](examples/day2/ex13/index.html) + [styles.css](examples/day2/ex13/styles.css) | `@media (max-width: 600px)` 규칙이 있는 상자 / 없는 상자 | 조건이 맞을 때만 안쪽 규칙이 살아난다. 같은 선택자 두 번 → 뒤가 이김(ex01) | `600px` → `900px`, 기기 모드 375 |
| [ex14/index.html](examples/day2/ex14/index.html) + [styles.css](examples/day2/ex14/styles.css) (선택 부록) | `static` / `relative; top; left` / `absolute; right; bottom` | 흐름을 유지하는 relative와 흐름에서 빠지는 absolute | `top`·`left`·`right`·`bottom` 값 바꾸기 |

## 수업 자료

- [한글 슬라이드](slides.md) · [영문 슬라이드](slides_en.md)
- [실습과 제출 안내](lab.md) · [따라하기와 전체 코드](walkthrough.md) · [예제 안내](examples/README.md)
- 교재 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week04_responsive_css/index.html

## 다음 주 인계

5주차는 이 결과를 `.git` 없이 새 `web-week05`에 복사하고 `styles.css`를 이어 쓴다. `app.js`를 다시 작성하여 제공 출력 버튼에서 결과를 확인한다. 4주차 방명록에는 글 추가·저장 기능이 없다. 이메일 기본 검사는 브라우저가 수행하고, 유효한 폼을 제출하면 현재 문서를 GET으로 다시 열어 입력이 초기화된다. 화면에 글을 추가하는 기능은 7주차에 다룬다.

## 공식 참고 자료

- [CSS 첫걸음 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Styling_basics/Getting_started)
- [CSS 선택자 — MDN](https://developer.mozilla.org/ko/docs/Web/CSS/CSS_selectors)
- [박스 모델 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Styling_basics/Box_model)
- [플렉스박스(Flexbox) — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Flexbox)
- [미디어 쿼리 시작하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Media_queries)
- [기기 모드로 모바일 기기 시뮬레이션 — Chrome DevTools](https://developer.chrome.com/docs/devtools/device-mode)
