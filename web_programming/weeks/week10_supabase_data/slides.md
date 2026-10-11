---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 10주차"
footer: "배열 데이터를 목록으로 그리기 · 비교 예제로 원리를 보고 마지막에 조립"
---

# 배열 데이터를 목록으로 그리기

7주차 방명록은 글을 남기면 카드 한 줄에 **마지막 글만** 보였습니다. 이번 주는 글을 **배열**에 쌓아 **목록**으로 그리고, 줄마다 **[삭제]** 를 붙입니다.

이번 주 방식도 같습니다: **비교 예제 7개**를 하나씩 보고, 마지막에 새 저장소 `web-week10` 의 `guestbook.html`·`guestbook.js` 를 **조립**합니다(지난주 완성본에서 시작).

- 값 여러 개는 배열 하나에 담고, 화면의 줄은 만들어서 붙입니다.
- 결과는 화면, **Console**(입력 칸에 `items` 치기), **Elements** 탭에서 봅니다.
- 파일 하나 = 개념 하나. 실습은 **값을 바꿔 보는 것**입니다.

---

# 1일차 — 배열과 목록 한 줄

`30분 설명·시연 → 60분 실습`

1. ex01 — 배열: `[]`·`push`·`length`·`items[i]` (오늘 문법)
2. ex02 — `for`: 처음부터 끝까지 (오늘 문법)
3. ex03 — 목록 한 줄: 만들고, 글자 넣고, 붙인다
4. ex04 — 누를 때마다 쌓기와 개수
5. 데이터가 가는 세 곳

---

## 1일차 · 0–5분 — ex01 배열: 값 여러 개를 순서대로

[examples/day1/index.html](examples/day1/index.html) 고르기 페이지 · [ex01_array.js](examples/day1/ex01_array.js)

```js
let items = [];                          // 1. 빈 배열, 개수 0
items.push('student01: 안녕하세요');      // 2. push 로 맨 뒤에 더한다
items.push('student02: 고맙습니다');      //    세 번 하면 개수 3
items.push('student03: 반갑습니다');
console.log('3. 첫 번째 items[0] :', items[0]);
console.log('4. 마지막 items[2] :', items[2]);
console.log('5. 없는 번호 items[3] :', items[3]);   // undefined
```

- 값이 셋이면 번호는 0·1·2, 개수는 3. **마지막 번호 = 개수 - 1**.
- 6번 `['student01', 'student02']` 는 쉼표로 나눠 처음부터 값을 넣은 배열입니다.

**배열은 값을 순서대로 담고, 번호는 0 부터 센다.**

---

## 1일차 · 5–10분 — ex02 for: 처음부터 끝까지

[examples/day1/ex02_for.js](examples/day1/ex02_for.js)

```js
// 배열에 4개가 들어 있다
for (let i = 0; i < 3; i++) {              // 1. 끝이 3 → 넷째를 빠뜨린다
    console.log('1.', i, items[i]);
}
for (let i = 0; i < items.length; i++) {   // 2. 끝이 length → 끝까지
    console.log('2.', i, items[i]);
}
```

- `let i = 0` 시작 · `i < items.length` 계속할 조건 · `i++` 한 바퀴마다 1 더하기.
- **몇 번째인지(`i`)가 필요해서** 이 모양을 씁니다. `items[i]` 가 그 번째 값입니다.

**끝은 숫자 대신 `items.length` 로 적는다.**

---

## 1일차 · 10–17분 — ex03 목록 한 줄: 만들고, 넣고, 붙인다

[examples/day1/ex03_create_li.js](examples/day1/ex03_create_li.js)

```js
const li2 = document.createElement('li');   // 만든다(아직 화면에 없다)
li2.textContent = '2. 만들고 붙인 줄';       // 글자를 넣는다
list.append(li2);                           // 목록 맨 뒤에 붙인다 → 보인다
```

- 1번(`li1`)은 만들기만 해서 Console 에만 있고, 화면과 **Elements** 에는 없습니다.
- `append` 는 늘 **맨 뒤**에 붙입니다. 3번이 2번 아래에 붙습니다.
- `textContent` 는 6주차와 같습니다. 글자를 글자 그대로 넣습니다.

**만든 요소는 `append` 로 붙여야 화면에 보인다.**

---

## 1일차 · 17–23분 — ex04 누를 때마다 쌓기와 개수

[examples/day1/ex04_push_add.js](examples/day1/ex04_push_add.js)

```js
addButton.addEventListener('click', function () {
    const text = textInput.value;
    items.push(text);                          // 1. 배열에 넣는다
    const li = document.createElement('li');   // 2. 화면에 붙인다
    li.textContent = text;
    list.append(li);
    count.textContent = `${items.length}개`;   // 3. 개수는 배열에서
});
```

- 배열과 화면은 **따로**입니다. 개수는 줄을 세지 않고 **`items.length`** 로 씁니다.

**배열이 원본이고, 화면은 그 배열을 비춘 것이다.**

---

## 1일차 · 23–27분 — 데이터가 가는 세 곳

```text
① 화면(배열)        오늘     새로고침하면 사라진다
② 브라우저 저장소   11주차   내 브라우저에 남는다
③ 인터넷 서버 DB    특강     여러 사람이 함께 본다
```

- 9주차에 본 그림입니다. 오늘 목록은 **①** — 배열과 화면에만 있습니다.
- 수업계획서의 "데이터 연결"은 이 순서로 갑니다: 오늘 ①, 다음 주 ②.
- ③은 [Supabase 선택 특강](../../specials/supabase_guestbook/README.md)에서 다룹니다.

**오늘 목록은 화면에만 있다. 새로고침하면 처음으로 돌아간다.**

---

## 1일차 · 27–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--배열과-목록-한-줄-60분) · [따라하기](walkthrough.md#1일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data)

1. 새 폴더 `web-week10` 에 지난주 완성본, `ex/` 에 오늘 다섯 파일.
2. ex01~ex04 — 줄 하나만 켜고 값 바꿔 보기. Console 입력 칸에 `items` 를 쳐 봅니다.
3. 새 저장소 `web-week10` 만들어 올리기 · Pages 켜기(2주차 순서 그대로).

**설명 합계: 5+5+7+6+4+3 = 30분**

---

# 2일차 — 다시 그리기와 삭제 버튼, 그리고 조립

`30분 설명·시연 → 60분 실습`

1. 지우려면 두 곳을 바꿔야 한다
2. ex05 — 비우고 다시 그리기: `list.innerHTML = ''`
3. ex06 — `showList()`: 화면을 배열대로
4. ex07 — 삭제 버튼 틀
5. 조립 — `web-week10` 의 `guestbook.html`·`guestbook.js`

---

## 2일차 · 0–4분 — 지우려면 두 곳을 바꿔야 한다

```text
1일차: 더하기 → 배열에 push         + 화면에 <li> 하나 append
오늘:  지우기 → 배열에서 하나 빼기  + 화면에서도 그 줄 빼기
```

- 한쪽만 바꾸면 배열과 화면이 어긋납니다. 1일차 ex04 에서 본 그대로입니다.
- 그래서 한 줄만 빼지 않고, **목록을 통째로 비우고 배열대로 다시 그립니다.**
- 더할 때도 지울 때도 같은 함수 하나를 부르면 됩니다.

**배열을 바꾸면 화면은 다시 그린다.**

---

## 2일차 · 4–10분 — ex05 비우고 다시 그리기

[examples/day2/ex05_redraw.html](examples/day2/ex05_redraw.html) · [ex05_redraw.js](examples/day2/ex05_redraw.js)

```js
// 2. 비우고 그리기
list.innerHTML = '';                        // 목록을 통째로 비운다
for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    list.append(li);
}
```

- 1번(비우지 않고)은 누를 때마다 세 줄씩 늘고, 2번은 몇 번을 눌러도 세 줄입니다.
- 이 수업에서 `innerHTML` 은 **비우기(`= ''`)에만** 씁니다. 글은 `textContent` 로 넣습니다.

**다시 그리기 전에 먼저 비운다.**

---

## 2일차 · 10–17분 — ex06 showList(): 화면을 배열대로

[examples/day2/ex06_show_list.html](examples/day2/ex06_show_list.html) · [ex06_show_list.js](examples/day2/ex06_show_list.js)

```js
function showList() {
    list.innerHTML = '';                       // 비우고
    for (let i = 0; i < items.length; i++) {   // 줄마다 만들어 붙이고
        …
    }
    count.textContent = `${items.length}개`;   // 개수와 안내 문장도
    if (items.length === 0) { … } else { … }
}
showList();                                    // 1. 열 때 한 번
```

- 2번: **더하기**를 누르면 `items.push(…)` 뒤에 `showList();` 를 부릅니다. 안내가 사라지고 개수가 오릅니다.

**화면에 보이는 것은 모두 배열에서 다시 만든다.**

---

## 2일차 · 17–24분 — ex07 삭제 버튼 틀

[examples/day2/ex07_delete_button.html](examples/day2/ex07_delete_button.html) · [ex07_delete_button.js](examples/day2/ex07_delete_button.js)

```js
const removeButton = document.createElement('button');
removeButton.textContent = '삭제';
removeButton.addEventListener('click', function () {
    items.splice(i, 1);     // 배열에서 i 번째 하나를 뺀다
    showList();             // 바뀐 배열대로 다시 그린다
});
li.append(removeButton);    // 버튼을 그 줄 안에 붙인다
```

- 이 일곱 줄은 **그대로 옮겨 쓰는 틀**입니다. `li.textContent` 줄과 `list.append(li)` 줄 사이에 넣습니다.
- 가운데를 지우면 그 줄만 사라지고 개수도 `3개` → `2개` 로 함께 줄어듭니다.

**`showList()` 가 다시 그릴 때 버튼마다 번호를 새로 붙인다.**

---

## 2일차 · 24–30분 — 조립: web-week10, 그리고 실습 인계

```text
guestbook.html  두 줄 → 네 줄(#list · #empty · #count) ← ex03 · ex06
guestbook.js    const list · empty · count             ← ex06
                let items = [];                        ← ex01
                showList(): 비우기 · for · li          ← ex05 · ex02 · ex03
                  + 삭제 버튼 틀 · 개수 · 안내         ← ex07 · ex04 · ex06
                submit: items.push(…); showList();     ← ex04 · ex06
                맨 끝: showList();                     ← ex06
```

[2일차 실습](lab.md#2일차--다시-그리기와-삭제-버튼-그리고-조립-60분) · [따라하기](walkthrough.md#2일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data)

1. ex05~ex07 `.html`·`.js` 를 `ex/` 에 저장, 값 바꾸기(29분까지).
2. 조립 → 375·1280 폭과 서버로 확인 → push → 3개 남기고 가운데 삭제, `2개` 캡처.

**설명 합계: 4+6+7+7+6 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/web-week10/guestbook.html
글 3개를 남기고 가운데 줄의 [삭제]를 누른 화면
· student01: 안녕하세요 [삭제]
· student03: 반갑습니다 [삭제]
2개
주소창이 함께 보이게 찍습니다
```

캡처에 실명·학번·실제 이메일이 보이지 않게 합니다. 새로고침하면 목록이 비므로 남긴 그 화면에서 바로 찍습니다.

---

## 다음 주 미리 보기

오늘 목록은 **화면에만** 있습니다. 새로고침하면 빈 목록으로 돌아갑니다.

11주차에는 새 저장소 `web-week11` 을 오늘 완성본에서 시작하고, 한 줄짜리 글을 이름·메시지·날짜를 담은 **객체**로 바꿉니다.
그리고 브라우저 저장소 `localStorage` 에 남겨 **새로고침해도 목록이 남게** 합니다. 그때부터 확인과 캡처는 **공개 주소에서만** 합니다.
