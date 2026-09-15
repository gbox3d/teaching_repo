# 4주차 예제 — ViewBinding·EditText·Switch·두 번째 Activity

Android Studio에서 **Empty Views Activity**로 만든 `SmartIO` 프로젝트(package `com.example.smartio`)를 기준으로 한다.
아래 파일은 해당 날짜의 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.
장치 이름 `ESP32_BLE_1`, 핀 번호 `3`은 연습용 값이다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 |
|---|---|
| [day1/build.gradle.kts](day1/build.gradle.kts) | `Gradle Scripts › build.gradle.kts (Module :app)` — `buildFeatures { viewBinding = true }`와 `dependencies`의 네 줄만 내 파일에 넣는다 |
| [day1/strings.xml](day1/strings.xml) | `app › res › values › strings.xml` |
| [day1/activity_main.xml](day1/activity_main.xml) | `app › res › layout › activity_main.xml` |
| [day1/MainActivity.kt](day1/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` |
| [day2/MainActivity.kt](day2/MainActivity.kt) | 같은 위치. [연결]이 `ControlActivity`로 이동한다 |
| [day2/ControlActivity.kt](day2/ControlActivity.kt) | `app › kotlin+java › com.example.smartio › ControlActivity.kt` — New › Activity로 만든 파일을 바꾼다 |
| [day2/activity_control.xml](day2/activity_control.xml) | `app › res › layout › activity_control.xml` |
| [day2/strings.xml](day2/strings.xml) | `app › res › values › strings.xml` — 2일차에 다섯 줄이 늘었다 |
| [day2/AndroidManifest.xml](day2/AndroidManifest.xml) | `app › manifests › AndroidManifest.xml` — `<activity android:name=".ControlActivity" …/>` 줄이 있는지만 확인한다 |
| [day2/res/values/themes.xml](day2/res/values/themes.xml) | 템플릿이 만든 것과 같다. 예제를 단독으로 빌드하기 위해 둔 파일이며 내 프로젝트에서는 고치지 않는다 |

`day2/activity_main.xml`과 `day2/build.gradle.kts`는 1일차와 같다.
`*.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.

## 1. ViewBinding — findViewById 없이 View 부르기

```kotlin
    buildFeatures {
        viewBinding = true
    }
```

```kotlin
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets -> ... }
        ...
        binding.connectButton.setOnClickListener { ... }
    }
```

| 코드 | 뜻 |
|---|---|
| `viewBinding = true` | 레이아웃마다 클래스를 만든다. `activity_main.xml` → `ActivityMainBinding` |
| `lateinit var binding` | 틀. "값은 `onCreate()`에서 넣는다"는 표시 |
| `inflate(layoutInflater)` + `setContentView(binding.root)` | 틀. 2주차의 `setContentView(R.layout.activity_main)` 대신 쓴다 |
| `binding.connectButton` | XML의 `@+id/connectButton`. `findViewById<Button>(R.id.connectButton)`과 같다 |

## 2. strings.xml — 글자는 한곳에

```xml
<resources>
    <string name="app_name">Smart I/O Controller</string>
    <string name="connect">연결</string>
</resources>
```

```xml
<Button android:text="@string/connect" ... />
```

- XML에서는 `@string/이름`으로 부른다. 직접 쓴 한글에 뜨는 노란 `Hardcoded string` 경고가 사라진다.
- 코드에서 만드는 문장(`"연결: $name"`)은 그대로 써도 된다.

## 3. EditText — 입력 읽기

```xml
<EditText
    android:id="@+id/deviceNameEdit"
    android:layout_width="240dp"
    android:layout_height="wrap_content"
    android:hint="@string/device_name_hint"
    android:inputType="text" />
```

```kotlin
val name = binding.deviceNameEdit.text.toString()
if (name.isEmpty()) {
    Toast.makeText(this, "장치 이름을 입력하세요", Toast.LENGTH_SHORT).show()
} else {
    Toast.makeText(this, "연결: $name", Toast.LENGTH_SHORT).show()
}
```

- `hint`: 비었을 때 흐리게 보이는 안내. `inputType`: `text`는 글자 키보드, `number`는 숫자 키패드.
- `.text.toString()`: 글자 상자에서 String을 꺼낸다. `.toString()`이 없으면 `==` 비교에서 오류가 난다.

## 4. Switch — 켜짐·꺼짐

```kotlin
binding.autoSwitch.setOnCheckedChangeListener { _, isChecked ->
    if (isChecked) {
        Toast.makeText(this, "자동 연결 켜짐", Toast.LENGTH_SHORT).show()
    } else {
        Toast.makeText(this, "자동 연결 꺼짐", Toast.LENGTH_SHORT).show()
    }
}
```

- `{ _, isChecked -> }`는 틀이다. 첫째(스위치 자신)는 쓰지 않아 `_`, 둘째 `isChecked`는 켜졌으면 `true`.
- 켤 때와 끌 때 모두 실행되므로 `if (isChecked)`로 나눈다.

## 5. 1일차 완성 — 연결 화면

[day1](day1/)의 네 파일을 넣고 실행한 결과:

```text
Smart I/O Controller
[ 장치 이름          ]
자동 연결        (O)
      [ 연결 ]
```

| 할 일 | Toast |
|---|---|
| 빈 채로 [연결] | `장치 이름을 입력하세요` |
| `ESP32_BLE_1` 입력 후 [연결] | `연결: ESP32_BLE_1` |
| 스위치 켜기 / 끄기 | `자동 연결 켜짐` / `자동 연결 꺼짐` |

## 6. 두 번째 Activity — Intent로 이동하고 값 넘기기

```xml
<activity
    android:name=".ControlActivity"
    android:exported="false" />
```

```kotlin
// 보내는 쪽 (MainActivity)
val intent = Intent(this, ControlActivity::class.java)
intent.putExtra("name", name)
startActivity(intent)
```

```kotlin
// 받는 쪽 (ControlActivity)
val name = intent.getStringExtra("name") ?: ""
binding.deviceText.text = "장치: $name"

binding.backButton.setOnClickListener {
    finish()
}
```

| 코드 | 뜻 |
|---|---|
| Manifest의 `<activity>` | Activity는 등록되어야 열 수 있다. New › Activity로 만들면 자동으로 생긴다 |
| `Intent(this, ControlActivity::class.java)` | 명시적 Intent. "이 화면에서 ControlActivity로" |
| `putExtra("name", name)` / `getStringExtra("name") ?: ""` | 이름표 `"name"`으로 넣고 꺼낸다. 없으면 `null`이므로 `?: ""` |
| `startActivity(intent)` / `finish()` | 다음 화면을 연다 / 지금 화면을 닫고 돌아간다 |

## 7. 2일차 완성 — 제어 화면과 명령 로그

[day2](day2/)의 파일을 넣고 `ESP32_BLE_1`을 입력해 [연결]을 누른 뒤, 핀 번호 `3`을 넣고 LED 스위치를 켜기 → 끄기 → 켜기 한 결과:

```text
장치: ESP32_BLE_1
[ 3        ]
LED        (O)
명령 로그
on 3
off 3
on 3
        [ 뒤로 ]
```

- 핀 번호가 비어 있을 때 스위치를 켜면 Toast `핀 번호를 입력하세요`만 뜨고 로그는 그대로다.
- `binding.logText.append("on $pin\n")`: `.text =`는 통째로 바꾸고 `append`는 뒤에 덧붙인다.
- [뒤로]로 돌아간 뒤 다시 [연결]하면 제어 화면이 새로 열려 로그가 비어 있다. 5주차 이후 이 흐름에 검색·연결 시간이 붙는다.

## 공식 참고 자료

- [뷰 결합(ViewBinding) — Android Developers](https://developer.android.com/topic/libraries/view-binding)
- [문자열 리소스 — Android Developers](https://developer.android.com/guide/topics/resources/string-resource)
- [다른 액티비티 시작하기 — Android Developers](https://developer.android.com/training/basics/firstapp/starting-activity)
