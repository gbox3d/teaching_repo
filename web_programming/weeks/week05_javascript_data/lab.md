# 5주차 실습 — 인사말을 만드는 app.js

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data

4주차까지 꾸민 `my-web`에 JavaScript를 되살린다. `index.html`에 `script` 한 줄을 넣고 `app.js`를 비운 뒤 새로 쓴다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.
**1일차는 화면을 건드리지 않는다.** 확인은 전부 브라우저의 **F12 › Console** 탭에서 한다.

## 1일차 — 값을 만들어 Console에 찍기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` 뒤 **File › Open Folder** |
| 5–15분 | `index.html`에 `<script src="app.js" defer></script>` 한 줄을 되살리고, `app.js`를 전부 지운 뒤 `console.log` 한 줄을 쓴다 |
| 15–30분 | `const name`과 `let hour`를 만들어 Console에 찍고, `hour`에 다른 값을 다시 넣어 본다 |
| 30–45분 | 템플릿 문자열로 인사 문장을 만들어 Console에 찍는다 |
| 45–55분 | 일부러 오타를 내고 빨간 줄의 `app.js:줄번호`를 찾아 고친다 → 확인용 Console 캡처 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 새로고침 → 공용 PC면 자격 증명 삭제 |

### 1. script 줄 되살리고 app.js 비우기 (`<script src="app.js" defer></script>`)

`index.html`의 `<link rel="stylesheet" href="styles.css">` 바로 아래에 `script` 한 줄을 넣고, `app.js`는 **전부 지운 뒤** 첫 줄을 새로 쓴다.
[따라하기 2~3단계](walkthrough.md#2-indexhtml에-script-줄-되살리기)를 본다.

- 2주차 카운터 코드(`() =>`·`#count-button`)는 남기지 않는다. 그 버튼은 3주차에 이미 사라졌다.
- 첫 줄은 `console.log('app.js가 실행되었습니다');` 한 줄이다. 저장하고 브라우저를 새로고침한다.
- **F12 › Console**에 그 글자가 보이면 연결된 것이다. 아무것도 없으면 `script` 줄의 파일 이름 철자를 본다.
- 화면은 4주차와 똑같다. 그것이 정상이다.

### 2. 값 만들기 (`const` · `let`)

`const name`과 `let hour`를 만들고 각각 `console.log`로 찍은 뒤, `hour`에 다른 숫자를 다시 넣어 또 찍는다.
[따라하기 4~5단계](walkthrough.md#4-const와-let으로-값-만들기)를 본다.

- 문자열은 따옴표 안에, 숫자는 따옴표 없이 쓴다. `'9'`와 `9`는 다르다.
- 다시 넣을 때 `let`을 또 쓰지 않는다. `hour = 15;`처럼 이름만 적는다.
- `name`에 다시 넣어 보면 Console에 `Uncaught TypeError: Assignment to constant variable.`이 뜬다. 확인했으면 그 줄은 지운다.
- 이름은 뜻이 보이게 적는다. `a`·`b`는 쓰지 않는다.

### 3. 문장 만들기 (템플릿 문자열 `` `${}` ``)

백틱으로 감싼 문장 안에 `${name}`·`${hour}`를 넣어 인사 문장을 만들고 Console에 찍는다.
[따라하기 6단계](walkthrough.md#6-템플릿-문자열로-인사말-만들기)를 본다.

- 백틱은 키보드 `1` 왼쪽, `Esc` 아래 키다. **한글 입력 상태에서는 다른 글자가 들어간다.**
- `${name}`이 글자 그대로 찍히면 백틱이 아니라 작은따옴표를 쓴 것이다.
- 문장에 본인 아이디가 들어가게 한다. 실명은 쓰지 않는다.

### 4. 오타를 내고 빨간 줄 읽기 (Console)

`name`을 `nmae`로 바꿔 저장하고 새로고침해 빨간 줄을 읽은 뒤 고친다. [따라하기 7단계](walkthrough.md#7-일부러-오타를-내고-빨간-줄-읽기)를 본다.

- 빨간 줄 오른쪽의 `app.js:6`이 **파일 이름과 줄 번호**다. 그 줄부터 본다.
- 오류가 난 줄에서 멈추므로 그 아래 `console.log`는 찍히지 않는다. 몇 줄이 사라졌는지 세어 본다.
- 고친 뒤 새로고침해 빨간 줄이 사라지고 여섯 줄이 모두 보이면 **확인용 캡처**를 저장한다.

### 5. 오늘 확인할 것

- [ ] Console에 `app.js가 실행되었습니다`를 포함해 여섯 줄이 보인다.
- [ ] 빨간 줄이 없다.
- [ ] `git push` 뒤 공개 주소를 열어도 화면은 그대로이고 Console에 같은 줄이 보인다.
- [ ] 확인용 Console 캡처를 저장했다(2일차를 못 끝내면 이 캡처로 인정한다).

## 2일차 — if와 함수로 인사말 만들기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` |
| 5–22분 | `index.html`의 `<main>` 첫 줄에 `<p class="card" id="greeting">`을 넣고, `if / else`로 오전·오후 인사를 고른다 |
| 22–40분 | `greet(name)`과 `hello(hour)` 함수 두 개를 만들어 문장을 조립한다 |
| 40–48분 | 복붙 틀 한 줄로 `#greeting`에 인사말을 표시한다 |
| 48–55분 | 오늘 작업을 먼저 commit한 뒤, 인사말을 일부러 틀리게 고쳐 다시 commit하고 `git revert HEAD`로 되돌린다 |
| 55–60분 | 끝 루틴: `git push` → 공개 주소 새로고침 → **캡처 1장** → 공용 PC면 자격 증명 삭제 |

### 1. 인사말 자리와 지금 시각 (`id="greeting"` · `new Date().getHours()`)

`index.html`의 `<main>` 첫 줄에 문단 하나를 넣고, `app.js`를 다시 쓰기 시작한다.
[따라하기 10~11단계](walkthrough.md#10-인사말-자리-만들기)를 본다.

- 문단의 글자는 `인사말을 준비 중입니다.`로 둔다. JavaScript가 도달하지 못하면 이 글자가 그대로 남는다.
- `id`는 `greeting` 하나만 쓴다. 6주차가 이 이름을 그대로 받는다.
- `const hour = new Date().getHours();`는 **복붙 틀 한 줄**이다. `console.log(hour)`로 숫자를 확인한다.

### 2. 오전·오후 고르기 (`if / else` · `>=`)

`if (hour >= 12) { } else { }`로 두 문장 중 하나를 고른다. [따라하기 12단계](walkthrough.md#12-if로-오전오후-인사-고르기)를 본다.

- 지금 시각 한 갈래만 확인된다. 다른 갈래를 보려면 `const hour = 9;`처럼 숫자를 직접 넣어 본다. 확인 뒤 틀 한 줄로 되돌린다.
- `=`는 넣는 것, `===`는 같은지 비교하는 것이다. `if (hour = 12)`라고 쓰지 않는다.
- 중괄호 `{ }`의 짝을 맞춘다. 짝이 안 맞으면 `Uncaught SyntaxError`가 뜬다.

### 3. 함수 두 개 (`function` · `return`)

`greet(name)`과 `hello(hour)`를 만들고 `return`한 값을 템플릿 문자열로 이어 붙인다.
[따라하기 13단계](walkthrough.md#13-함수-두-개로-묶기)를 본다.

- 함수는 정의만으로 실행되지 않는다. `greet(name)`처럼 **괄호를 붙여 호출**해야 값이 나온다.
- `console.log`만 하고 `return`을 빼면 결과가 `undefined`가 된다. 돌려줄 값은 `return`으로 내보낸다.
- 함수 이름은 `greet`·`hello` 그대로 쓴다. 6주차에 같은 이름을 다시 쓴다.

### 4. 화면에 띄우기 (복붙 틀 한 줄)

`app.js` 마지막 줄에 `document.querySelector('#greeting').textContent = message;`를 적는다.
[따라하기 14단계](walkthrough.md#14-문장-조립하고-화면에-띄우기)를 본다.

- 이 줄의 뜻은 6주차에 배운다. 오늘은 모양 그대로 쓰고 `#greeting`과 `message`만 내 것과 맞춘다.
- 글자가 안 바뀌면 Console의 빨간 줄을 먼저 본다. 대개 그 위 줄에서 멈춘 것이다.

### 5. 되돌리기 (`git revert HEAD`)

오늘 만든 코드를 `git add .` → `git commit -m "함수로 인사말 만들어 화면에 표시"`로 **먼저 commit한다**(따라하기 14단계 끝).
그런 다음 인사말을 일부러 틀리게 고쳐 다시 commit하고 `git revert HEAD`로 되돌린다. [따라하기 15단계](walkthrough.md#15-틀린-문장을-commit하고-git-revert로-되돌리기)를 본다.

- 먼저 commit해야 되돌리기가 문구 한 줄만 되돌린다(`1 file changed, 1 insertion(+), 1 deletion(-)`). 건너뛰면 오늘 작업 전체가 되돌아간다.
- 편집기 창이 뜨면 기본 메시지 `Revert "…"` 그대로 저장하고 닫는다.
- `git log --oneline`에 `인사말 문구 바꾸기`와 `Revert "인사말 문구 바꾸기"`가 모두 남아 있으면 맞다. 되돌리기도 기록으로 남는 것이 `revert`다.
- `git reset HEAD^`는 기록 자체를 지운다. push해서 공유한 commit에는 쓰지 않는다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 다시 확인해도 된다. `git status`에 `Your branch is ahead`가 있으면 push를 안 한 것이다 |
| Console에 아무 줄도 안 뜬다 | `index.html`에 `<script src="app.js" defer></script>`가 없거나 파일 이름 철자가 다르다. 파일 이름이 틀리면 `app.js` 안의 오류가 아니라 **파일을 못 불러왔다**는 줄이 뜬다(공개 주소에서는 `404`, `file://`에서는 `net::ERR_FILE_NOT_FOUND`). Console에 내 `console.log`가 하나도 없으면 연결부터 의심한다. `app.js`를 저장했는지도 본다 |
| `Uncaught ReferenceError: nmae is not defined` | 없는 이름을 썼다. 오른쪽 `app.js:6`의 줄로 가 철자를 고친다 |
| `Uncaught ReferenceError: helo is not defined` | 함수 이름 오타다. 정의한 이름(`hello`)과 부른 이름을 비교한다 |
| `Uncaught SyntaxError: Unexpected end of input` | 백틱이나 중괄호를 닫지 않았다. 문장 끝의 `` ` ``와 `}`를 세어 본다. 닫지 않은 백틱 **뒤에 백틱이 더 있으면** `Uncaught SyntaxError: Unexpected identifier '…'`로 나온다. 어느 쪽이든 백틱 짝부터 센다 |
| `Uncaught SyntaxError: missing ) after argument list` | 괄호를 닫지 않았다. `console.log(greet('student01'));`처럼 괄호 짝을 맞춘다 |
| `Uncaught TypeError: Assignment to constant variable.` | `const`로 만든 값에 다시 넣었다. 다시 넣어야 하면 `let`으로 만든다 |
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` | `app.js`에 2주차 카운터 코드가 남아 있다. 그 버튼은 3주차에 사라졌다. [따라하기 3단계](walkthrough.md#3-appjs-비우고-첫-줄-쓰기)처럼 전체를 지우고 새로 쓴다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` | `#greeting`을 못 찾았다. `id="greeting"` 철자, 그리고 `script` 줄에 `defer`가 있는지 본다 |
| Console에 `${name}`이 글자 그대로 찍힌다 | 작은따옴표로 감쌌다. 백틱(`` ` ``)으로 바꾼다. 한글 입력 상태에서 친 백틱은 다른 글자다 |
| 함수 결과가 `undefined`로 찍힌다 | 함수 안에 `return`이 없다. `console.log`는 찍기만 하고 값을 돌려주지 않는다 |
| 화면에 `인사말을 준비 중입니다.`가 그대로 있다 | 마지막 줄까지 가지 못했다. Console의 첫 빨간 줄을 고친 뒤 새로고침한다 |
| 인사말이 `좋은 오후입니다.`로 나온다 | 12시가 지나서 연 것이며 정상이다. 두 갈래 모두 정답이다 |
| `git revert HEAD` 뒤 편집기 창이 열려 멈춰 있다 | 기본 메시지를 그대로 두고 저장한 뒤 창을 닫는다(VS Code는 탭을 닫으면 된다). 그러면 터미널에 `[main …] Revert "…"`가 나온다 |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시와 `git log --oneline`을 본다 |
| 화면이 4주차와 똑같다 (1일차) | 정상이다. 1일차 `app.js`는 화면을 건드리지 않는다. 확인은 Console에서 한다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://<아이디>.github.io/my-web/`을 열고 **F12 › Console**을 켠 채로 한 화면을 캡처한다.

- 카드 한 줄에 `안녕하세요, <아이디>님! 좋은 아침입니다.`(또는 `좋은 오후입니다.`)가 보인다.
- Console에 시각 숫자와 같은 문장이 찍혀 있고 빨간 줄이 없다.
- 주소창이 함께 보이게 찍는다.

2일차를 끝내지 못했다면 1일차 확인용 Console 캡처를 대신 낸다. 캡처에 실명·학번·실제 이메일이 보이지 않게 한다.
제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 관심사 세 개를 담은 목록을 만들어 Console에 한 줄씩 찍어 본다. 아래 두 문법은 **10주차에 정식으로 배운다.** 오늘은 모양만 따라 해 본다.

```js
const interests = ['사진 찍기', '보드게임', '저녁 산책'];

for (const item of interests) {
  console.log(item);
}
```

- `console.log(interests)` 한 줄도 찍어 목록 전체가 어떻게 보이는지 확인한다.
- `hello(hour)` 안의 기준 시각 `12`를 다른 숫자로 바꿔 두 갈래를 모두 확인한 뒤 되돌린다.
- 인사 문장에 오늘 할 일을 한 줄 더 붙여 본다(`` `${message} 오늘도 좋은 하루 되세요.` ``).
- `console.log`를 `console.info`로 바꿔 보고 Console에서 모양이 어떻게 다른지 본다.

추가 과제는 선택 사항이며 채점하지 않는다.
