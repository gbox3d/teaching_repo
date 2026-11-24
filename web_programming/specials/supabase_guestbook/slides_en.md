---
marp: true
theme: default
paginate: true
header: "Web Programming Research Workshop"
footer: "Build a shared guestbook API with Supabase"
---

# Build a shared guestbook API with Supabase

Post an entry in one browser. Find it in another, then track the same entry through an edit and a deletion.

| Instructor | Students |
|---|---|
| Set up the guestbook and distribute its URL, publishable key and assigned tags. | Write under your tag and record the entry ID returned by the server. |

01 Connect → 02 Help → 03 Read → 04 Post → 05 Edit/delete → 06 HTTP console → 07 Guestbook

---

# The page address and the data address

| Location | Purpose |
|---|---|
| `http://localhost:8000/` | Open the example HTML and JavaScript on your computer. |
| Your GitHub Pages HTTPS URL | Open the published interface on another device. |
| `https://esoqbcwgzjtwcqszwvin.supabase.co` | The course API base URL. Both pages send their requests here. |

The guestbook path is `/rest/v1/guestbook`. A local HTTP page can call the shared HTTPS API.

The instructor's optional rehearsal API runs at `http://127.0.0.1:8787`.

---

# Instructor setup for a new or existing project

| Project | Files to run in the Supabase SQL Editor |
|---|---|
| New project | Run [schema.sql](../../tools/guestbook-api/schema.sql), then [about-help.sql](../../tools/guestbook-api/about-help.sql). The schema registers tags `student01` through `student30`. |
| Earlier course guestbook | Run [enable-public-crud.sql](../../tools/guestbook-api/enable-public-crud.sql) once. It preserves entries and tags and updates the edit/delete policies and the help view. |

Students share one **publishable key** and can use it to edit or delete entries under any tag. Each student uses an alias and practice text under their assigned tag. No student account is required.

---

# Set up REST Client and the browser

| Tool | What to configure in the example folder |
|---|---|
| VS Code REST Client (`humao.rest-client`) | Copy `.env.example` to `.env`. Set `API_BASE_URL` and `API_PUBLIC_KEY`. For guestbook requests, set `BOOK_ID` too. |
| Browser | Check the URL and tag in `config.example.js`. Enter the public key at the first prompt. It is saved in localStorage for that origin. |

In `requests.http`, click **Send Request** above a request. Compare its status and body with the results from the corresponding page.

[REST Client setup](examples/README.md#rest-client로-요청부터-확인하기)

---

# 01 · Connect to the API

```http
GET {{baseUrl}}/rest/v1/about
apikey: {{apiKey}}
```

Click **접속 확인** (Check connection). Expect `200` and an array with one object. Find `v1` in `version` and `/rest/v1/help` in `help_path`.

| Response | Where to look |
|---|---|
| 401 | In the browser, click **공개 키 지우기** and re-enter the key. In REST Client, check `.env`. |
| 404 | Check the project URL and the instructor's installation of the `about` view. |

[01 Connection page](examples/01_about/index.html) · [requests.http](examples/01_about/requests.http)

---

# 01 · Send the same GET in JavaScript

```js
const url = `${API_BASE_URL}/rest/v1/about`;
const response = await fetch(url, {
  headers: { apikey: API_PUBLIC_KEY }
});
```

1. Read `response.status` and compare it with the status in REST Client.
2. If `response.ok` is true, read the array with `await response.json()`.
3. Expand the array and read the name and version in its first object.

[01 Connection code](examples/01_about/app.js)

---

# 02 · Find a request in the help response

```http
GET {{baseUrl}}/rest/v1/help?order=step.asc
apikey: {{apiKey}}
```

Click **사용법 조회** (Load help). Read the `method`, `path` and `description` for each of the six rows, ordered by step.

- Rows 1 and 2 read the instructor's `about` and `help` views.
- Rows 3–6 cover POST, GET, PATCH and DELETE for entries. Locate both `book_id` and `id` in the edit and delete paths.

[02 Help page](examples/02_help/index.html) · [requests.http](examples/02_help/requests.http)

---

# Files in an example folder

| File | What you use it for |
|---|---|
| `requests.http`, `.env.example` | Send requests from VS Code and read the status and body. |
| `index.html` | Display fields and buttons, and load W3.CSS from the CDN. |
| `config.example.js` | Set the browser's URL, tag and public key. |
| `app.js` | Send requests on button clicks and display the responses. |

Each of the seven folders runs independently. Open a page on a local static server or publish it to Pages. Exclude the local `.env` file from deployment.

[Running the examples](examples/README.md)

---

# 03 · Read the entries under your tag

```http
GET {{baseUrl}}/rest/v1/guestbook?book_id=eq.{{bookId}}&order=id.desc&limit=50
apikey: {{apiKey}}
```

`book_id=eq.student01` selects entries tagged `student01`. `order=id.desc` puts the highest ID first. `limit=50` returns up to 50 entries.

Click **목록 조회** (Load list). Match each row's ID, alias and message to the JSON. A successful read with no matching entries returns `200 []`.

[03 Read page](examples/03_guestbook_get/index.html) · [requests.http](examples/03_guestbook_get/requests.http)

---

# Find the same entry in two browsers

1. In browser A, set your tag in example 03 and click **목록 조회**.
2. In browser B, open 03 with the same API URL, key and tag. For a phone, use a reachable Pages address.
3. Record the visible IDs, or `[]` if the list is empty. In the next step, browser A will post an entry and browser B will read the list again.

Enter the public key separately in each browser. The server-assigned `id` identifies the same entry in both lists.

[03 Read code](examples/03_guestbook_get/app.js) · [Research lab](lab.md)

---

# 04 · Save an entry and find its new ID

Click **새 글 저장** (Save new entry) in browser A. The page sends a JSON body like this to `POST /rest/v1/guestbook`.

```json
{"book_id":"student01","name":"연습생","message":"첫 관찰"}
```

Include `apikey` and `Content-Type: application/json`. The header `Prefer: return=representation` asks the server to return the inserted row.

Record `id` from the first object in the `201` array. In browser B, click **목록 조회** and find that ID and message.

[04 Post page](examples/04_guestbook_post/index.html) · [requests.http](examples/04_guestbook_post/requests.http)

---

# 05 · Edit an entry from the list

Click **목록 조회** in A. Click the button showing the ID of the entry you just posted (for example, **글 42 선택**). The alias and message fill the form.

Set the message to `두 번째 관찰` and click **선택한 글 수정** (Update selected entry). The page sends both fields as JSON and reads the entry again.

| What to check | Expected result |
|---|---|
| PATCH URL | The current `book_id` and the selected `id` |
| PATCH response | `200` and one updated row. An empty array means no rows changed. |
| GET with both filters | The original ID and your new message, `두 번째 관찰` |

[05 Edit page](examples/05_guestbook_edit/index.html) · [requests.http](examples/05_guestbook_edit/requests.http)

---

# 05 · Delete one entry from the list

Use example 04 to prepare three practice entries under your tag. In 05, click **목록 조회** and record their IDs. Here they are **43, 42 and 41**.

| After clicking **삭제** (Delete) beside 42 | Request and result |
|---|---|
| Cancel the dialog | No DELETE is sent. All three entries remain. |
| Click again, check the tag and ID 42, then confirm | DELETE returns `204` with an empty body. |
| GET with the same tag and ID | Expect `200 []`. IDs 43 and 41 still appear in the refreshed list. |

In `requests.http`, enter the same ID at the `entryId` prompts. Skip JSON parsing for the empty DELETE body.

---

# 06 · Change one condition in the HTTP console

Use the entry deleted in 05. Set the method, tag and ID yourself and click **요청 보내기** (Send request).

| Experiment | Predict, then check |
|---|---|
| GET the deleted ID | `200 []` |
| PATCH the same ID using **본문 예시 넣기** (Insert sample body) | `200 []`. No rows change. |
| GET an ID that still exists under your tag | `200` and one matching entry |

`buildRequest(method, book, id, bodyText)` assembles the URL and options. Explain what the empty array means in the [response exercise](examples/06_http_lab/exercise.js).

[06 HTTP console](examples/06_http_lab/index.html) · [requests.http](examples/06_http_lab/requests.http) · [Request tests](examples/06_http_lab/request.test.mjs)

---

# Check cross-device storage on GitHub Pages

1. Publish an example folder to Pages. Open its **HTTPS page URL** on two devices and enter the course public key on each one.
2. Use the same tag on both. Post an entry on device A, refresh the list on B and compare the ID.
3. Edit it on B and read it again on A. Record which device sent each request, which device checked the result, the tag, the ID and the HTTP status.

Record the local rehearsal separately from observations on the shared Supabase project. Run a request in REST Client and repeat it in the published browser interface.

[Pages guide](examples/README.md#github-pages에서-사용하기)

---

# 07 · Repeat the experiment in the complete guestbook

1. Use **글 등록** (Post) to create three practice entries. Click **목록 새로고침** (Refresh list) and record their IDs.
2. Click **수정** (Edit) in the middle row. Change the message, click **수정 저장** (Save changes) and check the new message under the same ID.
3. Click **삭제** in the middle row and cancel once. Click again and confirm. Refresh the other device's list and check that the two neighboring IDs remain.

[07 Complete guestbook](examples/07_guestbook_complete/index.html) · [requests.http](examples/07_guestbook_complete/requests.http) · [Walkthrough](walkthrough.md) · [Research lab](lab.md)

[Week 12 GET](../../weeks/week12_fetch_json/README.md) · [Week 13 CRUD](../../weeks/week13_guestbook_crud/README.md) · [Week 14 edit/delete](../../weeks/week14_project_presentation/README.md)
