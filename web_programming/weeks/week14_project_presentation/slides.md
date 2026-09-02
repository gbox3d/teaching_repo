---
marp: true
theme: default
paginate: true
title: 14주차 최종 프로젝트 발표
---

# 14주차

## 최종 프로젝트 발표

기능을 나열하지 말고 설계와 증거를 보여준다.

---

# 평가 대상

- 공개 배포·세션 복구
- core CRUD + relation
- Auth와 RLS 교차 검증
- six states
- 반응형·키보드
- 설명·질의·현장 수정
- 보고서와 재현 자료

---

# 1일차: 5분 발표 구조

1. 문제와 사용자 — 30초
2. 핵심 정상 흐름 — 90초
3. Auth·RLS 권한 — 60초
4. 오류·접근성 — 60초
5. 구조·회고 — 60초

---

# 시작 30초

좋은 시작:

> 캠퍼스 장소를 저장하고 본인 기록만 수정하는 앱입니다.

피할 시작:

> HTML부터 만들었고 CSS도 했고 JavaScript도 했습니다.

---

# 정상 흐름 시연

- 새 browser/profile 또는 로그아웃 상태
- 로그인
- 핵심 row 작성
- 목록·상세
- 수정·삭제
- relation 기능

미리 준비된 데이터와 즉석 생성 데이터를 함께 사용한다.

---

# 권한 시연

A가 만든 row를 B가 바꾸려 한다.

- UI 버튼이 없음
- 직접 요청도 DB가 거부
- 실제 row 불변
- policy 근거 설명

---

# 오류·접근성 시연

화면 6개를 다 열지 말고 대표 둘을 고른다.

- empty 또는 validation
- unauthorized 또는 network error
- 키보드 focus
- 375px 반응형

---

# 구조 설명

한 장으로 답한다.

~~~text
GitHub Pages UI
   └─ supabase-js
       ├─ Auth
       └─ Data API → Postgres + RLS
~~~

---

# 질의에 답하는 방법

1. 질문을 짧게 다시 말한다.
2. 현재 구현 사실을 먼저 답한다.
3. 선택 이유와 tradeoff를 말한다.
4. 못 한 부분은 한계와 다음 조치를 말한다.

---

# rehearsal 점검

- 시간이 넘는가?
- 계정·seed가 준비됐는가?
- Network 실패를 재현할 수 있는가?
- 마감 commit에서 실행하는가?
- secret·개인정보가 화면에 보이지 않는가?

---

# 2일차: 발표 규칙

- 제출 순서와 타이머 준수
- 사전 영상·보고서는 fallback 증거
- 현장 시연은 마감 release 기준
- 다른 학생 발표 중 코드 수정 금지
- 장애 발생 시 증거를 기록하고 다음 순번 진행

---

# 무작위 지정 시나리오

- 로그아웃 뒤 보호 기능 접근
- B가 A의 row 수정
- empty table
- 잘못된 form
- offline fetch
- 375px 키보드 흐름

---

# 현장 수정 예시

- validation 길이 변경
- 정렬 방향 변경
- empty 문구 변경
- 지정 함수 이름·책임 설명
- policy의 USING/WITH CHECK 설명

새 기능 개발이 아니라 개인 이해 확인이다.

---

# 보고서 마지막 확인

- URL·tag/SHA
- 기능표
- ERD
- schema/policies SQL
- 권한·오류 테스트
- 자산·코드·AI 출처
- 알려진 한계와 회고

---

# 발표의 핵심

> 동작합니다

에서 끝나지 말고

> 어떤 조건에서 왜 동작하고, 어떤 조건에서는 어디에서 거부되는지 증명합니다
