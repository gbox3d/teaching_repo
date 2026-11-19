# 12주차 따라하기 · API 소개에서 서버 목록까지

## 1. 사전 준비와 서버 실행

강의자는 제공 11주 완성본과 12주 틀을 배부한다. 학생의 11주 필수 산출물은 ex06 폼 복원이며 전체 객체 배열 방명록 구현을 전제하지 않는다. `web-week12` 작업 폴더·저장소는 수업 전에 준비한다. 홈·내 정보·app.js·styles.css·프로필을 이어 쓴다.

교재 저장소 최상위에서 API와 정적 서버를 서로 다른 터미널로 실행한다. Node.js 기본 모듈만 사용하며 npm 설치가 필요 없다.

```powershell
node web_programming/tools/guestbook-api/server.mjs
```

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week12_fetch_json/examples 8000
```

API는 `http://127.0.0.1:8787`, 예제는 `http://localhost:8000/day1/ex01/`에서 시작한다. 완성본은 `http://localhost:8000/day2/web-week12/guestbook.html`이다. 독립 폴더에서는 정적 서버 파일을 복사해 `node server.mjs`로 실행한다. `file://` 실행은 사용하지 않는다.

## 2. 브라우저와 REST Client 설정

브라우저의 제공 `api-settings.js`는 로컬 가상값으로 시작한다. 공용 서버를 쓰면 API 설정 패널에 배부받은 HTTPS 주소·공개 키·방명록 번호를 입력하고 적용한다. 메모리에서만 사용하므로 새로고침 후 다시 입력한다. 실제 값을 JS에 넣지 않는다. 공개 키·편집 키·서버 비밀 키를 혼동하지 않는다.

VS Code에 `humao.rest-client`를 설치한다. 각 폴더 `.env.example`을 `.env`로 복사한다. 같은 기본값은 그대로 실행되며 공용 값은 무시되는 `.env`에서만 수정한다. `requests.http`는 `{{$dotenv API_BASE_URL}}`·`{{$dotenv API_PUBLIC_KEY}}`·`{{$dotenv BOOK_ID}}`를 읽는다. 모든 요청에는 `apikey` 헤더가 있고 GET 본문은 없다. 브라우저 패널은 이 `.env`를 읽지 않는다.

## 3. about → help → GET 순서

ex01의 **Send Request**로 about 200과 정보 배열을 확인한다. ex02 help에서 200과 step 1~6을 읽는다. ex03 GET에서 자기 book_id와 limit 1·2·5를 비교한다. 각 브라우저 화면에서도 다시 요청을 눌러 같은 결과를 확인한다. JSON 단독 복습은 [11주 ex05](../week11_object_localstorage/examples/day2/ex05/)에 있다.

Network의 Fetch/XHR에서 URL·GET·상태·Response를 읽는다. 응답 객체의 status와 `response.json()`으로 읽은 본문 배열은 다르다. 200과 `[]`는 요청 성공·빈 데이터다. HTTP 404는 응답이 도착한 오류이고 Offline은 응답을 받지 못한 통신 실패다.

## 4. 로컬 보관본과 서버 화면

11주 제공 `guestbook.html`·`guestbook.js`를 `guestbook.local.html`·`guestbook.local.js`로 보관하고 보관 HTML의 script src를 고친다. 저장 키는 그대로 둔다. 같은 origin이면 기존 로컬 글을 읽을 수 있고 다른 origin이면 저장 공간이 다르다. 서버 목록을 만들며 localStorage를 지우거나 자동 이관하지 않는다.

기본 메뉴의 방명록은 서버 `guestbook.html`이다. 홈·내 정보·W3.CSS·목록 자리는 유지한다. 데이터 동작은 `guestbook.js`에 모으고 제공 `api-settings.js`를 앞에 연결한다. 추가 스타일은 함께 배부하는 `shared/examples.css`다.

## 5. 제공 틀의 세 곳 연결

30분 실습에서는 아래 `guestbook.js`의 GET URL, `response.json()`, `showList(items)` 세 곳을 연결한다. 나머지 설정·DOM·오류 틀은 제공한다. latestRequest/requestId는 설정 변경 중 늦은 이전 응답이 목록·버튼을 덮지 않게 하는 제공 코드다. 파일 전체를 다시 타이핑하지 않는다. 다음 두 코드 블록은 완성본 실파일과 같다.

### guestbook.html

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>온라인 방명록</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
    <link rel="stylesheet" href="shared/examples.css">
  <script src="api-settings.js" defer></script>
    <script src="guestbook.js" defer></script>
  </head>
  <body class="w3-light-grey">
    <header class="w3-container w3-teal w3-padding-16">
      <h1>온라인 방명록</h1>
    </header>
    <nav class="w3-bar w3-white w3-card" aria-label="주 메뉴">
      <a class="w3-bar-item w3-button w3-mobile" href="index.html">홈</a>
      <a class="w3-bar-item w3-button w3-mobile" href="about.html">내 정보</a>
      <a class="w3-bar-item w3-button w3-mobile w3-teal" href="guestbook.html" aria-current="page">방명록</a>
    </nav>
    <main class="teaching-example w3-content w3-padding">
      <details class="w3-margin-bottom">
  <summary>API 설정</summary>
  <form id="api-settings-form" autocomplete="off">
    <p><label for="api-base-url">API 주소</label>
      <input class="w3-input w3-border" id="api-base-url" type="url" required></p>
    <p><label for="api-public-key">공개 키</label>
      <input class="w3-input w3-border" id="api-public-key" type="password" autocomplete="off" required></p>
    <p><label for="api-book-id">방명록 번호</label>
      <input class="w3-input w3-border" id="api-book-id" pattern="[a-z0-9_-]{1,40}" required></p>
    <button class="w3-button w3-teal" type="submit">설정 적용</button>
    <p id="api-settings-notice" role="status">로컬 연습 설정</p>
  </form>
</details>
      <section class="w3-container w3-card w3-white w3-margin-top">
        <h2>서버에 남긴 글</h2>
        <p><button class="w3-button w3-teal" id="reload-button" type="button">새로 불러오기</button></p>
        <div class="w3-text-grey" id="load-notice" role="status"></div>
        <p id="empty" hidden>아직 남긴 글이 없습니다.</p>
        <ul id="list" class="w3-ul" aria-live="polite"></ul>
        <div id="count">최근 글 0개</div>
      </section>
      <p><a href="guestbook.local.html">11주 로컬 저장본</a></p>
    </main>
    <footer class="w3-container w3-center w3-text-grey w3-padding-16"><p>수업용 연습 페이지 · 별칭만 사용하세요.</p></footer>
  </body>
</html>
```

### guestbook.js

```js
const list = document.querySelector('#list');
const countBox = document.querySelector('#count');
const empty = document.querySelector('#empty');
const loadNotice = document.querySelector('#load-notice');
const reloadButton = document.querySelector('#reload-button');

// GET 응답 표시
function showList(items) {
  list.replaceChildren();
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message}`;
    list.append(li);
  }
  countBox.textContent = `최근 글 ${items.length}개`;
  empty.hidden = items.length !== 0;
}

// GET 요청
let latestRequest = 0;

async function loadMessages() {
  const requestId = ++latestRequest;
  loadNotice.textContent = '불러오는 중';
  reloadButton.disabled = true;
  try {
    const url = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`;
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    if (requestId !== latestRequest) return false;
    showList(items);
    loadNotice.textContent = '불러오기 완료';
    return true;
  } catch (error) {
    if (requestId !== latestRequest) return false;
    list.replaceChildren();
    empty.hidden = true;
    countBox.textContent = '조회 결과 없음';
    loadNotice.textContent = `조회 실패: ${error.message}. 주소와 연결을 확인하세요.`;
    return false;
  } finally {
    if (requestId === latestRequest) reloadButton.disabled = false;
  }
}

reloadButton.addEventListener('click', loadMessages);
setupApiSettings(loadMessages);
loadMessages();
```

제공 설정 파일은 [api-settings.js](examples/day2/web-week12/api-settings.js)다. 초기화는 모든 DOM 변수·함수·이벤트를 준비한 뒤 `setupApiSettings(loadMessages)`와 최초 `loadMessages()`를 실행한다. 13주도 이 순서를 이어 쓴다.

## 6. 확인과 수업 뒤 업로드

ex05에서 없는 필드→정상 필드를 선택해 로컬 400→200을 비교한다. ex06은 페이지를 연 상태에서 Network를 Offline으로 바꾸고 다시 요청한다. 실패 안내·버튼 복구를 확인하고 No throttling으로 되돌려 재시도한다. 완성본은 새로 불러오기를 반복해도 목록이 누적되지 않고 빈 배열이면 0개 안내가 보인다.

375px와 넓은 화면에서 메뉴·입력·목록을 확인한다. 현재 목록과 GET 200을 캡처하되 키 입력칸과 Request Headers는 접는다. 이전 screenshots 파일은 이번 주 검증 증거로 제출하지 않는다.

업로드는 수업 뒤 진행한다. `.gitignore`를 포함하고 `.env`·실제 키를 제외한 뒤 add·commit·push한다. 공용 Pages에서는 배부 HTTPS API 값을 패널에 입력한다. 로컬 리허설을 두 기기 공유 검증으로 표시하지 않는다. 공용 API가 준비됐을 때 두 브라우저의 같은 목록을 별도로 확인한다.
