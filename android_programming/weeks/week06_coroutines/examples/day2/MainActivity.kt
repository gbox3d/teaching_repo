package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.lifecycleScope
import com.example.smartio.databinding.ActivityMainBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlin.random.Random

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 6주차 2일차: [검색]이 시작한 코루틴. [중지]에서 취소하려고 보관한다. 아직 없으면 null이다.
    private var scanJob: Job? = null

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

        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.stopButton.isEnabled = true
            binding.retryButton.visibility = View.GONE
            binding.scanProgress.visibility = View.VISIBLE
            scanJob = lifecycleScope.launch {
                countDown()
                binding.stopButton.isEnabled = false
                tryConnect()
            }
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            scanJob?.cancel()
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
        }

        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            binding.retryButton.visibility = View.GONE
            binding.scanButton.isEnabled = false
            binding.scanProgress.visibility = View.VISIBLE
            lifecycleScope.launch {
                tryConnect()
            }
        }
    }

    // 5부터 1까지 1초마다 화면에 보여 준다. 안에서 delay를 쓰므로 suspend가 붙는다.
    private suspend fun countDown() {
        for (i in 5 downTo 1) {
            binding.stateText.text = "검색 중… $i"
            delay(1000)
        }
    }

    // 연결을 흉내 낸다. 2초 걸리고 절반은 실패한다. 진짜 막히는 일이므로 IO로 옮긴다.
    private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
        Thread.sleep(2000)
        if (Random.nextBoolean()) {
            throw Exception("연결 실패")
        }
        true
    }

    // 가짜 연결을 시도하고 결과를 화면에 보여 준다.
    private suspend fun tryConnect() {
        binding.stateText.text = "연결 중…"
        try {
            connectFake()
            binding.stateText.text = "연결됨"
            val intent = Intent(this, ControlActivity::class.java)
            intent.putExtra("name", binding.deviceNameEdit.text.toString())
            startActivity(intent)
        } catch (e: Exception) {
            binding.stateText.text = "연결 실패"
            Toast.makeText(this, e.message, Toast.LENGTH_SHORT).show()
            binding.retryButton.visibility = View.VISIBLE
        }
        binding.scanProgress.visibility = View.GONE
        binding.scanButton.isEnabled = true
    }
}
