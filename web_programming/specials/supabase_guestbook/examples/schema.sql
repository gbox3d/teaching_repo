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
