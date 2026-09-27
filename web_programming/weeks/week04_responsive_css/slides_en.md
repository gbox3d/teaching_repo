---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 4"
footer: "CSS and Responsive UI · compare the parts one at a time, then assemble at the end"
---

# CSS and Responsive UI

The three `my-web` pages from Week 3 are still unstyled. This week is CSS.

This week: **compare 12 parts one at a time**, then **assemble** `my-web`'s `styles.css` at the end.

- One file = one property. Siblings that differ in a single value sit side by side.
- The first sibling is the default. Comments hold the other values. Uncomment or change them.
- The lab is not about creating files but about **changing values** and watching.
- Building happens once, at the end of Day 2. We note which rule came from which file.

Same approach as last year's class (dayNN/exNN comparison files → build at the end).

---

# Day 1 — Selectors and Boxes

`30 min explanation & demo → 60 min lab`

1. ex01 selectors — a rule applies only when it matches; when they overlap, the class wins
2. ex02 display — whether an element takes a whole line is decided by display, not the tag
3. ex03 box model — padding · border · margin, three layers
4. ex04 width · max-width — which one shrinks when the window narrows
5. ex05 text-align — horizontal works, vertical centering doesn't

---

## Day 1 · 0–4 min — This Week: Parts First, Assembly Last

```css
selector {
  property: value;
}
```

- One rule = selector + braces + `property: value;` lines. `my-web` keeps them in `styles.css`, linked by `<link rel="stylesheet" href="styles.css">`.
- Color and font properties mean what they say: `color` · `background-color` · `font-size` · `font-family`.
- **CSS gives no error message when it's wrong.** A non-matching selector or a missing semicolon is silently ignored.
- So we put siblings side by side and compare **by eye**. A value that changes nothing is a result too.

---

## Day 1 · 4–10 min — ex01 Selectors: Must Match; the Class Wins

[examples/ex01_selector.html](examples/ex01_selector.html)
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

## Day 1 · 10–15 min — ex02 display: The Tag Doesn't Decide, display Does

[examples/ex02_display.html](examples/ex02_display.html)
Siblings: 3 divs / 3 spans / span + `display: block` / div + `display: inline`

```css
.as-block  { display: block; }   /* takes a whole line */
.as-inline { display: inline; }  /* flows sideways like text */
```

- No. 1 divs stack; No. 2 spans flow sideways. Only the default differs, and No. 3·4 change it.
- Try it: swap `block` and `inline` in the two classes → No. 3 and 4 swap shapes. Tomorrow's `flex` is another value.

**Whether an element takes a whole line is decided by `display`, not by the tag.**

---

## Day 1 · 15–21 min — ex03 Box Model: Three Layers

[examples/ex03_box_model.html](examples/ex03_box_model.html)
Siblings: default / `padding` / `border` / `margin` / all three (sky-blue box on a white frame)

```css
.pad { padding: 16px; }           /* inside the border */
.bd  { border: 4px solid navy; }  /* the border */
.mg  { margin: 16px; }            /* outside the border */
```

- The blue background is painted up to the `padding`; the gap `margin` opens shows the white frame.
- Try it: set the three values to 0 / 16 / 32 → which layer grows in box No. 5?

**Inner space (padding), border, and outer space (margin) are three different layers.**

---

## Day 1 · 21–26 min — ex04 width vs max-width, and margin auto

[examples/ex04_width.html](examples/ex04_width.html)
Siblings: default (parent width) / `width: 640px` / `max-width: 640px` / `max-width` + `margin: auto`

```css
.w      { width: 640px; }        /* stays 640px, sticks out of a narrow window */
.mw     { max-width: 640px; }    /* at most 640px, shrinks with the window */
.center { max-width: 640px; margin-left: auto; margin-right: auto; }
```

- Left and right `margin: auto` split the leftover width in half. Shorthand: `margin: 0 auto`.
- Try it: narrow the window to 400px → only No. 2 sticks out and a scrollbar appears.

**`width` pins the width; `max-width` only sets a ceiling, so it shrinks with the window.**

---

## Day 1 · 26–28 min — ex05 text-align vs vertical-align

[examples/ex05_text_align.html](examples/ex05_text_align.html)
Siblings: default / `center` / `right` / `vertical-align: middle` (no effect on a block)

```css
.center { text-align: center; }
.right  { text-align: right; }
.middle { vertical-align: middle; }  /* nothing happens on a block box */
```

- Horizontal alignment is one `text-align` line. In No. 4 the text stays at the top, no error.
- Try it: change `.middle` to `bottom` → still nothing. The answer is ex08.

**`vertical-align` aligns text within a line, not a box's content. Vertical alignment is the parent's job → ex08.**

---

## Day 1 · 28–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--선택자와-박스-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css)

1. Create `my-web/week04/` and save the five files ex01–ex05.
2. Change at least one value per file and watch the screen.
3. Push, then open `https://student01.github.io/my-web/week04/ex01_selector.html`.

Git: `git pull` at 0–5 min, `git add .` → `git commit` → `git push` at 55–60 min.
If nothing changes, check the **selector spelling** and **semicolons** first.

**Explanation total: 4+6+5+6+5+2+2 = 30 min**

---

# Day 2 — flex, Then Assembly

`30 min explanation & demo → 60 min lab`

1. Five lines of flex principle — parent, main axis, cross axis
2. ex06 · ex07 · ex08 — direction sets the main axis; justify is main axis, align is cross axis
3. ex09 · ex10 — wrap and gap go on the parent; flex: 1 takes the leftover space
4. ex11 — @media applies only when the condition holds
5. Assembly — gather `my-web/styles.css` from the parts

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
3. `justify-content` aligns along the **main axis**. Not "horizontal".
4. `align-items` aligns along the **cross axis**: vertical in `row`, horizontal in `column`.
5. `flex: 1` makes that child take the **leftover space** on the main axis.

ex06–ex10 let you see these five lines one at a time.

---

## Day 2 · 4–9 min — ex06 flex-direction: Sets the Main Axis

[examples/ex06_flex_direction.html](examples/ex06_flex_direction.html)
Siblings: none / row / row-reverse / column / column-reverse / row+center / column+center

```css
.flex   { display: flex; }               /* on the parent */
.column { flex-direction: column; }      /* main axis ↓ (default row: →) */
.center { justify-content: center; }     /* centered along the main axis */
```

- 6 and 7 share `justify-content: center`: horizontal center in row, vertical in column.
- Try it: swap 6 and 7's direction → the centering flips. `display: flex` on a child → the boxes don't move.

**The parent gets `display: flex`. `flex-direction` sets the main axis; `justify-content` follows it.**

---

## Day 2 · 9–13 min — ex07 justify-content: Leftover Space on the Main Axis

[examples/ex07_justify_content.html](examples/ex07_justify_content.html)
Siblings: flex-start / center / flex-end / space-between / space-around, comment space-evenly

```css
.start   { justify-content: flex-start; }    /* default: packed at the start */
.between { justify-content: space-between; } /* pinned to both ends */
.around  { justify-content: space-around; }  /* equal space on both sides of each box */
/* .evenly { justify-content: space-evenly; } */
```

- Three 48px boxes in a 300px frame. Each value puts the leftover space somewhere else.
- Try it: `height: 160px` on `.frame`, uncomment `column` → all five move vertically. Uncomment `.evenly` for frame 5.

**`justify-content` is how the leftover space on the main axis is divided.**

---

## Day 2 · 13–17 min — ex08 align-items: Cross Axis, ex05's Answer

[examples/ex08_align_items.html](examples/ex08_align_items.html)
Siblings: `stretch` (default) / `flex-start` / `center` / `flex-end`, frame comment `column`

```css
.stretch { align-items: stretch; }     /* default: no-height child stretches */
.start   { align-items: flex-start; }  /* top */
.center  { align-items: center; }      /* vertical center */
.end     { align-items: flex-end; }    /* bottom */
```

- `.box` has no height, so No. 1 stretches. No. 3 does the centering ex05 couldn't.
- Try it: uncomment `column` in `.frame` → all four move horizontally (cross axis now horizontal).

**`align-items` aligns along the cross axis: vertical in row, horizontal in column.**

---

## Day 2 · 17–21 min — ex09 flex-wrap and gap: Wrapping and Spacing

[examples/ex09_flex_wrap_gap.html](examples/ex09_flex_wrap_gap.html)
Siblings: `nowrap` (six 64px boxes squeezed into 300px) / `wrap` / `wrap` + `gap: 16px`

```css
.nowrap { flex-wrap: nowrap; }  /* default: forces one line */
.wrap   { flex-wrap: wrap; }    /* moves the rest to the next line */
.gap    { gap: 16px; }          /* space between children; on the parent */
```

- 64 × 6 = 384px in 300px: No. 1 squeezes, No. 2 wraps. `gap` on a child does nothing.
- Try it: 6 children → 3: no squeezing, no wrapping. Set `gap` to 0 / 16 / 32.

**`flex-wrap` decides wrapping; `gap` sets spacing. Both go on the parent.**

---

## Day 2 · 21–24 min — ex10 flex: 1 — Takes the Leftover Space

[examples/ex10_flex_grow.html](examples/ex10_flex_grow.html)
Siblings: default / middle only `flex: 1` / all three `flex: 1` / column screen (header · main `flex: 1` · footer)

```css
.grow   { flex: 1; }   /* this child takes the leftover space; flex: 2 = double share */
.screen { display: flex; flex-direction: column; height: 200px; }
```

- The one property that goes on the **child**: "I take the leftover space" is the child's claim. No. 4 shows it vertically — last year's title screen.
- Try it: `style="flex: 2"` on the middle `<div>` of No. 3 → double share. Uncommenting `flex: 2` in `.grow` changes nothing (all three become 2).

**`flex: 1` makes the child take the leftover space. Several children split it by their numbers.**

---

## Day 2 · 24–27 min — ex11 @media: Conditional Rules

[examples/ex11_media.html](examples/ex11_media.html)
Siblings: frame with `@media (max-width: 600px)` (`.narrow`) / frame without

```css
.frame { display: flex; flex-direction: row; }   /* horizontal normally */
@media (max-width: 600px) {                      /* try 900px */
    .narrow { flex-direction: column; }
}
```

- At 600px or less the inner rule comes alive; `.narrow` then has both, and the later wins (ex01).
- Try it: 600 → 900 → No. 1 goes vertical in a normal window. Drop the colon → block ignored, no error.

**The later rule lives only when the condition holds. At equal strength, the later wins.**

---

## Day 2 · 27–30 min — Assembly: my-web styles.css, Then the Lab

```text
body  { max-width: 640px; margin: 0 auto; padding: 16px }      ← ex04 + ex03
nav   { display: flex; gap: 16px; flex-wrap: wrap }            ← ex06 + ex09 (on the parent)
.card { background-color; padding; margin: 12px 0; border }    ← ex01 class + ex03 three layers
@media (max-width: 600px) { nav { flex-direction: column } }   ← ex11 + ex06
```

[Day 2 lab](lab.md#2일차--flex와-조립-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css)

1. Save ex06–ex11 in `week04/` and change values (until minute 35).
2. Assemble: `styles.css` in the table order, the `link` line on all three pages, `class="card"` in three places in `index.html`.
3. Check at 1280 and at 375 in device mode → `git add .` → `git commit` → `git push` → screenshot.

**Explanation total: 4+5+4+4+4+3+3+3 = 30 min**

---

## Appendix — ex12 position (Optional, Not Explained)

[examples/ex12_position.html](examples/ex12_position.html)
Siblings: `static` (default) / `relative; top: 20px; left: 40px` / `absolute; right: 4px; bottom: 4px`

```css
.frame    { position: relative; }                           /* anchor for absolute children */
.relative { position: relative; top: 20px; left: 40px; }    /* nudged; its slot stays */
.absolute { position: absolute; right: 4px; bottom: 4px; }  /* out of the flow, placed by the frame's corner */
```

- Not covered in class. If you finish early, open it and change the values.
- Why B moves up into A's place in No. 3: A has left the document flow.

**Two ways to leave the document flow. `relative` keeps its slot; `absolute` doesn't.**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/my-web/index.html
DevTools device mode 375px
Menu: 홈 / 내 정보 / 방명록 (Home / About / Guestbook)   ← one per line, vertically
Intro paragraphs · hobby list: white cards with a border
Capture it with the address bar and the 375 width indicator visible
```

The 1280px screen and the experiment files in `week04/` are for checking only. Keep your real name, student ID, and real email out of the screenshot.

---

## Next Week Preview

So far only what the three pages **look like** has changed. Buttons and input fields still do nothing.

In Week 5 we empty `app.js` and rewrite it to start JavaScript.
We bring back the `<script src="app.js" defer></script>` line and print values to the Console.
`styles.css` stays as it is. The `.card` colors you chose today come back in Week 6's dark mode.
