---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 5주차"
footer: "JavaScript · 60 + 30"
---

# JavaScript 데이터와 함수

4주차의 세 페이지와 자체 CSS를 이어 쓰고 홈에 인사말을 표시합니다.

- 각 차시: 강의·시연 60분 + 실습 30분
- 1일차 필수: ex03·ex05 값 4곳과 오류 1건 수정
- 2일차 필수: 조건·인사 함수·출력 각 1곳 수정
- 비교 예제 10개를 보존합니다. 나머지 비교는 시연·선택입니다.

화면의 버튼·출력은 제공 코드입니다. Console은 실행 순서와 오류를 확인하는 보조 도구입니다.

---

# 1일차: 스크립트와 값

| 강의·시연 | 시간 |
|---|---|
| 파일·서버 준비 확인 | 0–5분 |
| 실행 순서·defer | 5–15분 |
| let·const | 15–30분 |
| 숫자·문자열 | 30–45분 |
| 템플릿 문자열 | 45–55분 |
| 실습 안내 | 55–60분 |

이후 학생 실습 30분입니다. var·parseInt는 선택 비교입니다.

---

## 1일차 0–5분: 준비 확인

수업 전에 4주 파일·새 web-week05 저장소·ex01~ex10 폴더를 준비합니다.
Node.js 24 이상과 server.mjs도 사전 준비입니다. Git을 새로 설명하지 않습니다.

```text
ex/ex03/index.html  → 브라우저에서 열기
ex/ex03/app.js      → 값을 고치고 저장
화면 버튼          → 결과 확인
F12 › Console      → 로그와 오류의 파일:줄 확인
```

HTML은 내용, CSS는 모양, JavaScript는 동작입니다.
파일을 저장한 뒤 같은 폴더의 페이지를 새로고침합니다.

---

## 1일차 5–10분: ex01 실행 순서

[ex01 실행](examples/day1/ex01/index.html) · [설명](examples/day1/ex01/README.md)

```js
console.log('A. 페이지를 열자마자 실행된다');
document.getElementById('btn').addEventListener('click', function () {
    console.log('B. 버튼을 누를 때마다 실행된다');
});
console.log('C. A 바로 다음에 실행된다. B 보다 먼저');
```

발췌 코드입니다. 실제 파일의 화면 출력은 제공 코드입니다.
처음에는 A·C, 버튼 3회 뒤에는 B가 3회 추가됩니다.
클릭 함수는 등록할 때 실행하지 않습니다. 이벤트 직접 작성은 6주에 합니다.

---

## 1일차 10–15분: ex02 defer

[ex02 실행](examples/day1/ex02/index.html) · [설명](examples/day1/ex02/README.md)

```html
<script src="app.js" defer></script>
```

- head의 일반 script: body를 읽기 전이므로 document.body는 null
- body 끝의 script: body가 존재
- head의 defer 파일: HTML을 모두 읽은 뒤 실행

출력 버튼: `1: null → 2: body → 3: body`
강의자가 defer를 지우면 `1: null → 3: null → 2: body`입니다.
비교 뒤 defer를 복원합니다. 출력 버튼 연결은 제공 코드입니다.

---

## 1일차 15–30분: ex03 let·const

[ex03 실행](examples/day1/ex03/index.html) · [설명](examples/day1/ex03/README.md)

```js
let a = 0;
const b = 0;
// 클릭 함수 안
b = b + 1;
```

let은 재대입할 수 있습니다. const는 재대입할 수 없습니다.
const 버튼을 누르는 순간 `Assignment to constant variable.`이 납니다.
오류가 난 콜백의 다음 줄은 실행되지 않습니다.

학생은 a=10, b=20으로 변경합니다. const 오류를 보고 let으로 고치면 20→21입니다.
var 버튼은 선택 비교이며 필수 구현·평가에서 제외합니다.

---

## 1일차 30–45분: ex04 숫자와 문자열

[ex04 실행](examples/day1/ex04/index.html) · [설명](examples/day1/ex04/README.md)

```js
1 + 2                                    // 3
'1' + 2                                  // '12'
num1.value + num2.value                   // 문자열 연결
Number(num1.value) + Number(num2.value)   // 숫자 덧셈
```

입력 1·2에서 버튼 결과는 12와 3, 입력 10·5에서는 105와 15입니다.
입력 value는 문자열입니다. Number로 변환한 뒤 더합니다.

parseInt('12px')는 12, Number('12px')는 NaN입니다.
이 비교는 선택이며 필수 수정·평가에서 제외합니다.

---

## 1일차 45–55분: ex05 템플릿 문자열

[ex05 실행](examples/day1/ex05/index.html) · [설명](examples/day1/ex05/README.md)

```js
const name = 'student01';
const hour = 9;
`안녕하세요, ${name}님! 지금은 ${hour}시입니다.`
'안녕하세요, ${name}님!'
`한 시간 뒤는 ${hour + 1}시입니다.`
```

백틱의 ${}는 계산하고 작은따옴표에서는 글자 그대로입니다.
학생은 name=student02, hour=15로 바꿉니다.
제공 출력 버튼을 누르면 이름과 15시가 보입니다. Console의 한 시간 뒤는 16시입니다.

---

## 1일차 55–60분: 실습 인계

[1일차 실습](lab.md#1일차-30분-실습) · [따라하기](walkthrough.md#1일차)

| 실습 30분 | 학생 활동 |
|---|---|
| 0–15분 | ex03의 a·b, ex05의 name·hour: 값 4곳 변경 |
| 15–25분 | 출력 버튼 실행, const b를 let b로 수정 |
| 25–30분 | 11·21과 student02·15시 결과 확인 |

출력 지원 코드와 버튼 연결은 제공됩니다.
모든 비교 예제를 수정하는 과제는 없습니다.
공개 업로드는 수업 뒤 정리입니다.

---

# 2일차: 조건과 함수

| 강의·시연 | 시간 |
|---|---|
| 제공 시작 파일 확인 | 0–5분 |
| 비교·if | 5–20분 |
| 함수·return·날짜 제공 줄 | 20–40분 |
| querySelector·textContent | 40–50분 |
| 서버 요청 확인 | 50–55분 |
| 실습 안내 | 55–60분 |

이후 학생 실습 30분입니다. HTML 연결과 함수 틀은 사전 제공됩니다.

---

## 2일차 5–10분: ex06 비교

[ex06 실행](examples/day2/ex06/index.html) · [설명](examples/day2/ex06/README.md)

```js
1 === '1'   // false
12 >= 12    // true
12 > 12     // false
```

비교 결과는 true 또는 false입니다. ===는 타입과 값이 같아야 참입니다.
12시를 오후에 포함하려면 `hour >= 12`를 씁니다.
`=`는 대입입니다. `if (hour = 12)`는 시각 비교가 아닙니다.

==와 문자열 사전식 비교는 시연·선택입니다.
==는 필요한 타입 변환 뒤 비교하므로 단순히 값만 비교한다고 일반화하지 않습니다.

---

## 2일차 10–20분: ex07 if·else

[ex07 실행](examples/day2/ex07/index.html) · [설명](examples/day2/ex07/README.md)

```js
if (hour >= 12) {
    m2 = '오후';
} else {
    m2 = '오전';
}
```

9시는 오전, 12·15시는 오후입니다.
if 사슬은 처음 참인 갈래 하나만 실행합니다.

시연: ex07의 3번은 >=18을 먼저 검사해 20시에 저녁입니다.
4번은 >=12를 먼저 검사해 20시에도 오후입니다.

---

## 2일차 20–35분: ex08 함수와 return

[ex08 실행](examples/day2/ex08/index.html) · [설명](examples/day2/ex08/README.md)

```js
function greet(name) {
  return `안녕하세요, ${name}님!`;
}
greet('student01');
```

함수는 정의만으로 실행되지 않습니다. 괄호로 호출합니다.
매개변수 name에는 호출할 때 넣은 값이 들어갑니다.
return은 호출한 곳에 값을 돌려줍니다. 없으면 undefined입니다.

제공 시작 파일에서 학생이 고칠 곳은 greet의 반환 문장 1곳입니다.

---

## 2일차 35–40분: ex10 날짜 제공 줄

[ex10 실행](examples/day2/ex10/index.html) · [설명](examples/day2/ex10/README.md)

```js
const hour = new Date().getHours();
```

페이지가 실행된 순간의 시각을 0~23으로 읽습니다.
버튼을 다시 눌러도 같은 값을 표시합니다. 새로고침하면 다시 읽습니다.
날짜의 나머지 메서드 비교는 선택입니다.

실습 검증에서만 hour를 9와 15로 임시 변경합니다.
아침·오후 인사를 확인한 뒤 날짜 식으로 복원합니다.

---

## 2일차 40–50분: ex09 요소와 글자

[ex09 실행](examples/day2/ex09/index.html) · [설명](examples/day2/ex09/README.md)

```js
document.querySelector('#greeting').textContent = message;
```

querySelector는 CSS 선택자로 요소를 찾습니다. #은 id입니다.
textContent는 글자를 넣습니다. `<b>`를 넣어도 문자로 보입니다.
없는 id를 찾으면 null이고 textContent를 대입할 수 없습니다.

학생은 제공 시작 파일의 마지막 출력 1곳을 수정합니다.
getElementById·innerText는 선택 비교이며 필수 구현·평가에서 제외합니다.

---

## 2일차 50–55분: 제공 서버 확인

Node.js 24 이상과 [server.mjs](../../tools/static-server/server.mjs)는 사전 준비입니다.

```bash
node server.mjs
```

localhost:8000에서 홈을 엽니다. HTML·CSS·JS·그림은 각각 요청됩니다.
없는 파일은 404입니다. favicon 요청 유무와 요청 순서는 브라우저마다 다를 수 있습니다.

이번 주 예제는 file URL로도 실행됩니다. HTTP 요청 확인은 localhost에서 합니다.
환경 누락은 먼저 복구하며 서버 프로그램 구현은 학생 과제가 아닙니다.

---

## 2일차 55–60분: 세 곳 수정

[2일차 실습](lab.md#2일차-30분-실습) · [제공 시작 파일](examples/day2/start/README.md)

| 실습 30분 | 학생 활동 |
|---|---|
| 0–18분 | greet 반환 문장, hello 조건, textContent 출력 각 1곳 |
| 18–25분 | hour=9와 15 비교 후 현재 시각 식 복원 |
| 25–30분 | localhost 결과 확인·캡처 |

HTML의 defer·greeting, 날짜·함수 틀·message·로그는 제공 코드입니다.
app.js 전체를 새로 작성하지 않습니다.
var·==·parseInt·다른 DOM 접근법은 필수 평가에서 제외합니다.

---

## 제출과 수업 뒤 정리

수업 시간에는 캡처 1장을 만듭니다.

```text
주소: http://localhost:8000/
카드: 안녕하세요, student01님! 좋은 아침입니다.
Console: 시각 숫자 / 같은 인사말, 오류 없음
```

12시 이후의 오후 인사도 정답입니다.
미완성 학생은 ex01 클릭 후 A·C·B 화면을 임시 제출하고 다음 차시 첫 확인 시간에 보완합니다.
공개 업로드는 수업 뒤에 합니다. Pages 주소에서 한 번 더 확인합니다.
실명·학번·실제 이메일을 공개 파일과 캡처에 넣지 않습니다.

---

## 다음 주 인계

6주 작업 폴더는 이번 주 완성본으로 수업 전에 준비합니다.

- 세 HTML 페이지와 자체 CSS, 그림 유지
- greet(name)·hello(hour)·#greeting 이름 유지
- 제공 server.mjs 유지
- 정적 방명록은 입력 연습용이며 저장 기능 없음

6주는 클릭 이벤트와 횟수·다크 모드를 추가합니다.
[5주 완성 파일](examples/day2/web-week05/index.html)을 인계하며 시작 app.js와 혼동하지 않습니다.
