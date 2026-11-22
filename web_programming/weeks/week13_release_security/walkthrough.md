# 13주차 따라하기 · 기존 GET에 POST 연결

## 1. 사전 준비

1차시는 [ex02의 requests.http](examples/day1/ex02/requests.http)를 VS Code에서 연다. 수업 API 주소는 `https://esoqbcwgzjtwcqszwvin.supabase.co`다. 강의자가 배부한 공개 키와 내 방명록 번호를 준비한다.

2차시는 [완성 폴더](examples/day2/web-week13/)를 `web-week13`으로 복사한다. 글을 불러오는 함수와 목록 화면은 이 폴더에 들어 있다. 브라우저에서 배부받은 페이지를 연다. 내 PC에서 고친 HTML을 볼 때는 작업 폴더에 [정적 서버](../../tools/static-server/server.mjs)를 두고 다음 명령을 실행한다.

```powershell
node server.mjs
```

이때 화면 주소는 `http://localhost:8000/guestbook.html`이고, 글은 수업 API에 저장된다.

## 2. REST Client와 브라우저에 설정 적용

VS Code에서는 REST Client(`humao.rest-client`)를 사용한다. `.env.example`을 같은 폴더의 `.env`로 복사한 뒤 `API_PUBLIC_KEY`에 배부받은 공개 키, `BOOK_ID`에 내 방명록 번호를 적는다. `API_BASE_URL`에는 수업 주소가 들어 있다. 12주 선택 방명록 예제를 해 봤다면 그때 사용한 `.env`를 복사해도 된다.

브라우저에서는 **API 설정**에 공개 키와 방명록 번호를 입력하고 **설정 적용**을 누른다. ex02~ex05는 글을 보낼 준비가 되고, ex06과 완성 방명록은 기존 목록을 먼저 불러온다. 새로고침하면 브라우저 설정을 다시 입력한다. `.env`는 REST Client가 읽는다.

## 3. 1차시 30분 실습

1. [ex02의 첫 POST](examples/day1/ex02/requests.http)에서 `message`를 내 문장으로 바꾸고 **Send Request**를 한 번 누른다(10분). `Content-Type`은 JSON 본문을 알리고 `Prefer: return=representation`은 저장한 행을 응답으로 요청한다.
2. `201 Created` 응답 배열에서 `id`를 읽는다. 같은 파일의 GET 위에서 **Send Request**를 누른 뒤 `200 OK` 목록에서 같은 `id`와 문장을 찾는다(10분).
3. [ex03의 requests.http](examples/day1/ex03/requests.http)에서 빈 메시지와 정상 문장을 각각 보내고 `400`과 `201` 응답을 비교한다(10분).

객체를 JSON 문자열로 바꾸는 과정은 [ex01](examples/day1/ex01/README.md)에서 다시 볼 수 있다. 수업 API에 연결되지 않을 때는 선택 방명록 예제의 [접속 확인·도움말 요청](../week12_fetch_json/examples/day2/web-week12/requests.http)으로 점검한다.

## 4. 2차시 30분 실습

제공 [guestbook.js](examples/day2/web-week13/guestbook.js)의 다음 세 구역만 수정한다(15분). 설정과 방어 코드는 다시 구현하지 않는다.

### 1. 폼 값 읽기

```js
const name = nameInput.value.trim();
const message = messageInput.value.trim();
```

### 2. JSON 본문 만들기

`method: 'POST'`와 `apikey`·`Content-Type`·`Prefer`를 확인한 뒤 본문을 연결한다.

```js
body: JSON.stringify({ book_id: BOOK_ID, name: name, message: message })
```

### 3. 저장 후 조회

성공을 확인한 다음 GET으로 서버 목록을 읽는다. GET 함수는 실패해도 저장 성공 안내를 바꾸지 않는다.

```js
await loadMessages();
```

느린 연결에서 저장 버튼을 연달아 눌러 POST 한 건만 전송됐는지 확인한다. Offline에서 전송했을 때는 입력이 남는지 확인한다(7분). 연결을 복구한 뒤 두 번째 브라우저에 같은 설정을 적용하고 저장한 글을 캡처한다(8분). POST 응답을 받지 못했다면 GET으로 저장 여부부터 확인한다.

## 5. 파일 조립과 제공 코드

HTML은 다음 순서로 두 파일만 읽는다. `submit.js`는 이동 안내이므로 연결하지 않는다.

```html
<script src="api-settings.js" defer></script>
<script src="guestbook.js" defer></script>
```

`guestbook.js`에 들어 있는 `loadMessages()`와 `showList(items)`는 목록을 불러와 화면에 표시한다. **설정 적용**을 누르면 첫 목록을 불러온다. 이후 폼의 `submit`에서 POST 응답을 확인하고 `loadMessages()`를 한 번 호출한다. 조회가 실패해도 화면에 저장 성공 안내가 남는다.

화면은 [W3.CSS 4.1.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용한다. HTML의 폼 ID는 7주와 같고 목록 ID는 12주와 같다.

## 6. 수업 뒤 업로드

동작을 캡처하고 `.env`가 Git에 포함되지 않았는지 확인한 뒤 준비한 저장소에 commit·push한다. Pages에서도 같은 공개 키·방명록 번호로 저장한 글을 조회한다. 공용 PC에서는 수업 종료 후 계정 로그인을 정리한다.
