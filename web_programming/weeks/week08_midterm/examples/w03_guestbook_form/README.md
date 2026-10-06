[8주 문제 은행](../README.md) · [15주 문제 은행](../../../week15_final_exam/examples/README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

# w03_guestbook_form — 신청 폼 페이지

출처: [3주차 실습 제출](../../../week03_semantic_html/lab.md#제출--캡처-한-장) · 권장 10분 · 중간 A(HTML) · 기말 A(화면(HTML·CSS·README))

3주차에 만든 방명록 form 을 다른 값으로 다시 만든다. HTML 만 쓴다. `join.html` 을 열면 번호 목록과 이름표 붙은 입력 칸 세 개, 제출 버튼이 보이고, 이름표를 누르면 그 칸에 커서가 들어가야 한다.

## 시작 파일

| 파일 | 지금 상태 |
|---|---|
| `join.html` | 머리말(`h1`·메뉴 세 링크)·본문·꼬리말이 있다. 본문 `main` 에는 `h2` 와 `<!-- 여기에 -->` 주석뿐이다 |
| `index.html` · `about.html` | 메뉴로 오가는 짧은 완성 페이지다. 고치지 않는다 |

CSS·JavaScript 파일은 없다. 꾸미지 않은 화면이 정상이다.

## 할 일

`join.html` 의 `<!-- 여기에 -->` 자리에 차례로 넣는다. 주석은 지워도 된다.

1. `h3` 제목(`신청 순서`)을 넣는다.
2. 그 아래에 번호 목록을 만들고, 다음 문장을 이 순서로 한 줄씩 넣는다.
   - `닉네임을 적는다.`
   - `연락 메일을 적는다.`
   - `하고 싶은 말을 적는다.`
   - `신청하기 버튼을 누른다.`
3. 번호 목록 아래에 `form` 하나를 만들고, 그 안에 입력 칸 세 개를 이 순서로 넣는다. 칸마다 이름표를 붙이고, 이름표를 누르면 그 칸에 커서가 들어가게 한다.
   - 이름표 `닉네임` — 한 줄 입력 칸, id `nickname`
   - 이름표 `연락 메일` — 이메일용 입력 칸, id `contact`
   - 이름표 `하고 싶은 말` — 여러 줄 입력 칸(3줄 높이), id `memo`
4. 같은 `form` 안, 세 칸 아래에 제출 버튼 **신청하기** 를 넣는다.
5. `form` 에 `action`·`method` 를, 칸에 `name`·`required` 를 쓰지 않는다. `style` 속성도 쓰지 않는다. 보낼 곳이 없으므로 버튼을 누르면 같은 페이지가 다시 열리는 것이 맞다.

## 확인할 것

- [ ] `join.html` 에 `신청 순서` 제목이 보이고, 그 아래 번호 목록이 1번부터 위 문장 그대로 차례로 보인다.
- [ ] 이름표(`닉네임`·`연락 메일`·`하고 싶은 말`)가 붙은 입력 칸이 이 순서로 보이고, 그 아래 **신청하기** 버튼이 있다.
- [ ] 이름표 글자를 하나씩 누르면 그 이름표의 칸에 커서가 들어간다.
- [ ] F12 › Console 에 `document.querySelector('#nickname').type` 을 치면 `'text'`, `document.querySelector('#contact').type` 은 `'email'`, `document.querySelector('#memo').rows` 는 줄 수(`3`)가 나온다.
- [ ] Console 에 `document.querySelectorAll('form').length` 를 치면 `1`, `document.querySelector('form').elements.length` 는 `4` 가 나온다. 세 칸과 버튼이 한 `form` 안에 있다는 뜻이다.
- [ ] 칸을 모두 비운 채 **신청하기** 를 누르면 화면은 그대로이고, 주소창의 `join.html` 뒤에 `?` 가 붙는다. Console 에 빨간 줄이 없다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 고칠 파일 | `join.html` |
| 페이지 이름(h1·메뉴) | `가입 신청` |
| 본문 h2 | `사진 동아리 가입` |
| h3 제목 | `신청 순서` |
| 번호 목록 문장(차례로) | `닉네임을 적는다.` · `연락 메일을 적는다.` · `하고 싶은 말을 적는다.` · `신청하기 버튼을 누른다.` |
| 칸 1 이름표 | `닉네임` |
| 칸 1 id(한 줄 입력 칸) | `nickname` |
| 칸 2 이름표 | `연락 메일` |
| 칸 2 id(이메일용 입력 칸) | `contact` |
| 칸 3 이름표 | `하고 싶은 말` |
| 칸 3 id(여러 줄 입력 칸) | `memo` |
| 칸 3 줄 수(rows) | `3` |
| 버튼 글자 | `신청하기` |

시험에서는 같은 문제를 이 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다.

## 받기와 올리기

- 이번 주 저장소(8주는 `web-week08`, 15주는 `web-week15`) 맨 위에 [server.mjs](../../../../tools/static-server/server.mjs) 가 없으면 먼저 **Raw** 로 받아 둔다.
- 저장소 안에 `w03_guestbook_form/` 폴더를 만든다. 교재의 이 문제 폴더에 있는 시작 파일을 하나씩 열어 **Raw** 를 누르고 Ctrl+S(macOS ⌘+S)로 같은 이름으로 저장한다. 그림도 Raw 를 누르면 그림만 보이는 화면이 열리고, 거기서 같은 방법으로 저장한다. 하위 폴더(그림·데이터)는 GitHub 에서 그 폴더를 눌러 들어가 받고, 내 폴더에도 같은 이름으로 만든다. 저장한 이름 끝에 `.txt` 가 붙었으면 지운다. 이 `README.md`(지금 읽는 문제 문장)는 받지 않는다.
- 저장소 맨 위에서 `node server.mjs` 로 열면 주소는 `http://localhost:8000/w03_guestbook_form/join.html` 이다. Node 가 없는 PC 는 두 번 눌러 연다.
- `node server.mjs` 로 연 주소나 공개 주소에서는 `favicon.ico` 404 한 줄이 Console·Network 에 보여도 괜찮다(빨간 줄로 세지 않는다). 공개 주소에서 새로고침하면 Status 가 `304` 로 보일 수 있다. 이미 받은 파일을 다시 쓴다는 뜻이다.
- 올린 뒤 공개 주소는 `https://student01.github.io/web-week08/w03_guestbook_form/join.html`(15주에 풀었다면 `web-week15`)이다.
- 해답은 공개하지 않는다. 위 "확인할 것"이 모두 맞으면 된 것이다.
