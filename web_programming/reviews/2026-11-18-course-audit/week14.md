# 14주 구현·검증 기록

14주 전체 원고와 예제를 C01의 양일 강의·시연 60분+학생 실습 30분에 맞췄다. 완성 방명록은 `guestbook.js` 하나에 GET·POST·DELETE·PATCH를 모았고 설정은 제공 `api-settings.js`로 분리했다. 커밋·공용 서버 쓰기는 수행하지 않았다.

## 조사 범위

`web_programming/AGENTS.md`, `implementation.md`, `winner.md`, `proposal-C01.md`의 14주 행, `api-settings-contract.md`를 읽었다. 13주 완성본의 HTML·guestbook.js·api-settings.js·shared/examples.css와 홈 styles.css, 로컬 API server.mjs·server.test.mjs·README도 읽어 인계와 실제 응답 계약을 확인했다.

14주 폴더의 75개 파일을 목록화하고 읽기·구문·링크·자산 검사를 수행했다. 아래 표는 같은 역할의 파일을 묶은 조사 범위다.

| 위치 | 읽고 확인한 파일 | 처리 |
|---|---|---|
| 주차 루트 | README.md, lab.md, walkthrough.md, slides.md, slides_en.md | 시간·수정량·제공 코드·설정·실행 안내·전문 코드 일치 수정 |
| 주차 루트 | project_brief.md, rubric.md, demo_outline.md | 기존 링크와 별도 과제 안내 유지. 레포트 검사를 수업에 넣지 않음 |
| examples | README.md | 필수·시연·선택과 기본 배포 파일 구분 |
| day1/ex01 | index.html, app.js, config.example.js, styles.css, README.md, shared/examples.css | 인덱스/ID 시연 유지, 사용하지 않는 설정·옛 스타일은 안내 처리 |
| day1/ex02 | index.html, app.js, config.example.js, message.json, README.md, api-settings.js, requests.http, .env.example, .gitignore, shared/examples.css | DELETE와 같은 ID 재조회, 설정·키·오류 보호. 이전 message.json 배포 제외 |
| day1/ex03 | index.html, app.js, README.md | 과거 저장 예제를 11주 폼 저장 이동 안내로 변경, 현재 필수에서 제외 |
| day2/ex03 | index.html, app.js, config.example.js, README.md, api-settings.js, requests.http, .env.example, .gitignore, shared/examples.css | PATCH와 동일 ID 메시지 확인, 설정·키·오류 보호 |
| day2/ex04 | index.html, app.js, config.example.js, README.md, api-settings.js, requests.http, .env.example, .gitignore, shared/examples.css | 대상 GET 비교·선택 확인 |
| day2/web-week14 실행본 | index.html, about.html, guestbook.html, app.js, guestbook.js, api-settings.js, styles.css, shared/examples.css | 홈·내 정보 유지, 단일 CRUD JS·편집 DOM·키 지우기, 13주 다크 모드 대비 인계 |
| day2/web-week14 배포 자료 | README.md, requests.http, .env.example, .gitignore | 독립 배포 목록과 dotenv·마스킹 편집 키 요청 안내 |
| day2/web-week14 이전 JS | config.example.js, submit.js, actions.js, delete.js, edit.js, about.js, projects.js | 이동·제외 안내 주석으로 바꾸고 HTML에서 읽지 않음 |
| day2/web-week14 이전 화면·데이터 | projects.html, data/projects.json, images/site-map.svg | 옛 화면은 짧은 방명록 안내, 데이터·SVG는 보존하고 기본 배포 제외 |
| day2/web-week14 PNG 자산 | images/profile.png, project1.png, project2.png, project3.png; screenshots/home.png, projects.png, guestbook.png | 7개 이미지 직접 열어 확인. 프로필만 기본 배포. 옛 프로젝트와 이메일·전체 지우기 UI가 있는 캡처는 현재 결과로 사용하지 않음 |

## 차시와 학생 수정량

| 차시 | 강의·시연 60분 | 학생 실습 30분 |
|---|---|---|
| 14-1 | 준비 5, 인덱스와 ID 15, 편집 키 10, DELETE·204 15, 대상 재조회 10, 안내 5 | ID·.http 5, DELETE 대상 URL·method·헤더 3곳 12, 정답/틀린 키와 재조회 13 |
| 14-2 | 준비 5, PATCH 15, 기존 글→폼 10, 응답 배열·재조회 15, 전체 동작 10, 안내 5 | PATCH 대상 URL·JSON 본문·동일 ID 재조회 3곳 12, 세 글 검증·실패 복구 13, 키 지우기·캡처 5 |

한영 슬라이드는 각각 기존 13장을 유지했다. 파일 배부·저장소 준비는 사전, 공개 업로드는 수업 뒤로 이동했다. ex01·ex04와 전체 조립은 시연, 추가 재작성은 선택이다. 설정 패널·편집 키·DOM 연결·초기화·중복 클릭·응답 순서 보호·응답 검증은 제공한다.

## 구현 내용

- 13주 목록·POST 동작을 계승했다. 모든 DOM·함수·이벤트를 준비한 뒤 파일 끝의 setupApiSettings와 loadMessages를 실행한다. 목록은 latestRequest, 쓰기는 settingsVersion으로 이전 설정의 늦은 응답을 무시한다.
- 설정 적용은 새 글 폼·편집 폼·선택 ID·입력 및 메모리 편집 키를 초기화한다. 진행 중 요청이 서버에서 완료될 수 있음을 안내하고 이전 설정으로 돌아가 GET으로 확인하도록 했다.
- DELETE 204는 JSON으로 읽지 않고 같은 URL을 GET한다. PATCH는 변경 배열 1행과 ID를 확인하고 동일 ID GET에서 메시지를 비교한다. 틀린 키의 200 []·204를 완료로 표시하지 않는다.
- 요청 중 버튼 중복 클릭을 막고 실패 뒤 복구한다. 통신 결과를 모를 때 재작성 전에 GET을 안내한다. 기다리는 동안 새로 선택·입력한 폼은 이전 성공 응답으로 지우지 않는다.
- 네 REST 폴더 모두 README·requests.http·.env.example·.gitignore를 갖춘다. dotenv의 기본 URL·공개 키·BOOK_ID와 MESSAGE_ID를 쓰고 편집 키는 정확히 `# @prompt password`/`{{password}}`로 받는다. 요청 순서는 about·help·목록·대상 GET·변경·동일 ID 재조회다. ex04는 조회 요청만 제공한다.
- W3.CSS는 cdnjs 4.1.0을 사용한다. 추가 스타일은 폴더별 shared/examples.css이며 정본의 border-box 보정을 포함한다. 키와 실제 공용 설정을 추적 파일에 넣지 않았다.
- walkthrough의 guestbook.html·api-settings.js·guestbook.js 전문을 실행 파일과 대조했다. 기본 배포 목록에 이전 프로젝트 자료와 다중 동작 파일을 넣지 않았다.

## 실제 실행 결과

Chrome headless와 Playwright를 사용했다. 화면은 `http://localhost:8111`의 web_programming 루트, API는 createGuestbookServer를 일회용 임시 데이터 폴더·임시 루프백 포트로 실행했다. 임시 편집 키는 해당 임시 파일에서 메모리로 읽었고 로그·소스·캡처에 출력하지 않았다.

| 검증 | 관찰 결과 |
|---|---|
| 기존 초기화 경쟁 재현 | 원본에서 actions.js 600ms 지연+빠른 GET이면 목록 0개, 콘솔에 createEditButtons is not defined |
| 수정 후 동일 조건 | 같은 재현 서버의 허용 파일에 새 api-settings.js만 추가. 지연 0/600ms 모두 목록 1개·불러오기 완료·pageerror 없음. 옛 actions.js는 요청하지 않음 |
| about/help | 실제 로컬 API GET 200 확인 |
| ex01 | 버튼 클릭 결과 배열 위치 0, 서버 ID 41 |
| 완성본 POST | 연습 글 3개 생성, 생성 ID와 목록 GET 확인 |
| 빈 편집 키 | DELETE 요청 전 차단, 서버 글 유지 |
| 틀린 편집 키 | 실제 PATCH 200 []와 DELETE 204 후 성공 표시 없음, 원본 유지 |
| 올바른 편집 키 | PATCH 메시지와 GET 일치, 세 글의 가운데 ID만 삭제, 다른 글 유지 |
| 별도 페이지 조회 | 같은 Chrome의 다른 localhost 페이지에서 수정된 서버 글 확인 |
| 오프라인 | API 요청 중단 시 조회 실패·목록 초기화·버튼 복구, 연결 복구 후 정상 GET |
| 틀린 공개 키 | 401 안내 뒤 정상 설정으로 복구 |
| 설정 변경 | 새 글·수정 폼·선택 ID·편집 키 초기화 확인 |
| 늦은 GET | 첫 응답을 650ms 지연하고 다른 BOOK_ID 적용. 새 목록과 안내 유지 |
| 늦은 POST/PATCH/DELETE | 각 응답을 650ms 지연한 뒤 다른 BOOK_ID로 전환. 새 입력·편집 ID·편집 메시지·안내가 덮이지 않음 |
| ex02/ex03/ex04 | 실제 API DELETE/PATCH/GET과 쓰기 예제의 틀린 키 처리·키 칸 비우기 확인 |
| 375px | 설정 패널을 펼친 완성본과 ex02·ex03·ex04에서 가로 넘침 없음. 완성본 입력·버튼의 오른쪽 경계도 화면 안 |
| 홈·내 정보·이전 주소 | 인사·다크 버튼 클릭 2회, 내 정보 이동·뒤로가기, projects 안내·day1/ex03 이동 링크 확인 |
| requests.http | 4폴더 파일을 직접 읽고 임시 dotenv/prompt 값으로 치환해 6·6·4·8개 요청 실행. 모두 실제 API 응답과 일치 |
| 파일·원고 | 75파일 상대 링크·JS 구문, 전문 3개 일치, 설정 사본 4개·CSS 사본 5개 정본 일치, 한영 13/13장 확인 |
| 문구·공백 | Korean UI/doc 스타일 검사 통과. git diff --check 통과 |

브라우저 검증 묶음은 19개 확인 항목을 기록했고 pageerror는 없었다. 375px 완성본·DELETE 예제 캡처를 직접 열어 레이아웃도 확인했다. W13의 홈 다크 모드 제목·링크·footer 색 보정을 마지막에 그대로 복사했다.

검증 스크립트와 상세 로그는 저장소 밖 임시 폴더의 `week14-browser-test.mjs`, `week14-http-navigation.mjs`, `week14-static-check.mjs`, `week14-defer-race-fixed.mjs`, `course-audit-week14-20261118/`에 남겼다. 키를 포함하는 일회용 API 데이터는 저장소 밖에 있다.

## 제한과 인계

공용 Supabase 쓰기·공용 HTTPS CORS·GitHub Pages 배포·다른 기기·다른 브라우저 제품은 실행하지 않았다. REST Client 확장 UI 자체는 조작하지 않았으며 파일을 읽어 같은 HTTP 요청을 실행한 검증이다. 실제 초보 학생의 30분 수행 시간은 실측하지 않았다. 원본 경쟁 재현 서버는 CSS를 생략하고 CDN을 차단하므로 해당 재현 로그의 스타일 로딩 오류는 별도 375px 실제 화면 검사와 구분한다.

전체 사이트 빌드와 세 독립 심사자의 평가는 총괄 단계다. 14주 자료에 자체 통과 점수를 붙이지 않았다. 14주 핵심 HTML·JS·settings·shared CSS를 SPA 담당자에게 전달했으며, 마지막 홈 다크 모드 styles.css도 13주와 일치한다. 수정 범위는 14주 폴더와 이 보고서다.
