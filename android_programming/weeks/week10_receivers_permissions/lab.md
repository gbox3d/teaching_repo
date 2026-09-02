# 10주차 실습 — event·권한 상태 대시보드

## 시나리오

누적 `Smart I/O Controller`에 app-private 상태 event, 한 가지 system event, BLE capability/permission 상태를 표시한다. 실제 BLE scan/connect/GATT와 ESP32-C3 펌웨어는 구현하지 않는다. 외부 Intent는 불신 입력으로 다루고, 권한 거절 뒤에도 앱의 비-BLE 기능은 계속 사용할 수 있어야 한다.

## 공통 규칙

1. 강의 target/min SDK와 기준 device OS는 환경표의 `TBD`를 유지한다.
2. 등록 전 action source와 exported flag를 표로 승인받는다.
3. 권한 dialog는 사용자가 “장치 찾기” 기능을 선택한 문맥에서만 연다.
4. 코딩 전에 event/permission 상태 전이를 예측한다.

## 1일차 60분 — Receiver lifecycle과 입력 검증

### 먼저 예측

STARTED→event→STOPPED→event→STARTED→event 순서의 수신 횟수를 적는다. register를 두 번 하고 unregister를 한 번만 했을 때 예상 증상도 기록한다.

### 시간 상자

| 시간 | 활동 | 확인 증거 |
|---:|---|---|
| 0–8분 | source/export/lifecycle 예상표 | 설계 표 |
| 8–21분 | app-private receiver 등록/해제 | STARTED에서만 수신 |
| 21–33분 | action·extra allowlist | 잘못된 입력 무시 |
| 33–44분 | system event receiver 분리 | 출처별 filter/flag |
| 44–54분 | 중복 등록·복귀 검증 | event당 처리 1회 |
| 54–60분 | 상태 대시보드·commit | 로그/commit id |
| 합계 | **60분** | |

### 필수 구현

- app-private action은 package namespace를 쓰고 `setPackage`와 `RECEIVER_NOT_EXPORTED`를 적용한다.
- system/privileged source는 별도 receiver/filter로 분리하고 공식 문서에 맞는 flag를 선택한다.
- `onReceive()`는 action/extra를 검증하고 빠르게 ViewModel/repository에 전달한 뒤 반환한다.
- UI lifecycle 요구에 맞춰 register/unregister를 대칭 배치한다.
- external/system event를 최종 진실로 믿지 말고 필요하면 trusted API 상태를 재조회하는 메모를 남긴다.

### 검증

- [ ] 정상: STARTED에서 valid event가 대시보드에 한 번 표시된다.
- [ ] 경계: STOPPED event는 UI receiver가 처리하지 않고 복귀 뒤 중복이 없다.
- [ ] 실패: 잘못된 action, 누락/범위 밖 extra가 crash·상태 오염 없이 무시된다.
- [ ] `onReceive()`에 blocking I/O나 장기 loop가 없다.

<details>
<summary>힌트 1 — app-private broadcast</summary>

고유 package action, `intent.setPackage(context.packageName)`, `RECEIVER_NOT_EXPORTED`를 함께 사용한다.
</details>

<details>
<summary>힌트 2 — lifecycle 대칭</summary>

예를 들어 `onStart`에 등록했다면 `onStop`에서 해제한다. Boolean으로 등록 상태를 기록하면 진단이 쉽다.
</details>

<details>
<summary>힌트 3 — system source</summary>

공식 문서상 source가 system/privileged app이면 exported flag가 필요할 수 있다. app-private filter와 섞지 말고 payload를 불신한다.
</details>

## 2일차 60분 — BLE 권한 matrix와 거절 UX

### 먼저 예측

다음 조합의 필요 runtime 권한과 UI 상태를 적는다: target 31+/device 31+, target 31+/legacy device, BLE feature 없음, 사용자 deny, rationale 필요. 구체 course target 값은 `TBD`다.

### 시간 상자

| 시간 | 활동 | 확인 증거 |
|---:|---|---|
| 0–9분 | 공식표로 target/device matrix 작성 | 출처 링크/권한표 |
| 9–22분 | capability와 필요 권한 계산 | 기기/target 로그 |
| 22–35분 | Activity Result permission launcher | 문맥 있는 request |
| 35–46분 | denial/rationale/degrade UI | 앱 나머지 사용 가능 |
| 46–55분 | revoke/재진입·불가 상태 검증 | action 직전 check |
| 55–60분 | 증거·commit | matrix/commit id |
| 합계 | **60분** | |

### 필수 구현

- target SDK와 device API를 별도 값으로 관찰하고 권한 집합을 계산한다.
- target Android 12(API 31)+ 앱이 device 31+에서 scan/connect할 때 `BLUETOOTH_SCAN`과 `BLUETOOTH_CONNECT` runtime 상태를 확인한다.
- legacy scan 경로는 공식 Bluetooth permission 표에 따른 위치 runtime 권한을 사용하며 background scan은 이번 범위에서 제외한다.
- central 앱이 사용하지 않는 `BLUETOOTH_ADVERTISE`를 요청하지 않는다.
- grant 전, deny, rationale, BLE unavailable 상태를 서로 다른 UI로 표현한다.
- protected action 직전 grant를 재확인하고 없으면 실제 scan 대신 권한 흐름으로 돌아간다.

### 검증

- [ ] 정상: 필요한 권한이 granted이면 “scan 준비” 상태다. 실제 scan은 호출하지 않는다.
- [ ] 경계: BLE feature가 없으면 permission dialog 없이 unavailable이다.
- [ ] 실패: deny 뒤 앱이 종료되지 않고 기능 설명·취소/대체 경로가 있다.
- [ ] 재진입: 설정/revoke 또는 새 실행 뒤 현재 상태를 다시 계산한다.

<details>
<summary>힌트 1 — 두 축</summary>

`applicationInfo.targetSdkVersion`과 `Build.VERSION.SDK_INT`를 분리해 로그로 남긴다. 하나만 보고 matrix를 결정하지 않는다.
</details>

<details>
<summary>힌트 2 — 여러 권한 결과</summary>

`RequestMultiplePermissions` 결과 Map에서 필요한 항목이 모두 true인지 확인한다. permission group 이름에 의존하지 않는다.
</details>

<details>
<summary>힌트 3 — rationale/denial</summary>

`shouldShowRequestPermissionRationale`는 교육 UI 여부 판단에 사용한다. false 하나만으로 최초 요청과 재요청 불가를 단정하지 않는다.
</details>

## 확장

- exported receiver에 sender permission을 추가하는 보안 설계를 문서로 비교한다.
- `goAsync()`의 짧은 처리 계약과 WorkManager 위임 조건을 공식 문서에서 찾아 결정표에 추가한다.
- `neverForLocation`을 적용할 수 있는 제품 가정과 일부 beacon filtering tradeoff를 기록한다.

## 제출 증거

- receiver source/export/lifecycle 표와 valid/invalid event Logcat
- target/device BLE permission matrix와 공식 문서 링크
- granted·denied/rationale·unavailable UI 캡처
- normal·boundary·failure 체크표
- 1일차·2일차 commit id
