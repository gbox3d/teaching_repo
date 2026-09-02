---
marp: true
theme: default
paginate: true
title: 12주차 영속 CRUD와 관계 기능
---

# 12주차

## 영속 CRUD와 관계 기능

기능을 늘리기보다 하나의 흐름을 끝까지 완성한다.

---

# 이번 주 완료 조건

- 핵심 엔터티 full CRUD
- 관계 엔터티 create/read/delete
- 소유자 RLS
- six states
- release candidate

---

# 1일차: 화면이 아니라 흐름

목록 → 상세 → 작성 → 수정 → 삭제 → 목록

각 단계에서 확인할 것:

- 현재 사용자
- 대상 row id
- loading
- 성공 후 이동·재조회
- 실패 상태

---

# UI와 service의 책임

| UI | service |
|---|---|
| 입력 읽기 | Data API 호출 |
| loading 표시 | query 구성 |
| 결과 렌더링 | data/error 반환 |
| 사용자 메시지 | DB 세부 정보 캡슐화 |

한 함수가 DOM과 query를 모두 다루면 테스트와 변경이 어려워진다.

---

# 안전한 갱신 순서

초급 프로젝트의 기본:

1. 버튼 잠금
2. API 요청
3. 오류 확인
4. DB에서 재조회
5. 화면 갱신
6. 버튼 복구

정확성을 먼저 확보한 뒤 낙관적 갱신을 확장한다.

---

# not-found와 unauthorized

- not-found: 해당 id의 row가 없거나 읽을 수 없음
- unauthorized: 로그인·소유권 조건을 충족하지 않음
- 보안상 서버 응답이 둘을 의도적으로 구분하지 않을 수도 있음

사용자 메시지와 개발자 진단 정보를 분리한다.

---

# update에서 빠뜨리기 쉬운 것

- 빈 문자열 validation
- 타 사용자 row id
- owner_id 변경 시도
- 중복 submit
- 수정 후 stale 화면
- Network 실패 뒤 버튼 복구

---

# 1일차 실습 문제

게시글의 목록·상세·작성·수정·삭제를 완성하시오.

정상 시나리오 하나와 실패 시나리오 두 개를 반드시 기록한다.

---

# 2일차: 관계를 모델링한다

~~~text
posts 1 ───── N comments
  id              post_id
                  owner_id
                  body
~~~

FK는 존재하는 게시글에만 댓글이 연결되게 한다.

---

# 삭제 규칙을 선택한다

- on delete cascade: 게시글과 댓글을 함께 제거
- on delete restrict: 댓글이 있으면 게시글 삭제 거부
- soft delete: row는 남기고 삭제 상태 표시

수업 기본안은 cascade, 보고서에는 선택 이유를 기록한다.

---

# 관계마다 권한을 다시 설계

게시글 소유자가 다른 사람의 댓글을 지울 수 있는가?

기본안:

- 댓글 읽기: 공개
- 댓글 작성: 로그인 사용자
- 댓글 삭제: 댓글 작성자
- 게시글 소유자의 관리 권한: 선택 확장

---

# six states

1. loading
2. empty
3. validation
4. unauthorized
5. not-found
6. network error

상태는 CSS class 하나가 아니라 재현 가능한 테스트 시나리오다.

---

# 2일차 실습 문제

댓글 create/read/delete를 추가하시오.

- FK 위반
- 비로그인 작성
- 타 사용자 삭제
- 게시글 삭제 뒤 댓글

각 결과를 예측한 후 실행한다.

---

# 확장 주제

- 좋아요의 중복 방지 unique key
- 댓글 수 집계와 N+1 요청
- pagination
- Realtime
- soft delete와 감사 기록

---

# 이번 주 제출

- release candidate URL
- schema/policies SQL
- 정상·실패 테스트 표
- core CRUD + relation 기능 영상
- 남은 결함과 13주차 수정 계획
