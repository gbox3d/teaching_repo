[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/synthesizer)

# 특강 예제 — 소리 부품 비교 파일 9개와 디스코 연주기

이 폴더의 `exNN_*.html` 은 **파일 하나 = 개념 하나**다. 파일마다 같은 일을 다르게 한 **형제**(1 · 2 · 3번 …)를 단추로 나란히 놓는다.
결과는 **귀**(이어폰)와 **화면**(그림 · 글자) 두 곳에서 본다. 단추의 번호가 코드의 형제 번호와 같다. 값을 바꾸고 저장 → 새로고침 → 단추를 다시 눌러 무엇이 달라지는지 듣는다.
만들기는 마지막 하나, [`build/`](build/) 의 디스코 연주기뿐이다.

각 파일은 단일 HTML 이고 `<script>` 가 안에 있다. ex09 만 [ex09_song.json](ex09_song.json) 을 같은 폴더에서 `fetch` 로 불러온다.
교재 사이트 덱에서 링크를 누르면 바로 들어 볼 수 있다. 값을 바꿔 볼 파일만 저장소 `web-synth` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 가져오는 방법은 [따라하기 3단계](../walkthrough.md#3-비교-파일-받는-법)에 있다.
**이어폰을 끼고 음량을 작게 시작한다.** ex05 의 5번, ex06 의 킥, ex08 재생은 다른 단추보다 훨씬 크다.

## 비교 파일

| 파일 | 열면 보이는 것 · 들리는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_wave.html](ex01_wave.html) | 단추 4개(sine · square · sawtooth · triangle). 처음 누르면 `AudioContext 상태: running`. 같은 높이(220Hz)의 소리가 1초 나고, 아래 검은 칸에 지금 나가는 모양이 그려진다. sawtooth 는 톱니 모양 | 오실레이터는 같은 모양의 떨림을 계속 만든다. **모양(type)이 음색**을 정한다. 브라우저는 누르기 전에는 소리를 내 주지 않으므로 `new AudioContext()` 는 클릭할 때 만든다 | 33행 `osc.frequency.value = 220` 을 440 으로(한 옥타브 위, 그림의 물결이 촘촘해진다), 34행 `amp.gain.value = 0.2` 를 0.05 로 |
| [ex02_pitch.html](ex02_pitch.html) | 단추에 진동수가 적혀 있다: `A3 (220.0 Hz)` · `A4 (440.0 Hz)` · `A5 (880.0 Hz)`, `C4 도 (261.6 Hz)` · `D4 레 (293.7 Hz)` · `E4 미 (329.6 Hz)` · `F4 파 (349.2 Hz)` · `G4 솔 (392.0 Hz)` · `A4 라 (440.0 Hz)` · `B4 시 (493.9 Hz)` · `C5 도 (523.3 Hz)`. 누르면 아래에 `MIDI 69 → 440.0 Hz` 처럼 적힌다 | 음 높이 = 1초에 떨리는 횟수. **한 옥타브 = 2배, 반음 = 2^(1/12)배**. MIDI 번호(가운데 도 C4 = 60, 라 A4 = 69 = 440Hz)로 계산한다 | 30행 `midiToFreq` 의 440 을 432 로(단추 숫자가 모두 바뀐다), 11~22행 단추의 `data-midi` |
| [ex03_envelope.html](ex03_envelope.html) | 형제 다섯 줄의 표와 재생 단추. 모두 220Hz 사인파(파형을 정하지 않았다). 누를 때마다 아래 그림에 크기 변화(가로 2초)가 그려진다. 1번은 시작과 끝에 '딱', 4번은 1.2초 동안 커진다 | 소리 크기가 시간에 따라 변하는 모양(엔벨로프)이 성격을 정한다. 0 에서 시작해 0 으로 끝나지 않으면 '딱' 소리가 난다. exponential 은 귀에 고르게 줄어든다. exponential 은 0 에 닿지 못해서 0.0001 까지 줄인다 | 50~54행 `play(attack, hold, release, 곡선)` 의 숫자, 2번(linear)과 5번(exponential) 번갈아 듣기 |
| [ex04_chord.html](ex04_chord.html) | 누른 코드가 `Am = MIDI 57 · 60 · 64 — 근음에서 0 · 3 · 7 반음 위` 처럼 적힌다. Dm 62 · 65 · 69, G 55 · 59 · 62, C 60 · 64 · 67, F 65 · 69 · 72, Cm 60 · 63 · 67, A 57 · 61 · 64 | 화음 = 오실레이터 여러 개를 같은 시각에. 근음에서 몇 반음 위를 함께 치나: 장 [0, 4, 7], 단 [0, 3, 7] — **가운데 음 하나가 반음 차이** | 26행 `SHAPES` 에 `7: [0, 4, 7, 10]` 더하고 G7 단추 만들기 |
| [ex05_filter.html](ex05_filter.html) | 같은 sawtooth 220Hz 2초. 아래 막대 그림(왼쪽이 낮은 소리)에서 1번은 한 음인데 막대가 같은 간격으로 오른쪽 끝까지 줄지어 선다(220Hz 의 2배 · 3배 … 높이). 1 → 4번으로 갈수록 오른쪽 막대가 사라지고 소리가 어두워진다. 4번(200Hz)은 소리도 작아진다. 5번(Q 15)은 기준 근처가 울려 다른 단추보다 크다. 6번은 2초 동안 밝아진다 | sawtooth 는 높은 성분이 많다. lowpass 는 기준(cutoff)보다 높은 쪽을 깎아 **어둡게** 한다. 기준을 움직이면 쓸기 소리가 난다 | 11~14행 `data-cutoff`, 50행 Q `15`, 53행 쓸기 끝 `4000` 과 시간 `+ 2` |
| [ex06_drums.html](ex06_drums.html) | 킥(쿵) · 스네어(딱) · 하이햇(칙) 단추가 둘씩. 킥 1번은 높이가 그대로인 50Hz, 2번은 150 → 45Hz 로 떨어지는 '퍽'. 스네어 4번은 3번 잡음에 190Hz 짧은 톤(몸통)이 더해진다. 하이햇 5번은 0.05초, 6번은 0.3초 | 북소리도 오실레이터 · 잡음 + 아주 짧은 엔벨로프다. **높이가 빠르게 떨어지는 사인파 = 킥**, **잡음의 높은 쪽 = 하이햇**, 길이가 닫힘 · 열림을 가른다 | 78행 `kick(150, 45)`, 40행 떨어지는 시간 0.12, 81 · 82행 highpass 7000 과 길이 0.05 · 0.3 |
| [ex07_timing.html](ex07_timing.html) | 109 BPM → `한 박 0.550초, 16분음표 한 칸 0.138초`. 단추를 누르면 '틱' 16번 뒤 `간격(ms): … — 가장 짧은 …, 가장 긴 …`. 안 바쁠 때 1번 133~144, 2번 138(페이지를 열고 처음 누른 1번은 오디오 시계가 막 시작해 첫 간격이 짧게 나올 수 있다). "바쁘게" 를 켜면 1번은 139~203 으로 들쭉날쭉, 2번은 그대로 138 | 한 박 = 60/BPM 초, 16분음표 = 그 4분의 1. **JavaScript 타이머는 브라우저가 바쁘면 늦는다. 오디오 시계에 시각을 미리 적어 두면 정확하다**(25ms 마다 깨어나 앞으로 0.1초 안의 칸을 예약) | BPM 칸, "바쁘게" 체크 상자, 84행 붙잡는 시간 60(ms) |
| [ex08_pattern.html](ex08_pattern.html) | 줄 4개(kick · snare · hat · open) × 16칸 체크 상자(박의 첫 칸에 테두리), 아래에 배열 네 줄 `kick : [1, 0, 0, 0, …]`. 칸을 누르면 배열이 바로 바뀐다. 록 kick 은 `[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]`. ▶ 재생은 109 BPM 으로 되풀이, ■ 정지 | **리듬은 배열이다**(16칸 중 1 인 칸에서 친다). 디스코 = 박마다 킥(four on the floor) + 2 · 4박 스네어 + 엇박 열린 하이햇 | 칸 누르기, 1 · 2 · 3번 프리셋, 27~36행 `PRESETS`, 135행 `60 / 109 / 4` 의 109 |
| [ex09_fetch_song.html](ex09_fetch_song.html) | 단추 `ex09_song.json 불러오기`. http 로 열면 표 `연습곡 / 109 / 2 / A / Am / 2`, 펼침 `A:Am A:F A:C A:G B:Dm B:Am`, `불러왔다 — 주소: http://…`. 두 번 눌러 연 `file://` 은 `불러오지 못했다: Failed to fetch — 주소가 file:// 이면 브라우저가 막는다. …` 와 Console 의 `Access to fetch at 'file:///…/ex09_song.json' from origin 'null' has been blocked by CORS policy: …` | **곡은 데이터다**. 코드와 따로 둔 JSON 을 `fetch` 로 받아(`response.json()` 이 글자 → 객체) 점과 대괄호로 꺼내 쓴다. `file://` 에서는 브라우저가 막는다 → 서버로 연다 | `ex09_song.json` 을 고치고 다시 불러오기, 30~35행 표의 식 |
| [ex09_song.json](ex09_song.json) | ex09 가 불러오는 곡 데이터. `track_info`(연습곡 · student01 · Am · 4/4 · 109) + `sections`(A 구간 4마디 Am F C G, B 구간 2마디 Dm Am) | 연주기의 `only_you.json` · `my_song.json` 과 같은 모양이다. 객체 안의 배열 안의 객체. 코드 이름만 담는다 | 코드 이름 · bpm 바꾸기, B 구간에 마디 하나 더하기(앞 마디 `}` 뒤 쉼표) |

### 파일 안의 모양

형제는 같은 함수를 다른 값으로 부르는 것이다. [ex03_envelope.html](ex03_envelope.html)에서 인용:

```js
document.getElementById('b1').addEventListener('click', function () { play(0, 0.6, 0, 'linear'); });
document.getElementById('b2').addEventListener('click', function () { play(0.005, 0.02, 0.3, 'linear'); });
document.getElementById('b3').addEventListener('click', function () { play(0.3, 0.6, 0.8, 'linear'); });
document.getElementById('b4').addEventListener('click', function () { play(1.2, 0.2, 0.3, 'linear'); });
document.getElementById('b5').addEventListener('click', function () { play(0.005, 0.02, 0.3, 'exp'); });
```

숫자 넷은 attack(커지는 시간) · hold(유지) · release(사라지는 시간) · 줄이는 곡선이다. 2번과 5번은 숫자가 같고 곡선만 다르다. 그래서 둘을 번갈아 들으면 linear 와 exponential 의 차이만 들린다.

연주기의 박자를 맞추는 방법은 [ex07_timing.html](ex07_timing.html)의 2번이다.

```js
// 2. 25ms 마다 깨어나 앞으로 0.1초 안에 올 칸의 '시각'을 오디오 시계에 적어 둔다
//    소리는 오디오 쪽이 그 시각에 정확히 낸다. JavaScript 가 조금 늦게 깨어나도 상관없다
document.getElementById('b2').addEventListener('click', function () {
    if (!ctx) ctx = new AudioContext();
    const times = [];
    let next = ctx.currentTime + 0.05;
    const timer = setInterval(function () {
        while (next < ctx.currentTime + 0.1 && times.length < 16) {
            click(next);
            times.push(next);
            next += secondsPerStep();
        }
        if (times.length === 16) {
            clearInterval(timer);
            report(times);
        }
    }, 25);
});
```

`click(next)` 는 "지금" 이 아니라 `next` 시각에 소리가 나도록 예약한다. 1번은 `setTimeout` 이 깨어난 그때 `ctx.currentTime`(지금)에 친다. 그래서 브라우저가 바쁘면 1번만 간격이 흔들린다.
연주기 `index.js` 의 `tick`(89~95행)이 이 `while` 과 같은 모양이다.

## `build/` — 디스코 연주기

[`build/`](build/) 는 실습을 시작할 때 저장소 `web-synth` 맨 위에 받는 연주기 **여섯 파일 전체**다. 학생은 이 위에서 `my_song.json` · `PATTERNS` · `playTone` 에 넘기는 값을 바꾼다. 비교 파일을 둘 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않았다.
연주기는 `fetch` 와 `<script type="module">` 을 쓰므로 `node server.mjs` 로 띄운 `http://localhost:8000/` 이나 공개 주소에서 연다. 두 번 눌러 연 `file://` 화면에서는 모듈이 돌지 않는다. `index.html` 63~71행의 보통 `<script>` 가 머리 줄을 `곡 없음` 으로, 아래 문구를 `주소가 file:// 입니다. 연주기는 서버로 엽니다: 이 폴더에서 node server.mjs 를 띄우고 http://localhost:8000/ 을 여세요.` 로 바꿔 알려 준다.

| `build/` 파일 | 내 `web-synth` 의 위치 | 따라하기 단계 |
|---|---|---|
| [index.html](build/index.html) | `index.html` | [2단계](../walkthrough.md#2-연주기-여섯-파일-받기와-재생) 받기. 화면 뼈대라 고치지 않는다(먼저 끝났다면 곡 · 리듬 선택지를 더한다) |
| [main.css](build/main.css) | `main.css` | 2단계 받기. 고치지 않는다 |
| [index.js](build/index.js) | `index.js` | 2단계 받기, [5단계](../walkthrough.md#5-리듬-배열-고치기) `PATTERNS.disco` 한 줄, [6단계](../walkthrough.md#6-소리-하나-고치기) `playTone` 에 넘기는 값 |
| [synth.js](build/synth.js) | `synth.js` | 2단계 받기, 6단계(킥 · 하이햇을 바꿀 때) |
| [only_you.json](build/only_you.json) | `only_you.json` | 2단계 받기. 손대지 않는다. 곡 정보와 4구간 28마디의 코드 진행만 담았다 |
| [my_song.json](build/my_song.json) | `my_song.json` | 2단계 받기, [4단계](../walkthrough.md#4-my_songjson-고치기) 내 노래로 고친다(코드 진행만) |

### 조립표 — 연주기의 부분은 어느 ex 에서 본 것인가

연주기에는 새로 배우는 소리 원리가 없다. 비교 파일에서 본 것을 한 곳에 모은 것이다.

| 연주기의 부분 | 어느 ex 에서 본 것 |
|---|---|
| 재생을 처음 누를 때 `new AudioContext()`(`index.js` 115행) | [ex01](ex01_wave.html) |
| `midiToFreq`(`synth.js` 6~8행) | [ex02](ex02_pitch.html) |
| `playTone` 의 엔벨로프 — 0.0001 에서 시작, exponential 로 줄이기(`synth.js` 61~64행) | [ex03](ex03_envelope.html) 1 · 5번 |
| `playTone` 의 `osc.type`(`synth.js` 56행), 화면의 코드 파형 선택 | [ex01](ex01_wave.html) |
| `chordToMidis`(`synth.js` 23~34행) · 코드 층(음 수만큼 동시에, `index.js` 76~80행) | [ex04](ex04_chord.html) |
| 아르페지오 층(칸마다 코드 음을 차례로, `index.js` 81~84행) | [ex04](ex04_chord.html)(코드 음) + [ex08](ex08_pattern.html)(16칸 중 몇 번째 칸인가 — `i % notes.length` 로 음을 고른다) |
| `playTone` 의 lowpass(`synth.js` 58 · 59행), 화면의 필터 슬라이더 | [ex05](ex05_filter.html) |
| `playKick` · `playSnare` · `playHat` · `createNoise`(`synth.js` 37~108행) | [ex06](ex06_drums.html) |
| `secondsPerStep` · `tick`(오디오 시계 예약, `index.js` 42~44 · 89~95행) | [ex07](ex07_timing.html) 2번 |
| `PATTERNS` · `scheduleStep` 의 `p.kick[i]`(`index.js` 6~25 · 68행), 줄마다 16칸인지 확인하는 `checkPattern`(51~57행) | [ex08](ex08_pattern.html) |
| `loadSong`(`fetch` → 마디 펼치기, `index.js` 145~183행) | [ex09](ex09_fetch_song.html) |
| 화면(패널 · 악보 칸) | 4주차 flex(`.panel` 의 `flex-wrap` · `gap`), 10주차 `createElement` · `textContent` · `append` |

소리 원리가 가장 많이 모인 곳은 `playTone` 이다. [build/synth.js](build/synth.js)에서 인용:

```js
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
```

`osc.type` 은 ex01, `filter` 는 ex05, `amp.gain` 네 줄은 ex03 이다. `note` 는 객체 하나로 값을 받는다. 넘기지 않은 값은 `||` 뒤의 기본값을 쓴다.
그래서 `index.js` 74행의 베이스는 `type: 'square', cutoff: 700` 을, 78행의 코드 층은 화면의 파형과 필터 값을 넘긴다. 같은 함수가 층마다 다른 소리를 낸다.
`time` 이 `ctx.currentTime` 기준의 미래 시각이라는 점이 ex07 2번과 같다. `tick` 이 0.1초 앞의 칸을 예약할 때 그 시각을 그대로 넘긴다.

## 공식 참고 자료

- [Web Audio API — MDN](https://developer.mozilla.org/ko/docs/Web/API/Web_Audio_API)
- [OscillatorNode — MDN(영문)](https://developer.mozilla.org/en-US/docs/Web/API/OscillatorNode)
- [GainNode — MDN(영문)](https://developer.mozilla.org/en-US/docs/Web/API/GainNode)
- [BiquadFilterNode — MDN](https://developer.mozilla.org/ko/docs/Web/API/BiquadFilterNode)
- [AudioParam.exponentialRampToValueAtTime() — MDN](https://developer.mozilla.org/ko/docs/Web/API/AudioParam/exponentialRampToValueAtTime)
- [AnalyserNode — MDN](https://developer.mozilla.org/ko/docs/Web/API/AnalyserNode)
- [Fetch 사용하기 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- [JavaScript 모듈 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Modules)
