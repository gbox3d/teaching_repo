package com.example.roomcontrol

import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.roomcontrol.databinding.ActivityMainBinding
import com.example.roomcontrol.wleno.ConnState
import com.example.roomcontrol.wleno.Wleno
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private val client get() = Wleno.client
    private var pendingConnect = false
    private var openingControl = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { view, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            val gap = (16 * resources.displayMetrics.density).toInt()
            view.setPadding(bars.left + gap, bars.top + gap, bars.right + gap, bars.bottom + gap)
            insets
        }
        binding.wifiButton.setOnClickListener {
            // 시스템 설정에서 사용자가 네트워크를 선택한다. 앱이 Wi-Fi를 켜거나 검색하지 않는다.
            startActivity(Intent(Settings.ACTION_WIFI_SETTINGS))
        }
        binding.connectButton.setOnClickListener {
            val address = binding.addressEdit.text.toString().trim()
            if (address.isBlank()) {
                binding.addressEdit.error = "IPv4 주소와 포트를 입력하세요."
            } else {
                pendingConnect = true
                client.connect(address)
            }
        }
        binding.disconnectButton.setOnClickListener { client.disconnect() }
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                client.connectionState.collect { state ->
                    binding.stateText.text = "상태: $state"
                    val busy = state == ConnState.CONNECTING || state == ConnState.HANDSHAKING
                    binding.connectButton.isEnabled = !busy && state != ConnState.READY
                    binding.addressEdit.isEnabled = !busy && state != ConnState.READY
                    binding.disconnectButton.isEnabled = busy || state == ConnState.READY
                    if (state == ConnState.READY && pendingConnect) {
                        pendingConnect = false
                        openingControl = true
                        startActivity(Intent(this@MainActivity, ControlActivity::class.java))
                    } else if (state == ConnState.LOST) {
                        pendingConnect = false
                    }

                }
            }
        }
    }

    override fun onStart() {
        super.onStart()
        openingControl = false
    }

    override fun onStop() {
        client.stopScan()
        // 제어 화면으로 넘길 때는 TCP와 그 화면이 등록한 리스너를 보존한다.
        if (!openingControl) {
            pendingConnect = false
            client.onMessage(null)
            client.disconnect()
        }
        super.onStop()
    }
}
