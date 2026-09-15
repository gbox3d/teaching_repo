# 모바일프로그래밍 공용 교재

## 목차

- [범위](#범위)
- [진입점](#진입점)
- [학교 적용](#학교-적용)
- [미확정 기준](#미확정-기준)

## 범위

프로그래밍 경험이 거의 없는 학생을 기준으로, Kotlin 출력문에서 시작해 BLE 입출력 제어 앱까지 15주 동안 한 걸음씩 쌓는 공용 교재다.
1주차는 Kotlin Playground, 2~3주차는 첫 앱 `StudentCard`(화면·카운터·생명주기)를 만든다.
4주차부터는 `SmartIO`(Smart I/O Controller) 한 앱을 매주 키우며 ViewBinding·두 번째 화면(4주), Thread·Handler(5주),
코루틴(6주), ViewModel·StateFlow(7주), BroadcastReceiver·런타임 권한(10주), ListView·SharedPreferences(11주)를 배운다.
12~15주차에는 제공 라이브러리 `bleuno`로 사전 플래시된 ESP32-C3 보드를 검색·연결하고, LED 명령과 응답·온습도 입력·끊김과 재연결을 다룬다.
보드가 없어도 라이브러리의 가짜 클라이언트로 같은 흐름을 연습할 수 있다. 8주 중간고사, 9·14주 과제 발표, 15주 기말고사가 들어 있다.

## 진입점

- 주차별 색인: [`weeks/README.md`](weeks/README.md)
- 각 주차: `README.md`, `slides.md`, `walkthrough.md`, `lab.md`, `examples/` (강의 대본·실습 해답은 강의자 별도 관리)
- BLE 제공 라이브러리와 보드 명령 규약: [`bleuno/README.md`](bleuno/README.md)
- 과목별 설치 프로그램: [`ta_setup_guide.md`](ta_setup_guide.md)
- 공통 설치 프로그램: [`../ta_lab_setup_guide.md`](../ta_lab_setup_guide.md)
- 환경 기준표: [`../environment_baseline_template.md`](../environment_baseline_template.md)

1주차는 [Kotlin Playground](https://play.kotlinlang.org/)에서 학번·이름을 출력하며
출력문, 변수, 문자열·숫자, `if`와 `fun`을 연습한다. 실행할 수 있는 짧은 `.kt` 예제 세 개가 포함되어 있다.
2주차부터 `examples/dayN`은 그날 수업이 끝났을 때의 완성본 전체 파일이며 Empty Views Activity 템플릿 프로젝트에 넣으면 빌드된다.
파일을 넣는 위치 규칙은 [`weeks/README.md`](weeks/README.md#주차-폴더-구성)에 있다.

## 학교 적용

- 학교명·분반·실제 배점·시험·마감·LMS 정보는 학교 폴더에서 관리한다.
- 학교별 표지와 일정은 배포본에서 적용하고 공용 원고에 직접 넣지 않는다.

## 미확정 기준

Android Studio, 내장 JDK, Gradle/AGP/Kotlin, `compileSdk`·`targetSdk`·`minSdk`, 기준 기기 OS,
BLE UUID·GPIO·메시지 규약과 펌웨어 복구 이미지는 학기별 환경 기준표에서 교수 승인을 받아 확정한다.
값이 `TBD`이면 조교나 학생이 임의로 정하지 않는다.
