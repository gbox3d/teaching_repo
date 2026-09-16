---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 11주차"
footer: "객체와 localStorage · object, JSON.stringify, localStorage"
---

# 객체와 localStorage

10주차 방명록은 새로고침하면 **목록이 사라졌습니다.** 값도 `student01: 안녕하세요` 문자열 한 덩어리였습니다.
이번 주에는 항목을 객체로 바꾸고 브라우저 저장소에 적어 둡니다.

```text
guestbook.js   items = ['하늘: 안녕하세요']            ← 10주차
               items = [{ name, message, date }]       ← 오늘 1일차
               localStorage['guestbook'] 에 저장·복원   ← 오늘 2일차
```

고치는 파일은 `guestbook.html`·`guestbook.js` 둘뿐입니다.

---

# 1일차 — 항목을 객체로 바꾸기

`30분 설명·시연 → 60분 실습`

1. 오늘 문법 — 객체와 점 표기
2. 배열 안의 객체
3. 남긴 글을 객체로 바꾸기
4. 목록 한 줄에 이름·메시지·날짜

---

## 1일차 · 0–5분 — 오늘 문법: 객체와 점 표기

```js
const item = { name: '하늘', message: '안녕하세요', date: '2026. 9. 16.' };

console.log(item.name);      // 하늘
console.log(item.date);      // 2026. 9. 16.
```

- 객체 `{ }`는 **이름표가 붙은 값**을 한 묶음으로 담습니다.
- `이름: 값` 쌍을 쉼표로 이어 적습니다. 이름표는 `name`·`message`·`date` 세 개입니다.
- 꺼낼 때는 **점 표기** `item.name`을 씁니다. 이름표에 따옴표를 붙이지 않습니다.
- 배열 `[ ]`은 순서대로 여러 개, 객체 `{ }`는 이름표가 붙은 한 묶음입니다.

---

## 1일차 · 5–12분 — 배열 안의 객체

```js
let items = [];
items.push({ name: '하늘', message: '안녕하세요', date: '2026. 9. 16.' });
items.push({ name: '바다', message: '잘 봤습니다', date: '2026. 9. 16.' });

console.log(items.length);       // 2
console.log(items[0].name);      // 하늘
console.log(items[1].message);   // 잘 봤습니다
```

- 10주차의 배열은 그대로입니다. 담기는 값이 문자열에서 **객체**로 바뀔 뿐입니다.
- `items[i]`로 한 묶음을 꺼내고, 뒤에 `.name`을 붙여 그 안의 값 하나를 꺼냅니다.
- `items[0].name`은 "첫 번째 글의 이름"입니다. 번호는 **0부터** 셉니다.

---

## 1일차 · 12–18분 — 남긴 글을 객체로 바꾸기

```js
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
```

- 10주차에는 문장 하나를 넣었습니다. 이제 **세 값을 이름표와 함께** 넣습니다.
- `new Date().toLocaleDateString()`은 오늘 날짜를 `2026. 9. 16.`으로 만드는 **복붙 틀** 한 줄입니다.
- 안내 문구도 오늘 정리합니다. 두 갈래를 `if (name === '' || message === '')` 한 갈래로 합칩니다.
- `||`는 **또는**입니다. 둘 중 하나라도 비면 안내를 보여 주고 `return`으로 멈춥니다.
- `<p id="empty">`는 지우고, 빈 목록 안내는 개수 자리(`#count`)에서 함께 보여 줍니다.

---

## 1일차 · 18–25분 — 목록 한 줄에 이름·메시지·날짜

```js
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
```

```text
하늘: 안녕하세요 (2026. 9. 16.)   [삭제]
바다: 잘 봤습니다 (2026. 9. 16.)   [삭제]
2개
```

- `showList()`에서 바뀌는 줄은 **이 한 줄**입니다. 나머지는 10주차 그대로입니다.
- 점 표기를 빼고 `items[i]`만 쓰면 화면에 `[object Object]`가 보입니다.
- 개수 자리는 이제 두 가지 일을 합니다. 목록이 비면 안내 문장, 아니면 `2개`.

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--항목을-객체로-바꾸기-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls

1. `items.push`에 넣는 값을 이름·메시지·날짜 **객체**로 바꿉니다.
2. 목록 한 줄을 점 표기로 고쳐 세 값이 함께 보이게 합니다.
3. 안내 문구를 한 줄로 합치고, 빈 목록 안내를 개수 자리로 옮깁니다.

**설명 합계: 5+7+6+7+5 = 30분**

오늘은 아직 새로고침하면 사라집니다. 저장은 내일 합니다.

---

# 2일차 — 브라우저에 저장하고 되살리기

`30분 설명·시연 → 60분 실습`

1. 새로고침하면 왜 사라지나
2. `JSON.stringify`와 `saveList()`
3. 페이지를 열 때 되살리기
4. Application 탭과 전체 지우기

---

## 2일차 · 0–6분 — 새로고침하면 왜 사라지나

```text
① 화면(메모리)      새로고침하면 사라진다             ← 어제까지
② 브라우저 저장소    같은 브라우저·같은 주소면 남는다    ← 오늘
③ 인터넷 서버 DB     다른 사람·다른 PC에서도 본다        ← 선택 특강
```

- `let items = [];`는 페이지를 열 때마다 **빈 배열로 다시 시작**합니다.
- 브라우저에는 주소마다 작은 저장 칸이 있습니다. 이것이 `localStorage`입니다.
- 저장 칸에는 **문자열만** 넣을 수 있습니다. 배열은 그대로 들어가지 않습니다.
- 그래서 오늘 두 가지를 합니다. 배열을 문자열로 바꾸기, 문자열을 배열로 되살리기.

---

## 2일차 · 6–13분 — JSON.stringify와 saveList()

```js
function saveList() {
  localStorage.setItem('guestbook', JSON.stringify(items));
}
```

```text
Key     guestbook
Value   [{"name":"하늘","message":"안녕하세요","date":"2026. 9. 16."}]
```

- `JSON.stringify(items)`는 배열을 **한 줄 문자열**로 바꿉니다.
- `localStorage.setItem('키', '값')`은 그 문자열을 브라우저에 적어 둡니다.
- 키 이름은 `guestbook`으로 **고정**합니다. 이름이 다르면 다른 칸에 저장됩니다.
- 추가한 뒤·삭제한 뒤 **두 곳**에서 `saveList()`를 부릅니다.

---

## 2일차 · 13–20분 — 페이지를 열 때 되살리기

```js
let items = JSON.parse(localStorage.getItem('guestbook')) || [];
```

- `getItem('guestbook')`은 적어 둔 **문자열**을 꺼냅니다. 적어 둔 적이 없으면 `null`입니다.
- `JSON.parse(…)`는 그 문자열을 다시 **배열**로 되살립니다.
- `|| []`는 "앞이 없으면 빈 배열로"라는 뜻입니다. 처음 여는 사람은 여기로 갑니다.
- 이 한 줄은 **복붙 틀**입니다. `let items = [];` 자리에 그대로 바꿔 넣습니다.
- 파일 맨 끝의 `showList();`가 되살린 배열을 그려 줍니다. 10주차에 넣어 둔 줄입니다.

---

## 2일차 · 20–25분 — Application 탭과 전체 지우기

```js
clearButton.addEventListener('click', function () {
  items = [];
  localStorage.removeItem('guestbook');
  showList();
});
```

- **F12 › Application › Local Storage**에서 `guestbook` 키와 값을 눈으로 봅니다.
- `removeItem('guestbook')`은 저장 칸을 지우고, `items = [];`는 화면 쪽 배열을 비웁니다.
- 공용 PC에서는 같은 아이디의 `github.io` 주소가 저장 칸을 **함께** 씁니다.
- 앞사람 글이 보이면 **[전체 지우기]**를 먼저 누르고 **자기 항목만** 캡처합니다.

---

## 2일차 · 25–28분 — 내 목록은 내 브라우저에만 있다

```text
내 PC 브라우저   localStorage['guestbook']   내 화면에만 보인다
옆자리 PC        비어 있다                   내가 남긴 글이 없다
```

- 오늘 저장한 목록은 **내 브라우저 안**에만 있습니다. 그 글의 주인은 나 하나입니다.
- 옆 사람이 같은 공개 주소를 열어도 내가 남긴 글은 보이지 않습니다.
- 다른 PC에서도 함께 보려면 **인터넷 서버 DB와 로그인**이 필요합니다.
- 서버 DB와 로그인은 선택 특강에서 다룹니다. 이 과목의 저장은 여기까지입니다.

---

## 2일차 · 28–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--브라우저에-저장하고-되살리기-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls

1. `saveList()`를 만들고 추가한 뒤·삭제한 뒤에 부릅니다.
2. `let items = …` 줄을 복붙 틀로 바꿔 새로고침해도 남게 합니다.
3. **[전체 지우기]** 버튼을 붙이고 공개 주소에서 캡처합니다.

**설명 합계: 6+7+7+5+3+2 = 30분**

오늘부터 확인과 캡처는 **공개 주소에서만** 합니다.

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/my-web/guestbook.html
글 3개를 남기고 새로고침한 뒤 F12 › Application › Local Storage를 함께 연 화면

하늘: 안녕하세요 (2026. 9. 16.)   [삭제]      3개
Key: guestbook
Value: [{"name":"하늘","message":"안녕하세요","date":"2026. 9. 16."}, …]
```

주소창이 함께 보이게 찍습니다. 앞사람 글이 보이면 **[전체 지우기]**를 먼저 누릅니다.
캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

목록이 이제 **내 브라우저 안**에 남습니다. 다만 그 글은 나만 볼 수 있습니다.

12주차에는 `data/projects.json` 파일을 만들어 **fetch**로 불러오고, 읽어 온 값을 카드로 그립니다.
JSON 파일의 글자 모양은 오늘 Application 탭에서 본 값과 같습니다.
확인과 캡처는 12주차에도 공개 주소에서 합니다.
