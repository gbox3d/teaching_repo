package com.example.smartio

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.net.Uri
import android.os.BatteryManager
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.util.Log
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.smartio.bleuno.Bleuno
import com.example.smartio.bleuno.BleunoClient
import com.example.smartio.bleuno.ConnState
import com.example.smartio.bleuno.FakeBleunoClient
import com.example.smartio.bleuno.PermissionHelper
import com.example.smartio.databinding.ActivityMainBinding
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 10주차 1일차: 배터리 방송을 받는 Receiver. object : BroadcastReceiver() { … } 틀을 그대로 복사해 쓴다.
    // 방송이 오면 onReceive가 불리고, 함께 온 intent 안의 값(extras)으로 배터리 문구를 만든다.
    private val batteryReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            // 남은 양(level). intent가 null이거나 값이 없으면 -1이 된다.
            val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
            // 가득 찼을 때의 값(scale). 보통 100이다. 없으면 100으로 본다.
            val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, 100) ?: 100
            // 충전기 연결(plugged). 0이면 빠져 있고, 0이 아니면(AC·USB·무선) 꽂혀 있다.
            val plugged = intent?.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0) ?: 0
            if (level == -1) {
                return
            }
            val percent = level * 100 / scale
            val charging = if (plugged != 0) "충전 중" else "충전 안 함"
            binding.batteryText.text = "배터리 $percent% · $charging"
        }
    }

    // 10주차 2일차: 권한 요청 창을 띄우고 결과를 받는 틀. 화면이 시작되기 전에 만들어 두어야 하므로 클래스 안(onCreate 밖)에 둔다.
    // 사용자가 요청 창에서 고르면 { _ -> … }가 불린다. 넘어오는 결과는 쓰지 않고(_), 13번 함수로 지금 권한을 다시 확인한다.
    private val permissionLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
        // TODO(1) 권한 확인 흐름 — 요청 창의 결과 받기(15주차 1일차 리허설).
        //         13번 hasBlePermissions()로 지금 권한을 다시 확인한다. 모두 허용이면 Toast "권한 OK", 아니면 14번 showPermissionDialog()를 부른다.
    }

    // 11주차 2일차: 연락처 권한 요청 틀. 10주차 permissionLauncher와 같은 모양으로 클래스 안(onCreate 밖)에 둔다.
    // 결과는 읽지 않고(_) 지금 READ_CONTACTS가 허용됐는지 다시 확인한다. 허용이면 23번 함수로 연락처를 보여 준다.
    private val contactsLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) == PackageManager.PERMISSION_GRANTED) {
            showContacts()
        } else {
            AlertDialog.Builder(this)
                .setTitle("연락처 권한 없음")
                .setMessage("연락처를 읽으려면 권한이 필요합니다. 거절해도 앱의 다른 기능은 그대로 쓸 수 있습니다.")
                .setPositiveButton("확인", null)
                .show()
        }
    }

    // 12주차 1일차: true면 보드 없이 연습하는 가짜 클라이언트, false면 실제 보드에 연결하는 클라이언트를 만든다.
    // 실기기와 보드가 있으면 이 한 줄만 false로 바꾼다. 나머지 코드는 그대로 둔다.
    private val useFake = true

    // 12주차 1일차: 보드와 이야기하는 클라이언트. onCreate에서 받아 온다(24번). lateinit은 binding과 같은 틀이다.
    private lateinit var client: BleunoClient

    // 12주차 1일차: 블루투스 켜기 요청 창을 띄우고 결과를 받는 틀. 10주차에 본 setResult 결과 받기 틀(StartActivityForResult)과 같다.
    // 사용자가 요청 창에서 [허용]을 누르면 resultCode가 RESULT_OK로 돌아온다.
    private val bluetoothLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == RESULT_OK) {
            Toast.makeText(this, "블루투스 켜짐. [검색]을 다시 누르세요", Toast.LENGTH_SHORT).show()
        } else {
            Toast.makeText(this, "블루투스를 켜야 검색할 수 있습니다", Toast.LENGTH_SHORT).show()
        }
    }

    // 14주차 1일차: 마지막으로 연결을 시작한 보드 주소. 목록을 누를 때(43번) 담고 저장해 두었다가, [재연결](47번)에서 같은 주소로 다시 연결한다.
    // 화면이 새로 만들어지면(회전 등) 이 변수는 빈 글자("")로 돌아가므로 onCreate에서 저장소의 값을 다시 꺼내 넣는다(48번).
    private var lastAddress = ""

    // 14주차 1일차: 연결 시간 제한 코루틴. 다시 연결할 때 앞의 것을 취소하려고 보관한다(6주차 scanJob과 같다). 아직 없으면 null이다.
    private var connectTimeoutJob: Job? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 24. 앱 전체가 함께 쓰는 클라이언트를 받는다(12주차 1일차).
        //     이미 만들어 둔 것이 있으면(회전해서 onCreate가 다시 불린 경우) 그것을 그대로 쓰고, 없을 때만 Bleuno.create로 만든다.
        client = Bleuno.client ?: Bleuno.create(this, useFake)

        // 1. [연결] 버튼: 이름이 비면 Toast, 아니면 제어 화면으로 이름을 들고 이동한다.
        binding.connectButton.setOnClickListener {
            val name = binding.deviceNameEdit.text.toString()
            if (name.isEmpty()) {
                Toast.makeText(this, "장치 이름을 입력하세요", Toast.LENGTH_SHORT).show()
            } else {
                // 20. 연결하는 장치 이름을 앱 전용 저장소 "smartio"에 "last"라는 이름표로 저장한다(11주차 2일차).
                //     edit()로 고치기 시작 → putString으로 값 넣기 → apply()로 저장. 앱을 껐다 켜도 남는다.
                getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("last", name).apply()
                val intent = Intent(this, ControlActivity::class.java)
                intent.putExtra("name", name)
                startActivity(intent)
            }
        }

        // 2. 자동 연결 Switch: 켜고 끌 때마다 알린다.
        binding.autoSwitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                Toast.makeText(this, "자동 연결 켜짐", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "자동 연결 꺼짐", Toast.LENGTH_SHORT).show()
            }
        }

        // 15. 검색된 장치 이름을 담는 목록. 처음에는 비어 있고 add로 하나씩 늘린다(11주차 1일차).
        val devices = mutableListOf<String>()

        // 16. 어댑터: 목록(devices)의 이름을 한 줄짜리 기본 모양(simple_list_item_1)으로 ListView에 넣어 준다(11주차 1일차).
        val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, devices)
        binding.deviceList.adapter = adapter

        // 31. 찾은 보드의 주소를 목록 줄과 같은 순서로 담는다. 줄을 누르면 같은 번호의 주소로 연결한다(12주차 2일차).
        val addresses = mutableListOf<String>()

        // 3. [검색] 버튼: 권한과 블루투스를 확인한 뒤 5초 동안 보드를 검색한다(12주차 1일차에 가짜 검색을 교체).
        binding.scanButton.setOnClickListener {
            // 25. 권한이 없으면 10주차 흐름대로 요청 창을 띄우고, 블루투스가 꺼져 있으면 켜 달라고 요청한다(12주차 1일차).
            //     블루투스 켜기 요청 창도 권한이 있어야 띄울 수 있으므로 권한을 먼저 확인한다.
            if (hasBlePermissions() == false) {
                permissionLauncher.launch(PermissionHelper.required())
            } else if (PermissionHelper.isBluetoothEnabled(this) == false) {
                bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))
            } else if (isLocationOff()) {
                // 41. Android 11(API 30) 이하에서 위치 서비스가 꺼져 있으면 검색해도 0개가 나온다. 검색하지 않고 안내창(40번)을 띄운다(12주차 2일차).
                //     권한 → 블루투스 → 위치 순서로 확인하고, 셋 다 통과해야 아래 else에서 검색한다. 위치 확인은 42번 함수가 한다.
                showLocationDialog()
            } else {
                // 26. 목록을 비우고, 버튼과 ProgressBar를 "검색 중" 모양으로 바꾼다(12주차 1일차).
                //     검색할 때마다 목록을 새로 채우므로 [검색]을 여러 번 눌러도 같은 이름이 두 번 들어가지 않는다.
                devices.clear()
                adapter.notifyDataSetChanged()
                // 32. 주소 목록도 함께 비우고, 앞에서 보였을 수 있는 [다시 시도]를 숨긴다(12주차 2일차).
                addresses.clear()
                binding.retryButton.visibility = View.GONE
                binding.scanButton.isEnabled = false
                binding.stopButton.isEnabled = true
                binding.scanProgress.visibility = View.VISIBLE
                binding.stateText.text = "검색 중…"
                // 27. 5초 동안 검색한다. 보드를 찾을 때마다 onFound { }가, 검색이 끝나면 onFinished { }가 불린다(12주차 1일차).
                //     둘 다 메인 스레드에서 불리므로 안에서 View를 바로 바꿔도 된다. 한 번 검색하는 동안 같은 보드는 한 번만 알려 준다.
                client.startScan(5000, onFound = { device ->
                    val name = device.name
                    val address = device.address
                    // 28. 이름이 "ESP32_BLE"로 시작하는 보드만 목록에 "이름 (주소)"로 넣는다(12주차 1일차).
                    //     라이브러리도 같은 기준으로 거르지만, 앱에서 startsWith로 한 번 더 확인한다.
                    if (name.startsWith("ESP32_BLE")) {
                        devices.add("$name ($address)")
                        // 33. 같은 순서로 주소도 넣는다. devices의 0번 줄 ↔ addresses의 0번 주소(12주차 2일차).
                        addresses.add(address)
                        adapter.notifyDataSetChanged()
                        val count = devices.size
                        Log.d("Scan", "찾음: $name ($address), 장치 수: $count")
                    }
                }, onFinished = {
                    // 29. 검색이 끝나면(5초가 지났거나 [중지]) 버튼과 ProgressBar를 되돌리고 찾은 개수를 보여 준다(12주차 1일차).
                    binding.scanButton.isEnabled = true
                    binding.stopButton.isEnabled = false
                    binding.scanProgress.visibility = View.GONE
                    val count = devices.size
                    // 34. 하나도 못 찾았으면 안내하고 [다시 시도]를 보여 준다(12주차 2일차).
                    if (count == 0) {
                        binding.stateText.text = "장치를 찾지 못했습니다 — [다시 시도]를 누르세요"
                        binding.retryButton.visibility = View.VISIBLE
                    } else {
                        binding.stateText.text = "검색 완료 · 장치 수: $count"
                    }
                })
            }
        }

        // 4. [중지] 버튼: 검색을 바로 멈춘다(12주차 1일차에 가짜 검색 취소를 교체).
        binding.stopButton.setOnClickListener {
            // 30. 검색을 멈춘다. 이때도 onFinished가 한 번 불려 29번이 버튼·ProgressBar를 되돌린다(12주차 1일차).
            client.stopScan()
        }

        // 5. [다시 시도] 버튼: [검색]을 한 번 더 누른 것과 같다(12주차 2일차에 가짜 연결 재시도를 교체).
        binding.retryButton.setOnClickListener {
            // 35. performClick()은 코드로 버튼을 누른다. 3번 [검색]이 권한·블루투스 확인부터 그대로 다시 실행된다(12주차 2일차).
            binding.scanButton.performClick()
        }

        // 6. [해제] 버튼: 연결을 끊고 연결 안 됨으로 돌아간다(7주차 2일차).
        binding.disconnectButton.setOnClickListener {
            // 36. 보드와의 연결을 끊는다. 끊기면 connectionState가 "연결 안 됨"이 되어 7번이 화면을 고친다(12주차 2일차).
            client.disconnect()
        }

        // 7. 상태를 받아 화면을 고친다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(7주차 2일차).
        //    37. 7주차 viewModel.state 대신 보드와의 실제 연결 상태 client.connectionState를 받는다. 틀은 그대로다(12주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                client.connectionState.collect { state ->
                    binding.stateText.text = state
                    // 8. 먼저 모두 끄고, 상태에 맞는 것만 켠다. [연결]은 4주차 그대로 항상 켜 둔다(7주차 2일차).
                    binding.scanButton.isEnabled = false
                    binding.stopButton.isEnabled = false
                    binding.disconnectButton.isEnabled = false
                    binding.controlButton.isEnabled = false
                    binding.retryButton.visibility = View.GONE
                    binding.scanProgress.visibility = View.GONE
                    // 44. [재연결]은 끊김일 때만 보인다(45번). 먼저 숨긴다(14주차 1일차).
                    binding.reconnectButton.visibility = View.GONE
                    // 53. (시험용) [끊김 시험]은 준비됨일 때만 켠다(54번). 먼저 끈다(14주차 1일차).
                    binding.lostTestButton.isEnabled = false
                    when (state) {
                        ConnState.DISCONNECTED -> {
                            binding.scanButton.isEnabled = true
                        }
                        ConnState.CONNECTING -> {
                            // 연결 중에는 버튼을 모두 꺼 둔다. [중지]는 이제 검색 멈춤이라 켜지 않는다(12주차 2일차).
                            // 보드가 응답하지 않으면 한참(보통 30초쯤) 뒤 "끊김"이 되어 [검색]·[다시 시도]가 다시 켜진다.
                            // 14주차 1일차: 이제는 10초가 지나도 준비됨이 아니면 51번이 연결을 끊고 [검색]·[다시 시도]를 되살린다.
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.DISCOVERING -> {
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.READY -> {
                            binding.disconnectButton.isEnabled = true
                            // 준비됨일 때만 [제어 화면]을 누를 수 있다(12주차 2일차).
                            binding.controlButton.isEnabled = true
                            // 54. (시험용) 준비됨일 때만 [끊김 시험]을 누를 수 있다(14주차 1일차).
                            binding.lostTestButton.isEnabled = true
                        }
                        ConnState.LOST -> {
                            binding.scanButton.isEnabled = true
                            binding.retryButton.visibility = View.VISIBLE
                            // 45. 사용자가 해제하지 않았는데 끊겼다. [재연결]을 보여 주고 Toast로 알린다(14주차 1일차).
                            //     collect 틀 안에서는 this가 Activity가 아니어서 Toast는 46번 함수로 띄운다. 끊김인 채로 이 화면이 다시 보이면(회전, 제어 화면에서 [뒤로]) 또 뜬다.
                            binding.reconnectButton.visibility = View.VISIBLE
                            showLostToast()
                        }
                    }
                }
            }
        }

        // 12. [권한 확인] 버튼: 이미 모두 허용이면 "권한 OK", 하나라도 없으면 요청 창을 띄운다(10주차 2일차).
        binding.permissionButton.setOnClickListener {
            // TODO(1) 권한 확인 흐름 — [권한 확인] 버튼(15주차 1일차 리허설).
            //         13번 hasBlePermissions()가 true면 Toast "권한 OK"를 띄운다.
            //         아니면 permissionLauncher로 요청 창을 띄운다. 요청할 권한 목록은 PermissionHelper.required()가 준다.
        }

        // 19. 목록의 한 줄을 누르면: 누른 줄 번호(position)의 이름을 어댑터에서 꺼내 장치 이름 칸에 넣는다(11주차 1일차).
        //     1번 [연결]은 이 칸의 이름을 들고 제어 화면으로 가므로 1번 코드는 바꾸지 않는다.
        binding.deviceList.setOnItemClickListener { _, _, position, _ ->
            val name = adapter.getItem(position) ?: ""
            binding.deviceNameEdit.setText(name)
            Toast.makeText(this, "선택: $name", Toast.LENGTH_SHORT).show()
            // 38. 누른 줄과 같은 번호의 주소를 꺼내 연결을 시작한다. 검색 중이면 먼저 검색을 멈춘다(12주차 2일차).
            //     get(번호)는 add로 넣은 순서대로 꺼낸다. 번호는 0부터 센다.
            val address = addresses.get(position)
            client.stopScan()
            client.connect(address)
            // 43. 연결을 시작한 주소를 기억하고, 앱 전용 저장소 "smartio"에 "lastAddress"라는 이름표로도 저장한다(14주차 1일차).
            //     20번 장치 이름 저장과 같은 틀이다(11주차 2일차). 저장해 두면 화면이 새로 만들어져도 [재연결]이 이 주소를 쓴다(48번).
            lastAddress = address
            getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("lastAddress", address).apply()
            // 49. 10초 연결 시간 제한을 건다. 시간 제한은 50번 함수가 한다(14주차 1일차).
            startConnectTimeout()
        }

        // 39. [제어 화면] 버튼: 준비됨일 때만 켜진다(7번). 장치 이름 칸의 이름을 들고 제어 화면으로 간다(12주차 2일차).
        //     연결은 Bleuno.client에 들어 있으므로 제어 화면에서도 같은 연결을 이어 쓴다.
        binding.controlButton.setOnClickListener {
            val intent = Intent(this, ControlActivity::class.java)
            intent.putExtra("name", binding.deviceNameEdit.text.toString())
            startActivity(intent)
        }

        // 21. 앱이 시작되면(onCreate) 저장해 둔 마지막 장치 이름을 꺼내 보여 준다(11주차 2일차).
        //     저장한 적이 없으면 기본값 ""이 온다. getString은 String?를 돌려주므로 ?: ""로 null을 막는다.
        val prefs = getSharedPreferences("smartio", MODE_PRIVATE)
        val lastName = prefs.getString("last", "") ?: ""
        if (lastName.isEmpty()) {
            binding.lastDeviceText.text = "마지막 장치: 없음"
        } else {
            binding.lastDeviceText.text = "마지막 장치: $lastName"
        }

        // 48. 43번에서 저장한 마지막 보드 주소를 꺼내 lastAddress에 넣는다. 21번과 같은 틀이다(14주차 1일차).
        //     회전하거나 제어 화면에 가 있는 동안 이 화면이 새로 만들어져도 [재연결](47번)이 같은 주소를 쓴다. 저장한 적이 없으면 ""이다.
        lastAddress = prefs.getString("lastAddress", "") ?: ""

        // 52. 연결 중에 회전하면 화면이 새로 만들어지면서 앞 화면의 10초 예약도 함께 취소된다. 아직 연결 중·서비스 확인 중이면 시간 제한을 다시 건다(14주차 1일차).
        //     새로 거는 것이라 10초를 처음부터 다시 센다. 51번과 같은 listOf(…).contains(…) 검사다.
        if (listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(client.connectionState.value)) {
            startConnectTimeout()
        }

        // 22. [연락처 보기] 버튼: READ_CONTACTS가 이미 허용이면 바로 보여 주고, 아니면 요청 창을 띄운다(11주차 2일차, 시연·선택 실습).
        binding.contactsButton.setOnClickListener {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) == PackageManager.PERMISSION_GRANTED) {
                showContacts()
            } else {
                contactsLauncher.launch(arrayOf(Manifest.permission.READ_CONTACTS))
            }
        }

        // 47. [재연결] 버튼: 끊김일 때만 보인다(45번). 마지막으로 연결한 주소로 다시 연결한다(14주차 1일차).
        //     주소가 비어 있으면(앱을 설치하고 한 번도 목록을 눌러 연결한 적이 없으면) [검색]부터 하라고 알린다.
        binding.reconnectButton.setOnClickListener {
            if (lastAddress.isEmpty()) {
                Toast.makeText(this, "마지막 주소가 없습니다. [검색]부터 하세요", Toast.LENGTH_SHORT).show()
            } else {
                client.connect(lastAddress)
                // 49. 10초 연결 시간 제한을 건다(14주차 1일차).
                startConnectTimeout()
            }
        }

        // 55. (시험용) [끊김 시험] 버튼: 가짜 보드(useFake = true)일 때만 보인다. 보드 전원을 끈 것처럼 "끊김"을 만든다(14주차 1일차).
        //     simulateLost()는 FakeBleunoClient에만 있어서 as로 "가짜 클라이언트로 보고" 꺼낸 뒤 부른다. 실제 보드는 전원을 꺼서 시험한다.
        if (useFake) {
            binding.lostTestButton.visibility = View.VISIBLE
        }
        binding.lostTestButton.setOnClickListener {
            val fake = client as FakeBleunoClient
            fake.simulateLost()
        }
    }

    // 10. 화면이 보이기 시작하면 배터리 방송을 받도록 등록한다. 등록하자마자 마지막 배터리 값이 한 번 온다(10주차 1일차).
    override fun onStart() {
        super.onStart()
        ContextCompat.registerReceiver(
            this,
            batteryReceiver,
            IntentFilter(Intent.ACTION_BATTERY_CHANGED),
            ContextCompat.RECEIVER_NOT_EXPORTED
        )
    }

    // 11. 화면이 안 보이게 되면 등록을 푼다. onStart의 등록과 반드시 짝을 맞춘다(10주차 1일차).
    //     12주차 1일차: 검색도 여기서 멈춘다. 화면이 안 보이는 동안 검색이 끝나 onFinished(29번)가 보이지 않는 화면을 고치는 일을 막는다.
    override fun onStop() {
        super.onStop()
        unregisterReceiver(batteryReceiver)
        client.stopScan()
    }

    // 13. PermissionHelper.required()의 권한을 하나씩 checkSelfPermission으로 확인한다. 하나라도 허용 안 됐으면 false(10주차 2일차).
    //     12주차 1일차: 10주차 blePermissions()를 bleuno 패키지의 PermissionHelper.required()로 바꿨다. 돌려주는 권한 목록은 같다.
    private fun hasBlePermissions(): Boolean {
        // TODO(1) 권한 확인 흐름 — 권한을 하나씩 확인하기(15주차 1일차 리허설).
        //         for로 PermissionHelper.required()의 권한을 하나씩 꺼내 ContextCompat.checkSelfPermission(this, 권한)으로 확인한다.
        //         PackageManager.PERMISSION_GRANTED가 아닌 권한이 하나라도 있으면 그 자리에서 false를 돌려준다.
        //         아래 return true는 "모두 허용"일 때 돌려주는 줄이다. 지우지 말고 그 위에 채운다(지우면 빌드가 안 된다).
        return true
    }

    // 14. 거절했을 때 보여 주는 AlertDialog. [설정으로]를 누르면 이 앱의 정보(권한) 화면을 연다(10주차 2일차).
    private fun showPermissionDialog() {
        // TODO(1) 권한 확인 흐름 — 거절했을 때 안내 창(15주차 1일차 리허설).
        //         AlertDialog.Builder(this)로 제목 "권한이 필요합니다", 안내 문구, [설정으로]·[취소] 버튼이 있는 창을 띄운다.
        //         [설정으로]를 누르면 Settings.ACTION_APPLICATION_DETAILS_SETTINGS와 Uri.parse("package:$packageName")로 만든 암시적 Intent로 이 앱의 정보 화면을 연다.
        //         40번 showLocationDialog()가 같은 모양이다.
    }

    // 23. ContactsReader로 연락처 이름을 읽어 AlertDialog 목록으로 보여 준다(11주차 2일차).
    //     0건이면 목록 대신 안내 문구를 보여 준다. 0건은 실패가 아니다(에뮬레이터는 처음에 연락처가 없다).
    private fun showContacts() {
        val names = ContactsReader.names(contentResolver)
        if (names.isEmpty()) {
            AlertDialog.Builder(this)
                .setTitle("연락처")
                .setMessage("연락처가 0건입니다. 연락처 앱에서 한 명을 추가한 뒤 다시 눌러 보세요.")
                .setPositiveButton("확인", null)
                .show()
        } else {
            // setItems는 배열을 받으므로 toTypedArray()로 목록(List)을 배열(Array)로 바꿔 넘긴다.
            AlertDialog.Builder(this)
                .setTitle("연락처")
                .setItems(names.toTypedArray(), null)
                .setPositiveButton("닫기", null)
                .show()
        }
    }

    // 40. 위치 서비스가 꺼져 있을 때 보여 주는 AlertDialog. [설정으로]를 누르면 위치 설정 화면을 연다(12주차 2일차).
    //     14번과 같은 모양이다. [검색]을 눌렀을 때(41번) 부르므로 늘 화면이 보이는 동안 뜬다.
    private fun showLocationDialog() {
        AlertDialog.Builder(this)
            .setTitle("위치 서비스가 꺼져 있습니다")
            .setMessage("Android 11 이하에서는 위치 서비스를 켜야 보드가 검색됩니다. 위치를 켠 뒤 [검색]을 다시 누르세요.")
            .setPositiveButton("설정으로") { _, _ ->
                val intent = Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS)
                startActivity(intent)
            }
            .setNegativeButton("취소", null)
            .show()
    }

    // 42. Android 11(API 30) 이하이면서 위치 서비스가 꺼져 있으면 true, 아니면 false(12주차 2일차).
    //     Android 12 이상은 위치 서비스와 상관없이 검색되므로 늘 false다. 13번 hasBlePermissions()처럼 true/false를 돌려준다.
    private fun isLocationOff(): Boolean {
        if (Build.VERSION.SDK_INT <= 30) {
            if (PermissionHelper.isLocationEnabled(this) == false) {
                return true
            }
        }
        return false
    }

    // 46. 끊겼다고 알리는 Toast. 7번 collect의 끊김 가지(45번)에서 부른다(14주차 1일차).
    //     collect 틀 안의 this는 Activity가 아니어서 Toast.makeText(this, …)를 바로 쓸 수 없다. 함수로 빼면 this가 Activity다.
    private fun showLostToast() {
        Toast.makeText(this, "연결이 끊겼습니다. [재연결]을 누르세요", Toast.LENGTH_SHORT).show()
    }

    // 50. 연결 시간 제한을 건다. 앞에서 건 제한이 남아 있으면 먼저 취소한다(14주차 1일차).
    //     취소하지 않으면 앞 연결의 10초 예약이 새 연결을 끊을 수 있다. 6주차 [중지]의 scanJob?.cancel()과 같은 방법이다.
    private fun startConnectTimeout() {
        // TODO(3) 연결 시간 제한 걸기(15주차 1일차 리허설).
        //         connectTimeoutJob에 앞에서 건 코루틴이 남아 있으면 먼저 취소한다(아직 없으면 null이다).
        //         lifecycleScope.launch로 새 코루틴을 시작해 그 Job을 connectTimeoutJob에 보관하고, 코루틴 안에서 51번 waitConnectTimeout()을 부른다.
    }

    // 51. 10초를 기다린 뒤에도 아직 연결 중·서비스 확인 중이면 "연결 시간이 초과되었습니다"를 알리고 연결을 끊는다(14주차 1일차).
    //     그사이 준비됨·끊김·연결 안 됨이 되었으면 아무것도 하지 않는다. listOf(…).contains(…)는 13주차 오늘 문법이다.
    //     delay를 쓰므로 suspend가 붙는다(6주차 countDown과 같다). 이 함수 안의 this는 Activity라서 Toast에 그대로 쓴다.
    private suspend fun waitConnectTimeout() {
        // TODO(3) 10초 기다린 뒤 안내하기(15주차 1일차 리허설).
        //         delay로 10초(10000ms)를 기다린 뒤 client.connectionState.value를 읽는다.
        //         그 값이 ConnState.CONNECTING·ConnState.DISCOVERING 가운데 하나이면(52번과 같은 listOf(…).contains(…) 검사)
        //         Toast "연결 시간이 초과되었습니다"를 띄우고 client.disconnect()로 연결을 끊는다.
        //         이어서 stateText를 "연결 시간 초과 — [다시 시도]를 누르세요"로 바꾸고, scanProgress를 숨기고, [검색]을 켜고, [다시 시도]를 보이게 한다.
    }
}
