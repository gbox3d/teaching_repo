# 13주차 따라하기 · 기존 GET에 POST 연결

## 1. 사전 준비

[완성 폴더](examples/day2/web-week13/)를 작업 폴더 `web-week13`으로 복사한다. 홈·내 정보·이미지·CSS는 12주 자료와 이어진다. 정규 실습 중에는 Raw 파일 다운로드와 새 저장소 생성을 하지 않는다. 정적 서버 실행 파일은 수업 전에 준비한다.

로컬 API는 교재 저장소 최상위 터미널에서 실행한다.

```powershell
node web_programming/tools/guestbook-api/server.mjs
```

학생 폴더에는 [정적 서버](../../tools/static-server/server.mjs)를 두고 별도 터미널에서 실행한다.

```powershell
node server.mjs
```

학생 페이지는 `http://localhost:8000/guestbook.html`, API 기본값은 `http://127.0.0.1:8787`이다. `file://`로 열지 않는다.

## 2. 설정과 REST Client 확인

화면의 API 설정에 주소·공개 키·방명록 번호를 입력하고 설정 적용을 누른다. 제공 `api-settings.js`가 메모리의 세 변수를 바꾸고 GET을 호출한다. 새로고침 뒤에는 다시 입력한다. 공용 HTTPS 값과 실제 키를 `config.example.js`에 적지 않는다. 이 파일은 이동 안내만 남겼다.

VS Code REST Client(`humao.rest-client`)를 설치한다. 각 REST 폴더의 `.env.example`을 `.env`로 복사하고 로컬 또는 강의자 안내값으로 맞춘다. `.gitignore`도 복사한다. `.env`와 브라우저 설정은 자동 공유되지 않는다.

[requests.http](examples/day2/web-week13/requests.http)의 **Send Request**를 about → help → POST → GET 순서로 누른다. 처음 두 요청은 200과 정보 배열, POST는 201과 생성된 id, GET은 200과 글 목록을 반환한다. 마지막 빈 메시지 POST는 400을 비교하는 요청이다. 공개 키는 모든 요청의 `apikey`, JSON 본문과 응답 행 요청은 POST의 `Content-Type`·`Prefer` 헤더다.

## 3. 1차시 30분 실습

POST 요청의 message를 바꾸고 전송한다(10분). 201 응답의 서버 id를 GET에서 찾는다(10분). 빈 메시지를 보내 400과 정상 201을 비교한다(10분). ex01 JSON 변환과 ex02·ex03의 JS 구현은 시연 자료다.

## 4. 2차시 30분 실습

제공 [guestbook.js](examples/day2/web-week13/guestbook.js)의 다음 세 구역만 수정한다(15분). 설정과 방어 코드는 다시 구현하지 않는다.

### 학생 수정 1: 폼 값

```js
const name = nameInput.value.trim();
const message = messageInput.value.trim();
```

### 학생 수정 2: JSON 본문

`method: 'POST'`와 `apikey`·`Content-Type`·`Prefer`를 확인한 뒤 본문을 연결한다.

```js
body: JSON.stringify({ book_id: BOOK_ID, name: name, message: message })
```

### 학생 수정 3: 저장 후 조회

성공을 확인한 다음 GET으로 서버 목록을 읽는다. GET 함수는 실패해도 저장 성공 안내를 바꾸지 않는다.

```js
await loadMessages();
```

중복 클릭·실패 입력 보존을 확인한다(7분). 두 번째 브라우저에서 같은 설정을 적용하고 캡처한다(8분). POST 응답을 못 받았으면 다시 POST하기 전에 GET으로 확인한다. 로컬 API는 같은 PC의 두 브라우저에서 검증할 수 있고, 다른 기기에서는 공용 HTTPS API가 필요하다.

## 5. 파일 조립과 제공 코드

HTML은 다음 순서로 두 파일만 읽는다. `submit.js`는 이동 안내이므로 연결하지 않는다.

```html
<script src="api-settings.js" defer></script>
<script src="guestbook.js" defer></script>
```

`guestbook.js` 안에는 DOM 참조, GET 표시·요청, POST 폼 처리, 이벤트·설정 초기화가 차례로 있다. 맨 끝에서 최초 `loadMessages()`를 호출한다. 제공 요청 번호 검사는 느린 이전 GET이 새 목록을 덮지 않도록 한다. 설정을 바꾼 뒤 이전 POST가 끝나도 새 설정의 성공 안내나 입력 초기화로 처리하지 않는다.

W3.CSS CDN은 `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`, 추가 스타일은 폴더 안 `shared/examples.css`다. 화면에는 입력·버튼·결과·짧은 상태만 남긴다. HTML의 폼 ID는 7주와 같고 목록 ID는 12주와 같다.

## 6. 수업 뒤 업로드

동작 캡처를 먼저 마친 뒤 준비한 저장소에 commit·push한다. `.env`가 추적되지 않는지 확인한다. Pages에서 공용 API 설정을 입력하고 GET을 확인한다. 로컬 기본값을 공용 API 검증으로 표시하지 않는다. 공용 PC에서는 수업 종료 후 계정 로그인을 정리한다.
