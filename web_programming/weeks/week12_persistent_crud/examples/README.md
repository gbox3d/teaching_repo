# Week 12 example

이 예제는 UI와 Data API 호출을 분리한 최소 게시글·댓글 앱이다.

## 실행

1. 학생 Supabase 프로젝트에서 schema.sql을 실행한다.
2. config.js에 프로젝트 URL과 publishable key를 넣는다.
3. 로컬 정적 서버로 index.html을 연다.
4. Week 11에서 만든 사용자 A/B로 로그인해 교차 검증한다.

## 책임

- app.js: DOM, 현재 선택, loading과 사용자 메시지
- postService.js: posts query
- commentService.js: comments query
- api.js: Supabase client 한 개 생성
- schema.sql: 관계·grants·RLS

## 도전

app.js의 refresh 함수가 너무 많은 책임을 갖는지 표시하고, 상태와 렌더링을 한 단계 더 분리해 본다.
