---
marp: true
theme: default
paginate: true
header: 웹프로그래밍
footer: 10주차 · Supabase 데이터 연결
---

# Supabase 데이터 연결

## 1일차: 공개 읽기를 안전하게 열기

질문: **browser가 database를 직접 호출해도 되는 조건은 무엇인가?**

---

## 요청 경로

```text
Browser
  → supabase-js
  → Data API
  → Postgres grant
  → RLS policy
  → 허용된 rows
```

publishable key만으로 권한을 결정하지 않는다.

---

## 두 개의 인증

| 항목 | 뜻 |
|---|---|
| publishable key | 어느 Supabase project를 호출하는 공개 client인지 |
| 사용자 JWT | 로그인한 사용자가 누구인지 |

이번 주: 로그인 전 요청 → Postgres의 `anon` 역할<br>
11주차: 로그인 후 요청 → `authenticated` 역할 + 사용자 식별

---

## browser에 둘 수 있는 것

```js
const url = "https://YOUR_PROJECT_REF.supabase.co";
const key = "sb_publishable_REPLACE_ME";
```

가능: project URL, publishable key<br>
불가: secret key, service-role key, DB password, connection string

브라우저에 전달된 값은 DevTools에서 볼 수 있다.

---

## grant와 RLS는 다른 층

```sql
grant select on table public.course_posts to anon;
```

grant: 역할이 table의 어떤 명령을 실행할 수 있는가?

```sql
create policy "published rows are readable"
on public.course_posts for select to anon
using (is_published = true);
```

RLS: 그 명령이 어떤 row에 적용되는가?

---

## SQL로 만든 table은 RLS를 직접 켠다

```sql
alter table public.course_posts
enable row level security;
```

public처럼 Data API에 노출된 schema의 table은 RLS와 policy를 함께 검토한다.

policy가 없으면 publishable client에는 행이 보이지 않는 것이 안전한 기본값이다.

---

## 재현 가능한 schema

```sql
create table if not exists public.course_posts (...);

insert into public.course_posts (slug, title, ...)
values (...)
on conflict (slug) do update set ...;
```

- 이름과 constraint를 명시
- 안정된 unique key로 seed 중복 방지
- policy는 drop/create로 기대 상태 고정

---

## 공개 읽기만 허용

```sql
revoke all on table public.course_posts
from anon, authenticated;

grant select on table public.course_posts
to anon, authenticated;
```

이번 주에는 browser write를 열지 않는다.

다음 주 Auth와 owner policy 전에 임시 `using (true)` 쓰기 policy를 만들지 않는다.

---

## 관찰 실험

seed:

- published 2행
- unpublished 1행

| 실행 위치 | 기대 |
|---|---:|
| SQL Editor 관리자 조회 | 3행 |
| 로그인 전 browser client | 2행 |

차이는 UI filter가 아니라 RLS policy가 만든다.

---

# 2일차: data source를 교체하고 진단하기

UI 계약은 유지하고 data source 내부만 바꾼다.

---

## client 초기화

```js
import { createClient } from "@supabase/supabase-js";

const client = createClient(
  "https://YOUR_PROJECT_REF.supabase.co",
  "sb_publishable_REPLACE_ME"
);
```

예제는 browser ESM CDN의 고정된 major version을 사용한다.

placeholder를 실제 project 값으로 바꾸기 전 요청하지 않는다.

---

## select 결과

```js
const { data, error } = await client
  .from("course_posts")
  .select("id, slug, title, summary, created_at")
  .order("created_at", { ascending: false });

if (error) throw error;
```

필요한 column만 선택하고 error를 명시적으로 처리한다.

---

## RLS는 자동 filter처럼 보인다

```sql
using (is_published = true)
```

browser query가 모든 행을 요청해도 허용된 행만 반환한다.

중요:

- 숨겨진 행의 존재를 client가 구분할 수 없음
- “0행”은 error가 아님
- 관리 화면의 결과와 client 결과가 다를 수 있음

---

## UI 상태

```text
setup    : placeholder가 남음
loading  : 요청 중
empty    : data.length === 0
success  : 공개 rows 표시
error    : error 존재/연결 실패
```

setup은 network error가 아니다. 사용자가 해야 할 다음 행동을 정확히 안내한다.

---

## 오류를 층별로 읽기

| 관찰 | 우선 확인 |
|---|---|
| import 실패 | CDN/Network/CSP |
| project URL 실패 | URL·DNS |
| 401/invalid key | publishable key |
| permission denied | grant |
| 0 rows | RLS policy·seed 조건 |
| relation not found | table/schema 이름 |

Console과 Network의 첫 실패를 함께 본다.

---

## key를 숨기는 것과 권한을 제한하는 것

정적 Pages의 JavaScript 변수는 공개된다.

```text
난독화/별도 파일 ≠ secret
publishable key + RLS + least grant = 공개 client의 보안 모델
```

비밀이 필요한 기능은 server/Edge Function 경계 뒤로 이동한다.

---

## 배포 검증

1. 새 탭에서 Pages URL 열기
2. module/CDN/Data API Network 확인
3. published 2행 확인
4. unpublished slug가 DOM/응답에 없는지 확인
5. key 종류 재확인
6. Security Advisor와 policy 목록 확인

---

## 다음 주 질문

공개 읽기에서 개인 CRUD로 바뀌면 무엇이 추가되는가?

- Auth session과 JWT
- `owner_id`
- `to authenticated`
- `using (auth.uid() = owner_id)`
- `with check (auth.uid() = owner_id)`
- 본인/타인 계정 교차 검증
