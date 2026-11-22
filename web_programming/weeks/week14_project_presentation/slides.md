---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 14주차"
footer: "REST API · PATCH · DELETE"
---

# REST API로 방명록 수정·삭제

13주 GET·POST에 서버 ID 기반 DELETE·PATCH를 연결한다.

양일 강의·시연 60분 + 학생 실습 30분
1일차 DELETE 3곳 · 2일차 PATCH 3곳
파일·저장소 준비는 수업 전, 공개 업로드는 수업 뒤
레포트 검사·발표 평가는 별도 과제다.

---

# 1일차 · 0–20분: 준비와 서버 ID

준비 확인 5분 + 인덱스와 ID 15분

```js
const items = [{ id: 41 }, { id: 73 }];
console.log(items[0].id); // 41
```

위치 0과 ID 41은 다르다. 순서를 바꿔도 객체의 ID는 유지된다.
[ex01](examples/day1/ex01/index.html) · [코드](examples/day1/ex01/app.js)

---

# 1일차 · 20–30분: 편집 키

공개 키는 API 호출용, 편집 키는 방명록 변경 권한 확인용이다.
BOOK_ID는 글 구분값이다. 실행 중 편집 키를 입력한다.

```js
headers: { apikey: API_PUBLIC_KEY, 'X-Edit-Key': editKey }
```

설정 파일·키 처리는 제공한다. 편집 키의 [키 지우기]는 메모리도 비운다.
공개 키는 처음 열 때 묻는 창에 넣어 localStorage에 둔다. 편집 키는 저장하지 않는다.
공개 키를 잘못 넣었으면 [공개 키 지우기]를 누르고 다시 넣는다.

---

# 1일차 · 30–40분: DELETE 대상과 요청

```text
DELETE /rest/v1/guestbook?id=eq.41&book_id=eq.student01
```

학생 수정 3곳: 대상 URL · method · 헤더
자기 연습 글의 서버 ID를 쓴다.
[ex02](examples/day1/ex02/index.html) · [요청](examples/day1/ex02/requests.http)
about → help → 목록 → 대상 GET을 먼저 확인한다.

---

# 1일차 · 40–45분: 204와 응답 본문

```js
if (!response.ok) throw new Error(`HTTP ${response.status}`);
// DELETE 204 뒤 response.json()을 호출하지 않는다.
```

Network에서 Method·Status·Response를 본다.
204는 본문 없음이다. 틀린 키에도 204일 수 있다.

---

# 1일차 · 45–55분: 같은 ID 재조회

```js
const remaining = await readMessage(url);
```

배열이 비었는지, 다른 글이 남았는지 확인한다.
글이 남으면 키와 ID를 확인한다. 재조회·방어 코드는 제공한다.
[ex04](examples/day2/ex04/index.html) · [코드](examples/day2/ex04/app.js)

---

# 1일차 · 55–60분: 실습 안내

강의·시연: 5 + 15 + 10 + 15 + 10 + 5 = 60분

학생 실습 30분: ID·.http 5 → DELETE 3곳 12 → 정답·틀린 키 재조회 13
지정한 ID 하나만 삭제한다. 업로드는 수업 뒤에 한다.
[실습지](lab.md#1일차-실습) · [따라하기](walkthrough.md)

---

# 2일차 · 0–20분: 준비와 PATCH

준비 확인 5분 + PATCH 15분

```js
method: 'PATCH',
body: JSON.stringify({ message: message })
```

기존 ID를 고치며 id·book_id는 본문에 넣지 않는다.
학생 수정 3곳: 대상 URL · JSON 본문 · 같은 ID 재조회
[ex03](examples/day2/ex03/index.html) · [요청](examples/day2/ex03/requests.http)

---

# 2일차 · 20–30분: 기존 글을 폼에 넣기

```js
editId.value = item.id;
editMessage.value = item.message;
editMessage.focus();
```

클릭한 객체를 쓰며 새 글 폼과 수정 폼을 구분한다.
폼 연결은 제공 코드다.
[guestbook.js](examples/day2/web-week14/guestbook.js)

---

# 2일차 · 30–40분: 응답 배열 확인

PATCH 200 []이면 바뀐 글이 없다.
응답의 ID와 행 수를 확인한다.

```js
const changed = await response.json();
```

헤더: apikey · X-Edit-Key · Content-Type · Prefer
통신 오류 뒤에는 중복 쓰기 전에 GET으로 확인한다.

---

# 2일차 · 40–45분: 저장 메시지 재조회

```js
const saved = await readMessage(url);
```

같은 ID의 메시지가 입력과 일치해야 수정 확인 완료다.
재조회 실패는 쓰기 실패와 구분한다.
늦은 조회 응답이 최신 목록을 덮지 않도록 제공 코드가 확인한다.

---

# 2일차 · 45–55분: 한 파일에서 CRUD

guestbook.js에 GET·POST·DELETE·PATCH 구역을 둔다.
config.example.js는 별도 제공하며 BOOK_ID만 바꾼다.
모든 함수·이벤트 초기화 뒤 파일 끝에서 최초 GET을 실행한다.

[방명록](examples/day2/web-week14/guestbook.html) · [동작](examples/day2/web-week14/guestbook.js)
[설정](examples/day2/web-week14/config.example.js)
[홈](examples/day2/web-week14/index.html) · [내 정보](examples/day2/web-week14/about.html)

---

# 2일차 · 55–60분: 실습 안내

강의·시연: 5 + 15 + 10 + 15 + 10 + 5 = 60분

학생 실습 30분: PATCH 3곳 12 → 세 글 검증·실패 복구 13 → 키 지우고 캡처 5
localhost 확인을 먼저 끝내고 수업 뒤 Pages·다른 브라우저에서는 처음 묻는 창에 공개 키를 넣고 확인한다.
[실습지](lab.md#2일차-실습) · [따라하기](walkthrough.md)
