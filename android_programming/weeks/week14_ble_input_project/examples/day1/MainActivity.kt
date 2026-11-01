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
import com.example.smartio.bleuno.PermissionHelper
import com.example.smartio.databinding.ActivityMainBinding
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
        if (hasBlePermissions()) {
            Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
        } else {
            showPermissionDialog()
        }
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
                    when (state) {
                        ConnState.DISCONNECTED -> {
                            binding.scanButton.isEnabled = true
                        }
                        ConnState.CONNECTING -> {
                            // 연결 중에는 버튼을 모두 꺼 둔다. [중지]는 이제 검색 멈춤이라 켜지 않는다(12주차 2일차).
                            // 보드가 응답하지 않으면 한참(보통 30초쯤) 뒤 "끊김"이 되어 [검색]·[다시 시도]가 다시 켜진다.
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.DISCOVERING -> {
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.READY -> {
                            binding.disconnectButton.isEnabled = true
                            // 준비됨일 때만 [제어 화면]을 누를 수 있다(12주차 2일차).
                            binding.controlButton.isEnabled = true
                        }
                        ConnState.LOST -> {
                            binding.scanButton.isEnabled = true
                            binding.retryButton.visibility = View.VISIBLE
                        }
                    }
                }
            }
        }

        // 12. [권한 확인] 버튼: 이미 모두 허용이면 "권한 OK", 하나라도 없으면 요청 창을 띄운다(10주차 2일차).
        binding.permissionButton.setOnClickListener {
            if (hasBlePermissions()) {
                Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
            } else {
                permissionLauncher.launch(PermissionHelper.required())
            }
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

        // 22. [연락처 보기] 버튼: READ_CONTACTS가 이미 허용이면 바로 보여 주고, 아니면 요청 창을 띄운다(11주차 2일차, 시연·선택 실습).
        binding.contactsButton.setOnClickListener {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) == PackageManager.PERMISSION_GRANTED) {
                showContacts()
            } else {
                contactsLauncher.launch(arrayOf(Manifest.permission.READ_CONTACTS))
            }
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
        for (permission in PermissionHelper.required()) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                return false
            }
        }
        return true
    }

    // 14. 거절했을 때 보여 주는 AlertDialog. [설정으로]를 누르면 이 앱의 정보(권한) 화면을 연다(10주차 2일차).
    private fun showPermissionDialog() {
        AlertDialog.Builder(this)
            .setTitle("권한이 필요합니다")
            .setMessage("장치를 검색하고 연결하려면 권한이 필요합니다. 설정 › 권한에서 허용해 주세요.")
            .setPositiveButton("설정으로") { _, _ ->
                // 암시적 Intent: 무엇을 할지(ACTION)와 대상(package:앱 이름)만 적으면 시스템이 맞는 화면을 찾아 연다.
                val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))
                startActivity(intent)
            }
            .setNegativeButton("취소", null)
            .show()
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
}
