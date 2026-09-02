# 4주차 — Fragment, Navigation, RecyclerView

## 이번 주 질문

> 장치 목록과 제어 화면을 분리하면서도 Fragment의 View 수명, 선택한 장치, 잘못된 입력을 안전하게 관리하려면 어떤 경계를 세워야 할까?

## 학습 목표

수업을 마치면 학생은 다음을 수행할 수 있다.

1. Activity, Fragment, Fragment의 View lifecycle을 구분하고 `onDestroyView()` 뒤 View 참조 위험을 설명한다.
2. `NavHostFragment`와 navigation graph로 목록→제어→Back 흐름을 구성한다.
3. 화면 간에 전체 객체 대신 안정적인 mock device ID를 argument로 전달하고 누락값을 처리한다.
4. RecyclerView의 데이터–Adapter–ViewHolder–item View 관계를 그림과 코드로 설명한다.
5. `ListAdapter`와 `DiffUtil.ItemCallback`으로 mock 장치 목록을 표시하고 클릭 위치가 아닌 item 데이터를 전달한다.
6. 숫자 입력을 필수·형식·범위 순서로 검증하고 정상·경계·실패 결과를 UI에 표시한다.

## 누적 결과물

3주차 Activity 기반 제어판을 `DeviceListFragment`와 `DeviceControlFragment`로 나눈다. 고정 mock 장치 목록에서 항목을 선택하고 `100..5000ms` 범위의 mock 출력 펄스를 검증한다. 실제 BLE 송신과 ESP32-C3 펌웨어 작업은 하지 않는다.

## 2일 수업 흐름

| 일차 | 설명·시연 30분 | 실습 60분 | 산출물 |
|---|---|---|---|
| 1일차 | Fragment/View lifecycle, NavHost, graph, argument, Back stack | 목록·제어 Fragment 골격과 lifecycle 추적 | 화면 전환도와 로그 관찰표 |
| 2일차 | RecyclerView 파이프라인, ListAdapter, item click, 입력 검증 | mock 목록과 제어 입력 완성 | 장치 목록·제어 화면과 검증표 |

각 일차는 정확히 `30분 설명·live demo + 60분 개인 실습`이다.

## 선수 지식과 준비

- Activity lifecycle과 Logcat 추적
- saved instance state의 목적
- XML View, resource, `render()` 함수
- explicit Intent의 입력 계약 개념
- [3주차 자료](../week03_activity_lifecycle/README.md)

## 수업 자료

- [슬라이드](slides.md)
- 강의 스크립트: 강의자 별도 관리(비공개)
- [실습지](lab.md)
- [예제 스니펫 안내](examples/README.md)

## 완료 증거

- [ ] Activity–Fragment–Fragment View 수명 비교도
- [ ] 목록→제어→Back navigation graph와 실행 화면
- [ ] `onCreateView`/`onDestroyView`를 포함한 instance별 로그
- [ ] 0개·1개·여러 개 mock 목록 관찰 결과
- [ ] 정상 device ID와 argument 누락 결과
- [ ] 펄스 `100`, `5000`, `99`, `5001`, 빈 값, 문자 입력 검증표
- [ ] 실제 하드웨어 명령을 보내지 않는 mock 결과 문구

## 다음 주 연결

목록 구성과 입력 검증이 맞아도 긴 작업을 메인 스레드에서 실행하면 화면이 멈춘다. 5주차에는 의도적 blocking과 ANR 위험을 관찰하고 Thread/Executor로 작업과 UI 갱신을 분리한다.

## 공식 참고 자료

- [Fragments — Android Developers](https://developer.android.com/guide/fragments)
- [Fragment lifecycle — Android Developers](https://developer.android.com/guide/fragments/lifecycle)
- [Navigation — Android Developers](https://developer.android.com/guide/navigation)
- [Design your navigation graph — Android Developers](https://developer.android.com/guide/navigation/design)
- [Create dynamic lists with RecyclerView — Android Developers](https://developer.android.com/develop/ui/views/layout/recyclerview)
- [ListAdapter reference — Android Developers](https://developer.android.com/reference/androidx/recyclerview/widget/ListAdapter)
