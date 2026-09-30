import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { runInNewContext } from "node:vm";
import test from "node:test";

const source = readFileSync(new URL("../site/assets/deck.js", import.meta.url), "utf8");

// Marp 코드 블록의 비동기 레이아웃을 다음 ResizeObserver 알림에서 반영한다.
function viewer(initialHeight = 700) {
  let resize;
  let contentHeight = initialHeight;
  let writes = 0;
  let fontSize = "";
  const section = {
    clientHeight: 720,
    style: {
      get fontSize() { return fontSize; },
      set fontSize(value) { fontSize = value; writes++; },
    },
    children: [{ tagName: "MARP-PRE", offsetTop: 0, get offsetHeight() { return contentHeight; } }],
  };
  const slide = {
    querySelector: () => section,
    classList: { toggle() {} },
    setAttribute() {}, removeAttribute() {},
  };
  const listeners = {};
  const control = { style: {}, addEventListener() {} };
  const window = {
    location: { hash: "#slide-1" },
    history: { replaceState() {}, pushState() {} },
    addEventListener(name, fn) { listeners[name] = fn; },
    getComputedStyle: () => ({ fontSize: fontSize || "29px", paddingBottom: "64px" }),
  };
  runInNewContext(source, {
    window,
    document: {
      querySelectorAll: () => [slide],
      querySelector: (selector) => selector === "[data-language-select]" ? null : control,
      addEventListener() {}, body: { classList: { add() {} } },
    },
    ResizeObserver: class {
      constructor(callback) { resize = callback; }
      disconnect() {} observe() {}
    },
  });
  return {
    get size() { return Number.parseFloat(fontSize || "29px"); },
    get writes() { return writes; },
    notify(height) { contentHeight = height; resize(); },
  };
}

test("비동기 코드 블록이 줄어든 뒤 반복 알림에도 글자가 다시 커지지 않는다", () => {
  const deck = viewer();
  const fitted = deck.size;
  deck.notify(600);
  assert.equal(deck.size, fitted);
  const settledWrites = deck.writes;
  for (let i = 0; i < 30; i++) deck.notify(600);
  assert.equal(deck.writes, settledWrites, "안정된 화면의 스타일을 다시 쓰면 안 된다");
});

test("반복 알림에도 최초 크기의 62% 하한을 유지한다", () => {
  const deck = viewer();
  for (let i = 0; i < 30; i++) deck.notify(900);
  assert.equal(deck.size, Math.ceil(29 * 0.62));
});


test("늦게 커진 코드 블록도 맞추고 이후 알림에서 다시 키우지 않는다", () => {
  const deck = viewer(600);
  assert.equal(deck.size, 29);
  deck.notify(700);
  assert.ok(deck.size < 29);
  const fitted = deck.size;
  deck.notify(600);
  assert.equal(deck.size, fitted);
});
