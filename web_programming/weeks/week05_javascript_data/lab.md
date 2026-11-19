[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data)

# 5주차 실습: 값과 함수의 결과 확인

각 차시는 강의·시연 60분과 실습 30분이다. 파일·새 저장소·Node.js 24 이상·서버는 수업 전에 준비한다. 첫 5분에는 준비 상태만 확인한다. 공개 업로드는 수업 뒤 정리다.

비교 예제의 버튼과 출력은 제공 코드다. 필수 범위 밖의 `var`·`==`·`parseInt`·`getElementById`·`innerText`는 시연·선택 연습으로 남긴다. 모든 예제를 한 곳씩 수정하는 과제는 없다.

## 1일차 강의·시연 60분

| 시간 | 내용 |
|---|---|
| 0–5분 | 배부 폴더와 localhost 확인 |
| 5–15분 | ex01 실행 순서, ex02 defer와 body 존재 시점 |
| 15–30분 | ex03 let/const, 재대입 오류와 파일·줄 위치 |
| 30–45분 | ex04 숫자/문자열, 입력 value, Number |
| 45–55분 | ex05 템플릿 문자열과 계산 |
| 55–60분 | 값 4곳과 오류 1건 수정 안내 |

## 1일차 30분 실습

| 실습 시간 | 직접 수정·확인 |
|---|---|
| 0–15분 | ex03 `let a = 0`의 0을 10, `const b = 0`의 0을 20으로 변경. ex05 name을 student02, hour를 15로 변경. 값 수정은 이 4곳이다 |
| 15–25분 | 저장·새로고침 후 ex03 let 버튼 → 11, ex05 출력 버튼 → student02·15시 확인. ex03 const 버튼에서 오류 확인 후 `const b`를 `let b`로 변경·새로고침·클릭 → 21 확인 |
| 25–30분 | 다른 폴더 파일을 고치지 않았는지 확인하고 결과 화면 확인 |

[ex03 안내](examples/day1/ex03/README.md)와 [ex05 안내](examples/day1/ex05/README.md)를 참고한다. ex03 const 버튼의 오류는 비교를 위해 의도한 오류다. 처음 열 때는 오류가 없고 재대입 줄을 실행할 때 발생한다. 수정 후 새로고침하여 새 실행에서 오류가 사라졌는지 확인한다.

## 2일차 강의·시연 60분

| 시간 | 내용 |
|---|---|
| 0–5분 | 홈과 제공 시작 app.js 확인 |
| 5–20분 | ex06 비교·ex07 if/else, 9·12·15시 |
| 20–40분 | ex08 정의·호출·return, greet와 hello 조립, ex10 날짜 제공 줄 |
| 40–50분 | ex09 querySelector·textContent, 없는 id 오류 |
| 50–55분 | 제공 server.mjs 실행·HTML/CSS/JS 요청 확인 |
| 55–60분 | 수정 3곳과 9시/15시 검증 안내 |

## 2일차 30분 실습

배부된 `web-week05/app.js`는 [시작 파일](examples/day2/start/app.js)이다. HTML의 script와 `#greeting`, CSS·이미지·나머지 페이지는 이미 준비되어 있다. app.js 전체를 새로 작성하지 않는다.

| 실습 시간 | 직접 수정·확인 |
|---|---|
| 0–18분 | `greet`의 반환 문자열에 name 연결 1곳, `hello`의 오후 조건을 12시 기준으로 수정 1곳, 마지막 `querySelector('#greeting').textContent`에 message 출력 1곳 |
| 18–25분 | hour를 임시로 9 → 15로 바꿔 각각 아침·오후 확인. `new Date().getHours()`로 복원 |
| 25–30분 | localhost에서 인사말과 Console 두 줄 확인·캡처 1장 |

수정하는 세 줄은 다음과 같다. 함수의 다른 줄·message 조합·로그는 제공 코드다.

```js
  return `안녕하세요, ${name}님!`;
  if (hour >= 12) {
document.querySelector('#greeting').textContent = message;
```

9시는 `안녕하세요, student01님! 좋은 아침입니다.`, 15시는 `안녕하세요, student01님! 좋은 오후입니다.`가 나와야 한다. 12시도 오후다. 임시 검증 숫자는 제출 전에 원래 날짜 식으로 돌려놓는다. [완성 전문](walkthrough.md#완성-appjs)을 비교에 사용한다.

## 막혔을 때

| 증상 | 확인과 복구 |
|---|---|
| 화면이 그대로다 | 편집기 저장 → 같은 폴더 페이지 새로고침 → 출력 버튼 순서로 확인한다 |
| Assignment to constant variable | ex03의 b를 재대입했다. 필수 오류 수정은 `const b`를 `let b`로 바꾸는 것이다 |
| Cannot set properties of null | HTML id와 `#greeting` 철자, script의 defer를 대조한다 |
| greeting은 있지만 예전 count-button 오류가 난다 | 사전 배부가 빠졌다. 기존 2주 카운터 JS를 제공 시작 app.js로 교체한다 |
| SyntaxError | 백틱·괄호·중괄호의 짝을 본다. 문법 오류가 있으면 그 파일 전체가 실행되지 않는다 |
| 인사에 ${name}이 그대로다 | 작은따옴표를 백틱으로 바꾼다 |
| 9시인데 오후다 | `if (hour = 12)`는 대입이다. `hour >= 12`로 고친다 |
| 함수 결과가 undefined다 | return이 있는지 확인한다. console.log는 반환값을 대신하지 않는다 |
| node 명령이 없다 | 사전 설치·터미널 재시작을 확인한다. 이번 주는 HTML 직접 열기로 결과 확인을 먼저 마치고 환경은 다음 차시 전에 복구한다 |
| 포트 8000 사용 중 | 기존 서버를 확인하거나 `node server.mjs . 8001`로 실행한다 |

## 제출과 수업 뒤 정리

주소창·홈 인사말·Console의 시각 숫자와 인사말 두 줄이 보이는 캡처 1장을 제출한다. localhost 캡처로 수업 중 완료를 인정한다. 12시 이후의 오후 인사도 정답이다. 실명·학번·실제 이메일을 넣지 않는다.

미완성 학생은 ex01 클릭 뒤 A·C·B 결과를 임시 제출하고 다음 차시 첫 5분에 보완한다. 수업 뒤 기존 2주 업로드 순서로 `web-week05`를 공개하고 Pages에서 확인한다. 업로드 자체는 30분 실습에 넣지 않는다. 제출 위치·마감은 수업 공지를 따른다.

## 선택 연습

ex02 defer 제거·복원, ex04 입력 10·5와 Number/parseInt 비교, ex07 조건 순서 비교, ex08 return 없는 함수, ex09 다른 DOM 접근법, ex10 날짜 함수 추가는 각 예제 README를 따른다. 선택 연습을 마치지 않아도 필수 완료 조건을 충족할 수 있다.
