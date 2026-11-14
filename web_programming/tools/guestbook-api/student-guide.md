# 학생용 공용 방명록 API 사용 안내

강의자가 준비한 서버에 `fetch`로 글을 저장하고 읽는다. 학생은 Supabase 계정이나 SQL이 필요 없다.
먼저 01에서 API 접속을 확인하고 02에서 사용 안내를 읽는다. 이후 03 조회, 04 저장, 05 수정·삭제, 06 통합 실험 순서로 진행한다. 07에는 완성 방명록을 따로 제공한다.
정규 12주는 GET으로 목록을 읽고, 13주는 POST로 새 글을 저장한다. 화면은 학생이 만든 HTML·JavaScript가 담당한다.

강의자가 [about-help.sql](about-help.sql)을 공용 서버에 적용했으며 2026-11-14에 about·help GET 200과 응답 1행·6행을 확인했다.
로컬 01·02 브라우저 화면의 조회도 확인했다. 학생이 SQL을 실행할 필요는 없다.

## 1. 접속 주소와 설정

공용 API의 기본 주소는 다음과 같다. 뒤에 요청할 경로를 붙여 JSON 데이터를 주고받는다.

```text
https://esoqbcwgzjtwcqszwvin.supabase.co
```

예제 폴더의 `config.example.js`에서 아래 세 값을 설정한다. 공개 키는 강의자가 배부한 값으로 바꾼다.
`API_BASE_URL`에는 `/rest/v1/about` 같은 경로를 붙이지 않는다. 요청 코드가 뒤에 붙인다.

```js
const API_BASE_URL = 'https://esoqbcwgzjtwcqszwvin.supabase.co';
const API_PUBLIC_KEY = '강의자가_배부한_publishable_key';
const BOOK_ID = 'student01';
```

`BOOK_ID`는 글을 묶는 태그다. 강의자가 지정한 값을 사용한다.
2026-11-13에 등록을 확인한 태그는 `student01`, `student02`다. 등록되지 않은 태그로는 글을 저장할 수 없다.
조회·저장에는 위 공개 키만 필요하다. 학생 로그인이나 편집 키는 사용하지 않는다.

## 2. 접속 확인과 사용 안내

각 단계의 `requests.http`를 먼저 실행한다. VS Code의 REST Client 확장을 설치하고 해당 폴더에 `.env`가 없으면 `.env.example`을 복사한다.
`.env`에 배부받은 공개 키를 넣고 요청 위의 **Send Request**를 누른다. `.env`는 `.http`와 같은 폴더에 둔다.
이 요청에는 Node 정적 서버가 필요 없다. 성공한 요청을 확인한 뒤 같은 폴더의 `index.html`과 `app.js`로 이동한다.
브라우저는 `.env`를 읽지 않고 실행할 폴더 안의 `config.example.js`를 읽는다. 각 폴더의 설정은 독립적이다.

| 단계 | 요청 파일 | API 요청과 응답 |
|---|---|---|
| 01 접속 확인 | [01_about/requests.http](../../specials/supabase_guestbook/examples/01_about/requests.http) | `GET /rest/v1/about`: name·version·description·help_path를 가진 객체 하나의 배열 |
| 02 안내 조회 | [02_help/requests.http](../../specials/supabase_guestbook/examples/02_help/requests.http) | `GET /rest/v1/help?order=step.asc`: step·method·path·description 여섯 행의 배열 |

둘 다 `apikey` 헤더를 사용하며 GET 전용이다. `order=step.asc`는 단계 번호 순서로 정렬한다.
브라우저 코드에서는 다음처럼 접속을 확인한다. 02의 코드는 요청 경로를 help로 바꾸고 안내 목록을 표시한다.

```js
async function checkApi() {
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/about`, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const about = await response.json();
    console.log(about);
  } catch (error) {
    console.error('접속 확인 실패:', error.message);
  }
}

checkApi();
```

01·02는 글을 저장하거나 바꾸지 않는다. 404라면 강의자에게 안내 SQL 적용 여부를 확인한다.
요청 파일 사용법은 [REST Client 첫 실습](../../specials/supabase_guestbook/examples/README.md#rest-client로-요청부터-확인하기)에 있다.

## 3. 단계별 브라우저 예제 열기

[예제 목차](../../specials/supabase_guestbook/examples/README.md)에서 01부터 차례로 연다.
03·04는 방명록 요청을 하나씩 연습하고, 05·06은 앞 단계가 동작한 뒤 사용한다.

| 단계 | 요청 먼저 확인 | 브라우저 화면 |
|---|---|---|
| 03 조회 | [requests.http](../../specials/supabase_guestbook/examples/03_guestbook_get/requests.http) | [03_guestbook_get](../../specials/supabase_guestbook/examples/03_guestbook_get/index.html) |
| 04 저장 | [requests.http](../../specials/supabase_guestbook/examples/04_guestbook_post/requests.http) | [04_guestbook_post](../../specials/supabase_guestbook/examples/04_guestbook_post/index.html) |
| 05 수정·삭제 | [requests.http](../../specials/supabase_guestbook/examples/05_guestbook_edit/requests.http) | [05_guestbook_edit](../../specials/supabase_guestbook/examples/05_guestbook_edit/index.html) |
| 06 통합 실험 | [requests.http](../../specials/supabase_guestbook/examples/06_http_lab/requests.http) | [06_http_lab](../../specials/supabase_guestbook/examples/06_http_lab/index.html) |
| 07 완성 방명록 | [requests.http](../../specials/supabase_guestbook/examples/07_guestbook_complete/requests.http) | [07_guestbook_complete](../../specials/supabase_guestbook/examples/07_guestbook_complete/index.html) |

07은 등록 폼과 목록, 선택한 글의 수정·삭제를 한 화면에 모은 예제다. 요청 조건을 직접 바꾸는 실험은 06을 사용한다.

정규 주차의 완성 화면과 연결 코드는 다음 자료에서 확인한다.

- [12주 GET 완성 예제](../../weeks/week12_fetch_json/examples/day2/web-week12/guestbook.html): 목록 조회와 새로 불러오기
- [13주 POST 완성 예제](../../weeks/week13_release_security/examples/day2/web-week13/guestbook.html): 이름·메시지 입력과 서버 저장
- [12주 조회 코드](../../weeks/week12_fetch_json/examples/day2/web-week12/guestbook.js), [13주 저장 코드](../../weeks/week13_release_security/examples/day2/web-week13/submit.js)

예제는 HTML·CSS·JavaScript로 된 정적 화면이다. 공용 Supabase API를 설정한 화면이 GitHub Pages에 게시되어 있으면
강의자가 알려 준 HTTPS 화면 주소에 접속해 실습한다. 이 경우 Node.js 설치나 로컬 서버 실행은 필요 없다.

자신의 PC에서 파일을 수정하며 미리 볼 때는 저장소를 내려받고 Node.js 24 이상을 설치한다.
실행할 폴더의 브라우저용 설정을 확인하고 저장소 최상위 폴더의 터미널에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/specials/supabase_guestbook/examples 8000
```

브라우저에서 `http://localhost:8000/`을 열면 자동 폴더 목록이 나온다. 첫 단계는 `http://localhost:8000/01_about/`, 완성 방명록은 `http://localhost:8000/07_guestbook_complete/`이다.
`localhost:8000`은 각자 PC에서 실행한 화면 주소이고, 데이터는 위 Supabase HTTPS 주소에 저장된다.
다른 학생에게 `localhost` 주소를 보내도 내 PC 화면에 접속되지는 않는다. 각자 같은 예제를 실행한다.
정규 완성본을 열 때는 명령의 예제 폴더를 `web_programming/weeks/week13_release_security/examples/day2/web-week13` 또는 12주 폴더로 바꾸고 `/guestbook.html`을 연다.
실행 중인 서버를 `Ctrl+C`로 종료한 뒤 새 명령을 실행한다.

로컬의 HTTP 화면과 GitHub Pages의 HTTPS 화면은 모두 같은 Supabase HTTPS API를 사용한다. 로컬 페이지 주소는 HTTP로 유지되고 데이터 요청만 HTTPS를 쓴다.
GitHub Pages에 게시할 때는 공용 API 주소를 유지한다. `http://127.0.0.1:8787`은 내 PC의 모의 API 연습에만 쓴다.
공용 API를 사용하면 `tools/guestbook-api/server.mjs`를 실행할 필요가 없다.
특강 화면의 파일 구성과 게시 순서는 [GitHub Pages 사용 안내](../../specials/supabase_guestbook/examples/README.md#github-pages에서-사용하기)에 있다.
각 예제는 자체 HTML·JavaScript·설정·스타일을 가지므로 원하는 폴더 하나만 Pages에 게시할 수 있다.

## 4. GET으로 태그별 목록 읽기

```text
GET /rest/v1/guestbook?book_id=eq.student01&select=id,name,message,created_at&order=id.desc&limit=50
apikey: 강의자가 배부한 publishable key
```

| 요청 부분 | 뜻 |
|---|---|
| `/rest/v1/guestbook` | 방명록 테이블의 API 경로 |
| `book_id=eq.student01` | 태그가 `student01`과 같은 글만 선택. `eq.`는 같다는 뜻 |
| `select=id,name,message,created_at` | 응답에 포함할 열 선택. 생략하면 조회 가능한 모든 열 반환 |
| `order=id.desc` | 글 번호가 큰 순서로 정렬. 생략하면 순서를 보장하지 않음 |
| `limit=50` | 최대 50개 조회. 선택 사항 |
| `apikey` | 요청 헤더 이름. 값은 배부받은 공개 키 |

브라우저 주소창에는 `apikey` 헤더를 넣을 수 없으므로 주소만 열어서는 정상 조회되지 않는다.
아래는 요청 부분을 분리한 함수 예다. 위 설정을 먼저 읽은 JavaScript 파일에서 사용한다.
화면에 목록을 표시하는 코드는 12주 완성 예제에서 확인한다.

```js
async function readGuestbook() {
  try {
    const url = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`;
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const items = await response.json();
    console.log(items);
    return items;
  } catch (error) {
    console.error('목록 조회 실패:', error.message);
    return null;
  }
}

readGuestbook();
```

성공 응답은 `200`과 글 객체의 배열이다. 글이 없으면 `[]`이며, 오류가 아니다.

## 5. POST로 새 글 저장하기

POST 주소는 `/rest/v1/guestbook`이다. 태그는 URL 필터 대신 JSON 본문의 `book_id`에 넣는다.
`Content-Type`은 본문이 JSON임을 알리고, `Prefer: return=representation`은 저장된 글을 응답으로 요청한다.
`id`와 `created_at`은 서버가 만든다. 학생은 `book_id`, `name`, `message`만 보낸다.

```js
async function writeGuestbook(name, message) {
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook`, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify({ book_id: BOOK_ID, name: name, message: message })
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const saved = await response.json();
    console.log('저장된 글:', saved[0]);
    await readGuestbook();
    return saved;
  } catch (error) {
    console.error('저장 결과 확인 실패:', error.message);
    return null;
  }
}
```

예를 들어 저장 버튼의 이벤트 함수에서 `writeGuestbook('별칭', 'REST 저장 연습');`을 호출한다.
완성 예제는 폼의 제출 이벤트에서 입력값을 읽어 저장한다. 이름은 30자, 메시지는 500자까지이며 공백만 보낼 수 없다.
성공 응답은 `201`과 저장된 글 하나를 담은 배열이다. `saved[0].id`가 새 글 번호다.
같은 내용을 다시 POST하면 새 글이 하나 더 생긴다. 응답을 받지 못했을 때는 GET으로 먼저 저장 여부를 확인한다.

## 6. 두 화면에서 같은 데이터 확인하기

두 학생이 각자 예제를 실행하고 같은 `BOOK_ID`를 설정한다. 한 학생이 글을 저장한 뒤 다른 학생이 목록을 다시 조회한다.
두 번째 화면의 JavaScript가 GET을 보내면 같은 글을 확인할 수 있다. 다른 기기에서도 같은 방식으로 동작한다.
서버 저장만으로 다른 화면이 자동 갱신되지는 않는다. 이 예제는 버튼을 누르거나 저장한 뒤 GET을 다시 보낸다.

태그는 조회 필터이며 접근 권한을 나누지 않는다. 다른 등록 태그의 글도 읽거나 새로 쓸 수 있다.
수업용 공개 데이터이므로 이름에는 별칭을 쓰고 메시지에 개인정보를 넣지 않는다.
오류가 나면 개발자 도구의 Network에서 요청 주소·상태 번호·응답을 확인한다. 공개 키, 등록된 태그, 입력 길이를 먼저 점검한다.

## 7. 수정·삭제와 API 문법 자료

14주 PATCH·DELETE에는 강의자가 별도 배부하는 해당 방명록의 편집 키가 필요하다.
편집 키를 공개 설정 파일에 넣지 않는다. 요청 형식은 [공용 API 요청과 응답](README.md#요청과-응답)을 따른다.
05~07의 `.http` 요청은 자신이 만든 글 ID와 편집 키를 전송 시 입력 창에서 받는다. 편집 키 입력은 마스킹된다.
후속 GET에서도 방금 변경 요청한 글 ID를 입력해 같은 대상을 확인한다.
REST Client 요청 이력에는 헤더·본문이 남는다. 키가 든 이력·전체 요청 캡처는 공유하지 않고 실습 후 **Rest Client: Clear Request History**를 실행한다.
REST Client 성공과 브라우저 CORS 성공은 별도로 확인한다. `.env`는 Git·Pages 게시 파일에 포함하지 않는다.

- [Supabase Data REST API](https://supabase.com/docs/guides/api): 데이터베이스에서 생성되는 REST API와 접속 주소 설명
- [PostgREST 14 Tables and Views](https://docs.postgrest.org/en/v14/references/api/tables_views.html): `eq`, `select`, `order`, `limit`, GET·POST 요청 문법
- [VS Code REST Client](https://github.com/Huachao/vscode-restclient#usage): `.http` 요청 실행과 응답 확인

수업에서는 별도 SDK 없이 `fetch`를 쓴다. 공식 문서의 요청 경로·헤더·본문을 위 예제와 비교한다.
