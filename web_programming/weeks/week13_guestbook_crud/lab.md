# 13주차 실습 · 같은 글 번호로 CRUD 실행

내 방명록에 ‘토요일 모임’을 저장하고 ‘일요일 모임’으로 고친 뒤 삭제한다. 첫 응답의 글 번호를 2일차까지 보관한다. [설정과 실행](walkthrough.md#2-rest-client와-브라우저-설정)

## 1일차 실습

| 시간 | 할 일 | 확인할 결과 |
|---|---|---|
| 0–5분 | [첫 요청 파일](examples/day1/ex01_create/requests.http)에서 소개와 도움말 위의 **Send Request**를 누른다 | 두 요청 모두 `200 OK` |
| 5–15분 | **Create.** [생성 화면](examples/day1/ex01_create/index.html)에서 별칭과 ‘토요일 모임’을 저장하고 글 번호를 적는다 | POST `201`, 서버가 발급한 `id` |
| 15–30분 | **Read.** [조회 화면](examples/day1/ex02_read/index.html)에서 목록을 열어 같은 번호를 찾는다. 새로고침 후에도 확인한다 | GET `200`, 같은 번호의 ‘토요일 모임’ |

## 2일차 실습

| 시간 | 할 일 | 확인할 결과 |
|---|---|---|
| 0–10분 | **Update.** [수정 화면](examples/day2/ex03_update/index.html)에서 어제 기록한 번호를 선택하고 ‘일요일 모임’으로 수정한다 | PATCH `200`, 응답에 수정된 글 한 건 |
| 10–15분 | [수정 요청 파일](examples/day2/ex03_update/requests.http)에서 같은 번호의 GET을 실행한다 | 원래 번호에 ‘일요일 모임’이 저장되어 있다 |
| 15–30분 | **Delete.** [삭제 화면](examples/day2/ex04_delete/index.html)에서 같은 글 옆의 **삭제**를 누르고 글 번호를 확인한다. [삭제 확인 요청](examples/day2/ex04_delete/requests.http)으로 그 번호를 다시 읽는다 | DELETE `204`, 이어지는 GET `200`과 `[]` |

## 제출

실습한 글 번호, 조회한 원문, 수정 후 문장, 삭제 후 GET 응답을 순서대로 기록한다. [완성 방명록](examples/day2/web-week13/guestbook.html)과 [완성본의 요청 파일](examples/day2/web-week13/requests.http)에서도 같은 순서로 실행할 수 있다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 401 응답 | 브라우저는 HTML 옆 `config.json`, REST Client는 요청 파일 옆 `.env`의 주소와 공개 키를 확인한다 |
| 방금 만든 글이 목록에 없다 | 생성·조회 예제의 `BOOK_ID`가 같은지 확인한다 |
| PATCH 응답이 `[]`이거나 DELETE 뒤 글이 남는다 | 요청 주소의 방명록 태그와 글 번호를 확인한 뒤 같은 번호를 다시 조회한다 |
