# Memo

## 목차

- [제품 기준선](#제품-기준선)
- [강의 영상 제작·게시 재사용](#강의-영상-제작게시-재사용)
- [기본 설정값](#기본-설정값)
- [런타임 구조 메모](#런타임-구조-메모)
- [동작 규칙](#동작-규칙)
- [릴리스 전 검증 항목](#릴리스-전-검증-항목)
- [반복 금지](#반복-금지)
- [저장소 공통 교훈](#저장소-공통-교훈)
- [웹 REST와 Supabase 운영](#웹-rest와-supabase-운영)
- [HTTP 홈 IoT 연구 기준](#http-홈-iot-연구-기준)
- [공용 시뮬레이터 WlEno](#공용-시뮬레이터-wleno)
- [Android 보존 특강의 BLE 보드 연계](#android-보존-특강의-ble-보드-연계)

과목 안의 작업 규칙은 과목 지침이 정본이다: [Android](../android_programming/AGENTS.md), [웹](../web_programming/AGENTS.md), [오픈소스 AI](../open_source_ai/AGENTS.md). 저장소 공통 규칙과 여러 에이전트 운영 방식은 [루트 AGENTS.md](../AGENTS.md)에 있다. 이 문서는 그 규칙의 근거가 된 참고 정보와 교훈을 모은다.

## 제품 기준선

- 빌드 환경: Node.js 24, `@marp-team/marp-core` 4.4.0(`package-lock.json` 고정). GitHub Actions `pages.yml`이 main push마다 `npm ci` → `npm run build` → `npm test` → Pages 배포를 한다.
- 배포 주소: <https://gbox3d.github.io/teaching_repo/>
- 줄바꿈: `.gitattributes`로 전 파일 LF. Windows에서 만든 파일은 작업 트리에서 CRLF일 수 있지만 커밋할 때 LF로 바뀐다. BOM은 넣지 않는다.
- 실습 기준 PC(오픈소스 AI): Windows + RTX 4070(12 GB). GPU 없는 PC용 CPU·소형 모델 대체 경로를 항상 둔다.

## 강의 영상 제작·게시 재사용

[강의 영상 인수인계](lecture-video.md)에서 로컬 작업 기록과 `myAISkills`의 `lecture-video-editing` 스킬을 찾는다. 편집·자막·게시 단계별 상태를 실제 근거와 대조하고 남은 단계만 수행한다. 과거 주차 번호·절대 경로·품질 점수를 다른 강의에 그대로 적용하지 않는다.

그 문서의 독립 검토 기준(7점 초과, 5번째 반려에서 중단)은 2026-11-16 강의 영상 문서 요청의 기준이다. 2026-11-18부터 과목별 작업과 문서·지침 정비는 [루트 AGENTS.md의 여러 에이전트 작업 방식](../AGENTS.md#여러-에이전트로-작업하는-방식)(7점 이상 통과, 다시 작업 최대 3번)을 따른다.

## 기본 설정값

오픈소스 AI 응용 예제의 교재 검증용 기본값이다. 실제 학기 값은 `environment_baseline_template.md`로 확정한다. 새 예제는 파일 맨 위 대문자 상수로 두고(2026-11-05 결정), 5·6·9주차 `src/shared`와 8주차 `period3/config.py`·두 `broken_project/report.py`는 아직 `OLLAMA_MODEL` 환경변수로 기본값을 바꿀 수 있다.

| 값 | 기본값 | 쓰는 곳(2026-11-18) |
|---|---|---|
| 생성 모델 | `qwen3.5:2b` | 4~7·9~11·14주차 예제, 8주차 문서(README·lab·slides)와 period2·mock_exam 과제, 5·6·9주차 `src/shared`의 `OLLAMA_MODEL` 기본값, `tools/bleuno-control/src/bleuno_control/models.py`, `weeks/README.md` 기본값 표 |
| 생성 모델(초판 흐름) | `qwen3:8b`(CPU 대체 `qwen3:0.6b`) | 1~3주차 문서·예제, 8주차 `examples/period3`·두 `broken_project`·두 `make_broken_repo.ps1`, `ta_setup_guide.md`(두 모델을 모두 적음). 8주차는 두 모델이 섞여 있다(`plan.md`) |
| 11~13주차 작은 모델 | Needle 3, `cactus-compute==4.2.0` | 11~13주차 `examples/`, `tools/bleuno-control` |
| Ollama 주소 | `http://localhost:11434`(10주차는 `http://127.0.0.1:11434`) | 각 주차 상수와 `OLLAMA_HOST` 기본값 |
| Ollama 임베딩 | `bge-m3` | 2·6·8·9주차 |
| Hugging Face 텍스트 | `Qwen/Qwen2.5-0.5B-Instruct` | 1·2·7주차 |
| Hugging Face 임베딩 | `intfloat/multilingual-e5-small` | 1·2·9주차 |

두 생성 모델 기본값을 하나로 맞출지는 `plan.md`에 있다. Qwen3 계열은 thinking 출력이 섞이므로 Ollama API 호출에 `"think": false`를 넣는다.

생각 모드를 끌 수 있는 태그만 기본값으로 쓴다. Qwen3에서 `0.6b`·`1.7b`·`8b`·`14b`·`32b`는 하이브리드라 `think`가 실제로 꺼진다. `4b`·`30b`·`235b`는 2507 갱신에서 instruct/thinking으로 갈렸고, 접미사 없는 태그가 생각 전용 빌드를 가리켜 `"think": false`가 무시된다(2026-09-03 레지스트리 digest로 확인: `qwen3:4b` = `qwen3:4b-thinking-2507-q4_K_M`). 모델을 바꾸기 전에 `ollama show`나 레지스트리 digest로 이 구분을 다시 확인한다. 2026-09-03에 `weeks/README.md`에 넣었던 「생성 모델 태그를 고를 때」 절은 지금 파일에 없다.

수업 시간 구조:

| 과목 | 구조 |
|---|---|
| Android | 주 2회 × 90분, 매회 설명·시연 30분 + 실습 60분 |
| 웹 | 주 2회 × 90분. 일반 27차시는 강의·시연 60분 + 실습 30분, 8·15주 2차시는 안내 30분 + 실기 60분, 9주 2차시는 안내 5분·발표 75분·피드백 10분(C01 개편, `393c757`) |
| 오픈소스 AI | 60분 블록 × 3(1·2·3교시), 매 블록 설명·시연 20분 + 실습 30분 + 휴식 10분. 분반에 따라 2+1 또는 1+2로 이틀 배치 |
| 연구 특강 | 방학 실습·연구. 분량·차시 수·총시간 제한 없이 단계별 결과를 확인 |

## 런타임 구조 메모

- `site/catalog.json`이 덱 목록의 단일 기준이다. 새 주차·특강을 공개하려면 `catalog.json`에 chapter를 추가하고 두 스크립트의 `EXPECTED_*` 상수를 빌드 결과로 갱신한다. `sourcePath`는 세 과목 모두 `weeks/`·`specials/`를 매핑하므로 새 폴더 종류가 아니면 고치지 않는다.
- 슬라이드 수는 렌더된 HTML의 `<svg data-marpit-svg>` 개수로 센다. 원고의 `---` 줄 수와 다를 수 있으니(frontmatter 구분자 포함) 최종 값은 `npm run build` 출력으로 확정한다.
- `render-site.mjs`는 원고의 `<br>`(줄 끝)을 Markdown 줄바꿈 `\`로, `<code>`를 백틱으로 바꾼 뒤 남은 raw HTML이 있으면 빌드를 실패시킨다. `slides_en.md`에도 같은 규칙이 적용된다.
- 상대 `.md` 링크는 GitHub blob URL로 바뀌므로 원고에서 `lab.md#앵커` 링크를 써도 된다. 빌드는 대상 파일이 있는지 보지 않는다. 앵커 규칙은 GitHub 스타일(공백→`-`, 특수문자 제거, `—`가 빠지면 `--`가 남는다)이다.
- 웹 슬라이드가 예제 HTML을 상대 링크로 연결하면 그 단원 `examples/`의 공개 파일과 `web_programming/shared/`를 함께 복사한다(`render-site.mjs`). 아직 추적하지 않는 새 파일도 복사되므로 `examples/` 아래에 임시 파일을 두지 않는다. Android·오픈소스 AI 슬라이드는 링크한 파일만 복사하므로 실행 예제는 GitHub 링크로 제공하고 폴더째 내려받게 안내한다.
- 폴더 이름을 바꾼 덱의 옛 주소는 `catalog.json`의 `formerIds`가 새 덱으로 넘긴다. `check-site.mjs`는 리다이렉트 수(덱 수 + `formerIds` 수)와 쿼리·슬라이드 번호 보존을 검사한다. Android 정규 11~14주처럼 정규 주차를 특강으로 옮기면 옛 id는 보존 특강이 아니라 같은 번호의 새 정규 주차로 넘어간다.

## 동작 규칙

- 공용 교재에 학교명·분반·학수번호·실제 날짜·성적 비율·LMS 이름을 넣지 않는다. 오픈소스 AI 14·15주차의 원광대학교 소개 챗봇은 사용자 지시에 따른 예외다.
- 루브릭 배점 체계는 과목 관례를 따른다. 오픈소스 AI는 100점 상대 배점이다. Android는 8주 20점, 13주 30점(계획안 10, 시연 12, 보고서 8), 15주 20점이고, 웹은 8주 20점, 9주 10점, 15주 20점(구현 15, URL 재현·구술 5)이다. 어느 과목도 학교 성적 반영 비율은 넣지 않는다.
- 소프트웨어 정확 버전을 본문에 고정하지 않는다. 버전은 `environment_baseline_template.md`를 학기용으로 복사해 확정한다. 웹의 W3.CSS CDN 4.1.0처럼 과목 지침이 고정한 주소는 예외다.
- 전역 `pip install`을 쓰지 않는다. 오픈소스 AI 예제는 uv 프로젝트이고 `uv.lock`을 커밋한다. WlEno 시뮬레이터는 Python 3.10 이상 표준 라이브러리로 돈다. `tools/pyproject.toml`이 `tools/wleno`와 `tools/bleuno-control`을 PyPI 패키지 `wleno`로 묶고, 10주차는 그 패키지를 uv로 설치한다(`b3f25da`, `d0ad054`).
- 환경 설정은 `.env.example`·`config.example.json`에 자리표시자로 제공하고 실제 `.env`·`config.json`은 제외한다. Supabase의 브라우저용 publishable key 값은 파일에 쓰지 않고 secret key·DB 비밀번호도 포함하지 않는다. 학생용 starter와 강의자용 해답을 물리적으로 분리한다.
- 모델 다운로드는 실습 시간에 하지 않는다(사전 캐시).
- 강의 대본(`lecture_script.md`)과 해답(`lab_solution.md`)은 `univ_scoring_works/teaching_materials_private/`에 둔다. 대본의 구간 제목·분 범위는 공개 `slides.md`와 같아야 한다.

## 릴리스 전 검증 항목

원고를 크게 바꾼 뒤에는 다음을 확인한다. 사이트·슬라이드 맞춤·웹 실습 시험은 `npm test`를 쓰고, 나머지는 바꾼 범위에서 수행한다.

1. 줄바꿈·인코딩: `git ls-files --eol`(새 파일은 `-o --exclude-standard`를 붙인다)에 `w/crlf`가 없고 BOM이 없으며 파일 끝 개행이 1개인가.
2. 실행 산출물: `.ruff_cache/`, `__pycache__/`, `outputs/`, `.venv/`, `models/`, `dist/`가 포함되지 않았는가.
3. 금지 문자열: 학교명(과목 지침의 예외 제외), 분반, 학수번호, 성적 비율(%), 토큰·키, 작업 PC 절대 경로, 서버·장비 주소.
4. 시간 구조: 정규 주차는 과목별 시간 기준을 따른다. 오픈소스 AI는 설명 0–20분·실습 0–30분의 연속성을 확인한다. 연구 특강에는 고정 시간 검사를 적용하지 않는다.
5. Marp 제약: `theme: default` 덱당 1회, raw HTML은 줄 끝 `<br>`·`<code>`·주석만.
6. 링크: 모든 상대 링크의 대상 파일과 `#앵커`가 실제로 있는가(문서 링크는 자동 검사가 없다).
7. 코드: `python -m compileall`(`PYTHONPYCACHEPREFIX`를 저장소 밖 폴더로 두고)이 통과하고 `ruff check --select E9,F63,F7,F82`가 깨끗한가(8주차 `broken_project` 두 곳 제외). 웹 JS는 `node --check`.
8. 루브릭: 배점 합계가 문서에 적힌 총점과 같은가.
9. 대본: `lecture_script.md`의 구간 제목·분 범위가 같은 주차 `slides.md`와 일치하는가.
10. 사이트: `npm run build`와 `npm test`가 통과하고 덱·슬라이드 수 상수가 맞는가.

## 반복 금지

- 슬라이드를 고친 뒤 `EXPECTED_SLIDES`를 안 고쳐 CI가 깨지는 일. 빌드 출력의 장 수로 두 스크립트를 함께 갱신한다.
- 다른 과목 표현("1일차", "90분", "30분 설명")을 오픈소스 AI 자료에 복사해 오는 일. 오픈소스 AI는 "교시", "20분·30분·10분"이다.
- 강의 대본을 공개 저장소에 커밋하는 일.
- `materials_plan.md` 초안의 `materials/` 챕터 구조를 되살리는 일. 주차 폴더 구조로 확정했다.
- 존재하지 않는 CLI 명령 이름(예: 버전에 따라 바뀐 Hugging Face 캐시 명령)을 본문에 고정하는 일. Python API로 쓰거나 `--help`로 확인하라고 안내한다.
- 모델 태그가 가리키는 빌드가 그대로일 것이라고 가정하는 일. 태그에 의존하는 동작(생각 모드 on/off, 도구 호출, 컨텍스트 길이)을 가르칠 때는 레지스트리 digest나 `ollama show`로 실제 빌드를 확인한다.
- 학생용 실습지(`lab.md`)에 실측 결과를 정답처럼 적는 일. 실습지에는 예상·관찰 표와 힌트만 두고, 실측과 정답은 비공개 `lab_solution.md`에 둔다.
- 측정하지 않은 실행시간·VRAM·tokens/s를 사실처럼 적는 일. 확인할 수 없으면 자리표시자와 "기준 PC 실측값으로 채운다"로 둔다.
- 공용 도구(`tools/wleno`, `tools/bleuno-control`)의 동작이나 모델 프롬프트를 바꾸고 한 과목 문서만 고치는 일. 이전 측정표를 바뀐 코드의 결과처럼 두는 일도 같다.
- 공개 보고서·증거 스크립트에 작업 PC 절대 경로나 세션 상태(어느 포트에서 실행 중)를 남기는 일(2026-11-18 웹 개편 기록에 남은 사례가 있다).
- 학생이 읽는 흐름을 제공 코드가 가로채게 만드는 일. C01의 설정 패널은 제출 이벤트를 받아 학생 함수를 콜백으로 부르고 전역 값을 실행 중에 바꿔, 호출부 10개 파일에 설정 변경 대비 검사(`settingsVersion`)가 87줄 퍼졌다(2026-11-22 삭제). 제공 코드는 값을 준비하는 데서 멈추고 요청 → `await` → 화면 반영은 학생 파일에 그대로 보이게 한다.
- 공개 키(publishable key)를 숨길 수 있는 비밀처럼 설명하거나, 반대로 아무 데나 퍼뜨리는 일. 브라우저 코드가 쓰는 키라 숨길 수 없다. 2026-11-25 `bd02eaa`부터 편집 키가 없어 이 키 하나로 모든 태그의 글을 수정·삭제할 수 있다. 값은 파일과 공개 문서에 쓰지 않고 수업 기간에만 배부한다.

## 저장소 공통 교훈

- `git log`의 날짜 필터는 시각까지 적는다. `--since=2026-11-13`처럼 시각을 빼면 git이 지금 시각을 붙여 그날 앞부분 커밋이 빠진다(2026-11-18 실측: 11-13 06:12·07:52의 오픈소스 AI 개편 커밋 두 개가 빠졌다). 하루 단위로 볼 때는 `--since='YYYY-MM-DD 00:00'`을 쓴다.
- 작업 트리의 CRLF는 `git diff`와 커밋에서 보이지 않는다(`.gitattributes`가 정규화한다). 2026-11-18 작업 트리에는 추적 파일 187개(웹 155, Android 27, 루트 3, `tools` 2)와 새 파일 119개(모두 웹)가 CRLF였다. 사본 비교는 `cmp`나 `sha256sum` 대신 `git hash-object A B`로 한다. Windows Git Bash의 `grep -c $'\r'`는 CRLF 파일에도 0을 내는 등 결과를 믿을 수 없었다(2026-11-18 확인). CR 개수는 `tr -cd '\r' < 파일 | wc -c`나 `git ls-files --eol`로 센다.
- `git ls-files --eol`은 추적하지 않는 새 파일을 출력하지 않는다. 새 파일은 `git ls-files --eol -o --exclude-standard -- <경로>`로 본다.
- 같은 작업 폴더에서 여러 에이전트가 `npm run build`를 동시에 돌리면 `dist/`가 충돌한다. 빌드와 전체 시험은 한 곳에서 돌리고 과목 담당은 `npm run test:labs`와 단위 시험만 돌린다.
- 저장소 안에서 Python 시험을 돌리면 `__pycache__/`가 생긴다. Git 제외 대상이지만 배포 ZIP 검사 항목이므로 `python -B`로 돌린다. `uv run --project`·`--directory`는 대상 폴더에 `.venv/`를 만들고, `--frozen` 없이 돌리면 `uv.lock`이 바뀔 수 있다.
- `_forAI`의 과목 서술은 커밋보다 늦을 수 있다(2026-11-18 Android 개편 뒤에도 12~15주 BLE 서술이 남아 있었다). 작업을 시작할 때 dev_log 최신 날짜 이후의 `git log`와 `git status`를 본다.
- Claude Code는 `CLAUDE.md`를 읽는다. 그래서 `AGENTS.md`가 있는 폴더에 `@AGENTS.md` 한 줄짜리 `CLAUDE.md`를 둔다(2026-11-18 루트와 세 과목에 적용).
- 저장소 밖 전역 에이전트 지침에도 "REST API 예제에는 `.http`와 `.env.example`을 함께 제공한다"는 규칙이 있다. 그 파일의 경로는 기록하지 않는다.
- 셸의 현재 경로가 소문자 드라이브(`c:\…`)이면 홈 IoT 시뮬레이터 시험 하나가 `/` 404로 실패한다. 서버가 `realpath` 결과(`C:\…`)와 대소문자를 구분해 비교하기 때문이다(2026-11-23 확인). VS Code 터미널이 소문자로 시작하므로 `npm test`는 `cd "C:/…/teaching_repo"` 뒤에 돌린다.
- chrome-devtools MCP로 `prompt()`를 띄우는 화면을 열면 창이 떠 있는 동안 다음 호출이 `Network.enable timed out`으로 멈출 수 있다. 창 흐름은 처음 한 번만 실제 창으로 보고(`handle_dialog`), 나머지 화면은 `navigate_page`의 `initScript`로 `window.prompt`를 바꿔 끼워 확인한다. 원격 디버깅 Chrome은 저장소 밖 임시 프로필(`--user-data-dir`)로 띄운다(2026-11-23).

## 웹 REST와 Supabase 운영

- 정규 12주는 타이머와 키 없는 공개 API GET(할 일·환율·타로·공휴일, 선택 기온), 13주는 방명록 CRUD(POST → GET → PATCH → DELETE), 14주는 태그와 글 번호를 바꿔 수정·삭제한 뒤 같은 번호로 다시 조회해 결과를 확인한다(`bd02eaa`). 15주는 누적 문제은행 복습과 개인 실기를 유지한다. 레포트는 별도 공지하며 14주 검사 주차를 되살리지 않는다.
- 강의자가 준비한 서버를 학생 계정 없이 호출한다. Supabase 계정·SQL·키 등록은 구축 연구 특강의 담당자 작업이다. 특강 분량·회차·총시간은 제한하지 않는다.
- 브라우저 설정은 두 방식이 함께 있다.
  - 13주(`bd02eaa`): `load-config.js`가 같은 폴더의 `config.json`을 `fetch`로 읽고 주소·공개 키·`BOOK_ID`를 검사한다. 파일이 없으면(404) 복사 안내를, JSON 문법이나 값이 틀리면 확인 안내를 `#config-status`에 쓴다. `config.json`은 Git 제외이고 사이트 빌드도 복사하지 않으므로, 코드상 Pages의 13주 화면은 복사 안내에서 멈춘다.
  - 12주 선택 방명록·14·15주·hash SPA 04·Supabase 특강 01~07(2026-11-22 결정, `8cc49ea`): 주소와 `BOOK_ID`는 `config.example.js`에 둔다. 키가 없을 때 `prompt`로 한 번 묻고 localStorage의 `API_PUBLIC_KEY`에 저장한다. 취소·빈 칸이면 저장하지 않고(요청은 401) 새로고침하면 다시 묻는다. **공개 키 지우기**(`id="key-clear-button"`, 동작은 `config.example.js`가 붙인다)는 키를 지우고 새로고침한다. 같은 키 이름을 쓰므로 같은 출처에서는 한 번만 넣는다. 화면 설정 패널(`shared/api-settings.js`)은 없앴다.
- 13주 완성본을 14주가 이어 받으면 설정 방식이 `config.json`에서 묻는 창으로 바뀐다. 과목 지침은 "14주 이후에도 같은 설정이 필요할 때" 다시 보기로 했다.
- localStorage는 출처마다 따로다. 다른 브라우저, 포트가 다른 localhost, `127.0.0.1`과 `localhost`, Pages 주소, 휴대폰에서는 처음 열 때 다시 묻는다. 학기마다 키를 바꾸면 localStorage 쪽 학생은 **공개 키 지우기** 뒤 새 키를 넣고, 13주 학생은 `config.json`을 고친다. 저장소 파일은 고치지 않는다. 2026-11-22 확인한 Supabase 공식 문서에는 publishable key의 삭제·교체 절차가 적혀 있지 않다(secret key만 적혀 있다). 대시보드 Settings > API Keys에서 직접 확인한다.
- 공용 API 주소는 `web_programming/tools/guestbook-api/README.md`와 각 예제의 `config.example.js`·`config.example.json`·`.env.example`에 있다. 2026-11-22 이전 커밋의 특강 `config.example.js`와 walkthrough에는 공개 키 값이 들어 있었다(Git 기록에 남는다). 2026-11-14에 공용 서버에서 확인한 태그는 `student01`, `student02`다. 새 프로젝트의 `schema.sql`은 student01~30을 등록하지만, 기존 공용 프로젝트의 등록 현황은 SQL Editor에서 확인한다.
- `book_id`는 수업용 글을 구분하는 태그이고 학생 인증이 아니다. 2026-11-25 `bd02eaa`부터 편집 키가 없고, 공용 공개 키를 가진 사람은 모든 태그의 글을 작성·조회·수정·삭제할 수 있다. 예제는 PATCH·DELETE 주소에 `book_id`와 `id`를 함께 넣어 한 행을 지정한다.
- 모든 요청은 `apikey`만 보낸다. POST·PATCH는 `Content-Type: application/json`과 `Prefer: return=representation`을 붙인다. 이름은 1~30자, 메시지는 1~500자이며 공백만 있는 입력은 거부한다. 수정할 수 있는 열은 `name`·`message`다.
- GET `/rest/v1/about`은 name·version·description·help_path 한 행을, GET `/rest/v1/help?order=step.asc`는 요청 안내 여섯 행(about·help·CRUD 네 개)을 배열로 반환한다. help의 요청 순서와 예제 폴더 01~07은 별개다.
- 새 프로젝트는 `schema.sql` 다음에 `about-help.sql`을 실행한다. 이미 쓰는 프로젝트는 `enable-public-crud.sql`을 한 번 실행해 PATCH·DELETE 정책을 모든 태그에 열고 help를 CRUD 안내로 바꾼다(태그·글은 유지, 옛 `edit_key_hash` 열은 null 허용으로 남긴다). 태그를 더할 때는 `private.classroom_books`에 `book_id`만 넣는다. `provision.mjs`는 지웠다.
- `private.classroom_books`는 RLS를 켜고 클라이언트 권한을 모두 회수한 태그 목록이다. `guestbook.book_id`가 이 표를 외래 키로 참조해 등록하지 않은 태그의 글을 막는다. `private`를 Data API 노출 스키마에 추가하지 않는다.
- POST 201은 저장된 행의 배열이다. PATCH 200의 빈 배열과 DELETE 204만으로 실제 변경을 판단하지 않는다. book_id·id로 같은 글을 GET해 확인하고 204에 JSON 파싱을 하지 않는다.

Supabase 특강 예제는 루트 README와 독립 폴더 01~07로 구성한다. 06은 메서드·본문을 바꾸는 실험 화면, 07은 등록 폼·목록·선택 편집을 갖춘 완성 방명록이다.
각 폴더의 `.env`는 REST Client의 `requests.http` 전용이다. 브라우저는 같은 폴더의 `config.example.js`를 HTML의 `defer` 스크립트로 먼저 읽고 공개 키는 localStorage에서 읽는다(13주는 `config.json`). 한쪽 설정을 바꾸어도 다른 쪽은 자동으로 바뀌지 않는다. 12·13주의 `.env.example`은 수업용 서버를, 14·15주와 hash SPA의 `.env.example`은 로컬 모의 API를 가리킨다. 브라우저 기본값은 모두 수업용 서버다.
REST Client의 `{{$dotenv ...}}`는 `.http`와 같은 폴더의 `.env`를 읽는다. 요청 이력에는 `apikey` 헤더와 본문이 남는다. 공유 전 값을 확인하고 실습 후 **Rest Client: Clear Request History**로 정리한다.

`localfiles/`, `.local/`, 실제 `.env`·`config.json`, 비밀번호는 Git과 배포 ZIP·Pages에서 제외한다. `_forAI`에도 키 값을 복사하지 않는다.
로컬 HTTP 화면이 공용 HTTPS API를 호출할 수 있으며 페이지 주소는 HTTP로 유지된다. 브라우저 CORS와 REST Client 성공은 따로 검증한다. 각 폴더를 Pages에 게시할 때는 화면과 API 모두 HTTPS를 사용한다.
2026-11-14 확인 범위는 공용 about·help GET 200(1행·6행), localhost의 01·02 브라우저 조회, 방명록 GET·POST다. 2026-11-23에는 localhost에서 공개 키 묻는 창(취소 → 401, 새로고침 → 다시 묻기, 입력 → GET 200), **공개 키 지우기**, 12~15주·hash SPA·특강 대표 화면 13개의 GET과 375px 넘침을 확인했고, Pages에 새 파일이 올라간 것(HTTP 200)을 확인했다. 공용 PATCH·DELETE 권한과 Pages 화면에서의 조회는 미검증이다. 2026-11-25 `bd02eaa`(13주 `config.json`, 편집 키 폐지) 뒤의 브라우저·공용 서버 확인 기록은 저장소에 없다. 공용 프로젝트에 `enable-public-crud.sql`을 실행했는지도 기록이 없다. 13·14주 화면이 처음부터 수업용 서버를 부르므로 수업 전에 확인한다.

## HTTP 홈 IoT 연구 기준

`web_programming/specials/home_iot_http`는 Node.js 서버와 웹 UI로 가상 장치를 제어한다. 학생 PC의 `http://localhost:8014/`에서 GET·PATCH, 주기 조회, 단일 기준·26/29°C 히스테리시스, 통신 실패·복구를 비교한다.
온도는 수동으로 정하는 모의 값이고 팬이 실내 온도를 낮추는 물리 모델은 없다. 실제 냉각 성능이나 센서 정밀도를 측정한 것으로 기록하지 않는다.
상태와 제어 기록은 메모리에서 관리하며 서버 재시작 시 초기화된다. Android·오픈소스 AI가 쓰는 Python 시뮬레이터 WlEno와 코드를 섞지 않는다.

## 공용 시뮬레이터 WlEno

`tools/wleno`는 Android 11~15주와 오픈소스 AI 10~13주가 함께 쓰는 PC 시뮬레이터다. 명령·응답·이벤트의 정본은 `tools/wleno/README.md` 1·8절이다. 아래는 프로토콜 2.0.0(`543ab2e`) 기준이다.

- 배포(`b3f25da`, 2026-11-25): PyPI 패키지 `wleno` 0.1.0이 시뮬레이터(`wleno`, 명령 `wleno`)와 제어 라이브러리(`wleno.control` = `tools/bleuno-control/src/bleuno_control`)를 함께 담는다. 선택 의존성은 `needle`·`train`(`cactus-compute==4.2.0`)이다. 패키지 버전과 프로토콜 버전(2.0.0)은 따로 센다. 릴리스 `wleno-v0.1.0`과 PyPI 게시가 성공했다.
- 패키지에 든 두 폴더를 고치면 PyPI에 올린 0.1.0과 저장소 코드가 달라진다. 10주차는 PyPI 판을 쓰고 Android 문서와 11~13주는 저장소 코드를 쓴다. 동작을 바꿀 때 새 버전 게시와 10주 lock 갱신을 함께 정한다.

- 서비스: TCP 8266(명령 한 줄, JSON 한 줄 응답), UDP 8267(`bleuno?` 검색, 선택), HTTP `127.0.0.1:8080`(API). 기본 이름은 `WlEno_SIM1`이다. 보존 특강의 이름 필터를 쓸 때만 `--name ESP32_BLE_…`처럼 바꾼다.
- 연결 직후 `{"event":"hello",…}` 한 줄을 먼저 보낸다. 입력 이벤트에는 `sequence`가 붙는다.
- TCP 연결·해제는 LED·센서 상태를 초기화하지 않는다. 초기화는 화면이나 `POST /reset`으로 한다. 2026-11-12 결정(연결·해제 때 LED 끄기)을 바꾼 것이며 결정 출처는 저장소에 없다.
- 잘못된 정수·LED 번호·밝기는 요청 전체를 `{"result":"err"}`로 거부한다. `on 0 9`도 LED 0을 바꾸지 않는다. 빈 줄에는 답하지 않고, 공백만 있는 줄에는 `need command` 오류로 답한다.
- 실제 보드 펌웨어와 특강 Fake의 동작은 다르다. 보드·Fake 규칙은 `android_programming/bleuno/README.md`에 따로 있다. WlEno 동작을 보드와 같다고 쓰지 않는다.
- 오픈소스 AI 10~13주의 모델 도구는 `turn_on`·`turn_off`·`set_brightness`·`read_environment` 네 개이고, 센서 값을 바꾸는 `POST /set`은 모델에 주지 않는다. 비교할 초기 상태는 명령으로 맞추고 `GET /state`로 확인한다.

## Android 보존 특강의 BLE 보드 연계

옛 11~15주(지금 `android_programming/specials/legacy_week11~15_*`)와 `android_programming/bleuno/`에 해당한다. 정규 11~15주에는 적용하지 않는다.

- SmartIO + `android_programming/bleuno/src`가 특강의 학생용 기준이고, `bleunoApp/BleunoTest`는 강의자·조교의 점검·시연용이다.
- 교재·점검 앱·펌웨어에서 Service UUID `c6f8b088-2af8-4388-8364-ca2a907bdeb8`, Characteristic UUID `f6aa83ca-de53-46b4-bdea-28a7cb57942e`가 일치한다. 확인 범위는 소스 비교이며 실기 검증은 미완료다.
- 교재 GPIO `[4,3,1,0]`은 기존 수업의 `ledpin` 설정이다. 원본 type_m v1은 모터·서보용이며 GPIO0=CHKBAT, GPIO7=SLEEP이라 이 설정과 `dht11pin=7`을 그대로 적용하면 충돌한다. 모델명 `type_m`, 하드웨어 버전 `v1`, 펌웨어 `1.0.5_dev`는 별도로 관리한다.
- type_m v1 원본 회로도·PCB의 12부품·52핀 네트 매핑을 대조했다. SEN1은 MCU에 연결되지 않고 VIN은 전원 헤더 pin3에만 있다. KiCad 이전과 원본 대조는 완료했으며 전기적 미연결·모듈 핀 표기·실기 확인은 남아 있다. 근거는 `gbox3d/bleuno`의 `hardware/type_m/v1/pinmap.md`다.
- 펌웨어 소스(`gbox3d/bleuno` main, `ble.cpp`)는 연결될 때 외부 제어 LED를 모두 끄고(`onConnect`의 `ledOff(-1)`), 끊길 때 LED와 밝기를 모두 끈다(`onDisconnect`의 `clearAllControl()`). TENSTAR 빌드는 연결 중 내장 상태 LED가 파랑 고정이다. 실제 보드와의 대조는 아직 하지 않았다.
- 펌웨어 `onWrite`는 길이 0인 명령을 건너뛴다. `RealBleunoClient`·`TcpBleunoClient`는 `send("")`에 `\n`을 보내고, Fake는 보내기 전에 거른다. 버튼 입력 이벤트는 Fake용 가안이며 현재 펌웨어가 보내는 이벤트가 아니다.
- `TcpBleunoClient`는 WlEno의 TCP 8266, UDP 8267 `bleuno?` 검색, 첫 줄 hello에 맞춰 동작한다. WlEno 쪽을 바꾸면 `bleuno/README.md` 10절과 `TcpBleunoClient` 동작 표를 같이 본다.
- 공통 클래스를 고칠 때 함께 고치는 곳은 다음과 같다. 비공개 `check_week.py`는 주차 `examples/`의 .kt·.xml 전문과 walkthrough 코드 블록만 대조하고 정본 `bleuno/src`와는 대조하지 않으므로, 정본과 사본이 같은지는 `git hash-object`로 따로 본다.
  - 사본 7곳: `specials/legacy_week12_ble_gatt/examples/day1`·`day2`, `legacy_week13_ble_output/examples/day1`, `legacy_week14_ble_input_project/examples/day1`·`day2`, `legacy_week15_final_exam/examples/rehearsal_solution`·`rehearsal_starter`의 `bleuno/`
  - 해당 특강 `walkthrough.md` 부록의 전문, 파일 수를 적은 문서("9개"), `bleuno/README.md`의 3절 파일 표·5절 API 표
  - 비공개 특강 대본·해답과 `course_plan_2026.md` §5
