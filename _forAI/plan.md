# Plan

## 목차

- [Current goal](#current-goal)
- [Near-term work](#near-term-work)
- [미커밋 변경 처리](#미커밋-변경-처리)
- [웹프로그래밍 후속 작업](#웹프로그래밍-후속-작업)
- [Android 후속 작업](#android-후속-작업)
- [오픈소스 AI 후속 작업](#오픈소스-ai-후속-작업)
- [공용 도구·사이트·문서 작업](#공용-도구사이트문서-작업)
- [기존 과목의 대기 작업](#기존-과목의-대기-작업)
- [Structure decisions](#structure-decisions)
- [Risks](#risks)

## Current goal

- 2026-11-18 작업 트리의 커밋 안 된 변경(웹 C01 개편, WlEno 2.0.0과 두 과목의 반영, 에이전트 지침, `_forAI` 갱신)을 검토하고 커밋 여부와 묶음을 정한다. 결정은 사용자가 한다.
- 웹: C01 개편(15주와 특강 6개, 일반 차시 60+30, hash SPA 특강)을 수업에 연결한다. 공용 수정·삭제 권한, Pages 실배포, 비공개 평가 자료 정합성은 후속 확인한다.
- Android: 정규 11~15주(RoomControl + WlEno + AAR)를 예제 빌드, AAR 재빌드, 실기기·학교 Wi-Fi 연결로 검증한다. BLE·SmartIO 11~15주는 보존 특강으로 유지한다.
- 오픈소스 AI: 2026-11-13에 개편한 10~15주(시뮬레이터 제어·챗봇 성능 평가)를 포함한 15주 교재를 실습실 Windows·GPU에서 재현 검증해 개강 최소 2주 전 배포 가능 상태로 만든다.

## Near-term work

### 미커밋 변경 처리

1. 변경을 만든 세션과 근거를 확인한다. 웹 C01 개편분과 WlEno 2.0.0 재작성은 작성 세션이 기록에 없다. WlEno 2.0.0은 2026-11-12 결정(연결·해제 때 LED 끄기)을 바꾸는데 그 결정 출처가 저장소에 없다.
2. 커밋 묶음을 정한다. 도구와 문서가 따로 커밋되면 서로 어긋나므로 다음처럼 묶는 것을 제안한다.
   - WlEno 묶음: `tools/wleno`(수정 3, 삭제 3, 새 파일 17), `tools/bleuno-control`(수정 3), Android 범위 수정 27개, 오픈소스 AI 수정 32개, `android_programming/AGENTS.md`·`CLAUDE.md`, `open_source_ai/AGENTS.md`·`CLAUDE.md`
   - 웹 묶음: `web_programming`(수정 380, 삭제 24, 새 파일 341. `AGENTS.md`·`CLAUDE.md` 포함)과 루트 `README.md`·`package.json`·`scripts/render-site.mjs`·`scripts/check-site.mjs`·`site/catalog.json`. 루트 상수(58개 덱·1,175장)는 hash SPA 특강이 있어야 맞으므로 웹 묶음과 함께 커밋한다.
   - 문서 묶음: 루트 `AGENTS.md`·`CLAUDE.md`, `_forAI` 5개 문서
3. 커밋 전에 공개 저장소 규칙 위반을 고친다. `web_programming/reviews/2026-11-18-course-audit/`의 작업 PC 절대 경로(week01.md 71행, week03.md 68행, week04.md 86행, week05.md 65행, week06.md 54행, week14.md 75행, planning-review-technical.md 74·77행, `evidence/synth-*.mjs` 3개의 import 경로), final.md 58행의 세션 상태 문장, 개편 기록 여러 곳의 사용자 호칭, `web_programming/specials/synthesizer/walkthrough.md` 22행의 작업 PC 모양 예시 경로(`<내 폴더>/web-synth` 같은 자리표시자로 바꾼다)가 대상이다.
4. 커밋 전에 `android_programming/iot_sim/lab.md` 41행 "연결·해제 때 시뮬레이터는 LED를 끈다."를 WlEno 2.0.0 동작(상태 유지)에 맞춘다. 같은 문서 4절 표와 모순된다.
5. 커밋한 뒤 `git diff --cached --check`와 `git ls-files --eol`로 CRLF가 남지 않았는지 확인하고, push 뒤 Pages에서 58개 덱과 옛 주소 리다이렉트(`formerIds`)가 열리는지 본다.

### 웹프로그래밍 후속 작업

1. 공용 Supabase에서 연습 글을 대상으로 올바른 편집 키·다른 키·키 없음의 PATCH·DELETE를 비교하고 같은 ID의 GET으로 실제 변경을 판정한다. id·book_id·created_at 보호 열 거부도 확인한다.
2. 독립 폴더 하나, 우선 Supabase 07 완성 방명록을 Pages에 게시하고 HTTPS 화면에서 API 요청·CORS·다른 기기 공유를 확인한다. 교재 슬라이드 사이트 배포를 예제 앱 배포로 간주하지 않는다.
3. 수업 인원에 맞게 추가 방명록 태그 등록·키 배부를 준비한다. 공용 확인 태그는 student01·student02이며 로컬 student01~30을 그대로 공용 등록 완료로 표시하지 않는다. 기존 편집 키를 덮어쓰지 않는 절차를 정한다.
4. 비공개 대본·해답·평가 자료를 C01 개편 전체에 맞춘다. 1~15주 60+30 시간표, 15주 13문항 문제은행, 12~14주 설정 패널의 제공 범위가 기준이다. 기존 개편 안내와 과거 자료는 보존하고 레포트 일정·배점은 학교별 별도 공지로 관리한다.
5. 정규 수업을 리허설한다. 일반 차시 강의·시연 60분 + 실습 30분, 9주 발표 75분(30명 기준, 31명 이상은 사전 영상)이 실제로 맞는지 본다. 연구 특강은 학생의 단계별 진행으로 조정하고, IoT의 모의 온도·메모리 상태·통신 실패 실험 범위를 실제 장치 성능 평가와 구분한다.
6. 11~14주 완성본 `styles.css`에 10주까지 있던 두 줄(h1 `word-break: keep-all`, 입력 `box-sizing: border-box`)을 되살릴지 정한다. 6→7→9→10주와 11→12→13→14주는 홈 파일 해시가 같고 10→11주에서만 다르다. 정하기 전에는 11~14주 `styles.css`를 서로 같게 둔다.
7. 첫 운영에서 잰다: 11주 폼 복원부터 15주 독립 작성까지의 완료 시간과 오류 유형, 9주 발표 인원별 전환 시간, 기말 API 대체 서버와 감독 운영. 에이전트 수행 시간으로 대신하지 않는다.
8. 7주 타임라인(`day1/ex03b_list`와 방명록 피드) 후속 변경의 학습·기능 독립 심사를 받는다. 2026-11-18 최종 점수는 20:36:44 기준본에 한정되고 이 변경은 덱 넘침 재검사만 받았다.
9. 외부 환경을 검증한다: VS Code REST Client 확장 UI 직접 조작, Kakao 지도 실제 연결, 신시사이저 청취.
10. 작은 교재 오류를 고친다. `weeks/week15_final_exam/examples/README.md` 19행 "한 요청로", 작업 트리의 빈 폴더(7주 `day2/ex06~ex08`, 15주 `w12_fetch_cards/data`, `w14_readme_images/images`·`screenshots`), `weeks/README.md` 주차 폴더 구성 표에 `slides_en.md`가 없는 것이 대상이다.

### Android 후속 작업

1. 새 11~15주 예제 9개 폴더를 Empty Views Activity 프로젝트에 넣어 `assembleDebug`로 빌드하고, `tools/wleno/android`에서 `gradlew packageDistribution`으로 AAR을 다시 만든다. Release AAR 0.1.0과 WlEno 2.0.0을 에뮬레이터에서 실제로 연결한 기록도 dev_log에 남긴다.
2. WlEno 미검증 환경을 확인한다: macOS·Linux 실행, 다른 PC의 에뮬레이터, 실기기, 학교 Wi-Fi(단말 격리)에서 TCP 8266 연결.
3. 비공개 짝 저장소의 11~15주 자료를 RoomControl 수업에 맞춘다. 대본·해답을 새로 만들고, 주차 검사 스크립트가 새 구조(bleuno 없음, 11~15주 슬라이드 구간 제목 형식)에서 도는지 확인한다. 옛 `sim.py`용 `test_sim.py`를 공개 `tools/wleno/tests`로 대체할지 정한다. 이전 계획에 있던 두 가지도 확인한다: 10주차 수정 뒤 줄 번호를 다시 맞추고 `check_week.py`를 다시 돌리는 일, 비공개 문서에 '`dev/android/blueno` 기준'이라고 적은 문장 정리(갈래는 `6af3108`에서 main에 합쳐졌다).
4. 정규 9·10주에 남은 "12주차 BLE" 서술을 고친다. 9주 README 120·122행·slides 355행, 10주 README 9행·lab 3행·slides 12·335·371행·walkthrough 953행, `ConnState.kt` 주석(9·10주 예제와 walkthrough), 10주 `examples/README.md` 138행, `site/catalog.json`의 10주 설명(한·영)이 대상이다. 지금 12주는 조명 선택과 밝기 수업이므로 권한 수업의 목적을 다시 쓴다.
5. 11~15주 슬라이드의 구간 제목 형식을 통일할지 정한다. 1~10주는 `## N일차 · A–B분 — 제목`, 11·14·15주는 `# N일차 · A~B분: 제목`, 12·13주는 `# N일차 · A~B분 · 제목`이다. 비공개 대본 대조 도구와 맞는지 함께 본다.
6. `specials/legacy_week13_ble_output/README.md` 68행은 `../../iot_sim/lab.md`를 "Wi-Fi 시뮬레이터 실습"으로 안내하지만 그 문서는 이제 RoomControl 수업 전 연결 점검이다. 링크와 설명을 고친다.
7. `android_programming/ta_setup_guide.md`에서 Python 3.10이 필수 표와 "필요할 때만 설치" 표에 함께 있다. 설치 조건을 하나로 정한다.

### 오픈소스 AI 후속 작업

1. 10~13주 시뮬레이터 실행 명령 `python tools/wleno/main.py`가 uv만 준비한 실습실 PC에서 실행되는지 확인한다. `ta_setup_guide.md`는 Python을 uv로만 준비하게 하고 `python` 명령과 Tkinter를 요구하지 않는다. 안 되면 조교 설치 목록에 Python 3.10 이상·Tkinter를 넣거나 `uv run --no-project --python 3.12 tools/wleno/main.py`를 대안으로 검증한다(2026-11-18에는 `--help`만 확인).
2. 12주 `examples/period1/README.md`의 WlEno 시작 명령에 `--bind 127.0.0.1`을 붙여 10·11주와 맞출지 정한다. 지금 명령은 TCP·UDP를 모든 주소에 연다.
3. `tools/bleuno-control`의 Ollama 시스템 프롬프트가 미커밋으로 바뀌었다(두 문장 추가). `tools/bleuno-control/README.md`의 "2026-11-13 실행 기록" 표는 이전 프롬프트로 잰 값이므로 다시 재거나 표에 측정 시점의 프롬프트를 밝힌다.
4. 생성 모델 기본값을 정리할지 정한다. 4~7·9~11·14주차는 `qwen3.5:2b`, 1~3주차와 8주차 일부 예제·`ta_setup_guide.md`는 `qwen3:8b`다. 8주차는 한 주 안에서 섞인다. README는 "모의 A의 `.env`에도 `OLLAMA_MODEL=qwen3.5:2b`"라고 쓰지만 두 `make_broken_repo.ps1`은 `OLLAMA_MODEL=qwen3:8b`를 쓴다. 바꿀 곳 목록은 `open_source_ai/AGENTS.md`의 '생성 모델 기본값' 행에 있다.
5. 문서의 낡은 구조 서술을 고친다. `weeks/README.md` 주차 폴더 구성 표의 walkthrough 목록(실제 1·3·4·5·6·7·9·10·11·12·13주차)과 39행 "uv.lock은 환경 기준표 확정 후 생성", `materials_plan.md` 3절 폴더 구조(walkthrough·평가 문서 위치, `slides_en.md`, 14주차 `evaluation_spec.md`·`report_template.md` 누락)가 대상이다.
6. `_forAI/dev_log.md`에는 2026-09-04~11-12의 오픈소스 AI 커밋 23개(10-29 과정 순서 개편, 11-05 6주차 RAG, 11-12 7주차 LoRA 등)의 기록이 없다. 필요하면 `git log --since='2026-09-04 00:00' --until='2026-11-13 00:00' -- open_source_ai`로 보충한다.

### 공용 도구·사이트·문서 작업

1. `android_programming/specials/synthesizer/`와 `open_source_ai/specials/synthesizer/`의 악보 JSON 2개를 지울지 정한다. 웹 특강 `web_programming/specials/synthesizer/score/`의 같은 파일과 내용이 같고 참조하는 문서가 없다. 대중가요 악보라 공개 저장소 저작권 검토도 함께 한다.
2. `environment_baseline_template.md` 100행 "BLE 실습은 에뮬레이터만으로 완료 판정하지 않고…"를 정규 Android 11~15주(에뮬레이터 + WlEno)에 맞게 고치고, WlEno용 Python·Tkinter 행을 더할지 정한다.
3. `_forAI/lecture-video.md`의 Android 교재 링크(`../android_programming/weeks/week11_content_provider/examples/README.md`)가 깨졌다. 대상은 `android_programming/specials/legacy_week11_content_provider/examples/README.md`로 옮겨졌다. 이 문서는 사용자 동의를 받고 고친다.
4. Markdown 문서의 상대 링크·`#앵커` 검사 스크립트를 저장소에 둘지 정한다. 지금은 빌드된 덱 HTML만 `check-site.mjs`가 검사한다.
5. 세 과목 `weeks/README.md`의 주차 폴더 구성 표에 `slides_en.md`를 넣는다.
6. 여러 에이전트 운영 기준의 "3번 반복"을 확인한다. 루트 `AGENTS.md`는 "다시 작업 최대 3번"(총 4회차)으로 적었다. 사용자의 뜻이 총 3회차라면 고친다.

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
- 웹 주차 폴더 이름은 기존 링크를 위해 유지한다. 12주 GET→13주 POST→14주 PATCH·DELETE→15주 복습·개인 실기로 이어지며 레포트는 별도다.
- 웹 일반 27차시는 강의·시연 60분 + 실습 30분이다. SPA는 정규 과정에 넣지 않고 14주 뒤 선택 특강 `specials/hash_spa/`에서 다루며 정규 시험에 내지 않는다. 12~14주 API 설정은 제공 코드 `shared/api-settings.js` 패널로 받아 메모리에만 둔다(C01 개편, 미커밋).
- Supabase 특강 예제는 README만 있는 루트와 독립 폴더 01~07을 쓴다. 각 폴더의 .http·.env.example과 브라우저용 config.example.js를 함께 유지한다. 06 요청 실험과 07 완성 UI를 합치지 않는다.
- 정규 학생은 강의자 API를 사용하고, 방학 연구 특강의 담당자는 새 프로젝트를 직접 구축한다. 계정 없는 참여자는 강의자 시연과 공용 API 실습을 사용한다.
- Android 정규 11~15주는 RoomControl + WlEno + AAR 한 개다(커밋 `738c81f`). 학생은 연결 화면과 제어 화면만 작성하고 소켓·스레드·검색은 AAR이 맡는다. 옛 11~15주는 `specials/legacy_week11~15`에 보존하고 새 수업에 맞춰 고치지 않는다.
- `tools/wleno`와 `tools/bleuno-control`은 Android와 오픈소스 AI가 함께 쓰는 공용 도구다. 한 과목 작업에서 동작을 바꾸지 않고 두 과목 문서를 같이 고친다.
- 오픈소스 AI 응용은 `materials/` 챕터 구조 대신 다른 과목과 같은 `weeks/weekNN_slug/` 구조를 쓴다.
- 오픈소스 AI 수업 시간 구조는 60분 블록 × 3(설명 20 + 실습 30 + 휴식 10)이며 자료는 "교시" 단위로 쓴다. 분반별 요일 배치는 학교 문서가 정한다.
- 강의 대본·해답은 비공개 짝 저장소에 같은 주차 폴더 이름으로 둔다.
- 오픈소스 AI 평가 문서 파일명: 종합과제 `assignment_brief.md`·`assignment_rubric.md`(4·8·12·15주차), 실기 `exam_structure.md`·`exam_rubric.md`(8주차), 14주차 `assignment_brief.md`·`evaluation_spec.md`·`report_template.md`, 15주차 `final_review_rubric.md`·`presentation_rubric.md`(이름만 남긴 AI 성능 루브릭). 제안 문서(`proposal_template.md`·`proposal_rubric.md`)는 `specials/project_delivery/week10_project_governance`의 보존 자료다.
- 오픈소스 AI 새 예제는 모델·주소·학습 값을 파일 맨 위 대문자 상수로 둔다(2026-11-05). 5·6·9주차 `src/shared`와 8주차 `period3/config.py`·두 `broken_project/report.py`는 아직 `OLLAMA_MODEL` 환경변수를 읽는다. 기본값 표는 `open_source_ai/weeks/README.md`의 「교재 검증용 기본값」이다.

## Risks

- 2026-11-18 커밋 안 된 변경(수정 450, 삭제 27, 새 파일 358)은 작업 PC 한 곳에만 있다. 커밋·push 전까지 잃을 수 있다.
- 공용 방명록의 조회·추가는 공개 허용이다. book_id를 개인 접근 제한이나 학생 인증으로 해석하면 안 된다. 편집 키도 작성자 개인이 아닌 방명록 전체의 편집 권한이다.
- 공용 PATCH·DELETE와 Pages 실배포는 아직 검증하지 않았다. 로컬 자동 시험·REST Client 성공·localhost 브라우저 성공을 이 검증의 완료로 합치지 않는다.
- 실제 .env·localfiles·.local·편집 키가 소스·ZIP·Pages·요청 이력 캡처에 포함되지 않게 확인한다. 브라우저가 읽는 publishable key와 비밀 키를 구분한다. 웹 빌드는 `examples/`의 추적 안 된 새 파일도 사이트로 복사한다.
- 로컬 정적 서버, 홈 IoT Node 서버, WlEno는 현재 터미널의 프로세스다. 포트가 계속 열려 있거나 다음 세션에서도 살아 있다고 가정하지 않는다.
- 공개 자료와 비공개 평가 자료의 개편 진행 상태가 다르다(웹 C01, Android 11~15주, 오픈소스 AI 10~15주). 과거 실측 수치와 해답을 새 교재 결과로 표시하지 않는다.
- 모델 태그 변동: `qwen3.5:2b`, `qwen3:8b`, `bge-m3`, `Qwen/Qwen2.5-0.5B-Instruct` 등은 교재 작성 시점 기준이며 제공자가 같은 태그를 다른 빌드로 옮길 수 있다. 실제로 `qwen3:4b`가 생각 전용 빌드로 바뀐 적이 있다. 환경 기준표에서 확정한다.
- `transformers`·`peft`·`trl` API 변동: 7주차 LoRA 학습 예제는 메이저 버전 변화에 취약하다. 12주차는 `cactus-compute==4.2.0`(JAX)에 버전을 고정했다. lock 확정 후 재실행 검증이 필요하다.
- Ollama `think` 옵션과 툴 호출은 특정 버전 이상에서만 동작한다. 기준표의 Ollama 버전으로 확인한다.
- RTX 4070 실측(6주차 임베딩, 7주차 LoRA, 12주차 Needle 학습)이 아직 없다. 30분 실습 분량 판단이 실측 후 바뀔 수 있다.
- 사이트 검증 스크립트의 슬라이드 수 고정 검사는 원고 수정마다 상수 갱신을 요구한다.
- WlEno 2.0.0은 보드 펌웨어(`gbox3d/bleuno` main 1.0.5_dev)와 다르게 동작한다(연결·해제 때 상태 유지, 잘못된 요청 전체 거부, 버전 2.0.0). 보존 특강 문서와 비공개 해답이 보드 규칙과 WlEno 규칙을 섞어 쓰지 않는지 확인한다.
- 공용 도구 변경은 두 과목에 동시에 영향을 준다. `tools/bleuno-control` 프롬프트나 평가 함수를 바꾸면 오픈소스 AI 측정 기록이 낡는다.
