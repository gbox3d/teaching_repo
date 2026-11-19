# 5주차 따라하기

각 차시는 강의·시연 60분과 실습 30분이다. 실습 중에는 아래의 지정한 수정만 한다. 비교 예제의 나머지 실험은 강의자 시연 또는 선택 연습이다.

## 수업 전 준비

4주 완성 폴더를 새 `web-week05`에 준비한다. 비교 예제는 `ex/ex01`~`ex/ex10`으로 배부한다. 새 저장소·Pages 설정과 Node.js 24 이상 설치·server.mjs 배치는 사전 작업이다. Git 설명은 2주 자료를 참고한다.

2일차용 홈에는 script와 greeting 카드가 들어 있고, 맨 위 app.js는 [시작 파일](examples/day2/start/app.js)이다. 기존 2주 카운터 코드를 이어 붙이지 않는다. 강의자는 [시작 안내](examples/day2/start/README.md)대로 준비한다.

현재 폴더가 `web-week05`일 때 실행한다.

```bash
node server.mjs
```

`http://localhost:8000/`과 `http://localhost:8000/ex/ex03/`가 열리는지 확인한다. 서버 실행 환경이 빠졌으면 HTML 직접 열기로 이번 주 결과를 확인하고 다음 차시 전에 환경을 복구한다.

## 1일차

[실습지](lab.md#1일차-30분-실습)의 30분 순서를 따른다. `ex/ex03/app.js`에서 a를 10, b를 20으로 바꾼다. `ex/ex05/app.js`에서 name을 student02, hour를 15로 바꾼다. 수정은 값 4곳이다.

저장·새로고침 후 ex03의 let 버튼을 누르면 11이다. ex05 출력 버튼은 `안녕하세요, student02님! 지금은 15시입니다.`를 표시한다. 출력 버튼의 JavaScript는 제공 코드다.

ex03의 const 버튼을 누르면 Console에 `Assignment to constant variable.`이 생기고 화면의 값은 20에 머문다. `const b`를 `let b`로 수정하고 저장·새로고침한 뒤 다시 누르면 21이다. 오류는 클릭으로 재대입하는 순간 발생한다. 빨간 줄의 실제 파일·줄 번호를 읽고 그 코드를 확인한다.

## 2일차

[실습지](lab.md#2일차-30분-실습)의 30분 순서를 따른다. 수정 대상은 ex 폴더가 아닌 맨 위 `web-week05/app.js`다.

| 수정 위치 | 시작 상태 | 바꿀 내용 |
|---|---|---|
| greet의 return | 이름 연결 전 | 백틱 문자열에 `${name}` 연결 |
| hello의 if | hour >= 24 | hour >= 12 |
| 마지막 출력 | 출력 연결 전 | message |

HTML과 함수의 나머지 구조·현재 시각 식·message 조합·로그는 제공한다. 학생이 전체 파일을 지우고 다시 작성하지 않는다. 완성 코드는 아래와 같다.

## 완성 app.js

[실제 완성 파일](examples/day2/web-week05/app.js)과 같은 전문이다.

```js
const name = 'student01';
const hour = new Date().getHours();

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

const message = `${greet(name)} ${hello(hour)}`;

console.log(hour);
console.log(message);

document.querySelector('#greeting').textContent = message;
```

`greet`와 `hello`는 정의할 때 실행되지 않고 message 줄에서 호출된다. 두 반환 문자열을 연결한 뒤 마지막 줄이 화면을 바꾼다. 날짜 식은 파일이 실행된 순간의 시각을 읽는다.

hour를 임시로 9로 바꾸면 아침, 15로 바꾸면 오후다. 확인한 뒤 `new Date().getHours()`로 되돌린다. `hour >= 12`이므로 12시도 오후다.

## 완성 index.html

[실제 홈](examples/day2/web-week05/index.html)과 같은 전문이다. 4주 홈에 추가한 script·greeting 두 줄은 사전 제공된다.

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

`about.html`·`guestbook.html`·`styles.css`·그림은 4주 파일 그대로다. 홈에서 세 페이지를 왕복하고 375px에서는 메뉴가 세로, 1280px에서는 가로인지 확인한다. 입력 연습용 방명록은 메시지를 저장하지 않는다.

## 실행 확인과 제출

localhost에서 인사말 카드와 Console 두 줄을 확인한다. 서버 터미널에는 HTML·CSS·JS·그림 요청이 각각 남는다. 없는 파일을 요청하면 404이며 favicon.ico 요청은 브라우저에 따라 없을 수도 있다. 요청 순서와 개수를 고정된 정답으로 삼지 않는다.

주소창·카드·Console 두 줄이 보이는 캡처 1장을 수업 시간에 만든다. 수업 뒤 10분 이내 정리로 기존 업로드 순서를 수행하고 `https://student01.github.io/web-week05/`에서 확인한다. 업로드가 지연되면 localhost 결과로 완료하고 다음 차시 첫 확인 시간에 공개 주소를 점검한다. 증상별 복구는 [실습지](lab.md#막혔을-때)를 따른다.
