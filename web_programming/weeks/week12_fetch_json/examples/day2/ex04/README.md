# 서울 현재 기온

[실습 화면](index.html)에서 **기온 조회**를 누른다. [app.js](app.js)의 `fetch(url)`이 서울의 위도·경도와 `current=temperature_2m`을 보낸다. `await response.json()`으로 읽은 객체에서 `current.temperature_2m`은 기온, `current_units.temperature_2m`은 단위다.

VS Code에서 REST Client(`humao.rest-client`)를 설치하고 [requests.http](requests.http)를 연다. `@baseUrl`은 `https://api.open-meteo.com`이다. 공개 GET이라 API 키, `.env`, 별도 요청 헤더 없이 실행한다. 서울 요청 위 **Send Request**를 눌러 `200 OK`와 두 필드가 담긴 JSON 객체를 확인한다. 기온 값은 조회 시각에 따라 달라진다.

[Open-Meteo API 문서](https://open-meteo.com/en/docs)
