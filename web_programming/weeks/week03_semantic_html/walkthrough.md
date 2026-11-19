# 3주차 따라하기 — 제공 HTML 수정과 결과 확인

각 차시의 필수 실습은 30분이다. 파일 배부와 `my-web` 준비는 수업 전에 끝낸다. 아래 전체 코드는 강의자 시연·복습·오류 비교에 쓰며, 학생이 수업 시간에 모두 다시 입력할 분량은 아니다. 실제 수정량은 [실습지](lab.md)의 시간표를 따른다.

`student01`은 수업용 별칭이다. 공개 주소에서는 본인 GitHub 아이디를 사용하고 개인정보는 넣지 않는다. 이번 주에는 CSS·JavaScript를 작성하지 않는다.

## 사전 준비

2주차에 배운 절차로 `my-web`을 열고 `main`을 준비한다. 같은 PC는 수업 전에 `git pull`, 처음 쓰는 PC는 `git clone https://github.com/<아이디>/my-web.git`을 사용한다. 다운로드나 계정 문제가 있으면 배부 파일로 로컬 실습부터 진행하고 수업 뒤 정리한다. 초기화하지 않은 폴더에서 `remote add`만 해서는 push할 수 없으므로 저장소 복구는 2주차 절차를 따른다.

강의자는 `examples/day1`·`day2`를 미리 배부한다. 1차시에는 day1 홈·그림을 준비하고 지난주 소개·CSS·JS를 보존한다. 2차시에는 day2 소개·방명록과 홈 메뉴의 방명록 링크를 준비한다. 자신이 수정한 홈 전체를 참고본으로 덮어쓰지 않는다.

## 1차시

### 1. 제공 홈 열기 (5분)

`my-web/index.html`을 브라우저로 연다. 제공 홈에는 `header`·`nav`·`main`·`footer`가 들어 있다. `header` 안의 `nav`는 메뉴 링크를 담는다. 홈에는 아래 두 연결 줄이 없다. 연결을 해제하는 과정은 강의자가 시연한다.

```html
<link rel="stylesheet" href="styles.css">
<script src="app.js" defer></script>
```

파일 자체는 보존한다. 홈이 꾸며지지 않은 화면이고, 내 정보는 지난주 카드 모양인 상태가 맞다.

### 2. 제목·문단·alt·취미 바꾸기 (15분)

`h1`과 문단의 별칭을 고치고 취미 목록을 자신의 내용으로 바꾼다. `alt`는 제공 그림의 내용을 설명한다. `images/profile.png`는 수업 전에 준비한 파일이므로 수업 중 다운로드하지 않는다.

```html
<h1>student01의 웹 연습장</h1>
<p>웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
<img src="images/profile.png" alt="student01의 프로필 그림" width="160">
```

저장하고 새로고침하면 바꾼 글과 160px 너비의 그림이 보인다. `h1`은 페이지 제목, `h2`는 소개·취미의 제목이다. `h3`는 그 안에 작은 묶음이 있을 때 쓰며 글자 크기만으로 선택하지 않는다.

### 3. 링크 점검과 확인 (10분)

홈 메뉴의 `index.html`·`about.html`을 누르고 소개의 돌아가기 링크로 돌아온다(5분). 이어 홈의 제목·문단·그림·취미 목록을 확인한다(5분). 그림이 깨지면 `images/profile.png`의 경로와 철자를 대조한다.

### 4. 1차시 홈 전체 코드 (시연·복습)

[day1/index.html](examples/day1/index.html)의 원문이다. 학생 결과의 별칭·문구·alt·취미는 달라도 된다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
  </head>
  <body>
    <header>
      <h1>student01의 웹 연습장</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
      </nav>
    </header>
    <main>
      <h2>소개</h2>
      <img src="images/profile.png" alt="student01의 프로필 그림" width="160">
      <p>웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p>이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
      <h2>취미</h2>
      <ul>
        <li>사진 찍기</li>
        <li>보드게임</li>
        <li>저녁 산책</li>
      </ul>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

### 5. 보존 파일 전체 코드 (제공)

[day1/about.html](examples/day1/about.html)은 2주차 소개를 유지한다. CSS가 이 파일에만 연결되어 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 소개</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <main class="card">
      <p class="eyebrow">Week 02 · about 브랜치</p>
      <h1>소개</h1>
      <p>student01의 웹프로그래밍 연습 페이지입니다.</p>
      <p><a href="index.html">첫 페이지로 돌아가기</a></p>
    </main>
  </body>
</html>
```

[day1/styles.css](examples/day1/styles.css)는 2주차 완료본과 같다. 좁은 화면 폭 보정도 제공 코드에 포함하며 이번 주에 CSS 작성 과제를 추가하지 않는다. day2의 CSS도 같은 파일이다.

```css
body {
  min-height: 100vh;
  margin: 0;
  display: grid;
  place-items: center;
  font-family: system-ui, sans-serif;
  color: #17213a;
  background: #eef2ff;
}

.card {
  box-sizing: border-box;
  width: min(36rem, calc(100% - 2rem));
  padding: 2rem;
  border-radius: 1rem;
  background: white;
  box-shadow: 0 1rem 2.5rem rgb(30 50 100 / 12%);
}

h1 {
  word-break: keep-all;
}

.eyebrow {
  color: #3157d5;
  font-weight: 700;
}

button {
  padding: 0.7rem 1rem;
  border: 0;
  border-radius: 0.5rem;
  color: white;
  background: #3157d5;
}
```

[day1/app.js](examples/day1/app.js)도 보존 파일이며 day2와 같다. 3주차의 어떤 HTML에도 연결하지 않는다. 이 코드의 버튼 ID가 3주차 화면에 없으므로 연결하면 오류가 난다. 5주차에는 새 JavaScript 시작 틀을 사용한다.

```js
const countButton = document.querySelector('#count-button');
const status = document.querySelector('#status');

let clickCount = 0;

countButton.addEventListener('click', () => {
  clickCount += 1;
  status.textContent = `클릭 횟수: ${clickCount}`;
});

console.info('my-web ready');
```

## 2차시

### 6. 표 두 행 바꾸기 (5분)

제공 `about.html`에서 아이디·관심 분야의 `td` 내용 두 곳을 바꾼다. `th` 두 칸의 제목 행과 가상 이메일 행은 유지한다. `table`에 `tr`이 네 개, 각 행에 칸이 두 개여야 한다. 표의 선은 4주차에 CSS로 만든다.

[day2/about.html](examples/day2/about.html)의 전체 원문은 다음과 같다. 이 뼈대 전체 조립은 강의자 시연이다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
  </head>
  <body>
    <header>
      <h1>내 정보</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <h2>한눈에 보기</h2>
      <p>수업용 가상 정보입니다.</p>
      <table>
        <tr>
          <th>항목</th>
          <th>내용</th>
        </tr>
        <tr>
          <td>아이디</td>
          <td>student01</td>
        </tr>
        <tr>
          <td>이메일</td>
          <td>student01@example.com</td>
        </tr>
        <tr>
          <td>관심 분야</td>
          <td>웹 페이지 만들기</td>
        </tr>
      </table>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

### 7. label과 입력 연결 (15분)

제공 `guestbook.html`의 `label for` 값 세 개만 잠시 비운다. 이름표를 눌러 입력으로 이동하지 않는 것을 확인한 뒤 `name`·`email`·`message`를 다시 적는다. 각 입력의 `id`와 같은지 대조하고 세 이름표를 다시 눌러 본다. 이제 해당 입력으로 포커스가 이동해야 한다.

이름은 `type="text"`, 이메일은 `type="email"`, 메시지는 `textarea`다. 이메일에 `abc`를 넣고 남기기를 누르면 브라우저가 제출을 막는다. 이메일을 비우거나 `student01@example.com`으로 바꿔 다시 누르면 현재 페이지를 다시 열며 입력이 초기화된다. 주소 끝에 `?`가 붙을 수 있다. 글 추가·저장은 하지 않는다.

`required`가 없어 빈 입력은 허용된다. `action`·`method`가 없으면 현재 주소로 GET 제출하며 입력에 `name` 속성이 없어 입력값이 쿼리에 담기지 않는다. 이것은 HTML 기본 동작이며 JavaScript 동작 구현은 이번 주 범위가 아니다.

[day2/guestbook.html](examples/day2/guestbook.html)의 전체 원문이다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
  </head>
  <body>
    <header>
      <h1>방명록</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <h2>한 줄 남기기</h2>
      <form>
        <p>
          <label for="name">이름</label>
          <input id="name" type="text">
        </p>
        <p>
          <label for="email">이메일</label>
          <input id="email" type="email">
        </p>
        <p>
          <label for="message">메시지</label>
          <textarea id="message" rows="4"></textarea>
        </p>
        <button type="submit">남기기</button>
      </form>
      <p>입력 연습용입니다. 메시지는 저장되지 않습니다.</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

### 8. 세 페이지 이동 (5분)

홈의 기존 자기소개 내용은 유지하고 메뉴에 아래 한 줄만 더한 상태에서 시작한다. 소개와 방명록에는 이미 같은 메뉴가 제공되어 있다.

```html
<a href="guestbook.html">방명록</a>
```

세 페이지에서 각각 홈·내 정보·방명록을 눌러 아홉 경로를 확인한다. 열리지 않으면 파일 이름과 링크의 철자·대소문자를 비교한다. [day2/index.html](examples/day2/index.html)의 전체 원문은 다음과 같다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
  </head>
  <body>
    <header>
      <h1>student01의 웹 연습장</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <h2>소개</h2>
      <img src="images/profile.png" alt="student01의 프로필 그림" width="160">
      <p>웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p>이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
      <h2>취미</h2>
      <ul>
        <li>사진 찍기</li>
        <li>보드게임</li>
        <li>저녁 산책</li>
      </ul>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

### 9. 캡처 제출 (5분)

로컬 `guestbook.html`에서 메뉴·세 입력 칸·남기기 버튼과 주소창이 보이게 한 장을 캡처한다. 로컬 파일 주소 또는 수업용 로컬 서버 주소로 제출해도 된다. 공개 업로드를 기다리느라 캡처를 늦추지 않는다.

## 선택 연습

취미 `ul`을 `ol`로 바꿔 번호를 관찰하거나, 내 정보 표에 가상 정보 한 행을 추가한다. 정규 필수 결과를 확인한 뒤 진행한다. 방명록 입력 순서는 이름 입력 → 이메일 형식 확인 → 메시지 입력 → 남기기이며, 이 절차와 HTML 설명은 README에서 읽는다.

## 수업 뒤 업로드

현재 폴더는 `my-web`, 브랜치는 `main`이다. 2주차에 배운 반복 작업으로 업로드한다.

```bash
git add .
git commit -m "3주 HTML 실습"
git push
```

변경 파일 수와 commit 해시는 수정 내용마다 달라진다. `nothing to commit, working tree clean`은 이미 commit했거나 저장된 변경이 없다는 뜻이다. VS Code의 미저장 표시와 `git status`를 확인한다. 공개 주소 `https://<아이디>.github.io/my-web/guestbook.html`에서 확인한다. 공개 반영·계정 문제는 다음 차시 첫 5분에 확인하며 로컬 캡처는 인정한다.

## 4주차 준비

완성한 세 HTML·`images/`·보존 CSS·JS를 새 `web-week04` 폴더로 복사한다. `.git`은 복사하지 않는다. 다음 주 저장소 준비와 파일 배부는 수업 전에 끝낸다. CSS는 4주차 시작 틀로 교체해 연결하며, 공개 결과 주소는 `https://<아이디>.github.io/web-week04/`다. `my-web`은 3주차 결과로 남긴다.
