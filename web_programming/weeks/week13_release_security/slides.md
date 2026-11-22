---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 13주차"
footer: "REST API · POST"
---

# REST API로 방명록 저장하기

공개 API에서 익힌 `fetch` → 수업 방명록에 POST → 저장한 글 확인

- 7주 폼에 글쓰기 요청을 연결한다. 목록 함수는 제공한다.
- 서버가 만든 id와 201 응답을 확인한다.
- 매 차시 강의·시연 60분 + 학생 실습 30분.
- 파일·저장소는 사전 준비, 업로드는 수업 뒤 정리.

---

## 1일차 · 0–5분 · 준비와 요청 흐름

- ex02의 `.env.example`을 `.env`로 복사해 `API_PUBLIC_KEY`·`BOOK_ID`를 채운다.
- `POST /rest/v1/guestbook`의 본문에서 내 방명록 번호와 메시지를 찾는다.
- **Send Request**를 한 번 누르면 수업 방명록에 글 한 건이 생긴다.

---

## 1일차 · 5–20분 · POST와 JSON

[ex02 첫 POST](examples/day1/ex02/README.md) · [ex01 JSON 선택 복습](examples/day1/ex01/README.md)

```js
const item = {
  book_id: BOOK_ID, name: 'student01', message: '안녕하세요'
};
const body = JSON.stringify(item);
```

`body`에 담는 값은 방명록 번호·별칭·메시지다.
글 번호(`id`)와 작성 시각(`created_at`)은 서버가 채운다.

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

- 요청 본문에는 `book_id`, `name`, `message`가 들어 있다.
- `201 Created` 응답 배열에서 서버가 추가한 `id`를 찾는다.
- 같은 파일에서 GET의 **Send Request**를 누른다. `200 OK` 목록에서 방금 받은 `id`와 메시지를 확인한다.

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

## 2일차 · 0–5분 · 글쓰기 폼 준비

- 완성 방명록 `config.example.js`의 `BOOK_ID`를 내 방명록 번호로 바꾼다.
- 처음 열 때 묻는 창에 배부받은 공개 키를 넣는다(11주 localStorage에 저장). 틀리면 **공개 키 지우기**를 누르고 다시 넣는다.
- 이름은 별칭, 메시지는 500자 이내로 입력한다.
- 이메일은 POST 본문에 넣지 않는다.

설정 파일·요청 번호 검사·버튼 잠금·실패 처리는 제공 코드다.
학생은 폼 값·JSON 본문·재조회 호출 세 구역만 수정한다.

---

## 2일차 · 5–15분 · 폼에서 요청 본문 만들기

[ex04 시연](examples/day2/ex04/README.md)

```js
form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const message = messageInput.value.trim();
  // 검사 후 POST 요청
});
```

ex02에서는 정해진 문장을 보냈다. ex04에서는 폼에 입력한 메시지를 본문에 넣는다.
공백만 입력하면 제출을 멈춘다.

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

- 느린 연결에서 저장 버튼을 연달아 누른다. Network에 POST 한 건이 보여야 한다.
- Offline에서 보내면 입력이 남는다. `finally`에서 저장 버튼을 다시 활성화한다.
- 연결을 복구한다. 저장 응답을 못 받았으면 GET으로 먼저 확인한다.

---

## 2일차 · 45–55분 · 저장 후 GET

[ex06 시연](examples/day2/ex06/README.md)

```js
notice.textContent = `저장 완료 · 글 번호 ${saved[0].id}`;
await loadMessages(); // 학생 수정 3
```

제공된 `loadMessages()`로 방금 쓴 글을 확인한다.
POST 201 뒤 조회가 실패하면 **새로 불러오기**로 GET만 다시 보낸다.
두 번째 브라우저에서는 묻는 창에 공개 키를 넣은 뒤 저장한 문장을 찾는다.

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
[설정 파일](examples/day2/web-week13/config.example.js) · [REST Client](examples/day2/web-week13/requests.http)
[홈](examples/day2/web-week13/index.html) · [내 정보](examples/day2/web-week13/about.html)

HTML은 `config.example.js`, `guestbook.js` 순서로 읽는다. 두 파일 모두 `defer`를 쓴다.
완성 방명록은 페이지를 열 때 첫 GET을, **남기기**를 누르면 POST와 GET을 보낸다.
14주에는 저장한 글의 `id`로 수정과 삭제를 요청한다.

[예제 안내](examples/README.md) · [실습](lab.md) · [따라하기](walkthrough.md)
