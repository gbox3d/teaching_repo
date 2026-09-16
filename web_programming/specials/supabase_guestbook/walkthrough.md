# 특강 따라하기 — Supabase 방명록

처음에는 그대로 따라 하고, 결과가 나오면 본인 문구로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소의 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**)에서 실행한다. 명령 앞에 **현재 폴더**를 적어 두었다.

**확인의 기준은 공개 주소다.** `file://`로 열면 목록이 보이지 않는다(9단계에서 다시 설명한다).

## 준비

11주차까지의 `my-web`이 있어야 한다. 같은 PC면 `git pull`, 다른 PC면 `git clone`부터 한다. 현재 폴더: `my-web`

```bash
git pull
```

**예상 결과** — `Already up to date.` 또는 `Fast-forward`와 바뀐 파일 목록. `my-web` 폴더에 `index.html`·`guestbook.html`이 보인다.

## 1. 온라인 방명록 폴더 만들기

11주차까지 만든 `guestbook.html`은 그대로 둔다. 새 폴더에 오늘 것을 만든다.

1. VS Code 왼쪽 탐색기에서 **New Folder** 아이콘을 누르고 이름을 `online`으로 한다.
2. 그 폴더 안에 나중에 `config.js`·`guestbook.html`·`guestbook.js` 세 파일을 만든다.

**예상 결과** — `my-web` 안에 빈 폴더 `online`이 있다. 이 폴더의 공개 주소는 `https://student01.github.io/my-web/online/`이 된다.

## 2. Supabase 계정과 프로젝트 만들기

1. https://supabase.com 에서 **Start your project**를 누르고 GitHub 계정 또는 이메일로 가입한다.
2. **New project**를 누른다.
3. **Name**에 `my-web-guestbook`을 적는다.
4. **Database Password**는 만들어 주는 값을 그대로 쓰고 따로 메모해 둔다. 이 값은 오늘 한 번도 쓰지 않으며 화면에 띄우지 않는다.
5. **Region**은 가까운 곳을 고른다.
6. **Create new project**를 누르고 1~2분 기다린다.

**예상 결과** — 프로젝트 대시보드가 열리고 왼쪽에 **Table Editor**·**SQL Editor**·**Project Settings** 메뉴가 보인다.

- 화면 이름은 Supabase가 바꿀 수 있다. 메뉴 이름이 다르면 강의자 화면을 따른다.
- 이미 프로젝트가 있으면 새로 만들지 말고 그것을 쓴다. 단, 내 프로젝트인지 이름을 먼저 확인한다.

## 3. SQL Editor에서 표와 정책 만들기

1. 왼쪽 메뉴 **SQL Editor**를 누른다.
2. 아래 SQL 전체를 붙여 넣는다. 같은 파일이 [examples/schema.sql](examples/schema.sql)에 있다.

```sql
-- Supabase 대시보드의 SQL Editor 에 이 파일 전체를 붙여 넣고 Run 을 한 번 누른다.
-- 다시 실행해도 표가 지워지거나 글이 사라지지 않는다.

-- 1. 방명록 표 하나를 만든다.
create table if not exists public.guestbook (
  id bigint generated always as identity primary key,
  name text not null check (char_length(name) between 1 and 20),
  message text not null check (char_length(message) between 1 and 200),
  created_at timestamptz not null default now()
);

-- 2. 이 표를 잠근다. 이제 허용한 것만 된다.
alter table public.guestbook enable row level security;

-- 3. 로그인하지 않은 방문자(anon)에게 읽기와 쓰기 명령만 허용한다.
grant select, insert on table public.guestbook to anon;

-- 4. 읽기 정책: 모든 글을 읽을 수 있다.
drop policy if exists "guestbook read" on public.guestbook;
create policy "guestbook read"
on public.guestbook
for select
to anon
using (true);

-- 5. 쓰기 정책: 새 글을 추가할 수 있다. 수정과 삭제는 허용하지 않았으므로 안 된다.
drop policy if exists "guestbook write" on public.guestbook;
create policy "guestbook write"
on public.guestbook
for insert
to anon
with check (true);

-- 6. 지금 표에 글이 몇 개인지 확인한다.
select count(*) as guestbook_rows from public.guestbook;
```

3. **Run**을 한 번 누른다.

**예상 결과** — 아래 결과 칸에 `guestbook_rows` 한 칸이 나오고 값은 `0`이다. 아직 글이 없기 때문이다.

4. 왼쪽 메뉴 **Table Editor**에서 `guestbook` 표를 고른다. 칸 이름 `id`·`name`·`message`·`created_at`이 보이고 행은 없다.

- 같은 SQL을 다시 실행해도 된다. `create table if not exists`와 `drop policy if exists`가 있어 표와 글이 지워지지 않는다.
- 남의 프로젝트에서 실행하지 않는다. 화면 왼쪽 위의 프로젝트 이름을 먼저 본다.

## 4. 프로젝트 URL과 publishable key 복사하기

1. 대시보드 위쪽의 **Connect** 버튼을 누른다. 열린 화면에 **Project URL**과 **publishable key**가 함께 나온다.
2. **Project URL** `https://…supabase.co`를 복사해 둔다.
3. **publishable key**(`sb_publishable_`로 시작하는 값)를 복사해 둔다.

**예상 결과** — 두 값이 클립보드와 메모장에 있다.

- **Connect** 버튼이 안 보이면 두 값을 나눠 찾는다. 키는 **Project Settings › API Keys**, 주소는 **Project Settings › Data API**에 있다.
- `sb_secret_`로 시작하는 secret key, `service_role`, connection string, 데이터베이스 비밀번호는 복사하지 않는다. 화면 공유 중이면 그 영역을 가린다.
- 두 값을 남에게 보여 줘도 되는 이유는 3단계에서 표를 잠그고 정책 두 개만 허용했기 때문이다.

## 5. config.js 만들기

`online` 폴더에 `config.js`를 새로 만들고 아래 내용을 넣는다. 같은 파일이 [examples/config.example.js](examples/config.example.js)에 있다.

```js
// 이 파일을 복사해 config.js 로 만들고 두 줄의 값만 바꾼다.
// 여기에는 공개해도 되는 값만 적는다. 프로젝트 URL 과 publishable key 두 가지다.
// secret key, 데이터베이스 비밀번호, connection string 은 적지 않는다.

const SUPABASE_URL = 'https://YOUR_PROJECT.supabase.co';
const SUPABASE_KEY = 'sb_publishable_YOUR_KEY';
```

그다음 두 줄의 값을 4단계에서 복사한 내 값으로 바꾼다. 따옴표는 지우지 않는다.

**예상 결과** — `config.js`의 두 줄이 이런 모양이 된다.

```text
const SUPABASE_URL = 'https://abcdefghijklmnop.supabase.co';
const SUPABASE_KEY = 'sb_publishable_xxxxxxxxxxxxxxxxxxxx';
```

- 파일 이름은 `config.js`다. `config.example.js`라는 이름 그대로 두면 8단계에서 페이지가 값을 찾지 못한다.
- 이 파일은 GitHub에 올린다. 공개 페이지가 읽어야 하는 값이다.

## 6. guestbook.html 만들기

11주차 방명록과 달라지는 것은 **글을 어디에 두는가** 하나다.

| 하는 일 | 11주차 `guestbook.js` | 오늘 `online/guestbook.js` |
|---|---|---|
| 저장 | `items.push(...)` → `localStorage.setItem` | `insert({ ... })` |
| 읽기 | `JSON.parse(localStorage.getItem('guestbook'))` | `select(...)` |
| 목록 보관 | 내 브라우저의 배열 `items` | 서버의 표 `guestbook` |
| 삭제 버튼 | 있음(`splice`) | 없음 — 삭제 정책을 만들지 않았다 |

`online` 폴더에 `guestbook.html`을 만들고 아래 내용을 그대로 넣는다. 같은 파일이 [examples/guestbook.html](examples/guestbook.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 서버 방명록</title>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="config.js" defer></script>
    <script src="guestbook.js" defer></script>
  </head>
  <body>
    <main>
      <h1>서버에 저장하는 방명록</h1>
      <p>여기에 남긴 글은 인터넷 서버에 저장되어 다른 PC에서도 보입니다.</p>

      <form id="guestbook-form">
        <p>
          <label for="name">이름</label>
          <input id="name" type="text" maxlength="20">
        </p>
        <p>
          <label for="message">메시지</label>
          <input id="message" type="text" maxlength="200">
        </p>
        <button type="submit">남기기</button>
      </form>

      <p id="notice">불러오는 중…</p>
      <ul id="list"></ul>

      <p><a href="../index.html">첫 페이지로 돌아가기</a></p>
    </main>
  </body>
</html>
```

**예상 결과** — 아직 브라우저로 열지 않는다. 다음 단계의 `guestbook.js`가 없으면 화면이 `불러오는 중…`에서 멈춘다.

- 오늘 페이지는 폼과 목록만 남긴 최소판이다. 11주차 `guestbook.html`의 이메일 칸·개수 표시·전체 지우기 버튼은 없다.
- `<script>` 세 줄의 순서를 바꾸지 않는다. 첫 줄이 Supabase가 공개해 둔 파일이고, `config.js`가 `guestbook.js`보다 먼저다.
- 4주차 CSS를 쓰고 싶으면 `<head>`에 `<link rel="stylesheet" href="../styles.css">` 한 줄을 더한다. `online` 폴더에서 한 칸 위가 `my-web`이다.

## 7. guestbook.js 만들기

`online` 폴더에 `guestbook.js`를 만들고 아래 내용을 그대로 넣는다. 같은 파일이 [examples/guestbook.js](examples/guestbook.js)에 있다.

```js
const client = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const list = document.querySelector('#list');
const notice = document.querySelector('#notice');

async function showList() {
  const result = await client
    .from('guestbook')
    .select('name, message, created_at')
    .order('created_at', { ascending: false });

  if (result.error) {
    notice.textContent = '불러오지 못했습니다: ' + result.error.message;
    return;
  }

  const items = result.data;
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const date = new Date(items[i].created_at).toLocaleDateString();
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message} (${date})`;
    list.append(li);
  }
  notice.textContent = `방명록 ${items.length}개`;
}

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();

  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    return;
  }

  const result = await client
    .from('guestbook')
    .insert({ name: name, message: message });

  if (result.error) {
    notice.textContent = '저장하지 못했습니다: ' + result.error.message;
    return;
  }

  form.reset();
  nameInput.focus();
  showList();
});

showList();
```

**예상 결과** — 세 파일이 `online` 폴더에 모였다. `config.js`·`guestbook.html`·`guestbook.js`.

- `showList()`의 `for` 문은 10·11주차에 쓴 것과 같다. 배열이 서버에서 왔다는 점만 다르다.
- `await`는 "답이 올 때까지 기다린다"는 표시다. 이 줄들은 틀로 쓰고 넘어간다.

## 8. push하고 공개 주소에서 확인하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "특강: 서버 방명록 페이지 추가"
git push
```

**예상 결과** — `3 files changed`와 push 출력이 보인다. 1분쯤 뒤 아래 주소가 열린다.

```text
https://student01.github.io/my-web/online/guestbook.html
```

1. 주소를 열면 폼과 함께 `방명록 0개`가 보인다.
2. 이름에 `student01`, 메시지에 `잘 봤습니다`를 넣고 **남기기**를 누른다.
3. 목록에 한 줄이 생기고 안내 문구가 `방명록 1개`로 바뀐다.
4. **F5**로 새로고침해도 그 줄이 남아 있다.
5. Supabase **Table Editor**의 `guestbook` 표를 새로고침하면 같은 내용의 행이 한 줄 있다. 이 두 화면이 **캡처 1장**이다.

- 1~3분 늦게 반영될 수 있다. 5분 안에 안 보이면 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- `방명록 0개` 대신 빨간 안내 문구가 보이면 [실습지의 막혔을 때](lab.md#막혔을-때)에서 문구를 찾는다.

## 9. 다른 PC에서 열어 보기

휴대폰이나 옆자리 PC에서 같은 주소를 연다.

**예상 결과** — 방금 남긴 글이 **그대로 보인다**. 11주차 방명록은 다른 PC에서 비어 있었다. 오늘 글은 서버에 있기 때문에 보인다.

- `file://`로(파일을 더블클릭해) 열면 목록이 보이지 않는다. 브라우저가 파일에서 인터넷 요청을 막기 때문이다. 오늘 확인은 공개 주소에서만 한다.
- 옆자리 학생이 내 주소에 글을 남길 수 있다. 정책이 "누구나 쓰기"이기 때문이다. 캡처는 내 글이 보일 때 찍는다.

## 10. 특강이 끝나면

- 방명록 페이지를 남겨 두려면 그대로 둔다. 무료 프로젝트는 한동안 쓰지 않으면 일시정지되므로, 나중에 열었을 때 목록이 안 나오면 대시보드에서 프로젝트를 다시 켠다.
- 지우려면 `online` 폴더를 지우고 `git add . → git commit → git push` 한다. 11주차까지의 `guestbook.html`은 그대로 남는다.
- 공용 PC면 실습 끝에 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고, Supabase 대시보드에서도 로그아웃한다.

## 오류가 나면

먼저 화면의 안내 문구를 읽고, 없으면 DevTools **Console**의 빨간 줄을 읽는다.
자주 나오는 문구와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 실행하고, 해결되지 않으면 화면을 그대로 보여 주고 도움을 요청한다.
