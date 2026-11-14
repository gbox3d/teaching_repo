---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 연구 특강"
footer: "Supabase 공용 방명록 API 구축"
---

# Supabase 공용 방명록 API 구축

방학 연구 특강 · 폴더별로 한 단계씩 진행한다.

01 접속 → 02 안내 → 03 조회 → 04 저장
05 수정·삭제 → 06 비교 → 07 완성 방명록

각 단계는 requests.http 요청을 먼저 보내고 브라우저 코드로 이어 간다.
학생은 준비된 공용 API를 계정 없이 사용한다.

---

# 화면 주소와 API 주소

| 대상 | 주소·역할 |
|---|---|
| 로컬 화면 | http://localhost:8000/ · 화면 파일 미리보기 |
| 공용 API | Supabase HTTPS 주소 · 안내와 방명록 데이터 |
| Pages 화면 | 배포된 HTTPS 주소 · 학생에게 공유할 화면 |
| 선택 로컬 API | http://127.0.0.1:8787 · 리허설용 |

로컬 HTTP 화면에서도 공용 HTTPS API를 호출한다.
Node 정적 서버는 로컬 미리보기용이다.

---

# 시작 전 · 강의자 SQL 준비

기존 공용 프로젝트에는 [about-help.sql](../../tools/guestbook-api/about-help.sql)을 한 번 추가 실행한다.
새 프로젝트는 [schema.sql](../../tools/guestbook-api/schema.sql) 다음에 실행한다.

- 읽기 전용 about·help 안내 뷰 추가
- 기존 방명록 테이블 유지
- 학생 계정·SQL 작업 불필요

공용 방명록 GET·POST는 확인했다.
2026-11-14 안내 SQL 설치·GET 확인: about 1행, help 6행.

---

# 요청 먼저 · VS Code REST Client

1. 해당 단계의 .env.example을 .env로 복사한다.
2. 공개 키를 넣고 방명록 단계에서는 BOOK_ID도 확인한다.
3. 같은 폴더의 requests.http에서 **Send Request**를 누른다.
4. 상태 번호·JSON을 확인한 뒤 index.html·app.js를 읽는다.

.env는 .http와 같은 폴더에 둔다. Node 서버는 필요 없다.
브라우저는 같은 폴더의 config.example.js를 따로 읽는다.
[REST Client 사용법](https://github.com/Huachao/vscode-restclient#usage) · [설정 절차](examples/README.md#rest-client로-요청부터-확인하기)

---

# 01_about · API 접속 확인

[requests.http](examples/01_about/requests.http) → [브라우저 화면 소스](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/01_about/index.html)

```http
GET /rest/v1/about
apikey: <강의자가 배부한 공개 키>
```

접속 확인 버튼을 누른다. 응답은 200과 객체 한 개의 배열이다.
name · version · description · help_path를 읽는다.
404라면 강의자에게 안내 SQL 적용 여부를 확인한다.

---

# 01 · 요청과 코드를 연결하기

[01_about/app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/01_about/app.js)를 읽는다.

| 요청에서 본 것 | JavaScript에서 찾을 것 |
|---|---|
| GET 경로 | API_BASE_URL 뒤의 /rest/v1/about |
| apikey 헤더 | API_PUBLIC_KEY를 넣는 headers |
| 상태 번호 | response.status와 response.ok |
| JSON 응답 | response.json() |

이 단계에서는 글을 저장하거나 수정하지 않는다.
REST Client 성공 뒤 브라우저 요청도 확인한다.

---

# 02_help · API 사용 안내

[requests.http](examples/02_help/requests.http) → [브라우저 화면 소스](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/02_help/index.html)

```http
GET /rest/v1/help?order=step.asc
apikey: <강의자가 배부한 공개 키>
```

여섯 행의 step · method · path · description을 읽는다.
order=step.asc는 단계 번호 순서다.
about·help는 이 교재가 추가한 GET 전용 API다.

---

# 폴더 하나로 실행하기

```text
examples/
  README.md              예제 목차
  01_about/
    index.html · app.js
    config.example.js · styles.css
    requests.http · .env.example
  02_help/ ... 07_guestbook_complete/
```

각 단계는 자신의 설정과 스타일을 읽는다.
폴더 하나만 로컬에서 열거나 Pages에 게시할 수 있다. .env는 제외한다.

---

# 03_guestbook_get · 태그로 읽기

[requests.http](examples/03_guestbook_get/requests.http) → [조회 화면 소스](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/03_guestbook_get/index.html)

```http
GET /rest/v1/guestbook?book_id=eq.student01
apikey: <강의자가 배부한 공개 키>
```

book_id는 글을 묶는 태그, eq.는 같은 값 조건이다.
조회 버튼으로 배열을 읽는다. 글이 없으면 []이 정상이다.
태그는 권한 제한이 아니며 다른 등록 태그도 조회할 수 있다.

---

# 03 · 응답과 조회 조건

| 조건 | 역할 |
|---|---|
| select=id,name,message,created_at | 받을 열 선택 |
| order=id.desc | 큰 글 번호부터 정렬 |
| limit=50 | 최대 50개 조회 |

JSON 배열의 각 객체가 글 한 개다.
[조회 코드](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/03_guestbook_get/app.js)에서 응답과 화면 표시를 연결한다.
같은 태그를 두 화면에서 읽어 같은 서버 데이터를 확인한다.

---

# 04_guestbook_post · 글 저장

[requests.http](examples/04_guestbook_post/requests.http) → [저장 화면 소스](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/04_guestbook_post/index.html)

```json
{"book_id":"student01","name":"별칭","message":"첫 글"}
```

POST /rest/v1/guestbook
apikey · Content-Type: application/json · Prefer: return=representation

201 배열의 새 id를 기록하고 GET으로 다시 읽는다.
id·created_at은 서버가 만든다. 같은 POST를 반복하면 글이 더 생긴다.

---

# 05_guestbook_edit · 글 수정

[requests.http](examples/05_guestbook_edit/requests.http) → [편집 화면 소스](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/05_guestbook_edit/index.html)

목록에서 자신이 만든 글을 선택하거나 ID를 입력한다.
PATCH에는 book_id·id 조건과 X-Edit-Key가 필요하다.

```json
{"message":"수정한 글"}
```

편집 키는 요청할 때 입력한다. 공개 설정에 저장하지 않는다.
200이어도 빈 배열이면 바뀐 글이 없다. 같은 ID를 GET해 확인한다.

---

# 05 · 글 삭제와 빈 응답

DELETE에 book_id·id 조건과 편집 키를 보낸다.

- 204는 본문이 없는 응답이다.
- 빈 본문을 response.json()으로 읽지 않는다.
- 같은 ID를 GET해 실제로 사라졌는지 확인한다.
- 다른 글은 그대로 남아 있는지도 확인한다.

.http는 entryId·password 입력 창을 사용한다.
키 입력은 마스킹되지만 요청 이력은 남는다. [이력 정리](examples/README.md#rest-client로-요청부터-확인하기)를 따른다.

---

# 06_http_lab · 조건을 바꾸어 비교

[requests.http](examples/06_http_lab/requests.http) → [통합 화면 소스](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/06_http_lab/index.html)

01~05를 확인한 뒤 메서드·ID·JSON 본문을 직접 바꾼다.
POST·PATCH는 본문 예시를 넣고 한 조건만 수정한다.

- 올바른 키와 다른 방명록 키
- 존재하는 ID와 없는 ID
- 허용된 message와 보호된 book_id

[exercise.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/06_http_lab/exercise.js)에서 응답 해석을 확장한다.
[요청 시험](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/06_http_lab/request.test.mjs)과 공용 서버 검증을 구분한다.

---

# GitHub Pages와 확인 범위

원하는 예제 폴더 하나의 HTML·JS·설정·CSS를 함께 게시한다.
Pages가 화면을 제공하고 브라우저가 Supabase HTTPS API를 호출한다.
Node 서버·학생 계정은 필요 없다. .env·편집 키 파일은 게시하지 않는다.

현재 확인: 공용 방명록 GET·POST, about·help GET과 로컬 01·02 화면.
남은 확인: 이 화면의 Pages 실배포, 공용 PATCH·DELETE.

REST Client 성공만으로 브라우저 CORS 성공을 판단하지 않는다.
[Pages 사용 안내](examples/README.md#github-pages에서-사용하기)

---

# 07_guestbook_complete · 완성 방명록

[requests.http](examples/07_guestbook_complete/requests.http) → [방명록 화면 소스](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/supabase_guestbook/examples/07_guestbook_complete/index.html)

태그별 목록과 등록 폼을 한 화면에서 사용한다.
글을 선택하고 편집 키를 입력해 수정·삭제한 뒤 같은 ID를 재조회한다.
07은 완성 방명록, 06은 요청 조건을 바꾸는 실험 화면이다.
연구 분량·회차는 제한하지 않고 관찰 결과와 남은 확인을 기록한다.

[12주 GET](../../weeks/week12_fetch_json/README.md) · [13주 POST](../../weeks/week13_release_security/README.md) · [14주 수정·삭제](../../weeks/week14_project_presentation/README.md)
[따라하기](walkthrough.md) · [연구 실습](lab.md) · [예제 안내](examples/README.md)
[Supabase Data REST API](https://supabase.com/docs/guides/api)
