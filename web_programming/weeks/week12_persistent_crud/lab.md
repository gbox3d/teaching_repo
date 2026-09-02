# 12주차 실습 — full CRUD와 관계 기능

## 1일차 60분 — 핵심 엔터티

### 문제

게시글 목록·상세·작성·수정·삭제를 하나의 사용자 흐름으로 완성하시오.

### 단계

1. 0~10분: 현재 코드의 UI/service 책임을 표시한다.
2. 10~25분: create와 목록 재조회를 완성한다.
3. 25~40분: 소유자 update/delete를 완성한다.
4. 40~50분: 빈 제목, 존재하지 않는 id, 타 사용자 id를 검증한다.
5. 50~60분: loading·버튼 복구·commit·회고를 정리한다.

### 완료 조건

- mutation 동안 중복 submit을 막는다.
- 성공 뒤 DB 값을 다시 읽어 화면과 일치시킨다.
- 타 사용자의 변경 요청은 실패한다.
- 존재하지 않는 id에 안전한 메시지가 표시된다.

### 힌트

1. service 함수는 data/error를 반환하고 DOM을 직접 찾지 않는다.
2. UI 함수의 finally에서 버튼 상태를 복구한다.
3. update/delete 후 영향을 받은 row와 재조회 결과를 확인한다.

## 2일차 60분 — 댓글 관계

### 문제

게시글에 댓글 create/read/delete를 추가하고 FK와 댓글 소유자 RLS를 검증하시오.

### 단계

1. 0~10분: 관계와 삭제 규칙을 그림으로 결정한다.
2. 10~20분: comments table, FK, grants, policies를 작성한다.
3. 20~35분: 선택한 post의 댓글 목록과 작성 form을 연결한다.
4. 35~45분: 본인 댓글 삭제와 타 사용자 삭제 실패를 확인한다.
5. 45~55분: 게시글 삭제 후 댓글 결과와 offline을 확인한다.
6. 55~60분: release candidate tag와 남은 결함을 기록한다.

### 완료 조건

- 존재하지 않는 post_id에 댓글을 만들 수 없다.
- 비로그인 사용자는 댓글을 작성하지 못한다.
- 댓글 작성자만 자신의 댓글을 삭제한다.
- 게시글 삭제 정책의 결과가 설계와 일치한다.

### 힌트

1. comments.post_id는 posts.id를 참조한다.
2. 댓글 insert의 WITH CHECK는 auth.uid()와 owner_id를 비교한다.
3. 댓글 삭제 policy는 게시글 owner가 아니라 댓글 owner를 먼저 생각한다.

## 확장 문제

1. 한 사용자가 게시글 하나에 좋아요를 한 번만 누르게 unique(post_id, owner_id)를 설계한다.
2. 게시글 목록에 댓글 수를 표시할 때 발생하는 요청 수를 센다.
3. 삭제 대신 deleted_at을 기록하는 soft delete를 설계하고 읽기 policy를 수정한다.

## 제출

- 공개 URL과 release candidate SHA/tag
- schema.sql과 policies.sql
- six-state 테스트 표
- 남은 결함 3개 이하와 수정 계획
