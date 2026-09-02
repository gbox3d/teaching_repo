# 12주차 — BLE GATT와 연결 상태

## 이번 주 질문

“연결됨” 한 단어로 뭉개지 않고, 권한 요청부터 GATT 준비 완료까지 사용자가 이해하고 복구할 수 있는 상태로 어떻게 표현할까?

## 측정 가능한 학습 목표

- central/peripheral과 GATT client/server라는 두 역할 축을 섞지 않고 설명한다.
- `Idle → Scanning → Connecting → Discovering → Ready → Disconnected/Error` 상태 전이를 정상·실패 사건에 매핑한다.
- 앱·기기 조건에 따라 필요한 권한을 제공 helper로 판정하고 거절·다시 묻지 않음 상태의 복구 UX를 만든다.
- 제공 BLE 추상화로 시간 제한 scan, 장치 선택, connect, service discovery를 fake와 real transport에서 각각 수행한다.
- 장치 미발견, 권한 거절, 연결 실패, service 불일치를 재현하고 상태·로그·사용자 행동을 함께 기록한다.

## 1일차 — BLE 모델과 fake 연결

| 구간 | 내용 |
|---|---|
| 설명·라이브 시연 30분 | BLE 역할 두 축, advertising과 GATT, 버전 인식 권한, 연결 상태 기계 |
| 직접 실습 60분 | fake transport로 scan/connect/discover 상태 UI와 권한·미발견 실패 구현 |

## 2일차 — 사전 플래시 보드 연결

| 구간 | 내용 |
|---|---|
| 설명·라이브 시연 30분 | 제한 시간 scan, 장치 식별, service/characteristic 발견, 로그 기반 진단 |
| 직접 실습 60분 | 제공 Tenstar ESP32-C3에 실제 연결, fake/real 결과 비교, 실패 복구 검증 |

두 수업일 모두 정확히 `30분 설명·시연 + 60분 실습`이다.

## 선수 지식과 준비물

- 7주차 `StateFlow`, 10주차 런타임 권한 UX, 11주차 접근 계약
- BLE 기능이 있는 Android 실기기와 데이터 케이블
- 강의자가 제공한 BLE 추상화, fake transport, 사전 플래시된 Tenstar ESP32-C3
- 보드 식별 라벨. 학생은 펌웨어 코딩·빌드·플래싱을 하지 않는다.
- `SERVICE_UUID`, characteristic UUID, GPIO, 메시지 형식은 강의자가 고정하기 전까지 모두 `TBD`다.

## 자료

- [Marp 슬라이드](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [60분 실습지](lab.md)
- [추상화 계약·의사코드](examples/README.md)

## 완료 증거

- 두 BLE 역할 축을 분리한 장치 관계도
- fake와 real 각각의 전체 상태 전이 로그
- 정상 `Ready`, 경계 `0 devices`, 실패 `permission denied` 또는 `service mismatch` 증거
- scan이 대상 발견 또는 제한 시간에 종료된 로그
- UUID/GPIO/메시지 값을 추정하지 않고 `TBD`로 남긴 계약표

## 다음 주

[13주차 — BLE 출력 제어](../week13_ble_output/README.md)에서 `Ready` 상태 뒤의 write 명령과 확인 흐름을 구현한다.

## 공식 참고 자료

- [Bluetooth Low Energy overview — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/ble-overview)
- [Find BLE devices — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/find-ble-devices)
- [Connect to a GATT server — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
- [Transfer BLE data — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [Bluetooth permissions — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
