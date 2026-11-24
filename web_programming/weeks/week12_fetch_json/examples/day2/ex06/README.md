# 나라별 공휴일

[실습 화면](index.html)에서 한국·일본·미국을 선택하고 **공휴일 조회**를 누른다. [app.js](app.js)는 나라 코드와 현재 연도를 URL에 넣고 GET 요청을 보낸다. 응답을 `for`로 순회한다. `nationalHoliday`가 true이고 `holidayTypes`에 `Public`이 있는 항목의 날짜(`date`)와 영문 이름(`name`)을 목록에 표시한다.

개발자 도구의 Network에서 **Disable cache**를 켜고 Offline으로 바꿔 조회하면 실패 안내가 나온다. `finally`에서 나라 선택과 조회 버튼이 다시 활성화된다. 연결을 복구하고 같은 나라를 다시 조회한다.

VS Code REST Client(`humao.rest-client`)에서 [requests.http](requests.http)를 연다. `@baseUrl`은 `https://nagerholidays.com`이다. 브라우저와 같은 연도를 조회하려면 `@year`를 올해로 바꾼다. 요청 위 **Send Request**를 누르면 `200 OK`와 공휴일 배열이 온다. 공개 키나 별도 헤더 없이 실행한다.

[Nager.Date API 문서](https://nagerholidays.com/api)
