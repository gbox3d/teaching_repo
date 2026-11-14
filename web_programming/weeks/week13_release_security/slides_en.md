---
marp: true
theme: default
paginate: true
header: "Web programming · Week 13"
footer: "REST API"
---

# Save guestbook messages through a REST API

Week 12: GET → Week 13: POST, then GET again

- Send form values as a JSON request body.
- The server creates an id and timestamp.
- Read the same message on another device.
- Each day: 30 minutes of explanation + 60 minutes of practice.

---

## Day 1 · 0–4 min — GET and POST

- GET reads messages.
- POST creates a new message.
- The same endpoint can accept different methods.

Keep the list function from week 12.
Add request code without changing server settings.

---

## Day 1 · 4–9 min — A JSON request body

[Example 01](examples/day1/ex01/index.html) · [Code](examples/day1/ex01/app.js)

```js
const item = {
  book_id: BOOK_ID, name: 'student01', message: 'Hello'
};
const body = JSON.stringify(item);
```

Serialize the object before sending it as the body.
The server supplies id and created_at.

---

## Day 1 · 9–16 min — Three parts of a POST request

[Example 02](examples/day1/ex02/index.html) · [Code](examples/day1/ex02/app.js) · [Config](examples/day1/ex02/config.example.js)

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

---

## Day 1 · 16–22 min — Payload and Response

- method is the action; headers describe the request.
- body contains the data to send.
- Payload contains book_id, name and message.
- Response adds id and created_at. Status 201 means created.

Prefer asks this API to return the inserted row.
The publishable key is not a personal editing credential.

---

## Day 1 · 22–27 min — Server input validation

[Example 03](examples/day1/ex03/index.html) · [Code](examples/day1/ex03/app.js) · [Config](examples/day1/ex03/config.example.js)

- An empty message is rejected by the server.
- Replace it with text and compare the response.
- Read status, ok and the error body together.
- The server checks inputs independently of the page.

POST examples create real rows. Click once per experiment.

---

## Day 1 · 27–30 min — Practice handoff

- Start web-week13 from week 12.
- Compare body, status and generated ids in examples 01–03.
- Check empty text and whitespace.

Explanation: 4 + 5 + 7 + 6 + 5 + 3 = 30 minutes.

[Day 1 practice](lab.md#1일차-실습) · [Walkthrough](walkthrough.md)

---

## Day 2 · 0–5 min — From form input to a request

- Keep submit → preventDefault → value.trim from week 7.
- Put validated values into the POST body.
- Use an alias; messages have a 500-character limit.
- Do not request email addresses or passwords.

Keep input values until the server confirms success.

---

## Day 2 · 5–12 min — Connect the form to POST

[Example 04](examples/day2/ex04/index.html) · [Code](examples/day2/ex04/app.js) · [Config](examples/day2/ex04/config.example.js)

```js
form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const message = messageInput.value.trim();
  // Validate, then await fetch(...).
});
```

An async event handler can use await.
Compare the input text with Network’s Payload.

---

## Day 2 · 12–18 min — Pending, success and failure

[Example 05](examples/day2/ex05/index.html) · [Code](examples/day2/ex05/app.js) · [Config](examples/day2/ex05/config.example.js)

- Before the request: disable the button and show pending.
- After success: show confirmation and clear inputs.
- After failure: preserve inputs and check the saved list.
- In finally: enable the button again.

Use Network throttling to observe the pending state.
This reduces duplicate clicks; it is not a server guarantee.

---

## Day 2 · 18–23 min — Read after saving

[Example 06](examples/day2/ex06/index.html) · [Code](examples/day2/ex06/app.js) · [Config](examples/day2/ex06/config.example.js)

```js
const saved = await response.json();
notice.textContent = `Saved · id ${saved[0].id}`;
await loadMessages();
```

GET the server list after POST succeeds.
A failed reload does not mean saving failed.

---

## Day 2 · 23–27 min — Check two browsers

1. Save a message in browser A.
2. Read the same API and BOOK_ID in browser B.
3. Reload A and find the same message.

Other devices need the shared HTTPS API.
127.0.0.1 refers to each device itself.
If the save response was lost, GET the list before retrying.

---

## Day 2 · 27–30 min — Assemble the writing page

- guestbook.js: GET and list display.
- submit.js: POST and save feedback.
- Verify POST 201, GET 200 and the new message.

Explanation: 5 + 7 + 6 + 5 + 4 + 3 = 30 minutes.

[Day 2 practice](lab.md#2일차-실습) · [Walkthrough](walkthrough.md)

---

# Assembly files

[Guestbook](examples/day2/web-week13/guestbook.html) · [GET](examples/day2/web-week13/guestbook.js) · [Config](examples/day2/web-week13/config.example.js)
[POST](examples/day2/web-week13/submit.js)
[Home](examples/day2/web-week13/index.html) · [About](examples/day2/web-week13/about.html) · [Home JS](examples/day2/web-week13/app.js)
[CSS](examples/day2/web-week13/styles.css) · [Profile](examples/day2/web-week13/images/profile.png)

[Examples](examples/README.md) · [Practice](lab.md) · [Walkthrough](walkthrough.md)

Keep filenames and script order. Use instructor-provided settings.
