# ex02 · 첫 글 저장과 글 번호

VS Code REST Client(`humao.rest-client`)에서는 이 폴더의 [.env.example](.env.example)을 `.env`로 복사한다. 기본 수업 주소(`API_BASE_URL`)는 그대로 두고 `API_PUBLIC_KEY`에 수업용 공개 키, `BOOK_ID`에 배정받은 방명록 번호를 넣는다.

[requests.http](requests.http)의 POST 본문에서 `message`를 자기 문장으로 바꾼다. **Send Request**를 한 번 눌러 `201 Created`와 응답 배열 첫 행의 `id`를 읽는다. 이어서 GET의 **Send Request**를 누르고 `200 OK` 목록에서 같은 `id`와 문장을 찾는다. GET은 목록만 다시 읽으므로 여러 번 실행해도 된다.

[실습 화면](index.html)을 열기 전에 [config.example.js](config.example.js)의 `const BOOK_ID = 'student01';`에서 `student01`을 배정받은 방명록 번호로 바꾼다. 화면을 처음 열면 공개 키를 묻는 창에 배부받은 키를 넣는다. 키는 브라우저의 localStorage에 남아 같은 주소로 여는 다른 예제도 함께 쓰고, 다음부터는 묻지 않는다. 창을 취소하거나 빈 칸으로 두면 HTTP 401로 저장이 거절되고, 새로고침하면 다시 묻는다. 키를 잘못 넣었으면 제목 아래 **공개 키 지우기**를 누르고 다시 넣는다. **저장 요청**은 [app.js](app.js)에 적힌 고정 문장으로 새 글을 한 건 보낸다. REST Client와 결과를 비교할 때도 POST 한 번마다 글 한 건이 생긴다.
