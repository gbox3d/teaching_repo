# 12주차 — 영속 CRUD와 관계 기능

## 주간 목표

- 핵심 엔터티의 create/read/update/delete를 한 흐름으로 연결한다.
- UI, 상태, Data API 호출의 책임을 나눈다.
- 댓글·즐겨찾기·이력 중 관계 기능 하나를 FK와 RLS로 구현한다.
- unauthorized, not-found, network error를 서로 다른 상태로 표현한다.

## 1일차 — 핵심 엔터티 전체 CRUD

| 구간 | 내용 |
|---|---|
| 설명·시연 30분 | 목록-상세-작성-편집 흐름, service/UI 경계, 재조회 전략 |
| 직접 해결 60분 | 게시글 전체 CRUD, 소유자 UI, not-found와 오류 상태 |

## 2일차 — 관계 엔터티 통합

| 구간 | 내용 |
|---|---|
| 설명·시연 30분 | FK, cascade/restrict, 댓글 소유권, 관계별 policy |
| 직접 해결 60분 | 댓글 create/read/delete, 타인 삭제 공격 테스트, release candidate |

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습지](lab.md)
- [예제](examples/)

## 완료 기준

- 핵심 엔터티의 전체 CRUD가 공개 URL에서 재현된다.
- 관계 엔터티 하나가 핵심 row와 FK로 연결된다.
- 본인과 타인의 수정·삭제 권한이 DB policy로 구분된다.
- loading, empty, validation, unauthorized, not-found, network error가 구분된다.

## 확장 주제

- 낙관적 갱신과 재조회 중 어떤 전략이 초급 프로젝트에 적합한가?
- 게시글 삭제 시 댓글을 cascade로 지울 것인가, 보존할 것인가?
- 페이지네이션을 offset 방식과 cursor 방식 중 무엇으로 설계할까?
