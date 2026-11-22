[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_fetch_json)

# 12주차 · Promise와 async/await로 배우는 fetch

서울과 부산의 현재 기온을 조회하는 페이지를 만든다. 첫날에는 타이머의 출력 순서를 예측하고, 1초 타이머를 `.then()`과 `await`로 기다린 뒤 `async` 함수가 돌려주는 값을 확인한다. 이어서 JSONPlaceholder의 같은 응답을 `.then()`과 `async/await` 두 방식으로 읽는다. 둘째 날에는 Open-Meteo의 날씨 데이터를 화면에 표시하고 요청이 실패하면 다시 조회한다.

## 학습 목표

- 대기 중인 Promise와 결과가 나온 Promise를 구분하고, 동기 코드와 `.then()` 콜백의 실행 순서를 설명한다.
- `async` 함수를 호출하면 함수가 끝나기 전에 Promise를 받고, 함수 안의 `return` 값은 그 Promise의 성공 값, `throw`는 실패 이유가 된다는 것을 타이머 예제로 확인한다.
- `fetch()`가 반환한 Promise는 HTTP 응답을 받으면 Response로 이행한다. `response.json()`도 Promise를 반환한다. 두 결과를 기다리는 코드를 `.then()`과 `async/await`로 작성한다.
- HTTP 오류 응답과 응답을 받기 전의 통신 실패를 구분하고, 조회가 끝나면 버튼을 다시 활성화한다.

## 수업 구성

| 차시 | 강의·시연 60분 | 학생 실습 30분 |
|---|---|---|
| 1차시 | 타이머 준비 5, 타이머를 기다리는 동안 7, Promise를 돌려주는 wait 함수 8, async 함수와 await 10, async 함수가 돌려주는 값 8, 응답에서 할 일 제목까지 10, 같은 요청에 await 쓰기 7, 실습 안내 5 | ex01c 사본에 3초 줄 더하기·클릭 확인 8, REST Client와 then으로 응답 읽기 10, 두 await와 try/catch 직접 작성·실행 12 |
| 2차시 | 준비 5, 날씨 요청과 응답 15, HTTP 오류 15, 통신 실패 10, 도시 선택·재시도 10, 안내 5 | 서울 기온 읽기 8, 위도 오류와 정상 응답 비교 8, 두 도시 조회·Offline 복구 14 |

## 예제 순서

| 예제 | 학생이 확인할 내용 |
|---|---|
| [ex01 타이머](examples/day1/ex01/README.md) | 타이머를 기다리는 동안 먼저 실행되는 코드 |
| [ex01b wait 함수](examples/day1/ex01b_wait/README.md) | `wait(1000)`이 돌려준 Promise와 `return wait(1000)` 뒤 두 번째 `.then()`이 실행되는 때 |
| [ex01c async 함수와 await](examples/day1/ex01c_async_await/README.md) | `await wait(1000)`을 기다리는 동안에도 올라가는 클릭 수 |
| [ex01d async 함수가 돌려주는 값](examples/day1/ex01d_async_return/README.md) | 호출하자마자 받은 Promise, `return` 값과 `throw`의 실패 이유를 받는 자리 |
| [ex02 할 일 한 건](examples/day1/ex02/README.md) | `return response.json()` 뒤 다음 `.then()`이 받는 값 |
| [ex03 같은 요청을 await로](examples/day1/ex03/README.md) | 직접 고친 ex02의 `await` 코드와 결과를 대조하는 완성본 |
| [ex04 서울 현재 기온](examples/day2/ex04/README.md) | 요청한 좌표와 응답의 기온·단위 |
| [ex05 위도 오류](examples/day2/ex05/README.md) | 유효한 위도에서 받은 200과 `999`에서 받은 400 비교 |
| [ex06 도시별 날씨](examples/day2/ex06/README.md) | 서울·부산 선택, 대기 중 버튼 잠금, 실패 뒤 재조회 |

VS Code REST Client(`humao.rest-client`)에서는 ex02~ex06의 `requests.http`에 있는 **Send Request**를 누른다. 두 공개 API는 키나 별도 인증 헤더 없이 GET을 받는다. [따라하기](walkthrough.md) · [실습지](lab.md)

## 결과물과 다음 수업

1차시는 ex01c 사본에 ‘4. 3초 지남’을 더하고, 직접 `async/await`로 고친 할 일 조회 코드로 제목을 표시한다. 주차 결과물은 ex06의 도시별 날씨 화면이다. 선택한 도시의 기온과 단위를 표시하고, 연결을 복구한 뒤 같은 도시로 다시 요청한다.

[선택 방명록](examples/day2/web-week12/README.md)은 강의자가 준비한 Supabase API에서 글 목록을 읽는 예제다. 13주에는 조회 함수를 제공하고 글을 새로 쓰는 POST를 실습한다. [13주 수업](../week13_release_security/README.md)

[한국어 슬라이드](slides.md) · [영문 슬라이드](slides_en.md) · [예제 설명](examples/README.md) · [JSONPlaceholder](https://jsonplaceholder.typicode.com/guide/) · [Open-Meteo](https://open-meteo.com/en/docs)
