# 위도와 HTTP 응답

[실습 화면](index.html)에서 위도를 선택하고 **기온 조회**를 누른다. 서울 위도 `37.5665`에서는 `HTTP 200 · ok true`와 기온이 나온다. 위도를 `999`로 바꾸면 `HTTP 400 · ok false`와 오류 이유가 나온다. 두 요청은 위도만 다르다.

[app.js](app.js)에서 `fetch`는 400에도 응답을 돌려주므로 `response.ok`로 분기한다. 오류 JSON의 `reason`에서 위도 허용 범위를 확인한다. 개발자 도구의 Network를 **Offline**으로 바꾸고 다시 조회하면 응답을 받지 못해 `catch`로 이동한다. 확인 후 **No throttling**으로 복구한다.

VS Code의 REST Client(`humao.rest-client`)로 [requests.http](requests.http)를 연다. `@baseUrl`은 `https://api.open-meteo.com`이다. API 키, `.env`, 별도 요청 헤더는 필요 없다. 두 요청 위의 **Send Request**를 차례로 눌러 성공 JSON의 `current.temperature_2m`과 오류 JSON의 `error`, `reason`을 비교한다.

[Open-Meteo API 문서](https://open-meteo.com/en/docs)
