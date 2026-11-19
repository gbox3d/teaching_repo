---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 13주차"
footer: "REST API · POST"
---

# REST API로 방명록 저장하기

12주 GET → 13주 POST → GET 재조회

- 7주 폼과 12주 목록 함수를 이어 쓴다.
- 서버가 만든 id와 201 응답을 확인한다.
- 매 차시 강의·시연 60분 + 학생 실습 30분.
- 파일·저장소는 사전 준비, 업로드는 수업 뒤 정리.

---

## 1일차 · 0–5분 · 준비와 요청 흐름

- 정적 서버·API·제공 폴더를 확인한다.
- GET은 서버 목록을 읽고 POST는 새 글을 만든다.
- 같은 주소도 method에 따라 요청하는 일이 다르다.

API 설정 패널은 제공 코드다. 새로고침하면 로컬 기본값으로 돌아간다.
공용 값은 실행 중 다시 입력한다.

---

## 1일차 · 5–20분 · POST와 JSON

[ex01 시연](examples/day1/ex01/README.md) · [ex02 비교본](examples/day1/ex02/README.md)

```js
const item = {
  book_id: BOOK_ID, name: 'student01', message: '안녕하세요'
};
const body = JSON.stringify(item);
```

객체를 JSON 문자열로 바꿔 보낸다.
id와 created_at은 서버가 만든다. ex01은 변환만 하며 저장하지 않는다.

---

## 1일차 · 20–35분 · headers와 body

[POST 코드](examples/day1/ex02/app.js) · [REST Client](examples/day1/ex02/requests.http)

```js
const response = await fetch(url, {
  method: 'POST',
  headers: {
    apikey: API_PUBLIC_KEY,
    'Content-Type': 'application/json',
    Prefer: 'return=representation'
  },
  body: JSON.stringify(item)
});
```

apikey는 공개 호출용 키다. Prefer는 저장된 행을 응답으로 요청한다.

---

## 1일차 · 35–45분 · 201과 서버 id

- Payload: 보낸 book_id·name·message.
- Response: 서버가 추가한 id·created_at.
- 201: 새 글 생성 성공. 이어지는 GET 200에서 같은 id를 찾는다.

REST Client는 `.env.example`을 `.env`로 복사해 설정한다.
about → help → POST → GET의 **Send Request**를 차례로 누른다.
브라우저 설정과 `.env`는 별개다. 실제 키를 추적 파일에 적지 않는다.

---

## 1일차 · 45–55분 · 서버 입력 거절

[ex03 시연](examples/day1/ex03/README.md) · [요청](examples/day1/ex03/requests.http)

- 빈 메시지를 보내면 400, 정상 문장이면 201이다.
- response.ok·status와 Response를 함께 읽는다.
- 화면 검사와 별개로 서버도 입력을 검사한다.

ex03은 빈값을 보내려고 화면 검사를 생략한 비교 예제다.
POST는 글을 실제로 추가하므로 한 번 전송한 뒤 결과를 확인한다.

---

## 1일차 · 55–60분 · 30분 실습 안내

1. `.http`의 message 변경·POST: 10분.
2. 응답 id 확인·GET: 10분.
3. 빈값 거절과 정상 응답 비교: 10분.

강의·시연: 5 + 15 + 15 + 10 + 10 + 5 = 60분.
학생 실습: 10 + 10 + 10 = 30분.

[실습지](lab.md#1일차-실습) · [따라하기](walkthrough.md)

---

## 2일차 · 0–5분 · 폼과 서버 준비

- 12주 GET 목록과 API 설정을 확인한다.
- 이름은 별칭, 메시지는 500자 이내로 입력한다.
- 이메일은 POST 본문에 넣지 않는다.

설정 패널·요청 번호 검사·버튼 잠금·실패 처리는 제공 코드다.
학생은 폼 값·JSON 본문·재조회 호출 세 구역만 수정한다.

---

## 2일차 · 5–15분 · submit 복습

[ex04 시연](examples/day2/ex04/README.md)

```js
form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  // 검사 후 POST 요청
});
```

7주의 submit → preventDefault → value.trim을 이어 쓴다.
공백만 입력하면 요청을 보내지 않는다.

---

## 2일차 · 15–30분 · POST 연결

[완성본 POST 구역](examples/day2/web-week13/guestbook.js)

```js
method: 'POST',
headers: {
  apikey: API_PUBLIC_KEY,
  'Content-Type': 'application/json',
  Prefer: 'return=representation'
},
body: JSON.stringify({ book_id: BOOK_ID, name: name, message: message })
```

폼 값과 Network의 Payload를 비교한다.
학생 수정 1은 폼 값, 수정 2는 JSON 본문이다.

---

## 2일차 · 30–45분 · 대기와 실패

[ex05 시연](examples/day2/ex05/README.md)

- 요청 중: 중복 submit 차단, 저장 버튼 비활성화.
- 성공 확인: 저장 안내. 실패: 입력 보존.
- finally: 저장 버튼 재활성화.
- 응답 불명확: 다시 POST하기 전에 GET으로 확인.

Slow 3G·Offline을 비교하고 No throttling으로 복구한다.
설정이 바뀌면 이전 POST 결과가 새 안내나 폼을 바꾸지 않는다.

---

## 2일차 · 45–55분 · 저장 후 GET

[ex06 시연](examples/day2/ex06/README.md)

```js
notice.textContent = `저장 완료 · 글 번호 ${saved[0].id}`;
await loadMessages(); // 학생 수정 3
```

POST 성공 안내와 GET 실패 안내는 별개다. GET 실패 때 조회만 재시도한다.
두 브라우저에 같은 API·방명록 번호를 적용해 같은 글을 확인한다.
같은 PC의 로컬 확인과 공용 HTTPS API·다른 기기 확인을 구분한다.

---

## 2일차 · 55–60분 · 30분 실습 안내

1. 폼 값·JSON·loadMessages 세 구역: 15분.
2. 중복 클릭·실패 입력 보존: 7분.
3. 다른 브라우저·POST 201 → GET 200 캡처: 8분.

강의·시연: 5 + 10 + 15 + 15 + 10 + 5 = 60분.
학생 실습: 15 + 7 + 8 = 30분.

[실습지](lab.md#2일차-실습) · [따라하기](walkthrough.md)

---

# 만들기 파일과 14주 인계

[방명록](examples/day2/web-week13/guestbook.html) · [GET·POST 통합 JS](examples/day2/web-week13/guestbook.js)
[제공 설정](examples/day2/web-week13/api-settings.js) · [REST Client](examples/day2/web-week13/requests.http)
[홈](examples/day2/web-week13/index.html) · [내 정보](examples/day2/web-week13/about.html)

HTML: api-settings.js → guestbook.js, 모두 defer.
이벤트·설정을 초기화한 뒤 파일 맨 끝에서 최초 GET을 실행한다.
submit.js는 연결하지 않는다. 14주 PATCH·DELETE도 같은 파일에 이어 쓴다.

[예제 안내](examples/README.md) · [실습](lab.md) · [따라하기](walkthrough.md)
