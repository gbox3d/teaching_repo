---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 4"
footer: "CSS and Responsive UI · compare the parts one at a time, then assemble at the end"
---

# CSS and Responsive UI

Prepare the `web-week04` folder and new repository before class.
Start with Week 3 content and the provided CSS links and card classes.

- Keep all 13 comparisons and optional appendix ex14.
- The instructor demonstrates the comparisons and full assembly.
- Students edit only the required values in the supplied files.
- Each day: 60 minutes lecture/demo, then 30 minutes lab.
- Capture locally in class; upload after class. W3.CSS starts in Week 7.

---

# Day 1 — Selectors and Boxes

`60 min lecture & demo → 30 min lab`

1. ex01 selectors — a rule applies only when it matches; when they overlap, the class wins
2. ex02 display — whether an element takes a whole line is decided by display, not the tag
3. ex03 box model — padding · border · margin, three layers
4. ex04 width · max-width — which one shrinks when the window narrows
5. ex05 margin auto — split the leftover width to center a box
6. ex06 text-align — where the text sits horizontally inside a box

---

## Day 1 · 0–5 min — This Week: Parts First, Assembly Last

```css
selector {
  property: value;
}
```

- One rule = selector + braces + `property: value;` lines, kept in `styles.css` and loaded by `<link rel="stylesheet" href="styles.css">` (examples and pages alike).
- Color and font properties mean what they say: `color` · `background-color` · `font-size` · `font-family`.
- **CSS gives no error message when it's wrong.** A non-matching selector or a missing semicolon is silently ignored.
- So we put siblings side by side and compare **by eye**. A value that changes nothing is a result too.

First 5 minutes: check the prepared files and running page.

---

## Day 1 · 5–15 min — ex01 Selectors: Must Match; the Class Wins

[examples/day1/ex01/index.html](examples/day1/ex01/index.html) · [styles.css](examples/day1/ex01/styles.css)
Siblings: `p` / `p.red` / `div.red` / `p.Red` (typo) / `nav a` / `a` outside nav

```css
p     { color: blue; }    /* tag selector: every p */
.red  { color: red; }     /* class selector: class="red", any tag */
nav a { color: green; }   /* descendant selector: a inside nav */
/* p { color: gray; } */
```

- No. 2 is `p` and `.red` → red. No. 4 `class="Red"` is not `.red` → blue.
- Try it: uncomment → only No. 1 and 4 turn gray; No. 2 stays red. Change No. 4 to `class="red"` → red.

**A selector must match. In this example, a class selector has higher specificity than a tag selector. Only at equal strength does the later rule win.**

---

## Day 1 · 15–20 min — ex02 display: The Tag Doesn't Decide, display Does

[examples/day1/ex02/index.html](examples/day1/ex02/index.html) · [styles.css](examples/day1/ex02/styles.css)
Siblings: 3 divs / 3 spans / span + `display: block` / div + `display: inline`

```css
.as-block  { display: block; }   /* takes a whole line */
.as-inline { display: inline; }  /* flows sideways like text */
```

- No. 1 divs fill each line; No. 2 spans flow sideways, as wide as their text. A new color = a new box.
- Try it: swap `block` and `inline` in the two classes → No. 3 and 4 swap shapes.

**Whether an element takes a whole line is decided by `display`, not by the tag.**

---

## Day 1 · 20–35 min — ex03 Box Model: Three Layers

[examples/day1/ex03/index.html](examples/day1/ex03/index.html) · [styles.css](examples/day1/ex03/styles.css)
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

## Day 1 · 35–43 min — ex04 width vs max-width: Which One Shrinks

[examples/day1/ex04/index.html](examples/day1/ex04/index.html) · [styles.css](examples/day1/ex04/styles.css)
Siblings: default (parent width) / `width: 640px` / `max-width: 640px`

```css
.w  { width: 640px; }        /* stays 640px, sticks out of a narrow window */
.mw { max-width: 640px; }    /* at most 640px, shrinks with the window */
```

- In a wide window No. 2 and 3 are both 640px. The difference appears when the parent has less than 640px available.
- Try it: narrow the window to 400px → only No. 2 sticks out and a scrollbar appears.

**`width` pins the width; `max-width` only sets a ceiling, so it shrinks with the window.**

---

## Day 1 · 43–50 min — ex05 margin auto: Split the Leftover Width to Center

[examples/day1/ex05/index.html](examples/day1/ex05/index.html) · [styles.css](examples/day1/ex05/styles.css)
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

## Day 1 · 50–55 min — ex06 text-align: Where the Text Sits Inside a Box

[examples/day1/ex06/index.html](examples/day1/ex06/index.html) · [styles.css](examples/day1/ex06/styles.css)
Siblings: default (left) / `text-align: center` / `text-align: right`

```css
.center { text-align: center; }
.right  { text-align: right; }
```

- The box stays the full window width; only the **text inside** moves. ex05 moved the box itself.
- Try it: change No. 3's `right` to `center`. The assembly uses this line to center the footer text.

**`text-align` sets where text sits horizontally inside a box. The box itself doesn't move.**

---

## Day 1 · 55–60 min — Required Lab Edits

[Lab](lab.md#1일차--선택자와-박스-30분) · [Walkthrough](walkthrough.md#1일차)

1. 0–10 min: ex01 `.red` color → `orange`; ex03 `.pad` → `32px`.
2. 10–25 min: site `h1 color` → `#365314`, `.card padding` → `20px`, `body max-width` → `600px`.
3. 25–30 min: save, reload, and check the three pages.

ex02/04/05/06 are instructor demonstrations. Further edits are optional.
Files and repository are prepared before class; upload after class.
Lecture: preparation 5 + selectors 15 + box model 15 + width/margin 15 + comparison 5 + handoff 5 = 60 minutes.

---

# Day 2 — flex, Then Assembly

`60 min lecture & demo → 30 min lab`

1. Five lines of flex principle — parent, main axis, cross axis
2. ex07 · ex08 · ex09 — direction sets the main axis; justify is main axis, align is cross axis
3. ex10 · ex11 · ex12 — wrap and gap go on the parent; flex: 1 goes on the child
4. ex13 — @media applies only when the condition holds
5. Assembly — gather `styles.css` from the parts

---

## Day 2 · 0–10 min — Five Lines of flex: Parent, Main Axis, Cross Axis

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

ex07–ex12 check these five lines one per example. Gray is the parent; colored boxes are the children.

0–5 min: check files. 5–10 min: parent and axes.

---

## Day 2 · 10–15 min — ex07 flex-direction: Sets the Main Axis

[examples/day2/ex07/index.html](examples/day2/ex07/index.html) · [styles.css](examples/day2/ex07/styles.css)
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

## Day 2 · 15–25 min — ex08 justify-content: Leftover Space on the Main Axis

[examples/day2/ex08/index.html](examples/day2/ex08/index.html) · [styles.css](examples/day2/ex08/styles.css)
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

## Day 2 · 25–30 min — ex09 align-items: Position on the Cross Axis

[examples/day2/ex09/index.html](examples/day2/ex09/index.html) · [styles.css](examples/day2/ex09/styles.css)
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

## Optional reference — ex10 flex-wrap: Wrap When They Don't Fit

[examples/day2/ex10/index.html](examples/day2/ex10/index.html) · [styles.css](examples/day2/ex10/styles.css)
Siblings: `nowrap` (default) / `wrap` — six 80px children in a 300px frame

```css
.nowrap { flex-wrap: nowrap; }  /* default: forces one line */
.wrap   { flex-wrap: wrap; }    /* moves the rest to the next line */
```

- 80 × 6 = 480px. No. 1 shrinks all six to 50px; No. 2 wraps them into two lines of three.
- Try it: 6 children → 3 → no shrinking, no wrapping.

**Whether children wrap when they don't fit is decided by `flex-wrap`, on the parent.**

Optional reading; no required lab edit.

---

## Day 2 · 30–35 min — ex11 gap: Space Between Children

[examples/day2/ex11/index.html](examples/day2/ex11/index.html) · [styles.css](examples/day2/ex11/styles.css)
Siblings: no gap / `gap: 16px` / `gap: 32px`

```css
.gap16 { gap: 16px; }   /* space between children; goes on the parent */
.gap32 { gap: 32px; }
```

- Only the spaces between open up; no gap is added before the first or after the last box.
- Try it: move `gap16` from the frame to `상자 1`'s class → nothing happens.

**A gap between children can't be set by one child, so `gap` goes on the parent.**

---

## Optional reference: ex12 flex: 1, Takes the Leftover Space

[examples/day2/ex12/index.html](examples/day2/ex12/index.html) · [styles.css](examples/day2/ex12/styles.css)
Siblings: default / middle only `flex: 1` / all three `flex: 1`, comment `flex: 2`

```css
.grow { flex: 1; }   /* this child takes the leftover space on the main axis */
/* flex: 2; */       /* 2:1 when two share */
```

- The one property that goes on the **child**: "I take the leftover space" is the child's claim.
- Try it: `style="flex: 2"` on the middle `<div>` of No. 3 → double share. Uncommenting `flex: 2` in `.grow` changes nothing (all three become 2).

**`flex: 1` makes the child take the leftover space. Several children split it by their numbers.**

Optional reading; no required lab edit.

---

## Day 2 · 35–50 min — ex13 @media: Conditional Rules

[examples/day2/ex13/index.html](examples/day2/ex13/index.html) · [styles.css](examples/day2/ex13/styles.css)
Siblings: a box with an `@media (max-width: 600px)` rule / a box without

```css
.with-media { background-color: lightskyblue; }   /* normal color */
@media (max-width: 600px) {                        /* try 900px */
    .with-media { background-color: orange; }
}
```

- At ≤ 600px the inner rule lives; same selector twice → the later wins (ex01). Check at 375.
- Try it: 600 → 900 → orange at an 800px viewport. Drop the colon → ignored, no error.

**The inner rule lives only when the condition holds. Any property can change.**

---

## Day 2 · 50–60 min — Assembly Demo and Lab Handoff

50–55 min: demonstrate the supplied CSS assembly. 55–60 min: lab instructions.

```css
nav { display: flex; gap: 16px; flex-wrap: wrap; }
@media (max-width: 600px) { nav { flex-direction: column; } }
```

1. Lab 0–10: ex07 `.column` direction → `row`; ex08 `.center` alignment → `flex-end`.
2. 10–22: site `gap` → `24px`, breakpoint → `700px`; compare `row`, then restore `column` (3 existing lines, at most 5).
3. 22–30: check 375/1280px; capture the 375px home page locally.

[Lab](lab.md#2일차--flex와-조립-30분) · [Walkthrough](walkthrough.md#2일차)
Lecture: preparation 5 + parent/axes 20 + gap/alignment 10 + media 15 + assembly 5 + handoff 5 = 60 minutes. Upload after class.

---

## Appendix — ex14 position (Optional, Not Explained)

[examples/day2/ex14/index.html](examples/day2/ex14/index.html) · [styles.css](examples/day2/ex14/styles.css)
Siblings: `static` (default) / `relative; top: 40px; left: 40px` / `absolute; right: 0; bottom: 0`

```css
.frame    { position: relative; }                           /* anchor for absolute children */
.relative { position: relative; top: 40px; left: 40px; }    /* nudged; its slot stays */
.absolute { position: absolute; right: 0; bottom: 0; }      /* out of the flow, placed by the frame's corner */
```

- Not covered in class. If you finish early, open it and change the values.
- In No. 2 A's original slot (the top) stays empty; in No. 3 B moves up into A's place because `absolute` took A out of the document flow.

**`relative` stays in document flow and keeps its original slot. `absolute` leaves the flow.**

---

## What to Submit

Submit one screenshot of the 375px home page during class.

- A local file URL or localhost is accepted.
- Show the address bar and the device width indicator.
- Show the vertical menu and the bordered introduction/hobby cards.
- Check 1280px separately; example files are for checking only.

After class, upload to the prepared `web-week04` repository and check Pages.
Use aliases and fictional contact details.

---

## Next Week Preview

The guestbook has no message list or storage yet. Native email validation blocks invalid email; a valid submit reloads the current page with GET and clears the inputs.

Before Week 5, copy this result without `.git` into `web-week05`.
Keep the CSS; rewrite `app.js` and reconnect it with `defer`.
Use the supplied output button to see JavaScript results on screen.
The `.card` colors return in Week 6 dark mode. W3.CSS starts in Week 7.
