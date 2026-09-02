# 10주차 예제

## 구성

- `sql/schema.sql`: table, constraint, RLS, 최소 grant, policy, seed
- `sql/verify.sql`: 적용 상태를 읽기 전용으로 확인
- `starter/`: publishable client의 공개 SELECT 예제

## 1. SQL

[SQL 안내](sql/README.md)를 읽고 수업용 Supabase project에서 `schema.sql`을 실행한다.

## 2. starter

`starter/js/config.js`에는 처음부터 placeholder만 들어 있다.

```js
export const SUPABASE_URL = "https://YOUR_PROJECT_REF.supabase.co";
export const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_REPLACE_ME";
```

두 값을 Dashboard의 project URL과 **Publishable key**로 교체한다. 다른 종류의 key나 connection string은 사용하지 않는다.

```bash
cd starter
python -m http.server 8000
```

`http://localhost:8000`을 연다. placeholder 상태에서도 setup 안내 화면은 실행되며, 실제 값이 있을 때만 Supabase client module과 Data API를 호출한다.

## 기대 결과

- SQL Editor: seed 3행
- 로그인하지 않은 browser: published 2행
- Reload: 같은 2행
- table 이름 오타: error와 Console 원인

공식 기준은 [API keys](https://supabase.com/docs/guides/getting-started/api-keys)와 [RLS](https://supabase.com/docs/guides/database/postgres/row-level-security)를 확인한다.
