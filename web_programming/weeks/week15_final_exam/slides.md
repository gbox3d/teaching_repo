---
marp: true
theme: default
paginate: true
title: 15주차 기말 개인 실기
---

# 15주차

## 기말 개인 실기

완성품보다 읽기·수정·검증·설명 능력을 확인한다.

---

# 평가 구조

- 구현 15점
- 시연 5점

구현:

- JavaScript·DOM·module 4
- 비동기·오류 3
- Auth·session 2
- CRUD·RLS 5
- 제출·commit 1

---

# 허용 자료

- 강의 자료
- 본인 노트
- 지정 공식 문서

금지:

- 생성형 AI
- 메신저·타인 대화
- 타 학생 코드
- 미허용 저장소·답안

---

# 제출 증거

- LMS 압축본
- 최종 commit SHA
- 실행 URL 또는 로컬 실행
- 요구 기능 체크
- 시연 결과

Pages 장애보다 마감 압축본과 commit을 먼저 고정한다.

---

# 1일차: 문제 읽기

1. 입력
2. 기대 출력
3. 정상 조건
4. 실패·경계 조건
5. 수정 가능한 파일
6. 완료 증거

코드를 쓰기 전에 요구를 체크리스트로 바꾼다.

---

# starter 읽기

- index.html: DOM contract
- styles.css: 상태 표현
- data/service module: 데이터 경계
- app.js: event와 render
- TODO: 구현 위치

먼저 실행하고 현재 동작을 기록한다.

---

# 구현 순서

1. 앱이 계속 실행되는 최소 변경
2. 핵심 정상 흐름
3. validation
4. 비동기·오류
5. Auth·RLS
6. commit·재실행

---

# 막혔을 때

- Console 첫 오류
- Network 요청·status
- 현재 session
- 입력과 실제 query
- DOM selector
- 변경 전후 diff

무작정 다시 쓰기보다 증거로 범위를 줄인다.

---

# 1일차 종료

- 중간 commit
- 동작 항목 표시
- 실패 항목과 관찰 증거 기록
- 비밀·개인정보 없는지 확인

---

# 2일차: 권한 확인

- 현재 사용자는 누구인가?
- 대상 row owner는 누구인가?
- UI가 아니라 DB가 막는가?
- 실패 뒤 DB가 그대로인가?
- owner_id를 바꾸려 하면 어떻게 되는가?

---

# 시연 5점

- 정상·실패 시나리오 2
- 함수·데이터·권한 흐름 설명
- 작은 지정 수정 또는 디버깅

암기한 발표보다 현재 코드를 따라 설명한다.

---

# 현장 수정 예시

- filter 조건 하나 변경
- validation 경계 변경
- 오류 문구·retry 연결
- 지정 함수 책임 설명
- policy 조건의 결과 예측

실제 시험 값은 별도로 제공한다.

---

# 장애 절차

- 전체 네트워크 장애: 시간 기록·공통 보정
- Pages 장애: LMS 압축본·local 실행
- Supabase 장애: mock service로 프런트 확인 후 보완 시연
- 개인 PC 장애: 감독 확인 후 예비 PC와 저장본 사용

---

# 최종 5분

- 파일 저장
- 테스트 1회
- git status/diff
- 최종 commit
- SHA 기록
- 압축본 확인
- 제출 완료 화면 확인

---

# 시험의 핵심

> 무엇을 바꿨는지

> 왜 그렇게 동작하는지

> 실패를 어떻게 확인했는지

세 가지를 코드와 실행 결과로 연결한다.
