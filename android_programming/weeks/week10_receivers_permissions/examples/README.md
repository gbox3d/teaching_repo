# 10주차 Receiver·권한 예제 조각

다음은 강의자 Kotlin/XML Views 기준 프로젝트에 복사해 관찰하는 조각이다. **독립적으로 빌드 가능한 Gradle 프로젝트가 아니며**, package/action 이름, SDK·AndroidX 버전, course target/min SDK는 학기 기준표의 `TBD`를 따른다.

## 1. app-private context receiver

```kotlin
private const val ACTION_STATUS = "TBD.course.package.ACTION_STATUS"
private const val EXTRA_CODE = "TBD.course.package.EXTRA_CODE"

private val statusReceiver = object : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != ACTION_STATUS) return
        val code = intent.getIntExtra(EXTRA_CODE, -1)
        if (code !in 0..2) return
        viewModel.onPrivateStatus(code)
    }
}

override fun onStart() {
    super.onStart()
    ContextCompat.registerReceiver(
        requireContext(),
        statusReceiver,
        IntentFilter(ACTION_STATUS),
        ContextCompat.RECEIVER_NOT_EXPORTED
    )
}

override fun onStop() {
    requireContext().unregisterReceiver(statusReceiver)
    super.onStop()
}
```

보내는 쪽:

```kotlin
val intent = Intent(ACTION_STATUS)
    .setPackage(requireContext().packageName)
    .putExtra(EXTRA_CODE, 1)
requireContext().sendBroadcast(intent)
```

예상 관찰: 화면의 등록 범위 안에서 valid code만 한 번 처리된다. action/package/action namespace의 `TBD`는 실제 course package 확정 뒤 교체한다.

## 2. target/device별 수업용 BLE 권한 후보

```kotlin
fun requiredBleRuntimePermissions(context: Context): Array<String> {
    val deviceApi = Build.VERSION.SDK_INT
    val targetApi = context.applicationInfo.targetSdkVersion
    val targetsAndroid12Plus = targetApi >= Build.VERSION_CODES.S

    return when {
        deviceApi >= Build.VERSION_CODES.S && targetsAndroid12Plus -> arrayOf(
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.BLUETOOTH_CONNECT
        )
        deviceApi >= Build.VERSION_CODES.M -> arrayOf(
            Manifest.permission.ACCESS_FINE_LOCATION
        )
        else -> emptyArray()
    }
}
```

예상 관찰:

- target 31+·device 31+ 조합은 scan/connect runtime 권한을 반환한다.
- legacy device 경로는 scan에 필요한 위치 runtime 경로를 반환한다.
- 이 helper만으로 Manifest 선언·BLE feature availability·location 파생 정책이 해결되지는 않는다.
- course target SDK를 코드 문서에서 임의로 고정하지 않는다.

## 3. 여러 runtime 권한 요청

```kotlin
private val permissionHistory by lazy {
    requireContext().getSharedPreferences(
        "ble_permission_history",
        Context.MODE_PRIVATE,
    )
}

private fun wasRequestedBefore(permission: String): Boolean =
    permissionHistory.getBoolean(permission, false)

private fun markRequested(permissions: List<String>) {
    val editor = permissionHistory.edit()
    permissions.forEach { editor.putBoolean(it, true) }
    editor.apply()
}

private fun currentMissingBlePermissions(): List<String> =
    requiredBleRuntimePermissions(requireContext()).filter { permission ->
        ContextCompat.checkSelfPermission(requireContext(), permission) !=
            PackageManager.PERMISSION_GRANTED
    }

private fun dialogBlockedPermissions(missing: List<String>): List<String> =
    missing.filter { permission ->
        wasRequestedBefore(permission) &&
            !shouldShowRequestPermissionRationale(permission)
    }

private val permissionLauncher = registerForActivityResult(
    ActivityResultContracts.RequestMultiplePermissions()
) { results ->
    val stillMissing = requiredBleRuntimePermissions(requireContext())
        .filter { permission ->
            results[permission] != true &&
                ContextCompat.checkSelfPermission(requireContext(), permission) !=
                PackageManager.PERMISSION_GRANTED
        }

    when {
        stillMissing.isEmpty() -> viewModel.onBlePermissionReady()
        dialogBlockedPermissions(stillMissing).isNotEmpty() ->
            viewModel.onBlePermissionSettingsRequired()
        stillMissing.any { shouldShowRequestPermissionRationale(it) } ->
            viewModel.onBlePermissionRationaleNeeded()
        else -> viewModel.onBlePermissionSettingsRequired()
    }
}

private fun launchMissingPermissions(missing: List<String>) {
    if (missing.isEmpty()) {
        viewModel.onBlePermissionReady()
        return
    }
    markRequested(missing)
    permissionLauncher.launch(missing.toTypedArray())
}

private fun routeBlePermissionUi() {
    val missing = currentMissingBlePermissions()
    when {
        missing.isEmpty() -> viewModel.onBlePermissionReady()
        dialogBlockedPermissions(missing).isNotEmpty() ->
            viewModel.onBlePermissionSettingsRequired()
        missing.any { shouldShowRequestPermissionRationale(it) } ->
            viewModel.onBlePermissionRationaleNeeded()
        else -> launchMissingPermissions(missing) // 최초 요청
    }
}

private fun onFindDeviceClick() {
    val hasBle = requireContext().packageManager.hasSystemFeature(
        PackageManager.FEATURE_BLUETOOTH_LE
    )
    if (!hasBle) {
        viewModel.onBleUnavailable()
        return
    }
    routeBlePermissionUi() // 실제 scan은 12주차
}

private fun onRationaleContinueClick() {
    launchMissingPermissions(currentMissingBlePermissions())
}

private fun onOpenAppSettingsClick() {
    val uri = Uri.fromParts("package", requireContext().packageName, null)
    startActivity(Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, uri))
}
```

예상 관찰:

- BLE feature가 없으면 dialog 없이 unavailable이 되고, 사용자가 “장치 찾기”를 선택했을 때만 missing 권한을 처리한다.
- 최초 요청은 앱의 요청 이력이 없고 현재 rationale도 필요하지 않을 때 시작한다. `shouldShowRequestPermissionRationale() == false` 하나만으로 최초 요청과 재요청 불가를 구분하지 않는다.
- rationale이 필요하면 이유·기능 영향·계속/취소를 보여 준다. 계속 버튼은 `onRationaleContinueClick()`, 취소 버튼은 BLE 기능만 비활성화하는 상태로 연결한다.
- 이전에 요청한 권한인데 현재 rationale을 표시할 수 없으면 dialog를 반복하지 않고 설정 안내와 취소 경로를 보여 준다. 설정에서 돌아온 뒤 `routeBlePermissionUi()`로 현재 상태를 다시 계산한다.
- launcher callback은 전달받은 Map만 믿지 않는다. Map에 없는 기존 grant와 현재 revoke 상태를 `checkSelfPermission()`으로 다시 확인하고, `shouldShowRequestPermissionRationale()`의 **현재 값**으로 rationale/설정 안내를 판정한다.
- protected BLE API 호출 직전에도 현재 grant를 다시 확인한다.

## Manifest matrix 메모

```xml
<!-- target Android 12+ 수업안의 개념 예시. 최종 선언은 공식표와 TBD target으로 검증한다. -->
<uses-permission android:name="android.permission.BLUETOOTH"
    android:maxSdkVersion="30" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN"
    android:maxSdkVersion="30" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"
    android:maxSdkVersion="30" />
```

`neverForLocation`은 앱이 scan 결과로 물리 위치를 절대 파생하지 않는다는 강한 선언이 가능할 때만 검토하며 일부 BLE beacon이 filtering될 수 있다. 실제 BLE/GATT/UUID/firmware 코드는 이번 예제에 없다.
