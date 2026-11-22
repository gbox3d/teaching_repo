# ex02 · then으로 할 일 한 건 읽기

VS Code REST Client(`humao.rest-client`)에서 [requests.http](requests.http)를 열고 GET 위 **Send Request**를 누른다. 기본 주소 `@baseUrl`은 JSONPlaceholder이고, 경로는 `/todos/1`이다. `Accept: application/json`은 JSON 응답을 요청한다. 공개 API라 키나 `.env` 없이 실행한다.

`200 OK` 응답에서 `id`가 1인 객체를 찾는다. [화면](index.html)에서 **할 일 불러오기**를 누르면 같은 객체의 `title`인 `delectus aut autem`이 표시된다.

[app.js](app.js)의 첫 `then`은 서버 응답을 받아 `response.json()`을 반환한다. 두 번째 `then`은 JSON에서 읽은 객체의 `title`을 화면에 적는다. [다음 예제](../ex03/README.md)에서 두 줄을 `await`로 바꾼다.
