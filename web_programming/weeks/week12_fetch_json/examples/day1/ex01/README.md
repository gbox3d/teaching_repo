# ex01 · Promise 실행 순서

[화면](index.html)에서 **타이머 시작**을 누른다. ‘타이머 시작’과 ‘다음 줄 실행’이 먼저 나오고, 약 1초 뒤에 ‘타이머 완료’가 붙는다.

[app.js](app.js)에서 `setTimeout`이 기다릴 시간을 1000에서 3000으로 바꾼다. 세 번째 줄만 늦어진다. `resolve(message)`로 넘긴 문자열은 `then`에 등록한 함수의 인자로 들어간다.

다음 [ex01b](../ex01b_wait/README.md)에서는 Promise를 돌려주는 `wait` 함수로 1초씩 두 번 기다린다.
