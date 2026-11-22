---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 14"
footer: "REST API · PATCH · DELETE"
---

# Edit and delete guestbook messages

Extend Week 13 GET and POST with server-ID-based DELETE and PATCH.
Each day: lecture/demo 60 min + student lab 30 min.
Day 1: three DELETE edits. Day 2: three PATCH edits.
Prepare files/repository before class; publish after class.
Reports and presentations are separate assignments.

---

# Day 1 · 0–20 min: Setup and server IDs

Setup check 5 min + index and ID 15 min

```js
const items = [{ id: 41 }, { id: 73 }];
console.log(items[0].id); // 41
```

Position 0 differs from ID 41. Reordering keeps each object's ID.
[ex01](examples/day1/ex01/index.html) · [Code](examples/day1/ex01/app.js)

---

# Day 1 · 20–30 min: Edit keys

The public key permits API calls. The edit key controls changes.
BOOK_ID groups messages; it is not editing authorization.

```js
headers: { apikey: API_PUBLIC_KEY, 'X-Edit-Key': editKey }
```

The settings file and key handling are provided. The edit key's Clear key also clears memory.
Enter the public key at the first-visit prompt; it stays in localStorage. The edit key is never stored.
If the public key is wrong, press Clear public key and enter it again.

---

# Day 1 · 30–40 min: DELETE target and request

```text
DELETE /rest/v1/guestbook?id=eq.41&book_id=eq.student01
```

Three student edits: target URL, method, headers.
Use the server ID of your own practice message.
Check about → help → list → target GET first.
[ex02](examples/day1/ex02/index.html) · [Requests](examples/day1/ex02/requests.http)

---

# Day 1 · 40–45 min: 204 has no body

```js
if (!response.ok) throw new Error(`HTTP ${response.status}`);
// Do not call response.json() after DELETE 204.
```

Inspect Method, Status and Response in Network.
204 alone does not prove deletion; an invalid key may also return 204.

---

# Day 1 · 45–55 min: GET the same ID

```js
const remaining = await readMessage(url);
```

Check an empty result and ensure other records remain.
If the target remains, check the key and ID. Verification code is provided.
[ex04](examples/day2/ex04/index.html) · [Code](examples/day2/ex04/app.js)

---

# Day 1 · 55–60 min: Lab guidance

Lecture/demo: 5 + 15 + 10 + 15 + 10 + 5 = 60 min.
Lab 30 min: ID/.http 5 → three DELETE edits 12 → correct/wrong key verification 13.
Delete only the selected ID. Publish after class.
[Lab](lab.md#1일차-실습) · [Walkthrough](walkthrough.md)

---

# Day 2 · 0–20 min: Setup and PATCH

Setup check 5 min + PATCH 15 min

```js
method: 'PATCH',
body: JSON.stringify({ message: message })
```

Do not put id or book_id into the change body.
Three student edits: target URL, JSON body, same-ID GET.
[ex03](examples/day2/ex03/index.html) · [Requests](examples/day2/ex03/requests.http)

---

# Day 2 · 20–30 min: Fill the edit form

```js
editId.value = item.id;
editMessage.value = item.message;
editMessage.focus();
```

Use the clicked object's ID. Create and edit forms are separate.
Form wiring is provided.
[guestbook.js](examples/day2/web-week14/guestbook.js)

---

# Day 2 · 30–40 min: Inspect the response array

PATCH 200 [] does not prove a change.
Check the returned ID and row count.

```js
const changed = await response.json();
```

Headers: apikey, X-Edit-Key, Content-Type, Prefer.
After a network error, GET before repeating a write.

---

# Day 2 · 40–45 min: Verify the saved message

```js
const saved = await readMessage(url);
```

The same ID must contain the submitted message.
Distinguish verification failure from a rejected write.
Provided guards keep a late GET response from overwriting the newer list.

---

# Day 2 · 45–55 min: CRUD in one file

guestbook.js contains GET, POST, DELETE and PATCH sections.
config.example.js is provided separately; change only BOOK_ID.
Initialize DOM references, functions and events before the first GET.

[Page](examples/day2/web-week14/guestbook.html) · [Behavior](examples/day2/web-week14/guestbook.js)
[Settings](examples/day2/web-week14/config.example.js)
[Home](examples/day2/web-week14/index.html) · [About](examples/day2/web-week14/about.html)

---

# Day 2 · 55–60 min: Lab guidance

Lecture/demo: 5 + 15 + 10 + 15 + 10 + 5 = 60 min.
Lab 30 min: three PATCH edits 12 → three records and error recovery 13 → clear key/capture 5.
Complete localhost checks first. After class, enter the public key when Pages or another browser first prompts, then check.
[Lab](lab.md#2일차-실습) · [Walkthrough](walkthrough.md)
