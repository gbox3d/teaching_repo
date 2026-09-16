# 특강 — Supabase로 만드는 서버 방명록

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/supabase_guestbook

## 이 특강의 질문

> 방명록에 남긴 글을 인터넷 서버에 저장해 다른 PC에서도 보이게 할 수 있을까?

11주차까지 `my-web`의 방명록은 `localStorage`에 글을 저장했다. 내 PC에서는 새로고침해도 남지만, 다른 PC에서 같은 주소를 열면 목록이 비어 있다.
이번 특강에서는 Supabase에 표(table) 하나를 만들고, 같은 방명록을 **서버에 저장하고 불러오는** 페이지를 `my-web/online/`에 새로 추가한다.

정규 15주 수업 밖의 **선택 특강**이며 1회 110분이다. 주차별 실습 점수와 시험에는 들어가지 않는다.

## 대상과 전제

- 11주차(객체·`localStorage`)까지 마친 학생
- 공개된 `my-web` 저장소와 `https://<아이디>.github.io/my-web/` 주소가 이미 있다
- 11주차까지 만든 `guestbook.html`은 그대로 두고, 새 폴더 `online/`에 새 페이지를 만든다
- 로그인·회원가입은 만들지 않는다. 누구나 읽고 쓰는 방명록 하나만 만든다

## 학습 목표

1. 브라우저 저장소(`localStorage`)와 인터넷 서버 데이터베이스의 차이를 한 문장으로 말한다.
2. Supabase 프로젝트를 만들고 제공 SQL(`schema.sql`)을 SQL Editor에서 **한 번** 실행해 표와 정책을 만든다.
3. 공개해도 되는 publishable key와 적으면 안 되는 secret key·데이터베이스 비밀번호를 구분한다.
4. `config.js`의 두 줄만 바꿔 브라우저에서 Supabase에 연결한다.
5. 글을 서버에 저장하고(`insert`) 목록을 불러와(`select`) 화면에 그린다.
6. 다른 PC나 휴대폰에서 같은 공개 주소를 열어 같은 목록이 보이는 것을 확인한다.

## 이번 특강 결과물

```text
[캡처 1장] https://student01.github.io/my-web/online/guestbook.html
           방명록 3개가 보이고, 옆에 Supabase Table Editor의 guestbook 표에
           같은 3행이 보이는 화면
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 110분 흐름

| 시간 | 내용 | 결과 |
|---|---|---|
| 1부 설명·시연 25분 | 글이 저장되는 두 곳, 프로젝트 만들기, `schema.sql` 한 번 실행, publishable key 복사 | 내 프로젝트에 `guestbook` 표가 생긴다 |
| 2부 설명·시연 25분 | `config.js` 두 줄, 불러오기 `select`, 저장하기 `insert`, 오류 문구 보여 주기 | 코드가 어디서 무엇을 하는지 읽을 수 있다 |
| 실습 60분 | [실습지](lab.md#실습-60분)의 여섯 단계 | 공개 주소에서 방명록 저장·불러오기, 캡처 1장 |

## 준비

- `my-web` 저장소(11주차까지의 내용)와 공개 주소. 다른 PC면 `git clone`, 같은 PC면 `git pull`부터 한다
- 확인 메일을 받을 수 있는 이메일 주소 하나 (Supabase 가입용)
- Chrome(DevTools)과 VS Code
- 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 방명록에 적는 이름도 `student01` 같은 별칭으로 쓴다

## 이번 특강 용어

| 한국어 | English | 中文 |
|---|---|---|
| 서버 데이터베이스 | server database | 服务器数据库 |
| 표 | table | 数据表 |
| 행 | row | 行 |
| 공개 키 | publishable key | 可公开密钥 |
| 비밀 키 | secret key | 私密密钥 |
| 행 수준 보안 | Row Level Security (RLS) | 行级安全 |
| 정책 | policy | 策略 |
| 불러오기 / 저장하기 | select / insert | 查询 / 插入 |

## 이번 특강 범위

| 이름 | 이번 특강에서 알아둘 뜻 |
|---|---|
| Supabase | 인터넷에 데이터베이스와 그 데이터를 읽고 쓰는 주소를 만들어 주는 서비스 |
| project | Supabase에서 만드는 내 작업 공간 하나. 주소 `https://<프로젝트>.supabase.co`가 붙는다 |
| SQL Editor | 대시보드에서 SQL을 붙여 넣고 **Run**으로 실행하는 화면 |
| Table Editor | 만들어진 표와 행을 눈으로 보는 화면 |
| `schema.sql` | 표·잠금·정책을 한 번에 만드는 제공 SQL. 수업에서는 붙여 넣고 한 번 실행한다 |
| Row Level Security | 표를 잠그는 기능. 켜면 정책으로 허용한 것만 된다 |
| policy | "누가 어떤 명령을 할 수 있는가"를 적은 규칙. 이번에는 읽기·쓰기 두 개 |
| publishable key | 브라우저에 두어도 되는 공개 키. `sb_publishable_`로 시작한다 |
| secret key | 서버에서만 쓰는 비밀 키. 브라우저·저장소·캡처에 넣지 않는다 |
| `client.from('guestbook').select(...)` | 표에서 글을 불러온다 |
| `client.from('guestbook').insert({ ... })` | 표에 글 한 줄을 넣는다 |
| `async` / `await` | `await`는 인터넷에서 답이 올 때까지 기다린다는 표시다. 함수 앞의 `async`는 그 안에서 `await`를 쓰겠다는 표시이고, 두 단어는 항상 짝으로 붙인다. 오늘은 틀로만 쓴다(정규 수업은 12주차) |

로그인(Auth), 사용자별 소유자 권한, 수정·삭제, 관계 있는 두 표는 이번 특강에서 다루지 않는다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/supabase_guestbook/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 예제 파일: [config.example.js](examples/config.example.js) · [schema.sql](examples/schema.sql) · [guestbook.html](examples/guestbook.html) · [guestbook.js](examples/guestbook.js)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/supabase_guestbook

## 안전 규칙

- 브라우저와 저장소에는 **프로젝트 URL과 publishable key만** 둔다. 이 두 값은 공개되어도 되는 값이다.
- secret key(`sb_secret_`로 시작), 데이터베이스 비밀번호, connection string은 어디에도 붙여 넣지 않는다. 화면 공유·캡처에도 나오지 않게 한다.
- 데이터베이스 비밀번호는 프로젝트를 만들 때 한 번 정하고, 메모해 두되 수업 화면에 띄우지 않는다.
- 회원가입·로그인 기능을 만들지 않으므로 실제 계정의 이메일·비밀번호를 입력하는 칸이 없다.
- 방명록은 누구나 읽고 쓸 수 있다. 실명·학번·전화번호·실제 이메일을 적지 않는다.
- 남의 프로젝트에 SQL을 실행하지 않는다. 내 프로젝트 이름을 먼저 확인한다.

## 완료 기준

- [ ] 내 Supabase 프로젝트의 Table Editor에 `guestbook` 표가 있다.
- [ ] `my-web/online/`에 `guestbook.html`·`guestbook.js`·`config.js`가 있고 push되어 있다.
- [ ] 공개 주소 `https://<아이디>.github.io/my-web/online/guestbook.html`에서 이름·메시지를 남기면 목록에 바로 보인다.
- [ ] 다른 PC(또는 휴대폰)에서 같은 주소를 열어도 같은 목록이 보인다.
- [ ] 캡처 1장을 제출한다.

## 특강이 끝나면

- 무료 프로젝트는 일정 기간 쓰지 않으면 일시정지된다. 나중에 다시 열 때 대시보드에서 다시 켜야 할 수 있다.
- 방명록 페이지를 더 두고 싶지 않으면 `online/` 폴더를 지우고 push한다. 11주차까지의 `guestbook.html`은 그대로 남는다.
- 정규 수업의 방명록(`localStorage`)과 이 특강의 방명록(서버)은 서로 다른 페이지다. 14주 최종 과제는 정규 수업 쪽으로 제출한다.

## 공식 참고 자료

- [Supabase — Getting started](https://supabase.com/docs/guides/getting-started)
- [Supabase — API keys](https://supabase.com/docs/guides/api/api-keys)
- [Supabase — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Supabase — JavaScript client: select](https://supabase.com/docs/reference/javascript/select)
- [Supabase — JavaScript client: insert](https://supabase.com/docs/reference/javascript/insert)
- [MDN — async function](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/async_function)
