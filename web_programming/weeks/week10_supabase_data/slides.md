---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 10주차"
footer: "배열 데이터를 목록으로 그리기 · push, createElement, showList"
---

# 배열 데이터를 목록으로 그리기

7주차 방명록은 두 번째 글을 남기면 **앞 글이 사라졌습니다.**
카드가 한 줄이었기 때문입니다. 이번 주에는 글을 배열에 쌓아 목록으로 그립니다.

```text
guestbook.html   <ul id="list"></ul> · <p id="count">0개</p>   ← 목록 자리
guestbook.js     let items = []  →  push  →  <li>를 만들어 append
```

고치는 파일은 `guestbook.html`·`guestbook.js` 둘뿐입니다.

---

# 1일차 — 배열에 쌓아 목록으로 그리기

`30분 설명·시연 → 60분 실습`

1. 오늘 문법 — 배열 `push`·`length`·`[i]`·`for`
2. `createElement`·`textContent`·`append`
3. 7주차 코드에 다섯 줄 더하기
4. 항목 수와 데이터가 가는 세 곳

---

## 1일차 · 0–5분 — 오늘 문법: 배열에 쌓기

```js
let items = [];
items.push('student01: 안녕하세요');
items.push('student02: 고맙습니다');
console.log(items.length);   // 2
console.log(items[0]);       // student01: 안녕하세요

for (let i = 0; i < items.length; i++) {
  console.log(i, items[i]);
}
```

- 배열 `[ ]`은 값을 **여러 개** 담는 상자, `push`는 그 뒤에 하나를 더하는 일입니다.
- `length`는 개수, `items[0]`은 첫 번째 값입니다. 번호는 **0부터** 셉니다.
- `for`는 **몇 번째인지(`i`)가 필요해서** 씁니다. 오늘은 만들어만 두고 2일차에 씁니다.

---

## 1일차 · 5–12분 — createElement·textContent·append

```js
const li = document.createElement('li');
li.textContent = 'student01: 안녕하세요';
list.append(li);
```

```html
<ul class="card" id="list"></ul>   <!-- 비어 있는 채로 HTML에 둔다 -->
```

- `createElement('li')`는 **아직 화면에 없는** 새 `<li>`를 만듭니다.
- `textContent`는 그 안의 글자를 정합니다. 7주차에 쓴 것과 같습니다.
- `append`로 `<ul>` 안에 **붙여야** 비로소 화면에 보입니다. 세 줄이 한 묶음입니다.
- 만들기·글자 넣기·붙이기 순서를 바꾸지 않습니다.

---

## 1일차 · 12–20분 — 7주차 코드에 다섯 줄 더하기

```js
  clearNotice();
  const text = `${name}: ${message}`;
  items.push(text);
  const li = document.createElement('li');
  li.textContent = text;
  list.append(li);
```

- 7주차의 `last.textContent = …` 한 줄을 지우고 그 자리에 다섯 줄을 넣습니다.
- 같은 문장을 배열과 화면 **두 곳**에 넣습니다. 그래서 `const text`로 한 번만 만듭니다.
- 빈값 검사·`focus()`·`form.reset()`은 7주차 그대로 둡니다.
- `<p id="last">` 두 줄은 HTML에서 지우고 `<ul id="list">`로 바꿉니다.

---

## 1일차 · 20–25분 — 항목 수와 데이터가 가는 세 곳

```js
  count.textContent = `${items.length}개`;
```

```text
① 화면              오늘 목록이 있는 곳. 새로고침하면 사라진다
② 브라우저 저장소   내 브라우저에 남는다        → 11주차
③ 인터넷 서버       여러 사람이 함께 본다       → 선택 특강
```

- 화면에 쓰는 숫자를 세지 않습니다. **배열의 개수**를 그대로 보여 줍니다(9주차 복습).
- 오늘 목록은 **①**입니다. 새로고침하면 빈 목록으로 돌아갑니다.
- 데이터가 배열에 있고 화면은 그 배열을 비추는 것뿐이라는 점이 오늘의 핵심입니다.

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--배열에-쌓아-목록으로-그리기-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data

1. `guestbook.html`의 마지막 글 두 줄을 `<ul id="list">`와 `<p id="count">`로 바꿉니다.
2. `let items = []`에 쌓고, `<li>`를 만들어 목록에 붙입니다.
3. 남길 때마다 `N개`가 오르는지 보고, 이름을 비우고 눌러 7주차 안내가 그대로인지 봅니다.

**설명 합계: 5+7+8+5+5 = 30분**

막히면 Console의 **첫 빨간 줄**과 `guestbook.js:31` 같은 줄 번호부터 읽습니다.

---

# 2일차 — 다시 그리기와 삭제 버튼

`30분 설명·시연 → 60분 실습`

1. 지우려면 두 곳을 바꿔야 한다
2. `showList()` — 비우고 다시 그리기
3. 삭제 버튼 복붙 틀
4. 붙인 뒤 확인만

---

## 2일차 · 0–5분 — 지우려면 두 곳을 바꿔야 한다

```text
어제:  제출 → items에 push       + 화면에 <li> 하나 append
오늘:  삭제 → items에서 하나 빼기 + 화면에서도 그 줄만 빼기
```

- 어제는 **더하기**뿐이라 화면에 한 줄을 붙이면 끝이었습니다.
- 지우기는 배열과 화면 **두 곳**을 맞춰야 합니다. 한쪽만 바꾸면 숫자와 화면이 어긋납니다.
- 한 줄만 빼는 대신 **목록을 통째로 비우고 배열대로 다시 그리는** 방법을 씁니다.
- 방법이 하나라서 추가할 때도, 지울 때도 같은 함수를 부르면 됩니다.

---

## 2일차 · 5–12분 — showList(): 비우고 다시 그리기

```js
function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    list.append(li);
  }
  count.textContent = `${items.length}개`;
}
```

- `list.innerHTML = ''`는 목록을 **비웁니다.** 이 수업에서 `innerHTML`은 비우기에만 씁니다.
- 어제 submit 안에 있던 다섯 줄이 이 함수로 옮겨 오고, submit에는 두 줄만 남습니다.
- 목록 이름은 `showList`로 통일합니다. 추가·삭제 뒤에 이 함수를 부릅니다.

---

## 2일차 · 12–19분 — 삭제 버튼 복붙 틀

```js
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      showList();
    });
    li.append(removeButton);
```

- `splice(i, 1)`은 배열에서 `i`번째 값 **하나**를 뺍니다.
- 뺀 다음 `showList()`를 부르면 화면이 새 배열대로 다시 그려집니다.
- `showList()`가 다시 그릴 때 **버튼마다 번호를 새로 붙입니다.**
- 이 일곱 줄은 **그대로 옮겨 쓰는 틀**입니다. 오늘은 안을 뜯어보지 않습니다.

---

## 2일차 · 19–25분 — 붙인 뒤 확인만

```text
student01: 안녕하세요   [삭제]        3개
student02: 고맙습니다   [삭제]   →   가운데 [삭제] 클릭
student03: 반갑습니다   [삭제]
```

```text
student01: 안녕하세요   [삭제]        2개   ← 숫자도 함께 줄었다
student03: 반갑습니다   [삭제]
```

- 가운데를 지워도 남은 줄의 버튼이 **밀리지 않습니다.** 다시 그렸기 때문입니다.
- 항목 수는 `items.length`를 그대로 쓰므로 따로 빼거나 더하지 않습니다.
- 다 지우면 `아직 남긴 글이 없습니다.`가 보이게 한 줄을 더합니다.

---

## 2일차 · 25–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--다시-그리기와-삭제-버튼-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data

1. 어제 submit 안의 다섯 줄을 `showList()` 함수로 옮기고, submit에는 두 줄만 남깁니다.
2. 삭제 버튼 틀을 붙여 가운데 항목을 지워 봅니다.
3. 목록이 비면 `아직 남긴 글이 없습니다.`가 보이게 하고, push한 뒤 캡처합니다.

**설명 합계: 5+7+7+6+5 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/my-web/guestbook.html
글 3개를 남기고 가운데 한 줄의 [삭제]를 누른 화면

남긴 글
· student01: 안녕하세요   [삭제]
· student03: 반갑습니다   [삭제]
2개
```

주소창이 함께 보이게 찍습니다. 캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

지금 목록은 **화면에만** 있습니다. 새로고침하면 빈 목록으로 돌아갑니다.

11주차에는 항목을 `{ 이름, 메시지, 날짜 }` **객체**로 바꾸고 `localStorage`에 저장해
새로고침해도 남게 합니다. 그때부터 확인과 캡처는 **공개 주소에서만** 합니다.
12주차에는 JSON 파일에서 데이터를 불러와 카드로 그립니다.
