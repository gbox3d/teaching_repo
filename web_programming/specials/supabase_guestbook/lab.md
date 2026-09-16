# 특강 실습 — 서버에 저장되는 방명록 만들기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/supabase_guestbook

**확인과 캡처는 공개 주소에서만 한다.** 파일을 더블클릭해 `file://`로 열면 목록이 보이지 않는다.
브라우저가 파일에서 인터넷 요청을 막기 때문이다.

모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.
오늘은 설명·시연 50분(1부 25분 + 2부 25분) 뒤 아래 60분을 직접 한다.

## 실습 60분

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/student01/my-web.git`. `my-web` 안에 폴더 `online`을 만든다 |
| 5–15분 | Supabase에 가입하고 **New project**로 프로젝트 하나를 만든다 (준비까지 1~2분 기다린다) |
| 15–25분 | **SQL Editor**에 `schema.sql` 전체를 붙여 넣고 **Run** 한 번 → **Table Editor**에서 `guestbook` 표 확인 |
| 25–35분 | 위쪽 **Connect** 버튼(없으면 **Project Settings › API Keys**·**Data API**)에서 두 값을 복사해 `online/config.js`를 만든다 |
| 35–45분 | `guestbook.html`·`guestbook.js`를 `online/`에 넣고 `git push` → 공개 주소에서 `방명록 0개` 확인 |
| 45–55분 | 글을 남겨 목록을 만들고, 공개 페이지와 Table Editor를 함께 캡처한다. 휴대폰이나 옆자리 PC에서도 열어 본다 |
| 55–60분 | `git add .` → `git commit -m "…"` → `git push` → 공개 주소 새로고침. 공용 PC면 자격 증명과 Supabase 로그인을 정리한다 |

### 1. 새 폴더 준비

11주차까지 만든 `my-web/guestbook.html`은 **고치지 않는다**. `online` 폴더를 새로 만들고 그 안에서만 작업한다.
[따라하기 준비·1단계](walkthrough.md#1-온라인-방명록-폴더-만들기)를 본다.

- 시작 전 `git status`가 `nothing to commit, working tree clean`인지 본다.
- 폴더 이름은 소문자 `online`이다. 공개 주소에 그대로 들어간다.

### 2. 프로젝트와 표 만들기

Supabase 프로젝트를 만들고 [schema.sql](examples/schema.sql)을 SQL Editor에서 한 번 실행한다.
[따라하기 2~3단계](walkthrough.md#2-supabase-계정과-프로젝트-만들기)를 본다.

- **Database Password**는 메모만 하고 화면에 띄우지 않는다. 오늘 쓰지 않는 값이다.
- 힌트: 실행 결과 칸에 `guestbook_rows` = `0`이 나오면 성공이다.
- 힌트: Table Editor에 표가 안 보이면 왼쪽 위 프로젝트 이름이 내 것인지 먼저 본다.
- SQL을 두 번 실행해도 표와 글은 지워지지 않는다. 결과가 이상하면 다시 한 번 실행해도 된다.

### 3. 두 값 복사와 config.js

위쪽 **Connect** 버튼을 눌러 **Project URL**과 **publishable key**를 복사해 `online/config.js`를 만든다.
버튼이 없으면 키는 **Project Settings › API Keys**, 주소는 **Project Settings › Data API**에서 찾는다.
[따라하기 4~5단계](walkthrough.md#4-프로젝트-url과-publishable-key-복사하기)를 본다.

- 파일 이름은 `config.js`다. `config.example.js` 그대로 두면 페이지가 값을 찾지 못한다.
- 따옴표 안의 값만 바꾼다. 따옴표와 세미콜론은 지우지 않는다.
- `sb_secret_`로 시작하는 값, connection string, 데이터베이스 비밀번호는 복사하지 않는다.

### 4. 세 파일 push

`guestbook.html`·`guestbook.js`를 `online/`에 넣고 push한 뒤 공개 주소를 연다.
[따라하기 6~8단계](walkthrough.md#6-guestbookhtml-만들기)를 본다.

```text
https://student01.github.io/my-web/online/guestbook.html
```

- 화면에 폼과 `방명록 0개`가 보이면 연결이 된 것이다.
- 빨간 안내 문구가 보이면 아래 **막혔을 때**에서 그 문구를 찾는다.
- `<script>` 세 줄의 순서를 바꾸지 않는다.

### 5. 글 남기고 서버에서 확인

이름 `student01`, 메시지 `잘 봤습니다`를 넣고 **남기기**를 누른다.

- 목록에 한 줄이 생기고 안내 문구가 `방명록 1개`로 바뀐다.
- **F5**로 새로고침해도 남아 있다.
- Supabase **Table Editor**를 새로고침하면 같은 내용의 행이 보인다. 이 두 화면이 **제출 캡처**다.
- 이름이나 메시지를 비우고 눌러 `이름과 메시지를 모두 입력하세요.`가 나오는 것도 한 번 확인한다.

### 6. 다른 PC에서 확인하고 마무리

휴대폰이나 옆자리 PC에서 같은 주소를 연다. 방금 남긴 글이 그대로 보인다.

- 11주차 방명록은 다른 PC에서 비어 있었다. 오늘 글은 서버에 있어서 보인다. 이 차이가 오늘의 요점이다.
- 옆자리 학생이 내 주소에 글을 남길 수 있다. 정책이 "누구나 쓰기"이기 때문이다. 캡처는 내 글이 보일 때 찍는다.
- 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 새로고침. 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 Supabase에서도 로그아웃한다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 페이지가 옛 내용이다 | GitHub Pages 반영이 1~3분 늦는다. 5분 안에 안 보이면 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침하고, 그래도 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다 |
| 화면에 `불러오지 못했습니다: TypeError: Failed to fetch` | `config.js`의 `SUPABASE_URL`이 아직 `YOUR_PROJECT`이거나 주소에 오타가 있다. 또는 페이지를 `file://`로 열었다. 공개 주소로 연다 |
| 화면에 `불러오지 못했습니다: Invalid API key` | `SUPABASE_KEY` 한 줄을 다시 복사한다. `sb_publishable_`로 시작해야 한다 |
| 화면에 `Could not find the table 'public.guestbook' in the schema cache` | `schema.sql`을 실행하지 않았거나 다른 프로젝트에서 실행했다. Table Editor에 `guestbook` 표가 있는지 본다 |
| 화면에 `저장하지 못했습니다: new row violates row-level security policy for table "guestbook"` | 쓰기 정책이 없다. `schema.sql` 전체를 다시 한 번 실행한다 |
| Console에 `Uncaught ReferenceError: SUPABASE_URL is not defined` | `online/config.js`가 없거나 파일 이름이 `config.example.js`다. 이름을 `config.js`로 바꾼다 |
| Console에 `Uncaught ReferenceError: supabase is not defined` | `<head>`의 CDN `<script>` 한 줄이 빠졌다. 실습실에서 `cdn.jsdelivr.net`이 막힌 경우일 수도 있으니 강의자에게 알린다 |
| Console에 `Uncaught TypeError: Cannot read properties of null` | `guestbook.html`의 `id`와 `guestbook.js`의 `querySelector` 이름이 다르다. `#guestbook-form`·`#name`·`#message`·`#list`·`#notice` 다섯 개를 맞춘다 |
| 글은 저장되는데 목록이 늘지 않는다 | 저장 뒤 `showList()`를 부르는 줄이 있는지 본다. 새로고침하면 보이는 경우가 이것이다 |
| 공개 주소가 404 | 주소의 `online/`과 파일 이름 `guestbook.html`, 대소문자를 본다. `git push`가 끝났는지도 본다 |
| Supabase 대시보드가 프로젝트를 "paused"라고 한다 | 무료 프로젝트는 한동안 쓰지 않으면 일시정지된다. 대시보드에서 다시 켜고 1~2분 기다린다 |

한 번에 한 곳만 고치고 다시 확인한다. 해결되지 않으면 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://<아이디>.github.io/my-web/online/guestbook.html`에 방명록이 보이고,
옆에 Supabase **Table Editor**의 `guestbook` 표에 같은 행이 보이는 화면 한 장.

두 화면을 한 장에 담기 어려우면 두 장으로 나눠 찍어도 인정한다.
캡처에 이메일·실명·키 값이 보이지 않게 한다. 선택 특강이므로 주차별 실습 점수에는 넣지 않는다.

## 먼저 끝났다면

- `<head>`에 `<link rel="stylesheet" href="../styles.css">` 한 줄을 넣어 4주차 CSS를 입히고 push한다.
- `index.html`의 nav에 `online/guestbook.html` 링크를 더해 첫 페이지에서 갈 수 있게 한다.
- `select`의 `order('created_at', { ascending: false })`를 `true`로 바꿔 순서가 뒤집히는 것을 본다.
- Supabase **Table Editor**에서 행 하나를 직접 지우고 페이지를 새로고침한다. 목록에서도 사라진다.
- 페이지에서 글을 지우는 버튼은 만들 수 없다. 삭제 정책을 만들지 않았기 때문이다. 왜 그렇게 두었는지 한 문장으로 말해 본다.
