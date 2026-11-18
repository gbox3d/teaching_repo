[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_form_input)

# 7주차 CSS 응용 예제 · 모바일 피드와 방명록

1일차에는 W3.CSS로 입력창·메뉴를 꾸미고, 트위터식 피드의 행 여백을 바꾼다. 2일차에는 같은 목록을 방명록에 적용한다. 이름과 메시지를 입력하면 작성자·시각·본문이 한 행에 담기고 새 글이 맨 위에 나타난다.

강의·시연 60분 중 첫 5분에는 파일·서버를 확인하고 마지막 5분에는 실습을 안내한다. 이어지는 30분 동안 첫날은 ex02·ex03의 클래스와 ex03b의 행 여백을, 둘째 날은 방명록의 CDN·클래스·색상을 수정한다. 파일·저장소는 수업 전에 준비하고 업로드는 수업 뒤에 한다.

```text
examples/
  day1/
    ex01/       before.html, index.html, app.js, README.md
    ex02/       index.html, app.js, README.md
    ex03/       index.html, app.js, README.md
    ex03b_list/ 수업 타임라인
  day2/
    ex04/       index.html, app.js, README.md
    ex05/       index.html, app.js, README.md
    web-week07/ 완성 사이트
```

## 실행 순서

| 예제 | 화면 | 학습 내용 |
|---|---|---|
| [ex01 설명](day1/ex01/README.md) | [연결 전](day1/ex01/before.html) · [연결 후](day1/ex01/index.html) | 같은 클래스와 JS에서 CDN 유무 비교, 클릭 횟수 표시 |
| [ex02 설명](day1/ex02/README.md) | [입력창과 버튼](day1/ex02/index.html) | `w3-input`, `w3-border`, `w3-button`, 입력 미리보기 |
| [ex03 설명](day1/ex03/README.md) | [카드와 메뉴](day1/ex03/index.html) | 카드·컨테이너·모바일 메뉴, ex02와 같은 JS |
| [ex03b 설명](day1/ex03b_list/README.md) | [수업 타임라인](day1/ex03b_list/index.html) | 새 글 보기, 작성자·시각·본문 구분, 행 여백 변경, 375px·1280px 비교 |
| [ex04 설명](day2/ex04/README.md) | [변환 전 방명록](day2/ex04/index.html) | 기존 CSS와 제공 폼 JS의 동작 |
| [ex05 설명](day2/ex05/README.md) | [변환 후 방명록](day2/ex05/index.html) | 같은 JS로 글 두 건을 등록하고 작성자·본문 배치와 최신순 확인 |

예제를 받을 때는 `examples/` 전체 구조를 유지한다. ex04가 `../web-week07/styles.css`를 읽기 때문이다. HTML은 브라우저로 열고 JS는 VS Code에서 읽는다. 파일을 수정한 뒤 저장하고 새로고침한다.

## CSS 연결

W3.CSS는 CDN의 고정 버전을 사용한다.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
```

W3.CSS 로컬 사본은 없다. ex01의 `before.html`에는 CDN 연결이 없다. ex04는 비교용 기존 `../web-week07/styles.css`를 사용한다. 완성본의 홈·소개 페이지도 기존 `styles.css`를 사용하고, 방명록만 W3.CSS를 사용한다.

ex02·ex03과 2일차 예제는 각 폴더의 `shared/examples.css`에 있는 `example-output`으로 긴 입력을 줄바꿈한다. 2일차 파일에는 방명록 폼과 피드용 규칙도 있다. 해당 폴더를 복사할 때 `shared/`를 함께 가져온다. [공통 CSS](../../../shared/examples.css)

ex03b에서 여백을 수정할 파일은 `day1/ex03b_list/shared/examples.css`다. `.post`의 `padding-block`을 `0.5rem`에서 `1rem`으로 바꾸면 각 글의 위아래 여백이 늘어난다. 새로고침하고 375px와 1280px에서 구분선의 간격과 긴 본문의 줄 수를 비교한다.

Network에서 Disable cache를 켜고 새로고침하여 `w3.min.css`의 응답 200을 확인한다. 인터넷 연결이 끊기면 W3.CSS 모양을 불러올 수 없다.

## JavaScript와 id 유지

ex04와 ex05의 `app.js`는 완성본의 `guestbook.js`와 동일하다. `guestbook-form`, `name`, `message`, `notice`, `list`는 JavaScript가 찾는 `id`이므로 유지한다. `email`은 이메일 입력 칸의 `id`이며 현재 JS는 그 값을 읽지 않는다.

이메일을 비우면 제출할 수 있다. 이메일을 입력한 경우에는 브라우저가 `type="email"`의 형식을 먼저 검사한다. `abc`는 제출이 막히고 `student01@example.com`은 제출할 수 있으며 목록에는 이름·메시지만 표시된다.

제공 코드를 읽으며 제출 → 입력값 읽기 → 빈값 검사 → 글 한 행 생성 → 목록 맨 앞에 삽입 → 입력 초기화 순서를 확인한다. `list.prepend(li)`가 새 글을 기존 글 위에 넣는다. ex04와 ex05에서 두 건을 차례로 등록해 이 순서를 확인한다.

## 완성 사이트

[`day2/web-week07/`](day2/web-week07/)에는 변환 전 시작 파일과 완성 사이트가 있다. 학생 저장소 맨 위에 복사한 뒤 완성 `guestbook.html`은 `guestbook.reference.html`로 보관하고, `guestbook.before.html`을 `guestbook.html`로 복사하여 실습한다. `examples/`는 비교용으로 별도 유지한다. 변환을 마친 사이트가 9주차 시작 파일이다.

| 파일 | 역할 |
|---|---|
| [guestbook.before.html](day2/web-week07/guestbook.before.html) | 기존 CSS와 제공 JS로 동작하는 실습 시작 파일 |
| [guestbook.html](day2/web-week07/guestbook.html) | W3.CSS CDN으로 꾸민 방명록 |
| [guestbook.js](day2/web-week07/guestbook.js) | 제공된 빈값 검사와 목록 추가 동작 |
| [index.html](day2/web-week07/index.html) · [app.js](day2/web-week07/app.js) | 지난주 홈과 버튼 동작 |
| [about.html](day2/web-week07/about.html) | 지난주 소개 페이지 |
| [styles.css](day2/web-week07/styles.css) | 홈·소개 페이지의 기존 스타일 |
| [shared/examples.css](day2/web-week07/shared/examples.css) | 방명록 폼과 피드의 배치, 긴 입력 줄바꿈 |
| [images/profile.png](day2/web-week07/images/profile.png) | 기존 프로필 이미지 |

[실습지](../lab.md)에는 매일 30분의 변경·확인 과제가 있고, [따라하기](../walkthrough.md)에는 준비와 실행 순서가 있다.

## 6주에서 9주까지의 파일 인계

| 파일 | 6주 → 7주 변경 | 9주 시작 상태 |
|---|---|---|
| `index.html`, `app.js`, `about.html`, `styles.css`, `images/profile.png` | 6주 완성본 유지. 홈의 카운터·다크 모드 포함 | 같은 파일 유지 |
| `guestbook.before.html`, `guestbook.js` | 정적 폼 대신 빈값 검사·목록 추가가 되는 시작 파일과 JS 제공 | 비교본·동작 코드 유지 |
| `guestbook.html` | 제공 시작 파일에 CDN과 매핑 클래스를 적용 | HTML·폼 ID·JS 그대로 유지 |
| `shared/examples.css` | 긴 입력 줄바꿈, 방명록 폼과 피드 배치용 CSS 추가 | 폴더째 유지 |

8주 시험은 별도 폴더에서 수행한다. 9주는 이 완성 웹 파일에 README·캡처·제공 SVG를 추가하므로 시험 답안을 출발점으로 사용하지 않는다.
