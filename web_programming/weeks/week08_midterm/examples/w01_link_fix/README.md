[8주 문제 은행](../README.md) · [15주 문제 은행](../../../week15_final_exam/examples/README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

# w01_link_fix — 세 파일 연결 고치기

출처: [1주차 실습 제출](../../../week01_web_git/lab.md#제출--캡처-두-장) · 권장 8분 · 중간 A(HTML) · 기말 A(화면(HTML·CSS·README))

1주차에 만든 내 소개 페이지에서 세 파일의 연결이 끊어졌다. `index.html` 이 CSS 파일과 JS 파일을 틀린 이름으로 부른다. 두 이름을 고쳐 카드 모양과 버튼 동작을 되살리고 제목을 바꾼다.

## 시작 파일

| 파일 | 지금 상태 |
|---|---|
| `index.html` | 카드·버튼·상태 글자가 있다. `<link>` 의 `href` 와 `<script>` 의 `src` 가 폴더에 없는 파일 이름이고, `<h1>` 은 안내 문장이다 |
| `styles.css` | 완성본이다(배경색·카드·버튼 모양). 고치지 않는다 |
| `app.js` | 완성본이다(버튼을 누를 때마다 횟수를 올리고, Console 에 준비 문구를 남긴다). 고치지 않는다 |

## 할 일

1. `index.html` 을 열고 F12 › Network 를 연 채 새로고침한다. Status 가 `404` 인 두 줄이 `index.html` 이 틀리게 적은 이름이다. 두 번 눌러 연 `file://` 화면이면 Console 의 빨간 줄 두 개로 찾는다.
2. `index.html` 에서 `<link>` 의 `href` 를 `styles.css` 로, `<script>` 의 `src` 를 `app.js` 로 고친다. 파일 이름은 바꾸지 않고, 두 줄의 다른 속성은 그대로 둔다.
3. `<h1>` 의 글자를 `안녕하세요, guest07입니다` 로 바꾼다.
4. 저장하고 새로고침한다.

## 확인할 것

- [ ] F12 › Network 를 연 채 새로고침하면 `styles.css`·`app.js` 두 줄의 Status 가 `200` 이다. Status 가 `404` 인 줄은 없다.
- [ ] 배경이 `#eef2ff` 색이다. F12 › Elements 에서 `<body>` 를 고르면 Styles 에 `background: #eef2ff` 줄이 있고, 그 규칙 옆에 `styles.css` 파일 이름이 보인다.
- [ ] 제목(`<h1>`)에 `안녕하세요, guest07입니다` 가 보인다.
- [ ] 버튼 아래 글자가 처음에는 `클릭 횟수: 0` 이고, **눌러 보기** 를 3번 누른 뒤에는 `클릭 횟수: 3` 이다.
- [ ] F12 › Console 에 `w01 ready` 가 찍혀 있고 빨간 줄이 없다.

Status 번호는 서버가 보내는 번호라 `node server.mjs` 로 연 주소나 공개 주소에서만 보인다. 공개 주소는 새 시크릿 창으로 열어 본다. `favicon.ico` 는 브라우저가 탭 아이콘을 찾으려고 스스로 보낸 요청이라 404 로 보여도 괜찮다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 제목 h1 | `안녕하세요, guest07입니다` |
| CSS 파일 이름 | `styles.css` |
| JS 파일 이름 | `app.js` |
| index.html 에 틀리게 적힌 CSS 이름 | `style.css` |
| index.html 에 틀리게 적힌 JS 이름 | `apps.js` |
| 배경색(CSS 파일 안) | `#eef2ff` |
| 버튼 글자 | `눌러 보기` |
| 상태 글자 앞부분 | `클릭 횟수` |
| 확인 때 누를 횟수 | `3` |
| 누른 뒤 상태 글자 | `클릭 횟수: 3` |
| Console 준비 문구 | `w01 ready` |

시험에서는 같은 문제를 이 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다.

## 받기와 올리기

- 이번 주 저장소(8주는 `web-week08`, 15주는 `web-week15`) 맨 위에 [server.mjs](../../../../tools/static-server/server.mjs) 가 없으면 먼저 **Raw** 로 받아 둔다.
- 저장소 안에 `w01_link_fix/` 폴더를 만든다. 교재의 이 문제 폴더에 있는 시작 파일을 하나씩 열어 **Raw** 를 누르고 Ctrl+S(macOS ⌘+S)로 같은 이름으로 저장한다. 그림도 Raw 를 누르면 그림만 보이는 화면이 열리고, 거기서 같은 방법으로 저장한다. 하위 폴더(그림·데이터)는 GitHub 에서 그 폴더를 눌러 들어가 받고, 내 폴더에도 같은 이름으로 만든다. 저장한 이름 끝에 `.txt` 가 붙었으면 지운다. 이 `README.md`(지금 읽는 문제 문장)는 받지 않는다.
- 저장소 맨 위에서 `node server.mjs` 로 열면 주소는 `http://localhost:8000/w01_link_fix/` 이다. Node 가 없는 PC 는 두 번 눌러 연다.
- `node server.mjs` 로 연 주소나 공개 주소에서는 `favicon.ico` 404 한 줄이 Console·Network 에 보여도 괜찮다(빨간 줄로 세지 않는다). 공개 주소에서 새로고침하면 Status 가 `304` 로 보일 수 있다. 이미 받은 파일을 다시 쓴다는 뜻이다.
- 올린 뒤 공개 주소는 `https://student01.github.io/web-week08/w01_link_fix/`(15주에 풀었다면 `web-week15`)이다.
- 해답은 공개하지 않는다. 위 "확인할 것"이 모두 맞으면 된 것이다.
