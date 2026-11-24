# Hash SPA 특강

14주 REST 방명록을 마친 뒤 듣는 선택 특강이다. 정규 수업의 세 HTML 페이지(MPA)는 유지하며 이 자료는 정규 시험에 출제하지 않는다. 페이지 이동과 화면 전환을 비교한 뒤 기존 CRUD를 한 HTML에 합친다. 특강 전체 차시 수와 실험 시간을 제한하지 않는다.

## 학습 목표

실제 HTML 링크와 hash 링크의 요청 차이를 관찰한다. `hidden`, `location.hash`, `hashchange`로 화면을 선택하고 주소·포커스·입력을 함께 확인한다. 화면 전환, 새로고침, 서버 저장의 수명을 구별한다.

선수학습은 6주 DOM·이벤트, 7주 W3.CSS, 12~14주 fetch·JSON·CRUD다. 프레임워크·npm 설치·라우터 패키지·History API는 사용하지 않는다.

## 준비와 실행

Node.js 24 이상, VS Code, Chrome을 준비한다. 저장소 루트에서 정적 서버를 실행한다. 이 명령은 npm 설치가 필요 없다.

```bash
node web_programming/tools/static-server/server.mjs web_programming 8111
```

첫 주소는 http://localhost:8111/specials/hash_spa/examples/01_mpa/index.html 이다. 각 예제는 자기 폴더의 HTML과 JS를 함께 복사하면 별도로 실행할 수 있다. `examples/` 루트에는 안내 README만 둔다.

모든 화면은 [W3.CSS 4.1.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 읽는다. CDN을 읽으려면 인터넷 연결이 필요하다. 04의 REST 실행은 [해당 README](examples/04_rest_guestbook/README.md)를 따른다. 04는 처음 열 때 배부받은 공개 키를 묻는다.

## 단계와 수업 자료

| 단계 | 학생 수정 | 강의자 시연·제공 코드 | 확인 결과 |
|---|---|---|---|
| [01 MPA](examples/01_mpa/README.md) | 실제 세 파일 링크를 따라 이동 | 14주 세 페이지와 비교 | HTML 문서 재요청, 각 파일 직접 진입 |
| [02 두 화면](examples/02_two_screens/README.md) | `showScreen`의 표시 조건 | 포커스·현재 메뉴 갱신 | 한 DOM, 카운터 유지, 주소는 그대로 |
| [03 세 hash 화면](examples/03_hash_routes/README.md) | hash 읽기·표시 조건·이벤트 연결 | 미등록 경로·접근성 처리 | 직접 주소·뒤로/앞으로·입력 유지 |
| [04 CRUD 통합](examples/04_rest_guestbook/README.md) | section 조립·ID 충돌 확인 | 14주 REST·`config.example.js`·오류 처리 | 전환 중 입력 유지, 서버 CRUD 재조회 |

[한글 슬라이드](slides.md) · [영문 슬라이드](slides_en.md) · [실습지](lab.md) · [따라하기](walkthrough.md) · [예제 목록](examples/README.md)

## 운영과 완료 기준

설명·시연과 실습을 단계별로 반복한다. 01~03의 첫 운영은 60분 강의·시연과 30분 실습으로 시작할 수 있다. 04 조립과 실패 실험은 별도 후속 시간에 진행하며 이 시간표를 전체 특강의 상한으로 삼지 않는다. 파일 준비와 API 배부는 실습 전에 마친다.

필수는 빈 hash, 세 등록 hash, 미등록 hash, 뒤로·앞으로, 제목 포커스, 입력 보존과 POST 한 번이다. 강의자는 PATCH·DELETE 및 통신 실패를 시연한다. 학생은 후속 실습에서 세 글 추가·가운데 글 수정/삭제·오류 복구를 직접 재현한다. 선택 연구는 재조회 정책 변경이며 기본 구현의 전환 시 자동 GET을 추가하지 않는다.

GitHub Pages의 예시 주소는 `https://<아이디>.github.io/<저장소>/index.html#guestbook`이다. `index.html`은 실제 파일이며 hash는 서버 요청에 포함되지 않는다. 주소를 `/<저장소>/guestbook`으로 바꾸지 않는다. 루트와 저장소 하위 경로에서 직접 진입·새로고침이 모두 되어야 한다.

화면을 바꿀 때 section을 숨기므로 입력·홈 횟수는 유지된다. 새로고침은 문서를 다시 실행하므로 입력과 횟수가 초기화된다. 서버에 저장한 글과 이 브라우저의 localStorage에 저장한 공개 키는 새로고침해도 남는다. 서버 글은 GET으로 다시 확인한다.
