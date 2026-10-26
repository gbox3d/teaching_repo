[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project)

# 9주차 따라하기 — 마크다운 비교 예제로 README 1차판을 조립하고 발표하기

이번 주는 새 저장소 `web-week09` 를 만든다. 7주차 완성본을 넣고, 비교 예제(마크다운 `.md` 파일)는 그 안의 `ex/` 폴더에 저장한다. 기호나 띄어쓰기를 바꾼 뒤 결과를 **VS Code 미리 보기**와, 올린 뒤의 **GitHub 저장소 화면**에서 본다.
1일차 끝에 `web-week09` 맨 위에 `README.md` 1차판과 화면 캡처 두 장을 넣고 올린다. 사이트의 HTML·CSS·JavaScript 는 고치지 않는다. 2일차는 발표다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

비교 예제 3개는 교재 저장소의 [examples/day1](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project/examples/day1) 폴더에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다.

## 1일차

### 1. web-week09 폴더 만들고 7주차 완성본 넣기

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-week09` 를 만들고 VS Code **File › Open Folder** 로 연다.

7주차 완성본을 넣는다. 내 `web-week07` 저장소 GitHub 화면에서 **Code › Download ZIP** 을 누르고, 압축을 푼 폴더에서 맨 위 파일(`index.html`·`about.html`·`guestbook.html`·`styles.css`·`app.js`·`guestbook.js`·`server.mjs`)과 `images/` 를 `web-week09` 로 옮긴다. 지난주 `ex/` 폴더는 옮기지 않는다. 8주차 시험 저장소 `web-week08` 은 쓰지 않는다.
ZIP 을 못 받았으면 교재 [7주차 `examples/day2/web-week07/`](../week07_async_modules/examples/day2/web-week07/) 의 파일을 2단계와 같은 **Raw** 방법으로 받고, [server.mjs](../../tools/static-server/server.mjs) 도 같은 방법으로 받는다.

이어서 `web-week09` 안에 `ex` 폴더를 만든다. 현재 폴더: `web-week09`

```bash
mkdir ex
```

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week09/
  ex/            ← 아직 비어 있다
  images/
  about.html
  app.js
  guestbook.html
  guestbook.js
  index.html
  server.mjs
  styles.css
```

- `index.html` 을 두 번 눌러 열면 7주차 완성 화면(인사말 카드와 버튼 두 개)이 보인다. 이 사이트를 발표한다.
- 지난주 ZIP 에 `README.md` 가 있으면 그대로 둔다. 7단계에서 내용을 모두 지우고 1차판으로 다시 쓴다.
- 이번 주에는 HTML·CSS·JavaScript 파일을 고치지 않는다.

### 2. 비교 예제 가져오기

오늘 파일은 마크다운 세 개다. JavaScript 가 없어서 고르기 페이지(`index.html`)가 없다.

| 파일 | 비교하는 것 |
|---|---|
| [ex01_heading.md](examples/day1/ex01_heading.md) | 같은 글자 `공개 주소` 앞에 `#` 하나 / `##` 둘 / `#` 뒤 띄어쓰기 없음 |
| [ex02_list.md](examples/day1/ex02_list.md) | `- ` 로 시작하는 세 줄 / 기호 없는 세 줄 / `-` 뒤 띄어쓰기 없음 |
| [ex03_link.md](examples/day1/ex03_link.md) | 인터넷 주소 링크 / 같은 폴더의 파일 링크 / 그 링크에서 `]` 와 `(` 사이만 띄운 줄 |

[교재 저장소 examples/day1 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project/examples/day1)에서 파일을 누르고 오른쪽 위 **Raw** 를 누른다. 원문만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `web-week09/ex/` 에 저장한다. 파일 이름은 교재와 **같게** 둔다. Raw 가 열리지 않을 때만 주석 줄까지 그대로 친다.

**예상 결과** — `ex/` 안에 파일 세 개가 있다.

```text
ex/
  ex01_heading.md
  ex02_list.md
  ex03_link.md
```

- 저장한 이름이 `.txt` 로 끝나면(`ex01_heading.md.txt`) 이름을 고친다. 끝이 `.md` 여야 VS Code 가 마크다운으로 알아보고 미리 보기를 띄운다.
- 교재 GitHub 화면에서 파일을 누르면 처음에는 렌더된 모양이 보인다. 원문은 **Code** 나 **Raw** 를 눌러 본다.

### 3. 미리 보기 — 원문 옆에 렌더된 모양

VS Code 에서 `ex/ex01_heading.md` 를 연다. **Ctrl+K** 를 누르고 손을 뗀 뒤 **V**(macOS **⌘+K** 다음 **V**)를 누르면 오른쪽에 미리 보기가 열린다. 편집기 오른쪽 위의 미리 보기 아이콘(**Open Preview to the Side**)을 눌러도 된다.

**예상 결과** — 왼쪽은 원문, 오른쪽은 렌더된 모양이다. 세 줄은 글자(`공개 주소`)가 같고 `#` 개수와 띄어쓰기만 다르다.

```text
원문(왼쪽)                     렌더된 모양(오른쪽)
1번 — 샵(#) 하나, …            1번 — 샵(#) 하나, …
# 공개 주소                    공개 주소         ← 가장 큰 제목
2번 — 샵 둘, …                 2번 — 샵 둘, …
## 공개 주소                   공개 주소         ← 한 단계 작은 제목
3번 — 샵 하나, …               3번 — 샵 하나, …
#공개 주소                     #공개 주소        ← 보통 글자
```

- **렌더**는 원문의 기호를 읽어 제목·목록·링크 모양으로 그려 보이는 것이다. 이번 주에는 VS Code 미리 보기와 GitHub 저장소 화면이 렌더한다.
- 맨 위 `<!-- … -->` 두 줄은 HTML 주석이라 미리 보기에 보이지 않는다.
- 원문을 고치면 미리 보기가 따라 바뀐다. 저장은 Ctrl+S 로 따로 한다.

### 4. 값 바꾸는 요령

실험은 늘 같은 순서다. **원문을 고친다** → **미리 보기**를 본다 → 저장한다(Ctrl+S, macOS는 ⌘+S).
바꾸기 전에 무엇이 달라질지 먼저 말해 보고 확인한다.

**바꿔 보기** — `ex/ex02_list.md` 를 열고 미리 보기를 띄운다. 2번의 세 줄(`홈`·`내 정보`·`방명록`) 사이에 빈 줄을 하나씩 넣는다.

**예상 결과** — 넣기 전에는 2번이 `홈 내 정보 방명록` 한 줄로 이어져 보이고, 넣은 뒤에는 세 줄로 나뉘어 보인다. 줄 앞에 점(•)은 붙지 않는다. 점이 붙는 목록은 1번처럼 줄 맨 앞에 `- ` 가 있을 때다.

- 원문에서 줄을 바꾸기만 하면 렌더된 모양에서는 한 문단으로 이어진다. 빈 줄이 문단을 나눈다.
- 확인했으면 넣은 빈 줄을 지워 되돌린다. 원래대로 못 돌리겠으면 교재에서 그 파일을 다시 **Raw** 로 받아 덮어쓴다.
- 파일마다 무엇을 바꿔 볼지는 [1일차 실습](lab.md#1일차--마크다운-세-가지로-readme-1차판-60분)에 있다.

### 5. 화면 두 장 캡처와 데이터가 가는 세 곳

README 의 `## 화면` 에 넣을 캡처 두 장을 찍는다. 먼저 `web-week09` 맨 위에 `screenshots` 폴더를 만든다. 현재 폴더: `web-week09`

```bash
mkdir screenshots
```

1. `index.html` 을 열고 **인사 바꾸기**를 한 번 누른 뒤 화면을 캡처한다.
   - Windows: **Win+Shift+S** → 영역을 끌어 선택 → 그림판 등에 붙여 넣고 저장
   - macOS: **⌘+Shift+4** → 영역을 끌어 선택하면 바탕화면에 저장
2. 저장한 파일을 `screenshots/home.png` 로 옮긴다.
3. `guestbook.html` 에서 이름 `student01`, 메시지 `첫 방명록입니다.` 를 넣고 **남기기**를 누른 뒤 같은 방법으로 캡처해 `screenshots/guestbook.png` 로 옮긴다.

**예상 결과** — `screenshots/` 안에 `home.png` 와 `guestbook.png` 가 있다. 홈 캡처에는 `반갑습니다. 오늘도 좋은 하루 되세요.` 와 `클릭 1회`, 방명록 캡처에는 `student01: 첫 방명록입니다.` 가 보인다. 같은 자리의 예시가 [screenshots/home.png](examples/day2/web-week09/screenshots/home.png) 와 [screenshots/guestbook.png](examples/day2/web-week09/screenshots/guestbook.png) 다.

이제 방명록 탭을 **새로고침**한다. 이어서 같은 `guestbook.html` 을 새 탭으로 하나 더 연다.

**예상 결과** — 새로고침하면 `마지막으로 남긴 글` 아래가 `아직 남긴 글이 없습니다.` 로 돌아간다. 새 탭에도 남긴 글이 없다.

```text
데이터가 가는 세 곳
① 화면(이 탭)        지금 방명록 글. 새로고침하면 사라진다
② 브라우저 저장소     이 브라우저에만 남는다            → 11주차
③ 인터넷 서버 DB      여러 사람이 함께 본다             → 선택 특강
```

- 지금 방명록 글은 ① 이다. JavaScript 가 이 탭의 화면(DOM)에 쓴 글이라, 새로고침하면 브라우저가 파일을 다시 읽어 처음 화면을 만든다(6주차 ex03 과 같다).
- 사이트 파일(HTML·CSS·JS)은 GitHub 에 올려 두어 누구나 같은 파일을 받는다. 방문자가 남긴 글은 그 파일에 들어가지 않는다. ③ 은 [선택 특강](../../specials/supabase_guestbook/README.md)에서 다룬다.
- **동작한 뒤의 화면**을 찍는다. `클릭 0회` 나 `아직 남긴 글이 없습니다.` 인 캡처는 눌러 보지 않은 것으로 보인다.
- 파일 이름은 영문 소문자로 한다. 한글·공백·대문자가 섞이면 README 링크에서 틀리기 쉽다.

### 6. 조립표

28분부터 조립한다. 이제 `ex/` 가 아니라 `web-week09` **맨 위**에 `README.md` 를 쓴다. 조립하는 줄은 모두 비교 예제에서 본 모양이다.

| 조립할 줄 | 출처 |
|---|---|
| `# 내 사이트 이름` 한 줄 | [ex01](examples/day1/ex01_heading.md) 1번. 사이트 이름은 7주차 `index.html` 맨 위 `<h1>` 글자와 같게 |
| 소개 한 문장(기호 없이) | [ex02](examples/day1/ex02_list.md) 2번, 기호 없는 줄은 문단이 된다 |
| `## 공개 주소` · `## 페이지` · `## 기능` · `## 화면` · `## 이번에 배운 것` | [ex01](examples/day1/ex01_heading.md) 2번 |
| `- [https://student01.github.io/web-week09/](https://student01.github.io/web-week09/)` | [ex02](examples/day1/ex02_list.md) 1번 + [ex03](examples/day1/ex03_link.md) 1번(인터넷 주소) |
| `- [홈 (index.html)](index.html) — 설명` 세 줄 | [ex02](examples/day1/ex02_list.md) 1번 + [ex03](examples/day1/ex03_link.md) 2번(같은 저장소 안의 파일) |
| 기능 두 줄, 배운 것 세 줄 | [ex02](examples/day1/ex02_list.md) 1번 |
| `- [홈 화면 캡처](screenshots/home.png)` 두 줄 | [ex02](examples/day1/ex02_list.md) 1번 + [ex03](examples/day1/ex03_link.md) 2번. `폴더/파일` 경로는 3주차 `images/profile.png` 와 같다 |
| 덩어리 사이의 빈 줄 | ex01~ex03, 형제 사이를 빈 줄로 나눴다 |

옮겨 적을 때 출처 ex 파일을 옆에 열어 두고, 같은 모양이 거기서 어떻게 렌더됐는지 떠올린다.

### 7. README 1차판 조립하기

`web-week09` 맨 위(`index.html` 옆)에 새 파일 `README.md` 를 만든다. 이미 있으면 내용을 모두 지운다. 이름은 대문자 `README` 와 `.md` 를 그대로 쓴다.
조립표 순서로 쓴다.

1. 큰 제목 한 줄 — `# ` 와 내 사이트 이름(ex01 1번). 이름은 홈 `index.html` 맨 위 `<h1>` 글자와 같게 쓴다.
2. 소개 한 문장 — 기호 없이(ex02 2번).
3. `## 공개 주소` — 이번 주 내 공개 주소를 링크로 한 줄(ex03 1번).
4. `## 페이지` — 세 페이지를 `[보이는 글](파일 이름)` 링크로 세 줄, 링크 뒤에 한 줄 설명(ex03 2번).
5. `## 기능` — 버튼 한 줄, 폼 한 줄(ex02 1번).
6. `## 화면` — `screenshots/` 의 캡처 두 장을 링크로 두 줄(ex02 1번 + ex03 2번).
7. `## 이번에 배운 것` — 세 줄(ex02 1번).

덩어리 사이에는 빈 줄을 하나씩 둔다. 아래가 교재 예시 전문이다.

```markdown
# student01의 웹 연습장

웹프로그래밍 수업에서 한 주씩 늘려 가는 자기소개 사이트입니다.

## 공개 주소

- [https://student01.github.io/web-week09/](https://student01.github.io/web-week09/)

## 페이지

- [홈 (index.html)](index.html) — 인사말, 소개, 취미 목록
- [내 정보 (about.html)](about.html) — 아이디·이메일·관심 분야 표
- [방명록 (guestbook.html)](guestbook.html) — 이름·메시지 폼

## 기능

- 홈의 "인사 바꾸기"와 "다크 모드" 버튼을 누르면 문장과 배경색이 바뀌고 클릭 횟수가 1씩 오릅니다.
- 방명록에서 이름과 메시지를 적고 "남기기"를 누르면 아래에 한 줄로 보입니다. 빈칸이면 안내 문장이 나옵니다.

## 화면

- [홈 화면 캡처](screenshots/home.png)
- [방명록 화면 캡처](screenshots/guestbook.png)

## 이번에 배운 것

- HTML 뼈대와 nav로 세 페이지를 이어 놓는 법
- CSS로 색·박스·flex·화면 폭에 따른 배치를 정하는 법
- 버튼 클릭과 폼 제출을 자바스크립트로 받아 화면을 바꾸는 법
```

같은 파일이 [examples/day2/web-week09/README.md](examples/day2/web-week09/README.md)에 있다.

- 예시 그대로 두지 않는다. 사이트 이름(1행)은 내 홈 `<h1>` 글자와 같게, 소개 문장(3행)·기능 두 줄·배운 것 세 줄은 내 사이트와 내가 한 것에 맞게 쓴다. `student01` 이 남아 있으면 예시를 베낀 것으로 본다.
- 7행 공개 주소는 `student01` 자리만 본인 아이디로 바꾼다. 저장소 이름 `web-week09` 는 그대로다.
- 11~13행은 대괄호에 보이는 글, 소괄호에 같은 저장소 안의 파일 이름을 쓴 링크 뒤에 ` — 설명` 을 붙였다. 22·23행의 `screenshots/home.png` 는 `screenshots` 폴더 안의 `home.png` 다.

**예상 결과** — 미리 보기를 옆에 띄우면 큰 제목 한 줄, 소개 문장, 작은 제목 다섯과 그 아래 점이 붙은 목록이 보인다. 링크는 여섯 개다(공개 주소 하나, 페이지 셋, 캡처 둘). 줄 맨 앞의 `#`·`- ` 와 링크를 만드는 `[`·`](`·`)` 는 미리 보기에 보이지 않는다. `홈 (index.html)` 의 괄호는 대괄호 안에 쓴 보이는 글이라 그대로 보인다.

### 8. 확인 — 링크, 짝과 2분 연습, 서버(시간이 남으면)

미리 보기에서 `## 페이지`·`## 화면` 의 링크를 하나씩 눌러 그 파일이 열리는지 본다. 공개 주소 링크는 아직 저장소와 Pages 가 없으니 9단계에서 누른다.

이어서 짝과 번갈아 2분 발표 순서를 한 번씩 말하면서 눌러 본다. 오늘은 내 PC 화면으로 한다.

```text
0:00  사이트 이름과 한 줄 소개
0:20  nav 로 홈 → 내 정보 → 방명록
0:50  홈에서 [인사 바꾸기]
1:10  방명록에 이름·메시지를 넣고 [남기기]
1:30  이름을 비우고 [남기기] → 안내 문장
1:40  README 다섯 항목, Commits 탭은 잠깐 (2일차에 GitHub 화면으로)
```

**예상 결과** — 2분 안에 여섯 줄이 끝난다. 넘치면 어디를 줄일지 정한다. 대개 첫 소개가 길다.

서버 확인과 폭 확인은 **시간이 남으면** 한다. 사이트 파일은 7주차와 같다. 현재 폴더: `web-week09`

```bash
node server.mjs
```

`http://localhost:8000/` 에서 nav 로 세 페이지를 오가고 버튼과 폼을 한 번씩 해 본다. 이어서 주소창에 `http://localhost:8000/README.md` 를 친다.

**예상 결과** — 세 페이지는 두 번 눌러 연 것과 같게 동작한다. 터미널에는 브라우저가 받아 간 파일마다 `200 GET /…` 한 줄씩 찍힌다. `404 GET /favicon.ico` 줄도 보일 수 있는데 괜찮다([서버 사용 안내](../../tools/static-server/README.md#터미널에-찍히는-줄-읽기) 참고). DevTools Console 에도 같은 `favicon.ico` 의 404 빨간 줄(`Failed to load resource: the server responded with a status of 404 (Not Found)`) 하나가 보일 수 있는데 이것도 괜찮다. `README.md` 는 렌더되지 않고 `#`·`-`·대괄호가 그대로 있는 원문 글자로 보인다. 브라우저는 `.md` 를 받으면 글자 그대로 보여 준다. README 를 렌더해 보여 주는 곳은 GitHub 저장소 화면이다.
확인이 끝나면 터미널에서 **Ctrl+C** 로 서버를 멈춘다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다. Node 가 없는 PC 는 `index.html` 을 두 번 눌러 연 것으로 대신한다.

- DevTools 의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)로 폭 375 와 1280 에서 세 페이지를 본다. 375 에서는 메뉴가 세로로 선다(4주차 `@media`). 발표 화면이 좁아도 세 페이지가 깨지지 않으면 된 것이다.

### 9. 이번 주 저장소 만들어 올리기

1일차 50–60분에 한다. GitHub 에서 **New repository** 를 누르고 이름 `web-week09`, **Public** 으로 만든다. README 는 추가하지 않는다. 내 PC 에서 쓴 `README.md` 를 올린다.
터미널에서 2주차에 배운 순서 그대로 친다. 현재 폴더: `web-week09`

```bash
git init
git add .
git commit -m "9주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week09.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save** 를 누른다.

**예상 결과** — GitHub 저장소 화면 `https://github.com/student01/web-week09` 를 새로고침하면 파일 목록 아래에 README 가 렌더되어 보인다. 큰 제목, 작은 제목 다섯, 링크 여섯 개가 보인다. 이 화면을 캡처한다. **제출 캡처 1장**이다.
`ex` 폴더를 눌러 `ex01_heading.md` 를 열면 렌더된 모양이 보인다. 위쪽 **Code** 를 누르면 원문, **Preview** 를 누르면 다시 렌더된 모양이다.
1~3분 뒤 `https://student01.github.io/web-week09/` 를 열어 세 페이지·버튼·폼을 확인하고, README 의 공개 주소 링크도 눌러 본다.
공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com` 을 지우고 나간다.

- README 가 안 보이면 파일이 맨 위에 있는지, 이름이 `README.md` 인지 본다.
- 캡처 링크를 눌러 404 면 `screenshots/` 폴더가 올라갔는지, 링크의 파일 이름이 대소문자까지 같은지 본다. GitHub 은 대소문자를 가린다.
- push 가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../week02_github_pages/lab.md#막혔을-때)를 본다.

## 2일차

### 10. 폴더 열기와 탭 세 개

README 를 고칠 일이 있을 때만 폴더를 연다. 같은 PC에 `web-week09` 폴더가 남아 있으면 VS Code로 그대로 연다. 없으면 받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week09.git
```

내려받은 `web-week09` 를 **File › Open Folder** 로 연다.

자기 차례 두 사람 앞에서 브라우저 탭 세 개를 연다.

```text
탭 1  https://student01.github.io/web-week09/
탭 2  https://github.com/student01/web-week09
탭 3  https://github.com/student01/web-week09/commits
```

**예상 결과** — 세 탭이 모두 열려 있다. 탭 1 은 홈 화면 처음 상태(`클릭 0회`)이고, 탭 2 는 파일 목록 아래에 README 가 보이고, 탭 3 에는 `9주차 1일차` commit 이 있다.

- 방명록은 비워 둔 상태로 시작한다. 발표 중에 직접 한 줄 남긴다.
- 다크 모드를 켜 두었으면 끄고 시작한다. 첫 화면이 밝아야 글씨가 잘 보인다.
- 다른 사이트나 로그인 화면이 보이는 탭은 닫는다.

### 11. 2분 발표 순서대로

8단계에서 연습한 여섯 줄을 그대로 한다. 말하면서 누른다.

1. 탭 1을 보이며 "`student01`의 웹 연습장입니다. 세 페이지가 있습니다."
2. nav 로 홈 → 내 정보 → 방명록 → 홈.
3. **인사 바꾸기**를 누르며 "버튼을 누르면 문장이 바뀌고 클릭 횟수가 오릅니다."
4. 방명록에서 이름·메시지를 넣고 **남기기**.
5. 이름을 비우고 **남기기** → `이름을 입력하세요.`
6. 탭 2 의 README 다섯 항목을 짚고, 탭 3 의 **Commits** 탭은 올린 기록만 잠깐 보이며 마무리.

**예상 결과** — 2분 안에 끝나고, 채점자가 공개 주소·세 페이지·버튼·폼·README 를 화면에서 확인한다.

- 코드 파일은 띄우지 않는다. 구술 질문("이 버튼을 누르면 어느 파일이 실행됩니까?")을 받으면 그때 연다.
- 잘 안 되는 기능이 있으면 되는 것부터 보여 주고 남은 시간에 말한다.
- "남긴 글이 새로고침하면 사라지나요?"에는 "아직 화면에만 있습니다(세 곳 중 ①)"라고 답한다.
- 공개 주소가 열리지 않으면 탭 3 의 **Commits** 탭과 내 PC 화면으로 대신한다. 손을 들어 알린다.

### 12. 발표가 끝나면 — 끝 루틴

2일차 55–60분에 한다. README 를 고쳤으면 올린다. 고치지 않았으면 이 단계는 하지 않는다. 현재 폴더: `web-week09`

```bash
git add .
git commit -m "9주차 2일차"
git push
```

**예상 결과** — 저장소 첫 화면을 새로고침하면 고친 README 가 보인다.
공용 PC라면 자격 증명을 지우고 나간다.

- 제출은 발표 2분과 캡처 1장(저장소 첫 화면)이다. 제출 위치와 마감은 수업 공지를 따른다.
- 막히면 [실습지의 막혔을 때](lab.md#막혔을-때)를 본다.
