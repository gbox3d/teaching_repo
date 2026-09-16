---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 7주차"
footer: "폼 입력 읽기와 결과 표시 · submit, value, 빈값 안내"
---

# 폼 입력 읽기와 결과 표시

6주차에는 **버튼을 클릭했을 때** 화면을 바꿨습니다.
이번 주에는 **폼을 제출했을 때** 화면을 바꿉니다.

```text
my-web/
  guestbook.html  ← <form id="guestbook-form"> · <p id="notice"> · <p id="last">
  guestbook.js    ← 새 파일. submit · preventDefault · value · trim
  README.md       ← GitHub 웹에서 만들어 pull (2일차)
```

3주차에 만들어 두고 "눌러도 주소창만 바뀐다"고 적어 둔 그 폼이 오늘 동작합니다.

---

# 1일차 — 폼 제출을 내 코드로 받기

`30분 설명·시연 → 60분 실습`

1. 3주차 폼 다시 보기
2. `addEventListener('submit')`과 `event.preventDefault()`
3. `value`와 `trim()`으로 값 읽기
4. 결과 표시·빈값 안내·`focus()`·`reset()`
5. 8주차 중간 실기 공개

---

## 1일차 · 0–5분 — 3주차 폼 다시 보기

```html
<form>
  <label for="name">이름</label> <input id="name" type="text">
  <label for="email">이메일</label> <input id="email" type="email">
  <textarea id="message" rows="4"></textarea>
  <button type="submit">남기기</button>
</form>
```

- 3주차에 만든 폼입니다. **[남기기]**를 누르면 지금은 주소 끝에 `?`가 붙고 화면이 처음으로 돌아갑니다.
- 브라우저가 폼을 **보내려고** 하기 때문입니다. 보낼 곳(서버)이 없어도 일단 주소를 바꾸고 새로고침합니다.
- 오늘 할 일은 두 가지입니다. 그 동작을 **멈추고**, 입력한 값을 **내 코드로 받는 것**입니다.
- `<form>`에 `id="guestbook-form"`을 붙이는 것부터 시작합니다. 찾을 수 있어야 맡길 수 있습니다.

---

## 1일차 · 5–12분 — addEventListener('submit')과 preventDefault

```js
form.addEventListener('submit', function (event) {
  event.preventDefault();
});
```

- 6주차 `'click'` 자리에 `'submit'`이 들어갔습니다. 맡기는 방법은 똑같습니다.
- `submit`은 **[남기기]**를 누를 때도, 입력 칸에서 **Enter**를 칠 때도 일어납니다.
- 괄호 안의 `event`는 **방금 일어난 일**이 담겨 오는 이름입니다.
- `event.preventDefault()`는 "브라우저가 원래 하려던 일(주소 바꾸고 새로고침)을 하지 마라"는 뜻입니다.
- 이 한 줄이 없으면 아래 코드가 실행되더라도 화면이 곧바로 처음으로 돌아갑니다.

---

## 1일차 · 12–18분 — value와 trim으로 값 읽기

```js
const nameInput = document.querySelector('#name');

const name = nameInput.value.trim();
```

- `.value`는 그 입력 칸에 **지금 적혀 있는 글자**입니다. `textarea`도 같습니다.
- `.trim()`은 앞뒤 공백을 떼어 낸 값을 돌려줍니다. 공백만 친 칸을 빈칸으로 보기 위해서입니다.
- 값을 읽는 줄은 리스너 **안**에 둡니다. 누를 때마다 그때의 값을 새로 읽어야 합니다.
- `.velue`처럼 철자를 틀리면 `Cannot read properties of undefined (reading 'trim')`이 뜹니다.

---

## 1일차 · 18–24분 — 표시·빈값 안내·focus·reset

```js
  if (name === '') {
    notice.textContent = '이름을 입력하세요.';
    nameInput.focus();
    return;
  }

  last.textContent = `${name}: ${message}`;
  form.reset();
  nameInput.focus();
```

- **오늘 문법 5분**: `return`은 "여기서 이 함수를 끝내라". 없으면 안내를 띄운 뒤에도 아랫줄이 실행됩니다.
- `focus()`는 그 칸으로 커서를 옮기고, `form.reset()`은 폼을 비웁니다. 값을 읽어 **표시한 뒤에** 비웁니다.
- `guestbook.html`은 `guestbook.js`를, `index.html`은 `app.js`를 부릅니다. **페이지마다 자기 js 하나**입니다.

---

## 1일차 · 24–30분 ① — 8주차 중간 실기 공개

| 항목 | 내용 |
|---|---|
| 범위 | 2~7주차 — GitHub Pages, HTML, CSS, DOM, 폼 |
| 배점 | 20점. 오늘 만든 폼 입력·빈값 안내가 3점 |
| 작업 위치 | 새 저장소를 만들지 않고 `my-web/exam/`에 만들어 push |
| 오늘 공개 | [채점표](../week08_midterm/rubric.md) · [시험 구조](../week08_midterm/exam_structure.md) · [리허설 starter](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm/examples/rehearsal_starter) |

- 목록 **추가·삭제는 10주차**, 새로고침해도 남는 **저장은 11주차**, `fetch`는 **12주차**라 범위가 아닙니다.
- 리허설 starter는 오늘 실습 48–55분에 열어만 보고, 문제는 2일차와 8주차 1일차에 풉니다.

---

## 1일차 · 24–30분 ② — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--폼-제출을-받아-화면에-표시하기-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules

1. `guestbook.html`에 `id`와 결과 자리를 만들고 `guestbook.js`를 연결합니다.
2. 제출을 받아 새로고침을 막고, 값을 읽어 `이름: 메시지` 한 줄로 표시합니다.
3. 이름이 비면 안내하고 커서를 옮긴 뒤, `form.reset()`으로 다음 입력을 준비합니다.

**설명 합계: 5+7+6+6+6 = 30분**

막히면 Console의 **첫 빨간 줄**과 `guestbook.js:7` 같은 줄 번호부터 읽습니다.

---

# 2일차 — 두 칸을 끝까지 다듬기

`30분 설명·시연 → 60분 실습`

1. GitHub 웹에서 `README.md` 만들고 `git pull`
2. SSH 키 한 장 (개인 노트북 선택)
3. 두 칸 검사와 안내 문구 지우기
4. `reset`·`focus`로 다음 입력 준비
5. 리허설과 본시험 60분 배분

---

## 2일차 · 0–8분 ① — 오늘 Git 8분: GitHub 웹에서 README 만들기

**저장소 화면 › Add file › Create new file › `README.md` › Commit changes**

```bash
git pull
```

```text
Updating a69bc37..3d51f0c
Fast-forward
 README.md | 8 ++++++++
 1 file changed, 8 insertions(+)
 create mode 100644 README.md
```

- GitHub 화면에서 만든 파일은 **GitHub에만** 있습니다. `git pull`을 해야 내 PC에 생깁니다.
- 2주차 부록에서 본 `clone`·`pull`의 복습입니다. 지금까지는 내가 올리기만 했습니다.
- pull을 건너뛰고 commit하면 다음 push가 거부됩니다. **받아오는 것이 먼저**입니다.

---

## 2일차 · 0–8분 ② — SSH 키로 로그인하기 (개인 노트북 선택)

```bash
ssh-keygen -t ed25519 -C "student01@example.com"
```

- 개인 노트북에서 push할 때마다 `Username for 'https://github.com':`가 뜨는 경우의 대안입니다.
- `~/.ssh/id_ed25519.pub` 내용을 **Settings › SSH and GPG keys › New SSH key**에 붙여 넣습니다.
- `git remote set-url origin git@github.com:student01/my-web.git`으로 주소를 바꿉니다.
- 실습실 PC는 지금까지처럼 **HTTPS + 브라우저 로그인**으로 합니다. 이 장은 **채점하지 않습니다.**
- 개인 키 파일(`id_ed25519`)은 누구에게도 보내지 않습니다. 화면에 띄우지도 않습니다.

---

## 2일차 · 8–15분 — 두 칸 검사와 안내 문구 지우기

```js
  if (message === '') {
    notice.textContent = '메시지를 입력하세요.';
    messageInput.focus();
    return;
  }
```

```js
nameInput.addEventListener('input', clearNotice);
```

- 검사는 **위에서부터** 차례로 합니다. 이름이 비면 거기서 끝나 메시지 검사까지 가지 않습니다.
- 안내 문구는 칸마다 다르게 씁니다. 문구만 보고 어디를 고칠지 알 수 있어야 합니다.
- `'input'`은 글자가 바뀔 때마다 일어납니다. 6주차 `addEventListener`에서 **이벤트 이름만** 바뀌었습니다.
- 맡길 때 `clearNotice`에 괄호를 붙이지 않습니다. `clearNotice()`는 그 자리에서 한 번 실행하라는 뜻입니다.

---

## 2일차 · 15–21분 — reset·focus로 다음 입력 준비

```js
  clearNotice();
  last.textContent = `${name}: ${message}`;
  form.reset();
  nameInput.focus();
```

- 순서가 중요합니다. 값을 **읽어 표시한 뒤에** 비웁니다. 먼저 비우면 빈 값이 표시됩니다.
- `form.reset()`은 이메일 칸까지 폼 전체를 비웁니다. `focus()`로 커서를 이름 칸에 돌려 둡니다.
- 두 번째 글을 남기면 **앞 글이 사라집니다.** 카드가 한 줄이기 때문입니다.
- 글을 쌓아 목록으로 보여 주는 것은 **10주차**, 새로고침해도 남게 하는 것은 **11주차**입니다.

---

## 2일차 · 21–26분 ① — 리허설과 본시험 60분 배분

| 시각 | 하는 일 |
|---|---|
| 0–5 | 문제지를 끝까지 읽는다 |
| 5–15 | HTML: 뼈대·목록·표·폼 |
| 15–25 | CSS: 선택자·박스·flex·`@media` |
| 25–50 | DOM·폼: 클릭·제출·빈값 안내 |
| 50–55 | `add → commit → push` |
| 55–60 | 예비(Pages 반영 지연·재로그인) |

- 8주차 1일차에 리허설 네 문제를 풀고, **새 저장소 만들기와 Pages 켜기도 그날 끝냅니다.**
- 본시험 날에는 `my-web/exam/` 폴더에 만들어 push만 합니다.

---

## 2일차 · 21–26분 ② — 이 과목에서 비동기와 모듈은 어디 있나

```text
7주차  폼 제출 → 값 읽기 → 화면에 표시   ← 오늘
12주차 fetch로 JSON 파일 불러오기        ← 비동기는 여기
—      ES Module(import/export)·번들러   ← 이 과목 범위 밖
```

- 화면에서 일어난 일을 받아 처리하는 오늘의 흐름이 12주차 `fetch`의 바탕입니다.
- **비동기는 12주차 `fetch`에서** 다룹니다. 파일 하나를 불러와 카드로 그립니다.
- **모듈(`import`/`export`)은 이 과목 범위 밖**입니다. 우리는 `<script src="…" defer>` 하나로만 씁니다.
- 한 페이지에 자기 js 하나를 붙이는 지금 방식이 이 학기의 표준입니다.

---

## 2일차 · 26–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--두-칸-검사와-안내-문구-다듬기-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules

1. GitHub 웹에서 `README.md`를 만들고 `git pull`로 받아 옵니다.
2. 메시지 칸 검사를 더하고, 다시 입력하면 안내 문구가 지워지게 합니다.
3. 리허설 문항 하나(폼)를 풀어 보고, push한 뒤 공개 주소에서 캡처합니다.

**설명 합계: 8+7+6+5+4 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/my-web/guestbook.html
이름 student01 · 메시지 안녕하세요 를 넣고 [남기기]

마지막으로 남긴 글
student01: 안녕하세요
주소창이 함께 보이게 찍습니다
```

빈값 안내(`이름을 입력하세요.`)는 실습 중에 눈으로 확인하는 것이고 캡처에는 없어도 됩니다.
캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

이번 주로 **8주차 중간 실기 범위(2~7주차)**가 모두 채워졌습니다.

8주차 1일차는 시험과 같은 모양의 **리허설**이고, 2일차가 **본시험 60분**입니다.
본시험은 새 저장소를 만들지 않고 `my-web/exam/` 폴더에서 작업해 push합니다.
채점표와 리허설 starter는 오늘 공개했으니 미리 읽고 옵니다.
