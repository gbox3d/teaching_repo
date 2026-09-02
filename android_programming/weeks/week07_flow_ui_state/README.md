# 7주차 — Flow 기반 단방향 UI 상태

주간 질문: **연결 상태가 계속 바뀔 때 화면은 어떤 하나의 진실을 관찰해야 하는가?**

6주차의 일회성 coroutine 결과를 `StateFlow<ControllerUiState>`로 바꾼다. `Smart I/O Controller`의 fake device stream을 ViewModel이 상태로 만들고, Fragment의 XML View는 `STARTED` 이상일 때만 lifecycle-aware하게 수집한다.

## 학습 목표

수강생은 실습 종료 시 다음을 수행할 수 있다.

1. cold `Flow`와 hot `StateFlow`의 구독·현재값 차이를 실행 로그로 비교한다.
2. loading·ready·empty·error를 하나의 sealed UI 상태로 모델링한다.
3. 외부에는 읽기 전용 `StateFlow`를 공개하고 ViewModel만 상태를 변경하게 한다.
4. `viewLifecycleOwner.lifecycleScope`와 `repeatOnLifecycle(STARTED)`로 XML View를 안전하게 갱신한다.
5. timeout, 제한 재시도, 중복 수집을 normal·boundary·failure 시나리오로 검증한다.

## 2일 × 90분 흐름

| 일차 | 30분 설명·live demo | 60분 직접 실습 |
|---|---|---|
| 1일차 | Flow, StateFlow, producer/consumer, 단방향 상태 | fake 연결 상태 stream과 exhaustive render 구현 |
| 2일차 | lifecycle-aware collect, timeout/retry, 중복 수집 | 화면 이동·회전·실패 복구가 가능한 상태 대시보드 완성 |

## 선수 지식·준비

- `viewModelScope`, coroutine cancellation과 exception 처리
- Fragment view lifecycle과 XML View binding
- Kotlin sealed class/interface와 `when`
- 강의자 기준 프로젝트의 Lifecycle/coroutine 의존성. 버전은 `TBD` 기준표를 따른다.

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습](lab.md)
- [복사 가능한 코드 조각](examples/README.md)

## 완료 증거

- `Idle → Scanning → Connecting → Ready`와 실패 전이를 보여 주는 영상/Logcat
- 화면이 `STOPPED`인 동안 render 로그가 멈추고 복귀 시 최신 상태를 받는 증거
- 회전·뒤로 가기/복귀 뒤 collector와 producer 개수 기록
- normal·empty/경계·failure·retry 체크표와 1·2일차 commit id
- event → ViewModel → state → render 단방향 그림

## 다음 주 연결

[8주차 중간 실기](../week08_midterm/README.md)에서 UI, 생명주기, coroutine, Flow를 제한 시간 안에 개인 구현하고 설명한다.

## 공식 참고 자료

- [Android Developers — StateFlow and SharedFlow](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [Android Developers — lifecycle-aware coroutine and Flow](https://developer.android.com/topic/libraries/architecture/coroutines)
- [Android Developers — UI layer](https://developer.android.com/topic/architecture/ui-layer)
- [Kotlin — Flows](https://kotlinlang.org/docs/coroutines-flow.html)
