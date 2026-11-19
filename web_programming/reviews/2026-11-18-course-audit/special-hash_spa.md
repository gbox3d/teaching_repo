# Hash SPA 특강 구현·검증 기록

## 조사 범위

2026-11-18에 C01 선정 결과와 구현 계약을 기준으로 새 `specials/hash_spa/`를 작성했다. 기존 정규 MPA 파일과 공통 색인은 이 담당 범위에서 수정하지 않았다. 자체 점수를 부여하지 않으며 전체 빌드와 독립 심사는 총괄 통합에서 수행한다.

읽은 기준은 `web_programming/AGENTS.md`, 이 검토 폴더의 `implementation.md`, `winner.md`, `proposal-C01.md`, `api-settings-contract.md`다. 참고한 특강은 `specials/array_advanced/README.md`, `slides.md`, `specials/home_iot_http/README.md`다. 14주 `examples/day2/web-week14/`의 `index.html`, `about.html`, `guestbook.html`, `guestbook.js`, `api-settings.js`, `shared/examples.css`, `requests.http`와 `tools/guestbook-api/{README.md,server.mjs}`, `tools/static-server/server.mjs`를 읽었다.

14주 담당자와 복사 시점을 맞췄다. 최초 HTML에서 편집 DOM 누락을 발견해 담당자에게 알렸으며, 해당 담당자가 수정하고 실제 CRUD를 검증한 HTML·JS·설정을 복사했다. 일반 주차나 다른 특강의 파일은 변경하지 않았다.

## 전체 산출물

아래 목록은 `specials/hash_spa/` 기준 전체 파일이다. 모든 문서와 예제를 조사·작성·검사 대상으로 삼았다.

```text
README.md
examples/01_mpa/README.md
examples/01_mpa/about.html
examples/01_mpa/guestbook.html
examples/01_mpa/guestbook.js
examples/01_mpa/home.js
examples/01_mpa/index.html
examples/01_mpa/shared/examples.css
examples/02_two_screens/README.md
examples/02_two_screens/app.js
examples/02_two_screens/index.html
examples/02_two_screens/shared/examples.css
examples/03_hash_routes/README.md
examples/03_hash_routes/app.js
examples/03_hash_routes/index.html
examples/03_hash_routes/shared/examples.css
examples/04_rest_guestbook/.env.example
examples/04_rest_guestbook/.gitignore
examples/04_rest_guestbook/README.md
examples/04_rest_guestbook/api-settings.js
examples/04_rest_guestbook/app.js
examples/04_rest_guestbook/index.html
examples/04_rest_guestbook/requests.http
examples/04_rest_guestbook/shared/examples.css
examples/README.md
lab.md
slides.md
slides_en.md
walkthrough.md
```

| 자료·예제 | 구현 내용 | 실습 구분 |
|---|---|---|
| README·lab·walkthrough·examples README | 14주 이후 선택 특강, 시간 상한 없음, 단계·실행·확인·한계 | 정규 시험 제외, 01~03의 60+30은 운영 예 |
| slides·slides_en | 같은 순서의 한영 각 18장 | 학생 수정·시연·제공·선택 연구 일치 |
| 01_mpa | 세 실제 HTML, 홈 카운터, 방명록 미리 보기 | 실제 파일 링크·Document 요청 비교 |
| 02_two_screens | 두 section의 hidden 전환, 현재 메뉴·title·포커스 | 표시 조건 수정, 이벤트 중복 관찰 |
| 03_hash_routes | 세 hash·미등록 안내·빈 hash 홈·입력 유지 | hash 읽기·표시·이벤트 연결 |
| 04_rest_guestbook | 14주 CRUD와 설정 재사용, 단일 app.js, home 접두어 | section 조립·ID 구별, CRUD 검증 |
| requests.http·.env.example·.gitignore | about→help→GET→POST→대상GET→PATCH→대상GET→DELETE→대상GET | 실제 키 제외, password 예약 prompt |

각 예제의 CSS는 폴더 안 `shared/examples.css`이며 W3.CSS CDN은 `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`다. `examples/` 루트에는 README만 있고 실행 파일은 단계 폴더에 있다. 프레임워크·npm 의존성·History API를 추가하지 않았다.

## 실제 브라우저 검증

2026-11-18 11:00:30 UTC부터 Node Playwright의 Chrome headless를 실행했다. 기존 정적 서버의 하위 경로 `http://localhost:8111/specials/hash_spa/examples/`와 04 폴더를 루트로 제공하는 임시 서버 `http://127.0.0.1:8167/index.html`을 사용했다. CRUD는 임시 디렉터리에서 새 `createGuestbookServer` 인스턴스를 열어 실행했다. 실사용 공용 서버에는 쓰지 않았다. 임시 API의 편집 키는 메모리로 읽고 출력·소스·보고서에 기록하지 않았다.

| 실행 대상 | 실제 입력·조작 | 관찰 결과 |
|---|---|---|
| 01 모든 HTML | 홈→소개→방명록, 직접 열기·새로고침·뒤로/앞으로 | 실제 HTML 요청 증가, 올바른 문서 표시 |
| 01 방명록 | 한글과 `<b>텍스트</b>` 미리 보기 | HTML 실행 없이 텍스트 표시 |
| 02 | 두 화면 10회 전환, 카운터 1회, 키보드 Enter·새로고침 | 추가 Document 요청 0, 주소 유지, 카운터 1 증가, 제목 포커스 |
| 03 | 빈 hash·세 경로·없는 hash·홈 복귀·뒤로/앞으로·직접 진입·새로고침 | section 하나 표시, 미등록 화면 메뉴 선택 없음, 새로고침 후 초안 초기화 |
| 03 | 초안 입력 후 세 화면 10회 전환 | 입력 유지, 추가 Document 요청 0, 키보드 선택 후 H2 포커스 |
| 04 루트·하위 경로 | #guestbook 직접 진입·새로고침·빈 hash·없는 hash·뒤로/앞으로·키보드 | 같은 화면 선택, 제목 포커스, 중복 ID 없음 |
| 04 반복 전환 | 미전송 초안 입력 후 세 화면 10회 전환 | 초안 유지, 전환 중 GET 0건·Document 요청 0건 |
| 04 POST | `<b>첫 글</b>`, 가운데 글, 마지막 글 | POST 3건, 각 글 1개씩 생성, 태그는 텍스트 |
| 04 PATCH | 가운데 서버 ID 32, 틀린 키 후 올바른 키 | 틀린 키는 원문 유지, 올바른 키는 같은 ID 메시지 변경 |
| 04 DELETE | ID 32, 틀린 키 후 올바른 키 | 틀린 키는 대상 유지, 올바른 키는 대상 없음, 첫·마지막 글 유지 |
| 04 GET 실패·복구 | Offline, 새로 불러오기, Online 복구 | 초안 유지, 버튼 재활성화, 재조회 완료 |
| 04 새로고침 | 초안과 API 설정·키가 있는 상태 | 초안·설정·키 초기화, 서버 글 3행 유지 |
| 04 반응형 | 375px·1280px | scrollWidth 각각 375·1280, 가로 넘침 없음 |

브라우저의 uncaught page error는 0건이다. 직접 hash 진입 때 기본 앵커 처리가 제목 포커스를 BODY로 옮기는 현상을 최초 실행에서 재현했다. 03·04에 `load` 1회 리스너를 두어 브라우저 기본 처리 뒤 같은 `showRoute()`로 제목 포커스를 맞췄다. 수정 후 표의 전체 브라우저 절차를 다시 실행해 통과했다. `showRoute()` 안에서는 이벤트를 등록하지 않는다.

375px 전체 화면 캡처를 직접 읽어 입력·버튼·상태·목록 배치를 확인했다. 총괄이 [원시 JSON](evidence/hash-spa-browser.json), [375px](evidence/hash-spa-375.png), [1280px](evidence/hash-spa-1280.png)를 이 조사 기록에 보관했다. 검증 스크립트는 로컬 Temp의 `hash-spa-check.mjs`다. 검증 자료는 배포 예제에 포함하지 않는다.

## 요청 파일·문서 검사

`requests.http` 자체를 읽어 요청 구획·헤더·본문을 파싱하고 임시 API로 9개 요청을 순차 실행했다. POST 응답 ID를 다음 대상 요청에 넣었다. 실제 status 순서는 `200, 200, 200, 201, 200, 200, 200, 204, 200`이며 소개 1행·도움말 6행·최종 대상 GET 0행을 확인했다. DELETE 본문은 빈 문자열이었다. VS Code의 Send Request UI를 자동 조작했다고 기록하지 않는다.

모든 JS에 `node --check`를 실행했다. 로컬 Markdown 링크 51개가 존재하며 한영 슬라이드 각 18장을 확인했다. `check_ui_copy.mjs`와 `check_doc_style.py`를 특강 전체에 실행해 위반이 없었다. 한영 슬라이드는 예제 순서·주소·이벤트 코드·HTTP 상태·실습 구분을 대조했다.

## 통합 연결과 남은 제한

총괄은 `hash_spa` 덱 ID로 `slides.md`·`slides_en.md`, 특강 색인과 예제 패키지를 연결한다. 본 담당자는 공통 catalog·빌드 설정을 변경하지 않았다.

실제 GitHub Pages 배포, 공용 API PATCH·DELETE, 다른 PC·휴대폰, 초보 학생의 수행 시간은 측정하지 않았다. 로컬 루트·하위 경로 성공을 배포 검증으로 바꾸어 쓰지 않는다. 프롬프트 마스킹은 `password` 이름 규칙을 적용했으며 VS Code 확장의 실제 입력창은 이 검증에서 조작하지 않았다. 전체 빌드·기존 테스트·슬라이드 최종 렌더 검증·독립 3인 평가는 총괄 통합에서 별도로 수행한다.
