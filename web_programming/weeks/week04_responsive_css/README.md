# 4주차 — CSS와 반응형 UI

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

## 이번 주 질문

> 3주차에 만든 세 페이지를 색과 박스로 꾸미고, 휴대폰처럼 좁은 화면에서는 메뉴가 세로로 서게 할 수 있을까?

3주차에는 `my-web`을 홈·내 정보·방명록 세 페이지로 늘렸다. 화면은 꾸미지 않은 채로 두었다.
이번 주에는 `styles.css`를 **비우고 다시 써서** 세 페이지에 연결한다. 2주차 `styles.css`는 읽기만 한 틀이므로 한 줄도 남기지 않는다.
1일차에는 색과 글꼴, 2일차에는 박스와 `display: flex`, `@media` 한 덩어리로 375px 화면까지 맞춘다. 동작(JavaScript)은 5주차다.

## 학습 목표

1. `<link rel="stylesheet">`로 CSS 파일을 연결하고 `선택자 { 속성: 값; }` 규칙을 쓴다.
2. 태그 선택자(`body`·`h1`·`nav a`)와 `.class` 선택자(`.card`)로 대상을 고른다.
3. `color`·`background-color`·`font-size`·`font-family`·`text-align`으로 색과 글꼴을 정한다.
4. `padding`·`margin`·`border`로 박스를 만들고 `max-width`·`margin: 0 auto`로 본문을 가운데 둔다.
5. `display: flex`·`gap`·`flex-wrap`으로 메뉴를 가로로 놓고, `@media (max-width: 600px)`로 좁은 화면에서 세로로 바꾼다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/my-web/
         DevTools 기기 모드 375px
         메뉴 홈 / 내 정보 / 방명록 이 세로로 한 줄씩
         소개 문단과 취미 목록이 테두리 있는 흰 카드
         ← 주소창과 폭 375 표시가 함께 보이게 찍는다
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 제출은 이 캡처 **한 장**이다. 1280px 화면은 확인용이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | `git log --oneline`과 Commits 탭, `link` 줄 되살리기와 규칙의 모양, 태그·`.class` 선택자, 색과 글꼴 네 가지, DevTools Styles | 세 페이지에 `link` 줄 → `styles.css`를 비우고 `body`·`h1`·`h2`·`nav a`·`.card`·`footer` 여섯 규칙 | 확인용 화면 |
| 2일차 | `git restore`, 박스모델, `max-width`·`margin: 0 auto`, `display: flex`·`gap`·`flex-wrap`, `@media`와 기기 모드 375 | 메뉴 가로·카드 박스 → 본문 폭 → `@media` → 입력 칸 폭 → `git restore` | 캡처 1 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 3주차까지 push한 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, Chrome(DevTools), Git (`git --version`으로 확인)
- 이번 주에 고치는 파일은 `styles.css` 하나와 세 페이지의 `link` 한 줄씩이다. `app.js`는 열지 않는다(5주차에 비우고 다시 쓴다)
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 스타일시트 | stylesheet | 样式表 |
| 규칙 | rule | 规则 |
| 선택자 | selector | 选择器 |
| 속성 · 값 | property · value | 属性 · 值 |
| 클래스 | class | 类 |
| 박스모델 | box model | 盒模型 |
| 안여백 · 바깥여백 | padding · margin | 内边距 · 外边距 |
| 화면 폭 조건 | media query | 媒体查询 |

## 이번 주 범위

| 속성·명령 | 이번 주에 알아둘 뜻 |
|---|---|
| `<link rel="stylesheet" href="styles.css">` | 이 HTML이 쓸 CSS 파일을 연결한다. `<head>` 안에 둔다 |
| 규칙(rule) | `선택자 { 속성: 값; }` 한 덩어리. 속성 줄 끝에 세미콜론을 붙인다 |
| 태그 선택자 `body` · `h1` · `nav a` | 그 태그 전부를 고른다. `nav a`는 "`nav` 안에 있는 `a`" |
| `.class` 선택자 `.card` | HTML에 `class="card"`라고 적어 둔 것만 고른다. 점은 CSS에서만 쓴다 |
| `color` · `background-color` | 글자색 / 배경색. 값은 `#`과 여섯 자리로 적는다 |
| `font-size` · `font-family` | 글자 크기(`16px`) / 글꼴 목록(`system-ui, sans-serif`) |
| `text-align: center` | 글자를 가운데로 놓는다. 이번 주에는 `footer`에 쓴다 |
| `padding` · `margin` · `border` | 테두리 안쪽 여백 / 상자 바깥 여백 / 테두리(`1px solid #c3cbe6`) |
| `max-width: 640px` + `margin: 0 auto` | 본문이 640px보다 넓어지지 않게 하고, 남는 공간을 좌우로 나눠 가운데에 둔다 |
| `img`의 `width="160"` | 3주차에 HTML에 적은 그림 너비다. 이번 주에는 그대로 두고, 그림 크기를 CSS로 다루는 것은 이번 주 범위 밖이다 |
| `display: flex` · `gap` · `flex-wrap` | 안에 있는 것을 한 줄로 나란히 / 그 사이 간격 / 넘치면 다음 줄로 |
| `@media (max-width: 600px) { … }` | 화면 폭이 600px 이하일 때만 안쪽 규칙을 쓴다 |
| `flex-direction: column` | 가로로 놓던 것을 세로로 바꾼다 |
| `input, textarea { … }` | 쉼표로 묶으면 한 규칙을 두 대상에 함께 적용한다 |
| DevTools 기기 모드 | Ctrl+Shift+M(macOS ⌘+⇧+M). 폭을 `375`로 쳐서 좁은 화면을 본다 |
| `git restore <파일>` | commit하지 않은 수정을 마지막 commit 상태로 되돌린다 |
| `git restore --staged <파일>` | `git add`만 취소한다. 파일 내용은 그대로 둔다 |

우선순위(cascade)·specificity·상속 규칙, 이름 붙인 값(`--색이름`)·`clamp()`, `display: grid`, `transition`·애니메이션,
`:hover`·`:focus-visible` 같은 상태 선택자는 이번 주에 다루지 않는다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week04_responsive_css/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [styles.css](examples/day1/styles.css) · [index.html](examples/day1/index.html) · [about.html](examples/day1/about.html) · [guestbook.html](examples/day1/guestbook.html) · [app.js](examples/day1/app.js) · [images/profile.png](examples/day1/images/profile.png)
- 2일차 완성 코드: [styles.css](examples/day2/styles.css) · [index.html](examples/day2/index.html) · [about.html](examples/day2/about.html) · [guestbook.html](examples/day2/guestbook.html)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

## 완료 기준

- [ ] 세 페이지의 `<head>`에 `<link rel="stylesheet" href="styles.css">`가 있다.
- [ ] 공개 주소에서 배경색·제목 색·메뉴 색이 보인다.
- [ ] 소개 문단 두 개와 취미 목록이 테두리와 안여백이 있는 흰 카드로 보인다.
- [ ] 본문이 가운데로 모이고, 1280px에서 가로 스크롤 막대가 생기지 않는다.
- [ ] DevTools 기기 모드 375px에서 메뉴 세 개가 세로로 선다.
- [ ] 375px 화면 캡처 1장을 제출한다.

## 다음 수업 연결

이번 주까지 세 페이지는 **보이는 것**만 바뀌었다. 버튼도 입력 칸도 아직 아무 동작을 하지 않는다.
5주차에는 `app.js`를 비우고 다시 써서 JavaScript를 시작한다. `index.html`에 `<script src="app.js" defer></script>` 줄을 되살리고,
Console에 값을 찍어 보고, 함수가 만든 인사말을 화면에 한 줄 띄운다.
오늘 정한 색 값과 `.card`는 6주차 다크 모드에서 다시 쓴다. 결과는 같은 공개 주소 `https://<아이디>.github.io/my-web/`에서 확인한다.

## 공식 참고 자료

- [CSS 첫걸음 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Styling_basics/Getting_started)
- [CSS 선택자 — MDN](https://developer.mozilla.org/ko/docs/Web/CSS/CSS_selectors)
- [박스 모델 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Styling_basics/Box_model)
- [플렉스박스(Flexbox) — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Flexbox)
- [미디어 쿼리 시작하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Media_queries)
- [기기 모드로 모바일 기기 시뮬레이션 — Chrome DevTools](https://developer.chrome.com/docs/devtools/device-mode)
- [git restore — Git 공식 문서](https://git-scm.com/docs/git-restore)
- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
