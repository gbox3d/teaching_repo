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
        binding.onButton.setOnClickListener { send("on ${selectedLamp()}") }
        binding.offButton.setOnClickListener { send("off ${selectedLamp()}") }
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
        // value는 배열 자체가 아니라 배열을 담은 문자열이다.
        val values = JSONArray(WlenoMessage.value(line) ?: return)
        require(values.length() == 2)
        val temperature = values.getDouble(0)
        val humidity = values.getDouble(1)
        require(temperature.isFinite() && humidity.isFinite())
        binding.sensorText.text = "실내 온도: $temperature °C / 습도: $humidity %"
    }

    override fun onStop() {
        client.onMessage(null)
        client.disconnect()
        super.onStop()
    }
}
