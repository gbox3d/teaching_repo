---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 특강"
footer: "웹 신시사이저 만들어 보기 · 소리 부품을 비교하고 마지막에 디스코 연주기로 조립"
---

# 웹 신시사이저 만들어 보기

오늘은 브라우저로 소리를 만들고, 마지막에 **디스코 연주기**를 조립합니다.

- 방식: 소리 부품을 **비교 파일 9개**로 하나씩 듣고, 연주기는 그 부품을 모은 것으로 읽습니다.
- **이어폰 필수**입니다. 실습실 전체가 스피커로 소리를 내면 아무것도 들리지 않습니다.
- 실습은 **값을 바꿔 보는 것**입니다. 무엇이 달라질지 먼저 말해 보고 듣습니다.
- 결과물: 새 저장소 `web-synth` 의 공개 주소에서 **내가 고친 `my_song.json`** 을 재생하는 화면 캡처 1장.

곡 데이터는 **코드 진행만** 담습니다. 멜로디 · 가사 · 음원은 교재에도 과제에도 넣지 않습니다.

---

# 1부 — 소리를 만든다

`25분 설명·시연`

1. 소리는 공기의 떨림이고, 브라우저가 그 떨림을 만든다
2. ex01 — 파형: 같은 높이, 다른 모양
3. ex02 — 음 높이: 옥타브는 2배, 반음은 2^(1/12)배
4. ex03 — 엔벨로프: 크기가 시간에 따라 변하는 모양
5. ex04 — 화음: 근음에서 몇 반음 위를 함께 치나
6. ex05 — 필터: 높은 성분을 깎으면 어두워진다

---

## 1부 · 0–3분 — 소리는 공기의 떨림이고, 브라우저가 그 떨림을 만든다

```text
[클릭] → new AudioContext()  ← 누르기 전에는 소리를 내 주지 않는다
오실레이터 → 필터 → 게인 → 스피커(ctx.destination)
오실레이터 = type(모양) · frequency(높이)  ← ex01 · ex02
게인 = gain 을 시간에 따라 바꾼다  ← ex03
필터 = lowpass · cutoff(높은 쪽 깎기)  ← ex05
```

- 소리는 공기의 떨림입니다. 1초에 떨리는 횟수(Hz)가 높이, 떨림의 모양이 음색, 폭이 크기입니다.
- Web Audio API 는 부품(노드)을 `connect` 로 이어 소리를 만듭니다. 비교 파일이 부품을 하나씩 바꿉니다.
- 브라우저는 사용자가 누르기 전에는 소리를 내 주지 않습니다. `new AudioContext()` 는 클릭할 때 만듭니다.

**소리는 노드를 이어 만든다: 떨림(오실레이터) → 깎기(필터) → 크기(게인) → 스피커.**

---

## 1부 · 3–7분 — ex01 파형: 같은 높이, 다른 모양

[examples/ex01_wave.html](examples/ex01_wave.html)
형제: 1. sine / 2. square / 3. sawtooth / 4. triangle (220Hz · 1초 · 0.2 는 같다)

```js
const osc = ctx.createOscillator();  // 같은 모양의 떨림을 계속 만든다
osc.type = type;        // 'sine' | 'square' | 'sawtooth' | 'triangle'
osc.frequency.value = 220;           // 1초에 220번 떨린다
amp.gain.value = 0.2;
```

- 처음 누르면 `AudioContext 상태: running`. 아래 그림이 나가는 소리의 모양입니다.
- 바꿔 보기: `frequency.value` 220 → 440, `gain.value` 0.2 → 0.05.

**오실레이터는 같은 모양의 떨림을 계속 만든다. 모양(type)이 음색을 정한다.**

---

## 1부 · 7–11분 — ex02 음 높이: 옥타브는 2배, 반음은 2^(1/12)배

[examples/ex02_pitch.html](examples/ex02_pitch.html)
형제: 1. A3 · A4 · A5(같은 '라' 세 개) / 2. C4~C5 여덟 음(키보드 A S D F G H J K)

```js
// MIDI 번호: 피아노 건반에 붙인 번호. 가운데 도(C4) = 60, 라(A4) = 69
function midiToFreq(midi) {
    return 440 * 2 ** ((midi - 69) / 12);    // A4 = 440Hz
}
```

- 단추에 진동수가 적힙니다: A3 `220.0` · A4 `440.0` · A5 `880.0`. 키 H → `MIDI 69 → 440.0 Hz`.
- 바꿔 보기: 30행의 440 을 432 로 → 단추 숫자가 모두 바뀝니다. 버튼의 `data-midi` 값 바꾸기.

**음 높이 = 1초에 떨리는 횟수. 한 옥타브는 2배, 반음은 2^(1/12)배. MIDI 번호로 계산한다.**

---

## 1부 · 11–16분 — ex03 엔벨로프: 크기가 시간에 따라 변하는 모양

[examples/ex03_envelope.html](examples/ex03_envelope.html)
형제: 1. 켰다 끄기만 / 2. 짧게 / 3. 길게 / 4. 천천히 커지기 / 5. 2번을 exponential 로

```js
amp.gain.setValueAtTime(0.0001, t);
amp.gain.linearRampToValueAtTime(PEAK, t + attack);   // attack
amp.gain.setValueAtTime(PEAK, t + attack + hold);     // 유지
amp.gain.exponentialRampToValueAtTime(0.0001, t + attack + hold + release);
```

- 1번은 시작과 끝에 '딱'. 2번은 뜯는 소리, 3번은 깔리는 소리. 그림이 크기 변화입니다.
- 바꿔 보기: 2번과 5번을 번갈아 듣기(숫자는 같다). 51~55행의 attack · release 숫자.

**엔벨로프(크기가 시간에 따라 변하는 모양)가 소리의 성격을 정한다. 0 에서 시작해 0 으로 끝나야 '딱' 소리가 없다.**

---

## 1부 · 16–21분 — ex04 화음: 근음에서 몇 반음 위를 함께 치나

[examples/ex04_chord.html](examples/ex04_chord.html)
형제: 1. 곡의 코드 Am · Dm · G · C · F / 2. C vs Cm, A vs Am / 3. Am 차례로

```js
const SHAPES = { '': [0, 4, 7], m: [0, 3, 7] };   // 근음에서 몇 반음 위
for (const midi of midis) note(midi, ctx.currentTime, 1.2);   // 같은 시각
note(midis[i % 3] + 12, ctx.currentTime + i * 0.15, 0.14);  // 0.15초씩 늦게
```

- Am 을 누르면 `MIDI 57 · 60 · 64`. C 는 60 · 64 · 67, Cm 은 60 · 63 · 67 — 가운데만 다릅니다.
- 바꿔 보기: `SHAPES` 에 `7: [0, 4, 7, 10]` 을 더해 G7 치기. 아르페지오 간격 0.15 → 0.1.

**화음 = 오실레이터 여러 개를 같은 시각에. 장 [0, 4, 7], 단 [0, 3, 7] — 가운데 음 하나가 반음 차이다.**

---

## 1부 · 21–25분 — ex05 필터: 높은 성분을 깎으면 어두워진다

[examples/ex05_filter.html](examples/ex05_filter.html)
형제: Am 화음(sawtooth) + lowpass 1. 없음 / 2. 3000 / 3. 800 / 4. 200 / 5. Q 15 / 6. 쓸기

```js
filter.type = 'lowpass';   // 기준보다 높은 쪽을 깎고 낮은 쪽은 통과시킨다
filter.frequency.value = cutoff;
filter.Q.value = q;        // 기준 근처를 얼마나 도드라지게 하나
filter.frequency.exponentialRampToValueAtTime(4000, ctx.currentTime + 2);
```

- 1 → 4번으로 갈수록 어둡고 그림 오른쪽(높은 쪽) 막대가 사라집니다. 5번은 다른 단추보다 큽니다.
- 바꿔 보기: 버튼의 `data-cutoff` 값, 5번의 Q 15, 6번의 쓸기 시간 2초.

**lowpass 는 기준(cutoff)보다 높은 쪽을 깎아 어둡게 한다. 기준을 움직이면 쓸기 소리가 난다.**

**설명 합계: 3+4+4+5+5+4 = 25분**

---

# 2부 — 리듬과 곡

`25분 설명·시연`

1. ex06 — 북소리: 높이가 떨어지는 사인파와 잡음
2. ex07 — 박자: 타이머가 아니라 오디오 시계에 예약한다
3. ex08 — 리듬은 배열이다: 16칸 중 1 인 칸에서 친다
4. ex09 — 곡은 데이터다: JSON 을 fetch 로 받는다
5. 조립 — 디스코 연주기는 ex01~ex09 의 부품을 모은 것이다

---

## 2부 · 0–5분 — ex06 북소리: 떨어지는 사인파와 잡음

[examples/ex06_drums.html](examples/ex06_drums.html)
형제: 킥 1. 그대로 / 2. 떨어뜨리기 · 스네어 3. 잡음 / 4. + 톤 · 하이햇 5. 닫힘 / 6. 열림

```js
// 높이가 빠르게 떨어지면 '퍽'
osc.frequency.exponentialRampToValueAtTime(toFreq, t + 0.12);
for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
filter.type = 'highpass';   // 이 높이보다 낮은 쪽을 깎는다
```

- 킥 1 · 2번은 같은 사인파, 2번만 0.12초 만에 150 → 45Hz. 하이햇 5 · 6번은 길이만 다릅니다.
- 바꿔 보기: 2번의 150 · 45 · 0.12, 하이햇의 highpass 7000, 길이(decay).

**북소리도 오실레이터 · 잡음 + 아주 짧은 엔벨로프다. 떨어지는 사인파 = 킥, 잡음의 높은 쪽 = 하이햇.**

---

## 2부 · 5–10분 — ex07 박자: 타이머가 아니라 오디오 시계에 예약한다

[examples/ex07_timing.html](examples/ex07_timing.html)
형제: 1. setTimeout 으로 16번 치기 / 2. 오디오 시계에 16번 예약하기 — "바쁘게" 체크 상자

```js
return 60 / bpm / 4;                // 한 박 = 60/BPM 초, 16분음표 = 그 4분의 1
if (times.length < 16) setTimeout(hit, secondsPerStep() * 1000);   // 1.
while (next < ctx.currentTime + 0.1 && times.length < 16) {        // 2.
    click(next);                    // 그 시각에 나도록 예약한다
```

- 109 BPM → 한 박 `0.550`초, 한 칸 `0.138`초. 안 바쁠 때 1번 139~144ms, 2번 138ms 고정.
- 바쁘게를 켜면 1번은 155~203ms 로 들쭉날쭉, 2번은 그대로 138ms. 바꿔 보기: BPM 칸, 바쁘게 체크.

**JavaScript 타이머는 브라우저가 바쁘면 늦는다. 오디오 시계에 시각을 미리 적어 두면 정확하다.**

---

## 2부 · 10–15분 — ex08 리듬은 배열이다: 디스코 = 박마다 킥 + 엇박 하이햇

[examples/ex08_pattern.html](examples/ex08_pattern.html)
형제: 1. 디스코 / 2. 록 / 3. 비우기 — 줄 4개(kick · snare · hat · open) × 16칸, 109 BPM

```text
kick : [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]   ← 박마다 킥
snare: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]   ← 2박 · 4박
open : [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]   ← 엇박
if (pattern.kick[i]) kick(t);   ← i 번째 칸이 1 이면 그 시각에 예약
```

- 칸을 누르면 아래 배열이 바로 바뀝니다. 재생 중이면 그 칸이 다시 올 때부터 소리가 바뀝니다.
- 바꿔 보기: 디스코의 kick 줄에서 2 · 4박 칸을 끕니다. 무엇이 사라지나? 록 kick 과 비교합니다.

**리듬은 배열이다(16칸 중 1 인 칸에서 친다). 디스코 = 박마다 킥 + 2 · 4박 스네어 + 엇박 열린 하이햇.**

---

## 2부 · 15–19분 — ex09 곡은 데이터다: JSON 을 fetch 로 받는다

[examples/ex09_fetch_song.html](examples/ex09_fetch_song.html) · [ex09_song.json](examples/ex09_song.json)
형제: 같은 페이지를 1. `file:///…` 로 열기 / 2. `http://localhost:8000/` 으로 열기

```js
const response = await fetch('ex09_song.json');   // 같은 폴더의 파일을 '요청'한다
const song = await response.json();               // 글자(JSON) → 객체
document.getElementById('v1').innerText = song.track_info.title;
```

- http: 표 `연습곡 / 109 / 2 / A / Am / 2`, 펼치면 `A:Am A:F A:C A:G B:Dm B:Am`.
- file: 화면 `불러오지 못했다: Failed to fetch — …`, Console 에 CORS 빨간 줄.

**곡은 데이터다. 따로 둔 JSON 을 `fetch` 로 받아 객체로 쓴다. `file://` 은 막히니 서버로 연다.**

---

## 2부 · 19–25분 — 조립: 디스코 연주기, 그리고 실습 인계

[index.html](examples/build/index.html) · [main.css](examples/build/main.css) · [index.js](examples/build/index.js) · [synth.js](examples/build/synth.js) · [only_you.json](examples/build/only_you.json) · [my_song.json](examples/build/my_song.json)

```text
new AudioContext() ← ex01    playTone 의 엔벨로프 ← ex03 · lowpass ← ex05
midiToFreq ← ex02            playKick · playSnare · playHat ← ex06
chordToMidis ← ex04          코드 층 ← ex04 1·2번 · 아르페지오 층 ← ex04 3번
PATTERNS ← ex08              secondsPerStep · tick ← ex07 · loadSong ← ex09
```

[실습](lab.md#실습-60분) · [따라하기](walkthrough.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/synthesizer)

1. `web-synth` 폴더에 [server.mjs](../../tools/static-server/server.mjs) · 연주기 여섯 파일 → `node server.mjs` → ▶
2. ex03 · ex04 · ex08 바꿔 듣기 → `my_song.json` · `PATTERNS` · `playTone` 중 둘 이상
3. 새 저장소 `web-synth` 에 2주차에 배운 순서 그대로 올리기 → 공개 주소에서 캡처

**설명 합계: 5+5+5+4+6 = 25분**

---

## 제출하기

특강이 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/web-synth/
곡 선택 my_song.json → ▶ 재생
머리 줄: 내가 고친 제목 · BPM   (예: 금요일 밤 — student01 · Am · 4/4 · 124 BPM)
악보: 지금 마디 칸이 분홍색, 표시등 옆에 위치 줄   (예: A · 2/12마디 · F)
```

- 소리는 캡처되지 않습니다. 화면 조건(내 제목 · BPM, 강조된 마디)만 봅니다.
- 주소창이 함께 보이게 찍습니다. 실명 · 학번 · 실제 이메일이 보이지 않게 합니다.

---

## 특강이 끝나면

연주기 안에서 정규 수업의 문법이 쓰인 곳입니다.

- `fetch` · JSON(12주차) — `loadSong` 이 곡 파일을 받아 객체로 씁니다(ex09).
- 배열(10주차) — `PATTERNS` 의 16칸, 마디를 한 줄로 편 `bars`.
- 객체(11주차) — `song.track_info.title`, 마디 하나 `{ section, chord, midis }`.
- `createElement` · `append`(10주차) — 악보의 구간 줄과 마디 칸.

더 해 볼 것: 멜로디 층을 직접 만들기(내가 지은 멜로디만), ex02 키보드로 연주기 위에서 연주하기.
녹음해서 음원 파일로 만드는 것은 이 특강의 범위 밖입니다.
