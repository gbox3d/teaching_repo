---
marp: true
theme: default
paginate: true
header: "Web Programming Special Lecture"
footer: "Building a Server-Backed Guestbook with Supabase · Optional · 110 min"
---

# Building a Server-Backed Guestbook with Supabase

The Week 11 guestbook only lived in **your own browser**.
Today you store that same guestbook on an **internet server**, so it shows up on other PCs too.

```text
My PC's browser ── insert ──▶ Supabase table guestbook
                ◀── select ──
```

---

# Part 1 — Create a Project and a Table

`25 min explanation & demo`

1. Two places where entries can be stored
2. Create a Supabase project
3. Run the provided SQL once
4. Copy only the publishable key
5. Change two lines in `config.js`

---

## Part 1 · 0–5 min — Where Does an Entry Get Stored?

```text
Week 11   browser storage, localStorage
          └ exists only in this browser on my PC

Today     a database on an internet server
          └ anyone who knows the address sees the same entries, from any PC
```

- Open the Week 11 guestbook on a different PC, and the list is empty — the entries aren't on that PC.
- Today, entries go into **one table on a server**. The page reads that table and draws it on screen.
- Leave the Week 11 page as it is. You'll build a new page at `my-web/online/`.

---

## Part 1 · 5–12 min — Create a Supabase Project

1. https://supabase.com → **Start your project** → sign up with a GitHub account or email
2. **New project** → Name it `my-web-guestbook`
3. **Database Password**: note down the generated value, and **don't display it on screen**
4. Choose a nearby region (e.g., Northeast Asia) → **Create new project**
5. It takes 1–2 minutes to become ready

- One project is one database. It gets an address like `https://<project>.supabase.co`.
- You won't use this password even once in today's class. It's not a value you put in the browser.

---

## Part 1 · 12–18 min — Create the Table and Policies with One SQL Run

Left menu **SQL Editor** → paste all of `schema.sql` → **Run**

```sql
create table if not exists public.guestbook ( ... );
alter table public.guestbook enable row level security;
grant select, insert on table public.guestbook to anon;
create policy "guestbook read" ... for select ... using (true);
create policy "guestbook write" ... for insert ... with check (true);
```

- `enable row level security`: locks the table. Now **only what a policy allows** can happen.
- You made just two policies: reading, and inserting new entries. Updating and deleting aren't allowed, since you made no policy for them.
- Check the empty `guestbook` table in **Table Editor**.

---

## Part 1 · 18–22 min — Copy Only the Publishable Key

The **Connect** button at the top shows the Project URL and publishable key on one screen.
If you don't see it: the key is under **Project Settings › API Keys**, the address under **Project Settings › Data API**.

| Value | Where it goes |
|---|---|
| Project URL `https://…supabase.co` | Browser · repository (fine to make public) |
| **publishable key** `sb_publishable_…` | Browser · repository (fine to make public) |
| secret key `sb_secret_…` | Never paste this anywhere |
| Database Password | Never paste this anywhere |

The publishable key can be public because **the table is locked by RLS, and the policies allow only reading and inserting**.

---

## Part 1 · 22–25 min — Two Lines in config.js

```js
const SUPABASE_URL = 'https://YOUR_PROJECT.supabase.co';
const SUPABASE_KEY = 'sb_publishable_YOUR_KEY';
```

- Copy `config.example.js` to `config.js`, and change **only these two values**.
- You push this file to GitHub — your public page needs to read these values.
- This is exactly why you must never put the secret key here. The moment you push it, everyone can see it.

**Explanation total: 5+7+6+4+3 = 25 min**

---

# Part 2 — Saving and Loading

`25 min explanation & demo`

1. Two things the page exchanges with the server
2. Loading, `select`
3. Saving, `insert`
4. Showing errors on screen
5. Handing off the lab

---

## Part 2 · 0–6 min — The Page's Two Jobs

```text
When the page opens     showList()  → select → draws the list on screen
When you click [Post]   submit      → insert → calls showList() again
```

```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="config.js" defer></script>
<script src="guestbook.js" defer></script>
```

- The first line is a file Supabase provides. It's what lets you use `supabase.createClient`.
- The order matters. `config.js` must be read before `guestbook.js` uses those two values.

---

## Part 2 · 6–13 min — Loading with select

```js
const result = await client
  .from('guestbook')
  .select('name, message, created_at')
  .order('created_at', { ascending: false });
```

- `from('guestbook')`: which table. `select(...)`: which columns. `order(...)`: in what order.
- `await` means "wait until an answer comes back from the internet." Treat it as a template for today.
- `async` before a function means "I'll use `await` inside here." The two words always come in pairs (covered properly in Week 12).
- The answer comes back in two parts: `result.data` (an array of entries) and `result.error` (the reason it failed).

---

## Part 2 · 6–13 min — Drawing the Returned Array

```js
const items = result.data;
list.innerHTML = '';
for (let i = 0; i < items.length; i++) {
  const li = document.createElement('li');
  li.textContent = `${items[i].name}: ${items[i].message}`;
  list.append(li);
}
```

- This has the same shape as the `showList()` you wrote in Weeks 10–11.
- Only one thing is different: **where the array came from**. Now it comes from the server.

---

## Part 2 · 13–19 min — Saving with insert

```js
const result = await client
  .from('guestbook')
  .insert({ name: name, message: message });

form.reset();
showList();
```

- `insert({ ... })` takes the place of Week 11's `items.push({ ... })`.
- Don't write `id` or `created_at` — the server fills those in.
- After saving, call `showList()` again to refresh the screen with the new list.

---

## Part 2 · 19–22 min — Showing Errors on Screen

```js
if (result.error) {
  notice.textContent = 'Could not save this entry: ' + result.error.message;
  return;
}
```

| Message shown on screen | Check here first |
|---|---|
| `Invalid API key` | The key line in `config.js` |
| `Could not find the table …` | Whether you ran the SQL on the right project |
| `new row violates row-level security policy …` | The write policy (`schema.sql`, step 5) |

Anything that goes over the internet can fail. When it does, **write why, on screen**.

---

## Part 2 · 22–25 min — Try It Yourself

[Lab](lab.md#실습-60분) · [Walkthrough](walkthrough.md#1-온라인-방명록-폴더-만들기)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/supabase_guestbook

1. Create an `online/` folder → create a project → run `schema.sql` once.
2. Set the two lines in `config.js` → copy in `guestbook.html`/`guestbook.js` → push.
3. Post an entry at the public address, confirm it shows up on another PC too → take one screenshot.

**Explanation total: 6+7+6+3+3 = 25 min**

If you get stuck, read the on-screen notice text and the red line in the Console first.

---

## What We Didn't Use Today

- Login and sign-up (Auth), per-user ownership permissions
- Editing or deleting entries — no policy exists for these, so they don't work yet
- Two tables with a relationship between them

The regular course's guestbook is the `localStorage` version. Today's page lives separately, under `online/`.
