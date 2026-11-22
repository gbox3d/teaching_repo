# ex04 문자열 저장

## 실행

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

[실습 화면 열기](http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex04/)

화면 스타일은 [W3.CSS 4.1.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)에서 읽는다.

저장 키는 `week11-ex04-text`다. 실행에 외부 API나 별도 패키지는 필요 없다.

## 조작 순서

1. **저장할 문자열**에 문장을 입력하고 **저장**을 누른다. 결과에 입력한 문장과 `저장 완료`가 표시된다.
2. 입력 칸을 다른 문장으로 바꾸되 저장하지 않는다. **불러오기**를 누르면 저장했던 문장으로 복원된다.
3. 페이지를 새로고침하고 **불러오기**를 누른다. 새로고침은 저장값을 덮어쓰지 않는다.
4. **지우기**를 누른다. 이 예제의 키와 입력 칸이 비워진다.
5. **불러오기**를 누르면 결과는 `null`, 상태는 `저장된 값 없음`이다.

## 사용한 브라우저 API

```js
localStorage.setItem('week11-ex04-text', memoInput.value);
const saved = localStorage.getItem('week11-ex04-text');
localStorage.removeItem('week11-ex04-text');
```

`setItem`은 문자열을 저장하고, `getItem`은 문자열 또는 `null`을 반환한다.
`removeItem`은 지정한 키만 삭제한다. 다른 예제의 저장값은 유지한다.

## 확인할 차이

- 입력 칸을 비우고 저장하면 빈 문자열 `''`이 저장된다. 불러온 결과는 `"" (빈 문자열)`이다.
- 키를 지운 뒤 불러오면 `null`이다. 빈 문자열과 저장값이 없는 상태는 다르다.
- 브라우저가 저장을 허용하지 않으면 `저장 실패` 등의 상태가 표시된다.
- 저장값은 같은 브라우저의 같은 출처에서 공유된다. 주소의 프로토콜·호스트·포트를 바꾸면 다른 저장 공간이 된다.

입력은 `#memo`, 결과는 `#result`, 상태는 `#status`다. 동작 코드는 [app.js](app.js)에서 확인한다.
