[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_object_localstorage)

# 11주차 실습 — 객체 확인과 폼 저장

양일 모두 강의·시연 60분 뒤 실습 30분을 진행한다. 수업 전에 교재를 `shared` 폴더와 함께 받아 정적 서버를 준비한다. 새 저장소 생성, 방명록 전체 구현, 공개 업로드는 수업 중 필수 작업이 아니다.

## 실행 준비

`teaching_repo` 폴더에서 다음 명령을 실행한다. 이미 실행 중이면 그대로 사용한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

1일차는 [ex01](http://localhost:8111/weeks/week11_object_localstorage/examples/day1/ex01/), 2일차는 [ex04](http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex04/)부터 연다. `app.js`를 고친 뒤 저장하고 브라우저를 새로고침한다. 공용 CSS 경로를 유지하기 위해 예제 폴더만 따로 옮기지 않는다.

## 1일차 — 객체와 점 표기 (30분)

| 실습 시간 | 작업 |
|---|---|
| 0–8분 | ex01 속성 값 변경과 화면 결과 비교 |
| 8–16분 | ex02 인덱스 변경과 결과 비교 |
| 16–25분 | ex03 표시 필드 변경과 두 목록 비교 |
| 25–30분 | 바꾼 내용과 결과 확인 |

### ex01 객체의 값 읽기

[화면](examples/day1/ex01/index.html) · [코드](examples/day1/ex01/app.js)

객체의 `name` 값을 바꾸고 새로고침한다. 화면의 `item.name`이 바뀌는지 확인하고 이름 입력·이름 적용 버튼도 사용한다. 전체 객체는 Console에서 추가로 확인한다. `item.nmae`가 `undefined`인 이유를 속성 이름과 비교한다.

### ex02 배열에서 객체 고르기

[화면](examples/day1/ex02/index.html) · [코드](examples/day1/ex02/app.js)

`app.js` 마지막 화면 출력의 `items[0].name`을 `items[1].name`으로 바꾼다. 저장·새로고침한 뒤 배열 결과 확인을 눌러 하늘이 바다로 바뀌는지 확인한다. `items[0]`은 객체 하나, `.name`은 그 객체의 속성이라는 점을 말로 설명한다.

### ex03 화면에 필드 표시

[화면](examples/day1/ex03/index.html) · [코드](examples/day1/ex03/app.js)

`[object Object]`가 보이는 목록과 이름·메시지·날짜가 보이는 목록을 비교한다. 둘째 목록의 `items[i].name`을 `items[i].message`로 바꾸고 표시 필드가 달라지는지 확인한 뒤 되돌린다. 속성 철자를 `nmae`로 바꾸면 `undefined`가 보인다. 1일차는 별도 공개 업로드나 제출 캡처를 요구하지 않는다.

## 2일차 — 저장과 폼 복원 (30분)

| 실습 시간 | 작업 |
|---|---|
| 0–8분 | ex04 저장·불러오기·지우기 |
| 8–16분 | ex05 JSON 원문과 복원 결과 비교 |
| 16–27분 | ex06 저장·새로고침·폼 복원·지우기 |
| 27–30분 | ex06을 다시 저장·복원하고 캡처 |

### ex04 문자열 저장

[화면](examples/day2/ex04/index.html) · [코드](examples/day2/ex04/app.js)

1. 문자열 입력 → 저장 → 입력 변경 → 불러오기를 실행한다.
2. 새로고침 후 불러와도 저장한 값이 남는지 확인한다.
3. 빈 문자열을 저장했을 때 `""`, 지우고 불러왔을 때 `null`을 비교한다.

확인할 키는 `week11-ex04-text`다. `setItem`, `getItem`, `removeItem`이 각 버튼과 연결되는 위치를 찾는다.

### ex05 JSON 저장과 복원

[화면](examples/day2/ex05/index.html) · [코드](examples/day2/ex05/app.js)

1. JSON 저장 → 저장 원문 조회를 실행한다. 원문에서 `[]`, `{}`, `"name"`을 찾는다.
2. JSON 복원을 실행해 두 객체의 이름·메시지와 개수 2를 확인한다.
3. 지우기 후 다시 복원해 저장 값이 없는 상태를 확인한다.

키는 `week11-ex05-items`다. 저장할 때 `JSON.stringify`, 읽은 문자열을 복원할 때 `JSON.parse`를 사용한다.

### ex06 입력 폼 저장과 복원

[화면](examples/day2/ex06/index.html) · [코드](examples/day2/ex06/app.js)

1. 이름 `하늘`, 메시지 `안녕하세요`를 입력하고 저장한다.
2. 입력만 바꾼 뒤 불러와 저장한 값으로 돌아오는지 확인한다.
3. 새로고침 → 불러오기를 실행한다. 두 입력과 저장 JSON을 확인한다.
4. 지우기 → 불러오기를 실행해 저장 값이 없는 상태를 확인한다.
5. 캡처용으로 다시 입력·저장·새로고침·불러오기를 실행한다.

오류 처리·형식 검사와 버튼 연결은 제공 코드다. 학생은 저장·불러오기·지우기의 위치와 결과를 확인하며 방어 코드를 다시 작성하지 않는다.

키는 `week11-ex06-entry`다. 이 예제는 빈 입력도 객체의 문자열 필드로 저장한다. 초기 화면을 열기만 해서는 저장하지 않는다.

## 제출 — 복원한 폼 캡처 한 장

ex06에서 새로고침 후 불러온 화면을 캡처한다. 다음 내용이 함께 보이면 된다.

- 복원된 이름·메시지 입력
- `{"name":"하늘","message":"안녕하세요"}` 형태의 저장 JSON
- `http://localhost:8111/.../day2/ex06/` 주소창

로컬 실습 화면을 인정한다. Application 탭은 저장 값을 추가로 확인할 때 사용하며 캡처에 반드시 넣을 필요는 없다. 실명·학번·실제 이메일은 쓰지 않는다. 제출 위치와 마감은 수업 공지를 따른다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 버튼을 눌러도 반응이 없다 | Console의 오류와 `app.js` 경로를 확인한다 |
| 스타일이 적용되지 않는다 | W3.CSS CDN 연결을 위한 인터넷 상태와 `shared/examples.css` 경로를 확인한다. 서버 루트는 `web_programming`이다 |
| 저장한 값이 없다고 나온다 | 저장·불러오기의 키, 브라우저, 프로토콜·호스트·포트가 같은지 확인한다 |
| 새로고침 후 입력이 비었다 | ex06은 자동 복원이 아니다. 불러오기 버튼을 누른다 |
| JSON 복원 실패가 표시된다 | 해당 예제의 지우기를 누르고 다시 저장한다. 다른 예제의 키는 건드리지 않는다 |
| 파일을 두 번 눌러 열면 결과가 다르다 | `file://` 대신 위의 localhost 주소를 사용한다 |
| 서버 포트가 사용 중이라고 나온다 | 기존 서버 주소를 먼저 열어 본다. 같은 서버를 중복 실행하지 않는다 |

## 수업 후 정리와 별도 자료

공개 업로드나 개인 저장소 정리는 수업 후 필요에 따라 진행한다. 저장된 값은 origin별이므로 localhost에서 남긴 데이터가 공개 사이트로 자동 이전되지는 않는다.

[완성 방명록](examples/day2/web-week11/README.md)은 강의자 시연·12주차 준비 자료이며 이번 제출에 포함하지 않는다. [배열 심화 특강](../../specials/array_advanced/README.md)과 [고급 저장 참고](examples/day2/README.md#고급-저장-참고)는 정규 30분 실습 범위 밖이다.
