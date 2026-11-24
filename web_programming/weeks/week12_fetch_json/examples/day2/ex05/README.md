# 타로 카드로 HTTP 200과 404 비교

[실습 화면](index.html)에서 **카드 한 장 뽑기**를 누르면 `HTTP 200 · ok true`와 카드 이름·정방향 해석이 나온다. **없는 카드 요청**을 누르면 `HTTP 404 · ok false`가 나온다.

[app.js](app.js)는 `response.status`와 `response.ok`를 먼저 표시한다. `ok`가 true일 때 `cards[0].name`과 `cards[0].meaning_up`을 읽는다.

개발자 도구를 열어 둔 상태에서 Network의 **Disable cache**를 켜고 Offline으로 바꾼다. **카드 한 장 뽑기**를 누르면 HTTP 응답 없이 `catch`에서 요청 실패를 표시한다. 확인 후 No throttling으로 복구한다.

VS Code REST Client(`humao.rest-client`)에서 [requests.http](requests.http)를 연다. `@baseUrl`은 `https://tarotapi.dev`다. API 키, `.env`, 추가 요청 헤더 없이 각 GET 위 **Send Request**를 누른다. `200 OK`의 카드 배열과 `404 Not Found` 상태를 확인한다.

[Tarot API 문서](https://github.com/ekelen/tarot-api)
