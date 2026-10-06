// song.js — 곡 데이터 도우미. 연주기(index.js)와 조합기(compose.js)가 같이 쓴다. 소리는 내지 않는다.

const NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

// MIDI 번호 → 음 이름. 69 → 'A4'
export function noteName(midi) {
    return NAMES[midi % 12] + (Math.floor(midi / 12) - 1);
}

// 멜로디 하나를 글자 하나로. 같은 음 · 같은 칸 · 같은 길이면 같은 글자
function melodyKey(notes) {
    return notes.map(function (n) { return `${n.step}:${n.midi}:${n.duration_steps}`; });
}

export function sameMelody(a, b) {
    const x = melodyKey(a);
    const y = melodyKey(b);
    return x.length === y.length && x.every(function (k) { return y.includes(k); });
}

// 멜로디가 같은 마디에 같은 글자를 붙인다. 처음 나온 순서대로 A, B, C …
// 음 두 개 이하만 다르면(하나 바꿈 · 빠짐 · 더함) 새 글자 대신 변형 A′, A″ 로 적는다
export function tagMelodies(list) {
    const bases = [];       // { letter, notes, variants: [notes, …] }
    const diff = function (a, b) { return a.filter(function (x) { return !b.includes(x); }).length + b.filter(function (x) { return !a.includes(x); }).length; };
    return list.map(function (melody) {
        if (!melody || melody.length === 0) return null;
        const notes = melodyKey(melody);
        const same = function (other) { return other.length === notes.length && other.every(function (x) { return notes.includes(x); }); };
        for (let k = 0; k < bases.length; k++) {
            const base = bases[k];
            if (same(base.notes)) return { name: base.letter, color: k };
            const v = base.variants.findIndex(same);
            if (v >= 0) return { name: base.letter + '′'.repeat(v + 1), color: k };
        }
        for (let k = 0; k < bases.length; k++) {
            if (diff(notes, bases[k].notes) <= 2) {
                bases[k].variants.push(notes);
                return { name: bases[k].letter + '′'.repeat(bases[k].variants.length), color: k };
            }
        }
        bases.push({ letter: letterOf(bases.length), notes: notes, variants: [] });
        return { name: bases[bases.length - 1].letter, color: bases.length - 1 };
    });
}

// 0 → A … 25 → Z, 26 → AA
function letterOf(k) {
    return (k >= 26 ? letterOf(Math.floor(k / 26) - 1) : '') + String.fromCharCode(65 + (k % 26));
}

// 같은 색 = 같은 글자
export function tagColor(tag) {
    return `hsl(${tag.color * 67 % 360} 85% 72%)`;
}

// 멜로디를 반음 shift 만큼 옮긴다(새 배열)
export function transpose(notes, shift) {
    return notes.map(function (n) {
        const midi = n.midi + shift;
        return { step: n.step, note: noteName(midi), midi: midi, duration_steps: n.duration_steps };
    });
}

// 곡 JSON → 마디 목록 [{ section, chord, melody }]. 모양이 틀리면 알려 준다
export function songToBars(song) {
    if (!song || !Array.isArray(song.sections)) throw new Error('sections 배열이 없습니다');
    const bars = [];
    for (const section of song.sections) {
        if (!Array.isArray(section.progression)) throw new Error(`구간 '${section.section}' 에 progression 배열이 없습니다`);
        for (const bar of section.progression) {
            if (typeof bar.chord !== 'string') throw new Error(`구간 '${section.section}' ${bar.bar}마디에 chord 가 없습니다`);
            const melody = Array.isArray(bar.melody) ? bar.melody : [];
            for (const n of melody) {
                const whole = function (x, lo, hi) { return Number.isInteger(x) && x >= lo && x <= hi; };
                if (!whole(n.step, 1, 16) || !whole(n.midi, 0, 127) || !whole(n.duration_steps, 1, 64)) {
                    throw new Error(`구간 '${section.section}' ${bar.bar}마디 멜로디의 음이 틀렸습니다 (step 1~16, midi 0~127, duration_steps 1~64 의 정수)`);
                }
            }
            bars.push({ section: section.section || '', chord: bar.chord, melody: melody });
        }
    }
    if (bars.length === 0) throw new Error('마디가 하나도 없습니다');
    return bars;
}

// 마디 목록 → 곡 JSON. 이어진 같은 구간 이름끼리 한 구간으로 묶는다
export function barsToSong(info, bars) {
    const sections = [];
    for (const bar of bars) {
        let last = sections[sections.length - 1];
        if (!last || last.section !== bar.section) {
            last = { section: bar.section, bars_count: 0, progression: [] };
            sections.push(last);
        }
        last.bars_count += 1;
        const entry = { bar: last.bars_count, chord: bar.chord };
        if (bar.melody.length > 0) entry.melody = bar.melody;
        last.progression.push(entry);
    }
    return { track_info: info, sections: sections };
}
