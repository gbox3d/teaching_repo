# ex05 · 저장을 기다리는 동안의 폼

[실습 화면](index.html)의 API 설정에서 수업용 공개 키와 배정받은 방명록 번호를 입력하고 설정 적용을 누른다.

1. 개발자 도구의 Network에서 느린 연결을 선택한다. 메시지를 입력하고 **저장**을 누른다. 응답을 기다리는 동안 버튼이 잠기는지 본다.
2. 연결을 Offline으로 바꾼 뒤 새 문장을 입력해 저장한다. 통신 실패 뒤 문장은 입력 칸에 남고 버튼은 다시 활성화된다. 실습이 끝나면 No throttling으로 복구한다.

VS Code REST Client(`humao.rest-client`)에서는 이 폴더의 [.env.example](.env.example)을 `.env`로 복사한다. 기본 수업 주소(`API_BASE_URL`)는 그대로 두고 `API_PUBLIC_KEY`에 수업용 공개 키, `BOOK_ID`에 배정받은 방명록 번호를 넣는다. [requests.http](requests.http)의 첫 **Send Request**는 별칭이 빈 글을 보낸다. 서버는 `400`과 오류 정보를 돌려준다. 두 번째 요청은 `GET`으로 현재 글 목록을 읽는다(`200`). 저장 응답을 받지 못한 경우에는 이 목록부터 확인한다. 버튼 잠금과 입력 보존은 브라우저의 [app.js](app.js)가 처리한다.
