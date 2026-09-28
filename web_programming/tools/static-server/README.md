# 수업용 정적 웹 서버 — server.mjs

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/tools/static-server

폴더 하나를 `http://localhost:8000/` 주소로 열어 주는 작은 웹 서버다. 파일은 [server.mjs](server.mjs) 하나뿐이고 Node.js 기본 모듈만 쓴다. `npm install`이 필요 없다.
한 학기 내내 같은 파일을 쓴다. 매주 새로 만드는 저장소 폴더(`web-week05` 등)에 넣고 `node server.mjs` 한 줄로 띄운다.

## 왜 서버로 여나

HTML 파일을 두 번 눌러 열면 주소가 `file:///…`로 시작한다. 이것은 웹 서버를 거치지 않고 파일을 바로 읽는 방식이다. 대부분의 예제는 이렇게 열어도 되지만, 몇 가지는 다르게 동작한다.

| | `file:///…`(두 번 눌러 열기) | `http://localhost:8000/…`(이 서버) | 공개 주소 `https://<아이디>.github.io/…` |
|---|---|---|---|
| HTML·CSS·JS·그림 | 된다 | 된다 | 된다 |
| `fetch('data.json')` | 막힌다 | 된다 | 된다 |
| `<script type="module">` | 막힌다 | 된다 | 된다 |
| 요청이 보이나 | 안 보인다 | 터미널에 한 줄씩 찍힌다 | F12 › Network |
| 주소 모양 | 폴더 경로 | 공개 주소와 같은 모양 | — |

이 서버는 GitHub Pages가 하는 일(요청을 받아 파일을 돌려준다)을 내 PC에서 똑같이 한다. push 하기 전에 공개 주소와 같은 조건으로 미리 볼 수 있다.

## 준비

- Node.js LTS. 터미널에서 `node -v`를 쳐서 `v18` 이상이 나오면 된다. 없으면 https://nodejs.org 에서 LTS를 설치한다.
- [server.mjs](server.mjs)를 연다 → 오른쪽 위 **Raw** → **Ctrl+S**(macOS ⌘+S)로 그 주의 저장소 폴더에 `server.mjs` 이름으로 저장한다.

## 띄우기와 멈추기

VS Code에서 저장소 폴더를 연 뒤 **Terminal › New Terminal**을 열고 친다.

```bash
node server.mjs
```

```text
폴더: C:\Users\student\web-week05
주소: http://localhost:8000/   (멈추기: Ctrl+C)
```

브라우저 주소창에 `http://localhost:8000/`을 친다. 그 폴더의 `index.html`이 열린다. `index.html`이 없는 폴더는 파일 목록이 보인다.
파일을 고치고 저장한 뒤 **새로고침**하면 바로 바뀐다. 서버를 다시 띄울 필요는 없다.
멈출 때는 서버를 띄운 터미널을 누르고 **Ctrl+C**를 누른다.

## 터미널에 찍히는 줄 읽기

페이지 하나를 열면 여러 줄이 찍힌다.

```text
200 GET /
200 GET /styles.css
200 GET /app.js
200 GET /images/profile.png
404 GET /favicon.ico
```

- 브라우저는 HTML을 먼저 받고, 그 안의 `<link>`·`<script>`·`<img>`가 가리키는 파일을 **하나씩 따로** 요청한다(1주차 "요청과 응답").
- 앞의 숫자는 응답 코드다. `200` 찾아서 보냈다, `404` 그런 파일이 없다, `301` 주소 끝에 `/`를 붙여 다시 오라.
- `favicon.ico`는 브라우저가 탭 아이콘을 찾으려고 스스로 보내는 요청이다. 404여도 괜찮다.
- 내 파일이 404면 파일 이름·폴더·대소문자를 본다. `Styles.css`와 `styles.css`는 다른 이름이다.

## 바꿔 쓰기

| 하고 싶은 것 | 명령 |
|---|---|
| 포트 바꾸기(8000을 이미 쓰고 있을 때) | `node server.mjs . 5500` → `http://localhost:5500/` |
| 다른 폴더 열기 | `node server.mjs ../web-week04` |
| 교재 예제 폴더 통째로 열기 | `node server.mjs 교재저장소/web_programming/weeks/week05_javascript_data/examples` |

### 휴대폰으로 보기(같은 Wi-Fi)

기본은 **내 PC에서만** 열린다. 같은 Wi-Fi의 휴대폰에서 반응형 화면을 보고 싶을 때만 아래처럼 띄운다. 끝나면 Ctrl+C로 바로 멈춘다.

```bash
# macOS
HOST=0.0.0.0 node server.mjs
# Windows PowerShell
$env:HOST="0.0.0.0"; node server.mjs
```

휴대폰 브라우저에 `http://<PC의 IP 주소>:8000/`을 친다. PC의 IP는 Windows `ipconfig`, macOS **시스템 설정 › Wi-Fi › 세부사항**에서 본다. 공용 PC·공용 Wi-Fi에서는 쓰지 않는다.

### 코드 고쳐 보기

서버도 JavaScript다. 5주차에 배운 `if`·함수로 읽을 수 있다. 예를 들어 `/api/time` 주소에 지금 시각을 JSON으로 돌려주게 하려면, `http.createServer((req, res) => {` 바로 아래에 세 줄을 넣는다.

```js
  if (req.url === '/api/time') {
    return send(req, res, 200, JSON.stringify({ now: new Date().toISOString() }), 'application/json; charset=utf-8');
  }
```

저장 → Ctrl+C → `node server.mjs`로 다시 띄운 뒤 `http://localhost:8000/api/time`을 연다. 이런 주소는 **내 PC 서버에만** 있다. GitHub Pages는 파일만 돌려주므로 공개 주소에서는 404다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| `'node' is not recognized` / `command not found: node` | Node.js가 설치되지 않았거나 설치 뒤 터미널을 새로 열지 않았다. 설치 후 VS Code를 다시 연다 |
| `8000 번 포트를 이미 다른 프로그램이 쓰고 있습니다` | 다른 터미널에 서버가 떠 있다. 그 터미널에서 Ctrl+C 하거나 `node server.mjs . 8001`로 띄운다 |
| `Cannot find module …server.mjs` | 터미널의 현재 폴더에 `server.mjs`가 없다. `ls`(Windows `dir`)로 확인하고 저장소 폴더로 `cd` 한다 |
| 브라우저에 `사이트에 연결할 수 없음` | 서버가 멈춰 있다. 터미널에 `주소: http://localhost:8000/` 줄이 있는지 본다 |
| 고쳤는데 화면이 그대로 | 저장했는지(VS Code 탭의 ● 표시) 본다. 다른 폴더를 띄웠는지 터미널의 `폴더:` 줄을 본다 |
| 파일 목록만 보이고 페이지가 안 열린다 | 그 폴더에 `index.html`이 없다. 목록에서 파일을 누르거나 파일 이름을 확인한다 |

## 이 서버가 하지 않는 것

- 로그인, 글 저장, 데이터베이스는 없다. 파일을 **읽어서 돌려주기만** 한다(정적 서버).
- `server.mjs` 폴더 밖의 파일은 주소에 `../`를 넣어도 내보내지 않는다.
- 수업 밖 실제 서비스용이 아니다.
