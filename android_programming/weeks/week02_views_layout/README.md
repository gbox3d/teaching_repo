# 2주차 — XML View와 적응형 장치 제어판

## 이번 주 질문

> 같은 장치 제어 화면이 글자 길이, 글꼴 크기, 화면 방향이 달라도 읽고 조작할 수 있으려면 View와 resource를 어떻게 나눠야 할까?

## 학습 목표

수업을 마치면 학생은 다음을 수행할 수 있다.

1. XML layout을 View tree로 그려 부모·자식의 크기 결정 관계를 설명한다.
2. `dp`, `sp`, `wrap_content`, `match_parent`, constraint의 용도를 구분해 화면을 구현한다.
3. 문자열·색상·간격을 resource로 분리하고 코드에서 resource를 참조한다.
4. 세로·가로, 긴 장치 이름, 큰 글꼴 조건에서 잘림이나 겹침을 재현하고 최소 수정한다.
5. label, content description, 상태 문구, 활성/비활성 표현을 사용해 기본 접근성을 점검한다.
6. mock 연결 상태를 하나의 `render()` 함수로 화면에 일관되게 반영한다.

## 누적 결과물

강의자가 제공한 Kotlin + XML Views 기준 프로젝트를 `Smart I/O Controller`의 장치 제어판으로 확장한다. 1주차 산출물은 Kotlin 출력 코드이므로 Android 앱이 이미 완성되어 있다고 가정하지 않는다. 실제 BLE 연결은 아직 사용하지 않으며 `Disconnected`/`Ready` 두 mock 상태만 버튼으로 바꾼다. ESP32-C3 펌웨어 작업은 학생 범위가 아니다.

## 2일 수업 흐름

| 일차 | 설명·시연 30분 | 직접 해결 실습 60분 | 산출물 |
|---|---|---|---|
| 1일차 | View tree, 크기·단위, constraint, resource, 이벤트 렌더링 | 세로 장치 제어판과 mock 상태 구현 | XML 구조도와 정상 화면 |
| 2일차 | resource qualifier, 회전·큰 글꼴, 접근성, 상태 표현 | 가로·긴 문구·큰 글꼴·사용 불가 상태 점검 | 조건별 관찰표와 개선 화면 |

두 날 모두 `설명·시연 30분 + 직접 해결 실습 60분`이다.

## 선수 지식과 준비

- 1주차의 `println`, `val`/`var`, 문자열 출력 연습
- 강의자가 실행을 확인한 Android Studio 환경과 Kotlin + XML Views 기준 프로젝트
- 수업 시작 시 강의자가 프로젝트 열기·실행과 `MainActivity.kt`, `activity_main.xml`, `strings.xml`의 위치를 함께 안내한다.
- 예제에 필요한 함수·이벤트 연결 등은 사용하는 부분에서 설명한다. Logcat과 nullable 값 처리를 1주차에 배운 선수 지식으로 요구하지 않는다.
- [1주차 자료](../week01_android_kotlin/README.md)

## 수업 자료

- [슬라이드](slides.md)
- 강의 스크립트: 강의자 별도 관리(비공개)
- [실습지](lab.md)
- [예제 스니펫 안내](examples/README.md)

## 완료 증거

- [ ] View tree와 각 View의 폭/높이 정책을 적은 구조도
- [ ] 문자열 리터럴을 resource로 분리한 XML
- [ ] mock 상태 두 가지를 같은 `render()`에서 표시한 Kotlin 코드
- [ ] 세로·가로, 기본·큰 글꼴, 짧은·긴 이름 관찰표
- [ ] 정상·경계·실패 조건 각각의 화면 또는 관찰 기록
- [ ] 접근성 점검 4항목과 수정 전후 설명

## 다음 주 연결

회전하면 Activity와 View tree가 다시 만들어지고 현재 mock 상태가 초기화될 수 있다. 3주차에는 lifecycle callback을 로그로 관찰하고 저장 가능한 UI 상태와 일회성 화면 이동을 분리한다.

## 공식 참고 자료

- [Layouts in views — Android Developers](https://developer.android.com/develop/ui/views/layout/declaring-layout)
- [Build a responsive UI with ConstraintLayout — Android Developers](https://developer.android.com/develop/ui/views/layout/constraint-layout)
- [App resources overview — Android Developers](https://developer.android.com/guide/topics/resources/providing-resources)
- [Support different screen sizes — Android Developers](https://developer.android.com/training/multiscreen/screensizes)
- [Make apps more accessible — Android Developers](https://developer.android.com/guide/topics/ui/accessibility/apps)
- [String resources — Android Developers](https://developer.android.com/guide/topics/resources/string-resource)
