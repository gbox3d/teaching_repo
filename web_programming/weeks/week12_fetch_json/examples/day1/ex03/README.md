# ex03 · async/await로 같은 할 일 읽기

[화면](index.html)에서 **할 일 불러오기**를 누른다. [ex02](../ex02/README.md)와 같은 제목 `delectus aut autem`이 나온다. [ex02의 코드](../ex02/app.js)와 [이 예제의 코드](app.js)에서 서버 응답과 응답 본문을 받는 자리를 비교한다.

| ex02의 `then` | ex03의 `await` |
|---|---|
| 첫 `then`의 `response` | `const response = await fetch(url)` |
| 두 번째 `then`의 `todo` | `const todo = await response.json()` |

VS Code REST Client(`humao.rest-client`)로 [requests.http](requests.http)의 GET 위 **Send Request**를 누른다. `@baseUrl`은 JSONPlaceholder의 기본 주소이고 `Accept: application/json`은 원하는 응답 형식이다. 키나 `.env` 없이 `200 OK`와 할 일 객체 한 건을 받는다. 요청 경로의 `/todos/1`을 `/todos/2`로 바꿔 보내면 `id`와 `title`이 달라진다.
