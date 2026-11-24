---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 연구 특강"
footer: "Supabase 공용 방명록 API 구축"
---

# Supabase 공용 방명록 API 구축

한 브라우저에서 쓴 글을 다른 브라우저에서 찾고, 같은 글의 수정과 삭제를 확인한다.

| 강의자 | 학생 |
|---|---|
| 방명록과 태그를 준비하고 URL·공개 키·태그를 배부한다. | 자기 태그로 글을 남기고 서버가 돌려준 글 번호를 추적한다. |

01 접속 → 02 도움말 → 03 조회 → 04 저장 → 05 수정·삭제 → 06 HTTP 콘솔 → 07 완성 방명록

---

# 방명록 화면과 데이터의 주소

| 위치 | 역할 |
|---|---|
| `http://localhost:8000/` | 내 컴퓨터에서 실습 HTML·JS를 연다. |
| GitHub Pages의 HTTPS 주소 | 배포한 같은 화면을 다른 기기에서 연다. |
| `https://esoqbcwgzjtwcqszwvin.supabase.co` | 수업용 API 기본 주소. 브라우저가 이 주소에 요청한다. |

방명록 요청 경로는 `/rest/v1/guestbook`이다. 로컬 HTTP 화면에서도 공용 HTTPS API를 호출한다.

강의자의 로컬 리허설 API 주소는 `http://127.0.0.1:8787`이다.

---

# 강의자 준비 · 새 프로젝트와 기존 프로젝트

| 프로젝트 | Supabase SQL Editor에서 실행할 파일 |
|---|---|
| 새 프로젝트 | [schema.sql](../../tools/guestbook-api/schema.sql) → [about-help.sql](../../tools/guestbook-api/about-help.sql). 첫 파일이 `student01`부터 `student30`까지 등록한다. |
| 이전 수업 방명록이 있는 프로젝트 | [enable-public-crud.sql](../../tools/guestbook-api/enable-public-crud.sql) 한 번. 기존 글과 태그를 유지하고 수정·삭제 정책과 도움말을 갱신한다. |

학생들은 Supabase 계정 없이 같은 **publishable key**를 쓴다. 이 키로 모든 태그의 글을 수정·삭제할 수 있다. 학생은 자기 태그에 별칭과 연습 문장을 쓴다.

---

# REST Client와 브라우저 설정

| 도구 | 같은 폴더에서 준비할 것 |
|---|---|
| VS Code REST Client (`humao.rest-client`) | `.env.example`을 `.env`로 복사하고 `API_BASE_URL`·`API_PUBLIC_KEY`를 채운다. 방명록 단계에서는 `BOOK_ID`도 넣는다. |
| 브라우저 | `config.example.js`에서 URL과 태그를 확인한다. 처음 나타나는 입력창에 공개 키를 넣으면 해당 출처의 localStorage에 저장된다. |

`requests.http`에서 요청 위의 **Send Request**를 누른다. 상태 번호와 본문을 보고, 같은 단계의 화면에서 버튼을 눌러 결과를 비교한다.

[REST Client 설정](examples/README.md#rest-client로-요청부터-확인하기)

---

# 01 · 서버에 접속하기

```http
GET {{baseUrl}}/rest/v1/about
apikey: {{apiKey}}
```

**접속 확인**을 누르면 `200`과 객체 한 개가 든 배열이 돌아온다. 첫 객체에서 `version` 값 `v1`과 `help_path` 값 `/rest/v1/help`를 찾는다.

| 응답 | 확인할 곳 |
|---|---|
| 401 | 브라우저는 **공개 키 지우기**로 다시 입력한다. REST Client는 `.env`를 확인한다. |
| 404 | 프로젝트 주소와 강의자가 설치한 `about` 뷰를 확인한다. |

[01 접속 화면](examples/01_about/index.html) · [requests.http](examples/01_about/requests.http)

---

# 01 · 같은 GET을 자바스크립트로 보내기

```js
const url = `${API_BASE_URL}/rest/v1/about`;
const response = await fetch(url, {
  headers: { apikey: API_PUBLIC_KEY }
});
```

1. `response.status`로 REST Client에서 본 상태 번호를 읽는다.
2. `response.ok`가 참이면 `await response.json()`으로 배열을 읽는다.
3. 배열을 펼쳐 첫 객체의 이름과 버전을 확인한다.

[01 접속 코드](examples/01_about/app.js)

---

# 02 · 도움말에서 요청 고르기

```http
GET {{baseUrl}}/rest/v1/help?order=step.asc
apikey: {{apiKey}}
```

**사용법 조회**를 누르면 여섯 행이 단계 순서로 나온다. 각 행의 `method`, `path`, `description`을 짝지어 읽는다.

- 1·2번은 강의자가 추가한 `about`·`help`를 읽는다.
- 3~6번은 방명록의 POST·GET·PATCH·DELETE다. 수정과 삭제 경로에서 `book_id`와 `id` 두 조건을 찾는다.

[02 도움말 화면](examples/02_help/index.html) · [requests.http](examples/02_help/requests.http)

---

# 예제 폴더 하나의 구성

| 파일 | 실습에서 하는 일 |
|---|---|
| `requests.http`, `.env.example` | VS Code에서 요청을 보내고 상태 번호와 본문을 읽는다. |
| `index.html` | 입력칸과 버튼을 표시하고 W3.CSS를 CDN에서 읽는다. |
| `config.example.js` | 브라우저에서 사용할 URL·태그·공개 키를 준비한다. |
| `app.js` | 버튼 이벤트에서 요청을 보내고 응답을 화면에 표시한다. |

01부터 07까지 각각 독립된 폴더다. 웹 화면은 로컬 정적 서버나 Pages에서 연다. 개인 설정 파일인 `.env`는 배포에서 제외한다.

[폴더별 실행 안내](examples/README.md)

---

# 03 · 자기 태그의 글 조회하기

```http
GET {{baseUrl}}/rest/v1/guestbook?book_id=eq.{{bookId}}&order=id.desc&limit=50
apikey: {{apiKey}}
```

`book_id=eq.student01`은 `student01` 태그에 속한 글을 고른다. `order=id.desc`는 큰 글 번호부터, `limit=50`은 최대 50개다.

**목록 조회**를 누르고 각 행의 글 번호·별칭·메시지를 JSON과 대조한다. 등록된 글이 없어도 조회는 성공하며 `200 []`가 돌아온다.

[03 조회 화면](examples/03_guestbook_get/index.html) · [requests.http](examples/03_guestbook_get/requests.http)

---

# 두 브라우저에서 같은 글 찾기

1. 브라우저 A에서 03의 태그를 정하고 **목록 조회**를 누른다.
2. 브라우저 B에서 같은 API 주소와 공개 키, 같은 태그로 03을 연다. 휴대폰이라면 접속할 수 있는 Pages 화면을 쓴다.
3. 글이 보이면 번호를, 빈 목록이면 `[]`를 적는다. 다음 단계에서 A가 글을 쓰면 B에서 다시 조회한다.

공개 키는 브라우저마다 입력한다. 두 목록에서 같은 글을 가리키는 값은 서버가 붙인 `id`다.

[03 조회 코드](examples/03_guestbook_get/app.js) · [연구 실습지](lab.md)

---

# 04 · 글을 저장하고 새 번호 찾기

A에서 **새 글 저장**을 누르면 `POST /rest/v1/guestbook`이 다음과 같은 JSON을 보낸다.

```json
{"book_id":"student01","name":"연습생","message":"첫 관찰"}
```

`apikey`와 `Content-Type: application/json`을 보내고, `Prefer: return=representation`으로 저장된 행을 받는다.

`201` 응답 배열의 첫 객체에서 `id`를 적는다. B에서 **목록 조회**를 다시 눌러 그 번호와 메시지를 찾는다.

[04 저장 화면](examples/04_guestbook_post/index.html) · [requests.http](examples/04_guestbook_post/requests.http)

---

# 05 · 선택한 글 수정하기

A에서 **목록 조회**를 누른 뒤 방금 쓴 글의 번호가 적힌 버튼(예: **글 42 선택**)을 누른다. 해당 글의 별칭과 메시지가 입력칸에 채워진다.

메시지를 `두 번째 관찰`로 바꾸고 **선택한 글 수정**을 누른다. 화면은 두 값을 JSON으로 보내고 같은 글을 다시 조회한다.

| 확인할 값 | 예상 결과 |
|---|---|
| PATCH URL | 목록에 표시된 `book_id`와 선택한 `id` |
| PATCH 응답 | `200`과 수정한 행 한 개. `[]`이면 바뀐 행이 없다. |
| 같은 조건의 GET | 원래 글 번호와 바꾼 메시지 `두 번째 관찰` |

[05 편집 화면](examples/05_guestbook_edit/index.html) · [requests.http](examples/05_guestbook_edit/requests.http)

---

# 05 · 목록에서 한 글만 삭제하기

04에서 자기 태그에 연습 글 세 개를 준비한다. 05에서 **목록 조회**를 누르고 번호를 적는다. 예시는 **43, 42, 41**이다.

| 목록에서 42번 옆 **삭제**를 누른 뒤 | 요청과 결과 |
|---|---|
| 확인창에서 취소 | DELETE 요청이 발생하지 않는다. 세 글이 모두 남는다. |
| 다시 눌러 태그와 42번을 확인하고 승인 | DELETE 응답은 `204`이며 본문이 비어 있다. |
| 같은 태그·번호로 GET | `200 []`가 돌아온다. 새 목록에서 43번과 41번을 확인한다. |

`requests.http`로 실험하면 `entryId` 입력창에 같은 글 번호를 쓴다. DELETE의 빈 본문은 JSON으로 읽지 않는다.

---

# 06 · HTTP 콘솔에서 조건 하나 바꾸기

05에서 지운 글을 이용한다. 메서드·태그·글 번호를 직접 정하고 **요청 보내기**를 누른다.

| 실험 | 예측한 뒤 확인할 값 |
|---|---|
| GET, 지운 글 번호 | `200 []` |
| PATCH, 같은 번호, **본문 예시 넣기** | `200 []`. 바뀐 행이 없다. |
| GET, 같은 태그, 남아 있는 내 글 번호 | `200`과 글 한 개 |

`buildRequest(method, book, id, bodyText)`가 URL과 요청 옵션을 만든다. [응답 해석 과제](examples/06_http_lab/exercise.js)에서 빈 배열의 의미를 설명한다.

[06 HTTP 콘솔](examples/06_http_lab/index.html) · [requests.http](examples/06_http_lab/requests.http) · [요청 시험](examples/06_http_lab/request.test.mjs)

---

# Pages에서 기기 간 저장 확인하기

1. 실습 폴더를 Pages에 게시하고 두 기기에서 게시한 **HTTPS 화면 주소**를 연다. 각 기기에 수업용 공개 키를 입력한다.
2. 같은 태그로 A에서 글을 등록한다. B에서 목록을 새로고침하고 번호를 대조한다.
3. B에서 그 글을 수정한 뒤 A에서 다시 조회한다. 요청을 보낸 기기와 결과를 확인한 기기, 태그·번호·상태를 함께 기록한다.

로컬 API로 연습한 결과와 공용 Supabase에서 관찰한 결과는 기록을 나눈다. REST Client와 배포된 브라우저에서도 각각 요청을 보내 본다.

[Pages 실행 안내](examples/README.md#github-pages에서-사용하기)

---

# 07 · 완성 방명록에서 재현하기

1. **글 등록**으로 연습 글 세 개를 남긴다. **목록 새로고침**을 누르고 글 번호들을 기록한다.
2. 가운데 행의 **수정**을 눌러 문장을 바꾸고 **수정 저장**을 누른다. 같은 글 번호에서 새 문장을 확인한다.
3. 가운데 행의 **삭제**를 한 번 취소한 뒤 다시 눌러 승인한다. 다른 기기에서도 목록을 새로고침해 양옆 두 번호가 남는지 본다.

[07 완성 방명록](examples/07_guestbook_complete/index.html) · [requests.http](examples/07_guestbook_complete/requests.http) · [따라하기](walkthrough.md) · [연구 실습](lab.md)

[12주 GET](../../weeks/week12_fetch_json/README.md) · [13주 CRUD](../../weeks/week13_guestbook_crud/README.md) · [14주 수정·삭제](../../weeks/week14_project_presentation/README.md)
