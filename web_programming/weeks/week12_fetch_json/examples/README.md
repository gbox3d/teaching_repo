# 12주차 예제 · about → help → GET

[따라하기](../walkthrough.md)에서 서버를 실행한다. 각 폴더는 HTML·동작 JS·제공 `api-settings.js`·README·`requests.http`·`.env.example`·`.gitignore`를 포함한다. 폴더 전체를 복사하면 독립 실행할 수 있다. 공용 설정을 소스에 쓰지 않고 브라우저 패널 또는 별도 `.env`에서 입력한다.

| 예제 | 실행 화면 | 수업 역할 |
|---|---|---|
| [ex01 안내](day1/ex01/README.md) · [화면](day1/ex01/index.html) | about 200과 정보 배열 | 필수 접속 확인 |
| [ex02 안내](day1/ex02/README.md) · [화면](day1/ex02/index.html) | help 200과 사용법 배열 | 필수 도움말 확인 |
| [ex03 안내](day1/ex03/README.md) · [화면](day1/ex03/index.html) | GET 200과 자기 글 배열 | BOOK_ID·limit 비교 |
| [ex04 안내](day2/ex04/README.md) · [화면](day2/ex04/index.html) | 응답 배열을 목록으로 표시 | 강의 시연·조립 재사용 |
| [ex05 안내](day2/ex05/README.md) · [화면](day2/ex05/index.html) | 정상 200·없는 필드 오류 400 | 오류 비교 실습 |
| [ex06 안내](day2/ex06/README.md) · [화면](day2/ex06/index.html) | Offline 실패와 복구 | 재시도 실습 |
| [완성본 안내](day2/web-week12/README.md) · [방명록](day2/web-week12/guestbook.html) | 서버 글 목록과 새로 불러오기 | 제공 틀의 3곳 수정 |

JSON 단독 비교는 [11주 ex05](../../week11_object_localstorage/examples/day2/ex05/)로 연결한다. 11주 필수 폼 저장과 제공 객체 배열 방명록을 구분한다. 완성본의 `guestbook.local.html`·`guestbook.local.js`는 제공 로컬 저장본이며 서버 글과 자동으로 합치지 않는다.

## 파일 인계

| 파일 | 역할 |
|---|---|
| `api-settings.js` | 메모리 설정·제공 폼 연결. 공통 정본의 폴더별 사본 |
| `guestbook.js` | GET·showList·실패 안내·버튼 복구 |
| `guestbook.html` | 기존 메뉴·서버 목록·설정 패널 |
| `guestbook.local.html/js` | 11주 로컬 저장본 보존 |
| `requests.http`·`.env.example` | REST Client 접속→도움말→목록 요청 |

모든 요청 위 **Send Request**로 실행한다. `apikey` 헤더는 `.env`의 공개 키를 읽는다. about·help·GET 모두 200과 JSON 배열을 기대하고 `[]`도 정상이다. 브라우저 패널은 `.env`와 별개이며 새로고침 후 재입력한다.

W3.CSS 4.1.0은 `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`를 쓴다. 예제의 추가 스타일은 각 폴더 `shared/examples.css`의 배포 사본이며 원본은 `web_programming/shared/examples.css`다. 홈·내 정보는 기존 `styles.css`를 유지한다. 실제 `.env`는 Git·ZIP에서 제외한다.
