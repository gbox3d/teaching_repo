[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/synthesizer)

# 특강 — 웹 신시사이저 만들어 보기: 디스코 연주기

브라우저로 소리를 만든다. 소리 부품을 비교 파일 9개로 하나씩 듣고, 마지막에 그 부품을 모은 **디스코 연주기**를 내 노래로 바꿔 공개 주소에 올린다.
파일 하나에 개념 하나. 같은 일을 다르게 한 형제를 나란히 놓고 차이를 귀와 화면으로 본다.
정규 15주 수업 밖의 **선택 특강**이며 1회 110분이다. 주차별 실습 점수와 시험에는 들어가지 않는다.

## 이 특강의 질문

> 버튼 하나로 디스코 반주가 흘러나오게 하려면 브라우저에게 무엇을 시켜야 하나?

답은 명령 이름 몇 개가 아니다. 네 가지 원리다.
소리는 **떨림**이고, 떨림의 모양 · 높이 · 크기 변화를 부품(노드)으로 이어 만든다.
화음은 여러 음을 **같은 시각에** 치는 것이고, 리듬은 **배열**(16칸 중 1 인 칸에서 친다)이다.
박자는 JavaScript 타이머가 아니라 **오디오 시계에 시각을 예약**해야 맞는다.
곡은 코드와 따로 둔 **데이터(JSON)** 이고 `fetch` 로 받는다.

## 대상과 전제

- 12주차(`fetch` · JSON)까지 마친 학생을 권장한다.
- ex01~ex08 은 6주차(함수 · 이벤트)까지의 지식으로 읽을 수 있다. 배열 · 객체(10 · 11주차)는 ex04 · ex08 · ex09 와 연주기에서 쓴다.
- 연주기는 `index.html` + `main.css` + `index.js` 세 파일 구조다. `index.html` 끝의 `<script type="module">` 이 `import main from './index.js'; main();` 을 부르고, 소리 부품은 `synth.js` 에 따로 있다.
- 악보를 읽지 못해도 된다. 코드 이름(Am, G7 …)은 이 특강 안에서 "근음에서 몇 반음 위"로 설명한다.
- 새 저장소 `web-synth` 를 하나 만든다. 정규 주차 저장소는 건드리지 않는다.

## 학습 목표

1. 소리는 공기의 떨림이다. 오실레이터의 모양(type)이 음색을, 진동수가 높이를 정한다. 한 옥타브는 2배, 반음은 2^(1/12)배다. 브라우저는 사용자가 누르기 전에는 소리를 내 주지 않으므로 `AudioContext` 는 클릭할 때 만든다.
2. 소리 크기가 시간에 따라 변하는 모양(엔벨로프)이 소리의 성격을 정한다. 0 에서 시작해 0 으로 끝나야 '딱' 소리가 없다. lowpass 필터는 기준(cutoff)보다 높은 성분을 깎아 소리를 어둡게 한다.
3. 화음은 근음에서 몇 반음 위의 음을 같은 시각에 치는 것이다. 장 [0, 4, 7], 단 [0, 3, 7] — 가운데 음 하나가 반음 차이다. 북소리도 오실레이터 · 잡음 + 아주 짧은 엔벨로프로 만든다.
4. 박자는 오디오 시계에 시각을 미리 적어 두는 예약으로 맞춘다. JavaScript 타이머는 브라우저가 바쁘면 늦는다. 리듬은 한 마디 16칸 배열이다.
5. 곡은 코드와 따로 둔 JSON 이다. `fetch` 로 받아 객체로 쓴다. `file://` 에서는 브라우저가 막으므로 서버(`server.mjs`)나 공개 주소에서 연다.

## 이번 특강 결과물

```text
[캡처 1장] https://student01.github.io/web-synth/
           곡 선택 my_song.json → ▶ 재생 중인 디스코 연주기
           머리 줄 ─ 내가 고친 제목 · BPM (예: 금요일 밤 — student01 · Am · 4/4 · 124 BPM)
           악보   ─ 지금 마디 칸이 분홍색, 표시등 옆 위치 줄 (예: A · 2/12마디 · F)
           ← 주소창이 함께 보이게 찍는다
```

- 제출은 이 캡처 **한 장**이다. 소리는 캡처되지 않으므로 화면 조건만 본다.
- `my_song.json` 은 **코드 진행만** 바꾼다. 다른 노래의 멜로디 · 가사 · 음원을 넣지 않는다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 110분 흐름

| 시간 | 내용 | 결과 |
|---|---|---|
| 1부 설명·시연 25분 | 소리는 떨림, 노드 연결 → ex01 파형 → ex02 음 높이 → ex03 엔벨로프 → ex04 화음 → ex05 필터 | 소리 부품 다섯 가지를 귀로 구별한다 |
| 2부 설명·시연 25분 | ex06 북소리 → ex07 박자(오디오 시계 예약) → ex08 리듬 배열 → ex09 JSON 과 `fetch` → 조립표 | 연주기의 줄마다 어느 ex 에서 왔는지 읽는다 |
| 실습 60분 | [실습지](lab.md#실습-60분): `web-synth` 준비 → ex03 · ex04 · ex08 바꿔 보기 → 연주기를 내 것으로 → localhost 에서 확인 → 올리기 | 공개 주소에서 내 노래 재생, 캡처 1장 |

## 준비

- **이어폰(필수)**. 실습실 30명이 스피커로 소리를 내면 아무것도 들리지 않는다. 시작 전에 PC 음량을 작게 해 둔다
- Chrome(DevTools)과 VS Code
- Node.js LTS. `node -v` 로 확인한다. 연주기는 [server.mjs](../../tools/static-server/server.mjs) 로 띄워 연다([사용 안내](../../tools/static-server/README.md)). 연주기는 `type="module"` 과 `fetch` 를 써서, 두 번 눌러 연 `file://` 화면에서는 돌지 않는다. 머리 줄이 `곡 없음` 이 되고 서버로 열라는 안내가 뜬다. Node 가 없는 PC 는 push 뒤 공개 주소에서 확인한다
- GitHub 계정. 새 저장소 `web-synth` 를 만들어 Pages 로 공개한다(2주차에 배운 순서 그대로)
- 공개 저장소 · 공개 페이지 · 캡처에 실명 · 학번 · 전화번호 · 실제 이메일을 넣지 않는다. 예시는 `student01` 이다

## 이번 특강 용어

| 한국어 | English | 中文 |
|---|---|---|
| 오디오 작업대 | AudioContext | 音频上下文 |
| 오실레이터 | oscillator | 振荡器 |
| 파형 | waveform | 波形 |
| 진동수 · 음 높이 | frequency · pitch | 频率 · 音高 |
| 게인(소리 크기) | gain | 增益 |
| 엔벨로프 | envelope | 包络 |
| 화음 · 근음 | chord · root | 和弦 · 根音 |
| 필터 · 기준 진동수 | filter · cutoff | 滤波器 · 截止频率 |
| 잡음 | noise | 噪声 |
| 템포(분당 박 수) | tempo (BPM) | 速度(每分钟拍数) |
| 예약 | scheduling | 调度 |
| 코드 진행 | chord progression | 和弦进行 |

## 비교 파일

모두 HTML 파일 하나에 `<script>` 가 들어 있다. ex09 만 곡 파일 `ex09_song.json` 을 같은 폴더에서 불러온다.
이어폰을 끼고 단추를 눌러 듣는다. 값을 바꿀 때는 저장 → 새로고침 → 다시 누르기로 차이를 듣는다. 교재 사이트 덱에서 링크를 누르면 바로 들어 볼 수 있다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_wave.html](examples/ex01_wave.html) | 1. sine / 2. square / 3. sawtooth / 4. triangle — 같은 220Hz · 1초 · 크기 0.2. 파형 그림 | 오실레이터는 같은 모양의 떨림을 계속 만든다. **모양(type)이 음색**을 정한다. 브라우저는 누르기 전에는 소리를 내 주지 않아서 `AudioContext` 는 클릭할 때 만든다 | `frequency.value` 220 → 440, `gain.value` 0.2 → 0.05 |
| [ex02_pitch.html](examples/ex02_pitch.html) | 1. A3 · A4 · A5(옥타브) / 2. C4~C5 여덟 음(키보드 A S D F G H J K). 단추에 진동수가 적힌다 | 음 높이 = 1초에 떨리는 횟수. **한 옥타브 = 2배, 반음 = 2^(1/12)배**. MIDI 번호(가운데 도 C4 = 60, 라 A4 = 69 = 440Hz)로 계산한다 | `midiToFreq` 의 440 을 432 로, 버튼의 `data-midi` |
| [ex03_envelope.html](examples/ex03_envelope.html) | sawtooth 220Hz 로 1. 켰다 끄기만 / 2. 짧게 / 3. 길게 / 4. 천천히 커지기 / 5. 2번을 exponential 로. 크기 변화 그림 | 소리 크기가 시간에 따라 변하는 모양(엔벨로프)이 성격을 정한다. 0 에서 시작해 0 으로 끝나지 않으면 '딱' 소리가 난다. exponential 은 귀에 고르게 줄어든다 | attack · release 숫자, 2번과 5번 비교 |
| [ex04_chord.html](examples/ex04_chord.html) | 1. 곡의 코드 Am · Dm · G · C · F / 2. C vs Cm, A vs Am / 3. Am 을 차례로(아르페지오) | 화음 = 오실레이터 여러 개를 같은 시각에. 근음에서 몇 반음 위를 함께 치나: 장 [0, 4, 7], 단 [0, 3, 7] — **가운데 음 하나가 반음 차이**. 시각을 조금씩 늦추면 아르페지오 | `SHAPES` 에 `7: [0, 4, 7, 10]` 더하기, 아르페지오 간격 0.15 |
| [ex05_filter.html](examples/ex05_filter.html) | Am sawtooth 화음을 lowpass 로 1. 없음(20000Hz) / 2. 3000 / 3. 800 / 4. 200 / 5. 800 + Q 15 / 6. 200 → 4000 쓸기. 주파수 그림 | sawtooth 는 높은 성분이 많다. lowpass 는 기준(cutoff)보다 높은 쪽을 깎아 **어둡게** 한다. 기준을 움직이면 쓸기 소리가 난다 | cutoff, Q, 쓸기 시간 |
| [ex06_drums.html](examples/ex06_drums.html) | 킥 1. 사인파 50Hz 그대로 / 2. 150 → 45Hz, 스네어 3. 잡음만 / 4. 잡음 + 짧은 톤, 하이햇 5. 닫힘 0.05초 / 6. 열림 0.3초 | 북소리도 오실레이터 · 잡음 + 아주 짧은 엔벨로프다. **높이가 빠르게 떨어지는 사인파 = 킥**, **잡음의 높은 쪽 = 하이햇**, 길이가 닫힘 · 열림을 가른다 | 150 · 45 · 0.12, highpass 7000, 길이(decay) |
| [ex07_timing.html](examples/ex07_timing.html) | 1. `setTimeout` 으로 16번 치기 / 2. 오디오 시계에 16번 예약하기, "브라우저를 바쁘게" 체크 | 한 박 = 60/BPM 초, 16분음표 = 그 4분의 1(109 BPM → 0.550 / 0.138초). **JavaScript 타이머는 브라우저가 바쁘면 늦는다. 오디오 시계에 시각을 미리 적어 두면 정확하다** | BPM, 바쁘게 체크 |
| [ex08_pattern.html](examples/ex08_pattern.html) | 1. 디스코 / 2. 록 / 3. 비우기 — 줄 4개(kick · snare · hat · open) × 16칸 체크 상자, 아래에 배열이 바로 보인다. ▶ 재생(109 BPM) | **리듬은 배열이다**(16칸 중 1 인 칸에서 친다). 디스코 = 박마다 킥(four on the floor) + 2 · 4박 스네어 + 엇박 열린 하이햇 | 칸 누르기, 프리셋 바꾸기 |
| [ex09_fetch_song.html](examples/ex09_fetch_song.html) + [ex09_song.json](examples/ex09_song.json) | 같은 페이지를 `file://` 로 열 때 / `http://localhost:8000/`(server.mjs)로 열 때. 표의 식 6개, 마디 펼치기 | **곡은 데이터다**. 코드와 따로 둔 JSON 을 `fetch` 로 받아 객체로 쓴다. `file://` 에서는 브라우저가 막는다 → 서버로 연다 | json 의 코드 · bpm 을 바꾸고 다시 불러오기 |

만들기는 마지막 하나, [`examples/build/`](examples/build/) 의 디스코 연주기뿐이다. 새 문법은 없다. 위 부품을 모은 것이다. 줄마다 어느 ex 에서 왔는지는 [예제 설명의 조립표](examples/README.md#조립표--연주기의-부분은-어느-ex-에서-본-것인가)에 있다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/synthesizer/index.html — 덱의 예제 링크를 누르면 비교 파일과 연주기가 바로 열린다
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md) — 비교 파일 9개(ex09 는 JSON 까지)와 `build/`
- 디스코 연주기(`build/` 여섯 파일): [index.html](examples/build/index.html) · [main.css](examples/build/main.css) · [index.js](examples/build/index.js) · [synth.js](examples/build/synth.js) · [only_you.json](examples/build/only_you.json) · [my_song.json](examples/build/my_song.json)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/synthesizer

## 안전과 저작권

- **이어폰 음량을 먼저 줄인다.** 단추마다 크기가 다르다. ex05 의 5번(Q 15), ex06 의 킥, ex08 재생은 다른 단추보다 훨씬 크다. 작게 시작해서 한 단추씩 듣는다.
- 곡 데이터는 **코드 진행만** 담는다. 멜로디 · 가사 · 음원은 교재와 예제에 넣지 않았다. `only_you.json` 의 제목 · 가수는 곡 정보(사실)이고, 담긴 것은 마디마다의 코드 이름뿐이다.
- 학생 과제도 **코드 진행만** 바꾼다. `my_song.json` 에 다른 노래의 멜로디 · 가사를 적거나 음원 파일을 저장소에 올리지 않는다.
- 멜로디를 더해 보고 싶으면 **내가 지은 멜로디**만 쓴다. 녹음해서 음원 파일로 만드는 것은 이 특강의 범위 밖이다.
- 공개 저장소 · 캡처에 실명 · 학번 · 전화번호 · 실제 이메일을 넣지 않는다.

## 완료 기준

- [ ] 새 저장소 `web-synth` 맨 위에 연주기 여섯 파일과 `server.mjs` 가 있고, Pages 가 켜져 있다.
- [ ] 비교 파일 ex03 · ex04 · ex08 에서 값을 하나 이상씩 바꿔 들어 봤다.
- [ ] 연주기를 내 것으로 바꿨다: ① `my_song.json` 의 제목 · 코드 · bpm ② `PATTERNS.disco` 한 줄 ③ `playTone` 에 넘기는 소리 하나 — 셋 중 둘 이상.
- [ ] `node server.mjs` 로 연 `http://localhost:8000/` 에서 my_song.json 이 재생되고, Console 에 빨간 줄이 없다(`favicon.ico` 404 한 줄은 괜찮다).
- [ ] 공개 주소 `https://student01.github.io/web-synth/` 에서 my_song.json 을 재생하는 캡처 1장을 제출한다.

## 특강이 끝나면

- 연주기에서 정규 수업의 문법이 쓰인 곳: `fetch` · JSON(12주차)은 `loadSong`, 배열(10주차)은 `PATTERNS` 와 `bars`, 객체(11주차)는 `song.track_info` 와 마디 하나 `{ section, chord, midis }`, `createElement` · `append`(10주차)는 악보의 구간 줄과 마디 칸이다.
- 더 해 볼 것: 아르페지오 층을 켜고 내 노래에 맞게 고치기, 리듬 하나 더(`PATTERNS.funk`), 멜로디 층을 직접 만들기(내가 지은 멜로디만), ex02 키보드로 연주기 위에서 연주하기. 방법은 [실습지의 먼저 끝났다면](lab.md#먼저-끝났다면)에 있다.
- `web-synth` 저장소는 남겨 두어도 된다. 정규 주차 과제와는 따로다.

## 공식 참고 자료

- [Web Audio API — MDN](https://developer.mozilla.org/ko/docs/Web/API/Web_Audio_API)
- [Web Audio API 사용하기 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Web_Audio_API/Using_Web_Audio_API)
- [Web Audio API 의 기본 개념 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Web_Audio_API/Basic_concepts_behind_Web_Audio_API)
- [AudioContext — MDN](https://developer.mozilla.org/ko/docs/Web/API/AudioContext)
- [OscillatorNode — MDN(영문)](https://developer.mozilla.org/en-US/docs/Web/API/OscillatorNode)
- [GainNode — MDN(영문)](https://developer.mozilla.org/en-US/docs/Web/API/GainNode)
- [BiquadFilterNode — MDN](https://developer.mozilla.org/ko/docs/Web/API/BiquadFilterNode)
- [AudioParam.linearRampToValueAtTime() — MDN](https://developer.mozilla.org/ko/docs/Web/API/AudioParam/linearRampToValueAtTime)
- [AudioParam.exponentialRampToValueAtTime() — MDN](https://developer.mozilla.org/ko/docs/Web/API/AudioParam/exponentialRampToValueAtTime)
- [AnalyserNode — MDN](https://developer.mozilla.org/ko/docs/Web/API/AnalyserNode)
- [Fetch 사용하기 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- [JSON 으로 작업하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/JSON)
- [JavaScript 모듈 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Modules)
- [미디어와 Web Audio API 의 자동 재생 — MDN](https://developer.mozilla.org/ko/docs/Web/Media/Guides/Autoplay)
- [오디오 예약: A tale of two clocks — web.dev(영문)](https://web.dev/articles/audio-scheduling)
