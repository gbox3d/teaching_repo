# 13주차 — 보안·접근성·릴리스 점검

## 주간 목표

- 공개 브라우저 코드의 비밀 경계를 설명한다.
- XSS 입력, 타 사용자 권한, 만료 session과 network 실패를 재현한다.
- 키보드·focus·반응형·label을 관찰 가능한 기준으로 검사한다.
- schema/policy SQL, README, 출처와 테스트 증거를 포함한 release를 고정한다.

## 1일차 — 공격자 관점 보안 점검

| 구간 | 내용 |
|---|---|
| 설명·시연 30분 | publishable/secret 경계, XSS, RLS 우회 요청, session·로그 노출 |
| 직접 해결 60분 | secret scan, 악성 문자열, 익명/A/B, expired/offline 테스트 |

## 2일차 — 접근성·문서·릴리스

| 구간 | 내용 |
|---|---|
| 설명·시연 30분 | 키보드/focus/label/contrast, 재현 가능한 SQL과 release evidence |
| 직접 해결 60분 | 375px·1280px·키보드 점검, README 보완, tag와 발표 rehearsal |

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습지](lab.md)
- [예제와 점검 도구](examples/)

## 완료 기준

- 공개 저장소와 배포 파일에 secret이 없다.
- 익명/A/B의 권한 결과가 설계와 일치한다.
- 입력 문자열이 실행 가능한 HTML로 삽입되지 않는다.
- 키보드만으로 핵심 시나리오를 완료한다.
- release tag, 테스트 표, schema/policy SQL, 출처·AI 기록이 있다.

## 확장 주제

- CSP가 XSS 방어에서 맡는 역할
- 보안 오류를 사용자에게 얼마나 구체적으로 보여줄 것인가
- 자동 접근성 도구가 찾지 못하는 문제
- CI에서 secret scan·link check·format check를 자동화하는 방법
