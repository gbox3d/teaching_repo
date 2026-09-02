# 4주차 예제 스니펫 — mock 목록과 Navigation

## 사용 범위

이 폴더에는 설명용 대표 스니펫만 있고 **빌드 가능한 Gradle 프로젝트는 포함되어 있지 않다**. Navigation/RecyclerView가 설정된 강의자 기준 Kotlin + XML Views 프로젝트에서 package, import, resource ID, dependency를 확인해 옮긴다.

## 파일명과 문맥

| 파일명 예시 | 위치/역할 |
|---|---|
| `activity_main.xml` | NavHost를 담는 Activity layout |
| `nav_graph.xml` | `res/navigation/`, 두 destination과 action |
| `fragment_device_list.xml` | RecyclerView와 empty View |
| `item_device.xml` | 장치명·상태 한 행 |
| `fragment_device_control.xml` | ID, pulse 입력, mock 실행 결과 |
| `MockDevice.kt` | 안정 ID를 가진 item 모델 |
| `DeviceAdapter.kt` | ListAdapter와 ViewHolder |
| `DeviceListFragment.kt` | 목록 제출과 item navigation |
| `DeviceControlFragment.kt` | argument·숫자 검증과 mock render |

## NavHost 핵심

```xml
<androidx.fragment.app.FragmentContainerView
    android:id="@+id/navHost"
    android:name="androidx.navigation.fragment.NavHostFragment"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    app:defaultNavHost="true"
    app:navGraph="@navigation/nav_graph" />
```

## navigation graph 핵심

```xml
<navigation
    android:id="@+id/nav_graph"
    app:startDestination="@id/deviceListFragment">

    <fragment
        android:id="@+id/deviceListFragment"
        android:name="com.example.smartio.DeviceListFragment">
        <action
            android:id="@+id/action_list_to_control"
            app:destination="@id/deviceControlFragment" />
    </fragment>

    <fragment
        android:id="@+id/deviceControlFragment"
        android:name="com.example.smartio.DeviceControlFragment" />
</navigation>
```

package 이름은 기준 프로젝트 값으로 교체한다.

## item 모델과 Adapter 핵심

```kotlin
data class MockDevice(
    val id: String,
    val name: String,
    val ready: Boolean,
)

class DeviceAdapter(
    private val onClick: (MockDevice) -> Unit,
) : ListAdapter<MockDevice, DeviceAdapter.Holder>(DIFF) {

    companion object {
        val DIFF = object : DiffUtil.ItemCallback<MockDevice>() {
            override fun areItemsTheSame(old: MockDevice, new: MockDevice) =
                old.id == new.id

            override fun areContentsTheSame(old: MockDevice, new: MockDevice) =
                old == new
        }
    }

    inner class Holder(view: View) : RecyclerView.ViewHolder(view) {
        private val name = view.findViewById<TextView>(R.id.deviceName)
        private val status = view.findViewById<TextView>(R.id.deviceStatus)

        fun bind(item: MockDevice) {
            name.text = item.name
            status.setText(
                if (item.ready) R.string.status_ready
                else R.string.status_disconnected
            )
            itemView.setOnClickListener { onClick(item) }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_device, parent, false)
        return Holder(view)
    }

    override fun onBindViewHolder(holder: Holder, position: Int) {
        holder.bind(getItem(position))
    }
}
```

`ViewGroup`과 `LayoutInflater`를 포함한 import는 IDE에서 AndroidX class인지 확인한다. 이 클래스 블록은 동일성, item inflate, 전체 bind, item callback까지 한 흐름으로 복사할 수 있다.

## 목록→제어 이동 핵심

```kotlin
const val ARG_DEVICE_ID = "device_id"

private fun openDevice(device: MockDevice) {
    val args = bundleOf(ARG_DEVICE_ID to device.id)
    findNavController().navigate(R.id.action_list_to_control, args)
}
```

## 제어 입력 검증 핵심

```kotlin
private val deviceId: String?
    get() = arguments
        ?.getString(ARG_DEVICE_ID)
        ?.trim()
        ?.takeIf { it.isNotEmpty() }

fun runMockPulse(raw: String) {
    val currentDeviceId = deviceId
    val text = raw.trim()
    val looksLikeInteger = text.matches(Regex("[+-]?\\d+"))
    val millis = text.toLongOrNull()

    when {
        currentDeviceId == null -> renderMissingDevice()
        text.isEmpty() -> pulseInput.error = getString(R.string.pulse_required)
        !looksLikeInteger -> pulseInput.error = getString(R.string.pulse_number_only)
        millis == null || millis !in 100L..5000L ->
            pulseInput.error = getString(R.string.pulse_range)
        else -> {
            pulseInput.error = null
            resultView.text = getString(
                R.string.mock_pulse_result,
                currentDeviceId,
                millis.toInt(),
            )
        }
    }
}
```

`deviceId`는 Fragment 생성자의 eager initializer에서 고정하지 않고, Navigation이 arguments를 설정한 뒤 getter로 읽는다. View 참조는 `onViewCreated(view, ...)`에서 찾고 View lifecycle 밖에 보관하지 않는 문맥이다.

## 예상 관찰

1. empty list는 빈 상태 View를, 1개와 3개 list는 정확한 행 수를 보인다.
2. 두 번째 행 클릭은 position이 아니라 `mock-02` item ID를 전달한다.
3. `100`, `5000`은 성공 경계이고 `99`, `5001`, 문자, 빈 값은 각 오류다.
4. 성공 결과에는 `mock`임이 명시되고 실제 BLE write는 없다.
5. 목록→제어에서 목록 View가 파괴됐다가 Back 뒤 다시 만들어질 수 있다.

## 공식 참고 자료

- [Fragment view lifecycle — Android Developers](https://developer.android.com/guide/fragments/lifecycle)
- [Navigation graph — Android Developers](https://developer.android.com/guide/navigation/design)
- [RecyclerView — Android Developers](https://developer.android.com/develop/ui/views/layout/recyclerview)
