[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_events)

# 6주차 따라하기

강의·시연 60분과 실습 30분을 구분한다. [실습지](lab.md)의 필수 변경만 수업 중 작성한다. 아래 완성 코드는 비교용이며 전부 타이핑하는 과제가 아니다.

## 사전 준비

지난주 개인 홈·소개·방명록·CSS·JS·이미지를 web-week06에 복사한다. 강의자는 [완성 폴더](examples/day2/web-week06/)와 [변경표](examples/README.md)를 사용해 홈의 두 버튼·횟수 카드·다크 CSS를 배부한다. 개인 소개와 이미지는 그대로 둔다. 비교 예제 여섯 폴더는 개인 ex/ex01~ex06에 준비한다. 파일 다운로드와 저장소·remote 설정은 수업 전에 마친다.

1차시용 ex03/app.start.js를 개인 ex03/app.js로 복사한다. 2차시용 web-week06/app.start.js를 개인 홈 app.js로 복사한다. 각 HTML은 app.js 하나만 연결한다. app.start.js를 script에 추가로 연결하지 않는다. 완성 예제는 교재에서 비교하고 개인 사본만 수정한다.

## 1일차

첫 5분에 파일과 서버 상태를 확인한다. 강의에서는 ex01의 현재 DOM과 원본 HTML을 비교하고, ex02의 click 시점과 ex03의 함수 밖 count를 설명한다. 오류 시연 뒤 원본을 복구한다.

실습 첫 5분은 btn·count ID 대조다. 다음 15분에 [실습지 여섯 줄](lab.md#1일차)을 작성한다. 마지막 10분에는 세 번 클릭해서 3회, 새로고침해서 0회를 확인한다. Elements의 textContent는 바뀌어도 페이지 소스의 원래 HTML은 그대로다. Elements에서 임시로 바꾼 글자 역시 새로고침하면 사라진다.

## 2일차

첫 5분에 제공 홈이 열리는지 확인한다. 강의에서는 ex04의 add·remove·toggle, ex05의 다크 CSS, ex06의 공유 countUp을 시연한다. 두 리스너의 틀과 기존 greet·hello는 제공한다.

실습 첫 5분에 배경 #222222를 #202938로, 글자 #eeeeee를 #f5f7ff로 바꾼다. 다음 10분에 인사 리스너의 countUp 한 줄, 다크 리스너의 toggle·countUp 두 줄을 넣는다. 다음 10분에 두 버튼과 두 화면 폭을 확인하고 마지막 5분에 캡처한다.

body.dark의 color는 상속값이다. h1·h2·nav a·footer가 자기 color를 갖고 있으면 그 색이 먼저 쓰이므로 어두운 모드에서도 해당 선택자의 color를 지정한다. 제공 CSS는 제목·메뉴 #a7c5ff, 푸터 #c8d4eb를 사용한다. 버튼·횟수 카드만 보지 말고 제목·메뉴·푸터도 함께 확인한다.

## 완성 index.html

다음은 제공 HTML 전체다. 지난주 #greeting 아래에 버튼 두 개와 #count가 추가되었다. 개인 본문은 유지한다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
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
      <div class="card" id="greeting">인사말을 준비 중입니다.</div>
      <div>
        <button id="hello-button" type="button">인사 바꾸기</button>
        <button id="dark-button" type="button">다크 모드</button>
      </div>
      <div class="card" id="count">클릭 0회</div>
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

실제 파일: [index.html](examples/day2/web-week06/index.html).

## 완성 styles.css

다음은 제공 CSS 전체다. 실습에서는 다크 배경·글자 두 값을 바꾼다. 5주 CSS에 body.dark 규칙들을 추가했으며 W3.CSS는 다음 주에 도입한다.

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

body.dark,
body.dark .card {
  background-color: #222222;
  color: #eeeeee;
}

body.dark h1,
body.dark h2,
body.dark nav a {
  color: #a7c5ff;
}

body.dark footer {
  color: #c8d4eb;
}
```

실제 파일: [styles.css](examples/day2/web-week06/styles.css).

## 완성 app.js

다음은 세 TODO를 연결한 전체 결과다. 5주 greet·hello는 유지하고 countUp은 두 버튼이 공유한다. name과 hour의 수업용 값 변경 외에 함수 전체를 다시 쓰지 않는다.

```js
const name = 'student01';
const hour = new Date().getHours();
const greeting = document.querySelector('#greeting');
const countBox = document.querySelector('#count');
const helloButton = document.querySelector('#hello-button');
const darkButton = document.querySelector('#dark-button');
let count = 0;

function greet(name) {
  return `안녕하세요, ${name}님!`;
}

function hello(hour) {
  if (hour >= 12) {
    return '좋은 오후입니다.';
  } else {
    return '좋은 아침입니다.';
  }
}

function countUp() {
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
}

greeting.textContent = `${greet(name)} ${hello(hour)}`;

helloButton.addEventListener('click', function () {
  greeting.textContent = '반갑습니다. 오늘도 좋은 하루 되세요.';
  countUp();
});

darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
  countUp();
});
```

실제 파일: [app.js](examples/day2/web-week06/app.js).

## 화면과 초기화 확인

인사·다크·인사 순서로 클릭하면 3회이고 어두운 화면이다. 다크 버튼을 한 번 더 누르면 밝은 화면과 4회다. 새로고침하면 초기 인사·0회·밝은 화면이 된다. 두 버튼을 반복해도 한 번 클릭에 한 번만 증가해야 한다.

Chrome의 기기 툴바에서 375px와 1280px로 확인한다. 좁은 폭의 메뉴는 세로이고, 가로 스크롤 없이 글자·버튼을 읽을 수 있어야 한다. 홈·소개·방명록 링크를 왕복한다. 방명록은 입력 연습용이며 아직 저장하지 않는다. 잘못된 이메일은 브라우저가 제출을 막고, 유효한 입력은 같은 페이지에 기본 GET 탐색을 한다. name 속성이 없으므로 입력 내용이 URL에 실리지 않으며 목록이나 저장소에도 남지 않는다.

localhost를 쓰면 미리 준비한 [server.mjs](../../tools/static-server/server.mjs)를 개인 web-week06 폴더에서 실행한다.

```bash
node server.mjs
```

`http://localhost:8000/`에서 확인한 뒤 Ctrl+C로 종료한다. 서버가 없는 PC는 파일 주소로 확인한다. 수업 뒤 업로드·공개 주소 확인은 [실습지](lab.md#수업-뒤-업로드)를 따른다.
