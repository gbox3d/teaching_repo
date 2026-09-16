# 4주차 실습 — 세 페이지를 CSS로 꾸미기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

3주차에 만든 세 페이지에 `styles.css`를 연결하고 색·박스·`@media`로 꾸민다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.
이번 주에 고치는 파일은 `styles.css` 하나와 세 페이지의 `link` 한 줄씩, `index.html`의 `class="card"` 세 곳이다. `app.js`는 열지 않는다.

## 1일차 — 색과 글꼴 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` 뒤 **File › Open Folder** |
| 5–15분 | `styles.css`를 전체 지우고 `body` 규칙을 쓴 뒤, `index.html`에 `link` 한 줄을 넣어 색이 들어오는지 본다 |
| 15–28분 | `h1`·`h2` 색과 크기, `nav a` 색 |
| 28–45분 | `index.html`의 문단 두 개와 취미 목록에 `class="card"`를 붙이고 `.card` 규칙을 쓴다 |
| 45–55분 | `about.html`·`guestbook.html`에도 `link` 줄, `footer` 규칙, DevTools **Styles**에서 값을 바꿔 본다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 새로고침 → 공용 PC면 자격 증명 삭제 |

### 1. styles.css 비우고 body 규칙 (`background-color` · `color` · `font-family` · `font-size`)

`styles.css`의 2주차 내용을 **전체 지우고** `body` 규칙 하나만 쓴다. 그 다음 `index.html`에 `link` 줄을 넣는다.
[따라하기 2~3단계](walkthrough.md#2-stylescss-비우고-body-규칙-쓰기)를 본다.

- `link` 줄을 넣기 전에는 규칙을 아무리 써도 화면이 그대로다. **그것이 정상이다.** 연결한 뒤에 확인한다.
- 색은 `#`과 여섯 자리로 적는다. 글자색과 배경색을 너무 비슷하게 고르지 않는다.
- 배경이 안 바뀌면 `href="styles.css"`의 철자부터 본다. `style.css`는 다른 이름이다.

### 2. 제목과 메뉴 색 (`h1` · `h2` · `nav a`)

`styles.css`에 규칙 세 개를 더한다. [따라하기 4단계](walkthrough.md#4-제목과-메뉴-색-정하기)를 본다.

- `h1`에는 `color`와 `font-size` 두 줄을 쓴다. 3주차에 "크기는 CSS로 정한다"고 한 것이 이것이다.
- `nav a`는 두 낱말 사이를 띄운다. "`nav` 안에 있는 `a`"라는 뜻이다.
- 한 규칙만 안 먹으면 그 규칙의 중괄호 짝과 줄 끝 세미콜론을 본다.

### 3. 카드 class (`class="card"` · `.card`)

`index.html`의 소개 문단 두 개와 취미 `ul`에 `class="card"`를 붙이고, `styles.css`에 `.card` 규칙과 `footer` 규칙을 쓴다.
[따라하기 5단계](walkthrough.md#5-카드-class-붙이고-card-규칙-쓰기)를 본다.

- HTML에는 점 없이 `class="card"`, CSS에는 점을 붙여 `.card`라고 쓴다.
- 오늘 `.card`에는 배경색 한 줄만 준다. 흰 띠처럼 보이는 것이 맞다. 상자로 만드는 일은 2일차다.
- 안 먹으면 대소문자를 본다. `.Card`는 `.card`와 다른 선택자이며 오류도 나지 않는다.

### 4. 세 페이지 확인과 DevTools Styles

`about.html`·`guestbook.html`에도 같은 `link` 줄을 넣는다. [따라하기 6단계](walkthrough.md#6-나머지-두-페이지에도-link-줄-넣기)를 본다.

- 메뉴로 세 페이지를 오가며 배경색·제목 색·메뉴 색이 같은지 본다.
- F12 → **Elements**에서 `h1`을 고르고 오른쪽 **Styles**에서 `color` 값을 바꿔 본다. 화면이 바로 바뀐다.
- 새로고침하면 그 값이 사라진다. 정상이다. DevTools에서 바꾼 것은 파일에 저장되지 않는다. 마음에 드는 색을 찾으면 `styles.css`에 옮겨 적는다.

### 5. 오늘 확인할 것

- [ ] 세 페이지의 `<head>`에 `<link rel="stylesheet" href="styles.css">`가 있다.
- [ ] 배경색·`h1` 색·`h2` 색·메뉴 색이 세 페이지에서 같다.
- [ ] `index.html`의 문단 두 개와 취미 목록만 흰 배경이다.
- [ ] `git push` 뒤 공개 주소에서 같은 화면이 열린다(확인용. 제출은 2일차에 한 장만 한다).

## 2일차 — 박스와 반응형 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` |
| 5–20분 | `nav` 규칙(`display: flex`·`gap`·`flex-wrap`)을 새로 만들고 `.card`에 `padding`·`margin`·`border`를 더한다 |
| 20–30분 | `body`에 `max-width`·`margin: 0 auto`·`padding`을 더해 본문을 가운데로 모은다 |
| 30–42분 | 파일 맨 끝에 `@media` 세 줄을 붙이고 기기 모드 375px에서 메뉴가 세로로 서는지 본다 |
| 42–50분 | 폭을 1280으로 되돌려 확인하고 `input, textarea` 폭을 정한다 |
| 50–55분 | `styles.css`에서 한 줄을 일부러 지웠다가 `git restore styles.css`로 되돌린다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 375px **캡처 1장** → 공용 PC면 자격 증명 삭제 |

### 1. 메뉴와 카드 상자 (`display: flex` · `gap` · `padding` · `margin` · `border`)

`nav` 규칙을 새로 만들고 `.card`에 세 줄을 더한다. [따라하기 10단계](walkthrough.md#10-메뉴를-가로로-카드를-상자로)를 본다.

- `nav` 규칙은 `h2`와 `nav a` 사이에 넣는다. 순서가 달라도 동작하지만 파일을 읽기 쉽게 둔다.
- 간격이 안 보이면 `gap`이 `nav`(묶는 쪽)에 들어갔는지 본다. `nav a`에 넣으면 동작하지 않는다.
- 테두리 색은 바꿔도 된다. 배경이 흰색이므로 너무 연한 색은 보이지 않는다.

### 2. 본문 폭 (`max-width` · `margin: 0 auto`)

`body` 규칙에 `max-width`·`margin: 0 auto`·`padding` 세 줄을 더한다. [따라하기 11단계](walkthrough.md#11-본문을-가운데로-모으기)를 본다.

- `width: 640px`이 아니라 `max-width: 640px`이다. 이유는 다음 문제에서 확인한다.
- 가운데로 안 가면 `margin: 0 auto`의 `auto`를 본다. `margin: 0`만 있으면 왼쪽에 붙는다.
- 넓은 화면에서 좌우에 배경색만 남으면 맞다.

### 3. `@media`와 기기 모드 375px

파일 **맨 끝**에 `@media` 세 줄을 붙이고 기기 모드에서 확인한다. [따라하기 12단계](walkthrough.md#12-media-세-줄-붙이고-375에서-보기)를 본다.

| 폭 | 메뉴 |
|---|---|
| 1280px | 가로 한 줄, 사이 16px |
| 375px | 세로 세 줄 |

- 기기 모드는 F12 → **Ctrl+Shift+M**(macOS **⌘+⇧+M**) → 위쪽 폭 칸에 `375`.
- 375에서도 가로면 세 가지를 본다. ① `nav`가 `display: flex`인가 ② `(max-width: 600px)`의 콜론이 있는가 ③ 맨 끝 `}`가 두 개인가.
- 폭을 천천히 줄여 보면 600px을 지나는 순간 바뀐다. 그 숫자가 `@media`에 적은 값이다.

### 4. 입력 칸 폭 (`input, textarea`)

`footer` 규칙 바로 위에 규칙 하나를 더하고 1280px·375px 두 폭에서 본다. [따라하기 13단계](walkthrough.md#13-입력-칸-폭-정하기)를 본다.

- 선택자 두 개를 **쉼표**로 묶는다. 쉼표를 빠뜨리면 `input textarea`가 되어 아무것도 고르지 못한다.
- `guestbook.html`에서 확인한다. 다른 두 페이지에는 입력 칸이 없어 변화가 없다.
- 두 폭 모두에서 화면 아래에 가로 스크롤 막대가 생기지 않아야 한다.

### 5. 되돌리기 (`git restore`)

`gap: 16px;` 한 줄을 일부러 지워 간격이 사라지는 것을 보고, `git restore styles.css`로 되돌린다.
[따라하기 14단계](walkthrough.md#14-git-restore로-되돌려-보기)를 본다.

- 지운 뒤 **저장**해야 화면이 바뀐다. 저장하지 않으면 `git status`에도 안 나온다.
- `git restore`는 성공해도 아무 말이 없다. `git status`가 `working tree clean`이면 된 것이다.
- 되돌린 내용은 돌아오지 않는다. 살려야 할 수정이 있을 때는 쓰지 않는다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 다시 확인해도 된다. `git status`에 `Your branch is ahead`가 있으면 push를 안 한 것이다 |
| 꾸미기가 하나도 안 먹고 3주차 화면 그대로다 | `<head>`에 `link` 줄이 있는지, `href`가 `styles.css`인지 본다. `style.css`(s 빠짐)로 적으면 파일을 못 찾는다. 공개 주소(또는 로컬 서버)에서 F12 → **Network** 탭을 열고 새로고침하면 그 줄이 빨간 **404**로 보인다. 더블클릭으로 연 `file://` 화면에서는 404 대신 실패로만 표시되므로, 파일 이름은 `<head>`의 `href` 철자로 확인한다 |
| 한 페이지만 안 꾸며진다 | 그 페이지에만 `link` 줄이 없다. 세 페이지의 `<head>`를 나란히 비교한다 |
| `.card`만 안 먹는다 | ① HTML에 `class="card"`가 있는지 ② CSS가 `.card`인지(`.Card`·`.cards`는 다른 선택자다) ③ 점을 빠뜨리지 않았는지. 선택자가 틀려도 **오류 메시지는 나오지 않고** 그 규칙만 통째로 무시된다 |
| 한 속성만 무시된다 | 속성 이름 철자를 본다. `backgroud-color`처럼 틀리면 그 한 줄만 버려지고 나머지는 그대로 적용된다 |
| 두 줄이 한꺼번에 안 먹는다 | 바로 위 줄 끝의 세미콜론을 빠뜨렸다. `color: #17213a` 뒤에 `;`가 없으면 그 줄과 다음 `font-family` 줄이 함께 무시되어 글자색이 검정, 글꼴이 기본으로 돌아간다 |
| 규칙을 더했는데 그 아래 규칙들이 전부 이상해졌다 | 중괄호 짝을 본다. `}`를 빠뜨리면 다음 규칙이 앞 규칙 안으로 들어간 것으로 읽힌다. VS Code에서 `{`에 커서를 두면 짝이 되는 `}`가 함께 표시된다 |
| 375px에서도 메뉴가 가로다 | ① `nav`에 `display: flex`가 있는지 ② `@media (max-width: 600px)`의 **콜론**이 있는지 — `(max-width 600px)`로 적으면 오류 없이 덩어리 전체가 무시된다 ③ 기기 모드 폭이 600 이하인지 |
| 화면 아래에 가로 스크롤 막대가 생긴다 | `width: 640px`으로 적지 않았는지 본다. `max-width`로 고친다. `img`의 `width="160"`은 그대로 두어도 된다 |
| 카드가 화면 양 끝에 딱 붙는다 | `body`의 `padding: 16px`이 빠졌다 |
| DevTools에서 바꾼 색이 새로고침하면 사라진다 | 정상이다. DevTools는 화면에서만 바꾼다. 마음에 들면 `styles.css`에 옮겨 적고 저장한다 |
| `git restore`를 했는데 아무 말도 안 나온다 | 정상이다. 성공하면 출력이 없다. `git status`가 `nothing to commit, working tree clean`이면 되돌아간 것이다 |
| `error: pathspec 'style.css' did not match any file(s) known to git` | 파일 이름을 잘못 적었다. `git status`에 보이는 이름 그대로 적는다 |
| `git restore` 뒤에 쓰던 내용이 사라졌다 | commit하지 않은 수정은 되돌리면 돌아오지 않는다. 남은 부분부터 다시 쓴다. 다음부터는 작게 자주 commit한다 |
| `nothing to commit, working tree clean`인데 화면이 안 바뀐다 | 파일을 저장하지 않았다. VS Code 탭 제목의 ● 표시를 본다 |
| 내 PC에서는 꾸며지는데 공개 주소에서만 3주차 화면이다 | 파일 이름의 **대소문자**가 다르다. 내 PC는 `Styles.css`도 열어 주지만 공개 주소는 구분한다. 파일 이름과 `href`를 모두 소문자로 맞춘다 |

한 번에 한 곳만 고치고 다시 새로고침한다. 해결되지 않으면 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

`https://<아이디>.github.io/my-web/`을 열고 F12 → 기기 모드(**Ctrl+Shift+M**) → 폭 `375`로 맞춘 화면을 캡처한다.

- 메뉴 `홈`·`내 정보`·`방명록`이 **세로로 한 줄씩** 보인다.
- 소개 문단과 취미 목록이 테두리 있는 흰 카드로 보인다.
- **주소창과 폭 375 표시가 함께 보이게** 찍는다.

1280px 화면과 1일차 화면은 확인용이며 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- `.card`의 `border` 색과 `background-color`를 바꿔 보고 마음에 드는 조합을 고른다. 글자가 읽히는지 꼭 확인한다.
- `@media` 안에 `h1 { font-size: 22px; }` 한 줄을 더해 좁은 화면에서 제목만 작아지게 해 본다.
- `footer`에 `border-top: 1px solid #c3cbe6;` 한 줄을 더해 본문과 선으로 나눠 본다.
- `body`의 `max-width`를 `480px`·`900px`로 바꿔 보고 글줄 길이가 어떻게 달라지는지 본다. 끝나면 640px로 되돌린다.
- 기기 모드에서 폭을 600 근처에서 1px씩 움직여 메뉴가 바뀌는 지점을 찾아본다.

추가 과제는 선택 사항이며 채점하지 않는다.
