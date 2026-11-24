---
marp: true
theme: default
paginate: true
header: "Web Programming · Hash SPA"
footer: "MPA · hash · DOM · REST"
---

# Hash SPA Workshop

Combine the week 14 guestbook into three views in one document.

- Keep the regular course as an MPA.
- Optional workshop after week 14; excluded from regular exams.
- No framework, npm install, or History API.

[Lab](lab.md) · [Walkthrough](walkthrough.md)

---

## Setup and sequence

Prepare Node.js 24+, VS Code, and Chrome.

```bash
node web_programming/tools/static-server/server.mjs web_programming 8111
```

01 MPA → 02 two views → 03 three hashes → 04 REST integration

Load W3.CSS 4.1.0 from the CDN.
The workshop has no fixed total duration or session limit.

---

## Student changes and supplied code

| Role | Scope |
|---|---|
| Student changes | Visibility condition, hash, event wiring, unique IDs |
| Instructor demo | Document requests, unknown routes, focus, CRUD failures |
| Supplied | Week 14 REST, config.example.js, stale-response protection |
| Optional | Compare refresh-on-entry policies |

A first 01–03 session may use 60 minutes of lecture/demo + 30 minutes of lab.
Schedule 04 assembly and REST failure experiments as follow-up work.

---

## 01: Three HTML files are three documents

[01 MPA](examples/01_mpa/README.md)

```html
<a href="index.html">Home</a>
<a href="about.html">About</a>
<a href="guestbook.html">Guestbook</a>
```

Each URL maps to a real file. Observe Document requests on navigation.
Test direct URLs, reload, back, and forward.
Back navigation may restore a cached document.

---

## 02: Put two sections in one document

[02 two views](examples/02_two_screens/README.md)

Home and About already exist in the DOM. Buttons change visibility.

```js
for (let i = 0; i < sections.length; i++)
  sections[i].hidden = sections[i].id !== name;
```

Home count 2 → About → Home: the count remains 2.
The URL stays unchanged; Back cannot select a previous view.

---

## 03: Connect three views to hashes

[03 hash routes](examples/03_hash_routes/README.md)

```html
<a href="#home">Home</a>
<a href="#about">About</a>
<a href="#guestbook">Guestbook</a>
```

The address is index.html#guestbook.
The server receives index.html; browser code selects the view.
The fragment is not included in the server request.

---

## Empty and unknown hashes

```js
const route = location.hash.slice(1) || 'home';
const known = route === 'home' ||
  route === 'about' || route === 'guestbook';
const visibleId = known ? route : 'not-found';
```

An empty hash selects Home. Unknown hashes show a notice and Home link.
Do not insert an unknown string directly into a DOM selector.
No menu item is current on the unknown-route screen.

---

## Use the same function at startup and on change

```js
window.addEventListener('hashchange', showRoute);
window.addEventListener('load', showRoute, { once: true });
showRoute();
```

Read the initial URL and every later hash change.
Direct #guestbook entry, reload, Back, and Forward use the same function.
Do not register event handlers again when changing views.

---

## Current menu and heading focus

Set aria-current="page" on the active link; remove it from the others.
Update the document title and focus the visible section heading.

```js
const heading = document.querySelector(`#${visibleId} h2`);
document.title = `${heading.textContent} · Hash SPA`;
heading.focus();
```

The heading’s tabindex="-1" allows programmatic focus.
Tab to a menu link → Enter → verify heading focus.

---

## Keep the DOM to preserve inputs

hidden hides a view without removing its DOM.

Enter a name and message → Home → About → Guestbook

The draft remains. Do not recreate an entire section with innerHTML.
03 uses textContent for preview; it does not save data.
Reload resets the draft and Home counter.

---

## Register each event once

Register listeners outside showRoute().

- Navigate through Home, About, and Guestbook ten times.
- Click the Home count button once.
- Verify that the count increases by exactly one.
- In 04, verify one POST creates exactly one row.

Registering handlers on each transition can repeat a single action.

---

## 04: Assemble the week 14 interface

[04 REST integration](examples/04_rest_guestbook/README.md)

| Area | Names |
|---|---|
| Guestbook | guestbook-form, name, message, notice, list, count |
| Home | home-count, home-count-button, homeCount, homeCountBox |
| Behavior | One app.js file |
| Supplied settings | Separate config.example.js |

Replace the 03 preview code with week 14 CRUD.

---

## Run the first GET after initialization

Load config.example.js, then app.js, with defer.

Prepare DOM references, functions, and listeners → showRoute() → loadMessages()

Keep GET, POST, PATCH, and DELETE in named sections of app.js.
Do not fetch before edit DOM and functions are ready.
config.example.js sets the URL and BOOK_ID and asks for the public key first if none is stored.

---

## Start REST Client with about

Use VS Code extension humao.rest-client.
Copy .env.example to .env in the same folder.

Set API_BASE_URL, API_PUBLIC_KEY, and BOOK_ID.
Click Send Request above each request in requests.http.

about 200 → help 200 → GET 200 → POST 201

Copy the POST ID into MESSAGE_ID in .env.
REST Client reads .env on its own and does not use the public key stored in the browser.

---

## Verify PATCH and DELETE using the same ID

| Request | Verification |
|---|---|
| PATCH | 200 with one changed row, then same-ID GET and message |
| DELETE | 204 with no body, then same-ID GET returning [] |

PATCH 200 [] means no change. Do not call json() on a 204 response.
Use both the book tag and entry ID in PATCH and DELETE requests.
Keep real keys and server secrets out of tracked files.

---

## Fetch policy and state lifetime

| Action | Inputs and memory | GET |
|---|---|---|
| Hash navigation | Preserved | None |
| Reload list button | Preserved | Runs |
| Browser reload | Reset | Runs with config.example.js |
| Prompt canceled or left empty | Public key not saved | Runs, then HTTP 401 |
| Clear public key button | Key removed, page reloads | Runs after asking again |

The saved public key and server entries persist after a reload.
After an uncertain POST failure, fetch before retrying.

---

## Root and project subdirectory URLs

```text
/index.html#guestbook
/<repository>/index.html#guestbook
```

Reload the same real HTML path.
A new host, port, browser, or device asks for the public key once.
Do not invent a missing `/<repository>/guestbook` path.
Test empty/unknown hashes, direct entry, Back, and Forward.
Also test 375px, 1280px, and keyboard navigation.

---

## Evidence and further experiments

Record predictions, observed results, and screen/request evidence.

Compare MPA Document requests with hash transitions.
Verify ten transitions, draft retention, single events, and CRUD IDs.
Test missing IDs, network failure, and recovery by fetching.

Separate local rehearsal from public API, Pages, and cross-device tests.
Optional: change the fetch-on-entry policy and compare request counts.
