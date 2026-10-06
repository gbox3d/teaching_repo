# 8주차 따라하기 — 문제 은행 연습과 중간 실기 절차

이번 주는 새로 배우는 것이 없다. 1~7주 실습 제출을 정리한 [문제 은행](examples/README.md)의 문제를 받아 풀고, 2일차에는 같은 문제를 값만 바꾼 시험을 본다.
이 문서는 **절차**만 다룬다. 해답 코드는 없다. 문제마다 "확인할 것"으로 스스로 맞춘다.
1일차(1~8단계)는 연습 날 절차, 2일차(9~15단계)는 시험 날 절차다. 예는 공개 문제 [w05_greeting_card](examples/w05_greeting_card/)로 든다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

## 1일차

### 1. web-week08 폴더 만들고 server.mjs 받기

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-week08`을 만들고 VS Code **File › Open Folder**로 연다.
7주차에 은행의 폼 문제를 받으며 만든 `web-week08`(안에 `w07_form_result/`)이 같은 PC에 있으면 새로 만들지 않고 그 폴더를 연다. `w07_form_result/`도 오늘의 연습 폴더다.
이번 주는 지난주 완성본을 넣지 않는다. 문제마다 시작 파일이 따로 있다.

[server.mjs](../../tools/static-server/server.mjs)를 열고 오른쪽 위 **Raw**를 누른다. 코드만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `web-week08` 맨 위에 `server.mjs` 이름으로 저장한다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week08/
  server.mjs
```

- 7주차 폴더를 열었다면 `w07_form_result/`가 함께 보인다.
- 저장한 이름이 `server.mjs.txt`처럼 `.txt`로 끝나면 이름을 고친다. 브라우저가 붙인 것이다.
- Node가 없는 PC는 `server.mjs` 없이 진행한다. 페이지는 두 번 눌러 연다(5단계).

### 2. 문제 고르기

[문제 은행 목록](examples/README.md)을 연다. 1~7주 실습 제출이 문제 일곱 개로 정리돼 있다.

| 영역 | 문제 | 권장 |
|---|---|---|
| A HTML (4점) | [w01_link_fix](examples/w01_link_fix/) · [w02_about_page](examples/w02_about_page/) · [w03_guestbook_form](examples/w03_guestbook_form/) | 8 · 10 · 10분 |
| B CSS (4점) | [w04_responsive_css](examples/w04_responsive_css/) | 12분 |
| C JavaScript·DOM (5점) | [w05_greeting_card](examples/w05_greeting_card/) · [w06_dark_mode](examples/w06_dark_mode/) | 12 · 12분 |
| D 폼 (3점) | [w07_form_result](examples/w07_form_result/) | 11분 |

영역마다 한 문제씩, **자신 없는 영역부터** 셋을 고른다. 그 주 실습을 끝내지 못했거나 제출 캡처를 못 낸 주가 먼저다.

**예상 결과** — 오늘 풀 문제 셋의 id를 차례로 적어 두었다. 예: `w04_responsive_css` → `w05_greeting_card` → `w07_form_result`.

- 시험에는 영역마다 한 문제가 나온다. A는 셋 중 하나, C는 둘 중 하나다. 어느 문제가 나올지는 미리 알려 주지 않는다.
- 문제끼리 이어지지 않는다. 어느 문제부터 풀어도 된다.

### 3. w05_greeting_card 로 문제 읽는 법 보기

[w05_greeting_card](examples/w05_greeting_card/)를 연다. GitHub 폴더 화면의 파일 목록 아래에 문제 문장(`README.md`)이 보인다. 은행의 문제는 모두 같은 모양이다.

| 문제 문장의 자리 | 읽을 것 | w05_greeting_card 에서 |
|---|---|---|
| 제목 아래 줄 | 출처 주 · 권장 분 · 시험 영역 | 5주차 실습 제출 · 권장 12분 · 중간 C(JavaScript·DOM) |
| 시작 파일 | 파일마다 지금 상태. 고칠 파일과 고치지 않을 파일 | `index.html`은 `app.js` 연결 줄과 인사 카드가 없다. `styles.css`는 완성본이라 고치지 않는다. `app.js`는 주석 한 줄뿐이다 |
| 할 일 | 무엇을 어느 순서로 하나. 그 주에 배운 것만 쓴다 | `index.html` 두 곳, `app.js` 여섯 가지 |
| 확인할 것 | 다 했을 때 화면·F12에 보여야 할 결과. 해답 대신 이것으로 맞춘다. 채점도 이 항목으로 한다 | 카드 글자, Elements의 `app.js` 연결 줄과 카드 class·id, Console 두 줄, Console에 친 `hello(11)`·`hello(12)`·`hello(17)`·`hello(18)`·`greet('student99')`의 결과 |
| 이 문제의 값 | 시험에서 바뀌는 값 | 이름 `guest07`, 시각 `15`, 카드 id `welcome`, 문장들, 기준 `18`·`12` |
| 받기와 올리기 | 폴더 이름과 여는 주소 | `web-week08/w05_greeting_card/`, `http://localhost:8000/w05_greeting_card/` |

**예상 결과** — 코드를 쓰기 전에 "어느 파일의 어디를 고치나"와 "무엇이 보이면 끝인가"를 말할 수 있다. w05라면 "`index.html` 두 곳과 `app.js`를 쓰고, 카드에 `반가워요, guest07님. 즐거운 오후예요.`가 보이고 Console에 두 줄이 찍히고, Console에 친 `hello`·`greet`의 결과가 문제 문장과 같으면 끝"이다.

- 시험 문제는 문장·할 일·확인하는 방법이 그대로이고 "이 문제의 값" 표의 값만 다르다. 이 문제가 시험에 나온다면 이름·시각·id·문장·기준이 다른 값으로 바뀌어 있다. 그래서 답을 외우지 않고 **읽는 순서**를 익힌다.
- 값은 문제 문장에서 복사해 붙인다. 글자 하나·빈칸 하나·마침표 하나가 달라도 "확인할 것"이 맞지 않는다.
- 제목 아래 줄의 출처 링크를 누르면 그 주 실습지의 제출 절이 열린다. 그 주에 같은 것을 다른 값으로 만들었다. 그 주의 따라하기도 함께 본다.
- 해답은 공개하지 않는다. "확인할 것"이 모두 맞으면 된 것이다.

### 4. 문제 폴더 만들고 Raw 로 받기

`web-week08` 안에 문제 id와 같은 이름의 폴더를 만든다. VS Code 탐색기에서 **New Folder**를 눌러도 되고, 명령으로 만들어도 된다. 현재 폴더: `web-week08`

```bash
mkdir w05_greeting_card
```

문제 폴더 화면에서 파일을 하나씩 누르고 오른쪽 위 **Raw**를 누른다. 코드만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 방금 만든 폴더에 저장한다. 파일 이름은 교재와 **같게** 둔다.

- `README.md`는 받지 않는다. 지금 읽고 있는 문제 문장이다. 문장은 GitHub 화면에서 읽는다.
- 하위 폴더가 있는 문제(w04의 `images/`)는 같은 이름의 폴더를 먼저 만들고 그 안에 저장한다. 그림 파일도 **Raw**를 누르면 그림만 보이는 화면이 열린다. 그 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 같은 하위 폴더에 저장한다.

**예상 결과** — 탐색기가 아래 모양이다.

```text
web-week08/
  w05_greeting_card/
    app.js
    index.html
    styles.css
  server.mjs
```

- 저장한 파일 이름이 `index.html.txt`처럼 `.txt`로 끝나면 이름을 고친다. 이름은 VS Code 탐색기에서 확인한다(Windows 파일 탐색기는 기본 설정에서 확장자를 숨긴다).
- 폴더 이름은 문제 id 그대로다. 다르게 만들면 문제 문장의 주소와 공개 주소가 달라진다.
- Raw가 열리지 않으면 VS Code에서 같은 이름의 파일을 만들고 교재 화면을 보며 친다. 주석 줄도 그대로 친다.

### 5. 서버로 열기

현재 폴더: `web-week08`

```bash
node server.mjs
```

**예상 결과** — 터미널에 두 줄이 찍히고 서버가 떠 있다. 폴더 줄은 PC마다 다르다.

```text
폴더: C:\Users\student\web-week08
주소: http://localhost:8000/   (멈추기: Ctrl+C)
```

Chrome 주소창에 문제 문장 끝 "받기와 올리기"의 주소 `http://localhost:8000/w05_greeting_card/`를 친다.

**예상 결과** — 제목 `인사 카드`, `소개` 아래 흰 카드 한 장(`이 페이지를 열면 맨 위 카드에 인사말이 나온다.`)과 꼬리말이 보인다. 아직 인사 카드는 없다. 터미널에는 요청이 한 줄씩 늘었다(순서는 바뀔 수 있다).

```text
200 GET /w05_greeting_card/
200 GET /w05_greeting_card/styles.css
404 GET /favicon.ico
```

- `app.js` 줄이 없다. 지금 `index.html`이 `app.js`를 부르지 않기 때문이다. 할 일 1을 하고 새로고침하면 `200 GET /w05_greeting_card/app.js` 줄이 늘어난다.
- `favicon.ico`는 브라우저가 탭 아이콘을 찾으려고 스스로 보낸 요청이다. 404여도 괜찮다.
- `http://localhost:8000/`만 치면 파일 목록이 보인다. 저장소 맨 위에는 `index.html`이 없어서다. 목록에서 `w05_greeting_card/`를 눌러도 된다.
- 첫 페이지가 `index.html`이 아닌 문제(w03 `join.html`, w07 `comment.html`)는 주소 끝에 파일 이름까지 붙인다.
- 서버는 띄워 둔 채로 다음 문제도 연다. 폴더를 새로 만들어도 다시 띄울 필요가 없다. 멈출 때는 서버를 띄운 터미널에서 **Ctrl+C**.
- Node가 없는 PC는 `index.html`을 두 번 눌러 연다. 화면은 같다. Network의 Status 번호만 안 보인다(6단계).

### 6. 할 일 하고 확인할 것 맞추기

할 일을 위에서부터 한 덩어리씩 한다. 덩어리마다 **저장**(Ctrl+S, macOS는 ⌘+S) → 브라우저 **새로고침**(F5, macOS는 ⌘+R) → **F12 › Console**을 본다. 빨간 줄이 있으면 오른쪽 `파일:줄`로 간다.
다 했으면 "확인할 것"을 위에서부터 하나씩 직접 해 본다. w05는 다섯이다.

1. 화면 — 카드 글자를 문제 문장과 글자 단위로 비교한다.
2. Elements — F12 › **Elements**에서 `app.js`를 연결한 줄과 카드 `<p>`의 class·id를 본다.
3. Console — 페이지를 열자마자 찍힌 두 줄을 읽는다. 빨간 줄이 없어야 한다.
4. Console에 식 치기 — Console 맨 아래 `>` 옆을 누르고 `hello(11)`을 친 뒤 Enter. 이어서 `hello(12)`·`hello(17)`·`hello(18)`을 친다.
5. 이어서 `greet('student99')`를 친다.

**예상 결과** — 다섯 항목이 모두 문제 문장과 같다. Console은 아래 모양이다. 줄 오른쪽 `app.js:…`의 줄 번호는 사람마다 다르다.

```text
15                                       app.js:…
반가워요, guest07님. 즐거운 오후예요.      app.js:…
> hello(11)
< '상쾌한 아침이에요.'
> greet('student99')
< '반가워요, student99님.'
```

다른 문제의 "확인할 것"은 아래 자리에서 본다.

| "확인할 것"에 이런 말이 있으면 | 보는 곳 | 은행에서 |
|---|---|---|
| 화면에 … 가 보인다 · 누르면 … 로 바뀐다 | 페이지를 보고 직접 누른다 | 모든 문제 |
| Console 에 … 가 찍힌다 · Console 에 … 를 치면 · 빨간 줄이 없다 | F12 › **Console** | w05 `hello(11)`, w03 `document.querySelector('#memo').rows` |
| Status 가 `200` · `404` 인 줄이 없다 · 그 파일 줄은 없다 | F12 › **Network**를 연 채 새로고침 | w01 두 파일 200, w02 새 페이지 200 |
| `background-color` 가 `rgb(…)` · 상자 그림의 padding·border·margin | F12 › **Elements**에서 요소를 고르고 오른쪽 **Styles**·**Computed** | w04 카드, w06 다크 배경 |
| 폭 `375` 에서 · 가로 스크롤 막대가 없다 | 기기 모드(**Ctrl+Shift+M**, macOS는 ⌘+Shift+M)에서 위쪽 폭 칸에 숫자를 친다 | w04 메뉴 |
| 이름표를 누르면 커서 · Enter 로도 | 페이지에서 직접 누르고 친다 | w03 이름표, w07 Enter 제출 |

- Network의 Status 번호는 `node server.mjs`로 연 주소나 공개 주소에서만 보인다. 두 번 눌러 연 `file://` 화면에는 번호가 없다.
- CSS에 `#eef2ff`로 쓴 색은 Computed에서 `rgb(238, 242, 255)`로 보인다. 같은 색을 다르게 적은 것이다.
- 맞지 않는 항목이 있으면 그 항목이 가리키는 할 일로 돌아간다. 한 번에 한 곳만 고치고 새로고침한다.
- 어떤 방법으로 썼는지는 채점하지 않는다. "확인할 것"의 결과가 같으면 정답이다.

### 7. 이번 주 저장소 만들어 올리기

1일차 50–60분에 한다. 문제 셋을 다 못 풀었어도 이 시간에는 올린다.

GitHub에서 **New repository**를 누르고 이름 `web-week08`, **Public**으로 만든다. README는 추가하지 않는다.
터미널에서 2주차에 배운 순서 그대로 친다. 서버가 떠 있는 터미널에서는 칠 수 없으니 **Terminal › New Terminal**로 하나 더 연다. 현재 폴더: `web-week08`

```bash
git init
git add .
git commit -m "8주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week08.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save**를 누른다.

**예상 결과** — GitHub 저장소 화면을 새로고침하면 푼 문제 폴더(예: `w05_greeting_card/`)와 `server.mjs`가 보인다.

- push가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../week02_github_pages/lab.md#막혔을-때)를 본다.

### 8. 공개 주소에서 다시 확인

1~3분 뒤 `https://student01.github.io/web-week08/w05_greeting_card/`를 연다. 6단계에서 맞춘 "확인할 것"을 공개 주소에서 한 번 더 해 본다.

**예상 결과** — 로컬(`http://localhost:8000/w05_greeting_card/`)과 같은 화면·Console이다.

- `https://student01.github.io/web-week08/`만 치면 404다. 저장소 맨 위에는 `index.html`이 없다. 문제 폴더 이름까지 붙인다.
- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다. 새 시크릿 창(**Ctrl+Shift+N**, macOS는 ⌘+Shift+N)으로 열어도 된다.
- 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.
- 2일차에는 이 저장소에 `exam` 폴더를 넣는다. 저장소를 새로 만들지 않는다.

## 2일차

### 9. 시험 전 — 폴더 열고 서버 띄우기

같은 PC에 `web-week08` 폴더가 남아 있으면 그대로 연다. 없으면 1일차에 올린 저장소를 내려받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week08.git
```

내려받은 `web-week08`을 **File › Open Folder**로 열고 서버를 띄운다. 현재 폴더: `web-week08`

```bash
node server.mjs
```

**예상 결과** — `http://localhost:8000/`에 1일차 연습 폴더와 `server.mjs`가 목록으로 보인다.

- 1일차에 올린 공개 주소(`https://student01.github.io/web-week08/w05_greeting_card/` 등)가 열리는지도 본다. 열리지 않으면 시험 전에 손을 든다.
- 올리기 명령을 칠 터미널을 하나 더 열어 둔다(**Terminal › New Terminal**). 12·14단계는 그 터미널에서 친다.
- 1일차에 저장소를 만들지 못했으면 지금 7단계를 먼저 한다. 시험 시간에는 저장소를 만들지 않는다.

### 10. exam 폴더 받아 맨 위에 넣기

시험이 시작되면 강의자가 `exam` 폴더를 나눠 준다. 받는 곳은 강의자가 공지한다. 압축 파일로 받았으면 압축을 푼다.
`exam` 폴더를 **통째로** `web-week08` 맨 위로 옮긴다. 폴더 안의 파일을 꺼내지 않는다.

**예상 결과** — 탐색기가 아래 모양이다.

```text
web-week08/
  exam/
    README.md            ← 문제 문장 넷. 문제 문장은 여기에만 있다
    index.html           ← 목차. 문제마다 첫 페이지로 가는 링크
    a/                   ← 문제 A의 시작 파일
    b/                   ← 문제 B
    c/                   ← 문제 C
    d/                   ← 문제 D
  w05_greeting_card/ …   ← 1일차 연습 폴더. 그대로 둔다
  server.mjs
```

- `web-week08/exam/index.html`이 되어야 한다. 압축을 풀다가 `exam/exam/`처럼 한 겹 더 생기면 안쪽 `exam`을 맨 위로 옮기고 빈 바깥 폴더를 지운다.
- 문제 폴더(`a/`~`d/`)에는 시작 파일만 있다. 문제 문장의 "이 폴더"는 그 문제의 폴더다.
- 폴더·파일 이름을 바꾸지 않는다. 공개 주소는 대소문자를 구분한다.

### 11. 목차와 문제 문장 열기

Chrome 주소창에 `http://localhost:8000/exam/`을 친다.

**예상 결과** — 목차가 열리고 문제 A~D로 가는 링크 넷이 보인다. 하나씩 누르면 문제마다 첫 페이지가 열린다. 아직 아무것도 고치지 않았으니 미완성 화면이 맞다.

문제 문장은 VS Code에서 `exam/README.md`를 열고 **Ctrl+Shift+V**(macOS는 ⌘+Shift+V)로 미리 보기 한다. 문제마다 은행 문제와 같은 네 절(시작 파일·할 일·확인할 것·이 문제의 값)이 있고, 그 문제의 폴더와 권장 분이 적혀 있다.

- 0–5분은 읽는 시간이다. 12단계(시작 올리기)를 먼저 한 뒤 문제지를 훑어 문제마다 제목·권장 분·고칠 파일만 본다. 문장 전체는 그 문제를 풀 때 읽는다. 아직 코드를 쓰지 않는다.
- Node가 없는 PC는 `exam/index.html`을 두 번 눌러 연다. 끝이 `/`인 링크(폴더로 가는 링크)를 누르면 파일 목록이 보인다. 그 목록에서 `index.html`을 누른다.

### 12. 시작 올리기

아직 아무것도 고치지 않은 채로 한 번 올린다. 시험을 시작했다는 기록이다. 현재 폴더: `web-week08`

```bash
git add .
git commit -m "중간 실기 시작"
git push
```

**예상 결과** — `git push`의 마지막 줄에 `main -> main`이 보인다. GitHub 저장소 화면을 새로고침하면 맨 위에 `exam` 폴더가 보인다.

- 이것이 시험 시간의 첫 commit이다. 14단계의 마지막 commit과 합쳐 두 번 이상이 된다.

### 13. 문제 풀기

문제 하나를 푸는 순서는 1일차 3·6단계와 같다. 문제 문장 읽기 → 할 일 → 저장 → 새로고침 → "확인할 것" 맞추기. 페이지는 목차의 링크로 연다. 시간표는 [실습지 2일차](lab.md#2일차--중간-실기-60분)에 있다.

**예상 결과** — 문제마다 "확인할 것"이 로컬 주소(`http://localhost:8000/exam/…`)에서 맞고, Console에 빨간 줄이 없다.

- 문제마다 그 문제의 폴더(`exam/a/` 등) 안의 파일만 고친다. 문제가 새 파일을 만들라고 하면 그 폴더 안에 만든다. 목차 `exam/index.html`과 `exam/README.md`는 고치지 않는다.
- 한 문제에 5분 넘게 막히면 다음 문제로 간다. 문제끼리 이어지지 않는다. 넘긴 문제는 남는 시간에 돌아와 푼다.
- 문제 하나를 끝낼 때마다 12단계처럼 올려 두어도 된다. commit 메시지는 자유다.

### 14. 마지막 올리기

50–55분에 한다. VS Code 탭 제목에 ● 표시(저장 안 됨)가 없는지 먼저 본다. 현재 폴더: `web-week08`

```bash
git add .
git commit -m "중간 실기 끝"
git push
```

**예상 결과** — `git push`의 마지막 줄에 `main -> main`이 보인다.

- 저장하지 않은 파일은 올라가지 않는다.
- 마감(시험 60분이 끝나는 시각) 전 마지막 commit이 제출본이다.

### 15. 공개 주소 확인과 Commits 탭 캡처

1. 1~3분 뒤 `https://student01.github.io/web-week08/exam/`을 새로고침한다. 목차에서 문제마다 눌러 연다.
2. GitHub 저장소 화면 `https://github.com/student01/web-week08`에서 파일 목록 위 오른쪽의 **Commits**(시계 아이콘과 commit 수)를 누른다.
3. 맨 위 commit이 `중간 실기 끝`이고, 그 줄의 번호(오른쪽 끝 일곱 글자)와 시각(`committed … ago`와 그 위의 날짜 줄)이 주소창과 함께 한 화면에 보이게 캡처한다. Windows **Win+Shift+S**, macOS **⌘+Shift+4**.
4. 아래 세 가지를 제출한다.

```text
① https://student01.github.io/web-week08/exam/
② https://github.com/student01/web-week08
③ Commits 탭 캡처 1장
```

5. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

**예상 결과** — 공개 주소의 목차와 문제 페이지가 로컬과 같다. Commits 탭은 맨 위가 `중간 실기 끝`이고, 그보다 아래에 `중간 실기 시작`과 1일차의 `8주차 1일차`가 있다.

- 공개 주소가 시험 시간 안에 안 바뀌어도 감점하지 않는다. 채점자가 다음 날 다시 연다. 로컬 화면 캡처와 Commits 탭 캡처도 인정한다.
- `committed … ago`에 마우스를 올리면 정확한 시각이 뜬다.
- 캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 아이디는 보여도 된다.
- 채점이 끝날 때까지 저장소를 지우거나 이름을 바꾸지 않는다.

## 오류가 나면

브라우저에서는 F12 **Console**의 **첫 빨간 줄**을 읽는다. 줄 끝의 `app.js:7`이 파일 이름과 줄 번호다.
터미널에서는 첫 `error:` 또는 `fatal:` 줄을 읽는다. 자주 나오는 증상과 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 확인한다. 1일차에는 10분 넘게 같은 자리에 있으면 손을 들어 도움을 요청한다. 시험 중에는 환경·제출 문제만 함께 본다.
