# 주차별 강의 자료

## 운영 기준

- 15주, 주 2회 × 90분
- 매 수업: 설명·시연 30분 + 직접 해결 실습 60분
- 주당 합계: 이론·시연 60분 + 실습 120분
- 실습 순환: 문제 읽기 → 예상 → 구현 → 관찰 → 오류 설명 → 변형·확장
- 앞 주차 결과를 버리지 않고 `Smart I/O Controller`의 UI·상태·통신 구조로 누적한다.
- 기본 문제를 먼저 완성하고 남는 시간에 확장 문제를 수행한다.

시험과 발표 주차는 대학 일정과 분반 인원에 따라 실제 평가 시간이 달라질 수 있다. 공개 자료에는 평가 구조와 연습 절차만 두며, 학기별 실제 문항·정답·학생 정보는 별도 비공개 공간에서 관리한다.

## 주차 폴더 구성

각 폴더는 같은 기본 구조를 사용한다.

| 파일·폴더 | 역할 |
|---|---|
| `README.md` | 학습 질문, 목표, 1·2일차 흐름, 완료 기준과 제출 증거 |
| `slides.md` | Marp 호환 PT 원고. `---`가 슬라이드 구분자 |
| `lab.md` | 60분 직접 해결 실습, 단계별 힌트, 검증과 확장 |
| `examples/README.md` | Kotlin·XML 예제 조각, 적용 위치와 예상 관찰 결과 |

PT 원고는 Markdown으로 관리한다. 필요할 때 Marp CLI 또는 VS Code Marp 확장으로 HTML, PDF, PPTX로 내보낼 수 있다.

현재 `examples/`는 개념별 최소 코드와 관찰 절차를 문서로 제공한다. Android Studio·JDK·AGP·SDK 기준과 BLE 프로토콜을 개강 전에 고정한 뒤, 같은 폴더 구조에 검증된 starter와 reference solution을 별도 추가한다.

## 주차 목록

| 주차 | 주제 | 누적 산출물 | 폴더 |
|---:|---|---|---|
| 1 | Android 실행 구조와 Kotlin 진단 | Device Info 앱 골격 | [`week01_android_kotlin`](week01_android_kotlin/) |
| 2 | XML View와 반응형 layout | 정적 장치 제어판 | [`week02_views_layout`](week02_views_layout/) |
| 3 | Activity·Intent·생명주기 | 생명주기 추적 화면 | [`week03_activity_lifecycle`](week03_activity_lifecycle/) |
| 4 | Fragment·RecyclerView·Navigation | mock 장치 목록과 상세 화면 | [`week04_fragments_navigation`](week04_fragments_navigation/) |
| 5 | 메인 스레드·ANR·동시성 | 멈추는 앱 진단 결과 | [`week05_threading_anr`](week05_threading_anr/) |
| 6 | Coroutine과 구조화된 동시성 | 취소 가능한 비동기 작업 | [`week06_coroutines`](week06_coroutines/) |
| 7 | Flow와 생명주기 안전 UI 상태 | fake 연결 상태 시뮬레이터 | [`week07_flow_ui_state`](week07_flow_ui_state/) |
| 8 | 중간 개인 실기 | UI·생명주기·비동기 통합 | [`week08_midterm`](week08_midterm/) |
| 9 | Service와 1차 과제 | 앱 구조·중간 발표·보고서 | [`week09_services_project`](week09_services_project/) |
| 10 | BroadcastReceiver와 런타임 권한 | 권한·시스템 이벤트 대시보드 | [`week10_receivers_permissions`](week10_receivers_permissions/) |
| 11 | ContentProvider와 데이터 공유 | 센서 이력 조회 화면 | [`week11_content_provider`](week11_content_provider/) |
| 12 | BLE·GATT·연결 상태 | ESP32-C3 검색·연결 | [`week12_ble_gatt`](week12_ble_gatt/) |
| 13 | BLE read/write와 출력 제어 | LED·디지털 출력 제어 | [`week13_ble_output`](week13_ble_output/) |
| 14 | notification·재연결과 최종 발표 | Smart I/O Controller | [`week14_ble_input_project`](week14_ble_input_project/) |
| 15 | 기말 개인 실기·시연 | 구현 15점 + 시연 5점 | [`week15_final_exam`](week15_final_exam/) |

## 자료 작성 원칙

- `slides.md`에는 두 번의 30분 설명·시연에 필요한 핵심 개념만 두고 긴 발화는 대본으로 분리한다.
- 예제는 한 번에 한 개념만 보여 주며, 어느 파일·클래스·XML에 넣는지 함께 설명한다.
- `lab.md`에는 완성 정답 대신 완료 조건, 관찰 항목과 단계별 힌트를 둔다.
- 모든 실습은 정상 경로와 최소 한 개의 경계·실패 경로를 확인한다.
- UI는 Kotlin + XML View를 기본으로 하며 Jetpack Compose는 비교·확장 주제로만 다룬다.
- Flow는 화면 생명주기에 맞춰 수집하고, Service를 별도 스레드로 설명하지 않는다.
- BLE 실습은 scan 시간 제한, 권한 거절, 장치 미발견, 연결 해제와 재시도를 포함한다.
- `TBD`인 SDK 버전, UUID, GPIO 허용 목록과 메시지 규약은 임의 값으로 확정하지 않는다.
- 학생은 Android 앱과 BLE 상태·오류 처리를 구현하며 ESP32-C3 펌웨어의 코딩·빌드·플래싱은 수행하지 않는다.
- 학생용 starter, 강의자용 reference solution과 실제 시험 자료는 서로 분리한다.

## 공식 기준 자료

- [Android 앱 기본 구조](https://developer.android.com/guide/components/fundamentals)
- [Activity lifecycle](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [Lifecycle-aware coroutine](https://developer.android.com/topic/libraries/architecture/coroutines)
- [StateFlow와 SharedFlow](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [Services overview](https://developer.android.com/develop/background-work/services)
- [Bluetooth permissions](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
- [Bluetooth Low Energy overview](https://developer.android.com/develop/connectivity/bluetooth/ble/ble-overview)
