package com.example.smartio

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.net.Uri
import android.os.BatteryManager
import android.os.Bundle
import android.provider.Settings
import android.util.Log
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.smartio.databinding.ActivityMainBinding
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 7주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: ConnViewModel by viewModels()

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

    // 11주차 1일차: [검색]이 시작한 "목록에 이름 추가" 코루틴. [중지]에서 취소하려고 보관한다(6주차 scanJob과 같은 모양).
    private var deviceJob: Job? = null

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

        // 1. [연결] 버튼: 이름이 비면 Toast, 아니면 제어 화면으로 이름을 들고 이동한다.
        binding.connectButton.setOnClickListener {
            val name = binding.deviceNameEdit.text.toString()
            if (name.isEmpty()) {
                Toast.makeText(this, "장치 이름을 입력하세요", Toast.LENGTH_SHORT).show()
            } else {
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

        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            viewModel.startScan()
            // 17. 목록을 비우고, 1초마다 가짜 장치 이름을 하나씩 추가한다(11주차 1일차).
            //     목록을 바꾼 뒤에는 notifyDataSetChanged()로 어댑터에 알려야 화면의 ListView가 다시 그려진다.
            devices.clear()
            adapter.notifyDataSetChanged()
            deviceJob = lifecycleScope.launch {
                for (name in arrayOf("ESP32_BLE_A", "ESP32_BLE_B", "ESP32_BLE_C")) {
                    delay(1000)
                    devices.add(name)
                    adapter.notifyDataSetChanged()
                    val count = devices.size
                    Log.d("Scan", "추가: $name, 장치 수: $count")
                }
            }
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
            // 18. 목록에 이름을 넣던 코루틴도 함께 멈춘다. 이미 들어간 이름은 목록에 남는다(11주차 1일차).
            deviceJob?.cancel()
        }

        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            viewModel.retry()
        }

        // 6. [해제] 버튼: 연결을 끊고 연결 안 됨으로 돌아간다(7주차 2일차).
        binding.disconnectButton.setOnClickListener {
            viewModel.disconnect()
        }

        // 7. 상태를 받아 화면을 고친다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(7주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect { state ->
                    binding.stateText.text = state
                    // 8. 먼저 모두 끄고, 상태에 맞는 것만 켠다. [연결]은 4주차 그대로 항상 켜 둔다(7주차 2일차).
                    binding.scanButton.isEnabled = false
                    binding.stopButton.isEnabled = false
                    binding.disconnectButton.isEnabled = false
                    binding.retryButton.visibility = View.GONE
                    binding.scanProgress.visibility = View.GONE
                    when (state) {
                        ConnState.DISCONNECTED -> {
                            binding.scanButton.isEnabled = true
                        }
                        ConnState.CONNECTING -> {
                            binding.stopButton.isEnabled = true
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.DISCOVERING -> {
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.READY -> {
                            binding.disconnectButton.isEnabled = true
                        }
                        ConnState.LOST -> {
                            binding.scanButton.isEnabled = true
                            binding.retryButton.visibility = View.VISIBLE
                        }
                    }
                }
            }
        }

        // 9. 남은 초를 받아 "연결 중… 3"처럼 붙여 보여 준다. 7번과 같은 틀을 하나 더 쓴다(7주차 2일차).
        //    반드시 7번 틀 아래에 둔다. 7번이 "연결 중"을 먼저 쓰고 9번이 숫자를 붙여야 회전 뒤에도 숫자가 보인다.
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.seconds.collect { seconds ->
                    if (seconds > 0) {
                        binding.stateText.text = "연결 중… $seconds"
                    }
                }
            }
        }

        // 12. [권한 확인] 버튼: 이미 모두 허용이면 "권한 OK", 하나라도 없으면 요청 창을 띄운다(10주차 2일차).
        binding.permissionButton.setOnClickListener {
            if (hasBlePermissions()) {
                Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
            } else {
                permissionLauncher.launch(blePermissions())
            }
        }

        // 19. 목록의 한 줄을 누르면: 누른 줄 번호(position)의 이름을 어댑터에서 꺼내 장치 이름 칸에 넣는다(11주차 1일차).
        //     1번 [연결]은 이 칸의 이름을 들고 제어 화면으로 가므로 1번 코드는 바꾸지 않는다.
        binding.deviceList.setOnItemClickListener { _, _, position, _ ->
            val name = adapter.getItem(position) ?: ""
            binding.deviceNameEdit.setText(name)
            Toast.makeText(this, "선택: $name", Toast.LENGTH_SHORT).show()
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
    override fun onStop() {
        super.onStop()
        unregisterReceiver(batteryReceiver)
    }

    // 13. blePermissions()의 권한을 하나씩 checkSelfPermission으로 확인한다. 하나라도 허용 안 됐으면 false(10주차 2일차).
    private fun hasBlePermissions(): Boolean {
        for (permission in blePermissions()) {
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
}
