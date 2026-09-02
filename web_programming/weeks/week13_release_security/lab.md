# 13주차 실습 — release audit

## 1일차 60분 — 보안 audit

### 문제

프로젝트를 공격자 관점에서 검사하고 발견한 결함을 수정·재검증하시오.

### 단계

1. 0~10분: 공개 파일에서 secret pattern과 개인정보를 검색한다.
2. 10~20분: 사용자 입력을 HTML·URL·속성에 넣는 위치를 찾는다.
3. 20~35분: 익명/A/B로 select·insert·update·delete를 우회 요청한다.
4. 35~45분: logout, 사용자 전환, session 만료 가정 상태를 검사한다.
5. 45~55분: offline과 오류 메시지를 검사한다.
6. 55~60분: 발견-수정-재검증 commit을 연결한다.

### 완료 조건

- secret과 실제 개인정보가 공개 파일에 없다.
- 입력이 기본적으로 textContent 또는 안전한 DOM API로 출력된다.
- 타 사용자와 익명의 금지 요청이 DB에서 거부된다.
- 로그아웃 후 이전 사용자 데이터가 남지 않는다.

### 힌트

1. examples/release-check.mjs를 프로젝트 경로에 실행한다.
2. rg 또는 VS Code 검색으로 innerHTML, insertAdjacentHTML, localStorage, console.log를 찾는다.
3. UI 버튼을 숨기는 테스트가 아니라 직접 Data API 요청을 만든다.

## 2일차 60분 — 접근성·재현성 audit

### 단계

1. 0~10분: 키보드만으로 로그인-작성-수정-삭제를 수행한다.
2. 10~20분: label, heading, alt, button/link 역할과 focus를 확인한다.
3. 20~30분: 375px과 1280px에서 overflow와 읽기 순서를 확인한다.
4. 30~40분: 새 browser profile에서 release 후보를 실행한다.
5. 40~50분: README, SQL, 테스트 표, 출처·AI 기록을 보완한다.
6. 50~60분: release tag를 만들고 5분 발표를 rehearsal한다.

### 완료 조건

- 키보드 핵심 시나리오를 끝까지 수행한다.
- validation·오류 상태가 색 이외의 방법으로 전달된다.
- 새 환경에서 README와 SQL로 실행을 재현한다.
- release tag가 채점 기준 commit을 가리킨다.

## 테스트 기록

examples/test_matrix.md를 복사해 각 항목에 예상·실제·증거·수정 commit을 기록한다.

## 확장 문제

1. 간단한 Content-Security-Policy meta를 적용하고 깨지는 리소스를 설명한다.
2. release-check.mjs에 금지 파일명과 최대 파일 크기 검사를 추가한다.
3. 발표 직전에 장애가 발생했을 때 mock JSON으로 시연할 fallback을 만든다.

## 제출

- release tag와 SHA
- 채운 테스트 표
- release-check 결과
- 보안·접근성 수정 commit
- 알려진 결함 목록
