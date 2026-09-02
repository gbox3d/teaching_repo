# 3주차 예제 스니펫 — Lifecycle Trace와 Activity Result

## 사용 범위

이 문서는 대표 코드 조각을 제공하며 **빌드 가능한 Gradle 프로젝트는 포함하지 않는다**. 강의자 기준 프로젝트에 Activity, layout, Manifest 선언을 직접 추가하고 package/import/resource를 맞춘다.

## 파일명과 문맥

| 파일명 예시 | 위치/역할 |
|---|---|
| `MainActivity.kt` | lifecycle 로그, saved state, 결과 launcher |
| `DeviceDetailActivity.kt` | extra 검증, 별칭 저장·취소 |
| `activity_main.xml` | 탭 횟수, 상세 화면 버튼 |
| `activity_device_detail.xml` | 장치명, 별칭 EditText, 저장 버튼 |
| `AndroidManifest.xml` | 두 Activity 선언 |

## lifecycle trace 핵심

```kotlin
private const val TAG = "LifecycleTrace"
private const val KEY_TAPS = "tap_count"

private var tapCount = 0
private val instanceId = System.identityHashCode(this)

private fun trace(event: String) {
    Log.d(TAG, "id=$instanceId event=$event taps=$tapCount")
}

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
    tapCount = savedInstanceState?.getInt(KEY_TAPS) ?: 0
    trace("onCreate")
}

override fun onStart() {
    super.onStart()
    trace("onStart")
}

override fun onResume() {
    super.onResume()
    trace("onResume")
}

override fun onPause() {
    trace("onPause")
    super.onPause()
}

override fun onStop() {
    trace("onStop")
    super.onStop()
}

override fun onDestroy() {
    trace("onDestroy")
    super.onDestroy()
}

override fun onSaveInstanceState(outState: Bundle) {
    outState.putInt(KEY_TAPS, tapCount)
    super.onSaveInstanceState(outState)
}
```

예상 관찰:

- 최초 실행은 일반적으로 create→start→resume 흐름을 보인다.
- 회전 시 이전 instance id와 새 instance id를 구분할 수 있다.
- callback 세부 순서는 현재 환경의 실제 로그로 기록한다.
- `onDestroy()`가 모든 process 종료에서 호출된다고 가정하지 않는다.

## 결과 launcher 핵심

```kotlin
const val EXTRA_DEVICE_NAME = "device_name"
const val EXTRA_ALIAS = "device_alias"

private val editDevice = registerForActivityResult(
    ActivityResultContracts.StartActivityForResult()
) { result ->
    if (result.resultCode != Activity.RESULT_OK) return@registerForActivityResult

    val newAlias = result.data
        ?.getStringExtra(EXTRA_ALIAS)
        ?.trim()
        ?.takeIf { it.isNotEmpty() }

    if (newAlias != null) {
        alias = newAlias
        render()
    }
}

private fun openDetail() {
    val intent = Intent(this, DeviceDetailActivity::class.java)
        .putExtra(EXTRA_DEVICE_NAME, "Demo Mock Device")
    editDevice.launch(intent)
}
```

## `DeviceDetailActivity.kt` 핵심

```kotlin
val deviceName = intent.getStringExtra(EXTRA_DEVICE_NAME)
    ?.trim()
    ?.takeIf { it.isNotEmpty() }

if (deviceName == null) {
    setResult(Activity.RESULT_CANCELED)
    finish()
    return
}

saveButton.setOnClickListener {
    val alias = aliasInput.text.toString().trim()
    if (alias.isEmpty()) {
        aliasInput.error = getString(R.string.alias_required)
        return@setOnClickListener
    }

    val data = Intent().putExtra(EXTRA_ALIAS, alias)
    setResult(Activity.RESULT_OK, data)
    finish()
}
```

위 View 변수는 `onCreate()`에서 `findViewById`로 찾았다는 문맥이다.

## Manifest 핵심

```xml
<application ...>
    <activity
        android:name=".DeviceDetailActivity"
        android:exported="false" />
    <activity
        android:name=".MainActivity"
        android:exported="true">
        <!-- 기준 프로젝트의 launcher intent-filter 유지 -->
    </activity>
</application>
```

## 예상 결과 매트릭스

| 조건 | 예상 관찰 |
|---|---|
| 유효 별칭 저장 | Main의 alias 갱신 |
| 공백 저장 | Detail 입력 오류, 화면 유지 |
| Back | canceled, 기존 alias 유지 |
| 장치명 extra 누락 | crash 없이 canceled 종료 |
| 회전 | 저장한 탭 횟수 유지 |

## 공식 참고 자료

- [Activity lifecycle — Android Developers](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [Saving UI states — Android Developers](https://developer.android.com/topic/libraries/architecture/saving-states)
- [Activity result APIs — Android Developers](https://developer.android.com/training/basics/intents/result)
