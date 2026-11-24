---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · Hash SPA"
footer: "MPA · hash · DOM · REST"
---

# Hash SPA 특강

14주 방명록을 한 문서의 세 화면으로 합친다.

- 정규 수업은 MPA를 유지한다.
- 14주 이후 선택 특강이며 정규 시험 범위에서 제외한다.
- 프레임워크·npm 설치·History API 없이 구현한다.

[실습지](lab.md) · [따라하기](walkthrough.md)

---

## 준비와 단계

Node.js 24 이상·VS Code·Chrome을 준비한다.

```bash
node web_programming/tools/static-server/server.mjs web_programming 8111
```

01 MPA → 02 두 화면 → 03 세 hash → 04 REST 통합

화면 스타일은 W3.CSS 4.1.0 CDN에서 읽는다.
특강 차시 수와 실험 시간을 제한하지 않는다.

---

## 학생 수정과 제공 코드

| 구분 | 범위 |
|---|---|
| 학생 수정 | section 표시 조건·hash·이벤트 연결·ID 구별 |
| 강의자 시연 | MPA 요청·미등록 주소·포커스·CRUD 실패 |
| 제공 | 14주 REST·config.example.js·이전 요청 응답 보호 |
| 선택 | 방명록 진입 때 재조회 정책 비교 |

01~03은 60분 설명·시연+30분 실습 운영 예다.
04 조립·REST 실패 실험은 후속 시간에 진행한다.

---

## 01: 세 HTML은 세 문서다

[01 MPA](examples/01_mpa/README.md)

```html
<a href="index.html">홈</a>
<a href="about.html">내 정보</a>
<a href="guestbook.html">방명록</a>
```

각 주소에 실제 파일이 있다. 메뉴 클릭 시 Document 요청을 본다.
직접 주소·새로고침·뒤로/앞으로를 확인한다.
뒤로 가기는 캐시로 문서를 복원할 수도 있다.

---

## 02: 한 문서에 두 section을 둔다

[02 두 화면](examples/02_two_screens/README.md)

홈과 내 정보는 이미 DOM 안에 있다. 버튼이 표시만 바꾼다.

```js
for (let i = 0; i < sections.length; i++)
  sections[i].hidden = sections[i].id !== name;
```

홈 횟수 2 → 내 정보 → 홈: 횟수는 2다.
주소는 그대로이며 뒤로 가기로 화면을 선택할 수 없다.

---

## 03: 세 화면을 hash에 연결한다

[03 세 hash](examples/03_hash_routes/README.md)

```html
<a href="#home">홈</a>
<a href="#about">내 정보</a>
<a href="#guestbook">방명록</a>
```

주소는 index.html#guestbook이다.
서버는 index.html을 받고 브라우저 코드가 화면을 선택한다.
fragment는 서버 요청에 포함되지 않는다.

---

## 빈 주소와 미등록 주소

```js
const route = location.hash.slice(1) || 'home';
const known = route === 'home' ||
  route === 'about' || route === 'guestbook';
const visibleId = known ? route : 'not-found';
```

빈 hash는 홈이다. 없는 hash에는 안내와 홈 링크를 보인다.
미등록 문자열을 그대로 DOM 선택자에 넣지 않는다.
안내 화면에서는 현재 메뉴가 없다.

---

## 시작과 변경에 같은 함수를 쓴다

```js
window.addEventListener('hashchange', showRoute);
window.addEventListener('load', showRoute, { once: true });
showRoute();
```

처음 연 주소도 읽고, 이후 hash 변경도 읽는다.
직접 #guestbook 진입·새로고침·뒤로/앞으로가 같은 함수를 쓴다.
화면을 바꿀 때 이벤트를 다시 등록하지 않는다.

---

## 현재 메뉴와 제목 포커스

표시된 링크에 aria-current="page"를 두고 나머지는 제거한다.
문서 title과 표시된 section의 제목 포커스를 갱신한다.

```js
const heading = document.querySelector(`#${visibleId} h2`);
document.title = `${heading.textContent} · Hash SPA`;
heading.focus();
```

제목의 tabindex="-1"은 프로그램 포커스를 허용한다.
Tab으로 메뉴 이동 → Enter → 표시된 제목 포커스를 확인한다.

---

## DOM 유지와 입력 보존

hidden은 화면을 숨기며 DOM을 제거하지 않는다.

이름·메시지 입력 → 홈 → 내 정보 → 방명록

입력값은 남는다. innerHTML로 section 전체를 다시 만들지 않는다.
03의 미리 보기는 textContent로 표시하며 저장 기능이 아니다.
새로고침하면 초안과 홈 횟수는 초기화된다.

---

## 이벤트는 한 번만 등록한다

리스너 등록은 showRoute() 밖에서 수행한다.

- 홈·내 정보·방명록을 10회 오간다.
- 홈 횟수 증가를 한 번 누른다.
- 횟수가 정확히 1만 증가하는지 확인한다.
- 04에서 POST 한 번으로 글 하나만 생기는지 확인한다.

전환마다 함수를 등록하면 버튼 한 번이 여러 번 실행될 수 있다.

---

## 04: 14주 화면을 조립한다

[04 REST 통합](examples/04_rest_guestbook/README.md)

| 영역 | 유지할 이름 |
|---|---|
| 방명록 | guestbook-form, name, message, notice, list, count |
| 홈 | home-count, home-count-button, homeCount, homeCountBox |
| 동작 | app.js 한 파일 |
| 제공 설정 | config.example.js 별도 |

03 미리 보기 코드를 14주 CRUD로 교체한다.

---

## 모든 준비 뒤 최초 GET

config.example.js → app.js 순서로 defer 로딩한다.

DOM·함수·이벤트 준비 → showRoute() → loadMessages()

GET·POST·PATCH·DELETE는 app.js의 구역으로 구별한다.
편집 DOM과 함수가 준비되기 전에 조회를 시작하지 않는다.
config.example.js가 주소·BOOK_ID를 정하고 저장한 공개 키가 없으면 먼저 묻는다.

---

## REST Client는 about부터 시작한다

VS Code 확장 humao.rest-client를 사용한다.
.env.example을 같은 폴더의 .env로 복사한다.

API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 입력하고
requests.http의 각 요청 위 Send Request를 누른다.

about 200 → help 200 → GET 200 → POST 201

POST ID를 .env의 MESSAGE_ID에 적는다.
REST Client는 .env를 따로 읽고 브라우저에 저장한 공개 키는 쓰지 않는다.

---

## PATCH·DELETE는 같은 ID로 확인한다

| 요청 | 확인 |
|---|---|
| PATCH | 200과 변경 행, 같은 ID GET의 메시지 |
| DELETE | 204 빈 본문, 같은 ID GET의 빈 배열 |

PATCH 200 []는 변경 없음이다. 204에 json()을 호출하지 않는다.
PATCH·DELETE에는 방명록 태그와 글 번호를 함께 넣는다.
실제 키·서버 비밀 키를 추적 파일에 넣지 않는다.

---

## 조회 정책과 상태 수명

| 동작 | 입력·메모리 | GET |
|---|---|---|
| hash 이동 | 유지 | 없음 |
| 새로 불러오기 | 유지 | 실행 |
| 새로고침 | 초기화 | config.example.js 설정으로 실행 |
| 묻는 창 취소·빈 칸 | 공개 키 저장 안 함 | 실행 뒤 HTTP 401 |
| 공개 키 지우기 | 키 삭제 뒤 새로고침 | 다시 물은 뒤 실행 |

새로고침 뒤에도 공개 키와 서버에 저장한 글은 남는다.
POST 통신 실패는 재전송보다 조회를 먼저 한다.

---

## 루트와 프로젝트 하위 경로

```text
/index.html#guestbook
/<저장소>/index.html#guestbook
```

같은 실제 파일 경로를 새로고침한다.
호스트·포트·브라우저·기기가 바뀌면 처음 한 번 공개 키를 다시 묻는다.
`/<저장소>/guestbook` 같은 없는 경로를 만들지 않는다.
빈 hash·없는 hash·직접 주소·뒤로/앞으로를 모두 확인한다.
375px·1280px와 키보드 조작도 확인한다.

---

## 실습 증거와 후속 연구

관찰 표에 예상·실제·화면/요청 근거를 기록한다.

MPA Document 요청과 hash 전환을 비교한다.
10회 전환·초안 유지·이벤트 1회·CRUD 대상 ID를 확인한다.
없는 글 번호·통신 실패·복구 재조회를 시험한다.

로컬 리허설과 공용 API·Pages·다른 기기 검증을 구분한다.
선택 연구: 방명록 진입 시 GET 정책을 바꾸고 요청 수를 비교한다.
