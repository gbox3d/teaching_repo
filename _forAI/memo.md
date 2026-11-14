# Memo

## 목차

- [제품 기준선](#제품-기준선)
- [기본 설정값](#기본-설정값)
- [런타임 구조 메모](#런타임-구조-메모)
- [동작 규칙](#동작-규칙)
- [릴리스 전 검증 항목](#릴리스-전-검증-항목)
- [반복 금지](#반복-금지)
- [웹 REST와 Supabase 운영](#웹-rest와-supabase-운영)
- [HTTP 홈 IoT 연구 기준](#http-홈-iot-연구-기준)
- [Android BLE 보드 연계](#android-ble-보드-연계)

## 제품 기준선

- 빌드 환경: Node.js 24, `@marp-team/marp-core` 4.4.0(`package-lock.json` 고정). GitHub Actions `pages.yml`이 main push마다 build → check → Pages 배포.
- 배포 주소: <https://gbox3d.github.io/teaching_repo/>
- 줄바꿈: `.gitattributes`로 전 파일 LF. Windows에서 파일을 만들 때 CRLF·BOM이 섞이지 않게 한다.
- 실습 기준 PC(오픈소스 AI): Windows + RTX 4070(12 GB). GPU 없는 PC용 CPU·소형 모델 대체 경로를 항상 둔다.

## 기본 설정값

오픈소스 AI 응용 예제의 환경변수 기본값(교재 검증용, 실제 값은 환경 기준표가 확정):

| 환경변수 | 기본값 |
|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` |
| `OLLAMA_MODEL` | `qwen3:8b` (CPU·소형 대체 `qwen3:0.6b`) |
| `OLLAMA_EMBED_MODEL` | `bge-m3` |
| `HF_TEXT_MODEL` | `Qwen/Qwen2.5-0.5B-Instruct` |
| `HF_EMBED_MODEL` | `intfloat/multilingual-e5-small` |

Qwen3 계열은 thinking 출력이 섞이므로 Ollama API 호출에 `"think": false`를 넣는다.

**생각 모드를 끌 수 있는 태그만 기본값으로 쓴다.** Qwen3에서 `0.6b`·`1.7b`·`8b`·`14b`·`32b`는 하이브리드라 `think`가 실제로 꺼진다. `4b`·`30b`·`235b`는 2507 갱신에서 instruct/thinking으로 갈렸고 **접미사 없는 태그가 생각 전용 빌드**를 가리켜 `"think": false`가 무시된다(2026-09-03 레지스트리 digest로 확인: `qwen3:4b` = `qwen3:4b-thinking-2507-q4_K_M`). 모델을 바꾸기 전에 이 구분을 다시 확인한다. 근거와 확인 절차는 `open_source_ai/weeks/README.md`의 「생성 모델 태그를 고를 때」에 있다.

수업 시간 구조:

| 과목 | 구조 |
|---|---|
| 모바일·웹 | 주 2회 × 90분, 매회 설명·시연 30분 + 실습 60분 |
| 오픈소스 AI | 60분 블록 × 3(1·2·3교시), 매 블록 설명·시연 20분 + 실습 30분 + 휴식 10분. 분반에 따라 2+1 또는 1+2로 이틀 배치 |
| 웹 연구 특강 | 방학 실습·연구. 분량·차시 수·총시간 제한 없이 단계별 결과를 확인 |

## 런타임 구조 메모

- `site/catalog.json`이 덱 목록의 단일 기준이다. 새 과목·주차를 공개하려면 (1) `catalog.json`에 chapter 추가, (2) `render-site.mjs`·`check-site.mjs`의 `sourcePath`에 폴더 매핑, (3) 두 스크립트의 `EXPECTED_*` 상수 갱신 순서로 한다.
- 슬라이드 수는 렌더된 HTML의 `<svg data-marpit-svg>` 개수로 센다. 원고의 `---` 줄 수와 다를 수 있으니(frontmatter 구분자 포함) 최종 값은 `npm run build` 출력으로 확정한다.
- `render-site.mjs`는 원고의 `<br>`(줄 끝)을 Markdown 줄바꿈 `\`로, `<code>`를 백틱으로 바꾼 뒤 남은 raw HTML이 있으면 빌드를 실패시킨다.
- 상대 `.md` 링크는 GitHub blob URL로 재작성되므로 원고에서 `lab.md#앵커` 링크를 써도 된다. 앵커 규칙은 GitHub 스타일(공백→`-`, 특수문자 제거, `—`가 빠지면 `--`가 남는다).
- 슬라이드에서 실행 예제 HTML·JS를 상대 링크로 넣으면 renderer가 파일만 복사해 설정·스타일 의존성이 빠질 수 있다. 코드·화면 소스는 GitHub 절대 링크로 제공하고, 실행은 예제 폴더 전체를 내려받거나 별도 Pages에 게시하는 절차로 안내한다. `.http` 다운로드 링크는 상대 경로를 쓸 수 있다.

## 동작 규칙

- 공용 교재에 학교명·분반·학수번호·실제 날짜·성적 비율·LMS 이름을 넣지 않는다. 루브릭은 100점 상대 배점만 둔다.
- 소프트웨어 정확 버전을 본문에 고정하지 않는다. 버전은 `environment_baseline_template.md`를 학기용으로 복사해 확정한다.
- 전역 `pip install`을 쓰지 않는다. Python 예제는 uv 프로젝트(`pyproject.toml`, 의존성 버전 미고정)이며 `uv.lock`은 기준 PC에서 생성해 커밋한다.
- 환경 설정은 `.env.example`에 자리표시자로 제공하고 실제 `.env`는 제외한다. Supabase의 브라우저용 publishable key는 공개 설정으로 사용할 수 있지만 편집 키·secret key·DB 비밀번호는 포함하지 않는다. 학생용 starter와 강의자용 해답을 물리적으로 분리한다.
- 모델 다운로드는 실습 시간에 하지 않는다(사전 캐시).
- 강의 대본(`lecture_script.md`)과 해답(`lab_solution.md`)은 `univ_scoring_works/teaching_materials_private/`에 둔다. 대본의 구간 제목·분 범위는 공개 `slides.md`와 같아야 한다.

## 릴리스 전 검증 항목

원고를 크게 바꾼 뒤에는 다음을 확인한다. 사이트·슬라이드 맞춤·웹 실습 시험은 저장소의 `npm test`를 사용하고 추가 문서 검사는 필요한 범위에서 수행한다.

1. 줄바꿈·인코딩: CRLF와 BOM이 없고 파일 끝 개행이 1개인가.
2. 실행 산출물: `.ruff_cache/`, `__pycache__/`, `outputs/`, `.venv/`가 포함되지 않았는가. `uv.lock`은 기준 PC에서 버전을 확정한 뒤 추적하는 계획과 구분한다.
3. 금지 문자열: 학교명, 분반, 학수번호, 성적 비율(%), 정확한 소프트웨어 버전, 토큰.
4. 시간 구조: 정규 주차는 과목별 시간 기준을 따른다. 오픈소스 AI는 설명 0–20분·실습 0–30분의 연속성을 확인한다. 웹 연구 특강에는 고정 시간 검사를 적용하지 않는다.
5. Marp 제약: `theme: default` 주차당 1회, raw HTML은 줄 끝 `<br>`·`<code>`·주석만.
6. 링크: 모든 상대 링크의 대상 파일과 `#앵커`가 실제로 있는가.
7. 코드: 모든 `.py`가 `py_compile`을 통과하고 `ruff check --select E9,F63,F7,F82`가 깨끗한가(8주차 `broken_project` 제외).
8. 루브릭: 배점 합계가 100인가.
9. 대본: `lecture_script.md`의 구간 제목·분 범위가 같은 주차 `slides.md`와 일치하는가.
10. 사이트: `npm run build`와 `npm test`가 통과하고 덱·슬라이드 수 상수가 맞는가.

## 반복 금지

- 슬라이드를 고친 뒤 `EXPECTED_SLIDES`를 안 고쳐 CI가 깨지는 일. 빌드 출력의 장 수로 두 스크립트를 함께 갱신한다.
- 다른 과목 표현("1일차", "90분", "30분 설명")을 오픈소스 AI 자료에 복사해 오는 일. 오픈소스 AI는 "교시", "20분·30분·10분"이다.
- 강의 대본을 공개 저장소에 커밋하는 일.
- `materials_plan.md` 초안의 `materials/` 챕터 구조를 되살리는 일. 주차 폴더 구조로 확정했다.
- 존재하지 않는 CLI 명령 이름(예: 버전에 따라 바뀐 Hugging Face 캐시 명령)을 본문에 고정하는 일. Python API로 쓰거나 `--help`로 확인하라고 안내한다.
- 모델 태그가 가리키는 빌드가 그대로일 것이라고 가정하는 일. 제공자가 같은 태그를 다른 빌드로 옮긴다. 태그에 의존하는 동작(생각 모드 on/off, 도구 호출, 컨텍스트 길이)을 가르칠 때는 레지스트리 digest나 `ollama show`로 실제 빌드를 확인한다.
- 학생용 실습지(`lab.md`)에 실측 결과를 정답처럼 적는 일. 실습지에는 예상·관찰 표와 힌트만 두고, 실측과 정답은 비공개 `lab_solution.md`에 둔다.
- 측정하지 않은 실행시간·VRAM·tokens/s를 사실처럼 적는 일. 확인할 수 없으면 자리표시자와 "기준 PC 실측값으로 채운다"로 둔다.

## 웹 REST와 Supabase 운영

- 정규 12주는 GET, 13주는 POST, 14주는 PATCH·DELETE다. 15주는 누적 문제은행 복습과 개인 실기를 유지한다. 레포트는 별도 공지하며 14주 검사 주차를 되살리지 않는다.
- 강의자가 준비한 서버를 학생 계정 없이 호출한다. Supabase 계정·SQL·키 등록은 구축 연구 특강의 담당자 작업이다. 특강 분량·회차·총시간은 제한하지 않는다.
- 공용 프로젝트는 `esoqbcwgzjtwcqszwvin`, 기본 주소는 `https://esoqbcwgzjtwcqszwvin.supabase.co`다. 공용 등록 확인 태그는 `student01`, `student02`뿐이다. 로컬 API의 student01~30 안내 글을 클라우드 등록 현황으로 오해하지 않는다.
- `book_id`는 분류·조회 조건이다. 공개 키로 다른 등록 태그의 조회·추가도 허용한다. 편집 키는 해당 방명록의 모든 글을 수정·삭제하는 권한이며 개인 작성자 인증이 아니다.
- 모든 요청은 `apikey`를 사용한다. GET·POST에는 편집 키가 없고 PATCH·DELETE에는 `X-Edit-Key`가 필요하다. 이름은 30자, 메시지는 500자이며 빈 입력·공백만 있는 입력은 거부한다.
- GET `/rest/v1/about`은 name·version·description·help_path 한 행을, GET `/rest/v1/help?order=step.asc`는 요청 안내 여섯 행을 배열로 반환한다. help의 요청 순서와 예제 폴더 01~07은 별개다.
- 새 프로젝트는 `schema.sql` 다음에 `about-help.sql`을 실행하고 `provision.mjs`로 태그·편집 키 해시를 등록한다. 기존 방명록이 있는 프로젝트는 설치 SQL 전체를 다시 실행하지 않는다. 안내 API만 추가할 때는 `about-help.sql`을 쓴다.
- `private.classroom_books`는 RLS를 켜고 클라이언트 허용 정책을 두지 않는다. 같은 소유자의 SECURITY DEFINER 함수가 편집 키 해시를 검사한다. `private`를 Data API 노출 스키마에 추가하지 않는다.
- POST 201은 저장된 행의 배열이다. PATCH 200의 빈 배열과 DELETE 204만으로 실제 변경을 판단하지 않는다. book_id·id로 같은 글을 GET해 확인하고 204에 JSON 파싱을 하지 않는다.

Supabase 예제는 루트 README와 독립 폴더 01~07로 구성한다. 06은 메서드·본문을 바꾸는 실험 화면, 07은 등록 폼·목록·선택 편집을 갖춘 완성 방명록이다.
각 폴더의 `.env`는 REST Client의 `requests.http` 전용이다. 브라우저는 같은 폴더의 `config.example.js`를 HTML의 `defer` 스크립트로 먼저 읽는다. 한쪽 설정을 바꾸어도 다른 쪽은 자동으로 바뀌지 않는다.
REST Client의 `{{$dotenv ...}}`는 `.http`와 같은 폴더의 `.env`를 읽는다. 편집 키는 password prompt로 입력하지만 요청 이력에는 헤더·본문이 남는다. 공유 전 값을 확인하고 실습 후 **Rest Client: Clear Request History**로 정리한다.
API 예제를 만들 때 `.http`와 `.env.example`을 함께 제공하는 규칙은 `C:\Users\gbox3\.codex\AGENTS.md`에도 기록되어 있다. 이 전역 파일은 교재 저장소 밖에 있다.

`localfiles/`, `.local/`, 실제 `.env`, 편집 키·비밀번호는 Git과 배포 ZIP·Pages에서 제외한다. `_forAI`에도 키 값을 복사하지 않는다.
로컬 HTTP 화면이 공용 HTTPS API를 호출할 수 있으며 페이지 주소는 HTTP로 유지된다. 브라우저 CORS와 REST Client 성공은 따로 검증한다. 각 폴더를 Pages에 게시할 때는 화면과 API 모두 HTTPS를 사용한다.
2026-11-14 확인 범위는 공용 about·help GET 200(1행·6행), localhost의 01·02 브라우저 조회, 방명록 GET·POST다. 공용 PATCH·DELETE 권한과 예제의 Pages 실배포는 미검증이다.

## HTTP 홈 IoT 연구 기준

`web_programming/specials/home_iot_http`는 Node.js 서버와 웹 UI로 가상 장치를 제어한다. 학생 PC의 `http://localhost:8014/`에서 GET·PATCH, 주기 조회, 단일 기준·26/29°C 히스테리시스, 통신 실패·복구를 비교한다.
온도는 수동으로 정하는 모의 값이고 팬이 실내 온도를 낮추는 물리 모델은 없다. 실제 냉각 성능이나 센서 정밀도를 측정한 것으로 기록하지 않는다.
상태와 제어 기록은 메모리에서 관리하며 서버 재시작 시 초기화된다. Android용 Python Wi-Fi 시뮬레이터와 코드를 섞지 않는다.

## Android BLE 보드 연계

- SmartIO + `android_programming/bleuno/src`를 수업 정본으로 유지하고, `bleunoApp/BleunoTest`를 강의자·조교의 점검·시연용으로 사용한다.
- 교재·점검 앱·펌웨어에서 Service UUID `c6f8b088-2af8-4388-8364-ca2a907bdeb8`, Characteristic UUID `f6aa83ca-de53-46b4-bdea-28a7cb57942e`가 일치한다. 현재 확인 범위는 소스 비교이며 실기 검증은 미완료다.
- 교재 GPIO `[4,3,1,0]`은 기존 수업의 `ledpin` 설정이다. 원본 type_m v1은 모터·서보용이며 GPIO0=CHKBAT, GPIO7=SLEEP이라 이 설정과 `dht11pin=7`을 그대로 적용하면 충돌한다. 모델명 `type_m`, 하드웨어 버전 `v1`, 펌웨어 `1.0.5_dev`는 별도로 관리한다.
- type_m v1 원본 회로도·PCB의 12부품·52핀 네트 매핑을 대조했다. SEN1은 MCU에 연결되지 않고 VIN은 전원 헤더 pin3에만 존재한다. KiCad 이전과 원본 대조는 완료했으며 전기적 미연결·모듈 핀 표기·실기 확인은 남아 있다. 근거는 `bleuno/hardware/type_m/v1/pinmap.md`다.
- 펌웨어 소스(`gbox3d/bleuno` main, `ble.cpp`)는 연결될 때 외부 제어 LED를 모두 끈다(`onConnect`의 `ledOff(-1)`). 끊길 때는 LED와 밝기를 모두 끈다(`onDisconnect`의 `clearAllControl()`). TENSTAR 빌드는 연결 중 내장 상태 LED가 파랑 고정이다. 실제 보드와의 대조는 아직 하지 않았다.
- 펌웨어 `onWrite`는 길이 0인 명령을 건너뛴다. 그래서 빈 줄에는 응답이 없다. `RealBleunoClient`·`TcpBleunoClient`는 `send("")`에 `\n`을 보내고, Fake는 보내기 전에 거른다.
- 버튼 입력 이벤트는 Fake용 가안이며 현재 펌웨어가 실제로 전송하는 이벤트가 아니다. Wi-Fi 시뮬레이터는 화면 [입력 버튼]을 누를 때만 보낸다(교수 결정 2026-11-12).
- 공통 클래스를 수정할 때는 함께 고치는 곳이 있다. `check_week.py`(비공개 `android_programming/tools/android_verify/`)는 주차 `examples/`의 .kt·.xml 전문과 같은 코드 블록이 walkthrough에 없으면 경고(WARN)만 낸다(문제 0건이면 종료 코드 0). 정본 `bleuno/src`와는 대조하지 않는다. 그래서 정본과 복사본 7곳이 같은지는 sha256(또는 `cmp`)으로 따로 본다.
  - 복사본 7곳: 12주차 1·2일차, 13주차 1·2일차, 14주차 1일차, 15주차 rehearsal_solution·rehearsal_starter
  - 12~15주차 `walkthrough.md` 부록의 전문
  - 파일 수를 적은 주차 문서("9개")
  - `bleuno/README.md`의 파일 수('9개')·3절 파일 표·5절 API 표
  - `iot_sim/lab.md` 2-1의 `createTcp()` 코드 블록
  - 비공개 12~15주차 대본·해답과 `course_plan_2026.md` §5
  - 파일 수에서 나온 총수(15주차 '나머지 N개', 'N개 파일')
- Wi-Fi 시뮬레이터(`iot_sim/`)와 `TcpBleunoClient.kt` 사이의 약속은 다음과 같다. 한쪽을 바꾸면 다른 쪽도 고친다.
  - 명령 TCP 8266, 검색 UDP 8267(`bleuno?` → `{"name","port"}`)
  - 연결 직후 시뮬레이터가 먼저 보내는 `hello` 한 줄(앱은 첫 줄을 받으면 준비됨. hello 줄은 `onMessage`로 넘기지 않는다)
  - 기본 이름 `ESP32_BLE_SIM1`(예제 목록은 이름이 `ESP32_BLE`로 시작하는 장치만 보인다)
- 화면 HTTP 8080(`/state`·`/set`·`/input`·`/drop`)은 `sim.py` 자체 화면과 비공개 `tools/iot_sim/test_sim.py`가 쓴다. 바꾸면 `test_sim.py`를 같이 고친다. 포트 번호 8080은 `TcpBleunoClient.kt` 232행 주석과 실습지 8번에도 나온다.
- 시뮬레이터의 `dht11`은 화면 슬라이더 값이다(Fake는 세 값 반복). 연결·해제 때 LED를 끄고 빈 줄에 답하지 않는 것은 펌웨어와 같다. 펌웨어가 바뀌면 `sim.py`, `iot_sim/README.md`, `iot_sim/lab.md` 6번 차이 표와 막혔을 때 'LED가 저절로 모두 꺼짐' 줄, `bleuno/README.md` 1·10절, 비공개 `test_sim.py`와 `iot_sim/lab_solution.md` 결정 표를 같이 본다.
- 앱의 LED Switch·밝기 막대는 앱이 보낸 명령만 기억한다. 보드나 시뮬레이터가 스스로 LED를 끄면 화면과 어긋날 수 있다. 어느 화면에서 어긋나고 어느 화면에서 맞는지는 실습지 7번 표 2의 관찰 항목이라 여기 적지 않는다. 측정 기록과 정답은 비공개 `teaching_materials_private/android_programming/iot_sim/lab_solution.md`(결정 3과 실제 화면 흐름, 7번 표 2)에 있다. 실습지 7번이나 이 항목을 고칠 때는 그 기록부터 본다.
