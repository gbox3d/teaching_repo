---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 12주차"
footer: "REST API · GET"
---

# REST API로 방명록 읽기

11주: localStorage → 12주: 서버에 GET 요청

- 강의자가 공용 API를 준비한다.
- 학생은 요청을 보내고 응답을 화면에 표시한다.
- 결과: 서버 목록과 Network의 GET 200.
- 매 수업: 설명 30분 + 실습 60분.

---

## 1일차 · 0–4분 — 페이지와 API 서버

- 정적 서버: HTML·CSS·JS 파일을 보낸다.
- API 서버: 방명록 데이터를 JSON으로 보낸다.
- 127.0.0.1:8787은 내 PC 연습 주소다.
- Pages에서는 강의자가 제공한 HTTPS API를 쓴다.

[정적 서버](../../tools/static-server/server.mjs) · [API 안내](../../tools/guestbook-api/README.md)

---

## 1일차 · 4–9분 — JSON 글자와 배열

[ex01](examples/day1/ex01/index.html) · [코드](examples/day1/ex01/app.js)

JSON은 전송하는 글자다. parse 후 배열로 읽는다.

```js
const text = '[{"name":"student01","message":"안녕하세요"}]';
const items = JSON.parse(text);
console.log(items[0].message);
```

---

## 1일차 · 9–16분 — GET과 두 번의 await

[ex02](examples/day1/ex02/index.html) · [코드](examples/day1/ex02/app.js) · [설정](examples/day1/ex02/config.example.js)

```js
const response = await fetch(url, {
  headers: { apikey: API_PUBLIC_KEY }
});
const items = await response.json();
```

- fetch는 응답을 기다린다. 기본 메서드는 GET이다.
- json()은 응답 본문을 읽고 배열·객체로 바꾼다.
- await를 쓰는 함수 앞에는 async를 붙인다.

---

## 1일차 · 16–22분 — Network에서 요청 읽기

1. Network를 열고 새로고침한다.
2. Fetch/XHR에서 guestbook 요청을 선택한다.
3. Headers에서 URL·GET·상태 200을 확인한다.
4. Response에서 글 배열을 읽는다.

apikey는 공개 키다. 서버 비밀 키를 넣지 않는다.
이번 GET에는 JSON 요청 본문이 없다.

---

## 1일차 · 22–27분 — 주소의 쿼리 문자열

[ex03](examples/day1/ex03/index.html) · [코드](examples/day1/ex03/app.js) · [설정](examples/day1/ex03/config.example.js)

```text
/rest/v1/guestbook?book_id=eq.student01
&select=id,name,message,created_at&order=id.desc&limit=2
```

실제 주소는 줄바꿈 없이 한 줄이다.
- book_id: 읽을 방명록, select: 응답 항목.
- order: 최신 번호부터, limit: 최대 개수.
- 제공 URL에서 limit 하나를 바꿔 비교한다.

---

## 1일차 · 27–30분 — 실습 연결

- web-week12에 지난주 완성본을 이어 쓴다.
- ex01~ex03에서 값을 하나씩 바꾼다.
- 요청·응답·화면의 변화를 비교한다.

**설명 합계: 4 + 5 + 7 + 6 + 5 + 3 = 30분**

[1일차 실습](lab.md#1일차-실습) · [따라하기](walkthrough.md)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_fetch_json

---

## 2일차 · 0–5분 — 기존 목록 코드 재사용

- 10주: 배열을 읽어 li를 만들었다.
- 11주: localStorage에서 배열을 읽었다.
- 12주: 서버 응답에서 배열을 읽는다.

목록을 그리는 DOM 코드는 이어 쓴다.
11주 localStorage와 서버의 글은 자동으로 합쳐지지 않는다.

---

## 2일차 · 5–12분 — 서버 배열을 목록으로

[ex04](examples/day2/ex04/index.html) · [코드](examples/day2/ex04/app.js) · [설정](examples/day2/ex04/config.example.js)

```js
for (let i = 0; i < items.length; i++) {
  const li = document.createElement('li');
  li.textContent = `${items[i].name}: ${items[i].message}`;
  list.append(li);
}
```

서버의 메시지도 textContent로 넣는다.
빈 배열이면 반복하지 않아 빈 목록이 된다.

---

## 2일차 · 12–18분 — HTTP 실패도 응답이다

[ex05](examples/day2/ex05/index.html) · [코드](examples/day2/ex05/app.js) · [설정](examples/day2/ex05/config.example.js)

```js
if (!response.ok) {
  throw new Error(`HTTP ${response.status}`);
}
```

없는 끝점에도 응답을 받을 수 있다.
ok를 먼저 확인하고 성공한 JSON 목록만 그린다.
실패 번호·오류 본문은 API별로 다를 수 있다.

---

## 2일차 · 18–23분 — 연결 실패 표시

[ex06](examples/day2/ex06/index.html) · [코드](examples/day2/ex06/app.js) · [설정](examples/day2/ex06/config.example.js)

```js
try {
  // 요청, 응답 검사, JSON 읽기
} catch (error) {
  loadNotice.textContent = '목록을 불러오지 못했습니다.';
}
```

Network를 Offline으로 바꿔 보고 복구한다.
이전 목록과 실패 안내를 구별한다.

---

## 2일차 · 23–27분 — 기다리는 동안 버튼

```js
reloadButton.disabled = true;
try {
  // 목록 요청
} catch (error) {
  // 실패 안내
} finally {
  reloadButton.disabled = false;
}
```

finally는 성공·실패 어느 쪽에서도 마무리한다.

---

## 2일차 · 27–30분 — 방명록 읽기 조립

- 설정 → GET → JSON 배열 → showList 순서다.
- 새로 불러오기 버튼이 GET을 다시 보낸다.
- 서버 목록과 GET 200을 캡처 한 장으로 확인한다.

**설명 합계: 5 + 7 + 6 + 5 + 4 + 3 = 30분**

[2일차 실습](lab.md#2일차-실습) · [따라하기](walkthrough.md)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_fetch_json

---

# 만들기 파일

[방명록](examples/day2/web-week12/guestbook.html) · [GET 코드](examples/day2/web-week12/guestbook.js) · [설정](examples/day2/web-week12/config.example.js)
[홈](examples/day2/web-week12/index.html) · [내 정보](examples/day2/web-week12/about.html) · [홈 JS](examples/day2/web-week12/app.js)
[CSS](examples/day2/web-week12/styles.css) · [프로필](examples/day2/web-week12/images/profile.png)

[예제 설명](examples/README.md) · [실습](lab.md) · [따라하기](walkthrough.md)

파일 이름과 script 순서를 유지한다. 설정값은 강의자 안내값을 쓴다.
