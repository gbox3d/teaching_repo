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

# Day 1 · 0–5 min — Problem bank

A page · B DOM · C forms/lists · D browser storage · E REST

[Bank](examples/README.md): 13 problems.
The exam selects one problem per section.
A POST task appears in C or E, never both.

---

# Day 1 · 5–10 min — Read the task

Starter files → tasks → checks → values
The page and support code are supplied. Complete the request TODO.

[GET](examples/w12_rest_get/README.md) · [POST](examples/w13_rest_post/README.md)
[PATCH/DELETE](examples/w14_rest_edit/README.md)

---

# Day 1 · 10–15 min — API setup

The instructor prepares the API and individual test guestbooks.
Copy public configuration values only.
Enter an edit key at runtime. Never commit it.

localhost means this PC. Pages needs the shared HTTPS API.

---

# Day 1 · 15–20 min — Read after writing

GET: display the array.
POST: check stored data with GET.
PATCH: check changed rows and read the saved message.
DELETE: read the same ID and confirm absence.

Do not parse a 204 response as JSON.

---

# Day 1 · 20–25 min — Supplied code

view.js: rendering and supporting read requests.
app.js: request TODO.
config.example.js: public settings.

[GET page](examples/w12_rest_get/index.html)
[Code](examples/w12_rest_get/app.js) · [View](examples/w12_rest_get/view.js)
[Configuration](examples/w12_rest_get/config.example.js) · [CSS](examples/w12_rest_get/styles.css)

---

# Day 1 · 25–30 min — Practice

Choose three sections, including at least one REST task.

**Explanation total: 5 + 5 + 5 + 5 + 5 + 5 = 30 min**
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

Read 3 min → implement 48 → push 5 → reserve 4.
Add the one-minute oral check to the student’s deadline.

**Explanation total: 5 + 5 + 5 + 5 + 5 + 5 = 30 min**
[Exam](lab.md#2일차-시험) · [Walkthrough](walkthrough.md)
