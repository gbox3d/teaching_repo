---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 11주차"
footer: "객체와 localStorage · 비교 예제로 원리를 보고 마지막에 조립"
---

# 객체와 localStorage

10주차 방명록은 한 줄이 **글자 한 덩어리**였고, 새로고침하면 목록이 사라졌습니다.

이번 주 방식도 같습니다: **비교 예제 7개**를 하나씩 보고, 마지막에 새 저장소 `web-week11` 의 `guestbook.html`·`guestbook.js` 를 **조립**합니다(지난주 완성본에서 시작).

- 1일차: 한 줄을 이름·메시지·날짜 **객체**로 바꿉니다.
- 2일차: 목록을 브라우저 **저장 칸**(`localStorage`)에 남겨 새로고침해도 남게 합니다.
- **이번 주부터 확인·캡처는 공개 주소에서만** 합니다. 내 PC 와 공개 주소는 저장 칸이 다릅니다.

---

# 1일차 — 객체와 점 표기

`30분 설명·시연 → 60분 실습`

1. 고르기 페이지 — `index.html` 하나, script 줄 하나만 켠다
2. ex01 — 객체 `{ }` 와 점 표기 (오늘 문법)
3. ex02 — 배열 안의 객체 · 날짜 틀
4. ex03 — 객체를 목록 한 줄로

---

## 1일차 · 0–4분 — 고르기 페이지: script 줄 하나만 켠다

[examples/day1/index.html](examples/day1/index.html) — 세 예제가 같은 화면(목록 자리 두 개)을 씁니다.

```html
<script src="ex01_object.js"></script>
<!-- <script src="ex02_array_objects.js"></script> -->
<!-- <script src="ex03_list_line.js"></script> -->
```

- 6주차와 같은 방법입니다. 줄에 커서를 두고 **Ctrl+/**(macOS ⌘+/)로 켜고 끕니다.
- **한 줄만** 켭니다. 둘을 켜면 Console 이 섞이거나 이름이 겹쳐 빨간 줄이 뜹니다.
- ex01·ex02 는 Console 에, ex03 은 화면의 두 목록에 씁니다.

**어느 코드를 불러올지는 `script` 줄 하나가 정한다.**

---

## 1일차 · 4–11분 — ex01 객체와 점 표기

[examples/day1/ex01_object.js](examples/day1/ex01_object.js)

```js
const item = { name: '하늘', message: '안녕하세요', date: '2026. 11. 11.' };
console.log(item.name);    // 2. 하늘
console.log(item.nmae);    // 4. undefined — 빨간 줄 없음
const item5 = { name: name, message: message, date: '…' };   // 5.
```

- `{ }` 안에 `이름표: 값` 쌍을 쉼표로 잇습니다. 배열 `[ ]` 은 순서, 객체 `{ }` 는 이름표.
- 꺼낼 때는 **점 표기** `item.name`. 이름표에 따옴표를 붙이지 않습니다.
- `name: name` — 왼쪽은 이름표, 오른쪽은 변수입니다.

**객체는 이름표가 붙은 값 묶음이고, 점 뒤에 이름표를 쓰면 그 값이 나온다.**

---

## 1일차 · 11–19분 — ex02 배열 안의 객체 · 날짜 틀

[examples/day1/ex02_array_objects.js](examples/day1/ex02_array_objects.js)

```js
texts.push('하늘: 안녕하세요');                  // 1·2. 글자 한 덩어리
const today = new Date().toLocaleDateString();  // 날짜 글자 틀 한 줄
items.push({ name: '하늘', message: '안녕하세요', date: today });   // 3.
console.log(items[0].name);                     // 4. 하늘
```

- `texts[0]` 은 `'하늘: 안녕하세요'` 한 덩어리. 이름만 따로 꺼낼 수 없습니다.
- `items[0]` 으로 **몇 번째** 묶음, `.name` 으로 **무슨 값**. 대괄호가 먼저입니다.
- `toLocaleDateString()` 은 오늘 날짜를 `2026. 11. 11.` 모양 글자로 만드는 **틀**입니다.

**대괄호로 몇 번째인지, 점으로 무슨 값인지 고른다.**

---

## 1일차 · 19–27분 — ex03 객체를 목록 한 줄로

[examples/day1/ex03_list_line.js](examples/day1/ex03_list_line.js)

```js
li1.textContent = items[i];   // 1. 객체를 그대로
li2.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
```

```text
1. [object Object]       2. 하늘: 안녕하세요 (2026. 11. 11.)
```

- 객체를 통째로 글자 자리에 넣으면 `[object Object]`. **오류가 아니라서** Console 이 조용합니다.
- 백틱과 `${ }`(5주차)에 점 표기를 넣어 세 값을 한 줄로 씁니다.

**글자 자리에는 객체가 아니라 점 표기로 꺼낸 값을 넣는다.**

---

## 1일차 · 27–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--객체와-점-표기-60분) · [따라하기](walkthrough.md#1일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls)

1. 새 폴더 `web-week11` 에 지난주 완성본, `ex/` 에 오늘 네 파일.
2. ex01~ex03 — 줄 하나만 켜고 값 바꿔 보기. 무엇이 달라질지 먼저 말해 봅니다.
3. 새 저장소 `web-week11` 만들어 올리기 · Pages 켜기.

**설명 합계: 4+7+8+8+3 = 30분**

---

# 2일차 — 저장 칸에 남기고 되살리기, 그리고 조립

`30분 설명·시연 → 60분 실습`

1. ex04 — 저장 칸 `localStorage` 와 **Application** 탭
2. ex05 — `JSON.stringify` / `JSON.parse`
3. ex06 — `||` 또는 (오늘 문법)
4. ex07 — `removeItem`
5. 내 목록은 내 브라우저에만 있다
6. 조립 — `web-week11` 의 `guestbook.html`·`guestbook.js`

예제는 어제처럼 고르기 페이지 `index.html` 하나로 엽니다(script 줄 네 개 중 하나만).

---

## 2일차 · 0–7분 — ex04 저장 칸 localStorage

[examples/day2/index.html](examples/day2/index.html)(고르기 페이지, ex04 줄만 켬) · [ex04_storage.js](examples/day2/ex04_storage.js)

```js
let memo = '(처음 값)';                 // 1. 변수: 열 때마다 다시 시작
localStorage.getItem('ex04-memo');      // 2. 꺼내기. 없으면 null
localStorage.setItem('ex04-memo', '안녕하세요');   // 적기(키, 값)
```

- 저장하기 → 새로고침: 1번은 `(처음 값)`, 2번은 `안녕하세요`.
- **F12 › Application › Local Storage** › 지금 주소: 키와 값이 표로 보입니다.
- 저장 칸은 **주소마다** 따로 있고, **글자만** 담습니다.

**변수는 새로고침하면 처음으로 돌아가고, 저장 칸에 적은 것은 남는다.**

---

## 2일차 · 7–13분 — ex05 JSON: 배열을 글자로, 글자를 배열로

[examples/day2/ex05_json.js](examples/day2/ex05_json.js) — 고르기 페이지에서 ex05 줄만 켭니다.

```js
localStorage.setItem('ex05-raw', items);                      // 1.
localStorage.setItem('ex05-json', JSON.stringify(items));     // 2.
const back = JSON.parse(localStorage.getItem('ex05-json'));   // 3.
```

- 1번 값은 `[object Object],[object Object]`. 그대로 넣으면 내용이 사라집니다.
- 2번 값은 `[{"name":"하늘",…}]`. 3번 `JSON.parse` 로 되살려야 `back[0].name` 이 됩니다.
- 큰따옴표 `"name"` 모양을 기억해 둡니다. 12주차 JSON 파일과 같습니다.

**넣을 때 stringify, 꺼낼 때 parse.**

---

## 2일차 · 13–18분 — ex06 || 또는 (오늘 문법)

[examples/day2/ex06_or.js](examples/day2/ex06_or.js) — 고르기 페이지에서 ex06 줄만 켭니다.

```js
if (name === '' || message === '') { … }    // 1. 둘 중 하나라도 비면
const items = JSON.parse(localStorage.getItem('ex06-none')) || [];   // 3.
```

- `||` 는 **또는**입니다. if 안에서는 "둘 중 하나라도 참이면 참".
- 값 자리에서는 "앞이 없으면(`null`) 뒤 값". 처음 여는 사람의 저장 칸은 비어 있습니다.
- `|| []` 가 없으면 `null` 의 `length` 를 읽다가 빨간 줄이 뜹니다(4번 주석).

**처음 여는 사람을 위해 되살리는 줄 끝에 `|| []` 를 붙인다.**

---

## 2일차 · 18–23분 — ex07 removeItem: 저장 칸 지우기

[examples/day2/ex07_remove.js](examples/day2/ex07_remove.js) — 고르기 페이지에서 ex07 줄만 켭니다.

```js
items = [];                             // 1. 배열만 빈다. 저장 칸은 그대로
localStorage.removeItem('ex07-list');   // 2. 그 키를 지운다 → null
```

- 전체 지우기는 **둘 다** 합니다. 배열만 비우면 새로고침할 때 되살아납니다.
- `removeItem` 은 키 **하나**만 지웁니다. 다른 키(`ex07-other`)는 남습니다.
- 같은 아이디의 `github.io` 주소는 저장 칸을 **함께** 씁니다. 그래서 예제 키에 `ex07-` 를 붙였습니다.

**배열과 저장 칸은 따로다. 지울 때도 둘 다 지운다.**

---

## 2일차 · 23–26분 — 내 목록은 내 브라우저에만 있다

```text
내 PC 의 Chrome     'guestbook' 키에 내 글     내 화면에만 보인다
옆자리 PC           비어 있다                  내가 남긴 글이 없다
내 PC 의 file://    공개 주소와 다른 칸         그래서 확인은 공개 주소에서
```

- 저장한 목록의 주인은 **나 하나**입니다. 옆 사람이 같은 주소를 열어도 안 보입니다.
- 다른 PC 에서도 함께 보려면 **인터넷 서버 DB 와 로그인**이 필요합니다(선택 특강).
- 공용 PC 의 미리 보기 주소(`localhost:8000` 등)에는 앞사람 글이 남아 있을 수 있습니다. 같은 PC·같은 주소의 칸이기 때문입니다.

**localStorage 는 이 브라우저·이 주소에만 있는 저장 칸이다.**

---

## 2일차 · 26–30분 — 조립: web-week11, 그리고 실습 인계

```text
guestbook.html  #empty 줄 지우기 · [전체 지우기] 버튼   ← 10주 완성본 · ex04
guestbook.js    if (name === '' || message === '')       ← ex06 1번
                const today · push({ name: name, … })    ← ex02 · ex01 5번
                li.textContent = `${items[i].name}: …`    ← ex03 2번
                saveList() — setItem + JSON.stringify     ← ex04 · ex05
                let items = JSON.parse(getItem(…)) || []  ← ex05 · ex06 3번
                전체 지우기: items = [] + removeItem      ← ex07
```

[2일차 실습](lab.md#2일차--저장-칸에-남기고-되살리기-그리고-조립-60분) · [따라하기](walkthrough.md#2일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls)

1. 고르기 페이지와 ex04~ex07 `.js` 를 `ex/` 에 저장(어제 `index.html` 을 덮어씀), 값 바꾸기(29분까지).
2. 조립 → push → **공개 주소**에서 확인 → 캡처.

**설명 합계: 7+6+5+5+3+4 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/web-week11/guestbook.html
글 3개 → 새로고침 → F12 › Application › Local Storage 를 연 화면
하늘: 안녕하세요 (2026. 11. 11.)  [삭제]   …   3개
Key: guestbook   Value: [{"name":"하늘","message":"안녕하세요",…}, …]
```

주소창이 함께 보이게 찍습니다. 확인할 때 남긴 글이 보이면 **[전체 지우기]** 를 먼저 누릅니다.
캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

목록이 이제 **내 브라우저 안**에 남습니다. 다만 그 글은 나만 볼 수 있습니다.

12주차에는 새 저장소 `web-week12` 를 오늘 완성본에서 시작하고, `data/projects.json` 파일을 `fetch` 로 불러와 카드로 그립니다.
JSON 파일의 글자 모양은 오늘 Application 탭에서 본 값과 같습니다. 확인과 캡처는 12주차에도 공개 주소에서 합니다.
