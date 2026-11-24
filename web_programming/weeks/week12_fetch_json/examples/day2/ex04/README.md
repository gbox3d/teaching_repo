# 달러 기준 환율 읽기

[실습 화면](index.html)에서 **환율 조회**를 누른다. [app.js](app.js)는 Frankfurter에 기준 통화 `base=USD`와 조회할 통화 `symbols=KRW`를 보낸다. 응답 JSON 객체의 `rates.KRW`는 1달러당 원화 기준 환율이고 `date`는 환율 기준일이다.

VS Code REST Client(`humao.rest-client`)에서 [requests.http](requests.http)를 연다. `@baseUrl`은 `https://api.frankfurter.dev`다. API 키, `.env`, 추가 요청 헤더 없이 GET 요청 위 **Send Request**를 누른다. `200 OK` 응답의 환율과 기준일을 브라우저 화면과 대조한다.

[Frankfurter API 문서](https://frankfurter.dev/#v1)
