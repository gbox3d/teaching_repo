# 13주차 온라인 방명록

제공된 목록에 글쓰기 폼을 연결한 완성본이다. [config.example.js](config.example.js)의 `const BOOK_ID = 'student01';`에서 `student01`을 배정받은 방명록 번호로 바꾼다. [실습 화면](guestbook.html)을 처음 열면 공개 키를 묻는 창이 뜬다. 배부받은 키를 넣으면 서버 목록을 불러오고, 키는 브라우저의 localStorage에 남아 다음부터 묻지 않는다. 창을 취소하거나 빈 칸으로 두면 HTTP 401로 조회·저장이 실패하고, 새로고침하면 다시 묻는다. 키를 잘못 넣었거나 키가 바뀌면 제목 아래 **공개 키 지우기**를 누르고 새 키를 넣는다. 별칭과 메시지를 입력해 **남기기**을 누른다. Network에서 POST `201`의 글 번호를 읽고 이어진 GET `200`에서 같은 번호를 찾는다. 다른 브라우저에서는 같은 페이지를 열어 묻는 창에 공개 키를 넣은 뒤 같은 글을 찾는다.

## 학생이 연결할 부분

[guestbook.js](guestbook.js)에서 폼 값을 읽는 두 줄, `JSON.stringify`로 요청 본문을 만드는 줄, 저장 뒤 `loadMessages()`를 호출하는 줄을 찾는다. 저장 실패 뒤 입력이 남는지, 저장에 성공한 뒤 목록만 실패했을 때 **새로 불러오기**로 조회를 재시도할 수 있는지 확인한다.

## REST Client

VS Code REST Client(`humao.rest-client`)에서는 이 폴더의 [.env.example](.env.example)을 `.env`로 복사한다. 기본 수업 주소(`API_BASE_URL`)는 그대로 두고 `API_PUBLIC_KEY`에 수업용 공개 키, `BOOK_ID`에 배정받은 방명록 번호를 넣는다. [requests.http](requests.http)에 별칭과 문장을 적은 뒤 POST의 **Send Request**를 누른다. 응답 배열에는 서버가 정한 `id`가 들어 있다. GET의 **Send Request**로 같은 글을 확인한다. 저장 응답을 놓친 경우에도 GET으로 먼저 확인한다.

## 파일과 다음 주

| 파일 | 역할 |
|---|---|
| [guestbook.html](guestbook.html) | 별칭·메시지 폼과 서버 글 목록 |
| [guestbook.js](guestbook.js) | 폼 제출, POST, 저장 뒤 목록 조회 |
| [config.example.js](config.example.js) | 수업 API 주소·방명록 번호, 공개 키 입력·저장과 **공개 키 지우기** 동작 |
| [홈](index.html)·[내 정보](about.html) | 이전 주차에서 이어 쓴 두 페이지 |

14주에는 같은 방명록에 글 번호를 이용한 수정과 삭제를 추가한다.
