-- 정규 공용 API는 강의자가, 연구 특강은 프로젝트 담당자가 새 Supabase 프로젝트에서 실행한다.
-- 기존 방명록은 enable-public-crud.sql로 전환한다.
begin;
create schema if not exists private;
revoke all on schema private from public, anon, authenticated;

create table private.classroom_books (
  book_id text primary key check (book_id ~ '^[a-z0-9_-]{1,40}$')
);
alter table private.classroom_books enable row level security;
revoke all on private.classroom_books from public, anon, authenticated;

insert into private.classroom_books (book_id)
select 'student' || lpad(n::text, 2, '0') from generate_series(1, 30) as students(n);

create table public.guestbook (
  id bigint generated always as identity primary key,
  book_id text not null references private.classroom_books(book_id),
  name text not null check (char_length(name) <= 30 and name ~ '[^[:space:]]'),
  message text not null check (char_length(message) <= 500 and message ~ '[^[:space:]]'),
  created_at timestamptz not null default now()
);
create index guestbook_book_id_id on public.guestbook(book_id, id desc);
alter table public.guestbook enable row level security;

-- 공용 API 키로 수업용 글을 생성·조회·수정·삭제한다.
revoke all on public.guestbook from public, anon, authenticated;
grant select, delete on public.guestbook to anon;
grant insert (book_id, name, message) on public.guestbook to anon;
grant update (name, message) on public.guestbook to anon;
revoke all on sequence public.guestbook_id_seq from public, anon, authenticated;
grant usage on sequence public.guestbook_id_seq to anon;
create policy classroom_read on public.guestbook for select to anon using (true);
create policy classroom_post on public.guestbook for insert to anon with check (true);
create policy classroom_patch on public.guestbook for update to anon
  using (true) with check (true);
create policy classroom_delete on public.guestbook for delete to anon
  using (true);
commit;
notify pgrst, 'reload schema';
