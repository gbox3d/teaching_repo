---
marp: true
theme: default
paginate: true
title: 13주차 보안 접근성 릴리스
---

# 13주차

## 보안·접근성·릴리스 점검

새 기능을 멈추고 실패를 찾아내는 주간

---

# 이번 주 완료 조건

- secret 없음
- 익명/A/B RLS 검증
- 안전한 입력 출력
- 키보드와 반응형 점검
- 재현 가능한 SQL·README
- release tag

---

# 1일차: 공개 브라우저의 경계

브라우저에 전달된 값은 사용자가 볼 수 있다.

- HTML/JS source
- Network 요청
- localStorage/sessionStorage
- source map
- 빌드 시 주입된 환경 값

숨겨 보이는 것과 비밀인 것은 다르다.

---

# 공개 가능한 key와 금지 key

- publishable key: 브라우저용 프로젝트 식별자
- secret key: 서버 전용, RLS 우회 가능
- legacy service_role: 서버 전용, 브라우저 금지

publishable key가 안전하려면 RLS와 최소 권한이 함께 있어야 한다.

---

# XSS의 핵심

사용자 입력을 코드로 해석하면 안 된다.

~~~js
output.textContent = userInput; // 기본
output.innerHTML = userInput;   // 신뢰 경계 검토 필요
~~~

HTML이 꼭 필요하면 허용 목록 기반 sanitization을 별도 설계한다.

---

# RLS 공격 테스트

화면이 아니라 요청을 공격한다.

1. 타 사용자 row id 확보
2. 직접 update/delete 요청
3. 필드 owner_id 변경 시도
4. 익명 요청
5. DB 결과 확인

---

# session과 오류 로그

- token 전체를 Console에 출력하지 않기
- 오류 메시지에 내부 schema·query 노출하지 않기
- logout 뒤 사용자별 캐시 제거
- 만료 session에서 재로그인 경로 제공

---

# 1일차 실습 문제

프로젝트를 공격자 관점에서 검사하시오.

- secret pattern
- HTML 입력
- 익명/A/B
- offline
- session 전환

실패한 항목은 숨기지 말고 issue로 기록한다.

---

# 2일차: 접근성은 관찰 가능한 동작

- label과 입력 연결
- 논리적 heading
- 키보드 순서
- visible focus
- button/link 역할
- alt
- 375px·1280px에서 가로 스크롤 없음

---

# 자동 점검의 한계

도구는 빠른 출발점이다.

- 자동: 누락 label, contrast 일부, 문법
- 수동: 의미, 읽는 순서, 오류 이해, 실제 키보드 흐름

도구 점수 하나를 목표로 삼지 않는다.

---

# 재현 가능한 release

release에는 다음이 있어야 한다.

- commit SHA/tag
- 실행·배포 절차
- schema/seed/policies SQL
- 권한·오류 테스트 표
- 자산·코드·AI 출처
- 알려진 결함

---

# 완료의 정의

> 내 PC에서 한 번 됨

이 아니라

> 새 환경에서 같은 commit을 열고, 같은 절차로, 정상·실패 시나리오를 재현할 수 있음

---

# 2일차 실습 문제

키보드·375px·1280px·offline·A/B 시나리오를 수행하고 release candidate를 고정하시오.

---

# 확장 주제

- Content Security Policy
- dependency·supply-chain 위험
- CI secret scanning
- automated accessibility test
- privacy와 학기 종료 후 데이터 삭제

---

# 이번 주 제출

- release tag/SHA
- 테스트 표
- 보안·접근성 수정 commit
- schema/policies SQL
- README와 출처·AI 기록
- 발표 시나리오
