# ex02 · 첫 글 저장과 글 번호

VS Code REST Client(`humao.rest-client`)에서는 이 폴더의 [.env.example](.env.example)을 `.env`로 복사한다. 기본 수업 주소(`API_BASE_URL`)는 그대로 두고 `API_PUBLIC_KEY`에 수업용 공개 키, `BOOK_ID`에 배정받은 방명록 번호를 넣는다.

[requests.http](requests.http)의 POST 본문에서 `message`를 자기 문장으로 바꾼다. **Send Request**를 한 번 눌러 `201 Created`와 응답 배열 첫 행의 `id`를 읽는다. 이어서 GET의 **Send Request**를 누르고 `200 OK` 목록에서 같은 `id`와 문장을 찾는다. GET은 목록만 다시 읽으므로 여러 번 실행해도 된다.

[실습 화면](index.html)의 API 설정에서 수업용 공개 키와 배정받은 방명록 번호를 입력하고 설정 적용을 누른다. **저장 요청**은 [app.js](app.js)에 적힌 고정 문장으로 새 글을 한 건 보낸다. REST Client와 결과를 비교할 때도 POST 한 번마다 글 한 건이 생긴다.
