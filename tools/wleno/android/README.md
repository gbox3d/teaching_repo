# WlEno Android 라이브러리

11~15주차 정규 실습은 PC의 [WlEno 시뮬레이터](../README.md)에 LAN/TCP로 연결한다. 실기기는 Wi-Fi, PC는 유선이나 Wi-Fi로 같은 LAN에 참여할 수 있다. 에뮬레이터는 호스트 주소 `10.0.2.2`로 연결하므로 실제 Wi-Fi가 필요하지 않다.

## 학생 설치: AAR 파일 한 개

[wleno-android-0.1.0.aar 다운로드](https://github.com/gbox3d/teaching_repo/releases/download/wleno-android-v0.1.0/wleno-android-0.1.0.aar)를 눌러 파일 한 개를 내려받고 `app/libs/`에 그대로 넣는다. 압축을 풀지 않는다. [설치 안내](INSTALL.md)에 파일 위치, Gradle 설정, 확인 순서가 있다.

`app/build.gradle.kts`의 기존 `dependencies`에 추가한다.

```kotlin
implementation(files("libs/wleno-android-0.1.0.aar"))
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
```

기존 코루틴 의존성은 중복 선언하지 않는다. 파일 AAR의 의존성은 앱에서 함께 선언해야 한다. [Android 공식 라이브러리 안내](https://developer.android.com/studio/projects/android-library)

앱 패키지와 관계없이 `com.example.roomcontrol.wleno.Wleno`와 `ConnState`를 import한다. 이미 공통 소스를 복사한 프로젝트는 다섯 파일을 제거한 뒤 AAR을 추가한다.

## RoomControl 화면 프로젝트 설정

Android Studio의 Empty Views Activity로 `RoomControl`을 새로 만든다. 패키지는 `com.example.roomcontrol`, 언어는 Kotlin이다. 이전 수업 앱은 가져오지 않는다.

기준은 `minSdk = 26`, `targetSdk = 36`, `compileSdk = 36`이다. `app/build.gradle.kts`의 기존 `android` 블록 안에 `buildFeatures { viewBinding = true }`를 둔다. 기존 AppCompat·Core·Activity 의존성은 유지한다. 새 프로젝트에 필요한 항목이 없으면 아래 검증에 사용한 버전을 추가한다.

```kotlin
dependencies {
    implementation(files("libs/wleno-android-0.1.0.aar"))
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
    implementation("androidx.appcompat:appcompat:1.7.1")
    implementation("androidx.core:core-ktx:1.16.0")
    implementation("androidx.activity:activity-ktx:1.8.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.6.2")
}
```

SDK 36.1만 설치된 AGP 9 프로젝트에서는 `compileSdk = 36` 대신 다음 블록을 사용한다. `targetSdk`는 36으로 유지한다.

```kotlin
compileSdk {
    version = release(36) { minorApiLevel = 1 }
}
```

라이브러리 Manifest의 `INTERNET` 권한은 앱에 병합된다. 주차별 앱 Manifest에도 같은 권한이 있으며 중복 선언은 하나로 병합된다. 화면 레이아웃은 `app/src/main/res/layout/activity_main.xml`에, 앱 Manifest는 `app/src/main/AndroidManifest.xml`에 넣는다.

수업 예제는 Wi-Fi 검색 API를 호출하지 않으므로 Wi-Fi·위치·Bluetooth 권한을 요청하지 않는다. `targetSdk` 37 이상으로 바꾸면 LAN 통신에 `ACCESS_LOCAL_NETWORK` 런타임 권한 처리를 추가해야 한다. [Android 로컬 네트워크 권한](https://developer.android.com/privacy-and-security/local-network-permission)

## 강의자: 배포 파일 만들기

이 폴더는 독립 Android Library Gradle 프로젝트다. Android Studio에서 `tools/wleno/android`를 열면 된다. 터미널에서는 Android Studio의 JBR을 `JAVA_HOME`에 지정하고 Android SDK 경로를 `ANDROID_HOME` 또는 로컬 `local.properties`의 `sdk.dir`로 지정한다. `local.properties`는 저장소에 올리지 않는다.

필요한 SDK는 Android 36.1이며 Gradle 9.4.1, AGP 9.2.1을 고정했다. Windows에서는 이 폴더에서 실행한다.

```powershell
.\gradlew.bat packageDistribution
```

macOS/Linux에서는 `sh ./gradlew packageDistribution`을 실행한다. Gradle wrapper는 Gradle 다운로드 파일의 SHA-256을 검사한다.

생성 파일은 `dist/wleno-android-0.1.0.aar` 한 개다. GitHub Release에 이 AAR을 첨부하고 학생은 다운로드한 파일을 `app/libs/`에 넣는다.

`dist/`와 `build/`는 재생성하는 파일이라 Git에서 제외한다. 버전은 `gradle.properties`의 `wlenoVersion`으로 관리하며, 올릴 때 설치 안내와 교재의 AAR 파일명도 함께 갱신한다.

## 공통 소스 참고

[src](src)의 다섯 Kotlin 파일이 AAR에 컴파일된다. 학생 설치에는 필요하지 않으며 통신 구현을 읽거나 라이브러리를 수정할 때 참고한다.

| 파일 | 역할 |
|---|---|
| `Wleno.kt` | 앱 전체의 `Wleno.client` |
| `WlenoClient.kt` | TCP 연결, 줄 단위 송수신, UDP 검색 |
| `SimulatorDevice.kt` | 검색 결과 |
| `ConnState.kt` | 연결 상태 상수 |
| `WlenoMessage.kt` | JSON 응답 필드 읽기 |

## 제공 코드의 연결과 명령

연결 화면의 [제어 시작]에서 연결을 요청한다. `connect()`는 비동기이므로 호출 직후에 명령을 보내지 않는다.

```kotlin
val client = Wleno.client
client.connect("10.0.2.2:8266")
```

`connectionState`에서 `ConnState.READY`를 확인한 뒤 제어 화면을 연다. 제어 화면은 수신 리스너를 등록하고, 사용자가 조명 버튼을 눌렀을 때 명령을 보낸다. 아래 코드는 각각 해당 생명주기와 클릭 리스너 안에 넣는다.

```kotlin
// 제어 화면 onStart
client.onMessage { jsonLine -> /* 응답을 화면에 표시 */ }

// [조명 켜기] 클릭
if (client.isReady) client.send("on 0")

// 제어 화면 onStop
client.onMessage(null)
client.disconnect()
```

실제 두 화면의 전체 흐름은 [11주차 완성 예제](../../../android_programming/weeks/week11_lan_connection/examples/README.md)를 따른다.

공개 메서드는 메인 스레드에서 호출한다. 소켓 연결·읽기·쓰기는 클라이언트의 작업 스레드에서 실행한다. 리스너는 메인 스레드에서 호출된다. `send()`는 명령 끝에 줄바꿈을 붙이며, 빈 명령과 줄바꿈이 포함된 명령은 보내지 않는다.

주소는 IPv4와 포트로 입력한다. 포트를 생략하면 8266을 쓴다. 연결 시간 제한은 3초이고, 연결 후 `hello` 수신 시간 제한도 3초이다. `event=hello`, `app=WlEno`, 비어 있지 않은 `name`을 확인한 뒤에만 `준비됨`이 된다. TCP가 연결되었다는 사실만으로 준비 완료로 판단하지 않는다.

```text
연결 안 됨 → 연결 중 → 응답 확인 중 → 준비됨
연결 실패·잘못된 hello·상대 종료 → 끊김
사용자가 해제 → 연결 안 됨
```

| 명령 | 응답에서 확인할 값 |
| --- | --- |
| `about` | `result=ok`, `app=WlEno` |
| `on 0`, `off 0`, `off -1` | `result=ok`, `ms` |
| `pwm 0 128` | `result=ok`, `ms=pwm set` |
| `dht11` | `value`는 배열 모양의 문자열, 예: `"[24.5,40.0]"` |

`help` 명령은 없다. 도움말은 교재의 명령 표를 본다. 시뮬레이터의 입력 버튼은 요청 없이 `{"event":"input","index":0,"value":1}` 같은 이벤트를 보낸다. `WlenoMessage.event()`로 일반 응답과 구분한다.

## 선택 참고: UDP 검색

```kotlin
client.startScan(
    timeoutMs = 5000,
    onFound = { device -> /* device.name, device.address */ },
    onFinished = { /* 검색 완료 표시 */ }
)
client.stopScan()
```

UDP 8267에 호환 검색 문자열 `bleuno?`를 보내며, 응답의 이름과 TCP 포트로 `SimulatorDevice`를 만든다. 기본 장치 이름은 `WlEno_SIM1`이며 이름 접두사를 검사하지 않는다. 브로드캐스트가 차단된 환경에서는 IP를 직접 입력한다. `connect()`는 진행 중인 검색을 먼저 중지한다.

## 화면 수명과 연결

11주차 2일차부터 연결 성공 후 `MainActivity`가 `ControlActivity`를 연다. 이 화면 전환에서는 TCP 연결과 수신 리스너를 유지한다. 제어 화면은 `onStart()`에서 수신 리스너를 등록하고 `onStop()`에서 리스너와 연결을 해제한다. 제어 화면에서 뒤로 돌아오거나 홈으로 이동한 뒤에는 [제어 시작]으로 다시 연결한다. 화면 회전으로 제어 화면이 재생성되어 연결이 끊겼으면 [연결 화면]으로 돌아가 다시 연결한다.

연결 화면의 `pendingConnect`는 사용자가 누른 새 연결에만 화면 전환을 허용한다. 제어 화면에서 돌아올 때 준비 상태가 잠시 남아 있어도 자동으로 다시 열지 않는다. `openingControl`은 제어 화면을 여는 동안 연결 화면의 `onStop()`이 소켓을 닫지 않도록 구분한다. 이 수명 관리는 제공 코드로 사용하며 학생 실습은 연결과 제어 버튼에 집중한다.

상대가 연결을 닫으면 `끊김`이 된다. PC 절전이나 LAN 단절처럼 종료 신호가 없는 경우에는 운영체제의 TCP 감지가 늦을 수 있다. 응답이 멈추면 [해제] 후 주소와 시뮬레이터를 확인한다. 시뮬레이터는 연결·해제 때 LED를 모두 끄므로 다시 연결한 뒤 필요한 명령을 다시 보낸다.

## 통신 확인

앱 주소는 에뮬레이터에서 `10.0.2.2:8266`, 실기기에서 `PC의 LAN IPv4:8266`이다. `127.0.0.1`은 앱 자신을 가리킨다. [에뮬레이터 주소 공간](https://developer.android.com/studio/run/emulator-networking-address)

시뮬레이터의 HTTP 8080은 PC에서 상태를 확인하거나 입력을 재현하는 보조 API다. Android 앱은 TCP 8266을 사용한다. Logcat의 `tag:TCP`와 시뮬레이터 터미널 로그를 함께 확인한다.
