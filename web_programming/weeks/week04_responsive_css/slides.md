---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 4주차"
footer: "CSS와 반응형 UI · 선택자·색·박스·flex·@media"
---

# CSS와 반응형 UI

3주차에는 세 페이지를 만들었지만 화면은 꾸미지 않았습니다.
이번 주에는 `styles.css`를 **비우고 다시 써서** 세 페이지에 연결합니다.

```text
my-web/
  index.html      ← link 한 줄 + class="card" 세 곳
  about.html      ← link 한 줄
  guestbook.html  ← link 한 줄
  styles.css      ← 비우고 다시 쓴다 (이번 주의 주인공)
```

`app.js`는 이번 주에도 열지 않습니다. 동작은 5주차입니다.

---

# 1일차 — 색과 글꼴

`30분 설명·시연 → 60분 실습`

1. `git log --oneline`과 GitHub Commits 탭
2. `link` 줄 되살리기와 규칙의 모양
3. 선택자: 태그와 `.class`
4. 색·글꼴 네 가지와 DevTools Styles

---

## 1일차 · 0–5분 — 오늘 Git 5분: git log --oneline과 Commits 탭

```bash
git pull
git log --oneline
```

```text
9bd9ddb 방명록 페이지 추가
32b2716 자기소개 페이지 만들기
```

- 시작 0–5분은 `git pull`(같은 PC) 또는 `git clone`(다른 PC)입니다. 3주차와 같습니다.
- `git log --oneline`은 **내 PC의 기록**입니다. 앞의 일곱 글자는 PC마다 다릅니다.
- GitHub 저장소 화면의 **Commits** 탭에서 commit 하나를 누르면 그때 **바뀐 줄**이 초록·빨강으로 보입니다.
- 오늘 고칠 파일은 `styles.css` 하나입니다. 끝 루틴(add → commit → push)은 3주차와 같습니다.

---

## 1일차 · 5–11분 — link 줄 되살리기와 규칙의 모양

```html
    <link rel="stylesheet" href="styles.css">
```

```css
선택자 {
  속성: 값;
}
```

- 3주차에 뺐던 `link` 한 줄을 **세 페이지 모두** `<title>` 아래에 다시 넣습니다.
- 2주차 `styles.css`는 읽기만 한 **틀**입니다. 오늘 전체를 지우고 처음부터 씁니다.
- 규칙 하나 = 선택자 + 중괄호 + `속성: 값;` 줄들.
- 줄 끝 세미콜론을 빠뜨리면 그 줄과 **다음 줄까지** 함께 무시됩니다.

---

## 1일차 · 11–17분 — 선택자: 태그와 .class

```css
h1 { color: #1f3a93; }
nav a { color: #3157d5; }
.card { background-color: #ffffff; }
```

```html
<p class="card">웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
```

- 태그 선택자(`h1`)는 그 태그 **전부**를 고릅니다.
- `nav a`처럼 사이를 띄우면 "`nav` 안에 있는 `a`"라는 뜻입니다.
- `.card`는 HTML에 `class="card"`라고 적어 둔 것만 고릅니다. 점은 CSS에서만 씁니다.
- 선택자가 **한 글자라도 다르면** 아무 일도 일어나지 않습니다. `.Card`는 `.card`가 아닙니다.

---

## 1일차 · 17–25분 — 색과 글꼴 네 가지, 그리고 Styles 탭

```css
body {
  background-color: #eef2ff;
  color: #17213a;
  font-family: system-ui, sans-serif;
  font-size: 16px;
}
```

- `background-color` 배경색 · `color` 글자색 · `font-size` 글자 크기 · `font-family` 글꼴
- `body`에 준 글자색과 글꼴은 안쪽 글자에도 그대로 내려갑니다.
- DevTools **Elements › Styles**에서 값을 바꾸면 화면이 바로 바뀝니다.
- 다만 **새로고침하면 사라집니다.** 파일에 저장된 것이 아닙니다.
- `text-align: center`는 오늘 `footer` 한 곳에 씁니다.

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--색과-글꼴-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

1. 세 페이지에 `link` 줄을 넣고 `styles.css`를 전체 지웁니다.
2. `body`·`h1`·`h2`·`nav a` 네 규칙을 씁니다.
3. `index.html`의 문단 두 개와 취미 목록에 `class="card"`를 붙이고 `.card`·`footer` 규칙을 씁니다.

**설명 합계: 5+6+6+8+5 = 30분**

화면이 안 바뀌면 **선택자 철자**와 `link` 줄부터 봅니다.

---

# 2일차 — 박스와 반응형

`30분 설명·시연 → 60분 실습`

1. `git restore`로 되돌리기
2. 박스모델 `padding`·`margin`·`border`
3. `max-width`·`margin: 0 auto`
4. `display: flex`·`gap`·`flex-wrap`
5. `@media (max-width: 600px)`와 기기 모드 375

---

## 2일차 · 0–5분 — 오늘 Git 5분: git restore

```bash
git status
git restore styles.css
```

```text
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   styles.css
```

- 1주차에 **보기만** 했던 명령을 오늘 실제로 써 봅니다. `git status`가 방법을 같이 알려 줍니다.
- `git restore <파일>`: 저장은 했지만 commit하지 않은 수정을 마지막 commit 상태로 되돌립니다.
- `git add`까지 했다면 `git restore --staged <파일>`로 add만 취소합니다(파일 내용은 그대로).
- 되돌린 내용은 돌아오지 않습니다. 성공하면 **아무 말도 나오지 않습니다**.

---

## 2일차 · 5–12분 — 박스모델 padding·margin·border

```text
margin  ← 상자 바깥 여백
border  ← 상자 테두리
padding ← 테두리와 글자 사이
글자
```

```css
.card {
  padding: 16px;
  margin: 12px 0;
  border: 1px solid #c3cbe6;
}
```

- `margin: 12px 0`은 위아래 12px, 좌우 0이라는 뜻입니다.
- DevTools **Elements › Styles** 맨 아래 상자 그림에서 네 값을 그대로 볼 수 있습니다.

---

## 2일차 · 12–17분 — max-width와 margin: 0 auto

```css
body {
  max-width: 640px;
  margin: 0 auto;
  padding: 16px;
}
```

- `max-width: 640px`: 화면이 아무리 넓어도 본문은 640px까지만 넓어집니다. 글줄이 길면 읽기 어렵습니다.
- `margin: 0 auto`: 위아래 0, 좌우는 남는 공간을 **반씩** 나눠 가집니다. 그래서 가운데로 모입니다.
- `width: 640px`이 아니라 `max-width`인 이유는, 화면이 640px보다 좁으면 그 화면에 맞춰 줄어들어야 하기 때문입니다.
- `padding: 16px`은 화면 가장자리에 글자가 붙지 않게 합니다.

---

## 2일차 · 17–23분 — display: flex·gap·flex-wrap

```css
nav {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
```

```text
전: 홈 내 정보 방명록      ← 링크끼리 거의 붙어 있다
후: 홈   내 정보   방명록  ← 한 줄로 나란히, 사이 16px
```

- `display: flex`는 안에 있는 것들을 **한 줄로 나란히** 놓습니다.
- `gap`은 그 사이 간격, `flex-wrap: wrap`은 한 줄에 다 안 들어가면 다음 줄로 넘기라는 뜻입니다.
- flex로 바꾸는 진짜 이유는 다음 장입니다. 세로로 세울 수 있게 됩니다.

---

## 2일차 · 23–27분 — @media 세 줄과 기기 모드 375

```css
@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}
```

- 뜻: **화면 폭이 600px 이하일 때만** 안쪽 규칙을 쓴다.
- `flex-direction: column`은 가로로 놓던 것을 세로로 바꿉니다.
- 파일 **맨 끝**에 붙입니다. 이 세 줄은 그대로 복사해 씁니다.
- 확인은 DevTools **기기 모드**(Ctrl+Shift+M, macOS ⌘+⇧+M) → 폭에 `375`를 칩니다.
- 괄호 안 콜론(`max-width:`)을 빠뜨리면 오류 없이 **블록 전체가 무시**됩니다.

---

## 2일차 · 27–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--박스와-반응형-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

1. `nav`를 flex로, `.card`에 `padding`·`margin`·`border`를 줍니다.
2. `body`에 `max-width`·`margin: 0 auto`, 파일 끝에 `@media` 세 줄, 그 앞에 입력 칸 폭.
3. 375px에서 메뉴가 세로로 서면 캡처합니다. 마지막에 `git restore`를 한 번 써 봅니다.

**설명 합계: 5+7+5+6+4+3 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/my-web/
DevTools 기기 모드 375px
메뉴: 홈 / 내 정보 / 방명록   ← 세로로 한 줄씩
소개 문단·취미 목록: 테두리 있는 흰 카드
주소창과 폭 375 표시가 함께 보이게 찍습니다
```

1280px 화면은 확인용입니다. 캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

오늘까지 세 페이지는 **보이는 것**만 바뀌었습니다. 버튼도 입력 칸도 아직 아무 동작을 하지 않습니다.

5주차에는 `app.js`를 비우고 다시 써서 JavaScript를 시작합니다.
`<script src="app.js" defer></script>` 줄을 되살리고, Console에 값을 찍어 보고,
함수가 만든 인사말을 `index.html`에 한 줄 띄웁니다.

오늘 정한 색 값과 `.card`는 6주차 다크 모드에서 다시 씁니다.
