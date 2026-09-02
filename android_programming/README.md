# 모바일프로그래밍 공용 교재

## 목차

- [범위](#범위)
- [진입점](#진입점)
- [학교 적용](#학교-적용)
- [미확정 기준](#미확정-기준)

## 범위

Kotlin과 XML View로 Android 핵심 컴포넌트와 비동기 상태 관리를 학습하고,
제공된 BLE 추상화와 사전 플래시된 ESP32-C3를 이용해 입출력 제어 앱을 만드는 공용 교재다.

## 진입점

- 주차별 색인: [`weeks/README.md`](weeks/README.md)
- 각 주차: `README.md`, `slides.md`, `lab.md`, `examples/` (강의 대본은 강의자 별도 관리)
- 과목별 설치 프로그램: [`ta_setup_guide.md`](ta_setup_guide.md)
- 공통 설치 프로그램: [`../ta_lab_setup_guide.md`](../ta_lab_setup_guide.md)
- 환경 기준표: [`../environment_baseline_template.md`](../environment_baseline_template.md)

현재 예제는 주로 설명용 Kotlin/XML 조각이며, 전체가 독립적으로 빌드되는 Gradle 프로젝트는 아니다.

## 학교 적용

- 학교명·분반·실제 배점·시험·마감·LMS 정보는 학교 폴더에서 관리한다.
- 학교별 표지와 일정은 배포본에서 적용하고 공용 원고에 직접 넣지 않는다.

## 미확정 기준

Android Studio, 내장 JDK, Gradle/AGP/Kotlin, `compileSdk`·`targetSdk`·`minSdk`, 기준 기기 OS,
BLE UUID·GPIO·메시지 규약과 펌웨어 복구 이미지는 학기별 환경 기준표에서 교수 승인을 받아 확정한다.
값이 `TBD`이면 조교나 학생이 임의로 정하지 않는다.
