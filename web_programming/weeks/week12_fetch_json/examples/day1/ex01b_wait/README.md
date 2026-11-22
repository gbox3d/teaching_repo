# ex01b · Promise를 돌려주는 wait 함수

[화면](index.html)에서 **타이머 시작**을 누른다. ‘1. 시작’이 바로 나오고, 약 1초 뒤 ‘2. 1초 지남’, 다시 약 1초 뒤 ‘3. 2초 지남’이 붙는다. 세 번째 줄이 나올 때까지 버튼은 잠긴다.

[app.js](app.js)의 `wait(ms)`는 `setTimeout`을 Promise로 감싼 함수다. 호출하면 대기 중인 Promise를 바로 돌려주고, `ms`밀리초 뒤 `resolve()`로 그 Promise를 성공시킨다. 첫 `.then()`은 `return wait(1000);`으로 다음 Promise를 넘기고, 두 번째 `.then()`은 그 Promise가 성공한 뒤 실행된다. [ex02](../ex02/README.md)의 `return response.json()`과 같은 모양이다.

첫 `.then()`의 `return wait(1000);`에서 `return`을 지우고 저장한 뒤 새로고침해 **타이머 시작**을 누른다. ‘3. 2초 지남’이 ‘2. 1초 지남’과 거의 함께 나온다. 첫 `.then()`이 Promise를 넘기지 않으면 두 번째 `.then()`은 기다리지 않는다. 확인한 뒤 `return`을 되돌린다.

다음 [ex01c](../ex01c_async_await/README.md)에서는 같은 순서를 `async` 함수와 `await`로 쓴다.
