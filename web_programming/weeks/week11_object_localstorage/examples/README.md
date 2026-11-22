[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_object_localstorage)

# 11주차 예제 — 객체와 기본 저장

각 수업은 강의·시연 60분, 실습 30분이다. 필수 실습은 1일차 ex01~ex03과 2일차 ex04~ex06이다. 2일차 결과물은 새로고침 후 복원한 ex06 폼과 저장 JSON이다.

```text
web_programming/
  weeks/week11_object_localstorage/examples/
    day1/ex01/ ~ ex03/     객체·배열·목록
    day2/ex04/ ~ ex06/     문자열·JSON·폼 저장
    day2/web-week11/       강의자 시연·12주 선택 방명록 자료
    day2/ex07/             탭 동기화 참고
```

## 실행

ex01~ex07의 HTML은 [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)에서 스타일을 읽고, 같은 폴더의 `app.js`를 실행한다. CDN 스타일에는 인터넷 연결이 필요하다.

`teaching_repo` 폴더에서 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

[1일차 ex01](http://localhost:8111/weeks/week11_object_localstorage/examples/day1/ex01/) 또는 [2일차 ex04](http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex04/)를 연다. 경로의 일차와 예제 번호를 바꿔 다음 예제를 연다. 서버가 이미 실행 중이면 다시 실행하지 않는다.

## 필수 예제

| 예제 | 조작·비교 |
|---|---|
| [ex01 화면](day1/ex01/index.html) · [코드](day1/ex01/app.js) | 객체의 이름을 바꾸고 전체 객체·속성 값·`undefined` 비교 |
| [ex02 화면](day1/ex02/index.html) · [코드](day1/ex02/app.js) | `items[0].name`과 `items[1].name` 비교 |
| [ex03 화면](day1/ex03/index.html) · [코드](day1/ex03/app.js) | 객체 그대로 표시한 목록과 필드를 꺼내 쓴 목록 비교 |
| [ex04 화면](day2/ex04/index.html) · [코드](day2/ex04/app.js) | 문자열 저장·불러오기·지우기, 빈 문자열과 키 없음 비교 |
| [ex05 화면](day2/ex05/index.html) · [코드](day2/ex05/app.js) | JSON 저장·원문 조회·복원으로 이름·메시지 확인 |
| [ex06 화면](day2/ex06/index.html) · [코드](day2/ex06/app.js) | 이름·메시지 저장, 새로고침 후 폼 복원 |

ex01은 이름 적용, ex02는 배열 결과 확인 버튼으로 화면에서 확인한다. 전체 객체·배열은 Console에서 추가로 확인하고, ex03은 두 목록을 비교한다. ex04~ex06은 화면의 입력·버튼·결과로 확인한다. Application › Local Storage에는 `week11-ex04-text`, `week11-ex05-items`, `week11-ex06-entry`가 저장된다. 처음 화면을 여는 것만으로 저장하지 않는다.

저장 실습은 localhost에서 진행한다. `file://` 동작은 브라우저마다 다를 수 있다. 같은 브라우저·origin은 경로가 달라도 저장 공간을 공유하므로 예제별 키를 구분한다. [MDN localStorage](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)

## 확인과 제출

ex06에서 저장 → 새로고침 → 불러오기 순서로 입력을 복원한다. 복원된 폼·JSON·주소창을 한 장으로 캡처한다. localhost 화면을 인정한다. GitHub 저장소 생성·push·Pages 공개는 30분 실습에 포함하지 않으며 수업 후 필요에 따라 정리한다.

[실습지](../lab.md)와 [따라하기](../walkthrough.md)에 시간표와 확인 순서가 있다.

## 강의자용 완성 방명록

[`day2/web-week11/`](day2/web-week11/)은 객체 배열의 저장·복원을 보여 주는 완성본이다. 이번 주 학생 필수 구현 대상은 아니며 12주 선택 방명록에 이어 쓴다.

- [guestbook.html](day2/web-week11/guestbook.html) · [guestbook.js](day2/web-week11/guestbook.js)
- [완성본 안내](day2/web-week11/README.md) · [전체 코드 부록](../walkthrough.md#부록-강의자용-방명록-완성본)

## 이전 주와 다음 주의 파일 인계

| 파일·활동 | 이전 자료와 이번 범위 |
|---|---|
| 10주 `web-week10/guestbook.js` | 문자열 배열·고전 `for`·`showList`·`splice` 비교 기준 |
| ex01~ex03 | 학생이 속성 값·배열 인덱스·표시 필드를 수정. 화면 연결과 날짜는 제공 틀 |
| ex04~ex06 | 학생이 문자열·JSON·폼 저장을 실행하고 확인. 오류 처리·형식 검사는 제공 코드 |
| `web-week11/guestbook.html`·`guestbook.js` | 객체 배열·저장·손상 값 복구를 갖춘 제공 시연본. 학생 전체 구현 대상 아님 |
| `web-week11/index.html`·`about.html`·`app.js`·`styles.css`·`images/` | 이전 주 홈·소개 자료를 이어 씀 |
| 12주 로컬 보관본 | 제공 파일을 `guestbook.local.html`·`guestbook.local.js`로 보관. 서버용 `guestbook.html`과 분리, 로컬 글 이관·삭제 없음 |

## 별도 보강과 참고

[배열 심화 특강](../../../specials/array_advanced/README.md)은 별도 수업에서 삽입·삭제·순회·filter·map·reduce를 다룬다. 배열 예제는 특강 폴더로 이동했다.

[ex07 탭 동기화](day2/README.md#고급-저장-참고)는 정규 실습 범위 밖의 참고 자료다. 같은 origin의 다른 탭에서 저장 값의 변화를 확인한다.

완성본 `day2/web-week11/guestbook.html`은 [W3.CSS CDN 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용한다. 추가 CSS는 없으며 `styles.css`는 홈·내 정보에서 사용한다. CDN 스타일에는 인터넷 연결이 필요하다.
