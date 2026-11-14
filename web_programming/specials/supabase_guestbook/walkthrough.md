# 구축 따라하기 · Supabase 공용 방명록 API 구축

## 목차

- [0. 강의자 안내 API 준비](#0-강의자-안내-api-준비)
- [1. 작업 환경과 담당자](#1-작업-환경과-담당자)
- [2. 화면 실행과 로컬 리허설](#2-화면-실행과-로컬-리허설)
- [3. 새 Supabase 프로젝트](#3-새-supabase-프로젝트)
- [4. 정본 SQL 읽기와 적용](#4-정본-sql-읽기와-적용)
- [5. 방명록 번호와 편집 키 등록](#5-방명록-번호와-편집-키-등록)
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
강의자가 기존 프로젝트의 SQL Editor에서 [about-help.sql](../../tools/guestbook-api/about-help.sql)을 한 번 실행한다.
이 SQL은 안내용 읽기 전용 뷰를 추가하며 기존 방명록을 바꾸지 않는다. 기존 프로젝트에 schema.sql을 다시 실행하지 않는다.

새 프로젝트를 만드는 조는 4단계에서 schema.sql 다음에 about-help.sql을 실행한다.
공용 API를 사용하는 학생은 계정 생성·SQL 실행 없이 준비된 주소와 공개 키를 받는다.
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
조별로 별도 체크아웃을 사용하면 정본 도구가 생성하는 `.local/` 파일이 섞이지 않는다.

VS Code에서 REST Client 확장을 준비한다. 각 단계에 `.env`가 없으면 해당 폴더의 `.env.example`을 `.env`로 복사하고 공개 키를 설정한다.
`.env`는 `requests.http`와 같은 폴더에 둔다. 01 요청의 **Send Request**를 눌러 상태 번호와 JSON을 확인하고 다음 절의 브라우저 화면으로 이동한다.
`.http` 요청 자체에는 Node 정적 서버가 필요 없다. 각 폴더의 `.env` 설정과 브라우저용 `config.example.js` 설정은 별개다.
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

선택 리허설로 로컬 API를 사용하려면 실습할 폴더의 공개 설정 세 값을 보관하고 다음 값으로 바꾼다. 다른 폴더의 설정은 자동으로 바뀌지 않는다.

```js
const API_BASE_URL = 'http://127.0.0.1:8787';
const API_PUBLIC_KEY = 'classroom-local';
const BOOK_ID = 'student01';
```

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
로컬 리허설을 마치면 보관한 공용 설정으로 되돌리고 새로고침한다.
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
| private 스키마·classroom_books | 방명록 번호와 편집 키 해시를 보관 |
| public.guestbook | 공개 글의 열과 이름·메시지 길이 제한 |
| private.can_edit_book | X-Edit-Key를 SHA-256 해시로 바꾸어 등록값과 비교 |
| grant·revoke | 조회·추가·수정·삭제 명령과 수정 가능한 열 범위 |
| RLS 정책 | 조회·추가는 공개, 수정·삭제는 방명록 편집 키로 제한 |

프로젝트 담당자가 새 프로젝트의 SQL Editor에 정본 파일 전체를 붙여 넣고 한 번 실행한다.
이어서 [about-help.sql](../../tools/guestbook-api/about-help.sql)을 실행해 01·02에서 읽을 안내 API를 추가한다.
현재 파일은 새 테이블을 만드는 설치 스크립트다. 같은 프로젝트에 반복 실행하는 갱신 스크립트가 아니다.
이미 존재한다는 오류가 나면 테이블을 지우거나 SQL 일부를 생략하지 말고 대상 프로젝트와 이전 실행 여부를 확인한다.

확인할 결과:

- `public.guestbook`에 id·book_id·name·message·created_at 열이 있다.
- `private.classroom_books`에는 book_id·edit_key_hash 열이 있고 RLS가 켜져 있다. 클라이언트용 허용 정책은 만들지 않는다.
- `guestbook`에 RLS가 켜져 있고 조회·추가·수정·삭제 정책이 있다.
- Data API의 Exposed schemas에 `private`를 추가하지 않았다.

Table Editor나 SQL Editor의 관리자 화면은 브라우저의 공개 API와 권한이 다르다.
관리자 화면에서 행이 수정된 사실만으로 학생 API 권한이 올바르다고 판단하지 않는다.

## 5. 방명록 번호와 편집 키 등록

두 방명록을 등록하면 서로 다른 키를 비교할 수 있다.
현재 폴더: 교재 저장소 최상위.

```powershell
node web_programming/tools/guestbook-api/provision.mjs student01 student02
```

[provision.mjs](../../tools/guestbook-api/provision.mjs)는 Node.js 표준 모듈만 사용한다.
스크립트가 있는 폴더 아래에 다음 두 파일이 생긴다. 터미널의 현재 폴더에 생기는 파일이 아니다.

| 생성 파일 | 사용하는 곳 |
|---|---|
| `web_programming/tools/guestbook-api/.local/cloud-books.sql` | 새 프로젝트 SQL Editor에서 실행할 번호·해시 등록 SQL |
| `web_programming/tools/guestbook-api/.local/cloud-edit-keys.json` | 프로젝트 담당자가 별도로 보관·배부하는 편집 키 원문 |

SQL 파일을 열어 book_id와 해시만 들어 있는지 확인한 뒤, 같은 프로젝트 SQL Editor에서 한 번 실행한다.
키 JSON 파일은 SQL Editor에 붙여 넣지 않는다.
두 방명록 등록은 글을 생성하는 작업이 아니다. 아직 `guestbook`이 비어 있어도 정상이다.

생성기는 기존 배부 파일이 있으면 중단한다. 기존 파일을 지우고 다시 실행하면 이전에 배부한 키와 DB 해시가 달라질 수 있다.
다른 프로젝트를 추가로 연구할 때는 별도 체크아웃과 담당자를 사용한다. 키 변경·재배부 실험은 별도 계획으로 수행한다.

`.local/`은 Git에서 제외되지만 ZIP 도구가 자동으로 제외해 주는 것은 아니다.
예제 배포에는 필요한 화면 파일만 선택하고 `.local/`은 포함하지 않는다.

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

## 7. 실험 화면의 클라우드 설정

자신의 새 프로젝트로 연결할 때 사용할 폴더의 `config.example.js`에서 공개 값 세 줄을 바꾼다. 예: [01의 설정](examples/01_about/config.example.js).
01~07은 각자 설정을 가진 독립 폴더다. 여러 폴더를 같은 서버로 연결할 때는 사용할 폴더마다 값을 맞춘다.
강의자 공용 API를 그대로 사용하면 현재 설정을 유지한다.
파일 이름은 그대로 두며 `config.js`로 이름을 바꾸지 않는다.

```js
const API_BASE_URL = 'https://YOUR_PROJECT.supabase.co';
const API_PUBLIC_KEY = 'sb_publishable_YOUR_KEY';
const BOOK_ID = 'student01';
```

위 문자열은 자리표시자다. 실제 프로젝트 주소와 publishable key를 담당자가 입력한다.
편집 키는 이 파일에 쓰지 않는다. 수정·삭제 실험 때 화면의 편집 키 칸에 입력한다.

정적 서버가 실행 중이면 브라우저를 새로고침한다.
Network에서 요청 주소가 `127.0.0.1:8787` 대신 자신의 HTTPS 프로젝트인지 확인한다.
같은 UI가 열렸다는 사실만으로 서버가 전환됐다고 판단하지 않는다.

## 8. 접속 확인부터 방명록 저장까지

### 01_about · 접속 확인

[01_about/index.html](examples/01_about/index.html)을 연다. 로컬 주소는 `http://localhost:8000/01_about/`이다.
먼저 [01 requests.http](examples/01_about/requests.http)로 같은 요청을 확인한 뒤 화면 버튼과 코드를 비교한다.
접속 확인 버튼으로 `GET /rest/v1/about`을 보낸다. 공개 키는 요청의 `apikey` 헤더에 들어간다.
응답은 객체 한 개를 담은 배열이다. `name`, `version`, `description`, `help_path`를 확인한다.
`help_path`는 다음에 읽을 안내 경로다. 이 단계에서는 글을 저장하거나 수정하지 않는다.

Network에서 요청 주소와 200 응답을 확인한다. 404가 나오면 강의자의 about-help.sql 적용 여부를 먼저 확인한다.
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
이번 공개 방명록에서는 다른 등록 방명록의 조회·추가도 허용된다. 편집 키는 이 두 동작의 사용자 인증 수단이 아니다.

## 9. 수정·삭제와 통합 실험

### 05_guestbook_edit · 글 하나 수정·삭제

[05_guestbook_edit/index.html](examples/05_guestbook_edit/index.html)을 연다. 앞 단계에서 조회·저장한 경험을 이어서 사용한다.
먼저 [05 requests.http](examples/05_guestbook_edit/requests.http)를 실행한다. 요청할 때 입력 창에 자신이 만든 글 ID와 해당 방명록 편집 키를 넣는다.
편집 키 입력은 마스킹되며 `.env`나 요청 파일에 키를 저장하지 않는다.
REST Client의 요청 이력에는 헤더·본문이 남는다. 키가 든 이력·전체 요청 캡처를 공유하지 않고 실습 후 **Rest Client: Clear Request History**를 실행한다.
다음 순서로 조건을 한 번에 하나씩 바꾼다.

1. 04에서 student01에 실험용 글을 만들고 서버 id를 기록한다.
2. 해당 번호의 편집 키를 화면에 입력한다. 키는 공개 설정이나 JSON 본문에 넣지 않는다.
3. 메시지를 새 문장으로 바꾸어 수정 요청을 보낸다. 응답 배열의 항목과 후속 GET의 메시지를 모두 확인한다.
4. 04에서 다른 실험용 글을 하나 더 만든다. 05의 DELETE로 그 id만 지정해 삭제한다.
5. DELETE의 204 응답에는 JSON 본문이 없음을 확인한다. `response.json()`을 호출하지 않는다.
6. GET으로 삭제한 id가 사라지고 다른 글은 남아 있는지 확인한다.

수정·삭제 URL에는 `book_id=eq.student01`과 `id=eq.<대상 번호>`를 모두 지정한다.
편집 키는 `X-Edit-Key` 헤더로 보낸다. PATCH에는 JSON 본문과 `Prefer: return=representation`을 사용한다.
실험 화면의 키 입력 칸은 요청 직전 비워지므로 다음 수정·삭제 요청에는 키를 다시 입력한다.
`.http`의 후속 GET도 방금 수정·삭제한 글 ID를 입력해 대상 하나를 확인한다.

PATCH가 200과 빈 배열을 반환하거나 DELETE가 204를 반환해도 변경된 행이 없을 수 있다.
잘못된 편집 키나 없는 id를 넣은 경우의 실제 상태와 본문을 기록하고, 후속 GET으로 데이터가 그대로인지 확인한다.
공개 키 오류, 열 권한 오류, RLS에 따른 빈 결과를 같은 오류로 취급하지 않는다.

### 06_http_lab · 요청 조건 비교

[06_http_lab/index.html](examples/06_http_lab/index.html)은 메서드·글 ID·본문을 직접 바꾸는 통합 실험 화면이다.
같은 비교 요청의 출발점은 [06 requests.http](examples/06_http_lab/requests.http)다.
01~05를 확인한 뒤 사용한다. POST·PATCH는 **본문 예시 넣기**로 JSON을 준비하고 한 조건만 바꾼다.
다른 방명록 편집 키·없는 id·보호된 열을 비교하고 후속 GET으로 실제 상태를 확인한다.
세부 과제는 [실습지](lab.md), 실행 순서는 [예제 설명](examples/README.md#실험-순서)을 따른다.

## 10. 완성 방명록과 정규 예제 연결

[07_guestbook_complete](examples/07_guestbook_complete/index.html)는 목록·등록 폼·수정·삭제를 한 화면에 모은 완성 방명록이다.
[07 requests.http](examples/07_guestbook_complete/requests.http)로 요청을 확인하고 `http://localhost:8000/07_guestbook_complete/`을 연다.
태그를 정해 글을 등록한 뒤 목록의 **글 수정·삭제**에서 대상 글을 선택한다. 별칭·메시지와 편집 키를 입력해 수정하거나 삭제한다.
변경 후에는 같은 ID를 GET으로 확인하고 목록을 갱신한다. 편집 키는 요청 전에 입력 칸을 비운다.
07은 방명록 사용 흐름을 확인하는 화면이다. HTTP 메서드·JSON 본문을 직접 바꾸는 실험은 06을 사용한다.

실험 화면에서 API가 동작하면 정규 교재의 UI를 자신의 서버에 연결한다.
각 완성본의 `config.example.js`를 7단계와 같은 공개 값으로 바꾼다.

13주 화면을 확인할 때, 실행 중인 정적 서버를 Ctrl+C로 중지한 뒤 다음 명령을 실행한다.
현재 폴더: 교재 저장소 최상위.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week13_release_security/examples/day2/web-week13 8000
```

`http://localhost:8000/guestbook.html`에서 폼으로 글을 남기고 POST 다음 GET을 확인한다.

14주 화면은 다음과 같이 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week14_project_presentation/examples/day2/web-week14 8000
```

같은 주소에서 편집 키를 입력하고 글 하나를 수정·삭제한다.
서버 id로 지정한 글만 바뀌는지 새로고침 후 확인한다.
실험 도구와 방명록 UI가 같은 API 계약을 사용한다는 것을 비교한다.

## 11. 다른 기기와 권한 검증

특강 화면 또는 방명록 UI의 필요한 파일만 별도 학생 저장소에 올리고 GitHub Pages를 설정한다.
01~07은 폴더 하나만 별도 저장소나 Pages 게시 폴더로 옮겨 사용할 수 있다.
선택한 폴더의 `index.html`, `app.js`, `config.example.js`, `styles.css`를 함께 둔다. 06은 `request.js`·`exercise.js`도 포함한다.
HTML은 같은 폴더의 설정·스타일·앱 파일을 읽는다. 완성 방명록만 배포하려면 07 폴더를 선택한다.
학습 자료로 `requests.http`·`.env.example`을 함께 배부할 수 있지만 실제 `.env`는 제외한다.
GitHub Pages가 정적 파일을 제공하므로 Node 정적 서버나 로컬 API 서버를 실행할 필요가 없다.

배포 후 발급된 HTTPS 페이지 주소로 접속한다. 브라우저는 화면 파일을 Pages에서 받고 데이터는 Supabase HTTPS API에 요청한다.
config.example.js에는 공용 HTTPS API의 공개 설정만 둔다. 로컬 리허설 주소가 남아 있지 않은지 확인한다.
`localhost`·`127.0.0.1`은 방문자 각자의 기기이므로 공용 API 주소로 사용할 수 없다. 편집 키 파일은 복사하지 않는다.
정적 호스팅의 동작은 [GitHub Pages 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)를 참고한다.

공용 API의 GET·POST 확인과 이 화면의 Pages 배포 검증은 별개다. 다음 항목은 실제 배포한 뒤 확인한다.
새 안내 API SQL을 먼저 적용하고 배포 화면의 01·02에서 접속과 안내를 읽은 뒤 방명록 요청을 확인한다.
REST Client에서 성공해도 브라우저의 CORS 검증이 끝난 것은 아니다. `.env`는 Pages 게시 파일에 포함하지 않는다.

다른 PC·휴대폰에서 공개 페이지를 열어 다음 항목을 확인한다.

- 같은 방명록의 서버 id·메시지가 보이는지.
- 한 기기에서 추가한 글이 다른 기기의 GET에 나타나는지.
- 올바른 키로 수정·삭제한 결과가 다른 기기에도 보이는지.
- 다른 방명록 키와 키 없음으로 수정·삭제했을 때 대상 글이 유지되는지.
- 올바른 키를 사용해도 id·book_id·created_at 변경이 거부되는지.
- localhost와 GitHub Pages 양쪽에서 CORS 사전 요청과 실제 요청이 성공하는지.

Network의 Request Headers에는 실행 중인 편집 키가 보일 수 있다.
기록에는 키 이름과 사용 조건만 적고 값은 포함하지 않는다. 화면 캡처 전에 해당 값을 가린다.

## 12. 기록과 다음 모임 준비

[실습지](lab.md)의 기록표를 작성하고 프로젝트 담당자·실행 환경·교재 커밋·성공한 단계·남은 항목을 남긴다.
교재 커밋은 저장소 최상위에서 확인한다.

```powershell
git rev-parse --short HEAD
```

실험 결과를 공유하기 전에 수정한 공개 파일과 Git 상태를 확인한다.
키 파일을 제외한 소스 변경은 별도 브랜치나 개인 실습 저장소에서 관리한다.
프로젝트와 데이터의 보존·쓰기 권한 변경·종료 여부는 담당자와 강의자가 별도로 정한다.
