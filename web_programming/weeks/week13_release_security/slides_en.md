---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 13"
footer: "Security, Accessibility, and Release Check · see the principle through comparison examples, then assemble at the end"
---

# Security, Accessibility, and Release Check

By Week 12 you built four pages. This week is less about new features and more about **checking before you release**.

Same method as before: look at **8 comparison examples** one at a time, then **assemble** `about.html`, `about.js`, `projects.js`, and `README.md` in a new repository, `web-week13`, built on last week's files.

- Put typed text in **as text** — `textContent`
- Images, inputs, and links need **words that say what they are** — `alt`, `label for`, link text
- Before release: **links → Console → 375**; write the README with four Markdown marks

---

# Day 1 — Numbers, Text, and Accessibility

`30 min explanation & demo → 60 min lab`

1. The picker page — an input, a button, a result spot
2. ex01 — `Number()` and `isNaN()`
3. ex02 — `new Date().getFullYear()` and the year of study
4. ex03 — `textContent` vs. `innerHTML`
5. What never goes into a public repository
6. ex04 `alt` · ex05 `label for`

---

## Day 1 · 0–3 min — The picker page: a spot with an input

[examples/day1/index.html](examples/day1/index.html) — ex01 and ex02 use the same screen.

```html
<label for="year">입학 연도</label>
<input id="year" type="text" value="2023">
<button id="btn">눌러 보기</button>
<div id="result">결과 자리 — 버튼을 누르면 바뀐다</div>
```

- Turn on **only one** of the two `script` lines at the bottom (Ctrl+/, macOS ⌘+/).
- Type in the box and press **눌러 보기** → look at the screen and Console.

**What you type is read when the button is clicked.**

---

## Day 1 · 3–8 min — ex01 Number() and isNaN()

[examples/day1/ex01_number.js](examples/day1/ex01_number.js)

```js
const text = yearInput.value;                     // the box value is text
console.log('1. 글자 + 1 :', text + 1);            // 20231 — joined, not added
const year = Number(text);                        // text to a number
console.log('2. Number(글자) + 1 :', year + 1);    // 2024 — added
console.log('3. isNaN(바꾼 값) :', isNaN(year));    // false
```

- `Number('이천이십삼')` → `NaN` (Not a Number), `isNaN(NaN)` → `true`
- An empty box: `Number('')` → `0`. That is why we also check `text === ''`.

**Turn box text into a number with `Number()`, and ask whether it worked with `isNaN()`.**

---

## Day 1 · 8–12 min — ex02 This year and the year of study

[examples/day1/ex02_year.js](examples/day1/ex02_year.js)

```js
const thisYear = new Date().getFullYear();  // 1. this year → 2026
console.log('2. 올해 - 입학 연도 :', thisYear - year);  // 2. 2026 - 2023 → 3
const years = thisYear - year + 1;          // 3. the entry year is year 1 → 4
```

- This is `getFullYear()` from Week 5 ex10. Don't type `2026` by hand.
- Forget the parentheses (`getFullYear;`) and you get `NaN년차` with no error. Call with parentheses.

**Get this year with `new Date().getFullYear()`.**

---

## Day 1 · 12–18 min — ex03 textContent vs. innerHTML

[examples/day1/ex03_text_html.html](examples/day1/ex03_text_html.html) · [ex03_text_html.js](examples/day1/ex03_text_html.js)

```js
output.textContent = input.value;   // 1. <b>안녕</b> shows as plain text
output.innerHTML = input.value;     // 2. bold 안녕 — the tag becomes a real element
output.innerHTML = '';              // 3. emptying — the only use of innerHTML
```

- Same input, same spot, **one word** different.
- Type `<button>가짜 버튼</button>` → No. 2 makes a real button. What if someone else wrote it?

**Put typed text in with `textContent`. Use `innerHTML` only to empty.**

---

## Day 1 · 18–21 min — What never goes into a public repository

| Never put in | Use this example instead |
|---|---|
| Real name, student ID, phone number | `student01` |
| Real email | `student01@example.com` |
| Passwords, login keys | Write nothing |

- The repository is **Public**. Anyone with the address can open the files.
- Once uploaded, it stays in GitHub's earlier history even after you delete it from the file. Keep it out **from the start**.
- Screenshots too. Your ID in the address bar is fine.

**Use only example values in a public repository.**

---

## Day 1 · 21–25 min — ex04 alt: the words read when an image can't be seen

[examples/day1/ex04_alt.html](examples/day1/ex04_alt.html) · image [images/profile.png](examples/day1/images/profile.png)

```html
<img src="images/profile.png" alt="student01의 프로필 그림" width="160">
<img src="images/profile.png" width="160">
<img src="images/profile.png" alt="그림" width="160">
```

- 1 a fitting alt / 2 no alt / 3 the one word '그림'. All three look the same.
- Change `src` to `images/nothing.png` and what is left in each spot differs.

**`alt` is the text read in place of an image. Say what the image is.**

---

## Day 1 · 25–28 min — ex05 label for: connect the label to the box

[examples/day1/ex05_label.html](examples/day1/ex05_label.html)

```html
<label for="year1">입학 연도</label> <input id="year1">    <!-- 1. same -->
<label for="year2">입학 연도</label> <input id="years2">   <!-- 2. different -->
입학 연도 <input id="year3">                               <!-- 3. no label -->
```

- Click each label. Only No. 1 moves the cursor into its box.
- No. 1 and No. 3 look the same. You only know they are connected by **clicking**.

**`for` and `id` must match letter for letter to connect the label to the box.**

---

## Day 1 · 28–30 min — Your turn

[Day 1 lab](lab.md#1일차--숫자와-글자-그리고-접근성-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

1. New folder `web-week13` with last week's files; today's seven files and one image in `ex/`.
2. ex01–ex05 — change values. Say what will change first.
3. Create the new repository `web-week13`, push, and turn on Pages.

**Total explanation: 3+5+4+6+3+4+3+2 = 30 min**

---

# Day 2 — README, Checks, and Assembly

`30 min explanation & demo → 60 min lab`

1. ex06 — link and button text, and the Tab key
2. ex07 — Markdown `#` and `-`
3. ex08 — links and images, one `!` apart
4. The release check order — links → Console → 375
5. Week 14 presentation · Week 15 problem bank
6. Assembly — `about.html`, `about.js`, `projects.js`, `screenshots/`, `README.md`

---

## Day 2 · 0–5 min — ex06 Link and button text

[examples/day2/ex06_link_text.html](examples/day2/ex06_link_text.html)

```text
1. 페이지 열기 · 페이지 열기 · 페이지 열기          ← where does each go?
2. img 설명 열기 · label 설명 열기 · a 설명 열기    ← the text alone tells you
3. [▶]  [계산하기]                                  ← what does it do?
```

- Move with the **Tab** key and read only the text of the outlined item.
- In Week 12 all three card links said `페이지 열기`. You fix that in today's assembly.

**Write link and button text that tells what it is on its own.**

---

## Day 2 · 5–10 min — ex07 Markdown # and -

[examples/day2/ex07_line_marks.md](examples/day2/ex07_line_marks.md) — Week 9 review · preview (Ctrl+K V)

```markdown
# 큰 제목
## 작은 제목 — README 의 절 제목
- 목록 한 줄
#띄어쓰기가 없으면 글자 그대로
```

- Two plain lines with only a line break **join into one line** in the preview. That is why we add `- `.

**The mark at the start of a line, plus one space, decides what the line becomes.**

---

## Day 2 · 10–16 min — ex08 Links and images

[examples/day2/ex08_link_image.md](examples/day2/ex08_link_image.md) · image [images/profile.png](examples/day2/images/profile.png)

```markdown
[13주차 실습 페이지](https://github.com/…)        1. a link
![student01의 프로필 그림](images/profile.png)   2. ! before a link → an image
[student01의 프로필 그림](images/profile.png)    3. without ! → a link
![student01의 프로필 그림](images/Profile.png)   4. different capitals
```

- The text in the brackets is the image's `alt` (ex04).
- No. 4 shows in your PC's preview but breaks once it is on GitHub.

**An image is a link with `!` in front. Write the path exactly like the file name.**

---

## Day 2 · 16–21 min — The release check order

```text
1. Links     click all four nav links and three card links — no 404
2. Console   zero red lines on every page, also after clicks (favicon 404 aside)
3. 375 wide  device mode (Ctrl+Shift+M) — nothing pushed sideways
```

- Keep the order. If you read Console while a link is broken, the causes get mixed.
- Then check image `alt` (ex04), labels (ex05), and personal information once each.
- Your PC's server opens files even when capitals differ. After pushing, click the links **once more at the public address**.

**Find problems in order before fixing: links → Console → 375.**

---

## Day 2 · 21–25 min — Week 14 presentation and the Week 15 problem bank

- Week 14 is a **3-minute demo**, at the public address of `web-week14`, started from today's files.
- Order: public address → move between pages → dark mode → empty-form notice → add and delete guestbook entries → reload → JSON cards → Commits tab and README
- The report is today's final `README.md`. There is no separate document.
- The Week 15 final practical comes from the [problem bank](../week15_final_exam/examples/README.md) built from Weeks 1–14 labs, with the values changed.
- This week's submission is in it as the [w13_text_safe](../week15_final_exam/examples/w13_text_safe/README.md) problem.

**A presentation shows the screen by clicking, not by talking.**

---

## Day 2 · 25–30 min — Assembly: web-week13, then the lab

```text
about.html   script line · form · label for · result card  ← ex05 · ex06
about.js     Number · isNaN · getFullYear · + 1             ← ex01 · ex02
             submit · preventDefault · trim                 ← Week 12 guestbook.js
projects.js  `${projects[i].title} 열기`                    ← ex06 No. 2
README.md    # · ## · - · link · image lines                ← ex07 · ex08
```

[Day 2 lab](lab.md#2일차--readme-와-점검-그리고-조립-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

1. ex06–ex08 values (to min 17) → assemble (README last) → links, Console, 375.
2. Push → repo README → links again at the public URL → guestbook capture at 375.

**Total explanation: 5+5+6+5+4+5 = 30 min**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/web-week13/guestbook.html   (device mode 375px)
List ─ student02: <b>안녕</b> (date) [삭제]   ← plain text, not bold
F12 › Console ─ no red lines (a favicon.ico 404 doesn't count)
Include the address bar in the screenshot
```

Keep your real name, student ID, and real email out of the screenshot. Your ID is fine.

---

## Next Week Preview

This week your four pages became ready to release.

In Week 14 you start a new repository, `web-week14`, from today's files and give a **3-minute demo** at its public address.
The report is today's final `README.md`; there are no new features to build.
The Week 15 final takes one problem per area from the problem bank built from Weeks 1–14 labs, with only the values changed.
