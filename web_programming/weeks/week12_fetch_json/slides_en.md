---
marp: true
theme: default
paginate: true
header: "Web programming · Week 12"
footer: "REST API · GET"
---

# Read a guestbook through a REST API

Week 11 required work: save and restore one form object.
The object-array guestbook is an instructor-provided demonstration.
Week 12: about → help → GET your list.

- Each day: 60-minute lecture/demo + 30-minute practice.
- Prepare files before class; upload after class.
- Evidence: server list and GET 200 in Network.

---

## Day 1 · 0–5 min · Check the setup

- The static server sends files; the API server sends JSON.
- Local defaults: 127.0.0.1:8787 / classroom-local / student01.
- On Pages, enter the supplied public HTTPS API in the panel.
- Settings stay in memory. Re-enter them after a page reload.

[Walkthrough](walkthrough.md) · [API preparation](../../tools/guestbook-api/README.md)

---

## Day 1 · 5–15 min · URL and headers

- The URL identifies the server and request path.
- GET sends no JSON request body here.
- apikey is a public calling key, not a server secret.
- BOOK_ID is a data tag, not user authentication.
- The settings panel is provided; do not reimplement it.

---

## Day 1 · 15–30 min · about and help

[Example 01](examples/day1/ex01/README.md) → [Example 02](examples/day1/ex02/README.md)

1. Install REST Client and copy .env.example to .env.
2. about **Send Request**: 200 and an API information array.
3. help **Send Request**: 200 and a usage-step array.
4. Click the browser request button and compare results.

The browser panel and .env are separate. Exclude real values from Git/ZIP.

---

## Day 1 · 30–40 min · Review JSON

[Week 11 example 05](../week11_object_localstorage/examples/day2/ex05/README.md)

- JSON is a text format for transport and storage.
- Read fields and length after parsing it into objects/arrays.
- Distinguish response.status from name/message in the body.
- Find the array brackets and object fields in Network Response.

---

## Day 1 · 40–55 min · GET and await

[Example 03](examples/day1/ex03/README.md) · [Code](examples/day1/ex03/app.js)

```js
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
```

An async function waits first for the response, then the JSON body.
book_id filters the guestbook; limit caps rows. Compare 1, 2 and 5.

---

## Day 1 · 55–60 min · 30-minute practice

| Practice time | Activity |
|---|---|
| 0–5 min | Configure the browser and .env separately |
| 5–13 min | about/help Send Request |
| 13–23 min | Change BOOK_ID and limit |
| 23–30 min | Check URL, 200 and response array |

Lecture: 5+10+15+10+15+5=60 minutes. [Practice](lab.md)

---

## Day 2 · 0–5 min · Local copy and server data

- Compare Week 10 strings with the provided Week 11 object-array demo.
- Distinguish the required form task from that provided demonstration.
- guestbook.local.html/js retain the original storage key.
- guestbook.html reads the server list.
- Do not migrate or erase local entries.

---

## Day 2 · 5–20 min · Response to showList

[Example 04](examples/day2/ex04/README.md) · [Completed code](examples/day2/web-week12/guestbook.js)

```js
  list.replaceChildren();
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message}`;
    list.append(li);
  }
```

Clear before redrawing. Use textContent. [] is a valid empty list.

---

## Day 2 · 20–35 min · response.ok

[Example 05](examples/day2/ex05/README.md)

- Valid local fields: Status 200 · ok true.
- Missing local field: Status 400 · ok false.
- HTTP errors are responses. Read the status and error JSON.
- Restore the valid fields. Error codes/bodies may differ across APIs.

```js
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
```

---

## Day 2 · 35–45 min · try/catch and connection failure

[Example 06](examples/day2/ex06/README.md)

1. Open the page first.
2. Network Offline → request again → failure notice.
3. No throttling → request again → GET 200.

A connection failure differs from an HTTP error. catch displays a notice;
finally enables the button after success or failure so a retry is possible.

---

## Day 2 · 45–55 min · Retry and assembly

- Keep GET, showList and failure notices in guestbook.js.
- Load the provided api-settings.js first.
- Prepare DOM variables and events before the initial GET.

```js
reloadButton.addEventListener('click', loadMessages);
setupApiSettings(loadMessages);
loadMessages();
```

Repeated reload requests must not accumulate duplicate rows.

---

## Day 2 · 55–60 min · 30-minute practice

| Practice time | Activity |
|---|---|
| 0–12 min | Connect URL, JSON and showList in the supplied code |
| 12–22 min | HTTP error, Offline and recovery |
| 22–30 min | Check 375px; capture list and GET 200 |

Lecture: 5+15+15+10+10+5=60 minutes. [Practice](lab.md)
Local rehearsal and two-browser public API sharing are separate checks.

---

# Files for next week

[Guestbook](examples/day2/web-week12/guestbook.html) · [GET code](examples/day2/web-week12/guestbook.js) · [Provided settings](examples/day2/web-week12/api-settings.js)
[Folder guide](examples/day2/web-week12/README.md) · [Requests](examples/day2/web-week12/requests.http)
[Walkthrough](walkthrough.md) · [Practice](lab.md)

Week 13 restores name/message/guestbook-form/notice in this same folder
and adds POST to guestbook.js. Preserve the local copy.
Enter public API settings at runtime; keep them out of source files.
