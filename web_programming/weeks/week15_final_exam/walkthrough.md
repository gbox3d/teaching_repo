# 15주차 따라하기 — 문제 은행으로 연습하고 기말 실기 보기

이번 주는 새로 배우는 것이 없다. 1~14주 실습 제출을 한 문제씩으로 정리한 [문제 은행](examples/README.md)을 풀어 본다.
1일차는 연습이다. 문제 폴더를 받아 서버로 열고, 할 일을 하고, 문제 문장의 **"확인할 것"** 으로 스스로 맞춰 본다. 끝에 이번 주 새 저장소 `web-week15` 에 올린다.
2일차는 기말 실기 60분이다. 강의자가 나눠 주는 `exam` 폴더를 같은 저장소에 넣어 풀고 올린다.
이 문서에는 해답 코드가 없다. 예로 드는 문제는 공개 문제 [w12_fetch_cards](examples/w12_fetch_cards/)이고, 맞았는지는 "확인할 것"으로 본다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

## 1일차

### 1. web-week15 폴더 만들고 server.mjs 넣기

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-week15`를 만들고 VS Code **File › Open Folder**로 연다.
이번 주는 지난주 완성본을 넣지 않는다. 이 폴더에는 서버 파일 하나와 문제 폴더만 둔다.

교재 저장소의 [server.mjs](../../tools/static-server/server.mjs)를 연다 → 오른쪽 위 **Raw** → **Ctrl+S**(macOS는 ⌘+S)로 `web-week15` 맨 위에 `server.mjs` 이름으로 저장한다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week15/
  server.mjs
```

- 저장한 이름이 `server.mjs.txt`처럼 `.txt`로 끝나면 이름을 고친다. 브라우저가 붙인 것이다. 이름은 VS Code 탐색기에서 확인한다(Windows 파일 탐색기는 기본 설정에서 확장자를 숨긴다).
- 5주차에 쓴 서버다. 5주차 폴더(`web-week05`)에 있으면 복사해 와도 된다.

### 2. 은행 목록에서 세 문제 고르기

[문제 은행 목록](examples/README.md)을 연다. 1~14주 실습 제출 13문제가 영역 A~E로 나뉘어 있다.
1~7주 문제의 링크는 [8주차 문제 은행](../week08_midterm/examples/README.md)의 폴더로 간다. 같은 문제다.

오늘은 세 문제를 푼다.

1. 영역이 서로 다르게 고른다. 시험은 영역마다 한 문제씩, 다섯 문제가 나온다.
2. 자신 없는 영역부터 고른다.
3. 9~14주 문제(`w09`~`w14`)를 하나 이상 넣는다. 기말에 처음 나오는 문제다.

**예상 결과** — 고른 세 문제의 id를 적어 둔다. 이 문서는 E 불러오기(fetch)의 `w12_fetch_cards`를 예로 든다. 다른 문제도 3~6단계의 순서가 같다.

- 문제 id는 폴더 이름이다. 앞의 숫자가 출처 주다(`w12` = 12주차 실습 제출).
- 표의 권장 분은 시험에서 그 문제에 쓸 시간이다. 오늘은 받기와 확인까지 넣어 한 문제에 15분이다.

### 3. 문제 폴더 받기 — w12_fetch_cards

교재 저장소의 [examples/w12_fetch_cards](examples/w12_fetch_cards/) 폴더를 연다. 위에 시작 파일 목록이, 그 아래에 문제 문장(`README.md`)이 보인다.

`web-week15` 안에 `w12_fetch_cards` 폴더를 만들고, 그 안에 `data` 폴더를 만든다. 시작 파일을 하나씩 눌러 **Raw** → **Ctrl+S**(macOS는 ⌘+S)로 같은 이름, 같은 자리에 저장한다.

| 파일 | 저장할 곳 | 지금 상태(문제 문장의 시작 파일 표) |
|---|---|---|
| [index.html](examples/w12_fetch_cards/index.html) | `web-week15/w12_fetch_cards/` | 제목, 안내 자리, 빈 카드 상자가 있다. 고치지 않는다 |
| [styles.css](examples/w12_fetch_cards/styles.css) | 같은 곳 | 완성본이다. 고치지 않는다 |
| [app.js](examples/w12_fetch_cards/app.js) | 같은 곳 | 카드를 그리는 함수는 있고 `loadCards()`의 속이 비어 있다. **여기만 쓴다** |
| [data/html-docs.json](examples/w12_fetch_cards/data/html-docs.json) | `web-week15/w12_fetch_cards/data/` | 항목 3개가 들어 있다. 고치지 않는다 |

문제 문장인 `README.md`는 받지 않는다. 교재 화면에서 읽는다.

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week15/
  w12_fetch_cards/
    data/
      html-docs.json
    app.js
    index.html
    styles.css
  server.mjs
```

- 문제마다 폴더를 따로 만든다. 맨 위에 바로 저장하면 다음 문제의 `index.html`·`app.js`가 덮어쓴다.
- 폴더·파일 이름을 한 글자도 바꾸지 않는다. `index.html`과 문제 문장이 이 이름으로 부른다.
- 그림이 있는 문제(`w04_responsive_css`·`w09_readme_links`·`w14_readme_images`)는 그림도 같은 방법으로 받는다. 그림 파일에서 **Raw**를 누르면 그림만 열린다. 그 화면에서 **Ctrl+S**로 같은 하위 폴더에 저장한다.

### 4. 서버로 열고 시작 상태 보기

현재 폴더: `web-week15`

```bash
node server.mjs
```

**예상 결과** — 터미널에 두 줄이 찍히고 서버가 떠 있다. 폴더 줄은 PC마다 다르다.

```text
폴더: C:\Users\student\web-week15
주소: http://localhost:8000/   (멈추기: Ctrl+C)
```

Chrome 주소창에 `http://localhost:8000/`을 친다. 맨 위에는 `index.html`이 없어서 파일 목록(`w12_fetch_cards/`·`server.mjs`)이 보인다.
`w12_fetch_cards/`를 누른다. 주소가 `http://localhost:8000/w12_fetch_cards/`가 된다. **F12**를 눌러 **Console**과 **Network**를 연다.

**예상 결과** — 받은 그대로의 화면이다.

```text
화면     HTML 공부 자료 / 읽을 자료 / 자료를 불러오는 중입니다.   ← 카드가 없다
Console  빨간 줄 없음
터미널   200 GET /
         200 GET /w12_fetch_cards/
         200 GET /w12_fetch_cards/styles.css
         200 GET /w12_fetch_cards/app.js
         404 GET /favicon.ico
```

- 카드가 없고 `자료를 불러오는 중입니다.`가 그대로다. `loadCards()`의 속이 비어서 데이터 파일을 요청하지 않는다. 터미널에도 `html-docs.json` 줄이 없다.
- 받은 그대로는 "확인할 것" 가운데 맞지 않는 것이 있다. 그것을 맞추는 것이 이 문제다.
- 여기서 Console에 빨간 줄이 이미 있으면 할 일을 하기 전에 받은 파일 이름과 폴더부터 본다.
- 가운데 줄의 순서는 열 때마다 바뀔 수 있다. 줄 수만 본다. `favicon.ico`는 브라우저가 탭 아이콘을 찾으려고 스스로 보낸 요청이라 404여도 괜찮다.

### 5. 문제 문장 읽고 고치기

교재 화면에서 [w12_fetch_cards 문제 문장](examples/w12_fetch_cards/README.md)을 연다. 절은 다섯이고, 모든 문제가 같은 차례다.

| 절 | 읽는 법 |
|---|---|
| 시작 파일 | 고칠 파일과 고치지 않는 파일을 가른다. 이 문제는 `app.js`의 `loadCards()` 안만 쓴다 |
| 할 일 | 적힌 차례대로 한다. 하나를 쓰면 저장 → 새로고침 → Console을 본다 |
| 확인할 것 | 맞았는지 보는 기준이다. 6단계에서 위에서부터 하나씩 본다 |
| 이 문제의 값 | 파일 이름·문장·id처럼 시험에서 바뀌는 값이다. 할 일과 확인할 것에 이 값이 들어 있다 |
| 받기와 올리기 | 3단계와 8단계에서 하는 것이다 |

할 일 1~4는 12주차 실습에서 한 것과 같은 일이다. 쓸 말이 떠오르지 않으면 문제 문장 맨 위 "출처"의 [12주차 실습](../week12_persistent_crud/lab.md#제출--캡처-한-장)을 연다. 시험에서도 교재 사이트는 볼 수 있다.

**예상 결과** — 할 일 1~4를 쓰고 새로고침하면 카드가 나온다. 이 문서에는 해답 코드를 싣지 않는다. 맞았는지는 6단계의 "확인할 것"으로 본다.

- 할 일 1의 경로는 `index.html`이 있는 폴더에서 본 **상대 경로**다. 주소창의 `http://localhost:8000/w12_fetch_cards/` 뒤에 그대로 붙는다고 생각한다.
- 안내 문장은 "이 문제의 값" 표에서 복사해 붙여 넣는다. 한 글자만 달라도 확인할 것이 맞지 않는다.
- `var`·`getElementById`·`innerText`처럼 다른 방법으로 써도 확인 결과가 같으면 정답이다.

### 6. 확인할 것 맞추기 — 서버로 여는 이유

[문제 문장의 확인할 것](examples/w12_fetch_cards/README.md#확인할-것)을 위에서부터 하나씩 본다. 서버로 연 주소 `http://localhost:8000/w12_fetch_cards/`에서 한다.

1. **카드** — 카드 3장이 보이고 첫 카드 제목이 `HTML 텍스트 기초`다. 안내 자리는 비어 있다.
2. **Network** — F12 › **Network**를 연 채로 새로고침한다. 목록에서 `html-docs.json` 줄의 Status가 `200`이다. 그 줄을 누르면 Request URL이 `http://localhost:8000/w12_fetch_cards/data/html-docs.json`이다.
3. **Console** — 빨간 줄이 없다.
4. **파일이 없을 때(404)** — VS Code 탐색기에서 `data/html-docs.json`의 이름을 잠깐 `html-doc.json`으로 바꾸고 새로고침한다. 카드 없이 `자료를 불러오지 못했습니다.`가 보인다. Network에서 그 요청은 `404`이고, Console에는 그 요청이 404라는 줄(과 `favicon.ico` 404 줄) 말고 빨간 줄이 없다. `Uncaught`로 시작하는 줄은 없다. 확인했으면 이름을 되돌린다.
5. **두 번 눌러 열었을 때(`file://`)** — VS Code 탐색기에서 `index.html`을 오른쪽 클릭 › **Reveal in File Explorer**(macOS는 **Reveal in Finder**)로 찾아 두 번 눌러 연다. 주소가 `file:///…`로 시작하고, `자료를 불러오지 못했습니다.`가 보인다.

**예상 결과** — 터미널에는 데이터 파일 요청이 한 줄 늘었다. 4번을 할 때는 같은 줄이 `404`다.

```text
200 GET /w12_fetch_cards/data/html-docs.json
404 GET /w12_fetch_cards/data/html-docs.json
```

5번의 Console에는 아래처럼 시작하는 빨간 줄이 남는다. 터미널에는 아무 줄도 늘지 않는다.

```text
Access to fetch at 'file:///…/w12_fetch_cards/data/html-docs.json' from origin 'null' has been blocked by CORS policy: …
```

이것이 **서버로 여는 이유**다. `fetch`는 웹 서버에 파일을 **요청**한다(1주차 요청과 응답). 두 번 눌러 연 `file://` 화면에는 요청을 받을 서버가 없어서 브라우저가 요청을 막는다.
`node server.mjs`로 연 주소와 공개 주소(`https://student01.github.io/…`)는 서버가 파일을 돌려주므로 카드가 나온다. 시험 채점도 공개 주소에서 한다.

- 5번에서 빨간 줄이 남아도 `Uncaught (in promise) TypeError: Failed to fetch` 줄은 **없어야** 한다. 이 줄이 보이면 할 일 4를 다시 읽는다.
- 4번에서 `Uncaught`로 시작하는 줄이 보이면 할 일 2를 다시 읽는다.
- 이름 바꾸기는 VS Code 탐색기에서 한다(파일을 누르고 F2, macOS는 Enter). 확인이 끝나면 꼭 되돌린다. 되돌리지 않고 올리면 공개 주소에서도 카드가 나오지 않는다.
- 공개 주소에서도 같은지는 8단계에서 올린 뒤 본다.

### 7. 둘째·셋째 문제

고른 나머지 두 문제도 3~6단계 순서 그대로 한다. 서버는 띄운 채로 두고, 주소의 문제 id만 바꾼다(`http://localhost:8000/<문제 id>/`).

문제마다 "확인할 것"을 보는 곳이 다르다. 확인할 것에 적힌 곳을 연다.

| 문제 | 확인에 쓰는 곳 |
|---|---|
| README 문제(`w09_readme_links`·`w14_readme_images`) | VS Code에서 `README.md`를 열고 **Open Preview**(Ctrl+Shift+V, macOS는 ⌘+Shift+V). 서버 주소 뒤에 `README.md`를 붙여 열기. 올린 뒤 GitHub 저장소의 그 폴더 화면 |
| 목록·DOM 문제(`w05_greeting_card`·`w10_list_delete` 등) | F12 › Console에 문제에 적힌 식(`items.length` 등)을 쳐서 나오는 값 |
| 저장 문제(`w11_local_storage`) | F12 › **Application › Local Storage**에서 지금 주소를 골라 키와 값 보기, 키 지우기 |
| 좁은 화면을 보는 문제(`w04_responsive_css`·`w13_text_safe`) | F12 기기 모드(Ctrl+Shift+M, macOS는 ⌘+Shift+M)에서 폭을 적힌 값(375 등)으로 |
| 파일 연결 문제(`w01_link_fix`·`w02_about_page`) | F12 › Network에서 CSS·JS·새 페이지 요청이 200인지 |

- "확인할 것"이 모두 맞으면 그 문제는 끝이다. 해답과 비교하지 않는다.
- 저장 칸(Local Storage)은 주소의 앞부분(`http://localhost:8000`과 `https://student01.github.io`)마다 따로다. 서버 주소에서 넣은 목록은 공개 주소에 없다.
- 한 문제에 15분이 넘으면 남은 것은 두고 다음 문제로 간다. 시험에서도 5분 넘게 막히면 넘어간다.

### 8. 이번 주 저장소 만들어 올리기

1일차 50–60분에 한다. 세 문제를 다 못 끝냈어도 이 시간에는 올린다.

GitHub에서 **New repository**를 누르고 이름 `web-week15`, **Public**으로 만든다. README는 추가하지 않는다.
서버를 띄운 터미널이면 **Ctrl+C**로 멈추거나 새 터미널(**Terminal › New Terminal**)을 연다. 2주차에 배운 순서 그대로 친다. 현재 폴더: `web-week15`

```bash
git init
git add .
git commit -m "15주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week15.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save**를 누른다.

**예상 결과** — GitHub 저장소 화면을 새로고침하면 `server.mjs`와 푼 문제 폴더가 보인다.
1~3분 뒤 `https://student01.github.io/web-week15/w12_fetch_cards/`를 연다. 6단계의 1~3번(카드·Network 200·Console)을 공개 주소에서 다시 본다. Request URL은 `https://student01.github.io/web-week15/w12_fetch_cards/data/html-docs.json`이다. 공개 주소에서 새로고침하면 Status가 `304`로 보일 수 있다. 이미 받은 파일을 다시 쓴다는 뜻이다.
공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- `https://student01.github.io/web-week15/`는 404다. 맨 위에 `index.html`이 없어서다. 문제 폴더 주소로 연다.
- README 문제는 GitHub 저장소에서 그 폴더를 열어 파일 목록 아래에 README가 문서로 보이는지 본다.
- 404가 나면 주소의 `web-week15/`·문제 id·파일 이름이 저장소·폴더·파일 이름과 글자 단위로 같은지, Pages를 켰는지 본다.
- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- push가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../week02_github_pages/lab.md#막혔을-때)를 본다.
- 이 저장소와 Pages를 2일차 시험에 그대로 쓴다. 2일차에는 새로 만들지 않는다.

## 2일차

### 9. 시작 전 — 폴더 열고 서버 띄우기

시험 60분이 시작되기 전에 한다.
같은 PC에 `web-week15` 폴더가 남아 있으면 그대로 연다. 없으면 어제 올린 저장소를 내려받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week15.git
```

내려받은 `web-week15`를 **File › Open Folder**로 연다. 현재 폴더: `web-week15`

```bash
node server.mjs
```

**예상 결과** — `http://localhost:8000/`에 1일차에 푼 문제 폴더와 `server.mjs`가 보인다. 공개 주소 `https://student01.github.io/web-week15/w12_fetch_cards/`(어제 푼 문제)도 열린다.

- 공개 주소가 열리지 않으면 시험 전에 손을 든다. 저장소와 Pages는 1일차에 만들어 두었다.
- 서버를 띄운 터미널은 그대로 두고, 올리기는 새 터미널(**Terminal › New Terminal**)에서 한다.
- 볼 수 있는 것을 탭으로 열어 둔다: 교재 사이트, 본인 저장소, MDN.

### 10. exam 폴더 받아 맨 위에 넣기

시험이 시작되면 강의자가 `exam` 폴더를 나눠 준다. 받는 곳은 강의자가 공지한다. 압축 파일이면 푼다. 폴더 이름과 안의 파일을 바꾸지 않고 `web-week15` **맨 위**에 그대로 넣는다.

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week15/
  exam/
    a/  b/  c/  d/  e/   ← 문제 폴더. 시작 파일만 있다
    index.html           ← 목차. 문제 A~E로 가는 링크 다섯 줄
    README.md            ← 문제 문장 전체(A~E)
  w12_fetch_cards/       ← 1일차 연습 폴더. 그대로 둔다
  server.mjs
```

- 문제 A~E가 영역 A~E다. 문제 폴더 `a/`~`e/`에는 시작 파일만 있고, 문제 문장은 `exam/README.md` 한 곳에 있다.
- `web-week15/exam/exam/`처럼 한 겹 더 들어가면 공개 주소가 달라진다. 안쪽 `exam`을 맨 위로 꺼낸다.
- 1일차 연습 폴더는 지우지 않아도 된다. 채점은 `exam/` 폴더만 본다.

### 11. 목차 열기

서버가 떠 있는 브라우저에서 `http://localhost:8000/exam/`을 연다.

**예상 결과** — 목차가 열린다. 문제 A~E로 가는 링크가 다섯 줄이고, 누르면 그 문제의 화면이 열린다. 고치기 전이라 "확인할 것"이 맞지 않는 것이 정상이다.

- 목차 대신 파일 목록(`exam/` 한 줄)이 보이거나 404면 `exam` 폴더가 맨 위에 있는지(`web-week15/exam/index.html`), 한 겹 더 들어가 있지 않은지(`exam/exam/`) 본다. 서버를 다른 폴더에서 띄웠는지도 본다(터미널의 `폴더:` 줄).
- 받은 그대로의 상태는 문제 문장의 "시작 파일" 표에 적혀 있다. 표와 다르면(파일이 빠졌거나 문제 화면이 열리지 않으면) 고치기 전에 손을 든다.

### 12. 시작 올리기

아직 아무것도 고치지 않은 채로 한 번 올린다. 현재 폴더: `web-week15`(새 터미널)

```bash
git add .
git commit -m "기말 실기 시작"
git push
```

**예상 결과** — GitHub 저장소 화면을 새로고침하면 `exam/`이 보이고, 파일 목록 위에 보이는 마지막 commit 글이 `기말 실기 시작`이다.

- 올리기가 되는지 시험 처음에 확인해 두는 것이다. 여기서 막히면 바로 손을 든다. 시각이 기록된다.
- 1~3분 뒤면 `https://student01.github.io/web-week15/exam/`에 목차가 나온다. 지금 열어 보지 않아도 된다.

### 13. 문제 문장 읽고 풀기

문제 문장은 VS Code에서 `exam/README.md`를 열고 **Open Preview**(Ctrl+Shift+V, macOS는 ⌘+Shift+V)로 읽는다. 문제마다 절은 1일차와 같다(시작 파일·할 일·확인할 것·이 문제의 값). 3분 동안은 훑기만 한다. 문제마다 제목·권장 분·고칠 파일을 보고, 문장 전체는 그 문제를 풀 때 읽는다.

| 시간 | 할 일 |
|---|---|
| 0–3분 | `exam` 폴더 넣기, 목차 열기, 시작 올리기, 문제 문장 읽기 |
| 3–51분 | 문제 다섯(A~E) |
| 51–56분 | 마지막 올리기, 공개 주소 확인, Commits 탭 캡처 |
| 56–60분 | 예비(Pages 반영 기다리기, 제출 확인) |

- 문제 문장의 "이 폴더"는 그 문제의 폴더(`exam/a/` 등)다. 그 폴더 안의 파일만 고친다. 새 파일을 만들라는 문제는 그 폴더 안에 만든다.
- `exam/index.html`과 `exam/README.md`는 고치지 않는다.
- 순서는 자유다. 자신 있는 문제부터 해도 된다. 한 문제에 5분 넘게 막히면 다음 문제로 간다. 문제끼리 이어지지 않는다.
- 한 번에 한 곳만 고치고, 저장 → 새로고침 → 목차에서 그 문제를 열어 "확인할 것"을 본다.
- 문제를 하나 끝낼 때마다 `git add .` → `git commit -m "기말 실기 A"`(메시지는 자유) → `git push`로 올려 두어도 된다. 마지막에 몰리지 않는다.
- 시험 후반 30분 동안 강의자가 좌석을 돌며 **구술 1분**을 묻는다. 화면의 본인 코드에서 강의자가 가리킨 한 줄이 하는 일을 말하고, 이어서 푼다. 구술에 쓴 1분은 마감 때 돌려준다(시험 시간 안에 구술을 받은 사람은 마감이 1분 늦다).
- 질문은 문제 문장의 뜻·파일 위치·제출 방법·장애만 받는다. 코드가 맞는지는 답하지 않는다.

### 14. 마지막 올리기와 Commits 탭 캡처

51분이 되면 고치던 것을 멈추고 올린다. 현재 폴더: `web-week15`

```bash
git add .
git commit -m "기말 실기 끝"
git push
```

1. 1~3분 뒤 `https://student01.github.io/web-week15/exam/`을 새로고침하고 목차에서 문제마다 연다. **여기 보이는 것이 제출본이다.**
2. GitHub 저장소 화면에서 파일 목록 위 오른쪽의 **Commits**(시계 아이콘과 commit 수)를 눌러 Commits 탭을 연다.
3. 맨 위 commit이 `기말 실기 끝`이고 그 줄의 번호(일곱 글자)와 시각이 보이게, 주소창과 함께 캡처한다.
4. 제출 세 가지(공개 주소 `https://student01.github.io/web-week15/exam/`·저장소 주소 `https://github.com/student01/web-week15`·Commits 탭 캡처)를 낸다.
5. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

**예상 결과** — Commits 탭의 맨 위가 `기말 실기 끝`이다. 그 아래에 시험 중에 올린 commit과 `기말 실기 시작`이 있고, 맨 아래가 1일차의 `15주차 1일차`다.

- 저장하지 않은 파일은 올라가지 않는다. 올리기 전에 VS Code 탭 제목의 ● 표시(저장 안 됨)를 본다.
- 공개 주소가 5분 넘게 옛 화면이면 손을 들어 시각을 기록받고, 로컬 화면 캡처와 Commits 탭 캡처를 함께 낸다. 반영 지연은 감점하지 않는다. 채점자가 다음 날 공개 주소를 다시 연다.
- 마감(시험 60분이 끝나는 시각, 구술을 받은 사람은 1분 뒤) 전 마지막 commit이 제출본이다. 마감 뒤에는 이 저장소에 올리지 않는다.
- 증상별 확인 순서는 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다. 채점 기준은 [채점표](rubric.md)에 있다.
