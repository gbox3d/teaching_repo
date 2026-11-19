---
marp: true
theme: default
paginate: true
header: "Web programming · Week 13"
footer: "REST API · POST"
---

# Save guestbook messages with POST

Week 12 GET → Week 13 POST → GET again

- Reuse the week 7 form and week 12 list function.
- Read status 201 and the server-generated id.
- Each session: 60 minutes of lecture/demo + 30 minutes of practice.
- Prepare files and the repository before class; upload after class.

---

## Day 1 · 0–5 min · Check the starting point

- Check the static server, API and supplied folder.
- GET reads a list; POST creates a message.
- An endpoint can accept different methods.

The API settings panel is supplied code. Reloading restores local defaults.
Re-enter shared API settings at runtime.

---

## Day 1 · 5–20 min · POST and JSON

[Example 01 demo](examples/day1/ex01/README.md) · [Example 02](examples/day1/ex02/README.md)

```js
const item = {
  book_id: BOOK_ID, name: 'student01', message: 'Hello'
};
const body = JSON.stringify(item);
```

Serialize the object before sending it.
The server creates id and created_at. Example 01 sends no request.

---

## Day 1 · 20–35 min · Headers and body

[POST code](examples/day1/ex02/app.js) · [REST Client](examples/day1/ex02/requests.http)

```js
const response = await fetch(url, {
  method: 'POST',
  headers: {
    apikey: API_PUBLIC_KEY,
    'Content-Type': 'application/json',
    Prefer: 'return=representation'
  },
  body: JSON.stringify(item)
});
```

apikey identifies public access. Prefer asks for the inserted row.

---

## Day 1 · 35–45 min · Status 201 and id

- Payload: book_id, name and message sent by the page.
- Response: id and created_at added by the server.
- 201: created. Find the same id in the next GET 200 response.

Copy `.env.example` to `.env` for REST Client settings.
Use **Send Request** in order: about → help → POST → GET.
Browser settings and `.env` are separate. Keep actual keys out of tracked files.

---

## Day 1 · 45–55 min · Server validation

[Example 03 demo](examples/day1/ex03/README.md) · [Requests](examples/day1/ex03/requests.http)

- An empty message returns 400; valid text returns 201.
- Read response.ok, status and Response together.
- The server checks inputs independently of the page.

Example 03 intentionally skips the page's empty-input check.
POST creates real rows. Send once, then inspect the result.

---

## Day 1 · 55–60 min · Practice handoff

1. Change message in `.http` and POST: 10 minutes.
2. Read the generated id and GET the list: 10 minutes.
3. Compare empty-input rejection with success: 10 minutes.

Lecture/demo: 5 + 15 + 15 + 10 + 10 + 5 = 60 minutes.
Practice: 10 + 10 + 10 = 30 minutes.

[Practice](lab.md#1일차-실습) · [Walkthrough](walkthrough.md)

---

## Day 2 · 0–5 min · Check the form and server

- Check the week 12 GET list and API settings.
- Use an alias and a message of at most 500 characters.
- Do not include email in the POST body.

Settings, request guards, button state and failure handling are supplied.
Students edit only form values, the JSON body and the reload call.

---

## Day 2 · 5–15 min · Review submit

[Example 04 demo](examples/day2/ex04/README.md)

```js
form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  // Validate, then POST.
});
```

Reuse submit → preventDefault → value.trim from week 7.
Whitespace-only input sends no POST.

---

## Day 2 · 15–30 min · Connect POST

[Combined guestbook code](examples/day2/web-week13/guestbook.js)

```js
method: 'POST',
headers: {
  apikey: API_PUBLIC_KEY,
  'Content-Type': 'application/json',
  Prefer: 'return=representation'
},
body: JSON.stringify({ book_id: BOOK_ID, name: name, message: message })
```

Compare form values with Network's Payload.
Student edit 1 reads form values; edit 2 builds the JSON body.

---

## Day 2 · 30–45 min · Pending and failure

[Example 05 demo](examples/day2/ex05/README.md)

- Pending: guard duplicate submits and disable the button.
- Confirmed success: show saved. Failure: preserve input.
- finally: enable the button again.
- Uncertain response: GET the list before another POST.

Compare Slow 3G and Offline, then restore No throttling.
An old POST response cannot clear the form after settings change.

---

## Day 2 · 45–55 min · GET after saving

[Example 06 demo](examples/day2/ex06/README.md)

```js
notice.textContent = `Saved · id ${saved[0].id}`;
await loadMessages(); // Student edit 3
```

Saving and loading have separate status messages. Retry GET if loading fails.
Use the same API and book id in a second browser.
Distinguish same-PC local checks from shared HTTPS API/device checks.

---

## Day 2 · 55–60 min · Practice handoff

1. Edit form values, JSON and loadMessages: 15 minutes.
2. Check duplicate clicks and preserved failed input: 7 minutes.
3. Second browser and POST 201 → GET 200 capture: 8 minutes.

Lecture/demo: 5 + 10 + 15 + 15 + 10 + 5 = 60 minutes.
Practice: 15 + 7 + 8 = 30 minutes.

[Practice](lab.md#2일차-실습) · [Walkthrough](walkthrough.md)

---

# Assembly files and week 14 handoff

[Guestbook](examples/day2/web-week13/guestbook.html) · [Combined GET/POST](examples/day2/web-week13/guestbook.js)
[Supplied settings](examples/day2/web-week13/api-settings.js) · [REST Client](examples/day2/web-week13/requests.http)
[Home](examples/day2/web-week13/index.html) · [About](examples/day2/web-week13/about.html)

HTML: api-settings.js → guestbook.js, both with defer.
Initialize events and settings before the final initial GET call.
Do not load submit.js. Add week 14 PATCH/DELETE sections to the same file.

[Examples](examples/README.md) · [Practice](lab.md) · [Walkthrough](walkthrough.md)
