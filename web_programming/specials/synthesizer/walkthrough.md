# 특강 따라하기 — 디스코 연주기

처음에는 그대로 따라 하고, 결과가 나오면 내 노래와 내 소리로 바꾼다.
각 단계의 **예상 결과**가 화면에 보이면 다음 단계로 넘어간다. **이어폰을 끼고 음량을 작게 시작한다.**

`student01` 은 연습용 아이디다. 명령과 주소의 `student01` 은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code 의 터미널(**Terminal › New Terminal**, Windows 는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

비교 파일 9개와 연주기는 [교재 저장소의 examples 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/synthesizer/examples)에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다. 연주기 여섯 파일의 전문은 맨 아래 [연주기 전문](#연주기-전문)에 있다.

## 1. web-synth 폴더와 서버

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-synth` 를 만들고 VS Code **File › Open Folder** 로 연다.

[server.mjs](../../tools/static-server/server.mjs) 를 연다 → 오른쪽 위 **Raw** → **Ctrl+S**(macOS 는 ⌘+S)로 `web-synth` 에 `server.mjs` 이름으로 저장한다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.
비교 파일을 둘 `ex` 폴더도 만든다. VS Code 탐색기에서 **New Folder** 를 눌러도 되고, 명령으로 만들어도 된다. 현재 폴더: `web-synth`

```bash
mkdir ex
```

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-synth/
  ex/          ← 아직 비어 있다
  server.mjs
```

- 저장한 이름이 `server.mjs.txt` 처럼 `.txt` 로 끝나면 이름을 고친다. 이름은 VS Code 탐색기에서 확인한다(Windows 파일 탐색기는 기본 설정에서 확장자를 숨긴다).
- `node -v` 를 쳐서 `v18` 이상이 나오면 된다. 없으면 [Node.js LTS](https://nodejs.org/ko) 를 설치하고 VS Code 를 다시 연다.

## 2. 연주기 여섯 파일 받기와 재생

[examples/build 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/synthesizer/examples/build)의 여섯 파일을 1단계와 같은 **Raw** → 저장으로 `web-synth` 맨 위(`server.mjs` 옆)에 저장한다. 파일 이름은 교재와 **같게** 둔다.

| 파일 | 하는 일 |
|---|---|
| [index.html](examples/build/index.html) | 화면: 머리 줄(제목 · 곡 정보), 패널 두 개(재생 · 정지 · 곡 · 리듬 · BPM / 층 체크 상자 · 코드 파형 · 필터), 16칸 표시등과 위치 줄, 악보. 끝에서 `index.js` 의 `main` 을 부른다 |
| [main.css](examples/build/main.css) | 어두운 디스코 색. 패널은 flex(4주차), 지금 칸은 노랑, 지금 마디 `.bar.now` 는 분홍 |
| [index.js](examples/build/index.js) | 연주: 리듬 배열 `PATTERNS`, 한 칸의 소리 예약 `scheduleStep`, 오디오 시계 예약 `tick`, 곡 불러오기 `loadSong` |
| [synth.js](examples/build/synth.js) | 소리 부품: `midiToFreq` · `chordToMidis` · `playTone` · `playKick` · `playSnare` · `playHat`. 화면은 모른다 |
| [only_you.json](examples/build/only_you.json) | 곡 데이터(4구간 28마디의 코드 진행만). 손대지 않는다 |
| [my_song.json](examples/build/my_song.json) | 내가 고칠 곡 데이터(2구간 8마디) |

그다음 서버를 띄운다. 현재 폴더: `web-synth`

```bash
node server.mjs
```

**예상 결과** — 터미널에 두 줄이 찍히고 서버가 떠 있다. 폴더 줄은 PC 마다 다르다.

```text
폴더: C:\Users\student\web-synth
주소: http://localhost:8000/   (멈추기: Ctrl+C)
```

Chrome 주소창에 `http://localhost:8000/` 을 치고 **F12 › Console** 을 연다.

**예상 결과** — 머리 줄이 `Only You — Savage · Am · 4/4 · 109 BPM` 이다. 16칸 표시등 옆에 `정지`, 아래 악보에 구간 네 줄(`Intro / Synth Lead` · `Verse` · `Pre-Chorus` · `Chorus`)과 마디 28칸이 보인다. 터미널에는 요청이 한 줄씩 늘었다.

```text
200 GET /
200 GET /main.css
200 GET /index.js
200 GET /synth.js
200 GET /only_you.json
404 GET /favicon.ico
```

이제 **▶ 재생**을 누른다.

**예상 결과** — 소리가 나고 노란 표시등이 16칸을 돈다. 지금 마디 칸이 분홍색이 된다. 4.5초쯤 뒤 위치 줄은 `Intro / Synth Lead · 2/28마디 · Dm` 이다(109 BPM 에서 한 마디는 2.2초). **■ 정지**를 누르면 위치 줄이 `정지` 로 돌아가고 강조가 모두 꺼진다.

- `index.html` 이 `main.css` 와 `index.js` 를, `index.js` 가 2행 `import` 로 `synth.js` 를, `loadSong` 이 `fetch` 로 JSON 을 따로 요청한다. 그래서 터미널 줄이 여러 개다. 가운데 줄들의 순서는 열 때마다 바뀔 수 있다.
- 곡 선택을 my_song.json 으로 바꾸면 터미널에 `200 GET /my_song.json` 이 늘고, 머리 줄이 `내 노래 — student01 · C · 4/4 · 118 BPM` 이 된다. ▶ 재생 2.5초쯤 뒤 위치 줄은 `A · 2/8마디 · G` 다.
- 체크 상자로 층(킥 · 스네어 · 하이햇 · 베이스 · 코드 · 아르페지오)을 켜고 끈다. 아르페지오는 처음에 꺼져 있다. 코드 파형은 코드 층의 파형을, 필터는 코드 층과 아르페지오의 밝기를 바꾼다(ex01 · ex05). 아르페지오의 파형은 square 로 정해져 있다(`index.js` 83행).
- `index.html` 을 두 번 눌러 열면(`file:///…`) 머리 줄이 `곡 없음`, 아래에 `주소가 file:// 입니다. 연주기는 서버로 엽니다: 이 폴더에서 node server.mjs 를 띄우고 http://localhost:8000/ 을 여세요.` 가 뜨고 표시등도 악보도 없다. Console 에는 `Access to script at 'file:///…/index.js' from origin 'null' has been blocked by CORS policy: …` 가 뜬다. `type="module"` 의 `import` 와 `fetch` 는 서버나 공개 주소에서만 돈다.
- `favicon.ico` 는 브라우저가 탭 아이콘을 찾으려고 스스로 보낸 요청이다. 404 여도 괜찮다. Console 에 이 404 한 줄이 보여도 괜찮다.

## 3. 비교 파일 받는 법

비교 파일은 **듣기만 할 것**과 **고쳐 볼 것**을 나눈다.

1. **덱에서 바로 듣기** — 교재 사이트 덱(https://gbox3d.github.io/teaching_repo/webprg/decks/synthesizer/index.html)의 ex 장에서 파일 링크를 누르면 그 파일이 열린다. 받지 않고 바로 단추를 눌러 듣는다.
2. **고쳐 볼 것만 Raw 로 저장** — [examples 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/synthesizer/examples)에서 파일을 누르고 **Raw** → 저장으로 `web-synth/ex/` 에 넣는다. 필수는 ex03 · ex04 · ex08 이다.

| 파일 | 비교하는 것 |
|---|---|
| [ex03_envelope.html](examples/ex03_envelope.html) | 켰다 끄기만 / 짧게 / 길게 / 천천히 커지기 / 2번을 exponential 로 |
| [ex04_chord.html](examples/ex04_chord.html) | 곡의 코드 다섯 개 / 장 vs 단 |
| [ex08_pattern.html](examples/ex08_pattern.html) | 디스코 / 록 / 비우기 — 16칸 배열 |

저장한 파일은 서버로 연다. 주소에 `ex/` 를 붙인다.

```text
http://localhost:8000/ex/ex03_envelope.html
```

**예상 결과** — 제목 `ex03 엔벨로프: 소리 크기가 시간에 따라 어떻게 변하나` 와 형제 다섯 줄의 표가 보인다. 2번 재생을 누르면 짧게 뜯는 소리가 나고 아래 그림에 크기 변화가 그려진다.

- 실험은 늘 같은 순서다. VS Code 에서 고치고 **저장**(Ctrl+S, macOS 는 ⌘+S) → 브라우저 **새로고침**(F5, macOS 는 ⌘+R) → 단추를 다시 누른다. 저장을 안 하면 소리가 안 바뀐다. VS Code 탭 제목의 ● 표시는 저장 안 됨이다.
- ex09 는 `ex09_fetch_song.html` 과 `ex09_song.json` 을 **둘 다** 같은 `ex/` 폴더에 둔다. HTML 이 같은 폴더에서 그 이름을 `fetch` 하기 때문이다. 두 번 눌러 연 `file:///…` 에서는 `불러오지 못했다: Failed to fetch — …` 가 나오는 것까지 비교한다.
- ex01~ex08 은 `fetch` 도 `import` 도 쓰지 않는다. 두 번 눌러 열어도 소리가 난다.
- 값을 원래대로 못 돌리겠으면 그 파일을 다시 **Raw** 로 받아 덮어쓴다.

## 4. my_song.json 고치기

`my_song.json` 을 VS Code 로 연다. 구조는 ex09 의 `ex09_song.json` 과 같다. 처음 모양은 아래 [my_song.json 전문](#my_songjson)에 있다.

```text
{
  "track_info": { 제목 · 만든 사람 · 조 · 박자표 · bpm },   ← 객체 하나: 머리 줄에 보인다
  "sections": [                                            ← 배열: 구간이 차례로
    { "section": "A", "bars_count": 4, "progression": [    ← 구간 하나 = 객체
        { "bar": 1, "chord": "C" }, …                      ← 마디 하나 = 객체
    ] },
    …
  ]
}
```

연주기가 읽는 값은 이것뿐이다(`index.js` 145~183행 `loadSong`).

| 값 | 어디에 쓰이나 |
|---|---|
| `title` · `artist` · `key` · `time_signature` · `bpm` | 머리 줄 `제목 — 만든 사람 · 조 · 박자표 · bpm BPM` |
| `bpm` | BPM 슬라이더도 이 값으로 맞춘다. 슬라이더는 80~140 이라 그 밖의 값은 끝값이 된다 |
| `section` | 악보 줄 이름, 위치 줄의 첫 칸 |
| `chord` | 악보 칸의 글자와 소리(`chordToMidis`) |

`bars_count` 와 `bar` 는 사람이 읽기 좋게 적어 둔 숫자다. 연주기는 `progression` 배열의 길이로 마디를 센다. `time_signature` 도 머리 줄에 보여 주기만 한다. 연주기는 늘 한 마디를 16칸(4/4)으로 친다.

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

예: `F#dim`(파#에서 시작하는 dim), `Bb7`(시♭에서 시작하는 7), `Esus4`. 표에 없는 종류(`Am9`, `C6` 등)는 오류 문구가 나온다.

아래는 고친 예다. 제목 · 조 · bpm 을 바꾸고, B 구간의 코드를 바꾸고, C 구간을 하나 더했다. **코드 진행만** 바꾼다. 다른 노래의 멜로디 · 가사는 넣지 않는다.

```json
{
  "track_info": {
    "title": "금요일 밤",
    "artist": "student01",
    "key": "Am",
    "time_signature": "4/4",
    "bpm": 124
  },
  "sections": [
    {
      "section": "A",
      "bars_count": 4,
      "progression": [
        { "bar": 1, "chord": "Am" },
        { "bar": 2, "chord": "F" },
        { "bar": 3, "chord": "C" },
        { "bar": 4, "chord": "G" }
      ]
    },
    {
      "section": "B",
      "bars_count": 4,
      "progression": [
        { "bar": 1, "chord": "Dm7" },
        { "bar": 2, "chord": "G7" },
        { "bar": 3, "chord": "Cmaj7" },
        { "bar": 4, "chord": "E7" }
      ]
    },
    {
      "section": "C",
      "bars_count": 4,
      "progression": [
        { "bar": 1, "chord": "F" },
        { "bar": 2, "chord": "F#dim" },
        { "bar": 3, "chord": "G" },
        { "bar": 4, "chord": "Esus4" }
      ]
    }
  ]
}
```

저장 → 브라우저 새로고침 → 곡 선택에서 **my_song.json** 을 고른다. 새로고침하면 곡 선택이 only_you.json 으로 돌아가므로 고칠 때마다 다시 고른다.

**예상 결과** — 머리 줄이 `금요일 밤 — student01 · Am · 4/4 · 124 BPM`, 슬라이더 옆 숫자가 `124` 다. 악보는 `A` · `B` · `C` 세 줄, 마디 12칸(`Am F C G` / `Dm7 G7 Cmaj7 E7` / `F F#dim G Esus4`)이다. ▶ 재생 2.5초쯤 뒤 위치 줄은 `A · 2/12마디 · F` 다.

- 구간을 더할 때는 앞 구간의 `}` 뒤에 쉼표를 붙이고, 새 구간을 `{ … }` 로 감싸 `sections` 배열의 `]` 앞에 넣는다.
- 마디를 더할 때도 앞 마디 `}` 뒤에 쉼표를 붙인다. 배열의 **마지막 항목 뒤에는 쉼표가 없다**.
- 화면 아래 빨간 글자가 나오면 그 문구를 [실습지의 막혔을 때](lab.md#막혔을-때)에서 찾는다. 이때 Console 에는 빨간 줄이 없다. `loadSong` 이 던진 오류를 `showError`(`index.js` 215행)가 받아 화면에 적기 때문이다.
- 오류 문구가 뜨면 머리 줄이 `곡 없음` 이 되고 악보 칸이 모두 지워진다. ▶ 재생을 눌러도 소리가 나지 않는다. 고치고 저장 → 새로고침 → my_song.json 을 다시 고른 뒤 재생한다. 그동안 다른 곡(only_you.json)을 고르면 그 곡은 재생된다.

## 5. 리듬 배열 고치기

`index.js` 6~25행이 리듬이다. 줄마다 16칸, 1 이면 그 칸에서 친다(ex08). `bass` 는 1 = 낮은 근음, 2 = 한 옥타브 위 근음이다(5행 주석). 화면의 리듬 선택이 디스코면 `PATTERNS.disco`, 록이면 `PATTERNS.rock` 을 쓴다.

```js
    disco: {
        kick:  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],   // 박마다 킥(four on the floor)
        snare: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],   // 2박·4박
        hat:   [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        open:  [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],   // 엇박에 열린 하이햇 — 디스코의 표시
        bass:  [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0],
        chord: [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        arp:   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    },
```

고친 예: 8행 kick 을 박마다(1 · 5 · 9 · 13번째 칸)에서 1 · 9번째 칸(1박 · 3박)으로 줄인다. 주석도 바뀐 뜻에 맞게 고친다.

```js
        kick:  [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],   // 1 · 3박에만 킥
```

저장 → 새로고침 → ▶ 재생.

**예상 결과** — 소리가 나고 위치 줄이 움직이며, Console 에 빨간 줄이 없다. 박마다 울리던 킥이 1 · 3박에만 남는다. 디스코의 표시(four on the floor)가 빠진 소리를 듣는다. 확인했으면 되돌리거나 다른 줄을 내 것으로 바꾼다.

- 한 줄은 숫자 **16개**, 숫자 사이는 쉼표다. 쉼표가 빠지면 `index.js` 전체가 실행되지 않는다. 머리 줄이 `곡을 불러오는 중…` 에서 멈추고 Console 에 `Uncaught SyntaxError: Unexpected number` 와 `index.js:8` 이 뜬다.
- 숫자가 15개면 ▶ 재생을 눌러도 소리가 나지 않고 아래에 `리듬 'disco' 의 kick 줄이 16칸이 아닙니다` 가 뜬다. 재생 중에 리듬을 그 패턴으로 바꾸면 멈추고 같은 문구가 뜬다. 치기 전에 `checkPattern`(50~57행)이 일곱 줄(27행 `ROWS`)이 모두 16칸인지 확인하기 때문이다.
- `scheduleStep`(60~86행)은 줄마다 "체크 상자가 켜져 있고 이 칸이 1 이면" 소리를 예약한다. 체크 상자를 끄면 배열이 1 이어도 치지 않는다.

## 6. 소리 하나 고치기

소리 부품은 `synth.js` 의 `playTone` 하나다. 오실레이터(파형) → lowpass 필터 → 게인(엔벨로프) 순서로 잇는다(ex01 · ex05 · ex03). `index.js` 의 `scheduleStep` 이 층마다 다른 값을 객체로 넘긴다. 코드 층은 78행이다.

```js
            playTone(ctx, out, { freq: midiToFreq(midi), time: time, type: wave, cutoff: cutoff, attack: 0.005, length: len, release: 0.15, volume: 0.24 / bar.midis.length });
```

| 바꿀 곳 | 지금 값 | 바꿔 볼 값 | 어느 ex |
|---|---|---|---|
| `index.js` 78행 코드 층 `release` | `0.15` | `0.6` | ex03 3번 |
| `index.js` 78행 코드 층 `attack` | `0.005` | `0.1` | ex03 4번 |
| `index.js` 74행 베이스 `type` | `'square'` | `'sawtooth'` · `'triangle'` | ex01 |
| `index.js` 74행 베이스 `cutoff` | `700` | `300` · `2000` | ex05 |
| `synth.js` 75 · 76행 킥 높이 | `150` → `45` | `200` → `40` | ex06 2번 |
| `synth.js` 107행 하이햇 길이(열림 : 닫힘) | `0.28 : 0.05` | `0.4 : 0.03` | ex06 5 · 6번 |

고친 예: 78행 코드 층의 `release: 0.15` 를 `release: 0.6` 으로 바꾼다. 저장 → 새로고침 → ▶ 재생.

**예상 결과** — 소리가 나고 Console 에 빨간 줄 · 노란 줄이 없다. 짧게 끊기던 코드가 길게 깔린다(ex03 3번). 109 BPM 에서 코드는 0.55초마다 치는데, 한 번 친 코드가 0.74초(0.005 + 0.138 + 0.6) 동안 울려 다음 코드와 겹친다.

- 파형 이름이 틀리면(`'sqare'`) 오류로 멈추지 않는다. Console 에 노란 줄 `The provided value 'sqare' is not a valid enum value of type OscillatorType.` 이 계속 찍히고 소리는 sine 으로 난다.
- `volume` 은 조금씩(0.05 정도) 바꾼다. 크게 올리면 다른 층이 묻히고 소리가 찢어질 수 있다. 크게 듣고 싶으면 다른 층의 체크 상자를 끈다.
- 엔벨로프 숫자를 고칠 때 exponential 의 목표값에는 0 을 쓰지 않는다. `0.0001` 처럼 아주 작은 수를 쓴다(ex03, `synth.js` 61 · 64행).
- 화면의 `코드 파형` 과 `필터` 는 78행의 `wave` · `cutoff` 로 들어간다. 코드를 고치기 전에 화면에서 먼저 바꿔 들어 본다.

## 7. web-synth 저장소 만들어 올리기

실습 50–60분에 한다. 연주기를 내 것으로 바꾸고 localhost 에서 확인했으면 올린다.

서버가 떠 있는 터미널에서 **Ctrl+C** 로 서버를 멈춘다(또는 **Terminal › New Terminal** 로 새 터미널을 연다).
GitHub 에서 **New repository** 를 누르고 이름 `web-synth`, **Public** 으로 만든다. README 는 추가하지 않는다.
터미널에서 2주차에 배운 순서 그대로 친다. 현재 폴더: `web-synth`

```bash
git init
git add .
git commit -m "특강 웹 신시사이저"
git branch -M main
git remote add origin https://github.com/student01/web-synth.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save** 를 누른다.

**예상 결과** — GitHub 저장소 화면을 새로고침하면 파일 일곱 개(연주기 여섯 + `server.mjs`)가 보인다. 비교 파일을 저장했다면 `ex/` 폴더도 보인다. 빈 폴더는 올라가지 않는다.

- 올린 뒤에 다시 고쳤으면 `git add .` → `git commit -m "…"` → `git push` 로 한 번 더 올린다.
- push 가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../../weeks/week02_github_pages/lab.md#막혔을-때)를 본다.

## 8. 캡처

1. 1~3분 뒤 `https://student01.github.io/web-synth/` 을 연다.
2. 곡 선택에서 **my_song.json** 을 고르고 **▶ 재생**을 누른다.
3. 머리 줄의 내 제목 · BPM, 분홍색으로 강조된 마디, 표시등 옆 위치 줄이 한 화면에 보일 때 **주소창과 함께** 캡처한다. 이 한 장이 제출물이다.
4. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com` 을 지우고 나간다.

**예상 결과** — 공개 주소에서도 4단계의 localhost 화면과 같은 머리 줄과 악보가 보이고 소리가 난다.

- 소리는 캡처되지 않는다. 화면 조건(내 제목 · BPM, 강조된 마디)만 본다.
- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS 는 ⌘+Shift+R)로 새로고침한다.
- 404 가 나면 저장소 이름 `web-synth`, Pages 설정, 파일 이름 대소문자를 본다.
- 캡처에 실명 · 학번 · 실제 이메일이 보이지 않게 한다. 아이디는 보여도 된다.

## 연주기 전문

`examples/build/` 의 여섯 파일 전체다. 받은 파일과 한 줄씩 비교할 때, 오류 줄의 `파일:줄` 을 찾아갈 때 쓴다. 줄 번호는 VS Code 왼쪽 숫자와 같다.

### index.html

화면의 뼈대다. 고치지 않는다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>디스코 연주기</title>
    <link rel="stylesheet" href="main.css">
</head>
<body>
    <header>
        <h1>디스코 연주기</h1>
        <p id="track">곡을 불러오는 중…</p>
    </header>

    <main>
        <section class="panel">
            <button id="play">▶ 재생</button>
            <button id="stop">■ 정지</button>
            <label>곡
                <select id="song">
                    <option value="only_you.json">only_you.json</option>
                    <option value="my_song.json">my_song.json</option>
                </select>
            </label>
            <label>리듬
                <select id="pattern">
                    <option value="disco">디스코</option>
                    <option value="rock">록</option>
                </select>
            </label>
            <label>BPM <input id="bpm" type="range" min="80" max="140" value="109"> <b id="bpm-value">109</b></label>
        </section>

        <section class="panel">
            <label><input id="use-kick" type="checkbox" checked> 킥</label>
            <label><input id="use-snare" type="checkbox" checked> 스네어</label>
            <label><input id="use-hat" type="checkbox" checked> 하이햇</label>
            <label><input id="use-bass" type="checkbox" checked> 베이스</label>
            <label><input id="use-chord" type="checkbox" checked> 코드</label>
            <label><input id="use-arp" type="checkbox"> 아르페지오</label>
            <label>코드 파형
                <select id="wave">
                    <option value="sawtooth">sawtooth</option>
                    <option value="square">square</option>
                    <option value="triangle">triangle</option>
                    <option value="sine">sine</option>
                </select>
            </label>
            <label>필터 <input id="cutoff" type="range" min="200" max="5000" step="100" value="1800"> <b id="cutoff-value">1800</b> Hz</label>
        </section>

        <section class="panel">
            <div id="steps" class="steps"></div>
            <p id="where">정지</p>
        </section>

        <section id="sheet" class="sheet"></section>
        <p id="message"></p>
    </main>

    <footer>Web Audio API · 곡 데이터는 코드 진행만 담는다(멜로디·음원 없음)</footer>

    <script>
        // file:// 로 열면 아래 type="module" 스크립트를 브라우저가 막아 아무것도 돌지 않는다.
        // 그래서 이 안내만은 보통 script 로 둔다(보통 script 는 file:// 에서도 돈다 — ex01~ex08)
        if (location.protocol === 'file:') {
            document.getElementById('track').innerText = '곡 없음';
            document.getElementById('message').innerText =
                '주소가 file:// 입니다. 연주기는 서버로 엽니다: 이 폴더에서 node server.mjs 를 띄우고 http://localhost:8000/ 을 여세요.';
        }
    </script>
    <script type="module">
        import main from './index.js';
        main();
    </script>
</body>
</html>
```

- 17~31행 첫 패널: 재생 · 정지 · 곡 선택(`#song`) · 리듬 선택(`#pattern`) · BPM 슬라이더(`#bpm`, 80~140).
- 35~49행 둘째 패널: 층 체크 상자 여섯 개(아르페지오만 `checked` 가 없어 처음에 꺼져 있다), 코드 파형(`#wave`), 필터(`#cutoff`, 200~5000).
- 53 · 54행 16칸 표시등이 들어갈 `#steps` 와 위치 줄 `#where`. 57행 악보 `#sheet`, 58행 오류 문구 `#message`.
- 63~71행 보통 `<script>` 는 주소가 `file://` 일 때만 머리 줄을 `곡 없음` 으로, 58행 `#message` 를 서버로 열라는 안내로 바꾼다. 보통 script 는 `file://` 에서도 돈다(ex01~ex08).
- 72~75행 `<script type="module">` 이 `index.js` 의 `main` 을 가져와(`import`) 부른다. `type="module"` 은 서버나 공개 주소에서만 돈다.

### main.css

고치지 않는다.

```css
body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    margin: 0;
    background-color: #120a24;
    color: #f4ecff;
    font-family: system-ui, sans-serif;
}

header,
footer {
    padding: 12px 16px;
}

header h1 {
    margin: 0;
    color: #ff5fd2;
}

footer {
    color: #9c8fb8;
    font-size: 13px;
}

main {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 0 16px;
}

.panel {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 12px;
    padding: 12px;
    border: 1px solid #3c2a63;
    border-radius: 8px;
    background-color: #1c1236;
}

button {
    padding: 8px 16px;
    font-size: 16px;
}

.steps {
    display: flex;
    gap: 4px;
}

.step {
    width: 22px;
    height: 22px;
    border-radius: 4px;
    background-color: #2c2050;
}

.step.beat {
    background-color: #45307a;
}

.step.on {
    background-color: #ffd23f;
}

.row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
    margin-bottom: 8px;
}

.row h3 {
    width: 160px;
    margin: 0;
    font-size: 14px;
    color: #c7b8ee;
}

.bar {
    width: 56px;
    padding: 10px 0;
    text-align: center;
    border-radius: 6px;
    background-color: #2c2050;
}

.bar.now {
    background-color: #ff5fd2;
    color: #120a24;
    font-weight: bold;
}

#message {
    color: #ff8a8a;
}

@media (max-width: 600px) {
    .row h3 {
        width: 100%;
    }
}
```

- 1~9행 `body` 를 세로 flex, 최소 높이 `100vh` 로 둬서 꼬리(footer)가 화면 아래에 붙는다.
- 34~43행 `.panel` 은 `flex-wrap` + `gap`(4주차). 좁은 화면에서 줄이 바뀐다.
- 62~68행 박의 첫 칸 `.step.beat` 와 지금 칸 `.step.on`(노랑), 93~97행 지금 마디 `.bar.now`(분홍).
- 103~107행 600px 이하에서 구간 이름이 한 줄을 다 쓴다.

### synth.js

소리 부품이다. 화면은 모르고, `(ctx, 나갈 곳, 시각, …)` 을 받아 그 시각에 소리 하나를 예약한다. 함수마다 주석에 어느 ex 에서 왔는지 적혀 있다.

```js
// synth.js — 소리 부품. 화면은 모르고, (ctx, 나갈 곳, 시각, …)을 받아 그 시각에 소리 하나를 예약한다.
//   ctx  = AudioContext,  out = 소리가 나갈 노드(끝에 스피커가 있다),  time = ctx.currentTime 기준 초
// 각 부품이 어느 비교 예제(ex)에서 왔는지 주석에 적었다.

// ex02 — MIDI 번호 → 진동수. A4(69번) = 440Hz, 반음 하나 = 2^(1/12)배, 한 옥타브(12반음) = 2배
export function midiToFreq(midi) {
    return 440 * 2 ** ((midi - 69) / 12);
}

// ex04 — 코드 이름 → 음(MIDI 번호) 배열. 'Am' = 근음 A + [0, 3, 7] 반음
const NOTE_INDEX = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const CHORD_SHAPES = {
    '': [0, 4, 7],          // 장3화음(밝다): 근음 · 4반음 위 · 7반음 위
    m: [0, 3, 7],           // 단3화음(어둡다): 가운데 음만 반음 낮다
    7: [0, 4, 7, 10],
    m7: [0, 3, 7, 10],
    maj7: [0, 4, 7, 11],
    dim: [0, 3, 6],
    sus2: [0, 2, 7],
    sus4: [0, 5, 7],
};

export function chordToMidis(name) {
    const found = /^([A-G])([#b]?)(.*)$/.exec(name);     // 'C#m7' → 'C', '#', 'm7'
    if (!found) throw new Error(`코드 이름을 읽을 수 없습니다: ${name}`);
    const shape = CHORD_SHAPES[found[3]];
    if (!shape) throw new Error(`모르는 코드 종류입니다: ${name} — 쓸 수 있는 모양: C Cm C7 Cm7 Cmaj7 Cdim Csus2 Csus4 (C 자리에 A~G, 뒤에 # 이나 b)`);
    let root = NOTE_INDEX[found[1]];
    if (found[2] === '#') root += 1;
    if (found[2] === 'b') root -= 1;
    let base = 60 + ((root + 12) % 12);                  // 도(C4=60)부터 시(B4=71) 사이에서 근음을 고르고
    if (base > 66) base -= 12;                           // 너무 높으면 한 옥타브 내린다(G3~F#4)
    return shape.map(function (step) { return base + step; });
}

// ex06 — 잡음 1초. 스네어·하이햇의 재료. 한 번 만들어 두고 계속 쓴다
export function createNoise(ctx) {
    const buffer = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
    return buffer;
}

// ex01·ex03·ex05 — 음 하나: 오실레이터(파형) → 필터 → 게인(엔벨로프) → out
export function playTone(ctx, out, note) {
    const type = note.type || 'sawtooth';
    const attack = note.attack || 0.005;     // 커지는 시간
    const length = note.length || 0.2;       // 유지하는 시간
    const release = note.release || 0.1;     // 사라지는 시간
    const volume = note.volume || 0.2;
    const t = note.time;

    const osc = ctx.createOscillator();
    const filter = ctx.createBiquadFilter();
    const amp = ctx.createGain();
    osc.type = type;
    osc.frequency.value = note.freq;
    filter.type = 'lowpass';
    filter.frequency.value = note.cutoff || 20000;

    amp.gain.setValueAtTime(0.0001, t);                                    // 0 에서 시작해야 '딱' 소리가 안 난다
    amp.gain.exponentialRampToValueAtTime(volume, t + attack);
    amp.gain.setValueAtTime(volume, t + attack + length);
    amp.gain.exponentialRampToValueAtTime(0.0001, t + attack + length + release);   // ex03 5번: 귀에 고르게 줄어든다

    osc.connect(filter).connect(amp).connect(out);
    osc.start(t);
    osc.stop(t + attack + length + release + 0.05);
}

// ex06 — 킥: 사인파의 높이를 150Hz → 45Hz 로 빠르게 떨어뜨린다(퍽)
export function playKick(ctx, out, time) {
    const osc = ctx.createOscillator();
    const amp = ctx.createGain();
    osc.frequency.setValueAtTime(150, time);
    osc.frequency.exponentialRampToValueAtTime(45, time + 0.12);
    amp.gain.setValueAtTime(0.9, time);
    amp.gain.exponentialRampToValueAtTime(0.001, time + 0.4);
    osc.connect(amp).connect(out);
    osc.start(time);
    osc.stop(time + 0.45);
}

// ex06 — 잡음을 필터로 깎고 짧게 끊는다. 스네어·하이햇이 함께 쓴다
function playNoise(ctx, out, noise, time, highpass, volume, decay) {
    const src = ctx.createBufferSource();
    const filter = ctx.createBiquadFilter();
    const amp = ctx.createGain();
    src.buffer = noise;
    filter.type = 'highpass';                // 이 진동수보다 낮은 쪽을 깎는다
    filter.frequency.value = highpass;
    amp.gain.setValueAtTime(volume, time);
    amp.gain.exponentialRampToValueAtTime(0.001, time + decay);
    src.connect(filter).connect(amp).connect(out);
    src.start(time);
    src.stop(time + decay + 0.02);
}

// ex06 — 스네어: 잡음(칙) + 짧은 톤(몸통)
export function playSnare(ctx, out, noise, time) {
    playNoise(ctx, out, noise, time, 1200, 0.45, 0.18);
    playTone(ctx, out, { freq: 190, time: time, type: 'triangle', attack: 0.001, length: 0.01, release: 0.08, volume: 0.25 });
}

// ex06 — 하이햇: 잡음의 아주 높은 쪽만. 닫힘은 짧게, 열림은 길게
export function playHat(ctx, out, noise, time, open) {
    playNoise(ctx, out, noise, time, 7000, open ? 0.16 : 0.12, open ? 0.28 : 0.05);
}
```

- 6~8행 `midiToFreq` 는 ex02 와 같다.
- 12~21행 `CHORD_SHAPES` 가 쓸 수 있는 코드 종류다(4단계 표). 23~34행 `chordToMidis` 가 이름을 근음 · `#`/`b` · 종류로 나누고(24행), 모르는 종류면 오류 문구를 던진다(27행).
- 45~69행 `playTone` 은 오실레이터 → lowpass → 게인 → `out`. 61~64행 엔벨로프는 0.0001 에서 시작해 exponential 로 줄인다(ex03 5번).
- 72~82행 킥, 85~97행 잡음 치기, 100~103행 스네어(잡음 + 짧은 톤), 106~108행 하이햇(ex06).
- `export` 가 붙은 함수만 `index.js` 가 `import` 로 가져다 쓴다. `playNoise`(85행)는 `export` 가 없어 이 파일 안에서만 쓴다.

### index.js

연주를 맡는다. 곡을 불러오고, 16분음표 한 칸마다 `synth.js` 의 소리 부품을 예약한다.

```js
// index.js — 디스코 연주기. 곡(JSON)을 불러와 16분음표 한 칸마다 소리 부품(synth.js)을 예약한다.
import { midiToFreq, chordToMidis, createNoise, playTone, playKick, playSnare, playHat } from './synth.js';

// ex08 — 리듬은 배열이다. 한 마디 = 16칸(16분음표). 1 이면 그 칸에서 친다
// bass 는 1 = 낮은 근음, 2 = 한 옥타브 위 근음(디스코 베이스의 '둥-둥' 오르내림)
const PATTERNS = {
    disco: {
        kick:  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],   // 박마다 킥(four on the floor)
        snare: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],   // 2박·4박
        hat:   [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        open:  [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],   // 엇박에 열린 하이햇 — 디스코의 표시
        bass:  [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0],
        chord: [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        arp:   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    },
    rock: {
        kick:  [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        snare: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        hat:   [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        open:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        bass:  [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        chord: [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        arp:   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    },
};

const ROWS = ['kick', 'snare', 'hat', 'open', 'bass', 'chord', 'arp'];

const $ = function (id) { return document.getElementById(id); };

let ctx = null;        // AudioContext — 재생을 처음 누를 때 만든다(ex01)
let out = null;        // 모든 소리가 모이는 곳 → 압축기 → 스피커
let noise = null;
let bars = [];         // 곡 전체 마디를 한 줄로 편 것 [{ section, chord, midis }]
let cells = [];        // bars 와 같은 순서의 화면 칸
let timer = null;
let nextTime = 0;      // 다음 칸을 칠 시각(ctx.currentTime 기준)
let step = 0;          // 처음부터 몇 번째 칸인가
const queue = [];      // 화면에 보여 줄 { step, time }

// ex07 — 한 박 = 60 / BPM 초. 16분음표 한 칸은 그 4분의 1
function secondsPerStep() {
    return 60 / Number($('bpm').value) / 4;
}

function on(id) {
    return $(id).checked;
}

// 리듬 배열을 고치다 줄을 지우거나 칸 수를 틀리면 소리가 끊긴다. 치기 전에 확인해 알려 준다
function checkPattern(name) {
    for (const row of ROWS) {
        const line = PATTERNS[name][row];
        if (!line || line.length !== 16) return `리듬 '${name}' 의 ${row} 줄이 16칸이 아닙니다`;
    }
    return '';
}

// 한 칸에서 칠 소리를 모두 예약한다
function scheduleStep(n, time) {
    const bar = bars[Math.floor(n / 16) % bars.length];
    const i = n % 16;
    const p = PATTERNS[$('pattern').value];
    const len = secondsPerStep();
    const wave = $('wave').value;
    const cutoff = Number($('cutoff').value);

    if (on('use-kick') && p.kick[i]) playKick(ctx, out, time);
    if (on('use-snare') && p.snare[i]) playSnare(ctx, out, noise, time);
    if (on('use-hat') && p.hat[i]) playHat(ctx, out, noise, time, false);
    if (on('use-hat') && p.open[i]) playHat(ctx, out, noise, time, true);
    if (on('use-bass') && p.bass[i]) {
        const root = bar.midis[0] - 24 + (p.bass[i] === 2 ? 12 : 0);      // 코드 근음을 두 옥타브 아래로
        playTone(ctx, out, { freq: midiToFreq(root), time: time, type: 'square', cutoff: 700, attack: 0.003, length: len * 0.6, release: 0.06, volume: 0.3 });
    }
    if (on('use-chord') && p.chord[i]) {
        for (const midi of bar.midis) {                                   // ex04 — 음 수만큼 동시에
            playTone(ctx, out, { freq: midiToFreq(midi), time: time, type: wave, cutoff: cutoff, attack: 0.005, length: len, release: 0.15, volume: 0.24 / bar.midis.length });
        }
    }
    if (on('use-arp') && p.arp[i]) {
        const notes = bar.midis.concat(bar.midis[0] + 12);                // 코드 음 + 한 옥타브 위 근음
        playTone(ctx, out, { freq: midiToFreq(notes[i % notes.length] + 12), time: time, type: 'square', cutoff: cutoff, attack: 0.002, length: len * 0.4, release: 0.05, volume: 0.06 });
    }
    queue.push({ step: n, time: time });
}

// ex07 — 25ms 마다 깨어나서, 앞으로 0.1초 안에 올 칸을 오디오 시계에 미리 예약한다
function tick() {
    while (nextTime < ctx.currentTime + 0.1) {
        scheduleStep(step, nextTime);
        nextTime += secondsPerStep();
        step += 1;
    }
}

// 예약한 칸의 시각이 되면 화면 불을 옮긴다
function draw() {
    while (queue.length > 0 && queue[0].time <= ctx.currentTime) {
        show(queue.shift().step);
    }
    if (timer) requestAnimationFrame(draw);
}

function show(n) {
    const i = n % 16;
    const b = Math.floor(n / 16) % bars.length;
    document.querySelectorAll('.step').forEach(function (el, k) { el.classList.toggle('on', k === i); });
    cells.forEach(function (el, k) { el.classList.toggle('now', k === b); });
    $('where').innerText = `${bars[b].section} · ${b + 1}/${bars.length}마디 · ${bars[b].chord}`;
}

async function play() {
    if (!ctx) {
        ctx = new AudioContext();
        const compressor = ctx.createDynamicsCompressor();   // 여러 소리가 겹쳐도 찢어지지 않게 눌러 준다
        out = ctx.createGain();
        out.gain.value = 0.6;
        out.connect(compressor).connect(ctx.destination);
        noise = createNoise(ctx);
    }
    await ctx.resume();
    if (timer || bars.length === 0) return;
    const problem = checkPattern($('pattern').value);
    if (problem) {
        $('message').innerText = problem;
        return;
    }
    $('message').innerText = '';
    step = 0;
    nextTime = ctx.currentTime + 0.05;
    timer = setInterval(tick, 25);
    requestAnimationFrame(draw);
}

function stop() {
    clearInterval(timer);
    timer = null;
    queue.length = 0;
    document.querySelectorAll('.now, .step.on').forEach(function (el) { el.classList.remove('now', 'on'); });
    $('where').innerText = '정지';
}

// ex09 — 곡 JSON 을 불러와 마디를 한 줄로 편다. 코드 이름이 틀리면 여기서 알려 준다
async function loadSong(file) {
    stop();
    $('message').innerText = '';
    const response = await fetch(file);
    if (!response.ok) throw new Error(`${file} 을 불러오지 못했습니다 (${response.status})`);
    const song = await response.json();
    const info = song.track_info;

    bars = [];
    for (const section of song.sections) {
        for (const bar of section.progression) {
            bars.push({ section: section.section, chord: bar.chord, midis: chordToMidis(bar.chord) });
        }
    }

    $('track').innerText = `${info.title} — ${info.artist} · ${info.key} · ${info.time_signature} · ${info.bpm} BPM`;
    $('bpm').value = info.bpm;                           // 80~140 밖이면 슬라이더가 끝값으로 맞춘다
    $('bpm-value').innerText = $('bpm').value;

    // 악보: 구간마다 한 줄, 마디마다 한 칸
    const sheet = $('sheet');
    sheet.innerHTML = '';
    cells = [];
    for (const section of song.sections) {
        const row = document.createElement('div');
        row.className = 'row';
        const name = document.createElement('h3');
        name.textContent = section.section;
        row.append(name);
        for (const bar of section.progression) {
            const cell = document.createElement('div');
            cell.className = 'bar';
            cell.textContent = bar.chord;
            row.append(cell);
            cells.push(cell);
        }
        sheet.append(row);
    }
}

export default async function main() {
    for (let i = 0; i < 16; i++) {                       // 16칸 표시등
        const el = document.createElement('div');
        el.className = i % 4 === 0 ? 'step beat' : 'step';
        $('steps').append(el);
    }

    $('play').addEventListener('click', play);
    $('stop').addEventListener('click', stop);
    $('bpm').addEventListener('input', function () { $('bpm-value').innerText = $('bpm').value; });
    $('cutoff').addEventListener('input', function () { $('cutoff-value').innerText = $('cutoff').value; });
    $('song').addEventListener('change', function () {
        loadSong($('song').value).catch(showError);
    });
    $('pattern').addEventListener('change', function () {
        const problem = checkPattern($('pattern').value);
        if (problem) {
            stop();
            $('message').innerText = problem;
        }
    });

    try {
        await loadSong($('song').value);
    } catch (error) {
        showError(error);
    }
}

// 곡을 불러오다 실패하면 옛 악보도 지운다. 고장 난 곡은 재생하지 않는다
function showError(error) {
    stop();
    bars = [];
    cells = [];
    $('sheet').innerHTML = '';
    $('track').innerText = '곡 없음';
    $('message').innerText = `불러오지 못했습니다: ${error.message}`;
}
```

- 6~25행 `PATTERNS`(5단계). 27행 `ROWS` 는 리듬 한 벌에 있어야 할 줄 이름 일곱 개다. 31~39행은 연주 중에 바뀌는 값들이다. `ctx` 는 재생을 처음 누를 때 만든다(115행, ex01).
- 42~44행 `secondsPerStep` — 한 박 = 60/BPM 초, 한 칸은 그 4분의 1(ex07).
- 51~57행 `checkPattern` — 리듬의 일곱 줄이 모두 있고 16칸인지 본다. 아니면 `리듬 'disco' 의 arp 줄이 16칸이 아닙니다` 같은 문구를 돌려준다.
- 60~86행 `scheduleStep` — 한 칸에서 칠 소리를 모두 예약한다. 68~71행 북(ex06), 72~75행 베이스(코드 근음을 두 옥타브 아래로), 76~80행 코드(음 수만큼 동시에, ex04), 81~84행 아르페지오(칸마다 코드 음을 차례로. 코드 음은 ex04, 칸 번호 `i` 로 음을 고르는 것은 ex08).
- 89~95행 `tick` — 25ms 마다 깨어나 0.1초 앞까지 예약한다(ex07 2번). 132행 `setInterval(tick, 25)` 가 부른다.
- 98~111행 `draw` · `show` — 예약한 시각이 되면 표시등과 마디 강조를 옮기고 위치 줄을 쓴다.
- 113~134행 `play` — 첫 클릭에 AudioContext · 압축기 · 모든 소리가 모이는 게인(0.6)을 만든다. 124~128행에서 `checkPattern` 으로 리듬을 확인하고, 문제가 있으면 문구만 띄우고 재생하지 않는다. 136~142행 `stop`.
- 145~183행 `loadSong` — `fetch` → `response.json()` → 마디를 한 줄로 펴고(`bars`) → 머리 줄 · BPM → 악보 칸을 `createElement` · `append` 로 만든다(ex09, 10주차).
- 185~212행 `main` — 표시등 16칸을 만들고 이벤트를 단 뒤 첫 곡을 불러온다. 199~205행 리듬을 바꿀 때도 `checkPattern` 으로 확인해, 문제가 있으면 멈추고 문구를 띄운다.
- 215~222행 `showError` — 연주를 멈추고 `bars` 와 악보 칸을 비운 뒤, 머리 줄을 `곡 없음`, 아래 문구를 `불러오지 못했습니다: …` 로 적는다. 고장 난 곡은 재생되지 않는다.

### my_song.json

4단계에서 고칠 처음 모양이다.

```json
{
  "track_info": {
    "title": "내 노래",
    "artist": "student01",
    "key": "C",
    "time_signature": "4/4",
    "bpm": 118
  },
  "sections": [
    {
      "section": "A",
      "bars_count": 4,
      "progression": [
        { "bar": 1, "chord": "C" },
        { "bar": 2, "chord": "G" },
        { "bar": 3, "chord": "Am" },
        { "bar": 4, "chord": "F" }
      ]
    },
    {
      "section": "B",
      "bars_count": 4,
      "progression": [
        { "bar": 1, "chord": "Dm7" },
        { "bar": 2, "chord": "G7" },
        { "bar": 3, "chord": "Cmaj7" },
        { "bar": 4, "chord": "Am7" }
      ]
    }
  ]
}
```

### only_you.json

곡 정보와 4구간 28마디의 코드 진행만 담았다. 멜로디 · 가사 · 음원은 없다. 손대지 않는다.

```json
{
  "track_info": {
    "title": "Only You",
    "artist": "Savage",
    "key": "Am",
    "time_signature": "4/4",
    "bpm": 109
  },
  "sections": [
    {
      "section": "Intro / Synth Lead",
      "bars_count": 8,
      "progression": [
        { "bar": 1, "chord": "Am" },
        { "bar": 2, "chord": "Dm" },
        { "bar": 3, "chord": "G" },
        { "bar": 4, "chord": "C" },
        { "bar": 5, "chord": "Am" },
        { "bar": 6, "chord": "Dm" },
        { "bar": 7, "chord": "G" },
        { "bar": 8, "chord": "Am" }
      ]
    },
    {
      "section": "Verse",
      "bars_count": 8,
      "progression": [
        { "bar": 1, "chord": "Am" },
        { "bar": 2, "chord": "F" },
        { "bar": 3, "chord": "G" },
        { "bar": 4, "chord": "C" },
        { "bar": 5, "chord": "Am" },
        { "bar": 6, "chord": "F" },
        { "bar": 7, "chord": "G" },
        { "bar": 8, "chord": "C" }
      ]
    },
    {
      "section": "Pre-Chorus",
      "bars_count": 4,
      "progression": [
        { "bar": 1, "chord": "Am" },
        { "bar": 2, "chord": "F" },
        { "bar": 3, "chord": "Dm" },
        { "bar": 4, "chord": "G" }
      ]
    },
    {
      "section": "Chorus",
      "bars_count": 8,
      "progression": [
        { "bar": 1, "chord": "F" },
        { "bar": 2, "chord": "G" },
        { "bar": 3, "chord": "C" },
        { "bar": 4, "chord": "Am" },
        { "bar": 5, "chord": "F" },
        { "bar": 6, "chord": "G" },
        { "bar": 7, "chord": "C" },
        { "bar": 8, "chord": "Am" }
      ]
    }
  ]
}
```

## 오류가 나면

먼저 화면의 빨간 글자를 읽고, 없으면 **F12 › Console** 의 빨간 줄과 오른쪽 `파일:줄` 을 읽는다. JSON 오류와 리듬 칸 수 오류는 화면에, 그 밖의 코드 오류는 Console 에 나온다.
자주 나오는 문구와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다. 서버 쪽 문제는 [서버 사용 안내](../../tools/static-server/README.md#막혔을-때)를 본다.
한 곳을 고친 다음 저장 → 새로고침하고, 해결되지 않으면 화면과 Console 을 그대로 보여 주고 도움을 받는다.
