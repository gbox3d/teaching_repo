# 3주차 — Activity 생명주기와 상태 보존

## 이번 주 질문

> 화면 회전, 다른 화면 이동, Home 이동 뒤에도 사용자가 기대한 상태를 유지하려면 Activity callback과 상태 저장 책임을 어떻게 구분해야 할까?

## 학습 목표

수업을 마치면 학생은 다음을 수행할 수 있다.

1. `onCreate`, `onStart`, `onResume`, `onPause`, `onStop`, `onDestroy`의 여섯 핵심 callback을 로그 관찰 결과로 설명한다.
2. 최초 실행, 화면 회전, Home 이동·복귀, Back 종료에서 관찰된 callback 순서를 비교한다.
3. `onDestroy()`가 항상 호출된다고 가정하지 않고 정리·저장 전략의 한계를 설명한다.
4. 작은 일시적 UI 상태를 `onSaveInstanceState()`와 `savedInstanceState`로 저장·복원한다.
5. configuration change를 넘는 화면 상태에는 ViewModel이 적합하고, 영구 데이터에는 저장소가 필요함을 구분한다.
6. 명시적 Intent와 Activity Result API로 mock 장치 상세 화면을 열고 정상·취소·잘못된 입력을 처리한다.

## 누적 결과물

2주차 mock 제어판에 lifecycle 관찰 로그와 `DeviceDetailActivity`를 추가한다. 선택한 mock 장치명과 출력 탭 횟수를 회전 뒤 복원하고, 상세 화면에서 별칭을 편집해 결과를 돌려받는다. 실제 BLE나 ESP32-C3 펌웨어는 사용하지 않는다.

## 2일 수업 흐름

| 일차 | 설명·시연 30분 | 실습 60분 | 산출물 |
|---|---|---|---|
| 1일차 | Activity 상태와 여섯 callback, configuration change, saved state | 사용자 행동별 lifecycle 로그 수집, 상태 소실 재현·복원 | callback 관찰표와 복원 증거 |
| 2일차 | 명시적 Intent, extra 계약, Activity Result API, Back stack | 상세 화면 이동, 별칭 저장/취소/누락 처리 | 두 Activity 흐름과 결과 매트릭스 |

두 날 모두 `30분 설명·live demo + 60분 개인 실습`이다.

## 선수 지식과 준비

- 2주차 XML View, resource, click listener와 `render()`
- Logcat에서 앱 process와 tag 필터링
- nullable 값과 `?:` 대체값
- [2주차 자료](../week02_views_layout/README.md)

## 수업 자료

- [슬라이드](slides.md)
- 강의 스크립트: 강의자 별도 관리(비공개)
- [실습지](lab.md)
- [예제 스니펫 안내](examples/README.md)

## 완료 증거

- [ ] 네 사용자 시나리오의 실제 callback 관찰표
- [ ] `instanceId`를 포함한 로그로 이전 Activity와 새 Activity를 구분한 기록
- [ ] 회전 전후 탭 횟수 보존 화면과 저장·복원 코드
- [ ] saved state, ViewModel, 영구 저장소의 책임 비교 3문장
- [ ] 상세 화면의 정상 저장·빈 입력·취소·extra 누락 결과표
- [ ] deprecated `startActivityForResult()`를 쓰지 않은 Activity Result API 코드

## 다음 주 연결

Activity 하나에 장치 목록과 상세 UI를 모두 넣으면 책임과 상태가 커진다. 4주차에는 Fragment, Navigation, RecyclerView로 화면을 분리하고 Activity/Fragment View lifecycle 차이를 다룬다.

## 공식 참고 자료

- [The activity lifecycle — Android Developers](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [Save UI states — Android Developers](https://developer.android.com/topic/libraries/architecture/saving-states)
- [Intents and intent filters — Android Developers](https://developer.android.com/guide/components/intents-filters)
- [Get a result from an activity — Android Developers](https://developer.android.com/training/basics/intents/result)
- [Handle configuration changes — Android Developers](https://developer.android.com/guide/topics/resources/runtime-changes)
- [ViewModel overview — Android Developers](https://developer.android.com/topic/libraries/architecture/viewmodel)
