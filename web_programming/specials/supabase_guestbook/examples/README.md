# 특강 예제 — 서버에 저장하는 방명록

네 파일이 전부다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 위치 |
|---|---|---|
| [schema.sql](schema.sql) | [3단계](../walkthrough.md#3-sql-editor에서-표와-정책-만들기) — SQL Editor에 붙여 넣고 한 번 실행한다. 저장소에 넣지 않아도 된다 | (저장소 밖. Supabase 대시보드에서 실행) |
| [config.example.js](config.example.js) | [5단계](../walkthrough.md#5-configjs-만들기) — 복사해 `config.js`로 만들고 두 줄의 값만 바꾼다 | `online/config.js` |
| [guestbook.html](guestbook.html) | [6단계](../walkthrough.md#6-guestbookhtml-만들기) | `online/guestbook.html` |
| [guestbook.js](guestbook.js) | [7단계](../walkthrough.md#7-guestbookjs-만들기) | `online/guestbook.js` |

11주차까지 만든 `my-web/guestbook.html`은 손대지 않는다. 새 폴더 `online/`에 세 파일을 넣는다.

## 1. schema.sql — 표 하나와 정책 두 개

여섯 블록이다. 위에서부터 읽으면 이렇게 된다.

| 블록 | 하는 일 |
|---|---|
| 1 | `guestbook` 표를 만든다. 칸은 `id`·`name`·`message`·`created_at` 네 개 |
| 2 | 표를 잠근다(`enable row level security`) |
| 3 | 로그인하지 않은 방문자에게 읽기·쓰기 **명령**을 허용한다 |
| 4 | 읽기 정책: 모든 글을 읽을 수 있다 |
| 5 | 쓰기 정책: 새 글을 넣을 수 있다 |
| 6 | 지금 글이 몇 개인지 센다 |

수정·삭제 정책은 만들지 않았다. 그래서 누가 시도해도 되지 않는다.
`id`와 `created_at`은 서버가 넣어 주므로 페이지에서 적지 않는다.

## 2. config.example.js — 바꾸는 값 두 개

```js
const SUPABASE_URL = 'https://YOUR_PROJECT.supabase.co';
const SUPABASE_KEY = 'sb_publishable_YOUR_KEY';
```

두 값은 대시보드 위쪽의 **Connect** 버튼에서 함께 복사한다(버튼이 없으면 키는 **Project Settings › API Keys**, 주소는 **Project Settings › Data API**). 둘 다 공개해도 되는 값이라 GitHub에 올린다.
`sb_secret_`로 시작하는 키와 데이터베이스 비밀번호는 이 파일에 넣지 않는다.

## 3. guestbook.html — 폼 하나와 목록 하나

`<head>`의 `<script>` 세 줄 순서가 중요하다.

```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="config.js" defer></script>
<script src="guestbook.js" defer></script>
```

- 첫 줄은 Supabase가 공개해 둔 파일이다. 이 줄이 있어야 `supabase.createClient`를 쓸 수 있다. 특강에서만 쓰는 예외이며, 정규 주차 예제에는 외부 파일을 넣지 않는다.
- `config.js`가 `guestbook.js`보다 먼저 있어야 한다.
- 화면 요소는 `#guestbook-form`·`#name`·`#message`·`#list`·`#notice` 다섯 개다.
- 꾸미고 싶으면 `<head>`에 `<link rel="stylesheet" href="../styles.css">` 한 줄을 더해 4주차 CSS를 쓴다.

## 4. guestbook.js — 불러오기와 저장하기

```js
const client = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
```

| 부분 | 하는 일 |
|---|---|
| `showList()` | `select`로 글을 받아 `for`로 `li`를 만들어 붙인다. 10·11주차와 같은 모양이다 |
| `form`의 `submit` | 빈 값을 막고 `insert`로 한 줄을 보낸 뒤 `showList()`를 다시 부른다 |
| `result.error` | 실패하면 `#notice`에 이유를 적고 멈춘다 |
| 맨 아랫줄 `showList()` | 페이지를 열 때 목록을 한 번 불러온다 |

실행 결과는 이렇다.

```text
방명록 2개
student01: 잘 봤습니다 (2026. 9. 16.)
student02: 반갑습니다 (2026. 9. 16.)
```

`config.js`를 만들지 않고 열면 화면이 `불러오는 중…`에서 멈추고 Console에 빨간 줄이 하나 보인다.
그 문구와 조치는 [실습지의 막혔을 때](../lab.md#막혔을-때)에 있다.

## 공식 참고 자료

- [Supabase — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Supabase — API keys](https://supabase.com/docs/guides/api/api-keys)
- [Supabase — select](https://supabase.com/docs/reference/javascript/select) · [insert](https://supabase.com/docs/reference/javascript/insert)
