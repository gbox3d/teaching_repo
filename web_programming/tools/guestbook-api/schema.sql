-- 정규 공용 API는 강의자가, 연구 특강은 프로젝트 담당자가 새 Supabase 프로젝트에서 실행한다.
-- 이 파일에는 실제 편집 키가 없다. 정규 학생에게는 공용 서버의 SQL 편집 권한을 주지 않는다.
begin;
create schema if not exists private;
revoke all on schema private from public, anon, authenticated;
create extension if not exists pgcrypto with schema extensions;

create table private.classroom_books (
  book_id text primary key check (book_id ~ '^[a-z0-9_-]{1,40}$'),
  edit_key_hash text not null
);
alter table private.classroom_books enable row level security;
revoke all on private.classroom_books from public, anon, authenticated;

create table public.guestbook (
  id bigint generated always as identity primary key,
  book_id text not null references private.classroom_books(book_id),
  name text not null check (char_length(name) <= 30 and name ~ '[^[:space:]]'),
  message text not null check (char_length(message) <= 500 and message ~ '[^[:space:]]'),
  created_at timestamptz not null default now()
);
create index guestbook_book_id_id on public.guestbook(book_id, id desc);
alter table public.guestbook enable row level security;

create function private.can_edit_book(target_book text)
returns boolean language sql stable security definer set search_path = '' as $$
  select exists (
    select 1 from private.classroom_books b
    where b.book_id = target_book
      and b.edit_key_hash = encode(extensions.digest(
        coalesce(nullif(current_setting('request.headers', true), ''), '{}')::jsonb
          ->> 'x-edit-key', 'sha256'), 'hex')
  );
$$;
revoke all on function private.can_edit_book(text) from public, anon, authenticated;
grant usage on schema private to anon;
grant execute on function private.can_edit_book(text) to anon;

-- 공개 방명록: 읽기와 새 글 쓰기는 모두 허용, 수정·삭제는 해당 방명록 키로 제한.
revoke all on public.guestbook from public, anon, authenticated;
grant select, delete on public.guestbook to anon;
grant insert (book_id, name, message) on public.guestbook to anon;
grant update (name, message) on public.guestbook to anon;
revoke all on sequence public.guestbook_id_seq from public, anon, authenticated;
grant usage on sequence public.guestbook_id_seq to anon;
create policy classroom_read on public.guestbook for select to anon using (true);
create policy classroom_post on public.guestbook for insert to anon with check (true);
create policy classroom_patch on public.guestbook for update to anon
  using (private.can_edit_book(book_id)) with check (private.can_edit_book(book_id));
create policy classroom_delete on public.guestbook for delete to anon
  using (private.can_edit_book(book_id));
commit;
notify pgrst, 'reload schema';
