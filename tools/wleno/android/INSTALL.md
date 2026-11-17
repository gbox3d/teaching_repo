# WlEno Android 0.1.0 설치

이 배포본은 Android 앱에서 PC의 WlEno 시뮬레이터에 TCP로 연결하는 라이브러리다. 학생은 AAR 파일 한 개를 추가한다. 설치·실행 순서는 AAR 배치 → Gradle Sync → WlEno 실행 → IPv4:포트 입력 → 연결 → 제어다.

## 1. AAR 파일 배치

[wleno-android-0.1.0.aar 다운로드](https://github.com/gbox3d/teaching_repo/releases/download/wleno-android-v0.1.0/wleno-android-0.1.0.aar)를 눌러 파일 한 개를 내려받고 학생 프로젝트의 `app/libs/`에 그대로 넣는다. 압축을 풀지 않는다. 폴더가 없으면 만든다. Android Studio 왼쪽 보기에서 Android 대신 Project를 선택하면 실제 폴더 경로를 확인하기 쉽다.

```text
RoomControl/
└── app/
    ├── libs/
    │   └── wleno-android-0.1.0.aar
    ├── build.gradle.kts
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/...
        └── res/layout/activity_main.xml
```

이미 복사한 `ConnState.kt`, `SimulatorDevice.kt`, `Wleno.kt`, `WlenoClient.kt`, `WlenoMessage.kt`가 있으면 학생 프로젝트에서 제거한다. 이 다섯 클래스는 AAR에 들어 있으므로 함께 두면 중복 클래스가 생긴다.

## 2. 앱 모듈의 Gradle 의존성

`app/build.gradle.kts`의 기존 `dependencies` 블록에 다음 두 줄을 넣고 Sync Now를 누른다.

```kotlin
implementation(files("libs/wleno-android-0.1.0.aar"))
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
```

이미 coroutines-android 의존성이 있으면 중복 선언하지 않는다. 로컬 AAR 파일은 전이 의존성을 자동으로 가져오지 않으므로 코루틴 의존성은 앱에서 선언한다. [Android 공식 AAR 설치 안내](https://developer.android.com/studio/projects/android-library#psd-add-aar-jar-dependency)

앱의 `minSdk`는 26 이상을 사용한다. 정규 수업은 `targetSdk = 36`을 기준으로 한다. AAR에는 `INTERNET` 권한이 들어 있고 앱 Manifest에 병합된다. 앱의 Activity 등록과 테마 설정은 주차별 예제의 Manifest를 따른다.

AAR은 통신 코드만 제공한다. `MainActivity.kt`, 화면 XML, 문자열과 테마는 해당 주차 예제를 사용한다. ViewBinding과 lifecycleScope 등 화면 코드에 필요한 의존성은 교재의 프로젝트 설정을 따른다.

## 3. import 확인

`MainActivity.kt`에서 다음 import가 인식되면 라이브러리를 찾은 것이다.

```kotlin
import com.example.roomcontrol.wleno.ConnState
import com.example.roomcontrol.wleno.Wleno
```

앱 패키지가 `com.example.day1002` 등 다른 이름이어도 이 두 import는 바꾸지 않는다. AAR 내부의 패키지는 `com.example.roomcontrol.wleno`로 고정되어 있다. Activity 자체의 `package`와 `databinding` import는 학생 앱의 패키지를 사용한다.

## 4. 연결 확인

저장소 루트에서 다음 명령으로 PC의 WlEno를 실행한다. uv 설치 등 준비 사항은 [시뮬레이터 안내](../README.md#2-준비)를 따른다.

```powershell
cd tools/wleno
uv run main
```

앱의 [시뮬레이터 주소]에 실행 위치에 맞는 주소를 입력한다.

| 앱과 WlEno 실행 위치 | 앱에 넣을 주소 |
|---|---|
| 에뮬레이터와 WlEno가 같은 PC | `10.0.2.2:8266` |
| 에뮬레이터와 WlEno가 다른 PC | `WlEno PC의 LAN IPv4:8266` (예: `192.168.0.10:8266`) |
| Android 실기기 | `WlEno PC의 LAN IPv4:8266` (예: `192.168.0.10:8266`) |

다른 PC·실기기는 WlEno PC와 LAN 통신이 허용되어야 한다. WlEno의 기본 바인드 `0.0.0.0`은 앱에 넣는 주소가 아니며, Windows에서는 TCP 8266 인바운드 허용을 확인한다. UDP 8267은 선택 검색용이고 HTTP 8080은 앱 연결에 쓰지 않는다. [주소·방화벽 안내](../README.md#6-앱에서-붙을-주소)

11주차 1일차 앱에서 [제어 시작]을 눌러 `준비됨`을 확인한다. 2일차 앱에서는 연결 후 제어 화면이 열린다. [조명 켜기]와 [조명 끄기]를 누르고 WlEno PC의 LED 0 변화를 확인한다. 외부 인터넷에서는 LAN 주소만으로 접속할 수 없으며 별도 네트워크 구성이 필요하다.

## 오류 확인

| 오류 | 확인 |
|---|---|
| `Unresolved reference: wleno` | AAR 위치, app 모듈의 의존성 선언, Gradle Sync 결과 |
| `Unresolved reference: StateFlow` 또는 코루틴 관련 오류 | coroutines-android 의존성 |
| `Duplicate class` | 기존 공통 Kotlin 소스나 다른 버전 AAR 중복 포함 |
| `minSdkVersion ... cannot be smaller than version 26` | 앱 minSdk를 26 이상으로 설정 |
| `Element ScrollView must be declared` | 레이아웃을 Manifest에 넣었는지 확인. Manifest 루트는 `<manifest>`, 화면 XML 루트는 `<ScrollView>` |
| 연결이 `끊김`으로 끝난다 | WlEno 실행 상태, 같은 PC/다른 PC 주소 구분, TCP 8266 포트와 방화벽 확인 |

공개 API와 교재 원본: https://github.com/gbox3d/teaching_repo/tree/main/tools/wleno/android
저작권과 이용 조건은 저장소의 [LICENSE](../../../LICENSE)를 따른다.
