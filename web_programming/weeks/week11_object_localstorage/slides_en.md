---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 11"
footer: "Objects and localStorage · 60-minute lecture · 30-minute lab"
---

# Objects and localStorage

In Week 10, each guestbook line was **one lump of text**, and the list disappeared on reload.

Each class has a **60-minute lecture and demo plus a 30-minute lab**. Day 2 requires ex04–ex06 only. The completed guestbook is an instructor demo and an optional Week 12 guestbook example.

- Day 1: turn each line into an **object** with a name, a message, and a date.
- Day 2: save the name/message and restore the form after reloading.
- Submit the restored ex06 form and saved JSON. **Localhost screenshots are accepted.**

---

# Day 1 — Objects and Dot Notation

`60-minute lecture and demo → 30-minute lab`

1. Repository folders and the static server
2. ex01 — objects `{ }` and dot notation (today's syntax)
3. ex02 — objects inside an array · the date template line
4. ex03 — an object as one list line

---

## Day 1 · 0–10 min — Folder structure and server

Prepare the files and server before class. Keep the repository's `web_programming` folder structure.

```text
web_programming/
  weeks/week11_object_localstorage/examples/
```

- Serve `web_programming` on port `8111`.
- ex01–ex07 load W3.CSS 4.1.0 from the CDN. The CDN needs internet access.
- Use Apply Name in ex01 and Check Array Result in ex02. The Console is an extra check; ex03 compares two lists.

Command and URLs: [Walkthrough](walkthrough.md#준비)

---

## Day 1 · 10–25 min — ex01 Objects and dot notation

[examples/day1/ex01/index.html](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex01/index.html) · [app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex01/app.js)

```js
const item = { name: '하늘', message: '안녕하세요', date: '2026. 11. 11.' };
console.log(item.name);    // 2. 하늘
console.log(item.nmae);    // 4. undefined — no red line
const item5 = { name: name, message: message, date: '…' };   // 5.
```

- Inside `{ }`, join `label: value` pairs with commas. An array `[ ]` is ordered; an object `{ }` has labels.
- Read a value with **dot notation**, `item.name`. No quotes around the label.
- `name: name` — the left is the label, the right is the variable.

**An object is a bundle of labeled values; write the label after the dot to get its value.**

---

## Day 1 · 25–40 min — ex02 Objects in an array · date template

[examples/day1/ex02/index.html](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex02/index.html) · [app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex02/app.js)

```js
texts.push('하늘: 안녕하세요');                  // 1·2. Week 10: one lump
const today = new Date().toLocaleDateString();  // the date template
items.push({ name: '하늘', message: '안녕하세요', date: today });   // 3.
console.log(items[0].name);                     // 4. 하늘
```

- `texts[0]` is one lump, `'하늘: 안녕하세요'`. You cannot take out just the name.
- `items[0]` picks **which** bundle; `.name` picks **which value**. Brackets come first.
- `toLocaleDateString()` is a **template**: today as text, like `2026. 11. 11.`.

**Brackets pick which one; the dot picks which value.**

---

## Day 1 · 40–55 min — ex03 An object as one list line

[examples/day1/ex03/index.html](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex03/index.html) · [app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex03/app.js)

```js
li1.textContent = items[i];   // 1. the object as is
li2.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
```

```text
1. [object Object]       2. 하늘: 안녕하세요 (2026. 11. 11.)
```

- Put a whole object in a text spot and you get `[object Object]`. **It is not an error**, so the Console stays quiet.
- Put dot-notation values inside backticks and `${ }` (Week 5) to write all three in one line.

**Put dot-notation values in a text spot, not the object itself.**

---

## Day 1 · 55–60 min — The 30-minute lab

[Day 1 lab](lab.md#1일차--객체와-점-표기-30분) · [Walkthrough](walkthrough.md#1일차)

| Lab time | Check |
|---|---|
| 0–8 min | ex01: change the property value; compare on screen |
| 8–16 min | ex02: change the last screen output index from 0 to 1 |
| 16–25 min | ex03: change name to message; restore the field |
| 25–30 min | Check the changed values and results |

Lecture: 10+15+15+15+5 = 60 min. Public deployment is outside this lab.

---

# Day 2 — Save and restore a form

60-minute lecture and demo → 30-minute lab

- Required: ex04 strings, ex05 JSON arrays, ex06 form data.
- Verify storage boundaries and saved values.
- Capture the restored ex06 form and its JSON.
- The completed guestbook is an instructor demo, not required lab work.

[Day 2 lab](lab.md#2일차--저장과-폼-복원-30분) · [Example guide](examples/README.md)

---

## Day 2 · 0–10 min — ex04 Save, load, and delete text

[index.html](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex04/index.html) · [app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex04/app.js)

```js
const key = 'week11-ex04-text';
localStorage.setItem(key, memoInput.value); // Save
const saved = localStorage.getItem(key);   // Load
localStorage.removeItem(key);              // Delete this key
```

Type → Save → reload → Load. Then Delete → Load: the result is null.
An empty string is still a stored value; null means the key is absent.
Inspect the key and value in F12 → Application → Local Storage.

---

## Day 2 · 10–25 min — ex05 A fixed array as JSON

[index.html](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex05/index.html) · [app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex05/app.js)

```js
const items = [
  { name: '하늘', message: '안녕하세요' },
  { name: '바다', message: '잘 봤습니다' }
];
localStorage.setItem('week11-ex05-items', JSON.stringify(items));
const text = localStorage.getItem('week11-ex05-items');
const restored = JSON.parse(text); // restored[0].name
```

Save JSON → Read raw text → Restore JSON: inspect the two restored rows.
Change a fixed value in app.js, reload, and save again to compare results.
Error handling and type checks are provided code; do not rewrite them.

---

## Day 2 · 25–40 min — ex06 Save and restore a form

[index.html](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex06/index.html) · [app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex06/app.js)

```js
const entry = { name: nameInput.value, message: messageInput.value };
localStorage.setItem('week11-ex06-entry', JSON.stringify(entry));
// After confirming that the stored key exists:
const back = JSON.parse(localStorage.getItem('week11-ex06-entry'));
nameInput.value = back.name;
messageInput.value = back.message;
```

Enter name and message → Save → change the fields → Load.
Empty fields are allowed here: this example isolates saving and restoring.
After reloading, press Load to restore the fields.

---

## Day 2 · 40–50 min — Storage belongs to an origin and browser

Origin = protocol + host + port. A URL path is not a storage boundary.

- Different example folders on the same origin share localStorage.
- Use distinct keys such as week11-ex04-text and week11-ex06-entry.
- A different browser, profile, or device has a separate stored list.
- localhost and the public HTTPS site have different storage.
- Use localhost or HTTPS for practice. Do not open examples with file://.

Shared lab PCs may retain the previous user's data in the same profile.
Sharing a list across devices requires the server API introduced next week.

---

## Day 2 · 50–55 min — Verify the stored result

| Action | Expected result |
|---|---|
| Save, change input, then Load | Saved value is restored |
| Reload, then Load | Same values and JSON are restored |
| Delete, then Load | No stored value |
| Save and restore again for capture | Inputs match the JSON |

Locate `setItem` → `getItem` → `JSON.parse` after checking the screen.
The key and origin must match to read the same stored value.

---

## Day 2 · 55–60 min — The 30-minute lab

| Lab time | Task |
|---|---|
| 0–8 min | ex04: save, load, delete |
| 8–16 min | ex05: compare raw JSON and restored fields |
| 16–27 min | ex06: save, reload, restore, delete |
| 27–30 min | Save and restore ex06 again; capture |

[Day 2 lab](lab.md#2일차--저장과-폼-복원-30분) · [Walkthrough](walkthrough.md#2일차)
Lecture total: 10+15+15+10+5+5 = 60 min.

---

## Submission — One restored-form screenshot

In ex06, use Save → reload → Load.

```text
Name: 하늘
Message: 안녕하세요
Stored JSON: {"name":"하늘","message":"안녕하세요"}
Status: 폼 복원 완료
```

Capture the inputs, JSON, and address bar. **Localhost is accepted.**
Public deployment is after-class work. Use sample names and messages.

---

## Next week and separate materials

The [completed guestbook](examples/day2/web-week11/README.md) is an instructor demo and an optional Week 12 guestbook example. Students do not need to build it in this week's lab.

In Week 12, use a public weather API to learn Promises and async/await. The optional guestbook includes this week's local version.

The demo uses `week11-guestbook-items`. Damaged data triggers a notice; Delete All removes only this key. Recovery is provided code, outside student implementation.

- [Advanced arrays](../../specials/array_advanced/README.md) is a separate supplementary class.
- [ex07 cross-tab synchronization](examples/day2/README.md#고급-저장-참고) is reference material.
