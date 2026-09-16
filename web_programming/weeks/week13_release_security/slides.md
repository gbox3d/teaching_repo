---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 13주차"
footer: "보안·접근성·릴리스 점검 · textContent, alt·label, README 최종판"
---

# 보안·접근성·릴리스 점검

12주차까지 네 페이지를 만들었습니다. 이번 주에는 **새 기능을 멈추고 점검**합니다.

```text
입력한 글을 어떻게 넣는가 ── textContent  (글자 그대로)
그림과 입력 칸에 글이 있는가 ── alt · label for
링크는 다 열리는가 ── 404 · Console · 375px
내놓을 문서 ── README 최종판 + screenshots 3장
```

---

# 1일차 — 페이지 점검하고 고치기

`30분 설명·시연 → 60분 실습`

1. 오늘 문법 5분 — `Number`·`isNaN`·`getFullYear`
2. 글자로 넣기와 HTML로 넣기
3. 공개 저장소에 넣지 않는 것
4. 접근성 두 가지 — `alt`와 `label for`
5. 점검 순서 — 링크 → Console → 375px

---

## 1일차 · 0–5분 — 오늘 문법 5분: Number와 isNaN

```js
const text = yearInput.value.trim();
const year = Number(text);
if (text === '' || isNaN(year)) { … }
const thisYear = new Date().getFullYear();
```

- `Number('2023')` → `2023`, `Number('이천이십삼')` → `NaN`(숫자가 아님)
- `isNaN(값)`: 그 값이 `NaN`이면 `true`입니다. 숫자가 아닌 입력을 여기서 거릅니다.
- `new Date().getFullYear()`: 오늘 날짜에서 **연도**만 꺼냅니다. 2026년이면 `2026`
- 7주차 폼과 순서가 같습니다: `preventDefault` → `trim` → 안내하고 `return` → 화면에 쓰기

---

## 1일차 · 5–11분 — 글자로 넣기와 HTML로 넣기

```js
output.textContent = input.value;   // <b>안녕</b> 이 글자 그대로
output.innerHTML = input.value;     // 굵은 안녕
```

- 같은 입력, 같은 자리인데 **단어 하나**만 다릅니다.
- `innerHTML`은 받은 글을 **HTML로 해석**합니다. 다른 사람이 적은 태그가 내 페이지에서 실행됩니다.
- 그래서 입력한 글을 보여 줄 때는 `textContent`를 씁니다.
- `innerHTML`은 10주차처럼 **목록을 비울 때(`innerHTML = ''`)만** 씁니다.
- 내 `guestbook.js`의 `li.textContent = …` 줄을 직접 확인합니다.

---

## 1일차 · 11–15분 — 공개 저장소에 넣지 않는 것

| 넣지 않는 것 | 대신 쓰는 예시 |
|---|---|
| 실명·학번·전화번호 | `student01` |
| 실제 이메일 | `student01@example.com` |
| 비밀번호·로그인 키 | 적지 않습니다 |

- 저장소는 **Public**입니다. commit에 한 번 들어간 값은 지워도 기록에 남습니다.
- 캡처에도 같은 규칙이 적용됩니다. 주소창의 아이디는 보여도 됩니다.
- 내 정보 표의 값은 처음부터 **수업용 가상 정보**로 적었습니다. 그대로 둡니다.

---

## 1일차 · 15–21분 — 접근성 두 가지: alt와 label for

```html
<img src="images/profile.png" alt="student01의 프로필 그림" width="160">

<label for="year">입학 연도</label>
<input id="year" type="text">
```

- `alt`: 그림이 안 보일 때 대신 읽히는 글입니다. 비워 두지 않습니다.
- `label for`의 값과 `input`의 `id`는 **글자가 같아야** 합니다.
- 확인 방법: 이름표 글자를 눌러 보세요. 입력 칸에 커서가 가면 연결된 것입니다.
- 하나 더 — **링크·버튼 글자**는 그것만 읽어도 어디로 가는지 알 수 있게 적습니다.

---

## 1일차 · 21–27분 — 점검 순서: 링크 → Console → 375px

1. 네 페이지의 nav 링크를 **다 눌러 본다** (404가 없어야 합니다)
2. 각 페이지에서 **F12 › Console**에 빨간 줄이 없는지 본다
3. **F12 › 기기 모드** 폭 **375**에서 가로로 밀리는 곳이 없는지 본다

```text
link.textContent = '페이지 열기';           ← 12주차: 카드 세 장이 모두 같은 글자
link.textContent = `${projects[i].title} 열기`;  ← 13주차: 어디로 가는지 보입니다
```

순서를 지킵니다. 링크가 깨진 채로 Console을 보면 원인이 섞입니다.

---

## 1일차 · 27–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--페이지-점검하고-입학-연도-계산하기-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security

1. `about.html`에 입학 연도 폼을 넣고 `about.js`로 몇 년차인지 계산합니다.
2. 방명록에 `<b>안녕</b>`을 남겨 글자 그대로 보이는지 확인합니다.
3. `alt`·`label for`·링크 글자를 고치고 링크·Console·375px를 점검합니다.

**설명 합계: 5+6+4+6+6+3 = 30분**

막히면 Console의 첫 빨간 줄과 그 끝의 `파일 (줄 번호)`부터 읽습니다.

---

# 2일차 — README 최종판과 발표 준비

`30분 설명·시연 → 60분 실습`

1. README 마크다운 네 가지
2. `screenshots/`에 그림 넣기
3. `git log --oneline`으로 만든 과정 붙이기
4. Pages 주소가 만들어지는 두 가지 방식
5. 14주차 발표 3분 흐름과 15주차 리허설 공개

---

## 2일차 · 0–8분 — README 마크다운 네 가지

```markdown
# 제목
- 목록 한 줄
[공개 주소](https://student01.github.io/my-web/)
```

- 그림은 링크 앞에 `!`를 붙입니다. 소괄호에는 `screenshots/home.png`처럼 파일 이름만 넣습니다.

**최종판에 두는 절**

| 절 | 내용 |
|---|---|
| 공개 주소 | `https://<아이디>.github.io/my-web/` |
| 페이지 | 네 페이지와 한 줄 설명 |
| 기능 | 다섯 줄 |
| 화면 | 그림 세 장 |
| 사용 기술 · 어려움과 해결 · 만든 과정 | 각각 세 줄 안팎 |

---

## 2일차 · 8–13분 — screenshots 폴더와 그림 넣기

```text
my-web/
  screenshots/
    home.png   guestbook.png   projects.png
```

- 그림 줄은 링크 앞에 `!`를 붙인 것입니다. `!`가 없으면 그림 대신 **링크**가 됩니다.
- 파일 이름은 소문자로 두고 한글·공백을 쓰지 않습니다.
- `home.png`와 `Home.png`는 **다른 파일**입니다. GitHub에서 그림이 깨지는 가장 흔한 이유입니다.
- 9주차에 찍은 두 장은 nav가 세 페이지였으니 **새로 찍어 덮어씁니다**. 여기에 `projects.png`가 더해져 세 장입니다.

---

## 2일차 · 13–18분 — git log --oneline으로 만든 과정 붙이기

```bash
git log --oneline
```

```text
8f31c4a 방명록 글자 확인하고 alt·label 고치기
5c0b7e2 프로젝트 카드 안내 문장 넣기
2a94d16 projects.json 불러와 카드 그리기
7e12b05 방명록을 localStorage에 저장하기
4d6a893 방명록 목록 추가·삭제 만들기
```

- 최근 다섯 줄을 README 마지막 절에 `- `를 붙여 옮겨 적습니다.
- 앞의 일곱 글자는 PC마다 다릅니다. **본인 화면의 값**을 씁니다.

---

## 2일차 · 18–22분 — Pages 주소가 만들어지는 두 가지 방식

**Settings › Pages › Build and deployment**

| Source | 공개되는 파일 | 우리 수업 |
|---|---|---|
| Deploy from a branch · `main` · `/(root)` | `main` 브랜치의 파일 | **수업 표준** (2주차부터) |
| Deploy from a branch · `gh-pages` | `gh-pages` 브랜치의 파일 | 2주차 부록에서 한 줄로 본 방식 |

- 두 방식 모두 공개 주소는 같습니다. 어느 브랜치를 내보낼지만 다릅니다.
- 오늘은 화면만 확인하고 **바꾸지 않습니다**. 바꾸면 주소가 한동안 404가 됩니다.

---

## 2일차 · 22–26분 — 14주차 발표 3분 흐름

```text
공개 주소 열기 → 페이지 이동(nav) → 다크 모드 → 폼 빈값 안내
→ 방명록 추가·삭제 → 새로고침해도 남는 목록 → JSON 카드 → Commits 탭
```

- 새로 만드는 것은 없습니다. 지금 있는 화면을 **순서대로 보여 주는 것**이 발표입니다.
- 레포트는 오늘 쓴 `README.md` 최종판입니다. 따로 내는 문서는 없습니다.
- 말로 설명하지 말고 **화면을 눌러** 보여 줍니다. 3분은 생각보다 짧습니다.

---

## 2일차 · 26–30분 — 15주차 리허설 공개 · 이제 직접 해 보기

[2일차 실습](lab.md#2일차--readme-최종판과-발표-준비-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security

1. `README.md` 최종판을 쓰고 `screenshots/` 세 장을 넣습니다.
2. push한 뒤 저장소 첫 화면에서 그림이 깨지지 않는지 봅니다.
3. 짝과 3분 리허설을 한 번 합니다.

15주차 기말 리허설 자료(`rehearsal_starter`)와 채점표는 오늘 공개합니다.

**설명 합계: 8+5+5+4+4+4 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

- 공개 주소 `https://<아이디>.github.io/my-web/guestbook.html`
- **F12 › 기기 모드 375px**
- 이름 `student02`, 메시지 `<b>안녕</b>`으로 남긴 한 줄이 **글자 그대로** 보인다
- **F12 › Console**에 빨간 줄이 없다
- 주소창이 함께 보이게 찍는다

캡처에 이메일·실명이 보이지 않게 합니다. 아이디는 보여도 됩니다.

---

## 다음 주 미리 보기

이제 `my-web`은 내놓을 수 있는 상태입니다.

14주차에는 이 공개 주소를 그대로 열어 **3분 시연**을 합니다.
레포트는 오늘 쓴 `README.md` 최종판이고, 새로 만드는 기능은 없습니다.
15주차 기말은 같은 구조의 새 폴더에서 혼자 처음부터 만드는 시험입니다.
