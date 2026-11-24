# Hash SPA 따라하기

## 실제 파일과 section을 비교한다

[01 홈](examples/01_mpa/index.html)에서 내 정보 링크를 누르면 `about.html`을 받는다. [02](examples/02_two_screens/index.html)에서는 두 section이 이미 한 문서에 있고 버튼이 `hidden`만 바꾼다. `showScreen()` 안에서는 화면 표시만 하고 이벤트를 등록하지 않는다. 반복 전환 뒤 홈 횟수를 한 번 증가시켜 리스너 중복을 검사한다.

## 세 링크를 주소에 연결한다

[03 app.js](examples/03_hash_routes/app.js)의 `showRoute()`는 시작 때 한 번, hash가 바뀔 때마다 한 번 호출된다.

```js
const route = location.hash.slice(1) || 'home';
const known = route === 'home' || route === 'about' || route === 'guestbook';
const visibleId = known ? route : 'not-found';
```

빈 hash의 기본 화면은 홈이다. 미등록 hash는 정해진 안내 section을 쓴다. 각 section의 ID와 `visibleId`를 비교하여 하나만 표시한다. 링크의 `aria-current`, 문서 title, section 제목 포커스를 함께 갱신한다. 제목의 `tabindex="-1"`은 이 포커스 이동을 위한 속성이다.

```js
window.addEventListener('hashchange', showRoute);
window.addEventListener('load', showRoute, { once: true });
showRoute();
```

주소를 읽는 로직이 시작과 이후 전환에서 같아야 직접 주소와 새로고침이 동작한다. `load`의 한 번 실행은 직접 hash 진입 때 브라우저의 기본 앵커 처리 뒤 제목 포커스를 다시 맞추는 제공 코드다. `location.hash`에 들어온 문자열을 그대로 선택자에 넣지 않는다. 방명록 초안이 남는 이유는 숨긴 section이 DOM에 계속 있기 때문이다.

## 14주 방명록을 같은 문서에 넣는다

[04 index.html](examples/04_rest_guestbook/index.html)의 방명록 section은 14주 폼·목록·편집 구역을 이어 쓴다. `guestbook-form`, `name`, `message`, `notice`, `list`, `count` ID는 유지한다. 홈의 카운터는 `home-count`, `home-count-button`, `homeCount`, `homeCountBox`로 구별한다.

[04 app.js](examples/04_rest_guestbook/app.js)는 홈·라우팅과 14주 GET·POST·PATCH·DELETE를 한 동작 파일에 둔다. `config.example.js`만 별도 설정 파일이다. 이 파일이 수업용 서버 주소와 `BOOK_ID`를 정하고 공개 키는 이 브라우저의 localStorage에서 읽는다. 저장한 키가 없으면 처음 열 때 묻는 창을 띄우고 입력한 키를 localStorage에 저장한다. 방명록 제목 아래의 [공개 키 지우기] 버튼(`key-clear-button`)은 저장한 키를 지우고 새로고침해 다시 묻게 한다. 이 버튼의 동작도 `config.example.js`가 붙인다. 학생은 `BOOK_ID`를 배정받은 방명록 번호로 바꾼다. 초기 순서는 설정 스크립트 로딩→동작 DOM·함수·이벤트 준비→화면 선택→최초 `loadMessages()`다.

화면 전환은 서버 목록을 새로 읽지 않는다. 최초 실행, 새로 불러오기, 쓰기 뒤 확인이 GET을 실행한다. 다른 사람이 쓴 글은 새로 불러오기로 확인한다. 새로고침하면 초안과 편집 폼은 초기화되지만 서버에 저장한 글과 localStorage의 공개 키는 남아 최초 GET이 목록을 다시 보여 준다. 이는 단순 화면 전환과 다른 동작이다.

## 요청과 실패를 확인한다

[REST 안내](examples/04_rest_guestbook/README.md)에 따라 about·help·GET을 먼저 확인한다. POST는 생성 ID를 확인하고 PATCH·DELETE는 같은 ID의 GET으로 결과를 확인한다. 204 응답에는 `json()`을 호출하지 않는다.

방명록에서 글을 쓰는 동안 홈으로 이동해도 DOM은 유지된다. 전송이 완료되면 서버 결과와 안내가 갱신된다. 전송 성공 여부를 모르는 통신 오류에서는 다시 POST하기 전에 목록을 조회한다. GET 실패 후 새로 불러오기 버튼이 다시 활성화되는지 확인한다.

## 하위 경로와 키보드를 확인한다

예제 폴더를 정적 서버의 루트로 열어 `/index.html#guestbook`을 확인한 다음 저장소 루트 서버에서 `/web_programming/specials/hash_spa/examples/04_rest_guestbook/index.html#guestbook`을 연다. 두 주소 모두 실제 index 파일을 요청한다. GitHub Pages에서도 같은 상대 파일 경로를 사용한다. localStorage는 주소(출처)마다 따로이므로 포트가 다른 서버, 다른 브라우저, Pages 주소, 휴대폰에서는 처음 열 때 공개 키를 다시 묻는다.

각 주소에서 새로고침·뒤로·앞으로, `#missing`, 홈 복귀를 시험한다. Tab으로 메뉴를 선택하고 Enter를 누른 뒤 제목 포커스를 확인한다. 375px과 1280px에서 입력·버튼·안내가 가로로 넘치지 않는지 확인한다. 공용 API·실제 Pages·다른 기기는 별도 환경에서 검증해야 한다.
