# 12주차 구현·검증 보고

강의자의 C01 개편의 12주 담당 결과다. 12주 전체 폴더와 공통 API 설정 계약을 조사·수정했다. 다른 주차·API 서버 구현은 수정하지 않았다. 전역 빌드와 독립 심사는 총괄 단계이며 자체 점수를 부여하지 않는다.

## 차시와 원고 범위

| 차시 | 강의·시연 | 실습 | 수정·검증 |
|---|---|---|---|
| 12-1 | 준비 5·URL/헤더 10·about/help 15·JSON 복습 10·GET/await 15·안내 5 = 60분 | 설정 5·Send Request 8·BOOK_ID/limit 10·응답 7 = 30분 | about→help→GET을 README/lab/walkthrough/한영 슬라이드/예제 안내에 반영 |
| 12-2 | 준비 5·showList 15·response.ok 15·try/catch 10·재시도/조립 10·안내 5 = 60분 | URL/JSON/showList 12·오류/복구 10·캡처 8 = 30분 | 제공 틀 3곳만 필수 수정. 설정 패널·방어 코드는 제공 기능 |

한국어·영어 덱은 각각 기존 14장을 유지한다. 파일 준비는 사전, 업로드는 수업 뒤 정리다. 11주 필수는 폼 한 객체 저장·복원이며 전체 객체 배열 방명록은 제공 시연본으로 설명했다. JSON 단독 복습은 11주 ex05로 연결했다.

## 예제별 결과

| 예제 | 구현과 실행 확인 |
|---|---|
| ex01 | about 200, API 소개 배열 1개를 화면·실제 응답으로 확인 |
| ex02 | help 200, step 1~6 사용법 배열 확인 |
| ex03 | 자기 목록 GET, BOOK_ID와 limit 1/2/5 비교. 초기 데이터는 한 글이므로 모두 최대값 이하 |
| ex04 | 배열 목록 표시, 반복 조회 시 li 누적 없음 |
| ex05 | 정상 필드 200/true → 없는 필드 400/false → 정상 200 복구 |
| ex06 | Chrome Offline 실패 안내, 버튼 복구, 연결 복구 후 GET 200 |
| web-week12 | 초기 GET·재조회·빈 배열·401·잘못된 주소·Offline·복구·375/1280px 확인 |
| guestbook.local | 11주 수정본 인계, week11-guestbook-items 유지, 서버 조회 시 로컬 글 보존. 손상 JSON 안내 후 자기 키만 삭제하고 다른 키 보존 |

모든 REST 폴더에 README·requests.http·.env.example·.gitignore·api-settings.js를 배부했다. 브라우저 패널과 REST Client .env 설정은 별개다. 독립 폴더용 shared/examples.css 사본은 공통 스타일과 같은 내용이다. W3.CSS는 cdnjs 4.1.0 고정 CDN이다.

## HTTP 오류 재현 조정

기존 missing_table 요청은 로컬 API의 OPTIONS preflight에서 404가 나므로 브라우저에는 Failed to fetch가 보였다. 브라우저 비교는 정상 guestbook 경로의 select=missing_column으로 수정했다. 로컬 API는 400을 반환한다. PostgreSQL 42703(undefined_column)은 PostgREST의 기본 HTTP 400 매핑에 해당한다. [PostgreSQL 코드](https://www.postgresql.org/docs/current/errcodes-appendix.html), [PostgREST 매핑](https://docs.postgrest.org/en/stable/references/errors.html).

REST Client의 missing_table 404 예제는 유지하고 CORS 차이를 README에 설명했다. limit=0은 공용 서버에서 정상 빈 응답일 수 있으므로 오류 예제로 쓰지 않는다. 12주 담당은 공용 서버를 직접 호출하지 않았다. 총괄은 공용 서버의 about 200·1행, help 200·6행, select=missing_column 400·42703을 Node HTTP로 확인했다. [총괄 읽기 증거](live-read-checks.json). 이 결과는 브라우저 CORS 확인과 구분한다.

## 제공 설정과 요청 순서

공통 정본은 shared/api-settings.js이며 [설정 계약](api-settings-contract.md)을 먼저 확정해 13·14주에 전달했다. 실제 값은 추적 파일·localStorage·sessionStorage에 저장하지 않는다. 새로고침 후 로컬 기본값으로 돌아감을 브라우저에서 확인했다. 설정 파일의 사본 7개는 정본과 바이트 단위로 일치한다.

설정 변경 중 이전 GET이 늦게 끝나는 경우는 latestRequest/requestId로 보호한다. 새 요청만 목록·오류·버튼을 갱신한다. 실제 로컬 API 앞의 임시 지연 프록시로 이전/새 요청을 150/450ms와 450/100ms로 완료시켰다. 이전 finally가 새 요청 중 버튼을 켜지 않으며 마지막 렌더링은 새 태그의 id 2였다. 이 번호 비교는 제공 코드이며 학생 구현 범위에 넣지 않는다.

## 실행 증거와 정적 검사

실행 시각: 2026-11-18T10:43:31.807Z. API는 기존 guestbook-api/server.mjs의 createGuestbookServer와 임시 전용 데이터 디렉터리, 정적 서버는 8122 포트를 사용했다. 클라우드 쓰기는 수행하지 않았다. Chrome MCP는 이미 실행 중인 프로필 오류로 연결되지 않아 전용 사용자 데이터 폴더의 headless Chrome CDP로 대체했다. 다른 브라우저 프로필·설정은 변경하지 않았다.

- [브라우저·요청 기록](evidence/week12-browser.json): 예제 6개, 순서 경쟁, 완성본 화면 폭, .http의 24개 GET 요청, 로컬 보관본 검사. 총 34개 결과 항목.
- [375px 화면](evidence/week12-375.png) · [1280px 화면](evidence/week12-1280.png): 설정 패널·목록 줄바꿈·가로 넘침 없음 확인.
- [한영 슬라이드 렌더 기록](evidence/week12-slides.json): 설치된 Marp로 28장 렌더, 각 section의 scrollWidth/scrollHeight 넘침 없음.
- JS 전 파일 node --check 통과. UI·문서 한국어 문체 검사 통과.
- 82개 파일 중 텍스트 75개를 읽고 상대 링크·HTML 자산 경로 존재를 확인했다. 누락 0개.
- walkthrough의 완성 HTML·JS 코드 블록은 실파일과 정확히 일치한다. 한영 슬라이드의 모든 JS 발췌도 실제 파일의 연속 부분과 일치한다.

VS Code REST Client UI를 직접 누른 것으로 기록하지 않는다. requests.http의 GET URL·헤더를 .env.example 값으로 해석해 실제 로컬 API로 실행했다. 브라우저 GET은 실제 CORS preflight를 거쳤다. 두 검증을 구분한다.

## 자산 조사

PNG 7개를 직접 열어 확인했다. profile.png는 현재 홈에서 사용한다. project1/2/3.png와 ex04/picture.png는 이전 카드 그림이며 현재 REST 화면에서 참조하지 않으므로 안내에 용도를 적었다. site-map.svg의 세 실제 HTML 경로는 유효하다. home.png는 현재 홈 예시이며 guestbook.png는 오래된 폼 그림을 현재 로컬 서버 목록 화면으로 갱신했다. 배부 그림을 학생의 새 캡처로 인정하지 않는다.

## 한계와 총괄 인계

12주 담당은 공용 API 브라우저 요청·GitHub Pages·서로 다른 기기의 공유를 실행하지 않았다. 총괄의 별도 공용 Node HTTP 확인 범위는 위에 기록했다. 학생 30분 수행 시간도 실측하지 않았다. W3.CSS CDN 로딩은 검증 당시 성공했으며 오프라인 배포용 라이브러리 사본은 추가하지 않았다. 전체 npm build/check/test와 독립 심사는 총괄이 통합 후 수행한다. 11주 수정본 인계는 완료되어 추가 복사 대기는 없다. API 서버의 404 preflight 동작은 수정하지 않았다.

검증용 API 세션 46928(8787), 정적 서버 세션 59174(8122)는 총괄의 후속 확인을 위해 유지한다. 전용 headless Chrome과 지연 프록시는 검증 후 종료했다. 커밋·푸시는 하지 않았다.

## 총괄 추가 검증

공용 API의 브라우저 확인 과정에서 ex05의 두 번째 option 시작 태그가 닫는 태그로 작성된 오류를 발견해 고쳤다. 수정 후 실제 선택 메뉴로 `missing_column`을 선택했다. Chrome에서 localhost HTTP 페이지가 Supabase HTTPS에 about·help GET 200, 없는 필드 GET 400을 받고 화면에 상태를 표시함을 확인했다. 클라우드 쓰기는 하지 않았다. [공용 브라우저 읽기 기록](live-browser-read.json).

공통 CSS의 border-box 규칙을 7개 배부 사본에 반영했다. 위 세 예제는 API 설정을 펼친 상태에서도 375px 화면과 문서 폭이 일치했다. 이 추가 검증은 앞선 담당자의 로컬 검증과 구분한다.

## 전수 파일 목록

다음 목록의 텍스트는 읽기·링크·역할 확인 대상이고 PNG는 위의 직접 열기 대상이다. 경로는 week12_fetch_json 기준이다.

- `.`: `lab.md`, `README.md`, `slides.md`, `slides_en.md`, `walkthrough.md`
- `examples`: `README.md`
- `examples/day1/ex01`: `.env.example`, `.gitignore`, `api-settings.js`, `app.js`, `index.html`, `README.md`, `requests.http`
- `examples/day1/ex01/shared`: `examples.css`
- `examples/day1/ex02`: `.env.example`, `.gitignore`, `api-settings.js`, `app.js`, `config.example.js`, `index.html`, `README.md`, `requests.http`
- `examples/day1/ex02/shared`: `examples.css`
- `examples/day1/ex03`: `.env.example`, `.gitignore`, `api-settings.js`, `app.js`, `config.example.js`, `index.html`, `README.md`, `requests.http`
- `examples/day1/ex03/shared`: `examples.css`
- `examples/day2/ex04`: `.env.example`, `.gitignore`, `api-settings.js`, `app.js`, `config.example.js`, `index.html`, `picture.png`, `README.md`, `requests.http`
- `examples/day2/ex04/shared`: `examples.css`
- `examples/day2/ex05`: `.env.example`, `.gitignore`, `api-settings.js`, `app.js`, `config.example.js`, `index.html`, `README.md`, `requests.http`
- `examples/day2/ex05/shared`: `examples.css`
- `examples/day2/ex06`: `.env.example`, `.gitignore`, `api-settings.js`, `app.js`, `config.example.js`, `index.html`, `README.md`, `requests.http`
- `examples/day2/ex06/shared`: `examples.css`
- `examples/day2/web-week12`: `.env.example`, `.gitignore`, `about.html`, `api-settings.js`, `app.js`, `config.example.js`, `guestbook.html`, `guestbook.js`, `guestbook.local.html`, `guestbook.local.js`, `index.html`, `README.md`, `requests.http`, `styles.css`
- `examples/day2/web-week12/images`: `profile.png`, `project1.png`, `project2.png`, `project3.png`, `site-map.svg`
- `examples/day2/web-week12/screenshots`: `guestbook.png`, `home.png`
- `examples/day2/web-week12/shared`: `examples.css`
