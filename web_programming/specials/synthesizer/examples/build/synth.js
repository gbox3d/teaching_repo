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
