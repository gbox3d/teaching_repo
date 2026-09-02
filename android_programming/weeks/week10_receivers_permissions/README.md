# 10주차 — BroadcastReceiver와 런타임 권한

주간 질문: **시스템 event와 사용자 권한 결과를 앱 상태로 바꿀 때, 어디까지 신뢰하고 언제 등록·해제해야 하는가?**

context-registered/manifest-declared receiver의 수명과 노출 경계를 비교하고, 짧은 `onReceive()`에서 event를 ViewModel 상태로 전달한다. `Smart I/O Controller`의 BLE 기능을 실제로 구현하기 전, target SDK와 기기 OS에 따라 달라지는 scan/connect 권한을 대시보드 상태와 거절 UX로 모델링한다.

## 학습 목표

수강생은 실습 종료 시 다음을 수행할 수 있다.

1. context-registered와 manifest-declared receiver의 활성 범위·제약을 비교한다.
2. 등록/해제를 같은 lifecycle 경계에 배치하고 중복 등록·Context leak을 로그로 진단한다.
3. `RECEIVER_EXPORTED`/`RECEIVER_NOT_EXPORTED`를 event 출처별로 분리하고 action/extra를 불신 입력으로 검증한다.
4. Manifest 선언, runtime check, rationale, request, grant/deny, graceful degradation 흐름을 구현한다.
5. target Android 12(API 31)+의 `BLUETOOTH_SCAN`/`BLUETOOTH_CONNECT`와 legacy scan의 위치 권한 경로를 구분한다.

## 2일 × 90분 흐름

| 일차 | 30분 설명·live demo | 60분 직접 실습 |
|---|---|---|
| 1일차 | broadcast 모델, 등록 수명, exported 보안, 짧은 처리 | app-private/system event receiver와 상태 대시보드 |
| 2일차 | runtime permission workflow, BLE 버전 matrix, 거절 UX | target/device별 권한 계산과 grant/deny/rationale 복구 |

## 선수 지식·준비

- Activity/Fragment lifecycle, ViewModel/StateFlow와 `repeatOnLifecycle`
- Intent/action/extra와 AndroidManifest component 선언
- 강의 target SDK, min SDK, 기준 기기 OS: 학기 환경표 `TBD`
- 실제 BLE scan/connect는 12주차부터 진행하며 이번 주는 권한·event 상태만 다룬다.

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습](lab.md)
- [Receiver·권한 코드 조각](examples/README.md)

## 완료 증거

- START/STOP에 따른 receiver 등록·해제와 event 수신 횟수 Logcat
- app-private/system event filter·export 선택표와 spoof/잘못된 extra 방어 기록
- target SDK × device OS별 BLE 필요 권한 표
- granted·denied/rationale·기능 불가 상태 및 복구 UI 캡처
- 실제 권한 확인 직후에만 protected 작업을 호출하는 흐름도와 commit id

## 다음 주 연결

[11주차 ContentProvider와 데이터 공유](../week11_content_provider/README.md)에서 이벤트·권한 상태 대시보드에 센서 이력 조회의 URI/CRUD 경계를 추가한다.

## 공식 참고 자료

- [Android Developers — Broadcasts overview](https://developer.android.com/develop/background-work/background-tasks/broadcasts)
- [Android Developers — Insecure broadcast receivers](https://developer.android.com/privacy-and-security/risks/insecure-broadcast-receiver)
- [Android Developers — Request runtime permissions](https://developer.android.com/training/permissions/requesting)
- [Android Developers — Bluetooth permissions](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
