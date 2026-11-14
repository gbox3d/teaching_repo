---
marp: true
theme: default
paginate: true
header: "Web Programming Research Workshop"
footer: "Build a shared guestbook API with Supabase"
---

# Build a shared guestbook API with Supabase

A research workshop with one example folder per step.

01 Connect → 02 Read help → 03 Read entries → 04 Post
05 Edit → 06 Compare → 07 Complete guestbook

Send requests.http first, then study the browser implementation.
Students use the prepared shared API without a Supabase account.

---

# Page address and API address

| Target | Address and purpose |
|---|---|
| Local page | http://localhost:8000/ · preview static files |
| Shared API | Supabase HTTPS URL · metadata and guestbook data |
| Pages site | Published HTTPS URL · share the interface |
| Optional local API | http://127.0.0.1:8787 · local rehearsal |

A local HTTP page can call the shared HTTPS API.
The Node static server is for local preview only.

---

# Before class · Instructor SQL setup

Run [about-help.sql](../../tools/guestbook-api/about-help.sql) once in the existing shared project.
For a new project, run it after [schema.sql](../../tools/guestbook-api/schema.sql).

- Add read-only about and help views.
- Keep the existing guestbook table.
- Students do not need accounts or SQL access.

Shared guestbook GET and POST have been checked.
Installed and GET verified on 2026-11-14: about returns 1 row, help returns 6.

---

# Start with VS Code REST Client

1. Copy the step folder's .env.example to .env.
2. Set the public key and, for guestbook steps, BOOK_ID.
3. Click Send Request in requests.http in the same folder.
4. Inspect status and JSON, then open index.html and app.js.

Keep .env beside the .http file. No Node server is needed for these requests.
Browsers read config.example.js in the same folder instead.
[REST Client usage](https://github.com/Huachao/vscode-restclient#usage) · [Setup](examples/README.md#rest-client로-요청부터-확인하기)

---

# 01_about · Check API connectivity

[requests.http](examples/01_about/requests.http) → [Browser page source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/01_about/index.html)

```http
GET /rest/v1/about
apikey: <public key supplied by the instructor>
```

Click the connection button. Expect 200 and an array with one object.
Read name, version, description and help_path.
For a 404, ask whether the metadata SQL was applied.

---

# 01 · Map the request to code

Read [01_about/app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/01_about/app.js).

| In the request | In JavaScript |
|---|---|
| GET path | /rest/v1/about after API_BASE_URL |
| apikey header | API_PUBLIC_KEY in headers |
| HTTP status | response.status and response.ok |
| JSON response | response.json() |

This step does not create or edit entries.
Check the browser request after REST Client succeeds.

---

# 02_help · Read the API guide

[requests.http](examples/02_help/requests.http) → [Browser page source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/02_help/index.html)

```http
GET /rest/v1/help?order=step.asc
apikey: <public key supplied by the instructor>
```

Read six rows with step, method, path and description.
order=step.asc sorts the guide by step number.
The course adds these GET-only about and help APIs.

---

# Run one independent folder

```text
examples/
  README.md              example guide
  01_about/
    index.html · app.js
    config.example.js · styles.css
    requests.http · .env.example
  02_help/ ... 07_guestbook_complete/
```

Each step reads its own configuration and styles.
Run or publish one folder independently. Exclude .env from deployment.

---

# 03_guestbook_get · Read by tag

[requests.http](examples/03_guestbook_get/requests.http) → [Read page source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/03_guestbook_get/index.html)

```http
GET /rest/v1/guestbook?book_id=eq.student01
apikey: <public key supplied by the instructor>
```

book_id groups entries; eq. means equals.
Read the array. An empty guestbook correctly returns [].
A tag is a filter, not a permission boundary.

---

# 03 · Response and query options

| Option | Purpose |
|---|---|
| select=id,name,message,created_at | Choose response columns |
| order=id.desc | Sort by descending entry ID |
| limit=50 | Read at most 50 entries |

Each object in the JSON array is one entry.
Connect the response to its display in the [read code](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/03_guestbook_get/app.js).
Read the same tag in two pages and compare the server data.

---

# 04_guestbook_post · Save an entry

[requests.http](examples/04_guestbook_post/requests.http) → [Post page source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/04_guestbook_post/index.html)

```json
{"book_id":"student01","name":"alias","message":"First post"}
```

POST /rest/v1/guestbook
apikey · Content-Type: application/json · Prefer: return=representation

Record the new ID from the 201 array, then GET it again.
The server creates id and created_at. Repeating POST creates another entry.

---

# 05_guestbook_edit · Update an entry

[requests.http](examples/05_guestbook_edit/requests.http) → [Edit page source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/05_guestbook_edit/index.html)

Select an entry you created or enter its ID.
PATCH requires book_id and id filters plus X-Edit-Key.

```json
{"message":"An updated entry"}
```

Enter the edit key when sending; keep it out of public settings.
A 200 with [] changed no rows. GET the same ID to verify the update.

---

# 05 · Delete and an empty response

Send DELETE with book_id and id filters plus the edit key.

- A 204 response has no body.
- Do not call response.json() on an empty body.
- GET the same ID to verify that the entry is absent.
- Check that other entries remain unchanged.

The .http file prompts for entryId and password.
Input is masked, but request history remains. Follow the [history instructions](examples/README.md#rest-client로-요청부터-확인하기).

---

# 06_http_lab · Change one condition

[requests.http](examples/06_http_lab/requests.http) → [Combined page source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/06_http_lab/index.html)

Complete 01–05 before changing methods, IDs and JSON directly.
Insert a sample body for POST/PATCH, then change one field.

- Correct key versus another guestbook's key
- Existing ID versus absent ID
- Allowed message versus protected book_id

Extend response interpretation in [exercise.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/06_http_lab/exercise.js).
Keep [request tests](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/06_http_lab/request.test.mjs) separate from cloud verification.

---

# GitHub Pages and verification status

Publish the HTML, JavaScript, configuration and CSS from one example folder.
Pages serves files; the browser calls the Supabase HTTPS API.
No Node server or student account is required. Exclude .env and edit-key files.

Checked: shared guestbook GET/POST, metadata GET and local pages 01/02.
Pending: Pages deployment and cloud PATCH/DELETE.

REST Client success does not verify browser CORS.
[Pages guide](examples/README.md#github-pages에서-사용하기)

---

# 07_guestbook_complete · Complete guestbook

[requests.http](examples/07_guestbook_complete/requests.http) → [Guestbook page source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/07_guestbook_complete/index.html)

Use the entry list and posting form in one interface.
Select an entry, enter its edit key, then verify edits/deletion with a GET by ID.
07 is the complete guestbook; 06 is for changing raw request conditions.
There is no fixed session or content limit. Record results and pending checks.

[Week 12 GET](../../weeks/week12_fetch_json/README.md) · [Week 13 POST](../../weeks/week13_release_security/README.md) · [Week 14 edit/delete](../../weeks/week14_project_presentation/README.md)
[Walkthrough](walkthrough.md) · [Research lab](lab.md) · [Examples](examples/README.md)
[Supabase Data REST API](https://supabase.com/docs/guides/api)
