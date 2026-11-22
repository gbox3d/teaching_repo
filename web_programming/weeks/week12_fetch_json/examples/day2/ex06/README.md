# 도시별 현재 기온

[실습 화면](index.html)에서 서울과 부산을 번갈아 선택하고 **기온 조회**를 누른다. [app.js](app.js)는 선택한 도시의 좌표로 GET 요청을 보내고, 응답의 `current.temperature_2m`과 `current_units.temperature_2m`을 표시한다.

개발자 도구의 Network에서 느린 연결을 선택한다. 요청이 진행되는 동안 조회 버튼과 도시 선택이 잠기는지 본다. 이어 **Offline**으로 바꾸고 조회한다. 실패 안내가 나오면 **No throttling**으로 복구하고 같은 페이지에서 **기온 조회**를 다시 누른다. `finally`는 성공과 실패 양쪽에서 입력을 다시 활성화한다.

VS Code REST Client(`humao.rest-client`)에서 [requests.http](requests.http)를 연다. `@baseUrl`은 `https://api.open-meteo.com`이다. API 키, `.env`, 별도 요청 헤더는 필요 없다. 서울·부산 요청 위 **Send Request**를 각각 눌러 `200 OK`와 현재 기온·단위가 담긴 JSON 객체를 확인한다. 두 도시의 기온이 같을 수도 있다.

[Open-Meteo API 문서](https://open-meteo.com/en/docs)
