# ex05 JSON 저장과 복원

## 실행

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

[실습 화면 열기](http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex05/)

이 예제는 [W3.CSS CDN 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)과 [추가 공용 스타일](../../../../../shared/README.md)의 `shared/examples.css`를 사용한다. CDN 스타일을 읽으려면 인터넷 연결이 필요하다. 예제와 `web_programming/shared/`의 상대 위치를 유지한다.

저장 키는 `week11-ex05-items`다. 화면의 고정 배열은 이름과 메시지를 가진 객체 두 개다.

## 조작 순서

1. **JSON 저장**을 누른다. 배열을 `JSON.stringify`로 문자열로 바꿔 저장한다.
2. **저장 원문 조회**를 누른다. `getItem`으로 읽은 문자열이 **저장 원문**에 표시된다.
3. **JSON 복원**을 누른다. `JSON.parse`로 복원한 객체의 이름·메시지와 `복원 완료: 2개`를 확인한다.
4. 페이지를 새로고침하고 **저장 원문 조회**, **JSON 복원**을 누른다. 저장 버튼을 다시 누르지 않아도 이전 값이 남아 있다.
5. **지우기**를 누른 뒤 **JSON 복원**을 누른다. 원문은 `null`, 상태는 `저장된 값 없음`이다.

## 사용한 브라우저 API

```js
const text = JSON.stringify(items);
localStorage.setItem('week11-ex05-items', text);
const saved = localStorage.getItem('week11-ex05-items');
if (saved !== null) {
    const restored = JSON.parse(saved);
}
```

저장 칸에는 배열 대신 문자열이 들어간다. 복원 후에 `restored[0].name`처럼 객체 필드를 읽을 수 있다.
화면을 열 때는 배열을 화면에만 표시한다. 저장값은 버튼을 눌렀을 때만 바꾼다.

오류 처리와 형식 검사는 제공 코드다. 학생은 저장·복원 결과를 확인하며 이 부분을 다시 작성하지 않는다.

## 빈 값과 JSON 오류 확인

개발자 도구 Console에서 아래 코드를 실행한 뒤 **저장 원문 조회**, **JSON 복원**을 누른다.

```js
localStorage.setItem('week11-ex05-items', '');
```

빈 문자열은 존재하는 저장값이지만 JSON 문법에는 맞지 않는다. 원문은 `"" (빈 문자열)`, 상태는 `JSON 복원 실패`다.
`'{'`처럼 손상된 JSON도 같은 상태가 된다. `'[null]'`처럼 문법만 맞고 필드가 없는 값은 `배열과 필드 형식 확인 필요`로 구분한다.
**JSON 저장**을 누르면 고정 배열로 다시 저장할 수 있다.

**지우기**는 `removeItem('week11-ex05-items')`만 실행한다. 다른 예제의 키는 삭제하지 않는다.
결과는 `#stored-json`과 `#restored-items`에 표시한다. 동작 코드는 [app.js](app.js)에서 확인한다.
