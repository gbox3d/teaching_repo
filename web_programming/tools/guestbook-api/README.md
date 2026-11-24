# 강의자용 공용 방명록 API 준비

강의자가 한시적으로 운영하는 공개 실습 방명록이다. 학생에게 수업 URL, 공용 publishable key, 방명록 태그(`BOOK_ID`)를 알려 준다. 이 키로 모든 태그의 글을 생성·조회·수정·삭제할 수 있다. 태그는 학생별 글을 찾는 필터다.

## Supabase 공용 서버 준비

- **이미 사용하는 수업 프로젝트**에서는 SQL Editor에 [enable-public-crud.sql](enable-public-crud.sql)을 붙여 넣고 **Run**을 누른다. 이 한 번으로 수정·삭제 정책과 도움말이 바뀐다. 기존 등록 태그, 글 번호, 내용, 외래 키는 유지된다. 이전 방식으로 등록한 태그도 계속 쓸 수 있다.
- **새 수업 프로젝트**에서는 [schema.sql](schema.sql)을 한 번 실행하고 [about-help.sql](about-help.sql)을 실행한다. `student01`부터 `student30`까지 등록된다.

기존 프로젝트에 등록된 태그는 SQL Editor에서 확인한다.

```sql
select book_id from private.classroom_books order by book_id;
```

태그를 추가할 때는 아래처럼 번호만 등록한다.

```sql
insert into private.classroom_books (book_id)
values ('student31'), ('student32')
on conflict (book_id) do nothing;
```

`private.classroom_books`는 강의자용 태그 목록이다. Data API에는 `public` 스키마의 방명록과 안내 뷰를 노출한다. 학생은 Supabase에 가입하거나 SQL을 실행할 필요가 없다.

## 학생에게 배부할 자료

수업 API 기본 주소는 `https://esoqbcwgzjtwcqszwvin.supabase.co`다. 브라우저에 쓰는 publishable key와 등록된 태그를 [학생용 안내](student-guide.md)와 함께 배부한다. 학생마다 키를 생성할 필요가 없다. 강의자의 DB 비밀번호와 서버용 secret key는 학생 실습에 사용하지 않는다.

- 13주에는 HTML 옆에 `config.example.json`을 `config.json`으로 복사하고 URL·공개 키·태그를 넣는다. [정규 수업 CRUD](../../weeks/week13_guestbook_crud/examples/README.md)
- `config.example.js`를 쓰는 기존 예제는 파일에서 태그를 설정하고, 처음 열 때 공개 키를 입력한다. [방학 특강 예제](../../specials/supabase_guestbook/examples/README.md)
- VS Code REST Client(`humao.rest-client`)에서는 각 예제의 `.env.example`을 `.env`로 복사한 뒤 세 값을 입력한다. `requests.http`에서 **Send Request**를 누른다.

## 소개·도움말 API 추가

`GET /rest/v1/about`에는 서버 이름과 버전이, `GET /rest/v1/help?order=step.asc`에는 접속 확인과 CRUD 요청이 나온다. 두 요청 모두 `apikey` 헤더를 보낸다. 두 경로만 새로 설치할 때는 [about-help.sql](about-help.sql)을 사용한다. [접속 확인 요청](../../specials/supabase_guestbook/examples/01_about/requests.http) · [도움말 요청](../../specials/supabase_guestbook/examples/02_help/requests.http)

## 요청과 응답

모든 요청은 `apikey` 헤더에 같은 공개 키를 보낸다. POST·PATCH는 `Content-Type: application/json`과 `Prefer: return=representation`을 보낸다.

| 동작 | 예제 요청 | 응답 |
|---|---|---|
| Create | `POST /rest/v1/guestbook`, 본문 `{book_id, name, message}` | `201`, 새 글과 서버가 부여한 `id` |
| Read | `GET /rest/v1/guestbook?book_id=eq.student01&order=id.desc` | `200`, 해당 태그의 글 배열 |
| Update | `PATCH /rest/v1/guestbook?book_id=eq.student01&id=eq.123`, 본문 `{message}` | `200`, 수정된 행의 배열 |
| Delete | `DELETE /rest/v1/guestbook?book_id=eq.student01&id=eq.123` | `204`, 본문 없음 |

이름은 1~30자, 메시지는 1~500자이고 공백만으로는 저장할 수 없다. 수정 가능한 열은 `name`과 `message`다. 예제는 수정·삭제 URL에 태그와 글 번호를 함께 넣어 한 행을 지정한다. 대상이 없는 PATCH도 `200 []`, DELETE도 `204`일 수 있으므로 같은 조건으로 GET해 결과를 확인한다.

## 로컬 리허설

이 폴더에서 Node.js 24 이상으로 실행한다.

```powershell
node server.mjs
```

API 주소는 `http://127.0.0.1:8787`, 공개 키는 `classroom-local`이다. 첫 실행에 `student01`부터 `student30`까지 안내 글 한 개씩 준비하고 글은 Git에서 제외된 `.local/local-data.json`에 보관한다. 브라우저 화면은 과목의 [정적 서버](../static-server/server.mjs)로 별도 실행한다. 로컬 HTTP 화면에서도 공용 HTTPS API를 호출할 수 있다.

로컬 서버는 수정·삭제 URL에 태그와 글 번호 중 하나라도 빠지면 `400`을 반환한다. 공용 Supabase에서는 요청 URL의 조건에 맞는 모든 행이 대상이므로 예제처럼 두 조건을 모두 보낸다.

```powershell
node --test server.test.mjs
```

## 공용 서버 검증

1. 수업 프로젝트에서 [완성 방명록 요청 파일](../../weeks/week13_guestbook_crud/examples/day2/web-week13/requests.http)의 접속 확인과 도움말을 실행한다. 두 응답은 모두 `200`이다.
2. 테스트 글 한 건을 POST하고 응답의 `id`를 기록한다. 같은 태그를 GET해 방금 생성한 글을 찾는다.
3. 그 글을 PATCH하고 같은 번호를 GET해 새 문장을 확인한다. DELETE 뒤 같은 번호를 GET하면 `[]`다.
4. [완성 방명록 화면](../../weeks/week13_guestbook_crud/examples/day2/web-week13/guestbook.html)에서도 같은 흐름을 실행해 브라우저의 교차 출처 요청을 확인한다.

## 운영 범위

수업용 글은 공개 데이터다. 별칭과 연습 문장을 사용한다. 수업이 끝나면 강의자가 공개 운영을 종료하고 실습 자료를 정리한다.

[Supabase Data REST API](https://supabase.com/docs/guides/api) · [Supabase API 키](https://supabase.com/docs/guides/getting-started/api-keys) · [열 권한](https://supabase.com/docs/guides/database/postgres/column-level-security)
