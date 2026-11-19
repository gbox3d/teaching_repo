[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_fetch_json)

# 12주차 · REST API로 방명록 읽기

11주 필수 결과는 ex06의 폼 한 객체 저장·복원이다. 객체 배열을 저장하는 방명록은 강의자가 제공한 시연본이다. 이번 주에는 그 제공본의 홈·내 정보와 목록 자리를 이어 쓰고, 서버에 about → help → GET 요청을 보낸다. JSON 단독 복습은 [11주 ex05](../week11_object_localstorage/examples/day2/ex05/)를 사용한다.

## 학습 목표와 결과물

URL·GET·apikey 헤더·응답 본문을 구분하고 async/await로 응답과 JSON 본문을 기다린다. 서버 배열을 `for`·`createElement`·`textContent`로 표시하고 HTTP 오류와 통신 오류에서 다시 조회한다. 최종 결과는 서버 목록과 Network의 GET 200이 함께 보이는 캡처다.

## 양일 60분 강의·30분 실습

| 차시 | 강의·시연 60분 | 학생 실습 30분 |
|---|---|---|
| 12-1 | 준비 5, URL·헤더 10, REST Client about·help 15, JSON 복습 10, GET·await 15, 안내 5 | 설정 입력 5, about·help Send Request 8, GET의 BOOK_ID·limit 변경 10, 응답 확인 7 |
| 12-2 | 준비 5, 응답→showList 15, response.ok 15, try/catch 10, 재시도·조립 10, 안내 5 | 제공 fetch 틀의 URL·JSON·showList 3곳 12, Offline·HTTP 오류와 복구 10, 목록·Network 캡처 8 |

파일 배부·새 작업 저장소·정적 서버 준비는 수업 전에 끝낸다. 첫 5분에 실행 상태를 확인한다. GitHub 업로드는 수업 뒤 정리로 진행하며 30분 실습에 포함하지 않는다.

## 예제와 필수 범위

| 예제 | 역할 | 학생 활동 |
|---|---|---|
| [ex01](examples/day1/ex01/README.md) | about 접속 확인 | Send Request와 200 정보 배열 확인 |
| [ex02](examples/day1/ex02/README.md) | help 사용법 확인 | 단계·메서드·경로 읽기 |
| [ex03](examples/day1/ex03/README.md) | 자기 목록 GET | BOOK_ID와 limit 1·2·5 비교 |
| [ex04](examples/day2/ex04/README.md) | 배열→목록 | 제공 코드의 URL·JSON·showList 연결 이해 |
| [ex05](examples/day2/ex05/README.md) | HTTP 오류 | 없는 필드 오류 400와 정상 200 비교 |
| [ex06](examples/day2/ex06/README.md) | 통신 오류·재시도 | Offline 실패 후 복구 |
| [web-week12](examples/day2/web-week12/README.md) | 제공 틀 조립 | URL·JSON·showList 3곳 수정 및 캡처 |

오류 처리 틀과 API 설정 패널은 제공 코드다. 패널 재작성, 날짜 표시, 서버 글 쓰기, 로컬 글 자동 이관은 필수가 아니다. id 표시와 limit 추가 실험은 선택이다.

## 실행 설정과 데이터 인계

[따라하기](walkthrough.md)에서 로컬 API와 정적 서버를 실행한다. 기본 API 주소는 `http://127.0.0.1:8787`, 가상 공개 키는 `classroom-local`, 방명록 번호는 `student01`이다. `api-settings.js`는 제공 파일이며 실제 공용 값을 적지 않는다. 화면의 API 설정 패널에 배부받은 공용 HTTPS 주소·공개 키·번호를 입력하고 적용한다. 설정은 메모리에만 있으며 새로고침 후 다시 입력한다.

REST Client(`humao.rest-client`)는 폴더의 `.env.example`을 `.env`로 복사해 별도로 설정한다. 요청 위 **Send Request**를 about → help → GET 순으로 누른다. 모든 요청은 `apikey` 헤더를 쓰고, 각각 200·API 정보 배열, 200·사용법 배열, 200·글 배열을 기대한다. 브라우저 패널은 `.env`를 읽지 않는다. `.env`와 실제 키는 Git·ZIP에 넣지 않는다.

11주 제공본은 `guestbook.local.html`·`guestbook.local.js`로 보관한다. 원래 저장 키를 유지하므로 같은 origin에서 기존 글을 확인할 수 있다. 다른 origin으로 옮기면 저장 공간이 달라진다. `guestbook.html`은 서버 읽기 화면이며 로컬 글을 옮기거나 삭제하지 않는다. 홈·내 정보와 메뉴의 방명록 링크는 서버 화면을 가리킨다.

## 확인과 제출

- about·help·자기 목록 요청의 200과 배열을 확인한다. 빈 목록 `[]`도 정상이다.
- 새로 불러오기를 반복해도 글이 중복되지 않는다. 오류가 나면 실패 안내와 다시 활성화된 버튼을 확인한다.
- Offline에서 No throttling으로 복구하고 다시 조회한다. 375px와 넓은 화면에서 목록과 메뉴를 확인한다.
- 서버 목록·페이지 주소·GET 200을 한 장에 캡처한다. API 설정과 키가 보이는 Headers를 접는다.

로컬 API 리허설 캡처도 실습 결과로 인정한다. 다른 기기 공유는 공용 HTTPS API를 설정한 두 브라우저에서 같은 목록을 확인한 뒤 별도로 기록한다. REST Client 성공은 브라우저 CORS 성공과 같지 않다. 이번 교재 검증을 학생의 30분 수행 실측이나 공용 서버 공유 완료로 해석하지 않는다.

## 수업 자료와 다음 주

[한국어 슬라이드](slides.md) · [영문 슬라이드](slides_en.md) · [실습지](lab.md) · [따라하기](walkthrough.md) · [예제 설명](examples/README.md)

13주는 이 폴더 전체를 이어 쓰며 `guestbook-form`·`name`·`message`·`notice` 폼을 복원하고 `guestbook.js`에 POST와 재조회를 추가한다. 12주의 `API_BASE_URL`·`API_PUBLIC_KEY`·`BOOK_ID`, `loadMessages()`·`showList(items)` 이름을 유지한다.

공식 참고: [MDN Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch), [HTTP 메서드](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods), [Supabase Data API](https://supabase.com/docs/guides/api).
