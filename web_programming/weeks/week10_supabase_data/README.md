# 10주차 — Supabase 데이터 연결

9주차 walking skeleton의 static JSON data source를 Supabase Data API 읽기로 교체한다. SQL로 table·constraint·seed·grant·RLS policy를 재현하고, 브라우저에는 project URL과 publishable key만 둔다. 쓰기와 사용자별 소유권은 11주차 Auth/RLS에서 다룬다.

## 학습 목표

1. browser → Supabase client → Data API → Postgres → RLS 흐름을 설명한다.
2. 재실행 가능한 SQL로 읽기 전용 실습 table과 seed를 준비한다.
3. publishable key와 secret key의 보안 경계를 구분한다.
4. grant와 RLS policy가 서로 다른 두 접근 제어 층임을 설명한다.
5. Supabase JavaScript client의 `{ data, error }` 결과를 상태별 UI로 처리한다.
6. SQL Editor 결과 3행과 unauthenticated browser 결과 2행의 차이를 RLS로 설명한다.

## 수업 흐름

| 일차 | 30분 설명·시연 | 60분 직접 해결 |
|---|---|---|
| 1일차 | Data API, API key, grant, RLS와 policy | SQL 실행·재실행·정책 교차 검증 |
| 2일차 | client/query, 상태 UI, Network 진단 | data source 교체·Pages·오류 복구 |

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [두 차시 실습](lab.md)
- [예제 안내](examples/README.md)
- [재현 SQL 안내](examples/sql/README.md)
- [schema·policy·seed SQL](examples/sql/schema.sql)
- [브라우저 starter](examples/starter/index.html)

## 보안 규칙

- 브라우저에는 `https://YOUR_PROJECT_REF.supabase.co`와 `sb_publishable_REPLACE_ME` 형태의 placeholder만 제공한다.
- 실제 연결 시에도 publishable key만 사용한다.
- secret key, legacy `service_role`, database password, connection string을 HTML·JavaScript·Git에 넣지 않는다.
- publishable key는 공개 클라이언트용 식별자이며 데이터 허용 범위는 grant와 RLS로 제한한다.
- 11주차 전에는 `anon` 역할에 INSERT/UPDATE/DELETE를 허용하지 않는다.

## 완료 기준

- `schema.sql`을 두 번 실행해도 seed가 중복되지 않는다.
- SQL Editor의 관리자 조회에서는 seed 3행을 확인한다.
- 로그인하지 않은 starter에서는 `is_published = true`인 2행만 확인한다.
- placeholder, 잘못된 URL/key, policy 부재/오류를 구분해 진단한다.
- loading·empty·success·error 상태 중 하나만 화면에 보인다.
- Network 요청, 화면 결과, 적용 policy를 증거로 남긴다.

## 공식 참고

- [Supabase API key 이해](https://supabase.com/docs/guides/getting-started/api-keys)
- [데이터 보안](https://supabase.com/docs/guides/database/secure-data)
- [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [JavaScript client 초기화](https://supabase.com/docs/reference/javascript/initializing)
