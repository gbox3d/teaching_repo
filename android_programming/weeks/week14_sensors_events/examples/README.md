# 14주차 예제: 실내 온습도와 호출

| 폴더 | 완성 기능 |
|---|---|
| [day1](day1/) | 연결, 조명 제어, 온습도 1회 요청과 표시 |
| [day2](day2/) | day1 기능 + 호출 이력 최근 20건 |

연결 화면과 조명 기능은 이전 주차를 재사용한다. 이번 주 수정 대상은 `ControlActivity.kt`와 `activity_control.xml`이다. [따라하기](../walkthrough.md)대로 한 기능씩 넣고 완성본과 대조한다.

## 프로젝트에 넣을 위치

프로젝트는 `RoomControl`, package는 `com.example.roomcontrol`이다. [공통 설정](../../../../tools/wleno/android/README.md)에 맞춰 Empty Views Activity, ViewBinding, compileSdk·targetSdk 36을 사용한다. 통신 라이브러리는 제공 AAR로 설치한다.

| 예제 파일 | 프로젝트 위치 |
|---|---|
| `wleno-android-0.1.0.aar` | `app/libs/wleno-android-0.1.0.aar` |
| `MainActivity.kt`, `ControlActivity.kt` | `app/src/main/java/com/example/roomcontrol/` |
| `activity_main.xml`, `activity_control.xml` | `app/src/main/res/layout/` |
| `strings.xml` | `app/src/main/res/values/` |
| `res/values/themes.xml` | `app/src/main/res/values/themes.xml` |
| `AndroidManifest.xml` | `app/src/main/AndroidManifest.xml` |

[wleno-android-0.1.0.aar](https://github.com/gbox3d/teaching_repo/releases/download/wleno-android-v0.1.0/wleno-android-0.1.0.aar) 파일 한 개를 다운로드하고 학생 프로젝트의 `app/libs/`에 넣는다. 폴더가 없으면 만든다. `app/build.gradle.kts`의 기존 `dependencies` 블록에 다음 두 줄을 추가하고 Sync한다.

```kotlin
dependencies {
    implementation(files("libs/wleno-android-0.1.0.aar"))
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
}
```

공통 Kotlin 소스는 내부 구현 참고용이다. AAR을 사용할 때는 같은 클래스가 중복되지 않도록 `app/src/main/java/com/example/roomcontrol/wleno/`에 복사했던 공통 소스를 제거한다. 앱의 `MainActivity.kt`와 `ControlActivity.kt`는 유지한다.

11주차에서 AAR 설치를 마쳤다면 같은 파일과 의존성을 유지한다. 동일한 이름의 화면 파일은 교체한다. MainActivity는 연결 화면, ControlActivity는 내 방 제어 화면이다. 연결 성공 후 제어 화면으로 이동하는 동안에는 연결을 유지한다. 제어 화면에서 나가거나 앱을 배경으로 보내면 연결을 닫는다. 회전 뒤에도 연결 화면에서 다시 연결한다.

기존 SmartIO 프로젝트에 덧붙이지 않고 11주차부터 새로 만든 RoomControl 프로젝트를 사용한다. 각 폴더에는 두 화면의 전체 파일이 들어 있으며, 공통 통신 라이브러리는 위 위치에서 함께 사용한다.

## 실행

1. PC의 `tools/wleno`에서 `uv run main`을 실행한다.
2. 앱 연결 화면에 주소를 넣는다. 같은 PC의 에뮬레이터는 `10.0.2.2:8266`이다.
3. [제어 시작]을 눌러 제어 화면으로 이동한다.
4. 책상 조명, 온습도 확인, 호출 입력 순서로 확인한다. 호출 이력은 14주차 2일차부터 제공한다.

시뮬레이터 입력 이벤트는 `{"event":"input","index":0,"value":1}`이다. `value`는 누를 때마다 0과 1을 번갈아 보낸다. 온습도 응답의 `value`는 `"[24.5,40.0]"`처럼 배열을 담은 문자열이다. 센서는 버튼을 누를 때 한 번 읽는다.
