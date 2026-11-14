---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 13주차"
footer: "REST API · POST"
---

# REST API로 방명록 저장하기

12주: GET → 13주: POST 후 GET으로 다시 읽기

- 7주 폼의 입력값을 JSON 본문으로 보낸다.
- 서버가 id와 저장 시간을 만든다.
- 다른 기기에서도 같은 글을 확인한다.
- 매 수업: 설명 30분 + 실습 60분.

---

## 1일차 · 0–4분 — GET과 POST

- GET: 서버에서 목록을 읽는다.
- POST: 서버에 새 글을 추가한다.
- 같은 주소도 메서드에 따라 하는 일이 다르다.

12주 목록 함수를 그대로 사용한다.
오늘은 서버 설정을 바꾸지 않고 요청 코드를 추가한다.

---

## 1일차 · 4–9분 — JSON 요청 본문

[ex01](examples/day1/ex01/index.html) · [코드](examples/day1/ex01/app.js)

```js
const item = {
  book_id: BOOK_ID, name: 'student01', message: '안녕하세요'
};
const body = JSON.stringify(item);
```

객체를 그대로 넣지 않고 JSON 글자로 바꾼다.
id와 created_at은 서버가 넣는다.

---

## 1일차 · 9–16분 — POST의 세 부분

[ex02](examples/day1/ex02/index.html) · [코드](examples/day1/ex02/app.js) · [설정](examples/day1/ex02/config.example.js)

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

---

## 1일차 · 16–22분 — Payload와 Response

- method는 동작, headers는 설명, body는 전송 데이터다.
- Payload에서 book_id·name·message를 확인한다.
- Response에는 서버 id·created_at이 추가된다.
- 성공 상태 201은 새 글이 만들어졌다는 뜻이다.

Prefer는 저장된 행을 응답으로 달라는 이 API의 요청이다.
공개 키는 사용자별 수정·삭제 권한을 주는 키가 아니다.

---

## 1일차 · 22–27분 — 서버 입력 검사

[ex03](examples/day1/ex03/index.html) · [코드](examples/day1/ex03/app.js) · [설정](examples/day1/ex03/config.example.js)

- 빈 메시지를 보내면 서버가 거절한다.
- 정상 문장으로 바꾸면 저장된다.
- response.ok·status·오류 본문을 함께 본다.
- 화면 검사와 별도로 서버도 입력을 검사한다.

POST 예제는 실제로 글을 추가한다. 버튼을 한 번씩 누른다.

---

## 1일차 · 27–30분 — 실습 연결

- web-week13에 12주 완성본을 이어 쓴다.
- ex01~ex03에서 본문·상태·응답 id를 비교한다.
- 빈 문자열과 앞뒤 공백의 차이를 확인한다.

**설명 합계: 4 + 5 + 7 + 6 + 5 + 3 = 30분**

[1일차 실습](lab.md#1일차-실습) · [따라하기](walkthrough.md)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security

---

## 2일차 · 0–5분 — 폼에서 요청까지

- submit → preventDefault → value.trim은 7주와 같다.
- 검사한 값을 POST의 body에 넣는다.
- 이름은 별칭, 메시지는 500자 이내다.
- 이메일·비밀번호 입력 칸은 만들지 않는다.

저장 성공을 확인하기 전에 입력 칸을 비우지 않는다.

---

## 2일차 · 5–12분 — 입력값을 POST에 연결

[ex04](examples/day2/ex04/index.html) · [코드](examples/day2/ex04/app.js) · [설정](examples/day2/ex04/config.example.js)

```js
form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const message = messageInput.value.trim();
  // 값 검사 후 await fetch(...)
});
```

이벤트 함수도 async이면 await를 쓸 수 있다.
Network의 Payload와 실제 입력값을 비교한다.

---

## 2일차 · 12–18분 — 저장 중과 완료

[ex05](examples/day2/ex05/index.html) · [코드](examples/day2/ex05/app.js) · [설정](examples/day2/ex05/config.example.js)

- 요청 직전: 버튼 disabled = true, 저장 중 안내.
- 성공 응답: 저장 완료 표시, 입력 칸 비우기.
- 실패: 입력 보존, 목록에서 결과 확인 안내.
- finally: 버튼 disabled = false.

Network 속도를 낮춰 기다리는 동안의 버튼을 확인한다.
빠른 중복 클릭을 줄이지만 서버의 중복 저장을 보장해 막지는 않는다.

---

## 2일차 · 18–23분 — 저장 다음 GET

[ex06](examples/day2/ex06/index.html) · [코드](examples/day2/ex06/app.js) · [설정](examples/day2/ex06/config.example.js)

```js
const saved = await response.json();
notice.textContent = `저장 완료 · 글 번호 ${saved[0].id}`;
await loadMessages();
```

POST 성공 뒤 GET으로 서버 목록을 다시 읽는다.
저장 성공과 목록 읽기 실패는 서로 다른 결과다.

---

## 2일차 · 23–27분 — 두 브라우저에서 확인

1. 브라우저 A에서 글을 저장한다.
2. B에서 같은 API·BOOK_ID의 목록을 읽는다.
3. A를 새로고침하고 같은 글을 확인한다.

다른 PC·휴대폰에는 공용 HTTPS API가 필요하다.
127.0.0.1은 기기마다 자기 자신을 가리킨다.
저장 응답을 못 받았다면 GET으로 확인한 뒤 재전송한다.

---

## 2일차 · 27–30분 — 저장 방명록 조립

- guestbook.js: GET과 목록 표시.
- submit.js: POST와 저장 안내.
- POST 201 뒤 GET 200, 화면의 새 글을 확인한다.

**설명 합계: 5 + 7 + 6 + 5 + 4 + 3 = 30분**

[2일차 실습](lab.md#2일차-실습) · [따라하기](walkthrough.md)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security

---

# 만들기 파일

[방명록](examples/day2/web-week13/guestbook.html) · [GET](examples/day2/web-week13/guestbook.js) · [POST](examples/day2/web-week13/submit.js)
[설정](examples/day2/web-week13/config.example.js) · [홈](examples/day2/web-week13/index.html) · [내 정보](examples/day2/web-week13/about.html)
[홈 JS](examples/day2/web-week13/app.js) · [CSS](examples/day2/web-week13/styles.css) · [프로필](examples/day2/web-week13/images/profile.png)

[예제 설명](examples/README.md) · [실습](lab.md) · [따라하기](walkthrough.md)

설정 → GET 코드 → POST 코드 순서로 script를 연결한다.
