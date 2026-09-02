# Week 11 example

## 실행

1. 학생 개인 Supabase 프로젝트의 SQL Editor에서 schema.sql을 실행한다.
2. config.js의 URL과 publishable key를 학생 프로젝트 값으로 바꾼다.
3. 로컬 정적 서버에서 이 폴더를 연다.
4. 사용자 A/B를 만들고 권한을 교차 테스트한다.

publishable key는 공개 클라이언트용 식별자이며 데이터 보호는 RLS가 담당한다. secret key, DB 비밀번호, legacy service_role key를 넣지 않는다.

## 관찰 순서

1. 비로그인 상태에서 글 목록만 읽는다.
2. A로 로그인해 글을 추가·수정·삭제한다.
3. A가 만든 글의 id를 기록한다.
4. B로 로그인해 같은 id의 update/delete 요청을 시도한다.
5. Network 응답과 DB row가 바뀌지 않았음을 확인한다.

## 파일

- index.html: 인증·게시글 UI
- app.js: Auth 상태와 CRUD 요청
- config.js: 공개 URL/publishable key 자리
- schema.sql: table, grants, RLS policies
- styles.css: 상태가 보이는 최소 스타일
