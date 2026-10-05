---
marp: true
theme: default
paginate: true
header: "Web Programming · Special"
footer: "Building a Web Synthesizer · Compare sound parts, then assemble a disco player at the end"
---

# Building a Web Synthesizer

Today you make sound in the browser, and at the end you assemble a **disco player**.

- How: hear each sound part in **9 comparison files**. Then read the player as those parts put together.
- **Earphones are required.** If the whole lab plays through speakers, nobody hears anything.
- The lab is **changing values**. Say what will change first, then listen.
- Result: one screenshot of the public address of a new repository `web-synth`, playing **your edited `my_song.json`**.

Song data holds **chord progressions only**. No melody, lyrics or audio files, in the materials or the assignment.

---

# Part 1 — Making Sound

`25 min explanation & demo`

1. Sound is air vibrating, and the browser makes that vibration
2. ex01 — Waveforms: same pitch, different shape
3. ex02 — Pitch: an octave is ×2, a semitone is ×2^(1/12)
4. ex03 — Envelope: how loudness changes over time
5. ex04 — Chords: how many semitones above the root you play together
6. ex05 — Filter: cutting the high parts makes it darker

---

## Part 1 · 0–3 min — Sound Is Vibrating Air, Made by the Browser

```text
[click] → new AudioContext()  ← no sound until the user clicks
oscillator → filter → gain → speaker (ctx.destination)
oscillator = type (shape) · frequency (pitch)  ← ex01 · ex02
gain = change gain over time  ← ex03
filter = lowpass · cutoff (cut the high side)  ← ex05
```

- Sound is air vibrating. Vibrations per second (Hz) are pitch, the shape is tone, the width is loudness.
- The Web Audio API joins parts (nodes) with `connect`. Each comparison file swaps one part.
- The browser plays no sound until the user clicks. Create `new AudioContext()` on a click.

**Sound is nodes joined: vibration (oscillator) → cut (filter) → loudness (gain) → speaker.**

---

## Part 1 · 3–7 min — ex01 Waveforms: Same Pitch, Different Shape

[examples/ex01_wave.html](examples/ex01_wave.html)
Siblings: 1. sine / 2. square / 3. sawtooth / 4. triangle (220Hz · 1 s · 0.2 are the same)

```js
const osc = ctx.createOscillator();  // keeps making the same-shaped vibration
osc.type = type;        // 'sine' | 'square' | 'sawtooth' | 'triangle'
osc.frequency.value = 220;           // vibrates 220 times per second
amp.gain.value = 0.2;
```

- First press: `AudioContext 상태: running` (AudioContext state). The picture is the sound going out.
- Try changing: `frequency.value` 220 → 440, `gain.value` 0.2 → 0.05.

**An oscillator keeps making the same-shaped vibration. The shape (type) sets the tone.**

---

## Part 1 · 7–11 min — ex02 Pitch: Octave ×2, Semitone ×2^(1/12)

[examples/ex02_pitch.html](examples/ex02_pitch.html)
Siblings: 1. A3 · A4 · A5 (three A's) / 2. eight notes C4–C5 (keys A S D F G H J K)

```js
// MIDI number: a number for each piano key. Middle C (C4) = 60, A4 = 69
function midiToFreq(midi) {
    return 440 * 2 ** ((midi - 69) / 12);    // A4 = 440Hz
}
```

- Buttons show frequencies: A3 `220.0` · A4 `440.0` · A5 `880.0`. Key H → `MIDI 69 → 440.0 Hz`.
- Try changing: 440 on line 30 → 432 (all numbers change). A button's `data-midi`.

**Pitch = vibrations per second. Octave ×2, semitone ×2^(1/12). Computed from MIDI numbers.**

---

## Part 1 · 11–16 min — ex03 Envelope: How Loudness Changes Over Time

[examples/ex03_envelope.html](examples/ex03_envelope.html)
Siblings: 1. on/off only / 2. short / 3. long / 4. slow fade-in / 5. No. 2 as exponential

```js
amp.gain.setValueAtTime(0.0001, t);
amp.gain.linearRampToValueAtTime(PEAK, t + attack);   // attack
amp.gain.setValueAtTime(PEAK, t + attack + hold);     // hold
amp.gain.exponentialRampToValueAtTime(0.0001, t + attack + hold + release);
```

- No. 1 clicks at start and end. No. 2 plucks, No. 3 pads. The picture is the loudness change.
- Try changing: alternate No. 2 and No. 5 (same numbers). attack · release on lines 51–55.

**The envelope (loudness over time) sets the sound's character. Start at 0 and end at 0, or it clicks.**

---

## Part 1 · 16–21 min — ex04 Chords: Semitones Above the Root

[examples/ex04_chord.html](examples/ex04_chord.html)
Siblings: 1. song chords Am · Dm · G · C · F / 2. C vs Cm, A vs Am / 3. `Am 차례로` (Am in turn)

```js
const SHAPES = { '': [0, 4, 7], m: [0, 3, 7] };   // semitones above the root
for (const midi of midis) note(midi, ctx.currentTime, 1.2);   // same time
note(midis[i % 3] + 12, ctx.currentTime + i * 0.15, 0.14);  // 0.15 s later each
```

- Am shows `MIDI 57 · 60 · 64`. C is 60 · 64 · 67, Cm is 60 · 63 · 67 — only the middle differs.
- Try changing: add `7: [0, 4, 7, 10]` to `SHAPES` and play G7. Arpeggio gap 0.15 → 0.1.

**Chord = several oscillators at once. Major [0, 4, 7], minor [0, 3, 7] — the middle differs by one.**

---

## Part 1 · 21–25 min — ex05 Filter: Cut the Highs, Get Darker

[examples/ex05_filter.html](examples/ex05_filter.html)
Siblings: Am chord (sawtooth) + lowpass 1. none / 2. 3000 / 3. 800 / 4. 200 / 5. Q 15 / 6. sweep

```js
filter.type = 'lowpass';   // cuts above the cutoff, lets the low side through
filter.frequency.value = cutoff;
filter.Q.value = q;        // how much to boost around the cutoff
filter.frequency.exponentialRampToValueAtTime(4000, ctx.currentTime + 2);
```

- From 1 to 4 it gets darker, and the right (high) bars vanish. No. 5 is louder than the others.
- Try changing: a button's `data-cutoff`, the Q 15 of No. 5, the 2 s sweep time of No. 6.

**lowpass cuts above the cutoff and darkens the sound. Moving the cutoff makes a sweep.**

**Explanation total: 3+4+4+5+5+4 = 25 min**

---

# Part 2 — Rhythm and Song

`25 min explanation & demo`

1. ex06 — Drums: a falling sine wave and noise
2. ex07 — Timing: schedule on the audio clock, not a timer
3. ex08 — Rhythm is an array: hit on the cells that are 1, out of 16
4. ex09 — A song is data: get JSON with fetch
5. Assembly — the disco player is the parts of ex01–ex09 put together

---

## Part 2 · 0–5 min — ex06 Drums: A Falling Sine Wave and Noise

[examples/ex06_drums.html](examples/ex06_drums.html)
Siblings: kick 1. steady / 2. falling · snare 3. noise / 4. + tone · hi-hat 5. closed / 6. open

```js
// pitch dropping fast makes a 'thump'
osc.frequency.exponentialRampToValueAtTime(toFreq, t + 0.12);
for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
filter.type = 'highpass';   // cuts below this pitch
```

- Kick 1 · 2 are the same sine; only No. 2 drops 150 → 45Hz in 0.12 s. Hi-hat 5 · 6 differ in length only.
- Try changing: 150 · 45 · 0.12 in No. 2, the hi-hat's highpass 7000, length (decay).

**Drums are oscillators · noise + a very short envelope. Falling sine = kick, high noise = hi-hat.**

---

## Part 2 · 5–10 min — ex07 Timing: Audio Clock, Not a Timer

[examples/ex07_timing.html](examples/ex07_timing.html)
Siblings: 1. 16 hits by setTimeout / 2. 16 hits on the audio clock — "바쁘게" (busy) box

```js
return 60 / bpm / 4;                // beat = 60/BPM s, a 16th = 1/4 of it
if (times.length < 16) setTimeout(hit, secondsPerStep() * 1000);   // 1.
while (next < ctx.currentTime + 0.1 && times.length < 16) {        // 2.
    click(next);                    // schedule it to sound at that time
```

- 109 BPM → beat `0.550` s, step `0.138` s. Not busy: No. 1 139–144ms, No. 2 138ms.
- Busy: No. 1 jumps 155–203ms, No. 2 stays 138ms. Try changing: BPM, busy box.

**JS timers run late when the browser is busy. Times set ahead on the audio clock are exact.**

---

## Part 2 · 10–15 min — ex08 Rhythm Is an Array: Disco Kick and Hat

[examples/ex08_pattern.html](examples/ex08_pattern.html)
Siblings: 1. disco / 2. rock / 3. clear — 4 rows (kick · snare · hat · open) × 16 cells, 109 BPM

```text
kick : [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]   ← kick every beat
snare: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]   ← beats 2 · 4
open : [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]   ← off-beat
if (pattern.kick[i]) kick(t);   ← if cell i is 1, schedule at that time
```

- Click a cell: the array below changes at once. While playing, it sounds new from its next turn.
- Try changing: turn off beats 2 · 4 in disco's kick row. What's gone? Compare rock's kick.

**Rhythm is an array (hit the 1s of 16). Disco = kick each beat + snare 2 · 4 + off-beat open hat.**

---

## Part 2 · 15–19 min — ex09 A Song Is Data: Get JSON with fetch

[examples/ex09_fetch_song.html](examples/ex09_fetch_song.html) · [ex09_song.json](examples/ex09_song.json)
Siblings: open the same page 1. as `file:///…` / 2. as `http://localhost:8000/`

```js
const response = await fetch('ex09_song.json');   // 'request' a file in the same folder
const song = await response.json();               // text (JSON) → object
document.getElementById('v1').innerText = song.track_info.title;
```

- http: table `연습곡 / 109 / 2 / A / Am / 2` (practice song), bars `A:Am A:F A:C A:G B:Dm B:Am`.
- file: `불러오지 못했다: Failed to fetch — …` (could not load), red CORS line in Console.

**A song is data. `fetch` a separate JSON, use it as an object. `file://` is blocked; use a server.**

---

## Part 2 · 19–25 min — Assembly: Disco Player, Then the Lab

[index.html](examples/build/index.html) · [main.css](examples/build/main.css) · [index.js](examples/build/index.js) · [synth.js](examples/build/synth.js) · [only_you.json](examples/build/only_you.json) · [my_song.json](examples/build/my_song.json)

```text
new AudioContext() ← ex01    playTone's envelope ← ex03 · lowpass ← ex05
midiToFreq ← ex02            playKick · playSnare · playHat ← ex06
chordToMidis ← ex04          chord layer ← ex04 1·2 · arpeggio layer ← ex04 3
PATTERNS ← ex08              secondsPerStep · tick ← ex07 · loadSong ← ex09
```

[Lab](lab.md#실습-60분) · [Walkthrough](walkthrough.md) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/synthesizer)

1. [server.mjs](../../tools/static-server/server.mjs) · the six player files in `web-synth` → `node server.mjs` → ▶
2. Change ex03 · ex04 · ex08, listen → 2+ of `my_song.json` · `PATTERNS` · `playTone`
3. Upload to a new `web-synth` repository as in Week 2 → screenshot the public address

**Explanation total: 5+5+5+4+6 = 25 min**

---

## Submitting

After the special lecture, submit **one** screenshot.

```text
https://student01.github.io/web-synth/
곡 (song) select my_song.json → ▶ 재생 (play)
Header: your edited title · BPM   (e.g., Friday Night — student01 · Am · 4/4 · 124 BPM)
Sheet: current bar cell in pink, position line by the lights   (e.g., A · 2/12마디 · F = bar 2 of 12)
```

- Sound is not captured. Only the screen conditions (your title · BPM, highlighted bar) are checked.
- Include the address bar. Don't show your real name, student ID or real email.

---

## After the Special Lecture

Where regular-course syntax is used inside the player.

- `fetch` · JSON (Week 12) — `loadSong` gets the song file and uses it as an object (ex09).
- Arrays (Week 10) — the 16 cells of `PATTERNS`, and `bars`, all bars in one row.
- Objects (Week 11) — `song.track_info.title`, one bar `{ section, chord, midis }`.
- `createElement` · `append` (Week 10) — the section rows and bar cells of the sheet.

More to try: build a melody layer yourself (only melodies you wrote), play on top with the ex02 keyboard.
Recording to an audio file is outside this special lecture.
