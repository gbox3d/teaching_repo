# bleuno 패키지 — Smart I/O 보드와 이야기하는 제공 클래스

12주차부터 `SmartIO` 앱은 이 폴더의 클래스로 보드를 검색하고, 연결하고, 명령을 보내고, 응답을 받는다.
`BluetoothGatt`의 콜백은 클래스 안에 감싸져 있으므로 앱 코드에서는 `startScan`·`connect`·`send`·`onMessage` 네 가지만 부른다.
보드가 없어도 `fake = true`로 같은 코드를 그대로 실행할 수 있다.
PC에서 돌리는 Wi-Fi 시뮬레이터에 `Bleuno.createTcp()`로 연결해 같은 명령·응답을 주고받을 수도 있다([10절](#10-보드-없이-wi-fi-시뮬레이터로-연습하기)).

## 교재와 별도 앱의 역할

수업의 기준은 매주 확장하는 **SmartIO 앱과 이 폴더의 공통 클래스 9개**다.
이 폴더는 독립 Android Studio 프로젝트가 아니며, 아래 안내대로 학생의 SmartIO 프로젝트에 넣는다.

| 위치 | 역할 |
|---|---|
| 이 폴더의 `src/`와 주차별 SmartIO 예제 | 학생용 수업 코드. 같은 인터페이스로 Fake와 실제 보드를 바꿔 연습한다 |
| [bleunoApp/BleunoTest](https://github.com/gbox3d/bleunoApp/tree/main/BleunoTest) | 강의자·조교의 보드 점검 및 명령 시연용 독립 앱 |
| [bleunoApp](https://github.com/gbox3d/bleunoApp)의 `Ex01Scaner`, `ScanerSample` | 검색 기능을 따로 살펴보는 참고 예제 |
| [bleuno-sim](../../tools/bleuno-sim/README.md) | 보드 없이 PC에서 돌리는 Wi-Fi 시뮬레이터. `TcpBleunoClient`로 연결해 같은 명령·응답을 연습한다 |
| [bleuno](https://github.com/gbox3d/bleuno) | 펌웨어 정본. 마더보드 설계는 이 저장소의 `hardware/type_m/v1/`, `hardware/type_s/v1/`에서 모델별로 관리한다 |

**BLEuno type_m v1의 모델명은 `type_m`, 하드웨어 버전은 `v1`**이며, 펌웨어 버전 `1.0.5_dev`와 구분한다.
type_m v1 마더보드의 EasyEDA 원본을 확보하고 KiCad 이전·원본 대조를 마쳤다. 원본 설계의 전기적 미연결과 모듈 핀 표기 검토는 남아 있다.
원본은 **모터·서보 제어 보드**로, 아래의 기존 LED 4개·DHT11 실습을 바로 적용할 수 없다.
[type_m v1 원본 핀맵과 확인 사항](https://github.com/gbox3d/bleuno/blob/main/hardware/type_m/v1/pinmap.md)에 회로도·PCB에서 확인한 연결을 기록했다.
아래 GPIO와 상태 LED 설명은 기존 수업 설정을 기준으로 한다. type_m 전용 펌웨어·TypeMControl은 Android 실기기와 BLE 준비·STOP·배경 전환·재연결을 확인했으며, 모터·서보의 실제 부하 구동·파형 계측은 아직 하지 않았다.

type_m v1에서는 GPIO0이 배터리 분압 입력(CHKBAT), GPIO7이 모터 드라이버 SLEEP 제어다.
따라서 기존 `ledpin=[4,3,1,0]`과 `dht11pin=7`을 그대로 적용하지 않는다.
센서 커넥터의 SEN1은 원본에서 MCU에 연결되지 않았다. 기존 수업은 기존 보드 또는 Fake 모드로 유지한다. type_m v1 확장 실습의 부하 연결은 조교가 실제 전원과 결선을 점검한 장비에서 진행한다.

모터·서보 확장 수업은 [type_m 전용 90분 실습](type_m_lab.md)을 따른다. 독립 앱 `bleunoApp/TypeMControl`과 펌웨어 환경 `type_m`을 사용하며, CCCD 구독·모델 확인·`ready` 응답을 거친 뒤 제어한다. 아래 SmartIO/Fake의 JSON·LED 명령 규약과 구분한다. 업로드·실기 검증 현황은 해당 실습 자료에서 확인한다.

센서·입출력 커넥터 보드인 **type_s v1**은 [별도 원본 핀맵](https://github.com/gbox3d/bleuno/blob/main/hardware/type_s/v1/pinmap.md)을 참고한다.
DHT·CDS·DS18B20은 커넥터 표기이며 센서 실장이나 현재 펌웨어 지원을 의미하지 않는다. 기존 LED 설정은 센서·분압 입력과 충돌하며, 기존 `dht11pin=7`은 D2에 해당한다(DHT 헤더 신호는 GPIO3).
이 핀맵은 제조·실기 확정값이 아니다. 모델별 전원·외부 결선·펌웨어 설정을 검증하기 전에는 기존 보드 또는 Fake 모드의 실습 흐름을 유지한다.

## 1. 보드

| 항목 | 값 |
|---|---|
| 보드 | ESP32-C3 + bleuno 펌웨어 1.0.5_dev |
| 기기 이름 | `ESP32_BLE` + 칩 ID (예: `ESP32_BLE7C9EBF`). 검색할 때 이 앞글자로 보드를 고른다 |
| Service UUID | `c6f8b088-2af8-4388-8364-ca2a907bdeb8` |
| Characteristic UUID | `f6aa83ca-de53-46b4-bdea-28a7cb57942e` (읽기·쓰기·알림을 하나로 쓴다) |
| CCCD UUID | `00002902-0000-1000-8000-00805f9b34fb` (알림을 켜는 설정 항목) |

### 보드 LED 색으로 상태 보기

| 보드 LED | 뜻 |
|---|---|
| 빨강 | 전원이 막 들어옴(부팅 중) |
| 파랑 깜빡임 | 연결을 기다리는 중. 이때만 검색 목록에 보인다 |
| 파랑 고정 | 앱과 연결됨. 연결이 끊기면 상태 LED가 다시 파랑 깜빡임으로 돌아간다. 이 파랑 표시는 현재 TENSTAR 빌드의 소스 기준이다. 연결된 동안 `blink`나 `stopblk`를 보내면 이 파랑 표시가 꺼진다(펌웨어 소스 기준). 앱으로 제어하는 외부 LED는 연결될 때 모두 꺼지고, 연결이 끊길 때도 밝기(`pwm`)까지 모두 꺼진다. 이 LED 끄기는 TENSTAR 조건 밖의 공통 코드다(펌웨어 소스 기준, 실제 보드로는 확인하지 못했다) |

내장 상태 LED와 앱으로 제어하는 외부 LED는 별개다. 연결·해제 때 외부 LED를 끄는 곳은 펌웨어 `ble.cpp`의 연결 콜백이다. 연결될 때 `onConnect`가 `ledOff(-1)`로 LED 출력을 모두 끄고, 끊길 때 `onDisconnect`가 `clearAllControl()`(`main.cpp`)로 LED 출력과 `pwm` 밝기를 모두 0으로 만든다. 다른 빌드·보드의 상태 LED 표시 방식은 실제 보드에서 확인한다.

## 2. 명령과 응답

명령은 UTF-8 글자 한 줄이고 끝에 `\n`이 붙는다(`send`가 자동으로 붙인다). **명령마다 JSON 한 줄이 응답으로 온다.**

| 명령 | 뜻 | 응답 |
|---|---|---|
| `on N` / `on N N …` | LED 켜기 | `{"result":"ok","ms":"led(s) on"}` |
| `on -1` | 모든 LED 켜기 | 위와 같음 |
| `on` (번호 없음) | — | `{"result":"err","ms":"need pin index"}` |
| `off N` / `off -1` | LED 끄기 / 모두 끄기 | `{"result":"ok","ms":"led(s) off"}` |
| `pwm N V` | LED 밝기 (V는 0~255, N이 `-1`이면 전체) | `{"result":"ok","ms":"pwm set"}` |
| `pwm N 300` | 범위 밖 밝기 | `{"result":"err","ms":"pwm value range 0~255"}` |
| `pwm 9 100` | 범위 밖 번호 | `{"result":"err","ms":"pwm pin index error"}` |
| `dht11` | 온도·습도 읽기 | `{"result":"ok","value":"[24.5,40.0]"}` (온도, 습도) |
| `about` | 보드 정보 | `{"result":"ok","os":"cronos-v1","app":"BLEuno","version":"1.0.5_dev","author":"gbox3d","chipid":…}` |
| `blink` / `stopblk` | 내장 LED 깜빡임 켜기/끄기. 앱이 연결된 동안에는 `blink`를 보내도 깜빡이지 않는다(펌웨어 소스 기준, [1절](#보드-led-색으로-상태-보기)) | `{"result":"ok","ms":"led blink"}` / `{"result":"ok","ms":"led stop blink"}` |
| 그 밖의 글자 | 모르는 명령 | `{"result":"fail","ms":"unknown command"}` |

`result`가 `ok`면 성공, `err`면 명령은 맞지만 값이 틀림, `fail`이면 명령 자체를 모르는 것이다.

### N은 LED 인덱스다

`on 3`의 `3`은 GPIO 번호가 아니라 **LED 인덱스**다. 기존 수업 설정은 LED 4개와 인덱스 `0`, `1`, `2`, `3`을 사용한다.
아래 표는 기존 LED 보드에서 `ledpin = [4,3,1,0]`으로 설정한 경우다. type_m v1 마더보드의 GPIO0은 배터리 감지 입력이므로 이 표를 type_m v1 설정으로 사용하지 않는다.

| 인덱스 | 보드 핀 |
|---|---|
| 0 | GPIO4 |
| 1 | GPIO3 |
| 2 | GPIO1 |
| 3 | GPIO0 |
| -1 | 모두 |

보드는 `on`·`off`의 인덱스가 범위 안인지 검사하지 않는다(펌웨어 소스 기준. `pwm`은 위 명령 표의 `pwm 9 100`처럼 큰 번호에 `pwm pin index error`로 답한다). `on 9`처럼 범위 밖 번호를 보내면 보드가 엉뚱한 메모리를 건드려 어떻게 동작할지 알 수 없다.
그래서 **앱이 보내기 전에 `0~3` 또는 `-1`인지 검사**해야 한다(14주차 1일차 실습).

### 입력 이벤트 (가안)

보드가 스스로 보내는 메시지는 지금 펌웨어에는 없다. 온도·습도는 앱이 `dht11`을 보내고 응답을 받는 방식으로만 읽는다.
보드 버튼 입력은 펌웨어를 확장하면 아래 형식으로 올 예정이며, `FakeBleunoClient`는 이 형식을 10초마다 흉내 낸다.

```json
{"event":"input","index":0,"value":1}
```

## 3. 파일과 넣을 위치

`src/` 안의 9개 파일을 내 프로젝트의 `app › kotlin+java › com.example.smartio` 아래 **새 패키지 `bleuno`**에 복사한다.
파일 첫 줄은 모두 `package com.example.smartio.bleuno`다.
`TcpBleunoClient.kt`는 Wi-Fi 시뮬레이터로 연습할 때만 쓰지만, `Bleuno.kt`가 이 클래스를 부르므로 함께 넣어야 빌드된다. 넣기만 하고 쓰지 않으면 Fake·실보드 동작은 그대로다.

| 파일 | 하는 일 |
|---|---|
| [src/ConnState.kt](src/ConnState.kt) | 연결 상태 문자열 5개 (`연결 안 됨`·`연결 중`·`서비스 확인 중`·`준비됨`·`끊김`) |
| [src/BleunoDevice.kt](src/BleunoDevice.kt) | 찾은 보드 하나 (`name`, `address`, `rssi`) |
| [src/BleunoClient.kt](src/BleunoClient.kt) | 앱이 부르는 함수 목록(인터페이스) |
| [src/RealBleunoClient.kt](src/RealBleunoClient.kt) | 실제 보드용. `BluetoothGatt` 콜백 사슬이 들어 있다 |
| [src/FakeBleunoClient.kt](src/FakeBleunoClient.kt) | 보드 없이 연습용. 시간과 응답을 흉내 낸다 |
| [src/TcpBleunoClient.kt](src/TcpBleunoClient.kt) | PC의 Wi-Fi 시뮬레이터([bleuno-sim](../../tools/bleuno-sim/README.md))에 TCP로 연결한다. 검색은 UDP |
| [src/Bleuno.kt](src/Bleuno.kt) | 앱 전체가 공유하는 `client` 한 개를 만들고 보관한다. `createTcp()`가 `TcpBleunoClient`를 부른다 |
| [src/BleunoMessage.kt](src/BleunoMessage.kt) | 응답 JSON에서 `result`·`ms`·`value`·`event`를 꺼낸다 |
| [src/PermissionHelper.kt](src/PermissionHelper.kt) | 필요한 권한 목록, 블루투스·위치 켜짐 확인 |

Android Studio에서: `com.example.smartio`에서 마우스 오른쪽 › **New › Package** › `bleuno` 입력 › 9개 파일을 그 폴더에 붙여 넣는다.

## 4. Manifest 권한

`app › manifests › AndroidManifest.xml`의 `<manifest …>` 바로 아래, `<application>` 위에 넣는다.

```xml
<uses-feature
    android:name="android.hardware.bluetooth_le"
    android:required="true" />

<!-- Android 12(API 31) 이상 -->
<uses-permission
    android:name="android.permission.BLUETOOTH_SCAN"
    android:usesPermissionFlags="neverForLocation"
    tools:targetApi="s" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />

<!-- Android 11(API 30) 이하 -->
<uses-permission
    android:name="android.permission.BLUETOOTH"
    android:maxSdkVersion="30" />
<uses-permission
    android:name="android.permission.BLUETOOTH_ADMIN"
    android:maxSdkVersion="30" />
<uses-permission
    android:name="android.permission.ACCESS_FINE_LOCATION"
    android:maxSdkVersion="30" />
```

`tools:targetApi`가 빨갛게 표시되면 `<manifest>` 태그에 `xmlns:tools="http://schemas.android.com/tools"`가 있는지 확인한다.
Manifest에 적는 것과 별개로, `BLUETOOTH_SCAN`·`BLUETOOTH_CONNECT`(Android 11 이하는 `ACCESS_FINE_LOCATION`)는 실행 중에 사용자에게 허락을 받아야 한다(10주차 런타임 권한). 목록은 `PermissionHelper.required()`가 준다.

Wi-Fi 시뮬레이터(`Bleuno.createTcp()`)를 쓸 때는 같은 자리에 한 줄을 더한다. 일반 권한이라 실행 중 허락은 필요 없다.

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

## 5. API

### `Bleuno` — 하나만 만들어서 두 화면이 같이 쓴다

| 코드 | 뜻 |
|---|---|
| `Bleuno.create(this, fake = true)` | 가짜 클라이언트를 만들어 `Bleuno.client`에 보관하고 돌려준다 |
| `Bleuno.create(this, fake = false)` | 실제 보드용 클라이언트를 만든다 |
| `Bleuno.createTcp()` | Wi-Fi 시뮬레이터용 클라이언트(`TcpBleunoClient`)를 만들어 `Bleuno.client`에 보관하고 돌려준다. Manifest에 `INTERNET` 권한이 필요하다 |
| `Bleuno.client` | 만들어 둔 클라이언트. `ControlActivity`에서는 `Bleuno.client ?: return`처럼 꺼내 쓴다 |

### `BleunoClient` — 앱이 부르는 함수

| 코드 | 뜻 |
|---|---|
| `client.connectionState` | `StateFlow<String>`. 값은 `ConnState`의 문자열 다섯 개 중 하나. `collect { }`로 화면에 반영한다 |
| `client.isReady` | 지금 `준비됨`이면 `true` |
| `client.startScan(5000, onFound = { device -> … }, onFinished = { … })` | 5초 동안 검색. 보드를 찾을 때마다 `onFound`, 끝나면 `onFinished`. 권한이 없거나 블루투스가 꺼져 있으면 검색 없이 곧바로 `onFinished` |
| `client.stopScan()` | 검색을 바로 멈춘다. `onFinished`도 불린다 |
| `client.connect(device.address)` | 연결 시작. 상태가 `연결 중` → `서비스 확인 중` → `준비됨`으로 바뀐다 |
| `client.disconnect()` | 연결 해제. 상태가 `연결 안 됨`이 된다 |
| `client.send("on 3")` | 명령 한 줄 보내기. 끝의 `\n`은 자동. 여러 개를 연달아 보내도 순서대로 하나씩 나간다 |
| `client.onMessage { json -> … }` | 응답·이벤트를 받는 곳. `onStart`에서 등록하고 `onStop`에서 `onMessage(null)`로 해제한다 |

`onFound`·`onFinished`·`onMessage`·`connectionState`는 모두 **메인 스레드**에서 불리므로 안에서 바로 View를 바꿔도 된다.
`준비됨`이 아닐 때 `send`를 부르면 Logcat에 경고만 남고 아무 일도 하지 않는다.

### `BleunoMessage` — 응답에서 값 꺼내기

| 코드 | 결과 |
|---|---|
| `BleunoMessage.result(json)` | `"ok"`, `"err"`, `"fail"`, 없으면 `null` |
| `BleunoMessage.message(json)` | `"led(s) on"` 같은 `ms` 값 |
| `BleunoMessage.value(json)` | `dht11` 응답의 `"[24.5,40.0]"` |
| `BleunoMessage.event(json)` | 입력 이벤트의 `"input"` |
| `BleunoMessage.isOk(json)` | `result`가 `"ok"`면 `true` |

JSON이 아닌 글자를 넣어도 예외 없이 `null`(또는 `false`)을 돌려준다.

### `PermissionHelper` — 권한과 설정 확인

| 코드 | 결과 |
|---|---|
| `PermissionHelper.required()` | 이 기기에서 요청할 권한 배열. Android 12+는 `BLUETOOTH_SCAN`·`BLUETOOTH_CONNECT`, 그 이하는 `ACCESS_FINE_LOCATION` |
| `PermissionHelper.missing(this)` | 아직 허용되지 않은 권한만 |
| `PermissionHelper.hasAll(this)` | 모두 허용됐으면 `true` |
| `PermissionHelper.isBluetoothEnabled(this)` | 블루투스가 켜져 있으면 `true` |
| `PermissionHelper.isLocationEnabled(this)` | 위치 서비스가 켜져 있으면 `true`. Android 11 이하에서 검색 결과가 0개일 때 확인한다 |

## 6. 사용 예 — 검색 → 연결 → 상태 표시 → 명령 → 응답

```kotlin
// MainActivity (연결 화면)
private lateinit var client: BleunoClient

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    binding = ActivityMainBinding.inflate(layoutInflater)
    setContentView(binding.root)

    client = Bleuno.create(this, fake = true)   // 보드가 있으면 fake = false

    binding.scanButton.setOnClickListener {
        if (!PermissionHelper.hasAll(this)) {
            permissionLauncher.launch(PermissionHelper.required())   // 10주차 틀
            return@setOnClickListener
        }
        deviceNames.clear()
        client.startScan(5000, onFound = { device ->
            deviceNames.add(device.name)
            addresses.add(device.address)
            adapter.notifyDataSetChanged()
        }, onFinished = {
            Toast.makeText(this, "검색 완료: ${deviceNames.size}개", Toast.LENGTH_SHORT).show()
        })
    }

    binding.deviceList.setOnItemClickListener { _, _, position, _ ->
        client.connect(addresses[position])
    }

    lifecycleScope.launch {
        repeatOnLifecycle(Lifecycle.State.STARTED) {
            client.connectionState.collect { state ->
                binding.stateText.text = state
                binding.controlButton.isEnabled = (state == ConnState.READY)
            }
        }
    }
}
```

```kotlin
// ControlActivity (제어 화면) — 같은 client를 Bleuno.client로 꺼내 쓴다
override fun onStart() {
    super.onStart()
    Bleuno.client?.onMessage { json ->
        binding.logText.append("\n← $json")
        if (!BleunoMessage.isOk(json)) {
            Toast.makeText(this, BleunoMessage.message(json) ?: "오류", Toast.LENGTH_SHORT).show()
        }
    }
}

override fun onStop() {
    super.onStop()
    Bleuno.client?.onMessage(null)
}

binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
    val command = if (isChecked) "on 3" else "off 3"
    binding.logText.append("\n→ $command")
    Bleuno.client?.send(command)
}
```

Fake로 위 코드를 실행하면 로그가 이렇게 쌓인다.

```text
→ on 3
← {"result":"ok","ms":"led(s) on"}
→ off 3
← {"result":"ok","ms":"led(s) off"}
```

## 7. FakeBleunoClient의 동작

보드와 실기기가 없어도 앱을 끝까지 만들 수 있게, 실제 보드와 같은 순서로 답한다.

| 부른 것 | 일어나는 일 |
|---|---|
| `startScan(5000, …)` | 1초 뒤 `ESP32_BLE_FAKE1`(주소 `00:11:22:33:44:01`), 2초 뒤 `ESP32_BLE_FAKE2`(`00:11:22:33:44:02`)를 `onFound`로 알림. 5초 뒤 `onFinished` |
| `connect(주소)` | 바로 `연결 중` → 1초 뒤 `서비스 확인 중` → 다시 1초 뒤 `준비됨` |
| `send("on 0")` | 300ms 뒤 `{"result":"ok","ms":"led(s) on"}` |
| `send("on")` | 300ms 뒤 `{"result":"err","ms":"need pin index"}` |
| `send("pwm 0 300")` | 300ms 뒤 `{"result":"err","ms":"pwm value range 0~255"}` |
| `send("dht11")` | 300ms 뒤 `{"result":"ok","value":"[24.5,40.0]"}` — 부를 때마다 `[25.0,41.0]`, `[25.5,42.0]`로 조금씩 바뀐다 |
| `send("hello")` | 300ms 뒤 `{"result":"fail","ms":"unknown command"}` |
| `준비됨` 상태 유지 | 10초마다 `{"event":"input","index":0,"value":1}` (value는 0/1 번갈아) |
| `disconnect()` | 바로 `연결 안 됨` |
| `(client as FakeBleunoClient).simulateLost()` | 보드 전원이 꺼진 것처럼 `끊김` (14주차 재연결 연습용) |

Fake는 실제 검사 없이 응답만 흉내 내므로, `on 9`를 보내도 `ok`가 돌아온다. 인덱스 검사는 앱이 한다.

## 8. Logcat으로 콜백 사슬 보기

`RealBleunoClient`는 모든 콜백을 태그 `BLE`로 남긴다. Logcat 필터에 `package:mine tag:BLE`를 넣으면 이런 순서가 보인다.

```text
startScan: 5000ms 동안 "ESP32_BLE"로 시작하는 기기 검색
onScanResult: ESP32_BLE7C9EBF 84:F7:03:xx:xx:xx rssi=-48
scan timeout (5000ms)
stopScan: 찾은 기기 1개
connectGatt(84:F7:03:xx:xx:xx, autoConnect=false)
onConnectionStateChange: status=0 newState=2
STATE_CONNECTED → requestMtu(185)
onMtuChanged: mtu=185 status=0 → discoverServices()
onServicesDiscovered: status=0
characteristic 확보: f6aa83ca-de53-46b4-bdea-28a7cb57942e
writeDescriptor(CCCD, ENABLE_NOTIFICATION_VALUE)
onDescriptorWrite: status=0 → 준비됨
send: 큐에 추가 "on 3" (대기 1개)
writeCharacteristic("on 3") 호출 결과=true
onCharacteristicWrite: status=0
onCharacteristicChanged: {"result":"ok","ms":"led(s) on"}
```

Fake도 같은 태그로 `(가짜)`가 붙은 로그를 남기므로, 앱 문제인지 보드 문제인지 로그로 나눌 수 있다.
`TcpBleunoClient`는 태그 `TCP`를 쓴다. 필터 `package:mine tag:TCP`에서 `connect:` → `connected:` → `첫 줄 받음 → 준비됨` 순서가 보인다.

## 9. 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 검색해도 목록이 비어 있다 | 보드 LED가 파랑 깜빡임인가(다른 폰에 이미 연결되면 검색에 안 잡힌다) · `PermissionHelper.hasAll`이 `true`인가 · 블루투스가 켜져 있는가 · Android 11 이하면 위치 서비스가 켜져 있는가 |
| Logcat에 `startScan: 권한이 없어 무시함` | 런타임 권한을 아직 허용하지 않았다. 검색은 시작하지 않고 `onFinished`만 곧바로 불린다. `permissionLauncher.launch(PermissionHelper.required())` |
| 상태가 `연결 중`에서 멈춘다 | 보드 전원·거리 확인. 10초 넘게 그대로면 `disconnect()` 후 다시 시도(14주차 timeout) |
| 상태가 갑자기 `끊김` | 보드 전원이 꺼졌거나 멀어졌다. `connect(lastAddress)`로 재연결 |
| `send`를 불렀는데 응답이 없다 | `client.isReady`가 `true`인가. `onMessage`를 `onStart`에서 등록했는가 |
| `Unresolved reference 'bleuno'.` (`MainActivity.kt`·`ControlActivity.kt`의 `import` 줄) | 파일이 `com.example.smartio.bleuno` 패키지 폴더에 있는지, 첫 줄 `package`가 맞는지 |
| `Unresolved reference 'TcpBleunoClient'.` (`Bleuno.kt`) | `Bleuno.kt`만 새 판으로 바꾸고 `TcpBleunoClient.kt`를 넣지 않았다. 두 파일은 함께 넣는다 |
| Wi-Fi 시뮬레이터에 검색·연결이 안 된다 | 앱 쪽은 [Wi-Fi 시뮬레이터 실습의 막혔을 때](../iot_sim/lab.md#막혔을-때), 시뮬레이터 쪽은 [bleuno-sim README의 10. 막혔을 때](../../tools/bleuno-sim/README.md#10-막혔을-때)를 본다 |

## 10. 보드 없이 Wi-Fi 시뮬레이터로 연습하기

보드도 실기기도 없으면 PC에서 BLEuno 시뮬레이터를 돌리고, 앱이 Wi-Fi(TCP)로 연결해 실제로 명령·응답을 주고받을 수 있다.
시뮬레이터는 Python 3.10 이상과 pygame-ce로 실행하는 프로그램 하나이고, 별도 창에 LED 4개·온습도 슬라이더·[입력 버튼]·[연결 끊기]가 있다.

| 문서 | 내용 |
|---|---|
| [tools/bleuno-sim/README.md](../../tools/bleuno-sim/README.md) | 시뮬레이터 실행 방법, 화면, 포트(명령 TCP 8266 · 검색 UDP 8267 · HTTP API 8080), 방화벽, 막혔을 때 |
| [iot_sim/lab.md](../iot_sim/lab.md) | 90분 실습. 12주차 2일차 이후 `SmartIO`에서 네 곳(두 파일, `INTERNET`, `useTcp`, 주소 직접 입력)을 바꿔 연결한다 |

클라이언트를 고르는 곳은 아래 한 줄이다. 검색·연결·명령 코드(`startScan`·`connect`·`send`·`onMessage`)는 주차 코드 그대로다.

```kotlin
client = Bleuno.client ?: if (useTcp) Bleuno.createTcp() else Bleuno.create(this, useFake)
```

- 명령과 응답은 2절 표와 같다. 다른 점은 `about`의 `app`이 `BLEuno-SIM`, `version`이 `1.0.5_sim`이라는 것, 연결 직후 `hello` 줄이 먼저 온다는 것이다. 그 밖의 차이(`dht11`은 화면 슬라이더 값, 입력 이벤트는 화면의 [입력 버튼]을 누를 때만, 공백만 있는 줄은 `need command`)는 [bleuno-sim README 1절 '시뮬레이터가 대신하는 것'](../../tools/bleuno-sim/README.md#1-시뮬레이터가-대신하는-것)와 [8절 '명령과 응답'](../../tools/bleuno-sim/README.md#8-명령과-응답)에 있다.
- 앱이 연결되거나 끊길 때 LED를 모두 끄는 것과 빈 줄(길이 0)에 답하지 않는 것은 보드와 같다. 보드 쪽은 펌웨어 소스로 확인한 것이다([1절](#보드-led-색으로-상태-보기), [아래 표의 `send("")` 줄](#tcpbleunoclient의-동작-wi-fi-시뮬레이터)).
- 에뮬레이터에서는 주소 `10.0.2.2:8266`으로 연결한다. 실기기는 PC와 같은 Wi-Fi에서 `PC의 IP:8266`을 쓴다. 실기기와 학교 Wi-Fi에서는 아직 확인하지 못했다.
- 주차 실습의 관찰표·캡처·제출은 Fake 또는 실보드 기준이다. 시뮬레이터 실습은 그것을 대신하지 않는다.

### TcpBleunoClient의 동작 (Wi-Fi 시뮬레이터)

PC에서 돌리는 [bleuno-sim](../../tools/bleuno-sim/README.md)과 소켓으로 이야기한다. 앱이 부르는 함수와 상태 문자열은 Real·Fake와 같다.
아래 시간과 문구는 Android 에뮬레이터(API 31)와 같은 PC의 시뮬레이터로 확인한 것이다. 실기기는 확인하지 못했다.

| 부른 것 / 일 | 일어나는 일 |
|---|---|
| `startScan(5000, …)` | UDP로 `bleuno?`를 `255.255.255.255:8267`과 `10.0.2.2:8267`(에뮬레이터에서 본 PC) 두 곳에 보낸다. 답한 시뮬레이터마다 `onFound`(이름, 주소 `"IP:포트"`, `rssi` 0). 포트는 시뮬레이터가 답에 넣은 명령 포트로, 보통 8266이다. 같은 주소는 한 번만. 5초 뒤 `onFinished`. 권한·블루투스는 확인하지 않는다 |
| `connect("10.0.2.2:8266")` | 바로 `연결 중`. 포트를 빼면 8266. 연결되면 `서비스 확인 중` |
| 첫 줄(`hello`) | 연결된 뒤 첫 줄을 받으면 `준비됨`. 시뮬레이터는 연결 직후 `{"event":"hello",…}` 줄을 먼저 보내고, 이 hello 줄은 `onMessage`로 넘기지 않는다(첫 줄이 hello가 아니면 그 줄은 넘긴다) |
| `send("on 0")` | 끝에 언제나 `\n`을 붙여 부른 순서대로 쓴다. 응답 JSON 한 줄이 `onMessage`로 온다. `준비됨`이 아니면 Logcat 경고만 남긴다 |
| `send("")` | 거르지 않고 빈 줄 하나(`\n`)를 보낸다(`RealBleunoClient`와 같다). 시뮬레이터는 길이 0인 줄에 답하지 않는다. 보드 펌웨어도 길이 0인 명령은 건너뛰고 답하지 않는다(`ble.cpp`의 `onWrite`. 펌웨어 소스로 확인했고 실제 보드로는 확인하지 못했다). `FakeBleunoClient`는 `send()`에서 빈 줄을 걸러 낸다. 그래서 셋 다 응답이 오지 않는다. 공백만 있는 줄(`send(" ")`)은 다르다. 시뮬레이터는 `{"result":"fail","ms":"need command"}`, 보드는 `{"result":"fail","ms":"unknown command"}`(펌웨어 소스 기준)로 답하고, Fake는 걸러 내 답하지 않는다 |
| 시간 제한 | IP 주소로 연결할 때 3초 안에 연결되지 않으면 `끊김`. 그 전에 연결 오류가 오면 그때 `끊김`이 된다(예: 시뮬레이터가 꺼져 있으면 `ECONNREFUSED`, 없는 IP면 `EHOSTUNREACH`). 연결된 뒤 3초 안에 첫 줄이 오지 않아도 `끊김`(다른 포트, 예: HTTP API `:8080`). 주소에 이름(예: `abc`)을 넣으면 이름을 IP로 바꾸는 동안에는 이 3초 제한이 걸리지 않는다. 주소에는 IP를 쓴다 |
| 잘못된 주소 | 포트가 1~65535 밖이거나 숫자가 아니면, 또는 `:` 앞의 IP가 비면(예: `:8266`) 연결하지 않고 `연결 중`을 거쳐 곧바로 `끊김`(이미 `끊김`이어도 다시 알린다). IP가 빈 주소는 기기 자신(localhost)을 가리키므로 막는다. 지금 연결이 있으면 먼저 닫는다. `RealBleunoClient`는 잘못된 주소를 받으면 Logcat 경고만 남기고 지금 연결과 상태를 그대로 둔다. 없는 이름(`abc`)은 `UnknownHostException` 뒤 `끊김`. 앱은 멈추지 않는다 |
| 시뮬레이터 [연결 끊기]·Ctrl+C 종료 | `끊김`. Logcat은 `EOF: 상대가 연결을 닫음` → `connection ended → 끊김`. 명령을 쓰던 중이면 그 사이에 `write 오류: java.net.SocketException: Socket closed → 끊김`이 한 줄 더 찍힐 수 있지만 `끊김`은 한 번이다. 시뮬레이터 프로세스가 강제로 끝나면 `connect/read 오류: java.net.SocketException: Connection reset`. `connect(lastAddress)`로 재연결한다 |
| `disconnect()` | 바로 `연결 안 됨`(`끊김`이 아니다) |
| 입력 이벤트 | 시뮬레이터가 보낸 `{"event":"input",…}` 줄을 그대로 `onMessage`로 넘긴다. 시뮬레이터는 화면의 [입력 버튼]을 누를 때만 보낸다(Fake는 `준비됨`이면 10초마다). Fake·보드와의 차이는 [Wi-Fi 시뮬레이터 실습의 '시뮬레이터와 Fake·보드의 차이'](../iot_sim/lab.md#시뮬레이터와-fake보드의-차이)에 있다 |

12~15주차 예제 화면으로는 빈 줄이나 공백만 있는 줄을 보낼 수 없다. 예제가 `send()`에 넘기는 글자는 `on 번호`·`off 번호`·`off -1`·`pwm 0 값`·`dht11`뿐이고, LED 번호 칸이 비면 보내기 전에 Toast `LED 번호를 입력하세요`로 막는다(12~15주차 예제 코드 기준).
시뮬레이터도 Fake(7절)와 같이 범위 밖 번호(`on 9` 등)를 `ok`로 답하고 무시한다. 인덱스 검사는 앱이 한다.

## 공식 참고 자료

- [Bluetooth Low Energy 개요 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/ble-overview)
- [BLE 기기 찾기 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/find-ble-devices)
- [GATT 서버에 연결 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
- [블루투스 권한 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
- [bleuno 펌웨어 — GitHub](https://github.com/gbox3d/bleuno)
