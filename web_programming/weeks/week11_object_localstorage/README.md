[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_object_localstorage)

# 11주차 — 객체와 localStorage

이번 주는 객체를 읽고, 입력한 값을 브라우저에 저장했다가 불러오는 방법을 익힌다. 각 수업은 **강의·시연 60분 + 실습 30분**이다.

1일차 실습은 객체 예제 ex01~ex03, 2일차 실습은 문자열·JSON·폼 저장 예제 ex04~ex06으로 한정한다. 방명록 완성본은 강의자 시연과 12주차 준비 자료다. 수업 중 새 저장소 생성이나 방명록 전체 구현을 요구하지 않는다.

## 학습 목표

1. 객체의 속성을 `item.name`, `items[i].name`으로 읽는다.
2. 객체의 필드를 화면에 표시한다.
3. `setItem`, `getItem`, `removeItem`으로 문자열을 저장·불러오기·삭제한다.
4. `JSON.stringify`와 `JSON.parse`로 객체를 저장하고 복원한다.
5. 새로고침한 뒤 이름·메시지 폼을 복원하고 저장된 JSON을 확인한다.

## 2일 수업 흐름

| 일차 | 강의·시연 60분 | 실습 30분 | 확인 결과 |
|---|---|---|---|
| 1일차 | 실행 환경 10분 → 객체 15분 → 객체 배열 15분 → 목록 표시 15분 → 실습 안내 5분 | ex01~ex03의 값·속성을 바꾸고 결과 비교 | 객체 필드와 배열 인덱스를 구분한다 |
| 2일차 | 문자열 저장 10분 → JSON 15분 → 폼 복원 15분 → 저장 범위 10분 → 검증 순서 5분 → 실습 안내 5분 | ex04 저장·삭제 → ex05 원문·복원 → ex06 폼 복원·캡처 | 새로고침 후 복원한 폼과 저장 JSON |

강의 시간에는 강의자가 조작과 코드를 함께 보여 준다. 학생은 뒤의 30분에 기본 예제를 실행한다. 배열 심화와 탭 동기화는 정규 수업 범위에 포함하지 않는다.

## 준비와 실행

VS Code, Chrome, Node.js를 준비한다. 교재를 내려받을 때 `web_programming`의 폴더 구조와 `shared` 폴더를 유지한다. 예제 HTML·JS만 따로 복사하면 공용 CSS 경로가 끊길 수 있다.

`teaching_repo` 폴더에서 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

- 1일차: [ex01 열기](http://localhost:8111/weeks/week11_object_localstorage/examples/day1/ex01/)
- 2일차: [ex04 열기](http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex04/)
- 스타일: [W3.CSS CDN 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css) · [추가 공용 스타일](../../shared/examples.css)

예제마다 `index.html`은 화면, `app.js`는 동작이다. 2일차 ex04~ex07은 W3.CSS를 CDN에서 읽고 추가 공용 스타일 `shared/examples.css`를 불러온다. CDN 스타일을 읽으려면 인터넷 연결이 필요하다. 1일차 예제는 기존 구성을 유지한다. 설명과 조작 순서는 README에서 읽는다. [정적 서버 안내](../../tools/static-server/README.md)

저장 실습은 `file://` 대신 위의 localhost 주소에서 진행한다. 저장 공간은 브라우저의 origin(프로토콜·호스트·포트)별로 구분된다. 같은 origin의 폴더들은 저장 공간을 공유하고, 포트나 호스트가 다르면 별도 공간이다. [MDN localStorage](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)

## 기본 예제

| 예제 | 확인할 내용 |
|---|---|
| [ex01](examples/day1/ex01/index.html) · [코드](examples/day1/ex01/app.js) | 객체 전체와 `item.name`, 없는 속성의 `undefined` |
| [ex02](examples/day1/ex02/index.html) · [코드](examples/day1/ex02/app.js) | 문자열 배열과 객체 배열, `items[0].name` |
| [ex03](examples/day1/ex03/index.html) · [코드](examples/day1/ex03/app.js) | 객체 그대로 표시한 목록과 속성을 꺼낸 목록 |
| [ex04](examples/day2/ex04/index.html) · [코드](examples/day2/ex04/app.js) | 문자열 저장·불러오기·지우기, `''`와 `null`의 차이 |
| [ex05](examples/day2/ex05/index.html) · [코드](examples/day2/ex05/app.js) | JSON 문자열 저장 → 원문 조회 → 배열·필드 복원 |
| [ex06](examples/day2/ex06/index.html) · [코드](examples/day2/ex06/app.js) | 이름·메시지 저장 → 새로고침 → 폼 복원 |

## 완료 기준과 제출

2일차 ex06에서 이름과 메시지를 저장하고 새로고침한 뒤 불러온다. **복원된 입력, 저장된 JSON, 주소창**이 보이는 화면 한 장을 제출한다. localhost 실습 화면을 인정하며, 공개 업로드는 수업 후 정리로 분리한다.

- [ ] ex04에서 빈 문자열 저장과 키 삭제의 결과를 구분했다.
- [ ] ex05에서 저장 원문과 파싱한 이름·메시지 필드를 확인했다.
- [ ] ex06에서 새로고침 후 입력을 복원했다.
- [ ] ex06에서 지우기 후 다시 불러와 저장 값이 없는지 확인했다.
- [ ] 캡처용으로 다시 저장·새로고침·불러오기를 수행했다.

실명·학번·실제 이메일은 사용하지 않는다. 자세한 순서와 오류 해결은 [실습지](lab.md)에 있다.

## 강의자 시연과 다음 주 준비

[web-week11 완성 방명록](examples/day2/web-week11/README.md)은 객체 배열을 저장·복원하는 시연 자료다. 학생의 이번 주 필수 구현·제출에 포함하지 않는다. 전체 HTML·JS는 [따라하기 부록](walkthrough.md#부록-강의자용-방명록-완성본)에 있다.

12주차에는 이 준비된 완성본을 출발점으로 공용 REST API의 JSON 배열을 읽는다. 학생이 11주차에 방명록 전체를 만들었다고 가정하지 않는다.

## 별도 보강 자료

- [배열 심화 특강](../../specials/array_advanced/README.md): 삽입·삭제·순회·filter·map·reduce를 별도 시간에 다룬다.
- [고급 저장 참고](examples/day2/README.md#고급-저장-참고): ex07의 탭 동기화는 참고 자료다.

## 수업 자료

- [한글 슬라이드](slides.md) · [영문 슬라이드](slides_en.md)
- [따라하기](walkthrough.md) · [실습과 제출](lab.md)
- [예제 안내](examples/README.md) · [2일차 안내](examples/day2/README.md)

## 공식 참고 자료

- [객체로 작업하기 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Working_with_objects)
- [localStorage — MDN](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)
- [JSON.stringify (MDN)](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify) · [JSON.parse (MDN)](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse)
