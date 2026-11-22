[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_fetch_json)

# 12주차 실습 · 할 일과 날씨를 비동기로 읽기

각 차시의 실습 시간은 30분이다. 예제 화면과 VS Code REST Client(`humao.rest-client`)를 준비한다. 공개 API 요청은 예제 폴더의 `requests.http`에 들어 있다. 기본 URL로 바로 요청하며 별도 헤더와 키 설정은 없다.

## 1일차 실습

| 시간 | 할 일 | 확인할 결과 |
|---|---|---|
| 0~8분 | [ex01c](examples/day1/ex01c_async_await/index.html) 폴더의 사본을 만든다. 사본 `app.js`의 ‘3. 2초 지남’ 출력 줄과 `button.disabled = false;` 사이에 `await wait(1000);`과 출력 한 줄을 더해 ‘4. 3초 지남’을 표시한다. 기다리는 동안 **클릭**을 누른다 | 약 3초 뒤 네 번째 줄이 붙고, 기다리는 동안에도 클릭 수가 올라간다 |
| 8~18분 | [ex02 요청](examples/day1/ex02/requests.http)에서 **Send Request**를 누르고 같은 예제의 화면에서도 할 일을 조회한다 | REST Client의 `200 OK` 본문에서 `id`와 `title`을 찾아 화면의 제목과 대조한다 |
| 18~30분 | ex02 폴더 사본에서 클릭 콜백을 `async function`으로 바꾼다. `.then()` 체인을 `try/catch`와 두 번의 `await`로 고쳐 실행한 뒤 [ex03 완성본](examples/day1/ex03/app.js)과 대조한다 | 직접 작성한 코드가 같은 제목을 표시하고 실패하면 안내를 표시한다 |

18~30분에 작성할 때는 `await fetch(url)`로 Response를 받고, `response.ok`를 확인한 뒤 `await response.json()`으로 할 일 객체를 읽는다. 버튼 복구는 `finally`에 둔다. 제목이 나오면 두 `await`가 각각 어떤 Promise를 기다렸는지 설명한다.

선택 관찰은 두 가지다. [ex01b](examples/day1/ex01b_wait/index.html)의 첫 `.then()`에서 `return wait(1000);`의 `return`을 빼고 ‘3. 2초 지남’이 나오는 때를 본다. [ex01d](examples/day1/ex01d_async_return/index.html)에서 **실패 타이머**를 누르고 `catch`가 받은 실패 이유를 확인한다.

### 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 버튼이 반응하지 않고 Console에 `SyntaxError: await is only valid in async functions and the top level bodies of modules`가 보인다 | `await`를 쓴 함수에 `async`가 있는지 확인한다. 클릭 리스너라면 `async function () { … }`이다 |
| ‘4. 3초 지남’이 ‘3. 2초 지남’과 함께 나온다 | 새로 더한 `wait(1000);` 앞에 `await`가 있는지 확인한다 |
| 4번 줄이 나오기 전에 **타이머 시작**을 다시 누를 수 있고 줄 순서가 섞인다 | 새 두 줄을 `button.disabled = false;` 위에 넣었는지 확인한다 |
| ex01b에서 ‘3. 2초 지남’이 ‘2. 1초 지남’과 함께 나온다 | 첫 `.then()`의 `return wait(1000);`에서 `return`이 빠졌는지 확인한다 |

## 2일차 실습

| 시간 | 할 일 | 확인할 결과 |
|---|---|---|
| 0~8분 | [ex04 요청](examples/day2/ex04/requests.http)을 보낸 뒤 서울 기온 화면과 JSON을 대조한다 | `current.temperature_2m`이 기온이고 `current_units.temperature_2m`이 단위다 |
| 8~16분 | [ex05 요청](examples/day2/ex05/requests.http)에서 서울의 위도와 `999`를 각각 보낸다 | 두 요청 모두 응답을 받는다. 서울은 200, 범위를 벗어난 위도는 400이다 |
| 16~30분 | [ex06](examples/day2/ex06/index.html)에서 서울·부산을 번갈아 조회한다. 페이지를 열어 둔 채 Network를 Offline으로 바꾸고 다시 조회한다. 연결을 복구하고 같은 도시로 재시도한다 | 도시 선택에 따라 좌표가 달라지고, 요청이 성공하거나 실패한 뒤 버튼을 다시 누를 수 있다 |

## 확인과 제출

1. 도시 하나를 선택해 조회하고 화면의 도시·기온·단위와 Network의 GET 200을 캡처한다. 서울·부산은 같은 기온일 수도 있으므로 요청 URL의 좌표로 구분한다.
2. 위도 오류(HTTP 400)와 Offline 실패 때 서버의 HTTP 응답을 받은 쪽을 고르고, `response.ok` 검사와 `catch`가 각각 언제 실행되는지 적는다.
3. 개발자 도구의 네트워크 설정을 **No throttling**으로 되돌린다. 재시도 뒤 새 결과가 보이는지 확인한다.

필수 실습은 ex06에서 끝난다. 수업 방명록으로 같은 GET을 연습하려면 [선택 예제](examples/day2/web-week12/README.md)를 사용한다. 이 예제에 필요한 공개 키와 방명록 번호는 강의자가 배부한다. 방명록 번호는 그 폴더 `config.example.js`의 `BOOK_ID`에 적는다. 공개 키는 방명록 화면을 처음 열 때 뜨는 창에 넣는다. 잘못 넣었으면 **공개 키 지우기**를 누르고 다시 넣는다.
