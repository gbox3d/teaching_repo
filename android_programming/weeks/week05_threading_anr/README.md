# 5주차 — 메인 스레드, ANR 위험, 경쟁 상태

## 이번 주 질문

> 오래 걸리는 장치 작업을 실행하면서 화면 응답성과 상태 일관성을 지키려면 어떤 코드는 메인 스레드 밖으로 보내고, 결과는 어떻게 안전하게 돌아와야 할까?

## 학습 목표

수업을 마치면 학생은 다음을 수행할 수 있다.

1. 메인 스레드의 UI event 처리와 rendering 책임을 queue 그림으로 설명한다.
2. 교육용 blocking mock으로 화면 멈춤을 재현하고 “멈춤”과 시스템의 ANR 판단을 구분한다.
3. 긴 mock 작업을 `ExecutorService`에서 실행하고 `Handler(Looper.getMainLooper())`로 UI 결과를 전달한다.
4. worker thread에서 View를 직접 변경하지 않아야 하는 이유를 설명한다.
5. Fragment View가 파괴될 때 `Future.cancel(true)`와 stale-result token으로 늦은 결과를 무시한다.
6. 공유 정수의 read–modify–write 경쟁을 반복 관찰하고 `AtomicInteger`로 기대값을 보장한다.

## 누적 결과물

4주차 `DeviceControlFragment`의 mock 펄스에 `Idle → Running → Success/Error` 상태를 추가한다. 실제 BLE/GPIO 작업 대신 지연 가능한 mock 작업을 사용한다. 학생은 ESP32-C3 펌웨어를 작성·빌드·플래싱하지 않는다.

## 2일 수업 흐름

| 일차 | 설명·시연 30분 | 직접 해결 실습 60분 | 산출물 |
|---|---|---|---|
| 1일차 | 메인 Looper, blocking, ANR 위험, worker와 UI thread 경계 | 멈추는 mock 재현 후 Executor 기반 응답형 UI로 개선 | 전후 응답성 관찰표와 thread 로그 |
| 2일차 | Executor/Future 수명, 취소, 경쟁 상태, 원자적 갱신 | 회전/Back 취소와 unsafe/atomic counter 비교 | 취소 증거와 race 반복 결과표 |

두 날 모두 `설명·시연 30분 + 직접 해결 실습 60분`이다.

## 선수 지식과 준비

- Fragment와 Fragment View lifecycle
- RecyclerView item 선택과 navigation argument
- 정상·경계·실패 입력 검증
- Logcat의 timestamp, thread 이름, tag 필터
- [4주차 자료](../week04_fragments_navigation/README.md)

## 수업 자료

- [슬라이드](slides.md)
- 강의 스크립트: 강의자 별도 관리(비공개)
- [실습지](lab.md)
- [예제 스니펫 안내](examples/README.md)

## 완료 증거

- [ ] 메인 queue에 blocking 작업이 들어갔을 때의 흐름도
- [ ] blocking 버전의 입력 지연과 Executor 버전의 응답성 비교
- [ ] worker·main thread 이름이 구분된 Logcat 기록
- [ ] `Idle/Running/Success/Error` 상태별 버튼·문구 표
- [ ] Back 또는 회전 뒤 늦은 결과가 새 View를 덮지 않는 취소 기록
- [ ] worker 1개와 4개의 unsafe 결과 5회, atomic 결과 5회 표
- [ ] “한 번 기대값이 나옴”이 thread-safe 증거가 아닌 이유 2문장

## 다음 주 연결

Thread, Handler, Future를 직접 연결하면 수명·취소·오류 코드가 쉽게 흩어진다. 6주차에는 같은 mock 작업을 `suspend`, dispatcher, `lifecycleScope`, structured concurrency로 다시 표현한다.

## 공식 참고 자료

- [Processes and threads overview — Android Developers](https://developer.android.com/guide/components/processes-and-threads)
- [Threading on Android — Android Developers](https://developer.android.com/topic/performance/threads)
- [Keep your app responsive — Android Developers](https://developer.android.com/training/articles/perf-anr)
- [ANRs — Android Developers](https://developer.android.com/topic/performance/vitals/anr)
- [Handler reference — Android Developers](https://developer.android.com/reference/android/os/Handler)
- [Looper reference — Android Developers](https://developer.android.com/reference/android/os/Looper)
