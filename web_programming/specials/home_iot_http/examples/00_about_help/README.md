# 접속과 도움말

서버 소개 객체와 여섯 요청의 안내 배열을 읽는다. 장치 상태는 바꾸지 않는다.

## 실행

특강 루트 home_iot_http에서 Node.js 24 이상으로 실행한다.

```powershell
node examples/simulator/server.mjs
```

화면: http://localhost:8014/examples/00_about_help/

## REST Client

VS Code 확장 REST Client (humao.rest-client)를 설치하고 [requests.http](requests.http)를 연다. 맨 위 @baseUrl은 현재 Node 서버 주소다. 포트를 바꿨으면 이 값도 바꾼다. 인증 헤더와 .env는 필요 없다. PATCH에는 Content-Type: application/json을 사용한다.

about→help 순서로 요청 위 **Send Request**를 누르고 200 응답을 확인한다. 다음 요청은 주석의 상태 번호·응답과 비교한다. 브라우저에서 같은 요청을 실행한 뒤 Network와 화면도 확인한다. 이 서버는 같은 PC의 상태만 공유하며 GitHub Pages에서는 실행되지 않는다.

서버를 멈추면 조회 실패 안내가 나오고 버튼이 다시 활성화된다. 재시작 후 다시 요청한다.

[전체 실험과 관찰 기준](../../lab.md) · [예제 목록](../README.md)
