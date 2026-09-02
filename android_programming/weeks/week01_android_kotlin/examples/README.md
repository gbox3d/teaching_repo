# 1주차 예제 스니펫 — Device Info

## 사용 범위

이 폴더에는 복사 가능한 대표 스니펫만 있으며 **빌드 가능한 Gradle 프로젝트는 포함되어 있지 않다**. 강의자가 제공한 Kotlin + XML Views 기준 프로젝트에서 package 이름, import, resource 이름을 확인한 뒤 필요한 부분만 옮긴다.

## 파일명과 문맥

| 파일명 예시 | 프로젝트 안의 위치/역할 |
|---|---|
| `MainActivity.kt` | `app/src/main/java/<package>/`, 화면 생성·클릭 처리 |
| `DeviceSummary.kt` | 같은 package, 단말 표시 데이터와 순수 함수 |
| `activity_main.xml` | `app/src/main/res/layout/`, 정보와 버튼 View |
| `strings.xml` | `app/src/main/res/values/`, 사용자 표시 문자열 |

## `DeviceSummary.kt`

```kotlin
data class DeviceSummary(
    val manufacturer: String,
    val model: String,
    val apiLevel: Int,
)

fun normalizeBuildValue(raw: String?, unknownSentinel: String): String? =
    raw?.trim()?.takeIf {
        it.isNotEmpty() && !it.equals(unknownSentinel, ignoreCase = true)
    }
```

예상 관찰:

- `normalizeBuildValue(" Pixel ", "unknown")`은 `Pixel`이다.
- 공백, `null`, 플랫폼 sentinel인 `"unknown"`은 모두 `null`이다.
- 함수는 Android 객체와 사용자 표시 문구 없이 입력 정규화만 담당한다.

## `activity_main.xml` 핵심

부모 layout의 종류와 namespace 선언은 기준 프로젝트를 따른다.

```xml
<TextView
    android:id="@+id/deviceSummary"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:text="@string/device_unknown" />

<TextView
    android:id="@+id/refreshCount"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="@string/refresh_count_initial" />

<Button
    android:id="@+id/refreshButton"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="@string/refresh" />
```

## `MainActivity.kt` 핵심

필요한 Android class import는 IDE의 자동 import로 확인한다.

```kotlin
private const val TAG = "DeviceInfo"

class MainActivity : AppCompatActivity() {
    private var refreshCount = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val summaryView = findViewById<TextView>(R.id.deviceSummary)
        val countView = findViewById<TextView>(R.id.refreshCount)
        val refreshButton = findViewById<Button>(R.id.refreshButton)

        val unknownText = getString(R.string.value_unknown)
        val summary = DeviceSummary(
            manufacturer = normalizeBuildValue(Build.MANUFACTURER, Build.UNKNOWN)
                ?: unknownText,
            model = normalizeBuildValue(Build.MODEL, Build.UNKNOWN)
                ?: unknownText,
            apiLevel = Build.VERSION.SDK_INT,
        )
        summaryView.text = getString(
            R.string.device_summary_format,
            summary.manufacturer,
            summary.model,
            summary.apiLevel,
        )

        refreshButton.setOnClickListener {
            refreshCount += 1
            countView.text = getString(R.string.refresh_count, refreshCount)
            Log.d(TAG, "refreshCount=$refreshCount")
        }
        Log.d(TAG, "onCreate: screen ready")
    }
}
```

예상 관찰:

1. 최초 화면에는 단말 요약과 0회 문구가 보인다.
2. 버튼을 두 번 누르면 화면과 마지막 로그 값이 2다.
3. 화면 회전 시 Activity가 다시 만들어지면 현재 구현의 필드 값은 초기화될 수 있다. 상태 보존은 3주차에 다룬다.

## `strings.xml` 핵심

```xml
<resources>
    <string name="app_name">Smart I/O Controller</string>
    <string name="device_unknown">장치 정보를 불러오는 중</string>
    <string name="value_unknown">알 수 없음</string>
    <string name="device_summary_format">%1$s %2$s · API %3$d</string>
    <string name="refresh">새로고침</string>
    <string name="refresh_count_initial">새로고침 0회</string>
    <string name="refresh_count">새로고침 %1$d회</string>
</resources>
```

## 안전한 변형

- 실제 `Build` 값 대신 `DeviceSummary("Demo", "Emulator", 0)` 같은 가짜 입력으로 표시 형식을 시험한다.
- 단말 고유 ID, 계정, 전화번호, 위치는 예제 목적에 필요하지 않으므로 읽거나 로그로 남기지 않는다.

## 공식 참고 자료

- [Android app resources — Android Developers](https://developer.android.com/guide/topics/resources/providing-resources)
- [Logcat — Android Developers](https://developer.android.com/studio/debug/logcat)
- [Kotlin null safety — Kotlin Documentation](https://kotlinlang.org/docs/null-safety.html)
