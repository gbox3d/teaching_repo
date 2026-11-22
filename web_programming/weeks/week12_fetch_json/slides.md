---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 12주차"
footer: "fetch · Promise · async/await"
---

# Promise와 async/await로 배우는 fetch

먼저 타이머로 실행 순서와 `async` 함수를 익힌다.
JSONPlaceholder에서 할 일 한 건을 읽고, 같은 방식으로 서울과 부산의 기온을 조회한다.

각 차시 강의·시연 60분, 실습 30분. [예제 목록](examples/README.md)

---

## 1일차 · 0~5분 · 타이머 준비

[ex01 화면](examples/day1/ex01/index.html) · [코드](examples/day1/ex01/app.js)

버튼을 누르기 전에 로그 세 줄의 순서를 적는다. 버튼을 누르고 타이머가 끝날 때까지 어떤 줄이 먼저 보이는지 관찰한다.

ex01~ex01d는 브라우저 타이머만 쓴다. 뒤의 공개 API 예제도 키 없이 바로 실행한다.

---

## 1일차 · 5~12분 · 타이머를 기다리는 동안

1. **타이머 시작**을 누르면 첫 줄이 보인다.
2. 타이머를 예약한 뒤 다음 줄이 바로 실행된다.
3. 약 1초 뒤에 결과를 받은 콜백이 마지막 줄을 표시한다.

```js
const timer = new Promise(function (resolve) {
  setTimeout(function () { resolve('3. 타이머 완료'); }, 1000);
});
```

`new Promise(...)`는 대기 중인 Promise를 바로 돌려준다. 브라우저는 기다리는 동안 다른 입력도 처리한다.

---

## 1일차 · 12~16분 · Promise를 돌려주는 wait 함수

[ex01b 화면](examples/day1/ex01b_wait/index.html) · [코드](examples/day1/ex01b_wait/app.js)

```js
function wait(ms) {
  return new Promise(function (resolve) {
    setTimeout(function () {
      resolve();
    }, ms);
  });
}
```

`wait(1000)`을 호출하면 대기 중인 Promise를 바로 받는다. 약 1초 뒤 `resolve()`가 실행되면 그 Promise가 성공한다. ex01c와 ex01d도 이 함수를 쓴다.

---

## 1일차 · 16~20분 · Promise를 돌려주는 wait 함수

| 상태 | 의미 | ex01b에서 |
|---|---|---|
| pending | 결과를 기다리는 중 | `wait(1000)`을 호출한 직후 |
| fulfilled | 작업이 성공해 값이 정해짐 | 약 1초 뒤 `resolve()`가 실행된 뒤 |
| rejected | 작업이 실패해 이유가 정해짐 | 이 예제에는 없음. ex01d의 실패 타이머 |

첫 `.then()`이 `return wait(1000);`으로 다음 Promise를 넘기면 두 번째 `.then()`은 그 Promise가 성공한 뒤 실행된다. `return`을 빼면 3번 줄이 언제 나오는지는 선택 관찰로 확인한다.

---

## 1일차 · 20~30분 · async 함수와 await

[ex01c 화면](examples/day1/ex01c_async_await/index.html) · [코드](examples/day1/ex01c_async_await/app.js)

```js
button.addEventListener('click', async function () {
  output.textContent = '1. 시작\n';
  await wait(1000);
  output.textContent += '2. 1초 지남\n';
  await wait(1000);
  output.textContent += '3. 2초 지남\n';
});
```

`await`는 이 `async` 함수만 멈춘다. Promise가 성공하면 다음 줄로 넘어간다. 기다리는 동안에도 **클릭**을 누르면 클릭 수가 올라간다. ex01b의 두 `.then()`과 같은 순서다.

---

## 1일차 · 30~34분 · async 함수가 돌려주는 값

[ex01d 화면](examples/day1/ex01d_async_return/index.html) · [코드](examples/day1/ex01d_async_return/app.js)

```js
async function makeMessage() {
  await wait(1000);
  return '1초 타이머 완료';
}

messageButton.addEventListener('click', async function () {
  const promise = makeMessage();
  console.log(promise);
  output.textContent += '2. 다음 줄 먼저 실행\n';
  const message = await promise;
  output.textContent += `3. 받은 값: ${message}\n`;
});
```

`makeMessage()`는 끝나기 전에 Promise를 돌려준다. Console에 찍힌 Promise는 대기 중이고, 약 1초 뒤 `await promise`가 `return` 값을 받는다.

---

## 1일차 · 34~38분 · async 함수가 돌려주는 값

| async 함수의 규칙 | ex01d에서 볼 곳 |
|---|---|
| 호출하면 바로 Promise를 받는다 | `makeMessage()` 다음 줄이 먼저 실행 |
| `return` 값은 성공 값이 된다 | `await promise`가 받은 문자열 |
| `throw`는 실패 이유가 된다 | **실패 타이머**의 `error.message` |
| `await`는 `async` 함수 안에서만 쓴다 | 클릭 리스너의 `async function` |
| `await`는 그 함수만 멈춘다 | ex01c에서 기다리는 동안의 클릭 수 |

`<script src="app.js" defer>`로 읽는 파일에서는 함수 밖에 `await`를 쓸 수 없다. 그래서 클릭 리스너 함수에 `async`를 붙인다.

---

## 1일차 · 38~48분 · 응답에서 할 일 제목까지

[ex02 화면](examples/day1/ex02/index.html) · [REST Client 요청](examples/day1/ex02/requests.http)

```js
fetch(url)
  .then(function (response) {
    if (!response.ok) throw new Error('HTTP ' + response.status);
    return response.json();
  })
  .then(function (todo) {
    output.textContent = todo.title;
  });
```

첫 콜백은 HTTP 응답을 받는다. JSON을 읽는 Promise를 반환하면 다음 콜백은 할 일 객체를 받는다. ex01b의 `return wait(1000);`과 같은 모양이다.

---

## 1일차 · 48~55분 · 같은 요청에 await 쓰기

[ex03 화면](examples/day1/ex03/index.html) · [코드](examples/day1/ex03/app.js)

```js
const response = await fetch(url);
if (!response.ok) throw new Error('HTTP ' + response.status);
const todo = await response.json();
output.textContent = todo.title;
```

ex01c의 두 `await wait(1000);` 자리에 `await fetch(url)`과 `await response.json()`이 들어간 모양이다. 브라우저는 기다리는 동안에도 입력을 처리한다.

---

## 1일차 · 55~60분 · 실습 안내

| 실습 시간 | 학생 활동 |
|---|---|
| 0~8분 | ex01c 사본에 `await wait(1000);`과 출력 한 줄을 더해 ‘4. 3초 지남’ 표시, 기다리는 동안 **클릭** 확인 |
| 8~18분 | ex02 **Send Request**와 화면의 제목 대조 |
| 18~30분 | ex02 사본의 `.then()`을 `try/catch`와 두 `await`로 고쳐 실행하고 ex03과 대조 |

선택 관찰은 ex01b에서 `return`을 뺀 뒤 3번 줄이 나오는 때와 ex01d의 **실패 타이머**다. [실습지](lab.md)

---

## 2일차 · 0~5분 · 서울 날씨 요청

[ex04 화면](examples/day2/ex04/index.html) · [서울 기온 요청](examples/day2/ex04/requests.http)

`GET /v1/forecast`에 서울의 위도와 경도를 붙인다. `current=temperature_2m`은 현재 지상 2m 기온을 요청한다.

**Send Request**를 눌러 `current`와 `current_units`를 찾는다.

---

## 2일차 · 5~20분 · 기온과 단위 읽기

| 응답 필드 | 화면에 표시할 값 |
|---|---|
| `weather.current.temperature_2m` | 현재 기온 |
| `weather.current_units.temperature_2m` | 기온의 단위 |

[ex04 코드](examples/day2/ex04/app.js)에서 두 값을 찾아 실제 응답과 대조한다. API를 호출하는 시각에 따라 기온은 달라진다.

---

## 2일차 · 20~35분 · 위도 오류와 HTTP 응답

[ex05 화면](examples/day2/ex05/index.html) · [두 요청](examples/day2/ex05/requests.http)

| 위도 | HTTP 상태 | `response.ok` |
|---|---|---|
| 서울 37.5665 | 200 | true |
| 999 | 400 | false |

400이어도 서버가 응답했으므로 `fetch()`의 Promise는 성공한다. 상태와 오류 본문의 `reason`을 읽으면 요청의 어느 값이 잘못됐는지 알 수 있다.

---

## 2일차 · 35~45분 · 통신 실패와 catch

[ex06 날씨 실습](examples/day2/ex06/index.html) · [코드](examples/day2/ex06/app.js)

1. 페이지를 열어 둔 상태에서 개발자 도구 Network를 **Offline**으로 바꾼다.
2. **기온 조회**를 누른다. HTTP 응답을 받기 전에 `fetch()`가 실패해 `catch`가 실행된다.
3. **No throttling**으로 되돌린 뒤 같은 도시를 다시 조회한다.

HTTP 400도 `catch`에서 처리하려면 코드에서 `response.ok`를 검사해 오류를 던진다.

---

## 2일차 · 45~55분 · 도시 선택과 재시도

| 도시 | 위도 | 경도 |
|---|---|---|
| 서울 | 37.5665 | 126.9780 |
| 부산 | 35.1796 | 129.0756 |

ex06은 선택한 도시의 좌표로 URL을 만든다. 요청을 보내기 전 버튼을 잠그고, `finally`에서 다시 활성화한다. 버튼을 누를 때마다 도시를 고를 수 있다. [도시별 요청](examples/day2/ex06/requests.http)

---

## 2일차 · 55~60분 · 실습 안내

| 실습 시간 | 학생 활동 |
|---|---|
| 0~8분 | 서울 기온과 단위를 응답과 대조 |
| 8~16분 | 서울 위도와 999의 HTTP 상태 비교 |
| 16~30분 | 서울·부산 조회, Offline 실패 뒤 재시도 |

필수 결과물은 [도시별 날씨](examples/day2/ex06/index.html)다. 기온 화면과 Network의 GET 200을 함께 캡처한다. [실습지](lab.md)

---

# 다음 주 · 수업 방명록에 글 쓰기

13주에는 수업용 Supabase에 JSON을 POST하고 새로 생긴 글 번호를 읽는다. 목록을 읽는 함수는 13주 시작 코드에 들어 있다.

미리 해 볼 학생은 선택 방명록 폴더의 `config.example.js`에서 `BOOK_ID`를 배정받은 방명록 번호로 바꾼다. [선택 방명록](examples/day2/web-week12/guestbook.html)을 처음 열면 공개 키를 묻는 창이 뜬다. 배부받은 키를 넣으면 이 브라우저에 저장된다. 잘못 넣었으면 **공개 키 지우기**를 누르고 다시 넣는다. [접속 확인·도움말·목록 요청](examples/day2/web-week12/requests.http) · [설정 방법](examples/day2/web-week12/README.md)
