# 지역별 현재 기온

[실습 화면](index.html)을 열면 서울의 현재 기온이 표시된다. 전주 또는 익산을 선택하고 **기온 조회**를 누른다. [app.js](app.js)에서 선택한 도시의 위도와 경도가 GET 요청 주소에 들어가는 부분을 찾는다.

## VS Code에서 같은 요청 보내기

1. VS Code에 REST Client 확장(`humao.rest-client`)을 설치하고 [requests.http](requests.http)를 연다.
2. `@baseUrl`은 `https://api.open-meteo.com`이다. 수업용 요청은 API 키와 별도 헤더 없이 보낸다.
3. 도시 이름 아래의 **Send Request**를 누른다. `200 OK` 응답에서 `current.temperature_2m`은 기온, `current_units.temperature_2m`은 단위다. 두 값을 화면에 표시된 값과 비교한다.

[Open-Meteo 날씨 API 문서](https://open-meteo.com/en/docs)
