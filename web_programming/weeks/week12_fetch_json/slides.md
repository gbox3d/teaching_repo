---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 12주차"
footer: "fetch · Promise · async/await"
---

# Promise와 async/await로 배우는 fetch

먼저 타이머로 실행 순서와 `async` 함수를 익힌다.
JSONPlaceholder에서 할 일 한 건을 읽은 뒤 환율·타로 카드·공휴일 API로 응답 읽기와 오류 처리를 연습한다.

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

GET [https://jsonplaceholder.typicode.com/todos/1](https://jsonplaceholder.typicode.com/todos/1)

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

GET [https://jsonplaceholder.typicode.com/todos/1](https://jsonplaceholder.typicode.com/todos/1)

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

## 2일차 · 0~5분 · 달러 기준 환율 요청

[ex04 화면](examples/day2/ex04/index.html) · [환율 요청](examples/day2/ex04/requests.http)

GET [https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW](https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW)

기준 통화는 `USD`, 조회할 통화는 `KRW`다.

**Send Request**를 눌러 `date`와 `rates`를 찾는다.

---

## 2일차 · 5~20분 · 중첩 객체에서 환율 읽기

| 응답 필드 | 화면에 표시할 값 |
|---|---|
| `date` | 기준일 |
| `rates.KRW` | 1달러에 해당하는 원화 기준 환율 |

[ex04 코드](examples/day2/ex04/app.js)에서 두 값을 읽는 줄을 찾아 실제 응답과 대조한다.

---

## 2일차 · 20~35분 · 200과 404 응답 구분

[ex05 화면](examples/day2/ex05/index.html) · [두 요청](examples/day2/ex05/requests.http)

| GET 주소 | HTTP 상태 | `response.ok` |
|---|---|---|
| [https://tarotapi.dev/api/v1/cards/random?n=1](https://tarotapi.dev/api/v1/cards/random?n=1) | 200 | true |
| [https://tarotapi.dev/api/v1/cards/zzmissing](https://tarotapi.dev/api/v1/cards/zzmissing) | 404 | false |

서버가 `404`를 보내도 `fetch()`는 Response를 돌려준다. 본문을 읽기 전에 `response.ok`를 확인한다. `200`이면 `cards[0]`의 이름과 뜻을 읽는다.

---

## 2일차 · 35~45분 · 통신 실패와 catch

[ex06 공휴일 실습](examples/day2/ex06/index.html) · [코드](examples/day2/ex06/app.js)

1. 페이지를 열어 둔 상태에서 개발자 도구 Network의 Disable cache를 체크하고 Offline으로 바꾼다.
2. **공휴일 조회**를 누른다. HTTP 응답을 받기 전에 `fetch()`가 실패해 `catch`가 실행된다.
3. **No throttling**으로 되돌린 뒤 같은 나라를 다시 조회한다.

HTTP 오류도 `catch`에서 처리하려면 `response.ok`를 검사한 뒤 `throw`한다.

---

## 2일차 · 45~55분 · 공휴일 배열에서 목록 만들기

| 나라 | 2026년 GET 주소 |
|---|---|
| 한국 | [https://nagerholidays.com/api/v4/Holidays/KR/2026](https://nagerholidays.com/api/v4/Holidays/KR/2026) |
| 일본 | [https://nagerholidays.com/api/v4/Holidays/JP/2026](https://nagerholidays.com/api/v4/Holidays/JP/2026) |
| 미국 | [https://nagerholidays.com/api/v4/Holidays/US/2026](https://nagerholidays.com/api/v4/Holidays/US/2026) |

브라우저 예제는 올해 연도를 URL 끝에 넣는다.

ex06은 응답 배열에서 전국 공휴일을 골라 `date`와 `name`을 목록에 표시한다. 새 결과로 목록을 교체하며, `finally`에서 조회 버튼을 다시 활성화한다. [나라별 요청](examples/day2/ex06/requests.http)

---

## 2일차 · 55~60분 · 실습 안내

| 실습 시간 | 학생 활동 |
|---|---|
| 0~8분 | 환율 화면의 기준일과 값을 응답과 대조 |
| 8~16분 | 임의 카드와 없는 카드를 조회해 `200`과 `404` 비교 |
| 16~30분 | 나라별 공휴일 조회, Offline 실패 뒤 재시도 |

필수 결과물은 [나라별 공휴일 목록](examples/day2/ex06/index.html)이다. 목록과 Network의 GET `200`을 함께 캡처한다. [실습지](lab.md)

---

## 선택 실습 · 세 도시의 현재 기온

도시 주소를 열고 `current.temperature_2m`(기온)과 `current_units.temperature_2m`(단위)을 찾는다. 예제 화면에서 같은 도시의 **기온 조회** 결과와 비교한다.

**서울**\
[https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m](https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m)

**전주**\
[https://api.open-meteo.com/v1/forecast?latitude=35.8248&longitude=127.1480&current=temperature_2m](https://api.open-meteo.com/v1/forecast?latitude=35.8248&longitude=127.1480&current=temperature_2m)

**익산**\
[https://api.open-meteo.com/v1/forecast?latitude=35.9439&longitude=126.9544&current=temperature_2m](https://api.open-meteo.com/v1/forecast?latitude=35.9439&longitude=126.9544&current=temperature_2m)

[ex07 날씨 화면](examples/day2/ex07/index.html) · [세 도시의 REST Client 요청](examples/day2/ex07/requests.http)

---

# 12주 통합 예제와 13주 방명록

[통합 예제 홈](examples/day2/web-week12/index.html)은 날씨를 조회하고 방명록 메뉴는 글을 브라우저에 저장한다.

[서버 글 조회](examples/day2/web-week12/guestbook.html)는 다른 선택 실습이다. 공개 키를 `apikey` 헤더에 넣어 [REST Client 요청](examples/day2/web-week12/requests.http)을 보낸다. 아래는 `student01`의 예시다.

- [https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/about](https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/about)
- [https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/help?order=step.asc](https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/help?order=step.asc)
- [https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/guestbook?book_id=eq.student01&select=id,name,message,created_at&order=id.desc&limit=50](https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/guestbook?book_id=eq.student01&select=id,name,message,created_at&order=id.desc&limit=50)

13주에는 같은 서버에 글을 저장하고 수정·삭제한다. [통합 예제 실행 안내](examples/day2/web-week12/README.md)
