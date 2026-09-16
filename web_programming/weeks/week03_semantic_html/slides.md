---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 3주차"
footer: "시맨틱 HTML과 form · 세 페이지 자기소개 사이트"
---

# 시맨틱 HTML과 form

2주차에는 카드 한 장짜리 `index.html`을 공개했습니다.
이번 주에는 같은 `my-web`을 **세 페이지**로 늘리고, 이름과 메시지를 적는 입력 칸을 만듭니다.

```text
my-web/
  index.html      ← 자기소개 (다시 씀)
  about.html      ← 내 정보 표 (다시 씀)
  guestbook.html  ← 방명록 form (새 파일)
  images/profile.png
```

`styles.css`·`app.js`는 파일로 남기고 **연결하지 않습니다**. 이번 주는 HTML만 합니다.

---

# 1일차 — 뼈대와 자기소개 페이지

`30분 설명·시연 → 60분 실습`

1. 시작 루틴(`git pull`·`git clone`)과 끝 루틴
2. `header`·`nav`·`main`·`footer`
3. 제목·문단·강조
4. 링크와 그림, 목록

---

## 1일차 · 0–5분 — 오늘 Git 5분: 시작 루틴과 끝 루틴

```bash
git pull                                           # 같은 PC에서 이어 할 때
git clone https://github.com/student01/my-web.git  # 다른 PC에서 시작할 때
```

- 이번 주부터 실습 **0–5분은 항상 이 두 줄 중 하나**입니다. 2주차 부록 슬라이드의 복습입니다.

```bash
git add .
git commit -m "자기소개 페이지 만들기"
git push
```

- 실습 **55–60분은 항상 이것**입니다. push → 공개 주소 새로고침 → 캡처.
- 공용 PC는 나가기 전 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지웁니다.

---

## 1일차 · 5–10분 — 페이지의 뼈대 header·nav·main·footer

```html
<body>
  <header> … 제목과 메뉴 … </header>
  <main>   … 이 페이지의 본문 … </main>
  <footer> … 마무리 한 줄 … </footer>
</body>
```

- 2주차의 `<main class="card">` 한 덩어리를 **네 자리로 나눕니다**.
- `nav`는 링크 묶음이라는 뜻이며 `header` 안에 둡니다.
- `main`은 한 페이지에 하나입니다.
- 이름만 나눴을 뿐 화면은 아직 위에서 아래로 쌓입니다. 꾸미기는 4주차입니다.

---

## 1일차 · 10–16분 — 제목 h1~h3와 문단 p·strong

```html
<h1>student01의 웹 연습장</h1>
<h2>소개</h2>
<p>웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
```

- `h1`은 페이지에 **하나**. 그 아래 큰 묶음이 `h2`, 그 안이 `h3`입니다.
- 글자를 크게 하려고 `h1`을 고르지 않습니다. 크기는 4주차 CSS로 정합니다.
- `p`는 문단 하나, `strong`은 문단 안에서 중요한 말입니다.

---

## 1일차 · 16–22분 — 링크 a href와 그림 img alt

```html
<a href="about.html">내 정보</a>
<img src="images/profile.png" alt="student01의 프로필 그림" width="160">
```

- 같은 폴더의 파일은 **파일 이름만** 적습니다(상대 경로). 2주차 소개 링크와 같습니다.
- 그림은 `images/` 폴더를 만들어 그 안에 두고 `images/profile.png`로 부릅니다.
- `alt`는 그림이 안 보일 때 대신 읽히는 글입니다. "사진"·"이미지"라고만 쓰지 않습니다.
- 경로가 틀리면 그림 자리에 `alt` 글자만 보입니다. 그것이 확인 방법입니다.

---

## 1일차 · 22–27분 — 목록 ul·ol·li

```html
<ul>
  <li>사진 찍기</li>
  <li>보드게임</li>
</ul>
```

- `ul`: 순서가 없는 목록(점). `ol`: 순서가 있는 목록(1, 2, 3).
- 줄 하나가 `li` 하나입니다. `li`는 `ul`이나 `ol` **안에만** 둡니다.
- 2일차 `guestbook.html`의 "쓰는 순서"는 `ol`로 만듭니다.

---

## 1일차 · 27–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--세-페이지의-뼈대와-자기소개-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week03_semantic_html

1. `index.html`의 2주차 내용과 `link`·`script` 두 줄을 지우고 뼈대 네 개를 만듭니다.
2. `h1`·소개 문단·`strong`, 프로필 그림, 메뉴 링크 두 개.
3. 취미 `ul` 세 줄과 `footer`, 그리고 끝 루틴.

**설명 합계: 5+5+6+6+5+3 = 30분**

`styles.css`·`app.js`는 오늘 **열지 않습니다**. 파일은 두고 연결 줄만 뺍니다.

---

# 2일차 — 내 정보 표와 방명록 form

`30분 설명·시연 → 60분 실습`

1. `table`로 2열 표 만들기
2. `form`·`label`·`input`·`textarea`
3. `button type="submit"`이 지금 하는 일
4. `guestbook` 브랜치 → merge

---

## 2일차 · 0–6분 — 표 table·tr·th·td

```html
<table>
  <tr><th>항목</th><th>내용</th></tr>
  <tr><td>아이디</td><td>student01</td></tr>
</table>
```

- `table` 안에 줄(`tr`)을 쌓고, 줄 안에 칸을 넣습니다.
- `th`는 제목 칸(굵게·가운데), `td`는 내용 칸입니다.
- 선이 없는 것이 정상입니다. 선·여백은 4주차 CSS로 그립니다.
- 표에 실제 이메일·학번·전화번호를 넣지 않습니다. 수업용 가상 정보를 씁니다.

---

## 2일차 · 6–14분 — form과 label for·input·textarea

```html
<form>
  <label for="name">이름</label>
  <input id="name" type="text">
  <label for="message">메시지</label>
  <textarea id="message" rows="4"></textarea>
</form>
```

- `form`은 입력 칸을 묶는 영역입니다.
- `label`의 `for`와 `input`의 `id`가 **같아야** 이름표를 눌렀을 때 커서가 들어갑니다.
- `type="text"`는 한 줄, `type="email"`은 이메일용, `textarea`는 여러 줄입니다.
- 커서가 안 들어가면 `for`와 `id`의 철자를 대소문자까지 비교합니다.

---

## 2일차 · 14–19분 — button type submit과 아직 일어나지 않는 일

```html
<button type="submit">남기기</button>
```

```text
누르기 전: …/guestbook.html
누른 뒤  : …/guestbook.html?      ← 주소창만 바뀐다
```

- 지금은 눌러도 **화면에 아무 일도 일어나지 않습니다**. 주소창 끝에 `?`만 붙습니다.
- 적은 글을 화면에 띄우는 일은 **7주차**에 JavaScript로 합니다.
- 오늘은 "입력 칸을 올바로 만든다"까지가 목표입니다.

---

## 2일차 · 19–25분 — 오늘 Git 5분: guestbook 브랜치와 404

```bash
git switch -c guestbook     # 만들면서 바로 옮겨 간다
```

```bash
git switch main
git merge guestbook
git push
```

- `-c`는 2주차의 `git branch` + `git switch`를 한 줄로 한 것입니다.
- 2주차 마지막 장의 "다음 주에는 새 이름으로 브랜치를 또 만듭니다"가 오늘입니다.
- 링크가 404면 **파일 이름의 철자와 대소문자**를 봅니다. 내 PC에서는 `Guestbook.html`도 열리지만 공개 주소에서는 404입니다.

---

## 2일차 · 25–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--내-정보-표와-방명록-form-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week03_semantic_html

1. `git pull` → `git switch -c guestbook`.
2. `about.html`을 2열 4행 표로 다시 쓰고, `guestbook.html`을 새로 만듭니다.
3. 세 페이지 메뉴를 같게 맞추고 `merge` → `push` → 공개 주소에서 캡처.

**설명 합계: 6+8+5+6+5 = 30분**

막히면 화면의 그림·링크 경로부터 봅니다.

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/my-web/guestbook.html
메뉴: 홈 · 내 정보 · 방명록
입력 칸: 이름 · 이메일 · 메시지 + [남기기]
주소창이 함께 보이게 찍습니다
```

캡처에 실명·학번·실제 이메일이 보이지 않게 합니다. 아이디는 보여도 됩니다.

---

## 다음 주 미리 보기

오늘 만든 세 페이지는 꾸미지 않은 화면입니다.

4주차에는 `styles.css`를 비우고 다시 써서 세 페이지에 연결하고,
색·박스·`display: flex`·`@media`로 꾸밉니다.
오늘 만든 `header`·`nav`·`main`·`footer`·`ul`·`table`이 그대로 CSS의 대상이 됩니다.
