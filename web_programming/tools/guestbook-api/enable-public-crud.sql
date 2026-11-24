-- 기존 수업용 Supabase 방명록의 SQL Editor에서 실행한다.
-- 공용 API 키를 가진 사용자는 모든 태그의 글을 수정·삭제할 수 있다.
begin;

alter policy classroom_patch on public.guestbook to anon using (true) with check (true);
alter policy classroom_delete on public.guestbook to anon using (true);

-- 구버전의 기존 키 해시를 보존하고 새 태그는 book_id만으로 등록한다.
do $migration$
begin
  if exists (
    select 1 from information_schema.columns
    where table_schema = 'private' and table_name = 'classroom_books'
      and column_name = 'edit_key_hash' and is_nullable = 'NO'
  ) then
    alter table private.classroom_books alter column edit_key_hash drop not null;
  end if;
end
$migration$;

create or replace view public.help with (security_invoker = true) as
select * from (values
  (1, 'GET', '/rest/v1/about', '서버 소개와 API 버전을 확인합니다.'),
  (2, 'GET', '/rest/v1/help', '사용 가능한 요청을 확인합니다.'),
  (3, 'POST', '/rest/v1/guestbook', 'book_id, name, message를 JSON으로 보내 글을 저장합니다.'),
  (4, 'GET', '/rest/v1/guestbook?book_id=eq.student01', '태그별 방명록을 조회합니다.'),
  (5, 'PATCH', '/rest/v1/guestbook?book_id=eq.student01&id=eq.123', '태그와 글 번호로 선택한 글을 수정합니다.'),
  (6, 'DELETE', '/rest/v1/guestbook?book_id=eq.student01&id=eq.123', '태그와 글 번호로 선택한 글을 삭제합니다.')
) as endpoints(step, method, path, description);
revoke all on public.help from public, anon, authenticated;
grant select on public.help to anon;
commit;
notify pgrst, 'reload schema';
