---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 12주차"
footer: "REST API · GET"
---

# REST API로 방명록 읽기

11주 필수: 폼 한 객체 저장·복원. 객체 배열 방명록은 제공 시연본.
12주: about → help → 자기 목록 GET.

- 양일 강의·시연 60분 + 실습 30분.
- 준비는 사전, 업로드는 수업 뒤 정리.
- 결과: 서버 목록과 Network GET 200 캡처.

---

## 1일차 · 0~5분 · 실행 준비 확인

- 정적 서버는 HTML·CSS·JS, API 서버는 JSON을 보낸다.
- 로컬 기본값: 127.0.0.1:8787 / classroom-local / student01.
- Pages는 배부받은 공용 HTTPS API를 패널에 입력한다.
- 설정은 메모리에만 있다. 새로고침하면 다시 입력한다.

[따라하기](walkthrough.md) · [API 준비](../../tools/guestbook-api/README.md)

---

## 1일차 · 5~15분 · URL과 헤더

- URL은 요청할 서버와 경로를 가리킨다.
- GET에는 JSON 요청 본문이 없다.
- apikey 헤더는 공개 호출용 키다. 서버 비밀 키가 아니다.
- BOOK_ID는 분류 태그이며 사용자 인증이 아니다.
- 제공 패널을 재구현하지 않는다.

---

## 1일차 · 15~30분 · about와 help

[ex01](examples/day1/ex01/README.md) → [ex02](examples/day1/ex02/README.md)

1. REST Client 설치, .env.example을 .env로 복사한다.
2. about의 **Send Request**: 200과 API 정보 배열.
3. help의 **Send Request**: 200과 사용법 배열.
4. 브라우저에서도 다시 요청을 눌러 결과를 대조한다.

브라우저 패널과 .env는 별개다. 실제 값은 Git·ZIP에 넣지 않는다.

---

## 1일차 · 30~40분 · JSON 복습

[11주 ex05](../week11_object_localstorage/examples/day2/ex05/README.md)

- JSON은 전송·저장용 문자열 형식이다.
- 객체·배열로 읽은 뒤 필드와 길이에 접근한다.
- 응답 객체의 status와 본문의 name·message를 구분한다.
- Network Response에서 배열의 대괄호와 객체의 필드를 찾는다.

---

## 1일차 · 40~55분 · GET과 await

[ex03](examples/day1/ex03/README.md) · [코드](examples/day1/ex03/app.js)

```js
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
```

async 함수에서 응답과 JSON 본문을 차례로 기다린다.
book_id는 방명록 필터, limit은 최대 글 수다. 1·2·5를 비교한다.

---

## 1일차 · 55~60분 · 30분 실습 인계

| 실습 시간 | 활동 |
|---|---|
| 0~5분 | 브라우저와 .env 설정 |
| 5~13분 | about·help Send Request |
| 13~23분 | BOOK_ID·limit 변경 |
| 23~30분 | URL·200·응답 배열 확인 |

강의 합계 5+10+15+10+15+5=60분. [실습지](lab.md)

---

## 2일차 · 0~5분 · 로컬 보관본과 서버

- 10주 문자열 배열·목록, 11주 제공 객체 배열 방명록을 비교한다.
- 11주 필수 폼 실습과 제공 시연본을 구분한다.
- guestbook.local.html/js는 원래 저장 키를 유지한다.
- guestbook.html은 서버 읽기 화면이다.
- 로컬 글을 옮기거나 지우지 않는다.

---

## 2일차 · 5~20분 · 응답에서 showList로

[ex04](examples/day2/ex04/README.md) · [완성본](examples/day2/web-week12/guestbook.js)

```js
  list.replaceChildren();
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message}`;
    list.append(li);
  }
```

다시 그리기 전에 비운다. textContent로 표시한다. []는 정상 빈 목록이다.

---

## 2일차 · 20~35분 · response.ok

[ex05](examples/day2/ex05/README.md)

- 정상 필드: 로컬 Status 200 · ok true.
- 없는 필드: 로컬 Status 400 · ok false.
- HTTP 오류에도 응답이 도착한다. 상태와 오류 JSON을 읽는다.
- 정상 필드로 복구한다. API마다 오류 번호·본문은 다를 수 있다.

```js
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
```

---

## 2일차 · 35~45분 · try/catch와 통신 실패

[ex06](examples/day2/ex06/README.md)

1. 페이지를 먼저 연다.
2. Network Offline → 다시 요청 → 실패 안내.
3. No throttling → 다시 요청 → GET 200.

연결 실패는 HTTP 오류와 다르다. catch에서 안내하고 finally에서
버튼을 다시 활성화한다. 성공·실패 어느 쪽에서도 재시도가 가능하다.

---

## 2일차 · 45~55분 · 재시도와 조립

- guestbook.js 하나에 GET·showList·실패 안내를 모은다.
- api-settings.js를 먼저 읽는다. 패널은 제공 기능이다.
- 모든 DOM·이벤트 준비 뒤 최초 GET을 실행한다.

```js
reloadButton.addEventListener('click', loadMessages);
setupApiSettings(loadMessages);
loadMessages();
```

새로 불러오기를 반복해도 목록이 누적되지 않는다.

---

## 2일차 · 55~60분 · 30분 실습 인계

| 실습 시간 | 활동 |
|---|---|
| 0~12분 | URL·JSON·showList 세 곳 연결 |
| 12~22분 | HTTP 오류·Offline·복구 |
| 22~30분 | 375px·목록·GET 200 캡처 |

강의 합계 5+15+15+10+10+5=60분. [실습지](lab.md)
로컬 리허설과 공용 서버의 두 브라우저 공유 확인을 구분한다.

---

# 다음 주로 이어 쓰는 파일

[방명록](examples/day2/web-week12/guestbook.html) · [GET 코드](examples/day2/web-week12/guestbook.js) · [제공 설정](examples/day2/web-week12/api-settings.js)
[폴더 안내](examples/day2/web-week12/README.md) · [요청](examples/day2/web-week12/requests.http)
[따라하기](walkthrough.md) · [실습지](lab.md)

13주는 같은 폴더에 name·message·guestbook-form·notice 폼을 복원하고
guestbook.js에 POST를 추가한다. 기존 로컬 저장본은 보관한다.
공용 설정은 소스에 기록하지 않고 실행 중 입력한다.
