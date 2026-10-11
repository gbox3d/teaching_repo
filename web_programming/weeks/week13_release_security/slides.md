---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 13주차"
footer: "보안·접근성·릴리스 점검 · 비교 예제로 원리를 보고 마지막에 조립"
---

# 보안·접근성·릴리스 점검

12주차까지 네 페이지를 만들었습니다. 이번 주는 새 기능보다 **내놓기 전 점검**입니다.

이번 주 방식도 같습니다: **비교 예제 8개**를 하나씩 보고, 마지막에 새 저장소 `web-week13` 에 `about.html`·`about.js`·`projects.js`·`README.md` 를 **조립**합니다(지난주 완성본에서 시작).

- 입력한 글은 **글자로** 넣습니다 — `textContent`
- 그림·칸·링크에는 **무엇인지 알려 주는 글자** — `alt`·`label for`·링크 글자
- 내놓기 전 **링크 → Console → 375**, README 는 마크다운 네 가지

---

# 1일차 — 숫자와 글자, 그리고 접근성

`30분 설명·시연 → 60분 실습`

1. 고르기 페이지 — 입력 칸·버튼·결과 자리
2. ex01 — `Number()` 와 `isNaN()`
3. ex02 — `new Date().getFullYear()` 와 몇 년차
4. ex03 — `textContent` vs `innerHTML`
5. 공개 저장소에 넣지 않는 것
6. ex04 `alt` · ex05 `label for`

---

## 1일차 · 0–3분 — 고르기 페이지: 입력 칸이 있는 자리

[examples/day1/index.html](examples/day1/index.html) — ex01·ex02 가 같은 화면을 씁니다.

```html
<label for="year">입학 연도</label>
<input id="year" type="text" value="2023">
<button id="btn">눌러 보기</button>
<div id="result">결과 자리 — 버튼을 누르면 바뀐다</div>
```

- 맨 아래 `script` 두 줄 중 **하나만** 켭니다(Ctrl+/, macOS ⌘+/).
- 칸에 글자를 적고 **눌러 보기** → 화면과 Console 을 봅니다.

**칸에 적은 글자는 버튼을 누를 때 읽는다.**

---

## 1일차 · 3–8분 — ex01 Number() 와 isNaN()

[examples/day1/ex01_number.js](examples/day1/ex01_number.js)

```js
const text = yearInput.value;                     // 칸의 값은 글자
console.log('1. 글자 + 1 :', text + 1);            // 20231 — 이어 붙는다
const year = Number(text);                        // 글자를 숫자로
console.log('2. Number(글자) + 1 :', year + 1);    // 2024 — 더해진다
console.log('3. isNaN(바꾼 값) :', isNaN(year));    // false
```

- `Number('이천이십삼')` → `NaN`(숫자가 아님), `isNaN(NaN)` → `true`
- 빈칸은 `Number('')` → `0` 입니다. 그래서 `text === ''` 도 함께 묻습니다.

**칸의 글자는 `Number()` 로 바꾸고, 바뀌었는지는 `isNaN()` 으로 묻는다.**

---

## 1일차 · 8–12분 — ex02 올해와 몇 년차

[examples/day1/ex02_year.js](examples/day1/ex02_year.js)

```js
const thisYear = new Date().getFullYear();  // 1. 올해 → 2026
console.log('2. 올해 - 입학 연도 :', thisYear - year);  // 2. 2026 - 2023 → 3
const years = thisYear - year + 1;          // 3. 입학한 해가 1년차 → 4
```

- 5주차 ex10 에서 본 `getFullYear()` 입니다. 올해를 `2026` 이라고 직접 적지 않습니다.
- 괄호를 빠뜨리면(`getFullYear;`) 오류 없이 `NaN년차` 입니다. 부를 때는 괄호.

**올해는 `new Date().getFullYear()` 로 꺼낸다.**

---

## 1일차 · 12–18분 — ex03 textContent vs innerHTML

[examples/day1/ex03_text_html.html](examples/day1/ex03_text_html.html) · [ex03_text_html.js](examples/day1/ex03_text_html.js)

```js
output.textContent = input.value;   // 1. <b>안녕</b> 이 글자 그대로
output.innerHTML = input.value;     // 2. 굵은 안녕 — 태그가 진짜 요소가 된다
output.innerHTML = '';              // 3. 비우기 — 이때만 innerHTML
```

- 같은 입력, 같은 자리, **단어 하나** 차이입니다.
- 칸에 `<button>가짜 버튼</button>` → 2번에서 진짜 버튼이 생깁니다. 남이 쓴 글이라면?

**입력한 글은 `textContent` 로 넣는다. `innerHTML` 은 비울 때만.**

---

## 1일차 · 18–21분 — 공개 저장소에 넣지 않는 것

| 넣지 않는 것 | 대신 쓰는 예시 |
|---|---|
| 실명·학번·전화번호 | `student01` |
| 실제 이메일 | `student01@example.com` |
| 비밀번호·로그인 키 | 적지 않습니다 |

- 저장소는 **Public** 입니다. 주소만 알면 누구나 파일을 엽니다.
- 한 번 올린 것은 파일에서 지워도 GitHub 의 이전 기록에 남습니다. **처음부터** 넣지 않습니다.
- 캡처도 같습니다. 주소창의 아이디는 보여도 됩니다.

**공개 저장소에는 예시 값만 쓴다.**

---

## 1일차 · 21–25분 — ex04 alt: 그림이 안 보일 때 읽히는 글

[examples/day1/ex04_alt.html](examples/day1/ex04_alt.html) · 그림 [images/profile.png](examples/day1/images/profile.png)

```html
<img src="images/profile.png" alt="student01의 프로필 그림" width="160">
<img src="images/profile.png" width="160">
<img src="images/profile.png" alt="그림" width="160">
```

- 1 알맞은 alt / 2 alt 없음 / 3 '그림' 한 낱말. 셋은 눈으로 똑같습니다.
- `src` 를 `images/nothing.png` 로 바꾸면 그림 자리에 무엇이 남는지 다릅니다.

**`alt` 는 그림이 안 보일 때 대신 읽히는 글이다. 무슨 그림인지 적는다.**

---

## 1일차 · 25–28분 — ex05 label for: 이름표를 칸에 잇는다

[examples/day1/ex05_label.html](examples/day1/ex05_label.html)

```html
<label for="year1">입학 연도</label> <input id="year1">    <!-- 1. 같다 -->
<label for="year2">입학 연도</label> <input id="years2">   <!-- 2. 다르다 -->
입학 연도 <input id="year3">                               <!-- 3. label 없음 -->
```

- 이름표 글자를 눌러 보세요. 커서가 칸으로 가는 것은 1번뿐입니다.
- 1번과 3번은 눈으로 같습니다. 이어졌는지는 **눌러 봐야** 압니다.

**`for` 와 `id` 가 글자까지 같아야 이름표가 칸에 이어진다.**

---

## 1일차 · 28–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--숫자와-글자-그리고-접근성-60분) · [따라하기](walkthrough.md#1일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

1. 새 폴더 `web-week13` 에 지난주 완성본, `ex/` 에 오늘 일곱 파일과 그림 하나.
2. ex01~ex05 — 값 바꿔 보기. 무엇이 달라질지 먼저 말해 봅니다.
3. 새 저장소 `web-week13` 만들어 올리기 · Pages 켜기.

**설명 합계: 3+5+4+6+3+4+3+2 = 30분**

---

# 2일차 — README 와 점검, 그리고 조립

`30분 설명·시연 → 60분 실습`

1. ex06 — 링크·버튼 글자와 Tab 키
2. ex07 — 마크다운 `#` 과 `-`
3. ex08 — 링크와 그림, `!` 하나 차이
4. 내놓기 전 점검 순서 — 링크 → Console → 375
5. 14주차 발표 · 15주차 문제 은행
6. 조립 — `about.html`·`about.js`·`projects.js`·`screenshots/`·`README.md`

---

## 2일차 · 0–5분 — ex06 링크·버튼 글자

[examples/day2/ex06_link_text.html](examples/day2/ex06_link_text.html)

```text
1. 페이지 열기 · 페이지 열기 · 페이지 열기          ← 어디로 가나?
2. img 설명 열기 · label 설명 열기 · a 설명 열기    ← 글자만 읽어도 안다
3. [▶]  [계산하기]                                  ← 누르면 무엇을 하나?
```

- **Tab** 키로 옮겨 다니며 테두리가 생긴 것의 글자만 읽어 봅니다.
- 12주차 카드 링크 세 장은 모두 `페이지 열기` 였습니다. 오늘 조립에서 고칩니다.

**링크·버튼 글자는 그것만 읽어도 무엇인지 알게 쓴다.**

---

## 2일차 · 5–10분 — ex07 마크다운 # 과 -

[examples/day2/ex07_line_marks.md](examples/day2/ex07_line_marks.md) — 9주차 복습 · 미리 보기(Ctrl+K V)

```markdown
# 큰 제목
## 작은 제목 — README 의 절 제목
- 목록 한 줄
#띄어쓰기가 없으면 글자 그대로
```

- 기호 없이 줄만 바꾼 두 줄은 미리 보기에서 **한 줄로 붙습니다**. 그래서 `- ` 를 붙입니다.

**줄 맨 앞 기호와 띄어쓰기 한 칸이 그 줄의 모양을 정한다.**

---

## 2일차 · 10–16분 — ex08 링크와 그림

[examples/day2/ex08_link_image.md](examples/day2/ex08_link_image.md) · 그림 [images/profile.png](examples/day2/images/profile.png)

```markdown
[13주차 실습 페이지](https://github.com/…)        1. 링크
![student01의 프로필 그림](images/profile.png)   2. 링크 앞에 ! → 그림
[student01의 프로필 그림](images/profile.png)    3. ! 가 없으면 링크
![student01의 프로필 그림](images/Profile.png)   4. 대소문자 다름
```

- 대괄호 글자는 그림의 `alt` 입니다(ex04).
- 4번은 내 PC 미리 보기에서는 보이고, GitHub 에 올리면 깨집니다.

**그림은 링크 앞에 `!`. 경로는 파일 이름과 글자 하나까지 같게 적는다.**

---

## 2일차 · 16–21분 — 내놓기 전 점검 순서

```text
1. 링크      nav 네 개 · 카드 링크 세 개를 모두 눌러 404 가 없는지
2. Console   페이지마다 빨간 줄 0(favicon 404 제외). 버튼을 누른 뒤에도 본다
3. 375 폭    기기 모드(Ctrl+Shift+M)에서 가로로 밀리지 않는지
```

- 순서를 지킵니다. 링크가 깨진 채로 Console 을 보면 원인이 섞입니다.
- 이어서 그림 `alt`(ex04)·이름표(ex05)·개인정보를 한 번씩 봅니다.
- 내 PC 서버는 대소문자가 달라도 엽니다. push 뒤 **공개 주소에서 링크를 한 번 더** 누릅니다.

**고치기 전에 순서대로 찾는다: 링크 → Console → 375.**

---

## 2일차 · 21–25분 — 14주차 발표와 15주차 문제 은행

- 14주차는 **3분 시연**입니다. 오늘 완성본에서 시작한 `web-week14` 의 공개 주소로 합니다.
- 순서: 공개 주소 → 페이지 이동 → 다크 모드 → 폼 빈값 안내 → 방명록 추가·삭제 → 새로고침 → JSON 카드 → Commits 탭과 README
- 레포트는 오늘 쓰는 `README.md` 최종판입니다. 따로 내는 문서는 없습니다.
- 15주차 기말 실기는 1~14주 실습 제출로 만든 [문제 은행](../week15_final_exam/examples/README.md)에서 값을 바꿔 냅니다.
- 이번 주 제출도 그 안의 [w13_text_safe](../week15_final_exam/examples/w13_text_safe/README.md) 문제입니다.

**발표는 말보다 화면을 눌러 보여 주는 것이다.**

---

## 2일차 · 25–30분 — 조립: web-week13, 그리고 실습 인계

```text
about.html   script 줄 · 폼 · label for · 결과 카드  ← ex05 · ex06
about.js     Number · isNaN · getFullYear · + 1      ← ex01 · ex02
             submit · preventDefault · trim          ← 12주 guestbook.js
projects.js  `${projects[i].title} 열기`             ← ex06 2번
README.md    # · ## · - · 링크 · 그림 줄              ← ex07 · ex08
```

[2일차 실습](lab.md#2일차--readme-와-점검-그리고-조립-60분) · [따라하기](walkthrough.md#2일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

1. ex06~ex08 값 바꾸기(17분까지) → 조립(README 는 맨 끝) → 링크·Console·375 점검.
2. push → 저장소 첫 화면 README → 공개 주소에서 링크 한 번 더 → 375 방명록 캡처.

**설명 합계: 5+5+6+5+4+5 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/web-week13/guestbook.html   (기기 모드 375px)
목록 ─ student02: <b>안녕</b> (남긴 날짜) [삭제]   ← 굵게가 아니라 글자 그대로
F12 › Console ─ 빨간 줄 없음(favicon.ico 404 는 세지 않음)
주소창이 함께 보이게 찍습니다
```

캡처에 실명·학번·실제 이메일이 보이지 않게 합니다. 아이디는 보여도 됩니다.

---

## 다음 주 미리 보기

이번 주로 네 페이지가 내놓을 수 있는 상태가 되었습니다.

14주차에는 새 저장소 `web-week14` 를 오늘 완성본에서 시작하고, 그 공개 주소로 **3분 시연**을 합니다.
레포트는 오늘 쓴 `README.md` 최종판이고, 새로 만드는 기능은 없습니다.
15주차 기말은 1~14주 실습 제출로 만든 문제 은행에서 영역마다 한 문제씩, 값만 바꿔 내는 시험입니다.
