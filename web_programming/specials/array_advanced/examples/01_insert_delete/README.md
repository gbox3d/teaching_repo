# 배열 삽입과 삭제

## 실행

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

[실습 화면 열기](http://localhost:8111/specials/array_advanced/examples/01_insert_delete/)

이 예제는 [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용하므로 인터넷 연결이 필요하다.

배열은 메모리에만 있으며 새로고침하면 초기값으로 돌아간다.
버튼을 누르면 현재 배열·길이·메서드의 반환값을 함께 확인할 수 있다.

## 조작 순서

각 행을 확인하기 전에 **초기화**를 누른다. 초기 배열은 `['사과', '바나나', '포도']`다.

| 입력과 버튼 | 실행 후 배열 | 반환값 |
|---|---|---|
| 값 `귤`, push | `['사과', '바나나', '포도', '귤']` | 새 길이 `4` |
| 값 `귤`, unshift | `['귤', '사과', '바나나', '포도']` | 새 길이 `4` |
| pop | `['사과', '바나나']` | 삭제한 값 `'포도'` |
| shift | `['바나나', '포도']` | 삭제한 값 `'사과'` |
| 값 `귤`, 위치 `1`, splice 삽입 | `['사과', '귤', '바나나', '포도']` | 삭제한 항목 배열 `[]` |
| 위치 `1`, splice 삭제 | `['사과', '포도']` | 삭제한 항목 배열 `['바나나']` |

## 배열을 변경하는 코드

```js
const length = fruits.push('귤');
const removed = fruits.pop();
const inserted = fruits.splice(1, 0, '귤');
const deleted = fruits.splice(1, 1);
```

위 코드를 순서대로 실행하면 초기 배열에서 출발해 `귤`을 뒤에 추가하고 삭제한 뒤, 위치 1에 삽입하고 삭제한다.
`push`, `unshift`, `pop`, `shift`, `splice`는 원본 배열을 변경한다.
`splice(위치, 삭제할 개수, 추가할 값)`의 반환값은 추가한 항목이 아니라 삭제한 항목의 배열이다.

## 경계값 확인

- `pop`이나 `shift`를 반복해 빈 배열로 만든 뒤 한 번 더 누르면 길이는 `0`, 반환값은 `undefined`다.
- 이 화면에서 삽입 위치는 `0`부터 현재 길이까지, 삭제 위치는 `0`부터 현재 길이보다 1 작은 값까지 허용한다.
- 위치에 빈 값·음수·소수·범위를 벗어난 값을 넣으면 실행하지 않는다. JavaScript 자체의 `splice`는 음수 등의 다른 규칙도 지원하지만 이 예제는 위치 계산 연습 범위를 제한한다.
- 추가할 값이 비어 있거나 공백뿐이면 실행하지 않는다. 입력값의 앞뒤 공백은 제거한다.
- 새로고침과 **초기화**는 모두 처음 배열로 돌아간다. 저장소에는 값을 쓰지 않는다.

입력은 `#value`·`#position`, 결과는 `#array-output`·`#length-output`·`#return-output`이다.
코드는 [app.js](app.js)에 있다.
