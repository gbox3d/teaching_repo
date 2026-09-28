# 5주차 따라하기 — 비교 예제로 원리를 보고 마지막에 조립

이번 주 실습은 코드를 새로 짜는 것이 아니라 **값을 바꿔 보는 것**이다.
비교 파일을 내 저장소 `my-web/week05/`에 저장하고, 값·주석을 바꾼 뒤 결과를 **화면과 Console 두 곳**에서 본다.
`my-web`의 `index.html`·`app.js`는 2일차 끝에 부품에서 **조립**한다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

비교 파일 10개는 [교재 저장소의 examples 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data/examples)에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다.

## 1일차

### 1. week05 폴더 만들기

지난주에 쓰던 PC라면 폴더를 열고 새 commit만 받아 온다. 현재 폴더: `my-web`

```bash
git pull
```

처음 쓰는 PC라면 저장소를 통째로 내려받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

이어서 `my-web` 안에 `week05` 폴더를 만든다. VS Code 탐색기에서 **New Folder**를 눌러도 되고, 명령으로 만들어도 된다. 현재 폴더: `my-web`

```bash
mkdir week05
```

**예상 결과** — `git pull`은 집에서 push한 것이 없으면 `Already up to date.` 한 줄이다.
`my-web` 안에 `index.html`·`about.html`·`guestbook.html`·`styles.css`·`app.js`·`images/`·`week04/`와 나란히 빈 `week05/` 폴더가 보인다.

- 폴더 이름은 `week05`다. `Week05`·`week5`로 만들면 공개 주소가 달라져 5단계에서 404가 난다.
- 빈 폴더는 Git이 올리지 않는다. 2단계에서 파일을 넣으면 함께 올라간다.
- `my-web`의 `index.html`·`app.js`는 오늘 건드리지 않는다. 2일차 끝에 조립한다.

### 2. 비교 파일 가져오기

오늘 파일은 다섯 개다. `ex02`만 보조 파일 `.js`가 하나 더 있어서 모두 **여섯 개**를 받는다.
각 파일은 개념 하나만 비교한다.

| 파일 | 비교하는 것 |
|---|---|
| [ex01_click.html](examples/ex01_click.html) | 열자마자 실행(A·D) / 클릭할 때 실행(B·C), `function () {}` / `() => {}` |
| [ex02_script_position.html](examples/ex02_script_position.html) + [ex02_script_position.js](examples/ex02_script_position.js) | `script` 위치: head 안 / body 끝 / head에 `defer`로 연결한 파일 |
| [ex03_let_const.html](examples/ex03_let_const.html) | `let` / `const` / `var`에 1 더하기 |
| [ex04_plus.html](examples/ex04_plus.html) | `+`: 숫자 + 숫자 / 문자열 + 문자열 / 섞인 것 / `Number()`·`parseInt()`로 바꾼 것, 입력 칸 두 개 |
| [ex05_template.html](examples/ex05_template.html) | `+`로 잇기 / 백틱 템플릿 / 작은따옴표 안의 `${}` / `${}` 안의 계산 |

가져오는 방법은 둘 중 하나다.

1. **Raw로 저장** — [교재 저장소 examples 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data/examples)에서 파일을 누르고 오른쪽 위 **Raw**를 누른다. 코드만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `my-web/week05/`에 저장한다. 파일 이름은 교재와 **같게** 둔다.
2. **타이핑** — Raw가 열리지 않을 때만 쓴다. VS Code에서 `week05/ex01_click.html`을 새로 만들고 교재 화면을 보며 친다. 1일차 파일은 25~49줄이다. **주석 줄도 그대로 친다.** 주석에 원리와 실험 거리가 있고(ex02 11행처럼 `//`를 지워 실험하는 줄), 줄 번호가 교재와 같아야 오류 줄의 `파일:줄`을 교재와 맞춰 볼 수 있다.

`ex02`는 `ex02_script_position.html`과 `ex02_script_position.js`를 **둘 다** 받아 **같은 폴더**에 둔다.
HTML의 `<script src="ex02_script_position.js" defer>`가 같은 폴더에서 그 이름을 찾기 때문이다.

**예상 결과** — `week05/` 안에 파일 여섯 개가 있다.

```text
week05/
  ex01_click.html
  ex02_script_position.html
  ex02_script_position.js
  ex03_let_const.html
  ex04_plus.html
  ex05_template.html
```

- 저장한 파일 이름이 `ex01_click.html.txt`처럼 `.txt`로 끝나면 이름을 고친다. 브라우저가 붙인 것이다. 이름은 VS Code 탐색기에서 확인한다(Windows 파일 탐색기는 기본 설정에서 확장자를 숨긴다).
- `.js` 파일을 빠뜨리면 `ex02`를 열었을 때 Console에 3번 줄이 없고 `net::ERR_FILE_NOT_FOUND` 줄이 뜬다. 파일을 못 불러왔다는 뜻이다.
- 시작 5분 안에 여섯 파일을 다 받아 둔다. 5분 안에 다 못 받았으면 ex01 부터 시작하고, 나머지는 각 문항을 시작할 때 받는다.

### 3. 여는 법과 Console 여는 법

저장한 파일은 VS Code 탐색기에서 오른쪽 클릭 › **Reveal in File Explorer**(macOS는 **Reveal in Finder**)로 찾아 두 번 눌러 Chrome으로 연다.
`ex01_click.html`을 연다.
기본 브라우저가 Chrome이 아니면 파일을 Chrome 창에 끌어다 놓는다(Safari는 F12로 Console이 열리지 않는다).
`.js` 파일은 두 번 누르지 않는다. 브라우저에서 여는 것은 `.html`이고, `.js`는 `.html`이 불러온다.

**예상 결과** — 제목 `ex01 지금 실행 vs 클릭할 때 실행`, 이름 칸 하나, 버튼 두 개(`1. function 으로`·`2. 화살표로`), 그 아래 `버튼을 눌러 보세요`가 보인다.

이제 결과를 보는 두 번째 자리, **Console**을 연다.

1. 화면에서 오른쪽 클릭 › **검사**를 누른다. 또는 **F12**(노트북에서 안 열리면 **Fn+F12**, macOS는 ⌘+Option(⌥)+I).
2. DevTools 위쪽 탭에서 **Console**을 누른다.
3. 줄이 잘 안 보이면 DevTools 오른쪽 위 **⋮ › Dock side**에서 아래쪽 도킹을 고른다.

**예상 결과** — Console에 두 줄이 이미 찍혀 있다. 줄 오른쪽 끝에 `ex01_click.html:17`처럼 **파일 이름:줄 번호**가 보인다.

```text
A. 페이지를 열자마자 실행된다          ex01_click.html:17
D. A 바로 다음에 실행된다. B·C 보다 먼저   ex01_click.html:34
```

이름 칸에 `student01`을 치고 1번 버튼, 2번 버튼을 차례로 누른다.

**예상 결과** — 버튼을 누를 때마다 Console에 한 줄씩 늘어난다(1번은 `B. …`, 2번은 `C. …`).
화면 글자는 `student01님 (function)` → `student01님 (화살표)`로 바뀐다.
**새로고침**(F5, macOS는 ⌘+R)하면 Console이 지워지고 A·D 두 줄만 다시 찍힌다. 화면 글자도 `버튼을 눌러 보세요`로 돌아온다.

- 파일은 위에서 아래로 **한 번** 실행된다. 그래서 A 다음이 D다. `addEventListener` 안쪽(B·C)은 이때 **등록만** 해 두었다가 클릭할 때마다 실행된다.
- `function () {}`와 `() => {}`는 여기서 같은 일을 한다. 둘 다 "클릭하면 할 일"을 적은 것이다.
- 19~22행은 화면의 요소를 id로 찾아 이름을 붙여 두는 줄이다. `document`는 이 페이지 전체이고, 그 안에서 id로 찾는다. `var`는 ex03, `getElementById`와 `innerText`는 ex09, `.value`는 ex04에서 비교한다.
- 같은 줄이 연달아 찍히면 Console은 한 줄로 묶고 왼쪽에 `2`·`3` 같은 숫자를 붙인다. 버튼을 두 번 눌렀는데 줄이 하나면 그 숫자를 본다.
- 새로고침하면 Console도 새로 찍힌다. 실험 전후를 비교하려면 새로고침 직후의 Console을 본다.

### 4. 값 바꾸는 요령

실험은 늘 같은 순서다. **VS Code에서 고치고 저장**(Ctrl+S, macOS는 ⌘+S) → **브라우저에서 새로고침**(F5, macOS는 ⌘+R) → **화면과 Console**을 본다.
바꾸기 전에 무엇이 달라질지 먼저 말해 보고 확인한다.

**값 바꾸기** — `ex05_template.html`을 열고 17행 `const hour = 9;`를 `const hour = 13;`으로 바꾼 뒤 저장하고 새로고침한다.

**예상 결과** — 1·2번 문장이 `지금은 13시입니다.`로, 4번이 `한 시간 뒤는 14시입니다.`로 바뀐다. 3번은 `안녕하세요, ${name}님!` 그대로다.
3번만 작은따옴표로 감싸서 `${}`를 계산하지 않고 글자로 둔다.

**오류 읽기** — `ex02_script_position.html`을 열고 11행 맨 앞의 `// `를 지운다. 주석을 풀면 그 줄이 실행된다. 저장하고 새로고침한다.

**예상 결과** — Console에 빨간 줄이 하나 생긴다.

```text
1. head 안 script : null                                                  ex02_script_position.html:9
Uncaught TypeError: Cannot set properties of null (setting 'innerText')     ex02_script_position.html:11
2. body 끝 script : <p id="msg">…</p>                                       ex02_script_position.html:23
3. defer 로 연결한 파일 : <p id="msg">…</p>                                  ex02_script_position.js:2
```

빨간 줄 오른쪽의 `ex02_script_position.html:11`이 고칠 자리다. VS Code에서 11행으로 간다.
head 안의 스크립트는 브라우저가 그 줄을 **읽는 순간** 실행된다. 그때 아래 `<p id="msg">`는 아직 읽지 않았으니 찾으면 `null`이다. `null`은 '찾은 것이 없다'는 값이다. 없는 것의 글자는 바꿀 수 없어서 오류가 난다.
확인했으면 `// `를 다시 붙여 되돌린다.

- 저장(Ctrl+S, macOS는 ⌘+S) → 새로고침(F5, macOS는 ⌘+R). 이 두 동작을 한 쌍으로 익힌다. 저장을 안 하면 화면이 안 바뀐다. VS Code 탭 제목의 ● 표시는 저장 안 됨이다.
- CSS는 틀려도 조용히 무시됐다(4주차). JavaScript는 문법이 틀리거나 없는 것을 쓰면 **Console에 빨간 줄**이 뜬다. 결과만 다른 경우(ex04의 `12`)는 조용하다. 그래서 화면과 Console을 둘 다 본다. 빨간 줄이 있으면 오른쪽의 `파일:줄`로 간다.
- 오류 난 스크립트 덩어리는 그 줄에서 멈춘다. 위 예에서도 1번 `script`만 멈췄고, 2번·3번은 따로 있는 `script`라 제 할 일을 했다.
- 값을 원래대로 못 돌리겠으면 파일을 다시 받거나, 5단계 뒤라면 `git restore week05/ex02_script_position.html`로 마지막 commit 상태로 되돌린다.
- 파일마다 무엇을 바꿔 볼지는 [1일차 실습](lab.md#1일차--스크립트와-값-60분)에 있다.

### 5. push와 공개 주소 확인

다섯 파일에서 각각 값 하나 이상을 바꿔 봤으면 올린다. 현재 폴더: `my-web`

```bash
git add .
git commit -m "5주차 비교 파일 다섯 개 실험"
git push
```

**예상 결과** — `git commit`이 아래처럼 찍는다. 새 파일마다 `create mode` 줄이 하나씩 붙는다.

```text
[main 3c8e5a1] 5주차 비교 파일 다섯 개 실험
 6 files changed, 183 insertions(+)
 create mode 100644 week05/ex01_click.html
 create mode 100644 week05/ex02_script_position.html
 create mode 100644 week05/ex02_script_position.js
 create mode 100644 week05/ex03_let_const.html
 create mode 100644 week05/ex04_plus.html
 create mode 100644 week05/ex05_template.html
```

1분쯤 뒤 `https://student01.github.io/my-web/week05/ex01_click.html`을 연다. F12 › **Console**을 열면 로컬에서 본 것과 같이 A·D 두 줄이 찍혀 있다. 이 화면은 **확인용**이다.
공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 앞의 일곱 글자는 PC마다 다르다. 값을 바꾼 만큼 줄 수도 달라진다. 파일 수가 6인지만 본다.
- 404가 나면 주소의 `week05/`와 파일 이름이 폴더·파일 이름과 글자 단위로 같은지, `git push`가 끝났는지 본다.
- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.

## 2일차

### 6. 비교 파일 다섯 개 가져오기

먼저 새 commit을 받아 온다. 현재 폴더: `my-web`

```bash
git pull
```

오늘 파일은 다섯 개다. 2단계의 **Raw** → 저장으로 `my-web/week05/`에 넣는다(파일이 29~57줄이라 타이핑은 시간 안에 못 끝낸다). 시작 5분 안에 다섯 개를 다 받아 둔다. 5분 안에 다 못 받았으면 ex06부터 시작하고, 나머지는 각 문항을 시작할 때 받는다.

| 파일 | 비교하는 것 |
|---|---|
| [ex06_compare.html](examples/ex06_compare.html) | `==` / `===`, `>=` / `>`, 문자열끼리 비교 / 숫자로 바꿔 비교 |
| [ex07_if_else.html](examples/ex07_if_else.html) | `if`만 / `if` · `else` / `if` · `else if` · `else` / 같은 조건을 순서만 거꾸로 |
| [ex08_function.html](examples/ex08_function.html) | `return` 없는 함수 / `return` 하는 함수 / 같은 함수에 다른 값 / 정의만 하고 부르지 않은 함수 |
| [ex09_dom_write.html](examples/ex09_dom_write.html) | `getElementById` + `innerText` / `querySelector` + `textContent` / 태그를 넣은 글자 / 입력 칸 `value` |
| [ex10_date.html](examples/ex10_date.html) | `new Date()`의 `getHours()` · `getMinutes()` · `getFullYear()` · `getMonth()` · `getDay()` |

**예상 결과** — 다섯 개를 다 받으면 `week05/`에 파일이 열한 개 있다(1일차 여섯 + 오늘 다섯).
`ex06_compare.html`을 열면 표의 결과 칸이 위에서부터 `true` `false` `true` `false` `false` `true`다.

- `ex07`·`ex08`·`ex09`는 버튼이나 입력 칸이 있다. 누르기 전과 누른 뒤를 비교한다.
- `ex10`은 연 순간의 시각을 보여 준다. 새로고침하면 다시 잰다.
- 파일마다 무엇을 바꿔 볼지는 [2일차 실습](lab.md#2일차--조건과-함수-그리고-조립-60분)에 있다.

### 7. 조립표

이제 `my-web`의 `index.html`·`app.js`를 부품에서 조립한다. 줄마다 **어느 ex에서 본 것**인지 적어 두었다.
옮겨 적을 때 출처 ex 파일을 옆에 열어 두고, 같은 문법이 거기서 화면과 Console에 무엇을 냈는지 떠올린다.

| my-web의 줄 | 어느 ex에서 본 것 |
|---|---|
| `index.html` `<head>`의 `<script src="app.js" defer></script>` | [ex02](examples/ex02_script_position.html) 3번. `defer`는 HTML을 다 읽은 뒤 실행한다 → `#greeting`을 찾을 수 있다 |
| `index.html`의 `<p class="card" id="greeting">인사말을 준비 중입니다.</p>` | [ex09](examples/ex09_dom_write.html) 찾을 자리에 `id`, [4주차 ex01](../week04_responsive_css/examples/ex01_selector.html) 클래스 선택자(`.red`와 같은 원리), `.card` 규칙은 [4주차 styles.css](../week04_responsive_css/examples/build/styles.css) |
| `const name = 'student01';` | [ex03](examples/ex03_let_const.html) `const` |
| `const hour = new Date().getHours();` | [ex10](examples/ex10_date.html) 지금 시각 → 시, [ex03](examples/ex03_let_const.html) `const` |
| `` function greet(name) { return `안녕하세요, ${name}님!`; } `` | [ex08](examples/ex08_function.html) 정의·`return`, [ex05](examples/ex05_template.html) 템플릿 문자열 |
| `function hello(hour) { if (hour >= 12) { return … } else { return … } }` | [ex07](examples/ex07_if_else.html) `if` · `else`, [ex06](examples/ex06_compare.html) `>=`, [ex08](examples/ex08_function.html) `return` |
| `` const message = `${greet(name)} ${hello(hour)}`; `` | [ex05](examples/ex05_template.html) `${}` 안은 계산된다(함수 호출도), [ex08](examples/ex08_function.html) 호출 |
| `console.log(hour);` `console.log(message);` | [ex01](examples/ex01_click.html) Console |
| `document.querySelector('#greeting').textContent = message;` | [ex09](examples/ex09_dom_write.html) 2번. 먼저 찾고 → 그다음 바꾼다 |

**예상 결과** — 표의 위 두 줄이 8단계, 나머지 일곱 줄이 9단계에서 쓰는 순서와 같다. 표에 없는 문법은 `app.js`에도 없다.

- 새 문법은 없다. 이틀 동안 비교 파일에서 본 것을 한 파일에 모을 뿐이다.
- 비교 파일은 작년 방식(`var`·`getElementById`·`innerText`)과 이 교재의 방식(`const`·`querySelector`·`textContent`)을 나란히 보였다. `my-web`은 이 교재의 방식으로 쓴다. `const`는 다시 담지 않는 값이라는 표시다(ex03). `querySelector`는 CSS 선택자(`#id`·`.class`)를 받아서 찾는 법을 하나로 쓸 수 있다(ex09). `textContent`는 글자만 바꿀 때 `innerText`와 결과가 같다. 작년 방식으로 써도 화면은 같고, 어느 쪽으로 써도 정답이다(ex03·ex09).

### 8. index.html에 두 줄 넣기

`index.html`에 두 줄을 넣는다.

첫째, `<head>`의 `<link rel="stylesheet" href="styles.css">` **바로 아래**에 스크립트 연결 줄을 넣는다. 3주차에 뺐던 줄을 되살리는 것이다.

```html
    <script src="app.js" defer></script>
```

둘째, `<main>` **첫 줄**(`<h2>소개</h2>` 위)에 인사말 자리를 넣는다.

```html
      <p class="card" id="greeting">인사말을 준비 중입니다.</p>
```

**예상 결과** — 저장하고 새로고침하면 소개 위에 `인사말을 준비 중입니다.`라는 흰 카드가 하나 더 보인다.
그런데 **F12 › Console**에는 빨간 줄이 하나 생긴다.

```text
Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')   app.js:6
```

`script` 줄이 살아나서 `app.js`가 실행되기 시작했기 때문이다. 지금 `app.js`에는 2주차 카운터 코드가 남아 있다.
그 코드가 찾는 버튼 `#count-button`은 3주차에 사라졌다. 찾으면 `null`이고, `null`에는 `addEventListener`를 붙일 수 없다. 9단계에서 이 코드를 지운다.

- `defer`를 빼면 `app.js`가 `<head>`에서 **읽는 순간** 실행된다. 그때는 `#greeting`이 아직 없어서 `null`이다(ex02 1번과 같다).
- `id="greeting"`은 이 문단에만 붙인다. 한 페이지에 같은 `id`를 두 번 쓰지 않는다. `class="card"`는 4주차 카드 모양을 그대로 쓰려고 함께 둔다.
- `about.html`·`guestbook.html`에는 넣지 않는다. 이번 주 JavaScript는 `index.html`만의 것이다.

### 9. app.js 비우고 조립하기

`app.js`를 연다. 2주차 카운터 코드(11줄)가 들어 있다. **전체를 지운다.**
8단계의 빨간 줄이 이 코드에서 났다. 버튼이 없는 페이지에서 버튼을 찾는 코드는 남겨 둘 이유가 없다.

빈 `app.js`에 7단계 조립표 순서로 쓴다. 한 덩어리를 쓸 때마다 저장 → 새로고침해서 Console에 빨간 줄이 없는지 본다.

1. 값 두 개 — `name`(ex03), `hour`(ex10). 두 줄 다 다시 담지 않으므로 `const`다. `name`에는 **본인 아이디**를 넣는다(아래 전문의 `student01` 자리).
2. 함수 `greet(name)` — 받은 이름으로 문장을 만들어 `return`한다(ex08·ex05).
3. 함수 `hello(hour)` — `hour >= 12`면 `'좋은 오후입니다.'`, 아니면 `'좋은 아침입니다.'`를 `return`한다(ex07·ex06).
4. `message` — 두 함수를 **불러서** 나온 두 문장을 백틱 안에서 한 문장으로 잇는다(ex05·ex08).
5. `console.log` 두 줄 — `hour`와 `message`를 Console에 찍는다(ex01).
6. 마지막 줄 — `#greeting`을 찾아 글자를 `message`로 바꾼다(ex09).

다 쓴 파일은 11단계 전문과 같다.

**예상 결과** — 새로고침하면 8단계의 빨간 줄이 없어지고, 카드 글자가 바뀐다.

```text
바뀌기 전 : 인사말을 준비 중입니다.
바뀐 뒤   : 안녕하세요, student01님! 좋은 아침입니다.
```

- 1~5번까지 쓴 상태에서는 카드가 `인사말을 준비 중입니다.` 그대로다. 화면을 바꾸는 줄은 6번 하나뿐이다.
- 2·3번의 함수는 정의만으로는 아무것도 하지 않는다. 4번에서 `greet(name)`·`hello(hour)`처럼 **괄호를 붙여 부를 때** 실행된다(ex08의 `neverCalled`).
- 2주차 코드를 한 줄이라도 남기면 8단계의 빨간 줄이 계속 뜨고, 그 아래 줄은 실행되지 않는다.

### 10. index.html 전문

8단계를 마친 `index.html` 전체다. 내 파일과 한 줄씩 비교한다. 4주차 파일에서 늘어난 것은 `script` 한 줄과 `#greeting` 카드 한 줄뿐이다.
같은 파일이 [examples/build/index.html](examples/build/index.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <header>
      <h1>student01의 웹 연습장</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <p class="card" id="greeting">인사말을 준비 중입니다.</p>
      <h2>소개</h2>
      <img src="images/profile.png" alt="student01의 프로필 그림" width="160">
      <p class="card">웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p class="card">이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
      <h2>취미</h2>
      <ul class="card">
        <li>사진 찍기</li>
        <li>보드게임</li>
        <li>저녁 산책</li>
      </ul>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`about.html`·`guestbook.html`·`styles.css`·`images/profile.png`는 4주차 그대로다. 이번 주에 손대지 않는다. `examples/build/`의 같은 이름 파일도 4주차와 같다.

**예상 결과** — `index.html`의 `<head>`에 `link` 줄과 `script` 줄이 나란히 있고, `<main>`의 첫 요소가 `#greeting` 카드다.
`about.html`·`guestbook.html`을 열면 모양은 4주차와 같고 Console은 비어 있다. 두 페이지에는 `script` 줄이 없어서 `app.js`가 실행되지 않는다.

### 11. app.js 전문

9단계를 마친 `app.js` 전체다. 21줄이다. 내 파일과 한 줄씩 비교한다. 1행의 `student01`만 내 아이디로 다르고 나머지는 글자 단위로 같아야 한다.
같은 파일이 [examples/build/app.js](examples/build/app.js)에 있다.

```js
const name = 'student01';
const hour = new Date().getHours();

function greet(name) {
  return `안녕하세요, ${name}님!`;
}

function hello(hour) {
  if (hour >= 12) {
    return '좋은 오후입니다.';
  } else {
    return '좋은 아침입니다.';
  }
}

const message = `${greet(name)} ${hello(hour)}`;

console.log(hour);
console.log(message);

document.querySelector('#greeting').textContent = message;
```

**예상 결과** — 브라우저는 이 파일을 위에서 아래로 한 번 읽는다. 1·2행에서 값이 담기고, 4~14행은 함수에 이름만 붙여 두고, 16행에서 두 함수를 불러 문장을 만들고, 18·19행이 Console에 찍고, 21행이 화면을 바꾼다.

- 2행 `new Date().getHours()`는 ex10의 두 줄(`now` 만들기 → `now.getHours()`)을 한 줄로 이어 쓴 것이다. 파일을 **연 순간**의 시각이다.
- 4행 `greet(name)`의 `name`은 함수가 받는 값의 이름이다. 이것을 **매개변수**라고 한다. 1행의 `name`과 글자는 같지만, 함수 안에서는 **부를 때 넣어 준 값**이 들어간다(ex08 3번: 같은 함수, 다른 값).
- 9행 `hour >= 12`는 12시 정각도 `true`다(ex06 3번 `12 >= 12`). 그래서 12시 0분에 열면 `좋은 오후입니다.`다.
- 5행과 16행은 백틱(`` ` ``)이다. 작은따옴표로 쓰면 `${greet(name)}`이 글자 그대로 나온다(ex05 3번). 백틱은 키보드 `1` 왼쪽, `Esc` 아래 키다. 다른 글자(macOS 한글 입력이면 `₩`)가 들어가면 영문 입력으로 바꾼 뒤 다시 친다.
- 21행은 ex09처럼 찾은 요소를 `const`에 담아 두지 않고, 찾은 결과에 바로 `.textContent`를 붙였다. 2행과 같은 이어 쓰기다. `const card = document.querySelector('#greeting');` 다음 줄에 `card.textContent = message;`로 나눠 써도 같다(ex09 2번 모양).
- 21행 `textContent`에 넣은 것은 글자 그대로 보인다. 태그를 넣어도 굵어지지 않는다(ex09 3번).

### 12. 확인하고 push

먼저 로컬에서 본다. `index.html`을 Chrome으로 열고 **F12 › Console**을 연다.

**예상 결과** — 카드와 Console이 아래처럼 보인다. 오전 10시에 열었을 때다.

```text
카드    : 안녕하세요, student01님! 좋은 아침입니다.
Console : 10                                           app.js:18
          안녕하세요, student01님! 좋은 아침입니다.      app.js:19
```

- Console 첫 줄의 숫자는 지금 시각(0~23)이다. 12 이상이면 카드와 Console 둘째 줄이 `좋은 오후입니다.`로 끝난다. 둘 다 정답이다.
- 카드가 `인사말을 준비 중입니다.` 그대로면 21행까지 가지 못한 것이다. Console의 첫 빨간 줄 오른쪽 `app.js:줄`부터 고친다.
- `Cannot set properties of null (setting 'textContent')`가 뜨면 21행이 `#greeting`을 못 찾은 것이다. `index.html`의 `id="greeting"` 철자와 `script` 줄의 `defer`를 본다.

맞으면 올린다. 현재 폴더: `my-web`

```bash
git add .
git commit -m "함수로 인사말 만들어 화면에 표시"
git push
```

**예상 결과**

```text
[main 7b2d9f4] 함수로 인사말 만들어 화면에 표시
 7 files changed, 214 insertions(+), 8 deletions(-)
 create mode 100644 week05/ex06_compare.html
 create mode 100644 week05/ex07_if_else.html
 create mode 100644 week05/ex08_function.html
 create mode 100644 week05/ex09_dom_write.html
 create mode 100644 week05/ex10_date.html
```

`git push`의 마지막 두 줄은 아래 모양이다.

```text
To https://github.com/student01/my-web.git
   3c8e5a1..7b2d9f4  main -> main
```

1분쯤 뒤 `https://student01.github.io/my-web/`을 새로고침하고 **F12 › Console**을 연다. 로컬과 같은 카드와 두 줄이 보인다.

- 앞의 일곱 글자와 줄 수는 PC마다 다르다. 파일 수가 7인지만 본다(비교 파일 5 + `index.html` + `app.js`).
- `8 deletions`는 9단계에서 지운 2주차 카운터 코드다. 11줄 중 빈 줄 3개는 새 `app.js`에도 있어서 Git이 지운 줄로 세지 않는다.

### 13. 되돌리기 두 가지

실험하다 망친 파일을 되돌리는 방법은 **commit 전이냐 뒤냐**로 갈린다. 둘 다 실제로 한 번씩 해 본다.

**① commit 전 — `git restore`**

두 갈래를 다 보려고 `app.js` 2행을 `const hour = 9;`로 바꾸고 저장한다. 새로고침해서 `좋은 아침입니다.`를 본다. `15`로 바꾸면 `좋은 오후입니다.`다.
다 봤으면 이 변경을 버린다. 저장만 하고 commit은 하지 않은 상태다. `'좋은 아침입니다.'`를 아무 글자로 바꿔 저장해 봐도 같다. 현재 폴더: `my-web`

```bash
git status
```

**예상 결과**

```text
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   app.js

no changes added to commit (use "git add" and/or "git commit -a")
```

`modified:` 줄이 `app.js` 하나여야 한다. `week05/` 파일이 함께 보이면 먼저 `git restore week05/`로 되돌린다.

```bash
git restore app.js
git status
```

**예상 결과** — `git restore`는 아무것도 찍지 않는다. `git status`가 아래처럼 바뀌고, VS Code의 `app.js` 2행이 `const hour = new Date().getHours();`로 돌아와 있다.

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

- `git restore`는 파일을 **마지막 commit 상태로 덮는다.** commit 전의 변경은 기록이 없으므로 되살릴 수 없다. 버릴 것만 restore한다.

**② commit 뒤 — `git revert`**

`app.js` 5행 문장을 일부러 다른 문구로 바꾸고 저장한다.

```js
  return `반갑습니다, ${name}님!!!`;
```

이 잘못을 commit까지 한 뒤 되돌린다. 현재 폴더: `my-web`

```bash
git add app.js
git commit -m "인사말 문구 바꾸기"
git revert HEAD
```

`HEAD`는 가장 최근 commit을 가리킨다. `git revert HEAD`는 방금 한 commit을 거꾸로 되돌리는 새 commit을 만든다. `HEAD^`는 그 하나 전 commit이다.

**예상 결과** — `git commit`이 먼저 아래 두 줄을 찍는다.

```text
[main c41e0a8] 인사말 문구 바꾸기
 1 file changed, 1 insertion(+), 1 deletion(-)
```

이어 `git revert HEAD`에서 **편집기 창**이 열린다. 첫 줄의 기본 메시지 `Revert "인사말 문구 바꾸기"`를 그대로 두고 닫는다.

- VS Code가 열렸으면 새로 열린 탭(`COMMIT_EDITMSG`)을 닫는다.
- 터미널 화면이 바뀌고 줄 앞에 `~`가 보이면 Vim이다. **Esc**를 누르고 `:wq`를 친 뒤 **Enter**.
- 편집기를 건너뛰려면 처음부터 `git revert HEAD --no-edit`로 쳐도 결과가 같다.

창을 닫으면 터미널에 아래가 나온다.

```text
[main e9f3b26] Revert "인사말 문구 바꾸기"
 Date: Wed Sep 30 10:41:07 2026 +0900
 1 file changed, 1 insertion(+), 1 deletion(-)
```

```bash
git log --oneline -3
```

**예상 결과** — 기록이 셋 다 남아 있다.

```text
e9f3b26 Revert "인사말 문구 바꾸기"
c41e0a8 인사말 문구 바꾸기
7b2d9f4 함수로 인사말 만들어 화면에 표시
```

`app.js` 5행은 `` return `안녕하세요, ${name}님!`; ``로 돌아와 있다.

- `git revert`는 commit을 지우지 않는다. **거꾸로 바꾸는 새 commit**을 하나 더 만든다. 그래서 잘못한 기록과 되돌린 기록이 둘 다 남는다.
- `git reset HEAD^`는 기록 자체를 지운다. push한 commit을 지우면 내 PC 기록이 GitHub 기록과 어긋나 다음 `git push`가 거부(rejected)된다. 그래서 push한 뒤에는 기록을 더하는 `revert`를 쓴다.
- 가운데 `Date:` 줄은 `git revert`가 늘 한 줄 붙이는 것이다. 앞의 일곱 글자와 시각은 PC마다 다르다.

### 14. push와 캡처

되돌리기 연습의 두 commit도 올린다. 현재 폴더: `my-web`

```bash
git push
```

**예상 결과** — 마지막 두 줄이 아래 모양이다.

```text
To https://github.com/student01/my-web.git
   7b2d9f4..e9f3b26  main -> main
```

1. 1분쯤 뒤 `https://student01.github.io/my-web/`을 새로고침한다.
2. **F12 › Console**을 켠 채로, 카드의 인사말과 Console 두 줄(`hour`·`message`)이 **한 화면에** 보이게 한다.
3. 주소창이 함께 보이게 화면을 캡처한다. 이 한 장이 이번 주 제출물이다.
4. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 12시 이후에 열면 `좋은 오후입니다.`가 나온다. 둘 다 정답이다.
- 캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 아이디는 보여도 된다.
- 끝 루틴에서 `git add .` → `git commit`을 다시 해 보면 `nothing to commit, working tree clean`이 나온다. 12·13단계에서 이미 commit했으므로 정상이다.
- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 증상별 확인 순서는 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다. 한 번에 한 곳만 고치고 새로고침한다.
