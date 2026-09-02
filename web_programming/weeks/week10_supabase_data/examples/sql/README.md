# 재현 SQL 사용법

## 대상

개인 또는 수업용 Supabase project의 SQL Editor에서만 실행한다. project 이름을 다시 확인하고 운영 데이터가 있는 다른 project에는 실행하지 않는다.

## 실행

1. [`schema.sql`](schema.sql) 전체를 실행한다.
2. 결과 SELECT가 `all_rows = 3`, `published_rows = 2`인지 확인한다.
3. 같은 파일을 한 번 더 실행한다.
4. 다시 3/2인지 확인한다.
5. [`verify.sql`](verify.sql)을 실행해 RLS, policy, privilege를 확인한다.

`schema.sql`은 이 수업 전용 `public.course_posts`만 만들며 기존 table을 drop하지 않는다. stable `slug`와 `on conflict`를 사용하므로 seed를 재실행해도 중복되지 않는다.

## 기대 보안 상태

- RLS: enabled
- `anon`: SELECT true, INSERT/UPDATE/DELETE false
- `authenticated`: SELECT true, INSERT/UPDATE/DELETE false
- SELECT policy: `is_published = true`

SQL Editor의 관리자 결과와 browser의 `anon` 결과가 다를 수 있다. browser에서는 공개된 2행만 보여야 한다.
