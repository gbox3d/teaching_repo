-- 기존 프로젝트와 새 프로젝트 모두 이 파일로 소개·도움말 API를 추가한다.
-- 방명록 테이블·글·학생 태그·편집 키는 변경하지 않는다.
begin;

-- 고정 안내만 반환하는 뷰다. 학생 데이터나 비밀 테이블을 읽지 않는다.
create or replace view public.about with (security_invoker = true) as
select
  '수업용 REST API'::text as name,
  'v1'::text as version,
  'REST API 접속과 데이터 처리를 연습합니다.'::text as description,
  '/rest/v1/help'::text as help_path;

create or replace view public.help with (security_invoker = true) as
select * from (values
  (1, 'GET', '/rest/v1/about', '서버 소개와 API 버전을 확인합니다.'),
  (2, 'GET', '/rest/v1/help', '사용 가능한 요청을 확인합니다.'),
  (3, 'GET', '/rest/v1/guestbook?book_id=eq.student01', '태그별 방명록을 조회합니다.'),
  (4, 'POST', '/rest/v1/guestbook', 'book_id, name, message를 JSON으로 보내 글을 저장합니다.'),
  (5, 'PATCH', '/rest/v1/guestbook?book_id=eq.student01&id=eq.123', '해당 방명록 편집 키로 선택한 글을 수정합니다.'),
  (6, 'DELETE', '/rest/v1/guestbook?book_id=eq.student01&id=eq.123', '해당 방명록 편집 키로 선택한 글을 삭제합니다.')
) as endpoints(step, method, path, description);

-- 소개·도움말은 공개 키를 사용한 조회만 허용한다.
revoke all on public.about, public.help from public, anon, authenticated;
grant select on public.about, public.help to anon;
commit;
notify pgrst, 'reload schema';
