# Plan

## 목차

- [Current goal](#current-goal)
- [Near-term work](#near-term-work)
- [Structure decisions](#structure-decisions)
- [Risks](#risks)

## Current goal

- Android BLE 연계: 수업 정본 SmartIO + 공통 클래스 9개(2026-11-12에 Wi-Fi 시뮬레이터용 `TcpBleunoClient.kt` 추가)를 유지하고, 별도 `BleunoTest` 점검 앱 및 `bleuno/hardware/type_m/v1/` 마더보드 자료와 연결한다.
- 오픈소스 AI 응용 15주 초판(2026-09-02~03 작성, 문서·링크·코드 자동 검증 통과)을 기준 PC(RTX 4070)에서 재현 검증해 개강 최소 2주 전 배포 가능 상태로 만든다.

## Near-term work

1. 실습실 PC에 설치할 프로그램 버전(Python·uv·Ollama·PyTorch)과 수업에 쓸 모델 이름을 `environment_baseline_template.md`의 TBD 칸에 적는다. 교재는 `qwen3:8b` 등 기본값으로 이미 동작하므로, 바꿀 이유가 없으면 기본값을 그대로 적으면 된다.
2. RTX 4070이 있는 PC에서 각 주차 `examples/`를 한 번씩 실행한다. 그러면 `uv.lock`이 생기고(커밋한다), 학습 시간·VRAM·토큰 속도처럼 교재가 빈칸으로 둔 숫자를 채울 수 있다. Ollama가 없는 PC에서는 순수 Python 예제만 실행해 확인했다.
3. 8주차 실기평가 패킷(문항·fixture·정답·감독 체크), 15주차 기말·발표 패킷, 챕터 퀴즈 은행은 `teaching_materials_private/open_source_ai/`에 있다. 시행 전에 강의자가 한 번 읽고 값을 바꿀지 정한다.
4. 강의 대본 15개를 낭독 리허설해 20분 분량을 조정한다(구간을 바꾸면 `slides.md`도 같이).
5. `npm run build && npm test`가 통과한 상태로 main에 반영해 GitHub Pages에서 오픈소스 AI 덱 15개가 열리는지 확인한다.
6. `_shared/` 승격 후보 검토: Git 세 영역·PR 흐름(웹 1·2주차 ↔ 오픈소스 AI 2주차), 비밀정보·릴리스 점검(웹 13주차 ↔ 오픈소스 AI 13·14주차).
7. 학교 폴더 `univ_scoring_works/wku/subjects/opensw/materials.md`에 주차↔공용 모듈 매핑과 실제 배점·마감을 연결한다.
8. Android BLE: type_m v1 원본의 SEN1·VIN 미연결과 모듈 핀 표기를 검토하고, 모터·서보용 설정·정지 동작을 확정한 뒤 확장 실습을 만든다. 기존 LED·DHT11 수업은 기존 보드 또는 Fake로 유지한다. `RealBleunoClient`의 CCCD 실패 시 READY 처리와 MTU 요청 실패 fallback을 보완할 때 공통 코드 복사본 7곳과 12~15주차 walkthrough 부록도 동기화한 뒤 실기 연결·명령·재연결을 검증한다.
9. Android Wi-Fi 시뮬레이터에서 아직 확인하지 않은 것이 있다. 지금까지는 에뮬레이터와 펌웨어 소스로만 확인했다.
   - 실기기(PC와 같은 Wi-Fi)와 학교 Wi-Fi(같은 Wi-Fi 기기끼리 통신을 막는 설정)에서 검색·연결
   - 실제 보드에서 연결·해제 때 외부 LED가 꺼지는지
   - 실제 보드에서 앱이 연결된 동안 `blink`를 보내면 내장 LED가 깜빡이는지. 펌웨어 소스로는 연결 중에는 깜빡임 작업이 내장 LED를 끈 채로 두므로(`main.cpp`) 깜빡이지 않을 것이다(예상). 확인되면 `bleuno/README.md` 2절과 `iot_sim/README.md` 5절의 내장 LED 설명을 고친다.
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

- 오픈소스 AI 응용은 `materials/` 챕터 구조 대신 다른 과목과 같은 `weeks/weekNN_slug/` 구조를 쓴다.
- 수업 시간 구조는 60분 블록 × 3(설명 20 + 실습 30 + 휴식 10)이며 자료는 "교시" 단위로 쓴다. 분반별 요일 배치는 학교 문서가 정한다.
- 강의 대본·해답은 비공개 짝 저장소에 같은 주차 폴더 이름으로 둔다.
- 평가 문서 파일명: 종합과제 `assignment_brief.md`·`assignment_rubric.md`(4·8·12·15주차), 실기 `exam_structure.md`·`exam_rubric.md`(8주차), 제안 `proposal_template.md`·`proposal_rubric.md`(9주차), 기말·발표 `final_review_rubric.md`·`presentation_rubric.md`(15주차).
- 예제 코드의 모델·서버는 환경변수 + 기본값으로 읽는다. 기본값 표는 `open_source_ai/weeks/README.md`가 단일 기준이다.

## Risks

- 모델 태그 변동: `qwen3:8b`, `bge-m3`, `Qwen/Qwen2.5-0.5B-Instruct` 등은 교재 작성 시점 기준이며 제공자가 같은 태그를 다른 빌드로 옮길 수 있다. 실제로 `qwen3:4b`가 생각 전용 빌드로 바뀌어 기본값을 `qwen3:8b`로 교체했다. 환경 기준표에서 확정하고 예제는 환경변수로만 바꾼다.
- `transformers`·`peft`·`trl` API 변동: 10주차 LoRA 학습 스크립트는 `Trainer` 기반으로 썼으나 메이저 버전 변화에 취약하다. lock 확정 후 재실행 검증이 필요하다.
- Ollama `think` 옵션은 특정 버전 이상에서만 동작한다. 기준표의 Ollama 버전으로 확인한다.
- RTX 4070 실측(10주차 학습 시간·VRAM, 7주차 임베딩 시간)이 아직 없다. 30분 실습 분량 판단이 실측 후 바뀔 수 있다.
- 사이트 검증 스크립트의 슬라이드 수 고정 검사는 원고 수정마다 상수 갱신을 요구한다.
- Wi-Fi 시뮬레이터는 펌웨어 `gbox3d/bleuno` main(1.0.5_dev)의 `ble.cpp`·`parseCmd.cpp`와 `main.cpp`(`ledOff`·`clearAllControl`)에 맞췄다. 펌웨어가 바뀌면 동작이 어긋날 수 있다.
