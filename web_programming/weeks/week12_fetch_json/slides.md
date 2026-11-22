---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 12주차"
footer: "fetch · Promise · async/await"
---

# Promise와 async/await로 배우는 fetch

먼저 타이머로 코드의 실행 순서를 확인한다.
JSONPlaceholder에서 할 일 한 건을 읽고, 같은 방식으로 서울과 부산의 기온을 조회한다.

각 차시 강의·시연 60분, 실습 30분. [예제 목록](examples/README.md)

---

## 1일차 · 0~5분 · 타이머 준비

[ex01 화면](examples/day1/ex01/index.html) · [코드](examples/day1/ex01/app.js)

버튼을 누르기 전에 로그 세 줄의 순서를 적는다. 버튼을 누르고 타이머가 끝날 때까지 어떤 줄이 먼저 보이는지 관찰한다.

이 예제는 브라우저만 쓴다. 뒤의 공개 API 예제도 키 없이 바로 실행한다.

---

## 1일차 · 5~15분 · 타이머를 기다리는 동안

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

## 1일차 · 15~30분 · Promise의 결과 받기

| 상태 | 의미 |
|---|---|
| pending | 결과를 기다리는 중 |
| fulfilled | 작업이 성공해 값이 정해짐 |
| rejected | 작업이 실패해 이유가 정해짐 |

ex01에서 타이머가 `resolve`를 호출하면 대기하던 Promise가 성공한다. `.then()`에 등록한 함수가 그 값을 받는다. 실패는 `.catch()`에서 처리할 수 있다.

---

## 1일차 · 30~40분 · 응답에서 할 일 제목까지

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

첫 콜백은 HTTP 응답을 받는다. JSON을 읽는 Promise를 반환하면 다음 콜백은 할 일 객체를 받는다.

---

## 1일차 · 40~55분 · 같은 요청에 await 쓰기

[ex03 화면](examples/day1/ex03/index.html) · [코드](examples/day1/ex03/app.js)

```js
const response = await fetch(url);
if (!response.ok) throw new Error('HTTP ' + response.status);
const todo = await response.json();
output.textContent = todo.title;
```

`await`는 이 `async` 함수가 다음 줄로 넘어가는 시점을 늦춘다. 브라우저는 그동안 입력을 처리한다. `async` 함수를 호출하면 호출자는 Promise를 받는다.

---

## 1일차 · 55~60분 · 실습 안내

| 실습 시간 | 학생 활동 |
|---|---|
| 0~8분 | ex01 로그 순서 예측과 확인 |
| 8~18분 | ex02 **Send Request**와 화면의 제목 대조 |
| 18~30분 | ex02 사본의 `.then()`을 `try/catch`와 두 `await`로 고쳐 실행하고 ex03과 대조 |

`return response.json()`에서 `return`을 빼면 다음 콜백이 받는 값이 무엇인지 적는다. [실습지](lab.md)

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

미리 해 볼 학생은 [선택 방명록](examples/day2/web-week12/guestbook.html)에서 공개 키와 방명록 번호를 입력한다. [접속 확인·도움말·목록 요청](examples/day2/web-week12/requests.http) · [설정 방법](examples/day2/web-week12/README.md)
