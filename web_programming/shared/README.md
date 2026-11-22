# 웹 실습 공용 설정

## W3.CSS

[7주 CSS 응용](../weeks/week07_form_input/README.md)에서 아래 CDN을 연결한다. 입력창은 `w3-input`, 버튼은 `w3-button`, 긴 응답을 스크롤할 영역은 `w3-responsive`를 사용한다.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
```

## 정규 REST 예제의 설정

수업용 방명록 API를 부르는 정규 예제는 폴더마다 `config.example.js`를 둔다. 이 파일이 `API_BASE_URL`(수업용 Supabase 주소), `API_PUBLIC_KEY`, `BOOK_ID` 세 값을 정하고, HTML은 이 파일을 동작 JS보다 먼저 `defer`로 읽는다. 12주 필수 예제는 키 없이 공개 API에 직접 접속하므로 이 파일을 쓰지 않는다.

정본은 [12주 선택 방명록의 config.example.js](../weeks/week12_fetch_json/examples/day2/web-week12/config.example.js)다. 방명록 API를 부르는 13·14주 예제, 15주 REST 문항, hash SPA 특강 04는 정본을 그대로 복사해 두고, 사본의 `git hash-object` 값은 정본과 같아야 한다. 정본을 고치면 같은 작업에서 사본 전부를 고친다. 확인 명령은 [작업 지침의 검증 절](../AGENTS.md#검증)에 있다. 14주 `day1/ex01`의 `config.example.js`는 서버를 부르지 않는 예제의 안내 주석이라 사본이 아니다.

학생은 자기 저장소에 복사한 파일에서 `BOOK_ID`만 배정받은 방명록 번호로 바꾼다. 바꾸지 않으면 `student01` 방명록을 읽고 그곳에 글을 저장한다.

```js
const BOOK_ID = 'student01';
```

공개 키는 파일에 적지 않는다. localStorage에 키가 없으면 `config.example.js`가 처음 열 때 ‘배부받은 공개 키를 입력하세요.’라고 묻는 창을 띄운다. 학생이 강의자가 배부한 공개 키를 넣고 확인을 누르면 앞뒤 공백을 지운 값이 localStorage의 `API_PUBLIC_KEY`에 저장된다. 새로고침해도 저장한 키와 서버에 남긴 글이 그대로 있다. 취소를 누르거나 빈 칸으로 확인하면 저장하지 않으므로 서버가 HTTP 401을 돌려주고 화면에 조회·저장 실패가 보인다. 새로고침하면 다시 묻는다.

localStorage는 화면 주소의 출처(프로토콜·호스트·포트)마다 따로 저장된다. 같은 출처에서 연 다른 예제는 저장한 키를 함께 쓰고 다시 묻지 않는다. 다른 브라우저, 포트가 다른 `localhost`, GitHub Pages 주소, 휴대폰에서는 처음 열 때 한 번 묻는다.

각 화면의 제목 아래에는 **공개 키 지우기** 버튼(`id="key-clear-button"`)을 두고, 동작은 `config.example.js`가 붙인다. 버튼을 누르면 저장한 키를 지우고 새로고침해 다시 묻는다. 키를 잘못 넣었거나 학기가 바뀌어 강의자가 키를 바꾸면 이 버튼을 누르고 새 키를 넣는다. 휴대폰에서도 같다. 키를 바꿔도 저장소의 사본은 고치지 않는다.

강의자가 로컬 모의 API로 리허설할 때는 `config.example.js`의 주소를 `http://127.0.0.1:8787`로 바꾸고, **공개 키 지우기**를 누른 뒤 `classroom-local`을 넣는다. 리허설이 끝나면 주소를 되돌리고 **공개 키 지우기**를 누른 뒤 배부받은 공개 키를 넣는다.

14주 편집 키는 localStorage에도 파일에도 두지 않는다. 화면의 입력칸으로 받아 메모리에서만 쓴다.

VS Code REST Client의 `requests.http`는 같은 폴더의 `.env`에서 주소·공개 키·방명록 번호를 읽는다. 브라우저는 `.env`를 읽지 않는다. 실제 `.env`는 Git에서 제외한다.
