[8주 문제 은행](../README.md) · [15주 문제 은행](../../../week15_final_exam/examples/README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

# w05_greeting_card — 인사 카드

출처: [5주차 실습 제출](../../../week05_javascript_data/lab.md#제출--캡처-한-장) · 권장 12분 · 중간 C(JavaScript·DOM) · 기말 B(DOM)

5주차에 조립한 인사 카드를 다른 값으로 다시 만든다. 페이지를 열면 맨 위 카드에 이름과 시각에 맞는 인사말이 나오고, Console 에 시각과 같은 문장이 찍혀야 한다.

## 시작 파일

| 파일 | 지금 상태 |
|---|---|
| `index.html` | 머리말·본문·꼬리말이 있다. `app.js` 를 연결하는 줄과 인사 카드는 없다 |
| `styles.css` | 완성본이다(`.card` 규칙이 있다). 고치지 않는다 |
| `app.js` | 주석 한 줄뿐이다 |

## 할 일

1. `index.html` 의 `<head>` 에서 `styles.css` 연결 줄 아래에 `app.js` 를 연결한다. HTML 을 끝까지 읽은 뒤 실행되게 한다.
2. `<main>` 의 첫 줄에 `<p class="card" id="welcome">인사말을 준비 중입니다.</p>` 를 넣는다.
3. `app.js` 에 차례로 쓴다. 다시 담지 않는 값은 `const` 로 둔다.
   - 이름 `name` 에 `'guest07'`, 시각 `hour` 에 `15` 를 담는다. 실제 앱은 `new Date().getHours()` 지만 채점을 위해 시각을 정해 둔다.
   - 함수 `greet(name)` 은 `` `반가워요, ${name}님.` `` 문장을 돌려준다.
   - 함수 `hello(hour)` 는 `hour` 가 18 이상이면 `'편안한 저녁 되세요.'`, 12 이상이면 `'즐거운 오후예요.'`, 그 밖에는 `'상쾌한 아침이에요.'` 를 돌려준다.
   - 두 함수를 불러 만든 두 문장을 빈칸 하나로 이어 `message` 에 담는다.
   - Console 에 `hour` 와 `message` 를 한 줄에 하나씩 차례로 찍는다.
   - `#welcome` 카드의 글자를 `message` 로 바꾼다.

## 확인할 것

- [ ] 페이지를 열면 카드에 `반가워요, guest07님. 즐거운 오후예요.` 가 보인다. `인사말을 준비 중입니다.` 는 남아 있지 않다.
- [ ] F12 › Elements 에서 `app.js` 를 연결한 줄이 보인다. 카드 `<p>` 의 class 는 `card`, id 는 `welcome` 이고, 아래 소개 카드와 같은 흰 상자로 보인다.
- [ ] F12 › Console 에 `15` 만 있는 줄과 `반가워요, guest07님. 즐거운 오후예요.` 만 있는 줄이 이 순서로 찍히고 빨간 줄이 없다.
- [ ] Console 에 쳐 보면 `hello(11)` 의 결과는 `'상쾌한 아침이에요.'`, `hello(12)`·`hello(17)` 의 결과는 `'즐거운 오후예요.'`, `hello(18)` 의 결과는 `'편안한 저녁 되세요.'` 이다.
- [ ] Console 에 쳐 보면 `greet('student99')` 의 결과는 `'반가워요, student99님.'` 이다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 페이지 제목 h1 | `인사 카드` |
| 이름 name | `guest07` |
| 시각 hour | `15` |
| 카드 id | `welcome` |
| 카드의 처음 글자 | `인사말을 준비 중입니다.` |
| greet 가 돌려줄 문장 | `반가워요, ${name}님.` |
| 큰 기준(이상) | `18` |
| 작은 기준(이상) | `12` |
| 큰 기준 이상 | `편안한 저녁 되세요.` |
| 작은 기준 이상 | `즐거운 오후예요.` |
| 그 밖 | `상쾌한 아침이에요.` |
| 카드에 나올 문장 | `반가워요, guest07님. 즐거운 오후예요.` |

시험에서는 같은 문제를 이 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다.

## 받기와 올리기

- 이번 주 저장소(8주는 `web-week08`, 15주는 `web-week15`) 맨 위에 [server.mjs](../../../../tools/static-server/server.mjs) 가 없으면 먼저 **Raw** 로 받아 둔다.
- 저장소 안에 `w05_greeting_card/` 폴더를 만든다. 교재의 이 문제 폴더에 있는 시작 파일을 하나씩 열어 **Raw** 를 누르고 Ctrl+S(macOS ⌘+S)로 같은 이름으로 저장한다. 그림도 Raw 를 누르면 그림만 보이는 화면이 열리고, 거기서 같은 방법으로 저장한다. 하위 폴더(그림·데이터)는 GitHub 에서 그 폴더를 눌러 들어가 받고, 내 폴더에도 같은 이름으로 만든다. 저장한 이름 끝에 `.txt` 가 붙었으면 지운다. 이 `README.md`(지금 읽는 문제 문장)는 받지 않는다.
- 저장소 맨 위에서 `node server.mjs` 로 열면 주소는 `http://localhost:8000/w05_greeting_card/` 이다. Node 가 없는 PC 는 두 번 눌러 연다.
- `node server.mjs` 로 연 주소나 공개 주소에서는 `favicon.ico` 404 한 줄이 Console·Network 에 보여도 괜찮다(빨간 줄로 세지 않는다). 공개 주소에서 새로고침하면 Status 가 `304` 로 보일 수 있다. 이미 받은 파일을 다시 쓴다는 뜻이다.
- 올린 뒤 공개 주소는 `https://student01.github.io/web-week08/w05_greeting_card/`(15주에 풀었다면 `web-week15`)이다.
- 해답은 공개하지 않는다. 위 "확인할 것"이 모두 맞으면 된 것이다.
