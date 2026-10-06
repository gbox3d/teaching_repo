---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 4"
footer: "CSS and Responsive UI · compare the parts one at a time, then assemble at the end"
---

# CSS and Responsive UI

Week 3's three pages are still unstyled. This week is CSS.
New repository this week: `web-week04` → `https://student01.github.io/web-week04/`

This week: **compare 13 parts one at a time** (plus one appendix), then **assemble** `styles.css` at the end.

- One file = one topic. Siblings that differ in a single value sit side by side.
- No other topic is mixed in; boxes differ **only by background color**.
- The first sibling is the default; comments hold other values. You **change values** in the lab.
- Building happens once, at the end of Day 2. We note which rule came from which file.

Same approach as last year's class (dayNN/exNN comparison files → build at the end).

---

# Day 1 — Selectors and Boxes

`30 min explanation & demo → 60 min lab`

1. ex01 selectors — a rule applies only when it matches; when they overlap, the class wins
2. ex02 display — whether an element takes a whole line is decided by display, not the tag
3. ex03 box model — padding · border · margin, three layers
4. ex04 width · max-width — which one shrinks when the window narrows
5. ex05 margin auto — split the leftover width to center a box
6. ex06 text-align — where the text sits horizontally inside a box

---

## Day 1 · 0–4 min — This Week: Parts First, Assembly Last

```css
selector {
  property: value;
}
```

- One rule = selector + braces + `property: value;` lines. The three pages keep them in `styles.css`, linked by `<link rel="stylesheet" href="styles.css">`.
- Color and font properties mean what they say: `color` · `background-color` · `font-size` · `font-family`.
- **CSS gives no error message when it's wrong.** A non-matching selector or a missing semicolon is silently ignored.
- So we put siblings side by side and compare **by eye**. A value that changes nothing is a result too.

---

## Day 1 · 4–9 min — ex01 Selectors: Must Match; the Class Wins

[examples/day1/ex01_selector.html](examples/day1/ex01_selector.html)
Siblings: `p` / `p.red` / `div.red` / `p.Red` (typo) / `nav a` / `a` outside nav

```css
p     { color: blue; }    /* tag selector: every p */
.red  { color: red; }     /* class selector: class="red", any tag */
nav a { color: green; }   /* descendant selector: a inside nav */
/* p { color: gray; } */
```

- No. 2 is `p` and `.red` → red. No. 4 `class="Red"` is not `.red` → blue.
- Try it: uncomment → only No. 1 and 4 turn gray; No. 2 stays red. Change No. 4 to `class="red"` → red.

**A selector must match. A class picks more narrowly than a tag, so it is stronger. Only at equal strength does the later rule win.**

---

## Day 1 · 9–13 min — ex02 display: The Tag Doesn't Decide, display Does

[examples/day1/ex02_display.html](examples/day1/ex02_display.html)
Siblings: 3 divs / 3 spans / span + `display: block` / div + `display: inline`

```css
.as-block  { display: block; }   /* takes a whole line */
.as-inline { display: inline; }  /* flows sideways like text */
```

- No. 1 divs fill each line; No. 2 spans flow sideways, as wide as their text. A new color = a new box.
- Try it: swap `block` and `inline` in the two classes → No. 3 and 4 swap shapes.

**Whether an element takes a whole line is decided by `display`, not by the tag.**

---

## Day 1 · 13–18 min — ex03 Box Model: Three Layers

[examples/day1/ex03_box_model.html](examples/day1/ex03_box_model.html)
Siblings: default / `padding` / `border` / `margin` / all three (sky-blue box inside a gray frame)

```css
.pad { padding: 16px; }           /* inside the border */
.bd  { border: 4px solid navy; }  /* the border */
.mg  { margin: 16px; }            /* outside the border */
```

- The blue background is painted up to the `padding`; the gap `margin` opens shows the gray frame.
- Try it: set the three values to 0 / 16 / 32 → which layer grows in box No. 5?

**Inner space (padding), border, and outer space (margin) are three different layers.**

---

## Day 1 · 18–22 min — ex04 width vs max-width: Which One Shrinks

[examples/day1/ex04_width.html](examples/day1/ex04_width.html)
Siblings: default (parent width) / `width: 640px` / `max-width: 640px`

```css
.w  { width: 640px; }        /* stays 640px, sticks out of a narrow window */
.mw { max-width: 640px; }    /* at most 640px, shrinks with the window */
```

- In a wide window No. 2 and 3 are both 640px. The difference shows only below 640px.
- Try it: narrow the window to 400px → only No. 2 sticks out and a scrollbar appears.

**`width` pins the width; `max-width` only sets a ceiling, so it shrinks with the window.**

---

## Day 1 · 22–25 min — ex05 margin auto: Split the Leftover Width to Center

[examples/day1/ex05_margin_auto.html](examples/day1/ex05_margin_auto.html)
Siblings: default / `margin-left: auto` / both sides `auto` / `margin: 0 auto`

```css
.left-auto { margin-left: auto; }                      /* left takes it all → right side */
.both-auto { margin-left: auto; margin-right: auto; }  /* half each → center */
.short     { margin: 0 auto; }                         /* same as No. 3 */
```

- Leftover width exists only if the box is narrower than the window (ex04). `auto` takes it.
- Try it: drop No. 3's `margin-right: auto` → like No. 2. Drop `max-width` → all four alike.

**`auto` on `margin` takes the leftover width. When both sides share it, the box stands in the middle.**

---

## Day 1 · 25–28 min — ex06 text-align: Where the Text Sits Inside a Box

[examples/day1/ex06_text_align.html](examples/day1/ex06_text_align.html)
Siblings: default (left) / `text-align: center` / `text-align: right`

```css
.center { text-align: center; }
.right  { text-align: right; }
```

- The box stays the full window width; only the **text inside** moves. ex05 moved the box itself.
- Try it: change No. 3's `right` to `center`. The assembly uses this line to center the footer text.

**`text-align` sets where text sits horizontally inside a box. The box itself doesn't move.**

---

## Day 1 · 28–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--선택자와-박스-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css)

1. Put last week's files in a new folder `web-week04`, and save ex01–ex06 in `ex/`.
2. Change at least one value per file and watch the screen.
3. End: push to the `web-week04` repository and turn on Pages — steps are in the lab sheet

If nothing changes, check the **selector spelling** and **semicolons** first.

**Explanation total: 4+5+4+5+4+3+3+2 = 30 min**

---

# Day 2 — flex, Then Assembly

`30 min explanation & demo → 60 min lab`

1. Five lines of flex principle — parent, main axis, cross axis
2. ex07 · ex08 · ex09 — direction sets the main axis; justify is main axis, align is cross axis
3. ex10 · ex11 · ex12 — wrap and gap go on the parent; flex: 1 goes on the child
4. ex13 — @media applies only when the condition holds
5. Assembly — gather `styles.css` from the parts

---

## Day 2 · 0–4 min — Five Lines of flex: Parent, Main Axis, Cross Axis

```text
parent (container) display: flex, flex-direction: row
┌──────────── main axis → ──────────┐
│ [1] [2] [3]                       │  cross axis ↓
└───────────────────────────────────┘
```

1. `display: flex` goes on the **parent**. Its children get laid out.
2. `flex-direction` sets the **main axis**: `row` horizontal, `column` vertical.
3. `justify-content` aligns along the **main axis**: horizontal in `row`.
4. `align-items` aligns along the **cross axis**: vertical in `row`.
5. `flex: 1` makes that child take the **leftover space** on the main axis.

ex07–ex12 check these five lines one per file. Gray is the parent; colored boxes are the children.

---

## Day 2 · 4–8 min — ex07 flex-direction: Sets the Main Axis

[examples/day2/ex07_flex_direction.html](examples/day2/ex07_flex_direction.html)
Siblings: no flex / `display: flex` (default row) / `row-reverse` / `column` / `column-reverse`

```css
.flex           { display: flex; }                   /* on the parent; default row (→) */
.row-reverse    { flex-direction: row-reverse; }     /* ← */
.column         { flex-direction: column; }          /* ↓ */
.column-reverse { flex-direction: column-reverse; }  /* ↑ */
```

- No. 2: side by side, as wide as their text; the leftover is gray. No. 4 (column) looks like No. 1.
- Try it: add class `flex` to `상자 1` in No. 2 → nothing moves. flex works on the parent.

**`display: flex` goes on the parent; `flex-direction` sets the main axis.**

---

## Day 2 · 8–12 min — ex08 justify-content: Leftover Space on the Main Axis

[examples/day2/ex08_justify_content.html](examples/day2/ex08_justify_content.html)
Siblings: flex-start / center / flex-end / space-between / space-around, comment space-evenly

```css
.start   { justify-content: flex-start; }    /* default: packed at the start */
.between { justify-content: space-between; } /* pinned to both ends */
.around  { justify-content: space-around; }  /* equal space on both sides of each box */
/* .evenly { justify-content: space-evenly; } */ /* every gap equal */
```

- Gray is the leftover space. Each value puts it in a different place: front, back, or between.
- Try it: uncomment `.evenly` and set frame 5's class to `evenly` → how does it differ from around?

**`justify-content` is how the leftover space on the main axis is divided.**

---

## Day 2 · 12–16 min — ex09 align-items: Position on the Cross Axis

[examples/day2/ex09_align_items.html](examples/day2/ex09_align_items.html)
Siblings: `stretch` (default) / `flex-start` / `center` / `flex-end` — frame 100px tall

```css
.stretch { align-items: stretch; }     /* default: no-height child stretches */
.start   { align-items: flex-start; }  /* top */
.center  { align-items: center; }      /* vertical center */
.end     { align-items: flex-end; }    /* bottom */
```

- The boxes have no height, so No. 1 stretches to the frame's height. No. 3 is vertically centered.
- Try it: remove `height: 100px` from `.frame` → no vertical space left, so all four look the same.

**`align-items` aligns along the cross axis: vertical for children standing in a row.**

---

## Day 2 · 16–18 min — ex10 flex-wrap: Wrap When They Don't Fit

[examples/day2/ex10_flex_wrap.html](examples/day2/ex10_flex_wrap.html)
Siblings: `nowrap` (default) / `wrap` — six 80px children in a 300px frame

```css
.nowrap { flex-wrap: nowrap; }  /* default: forces one line */
.wrap   { flex-wrap: wrap; }    /* moves the rest to the next line */
```

- 80 × 6 = 480px. No. 1 shrinks all six to 50px; No. 2 wraps them into two lines of three.
- Try it: 6 children → 3 → no shrinking, no wrapping.

**Whether children wrap when they don't fit is decided by `flex-wrap`, on the parent.**

---

## Day 2 · 18–20 min — ex11 gap: Space Between Children

[examples/day2/ex11_gap.html](examples/day2/ex11_gap.html)
Siblings: no gap / `gap: 16px` / `gap: 32px`

```css
.gap16 { gap: 16px; }   /* space between children; goes on the parent */
.gap32 { gap: 32px; }
```

- Only the spaces between open up; the first and last box stay at the edges.
- Try it: move `gap16` from the frame to `상자 1`'s class → nothing happens.

**A gap between children can't be set by one child, so `gap` goes on the parent.**

---

## Day 2 · 20–23 min — ex12 flex: 1 — Takes the Leftover Space

[examples/day2/ex12_flex_grow.html](examples/day2/ex12_flex_grow.html)
Siblings: default / middle only `flex: 1` / all three `flex: 1`, comment `flex: 2`

```css
.grow { flex: 1; }   /* this child takes the leftover space on the main axis */
/* flex: 2; */       /* 2:1 when two share */
```

- The one property that goes on the **child**: "I take the leftover space" is the child's claim.
- Try it: `style="flex: 2"` on the middle `<div>` of No. 3 → double share. Uncommenting `flex: 2` in `.grow` changes nothing (all three become 2).

**`flex: 1` makes the child take the leftover space. Several children split it by their numbers.**

---

## Day 2 · 23–26 min — ex13 @media: Conditional Rules

[examples/day2/ex13_media.html](examples/day2/ex13_media.html)
Siblings: a box with an `@media (max-width: 600px)` rule / a box without

```css
.with-media { background-color: lightskyblue; }   /* normal color */
@media (max-width: 600px) {                        /* try 900px */
    .with-media { background-color: orange; }
}
```

- At ≤ 600px the inner rule lives; same selector twice → the later wins (ex01). Check at 375.
- Try it: 600 → 900 → orange even in a normal window. Drop the colon → ignored, no error.

**The inner rule lives only when the condition holds. Any property can change.**

---

## Day 2 · 26–30 min — Assembly: web-week04 styles.css → Lab

```text
body  { max-width: 640px; margin: 0 auto; padding: 16px }      ← ex04 + ex05 + ex03
nav   { display: flex; gap: 16px; flex-wrap: wrap }            ← ex07 + ex11 + ex10 (all on the parent)
.card { background-color; padding; margin: 12px 0; border }    ← ex01 class + ex03 three layers
@media (max-width: 600px) { nav { flex-direction: column } }   ← ex13 + ex07
```

[Day 2 lab](lab.md#2일차--flex와-조립-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css)

1. Save ex07–ex13 in `ex/` and change values (until minute 35).
2. Assemble: `styles.css` in the table order, the `link` line on all three pages, `class="card"` in three places in `index.html`.
3. Check at 1280 and 375 (device mode) → push to `web-week04` → screenshot (steps: lab sheet)

**Explanation total: 4+4+4+4+2+2+3+3+4 = 30 min**

---

## Appendix — ex14 position (Optional, Not Explained)

[examples/day2/ex14_position.html](examples/day2/ex14_position.html)
Siblings: `static` (default) / `relative; top: 40px; left: 40px` / `absolute; right: 0; bottom: 0`

```css
.frame    { position: relative; }                           /* anchor for absolute children */
.relative { position: relative; top: 40px; left: 40px; }    /* nudged; its slot stays */
.absolute { position: absolute; right: 0; bottom: 0; }      /* out of the flow, placed by the frame's corner */
```

- Not covered in class. If you finish early, open it and change the values.
- In No. 2 A's original slot (the top) stays empty; in No. 3 B moves up into A's place because `absolute` took A out of the document flow.

**Two ways to leave the document flow. `relative` keeps its slot; `absolute` doesn't.**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/web-week04/
DevTools device mode 375px
Menu: 홈 / 내 정보 / 방명록 (Home / About / Guestbook)   ← one per line, vertically
Intro paragraphs · hobby list: white cards with a border
Capture it with the address bar and the 375 width indicator visible
```

The 1280px screen and the experiment files in `ex/` are for checking only. Keep your real name, student ID, and real email out of the screenshot.

---

## Next Week Preview

So far only what the three pages **look like** has changed. Buttons and input fields still do nothing.

Week 5 starts in a new repository, `web-week05`, from today's files.
On top of them we empty `app.js` and rewrite it to start JavaScript.
We bring back the `<script src="app.js" defer></script>` line and print values to the Console.
`styles.css` stays as it is. The `.card` colors you chose today come back in Week 6's dark mode.
