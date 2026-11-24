# 12주차 따라하기 · Promise와 async/await로 배우는 fetch

## 1. 브라우저와 VS Code REST Client 준비

예제 화면 링크를 열거나 교재 저장소 최상위에서 다음 명령으로 HTML 파일을 연다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week12_fetch_json/examples 8000
```

첫 예제는 `http://localhost:8000/day1/ex01/`, 나라별 공휴일은 `http://localhost:8000/day2/ex06/`다. 타이머는 브라우저에서 실행하고, 조회 결과는 공개 API에서 읽는다.

VS Code에서는 REST Client(`humao.rest-client`)를 설치한다. ex02~ex06의 `requests.http`를 열고 요청 줄 위의 **Send Request**를 누른다. 예제마다 `@baseUrl`에 서비스의 기본 주소가 설정되어 있다. 필수 예제는 추가 헤더나 `.env` 설정 없이 실행한다.

## 2. 타이머와 Promise의 실행 순서

[ex01](examples/day1/ex01/index.html)을 열고 ‘타이머 시작’, ‘다음 줄 실행’, ‘타이머 완료’ 세 문장이 어떤 순서로 보일지 먼저 적는다. **타이머 시작**을 누르면 두 줄이 먼저 나오고 약 1초 뒤에 완료 문장이 붙는다.

타이머 콜백을 예약한 순간 `timer`는 대기 중(pending)이다. 타이머의 `resolve('3. 타이머 완료')`가 Promise를 성공(fulfilled) 상태로 바꾸면 `timer.then(...)`에 등록한 함수가 그 문장을 받는다. 실패(rejected)한 Promise의 이유는 `.catch()`에서 받는다.

## 3. Promise를 돌려주는 wait 함수

[ex01b](examples/day1/ex01b_wait/index.html)에서 **타이머 시작**을 누르면 ‘1. 시작’이 바로 나오고, 약 1초 간격으로 ‘2. 1초 지남’과 ‘3. 2초 지남’이 붙는다. `wait(ms)`는 ex01의 `new Promise`를 함수 안에 넣은 것이다. 호출할 때마다 대기 중인 Promise를 새로 돌려주고, `ms`밀리초 뒤 `resolve()`로 그 Promise를 성공시킨다.

```js
function wait(ms) {
  return new Promise(function (resolve) {
    setTimeout(function () {
      resolve();
    }, ms);
  });
}

button.addEventListener('click', function () {
  button.disabled = true;
  output.textContent = '1. 시작\n';

  wait(1000)
    .then(function () {
      output.textContent += '2. 1초 지남\n';
      return wait(1000);
    })
    .then(function () {
      output.textContent += '3. 2초 지남\n';
      button.disabled = false;
    });
});
```

첫 `.then()`이 `return wait(1000);`으로 새 Promise를 돌려주면 두 번째 `.then()`은 그 Promise가 성공할 때까지 기다린다. `return`을 지우면 첫 콜백의 반환값이 `undefined`가 되어 두 번째 콜백이 바로 실행되고, ‘3. 2초 지남’이 ‘2. 1초 지남’과 거의 함께 나온다. 확인한 뒤 `return`을 되돌린다.

## 4. async 함수와 await

[ex01c](examples/day1/ex01c_async_await/index.html)는 ex01b와 같은 순서를 `async` 함수로 쓴다. **타이머 시작**을 누르고 기다리는 동안 **클릭**을 누르면 클릭 수가 바로 올라간다. `await`는 이 `async` 함수만 멈추고, Promise가 성공하면 다음 줄로 넘어간다. 화면과 다른 리스너는 멈추지 않는다.

```js
clickButton.addEventListener('click', function () {
  count = count + 1;
  clickCount.textContent = `클릭 ${count}회`;
});

button.addEventListener('click', async function () {
  button.disabled = true;
  output.textContent = '1. 시작\n';

  await wait(1000);
  output.textContent += '2. 1초 지남\n';

  await wait(1000);
  output.textContent += '3. 2초 지남\n';

  button.disabled = false;
});
```

| 기다리는 Promise | ex01b의 then | ex01c의 await |
|---|---|---|
| 첫 `wait(1000)` | `wait(1000).then(function () { … })` | 첫 `await wait(1000);` |
| 두 번째 `wait(1000)` | 첫 콜백에서 `return wait(1000)` 후 다음 콜백이 실행됨 | 두 번째 `await wait(1000);` |

1차시 실습 0~8분에는 ex01c 폴더의 사본을 만든다. 사본의 ‘3. 2초 지남’ 출력 줄과 `button.disabled = false;` 사이에 `await wait(1000);`과 출력 한 줄을 더하면 약 3초 뒤 ‘4. 3초 지남’이 붙는다. 그동안에도 **클릭**이 동작하는지 확인한다.

## 5. async 함수가 돌려주는 값

[ex01d](examples/day1/ex01d_async_return/index.html)의 `makeMessage()`와 `makeError()`는 1초를 기다린 뒤 값을 돌려주거나 오류를 던지는 `async` 함수다.

```js
async function makeMessage() {
  await wait(1000);
  return '1초 타이머 완료';
}

async function makeError() {
  await wait(1000);
  throw new Error('타이머 실패');
}
```

**1초 타이머**를 누르면 ‘1. makeMessage() 호출’과 ‘2. 다음 줄 먼저 실행’이 바로 나오고, 약 1초 뒤 ‘3. 받은 값: 1초 타이머 완료’가 붙는다. 개발자 도구 Console을 먼저 연 뒤 누르면 `console.log(promise)`가 찍은 대기 중인 Promise가 보인다.

```js
messageButton.addEventListener('click', async function () {
  messageButton.disabled = true;
  errorButton.disabled = true;
  output.textContent = '1. makeMessage() 호출\n';

  const promise = makeMessage();
  console.log(promise);
  output.textContent += '2. 다음 줄 먼저 실행\n';

  const message = await promise;
  output.textContent += `3. 받은 값: ${message}\n`;

  messageButton.disabled = false;
  errorButton.disabled = false;
});
```

**실패 타이머**를 누르면 약 1초 뒤 ‘2. 실패 이유: 타이머 실패’가 나온다. `makeError()`가 던진 오류는 `await makeError()`에서 `catch`로 넘어가고, 두 버튼은 `finally`에서 다시 풀린다.

```js
errorButton.addEventListener('click', async function () {
  messageButton.disabled = true;
  errorButton.disabled = true;
  output.textContent = '1. makeError() 호출\n';

  try {
    await makeError();
  } catch (error) {
    output.textContent += `2. 실패 이유: ${error.message}\n`;
  } finally {
    messageButton.disabled = false;
    errorButton.disabled = false;
  }
});
```

| async 함수의 규칙 | ex01d에서 확인할 곳 |
|---|---|
| 호출하면 함수가 끝나기 전에 Promise를 받는다 | `const promise = makeMessage();` 다음 줄이 먼저 실행됨 |
| 함수 안의 `return` 값은 그 Promise의 성공 값이다 | `const message = await promise;`의 `message` |
| 함수 안의 `throw`는 그 Promise의 실패 이유다 | `catch (error)`의 `error.message` |
| `await`는 `async` 함수 안에서만 쓴다 | 두 클릭 리스너의 `async function` |
| `await`는 그 함수만 멈춘다 | 4절 ex01c에서 기다리는 동안 올라가는 클릭 수 |

`<script src="app.js" defer>`로 읽는 파일에서는 함수 밖에 `await`를 쓸 수 없다. `async`를 빼고 `await`를 쓰면 Console에 `SyntaxError: await is only valid in async functions and the top level bodies of modules`가 나오고 파일 전체가 실행되지 않는다.

## 6. 같은 GET을 두 방식으로 읽기

[ex02 요청](examples/day1/ex02/requests.http)에서 **Send Request**를 누른다. 응답은 `200 OK`이고 본문은 할 일 한 건을 나타내는 JSON 객체다. [ex02 화면](examples/day1/ex02/index.html)에서 **할 일 불러오기**를 누른 뒤 `title`이 같은지 확인한다.

ex02 폴더를 복사한다. 사본의 클릭 콜백을 `async function`으로 바꾸고 `.then()` 체인을 지운다. `try`에서 HTTP 응답과 JSON 본문을 순서대로 `await`하고 `todo.title`을 출력한다. `catch`에 실패 안내를, `finally`에 버튼 복구를 옮긴다. 사본을 실행해 제목을 확인한 뒤 [ex03 완성본](examples/day1/ex03/app.js)과 대조한다.

| 기다리는 값 | ex02의 then | ex03의 await |
|---|---|---|
| HTTP 응답 | `fetch(url).then(function (response) { … })` | `const response = await fetch(url);` |
| 본문에서 읽은 객체 | 첫 콜백에서 `return response.json()` 후 다음 콜백이 `todo`를 받음 | `const todo = await response.json();` |

`.then()` 콜백이 `response.json()`을 반환하면 다음 콜백은 본문을 읽을 때까지 기다린다. ex01b의 `return wait(1000);`과 같은 모양이다. `return`을 빼면 콜백의 반환값은 `undefined`다. ex03의 두 `await`는 ex01c의 `await wait(1000);` 두 줄과 같은 자리에서 HTTP 응답과 본문을 기다리고, 다음 줄에서 기다린 값을 쓴다. 브라우저는 기다리는 동안에도 다른 입력을 처리한다. `async` 함수의 반환값은 항상 Promise다.

## 7. 환율과 HTTP 상태 읽기

[ex04 요청](examples/day2/ex04/requests.http)은 Frankfurter에서 1달러당 원화 기준 환율을 가져온다. **Send Request**를 눌러 `date`와 `rates.KRW`를 찾는다. [환율 화면](examples/day2/ex04/index.html)에서 **환율 조회**를 누르고 기준일과 환율을 대조한다.

[ex05](examples/day2/ex05/index.html)에서 **카드 한 장 뽑기**와 **없는 카드 요청**을 눌러 Tarot API의 `200`과 `404` 응답을 비교한다. `200`의 본문에는 `cards[0].name`과 `cards[0].meaning_up`이 있다. `404`여도 서버가 응답했으므로 `await fetch(url)`은 Response를 돌려준다. 코드에서 `response.ok`가 `false`이면 본문을 읽기 전에 반환한다.

개발자 도구 Network에서 Disable cache를 체크하고 Offline으로 바꾸어 다시 요청한다. HTTP 응답을 받기 전에 `fetch()`가 실패해 `catch`가 실행된다. 확인 후 No throttling으로 되돌린다.

## 8. 나라별 공휴일 목록

[ex06](examples/day2/ex06/index.html)에서 나라를 골라 **공휴일 조회**를 누른다. [요청 파일](examples/day2/ex06/requests.http)의 `@year`를 화면에 표시된 연도로 맞추고 응답을 확인한다.

[app.js](examples/day2/ex06/app.js)는 선택한 나라 코드와 브라우저의 올해 연도로 `/api/v4/Holidays/{나라 코드}/{연도}` 경로를 만든다. `await response.json()`이 돌려준 배열에서 전국 공휴일을 골라 `date`와 `name`을 목록에 표시한다. 다른 나라를 조회하면 목록이 새 결과로 바뀐다.

Network에서 Disable cache를 체크하고 Offline으로 바꾼 뒤 같은 나라를 조회한다. 요청이 끝나면 `finally`가 나라 선택과 버튼을 다시 활성화한다. No throttling으로 돌아가 다시 조회한다.

## 9. 확인과 제출

1차시 실습은 ex01c 사본에 3초 줄 더하기·클릭 확인 8분, REST Client와 `.then()`으로 제목 읽기 10분, `async/await`로 직접 고쳐 실행하기 12분이다. 2차시 실습은 환율 응답 대조 8분, `200`과 `404` 비교 8분, 공휴일 목록 조회와 통신 복구 14분이다.

선택한 나라의 공휴일 목록과 Network의 GET `200`을 한 화면에 담는다. 접속을 복구한 뒤 버튼을 눌러 새 응답을 받는다. [실습지](lab.md)

[통합 예제 홈](examples/day2/web-week12/index.html)을 열면 `weather.js`가 서울 기온을 바로 조회한다. 도시를 바꾸고 **기온 조회**를 누르면 선택한 곳의 현재 기온이 표시된다. 방명록 메뉴에서 남긴 글은 `localStorage`에 저장된다. [서버 글 조회](examples/day2/web-week12/guestbook.html)는 선택 GET 실습이며, 서버에 글을 쓰는 POST는 13주에 다룬다. [통합 예제 실행 안내](examples/day2/web-week12/README.md)
