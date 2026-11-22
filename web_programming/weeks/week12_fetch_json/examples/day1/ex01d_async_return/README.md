# ex01d · async 함수가 돌려주는 값

[화면](index.html)에서 **1초 타이머**를 누른다. ‘1. makeMessage() 호출’과 ‘2. 다음 줄 먼저 실행’이 바로 나오고, 약 1초 뒤 ‘3. 받은 값: 1초 타이머 완료’가 붙는다. **실패 타이머**를 누르면 약 1초 뒤 ‘2. 실패 이유: 타이머 실패’가 나온다. 결과가 나올 때까지 두 버튼은 잠긴다.

[app.js](app.js)의 `makeMessage()`와 `makeError()`는 `async` 함수다. `const promise = makeMessage();`는 함수가 끝나기 전에 Promise를 받으므로 그다음 줄이 먼저 실행된다. 함수 안의 `return` 값은 그 Promise의 성공 값이 되고, `const message = await promise;`가 그 값을 받는다. `makeError()` 안의 `throw new Error('타이머 실패')`는 Promise의 실패 이유가 되어 `catch (error)`의 `error.message`로 들어간다. 개발자 도구 Console을 먼저 연 뒤 **1초 타이머**를 누르면 `console.log(promise)`가 찍은 Promise가 대기 중(pending)으로 보인다.

| async 함수의 규칙 | 이 예제에서 볼 곳 |
|---|---|
| 호출하면 함수가 끝나기 전에 Promise를 받는다 | `makeMessage()` 다음 줄이 먼저 실행 |
| `return` 값은 그 Promise의 성공 값이다 | `await promise`가 받은 ‘1초 타이머 완료’ |
| `throw`는 그 Promise의 실패 이유다 | `catch`의 `error.message` |
| `await`는 `async` 함수 안에서만 쓴다 | 두 클릭 리스너의 `async function` |
| `await`는 그 함수만 멈춘다 | [ex01c](../ex01c_async_await/README.md)에서 기다리는 동안 올라가는 클릭 수 |

`<script src="app.js" defer>`로 읽는 파일에서는 함수 밖에 `await`를 쓸 수 없다. 그래서 `await`를 쓰는 클릭 리스너 함수에 `async`를 붙였다. `makeMessage()`의 `return` 문자열을 다른 문장으로 바꾸고 새로고침하면 세 번째 줄의 받은 값이 바뀐다. `makeMessage()` 안의 1000을 3000으로 바꾸면 세 번째 줄만 늦어지고 앞의 두 줄은 그대로 바로 나온다.

다음 [ex02](../ex02/README.md)에서는 `fetch`가 반환한 Promise의 결과를 읽는다. 첫 HTTP 요청은 [ex02의 requests.http](../ex02/requests.http)에서 실행한다.
