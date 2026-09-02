# 12주차 실습 — BLE 연결 상태 기계

## 공통 시나리오

Android 앱이 수업용 ESP32-C3를 찾고, 연결하고, 필수 GATT 계약을 확인해 `Ready`가 된다. 학생은 제공 `BleGateway`와 사전 플래시 보드를 사용한다. 펌웨어 코딩·빌드·플래싱은 실습 범위가 아니다.

## 실행 전 예측

| 사건 | 현재 상태 | 예상 다음 상태 | 허용할 UI 행동 |
|---|---|---|---|
| scan 시작 | Idle |  |  |
| 대상 발견 | Scanning |  |  |
| link 연결 | Connecting |  |  |
| 필수 계약 일치 | Discovering |  |  |
| 보드 전원 off | Ready |  |  |

## 1일차 60분 — fake scan/connect/discover

### 시간표 — 합계 60분

- 0~10분: 역할도·권한 조건·상태 예측표 작성
- 10~25분: 상태 reducer와 상태별 XML View 활성화 연결
- 25~40분: fake 성공 trace로 `Idle → Ready` 완주
- 40~55분: 권한 거절·0 devices·mismatch 주입 및 복구 UI
- 55~60분: 증거 저장, commit, 회고

### 필수 구현

1. UI가 `BleGateway`만 참조하도록 한다.
2. `Idle`, `Scanning`, `Connecting`, `Discovering`, `Ready`, `Disconnected`, `Error`를 구분한다.
3. scan은 대상 발견 또는 fake 제한 시간 사건에서 종료한다.
4. 권한 미승인에서는 scan을 호출하지 않는다.

### 검증 매트릭스

| 종류 | 주입 | 기대 상태·화면 | 복구 |
|---|---|---|---|
| 정상 | target → connected → discovered | Ready, 연결 대상 표시 | Disconnect |
| 경계 | timeout, devices=0 | Disconnected/빈 결과 안내 | 새 scan |
| 실패 | permission denied | Error/권한 이유 | 다시 요청 또는 설정 안내 |
| 실패 | required service missing | Error/장치 불일치 | 다른 장치 선택 |

<details>
<summary>힌트 1 — reducer 입력</summary>

상태를 callback에서 직접 여러 View에 쓰지 말고 `BleEvent` 하나로 변환해 reducer에 보낸다.

</details>

<details>
<summary>힌트 2 — 중복 동작 차단</summary>

Scanning일 때 scan 버튼, Connecting/Discovering일 때 connect 버튼을 비활성화하는 표부터 만든다.

</details>

<details>
<summary>힌트 3 — 상태 뼈대</summary>

```kotlin
sealed interface LinkState {
    data object Idle : LinkState
    data object Scanning : LinkState
    data class Connecting(val device: DeviceId) : LinkState
    data class Discovering(val device: DeviceId) : LinkState
    data class Ready(val device: DeviceId) : LinkState
    data class Disconnected(val reason: String) : LinkState
    data class Error(val recovery: Recovery) : LinkState
}
```

</details>

## 2일차 60분 — real transport와 ESP32-C3

### 시간표 — 합계 60분

- 0~10분: 장비 라벨·권한·Bluetooth 상태 점검, fake 회귀 테스트
- 10~25분: 제공 real transport 주입, 제한 시간 scan과 대상 선택
- 25~40분: connect/discover 후 `Ready` 로그 확보
- 40~55분: 보드 off 또는 권한 거절 실패 주입, 복구 검증
- 55~60분: fake/real 비교표, commit SHA, 제출

### 필수 구현

1. 제공 설정 지점에서 fake를 real로 교체한다.
2. 대상 발견 또는 제한 시간에 scan이 종료됨을 로그로 보인다.
3. 필수 GATT 계약이 확인되기 전에 제어 UI를 활성화하지 않는다.
4. 연결 중 보드 전원을 끈 뒤 `Disconnected/Error`와 재시도 행동을 보인다.

### 검증 매트릭스

| 종류 | 절차 | 기대 관찰 | 증거 |
|---|---|---|---|
| 정상 | 라벨 보드 scan/connect | 전체 상태 뒤 Ready | 시간순 event log |
| 경계 | 보드 off로 scan | 제한 시간 뒤 0 devices | ScanStopped(reason=timeout) |
| 실패 | connect 중 보드 off | Disconnected/Error | UI + 마지막 성공 사건 |
| 실패 | 권한 거절 | scan 미시작 | 권한 상태 + 복구 버튼 |

<details>
<summary>힌트 1 — real이 안 될 때</summary>

먼저 fake 전체 경로가 여전히 통과하는지 확인한다. 통과하면 권한 → adapter → scan 종료 이유 → 장치 식별 → connect → discovery 순으로 좁힌다.

</details>

<details>
<summary>힌트 2 — 장치 식별</summary>

장치 이름 하나만 믿지 말고 강의자가 제공한 라벨/advertising 식별 계약을 사용한다. 계약값이 없으면 `TBD`로 보고한다.

</details>

<details>
<summary>힌트 3 — service mismatch</summary>

link 성공 로그와 discovery 결과를 분리해 캡처한다. 필수 UUID를 임의 값으로 대체하지 않는다.

</details>

## 확장 문제

- 사용자가 취소한 scan과 timeout scan을 다른 복구 문구로 만든다.
- 상태 event trace를 JSON이 아닌 읽기 쉬운 표로 export하는 방식을 제안한다.
- 두 보드가 동시에 보일 때 선택 규칙과 오선택 방지 UX를 설계한다.

## 제출

- 역할 두 축 그림과 상태 예측표
- fake/real 정상 trace 각 1개
- 경계 1개, 실패 1개의 UI·로그·복구 증거
- scan 종료 조건 확인표
- `TBD`가 보존된 프로토콜 계약표
- 개인 commit SHA와 3문장 회고
