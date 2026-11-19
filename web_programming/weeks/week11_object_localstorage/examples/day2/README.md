# 2일차 기본 저장 실습

이번 수업은 강의·시연 60분, 실습 30분으로 진행한다. 필수 예제는 문자열 저장, JSON 저장과 파싱, 폼 복원의 세 가지다. 배열 심화는 [별도 보강 특강](../../../../specials/array_advanced/README.md)에서 진행한다.

## 실행

`teaching_repo` 폴더의 터미널에서 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

브라우저에서 [ex04 문자열 저장](http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex04/)을 연다. 주소 끝의 `ex04`를 `ex05` 또는 `ex06`으로 바꾼다. 서버는 파일을 제공하고 실습 데이터는 브라우저에 저장한다.

예제는 [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)과 [추가 공용 CSS](../../../../shared/README.md)를 사용한다. CDN 스타일에는 인터넷 연결이 필요하다. `web_programming`을 서버 루트로 삼고 `shared/examples.css`와 예제의 상대 위치를 유지한다. 별도 배포 시 필요한 파일과 경로 조정은 공용 CSS 안내를 따른다.

`file://` 대신 localhost 또는 HTTPS 주소로 연다. 저장 공간은 브라우저와 origin(프로토콜·호스트·포트)별로 구분된다. 같은 origin의 폴더들은 저장 공간을 공유한다. 포트를 바꾸거나 공개 주소로 옮기면 기존 값은 보이지 않는다. [MDN localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)

## 필수 예제

| 순서 | 예제 | 조작과 확인 |
|---|---|---|
| 1 | [ex04 문자열 저장](ex04/README.md) | 저장 → 입력 변경 → 불러오기 → 새로고침 후 불러오기 → 지우기 |
| 2 | [ex05 JSON 저장과 파싱](ex05/README.md) | JSON 저장 → 원문 조회 → 파싱한 이름·메시지 확인 |
| 3 | [ex06 폼 데이터 저장](ex06/README.md) | 이름·메시지 입력 → 저장 → 폼 변경 → 불러오기 → 입력 복원 |

ex04에서는 다음 세 동작을 구분한다.

```js
localStorage.setItem('week11-ex04-text', '안녕하세요');
const text = localStorage.getItem('week11-ex04-text');
localStorage.removeItem('week11-ex04-text');
```

ex05와 ex06에서는 객체를 문자열로 바꿔 저장하고 읽은 문자열을 다시 객체로 만든다.

```js
const entry = { name: '하늘', message: '안녕하세요' };
localStorage.setItem('week11-ex06-entry', JSON.stringify(entry));
const saved = localStorage.getItem('week11-ex06-entry');
if (saved !== null) {
    const restored = JSON.parse(saved);
}
```

`getItem()`은 키가 없으면 `null`, 빈 문자열을 저장했으면 `''`을 반환한다. JSON 문법이 잘못되면 `JSON.parse()`에서 예외가 발생한다. 오류 처리와 형식 검사는 제공 코드이며 학생 재작성 범위가 아니다.

## 30분 실습

| 시간 | 실습 | 확인 |
|---|---|---|
| 0–8분 | ex04 저장·불러오기·지우기 | 저장 값과 `null` 구분 |
| 8–16분 | ex05 JSON 저장·원문·파싱 | 문자열과 객체 배열 구분 |
| 16–27분 | ex06 폼 저장·새로고침·복원 | 이름·메시지와 저장 JSON 일치 |
| 27–30분 | ex06 재저장·새로고침·복원과 캡처 | 복원한 폼과 JSON 결과 캡처 |

실습 확인은 localhost 화면에서 마친다. 저장소 생성·업로드·Pages 배포는 30분 실습에 포함하지 않으며 필요하면 수업 전 준비 또는 수업 후 정리로 진행한다.

[완성 방명록](web-week11/README.md)은 강의자가 저장 기능을 시연할 때 사용한다. 12주차 시작 자료로 제공하며 이번 실습 시간에 전체를 다시 작성하지 않는다.

## 고급 저장 참고

[ex07 탭 동기화](ex07/README.md)는 같은 origin의 다른 탭에서 `storage` 이벤트를 받는 예제다. 두 탭을 열고 한쪽에서 저장·삭제한 값이 다른 쪽에 반영되는지 확인한다. 이번 90분 수업과 필수 제출에서는 제외한다.
