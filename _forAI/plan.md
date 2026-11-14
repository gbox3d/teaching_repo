# Plan

## 목차

- [Current goal](#current-goal)
- [Near-term work](#near-term-work)
- [웹프로그래밍 후속 작업](#웹프로그래밍-후속-작업)
- [기존 과목의 대기 작업](#기존-과목의-대기-작업)
- [Structure decisions](#structure-decisions)
- [Risks](#risks)

## Current goal

- 웹 12~15주 REST 개편과 Supabase·HTTP 홈 IoT 연구 특강을 수업에 연결한다. 공개 자료·로컬 실행은 준비되었으며 공용 수정·삭제 권한, Pages 실배포, 비공개 평가 자료 정합성을 후속 확인한다.
- Android BLE 연계: 수업 정본 SmartIO + 공통 클래스 9개(2026-11-12에 Wi-Fi 시뮬레이터용 `TcpBleunoClient.kt` 추가)를 유지하고, 별도 `BleunoTest` 점검 앱 및 `bleuno/hardware/type_m/v1/` 마더보드 자료와 연결한다.
- 오픈소스 AI 응용 15주 초판(2026-09-02~03 작성, 문서·링크·코드 자동 검증 통과)을 기준 PC(RTX 4070)에서 재현 검증해 개강 최소 2주 전 배포 가능 상태로 만든다.

## Near-term work

### 웹프로그래밍 후속 작업

1. 공용 Supabase에서 연습 글을 대상으로 올바른 편집 키·다른 키·키 없음의 PATCH·DELETE를 비교하고 같은 ID의 GET으로 실제 변경을 판정한다. id·book_id·created_at 보호 열 거부도 확인한다.
2. 독립 폴더 하나, 우선 07 완성 방명록을 Pages에 게시하고 HTTPS 화면에서 API 요청·CORS·다른 기기 공유를 확인한다. 교재 슬라이드 사이트 배포를 예제 앱 배포로 간주하지 않는다.
3. 수업 인원에 맞게 추가 방명록 태그 등록·키 배부를 준비한다. 공용 확인 태그는 student01·student02이며 로컬 student01~30을 그대로 공용 등록 완료로 표시하지 않는다. 기존 편집 키를 덮어쓰지 않는 절차를 정한다.
4. 비공개 12~15주 대본·해답·평가 자료를 공개 REST 범위와 맞춘다. 기존 개편 안내와 과거 자료는 보존하고 새로운 실측·채점 기준을 작성한다. 레포트 일정·배점은 학교별 별도 공지로 관리한다.
5. 정규 2회×90분 수업을 리허설하고 연구 특강은 학생의 단계별 진행으로 조정한다. IoT의 모의 온도·메모리 상태·통신 실패 실험 범위를 실제 장치 성능 평가와 구분한다.

### 기존 과목의 대기 작업

아래 목록과 번호는 이전 작업의 대기 사항을 보존한 것이다. 해당 작업을 다시 시작할 때 현재 저장소·비공개 자료와 대조한다.

1. 실습실 PC에 설치할 프로그램 버전(Python·uv·Ollama·PyTorch)과 수업에 쓸 모델 이름을 `environment_baseline_template.md`의 TBD 칸에 적는다. 교재는 `qwen3:8b` 등 기본값으로 이미 동작하므로, 바꿀 이유가 없으면 기본값을 그대로 적으면 된다.
2. RTX 4070이 있는 PC에서 각 주차 `examples/`를 한 번씩 실행한다. 그러면 `uv.lock`이 생기고(커밋한다), 학습 시간·VRAM·토큰 속도처럼 교재가 빈칸으로 둔 숫자를 채울 수 있다. Ollama가 없는 PC에서는 순수 Python 예제만 실행해 확인했다.
3. 8주차 실기평가 패킷(문항·fixture·정답·감독 체크), 15주차 기말·발표 패킷, 챕터 퀴즈 은행은 `teaching_materials_private/open_source_ai/`에 있다. 시행 전에 강의자가 한 번 읽고 값을 바꿀지 정한다.
4. 강의 대본 15개를 낭독 리허설해 20분 분량을 조정한다(구간을 바꾸면 `slides.md`도 같이).
5. `npm run build && npm test`가 통과한 상태로 main에 반영해 GitHub Pages에서 오픈소스 AI 덱 15개가 열리는지 확인한다.
6. `_shared/` 승격 후보 검토: Git 세 영역·PR 흐름(웹 1·2주차 ↔ 오픈소스 AI 2주차), 공개 키·비밀정보 구분과 입력 검증(웹 REST 실습 ↔ 오픈소스 AI 배포 실습). 웹 13주차를 이전 릴리스·보안 독립 주제로 되돌리지 않는다.
7. 학교 폴더 `univ_scoring_works/wku/subjects/opensw/materials.md`에 주차↔공용 모듈 매핑과 실제 배점·마감을 연결한다.
8. Android BLE: type_m v1 원본의 SEN1·VIN 미연결과 모듈 핀 표기를 검토하고, 모터·서보용 설정·정지 동작을 확정한 뒤 확장 실습을 만든다. 기존 LED·DHT11 수업은 기존 보드 또는 Fake로 유지한다. `RealBleunoClient`의 CCCD 실패 시 READY 처리와 MTU 요청 실패 fallback을 보완할 때 공통 코드 복사본 7곳과 12~15주차 walkthrough 부록도 동기화한 뒤 실기 연결·명령·재연결을 검증한다.
9. Android Wi-Fi 시뮬레이터에서 아직 확인하지 않은 것이 있다. 지금까지는 에뮬레이터와 펌웨어 소스로만 확인했다.
   - 실기기(PC와 같은 Wi-Fi)와 학교 Wi-Fi(같은 Wi-Fi 기기끼리 통신을 막는 설정)에서 검색·연결
   - 실제 보드에서 연결·해제 때 외부 LED가 꺼지는지
   - 실제 보드에서 앱이 연결된 동안 `blink`를 보내면 내장 LED가 깜빡이는지. 펌웨어 소스로는 연결 중에는 깜빡임 작업이 내장 LED를 끈 채로 두므로(`main.cpp`) 깜빡이지 않는다. TENSTAR 빌드는 연결 중 `blink`·`stopblk`를 받으면 파랑 고정 표시가 꺼진다. 세 곳(`bleuno/README.md` 1·2절, `iot_sim/README.md` 5절)에 '펌웨어 소스 기준'으로 적어 두었다. 실보드로 확인되면 표시를 떼고, 다르면 세 곳을 고친다.
   - 수업 기준 AVD(API 33 이상)에서 실습지의 Logcat 줄을 다시 잰다. 지금 실측은 API 31 에뮬레이터 한 대다.
   - 14주차 예제의 [재연결] 버튼(47번)이 검색 중에 `stopScan()`을 부르지 않는 것을 고칠지 정한다. 고치면 15주차 예제와 walkthrough 인용도 같이 고친다.
   - 제어 화면의 명령 로그(`logText`)는 스크롤 설정이 없다(높이 0dp·weight 1). 14주차 기반 앱으로 잰 에뮬레이터에서는 앞의 몇 줄만 보였다. 같은 레이아웃이 12주차 day1·day2, 13주차 day1·day2, 14주차 day1, 15주차 rehearsal_solution·rehearsal_starter에 있다. 고칠지 정한다(기존 예제 문제). 고치면 각 주차 walkthrough의 `activity_control.xml` 전문도 같이 고친다.
   - 공개 bleuno README에 펌웨어 `safebackdelay`(설정하면 LED를 저절로 끈다) 설명을 넣을지 정한다. 지금은 비공개 해답에만 있다.
   - 실기기로 한 학생의 오류 글자가 실습지와 다를 때의 제출 판정(비공개 해답의 제출 판정은 초안이다).
10. 10주차 권한 흐름 수정에서 정할 것이 남아 있다: 15주차 루브릭 P2 확인, 15주차 해답을 세 갈래로 할지, `verify_rubric15_perm.py` 갱신, starter TODO 문구, 로그·캡처 위치. 10주차 작업에서 보고만 한 두 문제(`ConnViewModel`의 `catch (e: Exception)`이 취소를 삼킴 — 7·9·10·11·12주차 예제 8곳, Switch 리스너가 회전 때 다시 불림)를 고칠지 정한다.
11. Android 작업 갈래 `dev/android/blueno`를 main에 합칠지, 언제 합칠지 정한다. 이 갈래는 2026-10-29(`c15a686`)에 main과 갈라져 main의 2026-11-02 재구성(9주차 day1·day2, 13주차는 `day1`만, 14주차는 `day1`·`day2`, 13·15주 과제 이동)이 없다. type_m v1 연계(`76808fd`), 10주차 권한 수정(`68b41a4`), Wi-Fi 시뮬레이터·`TcpBleunoClient.kt`(2026-11-12)는 이 갈래에만 있다. 두 쪽이 함께 바꾼 파일이 26개다(2026-11-12 기준, 대부분 12~15주차 문서·예제). 합친 뒤 할 일은 다음과 같다.
   - `iot_sim/lab.md`와 비공개 해답의 주차·일차 표기를 고친다(이 갈래의 13주차 `day2` = main의 14주차 `day1`, 이 갈래의 14주차 `day1` = main의 14주차 `day2`).
   - bleuno 9개를 main의 복사본 7곳(12주차 `day1`·`day2`, 13주차 `day1`, 14주차 `day1`·`day2`, 15주차 두 곳)에 맞춘다.
   - 10주차 수정 뒤 줄 번호를 다시 맞추고 `check_week.py`와 예제 빌드를 다시 돌린다. 비공개 문서에 '`dev/android/blueno` 기준'이라고 적은 문장도 정리한다.

## Structure decisions

- 웹 주차 폴더 이름은 기존 링크를 위해 유지한다. 12주 GET→13주 POST→14주 PATCH·DELETE→15주 복습·개인 실기로 이어지며 레포트는 별도다.
- Supabase 특강 예제는 README만 있는 루트와 독립 폴더 01~07을 쓴다. 각 폴더의 .http·.env.example과 브라우저용 config.example.js를 함께 유지한다. 06 요청 실험과 07 완성 UI를 합치지 않는다.
- 정규 학생은 강의자 API를 사용하고, 방학 연구 특강의 담당자는 새 프로젝트를 직접 구축한다. 계정 없는 참여자는 강의자 시연과 공용 API 실습을 사용한다.
- 오픈소스 AI 응용은 `materials/` 챕터 구조 대신 다른 과목과 같은 `weeks/weekNN_slug/` 구조를 쓴다.
- 수업 시간 구조는 60분 블록 × 3(설명 20 + 실습 30 + 휴식 10)이며 자료는 "교시" 단위로 쓴다. 분반별 요일 배치는 학교 문서가 정한다.
- 강의 대본·해답은 비공개 짝 저장소에 같은 주차 폴더 이름으로 둔다.
- 평가 문서 파일명: 종합과제 `assignment_brief.md`·`assignment_rubric.md`(4·8·12·15주차), 실기 `exam_structure.md`·`exam_rubric.md`(8주차), 제안 `proposal_template.md`·`proposal_rubric.md`(9주차), 기말·발표 `final_review_rubric.md`·`presentation_rubric.md`(15주차).
- 예제 코드의 모델·서버는 환경변수 + 기본값으로 읽는다. 기본값 표는 `open_source_ai/weeks/README.md`가 단일 기준이다.

## Risks

- 공용 방명록의 조회·추가는 공개 허용이다. book_id를 개인 접근 제한이나 학생 인증으로 해석하면 안 된다. 편집 키도 작성자 개인이 아닌 방명록 전체의 편집 권한이다.
- 공용 PATCH·DELETE와 Pages 실배포는 아직 검증하지 않았다. 로컬 자동 시험·REST Client 성공·localhost 브라우저 성공을 이 검증의 완료로 합치지 않는다.
- 실제 .env·localfiles·.local·편집 키가 소스·ZIP·Pages·요청 이력 캡처에 포함되지 않게 확인한다. 브라우저가 읽는 publishable key와 비밀 키를 구분한다.
- 로컬 정적 서버와 홈 IoT Node 서버는 현재 터미널의 프로세스다. 포트가 계속 열려 있거나 다음 세션에서도 살아 있다고 가정하지 않는다.
- 공개 REST 자료와 비공개 평가 자료의 개편 진행 상태가 다르다. 과거 실측 수치와 해답을 새 교재 결과로 표시하지 않는다.
- 모델 태그 변동: `qwen3:8b`, `bge-m3`, `Qwen/Qwen2.5-0.5B-Instruct` 등은 교재 작성 시점 기준이며 제공자가 같은 태그를 다른 빌드로 옮길 수 있다. 실제로 `qwen3:4b`가 생각 전용 빌드로 바뀌어 기본값을 `qwen3:8b`로 교체했다. 환경 기준표에서 확정하고 예제는 환경변수로만 바꾼다.
- `transformers`·`peft`·`trl` API 변동: 10주차 LoRA 학습 스크립트는 `Trainer` 기반으로 썼으나 메이저 버전 변화에 취약하다. lock 확정 후 재실행 검증이 필요하다.
- Ollama `think` 옵션은 특정 버전 이상에서만 동작한다. 기준표의 Ollama 버전으로 확인한다.
- RTX 4070 실측(10주차 학습 시간·VRAM, 7주차 임베딩 시간)이 아직 없다. 30분 실습 분량 판단이 실측 후 바뀔 수 있다.
- 사이트 검증 스크립트의 슬라이드 수 고정 검사는 원고 수정마다 상수 갱신을 요구한다.
- Wi-Fi 시뮬레이터는 펌웨어 `gbox3d/bleuno` main(1.0.5_dev)의 `ble.cpp`·`parseCmd.cpp`와 `main.cpp`(`ledOff`·`clearAllControl`)에 맞췄다. 펌웨어가 바뀌면 동작이 어긋날 수 있다.
