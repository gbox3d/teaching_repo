create table if not exists public.course_posts (
  id bigint generated always as identity primary key,
  slug text not null unique,
  title text not null check (char_length(title) between 1 and 100),
  summary text not null default '' check (char_length(summary) <= 300),
  is_published boolean not null default false,
  created_at timestamptz not null default now()
);

alter table public.course_posts enable row level security;

revoke all on table public.course_posts from anon, authenticated;
grant select on table public.course_posts to anon, authenticated;

drop policy if exists "course posts published read" on public.course_posts;

create policy "course posts published read"
on public.course_posts
for select
to anon, authenticated
using (is_published = true);

create index if not exists course_posts_published_created_idx
on public.course_posts (is_published, created_at desc);

insert into public.course_posts (
  slug,
  title,
  summary,
  is_published,
  created_at
)
values
  (
    'dom-state',
    'DOM 상태 흐름',
    '입력, 상태 변경, render의 한 방향 흐름을 복습합니다.',
    true,
    '2026-01-10T09:00:00+00:00'
  ),
  (
    'async-ui',
    '비동기 UI 상태',
    'loading, empty, success, error를 구분합니다.',
    true,
    '2026-01-11T09:00:00+00:00'
  ),
  (
    'owner-rls-preview',
    '소유자 RLS 예고',
    '11주차 공개 전 초안이므로 browser에는 보이지 않아야 합니다.',
    false,
    '2026-01-12T09:00:00+00:00'
  )
on conflict (slug) do update
set
  title = excluded.title,
  summary = excluded.summary,
  is_published = excluded.is_published,
  created_at = excluded.created_at;

select
  count(*) as all_rows,
  count(*) filter (where is_published) as published_rows
from public.course_posts;
