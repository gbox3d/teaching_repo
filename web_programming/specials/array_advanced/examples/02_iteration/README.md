# 배열 순회

## 실행

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

[실습 화면 열기](http://localhost:8111/specials/array_advanced/examples/02_iteration/)

이 예제는 [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용하므로 인터넷 연결이 필요하다.
[공용 추가 스타일](../../../../shared/README.md)인 `web_programming/shared/examples.css`를 함께 준비하고 예제와의 상대 위치를 유지한다.

같은 객체 배열을 `for...of`와 `forEach`로 순회한다.
두 버튼은 이름·점수 목록을 표시하고 실행 후 원본 배열도 보여 준다.

## 조작 순서

1. **for...of 실행**을 누른다. 결과는 `하늘: 80점`, `바다: 60점`, `노을: 90점`이다.
2. 반환값 칸의 `해당 없음 (반복문)`을 확인한다. `for...of`는 메서드 호출이 아니라 반복문이다.
3. **forEach 실행**을 누른다. 같은 세 항목과 반환값 `undefined`를 확인한다.
4. 버튼을 여러 번 누른다. 이전 결과를 비운 뒤 표시하므로 목록은 항상 세 항목이다.
5. 실행 전후 원본을 비교한다. 이 예제는 객체를 읽기만 하므로 이름·점수가 바뀌지 않는다.

## 순회 코드 비교

```js
for (const student of students) {
    console.log(student.name, student.score);
}

const result = students.forEach(function (student) {
    console.log(student.name, student.score);
});
// result는 undefined다.
```

실제 [app.js](app.js)는 `console.log` 대신 `li`를 만들고 `textContent`로 이름·점수를 표시한다.
`forEach`는 각 항목마다 콜백 함수를 호출하며, 메서드의 반환값은 `undefined`다. 새 배열을 반환하지 않는다.
두 방식 모두 반복 중 객체의 값을 직접 대입하면 원본 객체를 바꿀 수 있다. 이 예제에는 그런 대입이 없다.

버튼은 `#for-of`·`#for-each`, 결과는 `#result-list`·`#return-output`·`#after-json`이다.
새로고침하면 순회 전 화면으로 돌아간다. 외부 API나 저장소를 사용하지 않는다.
