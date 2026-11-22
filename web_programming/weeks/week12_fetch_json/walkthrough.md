# 12주차 따라하기 · Promise와 async/await로 배우는 fetch

## 1. 브라우저와 VS Code REST Client 준비

예제 화면 링크를 열거나 교재 저장소 최상위에서 다음 명령으로 HTML 파일을 연다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week12_fetch_json/examples 8000
```

첫 예제는 `http://localhost:8000/day1/ex01/`, 도시별 날씨는 `http://localhost:8000/day2/ex06/`다. 타이머는 브라우저에서 실행하고 데이터는 두 공개 API에서 읽는다.

VS Code에서는 REST Client(`humao.rest-client`)를 설치한다. ex02~ex06의 `requests.http`를 열고 요청 줄 위의 **Send Request**를 누른다. 요청 파일의 기본 주소는 JSONPlaceholder(`https://jsonplaceholder.typicode.com`) 또는 Open-Meteo(`https://api.open-meteo.com`)다. 필수 예제는 추가 헤더나 `.env` 설정 없이 실행한다.

## 2. 타이머와 Promise의 실행 순서

[ex01](examples/day1/ex01/index.html)을 열고 ‘타이머 시작’, ‘다음 줄 실행’, ‘타이머 완료’ 세 문장이 어떤 순서로 보일지 먼저 적는다. **타이머 시작**을 누르면 두 줄이 먼저 나오고 약 1초 뒤에 완료 문장이 붙는다.

타이머 콜백을 예약한 순간 `timer`는 대기 중(pending)이다. 타이머의 `resolve('3. 타이머 완료')`가 Promise를 성공(fulfilled) 상태로 바꾸면 `timer.then(...)`에 등록한 함수가 그 문장을 받는다. 실패(rejected)한 Promise의 이유는 `.catch()`에서 받는다.

## 3. 같은 GET을 두 방식으로 읽기

[ex02 요청](examples/day1/ex02/requests.http)에서 **Send Request**를 누른다. 응답은 `200 OK`이고 본문은 할 일 한 건을 나타내는 JSON 객체다. [ex02 화면](examples/day1/ex02/index.html)에서 **할 일 불러오기**를 누른 뒤 `title`이 같은지 확인한다.

ex02 폴더를 복사한다. 사본의 클릭 콜백을 `async function`으로 바꾸고 `.then()` 체인을 지운다. `try`에서 HTTP 응답과 JSON 본문을 순서대로 `await`하고 `todo.title`을 출력한다. `catch`에 실패 안내를, `finally`에 버튼 복구를 옮긴다. 사본을 실행해 제목을 확인한 뒤 [ex03 완성본](examples/day1/ex03/app.js)과 대조한다.

| 기다리는 값 | ex02의 then | ex03의 await |
|---|---|---|
| HTTP 응답 | `fetch(url).then(function (response) { … })` | `const response = await fetch(url);` |
| 본문에서 읽은 객체 | 첫 콜백에서 `return response.json()` 후 다음 콜백이 `todo`를 받음 | `const todo = await response.json();` |

`.then()` 콜백이 `response.json()`을 반환하면 다음 콜백은 본문을 읽을 때까지 기다린다. `return`을 빼면 콜백의 반환값은 `undefined`다. `await`를 쓸 때는 현재 `async` 함수의 다음 줄에서 기다린 값을 사용할 수 있다. 브라우저는 기다리는 동안에도 다른 입력을 처리한다. `async` 함수의 반환값은 항상 Promise다.

## 4. 서울 기온과 오류 응답

[ex04 요청](examples/day2/ex04/requests.http)의 좌표는 서울의 위도 37.5665와 경도 126.9780이다. **Send Request**를 눌러 `current.temperature_2m`과 `current_units.temperature_2m`을 확인하고 [기온 화면](examples/day2/ex04/index.html)과 비교한다.

[ex05](examples/day2/ex05/index.html)에서 정상 위도와 잘못된 위도 `999`를 각각 조회한다. 정상 응답의 `response.ok`는 true다. 잘못된 위도에는 응답 상태 400과 오류 이유가 온다. 이때도 서버가 응답했으므로 `await fetch(url)`은 Response를 돌려준다. 개발자 도구 Network를 **Offline**으로 바꾸고 다시 요청하면 응답 자체를 받지 못해 `catch`가 실행된다. 확인 후 **No throttling**으로 되돌린다.

## 5. 도시별 날씨 완성본

[ex06](examples/day2/ex06/index.html)에서 서울 또는 부산을 고르고 **기온 조회**를 누른다. `#city`의 값으로 좌표를 고르고, 요청이 끝날 때까지 도시 선택과 조회 버튼을 잠근다. `finally`에서 두 요소를 다시 활성화하므로 조회에 실패해도 같은 도시로 다시 시도할 수 있다.

### index.html

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ex06 · 도시별 현재 기온</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
  <script src="app.js" defer></script>
</head>
<body class="w3-light-grey">
  <main class="w3-content w3-padding">
    <h1>도시별 현재 기온</h1>
    <p><label for="city">도시</label>
      <select class="w3-select w3-border" id="city">
        <option value="seoul">서울</option>
        <option value="busan">부산</option>
      </select></p>
    <button class="w3-button w3-teal" id="run-button" type="button">기온 조회</button>
    <p id="output" role="status">대기 중</p>
    <p><small><a href="https://open-meteo.com/">Weather data by Open-Meteo</a></small></p>
  </main>
</body>
</html>
```

### app.js

```js
const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const citySelect = document.querySelector('#city');
const cities = {
  seoul: { name: '서울', latitude: 37.5665, longitude: 126.9780 },
  busan: { name: '부산', latitude: 35.1796, longitude: 129.0756 }
};

async function readWeather() {
  const city = cities[citySelect.value];
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${city.latitude}&longitude=${city.longitude}&current=temperature_2m`;
  button.disabled = true;
  citySelect.disabled = true;
  output.textContent = '조회 중';
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const weather = await response.json();
    output.textContent = `${city.name} ${weather.current.temperature_2m}${weather.current_units.temperature_2m}`;
  } catch (error) {
    output.textContent = `조회 실패 · ${error.message}. 연결을 확인하고 다시 조회하세요.`;
  } finally {
    button.disabled = false;
    citySelect.disabled = false;
  }
}

button.addEventListener('click', readWeather);
```

## 6. 확인과 제출

1차시 실습은 타이머 출력 예측 8분, REST Client와 `.then()`으로 제목 읽기 10분, `async/await`로 직접 고쳐 실행하기 12분이다. 2차시 실습은 서울 기온 대조 8분, 위도 오류 비교 8분, 도시별 조회와 통신 복구 14분이다.

선택한 도시·기온·단위와 Network의 GET 200을 캡처한다. 서울과 부산의 기온이 같아도 요청 URL의 좌표로 도시를 구분할 수 있다. 접속을 복구한 뒤 버튼을 눌러 새 응답을 받는다. [실습지](lab.md)

13주에는 강의자가 운영하는 방명록 API에 글을 쓴다. 미리 방명록 목록을 읽어 보려면 [선택 방명록](examples/day2/web-week12/README.md)에서 Supabase 공개 키와 방명록 번호를 설정한다.
