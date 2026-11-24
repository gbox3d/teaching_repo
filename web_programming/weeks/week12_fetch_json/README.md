[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_fetch_json)

# 12주차 · Promise와 async/await로 배우는 fetch

첫날에는 타이머의 출력 순서를 예측하고, 1초 타이머를 `.then()`과 `await`로 기다린 뒤 `async` 함수가 돌려주는 값을 확인한다. 이어서 JSONPlaceholder의 같은 응답을 `.then()`과 `async/await` 두 방식으로 읽는다. 둘째 날에는 환율 응답에서 필요한 값을 읽고, 타로 카드 조회로 `200`과 `404`를 비교한 뒤, 공휴일 배열을 목록으로 표시한다.

## 학습 목표

- 대기 중인 Promise와 결과가 나온 Promise를 구분하고, 동기 코드와 `.then()` 콜백의 실행 순서를 설명한다.
- `async` 함수를 호출하면 함수가 끝나기 전에 Promise를 받고, 함수 안의 `return` 값은 그 Promise의 성공 값, `throw`는 실패 이유가 된다는 것을 타이머 예제로 확인한다.
- `fetch()`가 반환한 Promise는 HTTP 응답을 받으면 Response로 이행한다. `response.json()`도 Promise를 반환한다. 두 결과를 기다리는 코드를 `.then()`과 `async/await`로 작성한다.
- HTTP 오류 응답과 응답을 받기 전의 통신 실패를 구분하고, 조회가 끝나면 버튼을 다시 활성화한다.

## 수업 구성

| 차시 | 강의·시연 60분 | 학생 실습 30분 |
|---|---|---|
| 1차시 | 타이머 준비 5, 타이머를 기다리는 동안 7, Promise를 돌려주는 wait 함수 8, async 함수와 await 10, async 함수가 돌려주는 값 8, 응답에서 할 일 제목까지 10, 같은 요청에 await 쓰기 7, 실습 안내 5 | ex01c 사본에 3초 줄 더하기·클릭 확인 8, REST Client와 then으로 응답 읽기 10, 두 await와 try/catch 직접 작성·실행 12 |
| 2차시 | 환율 요청 준비 5, 응답 필드 읽기 15, HTTP 오류 15, 통신 실패 10, 공휴일 목록·재시도 10, 안내 5 | 환율 응답 대조 8, 200·404 비교 8, 공휴일 목록 조회·Offline 복구 14 |

## 예제 순서

| 예제 | 학생이 확인할 내용 |
|---|---|
| [ex01 타이머](examples/day1/ex01/README.md) | 타이머를 기다리는 동안 먼저 실행되는 코드 |
| [ex01b wait 함수](examples/day1/ex01b_wait/README.md) | `wait(1000)`이 돌려준 Promise와 `return wait(1000)` 뒤 두 번째 `.then()`이 실행되는 때 |
| [ex01c async 함수와 await](examples/day1/ex01c_async_await/README.md) | `await wait(1000)`을 기다리는 동안에도 올라가는 클릭 수 |
| [ex01d async 함수가 돌려주는 값](examples/day1/ex01d_async_return/README.md) | 호출하자마자 받은 Promise, `return` 값과 `throw`의 실패 이유를 받는 자리 |
| [ex02 할 일 한 건](examples/day1/ex02/README.md) | `return response.json()` 뒤 다음 `.then()`이 받는 값 |
| [ex03 같은 요청을 await로](examples/day1/ex03/README.md) | 직접 고친 ex02의 `await` 코드와 결과를 대조하는 완성본 |
| [ex04 기준 환율](examples/day2/ex04/README.md) | Frankfurter 응답의 `date`와 `rates.KRW` |
| [ex05 타로 카드 조회](examples/day2/ex05/README.md) | Tarot API의 `200`과 `404`, `response.ok` 분기 |
| [ex06 나라별 공휴일](examples/day2/ex06/README.md) | Nager.Date 배열을 목록으로 바꾸고 통신 실패 뒤 재시도 |
| [ex07 도시별 현재 기온](examples/day2/ex07/README.md) (선택) | 서울·전주·익산의 좌표로 Open-Meteo에 요청하고 기온과 단위 읽기 |

VS Code REST Client(`humao.rest-client`)에서는 ex02~ex07의 `requests.http`에 있는 **Send Request**를 누른다. 공개 API에 키나 별도 인증 헤더 없이 GET을 보낸다. [따라하기](walkthrough.md) · [실습지](lab.md)

## 결과물과 다음 수업

1차시는 ex01c 사본에 ‘4. 3초 지남’을 더하고, 직접 `async/await`로 고친 할 일 조회 코드로 제목을 표시한다. 주차 결과물은 ex06의 나라별 공휴일 화면이다. 날짜와 공휴일 이름을 목록에 표시하고, 연결을 복구한 뒤 같은 나라로 다시 요청한다.

[통합 예제 홈](examples/day2/web-week12/index.html)에서는 서울·전주·익산의 기온을 조회한다. **방명록** 메뉴를 열고 글을 남기면 11주에 배운 `localStorage`에 저장된다. Supabase에 있는 글 목록은 [선택 실습](examples/day2/web-week12/README.md#선택-실습-서버-글-조회)에서 읽는다. 서버에 글을 쓰는 POST는 13주에 실습한다. [13주 수업](../week13_guestbook_crud/README.md)

[한국어 슬라이드](slides.md) · [영문 슬라이드](slides_en.md) · [예제 설명](examples/README.md)
