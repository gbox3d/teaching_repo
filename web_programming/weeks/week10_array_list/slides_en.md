---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 10"
footer: "Arrays · for · showList · splice"
---

# Drawing Array Data as a List

The feed in Weeks 7 and 9 showed the author, time and message, newest first.

The Week 10 starter shows one string per row in insertion order. The first row is `items[0]`.

- Array: push, length, indexes
- Iteration: classic for
- Rendering: showList
- Deletion: splice(i, 1)

DOM-only deletion is possible. This lesson uses an array to study data and rendering.

---

# Day 1 — 60-Minute Lecture, 30-Minute Lab

| Lecture and demonstration | Minutes |
|---|---:|
| Preparation check | 5 |
| Arrays, push, length | 20 |
| Indexes and for | 20 |
| li, textContent, append | 10 |
| Lab handoff | 5 |

Required edits: two strings in ex01 and five lines in the ex02 starter.
Prepare files before class; upload after class.

---

## Arrays, push and length — Minutes 5–25

[ex01](examples/day1/ex01/index.html) · [Code](examples/day1/ex01/app.js)

```js
let items = [];
items.push('student01: 안녕하세요');
items.push('student02: 고맙습니다');
items.push('student03: 반갑습니다');
```

Check length 3, items[0], and items[2] on screen.
items[3] is undefined because that index does not exist.
Add a value, then reset to an empty array.

The display function and JSON.stringify are provided.

---

## The Classic for Loop — Minutes 25–45

[ex02 complete](examples/day1/ex02/index.html) · [Starter](examples/day1/ex02/start.html)

```js
for (let i = 0; i < items.length; i++) {
  const li = document.createElement('li');
  li.textContent = items[i];
  list.append(li);
}
```

Start at 0, continue below length, increment i by 1.
An empty array runs the body zero times.
Compare the fixed limit 3 above with the array length below.

---

## Create and Append — Minutes 45–55

[ex03](examples/day1/ex03/index.html)

```js
const li2 = document.createElement('li');
li2.textContent = '2. 만들고 붙인 줄';
list.append(li2);
```

li1 is created but initially detached.
Click the append button to place it at the end.
Appending the same li1 again moves it; it does not clone it. The total stays at three.

---

## Update the Array and DOM Separately

[ex04](examples/day1/ex04/index.html), instructor demonstration

```js
items.push(text);
const li = document.createElement('li');
li.textContent = text;
list.append(li);
count.textContent = `${items.length}개`;
```

Omit push: rows grow while the count stays zero.
Omit append: the count grows without rows.
An empty string is also one array value in this example.

---

## Memory, Browser Storage and the Server

| Location | Lesson | After reload |
|---|---|---|
| JavaScript array | Week 10 | Initial array |
| localStorage | Week 11 | Same-origin values remain |
| Shared server | Weeks 12–14 | Read again with GET |

Week 11 requires string, JSON and form storage. The full stored guestbook is a provided demonstration.
Supabase provisioning belongs to the [special session](../../specials/supabase_guestbook/README.md).

---

## Day 1 Required Lab — 30 Minutes

[Lab](lab.md#1일차) · [Walkthrough](walkthrough.md#1일차)

1. Change two push strings in ex01: 5 minutes
2. Complete five for/body lines in app.start.js: 15 minutes
3. Comment out the push line; compare arrays of 0, 1 and 3 values: 10 minutes

The lower list count must match the array.
The upper loop uses the fixed limit 3 and always produces three rows.
Editing ex03 and ex04 is optional.

---

# Day 2 — 60-Minute Lecture, 30-Minute Lab

| Lecture and demonstration | Minutes |
|---|---:|
| Preparation check | 5 |
| showList | 15 |
| Clear and redraw | 15 |
| Delete-button template | 15 |
| Form handoff | 5 |
| Lab handoff | 5 |

Required edits: two insertion lines and two deletion lines in the provided starter.

---

## showList — Minutes 5–20

[ex06](examples/day2/ex06/index.html)

```text
Clear the list
  → create and append one li per array value
  → display the count
  → display an empty notice when count is zero
```

Call it once on load and after changing the array.
The count and notice stay outside the loop.
They must run even when the array is empty.

---

## Clear and Redraw — Minutes 20–35

[ex05](examples/day2/ex05/index.html)

```js
list.innerHTML = '';
for (let i = 0; i < items.length; i++) {
  const li = document.createElement('li');
  li.textContent = items[i];
  list.append(li);
}
```

Button 1 produces 3, 6, 9 rows. Button 2 always produces 3.
Use textContent for input; use innerHTML only to clear.

---

## Delete-Button Template — Minutes 35–50

[ex07](examples/day2/ex07/index.html)

```js
removeButton.addEventListener('click', function () {
  items.splice(i, 1);
  showList();
});
```

Button creation, styles and the event wrapper are provided.
Students write the two lines that delete one value and redraw.
Redrawing gives each button a fresh index i.
Deleting the middle entry must preserve the first and third entries.

---

## Form Handoff — Minutes 50–55

[Guestbook starter](examples/day2/web-week10/guestbook.start.html)

In the Week 10 starter, replace the three lines that append a row inside submit with these two lines.

```js
items.push(`${name}: ${message}`);
showList();
```

HTML, validation, showList and the initial call are provided.
Leaving the old append lines adds the same entry twice.
The browser validates an optional email; it is not stored in the array.

---

## Day 2 Required Lab — 30 Minutes

[Lab](lab.md#2일차) · [Walkthrough](walkthrough.md#2일차)

1. Replace three insertion lines with two: 10 minutes
2. Complete the two deletion TODO lines: 8 minutes
3. Add three, delete the middle, then delete all: 7 minutes
4. Add three again, delete the middle and capture: 5 minutes

Copy the completed guestbook.start.js into guestbook.js and check the regular page.
Further changes to ex05–07 are optional.

---

## Submission and Checks

One screenshot: localhost address bar, two remaining entries, delete buttons and count 2.

- Reject blank names/messages and malformed email
- Display tag-like strings as text
- Check long text and buttons at 375px and 1280px
- Reload resets to an empty array and count zero

Commit, push and verify Pages after class. Deployment delay does not postpone the in-class capture.

---

## Next Week and Optional Practice

Week 11 reads object fields and practices string, JSON and form storage/retrieval.
The full stored guestbook is a provided demonstration, separate from required student implementation.
Localhost is valid for storage checks and screenshots.

forEach, filter, map and reduce belong to the separate [advanced arrays session](../../specials/array_advanced/README.md).
Direct SPA conversion is optional after Week 14.
