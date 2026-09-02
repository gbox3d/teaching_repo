# 13주차 — BLE 출력 제어와 명령 확인

## 이번 주 질문

사용자가 ON을 눌렀다는 사실, Android가 write를 요청했다는 사실, 보드 출력이 바뀌었다는 사실을 어떻게 구분하고 검증할까?

## 측정 가능한 학습 목표

- `UI event → ViewModel/use case → BLE abstraction → transport → ESP32-C3` 명령 경로를 추적한다.
- 연결 상태가 `Ready`일 때만 출력 명령을 허용하고 중복 탭·연결 끊김을 안전하게 처리한다.
- 제공 프로토콜 계약의 GPIO 식별자·level을 검증하되, 미확정 UUID·GPIO·encoding을 `TBD`로 보존한다.
- fake transport에서 성공·잘못된 채널·timeout·disconnect를 재현하고 UI 상태와 복구 행동을 구현한다.
- 사전 플래시 보드에서 출력 1개를 제어하고 “요청됨/확인됨/실패” 증거를 구분해 기록한다.

## 1일차 — fake 출력 명령과 상태

| 구간 | 내용 |
|---|---|
| 설명·라이브 시연 30분 | 출력 명령 계약, Ready gate, 요청과 확인의 차이, 중복·timeout 처리 |
| 직접 실습 60분 | fake transport로 출력 상태 reducer, 잘못된 채널·timeout·disconnect 검증 |

## 2일차 — 실제 출력 제어와 진단

| 구간 | 내용 |
|---|---|
| 설명·라이브 시연 30분 | 제공 write API, 프로토콜 검증, 보드 관찰과 로그 상관관계, 안전한 재시도 |
| 직접 실습 60분 | ESP32-C3 출력 제어, fake/real 비교, 실패 후 복구와 증거 패키지 작성 |

두 수업일 모두 정확히 `30분 설명·시연 + 60분 실습`이다.

## 선수 지식과 준비물

- 12주차 전체 연결 상태 기계와 `Ready` 도달 증거
- 강의자가 제공한 `BleGateway`/출력 제어 추상화와 fake transport
- 강의자가 펌웨어를 설치한 Tenstar ESP32-C3와 수업용 출력 회로
- 학생은 펌웨어 코딩·빌드·플래싱 또는 회로 변경을 하지 않는다.
- service/characteristic UUID, 허용 GPIO, 메시지 encoding·응답 의미는 instructor-pinned 프로토콜 전까지 `TBD`다.

## 자료

- [Marp 슬라이드](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [60분 실습지](lab.md)
- [출력 계약·의사코드](examples/README.md)

## 완료 증거

- 출력 명령의 5단계 호출 경로 그림
- fake 성공, 경계 입력, timeout/disconnect 실패의 예측·실행표
- real board의 `Ready → 요청 → 확인` 시간순 로그와 물리 출력 관찰
- 실패 중 제어 버튼이 비활성화되고 복구 뒤 다시 동작하는 화면
- 임의 UUID·핀 번호·payload를 만들지 않은 `TBD` 계약표

## 다음 주

[14주차 — BLE 입력 알림과 통합 프로젝트](../week14_ble_input_project/README.md)에서 입력 notification과 재연결을 결합한다.

## 공식 참고 자료

- [Transfer BLE data — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [Connect to a GATT server — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
- [Bluetooth Low Energy overview — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/ble-overview)
- [Lifecycle-aware coroutines for Views — Android Developers](https://developer.android.com/topic/libraries/architecture/views/coroutines-views)
