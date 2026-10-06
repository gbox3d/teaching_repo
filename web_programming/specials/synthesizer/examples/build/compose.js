// compose.js — 멜로디 조합기. 라이브러리의 멜로디 조각을 골라 마디로 이어 붙이고, 연주하고, 곡 JSON 으로 불러오고 내보낸다.
import { midiToFreq, chordToMidis, createNoise, playTone, playKick, playSnare, playHat } from './synth.js';
import { tagMelodies, tagColor, transpose, songToBars, barsToSong } from './song.js';

// 반주는 디스코 한 가지(index.js 의 PATTERNS.disco 와 같다)
const DISCO = {
    kick:  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    snare: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    hat:   [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    open:  [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    bass:  [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0],
    chord: [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
};

const $ = function (id) { return document.getElementById(id); };

let library = [];       // 멜로디 조각 [{ notes, chord }] — chord 는 처음 나온 마디의 코드(미리 듣기용)
let arrangement = [];   // 편곡 마디 [{ section, chord, melody: 라이브러리 번호 또는 -1, shift: 반음 }]
let selected = -1;      // 고른 편곡 마디
let tags = [];          // library 와 같은 순서의 { name, color }

let ctx = null;
let out = null;
let noise = null;
let session = null;     // 이번 연주의 소리가 모이는 게인. 정지하면 줄이고 끊어 남은 소리도 멈춘다
let timer = null;
let frame = 0;          // 화면 그리기 requestAnimationFrame 번호
let nextTime = 0;
let playBar = 0;        // 다음에 예약할 마디(source() 안의 번호)
let playStep = 0;       // 그 마디의 몇 번째 칸(0~15)
let source = null;      // 지금 연주하는 마디 목록을 돌려주는 함수
let looping = true;
let songInfo = {};      // 마지막으로 연 곡의 track_info(내보낼 때 artist · key 를 이어받는다)
const queue = [];

function secondsPerStep() {
    return 60 / Number($('bpm').value) / 4;
}

function on(id) {
    return $(id).checked;
}

function say(text) {
    $('message').innerText = text;
}

// ---------- 라이브러리 ----------

// 같은 멜로디가 이미 있으면 그 번호, 없으면 더하고 새 번호. 빈 멜로디는 -1
function addToLibrary(notes, chord) {
    if (notes.length === 0) return -1;
    const key = JSON.stringify(notes.map(function (n) { return [n.step, n.midi, n.duration_steps]; }).sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; }));
    for (let k = 0; k < library.length; k++) {
        if (library[k].key === key) return k;
    }
    library.push({ key: key, notes: notes.map(function (n) { return { step: n.step, note: n.note, midi: n.midi, duration_steps: n.duration_steps }; }), chord: chord });
    return library.length - 1;
}

function tagLabel(k) {
    return k >= 0 && tags[k] ? `♪${tags[k].name}` : '—';
}

function renderLibrary() {
    tags = tagMelodies(library.map(function (item) { return item.notes; }));
    const box = $('library');
    box.innerHTML = '';
    if (library.length === 0) {
        box.textContent = '비어 있다. 위에서 곡을 열거나 더한다.';
        return;
    }
    library.forEach(function (item, k) {
        const chip = document.createElement('div');
        chip.className = 'chip';
        chip.style.borderColor = tagColor(tags[k]);
        const listen = document.createElement('button');
        listen.textContent = `${tagLabel(k)} ${item.chord}`;
        listen.title = item.notes.map(function (n) { return `${n.step}칸 ${n.note} ${n.duration_steps}칸`; }).join(' · ');
        listen.style.color = tagColor(tags[k]);
        listen.addEventListener('click', function () { preview(k); });
        const add = document.createElement('button');
        add.textContent = '+';
        add.addEventListener('click', function () {
            insertBar({ section: currentSection(), chord: item.chord, melody: k, shift: 0 });
        });
        chip.append(listen, add);
        box.append(chip);
    });
}

// ---------- 편곡 줄 ----------

function currentSection() {
    if (selected >= 0) return arrangement[selected].section;
    return arrangement.length > 0 ? arrangement[arrangement.length - 1].section : 'A';
}

function insertBar(bar) {
    const at = selected >= 0 ? selected + 1 : arrangement.length;
    arrangement.splice(at, 0, bar);
    if (playingArrangement() && at <= playBar) playBar += 1;      // 연주 중인 마디가 뒤로 밀렸다
    selected = at;
    renderArrangement();
}

function playingArrangement() {
    return timer !== null && source === arrangementSource;
}

function renderArrangement() {
    renderCells();
    renderEditor();
}

// 편곡 줄의 칸만 다시 그린다(편집기 입력 칸은 건드리지 않아 글자를 치는 중에도 쓸 수 있다)
function renderCells() {
    const box = $('arrangement');
    box.innerHTML = '';
    arrangement.forEach(function (bar, k) {
        const cell = document.createElement('div');
        cell.className = k === selected ? 'bar selected' : 'bar';
        if (k === 0 || arrangement[k - 1].section !== bar.section) {
            const name = document.createElement('small');
            name.className = 'section-name';
            name.textContent = bar.section;
            cell.append(name);
        }
        cell.append(document.createTextNode(bar.chord));
        if (bar.melody >= 0) {
            const mark = document.createElement('small');
            mark.className = 'tag';
            mark.textContent = tagLabel(bar.melody) + (bar.shift ? ` ${bar.shift > 0 ? '+' : ''}${bar.shift}` : '');
            mark.style.color = tagColor(tags[bar.melody]);
            cell.append(mark);
        }
        cell.dataset.index = String(k);
        box.append(cell);
    });
    const seconds = arrangement.length * 16 * secondsPerStep();
    $('arrangement-info').textContent = `— ${arrangement.length}마디 · ${seconds.toFixed(1)}초 · 마디를 누르면 아래에서 고친다`;
}

function renderEditor() {
    const bar = arrangement[selected];
    for (const el of $('editor').querySelectorAll('input, select, button')) {
        el.disabled = !bar && el.id !== 'ed-empty';
    }
    const select = $('ed-melody');
    select.innerHTML = '';
    const none = document.createElement('option');
    none.value = '-1';
    none.textContent = '없음';
    select.append(none);
    library.forEach(function (item, k) {
        const option = document.createElement('option');
        option.value = String(k);
        option.textContent = `${tagLabel(k)} (${item.chord})`;
        select.append(option);
    });
    if (!bar) {
        $('ed-section').value = '';
        $('ed-chord').value = '';
        $('ed-shift').value = 0;
        return;
    }
    $('ed-section').value = bar.section;
    $('ed-chord').value = bar.chord;
    select.value = String(bar.melody);
    $('ed-shift').value = bar.shift;
}

// 'F G' → 마디를 반씩. 이름이 틀리면 chordToMidis 가 던진다
function readChords(text) {
    const parts = text.trim().split(/\s+/);
    if (parts.length === 0 || parts[0] === '') throw new Error('코드를 적는다 (예: Am, F G)');
    return parts.map(chordToMidis);
}

// 검사하고 빈칸 하나로 맞춘 코드 글자. '  F   G ' → 'F G'(연주기는 빈칸 하나로 나눈다)
function normalizeChord(text) {
    readChords(text);
    return text.trim().split(/\s+/).join(' ');
}

function setupEditor() {
    // 마디 고르기: 칸마다 달지 않고 줄 하나에 단다(칸을 다시 그려도 클릭을 놓치지 않는다)
    $('arrangement').addEventListener('click', function (event) {
        const cell = event.target.closest('.bar');
        if (!cell) return;
        const k = Number(cell.dataset.index);
        selected = selected === k ? -1 : k;      // 다시 누르면 고르기 풀기
        renderArrangement();
    });
    // 구간 · 코드 · 옮김은 칠 때마다(input) 반영한다. 칸만 다시 그리므로 치는 중인 글자는 그대로다
    $('ed-section').addEventListener('input', function () {
        if (selected < 0) return;
        arrangement[selected].section = $('ed-section').value.trim() || 'A';
        renderCells();
    });
    $('ed-chord').addEventListener('input', function () {
        if (selected < 0) return;
        try {
            arrangement[selected].chord = normalizeChord($('ed-chord').value);
            say('');
        } catch (error) {
            say(error.message);                  // 다 치기 전(예: 'F ')에는 마디를 바꾸지 않는다
        }
        renderCells();
    });
    $('ed-chord').addEventListener('change', function () {
        if (selected >= 0) $('ed-chord').value = arrangement[selected].chord;   // 틀린 채로 나가면 마디의 코드로 되돌린다
    });
    $('ed-melody').addEventListener('change', function () {
        if (selected < 0) return;
        arrangement[selected].melody = Number($('ed-melody').value);
        renderArrangement();
    });
    $('ed-shift').addEventListener('input', function () {
        if (selected < 0) return;
        arrangement[selected].shift = Math.max(-12, Math.min(12, Math.round(Number($('ed-shift').value) || 0)));
        renderCells();
    });
    $('ed-left').addEventListener('click', function () { move(-1); });
    $('ed-right').addEventListener('click', function () { move(1); });
    $('ed-copy').addEventListener('click', function () {
        if (selected >= 0) insertBar(Object.assign({}, arrangement[selected]));
    });
    $('ed-delete').addEventListener('click', function () {
        if (selected < 0) return;
        arrangement.splice(selected, 1);
        if (playingArrangement() && selected < playBar) playBar -= 1;  // 앞 마디가 빠지면 연주 위치도 당긴다
        selected = Math.min(selected, arrangement.length - 1);
        renderArrangement();
    });
    $('ed-empty').addEventListener('click', function () {
        insertBar({ section: currentSection(), chord: selected >= 0 ? arrangement[selected].chord : 'Am', melody: -1, shift: 0 });
    });
}

function move(by) {
    const to = selected + by;
    if (selected < 0 || to < 0 || to >= arrangement.length) return;
    const bar = arrangement.splice(selected, 1)[0];
    arrangement.splice(to, 0, bar);
    if (playingArrangement()) {                  // 연주 중인 마디가 자리를 바꿨으면 따라간다
        if (playBar === selected) playBar = to;
        else if (playBar === to) playBar = selected;
    }
    selected = to;
    renderArrangement();
}

// ---------- 연주 ----------

// 편곡 마디 → 소리 낼 모양 { chords: [[midi…]…], melody: [음…] }
function toPlayable(bar) {
    let chords;
    try {
        chords = readChords(bar.chord);
    } catch (error) {
        chords = [[]];
    }
    const melody = bar.melody >= 0 && library[bar.melody] ? transpose(library[bar.melody].notes, bar.shift) : [];
    return { chords: chords, melody: melody };
}

// index 번 마디의 i 번째 칸에서 칠 소리를 모두 예약한다
function scheduleStep(sourceBar, index, i, time) {
    const bar = toPlayable(sourceBar);
    const out = session;
    const len = secondsPerStep();
    const midis = bar.chords[Math.floor(i * bar.chords.length / 16)];

    if (on('use-drums')) {
        if (DISCO.kick[i]) playKick(ctx, out, time);
        if (DISCO.snare[i]) playSnare(ctx, out, noise, time);
        if (DISCO.hat[i]) playHat(ctx, out, noise, time, false);
        if (DISCO.open[i]) playHat(ctx, out, noise, time, true);
    }
    if (on('use-bass') && DISCO.bass[i] && midis.length > 0) {
        const root = midis[0] - 24 + (DISCO.bass[i] === 2 ? 12 : 0);
        playTone(ctx, out, { freq: midiToFreq(root), time: time, type: 'square', cutoff: 700, attack: 0.003, length: len * 0.6, release: 0.06, volume: 0.3 });
    }
    if (on('use-chord') && DISCO.chord[i]) {
        for (const midi of midis) {
            playTone(ctx, out, { freq: midiToFreq(midi), time: time, type: 'sawtooth', cutoff: 1800, attack: 0.005, length: len, release: 0.15, volume: 0.24 / midis.length });
        }
    }
    if (on('use-melody')) {
        for (const note of bar.melody) {
            if (note.step === i + 1) playTone(ctx, out, { freq: midiToFreq(note.midi), time: time, type: 'square', cutoff: 3000, attack: 0.01, length: note.duration_steps * len - 0.06, release: 0.05, volume: 0.12 });
        }
    }
    if (i === 0) queue.push({ time: time, index: index });
}

// ex07 — 25ms 마다 깨어나 앞으로 0.1초 안의 칸을 예약한다. 마디 번호와 칸 번호를 따로 센다
// (곡 처음부터 센 칸 수로 마디를 구하면 연주 중에 마디를 넣거나 빼는 순간 위치가 튄다)
function tick() {
    while (nextTime < ctx.currentTime + 0.1) {
        const bars = source();
        if (bars.length === 0) {
            stop();
            say('마디가 없어서 멈췄다.');
            return;
        }
        if (playBar >= bars.length) {
            if (looping) {
                playBar = 0;
            } else {                             // 반복을 끄면 이번 바퀴 끝에서 멈춘다
                clearInterval(timer);
                timer = null;
                const mine = session;
                setTimeout(function () { if (session === mine && !timer) stop(); }, (nextTime - ctx.currentTime) * 1000 + 300);
                return;
            }
        }
        scheduleStep(bars[playBar], playBar, playStep, nextTime);
        nextTime += secondsPerStep();
        playStep += 1;
        if (playStep === 16) {
            playStep = 0;
            playBar += 1;
        }
    }
}

function draw() {
    while (queue.length > 0 && queue[0].time <= ctx.currentTime) {
        const item = queue.shift();
        if (source === arrangementSource) {
            document.querySelectorAll('#arrangement .bar').forEach(function (el, k) { el.classList.toggle('now', k === item.index); });
            const bar = arrangement[item.index];
            if (bar) $('where').innerText = `${bar.section} · ${item.index + 1}/${arrangement.length}마디 · ${bar.chord} · ${tagLabel(bar.melody)}`;
        }
    }
    frame = timer || queue.length > 0 ? requestAnimationFrame(draw) : 0;
}

function arrangementSource() {
    return arrangement;
}

async function start(from, loop) {
    if (!ctx) {
        ctx = new AudioContext();
        const compressor = ctx.createDynamicsCompressor();
        out = ctx.createGain();
        out.gain.value = 0.6;
        out.connect(compressor).connect(ctx.destination);
        noise = createNoise(ctx);
    }
    await ctx.resume();
    stop();
    if (from().length === 0) {
        say('편곡 줄이 비어 있다. 라이브러리에서 + 로 마디를 더한다.');
        return;
    }
    say('');
    session = ctx.createGain();
    session.connect(out);
    source = from;
    looping = loop;
    playBar = 0;
    playStep = 0;
    nextTime = ctx.currentTime + 0.05;
    timer = setInterval(tick, 25);
    frame = requestAnimationFrame(draw);
}

function stop() {
    clearInterval(timer);
    timer = null;
    cancelAnimationFrame(frame);
    frame = 0;
    queue.length = 0;
    if (session) {                               // 이미 예약한 소리 · 길게 끄는 음도 0.1초 안에 줄여 끊는다
        const old = session;
        old.gain.setTargetAtTime(0, ctx.currentTime, 0.02);
        setTimeout(function () { old.disconnect(); }, 300);
        session = null;
    }
    document.querySelectorAll('#arrangement .bar.now').forEach(function (el) { el.classList.remove('now'); });
    $('where').innerText = '정지';
}

// 라이브러리 조각 하나를 그 코드와 함께 한 마디 듣는다
function preview(k) {
    const bar = { section: '', chord: library[k].chord, melody: k, shift: 0 };
    start(function () { return [bar]; }, false);
}

// ---------- 불러오기 · 내보내기 ----------

// replace = true 이면 편곡 줄과 라이브러리를 그 곡으로 바꾸고, false 이면 멜로디만 라이브러리에 더한다
function useSong(song, replace) {
    const bars = songToBars(song);
    for (const bar of bars) bar.chord = normalizeChord(bar.chord);   // 코드 이름이 틀리면 여기서 멈춘다
    stop();
    if (replace) {
        library = [];
        arrangement = [];
        selected = -1;
    }
    const before = library.length;
    const added = bars.map(function (bar) {
        return { section: bar.section, chord: bar.chord, melody: addToLibrary(bar.melody, bar.chord), shift: 0 };
    });
    if (replace) {
        arrangement = added;
        const info = song.track_info || {};
        songInfo = info;
        $('title').value = info.title || '내 편곡';
        if (info.bpm) $('bpm').value = info.bpm;
        $('bpm-value').innerText = $('bpm').value;
    }
    renderLibrary();
    renderArrangement();
    const fresh = library.length - before;
    say(replace ? `열었다: ${bars.length}마디, 멜로디 조각 ${library.length}개` : `라이브러리에 새 조각 ${fresh}개를 더했다(이미 있는 것은 건너뜀)`);
}

async function fetchSong(file) {
    const response = await fetch(file);
    if (!response.ok) throw new Error(`${file} 을 불러오지 못했습니다 (${response.status})`);
    return response.json();
}

function exportSong() {
    if (arrangement.length === 0) {
        say('내보낼 마디가 없다.');
        return;
    }
    const title = $('title').value.trim() || '내 편곡';
    const info = Object.assign({ artist: '', key: '', time_signature: '4/4' }, songInfo, { title: title, bpm: Number($('bpm').value) });
    const song = barsToSong(info, arrangement.map(function (bar) {
        const melody = bar.melody >= 0 ? transpose(library[bar.melody].notes, bar.shift) : [];
        return { section: bar.section, chord: bar.chord, melody: melody };
    }));
    const blob = new Blob([JSON.stringify(song, null, 2) + '\n'], { type: 'application/json' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${title.replace(/[\\/:*?"<>|\s]+/g, '_')}.json`;
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(function () { URL.revokeObjectURL(link.href); }, 1000);
    say(`내보냈다: ${link.download} — 연주기 폴더에 두고 index.html 의 곡 선택에 더하면 연주기에서도 열린다`);
}

export default async function main() {
    $('play').addEventListener('click', function () { start(arrangementSource, on('loop')); });
    $('stop').addEventListener('click', stop);
    $('loop').addEventListener('change', function () {
        if (source === arrangementSource) looping = on('loop');      // 미리 듣기(한 마디)는 늘 한 번만
    });
    $('bpm').addEventListener('input', function () {
        $('bpm-value').innerText = $('bpm').value;
        renderArrangement();
    });
    $('open-song').addEventListener('click', function () {
        fetchSong($('song').value).then(function (song) { useSong(song, true); }).catch(function (error) { say(`불러오지 못했습니다: ${error.message}`); });
    });
    $('add-song').addEventListener('click', function () {
        fetchSong($('song').value).then(function (song) { useSong(song, false); }).catch(function (error) { say(`불러오지 못했습니다: ${error.message}`); });
    });
    // 내 컴퓨터의 곡 JSON. 서버에 올리지 않고 브라우저가 바로 읽는다
    for (const [id, replace] of [['file-open', true], ['file-add', false]]) {
        $(id).addEventListener('change', async function () {
            const file = $(id).files[0];
            if (!file) return;
            try {
                useSong(JSON.parse(await file.text()), replace);
            } catch (error) {
                say(`${file.name} 을 읽지 못했습니다: ${error.message}`);
            }
            $(id).value = '';           // 같은 파일을 다시 골라도 change 가 나도록
        });
    }
    $('export').addEventListener('click', exportSong);
    setupEditor();

    try {
        useSong(await fetchSong('only_you.json'), true);
    } catch (error) {
        say(`불러오지 못했습니다: ${error.message}`);
        renderLibrary();
        renderArrangement();
    }
}
