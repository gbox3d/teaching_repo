[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/synthesizer)

# 특강 실습 — 소리 부품을 바꿔 듣고, 연주기를 내 노래로

**이어폰을 낀다.** 실습실 전체가 스피커로 소리를 내면 아무것도 들리지 않는다. PC 음량은 작게 시작한다.
이번 실습은 코드를 새로 짜는 것이 아니라 **값을 바꿔 보는 것**이다. 비교 파일에서 값을 바꿔 듣고, 디스코 연주기의 곡 · 리듬 · 소리를 내 것으로 바꾼다.
결과는 **귀, 화면, F12 › Console** 세 곳에서 본다. Console 은 실습 내내 열어 둔다.
결과물은 새 저장소 `web-synth` 의 공개 주소에서 **내가 고친 `my_song.json`** 을 재생하는 화면 캡처 한 장이다.
`student01` 은 예시 아이디이므로 본인 아이디로 바꾼다.

파일을 받는 법, 서버를 띄우는 법, 연주기 전문은 [따라하기](walkthrough.md)에 있다.
"바꿔 보기"는 **무엇이 달라질지 먼저 말해 보고** 저장 → 새로고침 → 단추를 다시 눌러 확인한다.
곡 데이터는 **코드 진행만** 바꾼다. 다른 노래의 멜로디 · 가사 · 음원은 넣지 않는다.

## 실습 60분

| 시간 | 할 일 |
|---|---|
| 0–5분 | 새 폴더 `web-synth` 를 VS Code 로 연다(**File › Open Folder**). [server.mjs](../../tools/static-server/server.mjs) 와 연주기 여섯 파일([`examples/build/`](examples/build/))을 **Raw** 로 맨 위에 저장하고 `ex` 폴더를 만든다. 터미널에서 `node server.mjs` → Chrome 에서 `http://localhost:8000/` → ▶ 재생으로 소리를 확인한다 |
| 5–25분 | 비교 파일 실험. 필수는 ex03 · ex04 · ex08 이다. 나머지는 덱에서 바로 들어 본다. 고쳐 볼 파일만 `ex/` 에 **Raw** 로 저장해 `http://localhost:8000/ex/…` 로 연다 |
| 25–45분 | 연주기를 내 것으로: ① `my_song.json` 의 제목 · 코드 · bpm 바꾸기 ② `PATTERNS.disco` 한 줄 바꾸기 ③ `playTone` 에 넘기는 소리 하나 바꾸기 — 셋 중 둘 이상 |
| 45–50분 | localhost 에서 확인: 곡 선택 my_song.json → ▶ 재생 → 머리 줄의 내 제목 · BPM, 강조된 마디, Console 에 빨간 줄 없음 |
| 50–60분 | 새 저장소 `web-synth` 만들어 올리기 → **Settings › Pages** → 공개 주소에서 my_song.json 재생 캡처 → 공용 PC면 자격 증명 삭제 |

5분 안에 일곱 파일을 다 받지 못했으면 연주기부터 띄우고, `server.mjs` 가 없으면 옆자리와 확인한다. 비교 파일은 덱에서 들을 수 있으므로 받지 않아도 시작할 수 있다.

### 1. 준비 — web-synth 폴더, 서버, 연주기

[따라하기 1 · 2단계](walkthrough.md#1-web-synth-폴더와-서버)를 본다. `index.html` 은 두 번 눌러 열지 않는다. 늘 `http://localhost:8000/` 으로 연다.

- 바꿔 보기: 연주기를 열고 터미널에 찍힌 줄을 센다. `index.html` 하나를 열었는데 왜 `/main.css` · `/index.js` · `/synth.js` · `/only_you.json` 이 따로 찍히나? `/synth.js` 는 어느 파일의 몇 행이 부른 것인가?
- 바꿔 보기: ▶ 재생 뒤 화면에서 움직이는 것은 무엇인가? 체크 상자 `킥` 을 끄면 무엇이 사라지나? `코드 파형` 을 sine 으로, 필터를 200 으로 바꾸면 코드 소리는 어떻게 되나?
- 바꿔 보기: 곡 선택을 my_song.json 으로 바꾼다. 터미널에 어떤 줄이 늘었나? 머리 줄과 BPM 숫자는 어떻게 바뀌었나?
- 흔한 실수: `index.html` 을 두 번 눌러 연다(`file:///…`). 머리 줄이 `곡 없음`, 아래에 `주소가 file:// 입니다. 연주기는 서버로 엽니다: 이 폴더에서 node server.mjs 를 띄우고 http://localhost:8000/ 을 여세요.` 가 뜨고 표시등도 악보도 없다. Console 에는 `Access to script at 'file:///…/index.js' from origin 'null' has been blocked by CORS policy` 가 뜬다. `type="module"` 의 `import` 와 `fetch` 는 서버나 공개 주소에서만 돈다.

### 2. ex03 엔벨로프 (`linearRampToValueAtTime` · `exponentialRampToValueAtTime`)

[examples/ex03_envelope.html](examples/ex03_envelope.html) 을 덱에서 듣는다. 숫자를 바꿀 때는 `ex/ex03_envelope.html` 로 저장해 `http://localhost:8000/ex/ex03_envelope.html` 로 연다.

- 바꿔 보기: 1번과 2번을 번갈아 누른다. 1번의 시작과 끝에서 들리는 '딱' 은 2번에서 왜 사라졌나? 아래 그림의 시작과 끝을 비교한다.
- 바꿔 보기: 2번과 5번은 attack · release 숫자가 같다. 무엇이 다르게 들리나? 52행과 55행에서 다른 글자는 무엇인가?
- 바꿔 보기: 53행 3번의 `play(0.3, 0.6, 0.8, 'linear')` 에서 첫 숫자(attack)를 `0.005` 로 바꾸면 '깔리는 소리' 가 어떻게 되나? 마지막 숫자(release)를 `2` 로 바꾸면 그림은 어떻게 되나?
- 흔한 실수: exponential 의 목표값에 `0` 을 쓴다(40행의 `0.0001` 을 `0` 으로). 5번을 누르면 Console 에 `Uncaught RangeError: Failed to execute 'exponentialRampToValueAtTime' on 'AudioParam': The float target value provided (0) should not be in the range (-1.40130e-45, 1.40130e-45).` 가 뜨고 소리가 나지 않는다. exponential 은 0 에 닿을 수 없다. `0.0001` 처럼 아주 작은 수를 쓴다.

### 3. ex04 화음 (`SHAPES` · 같은 시각)

[examples/ex04_chord.html](examples/ex04_chord.html) 을 `ex/ex04_chord.html` 로 저장한다.

- 바꿔 보기: 2번의 C 와 Cm 을 번갈아 누른다. 화면의 MIDI 세 숫자 중 어느 것이 몇만큼 다른가? A 와 Am 도 같은 자리가 다른가?
- 바꿔 보기: 먼저 28행을 `const SHAPES = { '': [0, 4, 7], m: [0, 3, 7], 7: [0, 4, 7, 10] };` 으로 바꾼다. 그다음 15행 F 단추 아래에 `<button data-chord="G7">G7</button>` 한 줄을 더한다. G7 을 누르면 화면에 무엇이 적히나? G 와 어떻게 다르게 들리나?
- 바꿔 보기: 72행 아르페지오의 `0.15` 를 `0.1` 로 바꾼다(74행 글자도 같이). 무엇이 빨라지나? 71행 `i < 8` 을 `i < 16` 으로 바꾸면?
- 흔한 실수: `SHAPES` 에 `7` 을 더하지 않고 G7 단추만 만든다. G7 을 누르면 Console 에 `Uncaught TypeError: shape is not iterable` 가 뜨고 소리가 나지 않는다. 없는 모양을 꺼내면 `undefined` 이기 때문이다. 연주기의 `chordToMidis` 는 같은 경우를 화면 문구로 알려 준다(6번).

### 4. ex08 리듬은 배열이다 (`PRESETS` · 16칸)

[examples/ex08_pattern.html](examples/ex08_pattern.html) 을 `ex/ex08_pattern.html` 로 저장한다.

- 바꿔 보기: ▶ 재생을 누르고 kick 줄의 5번째 · 13번째 칸(2박 · 4박)을 끈다. 아래 배열의 어디가 0 이 되었나? 무엇이 '디스코' 같지 않게 되었나?
- 바꿔 보기: 2. 록을 누르고 배열을 읽는다. kick 은 몇 번째 칸에서 치나? open 줄은 왜 모두 0 인가? 디스코의 open 줄과 비교한다.
- 바꿔 보기: 135행 `60 / 109 / 4` 의 `109` 를 `130` 으로 바꾸고 새로고침 → ▶ 재생. 무엇이 빨라지나? 한 칸은 몇 초가 되나(ex07 의 식)?
- 흔한 실수: 재생 중에 ▶ 재생을 또 누른다. 아무 일도 없다(129행 `if (timer) return;`). 숫자를 바꿨으면 ■ 정지 → 저장 → 새로고침 → ▶ 재생 순서로 듣는다.

### 5. (선택) 나머지 비교 파일 — ex01 · ex02 · ex05 · ex06 · ex07 · ex09

덱에서 듣고, 바꿔 보고 싶은 파일만 `ex/` 에 저장한다. 파일마다 바꿔 볼 값은 [예제 설명](examples/README.md#비교-파일) 표에 있다.

- ex01: 33행의 `220` 을 `440` 으로 바꾼다. 그림의 물결과 소리는 어떻게 달라지나? 네 단추의 높이는 서로 같은가?
- ex02: 30행의 `440` 을 `432` 로 바꾼다. 단추 숫자가 모두 바뀌는 이유는 무엇인가? 키보드 A S D F G H J K 로 '도레미파솔라시도' 를 친다. 한글 입력 상태면 왜 소리가 안 나나(56행)?
- ex05: 음량을 줄이고 5번(Q 15)을 누른다. 62행의 `15` 를 `5` 로 바꾸면? 65행의 `+ 2` 를 `+ 0.5` 로 바꾸면 쓸기가 어떻게 되나?
- ex06: 78행 `kick(150, 45)` 의 `45` 를 `100` 으로 바꾸면 '퍽' 이 어떻게 되나? 40행의 `0.12` 를 `0.4` 로 바꾸면?
- ex07: "바쁘게" 를 켜고 1번 · 2번을 번갈아 누른다. 간격의 가장 짧은 값과 가장 긴 값은? BPM 칸을 `130` 으로 바꾸면 한 칸은 몇 초인가?
- ex09: `ex09_fetch_song.html` 과 `ex09_song.json` 을 둘 다 `ex/` 에 둔다. `http://localhost:8000/ex/ex09_fetch_song.html` 과 두 번 눌러 연 `file:///…` 을 비교한다. JSON 의 B 구간에 `{ "bar": 3, "chord": "E7" }` 를 더하면 표 6번과 펼친 마디는 어떻게 되나? 앞 마디 `}` 뒤에 무엇을 붙여야 하나?

### 6. 내 노래 — my_song.json (코드 진행만)

[따라하기 4단계](walkthrough.md#4-my_songjson-고치기)에 고친 예와 전문이 있다. 고친 뒤에는 저장 → 새로고침 → 곡 선택에서 **my_song.json** 을 다시 고른다(새로고침하면 only_you.json 으로 돌아간다).

쓸 수 있는 코드는 근음 `A`~`G` 하나, 그 뒤에 (있으면) `#` 이나 `b`, 그 뒤에 종류 하나다.

| 종류 | C 로 쓰면 | 근음에서 몇 반음 위 |
|---|---|---|
| 장3화음 | `C` | 0 · 4 · 7 |
| 단3화음 | `Cm` | 0 · 3 · 7 |
| 7 | `C7` | 0 · 4 · 7 · 10 |
| m7 | `Cm7` | 0 · 3 · 7 · 10 |
| maj7 | `Cmaj7` | 0 · 4 · 7 · 11 |
| dim | `Cdim` | 0 · 3 · 6 |
| sus2 | `Csus2` | 0 · 2 · 7 |
| sus4 | `Csus4` | 0 · 5 · 7 |

`#` 은 반음 위(`F#m`), `b` 은 반음 아래(`Bb7`)다. 이 표에 없는 종류(`Am9`, `C6` 등)는 쓸 수 없다.

- 바꿔 보기: `title` 과 `artist` 를 바꾼다. 머리 줄의 어느 자리가 바뀌나? `key` 를 바꾸면 소리도 바뀌나, 글자만 바뀌나?
- 바꿔 보기: `bpm` 을 `100` 으로, 이어서 `200` 으로 바꾼다. 머리 줄의 BPM 과 슬라이더 옆 숫자는 같은가? 다르다면 왜인가(`index.html` 31행의 `min` · `max`)?
- 바꿔 보기: B 구간 `progression` 끝에 `{ "bar": 5, "chord": "E7" }` 를 더한다. 앞 줄 끝에 무엇을 붙여야 하나? 악보 칸 수와 위치 줄의 `/8마디` 는 어떻게 바뀌나? `bars_count` 를 고치지 않아도 되나?
- 바꿔 보기: 구간을 하나 더 만든다(`"section": "C"`). `sections` 배열의 어디에, 무엇으로 감싸 넣어야 하나?
- 흔한 실수: 표에 없는 종류를 쓴다. 머리 줄이 `곡 없음`, 아래 빨간 글자 `불러오지 못했습니다: 모르는 코드 종류입니다: Am9 — 쓸 수 있는 모양: C Cm C7 Cm7 Cmaj7 Cdim Csus2 Csus4 (C 자리에 A~G, 뒤에 # 이나 b)`. 악보 칸이 모두 지워지고 ▶ 재생을 눌러도 소리가 나지 않는다. Console 에는 빨간 줄이 없다. 화면 문구를 읽는다. 곡 선택에서 only_you.json 을 고르면 다시 재생된다.
- 흔한 실수: 쉼표를 빠뜨린다. `불러오지 못했습니다: Expected ',' or '}' after property value in JSON at position 44 (line 4 column 5)` 처럼 나온다. 쉼표는 표시된 줄의 **바로 위 줄 끝**에 빠져 있다(이 예는 3행 `"title": "내 노래"` 뒤).

### 7. 리듬 배열 — PATTERNS.disco 한 줄

[따라하기 5단계](walkthrough.md#5-리듬-배열-고치기)를 본다. `index.js` 6~25행이 리듬이다. 줄마다 16칸, 1 이면 그 칸에서 친다(ex08).

- 바꿔 보기: 8행 kick 을 `[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]` 으로 바꾼다. 무엇이 사라지나? ex08 에서 2 · 4박 킥을 끈 것과 같은가?
- 바꿔 보기: 12행 bass 의 `2` 를 모두 `1` 로 바꾼다. 무엇이 달라지나(5행 주석)?
- 바꿔 보기: 13행 chord 를 `[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]` 으로 바꾼다. 코드가 엇박에서 박 위로 옮겨 가면 느낌이 어떻게 바뀌나?
- 바꿔 보기: 화면의 리듬을 록으로 바꿔 듣는다. `PATTERNS.rock`(16~24행)의 kick · hat 은 디스코와 어디가 다른가?
- 흔한 실수: 숫자 사이 쉼표가 빠졌다. 머리 줄이 `곡을 불러오는 중…` 에서 멈추고 Console 에 `Uncaught SyntaxError: Unexpected number` 와 `index.js:8` 이 뜬다. 문법 오류가 있으면 `index.js` 전체가 실행되지 않는다.
- 흔한 실수: 숫자가 15개다. ▶ 재생을 누르면 소리 없이 아래에 `리듬 'disco' 의 kick 줄이 16칸이 아닙니다` 가 뜬다. 재생 중에 리듬을 그 패턴으로 바꾸면 멈추고 같은 문구가 뜬다. 칸 수는 16개를 지킨다.

### 8. 소리 하나 — playTone 에 넘기는 값

[따라하기 6단계](walkthrough.md#6-소리-하나-고치기)를 본다. 소리 부품은 `synth.js` 의 `playTone` 하나다. `index.js` 의 `scheduleStep` 이 층마다 다른 값을 넘긴다.

| 바꿀 곳 | 지금 값 | 바꿔 볼 값 | 어느 ex |
|---|---|---|---|
| `index.js` 78행 코드 층 `release` | `0.15` | `0.6` | ex03 3번 |
| `index.js` 78행 코드 층 `attack` | `0.005` | `0.1` | ex03 4번 |
| `index.js` 74행 베이스 `type` | `'square'` | `'sawtooth'` · `'triangle'` | ex01 |
| `index.js` 74행 베이스 `cutoff` | `700` | `300` · `2000` | ex05 |
| `synth.js` 75 · 76행 킥 높이 | `150` → `45` | `200` → `40` | ex06 2번 |
| `synth.js` 107행 하이햇 길이(열림 : 닫힘) | `0.28 : 0.05` | `0.4 : 0.03` | ex06 5 · 6번 |

- 바꿔 보기: 코드 층 `release` 를 `0.6` 으로 바꾼다. 짧게 끊기던 코드가 어떻게 되나? 109 BPM 에서 코드는 0.55초마다 친다. 0.6초에 걸쳐 사라지면 다음 코드와 어떻게 되나?
- 바꿔 보기: 베이스 `cutoff` 를 `300` 으로, 이어서 `2000` 으로 바꾼다. ex05 의 어느 단추와 닮았나?
- 바꿔 보기: 킥을 `200` → `40` 으로 바꾼다. '퍽' 의 무엇이 달라지나?
- 흔한 실수: 파형 이름을 틀리게 쓴다(`'sqare'`). 오류로 멈추지 않고 Console 에 노란 줄 `The provided value 'sqare' is not a valid enum value of type OscillatorType.` 이 계속 찍힌다. 소리는 sine 으로 난다. `'sine'` · `'square'` · `'sawtooth'` · `'triangle'` 넷 중 하나만 쓴다.
- 흔한 실수: `volume` 을 크게 올린다. 다른 층이 묻히고 소리가 찢어질 수 있다. 0.05 씩 바꾸고, 크게 듣고 싶으면 다른 층의 체크 상자를 끈다.

### 9. 새 저장소 web-synth 에 올리기

서버가 떠 있는 터미널은 **Ctrl+C** 로 멈추거나, **Terminal › New Terminal** 로 새 터미널을 연다.
GitHub 에서 **New repository** → 이름 `web-synth`, **Public**, README 는 추가하지 않는다. VS Code 터미널(현재 폴더 `web-synth`)에서 2주차에 배운 순서 그대로 친다.

```bash
git init
git add .
git commit -m "특강 웹 신시사이저"
git branch -M main
git remote add origin https://github.com/student01/web-synth.git
git push -u origin main
```

저장소 **Settings › Pages › Branch: main, /(root) › Save** → 1~3분 뒤 `https://student01.github.io/web-synth/` 을 연다. 곡 선택 my_song.json → ▶ 재생 → 아래 **제출** 조건대로 캡처한다. 공용 PC면 자격 증명을 지우고 나간다.
올린 뒤에 다시 고쳤으면 `git add .` → `git commit -m "…"` → `git push` 로 한 번 더 올린다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push 한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 **Ctrl+F5**(macOS 는 ⌘+Shift+R)로 새로고침하고, 그래도 안 보이면 localhost 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 것으로 인정한다 |
| push 가 거부되거나 로그인 창이 안 뜬다 | [2주차 막혔을 때](../../weeks/week02_github_pages/lab.md#막혔을-때) 표를 본다 |
| 소리가 안 난다 | ① 이어폰이 꽂혀 있는지, PC 음량 · 음소거를 본다 ② Chrome 탭이 음소거인지 본다(탭을 오른쪽 클릭 › **사이트 음소거 해제**) ③ ▶ 재생(비교 파일은 단추)을 눌렀는지 본다. 브라우저는 누르기 전에는 소리를 내 주지 않는다 ④ 연주기의 층 체크 상자가 모두 꺼져 있지 않은지 본다 |
| 머리 줄이 `곡 없음`, 아래에 `주소가 file:// 입니다. 연주기는 서버로 엽니다: 이 폴더에서 node server.mjs 를 띄우고 http://localhost:8000/ 을 여세요.` 가 뜨고 16칸 표시등도 악보도 없다. Console 에 `Access to script at 'file:///…/index.js' from origin 'null' has been blocked by CORS policy: Cross origin requests are only supported for protocol schemes: …` 와 `Failed to load resource: net::ERR_FAILED` | 주소가 `file:///…` 다(파일을 두 번 눌러 열었다). `type="module"` 의 `import` 와 `fetch` 는 서버나 공개 주소에서만 돈다. 화면 안내대로 `node server.mjs` 로 띄우고 `http://localhost:8000/` 으로 연다 |
| `곡을 불러오는 중…` 에서 멈췄다. Console 에 틀린 파일 이름(예: `synt.js`)과 `404 (Not Found)` 가 적힌 빨간 줄(`Failed to load resource: the server responded with a status of 404 (Not Found)`), 터미널에 `404 GET /synt.js` | `index.js` 2행 `from './synth.js'` 의 이름과 실제 파일 이름이 다르다. 대소문자와 확장자(`synth.js.txt`)까지 본다 |
| `곡을 불러오는 중…` 에서 멈췄다. Console 에 `Uncaught SyntaxError: Unexpected number`, 오른쪽에 `index.js:8` | `PATTERNS` 배열에서 숫자 사이 쉼표가 빠졌다. 표시된 줄에서 숫자 사이를 본다. 문법 오류가 있으면 `index.js` 전체가 실행되지 않는다 |
| 머리 줄이 `곡 없음`, 아래 빨간 글자 `불러오지 못했습니다: 모르는 코드 종류입니다: Am9 — 쓸 수 있는 모양: C Cm C7 Cm7 Cmaj7 Cdim Csus2 Csus4 (C 자리에 A~G, 뒤에 # 이나 b)` | `my_song.json` 에 연주기가 모르는 코드 종류가 있다. Console 에는 빨간 줄이 없다. 악보 칸이 지워지고 ▶ 재생을 눌러도 소리가 나지 않는다(다른 곡을 고르면 다시 재생된다). [6번](#6-내-노래--my_songjson-코드-진행만) 표의 모양으로 고치고 저장 → 새로고침 → 곡 선택 my_song.json 을 다시 고른다 |
| `곡 없음`, `불러오지 못했습니다: Expected ',' or '}' after property value in JSON at position 44 (line 4 column 5)` | JSON 의 쉼표가 빠졌다. 표시된 줄(line 4)의 **바로 위 줄 끝**을 본다. 이 예는 3행 `"title": "내 노래"` 뒤 쉼표가 없다 |
| `곡 없음`, `불러오지 못했습니다: Unexpected token ']', …` 로 시작해 `is not valid JSON` 으로 끝나는 여러 줄 | 배열의 마지막 항목 뒤에 쉼표가 남았다(`{ "bar": 4, "chord": "Am7" },` 다음 줄이 `]`). 마지막 항목 뒤 쉼표를 지운다 |
| `곡 없음`, `불러오지 못했습니다: Unexpected token ''', …` | 작은따옴표를 썼다(`'G'`). JSON 은 큰따옴표(`"G"`)만 쓴다 |
| 머리 줄은 `200 BPM` 인데 슬라이더 옆 숫자는 `140` 이다 | 연주기의 BPM 슬라이더는 80~140 이다. 그 밖의 값은 슬라이더 끝값으로 친다. `bpm` 을 80~140 안으로 바꾼다 |
| 곡을 고쳤는데 머리 줄이 그대로 `Only You — …` 다 | 새로고침하면 곡 선택이 only_you.json 으로 돌아간다. 곡 선택에서 my_song.json 을 다시 고른다. 그래도 그대로면 저장했는지(VS Code 탭의 ● 표시) 본다 |
| Console 에 노란 줄 `The provided value 'sqare' is not a valid enum value of type OscillatorType.` | `type` 에 쓴 파형 이름이 틀렸다. `'sine'` · `'square'` · `'sawtooth'` · `'triangle'` 넷 중 하나만 된다. 틀리면 오류 없이 sine 으로 난다 |
| ▶ 재생을 눌렀는데 소리가 없고 아래에 `리듬 'disco' 의 arp 줄이 16칸이 아닙니다` 처럼 뜬다. 재생 중에 리듬을 바꿨다면 멈추고 같은 문구가 뜬다 | Console 에는 빨간 줄이 없다. 문구에 적힌 리듬의 그 줄이 숫자 16개가 아니거나 빠졌다(새로 만든 `PATTERNS.funk` 에 줄을 빼먹었을 때도 `리듬 'funk' 의 arp 줄이 16칸이 아닙니다` 로 뜬다). kick · snare · hat · open · bass · chord · arp 일곱 줄을 모두 두고 줄마다 16개를 센다. 다른 리듬을 고르면 그 리듬으로 재생된다 |
| 재생은 되는데 소리가 찢어진다 | `volume` 을 키웠다. 되돌린다. 크게 듣고 싶으면 다른 층을 끈다. 연주기는 압축기로 소리를 눌러 주지만 모든 층을 크게 하면 감당하지 못한다 |
| 박자가 흔들리거나 소리가 끊긴다 | PC 가 바쁘다. 다른 탭 · 창(특히 영상)을 닫는다. 연주기는 0.1초 앞까지만 예약하므로 브라우저가 그보다 오래 멈추면 소리가 밀린다(ex07) |
| 공개 주소가 404 다 | ① 저장소 이름이 `web-synth` 이고 **Settings › Pages** 가 켜져 있는지 ② 파일 이름이 교재와 같은지(`Index.html` · `index.html` 은 다른 이름) ③ GitHub 저장소 화면에 여섯 파일이 올라가 있는지 본다 |
| `'node' is not recognized` / `command not found: node` | Node.js 가 없거나 설치 뒤 터미널을 새로 열지 않았다. 수업 중에는 push 한 뒤 공개 주소에서 확인한다 |
| `8000 번 포트를 이미 다른 프로그램이 쓰고 있습니다` | 다른 터미널에 서버가 떠 있다. 그 터미널에서 Ctrl+C 하거나 `node server.mjs . 8001` 로 띄우고 `http://localhost:8001/` 을 연다. 증상별 전체 목록은 [서버 사용 안내](../../tools/static-server/README.md#막혔을-때)에 있다 |

한 번에 한 곳만 고치고 새로고침한다. JSON 오류와 리듬 칸 수 오류는 화면 문구에, 그 밖의 코드 오류는 Console 에 나온다. 해결되지 않으면 화면과 Console 을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://student01.github.io/web-synth/`(본인 아이디)를 열고 곡 선택에서 **my_song.json** 을 고른 뒤 ▶ 재생한다. 재생 중에 한 화면을 캡처한다.

- 머리 줄에 내가 고친 제목과 BPM 이 보인다(예: `금요일 밤 — student01 · Am · 4/4 · 124 BPM`).
- 악보에서 지금 마디 칸이 분홍색으로 강조되고, 표시등 옆 위치 줄(예: `A · 2/12마디 · F`)이 보인다.
- **주소창이 함께 보이게** 찍는다. 소리는 캡처되지 않으므로 화면 조건만 본다.

캡처에 실명 · 학번 · 실제 이메일이 보이지 않게 한다. 선택 특강이므로 주차별 실습 점수에는 넣지 않는다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 아르페지오: 체크 상자 `아르페지오` 를 켜고 듣는다. `PATTERNS.disco.arp`(14행)의 1 을 몇 개 0 으로 바꾸면 내 노래에 어울리나?
- 리듬 하나 더: `PATTERNS` 에 `funk: { … }` 를 더하고, `index.html` 의 리듬 선택(26~29행)에 `<option value="funk">펑크</option>` 한 줄을 더한다. 줄 일곱 개(kick · snare · hat · open · bass · chord · arp)를 모두 둔다. `rock` 을 본보기로 하고 kick · snare · hat 부터 바꾼다.
- 키보드로 연주: 연주기 창과 ex02 창을 나란히 띄운다. 연주기를 재생해 둔 채 ex02 창을 누르고 A S D F G H J K 로 친다. 멜로디는 **직접 만든 것만** 친다.
- 곡 하나 더: `song2.json` 을 만들고 `index.html` 의 곡 선택(20~23행)에 `<option value="song2.json">song2.json</option>` 을 더한다. 코드 진행만 담는다.

추가 과제는 선택 사항이며 채점하지 않는다.
