# 11주차 따라하기: 연결한 뒤 책상 조명 제어

새 `RoomControl` 프로젝트로 시작한다. 완성본은 [1일차](examples/day1/)와 [2일차](examples/day2/)에 있다. 공통 통신 코드는 수정하지 않고 사용한다.

## 1일차: 연결 화면

### 1. 시뮬레이터 실행

터미널에서 저장소의 `tools/wleno` 폴더로 이동한다.

```powershell
uv run main
```

LED 네 개가 있는 창을 닫지 않는다. 이 프로그램이 앱의 명령을 받는다.

### 2. 새 프로젝트 생성

Android Studio에서 New Project → Empty Views Activity를 선택한다. 이름은 `RoomControl`, Package name은 `com.example.roomcontrol`, 언어는 Kotlin으로 지정한다. Compose 템플릿은 사용하지 않는다.

[공통 라이브러리 설치](../../../tools/wleno/android/README.md)의 SDK·ViewBinding 설정을 적용한다. 조교가 제공한 AAR을 사용하므로 통신 소스를 직접 복사하지 않는다.

[wleno-android-0.1.0.aar](https://github.com/gbox3d/teaching_repo/releases/download/wleno-android-v0.1.0/wleno-android-0.1.0.aar) 파일 한 개를 다운로드하고 압축을 풀지 않은 채 학생 프로젝트의 `app/libs/`에 넣는다. ZIP이나 공통 Kotlin 소스를 함께 넣지 않는다. 폴더가 없으면 만든다. `app/build.gradle.kts`의 기존 `dependencies` 블록에 다음 두 의존성 중 없는 항목만 추가하고 Gradle Sync를 실행한다.

```kotlin
dependencies {
    implementation(files("libs/wleno-android-0.1.0.aar"))
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
}
```

공통 Kotlin 소스는 내부 구현 참고용이다. AAR을 사용할 때는 같은 클래스가 중복되지 않도록 `app/src/main/java/com/example/roomcontrol/wleno/`에 복사했던 공통 소스를 제거한다. 앱의 `MainActivity.kt`와 `ControlActivity.kt`는 유지한다.

`Wleno`와 `ConnState` 클래스는 AAR 안에 있다. 다음 import는 예제 Activity 파일 위쪽의 `package` 다음에 있으며, 클래스를 직접 만들거나 소스 폴더에서 찾을 필요가 없다.

```kotlin
import com.example.roomcontrol.wleno.ConnState
import com.example.roomcontrol.wleno.Wleno
```

### 3. 연결 화면 배치

[day1/activity_main.xml](examples/day1/activity_main.xml)을 `res/layout/activity_main.xml`에 넣는다. 앱 제목과 주소 안내, 실기기 Wi-Fi 설정 버튼 아래에 주소 입력 칸을 둔다. 이어 [제어 시작], [해제], 연결 상태가 보인다.

[예제 위치 표](examples/README.md)를 따라 Manifest, strings, themes도 넣는다. 두 XML 파일은 역할과 위치가 다르다. XML 선언 다음의 루트 태그로 구분한다.

| 파일 경로 | 루트 태그 | 내용 |
|---|---|---|
| `app/src/main/AndroidManifest.xml` | `<manifest>` | 권한과 Activity 등록 |
| `app/src/main/res/layout/activity_main.xml` | `<ScrollView>` | 연결 화면의 입력 칸과 버튼 |

화면 XML은 `res/layout/activity_main.xml`에 넣는다. `AndroidManifest.xml`에 `<ScrollView>`가 보이면 잘못 붙인 것이므로 [day1/AndroidManifest.xml](examples/day1/AndroidManifest.xml) 내용으로 교체한다. Manifest의 `INTERNET` 권한은 TCP 소켓에 필요하다. 이 수업 설정에서는 권한 요청 대화상자를 따로 만들지 않는다.

### 4. 연결 버튼 구현

[day1/MainActivity.kt](examples/day1/MainActivity.kt)를 열고 연결 버튼의 다음 부분을 찾는다.

```kotlin
val address = binding.addressEdit.text.toString().trim()
```

입력한 주소를 문자열로 읽는다. 빈 칸이면 입력 오류를 표시하고, 값이 있으면 `client.connect(address)`를 호출한다. 실제 네트워크 작업은 제공 클라이언트가 수행한다.

WlEno와 같은 PC의 에뮬레이터에서는 `10.0.2.2:8266`을 넣는다. WlEno를 다른 PC에서 실행했다면 에뮬레이터도 그 PC의 LAN IPv4와 `:8266`을 넣는다. `10.0.2.2`는 에뮬레이터를 실행한 PC만 가리킨다. `8266`은 시뮬레이터의 TCP 포트이며 `http://`는 붙이지 않는다.

실기기에서는 [Wi-Fi 설정 (실기기)]으로 시스템 설정을 연다. 수업 LAN에 접속한 뒤 앱으로 돌아와 WlEno 실행 PC의 LAN IPv4와 `:8266`을 넣는다. PC가 유선 LAN이어도 휴대전화에서 그 주소로 통신할 수 있으면 된다. 다른 PC나 실기기에서 접속할 때는 WlEno 실행 PC의 TCP 8266 방화벽 허용도 확인한다. 주소와 네트워크 조건은 [연결 점검 표](../../iot_sim/lab.md#2-앱에-넣을-주소-결정)를 따른다.

### 5. 연결 결과 확인

앱을 실행하고 [제어 시작]을 누른다. 상태가 `연결 중`, `응답 확인 중`을 거쳐 `준비됨`이 된다. 빠른 PC에서는 중간 상태가 눈에 보이지 않을 수 있다.

[해제]를 누르면 `연결 안 됨`으로 돌아간다. 시뮬레이터를 종료한 뒤 같은 주소로 연결해 `끊김`을 확인한다. 시뮬레이터를 다시 실행하고 재연결하면 `준비됨`이 되어야 한다. 실패해도 앱이 종료되지 않아야 한다.

1일차는 이 화면까지 완성한다. 장치 검색, 목록, 마지막 주소 저장은 넣지 않는다.

## 2일차: 연결 성공 후 제어 화면

### 6. 제어 화면 추가

[day2/ControlActivity.kt](examples/day2/ControlActivity.kt)를 기본 패키지에 추가하고 [activity_control.xml](examples/day2/activity_control.xml)을 `res/layout`에 넣는다. [day2/AndroidManifest.xml](examples/day2/AndroidManifest.xml)에는 `ControlActivity` 등록이 포함되어 있다.

제어 화면에는 책상 조명(LED 0), [조명 켜기], [조명 끄기], 연결 상태, 마지막 명령과 응답, [연결 화면] 버튼을 배치한다. 먼저 XML을 적용하고 Design 미리보기에서 버튼을 확인한다.

### 7. 연결 성공과 화면 전환 연결

`MainActivity.kt`를 [2일차 완성본](examples/day2/MainActivity.kt)과 비교한다. 연결 버튼에서 `pendingConnect = true`를 설정한다. 상태가 `ConnState.READY`가 되면 아래 코드로 제어 화면을 연다.

```kotlin
startActivity(Intent(this@MainActivity, ControlActivity::class.java))
```

연결 버튼을 눌렀다는 사실만으로 화면을 열지 않는다. 시뮬레이터와 연결이 준비된 뒤 연다. `pendingConnect`와 `openingControl` 및 생명주기 처리는 제공된 틀을 유지한다.

실행해서 [제어 시작]을 누른다. 제어 화면이 열리고 `상태: 준비됨`이 보여야 한다. 연결이 실패하면 연결 화면에 남아 있어야 한다.

### 8. 책상 조명 켜기·끄기

`ControlActivity`에서 버튼 두 개를 연결한다. 아래 코드는 완성본과 같다.

```kotlin
binding.onButton.setOnClickListener { send("on 0") }
binding.offButton.setOnClickListener { send("off 0") }
```

`on`은 켜기, `off`는 끄기, `0`은 시뮬레이터의 첫 LED 번호다. `send` 함수는 화면에 보낸 명령을 표시한 뒤 `client.send(command)`를 호출한다. 줄바꿈과 전송은 제공 코드가 처리한다.

[조명 켜기]를 누르고 PC의 LED 0이 켜지는지 확인한다. 이어 [조명 끄기]를 눌러 꺼지는지 확인한다. 앱 버튼 반응과 시뮬레이터의 변화가 둘 다 있어야 완료다.

### 9. 응답과 재연결 확인

제어 화면의 `client.onMessage`는 시뮬레이터가 보낸 응답을 `responseText`에 표시한다. 이번 주에는 응답을 그대로 확인한다. JSON에서 값 꺼내기는 다음 주에 다룬다.

시뮬레이터의 [연결 끊기]를 누르면 앱의 상태가 `끊김`으로 바뀌고 조명 버튼이 비활성화된다. [연결 화면]으로 돌아가 [제어 시작]을 다시 누른다.

제어 화면에서 홈으로 나가거나 화면을 회전하면 이 예제는 연결을 해제한다. 돌아온 뒤 [연결 화면]에서 다시 연결한다. 연결·해제 때 시뮬레이터는 LED를 끄므로 새로 연결한 뒤 [조명 켜기]를 누른다.

## 오류 확인

| 증상 | 확인 |
|---|---|
| `Wleno`·`ConnState` import 오류 | `app/libs/`의 AAR 파일명과 Gradle 의존성 확인 후 Sync. 클래스를 새로 만들지 않음 |
| `Duplicate class` 오류 | AAR과 공통 `wleno` 소스가 함께 들어갔는지 확인하고 복사한 공통 소스 제거 |
| Manifest에서 `ScrollView` 오류 | 화면 XML을 `res/layout/activity_main.xml`로 옮기고 Manifest 예제 복원 |
| ActivityMainBinding을 찾을 수 없음 | ViewBinding 설정과 XML 오류 확인, Sync 후 빌드 |
| ControlActivity를 찾을 수 없음 | 파일 패키지와 Manifest 등록 확인 |
| 상태가 끊김 | 시뮬레이터 실행 여부, 주소, TCP 8266 확인 |
| 다른 PC의 에뮬레이터·휴대전화에서만 연결 실패 | WlEno 실행 PC의 LAN IPv4·TCP 8266 방화벽·단말 격리 확인 |
| 연결 직후 제어 화면이 끊김 | 2일차 MainActivity의 `openingControl` 처리 확인 |
| 조명 버튼이 비활성화됨 | 연결 화면으로 돌아가 재연결 |

전송 기록을 자세히 확인할 때만 Logcat의 `tag:TCP`와 시뮬레이터 터미널을 확인한다.
