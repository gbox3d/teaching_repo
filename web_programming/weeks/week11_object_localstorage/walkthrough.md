[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_object_localstorage)

# 11주차 따라하기 — 객체와 기본 저장

양일 모두 강의·시연 60분 뒤 실습 30분을 진행한다. 수업 중에는 준비된 기본 예제를 실행하고 값을 바꿔 확인한다. 방명록 전체 코드는 문서 끝의 강의자용 부록에 따로 두었다.

## 준비

수업 전에 교재 저장소를 내려받아 VS Code로 연다. 예제 HTML·JS뿐 아니라 `web_programming/shared`가 포함된 폴더 구조를 유지한다.

```text
web_programming/
  shared/examples.css
  weeks/week11_object_localstorage/examples/
    day1/ex01/ ~ ex03/
    day2/ex04/ ~ ex06/
```

`teaching_repo` 폴더의 터미널에서 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

서버가 이미 실행 중이면 다시 실행하지 않는다. ex01~ex07의 HTML은 [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css), 추가 공용 스타일 `shared/examples.css`, 같은 폴더의 `app.js`를 읽는다. CDN 스타일에는 인터넷 연결이 필요하다. 설명과 조작 순서는 README에서 확인한다. [서버 안내](../../tools/static-server/README.md)

## 1일차

[ex01](http://localhost:8111/weeks/week11_object_localstorage/examples/day1/ex01/)을 열고 이름 적용 버튼과 화면 결과를 확인한다. 전체 객체는 F12 › Console에서 추가로 확인한다. 주소의 마지막 번호를 바꾸면 ex02·ex03이 열린다.

1. ex01의 `app.js`에서 객체의 `name`을 바꾸고 저장·새로고침한다. 전체 객체와 `item.name`의 값을 비교한다.
2. ex02의 마지막 화면 출력에 있는 `items[0].name`을 `items[1].name`으로 바꾼다. 새로고침 후 배열 결과 확인을 눌러 하늘이 바다로 바뀌는지 확인한다.
3. ex03에서 두 목록을 비교하고 둘째 목록의 `items[i].name`을 `items[i].message`로 바꾼 뒤 되돌린다. 속성 이름을 잘못 쓰면 `undefined`가 표시되는지 확인하고 되돌린다.

객체에서 필드를 읽는 방법을 설명할 수 있으면 1일차 확인을 마친다. 새 GitHub 저장소 생성·push·Pages 설정은 실습 시간에 넣지 않는다. [1일차 시간표](lab.md#1일차--객체와-점-표기-30분)

## 2일차

[ex04](http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex04/)를 연다. 기본 순서는 문자열 → JSON → 입력 폼이며 30분 안에 아래 세 예제를 확인한다.

| 예제 | 조작 | 확인 |
|---|---|---|
| ex04 | 문자열 저장 → 입력 변경 → 불러오기 → 지우기 | 저장한 문자열, 빈 문자열 `''`, 키 없음 `null` |
| ex05 | JSON 저장 → 저장 원문 조회 → JSON 복원 | 저장된 문자열과 두 객체의 이름·메시지 |
| ex06 | 폼 저장 → 새로고침 → 불러오기 → 지우기 | 복원된 입력과 저장 JSON |

### ex04 저장·불러오기·지우기

문자열을 입력하고 저장한다. 입력을 바꾼 뒤 불러와 저장한 값을 확인한다. 새로고침한 뒤에도 불러올 수 있어야 한다. 빈 문자열을 저장한 결과와 지운 뒤의 `null`을 비교한다.

### ex05 JSON 변환

JSON 저장을 누르면 객체 배열이 문자열로 저장된다. 저장 원문 조회로 `[{"name":"하늘",…}]`를 읽는다. JSON 복원을 눌러 이름·메시지 필드를 확인한다. `JSON.stringify`와 `JSON.parse`의 위치를 코드에서 찾는다.

### ex06 폼 복원과 캡처

이름과 메시지를 입력하고 저장한다. 새로고침하면 입력이 비어 있으므로 불러오기를 누른다. 입력과 JSON이 저장한 값으로 복원되면 된다.

지우기 후에는 다시 불러와도 저장 값이 없어야 한다. 확인을 마치면 캡처용으로 다시 입력·저장·새로고침·불러오기를 실행한다. 복원한 폼·JSON·주소창이 보이는 화면 한 장을 제출한다. localhost 화면을 인정한다. [실습과 제출](lab.md#제출--복원한-폼-캡처-한-장)

## 저장 범위 확인

Application › Local Storage에서 현재 origin을 선택하면 다음 키가 보인다.

| 예제 | 키 |
|---|---|
| ex04 | `week11-ex04-text` |
| ex05 | `week11-ex05-items` |
| ex06 | `week11-ex06-entry` |

같은 브라우저의 프로토콜·호스트·포트가 같으면 경로가 달라도 저장 공간을 공유한다. `localhost:8111`과 `localhost:8000`, `127.0.0.1:8111`, 공개 HTTPS 주소는 서로 다르다. `file://` 동작은 브라우저마다 다를 수 있으므로 저장 실습은 정적 서버에서 한다. [MDN localStorage](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)

## 수업 후 자료

공개 업로드와 개인 저장소 정리는 수업 후 필요에 따라 진행한다. [배열 심화](../../specials/array_advanced/README.md)는 별도 보강특강이며, [ex07 탭 동기화](examples/day2/README.md#고급-저장-참고)은 참고 자료다. 둘 다 이번 필수 실습에 포함하지 않는다.

## 부록: 강의자용 방명록 완성본

아래 완성본은 객체 배열의 저장·복원을 보여 주는 시연 자료다. **학생이 30분 실습에서 직접 완성할 대상이 아니다.** 12주차 시작 전에 [web-week11 폴더](examples/day2/web-week11/)를 준비 자료로 제공한다.

```text
http://localhost:8111/weeks/week11_object_localstorage/examples/day2/web-week11/guestbook.html
```

| 시연할 부분 | 동작 |
|---|---|
| 객체 배열 | 이름·메시지·날짜를 묶어 목록에 표시 |
| `saveList()` | 추가·한 줄 삭제 후 배열을 JSON으로 저장 |
| 초기 목록 | 저장 값을 파싱하고 없으면 빈 배열로 시작, 손상 값은 안내 |
| 전체 지우기 | 배열과 `week11-guestbook-items` 키만 비운 뒤 화면 갱신 |

손상 값 검사와 해당 키만 삭제하는 복구는 제공 코드다. 초기화 후에는 이름·메시지를 다시 입력하며 다른 예제 키는 유지한다.

기본 예제와 이 시연의 저장 키는 서로 다르다. 학생에게는 예제에서 배운 저장·파싱이 목록 전체에 적용되는 점을 설명한다. 공개 업로드나 추가 구현을 이번 제출 조건으로 붙이지 않는다.

### guestbook.html 전문

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
    <script src="guestbook.js" defer></script>
  </head>
  <body class="w3-light-grey">
    <header class="w3-container w3-teal w3-padding-16">
      <h1>방명록</h1>
    </header>
    <nav class="w3-bar w3-white w3-card" aria-label="주 메뉴">
      <a class="w3-bar-item w3-button w3-mobile" href="index.html">홈</a>
      <a class="w3-bar-item w3-button w3-mobile" href="about.html">내 정보</a>
      <a class="w3-bar-item w3-button w3-mobile w3-teal" href="guestbook.html" aria-current="page">방명록</a>
    </nav>
    <main class="w3-content w3-padding">
      <section class="w3-container w3-card w3-white w3-margin-top">
        <h2>한 줄 남기기</h2>
        <form id="guestbook-form">
          <p>
            <label for="name">이름</label>
            <input id="name" class="w3-input w3-border" type="text">
          </p>
          <p>
            <label for="message">메시지</label>
            <textarea id="message" class="w3-input w3-border" rows="4"></textarea>
          </p>
          <p><button class="w3-button w3-teal" type="submit">남기기</button></p>
        </form>
        <p id="notice" class="w3-text-red" aria-live="polite"></p>
      </section>
      <section class="w3-container w3-card w3-white w3-margin-top">
        <h2>남긴 글</h2>
        <ul id="list" class="w3-ul" aria-live="polite"></ul>
        <div id="count">아직 남긴 글이 없습니다.</div>
        <p><button class="w3-button w3-teal" id="clear-button" type="button">전체 지우기</button></p>
      </section>
    </main>
    <footer class="w3-container w3-center w3-text-grey w3-padding-16">
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

### guestbook.js 전문

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const count = document.querySelector('#count');
const clearButton = document.querySelector('#clear-button');
const storageKey = 'week11-guestbook-items';
let items = [];

// 제공 코드: 저장 값이 손상되어도 화면과 초기화 버튼은 사용할 수 있다.
function loadList() {
  try {
    const saved = localStorage.getItem(storageKey);
    if (saved === null) return;
    const restored = JSON.parse(saved);
    if (!Array.isArray(restored)) throw new Error('배열 형식 오류');
    for (let i = 0; i < restored.length; i++) {
      const item = restored[i];
      if (item === null || typeof item.name !== 'string' || typeof item.message !== 'string' || typeof item.date !== 'string') {
        throw new Error('필드 형식 오류');
      }
    }
    items = restored;
  } catch {
    notice.textContent = '저장 값을 불러올 수 없습니다. 전체 지우기를 눌러 이 방명록만 초기화하세요.';
  }
}

function saveList() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(items));
    notice.textContent = '';
    return true;
  } catch {
    notice.textContent = '저장하지 못했습니다. 브라우저 저장 권한이나 여유 공간을 확인하세요.';
    return false;
  }
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      const removed = items.splice(i, 1)[0];
      if (!saveList()) {
        items.splice(i, 0, removed);
        return;
      }
      showList();
    });
    li.append(removeButton);
    list.append(li);
  }
  if (items.length === 0) {
    count.textContent = '아직 남긴 글이 없습니다.';
  } else {
    count.textContent = `${items.length}개`;
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    nameInput.focus();
    return;
  }
  notice.textContent = '';
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
  if (!saveList()) {
    items.pop();
    return;
  }
  showList();
  form.reset();
  nameInput.focus();
});

clearButton.addEventListener('click', function () {
  try {
    localStorage.removeItem(storageKey);
    items = [];
    showList();
    notice.textContent = '이 방명록의 저장 값 삭제 완료';
  } catch {
    notice.textContent = '저장 값을 지울 수 없습니다. 브라우저 저장 권한을 확인하세요.';
  }
});

loadList();
showList();
```
