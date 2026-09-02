select
  c.relname as table_name,
  c.relrowsecurity as rls_enabled,
  c.relforcerowsecurity as rls_forced
from pg_class as c
join pg_namespace as n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relname = 'course_posts';

select
  policyname,
  roles,
  cmd,
  qual,
  with_check
from pg_policies
where schemaname = 'public'
  and tablename = 'course_posts';

select
  role_name,
  has_table_privilege(role_name, 'public.course_posts', 'SELECT') as can_select,
  has_table_privilege(role_name, 'public.course_posts', 'INSERT') as can_insert,
  has_table_privilege(role_name, 'public.course_posts', 'UPDATE') as can_update,
  has_table_privilege(role_name, 'public.course_posts', 'DELETE') as can_delete
from (
  values ('anon'), ('authenticated')
) as roles(role_name);

select id, slug, title, is_published, created_at
from public.course_posts
order by created_at;
