---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 14"
footer: "REST API · PATCH · DELETE"
---

# Delete the middle entry and edit a remaining one

| Example ID | Before | After the exercise |
|---|---|---|
| 81 | Bring the sheet music | Bring the sheet music |
| 73 | Order snacks | Gone from the list |
| 41 | Rehearsal at 3 | Rehearsal at 4 |

Before class, open the [Week 14 guestbook](examples/day2/web-week14/guestbook.html). Enter the three messages from the bottom of the table up, click **남기기** (Post) for each, and record the three IDs you receive.

Day 1 covers deletion. Day 2 covers editing the rehearsal time. Each day has a 60-minute lecture and demo and a 30-minute lab.

---

# Day 1 · 0–20 min: Setup and server IDs

```js
const items = [{ id: 41 }, { id: 73 }];
console.log(items[0].id); // 41
```

Swap the two objects. Entry 73 now occupies position 0. Entry 41 moves to the second position and its ID is still 41.

The guestbook shows newest entries first. Adding an entry can move the middle one.
Each Delete button uses the `row.id` stored in its own row.

[Array position and server ID](examples/day1/ex01/index.html) · [Example code](examples/day1/ex01/app.js)

---

# Day 1 · 20–30 min: Book tags and entry IDs

```http
GET /rest/v1/guestbook?book_id=eq.student01&id=eq.73
```

`book_id` selects a guestbook. `id` selects an entry in it.
Set `BOOK_ID` to your tag in `config.example.js`. Enter the classroom publishable key when prompted on your first visit.

Anyone with that `apikey` can change entries under any tag. Use entries you wrote for the lab.

[Guestbook settings](examples/day2/web-week14/config.example.js)

---

# Day 1 · 30–40 min: DELETE target and request

Click **Delete (삭제)** beside entry 73, “Order snacks.”
Choose **Cancel** to send zero requests. Click the same button again and confirm.

```js
const url = bookUrl + '&id=eq.' + id;
const response = await fetch(url, {
  method: 'DELETE',
  headers: { apikey: API_PUBLIC_KEY }
});
```

`bookUrl` already includes your tag. The button supplies the entry ID.
[Delete from a row](examples/day1/ex02/index.html) · [Delete code](examples/day1/ex02/app.js)

---

# Day 1 · 40–45 min: 204 has no body

| Browser action | What the Network panel shows |
|---|---|
| Cancel the confirmation | No DELETE request |
| Confirm the deletion | DELETE → 204, empty response body |
| Send DELETE again with the same ID | Can also return 204 |

A 204 has no JSON body to read. After checking its status, **GET the same entry ID**.

---

# Day 1 · 45–55 min: GET the same ID

| What to look up after deletion | Example result |
|---|---|
| GET your tag and ID 73 | `200 []` |
| GET the list for your tag | Entries 81 and 41 remain |

Check that entry 73 exists before deletion so you can compare the two reads.
In [Read an entry again](examples/day2/ex04/index.html), enter the same ID and click **Read again (다시 읽기)**.
For the deleted ID, the page shows **해당 글 없음** (No matching entry).

---

# Day 1 · 55–60 min: Lab guidance

| Lab time | What to do in your guestbook |
|---|---|
| 0–5 min | Prepare three entries. Run about, help, and the list GET. Set `MESSAGE_ID` in `.env` to the middle entry's ID and GET that entry. |
| 5–17 min | In the supplied `guestbook.js`, fill in the DELETE URL, method, and headers. |
| 17–30 min | Cancel the middle row's deletion, then confirm it. Check the empty array for that ID and the two remaining entries. |

Open the [VS Code requests](examples/day1/ex02/requests.http) and click **Send Request** above each request.
[Day 1 lab](lab.md#1일차-실습)

---

# Day 2 · 0–20 min: Setup and PATCH

Change entry 41 from “Rehearsal at 3” to “Rehearsal at 4.”

```http
PATCH /rest/v1/guestbook?id=eq.41&book_id=eq.student01
apikey: {{apiKey}}
Content-Type: application/json
Prefer: return=representation

{ "message": "Rehearsal at 4" }
```

The URL selects the entry. The body carries the new value.
In the [PATCH example](examples/day2/ex03/index.html), enter the ID and new message, then click **수정 요청** (Send update).

---

# Day 2 · 20–30 min: Fill the edit form

In the complete guestbook, click **Edit (수정)** beside entry 41. Its ID and current message appear in the form.

```js
editId.value = item.id;
editMessage.value = item.message;
editMessage.focus();
```

The ID is read-only. Change the text to “Rehearsal at 4.” Clicking **Save changes (수정 저장)** sends PATCH.
[Complete guestbook](examples/day2/web-week14/guestbook.html) · [Form code](examples/day2/web-week14/guestbook.js)

---

# Day 2 · 30–40 min: Inspect the response array

With `Prefer: return=representation`, PATCH returns the changed rows in an array.

| PATCH target under your tag | HTTP status | What to find in the array |
|---|---|---|
| Entry 41, still present | 200 | One row · `id: 41` · new message |
| Entry 73, already deleted | 200 | `[]` · zero rows changed |

Use your IDs in the [PATCH requests](examples/day2/ex03/requests.http) to compare the responses.
Both return 200. Open each array and check its length and entry ID.

---

# Day 2 · 40–45 min: Verify the saved message

In [Read an entry again](examples/day2/ex04/index.html), look up each entry under your tag.

| Example ID | GET with the same tag and ID |
|---|---|
| 41 | One row · **Rehearsal at 4** |
| 73 | Empty array |
| 81 | One row · **Bring the sheet music** |

If the connection drops after sending PATCH, use the same GET to check the current message first.
[GET-only request file](examples/day2/ex04/requests.http)

---

# Day 2 · 45–55 min: CRUD in one file

| Button in the complete guestbook | Requests it sends |
|---|---|
| **남기기** (Post) | POST a new entry, then read the list. |
| **새로 불러오기** (Reload) | GET the latest entries under your tag. |
| Row's **수정** (Edit) → **수정 저장** (Save) | PATCH that ID, then read it again. |
| Row's **삭제** (Delete) → confirm | DELETE that ID, then read it and the list again. |

[Open the complete guestbook](examples/day2/web-week14/guestbook.html) · [guestbook.js](examples/day2/web-week14/guestbook.js)

---

# Day 2 · 55–60 min: Lab guidance

| Lab time | What to verify with your own entries |
|---|---|
| 0–12 min | Fill in the PATCH URL, JSON body, and GET for the same ID in `guestbook.js`. |
| 12–25 min | Use three fresh entries. Edit the middle one and read it back. Delete it, then PATCH its old ID and check the empty array. |
| 25–30 min | Capture the remaining list and the GET response that showed the edited text in one screenshot. |

Open **Response** in the Network panel to keep the key out of the screenshot.
[Day 2 lab](lab.md#2일차-실습) · [Walkthrough](walkthrough.md)
