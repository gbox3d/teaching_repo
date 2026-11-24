# 13주차 따라하기 · 방명록 글 하나의 CRUD

## 1. 예제 열기

저장소 루트에서 정적 서버를 시작한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week13_guestbook_crud/examples 8113
```

브라우저에서 `http://localhost:8113/day1/ex01_create/`를 연다. 정적 서버는 HTML과 JavaScript를 보내고, 방명록 데이터는 수업용 Supabase API에 저장한다.

## 2. REST Client와 브라우저 설정

1. [설정 견본](examples/day1/ex01_create/config.example.json)을 같은 폴더의 `config.json`으로 복사한다. `API_BASE_URL`에는 수업 주소, `API_PUBLIC_KEY`에는 배부받은 공개 키, `BOOK_ID`에는 내 방명록 태그를 넣는다.
2. VS Code에 REST Client(`humao.rest-client`)를 설치한다. `requests.http` 옆의 `.env.example`을 `.env`로 복사하고 같은 세 값을 넣는다. 두 설정 파일을 나머지 예제 폴더에도 복사한다.
3. [첫 요청 파일](examples/day1/ex01_create/requests.http)에서 `GET /rest/v1/about`, `GET /rest/v1/help` 위의 **Send Request**를 차례로 누른다. 각각 `200 OK`와 서버 소개, 사용 가능한 요청 목록을 확인하면 준비가 끝난다.

실제 `config.json`과 `.env`는 Git에서 제외한다. [학생용 API 안내](../../tools/guestbook-api/student-guide.md#1-접속-주소와-설정)

## 3. Create · 글 생성

[생성 화면](examples/day1/ex01_create/index.html)에 별칭과 ‘토요일 모임’을 입력하고 **저장**을 한 번 누른다. 응답은 `201 Created`이며 서버가 발급한 글 번호가 화면에 나온다. 이 번호를 적어 둔다. REST Client로 실습한다면 [생성 요청](examples/day1/ex01_create/requests.http)의 POST를 한 번 실행하고 응답 배열 첫 행의 `id`를 기록한다.

## 4. Read · 내 글 조회

[조회 화면](examples/day1/ex02_read/index.html)에서 **목록 보기**를 누른다. 기록한 번호와 ‘토요일 모임’이 같은 줄에 있는지 본다. [조회 요청](examples/day1/ex02_read/requests.http)의 `book_id=eq.` 뒤에는 내 방명록 태그가 들어간다. 서버가 돌려준 `200 OK` 응답에서도 같은 글을 찾는다.

## 5. Update · 메시지 수정

[수정 화면](examples/day2/ex03_update/index.html)에서 기록해 둔 번호의 글을 선택한다. 메시지를 ‘일요일 모임’으로 바꾸고 **수정**을 누른다. [수정 요청](examples/day2/ex03_update/requests.http)에는 내 태그와 글 번호가 주소에, 바꿀 메시지가 JSON 본문에 들어간다. PATCH 다음 GET에서 원래 글 번호와 바뀐 문장을 확인한다.

## 6. Delete · 같은 글 삭제

[삭제 화면](examples/day2/ex04_delete/index.html)에서 방금 수정한 글 옆의 **삭제**를 누르고 확인창에서 글 번호를 확인한다. DELETE의 `204 No Content`에는 응답 본문이 없다. [삭제 확인 요청](examples/day2/ex04_delete/requests.http)에서 같은 태그와 번호로 GET을 보내 `200 OK`와 `[]`를 확인한다. 글이 남아 있으면 요청에 넣은 태그와 글 번호를 확인한다.

네 단계를 한 화면에서 연습할 때는 `http://localhost:8113/day2/web-week13/guestbook.html`을 연다. [완성 방명록](examples/day2/web-week13/guestbook.html) · [완성본 REST Client 요청](examples/day2/web-week13/requests.http)
