# 강의자용 공용 방명록 API 준비

## 목차

- [수업과 서버의 역할](#수업과-서버의-역할)
- [학생에게 배부할 자료](#학생에게-배부할-자료)
- [소개·도움말 API 추가](#소개도움말-api-추가)
- [로컬 리허설](#로컬-리허설)
- [Supabase 공용 서버 준비](#supabase-공용-서버-준비)
- [요청과 응답](#요청과-응답)
- [공용 서버 검증](#공용-서버-검증)
- [운영 범위](#운영-범위)

## 수업과 서버의 역할

12주는 GET으로 읽고, 13주는 POST로 저장하고, 14주는 PATCH·DELETE로 고친다.
강의자가 서버와 방명록 번호를 준비한다. 학생은 Supabase 가입이나 SQL 작성 없이
브라우저의 `fetch`와 화면 구현을 연습한다. SDK나 npm 패키지는 필요 없다.

이 폴더는 실행 가능한 로컬 API와 공용 Supabase 설치 SQL을 제공한다.
`server.mjs`는 선택 사항인 로컬 모의 API다. 공용 Supabase를 사용할 때는 실행하지 않아도 된다.
`provision.mjs`는 학생 태그 등록 SQL과 편집 키를 생성하는 준비 도구다.
강의용 프로젝트 `db_api_study`의 주소는 `https://esoqbcwgzjtwcqszwvin.supabase.co`다.
2026-11-13에 공용 서버의 GET 조회와 POST 저장을 확인했다. 수정·삭제 등 남은 검증 항목은 아래에 기록했다.
방학 연구 수업에서는 [Supabase API 구축 특강](../../specials/supabase_guestbook/README.md)의 단계와 비교 실험을 따른다.
학생 또는 소그룹의 프로젝트 담당자가 이 폴더의 SQL과 도구를 재사용한다.

## 학생에게 배부할 자료

[학생용 공용 방명록 API 사용 안내](student-guide.md)에 접속 주소, 설정 세 값, GET·POST 문법과 `fetch` 예제를 모았다.
이 안내와 프로젝트의 publishable key, 개인별 `BOOK_ID`를 배부한다. 현재 공용 서버에서 등록을 확인한 태그는 `student01`, `student02`다.
추가 태그는 아래 등록 절차를 거친 뒤 배부한다.
특강 예제는 [01~07 폴더별 안내](../../specials/supabase_guestbook/examples/README.md)를 따른다. examples 루트에는 README만 둔다.
각 폴더는 자체 `config.example.js`·`styles.css`를 가지므로 하나만 별도로 배포할 수 있다.
완성 화면은 [07 방명록](../../specials/supabase_guestbook/examples/07_guestbook_complete/index.html), 요청 문법은 [07 requests.http](../../specials/supabase_guestbook/examples/07_guestbook_complete/requests.http)에서 확인한다.

강의자는 [프로젝트 Data API](https://supabase.com/dashboard/project/esoqbcwgzjtwcqszwvin/integrations/data_api/overview)에서
**Docs → Tables and Views → guestbook**을 선택해 자동 생성된 문서를 확인할 수 있다.
HTTP 요청 형식은 **cURL** 탭에서 확인한다. 학생에게는 계정 접근이 필요 없는 위 사용 안내를 배부한다.
메뉴 안내의 근거는 [Supabase 자동 생성 문서](https://supabase.com/docs/guides/api/rest/auto-generated-docs)다.

## 소개·도움말 API 추가

방명록을 다루기 전에 `GET /rest/v1/about`으로 접속을 확인하고 `GET /rest/v1/help`로 API 사용법을 읽는다.
기존 공용 프로젝트에는 SQL Editor에서 [about-help.sql](about-help.sql)을 추가 실행한다.
새 프로젝트는 `schema.sql` 실행 후 이 파일을 실행한다. 기존 프로젝트의 `schema.sql`을 다시 실행하지 않는다.
이 SQL은 고정 안내를 반환하는 `about`, `help` 뷰와 조회 권한만 설정하며 방명록 데이터와 편집 키는 변경하지 않는다.

2026-11-14에 공용 Supabase에 SQL을 적용하고 두 경로의 GET 200을 확인했다.
about은 version이 v1인 한 행, help는 `order=step.asc`로 단계 1~6의 여섯 행을 반환한다.
설치 후 [01 접속 확인 요청](../../specials/supabase_guestbook/examples/01_about/requests.http)과
[02 도움말 요청](../../specials/supabase_guestbook/examples/02_help/requests.http)을 VS Code REST Client로 보낸다.
각 폴더의 `.env.example`을 같은 폴더의 `.env`로 복사해 프로젝트 주소와 공개 키를 설정한 뒤 **Send Request**를 누른다.
200과 JSON 배열을 확인한 다음 같은 폴더의 HTML 예제로 진행한다.
REST Client 요청은 브라우저 CORS 검증과 별개다. 이후 로컬 화면과 Pages 화면에서도 확인한다.

## 로컬 리허설

Node.js 24 이상에서 이 폴더를 열고 실행한다.

```powershell
node server.mjs
```

로컬 API 주소는 `http://127.0.0.1:8787`이다. 학생용 웹페이지는 별도 터미널에서
`web_programming/tools/static-server/server.mjs`로 `http://localhost:8000/`에 연다.
두 서버의 역할은 각각 데이터 처리와 화면 파일 제공이다.
로컬 HTTP 화면에서 공용 Supabase HTTPS API를 호출할 수도 있다. 이 경우 화면 주소는 HTTP로 유지되고 API 요청만 HTTPS를 사용한다.
로컬 API를 연습할 예제의 `config.example.js`를 아래 값으로 설정한다.
Supabase 특강 예제는 현재 공용 HTTPS 주소로 설정되어 있으므로 로컬 연습 때만 전환한다.

```js
const API_BASE_URL = 'http://127.0.0.1:8787';
const API_PUBLIC_KEY = 'classroom-local';
const BOOK_ID = 'student01';
```

첫 실행에 `student01`부터 `student30`까지 각 한 개의 안내 글이 생긴다.
글은 `.local/local-data.json`에 저장되어 서버를 다시 시작해도 남는다.
14주 편집 키는 `.local/local-edit-keys.json`에서 해당 번호의 값만 학생에게 별도 배부한다.
터미널에 키를 출력하지 않는다. 이 서버는 루프백에서만 수신하므로 다른 PC·휴대폰은 접속할 수 없다.
다른 기기 확인은 아래 공용 HTTPS 서버 준비 후 수행한다.

```powershell
node --test server.test.mjs
```

이 서버는 수업에 쓰는 REST 요청만 재현한다. PostgREST 전체 구현이나 인터넷 공개용 서버가 아니다.
수정·삭제에는 `book_id`와 `id`를 모두 요구하며, 이 제한은 로컬 리허설의 추가 보호다.

## Supabase 공용 서버 준비

1. 정규 공용 API는 강의자 계정으로, 연구 특강은 학생 또는 소그룹 담당자 계정으로 **전용 새 프로젝트**를 만든다. 기존 방명록이 있는 프로젝트에 덮어쓰지 않는다.
2. SQL Editor에서 [schema.sql](schema.sql)을 한 번 실행하고 [about-help.sql](about-help.sql)을 실행한다. 기존 방명록이 설치된 프로젝트에는 `about-help.sql`만 추가 실행한다.
3. 다음 명령으로 배부할 실습 번호의 편집 키와 등록 SQL을 만든다. 실명·학번은 번호로 쓰지 않는다.

   ```powershell
   node provision.mjs student01 student02 student03
   ```

4. 생성된 `.local/cloud-books.sql`을 SQL Editor에서 실행한다. 키의 해시만 DB에 저장된다.
5. 프로젝트 URL과 **publishable key**를 학생에게 배부한다. 학생은 예제의 `API_BASE_URL`, `API_PUBLIC_KEY`, `BOOK_ID` 세 줄을 바꾼다.
6. 14주에는 `.local/cloud-edit-keys.json`의 해당 번호 키만 따로 배부한다. 학생은 웹 화면의 편집 키 칸에 입력한다. 키는 JavaScript 메모리에서만 사용하고 소스 파일에 적지 않는다.
7. 아래 검증을 완료한 뒤 수업 주소로 공지한다.

`private` 스키마는 Data API의 Exposed schemas에 추가하지 않는다.
두 테이블 모두 RLS를 켠다. `private.classroom_books`에는 클라이언트용 허용 정책을 만들지 않는다.
편집 키 검사 함수는 테이블과 같은 소유자의 권한으로 등록된 해시를 읽는다.
`schema.sql`은 공개 조회·추가와 방명록별 편집 권한을 분리한다.
`book_id`는 글을 묶는 번호다. 권한은 요청의 `X-Edit-Key`를 해시로 비교하는 RLS 정책이 검사한다.
이름과 메시지만 수정할 수 있고 `id`, `book_id`, `created_at`은 학생이 바꿀 수 없다.
테이블 권한을 먼저 회수한 뒤 수정 가능한 열만 허용한다. 함수와 identity sequence의 기본 권한도 회수해 프로젝트 기본 설정에 의존하지 않는다.

브라우저에는 publishable key만 둔다. secret key와 service_role key는 이 수업에 필요 없다.
`.local/`은 Git에서 제외되어 있다. 편집 키 파일을 자료 배포 ZIP이나 화면 공유에 포함하지 않는다.

## 요청과 응답

모든 요청은 `apikey: <publishable key>` 헤더를 쓴다. 로컬 리허설 값은 `classroom-local`이다.

| 동작 | 주소·메서드 | 본문과 응답 |
|---|---|---|
| 접속 확인 | `GET /rest/v1/about` | 200, `name`, `version`, `description`, `help_path`가 있는 객체 한 개의 배열 |
| 사용법 조회 | `GET /rest/v1/help` | 200, `step`, `method`, `path`, `description`이 있는 배열. 순서는 `?order=step.asc`로 지정 |
| 읽기 | `GET /rest/v1/guestbook?book_id=eq.student01&select=id,name,message,created_at&order=id.desc&limit=50` | 200, 글 객체의 배열 |
| 저장 | `POST /rest/v1/guestbook` | `{book_id,name,message}`, `Prefer: return=representation`이면 201과 배열 |
| 수정 | `PATCH /rest/v1/guestbook?book_id=eq.student01&id=eq.123` | `{message}`, 편집 키와 `Prefer: return=representation`, 200과 배열 |
| 삭제 | `DELETE /rest/v1/guestbook?book_id=eq.student01&id=eq.123` | 편집 키, 204와 빈 본문 |

POST·PATCH에는 `Content-Type: application/json`, PATCH·DELETE에는 `X-Edit-Key`가 필요하다.
`about`과 `help`는 조회 전용이며 방명록 태그나 편집 키가 필요 없다. 공통 `apikey` 헤더는 필요하다.
이름은 공백을 제외한 내용이 있어야 하며 30글자 이하, 메시지는 500글자 이하다. 길이는 앞뒤 공백을 포함한 전체 문자를 센다.
없는 글 또는 편집 권한이 없는 글을 수정하면 배열이 비어 있을 수 있다. 삭제는 204여도
바뀐 행이 없을 수 있다. 성공 번호만으로 수정·삭제를 판단하지 말고 GET으로 대상 글을 다시 확인한다.
204에는 JSON 본문이 없으므로 `response.json()`을 호출하지 않는다.

## 공용 서버 검증

로컬 자동 시험은 저장·조회·재시작 후 유지·잘못된 입력·다른 학생 키의 수정/삭제 거부를 검사한다.
SQL과 Supabase 게이트웨이의 실제 동작은 별도 공용 프로젝트에서 다음과 같이 확인한다.

1. 12주 예제의 GET으로 student01 목록을 확인한다. Network에서 HTTPS 주소와 200을 확인한다.
2. 13주 예제로 테스트 글을 POST한다. 201 응답의 `id`를 기록하고 다른 기기에서 GET으로 같은 글을 확인한다.
3. 14주 예제에서 student02의 편집 키로 그 글을 수정·삭제한다. 다시 읽어 원래 글이 남는지 확인한다.
4. student01의 키로 수정하고 GET으로 변경을 확인한다. 이어 삭제하고 GET으로 사라졌는지 확인한다.
5. localhost와 GitHub Pages 양쪽에서 CORS 사전 요청과 실제 요청이 성공하는지 확인한다. 특히 `X-Edit-Key` 헤더를 포함한 PATCH·DELETE를 확인한다.
6. 한글, 빈 입력, 500글자 초과, 틀린 공개 키를 확인한다. 공개 키 오류와 수정 권한에 의한 빈 결과를 구분한다.
7. 올바른 편집 키라도 `id`, `book_id`, `created_at` 변경이 거부되는지 확인한다. 편집 키 없이도 모든 방명록 조회·추가는 허용되며, 다른 방명록의 수정·삭제만 제한한다.

2026-11-13 검증에서는 공용 서버 GET 200과 사용자 실습의 POST 저장 후 재조회를 확인했다.
`http://localhost:8000` Origin의 GET 및 OPTIONS CORS 응답도 확인했다.
2026-11-14에는 about·help GET 200과 `http://localhost:8000` Origin의 허용 응답을 확인했다.
격리 Chrome의 로컬 01·02 화면에서도 실제 Supabase HTTPS 응답 200, JSON 1행·6행, 도움말 목록 6개를 확인했다.
이 브라우저 검증은 `127.0.0.1` 임시 포트에서 수행했으며 CORS·버튼 복구가 정상이고 페이지 오류는 없었다.
독립 폴더로 나눈 뒤에도 `http://localhost:8000/01_about/`와 `/02_help/`에서 각 폴더 설정·스타일을 읽고 실제 HTTPS API GET 200, 페이지 오류 없음을 확인했다.
공용 서버 PATCH·DELETE 권한, 다른 기기와 GitHub Pages에서의 접속, 잘못된 입력과 보호 열 변경 거부는 아직 검증하지 않았다.
로컬 자동 시험 통과를 이 항목들의 공용 서버 검증 완료로 표시하지 않는다.

## 운영 범위

모든 방명록은 누구나 읽고 새 글을 남길 수 있는 수업용 공개 데이터다.
편집 키는 해당 방명록 전체의 편집 권한이며 개인 로그인이나 작성자 인증이 아니다.
개인정보 대신 별칭과 연습 문장을 쓴다. 여러 학생이 같은 방명록 번호를 쓰면 같은 데이터가 보인다.
학기 종료 후 쓰기 권한을 닫거나 프로젝트를 정리하는 일은 강의자가 수행한다.

무료 프로젝트의 휴면 정책과 용량은 개강 전에 [요금제](https://supabase.com/pricing)에서 확인한다.
서버 중단 시 로컬 리허설로 요청 문법을 연습할 수 있지만, 기기 간 공유 검증은 대체하지 못한다.

구현 근거: [Data REST API](https://supabase.com/docs/guides/api),
[API 키](https://supabase.com/docs/guides/getting-started/api-keys),
[요청 헤더와 RLS](https://supabase.com/docs/guides/api/securing-your-api),
[열 권한](https://supabase.com/docs/guides/database/postgres/column-level-security),
[함수 권한](https://supabase.com/docs/guides/database/functions).
