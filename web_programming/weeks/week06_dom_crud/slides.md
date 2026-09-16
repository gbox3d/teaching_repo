---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 6주차"
footer: "DOM·이벤트·브라우저 CRUD · 클릭 카운터와 다크 모드"
---

# DOM·이벤트·브라우저 CRUD

5주차 코드는 페이지를 열 때 **한 번** 실행됐습니다.
이번 주에는 **버튼을 눌렀을 때** 실행되는 코드를 씁니다.

```text
my-web/
  index.html   ← 버튼 2개와 <p id="count">
  app.js       ← querySelector · textContent · addEventListener
  styles.css   ← body.dark 규칙 (2일차)
```

작업은 `dark-mode` 브랜치에서 하고 2일차 끝에 main에 합칩니다.

---

# 1일차 — 클릭하면 바뀌는 페이지

`30분 설명·시연 → 60분 실습`

1. 기능 브랜치 `dark-mode` 만들기
2. HTML과 DOM은 같은가
3. `querySelector`로 요소 찾기
4. `textContent`로 글자 바꾸기
5. `addEventListener('click')`과 클릭 횟수

---

## 1일차 · 0–5분 — 오늘 Git 5분: 기능 브랜치 dark-mode

```bash
git pull
git switch -c dark-mode
```

```text
Switched to a new branch 'dark-mode'
```

- 3주차 `guestbook` 브랜치와 같은 방법입니다. `-c`는 "만들면서 옮겨 가라"는 뜻입니다.
- 이번 주 작업은 이 브랜치에 쌓입니다. main은 그대로이고 **공개 페이지도 그대로**입니다.
- 2일차 끝에 main으로 돌아가 `merge`로 합칩니다. 그때 공개 페이지가 바뀝니다.
- 새 기능을 만드는 동안 공개 페이지를 건드리지 않는 것이 브랜치를 쓰는 이유입니다.

---

## 1일차 · 5–11분 — HTML과 DOM은 같은가

```html
<p class="card" id="greeting">인사말을 준비 중입니다.</p>
```

```text
내가 쓴 HTML 파일  ──읽기──▶  브라우저가 만든 요소 상자들(DOM)
                                        │
                          JavaScript가 찾아서 글자를 바꾼다
```

- **HTML**: 내가 파일에 적어 둔 글자입니다. 저장하면 그대로 남습니다.
- **DOM**: 브라우저가 그 글자를 읽어 만든 **요소 상자들**입니다. 화면에 보이는 것은 이쪽입니다.
- DevTools **Elements** 탭이 보여 주는 것이 DOM입니다. 여기서 바꾼 것은 파일에 저장되지 않습니다.
- 새로고침하면 브라우저가 파일을 다시 읽어 DOM을 새로 만듭니다. 그래서 `클릭 0회`로 돌아갑니다.

---

## 1일차 · 11–17분 — querySelector로 요소 찾기

```js
const greeting = document.querySelector('#greeting');

console.log(greeting);
```

- `document`는 **페이지 전체**입니다. 브라우저가 미리 만들어 둡니다.
- `querySelector('#greeting')`은 `id`가 `greeting`인 요소 **하나**를 찾아 돌려줍니다.
- `#`은 `id`를 찾으라는 표시입니다. 4주차 CSS 선택자와 같은 모양입니다.
- 찾은 것을 `const`에 담아 두면 그다음부터는 그 이름으로 씁니다.
- 못 찾으면 `null`입니다. 5주차에 본 `Cannot set properties of null`이 그것입니다.

---

## 1일차 · 17–22분 — textContent로 글자 바꾸기

```js
greeting.textContent = `${greet(name)} ${hello(hour)}`;
```

- `.textContent`는 요소 안의 **글자**입니다.
- `=` 오른쪽에 두면 읽고, **왼쪽에 두면 바꿔 넣습니다.**
- 5주차의 복붙 틀 한 줄이 오늘 두 줄로 나뉩니다. 먼저 **찾아 두고**(`querySelector`), 그다음 **바꿉니다**(`textContent`).
- 바뀌는 것은 화면(DOM)이지 HTML 파일이 아닙니다. 새로고침하면 파일의 글자로 돌아갑니다.

---

## 1일차 · 22–28분 — addEventListener('click')과 클릭 횟수

```js
let count = 0;

helloButton.addEventListener('click', function () {
  greeting.textContent = '반갑습니다. 오늘도 좋은 하루 되세요.';
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
});
```

- "이 버튼을 **클릭하면** 이 함수를 실행하라"고 브라우저에 맡겨 둡니다.
- 맡기는 순간에는 실행되지 않습니다. 누를 때마다 중괄호 안이 실행됩니다.
- `let count`는 함수 **밖**에 둡니다. 안에 두면 누를 때마다 0에서 다시 시작합니다.
- 2주차 `app.js`의 `() =>`는 틀로만 본 것입니다. 수업 코드는 `function () { }`로 씁니다.

---

## 1일차 · 28–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--클릭하면-바뀌는-페이지-만들기-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud

1. `git switch -c dark-mode`로 오늘 작업할 브랜치를 만듭니다.
2. `index.html`에 버튼과 `<p id="count">`를 넣고, `app.js`에서 찾아 글자를 바꿉니다.
3. 클릭 횟수를 세고, `null` 오류 두 가지를 일부러 만들어 고쳐 봅니다.

**설명 합계: 5+6+6+5+6+2 = 30분**

오늘 commit은 `dark-mode`에 쌓입니다. 공개 페이지는 아직 5주차 화면 그대로입니다.

---

# 2일차 — 다크 모드와 함수 재사용

`30분 설명·시연 → 60분 실습`

1. `merge`와 브랜치 정리
2. `classList.add / remove / toggle`
3. `body.dark` 규칙과 `classList.toggle('dark')`
4. 같은 함수를 두 버튼에
5. 8주차 중간 실기 예고

---

## 2일차 · 0–5분 — 오늘 Git 5분: merge와 브랜치 정리

```bash
git switch main
git merge dark-mode
git push
git branch -d dark-mode
```

```text
Updating e1bf03b..9a76325
Fast-forward
 app.js     | 23 +++++++++++++++++++----
```

- 2주차 `about` 브랜치와 같은 순서입니다. main으로 **돌아가서** 합칩니다.
- 합치기 전에 `dark-mode`를 먼저 push해 둡니다. 그래야 마지막 `branch -d`가 깨끗하게 지워집니다.
- merge 뒤 push해야 **공개 페이지**가 바뀝니다. 오늘 캡처는 그 화면입니다.

---

## 2일차 · 5–11분 — classList.add / remove / toggle

```js
document.body.classList.add('dark');
document.body.classList.remove('dark');
document.body.classList.toggle('dark');
```

- 요소가 달고 있는 **class 이름 목록**을 다루는 도구입니다.
- `add`는 붙이기만, `remove`는 떼기만 합니다.
- `toggle`은 **없으면 붙이고 있으면 뗍니다.** 버튼 하나로 켜고 끄기에 맞습니다.
- class를 붙였다고 모양이 바뀌지는 않습니다. 그 class를 쓰는 **CSS 규칙이 있어야** 바뀝니다.
- DevTools **Elements**에서 `<body class="dark">`로 바뀌는 것을 눈으로 볼 수 있습니다.

---

## 2일차 · 11–17분 — body.dark 규칙과 classList.toggle('dark')

```css
body.dark,
body.dark .card {
  background-color: #222222;
  color: #eeeeee;
}
```

```js
darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
});
```

- `body.dark`는 "`<body>`에 class `dark`가 붙었을 때"라는 뜻입니다. 사이를 띄우지 않습니다.
- `body.dark .card`는 그 안의 카드들입니다. 띄어 쓰면 "안에 있는"이라는 뜻입니다(4주차 선택자).
- JavaScript는 class 하나만 붙였다 뗍니다. 색을 정하는 것은 CSS입니다.

---

## 2일차 · 17–22분 — 같은 함수를 두 버튼에

```js
function countUp() {
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
}
```

- 두 버튼이 똑같이 "횟수를 1 올리고 화면에 쓴다"를 합니다. 같은 코드를 두 번 쓰지 않습니다.
- 5주차에 배운 `function`으로 묶고, 두 리스너에서 `countUp()`으로 **부릅니다.**
- 고칠 일이 생기면 한 곳만 고칩니다. 예를 들어 `클릭 ${count}번`으로 바꾸려면 한 줄만 고칩니다.
- 돌려줄 값이 없으므로 `return`은 쓰지 않습니다. 하는 일만 있는 함수입니다.

---

## 2일차 · 22–27분 — 8주차 중간 실기 예고

| 항목 | 내용 |
|---|---|
| 범위 | 2~7주차 — GitHub Pages, HTML, CSS, DOM, 폼 |
| 배점 | 20점. 폼 입력·빈값 안내 3점이 들어갑니다 |
| 작업 위치 | 새 저장소를 만들지 않고 `my-web/exam/`에 만들어 push합니다 |
| 공개 | 리허설 starter와 채점표는 **7주차 1일차**에 공개합니다 |

- 오늘 배운 `querySelector`·`textContent`·`addEventListener`가 그대로 나옵니다.
- 목록 **추가·삭제는 10주차**, 새로고침해도 남는 **저장은 11주차**입니다. 중간 실기 범위가 아닙니다.
- 7주차에 폼 입력을 읽어 화면에 띄우면 중간 실기 범위가 모두 채워집니다.

---

## 2일차 · 27–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--다크-모드와-함수-재사용-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud

1. `[다크 모드]` 버튼과 `body.dark` 규칙을 만들어 `classList.toggle('dark')`로 켜고 끕니다.
2. 두 버튼이 `countUp()` 한 함수를 쓰게 정리합니다.
3. `dark-mode`를 push한 뒤 main에서 `merge` → `push` → `branch -d`를 합니다.

**설명 합계: 5+6+6+5+5+3 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/my-web/
배경이 어두운 화면 · [인사 바꾸기] [다크 모드]
카드: 반갑습니다. 오늘도 좋은 하루 되세요.
카드: 클릭 3회
주소창이 함께 보이게 찍습니다
```

`클릭 0회`가 아니라 **1 이상**이어야 눌러 본 것이 보입니다.
캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

이번 주에는 **버튼**을 눌렀을 때 화면을 바꿨습니다.

7주차에는 **폼을 제출했을 때** 화면을 바꿉니다.
3주차에 만들어 두고 "눌러도 주소창만 바뀐다"고 적어 둔 `guestbook.html`의 [남기기]가 그 자리입니다.
`addEventListener`는 그대로 쓰고 `'click'` 대신 `'submit'`을, 그리고 입력 칸을 읽는 `input.value`를 배웁니다.
