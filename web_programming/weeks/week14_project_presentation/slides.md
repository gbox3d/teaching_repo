---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 14주차"
footer: "REST API · PATCH · DELETE"
---

# REST API로 방명록 수정·삭제

13주 POST로 저장한 글을 ID로 고친다.

1일차: ID · DELETE · 204 · 재조회
2일차: PATCH · 폼 · 변경 확인

레포트와 발표는 별도 과제다.

---

# 1일차 · 0–5분 — 배열 위치와 서버 ID

```js
const items = [{ id: 41 }, { id: 73 }];
console.log(items[0].id); // 41
```

배열 위치는 0부터 세지만 서버 ID는 글의 번호다.
목록을 정렬해도 ID는 바뀌지 않는다.
[ex01 화면](examples/day1/ex01/index.html) · [app.js](examples/day1/ex01/app.js) · [설정](examples/day1/ex01/config.example.js)

---

# 1일차 · 5–10분 — DELETE 요청

```text
DELETE /rest/v1/guestbook?id=eq.41&book_id=eq.student01
```

- 삭제할 ID와 자기 방명록 번호를 지정한다.
- 목록의 배열 위치를 보내지 않는다.
- 자신의 연습 글로 실행한다.
[ex02 화면](examples/day1/ex02/index.html) · [app.js](examples/day1/ex02/app.js) · [설정](examples/day1/ex02/config.example.js)

---

# 1일차 · 10–15분 — 편집 키를 헤더에 넣기

```js
headers: {
  apikey: API_PUBLIC_KEY,
  "X-Edit-Key": editKey
}
```

공개 키는 API 호출용, 편집 키는 자기 방명록의 변경 허용용이다.
편집 키는 실행 중 입력한다. 코드·URL·캡처에 적지 않는다.
`BOOK_ID`만 안다고 수정 권한이 생기지 않는다.

---

# 1일차 · 15–20분 — 204는 본문 없음

```js
if (!response.ok) {
  throw new Error(`HTTP ${response.status}`);
}
// DELETE 204 뒤 response.json()을 쓰지 않는다.
```

Network에서 Method, Status, Response를 본다.
204는 응답 본문이 없다는 뜻이다.

---

# 1일차 · 20–25분 — GET으로 삭제 확인

같은 ID를 GET으로 다시 읽는다.

- 배열이 비었으면 그 ID의 글이 없다.
- 글이 남아 있으면 편집 키와 ID를 확인한다.
- 잘못된 키에도 204가 올 수 있으므로 번호만으로 판단하지 않는다.

[재조회 예제](examples/day2/ex04/index.html) · [app.js](examples/day2/ex04/app.js) · [설정](examples/day2/ex04/config.example.js)

---

# 1일차 · 25–30분 — 실습 연결

자기 방명록에 세 글을 남기고 가운데 ID만 삭제한다.

1. DELETE 요청 전 ID 확인
2. Network의 204 확인
3. GET으로 실제 삭제 확인

**설명 합계: 5 + 5 + 5 + 5 + 5 + 5 = 30분**
[1일차 실습](lab.md#1일차-실습) · [따라하기](walkthrough.md)
[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation)

---

# 2일차 · 0–5분 — PATCH는 기존 글 수정

```text
POST   /rest/v1/guestbook           새 글
PATCH  /rest/v1/guestbook?id=eq.41&book_id=eq.student01
```

PATCH는 ID로 고른 글의 일부 값을 바꾼다.
[ex03 화면](examples/day2/ex03/index.html) · [app.js](examples/day2/ex03/app.js) · [설정](examples/day2/ex03/config.example.js)

---

# 2일차 · 5–10분 — 수정할 값을 JSON으로

```js
method: "PATCH",
body: JSON.stringify({ message: message })
```

헤더: `Content-Type: application/json`
헤더: `Prefer: return=representation`
공개 키와 편집 키도 헤더에 넣는다.
`id`와 `book_id`는 본문으로 바꾸지 않는다.

---

# 2일차 · 10–15분 — 기존 글을 폼에 넣기

```js
editId.value = item.id;
editMessage.value = item.message;
editMessage.focus();
```

수정 버튼은 클릭한 글의 객체를 사용한다.
새 글 폼과 수정 폼은 구별한다.
[actions.js](examples/day2/web-week14/actions.js)

---

# 2일차 · 15–20분 — 빈 배열도 확인

```js
const changed = await response.json();
if (changed.length !== 1) {
  throw new Error("편집 키와 글 번호를 확인하세요.");
}
```

PATCH가 200이어도 `[]`이면 바뀐 글이 없다.
다시 GET해 메시지가 실제로 바뀌었는지 확인한다.
[edit.js](examples/day2/web-week14/edit.js) · [delete.js](examples/day2/web-week14/delete.js)

---

# 2일차 · 20–25분 — 13주 방명록에 연결

- 기존 GET: `guestbook.js`
- 기존 POST: `submit.js`
- ID·키·수정 폼: `actions.js`
- 수정·삭제: `edit.js`, `delete.js`

[방명록](examples/day2/web-week14/guestbook.html) · [GET](examples/day2/web-week14/guestbook.js) · [POST](examples/day2/web-week14/submit.js)
[설정](examples/day2/web-week14/config.example.js) · [CSS](examples/day2/web-week14/styles.css)
[홈](examples/day2/web-week14/index.html) · [내 정보](examples/day2/web-week14/about.html) · [홈 JS](examples/day2/web-week14/app.js) · [프로필](examples/day2/web-week14/images/profile.png)

---

# 2일차 · 25–30분 — 실습 연결

수정한 글과 남은 글을 새로고침 후 확인한다.
키 입력 칸을 비우고 결과와 Network를 캡처한다.

**설명 합계: 5 + 5 + 5 + 5 + 5 + 5 = 30분**
[2일차 실습](lab.md#2일차-실습) · [따라하기](walkthrough.md)
[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation)
