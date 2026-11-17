# 12주차 예제 · 내 방 제어

`day1`은 책상·침대 조명 선택, `day2`는 밝기 조절과 전체 끄기를 추가한 완성본이다.

11주차의 `RoomControl` 프로젝트를 이어 쓴다. package는 `com.example.roomcontrol`이다. 프로젝트가 없으면 [공통 설정](../../../../tools/wleno/android/README.md)대로 Empty Views Activity를 만든다. 10주차 이전 프로젝트는 필요하지 않다.

| 예제 파일 | 프로젝트 위치 |
|---|---|
| `MainActivity.kt`, `ControlActivity.kt` | `app/src/main/java/com/example/roomcontrol/` |
| `activity_main.xml`, `activity_control.xml` | `app/src/main/res/layout/` |
| `strings.xml` | `app/src/main/res/values/strings.xml` |
| `res/values/themes.xml` | `app/src/main/res/values/themes.xml` |
| `AndroidManifest.xml` | `app/src/main/AndroidManifest.xml` |
| `wleno-android-0.1.0.aar` | `app/libs/wleno-android-0.1.0.aar` |

`compileSdk=36`, `targetSdk=36`, `minSdk=26`, ViewBinding, AppCompat·Lifecycle 의존성은 공통 설정을 따른다. 같은 일차의 Kotlin과 XML을 함께 사용한다.

[wleno-android-0.1.0.aar](https://github.com/gbox3d/teaching_repo/releases/download/wleno-android-v0.1.0/wleno-android-0.1.0.aar) 파일 한 개를 다운로드하고 압축을 풀지 않은 채 학생 프로젝트의 `app/libs/`에 넣는다. ZIP이나 공통 Kotlin 소스를 함께 넣지 않는다. 폴더가 없으면 만든다. `app/build.gradle.kts`의 기존 `dependencies` 블록에 다음 두 의존성 중 없는 항목만 추가하고 Gradle Sync를 실행한다.

```kotlin
dependencies {
    implementation(files("libs/wleno-android-0.1.0.aar"))
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
}
```

공통 Kotlin 소스는 내부 구현 참고용이다. AAR을 사용할 때는 같은 클래스가 중복되지 않도록 `app/src/main/java/com/example/roomcontrol/wleno/`에 복사했던 공통 소스를 제거한다. 앱의 `MainActivity.kt`와 `ControlActivity.kt`는 유지한다.

11주차에서 AAR 설치를 마쳤다면 같은 파일과 의존성을 유지한다.

학생은 제어 화면을 수정한다. 연결 화면은 제공 완성본이며 연결 성공 때 제어 화면을 연다. `selectedLamp()`는 책상 선택에 0, 침대 선택에 1을 반환한다. 버튼은 이 값을 `on`·`off`·`pwm` 명령에 넣는다. `brightnessBar.progress`는 0~255 범위다.

제어 화면의 `onStop()`은 수신 리스너를 해제하고 연결을 닫는다. 홈 화면 이동·회전 뒤에는 연결 화면에서 다시 제어를 시작한다. 원본 응답은 최근 한 건만 표시한다. 자동 재연결이나 UDP 검색 UI는 이 예제의 학습 범위가 아니다.
