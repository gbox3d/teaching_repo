# ex04 · 폼 입력을 POST 본문에 넣기

[실습 화면](index.html)의 API 설정에서 수업용 공개 키와 배정받은 방명록 번호를 입력하고 설정 적용을 누른다. 메시지 앞뒤에 공백을 두고 **저장**을 누른다. 브라우저 개발자 도구의 Network에서 해당 POST의 Payload를 연다. `message`는 [app.js](app.js)가 `trim()`으로 앞뒤 공백을 제거한 값이다. `201` 응답에서 같은 문장을 찾는다.

VS Code REST Client(`humao.rest-client`)에서는 이 폴더의 [.env.example](.env.example)을 `.env`로 복사한다. 기본 수업 주소(`API_BASE_URL`)는 그대로 두고 `API_PUBLIC_KEY`에 수업용 공개 키, `BOOK_ID`에 배정받은 방명록 번호를 넣는다. [requests.http](requests.http)의 `message`를 다른 문장으로 바꾸고 **Send Request**를 누른다. 폼의 Payload와 이 JSON 본문에는 모두 `book_id`·`name`·`message`가 들어간다. 성공 응답에는 서버가 정한 `id`도 있다.
