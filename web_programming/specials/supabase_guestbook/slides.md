---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 특강"
footer: "Supabase로 만드는 서버 방명록 · 선택 · 110분"
---

# Supabase로 만드는 서버 방명록

11주차 방명록은 **내 브라우저**에만 남았습니다.
오늘은 같은 방명록을 **인터넷 서버**에 저장해 다른 PC에서도 보이게 합니다.

```text
내 PC 브라우저 ── insert ──▶ Supabase 표 guestbook
              ◀── select ──
```

---

# 1부 — 프로젝트와 표 만들기

`25분 설명·시연`

1. 글이 저장되는 두 곳
2. Supabase 프로젝트 만들기
3. 제공 SQL 한 번 실행하기
4. publishable key만 복사하기
5. `config.js` 두 줄 바꾸기

---

## 1부 · 0–5분 — 글은 어디에 저장되나

```text
11주차  브라우저 저장소 localStorage
        └ 내 PC의 이 브라우저에만 있다

오늘    인터넷 서버의 데이터베이스
        └ 주소만 알면 다른 PC에서도 같은 글이 보인다
```

- 11주차 방명록을 다른 PC에서 열면 목록이 비어 있습니다. 글이 그 PC에 없기 때문입니다.
- 오늘은 글을 **서버의 표 한 개**에 넣습니다. 페이지는 그 표를 읽어 화면에 그립니다.
- 11주차 페이지는 그대로 두고 `my-web/online/`에 새 페이지를 만듭니다.

---

## 1부 · 5–12분 — Supabase 프로젝트 만들기

1. https://supabase.com → **Start your project** → GitHub 계정 또는 이메일로 가입
2. **New project** → Name `my-web-guestbook`
3. **Database Password**: 만들어 주는 값을 메모해 두고 **화면에 띄우지 않습니다**
4. Region은 가까운 곳(예: Northeast Asia) → **Create new project**
5. 준비되는 데 1~2분 걸립니다

- project 하나가 데이터베이스 하나입니다. 주소 `https://<프로젝트>.supabase.co`가 붙습니다.
- 이 비밀번호는 오늘 수업에서 한 번도 쓰지 않습니다. 브라우저에 넣는 값이 아닙니다.

---

## 1부 · 12–18분 — SQL 한 번으로 표와 정책 만들기

왼쪽 메뉴 **SQL Editor** → `schema.sql` 전체 붙여 넣기 → **Run**

```sql
create table if not exists public.guestbook ( ... );
alter table public.guestbook enable row level security;
grant select, insert on table public.guestbook to anon;
create policy "guestbook read" ... for select ... using (true);
create policy "guestbook write" ... for insert ... with check (true);
```

- `enable row level security`: 표를 잠급니다. 이제 **정책으로 허용한 것만** 됩니다.
- 정책 두 개만 만들었습니다. 읽기와 새 글 넣기. 수정·삭제는 허용하지 않았으므로 안 됩니다.
- **Table Editor**에서 빈 `guestbook` 표를 눈으로 확인합니다.

---

## 1부 · 18–22분 — publishable key만 복사하기

위쪽 **Connect** 버튼 — Project URL과 publishable key가 한 화면에 나옵니다.
없으면 키는 **Project Settings › API Keys**, 주소는 **Project Settings › Data API**.

| 값 | 어디에 두나 |
|---|---|
| Project URL `https://…supabase.co` | 브라우저 · 저장소 (공개해도 됨) |
| **publishable key** `sb_publishable_…` | 브라우저 · 저장소 (공개해도 됨) |
| secret key `sb_secret_…` | 어디에도 붙여 넣지 않음 |
| Database Password | 어디에도 붙여 넣지 않음 |

publishable key가 공개돼도 되는 이유는 **표가 RLS로 잠겨 있고 정책이 읽기·쓰기만 허용**하기 때문입니다.

---

## 1부 · 22–25분 — config.js 두 줄

```js
const SUPABASE_URL = 'https://YOUR_PROJECT.supabase.co';
const SUPABASE_KEY = 'sb_publishable_YOUR_KEY';
```

- `config.example.js`를 복사해 `config.js`로 만들고 **두 줄의 값만** 바꿉니다.
- 이 파일은 GitHub에 올립니다. 공개 페이지가 읽어야 하는 값이기 때문입니다.
- 여기에 secret key를 넣으면 안 되는 이유가 이것입니다. 올리는 순간 모두가 봅니다.

**설명 합계: 5+7+6+4+3 = 25분**

---

# 2부 — 저장하고 불러오기

`25분 설명·시연`

1. 페이지가 서버와 주고받는 두 가지
2. 불러오기 `select`
3. 저장하기 `insert`
4. 오류를 화면에 보여 주기
5. 실습 인계

---

## 2부 · 0–6분 — 페이지가 하는 두 가지

```text
페이지를 열 때        showList()  → select → 목록을 화면에 그린다
[남기기]를 눌렀을 때   submit      → insert → 다시 showList()
```

```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="config.js" defer></script>
<script src="guestbook.js" defer></script>
```

- 첫 줄은 Supabase가 만들어 둔 파일입니다. 이 줄 덕분에 `supabase.createClient`를 쓸 수 있습니다.
- 순서가 중요합니다. `config.js`가 먼저 읽혀야 `guestbook.js`가 두 값을 씁니다.

---

## 2부 · 6–13분 — 불러오기 select

```js
const result = await client
  .from('guestbook')
  .select('name, message, created_at')
  .order('created_at', { ascending: false });
```

- `from('guestbook')`: 어느 표에서. `select(...)`: 어떤 칸을. `order(...)`: 어떤 순서로.
- `await`는 "인터넷에서 답이 올 때까지 기다린다"는 표시입니다. 오늘은 틀로 씁니다.
- 함수 앞의 `async`는 그 안에서 `await`를 쓰겠다는 표시입니다. 두 단어는 늘 짝입니다(정규 수업은 12주차).
- 답은 `result.data`(글 배열)와 `result.error`(실패 이유) 두 칸으로 옵니다.

---

## 2부 · 6–13분 — 받은 배열을 화면에 그리기

```js
const items = result.data;
list.innerHTML = '';
for (let i = 0; i < items.length; i++) {
  const li = document.createElement('li');
  li.textContent = `${items[i].name}: ${items[i].message}`;
  list.append(li);
}
```

- 10·11주차에 쓴 `showList()`와 같은 모양입니다.
- 달라진 것은 **배열이 어디서 왔는가** 하나뿐입니다. 서버가 준 배열입니다.

---

## 2부 · 13–19분 — 저장하기 insert

```js
const result = await client
  .from('guestbook')
  .insert({ name: name, message: message });

form.reset();
showList();
```

- 11주차의 `items.push({ ... })` 자리에 `insert({ ... })`가 들어갔습니다.
- `id`와 `created_at`은 적지 않습니다. 서버가 넣어 줍니다.
- 저장한 뒤 `showList()`를 다시 불러 화면을 새 목록으로 바꿉니다.

---

## 2부 · 19–22분 — 오류를 화면에 보여 주기

```js
if (result.error) {
  notice.textContent = '저장하지 못했습니다: ' + result.error.message;
  return;
}
```

| 화면에 보이는 문구 | 먼저 볼 곳 |
|---|---|
| `Invalid API key` | `config.js`의 key 한 줄 |
| `Could not find the table …` | SQL을 실행한 프로젝트가 맞는지 |
| `new row violates row-level security policy …` | 쓰기 정책(`schema.sql` 5번) |

인터넷을 거치는 일은 실패할 수 있습니다. 실패하면 **왜인지 화면에 적습니다**.

---

## 2부 · 22–25분 — 이제 직접 해 보기

[실습](lab.md#실습-60분) · [따라하기](walkthrough.md#1-온라인-방명록-폴더-만들기)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/supabase_guestbook

1. `online/` 폴더 → 프로젝트 만들기 → `schema.sql` 한 번 실행
2. `config.js` 두 줄 → `guestbook.html`·`guestbook.js` 복사 → push
3. 공개 주소에서 글을 남기고, 다른 PC에서도 보이는지 확인 → 캡처 1장

**설명 합계: 6+7+6+3+3 = 25분**

막히면 화면의 안내 문구와 Console의 빨간 줄을 먼저 읽습니다.

---

## 오늘 쓰지 않은 것

- 로그인·회원가입(Auth), 사용자별 소유자 권한
- 글 수정·삭제 — 정책을 만들지 않았으므로 지금은 되지 않습니다
- 관계 있는 두 표

정규 수업의 방명록은 `localStorage` 쪽입니다. 오늘 만든 페이지는 `online/`에 따로 있습니다.
