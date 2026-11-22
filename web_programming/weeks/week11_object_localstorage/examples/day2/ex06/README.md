# ex06 입력 폼 저장과 복원

## 실행

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

[실습 화면 열기](http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex06/)

화면 스타일은 [W3.CSS 4.1.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)에서 읽는다.

저장 키는 `week11-ex06-entry`다. 이름·메시지 입력값을 객체 하나로 묶어 저장한다.

## 조작 순서

1. 이름과 메시지를 입력하고 **저장**을 누른다. 저장한 JSON과 `저장 완료`를 확인한다.
2. 입력값을 다른 내용으로 바꾸되 저장하지 않는다. **불러오기**를 누르면 저장된 값으로 폼이 복원된다.
3. 페이지를 새로고침하고 **불러오기**를 누른다. 이름과 메시지가 복원되고 `폼 복원 완료`가 표시된다.
4. **지우기**를 누르면 이 예제의 키와 입력 칸이 비워진다.
5. 다시 **불러오기**를 누르면 `null`과 `저장된 값 없음`이 표시된다.

## 입력값을 저장하고 복원하는 코드

```js
const entry = { name: nameInput.value, message: messageInput.value };
localStorage.setItem('week11-ex06-entry', JSON.stringify(entry));
const text = localStorage.getItem('week11-ex06-entry');
if (text !== null) {
    const saved = JSON.parse(text);
    nameInput.value = saved.name;
    messageInput.value = saved.message;
}
```

실제 [app.js](app.js)는 복원할 값이 객체이며 이름·메시지가 문자열인지 검사하고, 저장·파싱 실패를 상태에 표시한다.
새로고침 때 저장값을 덮어쓰지 않는다. **지우기**는 `removeItem('week11-ex06-entry')`만 실행한다.

오류 처리와 형식 검사는 제공 코드다. 학생은 저장·복원 결과를 확인하며 이 부분을 다시 작성하지 않는다.

## 빈 입력과 JSON 오류 확인

- 이름과 메시지를 모두 비워도 저장할 수 있다. 저장값은 `{"name":"","message":""}`이며 불러오기는 성공한다.
- 저장 키가 없을 때의 `null`은 위 객체와 다르다. 불러오기 실패나 저장값 없음일 때 현재 입력값은 유지한다.
- 개발자 도구 Console에서 아래 코드를 실행한 뒤 **불러오기**를 누르면 `JSON 불러오기 실패`가 표시된다.

```js
localStorage.setItem('week11-ex06-entry', '');
```

원문은 `"" (빈 문자열)`로 표시된다. `'{'`도 JSON 파싱에 실패한다.
`'null'`이나 `'[]'`는 JSON 문법에는 맞지만 필요한 객체가 아니므로 `이름·메시지 형식 확인 필요`가 표시된다.
이름·메시지를 입력하고 **저장**을 누르면 정상 값으로 다시 저장할 수 있다.

폼은 `#entry-form`, 입력 칸은 `#name`·`#message`, 결과는 `#stored-json`, 상태는 `#status`다.
