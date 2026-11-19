# 서버 접속과 도움말

Node.js 24에서 `../app` 폴더의 `npm start`로 서버를 시작한다. VS Code REST Client(`humao.rest-client`)를 설치하고 [requests.http](requests.http)의 **Send Request**를 위에서부터 실행한다. `@baseUrl` 기본값은 `http://localhost:3000`이며 서버 PORT를 바꿨다면 같은 값으로 수정한다.

이 세 요청은 인증·본문 헤더가 필요 없다. about의 200과 version, help의 네 항목, 설정의 setupRequired를 확인한다. 설정값은 [상위 안내](../README.md#설정)에 따르며 실제 키를 .http에 적지 않는다. 이 서버는 .env를 자동으로 읽지 않는다.

다음은 [relay 오류 확인](../01_relay_checks/README.md)이다.
