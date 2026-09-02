# 9주차 — 1차 과제와 풀스택 설계

중간까지 만든 정적 페이지를 데이터·인증·권한이 있는 프로젝트로 확장하기 전에, 기능 목록을 사용자 흐름·데이터 모델·실행 경계로 번역한다. 이번 주 산출물은 크게 보이는 아이디어가 아니라 10–14주차에 실제로 완성 가능한 작은 설계와 실행 가능한 walking skeleton이다.

## 학습 목표

1. UI, browser state, static asset, Supabase, 선택적 server API의 책임을 구분한다.
2. 사용자 이야기와 acceptance scenario를 정상·경계·오류 경로로 작성한다.
3. 핵심 entity와 관계, 소유자, 공개 범위를 데이터 표로 표현한다.
4. loading·empty·validation·unauthorized·not-found·network error를 설계에 포함한다.
5. 가장 위험한 경로 하나를 mock data로 처음부터 끝까지 실행한다.
6. 발표 5점·보고서 5점의 근거를 재현 가능한 링크와 diagram으로 제출한다.

## 수업 흐름

| 일차 | 설명·시연 30분 | 직접 해결 실습 60분 |
|---|---|---|
| 1일차 | 정적/동적 책임, 신뢰 경계, 데이터 흐름 | 문제 정의·사용자 흐름·데이터/상태 설계 |
| 2일차 | scope, walking skeleton, 계약과 증거 | 실행 골격·architecture 문서·3분 발표 |

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [두 차시 실습](lab.md)
- [1차 과제 안내](project_brief.md)
- [발표·보고서 채점표](rubric.md)
- [예제 안내](examples/README.md)
- [프로젝트 starter](examples/project-starter/index.html)

## 완료 기준

- 핵심 사용자 한 명과 해결할 문제 한 문장을 정했다.
- 필수 entity, owner, 관계 하나를 표로 설명한다.
- 정적 JSON, browser, Supabase, server 중 각 책임을 근거와 함께 배치한다.
- 최소 여섯 UI 상태의 발생 조건·표시·복구 행동을 적었다.
- mock data 기반 핵심 흐름이 로컬 HTTP 서버에서 실행된다.
- repository/Pages URL, architecture 문서, 발표·보고서가 서로 같은 범위를 가리킨다.

## 다음 주 연결

10주차에는 mock data source를 Supabase의 공개 읽기 테이블로 교체한다. 11주차 Auth·소유자 RLS 전까지 개인 쓰기 기능을 공개 정책으로 임시 개방하지 않는다.
