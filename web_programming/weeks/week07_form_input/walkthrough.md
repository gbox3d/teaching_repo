[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_form_input)

# 7주차 CSS 응용 따라하기 · 모바일 피드와 방명록

첫날은 W3.CSS 메뉴를 작은 화면에서 확인하고 트위터식 피드의 행 간격을 바꾼다. 둘째 날은 방명록 폼에 글을 남겨 같은 피드에 쌓이는 모습을 확인한다. 강의·시연은 매일 60분, 실습은 30분이다.

강의 첫 5분은 파일·서버 확인에, 마지막 5분은 실습·다음 수업 안내에 쓴다. 예제 비교와 폼 JS 읽기는 강의자와 함께 하고, 학생은 [실습지](lab.md)에 따라 CSS를 바꾸고 결과를 확인한다. 다운로드와 게시 작업은 수업 전후에 진행한다.

## 수업 전 준비

### 1. 작업 폴더와 예제 준비

새 작업 폴더 `web-week07`을 만들고 VS Code로 연다. 교재 저장소의 **Code › Download ZIP**으로 파일을 받은 뒤, `web_programming/weeks/week07_form_input/examples/`를 작업 폴더에 복사한다. Git을 사용 중이면 교재 저장소에서 필요한 폴더를 복사해도 된다.

이번 주 [사이트 폴더](examples/day2/web-week07/)의 파일과 `images/`, `shared/`도 작업 폴더 맨 위에 복사한다. 완성 `guestbook.html`의 이름을 `guestbook.reference.html`로 바꾸어 대조용으로 보관한다. `guestbook.before.html`을 복사하고 복사본 이름을 `guestbook.html`로 정한다. 실습은 이 변환 전 화면에서 시작한다. 폼 JS는 이미 동작하며, 홈·소개는 지난주 파일이다.

```text
web-week07/
  examples/
    day1/ex01/ ... ex03/
    day1/ex03b_list/
    day2/ex04/ ... ex05/
    day2/web-week07/
  images/profile.png
  shared/examples.css
  index.html
  about.html
  guestbook.html
  guestbook.before.html
  guestbook.reference.html
  guestbook.js
  app.js
  styles.css
  server.mjs
```

`server.mjs`는 [수업용 서버](../../tools/static-server/server.mjs)에서 준비한다. 예제의 `README.md`에는 설명, HTML에는 화면, JS에는 동작이 있다. `examples/day2/ex04/index.html`이 읽는 `../web-week07/styles.css` 경로를 유지해야 한다.

### 2. 저장소와 실행 준비

GitHub에 빈 저장소 `web-week07`을 만들고, Git 사용자 설정은 지난주 설정을 사용한다. 이미 이번 주 저장소가 있으면 다시 만들지 않는다. 새 작업 폴더에서만 다음 명령을 실행한다. `student01`은 본인 GitHub 아이디로 바꾼다.

```bash
git init
git branch -M main
git remote add origin https://github.com/student01/web-week07.git
```

VS Code 터미널의 현재 폴더가 `web-week07`인지 확인하고 서버를 시작한다.

```bash
node server.mjs
```

`http://localhost:8000/`을 연다. 서버가 없는 PC는 HTML 파일을 직접 열 수 있지만 CDN 연결에는 인터넷이 필요하다. Git 설정이나 다운로드가 끝나지 않았다면 강사가 제공한 예제를 먼저 열고 수업 후 준비를 마친다.

## 1일차

### 3. ex01 CDN 연결 전후 비교

`http://localhost:8000/examples/day1/ex01/before.html`을 연다. 버튼을 눌러 클릭 횟수를 확인하고 **연결 후** 링크로 이동한다. 두 페이지는 같은 `app.js`를 사용한다. 페이지가 바뀌면 횟수는 처음부터 다시 센다.

VS Code에서 `before.html`과 `index.html`을 연다. 두 파일 모두 버튼에 `w3-button w3-teal`이 있다. `index.html`에는 다음 CDN 연결이 추가되어 클래스의 모양이 적용된다.

```html
<link rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
```

강의자는 `index.html`의 `w3-teal`을 `w3-blue`로 바꾸어 시연한다. 저장하고 새로고침하여 색상과 클릭 동작을 확인한다. 학생의 같은 변경은 선택이다. `id="button"`은 JS가 버튼을 찾는 값이므로 유지한다.

### 4. CDN 요청 확인

F12 → Network를 연다. **Disable cache**를 켜고 새로고침한다. `w3.min.css`를 선택해 다음을 확인한다.

- Request URL: `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`
- Status Code: `200`
- Type: stylesheet 또는 CSS

CSS 요청이 없으면 `<link>`를, 요청이 실패하면 주소와 인터넷 연결을 확인한다. 다른 파일의 404는 해당 경로를 확인한다. CDN 라이브러리를 로컬 파일로 복사하지 않는다.

### 5. ex02 입력창과 버튼 확인

`http://localhost:8000/examples/day1/ex02/`를 연다. HTML에서 `w3-input w3-border`가 입력창에, `w3-button w3-teal`이 버튼에 있는지 확인한다. 이름·메시지를 입력하고 **미리보기**를 누른다. 결과에 `이름: 메시지`가 표시되고 입력은 유지된다.

버튼 색상 한 곳을 바꾸고 다시 실행한다. JavaScript는 수정하지 않아도 같은 미리보기가 나온다. HTML 클래스만 바꾼 뒤에도 입력 결과가 표시되는지 확인한다.

### 6. ex03 카드와 모바일 메뉴 확인

`http://localhost:8000/examples/day1/ex03/`를 연다. 입력 카드와 미리보기 카드가 위아래로 놓여 있다. `w3-card`는 카드 모양을, `w3-container`와 `w3-padding`은 내용의 여백을 정한다. 메뉴는 `w3-bar` 안에 `w3-bar-item w3-button w3-mobile`을 붙인다.

F12의 기기 도구 모음을 켜고 Responsive 폭을 1280에서 375로 바꾼다. `w3-mobile` 메뉴 항목은 600px 이하에서 세로로 배치된다. 카드는 두 폭에서 모두 위아래로 놓인다. 메뉴 색상이나 카드 여백 한 곳을 바꾼다.

### 6a. ex03b 트위터식 피드의 행 간격 변경

1. `http://localhost:8000/examples/day1/ex03b_list/`를 연다. 첫 글의 작성자를 보고 `Tab`으로 **새 글 1개 보기**에 이동해 `Enter`를 누른다. 김민서의 10:42 글이 기존 첫 글 위에 나타나고 김민서 이름에 초점이 표시된다.
2. `examples/day1/ex03b_list/index.html`의 `ol`에서 `li` 하나가 화면의 어느 글인지 본문으로 찾아본다. 각 행의 왼쪽에는 이름 한 글자를 넣은 원이, 오른쪽에는 작성자·시각과 본문이 보인다.
3. 폭을 375px로 맞춰 박준호의 글을 본다. `examples/day1/ex03b_list/shared/examples.css`에서 `.post`의 `padding-block: 0.5rem`을 `padding-block: 1rem`으로 바꾸고 저장한다. 새로고침한 뒤 박준호의 본문과 아래쪽 구분선 사이가 얼마나 벌어졌는지 확인한다.
4. 폭을 1280px로 바꾼다. 긴 글이 몇 줄로 보이는지 375px일 때와 비교한다. 글마다 작성자와 본문이 같은 행에 묶여 있는지, 375px에서 좌우로 스크롤할 필요가 있는지도 확인한다.

## 2일차

### 7. ex04와 ex05의 같은 동작 확인

`http://localhost:8000/examples/day2/ex04/`와 `http://localhost:8000/examples/day2/ex05/`를 각각 연다. ex04는 기존 `styles.css`, ex05는 W3.CSS CDN을 사용한다.

각 화면에서 이름을 비우고 **남기기**를 눌러 안내를 확인한다. `student01`로 `안녕하세요`를 쓰고 `student02`로 `반갑습니다`를 쓴다. 두 화면 모두 두 번째 글이 맨 위에 오고, 제출 뒤 입력이 비고 이름 칸으로 커서가 이동한다. ex05에서 작성자와 본문이 어떻게 배치되는지 전날 피드와 비교한다.

VS Code 탐색기에서 ex04의 `app.js`를 우클릭해 **Select for Compare**, ex05의 `app.js`를 우클릭해 **Compare with Selected**를 선택한다. 차이가 없다. 제공 JS는 완성본의 `guestbook.js`와도 같다.

### 8. 제공 JS의 처리 순서 읽기

`app.js`에서 다음 순서를 찾는다. 후속 수업의 배열·저장 기능이 이 흐름에서 이어지므로 코드와 화면 결과를 함께 확인한다.

```text
submit → preventDefault
value.trim() → 이름·메시지 읽기
빈값이면 안내·focus·return
작성자·본문을 textContent로 넣은 글 한 행 생성 → list.prepend(li)
reset → 이름 칸 focus
input 이벤트 → clearNotice
```

`return`을 만나면 그 아래의 목록 추가 코드를 건너뛴다. `prepend`는 새 글을 목록 맨 앞에 넣는다. 글 안에는 작성자와 작성 시각, 본문이 들어간다. `reset()`은 폼을 초기값으로 되돌린다. 이 폼의 초기값은 비어 있다. 이메일은 비워 두거나 `student01@example.com`을 입력한다. 브라우저는 submit 이벤트 전에 이메일 형식을 검사하고, 제공 JS는 이름과 메시지만 읽는다.

### 9. 방명록 HTML 변환

ex04와 ex05의 `index.html`을 비교한다. 기존 CSS 링크가 CDN 링크로 바뀌고, 입력창·버튼·메뉴·카드에 `w3-*` 클래스가 붙는다. `guestbook-form`, `name`, `message`, `notice`, `list`의 `id`는 유지된다.

작업 폴더 맨 위의 `guestbook.html`은 준비 단계에서 복사한 변환 전 파일이다. `<link>`의 `styles.css`를 지정된 CDN 주소로 바꾼다. `<nav>...</nav>`를 `<header>` 밖으로 옮겨 `</header>` 바로 뒤에 둔다.

시작 파일에는 이름·이메일을 감싸는 `.composer-fields`, 목록 제목과 ‘최신순’을 담은 `.feed-heading`, 첫 글을 쓰기 전에 보이는 `.feed-empty`가 들어 있다. 이 요소를 그대로 두고 두 구역을 만든다.

1. 첫 번째 `<section>`은 `<h2>글 남기기</h2>` 앞에서 시작해 `#notice` 뒤에서 닫는다.
2. 두 번째 `<section>`은 `<div class="feed-heading">` 앞에서 시작해 `<p class="feed-empty">`의 닫는 태그 뒤에서 닫는다.

다음 표의 클래스를 해당 태그에 넣는다.

| 대상 | class 값 |
|---|---|
| `body` | `w3-light-grey guestbook-page` |
| `header` | `w3-container w3-teal w3-padding-16` |
| `nav` | `w3-bar w3-white w3-card` |
| 각 메뉴의 `a` | `w3-bar-item w3-button w3-mobile` |
| `main` | `w3-content w3-padding` |
| 두 `section` | `w3-container w3-card w3-white w3-margin-top` |
| 이름·이메일 `input`, 메시지 `textarea` | `w3-input w3-border` |
| 제출 `button` | `w3-button w3-teal` |
| `#notice` | `w3-text-red` |
| `#list` | `card example-output`을 `w3-ul example-output feed-list`로 변경 |

여기까지 적용하고 버튼이나 제목의 `w3-teal`을 `w3-blue` 등으로 바꾼다. 현재 메뉴의 색상과 footer 여백은 대조 파일에서 확인할 수 있다.

제공된 `id`와 다음 `guestbook.js` 연결은 유지한다.

```html
<script src="guestbook.js" defer></script>
```

`index.html`과 `about.html`은 기존 `styles.css`를 사용한다. 방명록에는 `shared/examples.css` 링크를 유지한다. 이 파일에는 긴 입력을 줄바꿈하는 규칙과 `feed-list` 안에서 작성자·시각·본문을 배치하는 규칙이 들어 있다. 목록 뒤의 빈 상태 문구도 유지한다.

### 10. 동작과 375px 화면 점검

`http://localhost:8000/guestbook.html`을 열고 이름·메시지 빈값 안내를 확인한다. 입력하면 안내가 사라지는지, 제출 뒤 입력이 비고 이름 칸에 커서가 오는지 본다. 두 건을 차례로 등록해 두 번째 작성자와 본문이 첫 번째 글 위에 나타나는지 확인한다.

375px 화면에서 메뉴와 입력창이 가로로 넘치지 않는지 확인한다. Network에서 CDN 요청 200, Console에서 코드 오류가 없는지 확인한다. 주소, 변경한 색상, 글 두 건이 보이는 실행 화면 한 장을 캡처한다.

## 수업 뒤 게시

현재 폴더가 `web-week07`인지 확인하고 변경 파일을 검토한 뒤 올린다. CDN 파일은 내려받아 추가하지 않는다.

```bash
git status
git add .
git commit -m "Apply W3.CSS to the guestbook"
git push -u origin main
```

GitHub 저장소의 **Settings › Pages**에서 **Deploy from a branch**, `main`, `/(root)`를 선택한다. 게시 후 `https://student01.github.io/web-week07/guestbook.html`을 열어 글을 남겨 본다. 수업 중 캡처를 먼저 제출했다면 수업 뒤 공개 주소도 확인한다. 이미 저장소나 Pages가 준비되어 있으면 기존 설정을 사용한다.

## 문제 해결

| 증상 | 확인할 곳 |
|---|---|
| 버튼 색상과 입력 모양이 적용되지 않음 | CDN `<link>` 주소, Network 응답, 인터넷 연결 |
| 색상이 바뀌지 않음 | 저장 여부, 수정한 파일의 경로, `w3-*` 철자 |
| 남기기를 눌러도 결과가 없음 | 이메일 형식 검사 안내, `script src`, Console 오류, JS가 찾는 `id` |
| ex04의 기존 스타일이 없음 | `examples/day2/web-week07/styles.css`와 상대 경로 |
| 좁은 화면에서 메뉴가 한 줄로 남음 | 각 메뉴 항목의 `w3-mobile`, viewport 메타 태그 |
| 새로고침하면 목록이 사라짐 | 이번 주는 화면에만 추가한다. 저장은 11주차 범위 |
