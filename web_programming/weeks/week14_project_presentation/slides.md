---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 14주차"
footer: "REST API · PATCH · DELETE"
---

# 방명록 가운데 글 삭제와 남은 글 수정

| 글 번호 (예시) | 삭제 전 | 실습을 마친 뒤 |
|---|---|---|
| 81 | 악보 가져가기 | 악보 가져가기 |
| 73 | 간식 주문 | 목록에서 사라짐 |
| 41 | 연습 오후 3시 | 연습 오후 4시 |

수업 전 [14주 완성 방명록](examples/day2/web-week14/guestbook.html)에서 표의 글을 아래부터 한 건씩 **남기기**로 등록하고, 받은 글 번호 세 개를 적는다.

1일차에는 가운데 글을 삭제하고 2일차에는 연습 시간을 수정한다. 각 차시는 강의·시연 60분과 실습 30분이다.

---

# 1일차 · 0–20분: 준비와 서버 ID

```js
const items = [{ id: 41 }, { id: 73 }];
console.log(items[0].id); // 41
```

두 객체의 순서를 바꾸면 위치 0에는 73번 글이 온다. 41번 글은 두 번째 위치로 옮겨도 ID가 41이다.

방명록은 최신 글부터 표시한다. 새 글을 쓰면 가운데 글의 위치도 달라진다.
삭제 버튼은 그 행에 담긴 `row.id`를 사용한다.

[배열 위치와 서버 ID](examples/day1/ex01/index.html) · [예제 코드](examples/day1/ex01/app.js)

---

# 1일차 · 20–30분: 태그와 글 번호

```http
GET /rest/v1/guestbook?book_id=eq.student01&id=eq.73
```

`book_id`는 방명록을, `id`는 그 안에서 확인할 글을 고른다.
`config.example.js`의 `BOOK_ID`를 자기 태그로 바꾸고, 처음 열 때 수업용 공개 키를 입력한다.

모두 같은 `apikey`로 모든 태그의 글을 바꿀 수 있다. 실습에는 자기가 쓴 글을 사용한다.

[방명록 설정 파일](examples/day2/web-week14/config.example.js)

---

# 1일차 · 30–40분: DELETE 대상과 요청

목록에서 **73번 ‘간식 주문’ 옆의 삭제**를 누른다.
확인창의 **취소**를 누르면 요청은 0건이다. 다시 같은 행에서 **확인**을 누른다.

```js
const url = bookUrl + '&id=eq.' + id;
const response = await fetch(url, {
  method: 'DELETE',
  headers: { apikey: API_PUBLIC_KEY }
});
```

`bookUrl`에는 이미 자기 태그가 들어 있다. 버튼이 넘긴 `id`로 한 행을 지정한다.
[행별 삭제 예제](examples/day1/ex02/index.html) · [삭제 코드](examples/day1/ex02/app.js)

---

# 1일차 · 40–45분: 204와 응답 본문

| 브라우저에서 한 일 | Network에서 보이는 결과 |
|---|---|
| 확인창에서 취소 | DELETE 요청 없음 |
| 확인창에서 확인 | DELETE → 204, 응답 본문 없음 |
| 이미 지운 번호로 같은 DELETE 재전송 | 이때도 204가 올 수 있음 |

204 응답에는 읽을 JSON이 없다. 삭제 요청의 상태를 본 뒤 **같은 글 번호로 GET**을 보낸다.

---

# 1일차 · 45–55분: 같은 ID 재조회

| 삭제 후 확인할 것 | 예시 결과 |
|---|---|
| 자기 태그 + 73번으로 GET | `200 []` |
| 자기 태그의 목록으로 GET | 81번과 41번이 남음 |

먼저 삭제 전에 73번 글이 있었는지 확인해야 두 결과를 비교할 수 있다.
[글 다시 읽기](examples/day2/ex04/index.html)에서 같은 번호를 입력하고 **다시 읽기**를 누른다.
삭제된 번호면 화면에 **해당 글 없음**이 표시된다.

---

# 1일차 · 55–60분: 실습 안내

| 실습 시간 | 자기 방명록에서 할 일 |
|---|---|
| 0–5분 | 세 글을 준비한다. `.http`에서 about → help → 목록을 조회하고, 가운데 글 ID를 `.env`의 `MESSAGE_ID`에 넣어 대상 GET을 보낸다. |
| 5–17분 | 제공된 `guestbook.js`에서 삭제 대상 URL, method, 헤더를 작성한다. |
| 17–30분 | 가운데 글의 삭제를 취소한 뒤 다시 눌러 확인한다. 같은 ID의 빈 배열과 남은 두 글을 확인한다. |

[VS Code 요청 파일](examples/day1/ex02/requests.http)에서 각 요청 위 **Send Request**를 누른다.
[1일차 실습지](lab.md#1일차-실습)

---

# 2일차 · 0–20분: 준비와 PATCH

41번에 남아 있는 ‘연습 오후 3시’를 ‘연습 오후 4시’로 수정한다.

```http
PATCH /rest/v1/guestbook?id=eq.41&book_id=eq.student01
apikey: {{apiKey}}
Content-Type: application/json
Prefer: return=representation

{ "message": "연습 오후 4시" }
```

URL로 글을 고르고 본문에는 바꿀 값만 담는다.
[수정 요청 예제](examples/day2/ex03/index.html)에서 글 ID와 새 메시지를 입력하고 **수정 요청**을 누른다.

---

# 2일차 · 20–30분: 기존 글을 폼에 넣기

완성 방명록에서는 **41번 옆의 수정**을 누르면 폼에 글 번호와 현재 메시지가 채워진다.

```js
editId.value = item.id;
editMessage.value = item.message;
editMessage.focus();
```

글 번호는 읽기 전용이다. 메시지를 ‘연습 오후 4시’로 바꾸고 **수정 저장**을 누를 때 PATCH가 전송된다.
[완성 방명록](examples/day2/web-week14/guestbook.html) · [폼 연결 코드](examples/day2/web-week14/guestbook.js)

---

# 2일차 · 30–40분: 응답 배열 확인

`Prefer: return=representation`을 보내면 PATCH가 바꾼 행을 배열로 돌려준다.

| 자기 태그에서 PATCH한 글 | HTTP 상태 | 응답 배열에서 확인할 값 |
|---|---|---|
| 남아 있는 41번 | 200 | 한 행 · `id: 41` · 새 메시지 |
| 이미 삭제한 73번 | 200 | `[]` · 바뀐 행 0개 |

[수정 요청 파일](examples/day2/ex03/requests.http)에서 자신의 글 번호로 두 응답을 비교한다.
두 응답 모두 200이므로 배열을 열어 행 수와 글 번호를 읽는다.

---

# 2일차 · 40–45분: 저장 메시지 재조회

[글 다시 읽기](examples/day2/ex04/index.html)에서 자기 태그의 글 번호를 하나씩 조회한다.

| 글 번호 (예시) | 같은 태그와 번호로 GET한 결과 |
|---|---|
| 41 | 한 행 · **연습 오후 4시** |
| 73 | 빈 배열 |
| 81 | 한 행 · **악보 가져가기** |

수정 요청을 보낸 뒤 연결이 끊겨도 같은 GET으로 현재 메시지부터 확인한다.
[조회 전용 요청 파일](examples/day2/ex04/requests.http)

---

# 2일차 · 45–55분: 한 파일에서 CRUD

| 완성 방명록에서 누르는 버튼 | 서버에서 일어나는 일 |
|---|---|
| **남기기** | POST로 새 글을 저장하고 목록을 다시 읽는다. |
| **새로 불러오기** | GET으로 자기 태그의 최신 글을 불러온다. |
| 글 옆 **수정** → **수정 저장** | 해당 ID를 PATCH하고 같은 ID를 다시 읽는다. |
| 글 옆 **삭제** → 확인 | 해당 ID를 DELETE하고 같은 ID와 목록을 다시 읽는다. |

[완성 방명록 열기](examples/day2/web-week14/guestbook.html) · [guestbook.js](examples/day2/web-week14/guestbook.js)

---

# 2일차 · 55–60분: 실습 안내

| 실습 시간 | 자기 글로 확인할 것 |
|---|---|
| 0–12분 | `guestbook.js`에서 PATCH 대상 URL, JSON 본문, 같은 ID를 읽는 GET을 작성한다. |
| 12–25분 | 새 연습 글 세 개 중 가운데 글을 수정하고 같은 번호로 읽는다. 그 글을 지운 뒤 같은 번호로 PATCH해 빈 배열을 확인한다. |
| 25–30분 | 남은 목록과 수정 직후 GET의 응답을 한 화면에 담는다. |

캡처할 때는 Network에서 **Response**를 열어 공개 키가 화면에 나오지 않게 한다.
[2일차 실습지](lab.md#2일차-실습) · [단계별 따라하기](walkthrough.md)
