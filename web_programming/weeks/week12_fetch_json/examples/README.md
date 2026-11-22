# 12주차 예제 · Promise에서 도시별 날씨까지

1차시는 할 일을 읽는 ex02 사본을 `async/await`로 직접 고쳐 실행한 뒤 ex03과 대조한다. 2차시는 선택한 도시의 기온을 표시한다. 각 차시는 강의·시연 60분, 학생 실습 30분이다.

| 예제 | 화면 | 코드에서 볼 곳 |
|---|---|---|
| [ex01 타이머](day1/ex01/README.md) | [실행 순서](day1/ex01/index.html) | 타이머·`resolve`·`.then()` |
| [ex02 JSONPlaceholder](day1/ex02/README.md) | [할 일 한 건](day1/ex02/index.html) | `fetch` → `return response.json()` → 제목 |
| [ex03 async/await](day1/ex03/README.md) | [같은 할 일](day1/ex03/index.html) | 같은 요청을 두 번의 `await`로 읽기 |
| [ex04 Open-Meteo](day2/ex04/README.md) | [서울 기온](day2/ex04/index.html) | URL 좌표와 응답의 기온·단위 |
| [ex05 HTTP 오류](day2/ex05/README.md) | [위도 비교](day2/ex05/index.html) | 잘못된 위도 `999`, 400 응답 |
| [ex06 필수 결과물](day2/ex06/README.md) | [도시별 날씨](day2/ex06/index.html) | 도시 선택·요청 대기·오류 처리·재시도 |

ex01은 브라우저 타이머만 사용한다. ex02~ex06은 각 폴더의 `requests.http`에서 **Send Request**를 눌러 서버 응답도 확인할 수 있다. 두 공개 API의 기본 주소는 요청 파일에 있고 별도 헤더나 키 입력은 없다. [실습지](../lab.md) · [따라하기](../walkthrough.md)

[선택 방명록](day2/web-week12/README.md)에는 13주에 사용할 강의자 제공 API의 접속 확인·도움말·목록 GET이 있다. 방명록 설정과 `.env`는 이 폴더에서만 사용한다.
