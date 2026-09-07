# 1주차 — Android 실행 구조와 Kotlin 진단

## 이번 주 질문

> Android 앱은 어떤 파일에서 시작해 화면을 만들며, 실행 결과를 코드와 Logcat 증거로 어떻게 설명할 수 있을까?

## 학습 목표

수업을 마치면 학생은 다음을 수행할 수 있다.

1. Android 프로젝트에서 `AndroidManifest.xml`, Kotlin 소스, `res/layout`, `res/values`의 역할을 각각 한 문장으로 설명한다.
2. 에뮬레이터 또는 실기기에서 앱을 실행하고 실행 대상·화면·Logcat 세 가지 증거를 남긴다.
3. `val`/`var`, 함수, 데이터 클래스, nullable type과 안전 호출을 사용한 Kotlin 코드를 작성한다.
4. 단말 정보를 문자열로 가공해 XML View에 표시하고 비어 있거나 알 수 없는 값을 `알 수 없음`으로 처리한다.
5. 오류 메시지의 첫 원인 줄을 근거로 실행 실패와 코드 실패를 구분한다.

## 누적 결과물

이번 주에는 `Smart I/O Controller`의 출발점인 `Device Info` 화면을 만든다. 아직 BLE나 ESP32-C3를 연결하지 않는다. 학생은 Android 앱만 다루며, 이후 주차에 이 화면을 장치 제어 대시보드로 확장한다.

## 2일 수업 흐름

| 일차 | 설명·시연 30분 | 직접 해결 실습 60분 | 산출물 |
|---|---|---|---|
| 1일차 | Android 앱 실행 구조, 프로젝트 탐색, 에뮬레이터/실기기, Logcat | 기준 프로젝트 실행, 파일 역할 지도, 의도적 오류 진단 | 실행 증거와 진단 기록 |
| 2일차 | Kotlin 핵심 문법, null 안정성, View 갱신 | `Device Info` 화면과 입력 경계 처리 | 화면 캡처, 핵심 코드, 관찰표 |

두 날 모두 정확히 `설명·시연 30분 + 직접 해결 실습 60분`으로 운영한다.

## 선수 지식과 준비

- 프로그래밍 언어의 변수, 조건문, 함수 개념
- 강의자가 개강 전에 검증한 Android Studio와 SDK 환경
- 에뮬레이터 1대 또는 개발자 옵션이 허용된 Android 실기기 1대
- 수업용 Kotlin + XML Views 기준 프로젝트
- 개인 계정 비밀번호, API 키, 단말 고유 식별자는 제출물에 포함하지 않는다.

도구·SDK의 정확한 버전은 개강 전 검증본을 사용하며 장기 교안에는 임의의 번호를 고정하지 않는다.

## 수업 자료

- [슬라이드](slides.md) · [English slides](slides_en.md)
- 강의 스크립트: 강의자 별도 관리(비공개)
- [따라하기 절차](walkthrough.md)
- [실습지](lab.md)
- [예제 스니펫 안내](examples/README.md)

## 완료 증거

- [ ] 앱이 실행된 대상 이름과 화면 캡처 1장
- [ ] Logcat에서 자신의 태그로 남긴 시작 로그 1줄
- [ ] 프로젝트 핵심 경로 4개의 역할표
- [ ] Kotlin 진단표와 nullable 값 처리 코드
- [ ] 정상 값, 빈 값, `null`을 확인한 `Device Info` 관찰표
- [ ] 실패 하나를 재현하고 첫 원인 줄·수정·재검증을 적은 3문장 기록

## 다음 주 연결

이번 주에는 하나의 `TextView`에 정보를 표시했다. 2주차에는 같은 데이터를 여러 View와 리소스로 나누고, 세로·가로 화면과 접근성까지 고려한 장치 제어판 XML layout으로 확장한다.

## 공식 참고 자료

- [Create a project — Android Developers](https://developer.android.com/studio/projects/create-project)
- [Projects overview — Android Developers](https://developer.android.com/studio/projects)
- [Build and run your app — Android Developers](https://developer.android.com/studio/run)
- [View logs with Logcat — Android Developers](https://developer.android.com/studio/debug/logcat)
- [Kotlin basic syntax — Kotlin Documentation](https://kotlinlang.org/docs/basic-syntax.html)
- [Kotlin null safety — Kotlin Documentation](https://kotlinlang.org/docs/null-safety.html)
