# Dev Log

## 목차

- [Entries](#entries)

## Entries

최신 날짜가 위에 온다. 2026-11-18의 두 항목은 나중에 한 일(지침 정비)을 위에 두었다.

### 2026-11-28 — 원격과 동기화하고 `_forAI`를 `d0ad054`에 맞춤

- 사용자 요청: 저장소를 정리하고 원격과 동기화한다.
- 상태: `git fetch --prune` 뒤 로컬 main과 `origin/main`이 같았다(`d0ad054`). 커밋 안 된 변경은 2026-11-23에 고친 `_forAI` 5개 문서뿐이었다. 그사이 다른 세션이 커밋 7개를 올려(아래 항목), 그 문서들이 `8cc49ea`를 현재로 적고 있었다.
- 고친 것: README 스냅샷(60개 덱·1,219장, 과목별 변경), inventory(13주 폴더와 설정 파일, `config.example.js` 사본 9개, 서버 준비 SQL, `wleno` 패키지·게시 워크플로, 10주 PyPI 설치, 특강 `chatbot_rag_finetune`), memo(두 설정 방식, 편집 키 폐지 뒤의 권한, `wleno` 배포), plan(웹 1~4·10·12·13·16번 갱신, 18·19번 추가, 오픈소스 AI 7·8번, 공용 10번 브랜치 정리, 구조 결정과 위험).
- 확인: 릴리스 `wleno-v0.1.0`과 PyPI `wleno` 0.1.0 게시, `d0ad054`의 Pages 워크플로 성공을 GitHub에서 봤다. 작업 트리 CRLF 0개. 로컬 빌드와 시험은 다시 돌리지 않았다(교재 파일을 바꾸지 않았다).
- 정리하지 않은 것: Git 제외 폴더 `dist/`(빌드 산출물)와 `output/`(강의 영상 작업 산출물)은 그대로 두었다.
- 브랜치 정리(사용자 지시): main에 합쳐진 것을 확인하고 열린 PR이 없는 것을 본 뒤 `dev/android/blueno`(로컬·원격, `4bd8fcf`)와 원격 `docs/week01-git-status-slides`(`974d11d`)를 지웠다. main에 없는 커밋이 있는 `fix/github-classroom-reset-windows`는 남겼다(plan 공용 10번).

### 2026-11-24~25 — 다른 세션의 커밋(기록 보충)

`git log 8cc49ea..d0ad054`로 보충했다. 작업 세션의 판단 근거는 이 저장소에 없다.

- 2026-11-24 `f246e24` 오픈소스 AI 기말 챗봇 개선 특강 `chatbot_rag_finetune`(내 평가 문항과 실패 분류, 임베딩 RAG, 학습 예시와 LoRA 학습·등록, 추론 버그 잡기 4교시, 시험 89개, 60개 덱·1,218장).
- 2026-11-25 `bd02eaa` 웹 12주 공개 API(환율·타로·공휴일)와 13주 방명록 CRUD. 13주 폴더를 `week13_guestbook_crud`로 옮기고 옛 주소를 연결했다. 13주는 `config.json`을 읽고, 편집 키를 없애 공용 공개 키와 학생별 태그로 수정·삭제하게 했다(`enable-public-crud.sql` 추가, `provision.mjs` 삭제). 14·15주·hash SPA·Supabase 특강도 맞췄다.
- 2026-11-25 `e513180` 웹 12주 선택 예제 `ex07` 도시별 기온과 슬라이드의 전체 API 주소(60개 덱·1,219장).
- 2026-11-25 `b3f25da` WlEno 시뮬레이터와 BLEuno 제어 라이브러리를 PyPI 패키지 `wleno`로 묶고 게시 워크플로를 더했다. `378745a`·`b821770`·`d0ad054` 오픈소스 AI 10주 예제와 한영 슬라이드를 설치판에 맞추고 학생용 ZIP을 만들었으며, 최종적으로 ZIP과 저장소 예제 모두 PyPI의 `wleno`를 설치하게 했다.

### 2026-11-22~23 — 웹 설정 패널 삭제, 공개 키 localStorage와 지우기 버튼, 12주 타이머 예제

- 사용자 요청: `shared/api-settings.js`가 교재로 나쁜 예제인지 판단한 뒤 지운다. 공개 키는 localStorage에 저장한다(학기 말 키 교체 전제). Console 명령 대신 처음 열 때 `prompt`로 묻고, 화면에 지우기 버튼을 둔다. Supabase 특강도 같은 방식으로 바꾼다(나중에 로그인 기능을 배울 때 같은 원리라는 이유). 12주 1일차에 타이머로 `async`/`await`를 보여 주는 예제와 `async` 함수 설명을 더한다.
- 판정: 작업에 참여하지 않은 검토 셋(학습 설계·코드 설계·존재 이유)에 결론을 알리지 않고 맡겼다. 둘은 나쁜 예제, 하나는 고쳐 써야 하는 예제로 판정했다. 근거는 다음과 같다.
  - 실행 중에 다시 적용되는 전역 때문에 호출부 10개 파일에 `settingsVersion`·`requestVersion` 검사가 87줄 퍼져 요청 → `await` → 화면 반영 흐름을 가렸다.
  - 새로고침하면 설정이 사라져 13주의 '서버 저장은 새로고침 뒤에도 남는다'를 거꾸로 보여 줬다.
  - HTML `value` 유무에 따른 숨은 분기로 14·15주·hash SPA는 로컬 주소로 시작해 첫 GET이 실패했다.
  - 지키려던 공개 키는 이미 특강 `config.example.js` 7곳에 공개돼 있었다.
- 1단계(여러 에이전트, 루트 `AGENTS.md` 방식): 단위 6개를 동시에 고치고 독립 검증으로 채점했다. 이 단계의 공개 키는 Console 저장 방식이었다.

| 단위 | 회차 | 점수 |
|---|---|---|
| 12주 선택 방명록·공통 문서 | 1 | 9.0/10 |
| 13주 | 2(1회차 8.7, 필수 수정 1건 → 재작업) | 9.7/10 |
| 14주 | 1 | 9.5/10 |
| 15주 | 1 | 9.5/10 |
| hash SPA | 1 | 9.6/10 |
| 12주 타이머 예제 | 1회차 8.9(필수 수정 1건 → 재작업). 2회차 검증은 사용자 지시로 중단했고 총괄이 필수 수정 반영과 동작을 직접 확인했다 | — |
| Supabase 특강 문서(Console 방식) | 1 | 9.4/10 |

- 2단계(사용자가 고른 `prompt` 방식과 지우기 버튼): 총괄이 정규 `config.example.js` 정본과 사본 15개, 특강 7개, 화면 22곳의 **공개 키 지우기** 버튼을 직접 적용했다. 문서는 단위별 에이전트 6개가 고쳤다. 이 단계는 독립 채점을 거치지 않았고, 총괄이 정적 검사·빌드·브라우저로 확인했다.
- 결과(`8cc49ea`):
  - 12~15주·hash SPA의 `api-settings.js`와 패널, 설정 변경 대비 코드를 지웠다. 목록 화면은 열 때 첫 조회를 한다.
  - 공개 키는 파일에 두지 않는다. 키가 없으면 묻고 저장하며, 취소·빈 칸이면 저장하지 않는다(401). 지우기 버튼은 키를 지우고 새로고침한다.
  - 특강 문서에 로그인 원리 연결을 넣었다. 토큰 저장 → 요청 헤더, 지우기 = 로그아웃이고, 공개 키와 토큰의 차이도 적었다.
  - 12주에 `ex01b_wait`·`ex01c_async_await`·`ex01d_async_return`을 더하고 1차시를 다시 나눴다. 12주 덱이 4장 늘었다.
  - 문서, `AGENTS.md` 결정 기록, 장 수 상수를 함께 고쳤다.
- 확인:
  - `npm run build`: "교재 도서관 빌드 완료: 59개 덱, 1185장 (영문판 59개 덱, 1185장)". `npm test` 통과, `test:labs` 26개, 지도 25개.
  - 바꾼 JS 구문 검사, 사본 해시(정규 15개·특강 7개 각 한 종류), 실제 키 값 0건, 패널 흔적 0건, LF, 절대 경로 0건.
  - 원격 디버깅 Chrome(저장소 밖 임시 프로필)으로 확인했다. 실제 창으로 묻기·취소 → 401·새로고침 → 다시 묻기·지우기 → 다시 묻기를 봤고, `prompt`를 바꿔 끼운 대표 화면 13개에서 GET·오류 0·375px 넘침 없음을 봤다. 타이머 3개는 0·1·2초 출력과 기다리는 동안의 클릭을 확인했다.
  - push와 Pages 배포가 성공했고, 새 파일의 HTTP 200을 확인했다.
- 확인하지 못한 것: 공용 PATCH·DELETE 권한, Pages 화면에서의 조회, 휴대폰, Supabase publishable key 교체 절차(공식 문서에 없음).
- 남긴 문제는 plan의 웹 1·10~17번과 공용 7~9번에 있다. 비공개 짝 저장소(12주 대본 1차시 구간, 13~15주·특강의 키 입력 절차, 15주 채점·감독 안내)는 고치지 않았다.

### 2026-11-19~22 — 다른 세션의 커밋(기록 보충)

`git log --since='2026-11-18 21:00'`로 보충했다. 작업 세션의 판단 근거는 이 저장소에 없다.

- 2026-11-19 `da9403b` 오픈소스 AI 7주 GGUF 파일 확인과 로컬 Ollama 모델 등록 절차 구분, `3b61866` 기말 챗봇 공개 평가셋·사실별 출처 채점 v1.1, `9d42398` 9주 앱을 Streamlit 공식 명령으로 실행.
- 2026-11-19 `543ab2e` WlEno 2.0.0과 Android·오픈소스 AI 반영, `393c757` 웹 C01 개편, `dda441c` 저장소 지침과 `_forAI`(2026-11-18 작업 트리의 미커밋 변경을 세 묶음으로 커밋), `b2448d8` 오픈소스 AI 지침을 9주·14주 평가셋 v1.1에 맞춤.
- 2026-11-20 `97aa3cd` 9주 Streamlit 채팅·RAG의 빈 답변 처리와 대화 이력, `f5d0dc1` 추론 원문 관찰·답변 복구 복습 특강 `reasoning_tips`(오픈소스 AI 18개 덱·432장, 전체 59개 덱·1,181장).
- 2026-11-22 `b1d2aa4` 웹 W3.CSS 예제와 12·13주 비동기 GET·방명록 POST 실습 정리(`shared/examples.css`와 예제별 `.gitignore`·`styles.css` 정리), `116c8e8` 웹 `reviews/`를 Git 추적에서 제외.

### 2026-11-18 — 저장소·과목 에이전트 지침 정비와 _forAI 갱신

- 사용자 요청: 저장소 전체 갱신 내용을 정리해 문서에 기록하고, 새 에이전트가 쓸 지침을 만든다. 과목마다 별도 작업 에이전트가 독립적으로 작업하고, 독립 검증 에이전트가 10점 만점으로 채점해 7점 이상이면 통과, 미달이면 다시 작업하게 했다.
- 작업은 2026-11-18 21시 작업 트리(커밋 `5f701e7`과 커밋 안 된 변경)를 복사한 사본에서 했다. 사본에는 git 원격이 없다. 이 결과 파일을 원래 작업 트리로 옮길지와 커밋 여부는 사용자가 정한다.
- 과목 결과는 세 과목 모두 1회차에 통과했다. 통과 뒤 총괄이 검증이 남긴 고칠 점(must_fix) 가운데 지침·`_forAI`의 사실 오류를 실물과 대조해 바로 고쳤다(아래 '통과 뒤 반영'). 교재 본문의 문제는 `plan.md` 과목별 절에 남겼다.

| 과목 | 만든 파일 | 회차 | 점수 |
|---|---|---|---|
| Android | `android_programming/AGENTS.md`(새로), `android_programming/CLAUDE.md` | 1 | 7/10 |
| 웹 | `web_programming/AGENTS.md`(커밋 안 된 C01 수정판 예제 지침을 과목 전체 지침으로 다시 씀), `web_programming/CLAUDE.md` | 1 | 8/10 |
| 오픈소스 AI | `open_source_ai/AGENTS.md`(기존 규칙을 보존하고 구조·전파·검증·보고 절 추가), `open_source_ai/CLAUDE.md` | 1 | 8/10 |

- 통합: 루트 `AGENTS.md`(저장소 지도, 공개 저장소 규칙, 사이트 빌드·검증, 여러 에이전트 작업 방식과 채점 루브릭)와 `CLAUDE.md`(`@AGENTS.md` 한 줄)를 새로 만들고 `_forAI` 5개 문서를 갱신했다. 통합 결과도 독립 검증에서 1회차 8/10으로 통과했다.
- 통과 뒤 반영(검증 지적을 실물과 대조한 뒤 고침):
  - Android 지침: 채점표 배점(100점 → 8주 20점, 13주 10+20점, 15주 20점), 말투(슬라이드는 덱의 기존 말투, 1~10주 합쇼체·11~15주 해라체), 권한 규칙 범위(정규 11~15주), 새 파일 줄바꿈 확인 명령(`-o --exclude-standard`), 슬라이드 구간 제목 형식 차이.
  - 웹 지침: walkthrough 인용 범위(4~6·11·12·14주 전문, 7·9·10·13주 구역), 9주 → 15주 `w09_readme_links` 사본 관계, 11~14주 `styles.css` 결정 전 행동, `_forAI`와 다를 때의 우선순위.
  - 오픈소스 AI 지침: 생성 모델 기본값 두 갈래(`qwen3.5:2b`·`qwen3:8b`, 8주차 혼재), 시험 명령의 `-B`와 `PYTHONPYCACHEPREFIX`.
  - `_forAI`: 웹 15주 채점표 20점, 8주차의 `OLLAMA_MODEL`·모델 표, 이전 plan의 비공개 확인 항목 두 가지 복원.
- `_forAI` 정리 내용:
  - README 스냅샷을 2026-11-18 작업 트리 기준(58개 덱·1,175장, 과목별 구조, 미커밋 표시)으로 바꿨다.
  - inventory에 `tools/`, 과목 지침, 특강·개편 기록 폴더, 새 시험 명령을 넣었다.
  - memo의 Android 서술을 보존 특강과 공용 시뮬레이터 WlEno로 나눴다.
  - plan 11번(`dev/android/blueno` 병합)은 `6af3108`에서 끝나 지웠다.
  - 공개 저장소 규칙에 맞게 `_forAI`에서 작업 PC 절대 경로와 Supabase 프로젝트 주소를 지웠다. 주소는 교재의 설정 파일을 가리키게 했다.
  - dev_log의 2026-09-02 항목을 2026-09-03 두 항목 아래로 옮겨 최신순을 맞췄다.
- 검증: 바꾼 7개 문서의 문체 검사(`check_doc_style.py`) 위반 0건, 절대 경로 검색 0건. WlEno 시험 `python -B -m unittest discover -s tools/wleno/tests` 35개 OK를 통합 단계에서 다시 확인했다. 사이트는 총괄이 같은 작업 트리에서 실행한 결과("교재 도서관 빌드 완료: 58개 덱, 1175장 (영문판 58개 덱, 1175장)", `npm test` 통과)를 썼다.
- 커밋하지 않았다.

### 2026-11-18 — Android 11~15주 LAN 시뮬레이터 전환, 웹 7·11주 커밋, 미커밋 웹 C01·WlEno 2.0.0

2026-11-13 이후 커밋과 21시 작업 트리를 `git log --since='2026-11-13 00:00'`, `git status --porcelain -uall`, `git diff HEAD --stat`으로 대조했다. 11-13·11-15의 커밋은 아래 해당 날짜 항목에 보충했다.

Android 커밋(11-18):

- `738c81f`(01:11): 정규 11~15주를 새 앱 RoomControl(`com.example.roomcontrol`)과 PC 시뮬레이터 수업으로 바꿨다. 11주 주소 입력·연결·책상 조명, 12주 조명 선택·밝기, 13주 장면 점검과 계획안 발표, 14주 온습도·호출 입력 이력, 15주 기말 실기다. 옛 11~15주(연락처·BLE)는 `specials/legacy_week11~15`의 특강 1~5(109장)로 옮겼고, 옛 주차 id는 새 정규 주차의 `formerIds`로 남겼다. 통신 코드는 `tools/wleno/android/` Gradle 프로젝트가 만드는 `wleno-android-0.1.0.aar` 한 개로 제공한다. `tools/bleuno-sim`은 `tools/wleno`로 옮기고 `pyproject.toml`·`uv.lock`을 더했다(`uv run main`). `iot_sim/lab.md`는 RoomControl 수업 전 연결 점검으로 다시 썼다. 사이트의 Android는 15개 덱·305장에서 20개 덱·378장이 됐다. 같은 커밋에 오픈소스 AI 12개 파일의 시뮬레이터 경로 변경이 들어 있다.
- `df20c68`(01:33): 주소 규칙(같은 PC의 에뮬레이터 `10.0.2.2:8266`, 다른 PC·실기기는 WlEno 실행 PC의 LAN IPv4와 8266)과 AAR 설치 순서(압축 해제 없이 `app/libs/`, Gradle Sync)를 문서 25개에 맞췄다.

웹 커밋(11-18):

- `17fa624`(01:30): 11주를 강의·시연 60분 + 실습 30분과 문자열 → JSON → 폼 저장 순서로 줄였다. 배열 삽입·삭제·순회·filter·map·reduce를 `specials/array_advanced/`(예제 5개)로 분리했다. W3.CSS cdnjs 4.1.0, `shared/examples.css`·`shared/README.md`, 과목 `AGENTS.md`(예제 작성 규칙)를 처음 두었다. 웹은 19개 덱·339장에서 20개 덱·353장이 됐다.
- `5f701e7`(21:01): 7주를 W3.CSS 반응형 메뉴·카드·모바일 타임라인과 최신 글이 위에 오는 방명록 피드로 개편하고, 9주 완성본을 같은 내용으로 맞췄다.

커밋 안 된 변경(21시 기준 수정 450, 삭제 27, 새 파일 358. 새 파일 358개는 새 항목 221개를 `-uall`로 펼친 수):

- 웹 C01 개편(`web_programming` 수정 380, 삭제 24, 새 파일 341): 독립안 9개 중 C01을 골라 15주와 특강 6개에 반영했다. 일반 27차시를 60+30으로 통일하고, 12~14주에 설정 패널 `shared/api-settings.js`(값은 메모리에만)와 예제별 `requests.http`·`.env.example`을 두었다. 13·14주 방명록 동작을 `guestbook.js` 하나로 모으고 15주 문제은행을 13문항으로 재구성했다. SPA는 14주 뒤 선택 특강 `specials/hash_spa/`(한영 각 18장)로 신설했다. 정적 서버는 `.env`·`.git`·`.local`·`localfiles`를 403으로 막는다. 개편 기록은 `reviews/2026-11-18-course-audit/`(96개 파일)에 있고, 최종 독립 심사는 9.0·8.9·9.3이다.
- 루트(웹 개편에 딸림): `render-site.mjs`가 웹 슬라이드에 연결된 단원의 예제 의존 파일과 `web_programming/shared`를 함께 복사한다. `check-site.mjs`는 로컬 설정 유출을 검사하고 기대값이 58개 덱·1,175장(웹 21개·371장)이 됐다. `package.json`의 `test:labs`에 정적 서버 시험과 `test:maps`가 들어갔고, `catalog.json`에 hash SPA와 웹 주차 설명 수정이 들어갔다.
- WlEno 2.0.0(`tools/wleno` 수정 3, 삭제 3, 새 파일 17): 단일 `sim.py`·`pyproject.toml`·`uv.lock`을 지우고 `main.py`와 모듈 6개, 시험 35개, REST Client 예제 `examples/01~05`를 더했다. 실행은 `python main.py`(Python 3.10 이상, Tkinter, 추가 패키지 없음)다. TCP 연결·해제가 LED·센서 상태를 초기화하지 않고, 잘못된 정수·번호·밝기는 요청 전체를 거부한다. 2026-11-12 결정(연결·해제 때 LED 끄기)을 바꾼 것인데 결정 출처는 저장소에 없다.
- WlEno 반영: Android 범위 27개 파일(11·12·14·15주 실행 명령, 상태 유지 서술, 11~15주 `MainActivity.kt` 9곳의 `binding.addressEdit.error = null`, `bleuno/README.md` 10절, `ta_setup_guide.md`)과 오픈소스 AI 32개 파일(10~13주 실행 명령 `python tools/wleno/main.py --bind 127.0.0.1`, LED 유지 서술, `materials_plan.md` 10절, 10주 `ex01_manual`·13주 `ex03_app`의 연결 끊김 처리)을 고쳤다. `tools/bleuno-control`은 README에 시뮬레이터 실행 절을 더하고 `Board` docstring과 Ollama 시스템 프롬프트(두 문장)를 고쳤다.
- 확인한 것(과목 담당): WlEno 시험 35개, bleuno-control 시험 15개, 오픈소스 AI 14주 채점 도구 시험 23개, `compileall`(.py 214개), 웹 `npm run test:labs`(26개와 지도 시험 25개), 바꾼 웹 JS·MJS 115개 `node --check`, `api-settings.js` 사본 22개 동일. 하지 않은 것: Android 예제 빌드와 AAR 재빌드, 실기기·학교 Wi-Fi, Ollama·Needle·GPU 실행, 공용 API 쓰기, Pages 배포, 비공개 짝 저장소 대조.

### 2026-11-16 — 강의 영상 제작·게시 인수인계 정리

- [강의 영상 인수인계](lecture-video.md)를 추가하고 README·inventory·memo에서 연결했다. 재사용 절차와 범용 검사기는 `myAISkills`의 `lecture-video-editing` 스킬에서 관리하고, 이 저장소는 교재 대응과 로컬 작업 기록의 진입점을 제공한다.
- 조용한 발화 보호, 자막만 수정할 때의 원천 데이터·mux 갱신, 최종 프로젝트와 렌더 검증 범위, 게시 후 실제 화면·설정 재열기 등 검증한 방법을 스킬에 정리했다. 영상과 비공개 LMS 증거는 기존 제외 경로에 유지한다.
- 문서 정합성과 지침 유용성은 작성에 참여하지 않은 담당자가 각각 평가했다. 각각 7점 초과, 7점 이하 반려, 어느 평가든 5회 반려 시 중단하는 이번 요청의 기준을 기록했다. 1회차 결과는 정합성 9.0/10·유용성 8.8/10으로 모두 통과했고 반려는 각각 0회다. 권고한 참고 목록·파일 경로·검사 범위·보존 비교 예시도 보완했다.
- 변경 문서의 목차·로컬 링크·앵커·UTF-8/LF와 diff를 검사했다. `myAISkills`의 스킬 구조 검사, 검사기 실제 실행(17개 통과·전체 디코딩은 미실행), 최종 스킬 8파일의 현재 설치본 일치를 확인했다. 전체 디코딩은 동일 해시의 이전 근거를 재사용했다. 상세 검토 보고서는 `output/workflow_docs_review_2026-11-16/`에 있으며 Git 제외다.
- 교재·사이트의 2026-11-14 통합 검증은 당시 기록으로 보존했다. 이번 변경은 인수인계 문서이며 수업 코드·사이트 빌드를 변경하지 않는다.

### 2026-11-15 — 오픈소스 AI 7주차 GGUF 보완과 Android 11주차 상태 글자 수정

2026-11-18에 커밋 기록으로 보충한 항목이다.

- `4cd9695`: 오픈소스 AI 7주차 GGUF 변환 순서를 `ex05` 병합 → llama.cpp 변환(고정 커밋, `../tools/llama.cpp`) → 파일 확인 → Ollama 등록 → 대화로 나눴다. `examples/`가 작업 폴더라는 것과 `../tools` 상대 경로의 뜻을 설명하고, 7주차 `.gitignore`에 `/tools/llama.cpp/`를 넣었다(9개 파일).
- `52903f5`: Android 당시 11주차(SmartIO)의 [검색] 뒤 상태 글자에 `ScanState.SCANNING`(검색 중)을 더해 검색 상태와 연결 상태를 나눴고 12주차 서술도 맞췄다. Android 장 수가 304장에서 305장이 됐다. 이 두 주차는 2026-11-18 `738c81f`에서 `legacy_week11`·`legacy_week12` 특강으로 옮겨졌다.

### 2026-11-14 — 웹 REST 교재와 방학 연구 특강 정리

- 웹 12주를 GET 조회, 13주를 POST 저장, 14주를 PATCH·DELETE로 개편했다. 기존 주차 폴더 이름은 유지하고 README·한영 슬라이드·따라하기·실습·예제와 색인을 맞췄다. 15주 누적 문제은행·개인 실기의 REST 범위도 연결했다. 레포트는 별도 공지하며 14주 검사 주차를 없앴다.
- Supabase 공용 방명록 API 구축과 Node HTTP 홈 IoT 제어를 방학 연구 특강으로 정리했다. 차시·분량·총시간 제한 없이 단계별 실행·비교 실험·기록으로 진행한다. IoT는 주기 조회, 단일 기준과 히스테리시스, 통신 실패·복구 실험을 제공한다.
- 공용 프로젝트를 준비했다(주소는 `web_programming/tools/guestbook-api/README.md`와 Supabase 특강 예제의 설정 파일에 있다). 공용 등록 확인 태그는 student01·student02다. 학생은 계정 없이 공개 키와 태그로 조회·저장한다.
- about-help.sql을 적용하고 about GET 200·1행(v1), help GET 200·6행(step 1~6)을 확인했다. 실제 localhost:8000의 01·02 화면에서도 Supabase HTTPS 응답과 CORS, 버튼 복구, 페이지 오류 없음을 확인했다. 방명록 GET·POST 저장 후 재조회도 확인했다.
- Supabase 예제 루트는 README만 남기고 01_about부터 07_guestbook_complete까지 독립 폴더로 나눴다. 각 폴더는 HTML·앱·설정·스타일·requests.http·.env.example을 자체 보유한다. 06은 통합 요청 실험, 07은 완성 방명록이다. 폴더 하나만 내려받거나 Pages에 게시할 수 있다.
- REST Client는 같은 폴더의 .env를, 브라우저는 HTML에서 defer로 읽는 config.example.js를 사용하도록 문서에 구분했다. 실제 환경 파일·localfiles·.local·편집 키는 배포에서 제외하고 공개 publishable key만 브라우저 설정에 사용한다. 요청 시 편집 키 입력과 이력 정리도 안내했다.
- 사이트·슬라이드 맞춤·API 실습 시험을 npm test로 연결했다. 최종 통합 검증은 51개 덱, 한글·영문 각각 1,069장(Android 304·웹 339·오픈소스 AI 426)이다. 웹 API·시뮬레이터·통합 요청 시험과 브라우저 실습 확인을 수행했다. 원격 오픈소스 AI 개편은 별도 작업의 변경이며 이번 웹 개발 이력에 포함하지 않는다.
- 사용자 요청으로 _forAI 5개 문서를 갱신했다. 기존 Android·오픈소스 AI 이력은 보존하고 현재 작업 경로, 실행 명령, API 계약, 비밀정보 제외 기준과 남은 일을 추가했다. 저장소 밖 전역 AGENTS.md의 REST Client 제공 규칙은 별도로 관리한다.
- 남은 검증은 공용 PATCH·DELETE 권한·보호 열 거부·다른 기기 및 Pages 실배포다. 비공개 대본·해답·평가 자료의 전체 개편도 미완료다. 과거 실측 기록을 새 수업 검증 결과로 바꾸지 않는다. localhost:8000 서버는 작업 중 실행 상태를 확인했으며 영속 서비스로 운영하는 것은 아니다.

### 2026-11-13 — 오픈소스 AI 10~15주차 개편과 폴더 이름 변경

2026-11-18에 커밋 기록으로 보충한 항목이다. `materials_plan.md` 10절의 개편안을 이날 사용자가 승인했고, 기말 발표 점수를 AI 성능 평가로 대체하는 것은 11-12 사용자 지시다.

- `0b2048c`(06:12): 이전 10~13주차 원고(프로젝트 거버넌스, 데이터셋 평가, AI 서비스 배포, 테스트·CI·보안)를 `specials/project_delivery/`로 옮겨 보존했다(사이트 미등록).
  - 10주차: Python 함수 4개(`turn_on`·`turn_off`·`set_brightness`·`read_environment`)로 시뮬레이터를 제어하고 Ollama `qwen3.5:2b` 툴 호출에 연결해 고정 16문항으로 확인한다.
  - 11주차: Needle 3(`cactus-compute==4.2.0`)와 Ollama의 정확도·시간을 비교한다.
  - 12주차: 48개 명령 예제로 Needle LoRA를 학습·저장·복원한다.
  - 13주차: 제어 평가와 오류 개선 뒤 Streamlit 제어 화면을 만든다.
  - 14주차: 원광대학교 소개 챗봇 과제와 공개 평가(공개 20문항, 출처 요약 5개, `evaluation_spec.md`, 채점 도구 시험 23개)를 둔다.
  - 15주차: 발표 항목을 비공개 문항 AI 성능 평가로 대체하고 레포트를 따로 평가한다.
  - 공용 `tools/bleuno-control`(평가 16문항 `control_cases.json`)을 새로 만들었다.
- `29a667a`(07:52): 10~15주차 폴더 이름을 주제에 맞게 바꿨다(`week10_simulator_control`, `week11_tiny_tool_calling`, `week12_control_lora`, `week13_control_streamlit`, `week14_chatbot_project`, `week15_final_evaluation`). `site/catalog.json`의 `formerIds` 6개가 옛 덱 주소를 넘긴다.
- 2026-09-04~11-12의 오픈소스 AI 커밋 23개(10-29 과정 순서 개편, 11-05 6주차 RAG, 11-12 7주차 LoRA 등)는 아직 이 문서에 없다(`plan.md` 오픈소스 AI 후속 작업 6번).

### 2026-11-12 — 보드 없이 연습하는 Wi-Fi 시뮬레이터(`iot_sim/`)와 bleuno TCP 분기

- 새 폴더 `android_programming/iot_sim/`을 만들었다. 넣은 파일은 세 개다.
  - `sim.py`: Python 표준 라이브러리만 쓴다. 명령 TCP 8266, 검색 UDP 8267, 브라우저 화면 HTTP 8080을 연다.
  - `README.md`: 실행, 화면, 포트, 방화벽, 막혔을 때.
  - `lab.md`: 12주차 2일차 이후의 90분 선택 실습.
- `bleuno/src/`에 `TcpBleunoClient.kt`를 더하고 `Bleuno.kt`에 `createTcp()`를 더했다. 12~15주차 예제 복사본 7곳도 같은 9개 파일로 맞췄다. 학생은 실습할 때만 실습지 2-2~2-4를 넣는다.
  - Manifest `INTERNET`
  - MainActivity의 `useFake = false`·`useTcp` 두 줄과 24번 client 줄
  - 주소 직접 입력(strings 두 줄, 레이아웃 주소 칸, [주소로 연결] 리스너)
  - 2-1의 bleuno 두 파일은 9개 파일 예제에 이미 있다(실습지는 2-1까지 '네 곳'으로 센다)
- 주차 문서도 맞췄다.
  - 12~15주차 문서·슬라이드의 "제공 파일 8개"를 9개로 고쳤다. 15주차 README·`examples/README.md`의 '나머지 N개'도 16개로 고쳤다.
  - walkthrough 부록 4곳에 새 `Bleuno.kt`와 `TcpBleunoClient.kt` 전문을 넣었다.
  - 과목 README, `weeks/README.md`, 12~14주차 README '준비'에 시뮬레이터 링크를 한 줄씩 넣었다.
  - `bleuno/README.md`에 연결·해제 때 외부 LED 끄기(1절, 펌웨어 소스 기준), 9개 파일 표·`INTERNET`·`createTcp()`(3~5절), `tag:TCP`(8절), 막혔을 때 두 줄(9절), 10절 '보드 없이 Wi-Fi 시뮬레이터로 연습하기'와 그 끝의 'TcpBleunoClient의 동작' 표를 더했다.
  - 12주차 `lab.md` 막혔을 때에 `Unresolved reference 'TcpBleunoClient'.` 줄을 더했다.
  - 조교 설치 목록(`android_programming/ta_setup_guide.md`)에 Python 3.9 이상과 실기기로 붙일 때의 방화벽 허용을 더했다.
- 시뮬레이터 동작은 교수 결정(2026-11-12)을 따른다.
  - 보드와 같게 한 것(펌웨어 `ble.cpp` 기준): 앱이 연결될 때와 끊길 때 LED를 모두 끈다. 길이 0인 줄에는 답하지 않는다.
  - Fake와 다르게 둔 것: `dht11`은 화면 슬라이더 값이다. 입력 이벤트는 화면 [입력 버튼]을 누를 때만 보낸다.
- 실습지는 주차 실습지처럼 예상·관찰 표와 힌트만 둔다. 에뮬레이터 실측과 정답은 비공개 짝 저장소의 `teaching_materials_private/android_programming/iot_sim/lab_solution.md`에 두었다.
- 비공개 짝 저장소도 맞췄다: 12~15주차 해답과 12·15주차 대본의 파일 수(9개), 12~15주차 해답 검증 기록의 이번 예제 변경·빌드 결과, `course_plan_2026.md` §5(`TcpBleunoClient`, Wi-Fi 시뮬레이터 분기), README 표 두 줄, `tools/iot_sim/`(`test_sim.py`·`README.md`). 비공개 문서에는 '9개'·`TcpBleunoClient`·10주차 수정 뒤 줄 번호가 공개 `dev/android/blueno` 기준이라는 것을 밝혔다(README, `course_plan_2026.md` §5, 12~15주차 해답·대본).
- 검증: Android 에뮬레이터(API 31)에서 앱 A·B(28개 중 2개는 Fake·Combo 변형)로 실측했다(시뮬레이터 첫 판 28개 시나리오, 리뷰 반영 뒤 재측정 9건, LED 끄기·빈 줄 결정을 넣은 판 5개 시나리오(M1~M5)와 그 화면 비교). 시뮬레이터 자동 시험 23/23(저장소 배치, Python 3.9·3.14). check_week 12~15주차 문제 0건(경고는 기존 전문 블록 2·2·2·4건 그대로). bleuno 9개 파일은 정본과 예제 7곳에서 sha256이 같다. 예제 7곳은 `assembleDebug`가 BUILD SUCCESSFUL이고 Kotlin 경고는 0건이다(Windows, Gradle 9.4.1·AGP 9.2.1·Kotlin 2.2.10. 68b41a4의 8개 파일로 바꿔도 같다). 실습지 2-2~2-4를 넣은 6곳도 빌드된다.
- 실측에서 찾았지만 이번에 고치지 않은 것(14주차 [재연결] 버튼의 `stopScan`, 명령 로그 스크롤 등)은 `plan.md` 9번에 적었다.
- 이 작업은 Android 작업 갈래 `dev/android/blueno`에 커밋했다. 이 갈래에는 main의 2026-11-02 재구성이 없다. main과 합치는 일은 `plan.md` 11번에 적었다.
- 시뮬레이터 코드(`sim.py`·`README.md`·`test_sim.py`)는 별도 작업 세션이 만들고 시험했다. 앱 쪽 코드와 실습지, 저장소 반영은 이 작업에서 했다.
- 후속 커밋: 시뮬레이터 작업 세션이 고친 README와 비공개 자동 시험을 넣었다(`sim.py`는 그대로). README 7절에 시뮬레이터를 돌리는 Python의 방화벽 규칙만 보고 바꾸는 네 줄, 'Python 규칙 지우기', 관리자가 아닌 계정에서 생기는 막는 규칙, 포트 규칙은 관리자 권한 PowerShell에서 지운다는 것을 더했고, 보드 동작 문장에 '펌웨어 소스 기준'을 붙였다. 같은 뜻으로 실습지의 끝내기·확인 목록에 방화벽 규칙 지우기를, `bleuno/README.md`에 연결 중 `blink`·`stopblk`의 동작과 `on`·`off`만 번호를 검사하지 않는다는 것을, 조교 설치 안내에 막는 규칙 확인과 수업 뒤 지우기를 더했다. `plan.md` 9번의 `blink` 항목도 맞췄다. 시뮬레이터 자동 시험은 저장소 배치에서 Python 3.9~3.14 모두 23/23이다.
- 이후 경과(2026-11-18 덧붙임): `dev/android/blueno`는 같은 날 `6af3108`에서 main에 합쳐졌다. `iot_sim/sim.py`는 `cc92e34`에서 `tools/bleuno-sim`으로, `738c81f`에서 `tools/wleno`로 옮겨졌고, 작업 트리에서는 WlEno 2.0.0으로 대체됐다(미커밋).

### 2026-11-11 — 10주차 권한 거절 흐름과 배터리 첫 표시 수정, 11~15주차에 전파

- 권한 거절을 공식 흐름으로 나눴다.
  - `shouldShowRequestPermissionRationale`가 true면(처음 거절) Toast만 띄운다.
  - 더는 물어볼 수 없을 때만 '설정으로' 대화상자(14번)를 띄운다.
  - 새 함수나 새 주석 번호는 만들지 않았다.
- 배터리는 `ContextCompat.registerReceiver`가 돌려주는 마지막 방송으로 문구를 바로 채운다. Android 12 이하는 등록 직후 방송이 오지 않을 수 있다.
- 11~15주차 SmartIO 예제와 walkthrough·slides·lab·README를 같은 코드로 맞췄다. 15주차 rubric은 P2를 처음 거절과 두 번 거절의 두 갈래로 나누고 인용 행 번호를 고쳤다.
- 이전 주차에서 내려온 문제는 고치지 않고 보고만 했다.
  - `ConnViewModel`의 `catch (e: Exception)`이 취소를 삼킨다.
  - Switch 리스너가 회전할 때 다시 불린다.

### 2026-10-31 — Android BLE 교재·별도 앱·type_m v1 하드웨어 역할 정리

- SmartIO와 `android_programming/bleuno/src/` 공통 클래스 8개를 학생용 기준으로 유지하고, `gbox3d/bleunoApp/BleunoTest`를 강의자·조교의 보드 점검·시연용으로 연결했다.
- 과목 README·BLE 제공 클래스 안내·조교 설치 안내에 역할과 저장소 링크를 추가했다. 펌웨어·type_m v1 마더보드 자료는 `gbox3d/bleuno`의 `hardware/type_m/v1/`에서 관리한다.
- 교재 GPIO 표가 기존 수업 설정이며 type_m v1 확정 핀맵이 아님을 표시했다. TENSTAR 연결 상태 LED 설명을 현재 펌웨어 소스와 맞췄고 실기 검증 대기를 명시했다.
- 공통 클래스와 주차별 복사본 5곳의 8개 파일 해시가 일치함을 확인했다. 교재·점검 앱·펌웨어의 UUID·텍스트 명령 형식을 대조했다.
- 교재와 `bleunoApp`의 변경 Markdown 13개, 로컬 링크 75개, 앵커 55개 및 코드 복사본 해시 40개 비교를 통과했다. 양쪽 저장소의 `git diff --check`도 통과했다.
- 기존 `_forAI/` 문서에 이번 Android 연계 결정만 추가했다. Android 하위 중복 `_forAI/`는 만들지 않았다. 런타임 코드 수정·Git 커밋·Android 빌드·실기 검증은 하지 않았다.
- 이후 확보한 EasyEDA 원본은 `MovingTarget/MotorConT1`의 모터·서보 제어 보드였다. 회로도·PCB 12부품·52핀 네트 매핑을 대조하고, 기존 LED·DHT11 설정의 충돌과 SEN1·VIN 미연결을 교재 안내에 반영했다. 원본 확보·KiCad 이전·원본 대조 완료와 남은 전기적 설계 검토·실기 검증을 구분했다.

### 2026-09-03 — 15주 자료 마무리와 전체 정합성 검증

- 미완성 주차의 교재·예제를 채우고 슬라이드 원고를 15주 모두 같은 형식으로 맞췄다. 최종 규모는 285개 파일, Markdown 19,349줄, Python 8,017줄이다.
- 검증 결과: 슬라이드 분 범위가 교시마다 0–20분으로 연속하고(15주 × 3교시 × 7구간 = 315구간), 실습 시간표가 교시마다 0–30분으로 연속한다. 상대 링크와 앵커 178개 문서 전수 통과, 슬라이드 raw HTML 0건, `theme: default` 주차당 1회, Python 67개 파일 문법 오류 0건, ruff 치명 오류 0건이다.
- 루브릭 8종의 배점 합계가 모두 100점임을 확인했다. 12주차 과제 루브릭에 누락된 합계 행을 추가했다.
- 예제 폴더에 남은 실행 산출물(`.ruff_cache/`, `__pycache__/`, `outputs/`)을 제거하고 `HF_HOME` 예시 경로 표기를 통일했다.
- `materials_plan.md`의 남은 초안 문구를 정리했다. 콘텐츠 ID를 주차 폴더 이름으로 대체하고, 과제 표의 학교별 성적 비율(%)을 공용 교재가 제공하는 문서 링크로 바꿨다.
- 사이트: `site/catalog.json`의 오픈소스 AI 요약을 `15개 주차 · 407장`으로 확정했다. `npm run build`와 `npm test`가 46개 덱·923장으로 통과한다(모바일 228 + 웹 288 + 오픈소스 AI 407).
- 강의 대본 15종의 구간 제목과 분 범위가 같은 주차 `slides.md`와 정확히 일치함을 전수 확인했다.

### 2026-09-03 — 심층 검수와 기본 생성 모델 교체

- 주차별 심층 검수(사실 정확성·교육 정합성)에서 95건을 찾아 75건을 고쳤고, 주차 간 정합성에서 12건 중 8건을 고쳤다. 공식 문서 대조와 실제 실행으로 검증한 뒤 반박을 이겨낸 것만 반영했다.
- **기본 생성 모델을 `qwen3:4b`에서 `qwen3:8b`로 바꿨다.** Ollama 레지스트리에서 `qwen3:4b`의 model·template·params digest가 `qwen3:4b-thinking-2507-q4_K_M`과 동일함을 확인했다. 접미사 없는 이 태그는 생각 전용 빌드라 교재가 4주차에서 가르치는 `"think": false`가 동작하지 않는다. Qwen3에서 `0.6b`·`1.7b`·`8b`·`14b`·`32b`만 하이브리드이며 `4b`·`30b`·`235b`는 2507 갱신에서 instruct/thinking으로 갈렸다.
- 교체는 13개 주차의 공개·비공개 문서 106개 파일에 걸쳐 반영했다. 모델 크기(2.5 GB → 5.2 GB) 같은 확정값은 값으로, 실측치(tokens/s, VRAM 점유, 로드 시간)는 자리표시자와 "기준 PC 실측값으로 채운다" 안내로 바꿨다. 6·10주차는 Hugging Face 모델만 써서 대상이 아니었다.
- `weeks/README.md`에 「생성 모델 태그를 고를 때」 절을 추가했다. 하이브리드와 생각 전용 태그의 구분, 모델을 바꿀 때의 확인 절차를 기록했다.
- 13주차 예제 워크플로의 액션 버전을 올렸다(`actions/checkout@v5`, `astral-sh/setup-uv@v7`).
- 재검증: Python 67개 파일 문법 오류 0건, ruff 치명 오류 0건, 상대 링크·앵커 180개 문서 통과, 슬라이드 시간 배분과 실습 시간표 전 주차 통과, 루브릭 8종 합계 100점, `npm run build`·`npm test` 46개 덱·923장 통과.
- 검수 에이전트가 보고한 "저장소 파일이 CRLF"라는 관찰은 사실이 아니었다. `git ls-files --eol` 결과가 index·working tree 모두 `lf`이고 HEAD blob에 CR이 없다.
- 순수 Python 예제 9개(1·3·4·8·9·13·14·15주차)를 스크래치 복사본에서 `uv sync`부터 실제로 실행했다. 34개 확인 항목이 모두 의도대로 동작했다. Ollama 서버가 없을 때의 실패 경로(4주차 chat.py, 8주차 check_env.py)와 8주차 깨진 프로젝트의 의도된 TOML 오류도 확인했다. torch·gradio·Ollama가 필요한 예제(5·6·7·10·11·12주차)는 이 PC에서 실행하지 않았다.
- `_forAI/plan.md`의 남은 일을 전문 용어 없이 다시 썼다.

### 2026-09-02 — 오픈소스 AI 응용 15주 교재 초판 작성

- 원광대 수업계획서의 15주 주제를 공용 청사진으로 옮겨 `open_source_ai/weeks/weekNN_slug/` 15개 폴더를 만들었다. 각 폴더에 `README.md`, `slides.md`(Marp), `lab.md`, `examples/`(uv 프로젝트·템플릿)를 두고, 1·3·4·7·10·12주차에 `walkthrough.md`, 4·8·9·12·15주차에 평가 문서를 추가했다.
- 수업 시간 구조를 60분 블록 × 3(설명·시연 20분 + 실습 30분 + 휴식 10분)으로 확정하고 `open_source_ai/weeks/README.md`에 운영 기준·주차 목록·검증용 환경변수 기본값을 기록했다.
- 강의 대본 `lecture_script.md`와 실습 해답 `lab_solution.md` 15세트를 비공개 짝 저장소 `univ_scoring_works/teaching_materials_private/open_source_ai/weeks/`에 작성하고, `_shared/practice_operation.md`에 「60분 블록 수업 보정」 절을 추가했다.
- `open_source_ai/README.md`를 진입점 형식으로 바꾸고 `materials_plan.md`의 폴더 구조·제작 단계 상태·다음 작업을 갱신했다. 루트 `README.md` 교재 색인 문구를 갱신했다.
- 사이트: `site/catalog.json`의 `open-source-ai`를 `published`로 바꾸고 15개 chapter를 등록했다. `scripts/render-site.mjs`·`check-site.mjs`에 `open-source-ai → open_source_ai/weeks` 매핑을 추가하고 덱·슬라이드 수 상수를 빌드 결과로 갱신했다.
- 검수: 주차별 기술·형식 검수와 교육적 정합성 검수를 거쳤고 Python 예제는 문법 검사(`py_compile`)와 ruff 치명 오류 검사를 통과했다. 모델·GPU 실행은 기준 PC 실측 대기.
- `_forAI/` 문서 세트를 실제 구조·명령·규칙으로 채웠다.
