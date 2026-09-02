# 기말 실기 blueprint

## 평가 계약

학기별 실제 문제는 아래 범주에서 조합하되 공개 blueprint와 같은 점수·난도를 유지한다.

| 범주 | 점수 | 문제 형태 예시 |
|---|---:|---|
| JavaScript·DOM·module | 4 | 데이터 변환, render, event, module 경계 변경 |
| 비동기·오류 | 3 | loading, HTTP/network failure, retry |
| Auth·session | 2 | 로그인 상태, session 복구, 보호 UI |
| CRUD·RLS | 5 | 지정 mutation, owner/other 정책과 검증 |
| 제출·commit | 1 | 실행 가능한 기준본과 SHA |
| 정상·실패 시연 | 2 | 지정 두 시나리오 |
| 흐름 설명 | 1.5 | 함수·데이터·권한 설명 |
| 현장 수정·디버깅 | 1.5 | 작은 변경 또는 원인 분리 |

## 문제 작성 원칙

- 새 라이브러리 학습을 요구하지 않는다.
- 한 오류가 뒤의 모든 문항을 막지 않게 독립성을 확보한다.
- 정상 경로만으로 만점을 받을 수 없게 실패·권한 증거를 포함한다.
- 실제 계정·개인정보·secret을 배포본에 넣지 않는다.
- A/B형은 값과 화면 주제만 바꾸지 말고 같은 학습성과·단계 수를 유지한다.

## 사전 파일럿

- 새 PC와 새 browser profile
- local starter
- Git·LMS 제출
- mock fallback
- Supabase Auth/RLS
- 네트워크 차단
- 제한시간 내 강의자 기준 풀이
