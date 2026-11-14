---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 14"
footer: "REST API · PATCH · DELETE"
---

# Edit and delete a guestbook message

Use server IDs to change messages saved in Week 13.

Day 1: ID, DELETE, 204, read again
Day 2: PATCH, edit form, verify changes

Reports and presentations are separate assignments.

---

# Day 1 · 0–5 min — Array index and server ID

```js
const items = [{ id: 41 }, { id: 73 }];
console.log(items[0].id); // 41
```

Index 0 is a position. ID 41 identifies a server record.
Sorting does not change IDs.
[Example](examples/day1/ex01/index.html) · [Code](examples/day1/ex01/app.js)

---

# Day 1 · 5–10 min — Send DELETE

```text
DELETE /rest/v1/guestbook?id=eq.41&book_id=eq.student01
```

Choose one server ID in your assigned guestbook.
Never send an array index as the record ID.
[Example](examples/day1/ex02/index.html) · [Code](examples/day1/ex02/app.js)

---

# Day 1 · 10–15 min — Edit key header

```js
headers: {
  apikey: API_PUBLIC_KEY,
  "X-Edit-Key": editKey
}
```

The public API key does not identify a student.
Enter your assigned edit key while the page runs.
Keep it out of source files, URLs and screenshots.

---

# Day 1 · 15–20 min — 204 has no body

```js
if (!response.ok) {
  throw new Error(`HTTP ${response.status}`);
}
// Do not call response.json() after DELETE 204.
```

Inspect Method, Status and Response in Network.

---

# Day 1 · 20–25 min — Read again

GET the same ID after DELETE.

- Empty array: the record is absent.
- Record remains: check the ID and edit key.
- A rejected edit key may still produce 204 with no deletion.

[GET example](examples/day2/ex04/index.html) · [Code](examples/day2/ex04/app.js)

---

# Day 1 · 25–30 min — Lab

Create three practice messages, then delete the middle ID.
Check the request and GET the record again.

**Explanation total: 5 + 5 + 5 + 5 + 5 + 5 = 30 min**
[Lab](lab.md#1일차-실습) · [Walkthrough](walkthrough.md)

---

# Day 2 · 0–5 min — PATCH changes a record

```text
POST   /rest/v1/guestbook
PATCH  /rest/v1/guestbook?id=eq.41&book_id=eq.student01
```

POST creates a record. PATCH changes selected fields.
[Example](examples/day2/ex03/index.html) · [Code](examples/day2/ex03/app.js)

---

# Day 2 · 5–10 min — JSON request body

```js
method: "PATCH",
body: JSON.stringify({ message: message })
```

Include Content-Type, Prefer, apikey and X-Edit-Key headers.
Do not change id or book_id in the body.

---

# Day 2 · 10–15 min — Fill the edit form

```js
editId.value = item.id;
editMessage.value = item.message;
editMessage.focus();
```

Use the object belonging to the clicked button.
[Code](examples/day2/web-week14/actions.js)

---

# Day 2 · 15–20 min — Check changed rows

```js
const changed = await response.json();
if (changed.length !== 1) {
  throw new Error("Check the edit key and ID.");
}
```

A 200 response with [] did not change a record.
GET the same ID and compare its stored message.

---

# Day 2 · 20–25 min — Extend Week 13

Keep GET in guestbook.js and POST in submit.js.
Add actions.js, delete.js and edit.js.

[Page](examples/day2/web-week14/guestbook.html)
[GET](examples/day2/web-week14/guestbook.js) · [POST](examples/day2/web-week14/submit.js)
[DELETE](examples/day2/web-week14/delete.js) · [PATCH](examples/day2/web-week14/edit.js)
[Home](examples/day2/web-week14/index.html) · [About](examples/day2/web-week14/about.html) · [Home JS](examples/day2/web-week14/app.js) · [Profile](examples/day2/web-week14/images/profile.png)

---

# Day 2 · 25–30 min — Lab

Reload and verify the changed message and remaining records.
Clear the key field before taking a screenshot.

**Explanation total: 5 + 5 + 5 + 5 + 5 + 5 = 30 min**
[Lab](lab.md#2일차-실습) · [Walkthrough](walkthrough.md)
