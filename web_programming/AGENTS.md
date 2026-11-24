# 웹프로그래밍 작업 지침

`web_programming/`의 교재·예제·도구를 고치는 에이전트가 따르는 지침이다. Claude Code는 같은 폴더의 `CLAUDE.md`로 이 파일을 읽는다. 저장소 전체의 작업 문맥은 [`_forAI/`](../_forAI/README.md)에 있다.

## 범위

- 이 과목의 범위는 정규 15주(`weeks/`), 특강 6개(`specials/`), 공용 자산(`shared/`), 수업 도구(`tools/`), 개편 기록(`reviews/`)이다.
- 웹 덱을 더하거나 빼고 제목·장 수를 바꾸면 저장소 루트의 `site/catalog.json`(`web` 과목)을 고친다. 덱 수나 장 수가 바뀌면 `scripts/render-site.mjs`·`scripts/check-site.mjs`의 기대값도 고친다. 다른 과목 폴더와 저장소 루트의 `tools/`는 고치지 않는다.
- 커밋·푸시·브랜치 변경은 지시가 있을 때만 한다. 다른 창이나 다른 에이전트가 진행 중인 변경을 되돌리거나 덮어쓰지 않는다.

## 먼저 읽을 문서

1. [README.md](README.md): 과목 범위, 진입점, 운영 주의.
2. [weeks/README.md](weeks/README.md): 30차시 운영 기준, 3주차부터의 실습 루틴, 주차 폴더 구성, 문법·API를 처음 쓰는 주와 학기 범위 밖 문법, 실습 페이지 링크 규칙.
3. 작업할 주차·특강의 `README.md`와 `lab.md`. 특강 공통 운영은 [specials/README.md](specials/README.md), 공용 스타일과 REST 예제 설정은 [shared/README.md](shared/README.md).
4. 저장소 `_forAI/`의 `inventory.md`, `memo.md`(웹 REST와 Supabase 운영), `plan.md`(웹프로그래밍 후속 작업). `_forAI`와 이 파일·`weeks/README.md`가 다르면 이 파일을 따르고 다른 점을 보고에 적는다.
5. 수업 구성은 [주차별 교재](weeks/README.md)에서 확인한다. 이 PC에 개편 검토 기록이 있으면 `reviews/`에서 참고할 수 있다.

## 수업 구성

15주, 주 2회, 회당 90분이다. 일반 27차시는 강의·시연 60분과 학생 실습 30분이고, 8·15주 2차시는 안내 30분과 실기 60분, 9주 2차시는 안내 5분·발표 75분·피드백 10분이다. 1~6주는 자체 CSS를 쓰고 7주부터 W3.CSS 4.1.0을 cdnjs CDN으로 읽는다.

방명록 하나를 주차마다 넓힌다. 3주 폼에서 시작해 7주에 W3.CSS로 바꾸고 최신 글이 위에 오는 피드를 붙인다. 10주 배열 목록, 11주 객체·JSON·폼 저장, 12주 공개 API GET·Promise, 13주 방명록 CRUD, 14주 수정·삭제 결과 확인을 거쳐 15주 기말 실기로 끝난다. 4주부터 매주 새 저장소 `web-weekNN`을 쓰며, 방명록을 이어 가는 주에는 `examples/day2/web-weekNN/`을 다음 주 시작점으로 쓴다. 12주 필수 결과물은 나라별 공휴일 조회 화면이다. `web-week12`는 홈의 기온 조회와 브라우저 방명록을 담은 통합 예제이며, 서버 방명록 조회도 선택 실습으로 제공한다.

## 폴더와 파일의 역할

| 위치 | 역할 |
|---|---|
| `weeks/weekNN_slug/README.md` | 첫 줄 실습 페이지 링크, 목표·결과물·용어표·덱 주소·완료 기준·다음 수업 연결 |
| `slides.md`, `slides_en.md` | 한국어·영어 Marp 원고. 장 수와 순서, 시간표, 코드가 같아야 한다 |
| `walkthrough.md` | 처음부터 따라 하는 단계. 4~6·11·14주는 그 주에 바뀐 완성 파일을 전문으로 인용한다. 12주는 타이머 예제(ex01b~ex01d)에서 `.then()`과 `await`를, 같은 GET에서 Promise 체인과 `async`/`await` 코드를 대조한다. 7·9·10·13주는 고칠 구역을 보여 준다 |
| `lab.md` | 30분 시간표, 학생 수정 구역, 막혔을 때 표, 제출물. 평가 차시는 별도 시간표 |
| `examples/README.md` | 비교 예제 표(필수·시연·선택), 조립표, 주차 간 변경표 |
| `examples/dayN/exNN/` | 개념 하나의 예제. `index.html`·`app.js`, 5주부터는 예제별 `README.md`(기대 결과와 조작) |
| `examples/day2/web-weekNN/` | 그 주 완성본(4주부터). 3주까지는 `examples/dayN/`이 그날의 `my-web` 전체다 |
| `*.start.js`, `*.start.html`, `README.start.md` | 학생 시작 틀. 완성 파일과 따로 둔다 |
| `before.html`, `guestbook.before.html` | 7주 W3.CSS 변환 전 비교본(7주 `day1/ex01`, 7·9주 완성본) |
| `exam_structure.md`, `rubric.md`, `project_brief.md`, `demo_outline.md` | 평가 문서. 8주(`exam_structure`·`rubric`), 9주(`project_brief`·`rubric`), 14주(`project_brief`·`rubric`·`demo_outline`, 별도 과제 안내), 15주(`rubric`) |
| `weeks/week08_midterm/examples/w01_*`~`w07_*` | 1~7주 문제은행. 15주도 이 폴더를 다시 쓴다 |
| `weeks/week15_final_exam/examples/w09_*`~`w14_*` | 9~14주 문제은행. `w12_fetch_cards`·`w13_text_safe`·`w14_readme_images`는 옛 주소를 위한 이동 안내만 남은 폴더다 |
| REST 예제 폴더 | API를 호출하는 폴더에는 `requests.http`와 `README.md`를 둔다. 12주 필수 예제는 키 없는 URL을 요청 파일에 적는다. 13주는 `config.example.json`·`load-config.js`·`.env.example`을 둔다. 12주 선택 방명록, 14·15주와 hash SPA 특강 04는 `config.example.js`와 `.env.example`을 쓴다. Git 제외 규칙은 저장소 루트 `.gitignore`에서 관리한다 |
| 주석만 남은 `submit.js`·`edit.js` 등 | 13·14주에서 동작을 옮긴 뒤 옛 경로에 남긴 이동 안내. HTML에서 읽지 않는다. 14주 `day1/ex01`의 `config.example.js`도 서버를 부르지 않는 예제라 주석만 남긴 안내다 |
| `specials/NAME/` | README·slides·slides_en·walkthrough·lab·examples(`kakao_aerial_map`에는 walkthrough가 없다) |
| `shared/` | `README.md`(W3.CSS CDN 연결, 정규 REST 예제의 설정 안내) |
| `tools/static-server/` | 수업용 정적 서버 `server.mjs`와 시험 `server.test.mjs` |
| `tools/guestbook-api/` | 로컬 모의 API `server.mjs`(127.0.0.1:8787), Supabase 구축용 `schema.sql`·`about-help.sql`, 기존 프로젝트 전환용 `enable-public-crud.sql`, 학생 안내 `student-guide.md` |
| `reviews/<날짜>-<주제>/` | 로컬 개편 기록과 검토 자료. 루트 `.gitignore`에서 제외한다 |

이름 규칙은 다음과 같다.

- 13주차 방명록 CRUD의 폴더와 덱 ID는 `week13_guestbook_crud`이다. 새 자료는 이 이름으로 연결한다. 7주 CSS 응용과 14주 PATCH·DELETE는 기존 폴더 `week07_form_input`, `week14_project_presentation`을 사용한다.
- 예제 번호는 한 주 안에서 이어 센다(1일차 `ex01`~, 2일차는 그다음 번호부터). 문제 폴더는 `wNN_주제`이고 NN은 출처 주차다.
- 예시 계정은 `student01`, 이메일은 `student01@example.com`, 저장소는 3주까지 `my-web`, 4주부터 `web-weekNN`이다.

## 예제 작성 규칙

- HTML 실습 화면에는 제목, 입력, 버튼, 결과와 필요한 짧은 상태만 둔다. 수업 설명, 따라하기 절차, 개념 해설을 화면에 길게 넣지 않는다.
- 설명과 실습 순서는 예제 폴더의 README에 작성한다. 코드 주석은 해당 줄을 이해하는 데 필요한 내용만 남긴다.
- 기본 예제는 학생이 입력하고 버튼을 눌러 결과를 화면에서 확인할 수 있게 만든다. 콘솔 출력만으로 사용자 동작을 대신하지 않는다.
- 예제를 기본 동작부터 단계별 폴더로 나누고, 확장 기능은 기본 예제와 구분한다. 필수 수정, 강의자 시연, 선택 연습을 README·lab에 구분해 적는다.
- W3.CSS는 cdnjs의 버전 고정 주소 `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`로 연결한다. 입력창·버튼·목록은 HTML과 W3.CSS 클래스로 작성한다. 이교수님이 해당 실습에 별도 CSS를 쓰라고 직접 지시한 경우에만 추가한다. 그 지시가 없으면 별도 스타일시트, HTML의 `<style>`·`style` 속성, JavaScript로 추가하는 스타일을 사용하지 않는다. 스타일을 정리할 때는 예제 개수와 실습 내용을 유지한다. 주차 예제 색인에 CDN 주소를 한 번 안내한다.
- JavaScript는 클래식 `<script src="…" defer>`와 브라우저 기본 API를 쓴다. 문법·API를 처음 쓰는 주와 학기 범위 밖 문법은 [weeks/README.md](weeks/README.md#자료-작성-원칙)를 따른다.
- 차시 시간은 위 수업 구성을 따른다(일반 차시 60+30, 평가 차시 예외). 파일 준비·저장소 준비는 수업 전에, 3주 이후 공개 업로드는 수업 뒤에 한다. Git 자체를 배우는 1~2주는 Git 작업을 수업 안에 둔다.
- 7주차 CSS 응용에서는 W3.CSS로 반응형 메뉴와 카드, 최신 글이 위에 오는 피드를 구성해 방명록에 적용한다. 7주의 최신순 피드와 제공 JS를 9주까지 이어 쓴다. 10주부터는 같은 W3.CSS CDN·폼 ID를 쓰고, 배열 인덱스와 화면의 줄을 비교하도록 등록순으로 그리는 문자열 목록 틀을 제공한다.
- 11주차는 문자열 저장 → JSON → 폼 저장 순서다. 11주 전체 저장 방명록은 제공 시연본이며 기말 필수 저장 문항은 폼 한 객체 저장 수준이다.
- 동작 JavaScript는 페이지당 하나로 조립하고, 설정 파일 같은 제공 기능은 별도 파일로 표시한다. 초기 데이터 조회는 필요한 함수·이벤트·설정의 초기화 뒤에 실행한다.
- REST API 예제에는 VS Code REST Client용 `.http` 요청을 함께 제공한다. 슬라이드에는 예제에 쓰는 API의 전체 요청 주소(프로토콜·호스트·경로·쿼리)를 표시한다. 키 없이 조회하는 GET은 그 주소로 바로 연결한다. 첫 호출은 서비스의 공개 문서와 간단한 GET으로 확인한다. 수업용 방명록은 about·help로 접속·사용법을 확인하는 요청을 제공한다. 실제 인증 정보는 추적 파일에 넣지 않는다.
- 12주 필수 실습은 API 키 없이 Promise 실행 순서, `.then()` 체인, `async`/`await`, 오류 처리를 다룬다. 할 일·환율·타로 카드·공휴일·날씨 조회는 공개 GET API를 사용한다. 13주는 같은 폴더의 `config.json`에서 주소·공개 키·방명록 번호를 읽고 생성(Create·POST) → 조회(Read·GET) → 수정(Update·PATCH) → 삭제(Delete·DELETE) 순서로 실습한다. 생성 응답에서 받은 글 번호를 마지막 요청까지 사용한다. 목록의 각 글 옆에 삭제 버튼을 두고, 누른 글의 `book_id`와 `id`로 DELETE를 보낸다. 12주 선택 방명록, 14·15주와 hash SPA 특강 04는 `config.example.js`의 방명록 번호를 바꾸고 처음 열 때 묻는 창에 공개 키를 넣는다. 로컬 모의 API는 강의자 리허설용이다. [공용 설정 안내](shared/README.md)

## 함께 고칠 곳

한 파일을 고치면 아래 표의 짝도 같은 작업에서 고친다. 사본이 같은지는 저장소 루트에서 `git hash-object <파일A> <파일B>`로 본다. 두 해시가 같아야 한다(줄바꿈 차이는 무시된다).

| 고친 것 | 함께 고칠 곳 |
|---|---|
| `slides.md` | `slides_en.md`의 같은 장. 장 수를 바꾸면 `site/catalog.json`의 `web` 요약에 적힌 장 수, 두 빌드 스크립트의 `EXPECTED_SLIDES`, `check-site.mjs`의 `EXPECTED.web` |
| 덱 추가·삭제 | 위 항목과 `EXPECTED_DECKS`, `catalog.json`의 `chapters`, [specials/README.md](specials/README.md) 또는 [weeks/README.md](weeks/README.md) 목록 |
| 완성 파일(`web-weekNN/`, 3주까지 `dayN/`) | `walkthrough.md`가 인용한 코드(전문을 싣는 주는 전문, 구역만 싣는 주는 그 구역을 글자 단위로 같게), `examples/README.md`의 조립표, `lab.md`의 수정 구역, 다음 주차의 같은 파일 |
| 주차의 시간표·필수 범위 | 그 주 `README.md`·`lab.md`·`walkthrough.md`·`slides.md`·`slides_en.md`·`examples/README.md` 여섯 곳 |
| 홈 파일(`index.html`·`about.html`·`app.js`·`styles.css`·`images/profile.png`) | 이후 주차 완성본에 같은 파일을 넘길 때 함께 확인한다. 12·13주 홈과 내 정보는 W3.CSS CDN을 사용한다. 12주 홈은 도시별 날씨를 조회한다 |
| 12주 `web-week12/weather.js` | 홈의 도시 선택과 `weather.http`의 도시·좌표가 일치해야 한다. 홈을 열 때 한 번 조회한다 |
| 7주 `day2/web-week07/`의 9개 파일 | 9주 `day2/web-week09/`의 같은 이름 파일(현재 모두 같다) |
| 9주 `day2/web-week09/` | 15주 `examples/w09_readme_links/`. 두 폴더에 함께 있는 파일은 해시가 같다. `w09_readme_links`에는 `guestbook.before.html`과 `images/site-map.svg`를 두지 않는다 |
| 11주 `day2/web-week11/guestbook.js` | 12주 `day2/web-week12/guestbook.local.js`(현재 같다)와 11주 `walkthrough.md`의 코드 전문 |
| 7주 피드 CSS | 7주 완성 피드와 그 화면을 이어 쓰는 9주 발표·15주 README 문항에서 같은 배치를 확인한다 |
| 정본 `weeks/week12_fetch_json/examples/day2/web-week12/config.example.js` | 14·15주와 hash SPA 특강 04의 `config.example.js` 사본(14주 `day1/ex01` 제외), 각 화면의 `id="key-clear-button"` 버튼, [공용 설정 안내](shared/README.md) |
| 13주 `load-config.js`·`config.example.json` | 13주 기본 예제 네 폴더와 완성 방명록의 사본, 각 화면의 `id="config-status"`, [공용 설정 안내](shared/README.md) |
| 8주 문제 `w01`~`w07` | 15주 `examples/README.md` 문제은행 표와 `rubric.md` |
| 공통 운영 규칙(시간, 도입 주차, CDN, 업로드 시점) | [README.md](README.md), [weeks/README.md](weeks/README.md), [specials/README.md](specials/README.md), [ta_setup_guide.md](ta_setup_guide.md), 이 파일 |
| 방명록 API 계약(경로, 헤더, 상태 코드) | `tools/guestbook-api/`의 `server.mjs`·`schema.sql`·`about-help.sql`·`student-guide.md`, 12~14주 `requests.http`, `specials/supabase_guestbook/` |
| 공개 원고의 차시 구간·실습 정답에 닿는 변경 | 비공개 대본·해답(아래 경계 절). 공개 쪽만 고치고 보고에 적는다 |

## 검증

아래 명령은 저장소 루트에서 실행한다. 파이프가 있는 명령은 POSIX 셸(Windows에서는 Git Bash) 기준이다.

```bash
# 바꾸거나 새로 만든 JS·MJS의 구문 검사. 종료 코드 0이면 통과(git의 CRLF 안내 경고는 오류가 아니다)
{ git diff --name-only --diff-filter=d HEAD -- web_programming; git ls-files -o --exclude-standard -- web_programming; } | grep -E '\.m?js$' | xargs -n1 node --check

# 실습 서버·도구 시험. 정적 서버·방명록 API·홈 IoT·Supabase 06 시험 26개와 지도 시험 25개가 모두 통과해야 한다
npm run test:labs

# config.example.js 사본 중 13주와 14주 첫 예제를 제외한다. 해시는 한 종류여야 한다
git ls-files -co --exclude-standard -- 'web_programming/weeks/*config.example.js' 'web_programming/specials/hash_spa/*config.example.js' ':(exclude)web_programming/weeks/week13_guestbook_crud/**' ':(exclude)web_programming/weeks/week14_project_presentation/examples/day1/ex01/config.example.js' | xargs git hash-object | sort | uniq -c

# 13주 JSON 견본과 로더는 각각 한 종류여야 한다
git ls-files -co --exclude-standard -- 'web_programming/weeks/week13_guestbook_crud/*config.example.json' | xargs git hash-object | sort | uniq -c
git ls-files -co --exclude-standard -- 'web_programming/weeks/week13_guestbook_crud/*load-config.js' | xargs git hash-object | sort | uniq -c

# W3.CSS 주소는 4.1.0 한 종류만 나와야 한다
git grep --untracked -ohE 'w3-css/[0-9.]+/w3(\.min)?\.css' -- web_programming | sort | uniq -c
```

예제 동작은 정적 서버로 열어 확인한다. 포트는 비어 있는 번호를 쓰면 된다. 이 서버는 `.env`·`.git`·`.local`·`localfiles` 경로에 403을 돌려주고 `.env.example`은 200으로 준다.

```bash
node web_programming/tools/static-server/server.mjs web_programming 8111
# 예: http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex04/
```

브라우저에서는 버튼을 눌러 화면 결과가 문서의 기대 결과와 같은지, Console 오류가 0인지, 375px 폭에서 가로 넘침이 없는지 본다. 4주 `ex04`의 고정 640px 비교 상자는 의도한 넘침이다. `node --check`만으로 동작 검증을 대신하지 않는다.

전체 빌드·시험은 다음과 같다.

- `npm run build`와 `npm test`: 원고·예제·사이트 색인을 바꿨으면 실행한다. 전체 덱·슬라이드 수와 웹 교재의 언어별 장 수는 `scripts/check-site.mjs`의 `EXPECTED_DECKS`·`EXPECTED_SLIDES`·`EXPECTED.web`을 기준으로 검사한다. 빌드는 `dist/`를 다시 쓰므로 같은 작업 폴더에서 여러 에이전트가 동시에 실행하지 않는다.
- 수업용 방명록 예제를 로컬 모의 API로 확인할 때: `node web_programming/tools/guestbook-api/server.mjs`(127.0.0.1:8787, 데이터는 Git 제외 폴더 `tools/guestbook-api/.local/`에 생긴다).
- 홈 IoT 특강: `node web_programming/specials/home_iot_http/examples/simulator/server.mjs`(localhost:8014). 지도 특강: `npm --prefix web_programming/specials/kakao_aerial_map/examples/app start`(localhost:3000, 실제 지도에는 키 설정이 필요하다).

한국어 문서는 `korean-copy-style` 문서 규칙(해라체, 질문형 제목 금지, 꾸밈말 제거)을 따르고, 그 검사기가 있는 환경이면 바꾼 문서에 돌린다. 새 파일은 LF로 저장한다(`.gitattributes`가 `eol=lf`). `git diff --check`로 줄 끝 공백을 확인한다.

## 결정 사항

**SPA: 정규 과정은 세 HTML 페이지를 유지하고 SPA는 14주 뒤 선택 특강 `specials/hash_spa/`에서 다룬다**
- 근거: 정규 11~14주의 저장·REST 작성량과 선수학습을 늘리지 않는다. 9개 독립안을 비교해 이 구성을 선정했다.
- 대안: 9주에 작은 SPA 전환을 넣는 C02 등 정규 중간 전환안. 학생 수정 범위, 11→12주 인계, 기말 문항 연결에서 C01보다 낮게 평가됐다.
- 재검토: 실제 수업에서 학생 완료 시간을 측정한 뒤 정규 편입 여부를 다시 본다. SPA 특강은 정규 시험에 내지 않는다.

**12주는 키 없는 공개 API로 비동기 코드를 배우고, 13·14주는 강의자가 준비한 방명록에서 쓴다**
- 근거: 학생에게 Supabase 계정·SQL·SDK·로그인 구현을 요구하지 않고 HTTP 요청과 응답에 집중한다. 서버 구축은 `specials/supabase_guestbook/` 연구 특강의 몫이다.
- 대안: 학생이 각자 서버를 만드는 안. 정규 시간 안에 계정·권한 설정까지 넣어야 한다.
- 재검토: 학기마다 공용 API 운영 준비(태그 등록·공용 공개 키 배부, `_forAI/plan.md`)를 확인할 때.

**12주 선택 방명록·14주 이후의 REST 예제는 주소와 방명록 번호를 `config.example.js`에 두고 공개 키를 브라우저에 저장한다**
- 근거: 학생 코드에서 요청 흐름(이벤트 → `await fetch` → 화면 반영)이 그대로 보여야 한다. 2026-11-18 C01의 설정 패널(`shared/api-settings.js`)은 제출 이벤트를 제공 코드가 받고 전역 값을 실행 중에 바꿔, 호출부마다 설정 변경에 대비하는 코드를 만들었다. 새로고침하면 설정이 사라져 13주의 '서버에 저장한 글은 새로고침 뒤에도 남는다'를 거꾸로 보여 줬다. 공개 키를 파일 대신 localStorage에 두면 학기마다 키를 바꿔도 저장소의 사본을 고치지 않는다. 키를 묻는 창과 **공개 키 지우기** 버튼은 개발자 도구 없이 쓸 수 있어 휴대폰에서도 같은 순서로 키를 넣고 바꾼다. 묻기·저장·지우기는 제공 코드인 `config.example.js`가 맡아 학생 코드에 섞이지 않는다.
- 대안: 설정 패널(2026-11-22 이교수님 지시로 삭제). 공개 키를 `config.example.js`에 적는 방식은 키를 바꿀 때마다 사본을 모두 고쳐야 한다. 개발자 도구 Console에서 저장 명령을 치는 방식은 휴대폰에서 쓰기 어렵고 키를 바꿀 때마다 명령을 다시 쳐야 한다.
- 재검토: 첫 운영에서 키를 묻는 창을 취소하거나 키를 잘못 넣어 HTTP 401로 막힌 경우를 본 뒤.

**13주는 예제 폴더의 `config.json`에서 주소·공개 키·방명록 번호를 읽는다**
- 근거: 값 세 개를 한 파일에서 관리하고, 설정을 읽은 뒤 방명록 요청을 시작한다. 공용 교재에는 키를 비운 JSON 견본을 올린다.
- 재검토: 14주 이후에도 같은 설정이 필요할 때.

그 밖에 되돌리지 않는 결정은 다음과 같다.

- 13주차는 이전에 배포한 슬라이드 주소로 접속해도 새 덱이 열린다. 다른 주차는 기존 폴더 이름과 덱 ID를 유지한다.
- 14주를 레포트 검사 주차로, 13주를 릴리스·보안 독립 주제로 되돌리지 않는다. 레포트는 별도 과제로 공지한다.
- 배열 심화(`filter`·`map`·`reduce` 등)는 `specials/array_advanced/` 보강 특강에 두고 정규 시험에 넣지 않는다. 11주 `ex08` 이후 예제를 다시 만들지 않는다.
- 7주 2일차 예제는 `ex04`·`ex05`와 `web-week07`이다. 옛 `ex06`~`ex08`은 교재에서 빠졌다. 이교수님이 직접 수정하고 보존을 요청한 7주 타임라인·방명록 피드와 이를 이어 쓰는 9·15주 자료의 기존 CSS는 보존한다.

## 하지 말 것

- 실제 `config.json`과 `.env`, Supabase secret key, DB 비밀번호, `localfiles/`, `.local/`을 추적 파일·ZIP·캡처에 넣지 않는다. 브라우저용 publishable key만 공개 설정으로 쓸 수 있다.
- 13주에서는 Git에서 제외한 `config.json`의 `API_PUBLIC_KEY`에 브라우저용 공개 키를 넣는다. 12주 선택 방명록, 14·15주와 hash SPA 특강 04는 처음 열 때 공개 키를 받아 localStorage에 저장하며 **공개 키 지우기**로 바꾼다.
- `book_id`는 수업용 글을 구분하는 태그다. 공용 공개 키가 있으면 모든 태그의 글을 작성·조회·수정·삭제할 수 있다. 실습에서는 자기 태그에 쓴 글을 사용한다.
- PATCH 200의 빈 배열이나 DELETE 204만으로 변경 성공을 판정하지 않는다. 같은 `id`로 다시 GET해 확인하고, 204 응답에 JSON 파싱을 하지 않는다.
- 공용 Supabase의 실제 글을 지시 없이 추가·수정·삭제하지 않는다.
- 시험 시작 파일의 빈 구현에 해답을 채우지 않는다. 실제 출제 값과 정답은 공개 저장소에 두지 않는다.
- 로컬 자동 시험, REST Client 성공, localhost 브라우저 성공을 Pages 실배포나 공용 쓰기 검증으로 기록하지 않는다. 에이전트의 수행 시간을 학생 소요 시간으로 쓰지 않는다.
- `slides.md`에 raw HTML이나 꺾쇠 표기(`<b>`, `<repository>` 등)를 쓰지 않는다. 줄 끝 `<br>`, `<code>`, 주석 외에는 빌드가 실패한다. 꺾쇠가 필요하면 인라인 코드로 감싼다.
- `examples/` 아래에 임시 파일·캡처·검사 스크립트를 두지 않는다. 슬라이드가 예제 HTML을 연결한 단원은 빌드가 그 `examples/`의 공개 파일을 아직 추적하지 않는 새 파일까지 사이트로 복사한다(Git 제외 파일은 빠진다). 검사 산출물은 저장소 밖이나 `reviews/`에 둔다.
- 공개 문서와 보고서에 작업 PC의 절대 경로, 서버·장비 주소, 학교명·분반·실제 배점·실제 수업 일정, 학생 실명·학번·실제 이메일을 쓰지 않는다.
- 정적 서버나 실습 서버가 다음 세션에도 떠 있다고 가정하지 않는다.

## 완료 기준

- 바꾼 주차의 여섯 문서가 같은 시간표, 필수 범위, 파일 이름을 말한다.
- 위 표의 짝 파일을 고쳤고, 사본 검사 명령의 결과가 한 종류로 나온다.
- 바꾼 JS가 구문 검사를 통과하고, 바꾼 예제를 정적 서버에서 열어 기대 결과·Console 오류 0·375px 가로 넘침 없음을 확인했다.
- 서버·도구·특강 서버 코드를 바꿨으면 `npm run test:labs`가 통과한다. 원고·덱·예제를 바꿨으면 `npm run build`와 `npm test`가 통과한다.
- `git status`에 맡은 범위 밖의 변경이 없다.

## 보고 형식

보고에는 다음을 적는다. 자체 통과 점수는 붙이지 않는다.

1. 바꾼 파일(저장소 기준 상대 경로)과 수업 단위의 변경 요약.
2. 실행한 명령과 결과(통과 수, 실패 내용).
3. 실행하지 못한 검증과 이유(브라우저 조작, Pages 배포, 공용 API 쓰기, 학생 실측 등).
4. 같이 고쳐야 하지만 범위 밖이라 남긴 곳(다른 주차, 비공개 대본·해답, `_forAI/`).
5. 발견했지만 고치지 않은 문제.

여러 주차를 고칠 때 작성하는 검토 보고서는 `reviews/<날짜>-<주제>/`에 로컬로 보관한다. 이 폴더는 커밋·푸시 대상에서 제외한다.

## 비공개 짝 저장소와의 경계

강의 대본(`lecture_script.md`), 실습 해답(`lab_solution.md`), 시험의 실제 문항·값·정답은 비공개 짝 저장소 `univ_scoring_works/teaching_materials_private/`에 같은 주차 폴더 이름으로 있다. 학기 범위 밖 용어의 금지 목록도 공개 저장소 밖의 강의자 설계 문서가 관리한다. 공개 저장소에는 이 내용을 옮기지 않는다.

대본의 구간 제목과 분 범위는 공개 `slides.md`와 같아야 한다. 공개 원고의 차시 구간이나 실습 정답에 닿는 부분을 바꾸면 비공개 쪽을 직접 고치지 말고 보고에 남긴다. 12~15주 비공개 자료를 공개 REST 범위에 맞추는 일은 아직 남아 있다(`_forAI/plan.md`).
