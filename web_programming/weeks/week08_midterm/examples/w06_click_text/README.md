[8주 문제 은행](../README.md) · [15주 문제 은행](../../../week15_final_exam/examples/README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

# w06_click_text — 버튼을 누르면 글자가 바뀌고 횟수가 늘어난다

출처: [6주차 실습 제출](../../../week06_dom_crud/lab.md#제출--캡처-한-장) · 권장 10분 · 중간 C(JavaScript·DOM) · 기말 B(DOM)

6주차 실습(버튼으로 문구 바꾸기와 클릭 횟수)을 다른 값으로 다시 만든다. 버튼을 누르면 문단의 글자가 바뀌고, 누른 횟수가 다른 문단에 늘어난다.

## 시작 파일

| 파일 | 지금 상태 |
|---|---|
| `index.html` | 제목, 글자 문단(`id="message"`), 버튼(`id="change-button"`), 횟수 문단(`id="count"`)이 있고 `app.js` 를 `defer` 로 연결했다. 고치지 않는다 |
| `app.js` | 주석 한 줄뿐이다 |

## 할 일

`app.js` 에 차례로 쓴다.

1. `document.querySelector` 로 글자 문단(`#message`), 버튼(`#change-button`), 횟수 문단(`#count`)을 찾아 `const` 에 담는다.
2. 횟수를 담을 변수 `count` 를 `let` 으로 만들고 `0` 으로 시작한다.
3. 버튼에 `addEventListener('click', …)` 을 건다. 누를 때마다
   - `count` 를 1 올리고,
   - 글자 문단의 글자를 `버튼을 눌렀습니다!` 로 바꾸고,
   - 횟수 문단의 글자를 `클릭 N회` 꼴(N 은 지금 횟수)로 바꾼다.
4. 저장 → 새로고침 → 버튼을 3번 눌러 본다.

## 확인할 것

- [ ] 페이지를 열면 글자 문단은 `아직 누르지 않았습니다.`, 횟수 문단은 `클릭 0회` 다.
- [ ] 버튼을 3번 누르면 글자 문단이 `버튼을 눌렀습니다!`, 횟수 문단이 `클릭 3회` 다. 한 번 더 누르면 `클릭 4회` 가 되고 글자 문단은 그대로다.
- [ ] 새로고침하면 처음 글자로 돌아간다(저장하지 않는 것이 맞다).
- [ ] F12 › Console 에 빨간 줄이 없다. 특히 `Cannot read properties of null` 이 없다.

## 힌트

- 요소를 찾는 한 줄: `const message = document.querySelector('#message');` — `#` 뒤는 HTML 의 `id` 와 글자까지 같아야 한다.
- 글자를 바꾸는 한 줄: `message.textContent = '버튼을 눌렀습니다!';`. 숫자와 글자를 이을 때는 `'클릭 ' + count + '회'` 처럼 `+` 로 잇는다.
- `count` 를 `const` 로 만들면 `count = count + 1` 에서 빨간 줄이 난다. 값이 바뀌는 변수는 `let` 이다.
- `Cannot read properties of null` 은 `querySelector` 가 아무것도 못 찾았다는 뜻이다. `#` 과 철자를 본다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 페이지 제목 h1 | `버튼 연습` |
| 글자 문단 id | `message` |
| 처음 글자 | `아직 누르지 않았습니다.` |
| 누른 뒤 글자 | `버튼을 눌렀습니다!` |
| 버튼 id | `change-button` |
| 버튼 글자 | `글자 바꾸기` |
| 횟수 문단 id | `count` |
| 횟수 문장 꼴(N 은 횟수) | `클릭 N회` |
| 확인 때 누르는 수 | `3` |
| 누른 뒤 횟수 문장 | `클릭 3회` |

시험에서는 같은 문제를 이 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다.

## 받기와 올리기

- 이번 주 저장소(8주는 `web-week08`, 15주는 `web-week15`) 맨 위에 [server.mjs](../../../../tools/static-server/server.mjs) 가 없으면 먼저 **Raw** 로 받아 둔다.
- 저장소 안에 `w06_click_text/` 폴더를 만든다. 교재의 이 문제 폴더에 있는 시작 파일을 하나씩 열어 **Raw** 를 누르고 Ctrl+S(macOS ⌘+S)로 같은 이름으로 저장한다. 그림도 Raw 를 누르면 그림만 보이는 화면이 열리고, 거기서 같은 방법으로 저장한다. 하위 폴더(그림·데이터)는 GitHub 에서 그 폴더를 눌러 들어가 받고, 내 폴더에도 같은 이름으로 만든다. 저장한 이름 끝에 `.txt` 가 붙었으면 지운다. 이 `README.md`(지금 읽는 문제 문장)는 받지 않는다.
- 저장소 맨 위에서 `node server.mjs` 로 열면 주소는 `http://localhost:8000/w06_click_text/` 이다. Node 가 없는 PC 는 두 번 눌러 연다.
- `node server.mjs` 로 연 주소나 공개 주소에서는 `favicon.ico` 404 한 줄이 Console·Network 에 보여도 괜찮다(빨간 줄로 세지 않는다). 공개 주소에서 새로고침하면 Status 가 `304` 로 보일 수 있다. 이미 받은 파일을 다시 쓴다는 뜻이다.
- 올린 뒤 공개 주소는 `https://student01.github.io/web-week08/w06_click_text/`(15주에 풀었다면 `web-week15`)이다.
- 해답은 공개하지 않는다. 위 "확인할 것"이 모두 맞으면 된 것이다.
