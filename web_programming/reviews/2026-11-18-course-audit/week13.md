# 13주차 구현·검증 기록

2026-11-18, C01의 13-1·13-2 행과 구현 지시서·API 설정 계약을 기준으로 조사했다. 수정 범위는 `weeks/week13_release_security/`와 이 보고서다. 커밋·푸시·클라우드 변경은 수행하지 않았다.

## 차시와 학생 수정량

| 차시 | 강의·시연 60분 | 학생 실습 30분 |
|---|---|---|
| 13-1 | 준비 5, POST 15, headers·body 15, 201·id 10, 입력 거절 10, 안내 5 | .http message 변경·POST 10, id·GET 10, 빈값 비교 10 |
| 13-2 | 준비 5, submit 복습 10, POST 연결 15, 대기·실패 15, 재조회 10, 안내 5 | 폼 값·JSON·loadMessages 세 구역 15, 중복 클릭·실패 입력 7, 다른 브라우저·캡처 8 |

README·lab·walkthrough·examples 안내·한영 슬라이드를 같은 구성으로 고쳤다. 양 언어 슬라이드는 각각 기존 14장을 유지했다. ex01·ex04~06은 시연이며 전체 예제를 학생 필수 타이핑으로 배정하지 않는다. 설정·오류 처리·요청 번호 검사는 제공 코드다. 파일 배부·저장소 준비는 사전 준비, 업로드는 수업 뒤 정리다. 학생의 실제 수행 시간을 측정한 기록은 아니다.

## 조사 범위와 수정

완료 시 주차 안의 80개 파일을 조사했다. Markdown 13, HTML 9, JS 21, `.http` 6이며 설정 예시·gitignore·CSS·이미지를 포함한다. 아래 전수 목록의 모든 파일을 읽거나 동일 사본 해시·렌더 결과로 확인했다.

| 범위 | 조사와 반영 |
|---|---|
| 주차 README·lab·walkthrough·examples README | 60+30, 시연·필수 구분, 11주 필수 폼 저장과 제공 방명록 구분, 실행 중 설정·REST Client·수업 뒤 업로드 |
| KO/EN 슬라이드 각 14장 | 차시별 시간·수정 세 곳·통합 JS·메모리 설정·응답 불명확 시 GET 우선으로 교정 |
| day1/ex01 | 버튼으로 JSON 변환, API 요청 없음, 긴 화면 설명을 README로 이동 |
| day1/ex02 | 고정값 POST·201·id·수동 GET, `.http` 필수 요청 비교본 |
| day1/ex03 | 의도적으로 빈 메시지 전송, 서버 400과 정상 201 비교 |
| day2/ex04 | trim한 폼 입력과 JSON POST, 실패 입력 보존 |
| day2/ex05 | 저장 대기·중복 submit 차단·실패 뒤 버튼 복구 |
| day2/ex06 | POST 뒤 GET, 저장 안내와 조회 안내 분리 |
| day2/web-week13 | 7주 폼 ID·12주 GET 계약 유지, GET·POST를 guestbook.js 하나에 통합, 마지막 최초 조회 |
| REST 폴더 6개 | README·requests.http·.env.example·.gitignore·api-settings.js 배부, 실제 키 없음 |
| HTML·CSS | W3.CSS cdnjs 4.1.0 고정, 설명은 README로 이동, 별도 shared/examples.css 동봉 |
| 홈·내 정보·app.js·styles.css | 메뉴·클릭·다크 모드 동작 확인, 다크 모드 제목·메뉴·footer 색 대비 보완 |
| 프로필 3사본 | PNG 표시 확인, 세 파일 SHA256 일치. day1/ex04/images와 day2/images는 이전 경로 보존 자산 |
| project1~3.png·site-map.svg | 카드 그림 직접 확인, SVG의 세 페이지 이름과 연결 소스 확인. 이번 주 필수 구현과 구분 |
| screenshots | home·guestbook 캡처 갱신, 375px 방명록 캡처 추가. projects.png는 이전 프로젝트 참고임을 문서에 명시 |

## 구현에서 해결한 결함

- 기존 submit.js의 POST를 guestbook.js로 합쳤다. submit.js·config.example.js는 이동 안내만 남기며 HTML에서 로드하지 않는다. 문서의 모든 연결 안내를 바꿨다.
- api-settings.js는 공통 정본의 정확한 6사본이다. 공용 URL·공개 키·book_id는 메모리에만 보관하며 새로고침 뒤 재입력한다. 실제 `.env`는 만들지 않았다.
- POST 성공과 뒤따르는 GET 실패를 서로 다른 상태 요소에 표시한다. 성공 응답 본문의 JSON이 손상되면 성공 응답 수신을 알리고 GET으로 확인한다. 저장 응답 유실 때 입력을 보존하고 자동 재POST하지 않는다.
- saving guard와 disabled를 함께 사용한다. 요청이 실패해도 finally에서 버튼을 복구하며, 대기 중 새로 작성한 입력을 완료 시 무조건 지우지 않는다.
- GET은 12주의 latestRequest/requestId 방식을 이어 쓴다. POST는 settingsVersion을 확인해 이전 API·태그의 늦은 응답이 새 설정의 안내·입력을 바꾸지 않는다. 설정 적용 즉시 새 목록을 조회한다.
- 375px에서 설정 패널을 펼치면 input 오른쪽이 378px까지 넘는 결함을 재현했다. W3.CSS가 200으로 수신되고 link.sheet가 있는 조건이었다. 각 shared/examples.css에 border-box 규칙을 추가해 scrollWidth 375px를 확인했고 공통 담당자에게 전달했다.

## 실제 실행 결과

Node.js 24.18.0, Playwright의 설치된 Chrome·Microsoft Edge headless를 사용했다. `createGuestbookServer({directory: 일회용 temp})`로 임시 API를 만들고 임의 포트에서 검증했다. 기존 사용자 `.local` 데이터는 사용하지 않았다. 정적 페이지는 기존 localhost:8111의 web_programming 루트에서 열었다.

| 검사 | 관찰 결과 |
|---|---|
| API 소개·도움말 | GET 200, JSON 배열 |
| 6개 requests.http의 원문 요청 | 각 폴더에서 about 200 → help 200 → POST 201 → GET 200 → 빈 메시지 POST 400 |
| ex01 | 입력 JSON 변환, HTML 태그가 문자로 표시, API 호출 없음 |
| ex02~ex06 | 모든 POST 성공·GET 확인, ex03 빈 메시지 400 추가 확인, 펼친 설정 패널 포함 375px 넘침 없음 |
| 완성본 정상 저장 | POST 201의 서버 id, 뒤따르는 GET 목록에 같은 글 |
| 공백 입력 | 안내 표시, POST 요청 0회 |
| `<b>문자그대로</b>` 입력 | list 안 b 요소 0개, 원문 글자 표시 |
| 두 번 연속 requestSubmit | 대기 중 disabled, 실제 POST 1회 |
| POST 통신 실패 | 입력 보존, 결과 확인 안내, 버튼 재활성화 |
| POST 성공·GET 503 | 저장 완료 안내 유지, 목록에는 조회 실패 안내 |
| 서버 저장 후 응답 유실 | POST 1회, 입력 보존, 수동 GET에서 저장된 글 확인, 재POST 없음 |
| 201 JSON 손상 | 저장 응답 수신·번호 확인 실패 안내, 입력 보존, GET 목록 확인 |
| 이전 GET 450ms·새 GET 100ms | 새 태그 목록 유지, 이전 늦은 응답 무시 |
| POST 400ms 중 태그 변경 | 새 입력 보존, 이전 저장 결과 안내, 이전 글이 새 목록에 섞이지 않음 |
| POST 400ms 중 API URL 변경 | 두 번째 임시 API로 이동, 이전 서버 성공을 새 서버 성공으로 표시하지 않음; 이전 API에 다시 접속해 저장 글 확인 |
| 새로고침 | 런타임 설정 초기화, 로컬 기본 URL 복원 |
| Chrome → 별도 Microsoft Edge | Chrome에서 저장한 글을 Edge에서 같은 로컬 API·태그로 GET 확인 |
| 홈·내 정보 | 세 메뉴, 인사 클릭·횟수·다크 모드, 375px 폭 확인 |
| 브라우저 오류 | uncaught pageerror 0건 |
| CDN·스타일 | W3.CSS HTTP 200, stylesheet 존재, 설정 펼침 scrollWidth 375 |
| 슬라이드 | 저장소 teaching 테마로 KO/EN 각각 14장 렌더, 28장 모두 본문 하단 경계 넘침 없음, 코드 슬라이드 육안 확인 |
| 정적 검사 | JS 21파일 node --check, 로컬 문서·HTML 링크 누락 0, 설정 정본 6사본 byte 일치, 실제 .env 0 |
| 한국어 문구 | UI·문서 검사기 모두 종료 코드 0 |

`.http`는 원문 요청의 환경변수를 메모리에서 임시 API 값으로 치환해 실제 HTTP 요청으로 검증했다. VS Code REST Client 확장의 GUI 클릭 자체는 자동 실행하지 않았다. README에 확장명·환경 설정·Send Request·헤더·예상 상태와 응답을 설명했다.

화면 근거: [1280px 방명록](../../weeks/week13_release_security/examples/day2/web-week13/screenshots/guestbook.png), [375px 방명록](../../weeks/week13_release_security/examples/day2/web-week13/screenshots/guestbook-375.png), [홈](../../weeks/week13_release_security/examples/day2/web-week13/screenshots/home.png). 방명록 캡처의 글은 일회용 API에 만든 검증 데이터다.

## 인계와 남은 제한

14주에 guestbook.html·guestbook.js·api-settings.js·shared/examples.css를 인계했다. GET·POST 다음 PATCH·DELETE 구역을 추가하고 초기 GET을 마지막에 둔다. 설정 패널·폼·목록 ID 계약은 유지했다. 공통 CSS의 border-box 보완과 홈 다크 색 수정도 총괄에게 알렸다.

실제 공용 API·GitHub Pages·다른 기기에서는 요청을 보내지 않았다. 같은 PC의 Chrome·Edge와 임시 API 결과를 공용 서비스 검증 완료로 표시하지 않는다. 전체 사이트 빌드·과목 통합 테스트·독립 심사는 총괄 단계다.

## 파일 전수 목록

아래 경로는 `weeks/week13_release_security/` 기준이다.

```text
examples/day1/ex01/app.js
examples/day1/ex01/index.html
examples/day1/ex01/README.md
examples/day1/ex01/shared/examples.css
examples/day1/ex02/.env.example
examples/day1/ex02/.gitignore
examples/day1/ex02/api-settings.js
examples/day1/ex02/app.js
examples/day1/ex02/config.example.js
examples/day1/ex02/index.html
examples/day1/ex02/README.md
examples/day1/ex02/requests.http
examples/day1/ex02/shared/examples.css
examples/day1/ex03/.env.example
examples/day1/ex03/.gitignore
examples/day1/ex03/api-settings.js
examples/day1/ex03/app.js
examples/day1/ex03/config.example.js
examples/day1/ex03/index.html
examples/day1/ex03/README.md
examples/day1/ex03/requests.http
examples/day1/ex03/shared/examples.css
examples/day1/ex04/images/profile.png
examples/day2/ex04/.env.example
examples/day2/ex04/.gitignore
examples/day2/ex04/api-settings.js
examples/day2/ex04/app.js
examples/day2/ex04/config.example.js
examples/day2/ex04/index.html
examples/day2/ex04/README.md
examples/day2/ex04/requests.http
examples/day2/ex04/shared/examples.css
examples/day2/ex05/.env.example
examples/day2/ex05/.gitignore
examples/day2/ex05/api-settings.js
examples/day2/ex05/app.js
examples/day2/ex05/config.example.js
examples/day2/ex05/index.html
examples/day2/ex05/README.md
examples/day2/ex05/requests.http
examples/day2/ex05/shared/examples.css
examples/day2/ex06/.env.example
examples/day2/ex06/.gitignore
examples/day2/ex06/api-settings.js
examples/day2/ex06/app.js
examples/day2/ex06/config.example.js
examples/day2/ex06/index.html
examples/day2/ex06/README.md
examples/day2/ex06/requests.http
examples/day2/ex06/shared/examples.css
examples/day2/images/profile.png
examples/day2/web-week13/.env.example
examples/day2/web-week13/.gitignore
examples/day2/web-week13/about.html
examples/day2/web-week13/api-settings.js
examples/day2/web-week13/app.js
examples/day2/web-week13/config.example.js
examples/day2/web-week13/guestbook.html
examples/day2/web-week13/guestbook.js
examples/day2/web-week13/images/profile.png
examples/day2/web-week13/images/project1.png
examples/day2/web-week13/images/project2.png
examples/day2/web-week13/images/project3.png
examples/day2/web-week13/images/site-map.svg
examples/day2/web-week13/index.html
examples/day2/web-week13/README.md
examples/day2/web-week13/requests.http
examples/day2/web-week13/screenshots/guestbook-375.png
examples/day2/web-week13/screenshots/guestbook.png
examples/day2/web-week13/screenshots/home.png
examples/day2/web-week13/screenshots/projects.png
examples/day2/web-week13/shared/examples.css
examples/day2/web-week13/styles.css
examples/day2/web-week13/submit.js
examples/README.md
lab.md
README.md
slides.md
slides_en.md
walkthrough.md
```
