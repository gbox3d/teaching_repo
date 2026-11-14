[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

# 13주차 · REST API로 방명록 저장하기

## 목차

- [학습 목표](#학습-목표)
- [이번 주 결과물](#이번-주-결과물)
- [2일 수업 흐름](#2일-수업-흐름)
- [준비](#준비)
- [이번 주 용어](#이번-주-용어)
- [비교 예제](#비교-예제)
- [수업 자료](#수업-자료)
- [완료 기준](#완료-기준)
- [다음 수업 연결](#다음-수업-연결)

12주에는 서버의 목록을 GET으로 읽었다. 이번 주에는 7주에 배운 폼 입력을 POST의 JSON 본문으로 보내고, 저장 후 GET으로 목록을 다시 읽는다. 저장한 글은 브라우저가 아니라 서버에 남는다.

## 학습 목표

1. GET과 POST가 서버에 요청하는 일이 어떻게 다른지 설명한다.
2. method·headers·body를 지정하고 객체를 JSON.stringify로 바꿔 전송한다.
3. 이름·메시지 입력을 POST에 연결하고 201 응답과 서버 id를 확인한다.
4. 저장 중에는 버튼을 비활성화하고 성공·실패 안내를 구분한다.
5. 저장 후 GET으로 다시 읽고 다른 기기에서도 글이 보이는지 확인한다.

## 이번 주 결과물

내 폼에서 저장한 글이 서버 목록에 보이고 Network에 POST 201과 GET 200이 이어진 화면을 캡처 한 장으로 제출한다.
새 저장소 `web-week13`의 홈·내 정보·방명록 세 페이지를 이어 쓴다.
이번 주에는 프로젝트 카드나 레포트를 만들지 않는다.

## 2일 수업 흐름

| 일차 | 설명·시연 30분 | 실습 60분 |
|---|---|---|
| 1일차 | 객체를 JSON으로 → POST → 헤더 → 서버 입력 검사 | ex01~ex03에서 요청 본문과 응답 비교 |
| 2일차 | submit → 저장 중 → 실패 안내 → POST 다음 GET | ex04~ex06 비교 후 기존 방명록에 폼 연결 |

## 준비

- 지난주 완성본: [web-week12](../week12_fetch_json/examples/day2/web-week12/)
- VS Code·Git·Chrome과 Node.js. [정적 서버](../../tools/static-server/README.md)를 작업 폴더에 둔다.
- 강의자가 제공한 HTTPS API 주소·공개 키·방명록 번호. 학생은 Supabase 계정을 만들지 않는다.
- [강의자 API 준비·로컬 연습 안내](../../tools/guestbook-api/README.md). 설정 예제의 `127.0.0.1:8787`은 로컬 연습 주소이며 이미 배포된 공용 주소가 아니다.

`config.example.js`의 세 값을 수정하며 파일 이름은 그대로 쓴다. 공개 키는 학생별 편집 키나 서버 비밀 키와 다르다.
로컬 연습은 정적 서버 `http://localhost:8000`과 API `http://127.0.0.1:8787`을 함께 실행한다.
GitHub Pages에서는 강의자가 제공한 HTTPS API를 사용한다. 공용 API가 준비되기 전에는 로컬 화면·Network 캡처로 실습을 확인하고, 다른 기기 공유는 공용 API 설정 후 확인한다.

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| HTTP 메서드 | HTTP method | HTTP 方法 |
| 본문 | body | 正文 |
| 콘텐츠 형식 | Content-Type | 内容类型 |
| 생성 | POST | 创建 |
| 직렬화 | JSON.stringify | 序列化 |
| 비활성화 | disabled | 禁用 |
| 식별 번호 | id | 标识符 |

## 비교 예제

각 예제는 `index.html`·`app.js`와 필요한 `config.example.js`로 구성된다.
원리를 하나씩 확인하고 마지막에 [이번 주 완성본](examples/day2/web-week13/guestbook.html)을 조립한다.

| 예제 | 주제 | 확인할 것 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01](examples/day1/ex01/index.html) | JSON 본문 만들기 | 객체와 전송할 JSON 글자를 비교한다 | message 값 |
| [ex02](examples/day1/ex02/index.html) | 고정값 POST | 버튼을 누를 때만 글 한 줄을 저장한다 | 보내는 메시지 |
| [ex03](examples/day1/ex03/index.html) | 서버 입력 검사 | 빈 메시지는 서버가 거절한다 | 빈 문자열 → 문장 |
| [ex04](examples/day2/ex04/index.html) | 폼 입력 POST | 입력한 문장을 JSON 본문에 넣는다 | 입력 내용과 앞뒤 공백 |
| [ex05](examples/day2/ex05/index.html) | 저장 중 버튼 | 응답을 기다리는 동안 다시 누를 수 없다 | Slow 3G → No throttling |
| [ex06](examples/day2/ex06/index.html) | 저장 후 재조회 | POST 성공 뒤 GET 결과를 표시한다 | Network의 POST·GET 순서 |

## 수업 자료

- [슬라이드](slides.md) · [영문 슬라이드](slides_en.md)
- 교재 사이트: https://gbox3d.github.io/teaching_repo/webprg/decks/week13_release_security/index.html
- [따라하기](walkthrough.md) · [실습지](lab.md) · [예제 설명](examples/README.md)
- 강의 대본과 실습 해답은 강의자 별도 관리(비공개)다.

## 완료 기준

- [ ] 12주 GET 목록이 그대로 동작한다.
- [ ] 이름과 메시지를 입력하면 POST 201 뒤 GET 200이 보인다.
- [ ] 서버가 만든 id를 확인하고 새로고침해도 저장한 글이 보인다.
- [ ] 저장 중에는 버튼이 비활성화되고, 실패하면 입력값을 보존한다.
- [ ] 공용 HTTPS API를 사용하는 다른 브라우저·기기에서도 같은 글을 확인했다.
- [ ] 캡처 한 장에 저장한 글과 POST 201·GET 200이 보인다.

API에 처음 준비된 글 수는 환경에 따라 다르다. 특정 개수보다 요청·응답과 화면이 일치하는지 확인한다.
실명·학번·실제 이메일을 사용하지 않고 수업용 별칭으로 실습한다.

## 다음 수업 연결

14주에는 서버 id로 글 하나를 지정해 PATCH로 수정하고 DELETE로 삭제한다. 레포트는 별도 과제로 안내한다.

## 공식 참고 자료

- [MDN · Fetch API 사용](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [MDN · HTTP 요청 메서드](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods)
- [Supabase · Data REST API](https://supabase.com/docs/guides/api)
