[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data)

# 5주차 실습 — 값을 바꿔 보고 마지막에 조립하기

이번 주 실습은 코드를 새로 쓰는 것이 아니라 **값을 바꿔 보는 것**이다.
비교 파일 10개(ex02 는 `.js` 파일까지 11개)를 내 저장소 `my-web/week05/` 에 저장하고, 값이나 주석 하나를 바꾼 뒤 결과가 어떻게 달라지는지 본다.
결과는 **화면과 F12 › Console 두 곳**에서 본다. Console 은 실습 내내 열어 둔다.
DevTools 는 탭마다 따로 열린다. 새 파일을 두 번 눌러 열면 새 탭이라 F12 를 다시 누른다. 열린 탭의 주소창에서 파일 이름만 바꿔 Enter 하면 Console 이 열린 채로 남는다.
2일차 끝에 그 부품으로 `my-web` 의 `index.html` 두 줄과 `app.js` 를 조립한다. 채점 대상은 2일차 캡처 1장이다.
`student01` 은 예시 아이디이므로 본인 아이디로 바꾼다.

파일을 받는 법, Console 을 여는 법, 값을 바꾸는 요령은 [따라하기 1일차](walkthrough.md#1일차)에 있다.
"바꿔 보기"는 **무엇이 달라질지 먼저 말해 보고** 저장 → 새로고침으로 확인한다.

## 1일차 — 스크립트와 값 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/student01/my-web.git` 뒤 **File › Open Folder**. `my-web` 안에 `week05` 폴더를 만들고 다섯 파일(ex01~ex05, ex02 는 `.js` 까지 여섯 개)을 **Raw** 로 저장한다. 5분 안에 다 못 받았으면 ex01 부터 시작하고, 나머지는 각 문항을 시작할 때 저장한다 |
| 5–15분 | ex01 지금 실행 vs 클릭할 때 실행 |
| 15–25분 | ex02 script 위치 |
| 25–35분 | ex03 let · const · var |
| 35–45분 | ex04 `+` |
| 45–52분 | ex05 템플릿 문자열 |
| 52–55분 | 확인: 여섯 파일이 `week05/` 에 있고, 각각 값 하나 이상을 바꿨는지. 일부러 낸 오류와 옮긴 줄은 되돌려 두었는지 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 `https://student01.github.io/my-web/week05/ex01_click.html` 새로고침 → 공용 PC면 자격 증명 삭제 |

### 1. ex01 지금 실행 vs 클릭할 때 실행 (`console.log` · `addEventListener`)

[examples/ex01_click.html](examples/ex01_click.html) 을 `week05/ex01_click.html` 로 저장한다. [따라하기 1일차](walkthrough.md#1일차)의 3단계(여는 법과 Console 여는 법)를 본다.

- 바꿔 보기: 파일을 열고 버튼을 누르기 전에 Console 을 본다. A·B·C·D 중 무엇이 찍혀 있나? `console.log('D. …')` 는 파일 맨 아래에 있는데 왜 B 보다 먼저 찍히나?
- 바꿔 보기: 이름 칸에 `student01` 을 넣고 1번·2번 버튼을 번갈아 두 번씩 누른다. B 와 C 는 각각 몇 번 찍히나? `function () {}` 로 쓴 1번과 `() => {}` 로 쓴 2번은 하는 일이 다른가?
- 바꿔 보기: `console.log('D. …');` 줄을 1번 버튼의 `{ }` 안, `output.innerText = …` 아래로 옮긴다. 이제 D 는 언제 찍히나? 확인했으면 D 줄을 원래 자리(맨 아래)로 되돌린다.
- 흔한 실수: `addEventListener` 줄에서 안쪽 코드가 바로 실행된다고 본다. 안쪽은 **등록만** 해 두고 클릭할 때마다 실행된다.

### 2. ex02 script 위치 (`<script>` · `defer`)

[examples/ex02_script_position.html](examples/ex02_script_position.html) 과 [ex02_script_position.js](examples/ex02_script_position.js) 를 둘 다 `week05/` 에 저장한다. 두 파일이 같은 폴더에 있어야 한다.

- 바꿔 보기: Console 에 찍힌 세 줄의 **순서**와 **값**을 읽는다. 1번만 `null`(찾은 것이 없다는 값)인 이유는 무엇인가? 3번 파일도 `<head>` 에서 연결했는데 왜 `p#msg`(id 가 `msg` 인 `p`)를 찾았나?
- Console 은 찍힌 요소를 **지금 모습**으로 보여 준다. 2번 줄 안의 글자가 3번이 바꾼 글자여도 2번이 먼저 실행된 것이다. 순서는 줄 순서와 오른쪽 `파일:줄` 로 본다.
- 바꿔 보기: head 안 `// document.getElementById('msg').innerText = 'head 에서 바꿈';` 의 `//` 를 지운다. 빨간 줄 오른쪽의 `파일:줄` 은 몇 번째 줄을 가리키나? 2번·3번 줄은 여전히 찍히나?
- 바꿔 보기: 위 주석을 되돌린 뒤, `<script src="ex02_script_position.js" defer></script>` 에서 `defer` 만 지운다. 3번 줄에 무엇이 찍히나? `p#msg` 글자는 바뀌나? 세 줄의 순서도 바뀌나? 바뀌었다면 왜인가?
- 흔한 실수: `.js` 파일을 저장하지 않았거나 다른 폴더에 저장했다. 그러면 Console 에 3번 줄이 없고, 파일을 못 불러왔다는 빨간 줄이 뜬다.

### 3. ex03 let · const · var (`let` · `const` · `var`)

[examples/ex03_let_const.html](examples/ex03_let_const.html) 을 `week05/ex03_let_const.html` 로 저장한다.

- 바꿔 보기: 파일을 열자마자 Console 에 빨간 줄이 있나? 2번 버튼을 누른 뒤에는? 오류는 언제 생기나?
- 바꿔 보기: 세 버튼을 두 번씩 누른다. 1번·3번 숫자는 어떻게 되나? 2번은 왜 `0` 에서 움직이지 않나? 빨간 줄의 `파일:줄` 이 가리키는 줄과 그 바로 아래 줄을 읽는다.
- 바꿔 보기: `const b = 0;` 의 `const` 를 `let` 으로 바꾼다. 2번 버튼이 어떻게 되나?
- 흔한 실수: "`const` 는 다시 담을 수 없으니 파일을 열 때 오류가 난다"고 본다. 오류는 **그 줄이 실행될 때** 나고, 오류 난 줄 아래는 실행되지 않는다.

### 4. ex04 +는 두 가지 일을 한다 (`+` · `Number()` · `parseInt()`)

[examples/ex04_plus.html](examples/ex04_plus.html) 을 `week05/ex04_plus.html` 로 저장한다.
표 셋째 칸의 `typeof 값` 은 그 값의 종류를 글자로 알려 준다. number 는 숫자, string 은 문자열이다.

- 바꿔 보기: 입력 칸 `1`·`2` 그대로 6번·7번 버튼을 누른다. 결과가 왜 다른가? 입력 칸을 `10`·`5` 로 바꿔 다시 누르면?
- 바꿔 보기: 3번 식 `'1' + 2` 를 결과 줄(30행)과 `typeof` 줄(31행) 둘 다 `1 + '2'` 로 바꾼다. 결과와 종류가 달라지나? 숫자가 앞에 있으면 더할까?
- 바꿔 보기: 5번의 `parseInt('12px')` 를 결과 줄(34행)과 `typeof` 줄(35행) 둘 다 `Number('12px')` 로 바꾼다. 무엇이 찍히나? 종류 칸은? `parseInt` 와 `Number` 는 `'12px'` 의 어디까지를 읽나?
- 식을 바꿀 때는 표 왼쪽 칸(3번은 14행, 5번은 16행의 `<td>`)의 글자도 같이 바꾼다. 그 칸은 HTML 글자라서 안 바꾸면 옛 식이 그대로 남아 식과 결과가 어긋나 보인다.
- 흔한 실수: 결과에 `NaN`(Not a Number)이 보이면 숫자로 바꾸지 못한 것이다. `NaN` 은 숫자로 바꾸지 못했다는 뜻의 특별한 숫자 값이라 `typeof` 는 number 로 나온다.
- 흔한 실수: 입력 칸 두 개를 그냥 `+` 로 더해 `12` 가 나온다. 입력 칸의 `value` 는 **늘 문자열**이다. `Number()` 로 바꾼 뒤 더한다.

### 5. ex05 템플릿 문자열 (`` ` `` · `${}`)

[examples/ex05_template.html](examples/ex05_template.html) 을 `week05/ex05_template.html` 로 저장한다.

- 바꿔 보기: `const name = 'student01';` 과 `const hour = 9;` 를 `'student02'` 와 `14` 로 바꾼다. 네 줄 중 어느 줄이 바뀌나? 3번은 왜 안 바뀌나?
- 바꿔 보기: 3번 줄 `'안녕하세요, ${name}님!'` 의 작은따옴표 두 개를 백틱으로 바꾼다. 3번이 어떻게 되나?
- 바꿔 보기: 4번 줄 `${hour + 1}` 을 `${hour} + 1` 로 바꾼다. 무엇이 보이나? `+ 1` 은 어디서 계산되고 어디서 글자가 되나?
- 흔한 실수: 백틱 대신 작은따옴표를 쓴다. 백틱은 키보드 `1` 왼쪽, `Esc` 아래 키다. 그 키를 쳤는데 다른 글자(macOS 한글 입력이면 `₩`)가 들어가면 영문 입력으로 바꾼 뒤 다시 친다.

오늘 push 는 확인용이다. 공개 주소 `https://student01.github.io/my-web/week05/ex01_click.html` 이 열리고 Console 에 A·D 가 찍히면 된 것이다. 제출은 2일차에 캡처 한 장만 한다.

## 2일차 — 조건과 함수, 그리고 조립 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/student01/my-web.git` 뒤 **File › Open Folder**. 다섯 파일(ex06~ex10)을 **Raw** 로 `week05/` 에 먼저 저장한다. 5분 안에 다 못 받았으면 ex06 부터 시작하고, 나머지는 각 문항을 시작할 때 저장한다 |
| 5–11분 | ex06 비교 |
| 11–17분 | ex07 if / else |
| 17–23분 | ex08 function |
| 23–29분 | ex09 화면에 쓰기 |
| 29–33분 | ex10 new Date() |
| 33–48분 | 조립: `index.html` 에 두 줄, `app.js` 를 비우고 조립표 순서로 쓰기 → commit·push |
| 48–55분 | 되돌리기 두 가지(채점 안 함): 저장만 한 잘못은 `git restore app.js`, commit 한 잘못은 `git revert HEAD` |
| 55–60분 | 끝 루틴: `git push` → 공개 주소에서 Console 을 연 **캡처 1장** → 공용 PC면 자격 증명 삭제 |

다섯 파일을 받는 법과 조립 전문은 [따라하기 2일차](walkthrough.md#2일차)에 있다.
파일마다 **코드를 고치는 바꿔 보기를 하나 이상** 하고 넘어간다. 조립과 이어지는 것(ex08 `${greet()}`, ex09 `#p9`, ex10 `new Date().getHours()`)을 각 문항 맨 앞에 두었다. 33분이 되면 남은 것은 두고 조립을 시작한다. 조립 전에 고친 `week05/` 파일은 조립 commit 에 함께 들어가도 된다. 남은 바꿔 보기는 12번 되돌리기까지 끝낸 뒤 한다.

### 6. ex06 비교 (`==` · `===` · `>=` · `>`)

[examples/ex06_compare.html](examples/ex06_compare.html) 을 `week05/ex06_compare.html` 로 저장한다.

- 바꿔 보기: 열기 전에 여섯 식의 결과를 `true`·`false` 로 먼저 말해 본다. 몇 개가 맞았나? 1번과 2번은 왜 다른가?
- 바꿔 보기: 5번 식 `'10' > '9'`(25행)를 `'2' > '10'` 으로 바꾼다. 표 왼쪽 칸(16행 `<td>`)의 식 글자도 같이 바꾼다. 숫자라면 `false` 인데 결과는? 문자열은 무엇부터 비교하나?
- 바꿔 보기: 3번 `12 >= 12` 와 4번 `12 > 12` 는 숫자가 같은데 결과가 왜 다른가? 23·24행 식의 앞 숫자를 `13` 으로 바꾸고 표 왼쪽 칸(14·15행 `<td>`)도 같이 바꾸면? 12시 정각에 `hour >= 12` 는 참인가, `hour > 12` 는?
- 흔한 실수: `=` 와 `===` 를 같은 것으로 본다. `=` 는 담는 것, `===` 는 같은지 비교하는 것이다. `if (hour = 12)` 는 비교가 아니라 12 를 담는다. 담은 12 가 참으로 읽혀 늘 그 갈래로 간다(`my-web` 의 `hello` 라면 9시에도 오후). 오류가 나지 않으니 화면과 Console 숫자를 비교해 찾는다.

### 7. ex07 if / else (`if` · `else if` · `else`)

[examples/ex07_if_else.html](examples/ex07_if_else.html) 을 `week05/ex07_if_else.html` 로 저장한다.

- 바꿔 보기: 입력 칸에 `9`·`12`·`15`·`20` 을 차례로 넣고 **판단하기**를 누른다. 3번과 4번이 다르게 나오는 시각은 어느 것인가? 조건은 같은데 왜 다른가?
- 바꿔 보기: 4번의 `m4 = '저녁';` 옆 주석은 "이 줄에는 영영 오지 못한다"이다. 0~23 중 그 줄에 오는 값이 있나? 없다면 왜인가? 4번이 `저녁` 을 내려면 조건 두 줄을 어떻게 바꿔야 하나?
- 바꿔 보기: 1번의 `let m1 = '(담긴 것 없음)';` 을 `let m1;` 으로 바꾸고 `9` 를 넣는다. 1번 자리에 무엇이 보이나? 그 글자는 무슨 뜻일까? 25행 `let m2;` 도 값 없이 만든 변수다. 같은 글자를 ex08 에서 다시 본다.
- 흔한 실수: `if` 사슬에서 작은 기준(`>= 12`)을 먼저 쓴다. 위에서부터 **처음 참인 한 곳만** 실행되므로 큰 기준(`>= 18`)이 먼저 와야 한다.

### 8. ex08 function (`function` · `return`)

[examples/ex08_function.html](examples/ex08_function.html) 을 `week05/ex08_function.html` 로 저장한다.
괄호 안 `name` 은 부를 때 넣은 값을 받는 이름이다(**매개변수**). `greet('student02')` 로 부르면 그 안의 `name` 에 `'student02'` 가 담긴다.
`undefined` 는 아직 담긴 값이 없다는 값이다. 값 없이 만든 변수(ex07 의 `let m1;`)도, `return` 이 없는 함수를 부른 결과도 `undefined` 다.

- 바꿔 보기: 33행 `= greet('student02');` 의 오른쪽을 `` `${greet('student02')} 반가워요` `` 로 바꾼다(끝의 `;` 는 둔다). `${}` 안에서 함수를 불러도 되나? 화면 3번 첫 칸은 어떻게 되나? 조립의 `message` 줄이 이 모양이다.
- 바꿔 보기: 화면 1번과 2번은 왜 다른가? Console 에 찍힌 한 줄은 어느 함수에서 나왔나? 2번 문장은 왜 Console 에 없나?
- 바꿔 보기: `greetLog` 안의 `console.log('안녕하세요, ' + name + '님!');` 을 `return '안녕하세요, ' + name + '님!';` 으로 바꾼다. 화면 1번과 Console 이 각각 어떻게 달라지나?
- 바꿔 보기: `const a = greetLog('student01');` 줄 위에 `neverCalled();` 한 줄을 더한다. Console 에 무엇이 더 찍히나? 더하기 전에는 왜 없었나?
- 흔한 실수: 함수를 정의만 하고 부르지 않는다. 정의는 이름을 붙여 두기만 한다. `greet('student01')` 처럼 **괄호를 붙여 불러야** 실행된다.

### 9. ex09 화면에 쓰기 (`querySelector` · `textContent` · `value`)

[examples/ex09_dom_write.html](examples/ex09_dom_write.html) 을 `week05/ex09_dom_write.html` 로 저장한다.

- 바꿔 보기: `console.log(document.querySelector('#p9'));` 줄(23행) 아래에 `document.querySelector('#p9').textContent = '9';` 한 줄을 더한다. 빨간 줄은 무엇이라고 하나? 그 뒤에 **바꾸기** 버튼은 동작하나? 조립 마지막 줄에서 id 를 틀리면 이 빨간 줄이 뜬다. 확인했으면 더한 줄을 지운다. 남겨 두면 다음 바꿔 보기에서 바꾸기 버튼이 동작하지 않는다.
- 바꿔 보기: **바꾸기**를 누르기 전에 Console 두 줄을 읽는다. 둘째 줄이 `null` 인 이유는 무엇인가? 버튼을 누른 뒤 3번에 `<b>` 가 굵게 되나, 글자로 보이나?
- 바꿔 보기: 26행 `p1.innerText` 를 `p1.textContent` 로 바꾼다. 1번 화면이 달라지나? 글자만 바꿀 때 두 방법의 결과가 같은지 이것으로 확인한다.
- 바꿔 보기: 18행 `document.querySelector('#p2')` 를 `document.querySelector('#p3')` 으로 바꾼다. Console 첫 줄의 둘째 요소가 p3 로 바뀌었는지 먼저 본다. 버튼을 누르면 2번은 왜 그대로인가? 27행이 쓴 글자는 어디로 갔나?
- 흔한 실수: `getElementById('#p1')` 처럼 `#` 을 붙이거나 `querySelector('p2')` 처럼 `#` 을 빠뜨린다. 둘 다 `null` 이 된다. `querySelector` 는 CSS 선택자를 받는다(4주차 ex01 의 `.red`·`nav a` 와 같은 글자). `#` 은 id 를 뜻해서, id 로 찾을 때는 앞에 `#` 을 붙인다 — 2주차 `app.js` 의 `querySelector('#count-button')` 모양. `getElementById` 는 이름부터 'id 로 찾기'라서 id 글자만 받는다.

### 10. ex10 new Date() (`new Date()` · `getHours()`)

[examples/ex10_date.html](examples/ex10_date.html) 을 `week05/ex10_date.html` 로 저장한다.

- 바꿔 보기: 25행 `now.getHours()` 를 `new Date().getHours()` 로 바꾼다. 1번 숫자가 바꾸기 전과 같은가? 조립의 `hour` 줄이 이 모양이다.
- 바꿔 보기: 표 여섯 줄을 오늘 날짜·시각과 맞춰 본다. 4번과 5번은 왜 1 차이가 나나? 6번 숫자는 무슨 요일인가?
- 바꿔 보기: 1분 기다렸다가 새로고침한다. 무엇이 바뀌나? 파일을 고치지 않았는데 왜 바뀌나?
- 바꿔 보기: 마지막 `innerText` 줄 아래에 `console.log(now.getSeconds());` 한 줄을 더한다. 새로고침할 때마다 Console 이 어떻게 되나?
- 흔한 실수: `getMonth()` 를 그대로 월로 쓴다. 월은 0부터 센다. 사람이 읽는 월은 `getMonth() + 1` 이다.

### 11. 조립 — my-web `index.html` 두 줄과 `app.js` (`defer` · `id="greeting"`)

이제 `week05/` 가 아니라 `my-web` 맨 위의 `index.html`·`app.js` 를 연다. 전문과 단계는 [따라하기 2일차](walkthrough.md#2일차)에 있다.

- `index.html` 의 `<head>` 에서 `<link rel="stylesheet" href="styles.css">` 아래에 `<script src="app.js" defer></script>` 한 줄을 넣는다.
- `<main>` 첫 줄에 `<p class="card" id="greeting">인사말을 준비 중입니다.</p>` 한 줄을 넣는다. JavaScript 가 이 자리에 오지 못하면 이 글자가 그대로 남는다.
- `app.js` 는 **전부 지운다.** 2주차 카운터 코드가 남아 있다. 그 버튼은 3주차에 사라져서 남겨 두면 `null` 오류가 난다.
- 그다음 아래 조립표 순서로 `app.js` 를 쓴다. 줄마다 "어느 ex 에서 본 것"인지 적혀 있다.

| my-web 의 줄 | 어느 ex 에서 본 것 |
|---|---|
| `index.html` `<head>` 의 `<script src="app.js" defer></script>` | ex02 3번 (`defer`: HTML 을 다 읽은 뒤 실행 → `#greeting` 을 찾을 수 있다) |
| `index.html` 의 `<p class="card" id="greeting">인사말을 준비 중입니다.</p>` | ex09 (찾을 자리에 `id`), 4주차 ex01 (클래스 선택자, `.red` 와 같은 원리), `.card` 규칙은 4주차 `styles.css` |
| `const name = 'student01';` | ex03 (`const`) |
| `const hour = new Date().getHours();` | ex10 (지금 시각 → 시) + ex03 |
| `` function greet(name) { return `안녕하세요, ${name}님!`; } `` | ex08 (정의·`return`) + ex05 (템플릿 문자열) |
| `function hello(hour) { if (hour >= 12) { return … } else { return … } }` | ex07 (`if / else`) + ex06 (`>=`) + ex08 (`return`) |
| `` const message = `${greet(name)} ${hello(hour)}`; `` | ex05 (`${}` 안은 계산된다 — 함수 호출도) + ex08 (호출) |
| `console.log(hour);` `console.log(message);` | ex01 (Console) |
| `document.querySelector('#greeting').textContent = message;` | ex09 2번 (찾고 → 바꾼다) |

ex09 1번 모양(`getElementById('greeting').innerText`)으로 써도 결과가 같다. 교재가 2번을 쓰는 이유는 `querySelector` 가 4주차 CSS 선택자(`#id`·`.class`)를 그대로 받기 때문이다.

- 확인: 저장하고 `index.html` 을 새로고침한다. 카드 한 줄에 `안녕하세요, student01님! 좋은 아침입니다.`(또는 `좋은 오후입니다.`)가 보이고, Console 에 시각 숫자와 같은 문장 두 줄이 찍히면 된 것이다.
- 확인이 끝나면 `git add .` → `git commit -m "함수로 인사말 만들어 화면에 표시"` → `git push` 로 **먼저 올린다.** 12번 되돌리기가 이 commit 을 기준으로 한다.
- 바꿔 보기: 12시 전후 두 갈래는 12번 ① 에서 본다. 2행을 `9`·`15` 로 바꿔 두 갈래를 본 뒤 `git restore app.js` 로 되돌린다.
- 흔한 실수: `script` 줄에서 `defer` 를 빠뜨린다. ex02 에서 `defer` 를 지운 것과 같은 일이 일어난다. `#greeting` 을 찾기 전에 `app.js` 가 실행된다.

### 12. 되돌리기 두 가지 (`git restore` · `git revert`)

되돌리기는 채점하지 않는다. 55분이 되면 push·캡처가 먼저다. ② 를 시작했으면 `git revert HEAD` 까지 끝낸 뒤 push 한다.
11번 commit 이 끝난 상태에서 한다. [따라하기 2일차](walkthrough.md#2일차)의 되돌리기 단계를 본다.

- **① 저장만 한 잘못** — `app.js` 2행을 `const hour = 9;` 로 바꾸고 저장한다. 9 와 15 를 차례로 넣어 카드를 본 뒤(어느 ex 의 결과와 같은가?) commit 하지 않는다. 터미널에서 `git restore app.js` 를 친다. VS Code 탭의 2행이 어떻게 되나?
- **② commit 한 잘못** — `app.js` 5행 문장을 `` return `반갑습니다, ${name}님!!!`; `` 처럼 다른 문구로 바꾸고([따라하기 2일차](walkthrough.md#2일차) 13단계) `git add app.js` → `git commit -m "인사말 문구 바꾸기"` 까지 한다. 그다음 `git revert HEAD` 를 친다. 편집기 창이 뜨면 기본 메시지 `Revert "…"` 그대로 저장하고 닫는다.
- 바꿔 보기: `git log --oneline` 을 친다. `인사말 문구 바꾸기` 와 `Revert "인사말 문구 바꾸기"` 가 둘 다 남아 있나? `restore` 와 달리 `revert` 는 왜 기록이 하나 더 생기나?
- 먼저 commit 해야 되돌리기가 문구 한 줄만 되돌린다(`1 file changed, 1 insertion(+), 1 deletion(-)`). 11번 commit 을 건너뛰면 오늘 조립 전체가 되돌아간다.
- commit 전에 `git restore app.js` 를 치면 조립한 `app.js` 가 통째로 마지막 commit(2주차 카운터)으로 덮이고 되살릴 수 없다. 그래서 11번 commit 이 먼저다.
- `git reset HEAD^` 는 기록 자체를 지운다. push 한 commit 을 지우면 내 PC 기록이 GitHub 기록과 어긋나 다음 `git push` 가 거부(rejected)된다. 그래서 push 한 뒤에는 기록을 더하는 `revert` 를 쓴다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 다시 확인해도 된다. `git status`에 `Your branch is ahead`가 있으면 push를 안 한 것이다 |
| 화면이 생각과 다른데 이유를 모르겠다 | **Console 을 먼저 연다.** 빨간 줄 오른쪽 `파일:줄` 로 간다. 오류 난 줄 아래는 실행되지 않으므로 그 줄부터 본다 |
| Console 에 내가 쓴 `console.log` 줄이 하나도 없다 | ① 줄이 정말 하나도 없으면 `index.html`에 `<script src="app.js" defer></script>`가 없다. ② `Failed to load resource` 줄이 있으면 파일 이름 철자가 틀린 것이다. `app.js` 안의 오류가 아니라 **파일을 못 불러왔다**는 줄이다(공개 주소에서는 `404`, `file://`에서는 `net::ERR_FILE_NOT_FOUND`). ex02 는 `.js` 파일이 같은 `week05/` 폴더에 있는지 본다. 파일을 저장했는지도 본다 |
| `Uncaught ReferenceError: nmae is not defined` | 없는 이름을 썼다. 오른쪽 `파일:줄`의 줄로 가 철자를 고친다 |
| `Uncaught ReferenceError: helo is not defined` | 함수 이름 오타다. 정의한 이름(`hello`)과 부른 이름을 비교한다 |
| `Uncaught SyntaxError: Unexpected end of input` | 백틱이나 중괄호를 닫지 않았다. 문장 끝의 `` ` ``와 `}`를 세어 본다. 닫지 않은 백틱 **뒤에 백틱이 더 있으면** `Uncaught SyntaxError: Unexpected identifier '…'`로 나온다. 어느 쪽이든 백틱 짝부터 센다. SyntaxError 는 그 파일의 한 줄도 실행하지 않아 `console.log` 도 안 찍힌다. 표시된 줄보다 위를 본다 |
| `Uncaught SyntaxError: missing ) after argument list` | 괄호를 닫지 않았다. `console.log(greet('student01'));`처럼 괄호 짝을 맞춘다 |
| `Uncaught TypeError: Assignment to constant variable.` | `const`로 만든 값에 다시 넣었다. 다시 넣어야 하면 `let`으로 만든다. ex03 의 2번 버튼은 일부러 이 오류를 보이는 것이다 |
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` | `my-web` 의 `app.js`에 2주차 카운터 코드가 남아 있다. 그 버튼은 3주차에 사라졌다. [따라하기 2일차](walkthrough.md#2일차)처럼 전체를 지우고 조립표 순서로 새로 쓴다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'innerText')` | ex02 에서 head 주석을 풀었거나 `defer` 를 지웠다. 그 script 가 실행될 때 `p#msg` 를 아직 읽지 않아 `null` 이다. 확인했으면 되돌린다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` | `#greeting`을 못 찾았다. `id="greeting"` 철자, 그리고 `script` 줄에 `defer`가 있는지 본다. ex09 에서는 없는 id(`#p9`)에 쓴 것이다 |
| 더했는데 `3` 이 아니라 `12` 가 나온다 | 문자열을 이은 것이다. 입력 칸의 `value` 는 늘 문자열이다. `Number()` 로 바꾼 뒤 더한다(ex04 7번) |
| Console에 `${name}`이 글자 그대로 찍힌다 | 작은따옴표로 감쌌다. 백틱(`` ` ``)으로 바꾼다. 백틱 자리에 다른 글자가 들어가지 않았는지도 본다 |
| 백틱을 쳤는데 다른 글자(macOS 한글 입력이면 `₩`)가 들어간다 | 입력 상태가 한글이다. 영문 입력으로 바꾼 뒤(Windows 는 한/영 키, macOS 는 Caps Lock 이나 Ctrl+Space) `1` 왼쪽 키를 다시 친다. `₩` 가 들어간 채 저장하면 `Uncaught SyntaxError: Invalid or unexpected token` 이 뜬다 |
| 함수 결과가 `undefined`로 찍힌다 | 함수 안에 `return`이 없다. `console.log`는 찍기만 하고 값을 돌려주지 않는다 |
| 화면에 `인사말을 준비 중입니다.`가 그대로 있다 | 마지막 줄까지 가지 못했다. Console의 첫 빨간 줄을 고친 뒤 새로고침한다 |
| 인사말이 `좋은 오후입니다.`로 나온다 | 12시가 지나서 연 것이며 정상이다. 두 갈래 모두 정답이다 |
| 공개 주소 `…/my-web/week05/ex01_click.html` 이 404 다 | ① 폴더 이름이 `week05` 인지(`Week05`·`week5` 는 다른 이름) ② 파일 이름이 교재와 같은지 ③ `git push` 를 했는지 `git status` 로 본다 |
| `git revert HEAD` 뒤 편집기 창이 열려 멈춰 있다 | 기본 메시지를 그대로 두고 저장한 뒤 창을 닫는다(VS Code는 탭을 닫으면 된다). 그러면 터미널에 `[main …] Revert "…"`가 나온다 |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시와 `git log --oneline`을 본다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://student01.github.io/my-web/` (본인 아이디) 을 열고 **F12 › Console** 을 켠 채로 한 화면을 캡처한다.

- 카드 한 줄에 `안녕하세요, student01님! 좋은 아침입니다.`(또는 `좋은 오후입니다.`)가 보인다. 12시 이후면 `좋은 오후입니다.` 가 정답이다.
- Console 에 `console.log` 두 줄(시각 숫자와 같은 문장)이 찍혀 있고 빨간 줄이 없다.
- **주소창이 함께 보이게** 찍는다.

2일차를 끝내지 못했다면 `https://student01.github.io/my-web/week05/ex01_click.html` 을 열고 1번 버튼을 누른 뒤, Console 에 A·D·B 가 찍힌 화면을 대신 낸다.
1일차 push 와 `week05/` 실험 파일은 확인용이며 따로 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- ex04: 표 아래 입력 칸 두 개와 7번 버튼처럼 `−`·`×`·`÷` 버튼 세 개를 더한다. 식에서는 `-`·`*`·`/` 를 쓴다. 7번 버튼처럼 `Number()` 로 바꿔야 하나? 빼기도 `12` 처럼 이어 붙을까?
- ex07: 3번에 "새벽"(`hour < 6`) 갈래를 더한다. 사슬 맨 위에 넣을 때와 맨 아래 `else` 바로 위에 넣을 때, `3` 을 넣은 결과를 비교한다. 4번처럼 순서가 결과를 바꾸나? 왜 그런가?
- ex10 + ex07: `now.getDay()` 가 `0` 이면 "일요일", 아니면 "평일" 을 화면에 보이게 한다.
- ex08: `greet` 에 두 번째 매개변수(함수 괄호 안에서 받는 값의 이름. `greet(name)` 의 `name`) `hour` 를 더해 `안녕하세요, student01님! 지금은 9시입니다.` 를 돌려주게 한다. 부르는 쪽 괄호에는 무엇을 더 넣어야 하나?

추가 과제는 선택 사항이며 채점하지 않는다.
