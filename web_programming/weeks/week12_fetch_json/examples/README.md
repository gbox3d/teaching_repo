# 12주차 예제 · Promise와 공개 API

1차시는 타이머 예제 ex01~ex01d로 Promise와 `async` 함수를 익힌다. 실습은 ex01c 사본에 3초 줄 더하기·클릭 확인 8분, REST Client와 `.then()`으로 제목 읽기 10분, `async/await`로 직접 고쳐 실행하기 12분이다. 2차시는 환율 응답에서 값을 읽고, 타로 카드 조회로 HTTP 상태를 비교한 뒤, 공휴일 배열을 목록으로 그린다. 각 차시는 강의·시연 60분, 학생 실습 30분이다.

| 예제 | 구분 | 화면 | 코드에서 볼 곳 |
|---|---|---|---|
| [ex01 타이머](day1/ex01/README.md) | 시연 | [실행 순서](day1/ex01/index.html) | 타이머·`resolve`·`.then()` |
| [ex01b wait 함수](day1/ex01b_wait/README.md) | 시연·선택 관찰 | [1초씩 두 번](day1/ex01b_wait/index.html) | `wait(ms)`가 돌려주는 Promise, `return wait(1000)` |
| [ex01c async 함수와 await](day1/ex01c_async_await/README.md) | 1차시 필수 | [await와 클릭 수](day1/ex01c_async_await/index.html) | 두 번의 `await wait(1000)`, 기다리는 동안 올라가는 클릭 수 |
| [ex01d async 함수가 돌려주는 값](day1/ex01d_async_return/README.md) | 시연·선택 관찰 | [성공과 실패 타이머](day1/ex01d_async_return/index.html) | 호출하자마자 받는 Promise, `return` 값, `throw`와 `catch` |
| [ex02 JSONPlaceholder](day1/ex02/README.md) | 1차시 필수 | [할 일 한 건](day1/ex02/index.html) | `fetch` → `return response.json()` → 제목 |
| [ex03 async/await](day1/ex03/README.md) | 대조 완성본 | [같은 할 일](day1/ex03/index.html) | 같은 요청을 두 번의 `await`로 읽기 |
| [ex04 Frankfurter](day2/ex04/README.md) | 2차시 필수 | [기준 환율](day2/ex04/index.html) | 고정 GET과 중첩 객체에서 기준일·환율 읽기 |
| [ex05 Tarot API](day2/ex05/README.md) | 2차시 필수 | [타로 카드 조회](day2/ex05/index.html) | `200`과 `404`, 본문을 읽기 전 `response.ok` 검사 |
| [ex06 Nager.Date](day2/ex06/README.md) | 2차시 필수 | [나라별 공휴일](day2/ex06/index.html) | 경로에 연도·나라 코드 넣기, 배열로 목록 그리기, 실패 뒤 재시도 |
| [ex07 Open-Meteo](day2/ex07/README.md) | 2차시 선택 | [도시별 현재 기온](day2/ex07/index.html) | [도시별 GET](day2/ex07/requests.http)에서 좌표를 비교하고 응답에서 기온과 단위 읽기 |
| [web-week12 통합 예제](day2/web-week12/README.md) | 완성 사이트 | [홈의 현재 기온](day2/web-week12/index.html) | 홈의 날씨 GET과 브라우저 방명록 저장 |

ex01~ex01d는 브라우저 타이머만 사용한다. ex02~ex07은 각 폴더의 `requests.http`에서 **Send Request**를 눌러 서버 응답도 확인할 수 있다. 공개 API의 기본 주소는 요청 파일에 적혀 있다. 별도 헤더나 키 입력 없이 실행한다. [실습지](../lab.md) · [따라하기](../walkthrough.md)

통합 예제의 [weather.http](day2/web-week12/weather.http)는 키 없이 실행되는 날씨 GET이다. [requests.http](day2/web-week12/requests.http)는 강의자가 제공하는 방명록 API의 접속 확인·도움말·목록 GET을 알아보는 선택 실습에 사용한다.
