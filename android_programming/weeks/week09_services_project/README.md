# 9주차 — Service와 1차 과제

주간 질문: **화면이 없어도 계속되어야 하는 작업과 단순히 main thread 밖에서 해야 하는 작업은 어떻게 다른가?**

Android의 started, bound, foreground service를 비교하고, **Service는 기본적으로 hosting process의 main thread에서 실행되며 worker thread를 만들지 않는다**는 사실을 로그로 검증한다. 누적 `Smart I/O Controller` 중간 앱은 fake transport를 사용해 발표·레포트로 점검하며 ESP32-C3 펌웨어 작업은 포함하지 않는다.

## 학습 목표

수강생은 실습 종료 시 다음을 수행할 수 있다.

1. started·bound·foreground service의 시작 주체, 수명, 사용자 가시성을 비교한다.
2. Activity와 Service callback의 thread 이름을 기록해 Service가 별도 thread가 아님을 입증한다.
3. UI 수명 작업, 예약/지연 작업, 사용자가 인지하는 지속 작업에 맞는 API 후보를 선택한다.
4. Service 내부 blocking 작업을 명시적 coroutine scope/dispatcher로 분리하고 `onDestroy()`에서 정리한다.
5. 중간 앱의 UI→ViewModel→fake transport 상태 흐름과 normal·boundary·failure를 3분 이내에 시연한다.

## 2일 × 90분 흐름

| 일차 | 설명·시연 30분 | 직접 해결 실습 60분 |
|---|---|---|
| 1일차 | Service 유형·수명·main thread, 대안 선택 | started/bound 관찰과 coroutine cleanup 실험 |
| 2일차 | foreground service의 사용자 가시성·제약, 과제 기준 | 중간 앱 발표 리허설·실패 재현·레포트 증거 정리 |

## 선수 지식·준비

- ViewModel, coroutine cancellation, StateFlow와 lifecycle-aware collect
- AndroidManifest component 선언과 explicit Intent 기초
- 강의자 기준 프로젝트의 target SDK/notification 정책: `TBD` 환경표에서 확정
- [1차 과제 명세](project_brief.md)와 [10점 rubric](rubric.md)

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습](lab.md)
- [Service 코드 조각](examples/README.md)
- [1차 과제 명세](project_brief.md)
- [1차 과제 rubric](rubric.md)

## 완료 증거

- Activity와 Service callback의 같은 main thread 로그
- worker coroutine 전환 및 Service 종료 뒤 child Job 취소 로그
- started/bound/foreground/ViewModel/WorkManager 선택표
- 중간 앱 normal·empty/연속 event·failure/retry 시연 영상 또는 캡처
- 발표 자료, 레포트, commit id와 개인 설명/기여 증거

## 운영 정책 경계

1차 과제의 개인/팀 운영 방식은 **과목 운영 정책 `TBD`**다. 팀으로 운영하더라도 개인별 코드 설명, 장애 대응, commit/작업 근거 등 개인 증거는 별도로 확인한다. 명시적인 팀원/제출 근거 없이 다른 학생에게 결과를 자동 적용하지 않는다.

## 다음 주 연결

[10주차 BroadcastReceiver와 권한](../week10_receivers_permissions/README.md)에서 일시적인 시스템 event 진입점과 런타임 권한 상태를 대시보드에 연결한다.

## 공식 참고 자료

- [Android Developers — Services overview](https://developer.android.com/develop/background-work/services)
- [Android Developers — Bound services overview](https://developer.android.com/develop/background-work/services/bound-services)
- [Android Developers — Foreground services overview](https://developer.android.com/develop/background-work/services/fgs)
- [Android Developers — Background work](https://developer.android.com/develop/background-work/background-tasks)
