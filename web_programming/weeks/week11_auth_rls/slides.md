---
marp: true
theme: default
paginate: true
title: 11주차 Auth와 소유자 RLS
---

# 11주차

## Auth와 소유자 RLS

인증된 사용자와 허용된 행동은 같은 말이 아니다.

---

# 이번 주 완료 조건

- 가입·로그인·로그아웃
- 새로고침 후 session 복구
- 본인 글 작성·수정·삭제
- 타 사용자 변경 요청 거부
- 익명/A/B 권한 행렬

---

# 1일차: 인증이 답하는 질문

> 지금 요청한 사용자는 누구인가?

- email/password는 신원 확인 수단
- session에는 access token과 갱신 정보가 있다
- Supabase client가 로그인 사용자의 JWT를 요청에 함께 보낸다

---

# 인증 상태의 네 장면

1. 앱 시작: session 확인 중
2. 비로그인: 로그인 form
3. 로그인: 사용자 정보와 작성 form
4. 로그아웃: 민감한 UI와 로컬 상태 제거

loading을 생략하면 비로그인 화면이 잠깐 깜빡인다.

---

# 최소 인증 API

~~~js
await supabase.auth.signUp({ email, password });
await supabase.auth.signInWithPassword({ email, password });
await supabase.auth.signOut();

const { data } = await supabase.auth.getSession();
supabase.auth.onAuthStateChange((_event, session) => {
  renderAuth(session);
});
~~~

---

# 세션은 권한 그 자체가 아니다

- 로그인 성공: 사용자가 누구인지 확인
- DB policy: 그 사용자가 어느 row에 무엇을 할 수 있는지 판단
- 버튼 숨김: 편의 기능
- RLS: 우회할 수 없는 권한 강제

---

# 1일차 실습 문제

로그인 전후 UI를 상태 기반으로 바꾸시오.

- 새로고침 후 사용자 표시
- 오류 메시지를 form 가까이에 표시
- 로그아웃 후 작성 form 숨김
- 비밀번호를 로그·DOM·URL에 남기지 않기

---

# 2일차: 소유권 데이터

~~~sql
owner_id uuid not null
  references auth.users(id)
~~~

- row가 누구의 것인지 DB가 판단할 근거
- insert 때 현재 사용자와 owner_id 일치 확인
- update/delete 때 기존 row의 owner_id 확인

---

# USING과 WITH CHECK

- USING: 기존 row를 읽거나 변경 대상으로 선택해도 되는가?
- WITH CHECK: 새 row 또는 변경 결과가 허용되는가?

~~~sql
using ((select auth.uid()) = owner_id)
with check ((select auth.uid()) = owner_id)
~~~

---

# 최소 권한 정책

| 작업 | 익명 | 소유자 | 타 사용자 |
|---|---:|---:|---:|
| select | 설계에 따라 | 허용 | 설계에 따라 |
| insert | 거부 | 허용 | 해당 없음 |
| update | 거부 | 허용 | 거부 |
| delete | 거부 | 허용 | 거부 |

먼저 표를 정하고 policy를 작성한다.

---

# 실패도 성공적인 테스트다

타 사용자 update가 다음처럼 끝나야 한다.

- 변경된 row 수 0
- 또는 권한 오류
- DB 내용은 그대로
- UI는 unauthorized 상태 안내

버튼을 숨긴 화면만 보고 통과시키지 않는다.

---

# 공격자 관점 교차 검증

1. A가 글 작성
2. B가 A의 id로 update 시도
3. B가 delete 시도
4. 익명 요청 시도
5. dashboard에서 실제 row 확인

---

# 흔한 오류

- RLS를 켰지만 policy가 없음
- insert에 WITH CHECK 누락
- owner_id를 form 입력으로 신뢰
- secret key를 브라우저에 사용
- 사용자 전환 후 이전 데이터가 화면에 남음

---

# 확장 질문

- 공개 게시판의 select는 anon에게 허용할 것인가?
- soft delete는 누구에게 허용할 것인가?
- 관리자 기능은 브라우저 publishable key만으로 충분한가?
- 만료된 session에서 작성 중인 입력은 어떻게 보존할까?

---

# 이번 주 제출

- Auth 동작 영상
- 익명/A/B 권한 행렬
- policies.sql
- 성공 요청 2개와 실패 요청 2개의 Network 증거
- 마감 commit SHA
