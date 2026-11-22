---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 15"
footer: "Final practical exam · REST"
---

# Final practical exam

Practice with the Weeks 1–14 bank, then solve the same tasks with new values.
Weeks 12–14: REST GET, POST, PATCH and DELETE.
Reports are separate assignments.

---

# Day 1 · 0–5 min — Setup and problem bank

Check supplied folders, server and editor.
A page · B DOM · C forms/lists · D browser storage · E REST

[Bank](examples/README.md): 13 problems.
The exam selects one problem per section.
A POST task appears in C or E, never both.

---

# Day 1 · 5–15 min — Exam environment

Starter files → tasks → checks → values
The page and support code are supplied. Complete the request TODO.

[GET](examples/w12_rest_get/README.md) · [POST](examples/w13_rest_post/README.md)
[PATCH/DELETE](examples/w14_rest_edit/README.md)

---

# Day 1 · 15–25 min — Sections and supplied code

w11 saves one form object; w14 implements PATCH or DELETE, not both.
The instructor prepares the API and individual test guestbooks.
Enter values in the supplied API settings panel. Refresh resets the panel.
Enter an edit key at runtime. Never commit it.

localhost means this PC. Pages needs the shared HTTPS API.

---

# Day 1 · 25–40 min — Storage and REST errors

Form: save JSON, reload, restore, remove only its key.
GET: display the array.
POST: check stored data with GET.
PATCH: check changed rows and read the saved message.
DELETE: read the same ID and confirm absence.

Do not parse a 204 response as JSON.

---

# Day 1 · 40–55 min — Reproduce the result

app.js: one request TODO, with supplied rendering and read-back code.
api-settings.js: supplied runtime settings.
The storage task saves one form object. PATCH or DELETE is one request task.

[GET page](examples/w12_rest_get/index.html)
[Code](examples/w12_rest_get/app.js) · [Settings](examples/w12_rest_get/api-settings.js)
[.http](examples/w12_rest_get/requests.http)

---

# Day 1 · 55–60 min — Practice instructions

Required practice: form storage 10 min, one REST task 12, checks 8.
Prepare files before class; upload after Day 1.

**Day 1: 60 min lecture + 30 min practice**
[Lab](lab.md#1일차-실습) · [Walkthrough](walkthrough.md)

---

# Day 2 · 0–5 min — Check the packet

web-week15/exam/ contains an index and A–E folders.
Check your assigned test guestbook and initial records.

Do not use practice data or another student’s test data.
Keep the edit key out of source code.

---

# Day 2 · 5–10 min — Proposed points

A 3 + B 3 + C 4 + D 2 + E 3 = implementation 15.
URL reproduction 3 + oral explanation 2 = 5.

Total 20 is a proposal. The class announcement is authoritative.
[Rubric](rubric.md)

---

# Day 2 · 10–15 min — Verify changes

HTTP success does not prove a row changed.
A rejected key may give PATCH 200 [] or DELETE 204.

GET the same ID. Check the saved value or absence.

---

# Day 2 · 15–20 min — Server outages

Tell the supervisor when the API is unavailable.
Use an equivalent local API with the same initial data.
Compensate for outage time.

If no equivalent environment exists, defer REST assessment.

---

# Day 2 · 20–25 min — Submission

Submit public URL, repository URL and a Commits screenshot.
Explain one line of your own code.

Do not submit edit keys. The instructor keeps their own copy.
Reproduction uses a copy of the submitted server data.

---

# Day 2 · 25–30 min — Start the exam

Read 3 min → implement 40 → verify/push 12 → submit 5.
Compensate each student for the one-minute oral check.
Plan supervisors from class size and transition time.

**Explanation total: 5 + 5 + 5 + 5 + 5 + 5 = 30 min**
[Exam](lab.md#2일차-시험) · [Walkthrough](walkthrough.md)
