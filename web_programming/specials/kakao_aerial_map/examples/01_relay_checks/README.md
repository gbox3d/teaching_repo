# relay 오류 응답

[00 접속·도움말](../00_connection/README.md)을 마친 뒤 같은 서버에서 [requests.http](requests.http)를 실행한다. REST Client의 **Send Request**로 각 요청을 따로 보내고 403·400·405를 비교한다. `@baseUrl`은 서버 주소이며 Referer에도 같은 값을 사용한다. GET에는 본문과 Content-Type이 없다. 인증 키는 요청에 넣지 않는다.

Sec-Fetch-Site와 Referer는 로컬 relay가 검사하는 요청 문맥이다. 여기서는 REST Client로 오류 분기를 관찰하기 위해 직접 적는다. 이 헤더가 사용자를 인증하는 비밀 값은 아니다. 성공 이미지 요청은 [완성 앱](../app/index.html)에서 공식 SDK가 생성한 source로 수행하며 URL을 임의로 조립하지 않는다.

완성 앱은 반드시 `http://localhost:3000`으로 연다. 공용 정적 미리보기와 GitHub Pages에는 Node relay가 없어 지도 이미지 전달이 동작하지 않는다. 키 없이도 로컬 이미지의 Canvas 편집은 실습할 수 있다.
