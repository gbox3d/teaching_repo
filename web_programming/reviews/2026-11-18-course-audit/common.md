# 공통 자료·실행 도구·배포 통합

총괄이 공통 자료 19개와 웹 교재의 빌드·색인을 확인했다. 다른 과목 원고와 별도 개발 도구의 동시 변경은 작업 범위에 넣지 않았다.

아래 전수 검증 기록은 20:36:44 KST의 기준본과 이후 명시한 저장 실패 보완에 해당한다. 7주 타임라인 완성 뒤 진행한 브라우저 검사, 재빌드와 연계 단원 심사는 [후속 결과](final.md#7주-타임라인-후속-심사)에서 확인한다.

## 공통 안내

README·주차 색인·조교 안내·AGENTS에 C01의 27개 일반 차시 60+30분과 시험·발표 예외를 맞췄다. 3주 이후 파일 배부·저장소 준비는 수업 전, 업로드는 수업 뒤로 안내한다. 11주 필수 폼 저장과 제공 방명록을 구분하고, 배열 심화·SPA 직접 전환은 특강에 둔다.

7주 W3.CSS CDN 도입, 12주 about/help/GET, 13주 POST, 14주 PATCH/DELETE 순서를 공통 API 안내에 반영했다. 정규 수업은 실행 중 설정 패널, Supabase 특강은 config.example.js, REST Client는 .env를 사용한다고 구분했다. 브라우저 설정은 메모리에만 유지된다.

공용 CSS에 border-box와 긴 출력 문자열 줄바꿈을 보완했다. 11·12주 홈의 다크 모드 제목·메뉴·footer 대비도 6주 수정과 맞췄다. 12주 HTTP 오류 예제의 잘못 닫힌 option 태그를 수정해 missing_column 선택이 실제 요청에 적용되게 했다.

## 서버와 구성

- 정적 서버: 실제 .env·.git·.local·localfiles 접근과 목록 표시를 차단하고 .env.example은 제공한다. 임시 포트 실행 시 실제 포트를 안내한다. 파일·HEAD·404·405·비공개 경로를 임시 파일로 검증했다.
- 방명록 API: 기존 CRUD·CORS·학생 태그·편집 키·재시작 후 저장 시험 5개를 유지했다. schema.sql·about-help.sql의 권한·정책·데이터 모델과 student-guide를 대조했다.
- provision.mjs: 잘못된 인수 3종, 임시 태그 두 개, 키 해시 생성, 기존 출력 덮어쓰기 거부를 실제 실행했다. 출력은 임시 폴더에서 검사했으며 실제 학생 키를 읽지 않았다.
- API 설정: canonical api-settings.js와 각 주차 사본을 비교한다. 학생 작성 범위는 요청·응답 처리이며 설정 패널 작성은 제외한다.

공용 Supabase에서 실제 about/help GET 200과 없는 열 GET 400을 확인했다. Chrome localhost에서 HTTPS Supabase로 읽는 CORS도 확인했다. [Node 읽기 기록](live-read-checks.json)과 [브라우저 읽기 기록](live-browser-read.json)을 남겼다. 현재 작업에서 공용 서버의 쓰기나 정책 변경은 실행하지 않았다.

## 교재 사이트 생성

슬라이드에 연결한 HTML만 복사하고 인접 JS·CSS·이미지를 누락하던 문제를 실제 npm check의 실패로 확인했다. 빌드가 해당 단원의 공개 examples 파일과 공용 CSS·JS를 함께 복사하도록 고쳤다. 다른 주차 HTML로 이어지는 링크도 검사한다. Git이 공개 파일로 취급하는 목록을 사용하고 ignored 파일·숨김 경로·localfiles·조사 보고서는 복사하지 않는다.

기존 배포 규칙대로 Markdown 원고는 dist에 복사하지 않는다. 예제 HTML에서 README로 가는 링크는 저장소 주소로 바꾼다. 공용 비밀번호나 로컬 구성 파일은 빌드 입력에 포함하지 않는다. 두 영문 원고의 `<b>`·`<repository>` 표시도 인라인 코드로 고쳐 빌드 오류를 해결했다.

SPA 특강을 색인에 추가해 웹 교재는 21개 덱·371장, 전체 사이트는 언어별 58개 덱·1175장이다. 기존 단원의 한영 장수는 유지했다. 다른 과목의 내용·장수는 바꾸지 않았다.

## 통합 검증 기록

- npm run build와 npm run check: 내부 파일·앵커·기존 주소 검사 통과.
- npm test: 덱 맞춤 3개, 서버·방명록·IoT·HTTP 26개, 지도 25개, 총 54개 통과.
- [생성된 덱 브라우저 검사](evidence/deck-browser.json): 웹 42개 한영 덱·742장을 실제 뷰어에서 순서대로 이동해 본문 넘침을 검사했다. 대표 5장 캡처도 확인했다. 마지막으로 수정한 10·15주와 신시사이저의 6개 덱·90장을 [다시 검사](evidence/deck-browser-selected.json)했으며 넘침이 없었다.
- [소스 검사](evidence/source-checks.json): 공개 파일 889개, 외부 JS 199개 구문·HTML 171개의 로컬 자산 462개·API 설정 사본 22개를 검사했다. 누락·구문 오류·설정 사본 불일치가 없었다. 인라인 스크립트는 해당 단원의 브라우저·구문 검사에 포함했다.
- [배포본 예제 실행](evidence/built-examples-browser.json): 실제 dist의 5주 외부 JS 버튼, 12주 설정·about GET, 14주 POST·텍스트 출력·홈/소개/방명록 이동·프로필 이미지·설정 초기화를 Chrome에서 확인했다. 로컬 자산 HTTP 실패와 처리되지 않은 예외가 없었다.
- 한국어 UI·문서 검사: 공통 문서·도구와 총괄 담당 특강에서 위반 없음.

최종 학습 심사에서 12주 ex01의 about만 필수라는 안내와 전체 REST 순서 안내가 섞인 점을 지적했다. ex01에서는 about만 실행하고 help·방명록 GET은 후속 단계의 참고 요청이라고 명확히 했다.

최종 기술 심사에서 11주 제공 방명록의 저장 용량 초과 예외를 발견했다. 11주 완성본과 12주 로컬 보관본에 실패 안내와 배열 복원을 추가하고 11주 코드 전문을 맞췄다. 독립 심사자가 두 화면에 QuotaExceededError를 주입해 등록·삭제 실패 때 입력·목록·기존 저장값을 유지하고, 복구 후 중복 없이 등록되는지 재확인했다.

학생 집단의 소요 시간, 실제 Pages 게시, VS Code 확장 UI, 실제 Kakao 연결·오디오 청취는 위 검사로 입증하지 않는다. 주차별·특강별 보고서에 실행 방법과 제한을 별도로 기록한다.

## 공통 파일 목록

- AGENTS.md, README.md, ta_setup_guide.md, weeks/README.md, specials/README.md
- shared/README.md, shared/examples.css, shared/api-settings.js
- tools/static-server/README.md, server.mjs, server.test.mjs
- tools/guestbook-api/.gitignore, README.md, student-guide.md, schema.sql, about-help.sql, provision.mjs, server.mjs, server.test.mjs
- 통합 변경: 저장소 README.md, site/catalog.json, scripts/render-site.mjs, scripts/check-site.mjs, package.json
