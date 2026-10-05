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
