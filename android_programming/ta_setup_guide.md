# 모바일프로그래밍 실습조교용 설치 프로그램 목록

## 목차

- [필수 설치](#필수-설치)
- [필요할 때만 설치](#필요할-때만-설치)
- [별도 설치하지 않는 항목](#별도-설치하지-않는-항목)
- [설치 확인](#설치-확인)

## 필수 설치

| 프로그램·구성요소 | 공식 경로 | 비고 |
|---|---|---|
| [Git for Windows](https://git-scm.com/install/windows) | Git 공식 사이트 | 수업 프로젝트 받기 |
| [Android Studio](https://developer.android.com/studio/install) | Android 공식 사이트 | 내장 JBR/JDK 사용 |
| Android SDK Platform | Android Studio의 SDK Manager | 정확한 버전은 TBD |
| Android SDK Build Tools | Android Studio의 SDK Manager | 정확한 버전은 TBD |
| Android SDK Platform Tools | Android Studio의 SDK Manager | ADB 포함 |
| Android Emulator·AVD system image | Android Studio의 Device Manager | 승인된 기기 profile과 image 사용 |

## 필요할 때만 설치

| 프로그램 | 설치 조건 |
|---|---|
| Android 제조사 USB 드라이버 | 실기기가 인식되지 않고 제조사 드라이버가 필요한 경우 |
| Windows 가상화 구성요소 | AVD 실행에 필요하며 전산실이 승인한 경우 |

## 별도 설치하지 않는 항목

- 별도 JDK: Android Studio의 내장 JBR을 우선 사용한다.
- Arduino IDE·ESP-IDF: ESP32-C3는 사전 플래시 보드를 사용하므로 조교 설치 대상이 아니다.
- 임의 SDK·Gradle·Kotlin 버전: 학기별 기준값이 정해질 때까지 설치하지 않는다.

## 설치 확인

```powershell
git --version
adb --version
adb devices
```

Android Studio의 **Help > About**, **SDK Manager**, **Device Manager** 화면에서 실제 버전을 확인한다.
정확한 Android Studio·SDK·AVD·기기 OS 값은 [학기별 환경 기준표](../environment_baseline_template.md)에서 담당 교수가 확정한다.
