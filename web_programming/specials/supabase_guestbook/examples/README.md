# Supabase 공용 방명록 API 구축 · 단계별 예제

01 접속 확인부터 시작해 02 안내 읽기, 03 방명록 조회, 04 저장 순서로 진행한다.
각 폴더의 `requests.http`로 요청·응답을 먼저 확인하고, 같은 폴더의 `index.html`과 `app.js`에서 브라우저 구현을 읽는다.
05는 글 수정과 목록 행 삭제, 06은 HTTP 콘솔, 07은 등록·조회·수정·삭제가 한 화면에 있는 완성 방명록이다.
examples 루트에는 이 README만 두고 실행 예제는 01~07 폴더 안에 둔다.

## 시작 전 강의자 준비

- 새 프로젝트에서는 [schema.sql](../../../tools/guestbook-api/schema.sql)을 실행한다. 테이블과 `student01`~`student30` 태그 30개가 생긴다. 이어서 [about-help.sql](../../../tools/guestbook-api/about-help.sql)을 실행해 접속 확인과 도움말 경로를 추가한다.
- 기존 수업 프로젝트에서는 [enable-public-crud.sql](../../../tools/guestbook-api/enable-public-crud.sql)을 SQL Editor에서 한 번 실행한다. 기존 글과 태그를 유지하면서 공개 수정·삭제 정책과 도움말을 갱신한다.

공용 서버의 방명록 GET·POST를 확인했으며, 2026-11-14에 `/rest/v1/about`·`/rest/v1/help` 설치와 GET 200도 확인했다.
about은 v1 안내 한 행, help는 단계 1~6의 여섯 행을 반환한다.
01·02의 404는 안내 SQL 적용 여부와 요청 경로를 먼저 확인한다. 학생은 Supabase 계정이나 SQL 작업 없이 준비된 API를 사용한다.

## REST Client로 요청부터 확인하기

1. VS Code의 **REST Client** 확장을 설치하고 `01_about` 폴더를 연다.
2. 그 폴더의 `.env.example`을 `.env`로 복사한다. 기존 `.env`가 있으면 덮어쓰지 않고 설정을 확인한다.
3. `.env`의 API 주소와 강의자가 배부한 공개 키를 설정한다. 03 이후에는 배부받은 `BOOK_ID`도 확인한다.
4. `requests.http`를 열고 요청 위의 **Send Request**를 누른다.
5. 응답 창에서 상태 번호와 JSON을 읽는다. 이 단계의 예상 응답과 일치하면 `index.html`·`app.js`로 이동한다.
6. 다음 폴더에서도 `.env`를 준비하고 같은 순서로 진행한다.

`{{$dotenv ...}}`는 `.http` 파일과 같은 폴더의 `.env`를 읽는다. examples 루트에 하나만 두면 각 단계의 설정을 대신하지 못한다.
`.http` 요청에는 Node 정적 서버가 필요 없다. 브라우저 화면을 열 때만 아래 미리보기 서버나 GitHub Pages를 사용한다.
REST Client의 성공은 브라우저 CORS 검증 결과와 별개다.

05~07에서 수정·삭제 요청을 보낼 때 `entryId` 입력 창에 실험용 글의 서버 ID를 넣는다. 후속 GET도 같은 태그와 ID로 보낸다.
`.env`는 Git 제외 대상이며 Pages 게시 파일에도 포함하지 않는다. 브라우저는 `.env` 대신 같은 폴더의 `config.example.js`와 localStorage의 공개 키를 읽는다.

출처: [REST Client 사용법](https://github.com/Huachao/vscode-restclient#usage), [환경 변수](https://github.com/Huachao/vscode-restclient#system-variables), [요청 시 입력 변수](https://github.com/Huachao/vscode-restclient#prompt-variables).

## 설정을 읽는 순서

| 실행 방식 | 설정 위치 | 값을 읽는 주체 |
|---|---|---|
| VS Code의 `requests.http` | 같은 폴더의 `.env` | REST Client가 `{{$dotenv API_BASE_URL}}` 등의 변수를 치환 |
| 브라우저의 `index.html` | 같은 폴더의 `config.example.js`(주소·`BOOK_ID`)와 화면 주소의 localStorage(공개 키) | HTML이 설정 스크립트를 먼저 실행하고, 설정 스크립트가 localStorage의 `API_PUBLIC_KEY`를 읽음 |

`.env.example`은 복사해서 사용하는 설정 견본이며 `.env` 자체가 실행되는 것은 아니다.
이 예제의 Node 정적 서버는 `.env`를 자동으로 읽지 않는다. 공개 키는 브라우저가 localStorage에서, REST Client가 `.env`에서 따로 읽으므로 한쪽을 바꿔도 다른 쪽은 바뀌지 않는다.

HTML은 다음 순서로 JavaScript를 불러온다.

```html
<script src="config.example.js" defer></script>
<script src="app.js" defer></script>
```

`defer`가 있는 일반 스크립트는 HTML 해석이 끝난 뒤 작성 순서대로 실행된다.
먼저 설정 파일이 `API_BASE_URL`, `API_PUBLIC_KEY`, `BOOK_ID`를 선언하고, 뒤의 `app.js`가 같은 페이지의 상수를 참조한다.
`API_PUBLIC_KEY`는 설정 파일이 실행될 때 localStorage에서 읽은 값이다. 키를 묻는 창에 넣은 값은 설정 파일이 저장한 직후 읽으므로 그 페이지의 요청에 바로 들어간다.
`app.js`가 설정 파일을 직접 읽거나 import하는 구조는 아니다. `config.example.js`라는 파일 이름에 자동 로딩 기능이 있는 것도 아니다.

## 단계별 폴더

| 순서 | 먼저 보낼 요청 | 응답에서 확인할 것 | 브라우저 화면 |
|---|---|---|---|
| 01 접속 확인 | [01_about/requests.http](01_about/requests.http) | about 한 행의 name·version·description·help_path | [01_about](01_about/index.html) |
| 02 사용 안내 | [02_help/requests.http](02_help/requests.http) | step 순서의 method·path·description 여섯 행 | [02_help](02_help/index.html) |
| 03 방명록 읽기 | [03_guestbook_get/requests.http](03_guestbook_get/requests.http) | book_id로 선택한 글 배열 | [03_guestbook_get](03_guestbook_get/index.html) |
| 04 방명록 저장 | [04_guestbook_post/requests.http](04_guestbook_post/requests.http) | 201의 새 id와 후속 GET | [04_guestbook_post](04_guestbook_post/index.html) |
| 05 수정·삭제 | [05_guestbook_edit/requests.http](05_guestbook_edit/requests.http) | 선택한 id의 변경·삭제 여부 | [05_guestbook_edit](05_guestbook_edit/index.html) |
| 06 통합 실험 | [06_http_lab/requests.http](06_http_lab/requests.http) | 조건을 바꾼 응답과 실제 데이터의 차이 | [06_http_lab](06_http_lab/index.html) |
| 07 완성 방명록 | [07_guestbook_complete/requests.http](07_guestbook_complete/requests.http) | 등록·조회·수정·삭제 후 같은 ID 재조회 | [07_guestbook_complete](07_guestbook_complete/index.html) |

각 폴더는 `index.html`, `app.js`, `config.example.js`, `requests.http`, `.env.example`을 자체 보유한다.
각 폴더의 README에 조작·응답·설정 방법을 둔다. W3.CSS는 cdnjs 4.1.0 CDN에서 읽으므로 인터넷 연결이 필요하다.
예를 들어 01은 [자신의 설정](01_about/config.example.js)을 읽는다. 상위 폴더의 파일에 의존하지 않는다.
06에는 [request.js](06_http_lab/request.js), [exercise.js](06_http_lab/exercise.js), [request.test.mjs](06_http_lab/request.test.mjs)가 더 있다.
예제 목차는 이 README다. 원하는 폴더 하나만 복사하거나 Pages에 게시할 수 있다.

## 화면 주소와 API 주소

| 구분 | 주소 | 역할 |
|---|---|---|
| 로컬 화면 | `http://localhost:8000/` | 내 PC에서 HTML·CSS·JavaScript 미리보기 |
| 배포한 화면 | GitHub Pages가 제공하는 `https://…github.io/…/` | 학생에게 공유할 웹페이지 |
| 공용 API | `https://esoqbcwgzjtwcqszwvin.supabase.co` | Supabase의 안내·방명록 API |
| 선택 로컬 API | `http://127.0.0.1:8787` | 로컬 리허설용 모의 API |

로컬 화면을 HTTP로 열어도 공용 API에는 HTTPS로 요청한다. 페이지 주소는 HTTP로 유지되고 데이터 요청만 HTTPS를 쓴다.
GitHub Pages에서는 화면과 API 모두 HTTPS를 쓴다.
현재 각 폴더의 `config.example.js`는 위 공용 Supabase 주소를 가리킨다. publishable key는 파일에 없고 처음 열 때 [입력해 브라우저에 저장](#공개-키-입력과-지우기)한 값을 읽는다.
공용 API를 사용하면 `tools/guestbook-api/server.mjs`를 실행할 필요가 없다.
HTTP 메서드·HTTP 상태라는 용어는 HTTPS 요청에도 그대로 사용한다.
2026-11-14에 `http://localhost:8000/01_about/`와 `/02_help/` 화면에서 실제 Supabase HTTPS GET 200과 페이지 오류 없음을 확인했다.

## 공용 API를 사용하며 로컬에서 화면 미리보기

현재 폴더: 저장소 루트 `teaching_repo`. Node.js 24 이상을 사용한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/specials/supabase_guestbook/examples 8000
```

브라우저에서 `http://localhost:8000/`을 열면 자동 폴더 목록이 나온다.
01을 바로 열 주소는 `http://localhost:8000/01_about/`, 완성 방명록은 `http://localhost:8000/07_guestbook_complete/`이다.
위 Node 명령은 화면 파일만 제공한다. API 요청은 실행한 폴더의 설정에 지정한 서버로 보낸다.

## 공개 키 입력과 지우기

공개 키는 `config.example.js`에 적지 않는다. 설정 파일의 `const API_PUBLIC_KEY = localStorage.getItem("API_PUBLIC_KEY") || "";` 줄이 이 브라우저에 저장한 값을 읽는다.
localStorage에 키가 없으면 예제 화면을 처음 열 때 `공개 키(publishable key)를 입력하세요.`라고 묻는 창이 뜬다.
강의자가 배부한 공개 키를 넣으면 설정 파일이 앞뒤 공백을 지우고 localStorage의 `API_PUBLIC_KEY`에 저장한다.
localStorage는 화면 주소의 출처(프로토콜·호스트·포트)마다 따로 저장된다. 같은 주소의 01~07이 이 값을 함께 쓰므로 다음부터는 묻지 않는다.

- 창을 취소하거나 빈 칸으로 두면 키를 저장하지 않는다. 요청은 HTTP 401로 실패하고, 새로고침하면 다시 묻는다.
- 틀린 키를 넣으면 그 값이 저장되어 다시 묻지 않는다. 키를 잘못 넣었거나 학기에 키가 바뀌면 화면 제목 아래 **공개 키 지우기**를 누른다. 저장한 키를 지우고 새로고침하므로 묻는 창에 새 키를 넣는다. 저장소 파일은 고치지 않는다.
- 휴대폰도 같은 창에 키를 넣고, 바꿀 때는 같은 버튼을 쓴다.
- 다른 브라우저, 포트가 다른 `localhost`, `127.0.0.1`과 `localhost`처럼 이름이 다른 주소, GitHub Pages 주소, 휴대폰에서는 처음 한 번 묻는다.
- 자기 새 프로젝트로 연결하는 담당자는 `config.example.js`의 `API_BASE_URL`·`BOOK_ID`를 자기 값으로 바꾸고, **공개 키 지우기**를 누른 뒤 자기 프로젝트의 publishable key(`sb_publishable_...`)를 넣는다.
- 주소·`BOOK_ID`는 REST Client가 `.env`에서, 브라우저가 `config.example.js`에서 따로 읽는다. 공개 키도 REST Client가 `.env`에서, 브라우저가 localStorage에서 따로 읽으므로 `requests.http`용 키는 같은 폴더의 `.env`에 넣는다.

## 실험 순서

1. **01_about**: 접속 확인 버튼으로 `GET /rest/v1/about`을 보낸다. 200과 객체 한 개를 담은 배열을 확인한다.
2. **02_help**: 사용법 조회 버튼으로 `GET /rest/v1/help?order=step.asc`를 보낸다. 여섯 행에서 다음 요청의 method와 path를 찾는다.
3. **03_guestbook_get**: 배부받은 방명록 태그로 목록을 읽는다. `book_id=eq.student01`은 같은 태그의 글을 고르는 조건이다. 글이 없으면 `[]`이 정상이다.
4. **04_guestbook_post**: 별칭·메시지를 입력해 저장한다. 201 응답의 새 id를 기록하고 GET으로 같은 글을 확인한다.
5. **05_guestbook_edit**에서 글 ID를 선택해 이름·메시지를 수정한다. 삭제할 때는 목록 행의 **삭제**와 확인창을 차례로 누른다.
6. **06_http_lab** HTTP 콘솔에서 메서드·태그·글 번호·본문을 바꾼다. POST·PATCH는 **본문 예시 넣기**를 누른 뒤 한 조건만 바꿔 본다.
7. **07_guestbook_complete**에서 글을 등록한다. 글이 보이면 그 행의 **수정** 또는 **삭제**를 누른다. 수정은 **수정 저장**, 삭제는 글 번호 확인을 거친다.

about·help는 이 교재가 추가한 GET 전용 안내 API이며 두 요청에도 `apikey` 헤더가 필요하다.
POST는 book_id·name·message만 보낸다. id와 created_at은 서버가 만든다. 같은 POST를 반복하면 새 글이 더 생긴다.
PATCH 200의 배열이 비어 있거나 DELETE가 204여도 변경된 행이 없을 수 있다. 후속 GET으로 판단한다.
DELETE 204에는 JSON 본문이 없다.
05~07의 `.http` 후속 GET은 방금 수정·삭제한 글 ID를 다시 입력해 같은 대상을 조회한다.

공개 키로 모든 태그의 글을 조회·저장·수정·삭제할 수 있다. 태그는 학생별 글을 묶는 값이며, 수정·삭제 예제에서는 글 번호를 함께 지정한다. [학생용 API 안내](../../../tools/guestbook-api/student-guide.md)

## GitHub Pages에서 사용하기

1. 게시할 예제 폴더 하나를 고른다. 완성 방명록만 필요하면 `07_guestbook_complete`를 사용한다.
2. 선택한 폴더의 HTML·JavaScript·설정을 함께 게시한다. 그 폴더 설정의 API 주소가 공용 `https://` 주소인지, BOOK_ID가 맞는지 확인한다. 게시 파일에는 공개 키가 없다.
3. 해당 폴더가 Pages 게시 결과에 포함되도록 게시 대상을 정하고 **Settings → Pages → Enforce HTTPS**를 확인한다.
4. 발급된 HTTPS 화면 주소에서 선택한 예제를 연다. 처음 열면 공개 키를 묻는 창이 뜨므로 배부받은 키를 넣고, Network에서 공용 API 주소와 응답을 확인한다.
5. 다른 기기에서도 공개 키를 입력하고 같은 태그로 조회한다. 실험 글을 만들고 수정·삭제한 결과가 다른 기기의 목록에 반영되는지 확인한다.

GitHub Pages가 정적 파일을 제공하므로 학생이 Node 서버를 실행할 필요가 없다.
Pages 주소에는 로컬 미리보기에서 저장한 키가 없다. 묻는 창에 키를 입력하지 않은 방문자는 401로 조회가 실패한다.
각 HTML은 같은 폴더의 `config.example.js`와 W3.CSS CDN을 읽는다. 다른 단계나 examples 루트의 파일은 필요 없다.
학습용 `requests.http`·`.env.example`은 함께 배부할 수 있다. 06의 실행에는 `request.js`·`exercise.js`도 포함한다.
`localhost`·`127.0.0.1` API 주소는 방문자 각자의 PC를 가리킨다. Pages용 설정에는 공용 HTTPS 주소를 유지한다.
`.env`, `localfiles/`, DB 비밀번호는 게시 파일에서 제외한다.

공용 방명록 GET·POST와 안내 API GET을 확인했다. 로컬 01·02 브라우저 화면에서도 실제 공용 API 응답 200과 1행·6행을 확인했다.
Pages 실배포와 공용 PATCH·DELETE는 아직 검증하지 않았다.

## 선택 사항: 로컬 API 리허설

모의 API로 바꿀 때만 실습할 폴더의 `config.example.js`에서 `API_BASE_URL`을 `http://127.0.0.1:8787`로 바꾼다. 그 화면에서 **공개 키 지우기**를 누르고 묻는 창에 `classroom-local`을 넣는다. REST Client는 같은 폴더의 `.env`도 같은 서버로 설정한다.
저장한 키는 같은 주소의 다른 폴더도 함께 쓴다. 리허설 중에는 주소를 바꾸지 않은 폴더의 공용 API 요청이 401로 실패한다.

화면 미리보기와 별도 터미널에서 `node web_programming/tools/guestbook-api/server.mjs`를 실행한다.
로컬도 `/rest/v1/about`·`/rest/v1/help`부터 같은 순서로 진행한다. 로컬 API에는 SQL을 실행하지 않는다.
이때만 화면과 API를 모두 내 PC의 HTTP 주소로 사용한다. 리허설 후 주소를 공용 HTTPS 주소로 되돌리고, **공개 키 지우기**를 누른 뒤 배부받은 공개 키를 다시 넣는다.
키를 되돌리지 않으면 01~07의 공용 API 요청이 401로 실패한다.
로컬 성공을 실제 Supabase SQL·게이트웨이·다른 기기 검증 완료로 표시하지 않는다.

## 학생 확장 과제와 검증

[06_http_lab/exercise.js](06_http_lab/exercise.js)의 `describeObservation(method, status, responseText)`는 기본 안내만 반환한다.
PATCH의 빈 배열, POST의 새 ID, DELETE 뒤 GET 필요 여부를 구별하도록 확장한다.
실험 기록은 메서드·입력·예상·응답·후속 GET·설명 순서로 남긴다. 자동 재조회가 무한 반복되지 않게 한다.

현재 폴더: 저장소 루트.

```powershell
node --test web_programming/specials/supabase_guestbook/examples/06_http_lab/request.test.mjs
```

이 검사는 통합 요청 구성과 화면 처리만 확인한다. 실제 Supabase 검증은 [서버 안내](../../../tools/guestbook-api/README.md#공용-서버-검증)를 따른다.
정규 수업 화면은 [12주 GET](../../../weeks/week12_fetch_json/examples/day2/web-week12/guestbook.html)·[13주 방명록 CRUD](../../../weeks/week13_guestbook_crud/examples/day2/web-week13/guestbook.html)·[14주 수정·삭제](../../../weeks/week14_project_presentation/examples/day2/web-week14/guestbook.html)에 연결한다.

근거: [GitHub Pages 정적 호스팅](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages),
[GitHub Pages HTTPS 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https),
[브라우저에서 Supabase API 호출](https://supabase.com/docs/guides/api).
