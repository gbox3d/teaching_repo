# 11주차 실습 — Auth와 소유자 RLS

## 공통 준비

1. [예제 폴더](examples/)의 README를 읽는다.
2. 학생별 Supabase 프로젝트에 schema.sql을 실행한다.
3. config.js의 URL과 publishable key만 바꾼다.
4. 사용자 A와 B는 수업용 가상 이메일로 만든다.

## 1일차 60분 — 인증 상태 UI

### 문제

가입·로그인·로그아웃과 session 복구를 구현하고 로그인 상태에 따라 화면을 바꾸시오.

### 시간 권장

- 0~15분: sign-up/sign-in form 연결
- 15~30분: 초기 getSession과 사용자 표시
- 30~45분: onAuthStateChange와 sign-out
- 45~55분: 잘못된 비밀번호·offline 오류
- 55~60분: commit과 짧은 회고

### 완료 조건

- 새로고침 후 로그인 사용자 이메일이 표시된다.
- 비로그인 상태에서는 작성 form이 보이지 않는다.
- 로그아웃하면 이전 사용자 데이터와 메시지가 정리된다.
- 비밀번호가 URL, Console, DOM에 노출되지 않는다.

### 단계별 힌트

1. submit 이벤트에서 preventDefault를 먼저 확인한다.
2. 앱 시작 시 getSession 결과를 renderAuth에 전달한다.
3. 가입·로그인 함수마다 UI를 직접 중복 수정하지 말고 auth state listener에서 한 번 처리한다.

### 검증

정상 로그인, 잘못된 비밀번호, 새로고침, 로그아웃, DevTools offline을 각각 기록한다.

## 2일차 60분 — 소유자 RLS 공격 테스트

### 문제

A가 작성한 글을 A만 수정·삭제할 수 있게 policy를 완성하고 B의 우회 요청이 실패함을 증명하시오.

### 시간 권장

- 0~10분: 익명/A/B 권한 행렬 작성
- 10~25분: insert/update/delete policy 작성
- 25~40분: 앱에서 본인 CRUD
- 40~50분: B와 익명 공격 요청
- 50~60분: 결과 표·commit·회고

### 완료 조건

- insert의 owner_id는 현재 로그인 사용자 ID다.
- A의 update/delete는 성공한다.
- B가 A의 row id를 알아도 update/delete하지 못한다.
- RLS를 잠시 끄는 방식으로 문제를 회피하지 않는다.

### 단계별 힌트

1. insert policy에는 WITH CHECK가 필요하다.
2. update policy는 기존 row와 변경 결과를 모두 생각한다.
3. UI에서 버튼을 숨긴 결과가 아니라 Data API 응답과 DB row를 확인한다.

### 권한 기록표

| 주체 | select | insert | update own | update other | delete own | delete other |
|---|---|---|---|---|---|---|
| 익명 |  |  | 해당 없음 |  | 해당 없음 |  |
| A |  |  |  |  |  |  |
| B |  |  |  |  |  |  |

## 확장 문제

1. 공개 읽기를 허용하되 작성은 로그인 사용자만 허용한다.
2. session이 만료되면 작성 중인 내용을 localStorage에 임시 보존한다.
3. 공개 이름은 별도 profiles table에 두고 auth.users의 이메일을 게시물에 노출하지 않는다.

## 제출

- Pages 또는 로컬 실행 URL
- policies.sql
- 채운 권한 행렬
- 정상 2건·거부 2건의 증거
- 마감 commit SHA
