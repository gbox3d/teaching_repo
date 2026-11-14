---
marp: true
theme: default
paginate: true
header: "Web programming · Week 12"
footer: "REST API"
---

# Read a guestbook through a REST API

Week 11: browser storage → Week 12: GET from a server

- The instructor prepares the shared API.
- Students send requests and display responses.
- Result: the server list and GET 200 in Network.
- Each day: 30 minutes of explanation + 60 minutes of practice.

---

## Day 1 · 0–4 min — Page server and API server

- A static server sends HTML, CSS and JavaScript.
- An API server sends guestbook data as JSON.
- 127.0.0.1:8787 is the local practice address.
- GitHub Pages uses the instructor-provided HTTPS API.

[Static server](../../tools/static-server/server.mjs) · [API setup](../../tools/guestbook-api/README.md)

---

## Day 1 · 4–9 min — JSON text and an array

[Example 01](examples/day1/ex01/index.html) · [Code](examples/day1/ex01/app.js)

```js
const text = '[{"name":"student01","message":"Hello"}]';
const items = JSON.parse(text);
console.log(items[0].message);
```

JSON is text for transport. Parse it before reading array items.

---

## Day 1 · 9–16 min — GET and two awaits

[Example 02](examples/day1/ex02/index.html) · [Code](examples/day1/ex02/app.js) · [Config](examples/day1/ex02/config.example.js)

```js
const response = await fetch(url, {
  headers: { apikey: API_PUBLIC_KEY }
});
const items = await response.json();
```

fetch waits for a response. Its default method is GET.
json reads and parses the response body.
Use await inside an async function.

---

## Day 1 · 16–22 min — Read the Network panel

1. Open Network and reload.
2. Select the guestbook request under Fetch/XHR.
3. Find the URL, GET and status 200 under Headers.
4. Read the array under Response.

The apikey header contains a publishable key, not a server secret.
This GET request sends no JSON body.

---

## Day 1 · 22–27 min — Query parameters

[Example 03](examples/day1/ex03/index.html) · [Code](examples/day1/ex03/app.js) · [Config](examples/day1/ex03/config.example.js)

```text
/rest/v1/guestbook?book_id=eq.student01
&select=id,name,message,created_at&order=id.desc&limit=2
```

The real URL is one line.
- book_id selects a guestbook; select chooses response fields.
- order sorts by newest id; limit caps the row count.
- Change only limit and compare responses.

---

## Day 1 · 27–30 min — Practice handoff

- Create web-week12 from last week’s files.
- Change one value at a time in examples 01–03.
- Compare the request, response and visible result.

Explanation: 4 + 5 + 7 + 6 + 5 + 3 = 30 minutes.

[Day 1 practice](lab.md#1일차-실습) · [Walkthrough](walkthrough.md)

---

## Day 2 · 0–5 min — Reuse the list code

- Week 10: loop over an array to create list items.
- Week 11: read the array from localStorage.
- Week 12: read an array from the server response.

Reuse the DOM code.
Server data does not automatically import localStorage data.

---

## Day 2 · 5–12 min — Display the response array

[Example 04](examples/day2/ex04/index.html) · [Code](examples/day2/ex04/app.js) · [Config](examples/day2/ex04/config.example.js)

```js
for (let i = 0; i < items.length; i++) {
  const li = document.createElement('li');
  li.textContent = `${items[i].name}: ${items[i].message}`;
  list.append(li);
}
```

Use textContent for server messages too.
An empty array produces an empty list.

---

## Day 2 · 12–18 min — HTTP failures are responses

[Example 05](examples/day2/ex05/index.html) · [Code](examples/day2/ex05/app.js) · [Config](examples/day2/ex05/config.example.js)

```js
if (!response.ok) {
  throw new Error(`HTTP ${response.status}`);
}
```

A missing endpoint may still return a response.
Check ok before displaying the JSON list.
Error codes and bodies may differ between APIs.

---

## Day 2 · 18–23 min — Display connection failures

[Example 06](examples/day2/ex06/index.html) · [Code](examples/day2/ex06/app.js) · [Config](examples/day2/ex06/config.example.js)

```js
try {
  // Request, validate and read JSON.
} catch (error) {
  loadNotice.textContent = 'Could not load the list.';
}
```

Try Offline in Network, then restore the connection.
Distinguish the old list from the failure message.

---

## Day 2 · 23–27 min — A button while waiting

```js
reloadButton.disabled = true;
try {
  // Request the list.
} catch (error) {
  // Display a failure message.
} finally {
  reloadButton.disabled = false;
}
```

finally runs after either success or failure.

---

## Day 2 · 27–30 min — Assemble the reading page

- Configuration → GET → JSON array → showList.
- Reload sends the same request again.
- Capture the list and GET 200 together.

Explanation: 5 + 7 + 6 + 5 + 4 + 3 = 30 minutes.

[Day 2 practice](lab.md#2일차-실습) · [Walkthrough](walkthrough.md)

---

# Assembly files

[Guestbook](examples/day2/web-week12/guestbook.html) · [GET](examples/day2/web-week12/guestbook.js) · [Config](examples/day2/web-week12/config.example.js)
[Home](examples/day2/web-week12/index.html) · [About](examples/day2/web-week12/about.html) · [Home JS](examples/day2/web-week12/app.js)
[CSS](examples/day2/web-week12/styles.css) · [Profile](examples/day2/web-week12/images/profile.png)

[Examples](examples/README.md) · [Practice](lab.md) · [Walkthrough](walkthrough.md)

Keep filenames and script order. Use instructor-provided settings.
