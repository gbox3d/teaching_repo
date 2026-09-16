# 3주차 실습 — 세 페이지 자기소개 사이트

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week03_semantic_html

2주차에 공개한 `my-web`을 홈·내 정보·방명록 세 페이지로 늘린다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.
이번 주는 HTML만 쓴다. `styles.css`와 `app.js`는 **지우지 말고** 그대로 둔다. 화면이 꾸며지지 않은 것이 정상이다.

## 1일차 — 세 페이지의 뼈대와 자기소개 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` 뒤 **File › Open Folder** |
| 5–15분 | `index.html`의 2주차 내용과 `<link>`·`<script>` 두 줄을 지우고 `header`·`nav`·`main`·`footer` 뼈대를 만든다 |
| 15–28분 | `h1`에 수업용 별칭, `main`에 `h2 소개`와 문단 두 줄, `strong` 하나 |
| 28–40분 | `images` 폴더에 `profile.png`를 넣고 `img`·`alt`, `nav`에 링크 두 개(`index.html`·`about.html`) |
| 40–55분 | `h2 취미`와 `ul`·`li` 세 줄, `footer` 한 줄 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 새로고침 → 공용 PC면 자격 증명 삭제 |

### 1. 뼈대 만들기 (`header` · `nav` · `main` · `footer`)

`index.html`의 `<body>` 안을 모두 지우고 `<head>`의 `<link>`·`<script>` 두 줄도 지운 뒤 뼈대 네 개를 만든다.
[따라하기 2단계](walkthrough.md#2-indexhtml-비우고-뼈대-만들기)를 본다.

- 지운 직후에는 **아무것도 없는 흰 화면**이 정상이다. 카드와 버튼이 사라졌는지 새로고침해 확인한다.
- `styles.css`·`app.js` 파일은 지우지 않는다. `index.html`에서 연결 줄만 뺐다.
- `<title>`과 `<meta>` 두 줄은 그대로 둔다.

### 2. 제목과 문단 (`h1` · `h2` · `p` · `strong`)

`header`에 `h1`, `main`에 `h2`와 `p` 두 줄을 넣고 한 곳에 `strong`을 쓴다. [따라하기 3단계](walkthrough.md#3-제목과-소개-문단-쓰기)를 본다.

- `h1`은 페이지에 하나만 둔다. 이름 대신 수업용 별칭을 쓴다(실명 금지).
- `h2`가 `h1`보다 글자가 작게 보이는 것이 맞다. 크기를 바꾸려고 태그를 고르지 않는다.
- 굵게 보이는 곳이 없으면 `<strong>`이 닫혔는지 본다.

### 3. 그림과 링크 (`img src` · `alt` · `a href`)

`my-web/images/` 폴더를 만들고 [examples/day1/images/profile.png](examples/day1/images/profile.png)를 넣은 뒤 `img`와 `nav` 링크 두 개를 만든다.
[따라하기 4단계](walkthrough.md#4-프로필-그림과-nav-링크-넣기)를 본다.

- 그림 자리에 글자만 보이면 경로가 틀린 것이다. 폴더 이름(`images`)과 파일 이름(`profile.png`)의 철자를 본다.
- `alt`에는 그림이 안 보일 때 대신 읽힐 말을 쓴다. "사진"·"이미지"만 쓰지 않는다.
- `내 정보`를 눌러 2주차 `about.html`이 열리면 상대 경로가 맞은 것이다.

### 4. 취미 목록 (`ul` · `li`)

`h2 취미`와 `ul` 안에 `li` 세 줄, 마지막으로 `footer` 한 줄을 넣는다. [따라하기 5단계](walkthrough.md#5-취미-목록과-footer-넣기)를 본다.

- 세 줄 앞에 점(•)이 붙으면 맞다. 점이 없으면 `li`가 `ul` 밖에 있는 것이다.
- 목록 항목 사이에 `<br>`을 넣지 않는다. 줄 하나가 `li` 하나다.

### 5. 오늘 확인할 것

- [ ] 브라우저에 제목 · 링크 두 개 · 소개 · 그림 · 문단 · 취미 목록 · 맨 아래 한 줄이 차례로 보인다.
- [ ] `git push` 뒤 공개 주소에서 같은 화면이 열린다(확인용 캡처. 제출은 2일차에 한 장만 한다).
- [ ] `styles.css`와 `app.js` 파일이 폴더에 그대로 있다.

## 2일차 — 내 정보 표와 방명록 form (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` → `git switch -c guestbook`으로 브랜치를 만들며 옮겨 간다 |
| 5–20분 | `about.html`을 전체 지우고 세 페이지 공통 뼈대 + 내 정보 표(2열 4행)로 다시 쓴다 |
| 20–40분 | `guestbook.html`을 새로 만들어 `ol` 쓰는 순서와 이름·이메일·메시지 `form`을 넣는다 |
| 40–50분 | `index.html`의 `nav`에 `방명록`을 더해 세 페이지 메뉴를 같게 맞추고 링크로 오가 본다 |
| 50–55분 | `git add .` → `git commit` → `git switch main` → `git merge guestbook` |
| 55–60분 | 끝 루틴: `git push` → 공개 주소의 `guestbook.html` 확인 → **캡처 1장** → 공용 PC면 자격 증명 삭제 |

### 1. 브랜치 만들기 (`git switch -c guestbook`)

`git pull` 뒤 `git switch -c guestbook`을 한다. [따라하기 8단계](walkthrough.md#8-guestbook-브랜치-만들기)를 본다.

- `Switched to a new branch 'guestbook'`이 보이고 `git branch`에 `* guestbook`이 있어야 한다.
- 이미 만들어 두었다면 `-c` 없이 `git switch guestbook`만 한다.
- `git pull`이 거부되면 아래 **막혔을 때**의 `local changes` 줄을 본다.

### 2. 내 정보 표 (`table` · `tr` · `th` · `td`)

`about.html`을 전체 지우고 `header`·`nav`·`main`·`footer` 뼈대 위에 2열 4행 표를 만든다.
[따라하기 9단계](walkthrough.md#9-abouthtml을-내-정보-표로-다시-쓰기)를 본다.

| 줄 | 왼쪽 칸 | 오른쪽 칸 |
|---|---|---|
| 1 | `th` 항목 | `th` 내용 |
| 2 | `td` 아이디 | `td` 본인 GitHub 아이디 |
| 3 | `td` 이메일 | `td` `student01@example.com` 같은 수업용 주소 |
| 4 | `td` 관심 분야 | `td` 자유 |

- 첫 줄만 굵고 가운데로 보이면 `th`가 맞게 들어간 것이다.
- 선이 없는 것이 정상이다. `border` 속성을 쓰지 않는다. 선은 4주차 CSS로 그린다.
- **실제 이메일·학번·전화번호를 넣지 않는다.** 수업용 가상 정보를 쓴다.
- 이 파일의 `nav`에는 처음부터 링크 세 개를 넣는다. `방명록`은 다음 단계에서 만든다.

### 3. 방명록 form (`form` · `label for` · `input` · `textarea` · `button`)

`guestbook.html`을 새로 만들고 `h3 쓰는 순서` + `ol`, 그 아래 입력 칸 세 개와 제출 버튼을 넣는다.
[따라하기 10단계](walkthrough.md#10-guestbookhtml-만들기)를 본다.

- 이름은 `type="text"`, 이메일은 `type="email"`, 메시지는 `textarea rows="4"`로 만든다.
- `label`의 `for`와 `input`의 `id`를 같게 한다. 세 쌍 모두 이름표를 눌러 커서가 들어가는지 확인한다.
- **남기기**를 누르면 주소창 끝에 `?`만 붙고 화면은 그대로다. 정상이다. 화면에 띄우는 일은 7주차에 한다.
- `form`에 `action`·`method`를 적지 않는다. 이번 주에는 보낼 곳이 없다.

### 4. nav 통일과 이동 확인 (`a href`)

`index.html`의 `nav`에 `<a href="guestbook.html">방명록</a>` 한 줄을 더해 세 페이지 메뉴를 같게 만든다.
[따라하기 11단계](walkthrough.md#11-세-페이지-nav-통일하기)를 본다.

- 세 페이지에서 세 링크를 모두 눌러 본다. 아홉 번 눌러 모두 열려야 한다.
- 404가 나면 파일 이름의 철자와 대소문자를 본다. 내 PC에서는 열려도 공개 주소에서는 404가 될 수 있다.

### 5. merge와 push (`git merge` · `git push`)

commit 뒤 `git switch main` → `git merge guestbook` → `git push`를 한다. [따라하기 12단계](walkthrough.md#12-main에-merge하고-push-하기)를 본다.

- `git switch main` 직후 `guestbook.html`이 잠시 사라진다. 2주차와 같다. merge 뒤 돌아온다.
- merge 출력에 `Fast-forward`와 `3 files changed`가 보여야 한다.
- push 뒤 1분쯤 기다렸다가 공개 주소의 `guestbook.html`을 열어 캡처한다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 다시 확인해도 된다. `git status`에 `Your branch is ahead`가 있으면 push를 안 한 것이다 |
| `fatal: destination path 'my-web' already exists and is not an empty directory.` | 그 자리에 이미 `my-web` 폴더가 있다. clone 대신 그 폴더를 열고 `git pull`을 한다 |
| `error: Your local changes to the following files would be overwritten by merge:` / `Please commit your changes or stash them before you merge.` / `Aborting` | 고쳐 놓고 commit하지 않은 파일이 있는 채로 `git pull`을 했다. 먼저 `git add .` → `git commit` 하고 다시 `git pull` 한다 |
| `fatal: a branch named 'guestbook' already exists` | 이미 만든 브랜치다. `-c`를 빼고 `git switch guestbook`만 한다 |
| `fatal: The current branch guestbook has no upstream branch.` | `guestbook` 브랜치에서 `git push`를 쳤다. 이번 주 순서에서는 브랜치를 push하지 않는다. `git switch main` → `git merge guestbook` → `git push` |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시와 `git log --oneline`을 본다 |
| 그림 자리에 `student01의 프로필 그림` 글자만 보인다 | `img`의 경로가 틀렸다. `images` 폴더가 `my-web` 바로 아래에 있는지, 파일 이름이 `profile.png`인지 본다. 이 화면은 `alt`가 제대로 보이는 화면이기도 하다 |
| 그림을 눌러도 아무 일이 없다 | 정상이다. `img`는 링크가 아니다 |
| 브라우저에 `파일에 액세스할 수 없음` / `ERR_FILE_NOT_FOUND` | 내 PC에서 없는 파일을 연 것이다. 주소창 끝의 파일 이름 철자를 본다 |
| 내 PC에서는 링크가 열리는데 공개 주소에서만 404 | 파일 이름의 **대소문자**가 다르다. 내 PC는 대소문자를 구분하지 않아 `Guestbook.html`도 열리지만 공개 주소는 구분한다. 링크와 파일 이름을 모두 소문자로 맞춘다 |
| 이름표를 눌러도 입력 칸에 커서가 안 간다 | `label`의 `for`와 `input`의 `id`가 다르다. 대소문자까지 비교한다 |
| **남기기**를 눌렀더니 주소창에 `?`가 붙고 아무 일이 없다 | 정상이다. `form`에 보낼 곳이 없어 주소만 바뀐다. 화면에 띄우는 일은 7주차에 한다 |
| 표에 선이 없다 | 정상이다. `border` 속성을 쓰지 않는다. 선은 4주차 CSS로 그린다 |
| 화면이 2주차처럼 안 예쁘다 | 정상이다. `index.html`에서 `styles.css` 연결을 뺐다. 4주차에 다시 연결한다 |
| `about.html`만 옛날 카드 화면이다 | 1일차에는 그것이 맞다. 2일차 두 번째 구간에서 표로 다시 쓴다 |

한 번에 한 곳만 고치고 다시 확인한다. 해결되지 않으면 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

`https://<아이디>.github.io/my-web/guestbook.html`을 열고 **주소창이 함께 보이게** 화면을 캡처한다.

- 메뉴에 `홈`·`내 정보`·`방명록` 세 링크가 보인다.
- `이름`·`이메일`·`메시지` 입력 칸과 **남기기** 버튼이 보인다.

1일차 화면과 `about.html` 표는 확인용이며 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- `index.html`의 취미 `ul`을 `ol`로 바꿔 보고 점과 번호의 차이를 본다. 다시 `ul`로 되돌린다.
- `about.html` 표에 줄(`tr`)을 하나 더해 5행으로 만든다.
- `guestbook.html`의 `ol`에 순서를 한 줄 더 적는다.
- 이메일 칸에 `abc`처럼 `@`가 없는 값을 넣고 **남기기**를 눌러 본다. 브라우저가 무엇을 하는지 본다. `type="email"`을 보고 브라우저가 스스로 해 주는 일이며, 이 과목에서는 `required`·`pattern`을 쓰지 않는다.
- `footer`에 오늘 날짜를 한 줄 적어 push하고 공개 주소가 따라 바뀌는지 본다.

추가 과제는 선택 사항이며 채점하지 않는다.
