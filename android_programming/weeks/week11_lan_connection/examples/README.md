# 11주차 예제: 내 방 제어

새 `RoomControl` 앱을 만든다. 1일차는 시뮬레이터와 연결하고, 2일차는 연결 후 열린 제어 화면에서 책상 조명을 켜고 끈다. [따라하기](../walkthrough.md) 순서로 실습한다.

## 새 프로젝트 준비

Android Studio의 Empty Views Activity로 `RoomControl`을 만든다. 패키지는 `com.example.roomcontrol`, 언어는 Kotlin이다. 이전 수업 프로젝트를 이어 쓰지 않는다.

[공통 라이브러리 배포·설치 안내](../../../../tools/wleno/android/README.md)를 따라 AAR을 준비하고 ViewBinding과 의존성을 설정한다. 기준은 `minSdk 26`, `targetSdk 36`, `compileSdk 36`이다.

[wleno-android-0.1.0.aar](https://github.com/gbox3d/teaching_repo/releases/download/wleno-android-v0.1.0/wleno-android-0.1.0.aar) 파일 한 개를 다운로드하고 압축을 풀지 않은 채 학생 프로젝트의 `app/libs/`에 넣는다. ZIP이나 공통 Kotlin 소스를 함께 넣지 않는다. 폴더가 없으면 만든다. `app/build.gradle.kts`의 기존 `dependencies` 블록에 다음 두 의존성 중 없는 항목만 추가하고 Gradle Sync를 실행한다.

```kotlin
dependencies {
    implementation(files("libs/wleno-android-0.1.0.aar"))
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
}
```

공통 Kotlin 소스는 내부 구현 참고용이다. AAR을 사용할 때는 같은 클래스가 중복되지 않도록 `app/src/main/java/com/example/roomcontrol/wleno/`에 복사했던 공통 소스를 제거한다. 앱의 `MainActivity.kt`와 `ControlActivity.kt`는 유지한다.

## 파일 배치

| 예제 파일 | 학생 프로젝트 경로 |
| --- | --- |
| `wleno-android-0.1.0.aar` | `app/libs/wleno-android-0.1.0.aar` |
| `dayN/MainActivity.kt` | `app/src/main/java/com/example/roomcontrol/MainActivity.kt` |
| `dayN/activity_main.xml` | `app/src/main/res/layout/activity_main.xml` |
| `dayN/AndroidManifest.xml` | `app/src/main/AndroidManifest.xml` |
| `dayN/strings.xml` | `app/src/main/res/values/strings.xml` |
| `dayN/res/values/themes.xml` | `app/src/main/res/values/themes.xml` |
| `day2/ControlActivity.kt` | `app/src/main/java/com/example/roomcontrol/ControlActivity.kt` |
| `day2/activity_control.xml` | `app/src/main/res/layout/activity_control.xml` |

2일차에는 1일차 파일을 `day2` 것으로 바꾸고 제어 화면 두 파일을 추가한다. Manifest에는 `ControlActivity` 선언과 INTERNET 권한이 들어 있다. 기존 `res/values-night/themes.xml`이 있으면 `Theme.RoomControl`의 상속을 `Theme.AppCompat.DayNight.NoActionBar`로 맞춘다.

## 1일차: 연결

시뮬레이터를 `tools/wleno`에서 `uv run main`으로 실행한다. WlEno와 같은 PC의 에뮬레이터는 `10.0.2.2:8266`을 사용한다. 실제 Wi-Fi 연결 없이 호스트 PC로 접근한다. WlEno가 다른 PC에서 실행 중이면 에뮬레이터도 그 PC의 LAN IPv4와 `:8266`을 입력한다. 실기기는 [Wi-Fi 설정 (실기기)]에서 수업 LAN에 연결한 뒤 WlEno 실행 PC의 LAN IPv4와 `:8266`을 입력한다. [주소와 방화벽 조건](../../../iot_sim/lab.md#2-앱에-넣을-주소-결정)을 확인한다.

[제어 시작]을 누르면 `연결 중` → `응답 확인 중` → `준비됨`으로 바뀐다. [해제] 뒤에는 `연결 안 됨`이 된다. 1일차는 연결 확인까지 진행한다.

## 2일차: 책상 조명 제어

[제어 시작]으로 연결되면 `내 방 제어` 화면이 열린다. [조명 켜기]는 `on 0`, [조명 끄기]는 `off 0`을 보낸다. WlEno 창의 LED 0이 켜지고 꺼지는지 확인한다. 화면 아래에는 보낸 명령과 JSON 응답이 표시된다. 정상 응답의 `result`는 `ok`이다.

[연결 화면]을 누르면 연결을 해제하고 시작 화면으로 돌아간다. 다시 [제어 시작]을 눌러 같은 실습을 반복한다. 홈 이동이나 화면 회전으로 연결이 끊겼으면 연결 화면에서 다시 시작한다.

## 확인 기준

- 입력한 주소로 연결되고 제어 화면이 열린다.
- [조명 켜기]와 [조명 끄기]가 시뮬레이터 LED 0에 반영된다.
- 시뮬레이터를 종료하면 제어 버튼이 비활성화된다.
- 연결 화면으로 돌아가 시뮬레이터를 다시 실행한 뒤 재연결할 수 있다.
