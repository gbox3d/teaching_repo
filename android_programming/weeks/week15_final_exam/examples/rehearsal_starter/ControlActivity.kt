package com.example.roomcontrol

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.roomcontrol.databinding.ActivityControlBinding
import com.example.roomcontrol.wleno.ConnState
import com.example.roomcontrol.wleno.Wleno
import com.example.roomcontrol.wleno.WlenoMessage
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject

class ControlActivity : AppCompatActivity() {
    private lateinit var binding: ActivityControlBinding
    private val client get() = Wleno.client

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityControlBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { view, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            val gap = (16 * resources.displayMetrics.density).toInt()
            view.setPadding(bars.left + gap, bars.top + gap, bars.right + gap, bars.bottom + gap)
            insets
        }
        binding.onButton.setOnClickListener {
            // TODO 1a: selectedLamp()로 선택한 조명을 켠다.
        }
        binding.offButton.setOnClickListener {
            // TODO 1b: 선택한 조명을 끈다.
        }
        binding.pwmButton.setOnClickListener {
            send("pwm ${selectedLamp()} ${binding.brightnessBar.progress}")
        }
        binding.allOffButton.setOnClickListener { send("off -1") }
        binding.sensorButton.setOnClickListener { send("dht11") }
        binding.backButton.setOnClickListener { finish() }
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                client.connectionState.collect { state ->
                    binding.stateText.text = "상태: $state"
                    val ready = state == ConnState.READY
                    binding.sensorButton.isEnabled = ready
                    binding.onButton.isEnabled = ready
                    binding.offButton.isEnabled = ready
                    binding.pwmButton.isEnabled = ready
                    binding.allOffButton.isEnabled = ready
                    if (!ready) binding.resultText.text = "연결 화면에서 다시 연결하세요."
                }
            }
        }
    }

    private fun selectedLamp(): Int {
        return if (binding.deskRadio.isChecked) 0 else 1
    }

    private fun send(command: String) {
        if (!client.isReady) return
        binding.resultText.text = "응답 대기 중"
        binding.commandText.text = "보냄: $command"
        client.send(command)
    }

    override fun onStart() {
        super.onStart()
        client.onMessage { line ->
            binding.responseText.text = "받음: $line"
            try {
                if (WlenoMessage.event(line) == "input") {
                    showInput(line)
                    return@onMessage
                }
                val result = WlenoMessage.result(line)
                binding.resultText.text = when (result) {
                    "ok" -> "요청 완료"
                    "err", "fail" -> "요청 실패: ${WlenoMessage.message(line) ?: line}"
                    else -> "기타 응답"
                }
                if (result == "ok" && WlenoMessage.value(line) != null) showSensor(line)
            } catch (e: Exception) {
                binding.resultText.text = "응답 형식을 확인하세요."
            }
        }
    }

    private fun showSensor(line: String) {
        // TODO 2: value 문자열을 JSONArray로 읽어 실내 온도와 습도를 표시한다.
    }

    private val inputHistory = mutableListOf<String>()

    private fun showInput(line: String) {
        // TODO 3: index와 value를 읽고 호출 이력을 한 줄 추가한다.
    }

    override fun onStop() {
        client.onMessage(null)
        client.disconnect()
        super.onStop()
    }
}
