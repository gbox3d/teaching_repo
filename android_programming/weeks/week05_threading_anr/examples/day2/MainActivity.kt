package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.smartio.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 5주차 2일차: 메인 스레드의 메시지 큐에 "나중에 할 일"을 넣어 주는 Handler
    private val handler = Handler(Looper.getMainLooper())

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

        // 3. 검색이 끝났을 때 할 일(5주차 2일차). 이름을 붙여 두어야 [중지]에서 취소할 수 있다.
        val finishScan = Runnable {
            binding.stateText.text = "검색 완료"
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
            Toast.makeText(this, "검색 완료", Toast.LENGTH_SHORT).show()
        }

        // 4. [검색] 버튼: 검색 중 화면으로 바꾸고, 5초 뒤에 finishScan을 실행하도록 예약한다.
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.stopButton.isEnabled = true
            binding.stateText.text = "검색 중…"
            binding.scanProgress.visibility = View.VISIBLE
            handler.postDelayed(finishScan, 5000)
        }

        // 5. [중지] 버튼: 예약을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            handler.removeCallbacks(finishScan)
            binding.stateText.text = "검색 중지"
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
        }
    }
}
