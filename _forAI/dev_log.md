# Dev Log

## 목차

- [Entries](#entries)

## Entries

### 2026-11-14 — 웹 REST 교재와 방학 연구 특강 정리

- 웹 12주를 GET 조회, 13주를 POST 저장, 14주를 PATCH·DELETE로 개편했다. 기존 주차 폴더 이름은 유지하고 README·한영 슬라이드·따라하기·실습·예제와 색인을 맞췄다. 15주 누적 문제은행·개인 실기의 REST 범위도 연결했다. 레포트는 별도 공지하며 14주 검사 주차를 없앴다.
- Supabase 공용 방명록 API 구축과 Node HTTP 홈 IoT 제어를 방학 연구 특강으로 정리했다. 차시·분량·총시간 제한 없이 단계별 실행·비교 실험·기록으로 진행한다. IoT는 주기 조회, 단일 기준과 히스테리시스, 통신 실패·복구 실험을 제공한다.
- 공용 프로젝트 `esoqbcwgzjtwcqszwvin`을 준비했다. 공개 기본 주소는 `https://esoqbcwgzjtwcqszwvin.supabase.co`이며 공용 등록 확인 태그는 student01·student02다. 학생은 계정 없이 공개 키와 태그로 조회·저장한다.
- about-help.sql을 적용하고 about GET 200·1행(v1), help GET 200·6행(step 1~6)을 확인했다. 실제 localhost:8000의 01·02 화면에서도 Supabase HTTPS 응답과 CORS, 버튼 복구, 페이지 오류 없음을 확인했다. 방명록 GET·POST 저장 후 재조회도 확인했다.
- Supabase 예제 루트는 README만 남기고 01_about부터 07_guestbook_complete까지 독립 폴더로 나눴다. 각 폴더는 HTML·앱·설정·스타일·requests.http·.env.example을 자체 보유한다. 06은 통합 요청 실험, 07은 완성 방명록이다. 폴더 하나만 내려받거나 Pages에 게시할 수 있다.
- REST Client는 같은 폴더의 .env를, 브라우저는 HTML에서 defer로 읽는 config.example.js를 사용하도록 문서에 구분했다. 실제 환경 파일·localfiles·.local·편집 키는 배포에서 제외하고 공개 publishable key만 브라우저 설정에 사용한다. 요청 시 편집 키 입력과 이력 정리도 안내했다.
- 사이트·슬라이드 맞춤·API 실습 시험을 npm test로 연결했다. 최종 통합 검증은 51개 덱, 한글·영문 각각 1,069장(Android 304·웹 339·오픈소스 AI 426)이다. 웹 API·시뮬레이터·통합 요청 시험과 브라우저 실습 확인을 수행했다. 원격 오픈소스 AI 개편은 별도 작업의 변경이며 이번 웹 개발 이력에 포함하지 않는다.
- 사용자 요청으로 _forAI 5개 문서를 갱신했다. 기존 Android·오픈소스 AI 이력은 보존하고 현재 작업 경로, 실행 명령, API 계약, 비밀정보 제외 기준과 남은 일을 추가했다. 저장소 밖 전역 AGENTS.md의 REST Client 제공 규칙은 별도로 관리한다.
- 남은 검증은 공용 PATCH·DELETE 권한·보호 열 거부·다른 기기 및 Pages 실배포다. 비공개 대본·해답·평가 자료의 전체 개편도 미완료다. 과거 실측 기록을 새 수업 검증 결과로 바꾸지 않는다. localhost:8000 서버는 작업 중 실행 상태를 확인했으며 영속 서비스로 운영하는 것은 아니다.

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

### 2026-09-02 — 오픈소스 AI 응용 15주 교재 초판 작성

- 원광대 수업계획서의 15주 주제를 공용 청사진으로 옮겨 `open_source_ai/weeks/weekNN_slug/` 15개 폴더를 만들었다. 각 폴더에 `README.md`, `slides.md`(Marp), `lab.md`, `examples/`(uv 프로젝트·템플릿)를 두고, 1·3·4·7·10·12주차에 `walkthrough.md`, 4·8·9·12·15주차에 평가 문서를 추가했다.
- 수업 시간 구조를 60분 블록 × 3(설명·시연 20분 + 실습 30분 + 휴식 10분)으로 확정하고 `open_source_ai/weeks/README.md`에 운영 기준·주차 목록·검증용 환경변수 기본값을 기록했다.
- 강의 대본 `lecture_script.md`와 실습 해답 `lab_solution.md` 15세트를 비공개 짝 저장소 `univ_scoring_works/teaching_materials_private/open_source_ai/weeks/`에 작성하고, `_shared/practice_operation.md`에 「60분 블록 수업 보정」 절을 추가했다.
- `open_source_ai/README.md`를 진입점 형식으로 바꾸고 `materials_plan.md`의 폴더 구조·제작 단계 상태·다음 작업을 갱신했다. 루트 `README.md` 교재 색인 문구를 갱신했다.
- 사이트: `site/catalog.json`의 `open-source-ai`를 `published`로 바꾸고 15개 chapter를 등록했다. `scripts/render-site.mjs`·`check-site.mjs`에 `open-source-ai → open_source_ai/weeks` 매핑을 추가하고 덱·슬라이드 수 상수를 빌드 결과로 갱신했다.
- 검수: 주차별 기술·형식 검수와 교육적 정합성 검수를 거쳤고 Python 예제는 문법 검사(`py_compile`)와 ruff 치명 오류 검사를 통과했다. 모델·GPU 실행은 기준 PC 실측 대기.
- `_forAI/` 문서 세트를 실제 구조·명령·규칙으로 채웠다.

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
