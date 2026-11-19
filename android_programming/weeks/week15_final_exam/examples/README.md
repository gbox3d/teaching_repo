# 15주차 예제: 기말 리허설

| 폴더 | 용도 |
|---|---|
| [rehearsal_starter](rehearsal_starter/) | 실행 가능한 시작 코드. TODO 1 조명 버튼, TODO 2 온습도 표시, TODO 3 호출 이력 |
| [rehearsal_solution](rehearsal_solution/) | 세 TODO를 채운 연습용 완성본 |

두 폴더의 연결 화면·XML·공통 설정은 같다. 시작 코드도 연결하고 제어 화면을 열 수 있지만 TODO 부분의 기능은 아직 동작하지 않는다. 공개 예제는 연습 자료이며 실제 시험 문항은 별도 공지한다.

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

[wleno-android-0.1.0.aar](https://github.com/gbox3d/teaching_repo/releases/download/wleno-android-v0.1.0/wleno-android-0.1.0.aar) 파일 한 개를 다운로드하고 압축을 풀지 않은 채 학생 프로젝트의 `app/libs/`에 넣는다. ZIP이나 공통 Kotlin 소스를 함께 넣지 않는다. 폴더가 없으면 만든다. `app/build.gradle.kts`의 기존 `dependencies` 블록에 다음 두 의존성 중 없는 항목만 추가하고 Gradle Sync를 실행한다.

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

1. PC의 `tools/wleno`에서 `python main.py`를 실행한다.
2. 앱 연결 화면에 주소를 넣는다. 같은 PC의 에뮬레이터는 `10.0.2.2:8266`이다.
3. [제어 시작]을 눌러 제어 화면으로 이동한다.
4. 책상 조명, 온습도 확인, 호출 입력 순서로 확인한다. 호출 이력은 14주차 2일차부터 제공한다.

시뮬레이터 입력 이벤트는 `{"event":"input","index":0,"value":1}`이다. `value`는 누를 때마다 0과 1을 번갈아 보낸다. 온습도 응답의 `value`는 `"[24.5,40.0]"`처럼 배열을 담은 문자열이다. 센서는 버튼을 누를 때 한 번 읽는다.
