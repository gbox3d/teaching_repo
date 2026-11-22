---
marp: true
theme: default
paginate: true
header: "Web programming · Week 13"
footer: "REST API · POST"
---

# Save guestbook messages with POST

From public API reads to writing a guestbook entry and checking the result

- Connect the week 7 form to a POST request. The list function is supplied.
- Read status 201 and the server-generated id.
- Each session: 60 minutes of lecture/demo + 30 minutes of practice.
- Prepare the files and repository before class. Upload after class.

---

## Day 1 · 0–5 min · Check the starting point

- In example 02, copy `.env.example` to `.env`. Fill in `API_PUBLIC_KEY` and `BOOK_ID`.
- Find your book id and message in the body of `POST /rest/v1/guestbook`.
- Click **Send Request** once to add a message to the class guestbook.

---

## Day 1 · 5–20 min · POST and JSON

[First POST in example 02](examples/day1/ex02/README.md) · [Optional JSON review](examples/day1/ex01/README.md)

```js
const item = {
  book_id: BOOK_ID, name: 'student01', message: 'Hello'
};
const body = JSON.stringify(item);
```

The request body contains the book id, alias and message.
The server assigns the message number (`id`) and creation time (`created_at`).

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

- The request body contains `book_id`, `name` and `message`.
- Find the server-assigned `id` in the `201 Created` response array.
- Click **Send Request** above the GET in the same file. Find that `id` and your message in the `200 OK` list.

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

## Day 2 · 0–5 min · Prepare the message form

- In the completed guestbook's `config.example.js`, change `BOOK_ID` to your book id.
- When the page first opens, enter the publishable key from the instructor in the prompt (stored in week 11 localStorage). If the key is wrong, click **공개 키 지우기** and enter it again.
- Use an alias and a message of at most 500 characters.
- Do not include email in the POST body.

The config file, request guards, button state and failure handling are supplied.
Students edit only form values, the JSON body and the reload call.

---

## Day 2 · 5–15 min · Build the request body from the form

[Example 04 demo](examples/day2/ex04/README.md)

```js
form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const message = messageInput.value.trim();
  // Validate, then POST.
});
```

Example 02 sent a fixed message. Example 04 sends the message entered in the form.
Stop submission if either field contains only whitespace.

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

- On a slow connection, click Save twice. Look for a single POST in Network.
- Submit while Offline. The input stays in the form and `finally` re-enables the button.
- Restore the connection. If the save response did not arrive, check the list with GET first.

---

## Day 2 · 45–55 min · GET after saving

[Example 06 demo](examples/day2/ex06/README.md)

```js
notice.textContent = `Saved · id ${saved[0].id}`;
await loadMessages(); // Student edit 3
```

The supplied `loadMessages()` function shows the new message.
If GET fails after POST returns 201, click **새로 불러오기** to retry the GET.
In a second browser, enter the publishable key in the prompt, then find the saved message.

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
[Config file](examples/day2/web-week13/config.example.js) · [REST Client](examples/day2/web-week13/requests.http)
[Home](examples/day2/web-week13/index.html) · [About](examples/day2/web-week13/about.html)

The page loads `config.example.js` and `guestbook.js` in that order with `defer`.
The completed guestbook sends the first GET when the page opens. **남기기** sends a POST followed by GET.
In week 14, use the saved `id` to update and delete that message.

[Examples](examples/README.md) · [Practice](lab.md) · [Walkthrough](walkthrough.md)
