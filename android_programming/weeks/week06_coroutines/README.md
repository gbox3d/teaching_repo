# 6주차 — Kotlin Coroutine과 취소 가능한 작업

주간 질문: **화면을 떠난 뒤에도 비동기 작업이 계속된다면, 누가 언제 취소해야 하는가?**

5주차의 메인 스레드·ANR 관찰을 `suspend`, scope, dispatcher, structured concurrency로 확장한다. `Smart I/O Controller`의 실제 BLE 대신 지연 가능한 fake 연결 작업을 사용하여 UI 응답성, 취소, 오류 복구를 먼저 검증한다.

## 학습 목표

수강생은 실습 종료 시 다음을 수행할 수 있다.

1. coroutine과 thread의 차이를 실행 로그와 함께 설명한다.
2. `suspend` 함수가 호출 스레드를 막는 함수와 같지 않음을 예측 결과로 입증한다.
3. `viewModelScope`와 `lifecycleScope` 중 작업 소유자에 맞는 scope를 선택한다.
4. CPU·blocking I/O 작업을 적절한 dispatcher로 옮기고 UI 변경은 main에서 수행한다.
5. 취소와 일반 실패를 구분하고, 중복 요청·화면 종료·timeout을 재현한다.

## 2일 × 90분 흐름

| 일차 | 30분 설명·live demo | 60분 직접 실습 |
|---|---|---|
| 1일차 | suspend, scope, dispatcher, structured concurrency | fake 연결 작업을 UI를 멈추지 않게 실행하고 소유자에 따라 취소 |
| 2일차 | cancellation, timeout, exception propagation, cleanup | 최신 요청만 유지하고 정상·경계·실패 상태 및 재시도 구현 |

## 선수 지식·준비

- 메인 스레드와 ANR, callback의 역할
- Activity/Fragment 생명주기와 ViewModel의 소유 범위
- Kotlin lambda, sealed class, `try/catch/finally`
- 강의자가 제공한 Kotlin/XML Views 기준 프로젝트. 의존성 버전은 학기 기준표의 `TBD`를 따른다.

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습](lab.md)
- [복사 가능한 코드 조각](examples/README.md)

## 완료 증거

- 버튼을 누르는 동안 화면이 응답하는 영상 또는 연속 클릭 로그
- `START → CANCELLED`와 `START → SUCCESS`가 각각 보이는 Logcat
- 화면 회전 전후 작업 소유권을 설명한 상태 전이 그림
- normal·boundary·failure 체크표와 1·2일차 commit id
- “`Service`를 쓰지 않아도 백그라운드 dispatcher에서 실행할 수 있는 이유” 한 문장

## 다음 주 연결

[7주차 Flow 기반 UI 상태](../week07_flow_ui_state/README.md)에서 단일 작업 결과를 지속적인 상태 stream으로 바꾸고, XML View가 보일 때만 안전하게 수집한다.

## 공식 참고 자료

- [Android Developers — lifecycle-aware coroutine](https://developer.android.com/topic/libraries/architecture/coroutines)
- [Android Developers — Kotlin coroutines best practices](https://developer.android.com/kotlin/coroutines/coroutines-best-practices)
- [Kotlin — Cancellation and timeouts](https://kotlinlang.org/docs/coroutines-cancellation.html)
- [Kotlin — Coroutine context and dispatchers](https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html)
