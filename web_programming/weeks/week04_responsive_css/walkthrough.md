# 4주차 따라하기 — 제공 CSS의 값 변경

각 차시는 강의·시연 60분과 학생 실습 30분이다. 아래 필수 순서만 실습 시간에 수행한다. 전문 재입력·전체 조립·다른 비교값 변경은 시연·복습용이다. 비교 예제 13개와 선택 부록 ex14는 모두 보존한다.

## 수업 전 준비

3주차 `my-web` 결과를 `.git` 없이 새 `web-week04`에 복사한다. 저장소·Pages 설정과 비교 폴더 `ex/ex01`~`ex/ex14` 배부를 마친다. 강의자는 [제공 완성본](examples/day2/web-week04/)의 CSS 연결·카드 클래스를 반영하되 학생 소개·취미를 보존한다. 파일이 없는 학생은 제공본으로 시작한다. 파일별 Raw 다운로드와 Git 신규 설명은 수업 안에서 하지 않는다.

## 1일차

강의 첫 5분에 파일과 실행 상태를 확인한다. 선택자 15분, 박스모델 15분, max-width·margin 15분, 다른 비교 5분, 실습 안내 5분으로 강의·시연 60분을 구성한다.

1. 실습 0–10분: `ex/ex01/styles.css`의 `.red` 색을 `orange`로, `ex/ex03/styles.css`의 `.pad`를 `32px`로 바꾼다. ex01 2·3번 색과 ex03 2·5번 안쪽 여백이 바뀐다.
2. 10–25분: 사이트 `styles.css`의 `h1 color`를 `#365314`, `.card padding`을 `20px`, `body max-width`를 `600px`로 바꾼다. 제공 CSS의 세 값만 편집한다.
3. 25–30분: 저장·새로고침 후 제목 색·카드 여백·본문 폭과 세 페이지 CSS 연결을 확인한다. ex02·ex04·ex05·ex06은 강의자 시연이며 추가 실험은 선택이다.

DevTools에서 바꾼 값은 새로고침하면 사라진다. 제출할 변화는 파일에 저장한다. CSS 오류는 JavaScript 예외처럼 멈추지 않으므로 Elements·Styles에서 적용된 규칙과 무시된 선언을 살핀다.

## 2일차

강의 첫 5분에 준비를 확인한다. flex 부모·축 20분, gap·정렬 10분, media 15분, 전체 조립 시연 5분, 실습 안내 5분이다.

1. 실습 0–10분: `ex/ex07/styles.css`의 `.column`을 `flex-direction: row`로 바꿔 4번의 가로 배치를 본다. `ex/ex08/styles.css`의 `.center`를 `justify-content: flex-end`로 바꿔 2번 오른쪽 정렬을 본다.
2. 10–22분: 사이트 `nav gap`을 `24px`, media 경계를 `700px`로 바꾼다. media 안의 방향을 `row`로 비교한 뒤 `column`으로 복원한다. 기존 3줄(5줄 이내)만 수정한다.
3. 22–30분: Chrome 기기 모드에서 1280px·375px로 세 페이지를 확인한다. 메뉴는 가로·세로로 바뀌고 가로 넘침이 없다. 375px 홈 화면을 캡처한다. 파일 주소 또는 localhost로 완료할 수 있다.

완성 예시의 경계 600px과 실습의 700px은 375/1280px에서 같은 최종 메뉴 방향을 보인다. ex09~ex13 추가 실험과 ex14는 [예제 안내](examples/README.md)를 참고한다.

## 조립 시연과 전문

이하 코드는 제공 완성본 그대로이며 학생 변경값을 적용하기 전이다. 3주차 HTML에 CSS 링크 한 줄씩, 홈의 카드 클래스 세 곳을 더한 구조다. 이를 빈 파일부터 다시 입력하는 활동은 필수가 아니다.

| 규칙 | 비교 예제 |
|---|---|
| 색·선택자 | ex01 |
| padding·border·margin | ex03 |
| max-width·가운데 정렬 | ex04·ex05 |
| footer text-align | ex06 |
| nav의 flex·gap·wrap | ex07·ex11·ex10 |
| media 안 column | ex13·ex07 |

`h1`의 `word-break: keep-all`과 입력의 `box-sizing: border-box`는 제공하는 줄바꿈·폭 보정이다. 입력의 280px은 테두리까지 포함한다. 모든 완성본은 자체 CSS를 쓰고 W3.CSS는 7주에 도입한다.

### styles.css 전문

[실행 파일](examples/day2/web-week04/styles.css)과 같은 내용이다.

```css
body {
  background-color: #eef2ff;
  color: #17213a;
  font-family: system-ui, sans-serif;
  font-size: 16px;
  max-width: 640px;
  margin: 0 auto;
  padding: 16px;
}

h1 {
  color: #1f3a93;
  font-size: 28px;
  word-break: keep-all;
}

h2 {
  color: #3157d5;
}

nav {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

nav a {
  color: #3157d5;
}

.card {
  background-color: #ffffff;
  padding: 16px;
  margin: 12px 0;
  border: 1px solid #c3cbe6;
}

input,
textarea {
  box-sizing: border-box;
  width: 280px;
  max-width: 100%;
}

footer {
  color: #5a6478;
  text-align: center;
  font-size: 14px;
}

@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}
```

### index.html 전문

[실행 파일](examples/day2/web-week04/index.html)과 같은 내용이다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
    <link rel="stylesheet" href="styles.css">
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
      <p class="card">웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p class="card">이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
      <h2>취미</h2>
      <ul class="card">
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

### about.html 전문

[실행 파일](examples/day2/web-week04/about.html)과 같은 내용이다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
    <link rel="stylesheet" href="styles.css">
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

### guestbook.html 전문

[실행 파일](examples/day2/web-week04/guestbook.html)과 같은 내용이다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
    <link rel="stylesheet" href="styles.css">
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

### app.js 전문

[실행 파일](examples/day2/web-week04/app.js)과 같은 내용이다.

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

`app.js`는 보존 파일이다. 세 HTML에 script 줄이 없어 실행되지 않는다. 5주차에 다시 작성한다. `images/profile.png`는 3주차와 같은 그림이며 alt도 유지한다.

## 폼과 이동 확인

홈·내 정보·방명록 메뉴를 왕복한다. 방명록 label 세 개를 클릭해 해당 입력의 포커스를 확인한다. 이메일 `abc`는 브라우저가 제출을 막는다. 빈 이메일 또는 `student01@example.com`은 기본 GET으로 현재 문서를 다시 열고 입력은 초기화된다. 글 추가·저장 기능은 없다.

## 수업 뒤 업로드

준비한 저장소에 2주차의 저장·commit·push 순서로 업로드하고 Pages를 확인한다. 공개 주소는 `https://student01.github.io/web-week04/`이며 아이디를 본인 것으로 바꾼다. 업로드 문제는 로컬 캡처와 commit 기록을 남기고 다음 수업 첫 5분에 확인한다. 5주차 `web-week05` 준비 때는 `.git` 없이 결과 파일을 복사한다.
