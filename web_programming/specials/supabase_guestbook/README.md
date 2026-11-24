# 연구 특강 · Supabase 공용 방명록 API 구축

## 목차

- [수업의 목적](#수업의-목적)
- [시작 전 서버 준비](#시작-전-서버-준비)
- [참여 방식과 준비](#참여-방식과-준비)
- [화면 주소와 API 주소](#화면-주소와-api-주소)
- [학습 목표](#학습-목표)
- [단계별 도달 기준](#단계별-도달-기준)
- [구현 범위와 권한](#구현-범위와-권한)
- [연구 주제](#연구-주제)
- [자료와 정본](#자료와-정본)
- [기록과 완료 기준](#기록과-완료-기준)
- [운영 상태](#운영-상태)
- [공식 참고 자료](#공식-참고-자료)

교재 소스: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/supabase_guestbook

## 수업의 목적

정규 12~14주에는 강의자가 준비한 API를 `fetch`로 호출한다.
이 특강의 화면 실습은 `01_about` 접속 확인부터 시작해 `02_help` 안내 조회, 방명록 읽기·저장 순서로 진행한다. 완성 화면은 `07_guestbook_complete`에 따로 둔다.
이 특강에서는 그 API를 새 Supabase 프로젝트에 직접 만들고 요청 결과와 실제 데이터 변화를 대조한다.
강의자가 수업용 테이블과 공개 API를 준비하고 학생은 방명록 화면에서 요청을 보낸다. 방학 연구수업에서는 원하는 조가 새 프로젝트를 직접 구축할 수 있다.

방학 연구수업으로 운영한다. 전체 분량이나 회차를 고정하지 않고 각 단계의 도달 기준을 확인한 뒤 다음 단계로 넘어간다.
기본 구축이 끝난 조는 권한·응답·동시 편집 같은 비교 실험을 이어 간다. 정규 주차 실습 점수·시험·레포트 검사와는 별도로 운영한다.

Supabase SDK를 설치하지 않고 브라우저의 `fetch`로 GET·POST·PATCH·DELETE를 직접 보낸다.
데이터베이스 준비 코드는 [공용 API 도구](../../tools/guestbook-api/README.md)를 정본으로 사용한다.

## 시작 전 서버 준비

- 새 프로젝트에서는 [schema.sql](../../tools/guestbook-api/schema.sql)을 실행한다. 테이블과 `student01`~`student30` 태그 30개가 생긴다. 이어서 [about-help.sql](../../tools/guestbook-api/about-help.sql)을 실행해 접속 확인과 도움말 경로를 추가한다.
- 기존 수업 프로젝트에서는 [enable-public-crud.sql](../../tools/guestbook-api/enable-public-crud.sql)을 SQL Editor에서 한 번 실행한다. 기존 글과 태그를 유지하면서 공개 수정·삭제 정책과 도움말을 갱신한다.

학생에게는 API 주소·publishable key·실습 태그를 배부한다.

실제 경로는 `GET /rest/v1/about`과 `GET /rest/v1/help`다. 둘 다 `apikey` 헤더가 필요하며 GET만 사용한다.
이 수업이 추가하는 안내 API이므로 Supabase의 모든 프로젝트에 기본으로 존재하지는 않는다.
2026-11-14에 공용 서버에 안내 SQL을 적용하고 두 GET의 200 응답을 확인했다. about은 1행, help는 단계 1~6의 여섯 행을 반환한다.

## 참여 방식과 준비

| 방식 | 준비 | 수행 범위 |
|---|---|---|
| 개인·소그룹 구축 | 실습 전용 새 Supabase 프로젝트 | SQL 적용·태그 확인·API 요청 검증 |
| 강의자 시연과 공용 실습 | API 주소·공개 키·실습 태그 | 계정 없이 준비된 API로 요청·응답 실험 |
| 로컬 선행 연습 | Node.js와 교재 파일 | 요청 문법과 화면 실행 확인. 클라우드 구축·기기 간 공유 검증은 미완료로 기록 |

권장 선수 내용은 정규 12~14주의 `fetch`, JSON, 폼, 서버 `id`, PATCH·DELETE다.
Node.js 24 이상, VS Code, Git, Chrome 개발자 도구의 Network 탭과 Console을 준비한다.
계정이 없는 학생에게 유료 계정이나 프로젝트 생성을 요구하지 않는다. 강의자 시연과 공용 API 실습으로 계속 참여할 수 있다.

Supabase의 무료 범위·활성 프로젝트 제한·휴면 정책은 수업 시작 시 [공식 요금제](https://supabase.com/pricing)에서 확인한다.
무료 범위를 넘는 상황에서는 유료 전환을 진행하지 않고 실습 구성과 프로젝트 사용 현황을 다시 정한다.

## 화면 주소와 API 주소

실험 화면은 HTML·CSS·JavaScript로 이루어져 있다. 01~07 각 폴더의 `config.example.js`는 공용 Supabase HTTPS API를 가리킨다.
examples 루트에는 예제 안내 README만 두고, 각 폴더에 설정·화면·요청 파일을 둔다.
7주에서 소개한 [W3.CSS CDN 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용한다. CDN 연결에는 인터넷이 필요하다. 조작 설명은 각 예제의 README에서 읽는다.
화면을 연 주소와 데이터 요청 주소는 다음처럼 구분한다.

| 대상 | 주소 | 역할 |
|---|---|---|
| 로컬 화면 | `http://localhost:8000/` | 내 PC에서 HTML·CSS·JavaScript 미리보기 |
| 로컬 API | `http://127.0.0.1:8787` | 설정을 전환해 사용하는 선택 리허설 서버 |
| 공용 API | `https://esoqbcwgzjtwcqszwvin.supabase.co` | 방명록 데이터 저장·조회 |
| GitHub Pages 화면 | 배포 후 발급되는 `https://<계정>.github.io/...` | 학생이 접속할 공개 실험 화면 |

로컬 화면 주소가 HTTP여도 브라우저는 공용 HTTPS API에 요청할 수 있다. 페이지 주소는 HTTP로 유지되고 데이터 요청만 HTTPS를 쓴다.
Node 정적 서버는 로컬 미리보기용이며 GitHub Pages에서는 실행하지 않는다.
GitHub Pages가 화면 파일을 제공하고 브라우저의 `fetch`가 Supabase에 직접 요청한다.
배포 방법과 다른 기기 확인은 [따라하기 11단계](walkthrough.md#11-다른-기기와-권한-검증)를 따른다.

공개 키는 `config.example.js`에 적지 않는다. 예제 화면을 처음 열면 공개 키를 묻는 창이 뜨고, 넣은 키는 이 브라우저의 localStorage에 `API_PUBLIC_KEY`로 저장된다. 같은 주소의 01~07이 이 값을 함께 쓴다.
키를 잘못 넣었거나 학기에 키가 바뀌면 화면 제목 아래 **공개 키 지우기**를 누르고 새 키를 넣는다. 저장소 파일은 고치지 않는다.
다시 묻는 주소, 401 대처, 로컬 리허설의 키 전환은 [공개 키 입력과 지우기](examples/README.md#공개-키-입력과-지우기)에 있다.

## 학습 목표

1. 브라우저, REST API, 테이블, RLS 정책이 맡은 일을 요청 하나에 연결해 설명한다.
2. 정본 SQL을 읽고 새 연습 프로젝트에 테이블·정책·열 권한을 적용한다.
3. 기본 태그 30개를 확인하고 배정받은 하나를 `BOOK_ID`로 사용한다.
4. 프로젝트 URL·publishable key·방명록 번호로 기존 `fetch` 예제를 연결한다.
5. GET·POST·PATCH·DELETE의 상태 코드·응답 본문·후속 GET 결과를 각각 확인한다.
6. 태그와 글 번호가 일치할 때와 일치하지 않을 때의 결과를 비교한다.
7. 로컬 재현 결과와 실제 클라우드·다른 기기 검증 결과를 구분해 기록한다.

## 단계별 도달 기준

| 예제 폴더 | 할 일 | 다음 단계로 넘어갈 기준 |
|---|---|---|
| [01_about](examples/01_about/index.html) | API 접속 확인 | 200과 안내 객체 한 개를 담은 배열 확인 |
| [02_help](examples/02_help/index.html) | API 사용 안내 읽기 | step·method·path·description 여섯 행을 순서대로 확인 |
| [03_guestbook_get](examples/03_guestbook_get/index.html) | 태그별 글 조회 | book_id 필터와 응답 배열의 관계 설명 |
| [04_guestbook_post](examples/04_guestbook_post/index.html) | 이름·메시지 저장 | 201의 새 id를 GET으로 재확인 |
| [05_guestbook_edit](examples/05_guestbook_edit/index.html) | 글 하나 수정·삭제 | 목록 행에서 삭제하고 같은 ID의 GET으로 결과 확인 |
| [06_http_lab](examples/06_http_lab/index.html) | HTTP 콘솔에서 요청 구성 | 메서드·태그·글 번호·본문 중 한 조건을 바꿔 응답 비교 |
| [07_guestbook_complete](examples/07_guestbook_complete/index.html) | 완성 방명록 사용 | 폼·목록·선택한 글의 수정·삭제를 한 화면에서 확인 |

일정은 단계별 진행 상태로 정한다. 단계마다 화면을 캡처할 수 있지만 캡처 한 장을 전체 완료 조건으로 삼지 않는다.
자체 프로젝트를 구축하는 조는 [따라하기](walkthrough.md)에서 SQL 실행과 기본 태그 확인 절차를 따른다.
각 폴더는 `requests.http`의 요청부터 확인한 뒤 `index.html`과 `app.js`를 읽는다.
VS Code REST Client에서 같은 폴더의 `.env.example`을 `.env`로 복사하고 공개 키를 넣은 뒤 **Send Request**를 누른다.
처음에는 01·02만 열고 접속과 응답을 확인한 뒤 다음 폴더로 이동한다. 자세한 설정은 [예제 안내](examples/README.md)를 따른다.

## 구현 범위와 권한

이번 서비스는 연습용 공개 방명록이다. 다음 규칙은 [정본 SQL](../../tools/guestbook-api/schema.sql)에 구현되어 있다.

| 대상 | 역할과 허용 범위 |
|---|---|
| public.guestbook | id·book_id·name·message·created_at을 저장하는 공개 글 테이블 |
| private.classroom_books | 등록된 방명록 태그 목록. 신규 설치 시 `student01`~`student30` 포함 |
| publishable key | 같은 수업 프로젝트에 접속할 때 쓰는 공용 `apikey` 헤더 값 |
| book_id | 글을 모아 볼 때 사용하는 태그 |
| GET·POST | 글 목록 조회와 새 글 저장 |
| PATCH·DELETE | 공개 키로 모든 태그의 글을 수정·삭제할 수 있다. 예제는 `book_id`와 `id`로 대상 한 건을 지정한다. |
| 보호된 열 | id·book_id·created_at은 학생 클라이언트가 수정할 수 없음 |

`private` 스키마는 Data API의 Exposed schemas에 추가하지 않는다.
`config.example.js`에는 API 주소와 방명록 번호만 넣고, publishable key는 브라우저 localStorage에 저장한다. secret key·service_role key·DB 비밀번호를 사용하지 않는다.
실험의 이름·메시지는 별칭과 연습 문장만 사용한다.

브라우저는 저장한 publishable key를 요청마다 `apikey` 헤더에 넣는다. **공개 키 지우기**를 누르면 다음 실행에서 새 값을 입력할 수 있다.

## 연구 주제

- 같은 글 번호에 원래 태그와 다른 태그를 지정하고 응답을 비교한다.
- 같은 200 또는 204 응답이어도 데이터가 바뀌지 않는 경우를 조사한다.
- URL의 `book_id` 필터와 데이터베이스가 허용하는 수정 열을 구별한다.
- 화면의 입력 길이 제한을 바꾸어도 서버 제약이 유지되는지 검사한다.
- 두 브라우저에서 같은 글을 연속 수정하고 마지막 저장 결과를 설명한다.
- 서버가 응답하지 않는 상황에서 재전송 전에 GET으로 확인해야 하는 이유를 관찰한다.

선택 실험은 [실습지](lab.md)의 조건과 기록 양식을 사용한다.
추가 기능은 먼저 원래 요청이 통과하는지 확인한 뒤 하나씩 붙인다.

## 자료와 정본

| 자료 | 위치 |
|---|---|
| 단계별 구축 안내 | [walkthrough.md](walkthrough.md) |
| 비교 실험·연구 기록 | [lab.md](lab.md) |
| 한·영 슬라이드 | [slides.md](slides.md) · [slides_en.md](slides_en.md) |
| 단계별 실습 목차 | [examples/README.md](examples/README.md) · [01 접속 확인](examples/01_about/index.html) |
| 폴더별 주소·방명록 번호 설정 | [01의 config.example.js](examples/01_about/config.example.js). 다른 폴더도 각자 같은 이름의 파일 사용. 공개 키는 브라우저 localStorage에서 읽음 |
| 통합 요청·실행 코드 | [request.js](examples/06_http_lab/request.js) · [app.js](examples/06_http_lab/app.js) |
| 학생 확장 코드 | [exercise.js](examples/06_http_lab/exercise.js) |
| 완성 방명록 | [07 화면](examples/07_guestbook_complete/index.html) · [앱 코드](examples/07_guestbook_complete/app.js) · [요청 파일](examples/07_guestbook_complete/requests.http) |
| 서버 준비와 운영 기준 | [tools/guestbook-api/README.md](../../tools/guestbook-api/README.md) |
| 테이블·정책 정본 | [schema.sql](../../tools/guestbook-api/schema.sql) |
| 안내 API 추가 SQL | [about-help.sql](../../tools/guestbook-api/about-help.sql) |
| 기존 수업 프로젝트 갱신 | [enable-public-crud.sql](../../tools/guestbook-api/enable-public-crud.sql) |
| 방명록 CRUD 완성본 | [13주 예제](../../weeks/week13_guestbook_crud/examples/day2/web-week13/guestbook.html) |
| PATCH·DELETE 방명록 완성본 | [14주 예제](../../weeks/week14_project_presentation/examples/day2/web-week14/guestbook.html) |

연구 결과에는 실행한 SQL의 교재 커밋과 날짜를 기록한다.
교재 사이트: https://gbox3d.github.io/teaching_repo/webprg/decks/supabase_guestbook/index.html

## 기록과 완료 기준

- [ ] 어떤 환경에서 실행했는지 로컬·공용 서버·자체 클라우드로 구분했다.
- [ ] 직접 구축한 프로젝트에서 기본 태그 30개를 확인했다.
- [ ] 요청별 상태 코드·본문·후속 GET 결과를 기록했다.
- [ ] 같은 글 번호로 태그를 바꾸어 조회 결과를 비교했다.
- [ ] 보호된 열이 바뀌지 않는지 확인했다.
- [ ] 공용 HTTPS API를 다른 기기에서 확인했거나 아직 확인하지 못한 항목을 표시했다.
- [ ] 키 원문과 개인정보를 제외하고 재현 절차·관찰·해석·남은 질문을 남겼다.

실험 기록은 소스 저장소의 별도 Markdown 문서나 연구 노트로 작성한다.
정규 수업 레포트와 합칠지, 조별로 제출할지는 강의자가 별도로 안내한다.

## 운영 상태

2026-11-14 기준 공용 Supabase 서버가 준비되어 있으며 GET·POST를 확인했다.
현재 특강 예제의 `config.example.js`도 이 공용 HTTPS API 주소를 가리킨다.
2026-11-14에 `/rest/v1/about`·`/rest/v1/help` 설치와 GET을 확인했다. 로컬 01·02 화면에서도 실제 공용 API 응답 200과 1행·6행을 확인했다.
이 실험 화면의 GitHub Pages 실배포와 공용 서버 PATCH·DELETE는 아직 검증하지 않았다.
배포 후 다른 기기에서 공용 API의 조회·수정·삭제 결과를 확인한다.

연구수업 종료 시 남길 프로젝트와 글, 다음 모임의 담당자, 공개 쓰기 운영 여부를 정한다.
프로젝트나 데이터를 정리하는 작업은 소유자가 범위를 확인한 뒤 별도로 수행한다.

## 공식 참고 자료

- [GitHub Pages의 정적 사이트 호스팅](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Data REST API](https://supabase.com/docs/guides/api)
- [API 키](https://supabase.com/docs/guides/getting-started/api-keys)
- [API 권한 설정](https://supabase.com/docs/guides/api/securing-your-api)
- [RLS](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [열 권한](https://supabase.com/docs/guides/database/postgres/column-level-security)
- [MDN · Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
