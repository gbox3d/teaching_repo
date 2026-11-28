# Inventory

## 목차

- [Repository](#repository)
- [Top-level structure](#top-level-structure)
- [Entrypoints and key modules](#entrypoints-and-key-modules)
- [Build and validation commands](#build-and-validation-commands)
- [Tests](#tests)
- [Notes](#notes)
- [웹 REST 교재와 연구 특강](#웹-rest-교재와-연구-특강)
- [Android RoomControl과 WlEno](#android-roomcontrol과-wleno)
- [오픈소스 AI 10~13주와 공용 도구](#오픈소스-ai-1013주와-공용-도구)

## Repository

강의 편집·게시 작업의 로컬 폴더와 다른 저장소의 스킬 연결은 [강의 영상 인수인계](lecture-video.md)를 따른다. `output/`은 Git 제외이며 편집 결과가 소스 동기화로 전달되지는 않는다.

- Name: `teaching_repo`
- Path: 현재 체크아웃에서 `git rev-parse --show-toplevel`로 확인한다. 다른 머신의 과거 경로를 가정하지 않는다.
- Summary: 대학·학기와 무관하게 재사용하는 공개 수업교재(모바일·웹·오픈소스 AI)의 단일 기준. Markdown 원고를 Marp로 렌더해 GitHub Pages 슬라이드 도서관으로 배포한다.
- 기준: 2026-11-28 커밋 `d0ad054`(`origin/main`과 같다). `8cc49ea` 뒤 다른 세션의 커밋 7개(2026-11-24~25)를 반영했다.

## Top-level structure

```text
teaching_repo/
├─ AGENTS.md · CLAUDE.md              저장소 전체 에이전트 지침(CLAUDE.md는 @AGENTS.md 한 줄)
├─ README.md                          교재 색인·공용 교재와 학교 자료의 경계·편집 원칙·라이선스
├─ environment_baseline_template.md   학기별 실습환경 기준표(복사용, TBD는 교수 승인값)
├─ ta_lab_setup_guide.md              실습조교 공통 설치 목록
├─ _shared/README.md                  과목 공통 자산 승격 기준(아직 내용 없음)
├─ _forAI/                            작업 문맥(README·inventory·memo·dev_log·plan·lecture-video)
├─ android_programming/               모바일프로그래밍
│  ├─ AGENTS.md · CLAUDE.md           과목 작업 지침
│  ├─ weeks/weekNN_*/                 정규 15주(11~15주 RoomControl·WlEno)
│  ├─ specials/legacy_week11~15_*/    옛 11~15주 보존 특강 1~5(연락처·BLE)
│  ├─ specials/synthesizer/           악보 JSON 2개만 있음(참조 없음, plan 참고)
│  ├─ bleuno/                         특강용 BLE 공통 클래스 9개(src/)·보드 안내·type_m 실습
│  ├─ iot_sim/lab.md                  RoomControl 수업 전 LAN 연결 점검
│  └─ ta_setup_guide.md
├─ web_programming/                   웹프로그래밍
│  ├─ AGENTS.md · CLAUDE.md           과목 작업 지침
│  ├─ weeks/weekNN_*/                 정규 15주
│  ├─ specials/                       특강 6개(배열 심화·지도·Supabase 방명록·신시사이저·HTTP 홈 IoT·hash SPA)
│  ├─ shared/README.md                W3.CSS CDN 연결과 정규 REST 예제 설정(13주 config.json, 그 밖의 config.example.js·공개 키) 안내
│  ├─ tools/guestbook-api/            공용 API SQL·학생 안내·로컬 모의 API와 시험
│  ├─ tools/static-server/            로컬 미리보기 서버와 시험
│  └─ reviews/                        로컬 개편 기록(Git 제외, 116c8e8). 이 PC에는 없다
├─ open_source_ai/                    오픈소스 AI 응용
│  ├─ AGENTS.md · CLAUDE.md           과목 작업 지침
│  ├─ README.md · materials_plan.md · ta_setup_guide.md · uv_guide.md · github_distribution.md
│  ├─ weeks/weekNN_*/                 정규 15주
│  └─ specials/                       huggingface_hub·pytorch_basics·chatbot_rag_finetune·reasoning_tips(사이트), project_delivery(옛 10~13주 보존, 사이트 미등록), synthesizer(악보 JSON 2개만)
├─ tools/
│  ├─ pyproject.toml · LICENSE        PyPI 패키지 wleno 0.1.0(wleno/ + bleuno-control/src를 wleno.control로 묶음, 명령 wleno)
│  ├─ wleno/                          LAN 시뮬레이터 WlEno(main.py와 모듈 6개, tests/, examples/*.http, android/ AAR 프로젝트)
│  ├─ bleuno-control/                 WlEno 제어·평가·학습 Python 패키지(uv 프로젝트, tests/)
│  └─ github-classroom-pc-reset/      실습실 PC GitHub 로그인 정리(Windows·macOS·Linux, tests/)
├─ site/                              도서관 원본(index.html, course.html, assets/, catalog.json)
├─ scripts/                           render-site.mjs, check-site.mjs, deck-fit.test.mjs
├─ .github/workflows/                 pages.yml(main push 시 npm ci → build → npm test → Pages 배포), publish-wleno.yml(수동 실행, wleno-v* 태그 릴리스의 wheel·sdist를 PyPI Trusted Publishing으로 게시)
├─ package.json                       Node 24 이상, @marp-team/marp-core 4.4.0
├─ .gitattributes                     * text=auto eol=lf
└─ .gitignore                         config.json·config.js, .env(.env.example 제외), dist/, output/, node_modules/, .venv/, __pycache__/, *.egg-info/, build/, localfiles/, _localworks/
```

주차·특강 폴더 공통 구성: `README.md`, `slides.md`(Marp 한국어판), `slides_en.md`(영문판, 장 수·순서가 같다), `lab.md`, `examples/`. `walkthrough.md`는 Android·웹의 모든 주차와 오픈소스 AI 1·3·4·5·6·7·9·10·11·12·13주차에 있다. 평가 문서(`exam_structure.md`, `rubric.md`, `project_brief.md`, `assignment_brief.md` 등)는 평가 주차에만 있고, 파일 이름과 위치는 과목 지침에 있다. 세 과목의 `weeks/README.md` 주차 폴더 구성 표에는 아직 `slides_en.md`가 없다.

## Entrypoints and key modules

- 사람이 읽는 진입점: `README.md` → 과목 `README.md` → `weeks/README.md` → 주차 `README.md`
- 에이전트 진입점: 루트 `AGENTS.md` → 과목 `AGENTS.md` → `_forAI/README.md`
- 빌드 진입점: `scripts/render-site.mjs`. `site/catalog.json`의 `courses[].chapters[]`를 순회하며 `sourcePath(course, chapter)`로 원고 위치를 정한다. 매핑은 `android`→`android_programming/{weeks,specials}`, `web`→`web_programming/{weeks,specials}`, `open-source-ai`→`open_source_ai/{weeks,specials}`이고 `chapter.type`(`week`·`special`)이 폴더를 고른다. 같은 폴더에 `slides_en.md`가 있으면 영문판을 함께 만든다.
- 웹 예제 복사: 웹 슬라이드가 예제 HTML을 연결하면 `render-site.mjs`가 그 단원 `examples/`의 공개 파일과 `web_programming/shared/`를 함께 복사한다. 파일 목록은 `git ls-files --cached --others --exclude-standard`에서 고르고 숨김 파일, `reviews/`, `localfiles/`, `config.js`·`config.json`은 뺀다. 그래서 빌드에는 Git 체크아웃이 필요하다.
- 검증 진입점: `scripts/check-site.mjs`. 같은 `sourcePath` 매핑과 `EXPECTED` 상수(과목별 덱·장 수)로 `dist/`를 대조하고, 로컬 링크·`#앵커`·옛 주소 리다이렉트(`formerIds`)·로컬 설정 유출(`.git`, `.local`, `localfiles`, `config.js`·`config.json`, `.env`)을 검사한다. `config.example.js`는 공개 설정 파일이라 사이트에 복사된다(공개 키 값은 담지 않는다).
- 도서관 UI: `site/index.html` + `site/assets/library.{css,js}`가 전체 도서관, `site/course.html` + `site/assets/course.{css,js}`가 교재별 표지·목차, `site/assets/deck.{css,js}`와 `marp-theme.css`가 덱 화면이다. 교재별 배포 폴더는 `dist/android/`, `dist/webprg/`, `dist/open_source_ai/`이다.
- 비공개 짝 저장소: `univ_scoring_works/teaching_materials_private/`. 같은 주차 폴더 구조로 `lecture_script.md`, `lab_solution.md`, `_shared/practice_operation.md`(실습 운영 대본)를 둔다. 2026-11-12 기록으로는 비공개 `android_programming/`에 `tools/android_verify/`(`check_week.py`·`verify_rubric15_perm.py` 등), `tools/iot_sim/`(옛 `sim.py`용 `test_sim.py`), `iot_sim/lab_solution.md`가 있다. 새 11~15주 구조에 맞췄는지는 확인하지 않았다.

## Build and validation commands

```powershell
npm ci
npm run build      # node scripts/render-site.mjs → dist/
npm run check      # dist/ 사이트·링크 검사
npm run test:labs  # 웹 정적 서버·방명록 API·홈 IoT·Supabase 06 시험 + test:maps
npm run test:maps  # 지도 특강 앱 시험(web_programming/specials/kakao_aerial_map/examples/app)
npm test           # check + scripts/deck-fit.test.mjs + test:labs
```

- Node.js 24 이상이 필요하다(스크립트가 검사). 빌드는 Git 체크아웃에서 실행한다.
- 커밋 `d0ad054`의 기대값: 60개 덱, 한글·영문 각 1,219장(Android 20개·378장, 웹 21개·376장, 오픈소스 AI 19개·465장). 2026-11-25 Pages 워크플로의 빌드·`npm test`가 통과했다. 로컬 빌드 출력의 마지막 기록은 `8cc49ea`의 "59개 덱, 1185장, 상대 Markdown 링크 657개 변환, 자산 698개 복사"다. 과목별 기대값은 `scripts/check-site.mjs`의 `EXPECTED`에 있다.
- `render-site.mjs`의 `EXPECTED_DECKS`·`EXPECTED_SLIDES`와 `check-site.mjs`의 같은 상수, `EXPECTED[course]`는 정확한 수를 고정 검사한다. 장 수를 바꾸면 두 파일을 함께 갱신해야 빌드가 통과한다.
- 원고 검사 규칙: `theme: default`는 파일당 정확히 1회, raw HTML은 줄 끝 `<br>`·`<code>`·HTML 주석만 허용, 상대 `.md` 링크는 GitHub blob URL로, 상대 자산은 `dist/<교재>/decks/<단원>/assets/`로 복사된다.
- 영문판 장 수가 한국어판과 다르면 `경고: 영문판 장수가 한국어판과 다릅니다`만 출력하고 빌드는 계속된다.

## Tests

`npm test`와 `npm run test:labs`의 대상은 위 절에 있다. `test:labs`의 node 시험 파일은 `web_programming/tools/static-server/server.test.mjs`, `web_programming/tools/guestbook-api/server.test.mjs`, `web_programming/specials/home_iot_http/examples/simulator/server.test.mjs`, `web_programming/specials/supabase_guestbook/examples/06_http_lab/request.test.mjs`다. 2026-11-23 결과는 26개와 지도 시험 25개 통과다. 셸의 현재 경로가 소문자 드라이브(`c:\…`)이면 홈 IoT 시험 1개가 404로 실패한다. `C:` 경로에서 실행한다(plan 참고).

사이트 밖의 시험은 저장소 루트에서 실행한다. 모델·Ollama·실행 중인 시뮬레이터가 필요 없다.

| 대상 | 명령 | 2026-11-18 결과 |
|---|---|---|
| WlEno | `python -B -m unittest discover -s tools/wleno/tests` | 35개 OK |
| bleuno-control | `uv run --frozen --project tools/bleuno-control python -B -m unittest discover -s tools/bleuno-control/tests` | 15개 OK(`tools/bleuno-control/.venv` 생성) |
| 오픈소스 AI 14주 채점 도구 | `uv run --frozen --directory open_source_ai/weeks/week14_chatbot_project/examples python -B -m unittest discover -s tests` | 28개 OK(2026-11-19 평가셋 v1.1 뒤) |
| 오픈소스 AI 특강 `chatbot_rag_finetune` | `uv run --frozen --directory open_source_ai/specials/chatbot_rag_finetune/examples python -B -m unittest discover -s tests` | 89개 OK(2026-11-24, 과목 지침의 기록) |
| Python 문법 | `PYTHONPYCACHEPREFIX`를 저장소 밖 폴더로 둔 뒤 `python -m compileall -q open_source_ai tools/bleuno-control tools/wleno` | .py 214개 통과 |
| GitHub 로그인 정리 도구 | `tools/github-classroom-pc-reset/README.md`의 PowerShell 시험 3개 | 이번 기준일에 실행 기록 없음 |

- `ruff check --select E9,F63,F7,F82`를 돌릴 때는 일부러 깨뜨린 8주차 `examples/mock_exam/broken_project`와 `examples/period1/broken_project`를 뺀다. 두 `pyproject.toml`은 TOML 파싱이 실패하는 것이 정상이다.
- 브라우저에서 실제 Supabase 응답을 읽는 검증과 `.http` 요청 검증은 자동 단위 시험과 구분한다. 클라우드의 수정·삭제 권한과 Pages 게시 결과는 별도 확인 대상이다.
- Android 예제의 `assembleDebug`와 AAR 빌드(`tools/wleno/android`에서 `gradlew packageDistribution`)는 Android SDK가 필요하다. 새 11~15주 예제와 AAR 재빌드의 실행 기록은 아직 없다.
- Markdown 문서의 링크·앵커 검사 스크립트와 슬라이드·실습 시간 합계 검사 스크립트는 저장소에 없다. 빌드된 덱 HTML의 링크와 앵커만 `check-site.mjs`가 본다.

## Notes

- 강의 대본·실습 해답은 이 저장소에 두지 않는다(비공개 짝 저장소). 주차 README의 "강의 대본: 강의자 별도 관리(비공개)" 문구가 그 표시다.
- 수업 시간 구조는 과목마다 다르다. 값은 [memo의 수업 시간 구조](memo.md#기본-설정값)에 있다.
- 오픈소스 AI 예제의 `uv.lock`은 3·4주차 일부 교시와 5·6·7·9~14주차, 특강 4개(`huggingface_hub` 교시 3개, `pytorch_basics`, `reasoning_tips`, `chatbot_rag_finetune`의 `examples/`·`finetune/`), `tools/bleuno-control`에 커밋되어 있다. 10주차 lock은 PyPI의 `wleno==0.1.0`을 고정한다. `tools/wleno/uv.lock`은 `543ab2e`에서 삭제됐다.
- `dist/`는 빌드 산출물로 추적하지 않는다. `site/`가 원본이다.
- 2026-11-28 `d0ad054`의 CRLF 파일은 0개다. 새 파일도 LF로 저장한다. 비교 방법은 [memo의 저장소 공통 교훈](memo.md#저장소-공통-교훈)에 있다.

## 웹 REST 교재와 연구 특강

과목 작업 규칙과 함께 고칠 곳은 [web_programming/AGENTS.md](../web_programming/AGENTS.md)가 정본이다. 여기에는 위치와 실행 명령만 둔다. 정규 12~14주는 11주의 폼·객체·JSON·localStorage 학습을 서버 저장으로 확장한다. 13주 폴더만 `bd02eaa`에서 `week13_guestbook_crud`로 바꿨고(옛 `week13_release_security` 주소는 `formerIds`로 넘긴다) 다른 주차 폴더 이름은 유지한다.

| 자료 | 위치·역할 |
|---|---|
| 12주 타이머·공개 API GET | `web_programming/weeks/week12_fetch_json/`. 1일차 `ex01`(타이머 실행 순서), `ex01b_wait`(`wait` 함수와 `.then()`), `ex01c_async_await`(같은 순서를 `await`로), `ex01d_async_return`(`async` 함수가 돌려주는 Promise, `return`·`throw`), `ex02`·`ex03`(JSONPlaceholder 할 일 한 건을 `.then()`과 `await`로). 2일차 `ex04` 환율(Frankfurter), `ex05` 타로 카드 200·404, `ex06` 나라별 공휴일(Nager.Date, 주차 결과물), `ex07` 도시별 기온(Open-Meteo, 선택). `web-week12`는 홈 기온 조회(`weather.js`·`weather.http`), 브라우저 방명록(`guestbook.local.*`), 선택 서버 글 조회(`guestbook.html`·`config.example.js`)다 |
| 13주 방명록 CRUD | `web_programming/weeks/week13_guestbook_crud/`. `ex01_create`(POST) → `ex02_read`(GET) → `ex03_update`(PATCH) → `ex04_delete`(DELETE)와 완성 `web-week13`. 각 폴더에 `load-config.js`·`config.example.json`·`requests.http`·`.env.example`이 있다 |
| 14주 수정·삭제 결과 확인 | `web_programming/weeks/week14_project_presentation/` |
| 15주 누적 복습·개인 실기 | `web_programming/weeks/week15_final_exam/` |
| REST 예제 설정 | 13주는 `load-config.js`가 같은 폴더의 Git 제외 `config.json`(`config.example.json`을 복사해 주소·공개 키·`BOOK_ID`를 넣는다)을 읽고 `#config-status`에 상태를 쓴다(사본 5곳). 그 밖의 정본은 `weeks/week12_fetch_json/examples/day2/web-week12/config.example.js`이고 14주 4곳·15주 REST 문항 3곳·hash SPA 04에 같은 사본이 있다(정본 포함 9개, 14주 `day1/ex01`의 주석 안내 파일은 제외). 각 폴더에는 `requests.http`·`.env.example`·`README.md`도 있다. Git 제외 규칙은 루트 `.gitignore` 한 곳이다 |
| 강의자 서버 준비 | `web_programming/tools/guestbook-api/`. 새 프로젝트는 `schema.sql` → `about-help.sql`, 이미 쓰는 프로젝트는 `enable-public-crud.sql`(공개 키로 모든 태그 PATCH·DELETE 허용, 옛 `edit_key_hash` 열을 null 허용으로 바꿈). `provision.mjs`는 `bd02eaa`에서 지웠다 |
| 학생 요청 안내 | `web_programming/tools/guestbook-api/student-guide.md` |
| Supabase 구축 연구 | `web_programming/specials/supabase_guestbook/` |
| Node HTTP 홈 IoT 연구 | `web_programming/specials/home_iot_http/` |
| hash SPA | `web_programming/specials/hash_spa/`. 14주 뒤 선택 특강이며 정규 시험에 내지 않는다 |
| 배열 심화 | `web_programming/specials/array_advanced/`. 정규 시험에 넣지 않는다 |

Supabase `examples/` 루트에는 README만 둔다. 하위 `01_about`, `02_help`, `03_guestbook_get`, `04_guestbook_post`, `05_guestbook_edit`, `06_http_lab`, `07_guestbook_complete`는 각각 독립 실행·배포 폴더다. 각 폴더에 `index.html`, `app.js`, `config.example.js`, `requests.http`, `.env.example`, `README.md`가 있다. 06에는 `request.js`, `exercise.js`, 요청 시험이 더 있다. 특강의 `config.example.js` 7개는 서로 같고 정규 정본과는 주석·따옴표·묻는 문구가 다르다. 공용 API 주소는 공개 설정이며 `web_programming/tools/guestbook-api/README.md`와 각 폴더의 `config.example.js`·`config.example.json`·`.env.example`에 있다. 공개 키 값은 저장소 파일에 두지 않는다(브라우저 localStorage, 13주는 Git 제외 `config.json`, REST Client는 Git 제외 `.env`). 키 값은 `_forAI`에도 기록하지 않는다.

저장소 최상위에서 정적 미리보기를 실행한다. 포트는 비어 있는 번호를 쓴다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
node web_programming/tools/static-server/server.mjs web_programming/specials/supabase_guestbook/examples 8000
```

정적 서버는 `.env`·`.git`·`.local`·`localfiles` 경로에 403을 돌려준다. 공용 API 대신 로컬 리허설을 할 때만 별도 터미널에서 로컬 모의 API(`http://127.0.0.1:8787`, 데이터는 Git 제외 폴더 `.local/`)를 실행한다.

```powershell
node web_programming/tools/guestbook-api/server.mjs
node web_programming/specials/home_iot_http/examples/simulator/server.mjs
```

홈 IoT 화면은 `http://localhost:8014/`이다. 이 Node 시뮬레이터와 Android·오픈소스 AI가 쓰는 WlEno는 별도 자료다. 서버는 모두 터미널 프로세스이며 다음 세션에도 살아 있다고 가정하지 않는다.

## Android RoomControl과 WlEno

과목 작업 규칙, 예제 사본 관계, 함께 고칠 곳은 [android_programming/AGENTS.md](../android_programming/AGENTS.md)가 정본이다.

- 정규 11~15주 앱은 RoomControl(`com.example.roomcontrol`)이다. 학생은 GitHub Release의 `wleno-android-0.1.0.aar` 한 개를 압축을 풀지 않고 `app/libs/`에 넣는다. 설치 순서는 `tools/wleno/android/INSTALL.md`, API는 `tools/wleno/android/README.md`, 버전은 `tools/wleno/android/gradle.properties`의 `wlenoVersion`에 있다.
- 주소 규칙: WlEno와 같은 PC의 에뮬레이터는 `10.0.2.2:8266`, 다른 PC의 에뮬레이터와 실기기는 WlEno 실행 PC의 LAN IPv4와 포트 8266이다. 다른 기기에서 붙을 때는 TCP 8266 인바운드를 허용한다.
- WlEno 실행(프로토콜 버전 2.0.0, `543ab2e`): Android 문서는 `tools/wleno`에서 `python main.py`로 켠다. Python 3.10 이상의 표준 라이브러리와 Tkinter만 쓴다. 같은 코드가 PyPI 패키지 `wleno` 0.1.0(명령 `wleno`)으로도 배포된다. 창 없이 돌릴 때는 `--no-window`. 서비스는 TCP 8266(명령), UDP 8267(`bleuno?` 검색, 선택), HTTP `127.0.0.1:8080`(API)이다. 옛 `uv run main`·pygame-ce·`sim.py`는 `543ab2e`에서 지웠다.
- `android_programming/iot_sim/`에는 `lab.md`(RoomControl 수업 전 연결 점검)만 있다.
- `android_programming/bleuno/src/` 9개 파일은 보존 특강 전용이다. 사본 7곳은 `specials/legacy_week12_ble_gatt/examples/day1`·`day2`, `legacy_week13_ble_output/examples/day1`, `legacy_week14_ble_input_project/examples/day1`·`day2`, `legacy_week15_final_exam/examples/rehearsal_solution`·`rehearsal_starter`의 `bleuno/`다.
- 별도 저장소: 점검·시연 앱 `gbox3d/bleunoApp/BleunoTest`, 펌웨어와 type_m v1 마더보드 `gbox3d/bleuno`(`hardware/type_m/v1/`). 이 교재에 설계를 복제하지 않는다. type_m v1 원본 연결 근거는 그 저장소의 `hardware/type_m/v1/pinmap.md`에 있다.

## 오픈소스 AI 10~13주와 공용 도구

과목 작업 규칙과 전파 표는 [open_source_ai/AGENTS.md](../open_source_ai/AGENTS.md)가 정본이다.

- 10주 `examples/`는 PyPI의 `wleno==0.1.0`을 `uv sync --locked`로 설치한다. 시뮬레이터는 `uv run wleno --bind 127.0.0.1`, 제어는 `from wleno.control import Board`다. 학생용 ZIP은 주차 폴더에서 `uv run --python 3.12 python distribution/build.py --out-dir dist`로 만들고 릴리스 `wleno-v0.1.0`에 `week10-simulator-lab-0.1.0.zip`으로 올렸다. 설치 안내는 `distribution/README.md`다.
- 11~13주 `examples/pyproject.toml`의 `[tool.uv.sources]`는 여전히 상대 경로로 `tools/bleuno-control`을 가리킨다. 주차 폴더만 떼어 내면 실행되지 않으므로 저장소 전체를 복제한다. 13주는 12주 `examples/models/`의 학습 결과를 읽는다(`models/`는 Git 제외).
- 11주 문서는 시뮬레이터를 저장소 루트에서 `python tools/wleno/main.py --bind 127.0.0.1`로 켜게 한다. 12주 `examples/period1/README.md`는 상대 경로(`python ../../../../tools/wleno/main.py`)로 `--bind` 없이 실행한다.
- `wleno` 새 버전 게시: 저장소 루트에서 `uv build tools --out-dir dist`로 wheel과 sdist를 만들어 `wleno-v<버전>` 릴리스에 올린 뒤 그 태그에서 `publish-wleno.yml`을 수동 실행한다. 패키지 버전(0.1.0)과 시뮬레이터 프로토콜 버전(`protocol.py`의 `VERSION` 2.0.0)은 따로 센다.
- 특강 `chatbot_rag_finetune`: `examples/`(명령 `ex04`~`ex07`, `rag_bot`)는 14주 예제 프로젝트를 상대 경로로 설치하고, `finetune/`(`prepare`·`ft01`·`ft02`)은 7주와 같은 torch·transformers·peft 버전을 쓴다. 학습 산출물과 `finetune/tools/llama.cpp/`는 특강 루트 `.gitignore`로 막는다.
- `tools/bleuno-control`은 TCP 연결·명령 검증·평가 16문항(`control_cases.json`)·학습 도우미를 담은 uv 프로젝트다. Ollama 시스템 프롬프트는 `src/bleuno_control/models.py`에 있다.
