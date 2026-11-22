# ex06 · 저장한 뒤 목록 새로 불러오기

[실습 화면](index.html)의 API 설정에서 수업용 공개 키와 배정받은 방명록 번호를 입력하고 설정 적용을 누른다. **저장 요청**을 한 번 누른다. Network에서 POST `201` 다음에 GET `200`이 이어지는지 본다. [app.js](app.js)는 저장 응답을 받은 다음 `loadMessages()`를 호출한다. 저장 완료 뒤 목록만 불러오지 못한 경우 **새로 불러오기**를 눌러 GET만 다시 보낸다.

VS Code REST Client(`humao.rest-client`)에서는 이 폴더의 [.env.example](.env.example)을 `.env`로 복사한다. 기본 수업 주소(`API_BASE_URL`)는 그대로 두고 `API_PUBLIC_KEY`에 수업용 공개 키, `BOOK_ID`에 배정받은 방명록 번호를 넣는다. [requests.http](requests.http)에서 POST와 GET의 **Send Request**를 차례로 누른다. 첫 응답에서 확인한 `id`를 두 번째 응답의 글 목록에서 찾는다. 이 두 요청이 브라우저에서 **저장 요청** 한 번으로 실행된다.
