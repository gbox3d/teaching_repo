# 구축 따라하기 · Supabase 공용 방명록 API 구축

## 목차

- [0. 강의자 안내 API 준비](#0-강의자-안내-api-준비)
- [1. 작업 환경과 담당자](#1-작업-환경과-담당자)
- [2. 화면 실행과 로컬 리허설](#2-화면-실행과-로컬-리허설)
- [3. 새 Supabase 프로젝트](#3-새-supabase-프로젝트)
- [4. 정본 SQL 읽기와 적용](#4-정본-sql-읽기와-적용)
- [5. 수업용 방명록 태그 확인](#5-수업용-방명록-태그-확인)
- [6. 프로젝트 URL과 공개 키](#6-프로젝트-url과-공개-키)
- [7. 실험 화면의 클라우드 설정](#7-실험-화면의-클라우드-설정)
- [8. 접속 확인부터 방명록 저장까지](#8-접속-확인부터-방명록-저장까지)
- [9. 수정·삭제와 통합 실험](#9-수정삭제와-통합-실험)
- [10. 완성 방명록과 정규 예제 연결](#10-완성-방명록과-정규-예제-연결)
- [11. 다른 기기와 권한 검증](#11-다른-기기와-권한-검증)
- [12. 기록과 다음 모임 준비](#12-기록과-다음-모임-준비)

시간을 고정하지 않고 단계마다 실제 결과를 확인한다. 준비가 끝난 조는 [비교 실험](lab.md)으로 넘어간다.
현재 예제는 강의자 공용 HTTPS API로 설정되어 있으며 공용 서버 GET·POST를 확인했다.
공용 API를 사용하는 학생은 2단계에서 화면을 연 뒤 8단계로 이동한다. 3~7단계는 자신의 새 프로젝트를 구축할 때 수행한다.
이 실험 화면의 GitHub Pages 실배포와 공용 서버 PATCH·DELETE는 아직 검증하지 않았다. 실행 결과를 연구 기록에 구분한다.

## 0. 강의자 안내 API 준비

01·02 예제는 `/rest/v1/about`·`/rest/v1/help`를 읽는다. 2026-11-14에 공용 프로젝트 설치와 두 GET의 200 응답을 확인했다.
about은 version이 v1인 한 행, help는 단계 1~6의 여섯 행을 반환한다. 로컬 01·02 브라우저 화면에서도 같은 응답을 확인했다.
- 새 프로젝트에서는 [schema.sql](../../tools/guestbook-api/schema.sql)을 실행한다. 테이블과 `student01`~`student30` 태그 30개가 생긴다. 이어서 [about-help.sql](../../tools/guestbook-api/about-help.sql)을 실행해 접속 확인과 도움말 경로를 추가한다.
- 기존 수업 프로젝트에서는 [enable-public-crud.sql](../../tools/guestbook-api/enable-public-crud.sql)을 SQL Editor에서 한 번 실행한다. 기존 글과 태그를 유지하면서 공개 수정·삭제 정책과 도움말을 갱신한다.

공용 API를 사용하는 학생에게는 프로젝트 URL·공개 키·실습 태그만 배부한다.
안내 API도 `apikey` 헤더가 필요하며 GET 전용이다. URL 주소창만 열어서는 이 헤더가 전달되지 않는다.

## 1. 작업 환경과 담당자

개인 또는 소그룹마다 프로젝트 담당자를 정한다. 담당자는 자신의 새 연습 프로젝트에서 SQL을 실행한다.
다른 서비스나 정규 수업 공용 서버가 들어 있는 프로젝트는 사용하지 않는다.
학생 계정이 없으면 강의자 구축 시연을 보고 공용 API에서 요청 실험을 계속한다.

별도 작업 폴더가 필요한 경우 아래처럼 교재를 clone한다. 기존 작업물을 덮어쓰지 않는다.
현재 폴더: 새 폴더를 만들 상위 작업 디렉터리.

```powershell
git clone https://github.com/gbox3d/teaching_repo.git supabase-study-team01
cd supabase-study-team01
node --version
```

이후 명령의 현재 폴더는 모두 이 교재 저장소 최상위다. Node.js 24 이상을 사용한다.
`npm install`이나 Supabase SDK 설치는 필요 없다.

VS Code에서 REST Client 확장을 준비한다. 각 단계에 `.env`가 없으면 해당 폴더의 `.env.example`을 `.env`로 복사하고 공개 키를 설정한다.
`.env`는 `requests.http`와 같은 폴더에 둔다. 01 요청의 **Send Request**를 눌러 상태 번호와 JSON을 확인하고 다음 절의 브라우저 화면으로 이동한다.
`.http` 요청 자체에는 Node 정적 서버가 필요 없다. 공개 키는 REST Client가 각 폴더의 `.env`에서, 브라우저가 localStorage에서 따로 읽는다.
절차와 출처는 [REST Client 첫 실습](examples/README.md#rest-client로-요청부터-확인하기)에 있다.

## 2. 화면 실행과 로컬 리허설

먼저 특강 실험 화면을 로컬 정적 서버로 연다. 현재 폴더는 교재 저장소 최상위다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/specials/supabase_guestbook/examples 8000
```

브라우저에서 `http://localhost:8000/`을 열면 자동 폴더 목록이 표시된다. 예제 목차는 [examples/README.md](examples/README.md)에 있다.
현재 각 폴더의 설정은 `https://esoqbcwgzjtwcqszwvin.supabase.co`의 공용 API를 가리킨다. [01의 설정 파일](examples/01_about/config.example.js)을 기준으로 확인한다.
화면 주소는 로컬 HTTP로 유지되고 데이터 요청은 Supabase HTTPS를 사용한다. Node 정적 서버는 화면 파일만 제공한다.
[01_about](examples/01_about/index.html)은 `http://localhost:8000/01_about/`에서 바로 연다. 상세 진행은 8단계의 01부터 따른다.
처음에는 접속 확인만 수행하고 안내 조회·방명록 실습을 차례로 연다.

공개 키는 설정 파일에 없다. 01 화면을 처음 열면 공개 키를 묻는 창이 뜬다. 배부받은 공개 키를 넣으면 `config.example.js`가 앞뒤 공백을 지워 localStorage의 `API_PUBLIC_KEY`에 저장하고, 다음 한 줄로 그 값을 읽는다.

```js
const API_PUBLIC_KEY = localStorage.getItem("API_PUBLIC_KEY") || "";
```

같은 `http://localhost:8000`의 01~07은 이 값을 함께 쓰므로 다음부터 묻지 않는다. 창을 취소하거나 빈 칸으로 두면 401이 오고, 새로고침하면 다시 묻는다.
키를 잘못 넣었거나 학기에 키가 바뀌면 화면 제목 아래 **공개 키 지우기**를 누르고 새 키를 넣는다. 다시 묻는 주소와 자세한 절차는 [공개 키 입력과 지우기](examples/README.md#공개-키-입력과-지우기)에 있다.

선택 리허설로 로컬 API를 사용하려면 실습할 폴더의 `config.example.js`에서 `API_BASE_URL`을 `http://127.0.0.1:8787`로 바꾸고, 그 화면에서 **공개 키 지우기**를 누른 뒤 묻는 창에 `classroom-local`을 넣는다. 다른 폴더의 주소는 자동으로 바뀌지 않는다.
저장한 키는 같은 주소의 다른 폴더도 함께 쓰므로, 주소를 바꾸지 않은 폴더는 401로 실패한다.

이때만 별도 터미널에서 로컬 API 서버를 실행한다.

```powershell
node web_programming/tools/guestbook-api/server.mjs
```

브라우저를 새로고침한 뒤 확인할 결과:

- API는 `http://127.0.0.1:8787`, 페이지는 `http://localhost:8000/`에서 실행된다.
- 01·02는 같은 `/rest/v1/about`·`/rest/v1/help` 경로에서 안내 배열을 읽는다. 로컬에는 SQL 실행이 필요 없다.
- GET 200에 JSON 배열이 온다. 로컬 첫 실행에는 student01~student30에 안내 글이 준비된다.
- POST가 성공하면 서버 id가 붙는다. GET으로 같은 글을 다시 찾는다.
- `127.0.0.1`은 각 기기 자신이다. 이 결과로 다른 PC·휴대폰 연결을 확인한 것은 아니다.

사용 중인 포트가 겹치면 해당 서버 터미널에서 Ctrl+C로 중지한 뒤 다시 시작한다.
로컬 리허설을 마치면 `API_BASE_URL`을 공용 주소로 되돌리고, **공개 키 지우기**를 누른 뒤 배부받은 공개 키를 다시 넣는다.
같은 주소의 01~07이 저장값을 함께 쓰므로 키를 되돌리지 않으면 공용 API 요청이 401로 실패한다.
공용 API 사용 중에는 로컬 API 서버를 중지해도 된다. 로컬 화면을 계속 볼 때는 정적 서버만 사용한다.

## 3. 새 Supabase 프로젝트

프로젝트 담당자가 [Supabase 대시보드](https://supabase.com/dashboard)에 직접 로그인한다.
계정과 프로젝트 생성은 실제 서비스 사용 조건을 확인한 담당자가 수행한다.

1. 무료 범위에서 사용할 조직과 프로젝트 수를 [공식 요금제](https://supabase.com/pricing)로 확인한다.
2. 새 연습 프로젝트를 만든다. 이름은 `guestbook-study-team01`처럼 실명·학번을 포함하지 않는 이름을 사용한다.
3. 데이터베이스 비밀번호는 담당자가 별도로 보관한다. 웹 예제에는 쓰지 않는다.
4. 사용 가능한 가까운 리전을 선택하고 프로젝트 준비 완료를 기다린다.
5. 프로젝트 이름과 URL을 확인한다. 정규 수업 서버나 다른 서비스가 아님을 확인한 뒤 SQL 단계로 넘어간다.

이미 가진 프로젝트 수 때문에 새 무료 프로젝트를 만들 수 없다면 유료 전환을 진행하지 않는다.
강의자 시연·공용 API 실습으로 이어 가거나 그룹별 프로젝트 배치를 조정한다.

## 4. 정본 SQL 읽기와 적용

VS Code에서 [tools/guestbook-api/schema.sql](../../tools/guestbook-api/schema.sql)을 연다.
특강 폴더의 옛 SQL을 복사하지 않고 이 정본을 사용한다. SQL 전문을 이 문서에 중복하지 않는다.

| 블록 | 확인할 내용 |
|---|---|
| private.classroom_books | 기본 태그 `student01`~`student30` 보관 |
| public.guestbook | 공개 글의 열과 이름·메시지 길이 제한 |
| guestbook.book_id 외래 키 | 등록된 태그로만 글 저장 |
| grant·revoke | 조회·추가·수정·삭제 명령과 수정 가능한 열 범위 |
| RLS 정책 | 수업 프로젝트의 공용 `anon` 역할에 조회·추가·수정·삭제 허용 |

프로젝트 담당자가 새 프로젝트의 SQL Editor에 정본 파일 전체를 붙여 넣고 한 번 실행한다.
이어서 [about-help.sql](../../tools/guestbook-api/about-help.sql)을 실행해 01·02에서 읽을 안내 API를 추가한다.
현재 파일은 새 테이블을 만드는 설치 스크립트다. 같은 프로젝트에 반복 실행하는 갱신 스크립트가 아니다.
이미 존재한다는 오류가 나면 테이블을 지우거나 SQL 일부를 생략하지 말고 대상 프로젝트와 이전 실행 여부를 확인한다.

확인할 결과:

- `public.guestbook`에 id·book_id·name·message·created_at 열이 있다.
- `private.classroom_books`에 30개의 `book_id`가 있고 RLS가 켜져 있다.
- `guestbook`에 RLS가 켜져 있고 조회·추가·수정·삭제 정책이 있다.
- Data API의 Exposed schemas에 `private`를 추가하지 않았다.

Table Editor나 SQL Editor의 관리자 화면은 브라우저의 공개 API와 권한이 다르다.
관리자 화면에서 행이 수정된 사실만으로 학생 API 권한이 올바르다고 판단하지 않는다.

## 5. 수업용 방명록 태그 확인

SQL Editor에서 다음 쿼리를 실행한다.

```sql
select book_id
from private.classroom_books
order by book_id;
```

새 프로젝트에서 `student01`부터 `student30`까지 30행이 나오면 학생에게 하나씩 배정한다. 기존 프로젝트에서는 조회된 태그 중 하나를 사용한다. 태그는 글을 묶는 값이다. 아직 쓴 글이 없으면 해당 태그의 방명록 GET 결과는 `[]`이다.

## 6. 프로젝트 URL과 공개 키

[공식 Data API 안내](https://supabase.com/docs/guides/api)의 현재 경로는 다음과 같다.
화면이 달라지면 공식 안내에서 경로를 다시 확인한다.

- API 주소: **Integrations › Data API**.
- API 키: **Settings › API Keys**의 publishable key.

프로젝트 URL은 `https://<프로젝트>.supabase.co` 형태의 기본 주소다.
`API_BASE_URL`에 `/rest/v1/guestbook`까지 붙이지 않는다. 예제 코드가 요청 경로를 덧붙인다.

[API 키 안내](https://supabase.com/docs/guides/getting-started/api-keys)를 보고 키의 역할을 구분한다.
`sb_publishable_...` 값은 `apikey` 헤더에 넣는다. 이 키를 `Authorization: Bearer`에 넣지 않는다.
서버 secret key·service_role key·데이터베이스 비밀번호는 이 예제에 필요 없다.
publishable key는 파일에 적지 않는다. 7단계에서 화면이 묻는 창에 넣으면 localStorage에 저장되고, 예제가 페이지를 열 때 그 값을 읽어 요청마다 `apikey` 헤더에 붙인다.

이 프로젝트의 공개 키는 수업 참여자가 함께 쓴다. **공개 키 지우기**를 누르면 예제에 저장한 값을 다시 입력할 수 있다.

## 7. 실험 화면의 클라우드 설정

사용할 폴더의 `config.example.js`에 6단계의 프로젝트 URL과 5단계에서 확인한 `BOOK_ID`를 넣는다. [01의 설정](examples/01_about/config.example.js)
01~07은 각자 설정을 가진 독립 폴더다. 여러 폴더를 같은 서버로 연결할 때는 사용할 폴더마다 주소와 번호를 맞춘다.
강의자 공용 API를 그대로 사용하면 현재 설정을 유지한다.
파일 이름은 그대로 두며 `config.js`로 이름을 바꾸지 않는다.

자기 프로젝트의 publishable key는 파일에 적지 않는다. 화면 제목 아래 **공개 키 지우기**를 누르고, 묻는 창에 6단계에서 확인한 자기 프로젝트의 키(`sb_publishable_...`)를 넣는다.
같은 주소의 01~07은 이 저장값을 함께 쓰므로, 공용 API를 쓰는 폴더로 돌아갈 때는 다시 **공개 키 지우기**를 누르고 배부받은 키를 넣는다.

정적 서버가 실행 중이면 브라우저를 새로고침한다.
Network에서 요청 주소가 `127.0.0.1:8787` 대신 자신의 HTTPS 프로젝트인지 확인한다.
같은 UI가 열렸다는 사실만으로 서버가 전환됐다고 판단하지 않는다.

## 8. 접속 확인부터 방명록 저장까지

### 01_about · 접속 확인

[01_about/index.html](examples/01_about/index.html)을 연다. 로컬 주소는 `http://localhost:8000/01_about/`이다.
먼저 [01 requests.http](examples/01_about/requests.http)로 같은 요청을 확인한 뒤 화면 버튼과 코드를 비교한다.
접속 확인 버튼으로 `GET /rest/v1/about`을 보낸다. 2단계에서 넣은 공개 키(자기 프로젝트는 7단계에서 넣은 키)가 요청의 `apikey` 헤더에 들어간다.
응답은 객체 한 개를 담은 배열이다. `name`, `version`, `description`, `help_path`를 확인한다.
`help_path`는 다음에 읽을 안내 경로다. 이 단계에서는 글을 저장하거나 수정하지 않는다.

Network에서 요청 주소와 200 응답을 확인한다. 404가 나오면 강의자의 about-help.sql 적용 여부를 먼저 확인한다.
401이 나오면 이 주소에서 공개 키를 넣었는지 확인한다. 창을 취소했으면 새로고침해 다시 넣고, 틀린 키를 넣었으면 **공개 키 지우기** 뒤 다시 넣는다.
방명록 GET이 성공한 사실만으로 새 안내 API까지 준비되었다고 판단하지 않는다.

### 02_help · 사용 안내 조회

[02_help/index.html](examples/02_help/index.html)에서 `GET /rest/v1/help?order=step.asc`를 보낸다.
이 단계도 [02 requests.http](examples/02_help/requests.http)에서 응답을 먼저 읽는다.
`step`, `method`, `path`, `description`을 가진 여섯 행이 배열로 온다.
`order=step.asc`는 안내를 단계 번호 순서로 정렬하는 조건이다.
help의 step은 요청 종류의 순서다. 예제 폴더 05에서는 안내의 PATCH와 DELETE를 함께 다룬다.
about과 help는 이 교재가 추가하는 안내 API이며 GET 전용이다. 두 응답을 읽은 뒤 방명록 실습으로 이동한다.

### 03_guestbook_get · 방명록 읽기

[03_guestbook_get/index.html](examples/03_guestbook_get/index.html)에서 준비한 방명록 번호를 조회한다.
먼저 [03 requests.http](examples/03_guestbook_get/requests.http)의 조회 요청을 실행한다.
요청 경로는 `/rest/v1/guestbook?book_id=eq.student01`이며 예제는 정렬·조회 수 조건도 붙인다.
`eq.`가 같은 값을 고르는 조건이라는 점과 글 객체가 배열에 담긴다는 점을 확인한다.

GET부터 실행한다. 아직 글을 쓰지 않았다면 정상 응답이 빈 배열 `[]`일 수 있다.
요청 주소와 응답 상태·본문을 [실험 기록](lab.md#실험-기록)에 남긴다.

### 04_guestbook_post · 방명록 저장

[04_guestbook_post/index.html](examples/04_guestbook_post/index.html)에서 이름과 메시지를 입력해 저장한다.
먼저 [04 requests.http](examples/04_guestbook_post/requests.http)의 POST와 후속 GET을 실행한다. 두 방식에서 같은 요청 구조를 찾는다.
POST의 본문에는 다음 필드만 사용한다. 실명 대신 별칭을 쓴다.

```json
{"book_id":"student01","name":"연습A","message":"클라우드에 저장하는 첫 글입니다."}
```

요청에는 `Content-Type: application/json`과 `Prefer: return=representation`을 사용한다.
성공 응답 201의 배열에서 서버 id를 확인하고 그 id를 기록한다. `created_at`도 서버가 만든다.
다시 GET해 같은 id·메시지를 찾는다. 화면에 로컬로 덧붙인 글과 서버 저장을 구별하는 단계다.

POST를 student02로 보내고 GET의 방명록 조건도 student02로 바꾸어 본다.
공개 키를 가진 사람은 다른 등록 태그의 글도 조회·저장·수정·삭제할 수 있다. 실습에서는 배정받은 태그와 직접 만든 글을 사용한다.

## 9. 수정·삭제와 통합 실험

### 05_guestbook_edit · 글 하나 수정·삭제

[05_guestbook_edit/index.html](examples/05_guestbook_edit/index.html)을 연다. 앞 단계에서 조회·저장한 경험을 이어서 사용한다.
[05 requests.http](examples/05_guestbook_edit/requests.http)에서는 변경하려는 글의 ID를 `entryId`에 입력한다. 브라우저에서는 다음 순서로 같은 요청을 보낸다.

1. 04에서 같은 태그로 실험용 글 두 개를 만든 뒤 05에서 목록을 조회한다.
2. 첫 번째 글의 ID를 선택하고 이름·메시지를 바꾼 뒤 **선택한 글 수정**을 누른다. PATCH 200의 배열과 후속 GET에 새 값이 있는지 확인한다.
3. 두 번째 글이 있는 행에서 **삭제**를 누른다. 확인창에 나온 태그와 글 번호를 읽고 삭제한다.
4. DELETE 204에는 응답 본문이 없다. 같은 태그와 글 번호로 GET을 보내 `[]`를 확인하고, 목록에서 첫 번째 글이 남아 있는지 살펴본다.

변경 URL에는 `book_id=eq.student01`과 `id=eq.<글 번호>`를 함께 넣는다. 조건에 맞는 행이 없어도 PATCH는 200과 `[]`, DELETE는 204를 반환할 수 있다.

### 06_http_lab · 요청 조건 비교

[06_http_lab/index.html](examples/06_http_lab/index.html)은 메서드·태그·글 번호·JSON 본문을 직접 지정해 요청하는 HTTP 콘솔이다.
같은 비교 요청의 출발점은 [06 requests.http](examples/06_http_lab/requests.http)다.
01~05를 확인한 뒤 사용한다. POST·PATCH는 **본문 예시 넣기**로 JSON을 준비하고 한 조건만 바꾼다.
`request.js`의 `buildRequest(method, book, id, bodyText)`가 요청을 만든다. 없는 ID, 다른 태그, 수정할 수 없는 열을 지정해 응답과 후속 GET을 비교한다.
세부 과제는 [실습지](lab.md), 실행 순서는 [예제 설명](examples/README.md#실험-순서)을 따른다.

## 10. 완성 방명록과 정규 예제 연결

[07_guestbook_complete](examples/07_guestbook_complete/index.html)는 목록·등록 폼·수정·삭제를 한 화면에 모은 완성 방명록이다.
[07 requests.http](examples/07_guestbook_complete/requests.http)로 요청을 확인하고 `http://localhost:8000/07_guestbook_complete/`을 연다.
태그를 정해 글을 등록한다. 행의 **수정**을 누르고 별칭·메시지를 바꿔 **수정 저장**을 누른다. 삭제할 때는 해당 행의 **삭제**를 누르고 확인창에서 글 번호를 확인한다. 같은 ID의 GET과 새 목록에서 결과를 확인한다.
07은 방명록 사용 흐름을 확인하는 화면이다. HTTP 메서드·JSON 본문을 직접 바꾸는 실험은 06을 사용한다.

실험 화면에서 API가 동작하면 정규 교재의 UI를 자신의 서버에 연결한다.
13주 완성본에서는 `guestbook.html` 옆의 `config.example.json`을 `config.json`으로 복사하고 7단계의 주소·공개 키·태그를 넣는다. 12주 선택 예제와 14주 완성본은 `config.example.js`의 `API_BASE_URL`과 `BOOK_ID`를 사용한다. 같은 `http://localhost:8000`에서 열면 이 두 예제는 7단계에서 브라우저에 저장한 공개 키를 함께 쓴다.

13주 화면을 확인할 때, 실행 중인 정적 서버를 Ctrl+C로 중지한 뒤 다음 명령을 실행한다.
현재 폴더: 교재 저장소 최상위.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week13_guestbook_crud/examples/day2/web-week13 8000
```

`http://localhost:8000/guestbook.html`에서 글 한 건을 저장하고 목록에서 글 번호를 찾는다. 그 글의 내용을 수정하고 같은 글 번호로 삭제한다.

14주 화면은 다음과 같이 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week14_project_presentation/examples/day2/web-week14 8000
```

같은 태그에서 실험용 글 하나를 수정하고 그 행의 삭제 버튼으로 지운다.
서버 id로 지정한 글만 바뀌는지 새로고침 후 확인한다.
실험 도구와 방명록 UI가 같은 API 계약을 사용한다는 것을 비교한다.

## 11. 다른 기기와 권한 검증

특강 화면 또는 방명록 UI의 필요한 파일만 별도 학생 저장소에 올리고 GitHub Pages를 설정한다.
01~07은 폴더 하나만 별도 저장소나 Pages 게시 폴더로 옮겨 사용할 수 있다.
선택한 폴더의 `index.html`, `app.js`, `config.example.js`를 함께 둔다. 06은 `request.js`·`exercise.js`도 포함한다.
HTML은 같은 폴더의 설정과 앱 파일을 읽는다. 완성 방명록만 배포하려면 07 폴더를 선택한다.
학습 자료로 `requests.http`·`.env.example`을 함께 배부할 수 있지만 실제 `.env`는 제외한다.
GitHub Pages가 정적 파일을 제공하므로 Node 정적 서버나 로컬 API 서버를 실행할 필요가 없다.

배포 후 발급된 HTTPS 페이지 주소로 접속한다. 브라우저는 화면 파일을 Pages에서 받고 데이터는 Supabase HTTPS API에 요청한다.
`config.example.js`에는 HTTPS API 주소와 `BOOK_ID`만 둔다. 로컬 리허설 주소가 남아 있지 않은지 확인한다.
게시 파일에는 공개 키가 없다. 게시한 주소를 처음 열면 공개 키를 묻는 창이 뜨고, 키를 넣어야 목록이 보인다. 키를 입력하지 않은 방문자는 401로 조회가 실패한다.
`localhost`·`127.0.0.1`은 방문자 기기를 가리킨다. 게시할 설정에는 공용 HTTPS API 주소를 넣는다.
정적 호스팅의 동작은 [GitHub Pages 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)를 참고한다.

공용 API의 GET·POST 확인과 이 화면의 Pages 배포 검증은 별개다. 다음 항목은 실제 배포한 뒤 확인한다.
새 안내 API SQL을 먼저 적용하고 배포 화면의 01·02에서 접속과 안내를 읽은 뒤 방명록 요청을 확인한다.
REST Client에서 성공해도 브라우저의 CORS 검증이 끝난 것은 아니다. `.env`는 Pages 게시 파일에 포함하지 않는다.

다른 PC·휴대폰에서 공개 페이지를 열면 그 브라우저에서도 처음 한 번 공개 키를 묻는다. 키를 넣은 뒤 다음 항목을 확인한다.
휴대폰에서 키를 잘못 넣었으면 같은 **공개 키 지우기** 버튼으로 지우고 다시 넣는다.

- 같은 방명록의 서버 id·메시지가 보이는지.
- 한 기기에서 추가한 글이 다른 기기의 GET에 나타나는지.
- 한 기기에서 수정·삭제한 결과가 다른 기기의 새로고침한 목록에도 보이는지.
- 같은 글 번호에 다른 태그를 지정하면 GET에서 빈 배열이 돌아오는지.
- PATCH로 id·book_id·created_at을 바꾸려고 할 때 서버가 거절하는지.
- localhost와 GitHub Pages 양쪽에서 CORS 사전 요청과 실제 요청이 성공하는지.


## 12. 기록과 다음 모임 준비

[실습지](lab.md)의 기록표를 작성하고 프로젝트 담당자·실행 환경·교재 커밋·성공한 단계·남은 항목을 남긴다.
교재 커밋은 저장소 최상위에서 확인한다.

```powershell
git rev-parse --short HEAD
```

실험 결과를 공유하기 전에 수정한 공개 파일과 Git 상태를 확인한다.
공개할 소스 파일과 실습용 `.env`를 구분해 게시 대상을 확인한다.
프로젝트와 데이터의 보존·쓰기 권한 변경·종료 여부는 담당자와 강의자가 별도로 정한다.
