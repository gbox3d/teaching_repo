# ex03 · 빈 메시지를 보냈을 때

VS Code REST Client(`humao.rest-client`)에서는 이 폴더의 [.env.example](.env.example)을 `.env`로 복사한다. 기본 수업 주소(`API_BASE_URL`)는 그대로 두고 `API_PUBLIC_KEY`에 수업용 공개 키, `BOOK_ID`에 배정받은 방명록 번호를 넣는다. [requests.http](requests.http)에서 첫 POST의 **Send Request**를 누른다. 빈 `message`를 보내면 서버가 `400 Bad Request`와 오류 정보를 반환한다. 두 번째 POST는 같은 방명록에 문장 한 줄을 보낸다. `201 Created`와 글 번호를 확인한다.

[실습 화면](index.html)의 API 설정에서 수업용 공개 키와 배정받은 방명록 번호를 입력하고 설정 적용을 누른다. 메시지 칸을 비우고 **저장 요청**을 누른 뒤 문장을 입력해 두 응답을 비교한다. [app.js](app.js)에서 `response.ok`와 `response.status`를 확인한다.
