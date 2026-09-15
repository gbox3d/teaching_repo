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
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

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

        // 3. [검색] 버튼(6주차 1일차): 코루틴으로 5초 카운트다운을 보여 준다.
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.scanProgress.visibility = View.VISIBLE
            lifecycleScope.launch {
                countDown()
                binding.stateText.text = "검색 완료"
                binding.scanProgress.visibility = View.GONE
                binding.scanButton.isEnabled = true
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
}
