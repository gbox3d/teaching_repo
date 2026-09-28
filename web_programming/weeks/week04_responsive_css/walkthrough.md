# 4주차 따라하기 — 부품을 비교하고 마지막에 조립

이번 주 실습은 파일을 만드는 것이 아니라 **값을 바꿔 보는 것**이다.
이번 주부터 주마다 새 저장소를 만든다. 이번 주 저장소는 `web-week04`이고, 지난주 완성본에서 시작한다.
비교 파일을 `web-week04/ex/`에 저장하고, 값을 바꾼 뒤 화면이 어떻게 달라지는지 본다.
`web-week04`의 `styles.css`는 2일차 끝에 부품에서 **조립**한다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

비교 파일 12개는 [교재 저장소의 examples 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css/examples)에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다.

## 1일차

### 1. web-week04 폴더 만들고 지난주 파일 넣기

문서 폴더 등 원하는 위치에 새 폴더 `web-week04`를 만들고 VS Code **File › Open Folder**로 연다.
이어서 지난주 완성본을 넣는다. 방법은 둘 중 하나다.

1. **내 3주차 저장소에서** — GitHub에서 내 3주차 저장소(`my-web`) 화면을 열고 **Code › Download ZIP**을 누른다. 압축을 풀면 `my-web-main` 폴더가 생긴다. 그 **안의** 파일과 `images/` 폴더를 `web-week04`로 옮긴다.
2. **교재에서** — 1번을 못 했으면 [3주차 examples/day2/](../week03_semantic_html/examples/day2/)의 `index.html`·`about.html`·`guestbook.html`·`styles.css`·`app.js`를 **Raw**로 받는다. `images/profile.png`는 파일 화면의 내려받기 단추로 받아 `web-week04/images/`에 넣는다.

마지막으로 `web-week04` 안에 `ex` 폴더를 만든다. VS Code 탐색기에서 **New Folder**를 눌러도 되고, 명령으로 만들어도 된다. 현재 폴더: `web-week04`

```bash
mkdir ex
```

**예상 결과** — `web-week04` 안에 `index.html`·`about.html`·`guestbook.html`·`styles.css`·`app.js`·`images/`와 나란히 빈 `ex/` 폴더가 보인다.

- `my-web-main` 폴더째 넣지 않는다. 폴더가 한 겹 더 생기면 공개 주소가 달라진다. 파일만 옮긴다.
- 폴더 이름은 `ex`다. `Ex`·`examples`로 만들면 공개 주소가 달라져 4단계에서 404가 난다.
- 빈 폴더는 GitHub에 올라가지 않는다. 2단계에서 파일을 넣으면 함께 올라간다.

### 2. 비교 파일 다섯 개 가져오기

오늘 파일은 다섯 개다. 각 파일은 속성 하나만 비교한다.

| 파일 | 비교하는 것 |
|---|---|
| [ex01_selector.html](examples/ex01_selector.html) | 선택자 `p` / `.red` / `nav a` |
| [ex02_display.html](examples/ex02_display.html) | `display: block` / `inline` |
| [ex03_box_model.html](examples/ex03_box_model.html) | `padding` / `border` / `margin` |
| [ex04_width.html](examples/ex04_width.html) | `width` / `max-width` / `margin` 좌우 `auto` |
| [ex05_text_align.html](examples/ex05_text_align.html) | `text-align` / `vertical-align` |

가져오는 방법은 둘 중 하나다.

1. **Raw로 저장** — [교재 저장소 examples 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css/examples)에서 파일을 누르고 오른쪽 위 **Raw**를 누른다. 코드만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `web-week04/ex/`에 저장한다. 파일 이름은 교재와 **같게** 둔다.
2. **타이핑** — VS Code에서 `ex/ex01_selector.html`을 새로 만들고 교재 화면을 보며 친다. 1일차 파일은 31~45줄이다. 주석은 빼도 된다.

저장한 파일은 VS Code 탐색기에서 오른쪽 클릭 › **Reveal in File Explorer**(macOS는 **Reveal in Finder**)로 찾아 두 번 눌러 브라우저로 연다.

**예상 결과** — `ex01_selector.html`을 열면 여섯 줄이 보인다. 1번 파랑, 2·3번 빨강, 4번 파랑, 5번 초록, 6번 기본 링크색이다.
`ex/` 안에 파일 다섯 개가 있다.

- 저장한 파일 이름이 `ex01_selector.html.txt`처럼 `.txt`로 끝나면 이름을 고친다. 브라우저가 붙인 것이다.
- 다섯 파일을 한 번에 다 받고 시작해도 되고, 하나씩 받아 실험하고 다음으로 가도 된다.

### 3. 값 바꾸는 요령

실험은 두 가지 방법으로 한다. 먼저 DevTools에서 시험하고, 마음에 드는 값을 파일에 옮긴다.

**DevTools에서 먼저 시험** — F12 › **Elements**에서 상자를 고른다. 오른쪽 **Styles**에 그 상자에 적용된 규칙이 보인다. 값을 누르면 바로 고칠 수 있다.
`ex01_selector.html`에서 2번 문단을 고르고 `.red`의 `red`를 `orange`로 바꾼다.

**예상 결과** — 값을 바꾸는 순간 화면이 바뀐다. 2·3번이 주황이 된다. 새로고침하면 원래대로 돌아온다. DevTools에서 바꾼 것은 파일에 남지 않기 때문이다.

**파일에 옮기기** — VS Code에서 같은 값을 고치고 저장한다. 브라우저에서 **새로고침**(F5)한다.
`ex01_selector.html`에서 `/* p { color: gray; } */`의 주석 기호 `/*`·`*/`를 지우고 저장한다.

**예상 결과** — 새로고침하면 1·4번이 회색이 된다. 2번은 빨강 그대로다.
같은 선택자 `p`를 두 번 썼으니 뒤에 쓴 회색이 이기고, 2번은 클래스 `.red`가 태그 `p`를 이긴다.

- 저장(Ctrl+S) → 새로고침(F5). 이 두 동작을 한 쌍으로 익힌다. 저장을 안 하면 화면이 안 바뀐다.
- CSS는 틀려도 **오류 메시지가 없다.** 아무 일도 안 일어나면 DevTools Styles에서 내 규칙이 그 상자에 보이는지 본다. 안 보이면 선택자가 안 맞은 것이다.
- 값을 원래대로 못 돌리겠으면 교재에서 그 파일을 다시 받는다.
- 파일마다 무엇을 바꿔 볼지는 [1일차 실습](lab.md#1일차--선택자와-박스-60분)에 있다.

### 4. 이번 주 저장소 만들어 올리기

50분이 되면 올린다. 2주차에 배운 순서 그대로다.

먼저 GitHub에서 새 저장소를 만든다. 이름은 `web-week04`, **Public**으로 하고 README는 추가하지 않는다.
이어서 VS Code 터미널에서 친다. 현재 폴더: `web-week04`

```bash
git init
git add .
git commit -m "4주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week04.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save**를 누른다.

**예상 결과** — GitHub의 `web-week04` 저장소 화면을 새로고침하면 세 페이지·`styles.css`·`app.js`·`images/`·`ex/`가 보인다.
1~3분 뒤 `https://student01.github.io/web-week04/`을 열면 3주차의 꾸미지 않은 세 페이지가 보인다. `https://student01.github.io/web-week04/ex/ex01_selector.html`은 로컬에서 보던 것과 같은 화면이다. 두 화면은 **확인용**이다.
공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 404가 나면 주소의 `web-week04/`·`ex/`와 파일 이름이 폴더·파일 이름과 글자 단위로 같은지, Pages를 켰는지 본다.
- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- push가 거부되거나 로그인 창이 안 뜨면 [2주차 막혔을 때 표](../week02_github_pages/lab.md#막혔을-때)를 본다.

## 2일차

### 5. flex 파일 여섯 개 가져오기

같은 PC에 `web-week04` 폴더가 남아 있으면 **File › Open Folder**로 연다.
없으면 저장소를 내려받은 뒤 **File › Open Folder**로 연다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week04.git
```

오늘 파일은 여섯 개다. 2단계의 **Raw** → 저장으로 `web-week04/ex/`에 넣는다(파일이 47~68줄이라 타이핑은 시간 안에 못 끝낸다). 시작 5분 안에 여섯 개를 다 받아 둔다.

| 파일 | 비교하는 것 |
|---|---|
| [ex06_flex_direction.html](examples/ex06_flex_direction.html) | `flex-direction` `row` / `row-reverse` / `column` / `column-reverse`, 같은 `justify-content: center`를 row와 column에서 |
| [ex07_justify_content.html](examples/ex07_justify_content.html) | `justify-content` 다섯 값 |
| [ex08_align_items.html](examples/ex08_align_items.html) | `align-items` 네 값 |
| [ex09_flex_wrap_gap.html](examples/ex09_flex_wrap_gap.html) | `flex-wrap` / `gap` |
| [ex10_flex_grow.html](examples/ex10_flex_grow.html) | `flex: 1` |
| [ex11_media.html](examples/ex11_media.html) | `@media (max-width: 600px)` |

[ex12_position.html](examples/ex12_position.html)은 부록이다. 시간이 남으면 열어 본다.

**예상 결과** — `ex/`에 파일이 열한 개(부록까지 열두 개) 있다. `ex06_flex_direction.html`을 열면 검은 바탕에 흰 테두리 상자 일곱 개가 보인다. 1번은 세로로 쌓여 있고 2번부터 flex로 배치된다(2·3·6번은 가로, 4·5·7번은 세로).

- flex 파일은 같은 틀을 쓴다. 부모 `.frame`에 `display: flex`, 자식은 `.box`. frame에 붙인 클래스 하나로 형제를 만든다.
- 파일마다 무엇을 바꿔 볼지는 [2일차 실습](lab.md#2일차--flex와-조립-60분)에 있다.

### 6. 조립표

이제 `web-week04`의 `styles.css`를 부품에서 조립한다. 규칙마다 **어느 ex에서 본 것**인지 적어 두었다.
규칙을 옮겨 적을 때 출처 ex 파일을 옆에 열어 두고, 같은 속성이 거기서 어떻게 움직였는지 떠올린다.

| `styles.css` 규칙 | 어느 ex에서 본 것 |
|---|---|
| `body { background-color; color; font-family; font-size }` | [ex01](examples/ex01_selector.html) 태그 선택자. 색·글꼴 네 속성은 3주차 HTML에 없던 새 속성이다 |
| `body { max-width: 640px; margin: 0 auto; padding: 16px }` | [ex04](examples/ex04_width.html) `max-width`·`margin` 좌우 `auto`, [ex03](examples/ex03_box_model.html) `padding` |
| `h1`·`h2` `{ color … }` | [ex01](examples/ex01_selector.html) 태그 선택자 |
| `nav { display: flex; gap: 16px; flex-wrap: wrap }` | [ex06](examples/ex06_flex_direction.html) flex는 부모에, [ex09](examples/ex09_flex_wrap_gap.html) `gap`·`wrap`도 부모에 |
| `nav a { color }` | [ex01](examples/ex01_selector.html) 자손 선택자 |
| `.card { background-color; padding; margin: 12px 0; border }` | [ex01](examples/ex01_selector.html) 클래스 선택자, [ex03](examples/ex03_box_model.html) 세 층 |
| `input, textarea { width: 280px; max-width: 100% }` | [ex04](examples/ex04_width.html) 3번 `max-width` 로 좁은 화면 대비. `width: 280px` 은 평소 폭, `max-width: 100%` 는 부모보다 못 커지게 하는 상한. 쉼표 = 두 대상에 같은 규칙 |
| `footer { text-align: center; … }` | [ex05](examples/ex05_text_align.html) |
| `@media (max-width: 600px) { nav { flex-direction: column } }` | [ex11](examples/ex11_media.html) 조건 + [ex06](examples/ex06_flex_direction.html) `column` |

**예상 결과** — 표의 아홉 줄이 9단계 `styles.css`의 규칙 순서와 같다. 표에 없는 속성은 `styles.css`에도 없다.

- `nav`의 `display: flex`·`gap`·`flex-wrap`은 셋 다 **부모** `nav`에 쓴다. `nav a`에 쓰면 아무 일도 없다(ex06·ex09).
- `@media` 안의 `nav { flex-direction: column }`은 위의 `nav` 규칙과 같은 선택자다. 조건이 맞을 때만 뒤 규칙이 살아나 앞을 덮는다(ex11, ex01).

### 7. 세 페이지 head에 link 줄 넣기

`index.html`·`about.html`·`guestbook.html`의 `<title>` 바로 아래에 같은 한 줄을 넣는다. 3주차에 뺐던 줄을 되살리는 것이다.

```html
    <link rel="stylesheet" href="styles.css">
```

**예상 결과** — 저장하고 새로고침하면 `styles.css`에 남아 있던 2주차 규칙이 살아나 배경이 연한 파랑이 되고 header·main·footer가 화면 가운데로 모인다(2주차 `body { display: grid }`). 9단계에서 이 파일을 새로 쓰면 본문이 640px 안에 왼쪽 정렬로 돌아온다.
연결이 됐는지는 F12 › **Elements**의 `<head>` 안에 `link` 줄이 보이는 것으로 확인한다.

- 규칙을 아무리 잘 써도 **연결하지 않으면 아무 일도 일어나지 않는다.**
- `href`의 파일 이름을 `style.css`(s 빠짐)로 적으면 파일을 찾지 못한다. 오류 메시지는 없다.
- 세 페이지 모두 넣는다. 한 페이지만 안 꾸며지면 그 페이지의 `link` 줄을 본다.

### 8. index.html에 class="card" 세 곳

`index.html`에서 소개 문단 두 개와 취미 목록에 `class="card"`를 붙인다.

```html
      <p class="card">웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p class="card">이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
```

```html
      <ul class="card">
```

**예상 결과** — 2주차 `.card` 규칙이 아직 남아 있어 세 곳이 곧바로 둥근 흰 카드(그림자 있음)가 된다. 9단계에서 새 규칙으로 바꾸면 모서리가 각지고 그림자가 없어진다. 새 `.card`는 ex03에서 본 `padding`·`margin`·`border` 세 층뿐이다.

- `.card`의 점은 CSS에서만 쓴다. HTML에는 `class="card"`라고 점 없이 적는다(ex01).
- `about.html`·`guestbook.html`에는 붙이지 않는다. 카드는 `index.html`에만 둔다.

### 9. styles.css 전문

`styles.css`를 연다. 2주차에 쓴 내용이 들어 있다. **전체를 지우고** 6단계 조립표 순서로 아래 규칙을 쓴다.
같은 파일이 [examples/build/styles.css](examples/build/styles.css)에 있다.

```css
body {
  background-color: #eef2ff;
  color: #17213a;
  font-family: system-ui, sans-serif;
  font-size: 16px;
  max-width: 640px;
  margin: 0 auto;
  padding: 16px;
}

h1 {
  color: #1f3a93;
  font-size: 28px;
}

h2 {
  color: #3157d5;
}

nav {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

nav a {
  color: #3157d5;
}

.card {
  background-color: #ffffff;
  padding: 16px;
  margin: 12px 0;
  border: 1px solid #c3cbe6;
}

input,
textarea {
  width: 280px;
  max-width: 100%;
}

footer {
  color: #5a6478;
  text-align: center;
  font-size: 14px;
}

@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}
```

**예상 결과** — 저장하고 `index.html`을 새로고침하면 다음이 한 번에 보인다.

1. 배경이 연한 파랑, 본문이 화면 가운데 640px 안에 모인다(`body`).
2. 제목이 남색·파랑으로 바뀐다(`h1`·`h2`).
3. 메뉴 세 개가 한 줄에 16px 간격으로 선다(`nav`).
4. 문단 두 개와 취미 목록이 테두리 있는 흰 상자가 된다(`.card`).
5. 맨 아래 한 줄이 회색·가운데로 간다(`footer`).

- `margin: 0 auto`는 위아래 0, 좌우 `auto`다. `auto`가 남는 폭을 반씩 나눠 가운데로 간다(ex04). `width: 640px`로 쓰면 좁은 화면에서 삐져나간다.
- `margin: 12px 0`은 위아래 12px, 좌우 0이다. `border: 1px solid #c3cbe6`은 두께·모양·색을 한 줄에 적은 것이다(ex03).
- `input, textarea`의 `width: 280px`은 평소 폭, `max-width: 100%`는 부모보다 커지지 않는 상한이다. ex04의 2번(`width`)과 3번(`max-width`)을 한 상자에 합친 것이라 375에서도 삐져나가지 않는다.
- `input, textarea`의 쉼표를 빠뜨리면 `input textarea`(input 안의 textarea)가 되어 아무것도 고르지 못한다.
- 색은 `#`과 여섯 자리다. 다른 색을 써도 되지만, 글자색과 배경색이 너무 비슷하면 읽기 어렵다.
- 상자가 안 보이면 8단계의 `class="card"`가 들어갔는지 본다. 화면 전체가 안 바뀌면 7단계의 `link` 줄을 본다.

### 10. index.html·about.html·guestbook.html 전문

7·8단계를 마친 세 페이지 전체다. 내 파일과 한 줄씩 비교한다. 3주차 파일에서 늘어난 것은 `link` 한 줄과 `index.html`의 `class="card"` 세 곳뿐이다.

`index.html` — 같은 파일이 [examples/build/index.html](examples/build/index.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <header>
      <h1>student01의 웹 연습장</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <h2>소개</h2>
      <img src="images/profile.png" alt="student01의 프로필 그림" width="160">
      <p class="card">웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p class="card">이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
      <h2>취미</h2>
      <ul class="card">
        <li>사진 찍기</li>
        <li>보드게임</li>
        <li>저녁 산책</li>
      </ul>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`about.html` — 같은 파일이 [examples/build/about.html](examples/build/about.html)에 있다. `link` 한 줄만 늘었다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <header>
      <h1>내 정보</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <h2>한눈에 보기</h2>
      <p>수업용 가상 정보입니다.</p>
      <table>
        <tr>
          <th>항목</th>
          <th>내용</th>
        </tr>
        <tr>
          <td>아이디</td>
          <td>student01</td>
        </tr>
        <tr>
          <td>이메일</td>
          <td>student01@example.com</td>
        </tr>
        <tr>
          <td>관심 분야</td>
          <td>웹 페이지 만들기</td>
        </tr>
      </table>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`guestbook.html` — 같은 파일이 [examples/build/guestbook.html](examples/build/guestbook.html)에 있다. `link` 한 줄만 늘었다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <header>
      <h1>방명록</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <h2>한 줄 남기기</h2>
      <h3>쓰는 순서</h3>
      <ol>
        <li>이름을 적는다.</li>
        <li>메시지를 적는다.</li>
        <li>남기기 버튼을 누른다.</li>
      </ol>
      <form>
        <p>
          <label for="name">이름</label>
          <input id="name" type="text">
        </p>
        <p>
          <label for="email">이메일</label>
          <input id="email" type="email">
        </p>
        <p>
          <label for="message">메시지</label>
          <textarea id="message" rows="4"></textarea>
        </p>
        <button type="submit">남기기</button>
      </form>
      <p>지금은 눌러도 주소창만 바뀐다. 화면에 띄우는 일은 7주에 한다.</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

**예상 결과** — 세 페이지의 배경색·제목 색·메뉴 모양이 같다. 메뉴로 오가며 확인한다.
`guestbook.html`의 이름·이메일 칸과 메시지 칸은 폭이 280px로 같다(`input, textarea`). `about.html`의 표는 아직 꾸미지 않아 3주차와 같은 모양이다.

- `images/profile.png`는 3주차 파일 그대로다. 이번 주에 손대지 않는다.

### 11. app.js는 열지 않는다

`app.js`는 이번 주에 **한 글자도 고치지 않는다.** 폴더에 그대로 있는지만 확인한다. 내용은 2주차와 같다.
같은 파일이 [examples/build/app.js](examples/build/app.js)에 있다.

```js
const countButton = document.querySelector('#count-button');
const status = document.querySelector('#status');

let clickCount = 0;

countButton.addEventListener('click', () => {
  clickCount += 1;
  status.textContent = `클릭 횟수: ${clickCount}`;
});

console.info('my-web ready');
```

**예상 결과** — 세 페이지 어디에도 `<script>` 줄이 없으므로 이 파일은 실행되지 않는다. 그래서 오류도 나지 않는다.

- 5주차에 이 파일을 비우고 다시 쓴다. 그때 `<script src="app.js" defer>` 줄을 되살린다.
- 지우지 않는다. 지운 학생은 [examples/build/app.js](examples/build/app.js)를 **Raw**로 다시 받는다.

### 12. 1280·기기 모드 375 확인 → push → 캡처

먼저 로컬에서 두 폭을 본다. `index.html`을 연 Chrome에서 순서대로 한다.

1. F12로 DevTools를 연다.
2. **Ctrl+Shift+M**(macOS는 **⌘+⇧+M**)으로 기기 모드를 켠다.
3. 위쪽 폭 칸에 `1280`을 치고 Enter, 다시 `375`를 치고 Enter를 누른다.

**예상 결과** — 1280에서는 메뉴 세 개가 한 줄이고 본문이 가운데 640px 안에 있다.
375에서는 메뉴가 `홈`·`내 정보`·`방명록` **세 줄로 세로로 선다.** 카드 테두리는 두 폭 모두 화면 안에 들어오고 가로 스크롤 막대는 생기지 않는다.

- 375는 600보다 작으므로 `@media (max-width: 600px)` 안의 규칙이 산다. 1280에서는 죽어 있다(ex11).
- 375에서도 메뉴가 가로 그대로면 `@media (max-width 600px)`처럼 콜론이 빠졌는지, 중괄호 `}`가 두 개 다 있는지 본다. 틀려도 오류 없이 덩어리 전체가 무시된다.

두 폭이 맞으면 올린다. 2주차에 배운 순서 그대로다. 현재 폴더: `web-week04`

```bash
git add .
git commit -m "4주차 2일차"
git push
```

**예상 결과** — GitHub의 `web-week04` 저장소 화면에서 `ex/`에 비교 파일이 열한 개(부록까지 열두 개) 보이고, `styles.css`를 누르면 9단계의 내용이 보인다.

1. 1분쯤 뒤 `https://student01.github.io/web-week04/`을 새로고침한다.
2. F12 → 기기 모드(**Ctrl+Shift+M**) → 폭 `375`.
3. 메뉴가 세로로 서고 카드에 테두리가 보이면 **주소창과 폭 375 표시가 함께 보이게** 화면을 캡처한다. 이 한 장이 이번 주 제출물이다.
4. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 아이디는 보여도 된다.
- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 실험하다 비교 파일을 망쳤으면 교재에서 다시 받는다. 증상별 확인 순서는 [실습지](lab.md#막혔을-때)의 막혔을 때 표에 있다.
- 선택: Node.js가 있으면 정적 서버 [`server.mjs`](../../tools/static-server/README.md)로 `web-week04`를 `http://localhost:8000/`에서 열어 볼 수 있다. 설명은 5주차에 한다.
