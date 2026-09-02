# 10주차 실습 — RLS가 적용된 공개 데이터 읽기

수업용 별도 Supabase project를 사용한다. 실제 서비스·타인의 project에 SQL을 실행하지 않는다. browser config에는 project URL과 publishable key만 입력한다.

## 1일차 60분 — schema·grant·RLS 재현

### 문제

[schema.sql](examples/sql/schema.sql)을 실행해 공개 읽기 전용 `course_posts`를 만든다. SQL Editor에서는 seed 3행, unauthenticated Data API에서는 published 2행만 보이도록 만들고 그 차이를 설명한다.

### 시간 상자

| 시간 | 활동 | 검증 |
|---:|---|---|
| 0–7분 | 실습 project 확인·기대 작성 | project ref, 예상 3/2 |
| 7–20분 | schema/constraint/seed 실행 | 관리자 3행 |
| 20–30분 | RLS/grant/policy 확인 | catalog 조회 |
| 30–39분 | 전체 SQL 재실행 | 여전히 3행 |
| 39–50분 | starter config·anon 읽기 | 공개 2행 |
| 50–57분 | policy 조건 관찰 | unpublished 숨김 |
| 57–60분 | commit·증거 | SQL/Network |

### 실행 순서

1. Supabase Dashboard에서 이번 수업용 project인지 다시 확인한다.
2. SQL Editor에 `schema.sql` 전체를 붙여 넣고 실행한다.
3. 마지막 결과가 3행인지 확인한다.
4. 같은 SQL을 다시 실행하고 slug별 한 행만 있는지 확인한다.
5. `verify.sql`로 RLS, policy, table privilege를 조회한다.
6. starter의 placeholder를 project URL/publishable key로 바꾼다.
7. browser에서 published 2행을 확인한다.

### 단계별 힌트

**힌트 1 — 중복 seed:** 자동 id가 아니라 unique `slug`를 conflict target으로 사용한다.

**힌트 2 — 두 보안 층:** `has_table_privilege('anon', ..., 'SELECT')`와 `pg_policies`는 서로 다른 사실을 보여 준다.

**힌트 3 — 3 vs 2:** SQL Editor 관리 조회는 RLS를 우회할 수 있고, unauthenticated browser 요청은 `anon` policy를 적용받는다.

### 검증

- [ ] `course_posts`에 PK, unique slug, 길이 constraint가 있다.
- [ ] RLS가 enabled이다.
- [ ] `anon`/`authenticated`에는 SELECT만 부여했다.
- [ ] SELECT policy는 `is_published = true` 조건이다.
- [ ] SQL을 두 번 실행해도 slug가 중복되지 않는다.
- [ ] SQL Editor 3행, browser 2행이다.
- [ ] unpublished 제목/slug가 browser DOM과 API response에 없다.

### 실패 경로

policy 이름을 삭제하거나 권한을 확대하지 말고, starter에서 table 이름을 임시로 `course_post_typo`로 바꿔 오류를 관찰한 뒤 되돌린다. Console의 error code/message와 Network status를 기록한다.

## 2일차 60분 — project data source 교체

### 문제

9주차 project에서 UI contract를 유지하고 static JSON data source를 Supabase SELECT로 교체한다. 설정 누락, loading, empty, success, error 상태를 제공하고 Pages에서도 같은 공개 행을 확인한다.

### 시간 상자

| 시간 | 활동 | 검증 |
|---:|---|---|
| 0–8분 | contract/field mapping | 기존 UI와 SQL column |
| 8–20분 | client·config 연결 | publishable prefix |
| 20–34분 | SELECT·정렬 | data/error |
| 34–44분 | 다섯 UI 상태 | 단일 상태 |
| 44–52분 | 오류 재현·복구 | URL/table 오타 |
| 52–58분 | Pages 새 탭 검증 | Network/2행 |
| 58–60분 | commit | 비밀값 검색 |

### 필수 요구사항

- `config.js`에는 project URL과 publishable key만 둔다.
- placeholder가 남으면 요청하지 않고 setup 안내를 보인다.
- data module이 `course_posts` SELECT와 error 변환을 담당한다.
- 필요한 column만 명시적으로 선택한다.
- UI module은 Supabase URL, key, query builder를 모른다.
- setup/loading/empty/success/error 중 하나만 표시한다.
- Network 또는 query error의 원인은 Console에 남기고, 사용자는 재시도할 수 있다.
- Pages에서 unpublished row가 노출되지 않는다.
- repository 전체에 secret, service-role key, DB password가 없다.

### 단계별 힌트

**힌트 1:** 9주차 `listItems()`의 반환 field와 SQL column을 표로 매핑하고 UI를 먼저 바꾸지 않는다.

**힌트 2:** Supabase query는 throw 대신 `{ data, error }`를 반환할 수 있으므로 `if (error) throw ...` 경계를 data module에 둔다.

**힌트 3:** empty를 시험하려면 seed의 published 값을 영구 변경하지 말고, 임시 query 조건을 존재하지 않는 slug로 좁혔다가 되돌린다.

### 상태 검증

| 상태 | 재현 | 기대 |
|---|---|---|
| setup | placeholder | 설정 안내, 요청 없음 |
| loading | Network throttling | 진행 안내, 이전 목록 제거 |
| success | 정상 config/query | 공개 2행 |
| empty | 없는 slug 조건 | 오류 아닌 empty |
| error | table 이름 오타 | 사용자 안내 + Console 원인 |

- [ ] error를 복구한 뒤 새로고침 없이 재시도할 수 있다.
- [ ] 공개 URL의 source에서 publishable key 이외 credential이 없다.
- [ ] client-side `.eq()`를 보호 정책 자체라고 설명하지 않는다.

## 제출 증거

- schema와 policy SQL commit
- SQL Editor 3행 결과
- browser 2행과 Network request
- empty 또는 error 한 상태와 복구 화면
- Pages URL과 마지막 commit
- “grant와 RLS의 차이” 각 한 문장

## 확장 주제

1. query에 `limit`, pagination을 추가하고 index 필요성을 토론한다.
2. `AbortController` 또는 최신 요청 id로 연속 query 경쟁을 방어한다.
3. Supabase generated TypeScript types가 data contract 오류를 줄이는 방식을 조사한다.
4. static JSON fallback이 stale data를 보여 줄 위험과 적용 조건을 논의한다.
5. 11주차 owner CRUD를 위해 `owner_id` migration과 정책 testcase만 설계한다.
