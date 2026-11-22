# 선택 예제 · 수업 방명록에서 글 읽기

도시별 날씨 실습을 마친 뒤 같은 GET으로 방명록의 글을 읽어 볼 수 있다. 13주에는 이 조회 함수가 포함된 시작 코드를 제공한다.

## 브라우저

1. [config.example.js](config.example.js)에서 `BOOK_ID`의 `student01`을 배정받은 방명록 번호로 바꾼다. 주소는 수업용 Supabase 서버로 채워져 있다.

   ```js
   const BOOK_ID = 'student01';
   ```

2. [방명록](guestbook.html)을 처음 열면 ‘배부받은 공개 키를 입력하세요.’라고 묻는 창이 뜬다. 강의자가 배부한 공개 키를 넣고 확인을 누른다. 키는 이 브라우저의 localStorage에 저장되고, 같은 주소(출처)에서 여는 다른 예제도 이 키를 함께 쓴다. 다음부터는 묻지 않는다.

3. 페이지가 열리면 첫 GET을 보내 서버가 돌려준 최근 글을 최대 50개까지 표시한다. 글이 없으면 빈 목록도 정상이다. **새로 불러오기**는 같은 GET을 다시 보낸다. 새로고침해도 공개 키를 다시 넣지 않고 같은 서버 글을 읽는다.

localStorage는 화면 주소(출처)마다 따로 저장된다. 다른 브라우저, 포트가 다른 `localhost`, GitHub Pages 주소, 휴대폰에서는 처음 열 때 한 번 묻는다.

창에서 취소를 누르거나 빈 칸으로 확인하면 키를 저장하지 않는다. 이때 GET은 HTTP 401로 실패해 조회 실패가 보이고, 새로고침하면 다시 묻는다. 키를 잘못 넣었거나 학기가 바뀌어 키가 바뀌면 제목 아래의 **공개 키 지우기**를 누르고 새 키를 넣는다. 휴대폰에서도 같다. `BOOK_ID`를 바꾸지 않으면 `student01` 방명록의 글을 읽는다.

## VS Code REST Client

1. VS Code에 REST Client(`humao.rest-client`)를 설치한다. 이 폴더의 `.env.example`을 `.env`로 복사한다.
2. `API_BASE_URL`에 수업 주소가 있는지 확인하고, `API_PUBLIC_KEY`에 배부받은 공개 키, `BOOK_ID`에 내 방명록 번호를 입력한다.
3. [requests.http](requests.http)의 **Send Request**를 접속 확인 → 도움말 → 자기 목록 순서로 누른다. 앞의 두 응답은 API 정보와 사용법을 담은 JSON 배열이다. 목록 요청은 `200 OK`와 방명록 글 배열을 반환한다.

모든 요청의 `apikey` 헤더는 REST Client가 `.env`에서 읽는다. 401이면 키를, 404이면 기본 URL과 경로를 확인한다. 브라우저는 `.env`를 읽지 않고 `config.example.js`와 localStorage에 저장한 공개 키를 사용한다. 실제 `.env`는 Git과 제출 파일에서 제외한다.

## 파일

[config.example.js](config.example.js)는 주소와 방명록 번호를 정하고, 공개 키를 묻거나 저장된 키를 읽으며, **공개 키 지우기** 버튼의 동작을 붙인다. 이 파일은 `guestbook.js`보다 먼저 읽힌다. 13주 이후 방명록 예제는 이 파일을 그대로 복사해 쓴다([공용 설정 안내](../../../../../shared/README.md)). [guestbook.js](guestbook.js)의 `loadMessages()`가 서버 목록을 읽고 `showList(items)`가 글을 화면에 표시한다. 홈·내 정보는 기존 페이지를 이어 쓴다. [11주 로컬 저장본](guestbook.local.html)은 같은 브라우저의 localStorage를 사용한다.
