# 주차별 강의 자료

## 운영 기준

- 15주, 주 2회 × 90분
- 매 수업: 설명·시연 30분 + 직접 해결 실습 60분
- 주당 합계: 이론·시연 60분 + 실습 120분
- 8주 중간고사, 9주 1차 과제 발표, 14주 2차 과제 발표, 15주 기말고사는 고정이다.
- 1주차는 Kotlin Playground에서 출력·변수·`if`·`fun`을 연습한다. 2~3주차는 `StudentCard` 앱을 만들고, 4주차부터 15주차까지는 `SmartIO` 한 앱(앱 이름 "Smart I/O Controller")을 매주 키운다.
- 매주 시작점은 전주 `examples/day2` 완성본이다. 자기 코드로 이어 가도 되고, 막히면 전주 완성본을 받아 이어 간다.
- 기본 문제를 먼저 완성하고 남는 시간에 확장 문제를 수행한다.

시험과 발표 주차는 대학 일정과 분반 인원에 따라 실제 평가 시간이 달라질 수 있다. 공개 자료에는 평가 구조와 연습 절차만 두며, 학기별 실제 문항·정답·학생 정보는 별도 비공개 공간에서 관리한다.

## 주차 폴더 구성

각 폴더는 같은 기본 구조를 사용한다.

| 파일·폴더 | 역할 |
|---|---|
| `README.md` | 이번 주 질문, 학습 목표, 결과물(캡처 예), 2일 수업 흐름, 준비, 이번 주 범위, 수업 자료, 완료 기준, 다음 수업 연결 |
| `slides.md` | Marp 원고. `---`가 슬라이드 구분자. 일차마다 설명 30분을 `N일차 · A–B분 — 제목` 구간으로 나눈다 |
| `walkthrough.md` | 모든 주차. 처음부터 그대로 따라 하는 단계(할 일 → 예상 결과). 전체 코드 블록은 `examples/` 파일과 글자 단위로 같다 |
| `lab.md` | 일차별 60분 시간표, 단계별 문제와 힌트, 막혔을 때 표(실제 오류 메시지), 제출물, 먼저 끝났다면 |
| `examples/README.md` | 예제 파일 ↔ 프로젝트 위치 표, 개념별 최소 코드와 실행 결과 |
| `examples/dayN/` | 그날 수업이 끝났을 때의 **완성본 전체 파일**(2~7주·10~13주는 `day1`·`day2`, 14주는 `day1`). 1주차는 Playground용 `.kt` 파일, 8·15주는 `rehearsal_starter`·`rehearsal_solution`, 9주는 시연용 `service_demo`·`fragment_demo`·`fake_request`를 같은 규칙으로 둔다 |
| `exam_structure.md`·`project_brief.md`·`rubric.md` | 시험·과제 주차만. 8주 시험 구조·채점표, 9·14주 과제 안내·채점표, 15주 채점표 |

`examples/dayN/`의 파일은 Android Studio의 **Empty Views Activity** 템플릿 프로젝트에 다음 규칙으로 넣으면 그대로 빌드된다.

| 예제 파일 | 넣는 곳 |
|---|---|
| `*.kt` | `app/src/main/java/<package>/` (하위 폴더 `bleuno/`는 폴더째) |
| `activity_*.xml`·`fragment_*.xml` | `app/src/main/res/layout/` |
| `strings.xml`·`colors.xml` | `app/src/main/res/values/` |
| `res/…` | `app/src/main/res/…` 같은 경로 |
| `AndroidManifest.xml`·`build.gradle.kts` | 있으면 `app/src/main/AndroidManifest.xml`·`app/build.gradle.kts`를 교체 |

package는 2~3주 `com.example.studentcard`, 4~15주 `com.example.smartio`다(8주 리허설·9주 Fragment·요청 시연처럼 새 프로젝트로 만드는 예제는 그 폴더의 `examples/README.md`에 적었다).

12~15주는 제공 라이브러리 [`../bleuno/`](../bleuno/README.md)를 쓴다. `bleuno/src/`의 파일을 `app/src/main/java/com/example/smartio/bleuno/`로 복사하며(package `com.example.smartio.bleuno`), 12~15주 `examples/`의 `bleuno/` 폴더에 같은 파일이 들어 있다. 보드 명령·응답 규약과 라이브러리 사용법은 [bleuno README](../bleuno/README.md)에 있다.

PT 원고는 Markdown으로 관리한다. 필요할 때 Marp CLI 또는 VS Code Marp 확장으로 HTML, PDF, PPTX로 내보낼 수 있다.

## 주차 목록

| 주차 | 주제 | 누적 산출물 | 폴더 |
|---:|---|---|---|
| 1 | Kotlin 첫걸음: 학번과 이름 출력하기 | Playground에서 학번·이름·합격 여부 출력(`StudentCard.kt`) | [`week01_android_kotlin`](week01_android_kotlin/) |
| 2 | 첫 Android 앱: 내 정보 화면과 카운터 | `StudentCard`: 내 정보 화면과 [-1]·[초기화]·[+1] 카운터 | [`week02_views_layout`](week02_views_layout/) |
| 3 | Activity 생명주기와 상태 보존 | 회전해도 숫자 3이 남는 화면, 생명주기 콜백 순서 Logcat | [`week03_activity_lifecycle`](week03_activity_lifecycle/) |
| 4 | SmartIO 시작: ViewBinding·입력 위젯·두 번째 화면 | `SmartIO`: 장치 이름 입력 → 제어 화면에 이름과 `on 3`·`off 3` 명령 로그 | [`week04_fragments_navigation`](week04_fragments_navigation/) |
| 5 | 메인 스레드와 백그라운드: Thread·Handler | [검색] 5초 동안 버튼 비활성·ProgressBar, [중지] | [`week05_threading_anr`](week05_threading_anr/) |
| 6 | 코루틴: delay·취소·오류 처리 | `검색 중… 3` 카운트다운과 [중지], 가짜 연결 실패와 [다시 시도] | [`week06_coroutines`](week06_coroutines/) |
| 7 | ViewModel과 StateFlow: 회전해도 살아 있는 상태 | 회전해도 이어지는 `연결 중… 3`, 상태에 맞게 켜지는 버튼 | [`week07_flow_ui_state`](week07_flow_ui_state/) |
| 8 | 중간고사(개인 실기) | 리허설 앱 `Rehearsal`: [시작] 카운트다운·[취소]·회전 유지(범위 2~7주) | [`week08_midterm`](week08_midterm/) |
| 9 | 앱 컴포넌트 비교와 1차 과제 발표 | `LogService` 시연, 1차 과제 발표(SmartIO 시뮬레이터 또는 자유 앱) | [`week09_services_project`](week09_services_project/) |
| 10 | BroadcastReceiver와 런타임 권한 | 연결 화면 배터리 문구, [권한 확인] → 거절 AlertDialog → 설정 화면 | [`week10_receivers_permissions`](week10_receivers_permissions/) |
| 11 | 목록과 저장: ListView·SharedPreferences·ContentProvider 비교 + 실기기 준비 | 장치 이름 목록, 앱을 다시 켜도 남는 `마지막 장치: …`, 실기기 실행 | [`week11_content_provider`](week11_content_provider/) |
| 12 | BLE 기초: Bleuno 클라이언트로 검색·연결 | 보드 검색 목록, 목록 탭 → `준비됨`, 제어 화면 상태 표시 | [`week12_ble_gatt`](week12_ble_gatt/) |
| 13 | BLE 출력 제어: 문자열 명령과 응답 | LED on/off 명령과 JSON 응답 로그, 허용 번호 검사·오류 표시 | [`week13_ble_output`](week13_ble_output/) |
| 14 | 입력 수신·끊김·재연결과 2차 과제 발표 | 완성 Smart I/O Controller: 온습도 입력 이력·[재연결]·연결 시간 제한, 2차 과제 발표 | [`week14_ble_input_project`](week14_ble_input_project/) |
| 15 | 기말고사(개인 실기) | 리허설: 권한 확인·LED 명령과 응답·연결 시간 제한, 개인 시연·구술 | [`week15_final_exam`](week15_final_exam/) |

## 자료 작성 원칙

- **학생 기준선**: 프로그래밍 경험이 거의 없는 대학생이다. 1주차는 Kotlin Playground에서 `println`·`val`/`var`·문자열 템플릿·`if/else`·`fun`, 2주차는 Empty Views Activity·LinearLayout·TextView·`findViewById`·`setOnClickListener`·`var` 카운터까지 배웠다. 그 밖의 것은 모른다고 전제한다.
- **기준 자료 우선순위**: (1) 강의자 작년 슬라이드(1강~7장, 특강 1 BLE) → (2) 구글 "Android Kotlin Fundamentals"(View 기반) → (3) 국내 입문 교재 관례. 순서·용어·API는 이 셋과 같게 쓴다.
- **한 주 새 개념은 3~5개**다. 앞 주에서 배운 것만 전제하고, 난이도가 한 주에 두 단계 뛰지 않는다.
- **매주 캡처로 보여 줄 앱·화면 하나로 끝난다.** 산출물이 보고서·로그 문장·회고여서는 안 된다.
- **표준 API만 쓴다.** 클릭 리스너 안에서 View를 직접 바꾸고, 7주부터는 ViewModel + StateFlow `collect` 안에서 바꾼다. BLE는 콜백 기반 `BluetoothGatt` 흐름을 감싼 제공 라이브러리 `bleuno`를 호출한다.
- 표준 입문 교재에 없는 설계 틀과 용어를 들여오지 않는다. 금지 목록은 강의자 설계 문서가 관리하며, 주차 검사 스크립트가 공개·비공개 문서를 모두 검사한다.
- **Kotlin 문법은 한 주에 몰아넣지 않고 쓰는 주에 5분**으로 도입한다.

| 문법 | 처음 쓰는 주 | 형태 |
|---|---|---|
| `if/else`, `fun` 정의·호출 | 1주 2일차 | Playground 두 장 |
| null 안전성 `?`, `?.`, `?:` (`!!` 금지 한 줄) | 3주 2일차 | 정식 항목, 8주 채점 범위 |
| 문자열 붙이기 `"on $pin"`, `.toInt()`, `isEmpty()` | 4주 1일차 | 오늘 문법 5분 |
| `getStringExtra(...) ?: ""` | 4주 2일차 | 오늘 문법 5분 |
| 람다 `{ }` 안에서 바깥 변수 쓰기 | 5주 1일차 | 오늘 문법 5분 |
| `for (i in 5 downTo 1)` | 6주 1일차 | 오늘 문법 5분 |
| `try/catch`, `throw Exception("...")` | 6주 2일차 | 오늘 문법 5분 |
| `class` 정의·프로퍼티 | 7주 1일차 | 작년 2강 클래스 장 |
| `object` 상수 묶음, `when (state)` | 7주 2일차 | 작년 2강 when 장 |
| 익명 객체 `object : BroadcastReceiver() { override fun onReceive }` | 10주 1일차 | 복붙 틀 |
| `mutableListOf`, `add`, `size` | 11주 1일차 | 작년 2강 리스트 장 |
| `listOf(...).contains(x)` | 13주 1일차 | 오늘 문법 5분 |
| `split(" ")`, `[0]`, `[1]`, JSON 문자열에서 값 꺼내기(제공 helper) | 14주 1일차 | 오늘 문법 5분 |

`when`·`while`·상속·제네릭·확장 함수·`lateinit`은 필요할 때 한 줄로만 설명하고 채점하지 않는다. `lateinit var binding`은 4주 ViewBinding 틀에 나오므로 "이 줄은 틀이다"로 처리한다.

## 공식 기준 자료

- [Android 앱 기본 구조](https://developer.android.com/guide/components/fundamentals)
- [Activity lifecycle](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [Lifecycle-aware coroutine](https://developer.android.com/topic/libraries/architecture/coroutines)
- [StateFlow와 SharedFlow](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [Services overview](https://developer.android.com/develop/background-work/services)
- [Bluetooth permissions](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
- [Bluetooth Low Energy overview](https://developer.android.com/develop/connectivity/bluetooth/ble/ble-overview)
