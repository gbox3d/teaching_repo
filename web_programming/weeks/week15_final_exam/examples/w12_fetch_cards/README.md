[15주 문제 은행](../README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam)

# w12_fetch_cards — JSON 카드 불러오기

출처: [12주차 실습 제출](../../../week12_persistent_crud/lab.md#제출--캡처-한-장) · 권장 9분 · 기말 E(불러오기(fetch))

12주차에 만든 "JSON 파일을 읽어 그리는 카드"를 다른 값으로 다시 만든다. 페이지를 열면 `data/html-docs.json` 의 항목이 카드로 나오고, 파일을 읽지 못하면 카드 대신 안내 문장이 보여야 한다. 카드를 그리는 함수는 이미 있다.

## 시작 파일

| 파일 | 지금 상태 |
|---|---|
| `index.html` | 제목, 안내 자리 `<p id="notice">`(처음 글자 `자료를 불러오는 중입니다.`), 빈 카드 상자 `<div id="doc-list">` 가 있다. `app.js` 는 `defer` 로 연결돼 있다. 고치지 않는다 |
| `styles.css` | 완성본이다(`.card` 규칙이 있다). 고치지 않는다 |
| `data/html-docs.json` | 항목 3개가 들어 있다. 이름표는 `title`(제목)·`description`(설명)·`link`(링크)다. 고치지 않는다 |
| `app.js` | 안내 자리(`#notice`)를 담은 변수 `notice` 와 카드 상자(`#doc-list`)를 담은 변수 `cardBox` 를 만드는 두 줄, 카드를 그리는 `showCards(items)`(완성), 속이 빈 `async function loadCards()`, 마지막 줄 `loadCards();` 가 있다 |

## 할 일

`app.js` 의 `loadCards()` 안만 쓴다. `showCards` 와 다른 파일은 고치지 않는다.

1. `data/html-docs.json` 파일을 `fetch` 로 요청하고 응답을 기다린다. 경로는 `index.html` 이 있는 폴더에서 본 상대 경로로 쓴다.
2. 응답이 정상이 아니면(`response.ok` 가 `false`) 안내 자리에 `자료를 불러오지 못했습니다.` 를 쓰고 함수를 끝낸다.
3. 응답을 JSON 으로 바꿔 배열을 받는다. 안내 자리를 비운 뒤 그 배열로 `showCards` 를 부른다.
4. 1~3 을 `try / catch` 로 감싼다. 요청이나 변환 중에 오류가 나면 `catch` 에서 안내 자리에 같은 문장 `자료를 불러오지 못했습니다.` 를 쓴다.

## 확인할 것

`node server.mjs` 로 연 주소나 공개 주소에서 확인한다.

- [ ] 카드 3장이 보이고 첫 카드 제목이 `HTML 텍스트 기초` 이다. 안내 자리의 `자료를 불러오는 중입니다.` 는 사라지고 비어 있다.
- [ ] F12 › Network 에 `html-docs.json` 이 Status 200 으로 보인다. 요청 주소는 이 문제 폴더 안의 `data/html-docs.json` 이다.
- [ ] F12 › Console 에 빨간 줄이 없다.
- [ ] `data/html-docs.json` 의 이름을 잠깐 다른 이름으로 바꾸고 새로고침하면 카드 없이 `자료를 불러오지 못했습니다.` 가 보인다. Network 에서 그 요청은 404 이고, Console 에는 그 404 줄(과 `favicon.ico` 404 줄) 말고 빨간 줄이 없다. `Uncaught` 로 시작하는 줄도 없다. 확인한 뒤 이름을 되돌린다.
- [ ] 서버 없이 `index.html` 을 두 번 눌러 열면(`file://` 에서는 요청이 막힌다) `자료를 불러오지 못했습니다.` 가 보인다. Console 에 CORS 안내 같은 빨간 줄은 남지만 `Uncaught (in promise) TypeError: Failed to fetch` 줄은 없다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 데이터 파일 | `data/html-docs.json` |
| 항목 이름표(제목·설명·링크 차례) | `title` · `description` · `link` |
| 항목 수 | `3` |
| 첫 항목 제목 | `HTML 텍스트 기초` |
| 카드 상자 id | `doc-list` |
| 안내 자리 id | `notice` |
| 안내 자리의 처음 글자 | `자료를 불러오는 중입니다.` |
| 불러오지 못했을 때 안내 문장 | `자료를 불러오지 못했습니다.` |
| 페이지 제목(h1) | `HTML 공부 자료` |
| 카드 링크 글자 | `문서 열기` |

시험에서는 같은 문제를 이 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다.

## 받기와 올리기

- 이번 주 저장소(`web-week15`) 맨 위에 [server.mjs](../../../../tools/static-server/server.mjs) 가 없으면 먼저 **Raw** 로 받아 둔다.
- 저장소 안에 `w12_fetch_cards/` 폴더를 만든다. 교재의 이 문제 폴더에 있는 시작 파일을 하나씩 열어 **Raw** 를 누르고 Ctrl+S(macOS ⌘+S)로 같은 이름으로 저장한다. 그림도 Raw 를 누르면 그림만 보이는 화면이 열리고, 거기서 같은 방법으로 저장한다. 하위 폴더(그림·데이터)는 GitHub 에서 그 폴더를 눌러 들어가 받고, 내 폴더에도 같은 이름으로 만든다. 저장한 이름 끝에 `.txt` 가 붙었으면 지운다. 이 `README.md`(지금 읽는 문제 문장)는 받지 않는다.
- 저장소 맨 위에서 `node server.mjs` 로 열면 주소는 `http://localhost:8000/w12_fetch_cards/` 이다. Node 가 없는 PC 는 두 번 눌러 연다.
- 이 문제는 `fetch` 로 파일을 받는다. 두 번 눌러 연 `file://` 화면에서는 요청이 막혀 받은 내용이 나오지 않으므로, `node server.mjs` 로 연 주소(`http://localhost:8000/w12_fetch_cards/`)나 공개 주소에서 확인한다.
- `node server.mjs` 로 연 주소나 공개 주소에서는 `favicon.ico` 404 한 줄이 Console·Network 에 보여도 괜찮다(빨간 줄로 세지 않는다). 공개 주소에서 새로고침하면 Status 가 `304` 로 보일 수 있다. 이미 받은 파일을 다시 쓴다는 뜻이다.
- 올린 뒤 공개 주소는 `https://student01.github.io/web-week15/w12_fetch_cards/`이다.
- 해답은 공개하지 않는다. 위 "확인할 것"이 모두 맞으면 된 것이다.
