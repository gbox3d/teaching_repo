# Plan

## 목차

- [Current goal](#current-goal)
- [Near-term work](#near-term-work)
- [웹프로그래밍 후속 작업](#웹프로그래밍-후속-작업)
- [Android 후속 작업](#android-후속-작업)
- [오픈소스 AI 후속 작업](#오픈소스-ai-후속-작업)
- [공용 도구·사이트·문서 작업](#공용-도구사이트문서-작업)
- [기존 과목의 대기 작업](#기존-과목의-대기-작업)
- [Structure decisions](#structure-decisions)
- [Risks](#risks)

## Current goal

- 웹: C01 개편(15주와 특강 6개, 일반 차시 60+30, hash SPA 특강), 2026-11-22 설정 방식 변경(`config.example.js` + 공개 키 localStorage, 설정 패널 삭제), 12주 타이머 예제, 2026-11-25 12주 공개 API·13주 CRUD 개편과 편집 키 폐지(`bd02eaa`)를 수업에 연결한다. 13·14주 화면이 처음부터 수업용 서버로 PATCH·DELETE를 보내므로 공용 서버의 공개 CRUD 정책 적용을 수업 전에 확인한다. Pages 화면 조회와 비공개 평가 자료 정합성도 후속 확인한다.
- Android: 정규 11~15주(RoomControl + WlEno + AAR)를 예제 빌드, AAR 재빌드, 실기기·학교 Wi-Fi 연결로 검증한다. BLE·SmartIO 11~15주는 보존 특강으로 유지한다.
- 오픈소스 AI: 2026-11-13에 개편한 10~15주(시뮬레이터 제어·챗봇 성능 평가)를 포함한 15주 교재를 실습실 Windows·GPU에서 재현 검증해 개강 최소 2주 전 배포 가능 상태로 만든다.

## Near-term work

### 웹프로그래밍 후속 작업

1. (수업 전 필수) 공용 Supabase 프로젝트에 `enable-public-crud.sql`을 실행했는지 SQL Editor에서 확인한다. 연습 글을 대상으로 공개 키·키 없음의 PATCH·DELETE를 비교하고 같은 ID의 GET으로 실제 변경을 판정한다. id·book_id·created_at 보호 열 거부와 PATCH·DELETE의 CORS 사전 요청도 확인한다. 13·14주 예제는 기본값이 수업용 서버다.
2. 독립 폴더 하나, 우선 Supabase 07 완성 방명록을 Pages에 게시하고 HTTPS 화면에서 공개 키 묻는 창·**공개 키 지우기**·API 요청·CORS·다른 기기(휴대폰 포함) 공유를 확인한다. 13주 `config.json`은 사이트 빌드가 복사하지 않으므로 Pages에서 13주 예제를 어떻게 보여 줄지도 정한다. 교재 슬라이드 사이트 배포를 예제 앱 배포로 간주하지 않는다.
3. 수업 인원에 맞게 방명록 태그를 등록하고 공용 공개 키를 배부할 준비를 한다. 기존 공용 프로젝트의 등록 태그를 `select book_id from private.classroom_books`로 확인하고, 모자라면 `book_id`만 insert한다. 로컬 student01~30을 그대로 공용 등록 완료로 표시하지 않는다.
4. 비공개 대본·해답·평가 자료를 C01 개편, 2026-11-22 변경, 2026-11-25 `bd02eaa`(12주 2일차 공개 API, 13주 CRUD 네 예제와 `config.json`, 14주 수정·삭제 결과 확인, 편집 키 폐지)에 맞춘다. 1~15주 60+30 시간표, 15주 13문항 문제은행, 12주 1차시 새 구간(타이머 준비 5·타이머를 기다리는 동안 7·wait 함수 8·async 함수와 await 10·async 함수가 돌려주는 값 8·응답에서 할 일 제목까지 10·같은 요청에 await 7·안내 5, 실습 0~8분은 ex01c 사본에 '4. 3초 지남' 더하기), 12~15주·hash SPA·Supabase 특강의 공개 키 입력 절차(묻는 창, **공개 키 지우기**. 옛 설정 패널·Console 안내를 지운다)가 기준이다. 15주 채점·감독 안내에는 연습 때 저장한 키가 남으면 **공개 키 지우기** 뒤 시험용 키를 넣는 절차를 넣는다. 기존 개편 안내와 과거 자료는 보존하고 레포트 일정·배점은 학교별 별도 공지로 관리한다.
5. 정규 수업을 리허설한다. 일반 차시 강의·시연 60분 + 실습 30분, 9주 발표 75분(30명 기준, 31명 이상은 사전 영상)이 실제로 맞는지 본다. 연구 특강은 학생의 단계별 진행으로 조정하고, IoT의 모의 온도·메모리 상태·통신 실패 실험 범위를 실제 장치 성능 평가와 구분한다.
6. 11~14주 완성본 `styles.css`에 10주까지 있던 두 줄(h1 `word-break: keep-all`, 입력 `box-sizing: border-box`)을 되살릴지 정한다. 6→7→9→10주와 11→12→13→14주는 홈 파일 해시가 같고 10→11주에서만 다르다. 정하기 전에는 11~14주 `styles.css`를 서로 같게 둔다.
7. 첫 운영에서 잰다: 11주 폼 복원부터 15주 독립 작성까지의 완료 시간과 오류 유형, 9주 발표 인원별 전환 시간, 기말 API 대체 서버와 감독 운영. 에이전트 수행 시간으로 대신하지 않는다.
8. 7주 타임라인(`day1/ex03b_list`와 방명록 피드) 후속 변경의 학습·기능 독립 심사를 받는다. 2026-11-18 최종 점수는 20:36:44 기준본에 한정되고 이 변경은 덱 넘침 재검사만 받았다.
9. 외부 환경을 검증한다: VS Code REST Client 확장 UI 직접 조작, Kakao 지도 실제 연결, 신시사이저 청취.
10. 작은 교재 오류를 고친다. `weeks/week15_final_exam/examples/README.md` 19행 "한 요청로", 12주 `ex01/README.md` 5행의 "`resolve(message)`로 넘긴 문자열"(코드는 `resolve('3. 타이머 완료')`), `weeks/README.md` 152행 표의 `||`가 칸 구분으로 읽히는 것(`\|\|`), `weeks/README.md` 주차 폴더 구성 표에 `slides_en.md`가 없는 것, `specials/synthesizer/walkthrough.md` 22행의 작업 PC 모양 예시 경로(`<내 폴더>/web-synth` 같은 자리표시자로 바꾼다)가 대상이다.
11. REST Client 기본값을 맞출지 정한다. 14주 4개, 15주 REST 문항 3개, hash SPA 04의 `.env.example`은 로컬 모의 API(`127.0.0.1:8787`, `classroom-local`)를 가리키고, 브라우저 기본값(`config.example.js`)은 수업용 서버다. 그대로면 REST Client로 읽은 글 ID가 화면 쪽 서버에 없을 수 있다.
12. 조회 실패 문구 "`조회 실패: ${error.message}. 새로 불러오기를 누르세요.`"는 401(키 미입력·오류)일 때 맞지 않는다. 14주 `web-week14/guestbook.js`와 walkthrough 인용, hash SPA 04 `app.js` 세 곳을 함께 고칠지 정한다(13주 두 곳은 `bd02eaa`에서 없어졌다). 12주 선택 방명록의 "주소와 연결을 확인하세요."도 같다.
13. 12주 완성본의 `screenshots/guestbook.png`에 옛 "API 설정" 줄이 찍혀 있다(13주 캡처는 `bd02eaa`에서 옛 폴더와 함께 지워졌다). 참조하는 문서는 없다. 다시 찍거나 지운다. 14주 캡처도 함께 본다.
14. 입력 `pattern="[a-z0-9_-]{1,40}"`은 HTML 표준이 쓰는 `v` 플래그에서 문법 오류라 브라우저가 검사를 건너뛴다(Supabase 특강 04·07 등). `[a-z0-9_\-]{1,40}`로 고칠지 정한다.
15. 사이트 데이터가 차단된 브라우저처럼 localStorage 접근이 예외를 던지면 `config.example.js`가 중간에 멈춰 뒤의 `app.js`가 `ReferenceError`로 멈춘다. 드문 경우라 그대로 두었다. 첫 운영에서 나오면 정본에 예외 처리를 넣는다.
16. 학기 말 공개 키 교체 절차를 정한다. 편집 키가 없어진 뒤(`bd02eaa`)에는 키를 바꾸는 것이 지난 학기 사용자의 수정·삭제를 막는 유일한 방법이다. Supabase 공식 문서에는 publishable key의 삭제·교체가 적혀 있지 않다(2026-11-22 확인). 대시보드 Settings > API Keys에서 새로 만들기·삭제가 되는지 확인하고, 안 되면 RLS 정책을 닫는 SQL을 학기 말 절차로 둔다. 2026-11-22 이전 커밋에는 키 값이 남아 있다.
17. 12주 README에 '이번 주 용어' 표가 없고, 12주 `examples/README.md`에 W3.CSS CDN 주소 안내가 없다(과목 지침과 다르다). 12주 README 2차시 행의 구간 이름(환율 요청 준비·응답 필드 읽기…)이 slides 2일차 장 제목(달러 기준 환율 요청·중첩 객체에서 환율 읽기…)과 다르다.
18. 13→14주 설정 방식을 하나로 할지 정한다. 13주 완성본은 `config.json`을 읽고 14주 완성본은 `config.example.js`와 묻는 창을 쓴다. 학생이 13주 결과를 14주 시작점으로 이어 쓰면 설정 파일과 키 입력 방식이 바뀐다. 과목 지침의 13주 결정 기록은 "14주 이후에도 같은 설정이 필요할 때" 다시 본다고 적었다.
19. 공용 공개 키로 누구나 모든 태그의 글을 지울 수 있다. 수업 중 장난이나 실수로 다른 학생의 글이 지워졌을 때의 복구 방법(Supabase 백업, 강의자 재등록)과 수업 안내 문구를 정한다.

### Android 후속 작업

1. 새 11~15주 예제 9개 폴더를 Empty Views Activity 프로젝트에 넣어 `assembleDebug`로 빌드하고, `tools/wleno/android`에서 `gradlew packageDistribution`으로 AAR을 다시 만든다. Release AAR 0.1.0과 WlEno 2.0.0을 에뮬레이터에서 실제로 연결한 기록도 dev_log에 남긴다.
2. WlEno 미검증 환경을 확인한다: macOS·Linux 실행, 다른 PC의 에뮬레이터, 실기기, 학교 Wi-Fi(단말 격리)에서 TCP 8266 연결.
3. 비공개 짝 저장소의 11~15주 자료를 RoomControl 수업에 맞춘다. 대본·해답을 새로 만들고, 주차 검사 스크립트가 새 구조(bleuno 없음, 11~15주 슬라이드 구간 제목 형식)에서 도는지 확인한다. 옛 `sim.py`용 `test_sim.py`를 공개 `tools/wleno/tests`로 대체할지 정한다. 이전 계획에 있던 두 가지도 확인한다: 10주차 수정 뒤 줄 번호를 다시 맞추고 `check_week.py`를 다시 돌리는 일, 비공개 문서에 '`dev/android/blueno` 기준'이라고 적은 문장 정리(갈래는 `6af3108`에서 main에 합쳐졌다).
4. 정규 9·10주에 남은 "12주차 BLE" 서술을 고친다. 9주 README 120·122행·slides 355행, 10주 README 9행·lab 3행·slides 12·335·371행·walkthrough 953행, `ConnState.kt` 주석(9·10주 예제와 walkthrough), 10주 `examples/README.md` 138행, `site/catalog.json`의 10주 설명(한·영)이 대상이다. 지금 12주는 조명 선택과 밝기 수업이므로 권한 수업의 목적을 다시 쓴다.
5. 11~15주 슬라이드의 구간 제목 형식을 통일할지 정한다. 1~10주는 `## N일차 · A–B분 — 제목`, 11·14·15주는 `# N일차 · A~B분: 제목`, 12·13주는 `# N일차 · A~B분 · 제목`이다. 비공개 대본 대조 도구와 맞는지 함께 본다.
6. `specials/legacy_week13_ble_output/README.md` 68행은 `../../iot_sim/lab.md`를 "Wi-Fi 시뮬레이터 실습"으로 안내하지만 그 문서는 이제 RoomControl 수업 전 연결 점검이다. 링크와 설명을 고친다.
7. `android_programming/ta_setup_guide.md`에서 Python 3.10이 필수 표와 "필요할 때만 설치" 표에 함께 있다. 설치 조건을 하나로 정한다.

### 오픈소스 AI 후속 작업

1. 11·12주 시뮬레이터 실행 명령 `python tools/wleno/main.py`가 uv만 준비한 실습실 PC에서 실행되는지 확인한다. `ta_setup_guide.md`는 Python을 uv로만 준비하게 하고 `python` 명령과 Tkinter를 요구하지 않는다. 10주는 `d0ad054`에서 `uv run wleno`로 바꿨으므로, 11~13주도 PyPI의 `wleno`로 옮길지 함께 정한다(지금은 `tools/bleuno-control` 상대 경로).
2. 12주 `examples/period1/README.md`의 WlEno 시작 명령에 `--bind 127.0.0.1`을 붙여 10·11주와 맞출지 정한다. 지금 명령은 TCP·UDP를 모든 주소에 연다.
3. `tools/bleuno-control`의 Ollama 시스템 프롬프트가 `543ab2e`에서 바뀌었다(두 문장 추가). `tools/bleuno-control/README.md`의 "2026-11-13 실행 기록" 표는 이전 프롬프트로 잰 값이므로 다시 재거나 표에 측정 시점의 프롬프트를 밝힌다.
4. 생성 모델 기본값을 정리할지 정한다. 4~7·9~11·14주차는 `qwen3.5:2b`, 1~3주차와 8주차 일부 예제·`ta_setup_guide.md`는 `qwen3:8b`다. 8주차는 한 주 안에서 섞인다. README는 "모의 A의 `.env`에도 `OLLAMA_MODEL=qwen3.5:2b`"라고 쓰지만 두 `make_broken_repo.ps1`은 `OLLAMA_MODEL=qwen3:8b`를 쓴다. 바꿀 곳 목록은 `open_source_ai/AGENTS.md`의 '생성 모델 기본값' 행에 있다.
5. 문서의 낡은 구조 서술을 고친다. `weeks/README.md` 주차 폴더 구성 표의 walkthrough 목록(실제 1·3·4·5·6·7·9·10·11·12·13주차)과 39행 "uv.lock은 환경 기준표 확정 후 생성", `materials_plan.md` 3절 폴더 구조(walkthrough·평가 문서 위치, `slides_en.md`, 14주차 `evaluation_spec.md`·`report_template.md` 누락)가 대상이다.
6. `_forAI/dev_log.md`에는 2026-09-04~11-12의 오픈소스 AI 커밋 23개(10-29 과정 순서 개편, 11-05 6주차 RAG, 11-12 7주차 LoRA 등)의 기록이 없다. 필요하면 `git log --since='2026-09-04 00:00' --until='2026-11-13 00:00' -- open_source_ai`로 보충한다.
7. 실습실 Windows PC에서 10주 학생용 ZIP(`week10-simulator-lab-0.1.0.zip`)을 받아 `uv sync --locked` → `uv run wleno --bind 127.0.0.1` → `uv run ex01`~`ex03`을 재현한다. 학교망에서 PyPI 접속이 막힐 때의 대체 경로도 정한다.
8. 특강 `chatbot_rag_finetune`을 실습실 GPU에서 재현한다. 과목 지침에는 시험 89개 통과만 적혀 있다. 임베딩 RAG, LoRA 학습·병합, GGUF 변환·Ollama 등록의 시간·VRAM은 기록이 없다.

### 공용 도구·사이트·문서 작업

1. `android_programming/specials/synthesizer/`와 `open_source_ai/specials/synthesizer/`의 악보 JSON 2개를 지울지 정한다. 웹 특강 `web_programming/specials/synthesizer/score/`의 같은 파일과 내용이 같고 참조하는 문서가 없다. 대중가요 악보라 공개 저장소 저작권 검토도 함께 한다.
2. `environment_baseline_template.md` 100행 "BLE 실습은 에뮬레이터만으로 완료 판정하지 않고…"를 정규 Android 11~15주(에뮬레이터 + WlEno)에 맞게 고치고, WlEno용 Python·Tkinter 행을 더할지 정한다.
3. `_forAI/lecture-video.md`의 Android 교재 링크(`../android_programming/weeks/week11_content_provider/examples/README.md`)가 깨졌다. 대상은 `android_programming/specials/legacy_week11_content_provider/examples/README.md`로 옮겨졌다. 이 문서는 사용자 동의를 받고 고친다.
4. Markdown 문서의 상대 링크·`#앵커` 검사 스크립트를 저장소에 둘지 정한다. 지금은 빌드된 덱 HTML만 `check-site.mjs`가 검사한다.
5. 세 과목 `weeks/README.md`의 주차 폴더 구성 표에 `slides_en.md`를 넣는다.
6. 여러 에이전트 운영 기준의 "3번 반복"을 확인한다. 루트 `AGENTS.md`는 "다시 작업 최대 3번"(총 4회차)으로 적었다. 사용자의 뜻이 총 3회차라면 고친다.
7. WlEno 2.0.0(`543ab2e`)은 2026-11-12 결정(연결·해제 때 LED 끄기)을 '상태 유지'로 바꿨는데 그 결정의 출처가 저장소에 없다. 사용자에게 확인해 `tools/wleno/README.md`나 과목 지침의 결정 사항에 근거를 남긴다.
8. push 뒤 Pages에서 옛 주소 리다이렉트(`formerIds`)가 실제로 열리는지 본다. 웹 13주의 옛 `week13_release_security` 주소(`bd02eaa`)도 대상이다. 2026-11-23에는 첫 화면과 12·13주 새 예제 파일의 HTTP 200만 확인했다.
9. 홈 IoT 시뮬레이터 `server.mjs`의 경로 비교가 드라이브 문자 대소문자를 구분해, 셸 경로가 `c:\…`이면 시험 하나가 404로 실패한다(memo의 저장소 공통 교훈). 비교 전에 두 경로를 같은 방식으로 정규화할지 정한다.
10. 원격 브랜치 `fix/github-classroom-reset-windows`를 어떻게 할지 정한다. main에 없는 커밋 1개(2026-11-06 Windows 판 재작성, 실기 검증 전)가 남아 있다. 실기 검증 뒤 합치거나 버린다. main에 합쳐진 `dev/android/blueno`(로컬·원격)와 `docs/week01-git-status-slides`는 2026-11-28에 지웠다.

### 기존 과목의 대기 작업

1~7은 오픈소스 AI, 8~10은 Android 항목이다. 다른 문서가 번호로 가리키므로 번호를 유지한다. 11번(Android 작업 갈래 `dev/android/blueno` 병합)은 2026-11-12 `6af3108`에서 이미 합쳐져 지웠다(dev_log 2026-11-18). 2026-11-18에 더한 항목은 위 과목별 절에 있다.

1. 실습실 PC에 설치할 프로그램 버전(Python·uv·Ollama·PyTorch·`cactus-compute`)과 수업 모델 이름을 `environment_baseline_template.md`의 TBD 칸에 적는다. 4주차부터의 예제 기본값은 `qwen3.5:2b`, 11~13주차는 Needle 3(`cactus-compute==4.2.0`)이다. 1~3·8주차의 `qwen3:8b`는 오픈소스 AI 후속 작업 4번에서 정리한다.
2. Windows·RTX 4070 PC에서 실측한다. 우선 11~13주차 Needle 설치·추론, 12주차 학습(지금은 Mac M1 Max CPU 기록 339.4초뿐), 13주차 Streamlit 앱, 6주차 임베딩, 7주차 LoRA 학습 시간·VRAM이다. 교재가 빈칸으로 둔 수치를 채운다. `uv.lock`은 이미 3·4주차 일부 교시와 5·6·7·9~14주차에 커밋되어 있고 7주차는 8GB GPU 측정 기록이 있다.
3. 8주차 실기평가 패킷(문항·fixture·정답·감독 체크), 15주차 AI 성능 평가·레포트 자료와 비공개 최종 문항(40문항 초안), 챕터 퀴즈 은행은 `teaching_materials_private/open_source_ai/`에 있다. 시행 전에 강의자가 출제를 검토하고 학생 프로그램을 격리 실행하는 절차를 검증한다.
4. 강의 대본 15개를 낭독 리허설해 20분 분량을 조정한다(구간을 바꾸면 `slides.md`도 같이). 10~15주 대본·해답이 2026-11-13 새 흐름, 새 폴더 이름(`29a667a`), WlEno의 LED 유지 동작과 맞는지 확인한다.
5. `npm run build && npm test`가 통과한 상태로 main에 반영해 GitHub Pages에서 오픈소스 AI 덱 17개(15주 + 특강 2개)와 10~15주 옛 주소 리다이렉트 6개가 열리는지 확인한다.
6. `_shared/` 승격 후보 검토: Git 세 영역·PR 흐름(웹 1·2주차 ↔ 오픈소스 AI 2주차), 공개 키·비밀정보 구분과 입력 검증(웹 REST 실습 ↔ 오픈소스 AI 배포 실습). 배포 실습은 이제 정규 주차가 아니라 `specials/project_delivery/week12_ai_service_deploy`의 보존 자료다. 웹 13주차를 이전 릴리스·보안 독립 주제로 되돌리지 않는다.
7. 학교 폴더 `univ_scoring_works/wku/subjects/opensw/materials.md`에 주차↔공용 모듈 매핑과 실제 배점·마감을 연결한다. 10~15주차 새 주제·폴더 이름과 "기존 발표 점수 → AI 성능 평가, 레포트 별도"를 반영한다.
8. Android BLE 특강: type_m v1 원본의 SEN1·VIN 미연결과 모듈 핀 표기를 검토하고, 모터·서보용 설정·정지 동작을 확정한 뒤 확장 실습을 만든다. `RealBleunoClient`의 CCCD 실패 시 READY 처리와 MTU 요청 실패 fallback을 보완할 때는 사본 7곳(`specials/legacy_week12_ble_gatt` day1·day2, `legacy_week13_ble_output` day1, `legacy_week14_ble_input_project` day1·day2, `legacy_week15_final_exam` 두 곳)과 그 특강 walkthrough 부록도 동기화한 뒤 실기 연결·명령·재연결을 검증한다.
9. Android 보존 특강과 BLE 보드에서 아직 확인하지 않은 것이 있다. 지금까지는 에뮬레이터와 펌웨어 소스로만 확인했다.
   - 실제 보드에서 연결·해제 때 외부 LED가 꺼지는지(`bleuno/README.md`에 '펌웨어 소스 기준'으로 적음)
   - 실제 보드에서 앱이 연결된 동안 `blink`를 보내면 내장 LED가 깜빡이는지. 펌웨어 소스로는 연결 중에는 깜빡이지 않고, TENSTAR 빌드는 연결 중 `blink`·`stopblk`를 받으면 파랑 고정 표시가 꺼진다. 실보드로 확인되면 표시를 떼고, 다르면 `bleuno/README.md`를 고친다.
   - 수업 기준 AVD(API 33 이상)에서 RoomControl 연결 점검(`iot_sim/lab.md`)과 특강의 Logcat 흐름을 다시 잰다. 이전 실측은 API 31 에뮬레이터 한 대다.
   - `legacy_week14` 예제의 [재연결] 버튼이 검색 중에 `stopScan()`을 부르지 않는 것을 고칠지 정한다. 고치면 `legacy_week15` 예제와 walkthrough 인용도 같이 고친다.
   - 특강 제어 화면의 명령 로그(`logText`)에 스크롤 설정이 없다(높이 0dp·weight 1). 같은 레이아웃이 bleuno 사본 7곳의 예제에 있다. 고칠지 정한다. 고치면 각 walkthrough의 `activity_control.xml` 전문도 같이 고친다.
   - 공개 `bleuno/README.md`에 펌웨어 `safebackdelay`(설정하면 LED를 저절로 끈다) 설명을 넣을지 정한다. 지금은 비공개 해답에만 있다.
   - 실기기로 한 학생의 오류 글자가 실습지와 다를 때의 제출 판정(비공개 해답의 제출 판정은 초안이다)
10. 10주차 권한 흐름 수정에서 정할 것이 남아 있다. `legacy_week15` 특강 루브릭 P2 확인, 그 해답을 세 갈래로 할지, `verify_rubric15_perm.py` 갱신, starter TODO 문구, 로그·캡처 위치. 10주차 작업에서 보고만 한 두 문제를 고칠지도 정한다. `ConnViewModel`의 `catch (e: Exception)`이 취소를 삼키는 문제는 정규 7·9·10주 예제 6개 파일과 특강 3개 파일(`legacy_week11` day1·day2, `legacy_week12` day1)에 있다. 다른 하나는 Switch 리스너가 회전 때 다시 불리는 문제다.

## Structure decisions

- 저장소 공통 작업 규칙과 여러 에이전트 운영 방식은 루트 `AGENTS.md`, 과목 규칙은 과목 `AGENTS.md`에 둔다. 각 폴더의 `CLAUDE.md`는 `@AGENTS.md` 한 줄이다(2026-11-18).
- 웹 주차 폴더 이름은 기존 링크를 위해 유지한다. 13주만 `week13_guestbook_crud`로 바꾸고 옛 주소는 `formerIds`로 넘긴다(`bd02eaa`). 12주 타이머·공개 API GET → 13주 방명록 CRUD → 14주 수정·삭제 결과 확인 → 15주 복습·개인 실기로 이어지며 레포트는 별도다.
- 웹 일반 27차시는 강의·시연 60분 + 실습 30분이다. SPA는 정규 과정에 넣지 않고 14주 뒤 선택 특강 `specials/hash_spa/`에서 다루며 정규 시험에 내지 않는다. 13주는 Git 제외 `config.json`에서 주소·공개 키·`BOOK_ID`를 읽는다(`bd02eaa`). 그 밖의 REST 예제는 주소와 `BOOK_ID`를 `config.example.js`에 두고, 공개 키는 처음 열 때 `prompt`로 받아 localStorage에 저장하며 화면에는 **공개 키 지우기** 버튼만 둔다(2026-11-22, `8cc49ea`). 결정 기록은 `web_programming/AGENTS.md`에 있다. C01의 설정 패널 `shared/api-settings.js`는 삭제했다.
- 수업용 방명록에는 편집 키가 없다. 공용 공개 키 하나로 모든 태그의 글을 생성·조회·수정·삭제하고, `book_id`는 학생별 글을 찾는 태그다(`bd02eaa`).
- 12주 1일차는 타이머로 Promise·`async` 함수·`await`를 먼저 익힌 뒤 fetch로 넘어간다. 끼운 예제는 7주 `ex03b_list` 선례대로 `ex01b`·`ex01c`·`ex01d`로 이름 붙여 ex02~ex06의 번호와 링크를 유지한다.
- Supabase 특강 예제는 README만 있는 루트와 독립 폴더 01~07을 쓴다. 각 폴더의 .http·.env.example과 브라우저용 config.example.js를 함께 유지한다. 06 요청 실험과 07 완성 UI를 합치지 않는다.
- 정규 학생은 강의자 API를 사용하고, 방학 연구 특강의 담당자는 새 프로젝트를 직접 구축한다. 계정 없는 참여자는 강의자 시연과 공용 API 실습을 사용한다.
- Android 정규 11~15주는 RoomControl + WlEno + AAR 한 개다(커밋 `738c81f`). 학생은 연결 화면과 제어 화면만 작성하고 소켓·스레드·검색은 AAR이 맡는다. 옛 11~15주는 `specials/legacy_week11~15`에 보존하고 새 수업에 맞춰 고치지 않는다.
- `tools/wleno`와 `tools/bleuno-control`은 Android와 오픈소스 AI가 함께 쓰는 공용 도구다. 한 과목 작업에서 동작을 바꾸지 않고 두 과목 문서를 같이 고친다. 두 폴더는 `tools/pyproject.toml`로 PyPI 패키지 `wleno`가 되며, `wleno-v<버전>` 릴리스에 올린 파일을 `publish-wleno.yml`(수동 실행, Trusted Publishing)이 게시한다(`b3f25da`).
- 오픈소스 AI 응용은 `materials/` 챕터 구조 대신 다른 과목과 같은 `weeks/weekNN_slug/` 구조를 쓴다.
- 오픈소스 AI 수업 시간 구조는 60분 블록 × 3(설명 20 + 실습 30 + 휴식 10)이며 자료는 "교시" 단위로 쓴다. 분반별 요일 배치는 학교 문서가 정한다.
- 강의 대본·해답은 비공개 짝 저장소에 같은 주차 폴더 이름으로 둔다.
- 오픈소스 AI 평가 문서 파일명: 종합과제 `assignment_brief.md`·`assignment_rubric.md`(4·8·12·15주차), 실기 `exam_structure.md`·`exam_rubric.md`(8주차), 14주차 `assignment_brief.md`·`evaluation_spec.md`·`report_template.md`, 15주차 `final_review_rubric.md`·`presentation_rubric.md`(이름만 남긴 AI 성능 루브릭). 제안 문서(`proposal_template.md`·`proposal_rubric.md`)는 `specials/project_delivery/week10_project_governance`의 보존 자료다.
- 오픈소스 AI 새 예제는 모델·주소·학습 값을 파일 맨 위 대문자 상수로 둔다(2026-11-05). 5·6·9주차 `src/shared`와 8주차 `period3/config.py`·두 `broken_project/report.py`는 아직 `OLLAMA_MODEL` 환경변수를 읽는다. 기본값 표는 `open_source_ai/weeks/README.md`의 「교재 검증용 기본값」이다.

## Risks

- 공용 방명록은 공개 키만 있으면 모든 태그의 글을 생성·조회·수정·삭제할 수 있다(`bd02eaa`). book_id를 개인 접근 제한이나 학생 인증으로 해석하면 안 된다. 키가 수업 밖으로 퍼지면 누구나 글을 지울 수 있다.
- 공용 PATCH·DELETE와 Pages 화면에서의 조회는 아직 검증하지 않았다. 공용 프로젝트에 `enable-public-crud.sql`을 실행했는지도 기록이 없다. 13·14주 화면은 처음부터 수업용 서버를 부른다. 로컬 자동 시험·REST Client 성공·localhost 브라우저 성공을 이 검증의 완료로 합치지 않는다.
- 공개 키를 묻는 창을 학생이 취소하거나 키를 잘못 넣으면 401이 난다. 화면의 "새로 불러오기"로는 풀리지 않고 새로고침이나 **공개 키 지우기**가 필요하다. 첫 운영에서 막힘을 본다.
- `wleno` 0.1.0은 PyPI에 올린 판이 고정돼 있다. 저장소의 `tools/wleno`·`tools/bleuno-control`만 고치면 10주(PyPI 판)와 11~13주·Android(저장소 코드)의 동작이 갈린다.
- 실제 .env·config.json·localfiles·.local이 소스·ZIP·Pages·요청 이력 캡처에 포함되지 않게 확인한다. 브라우저가 읽는 publishable key와 비밀 키를 구분한다. 웹 빌드는 `examples/`의 추적 안 된 새 파일도 사이트로 복사한다.
- 로컬 정적 서버, 홈 IoT Node 서버, WlEno는 현재 터미널의 프로세스다. 포트가 계속 열려 있거나 다음 세션에서도 살아 있다고 가정하지 않는다.
- 공개 자료와 비공개 평가 자료의 개편 진행 상태가 다르다(웹 C01, Android 11~15주, 오픈소스 AI 10~15주). 과거 실측 수치와 해답을 새 교재 결과로 표시하지 않는다.
- 모델 태그 변동: `qwen3.5:2b`, `qwen3:8b`, `bge-m3`, `Qwen/Qwen2.5-0.5B-Instruct` 등은 교재 작성 시점 기준이며 제공자가 같은 태그를 다른 빌드로 옮길 수 있다. 실제로 `qwen3:4b`가 생각 전용 빌드로 바뀐 적이 있다. 환경 기준표에서 확정한다.
- `transformers`·`peft`·`trl` API 변동: 7주차 LoRA 학습 예제는 메이저 버전 변화에 취약하다. 12주차는 `cactus-compute==4.2.0`(JAX)에 버전을 고정했다. lock 확정 후 재실행 검증이 필요하다.
- Ollama `think` 옵션과 툴 호출은 특정 버전 이상에서만 동작한다. 기준표의 Ollama 버전으로 확인한다.
- RTX 4070 실측(6주차 임베딩, 7주차 LoRA, 12주차 Needle 학습)이 아직 없다. 30분 실습 분량 판단이 실측 후 바뀔 수 있다.
- 사이트 검증 스크립트의 슬라이드 수 고정 검사는 원고 수정마다 상수 갱신을 요구한다.
- WlEno 2.0.0은 보드 펌웨어(`gbox3d/bleuno` main 1.0.5_dev)와 다르게 동작한다(연결·해제 때 상태 유지, 잘못된 요청 전체 거부, 버전 2.0.0). 보존 특강 문서와 비공개 해답이 보드 규칙과 WlEno 규칙을 섞어 쓰지 않는지 확인한다.
- 공용 도구 변경은 두 과목에 동시에 영향을 준다. `tools/bleuno-control` 프롬프트나 평가 함수를 바꾸면 오픈소스 AI 측정 기록이 낡는다.
