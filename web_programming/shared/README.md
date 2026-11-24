# 웹 실습 공용 설정

## W3.CSS

[7주 CSS 응용](../weeks/week07_form_input/README.md)에서 아래 CDN을 연결한다. 입력창은 `w3-input`, 버튼은 `w3-button`, 긴 응답을 스크롤할 영역은 `w3-responsive`를 사용한다.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
```

## 13주 방명록의 JSON 설정

예제 폴더의 `config.example.json`을 같은 폴더의 `config.json`으로 복사한다. `API_BASE_URL`에 수업 API 주소, `API_PUBLIC_KEY`에 배부받은 publishable key, `BOOK_ID`에 배정받은 방명록 번호를 넣는다. `load-config.js`가 이 파일을 읽으면 예제의 버튼을 사용할 수 있다.

브라우저에서 JSON을 직접 열 수 있으므로 공개 키만 사용한다. 실제 `config.json`은 Git과 교재 사이트 배포에서 제외한다. 설정을 준비한 뒤 로컬 정적 서버에서 예제를 연다. [13주 따라하기](../weeks/week13_guestbook_crud/walkthrough.md)

## 12주 선택 방명록·14주 이후의 설정

12주 선택 방명록, 14·15주 REST 예제와 hash SPA 특강 04는 폴더마다 `config.example.js`를 둔다. HTML은 이 파일을 동작 JS보다 먼저 `defer`로 읽는다.

정본은 [12주 선택 방명록의 config.example.js](../weeks/week12_fetch_json/examples/day2/web-week12/config.example.js)다. 14주 예제, 15주 REST 문항과 hash SPA 특강 04의 사본은 `git hash-object` 값이 정본과 같아야 한다. 14주 `day1/ex01`에는 안내 주석만 있다. [작업 지침의 검증 절](../AGENTS.md#검증)

학생은 자기 저장소에 복사한 파일에서 `BOOK_ID`만 배정받은 방명록 번호로 바꾼다. 바꾸지 않으면 `student01` 방명록을 읽고 그곳에 글을 저장한다.

```js
const BOOK_ID = 'student01';
```

공개 키는 파일에 적지 않는다. localStorage에 키가 없으면 `config.example.js`가 처음 열 때 ‘배부받은 공개 키를 입력하세요.’라고 묻는 창을 띄운다. 학생이 강의자가 배부한 공개 키를 넣고 확인을 누르면 앞뒤 공백을 지운 값이 localStorage의 `API_PUBLIC_KEY`에 저장된다. 새로고침해도 저장한 키와 서버에 남긴 글이 그대로 있다. 취소를 누르거나 빈 칸으로 확인하면 저장하지 않으므로 서버가 HTTP 401을 돌려주고 화면에 조회·저장 실패가 보인다. 새로고침하면 다시 묻는다.

localStorage는 화면 주소의 출처(프로토콜·호스트·포트)마다 따로 저장된다. 같은 출처에서 연 다른 예제는 저장한 키를 함께 쓰고 다시 묻지 않는다. 다른 브라우저, 포트가 다른 `localhost`, GitHub Pages 주소, 휴대폰에서는 처음 열 때 한 번 묻는다.

각 화면의 제목 아래에는 **공개 키 지우기** 버튼(`id="key-clear-button"`)을 두고, 동작은 `config.example.js`가 붙인다. 버튼을 누르면 저장한 키를 지우고 새로고침해 다시 묻는다. 키를 잘못 넣었거나 학기가 바뀌어 강의자가 키를 바꾸면 이 버튼을 누르고 새 키를 넣는다. 휴대폰에서도 같다. 키를 바꿔도 저장소의 사본은 고치지 않는다.

강의자가 로컬 모의 API로 리허설할 때 13주는 `config.json`에서 주소를 `http://127.0.0.1:8787`, 키를 `classroom-local`로 바꾼다. `config.example.js`를 쓰는 예제에서는 주소를 바꾸고 **공개 키 지우기**를 누른 뒤 `classroom-local`을 넣는다. 리허설 뒤 두 값을 수업용 주소와 공개 키로 되돌린다.

학생은 자기 `BOOK_ID`로 글을 모아 본다. 수업용 공개 키로 모든 태그의 글을 수정·삭제할 수 있으므로 실습에는 자기 태그를 쓴다.

VS Code REST Client의 `requests.http`는 같은 폴더의 `.env`에서 주소·공개 키·방명록 번호를 읽는다. 브라우저는 `.env`를 읽지 않는다. 실제 `.env`는 Git에서 제외한다.
