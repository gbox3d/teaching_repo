---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 11주차"
footer: "객체와 localStorage · 강의 60분 · 실습 30분"
---

# 객체와 localStorage

10주차 방명록은 한 줄이 **글자 한 덩어리**였고, 새로고침하면 목록이 사라졌습니다.

각 수업은 **강의·시연 60분 + 실습 30분**입니다. 2일차 필수 실습은 ex04~ex06이며, 완성 방명록은 강의자 시연·12주차 준비 자료입니다.

- 1일차: 한 줄을 이름·메시지·날짜 **객체**로 바꿉니다.
- 2일차: 이름·메시지를 저장하고 새로고침 후 폼에 복원합니다.
- 제출은 ex06의 복원된 폼과 저장 JSON입니다. **localhost 캡처를 인정합니다.**

---

# 1일차 — 객체와 점 표기

`강의·시연 60분 → 실습 30분`

1. 교재 폴더와 공용 CSS, 정적 서버
2. ex01 — 객체 `{ }` 와 점 표기 (오늘 문법)
3. ex02 — 배열 안의 객체 · 날짜 틀
4. ex03 — 객체를 목록 한 줄로

---

## 1일차 · 0–10분 — 교재 폴더와 실행 환경

교재의 `web_programming` 폴더 구조를 유지합니다.

```text
web_programming/
  shared/examples.css
  weeks/week11_object_localstorage/examples/
```

- 서버 루트는 `web_programming`, 포트는 `8111`입니다.
- 2일차는 W3.CSS CDN과 `shared/examples.css`를 읽습니다. CDN에는 인터넷 연결이 필요합니다.
- ex01·ex02는 Console, ex03은 화면의 두 목록을 비교합니다.

실행 명령과 주소: [따라하기](walkthrough.md#준비)

---

## 1일차 · 10–25분 — ex01 객체와 점 표기

[examples/day1/ex01/index.html](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex01/index.html) · [app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex01/app.js)

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

## 1일차 · 25–40분 — ex02 배열 안의 객체 · 날짜 틀

[examples/day1/ex02/index.html](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex02/index.html) · [app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex02/app.js)

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

## 1일차 · 40–55분 — ex03 객체를 목록 한 줄로

[examples/day1/ex03/index.html](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex03/index.html) · [app.js](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day1/ex03/app.js)

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

## 1일차 · 55–60분 — 30분 실습 안내

[1일차 실습](lab.md#1일차--객체와-점-표기-30분) · [따라하기](walkthrough.md#1일차)

| 실습 시간 | 확인 |
|---|---|
| 0–5분 | 서버·ex01·Console 열기 |
| 5–13분 | 객체의 이름과 속성 출력 비교 |
| 13–21분 | 배열 인덱스 0과 1 비교 |
| 21–28분 | 목록과 속성 철자 비교 |
| 28–30분 | 변경한 값과 결과 설명 |

강의 합계: 10+15+15+15+5 = 60분. 공개 업로드는 실습에 포함하지 않습니다.

---

# 2일차 — 문자열에서 폼 저장까지

`강의·시연 60분 → 실습 30분`

1. ex04 — 문자열 저장·불러오기·지우기
2. ex05 — JSON 문자열과 복원한 배열 비교
3. ex06 — 이름·메시지 폼 저장·복원
4. 저장 범위와 검증 순서
5. 30분 실습과 캡처 안내

필수는 **ex04~ex06 세 개**입니다. 화면에서 입력하고 버튼을 누른 다음 코드를 읽습니다.

---

## 2일차 · 0–10분 — ex04 문자열 저장

[화면 소스](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex04/index.html) · [JavaScript](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex04/app.js)

```js
localStorage.setItem('week11-ex04-text', '안녕하세요');
const text = localStorage.getItem('week11-ex04-text');
localStorage.removeItem('week11-ex04-text');
```

- 입력 → **저장** → 입력 변경 → **불러오기**로 저장한 값을 확인합니다.
- 새로고침 후에도 **불러오기**로 읽을 수 있습니다.
- 빈 문자열을 저장하면 `''`, 키를 지우면 `null`입니다.
- **Application › Local Storage**에서 현재 origin의 키와 값을 확인합니다.

---

## 2일차 · 10–25분 — ex05 JSON 저장과 복원

[화면 소스](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex05/index.html) · [JavaScript](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex05/app.js)

```js
localStorage.setItem('week11-ex05-items', JSON.stringify(items));
const text = localStorage.getItem('week11-ex05-items');
const restored = JSON.parse(text); // 저장된 JSON이 있을 때
```

1. **JSON 저장**: 고정된 두 객체의 배열을 문자열로 저장합니다.
2. **저장 원문 조회**: `[{"name":"하늘",…}]`를 확인합니다.
3. **JSON 복원**: 각 객체의 이름·메시지와 개수 2를 확인합니다.

코드의 배열을 바꾸어도 기존 저장 값은 그대로입니다. 다시 저장한 뒤 비교합니다.

---

## 2일차 · 25–40분 — ex06 입력 폼 저장과 복원

[화면 소스](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex06/index.html) · [JavaScript](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week11_object_localstorage/examples/day2/ex06/app.js)

```js
const entry = { name: nameInput.value, message: messageInput.value };
const text = JSON.stringify(entry);
localStorage.setItem(key, text);
// 저장된 JSON이 있는 상태에서 불러오기
const restored = JSON.parse(localStorage.getItem(key));
nameInput.value = restored.name;
messageInput.value = restored.message;
```

- 이름·메시지 입력 → **저장** → 입력 변경 → **불러오기**.
- 새로고침 후 불러와도 두 입력이 복원됩니다. **지우기**는 키와 입력을 비웁니다.
- 이 예제는 빈 입력도 저장합니다. 새로고침한 뒤에는 불러오기를 눌러 복원합니다.

---

## 2일차 · 40–50분 — 저장 공간은 브라우저·origin별

```text
localhost:8111의 ex04·ex06  같은 origin, 다른 키
localhost:8000             다른 포트 → 다른 저장 공간
127.0.0.1:8111             다른 호스트 → 다른 저장 공간
공개 HTTPS 사이트         다른 origin → 다른 저장 공간
```

- origin은 **프로토콜·호스트·포트**입니다. 폴더 경로는 포함하지 않습니다.
- 같은 origin이어도 다른 브라우저나 다른 PC와 공유하지 않습니다.
- `file://`의 저장 동작은 브라우저마다 다를 수 있으므로 정적 서버로 엽니다.
- 다른 PC와 공유하는 서버 방명록은 12~14주에 만듭니다.

---

## 2일차 · 50–55분 — 저장 결과 검증

| 조작 | 예상 결과 |
|---|---|
| 저장 후 입력만 바꾸고 불러오기 | 저장한 값으로 복원 |
| 새로고침 후 불러오기 | 같은 값과 JSON 복원 |
| 지우기 후 불러오기 | 저장된 값 없음 |
| 캡처용으로 다시 저장·복원 | 입력과 JSON 일치 |

화면에서 확인한 뒤 `setItem` → `getItem` → `JSON.parse`를 코드에서 찾습니다.
저장 키와 origin이 같아야 같은 값을 읽습니다.

---

## 2일차 · 55–60분 — 30분 실습 안내

| 실습 시간 | 작업 |
|---|---|
| 0–8분 | ex04 저장·불러오기·지우기 |
| 8–16분 | ex05 원문·복원 비교 |
| 16–27분 | ex06 저장·새로고침·폼 복원·지우기 |
| 27–30분 | ex06을 다시 저장·복원하고 캡처 |

[2일차 실습](lab.md#2일차--저장과-폼-복원-30분) · [따라하기](walkthrough.md#2일차)

강의 합계: 10+15+15+10+5+5 = 60분

---

## 제출 — 복원한 폼 한 장

ex06에서 저장 → 새로고침 → 불러오기를 실행합니다.

```text
이름: 하늘
메시지: 안녕하세요
저장 JSON: {"name":"하늘","message":"안녕하세요"}
상태: 폼 복원 완료
```

입력·JSON·주소창을 함께 캡처합니다. **localhost 화면을 인정합니다.**
공개 업로드는 수업 후 정리하며, 실명·학번·실제 이메일은 쓰지 않습니다.

---

## 다음 주 준비와 별도 자료

[완성 방명록](examples/day2/web-week11/README.md)은 강의자가 시연하고 12주차 준비 자료로 제공합니다. 이번 주 학생 필수 구현 대상이 아닙니다.

12주차에는 준비된 화면에서 공용 REST API의 JSON 목록을 읽습니다.

- [배열 심화](../../specials/array_advanced/README.md)는 별도 보강특강입니다.
- [ex07 탭 동기화](examples/day2/README.md#고급-저장-참고)은 참고 자료입니다.
