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
import kotlinx.coroutines.launch

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
        binding.onButton.setOnClickListener { send("on 0") }
        binding.offButton.setOnClickListener { send("off 0") }
        binding.backButton.setOnClickListener { finish() }
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                client.connectionState.collect { state ->
                    binding.stateText.text = "상태: $state"
                    binding.onButton.isEnabled = state == ConnState.READY
                    binding.offButton.isEnabled = state == ConnState.READY
                }
            }
        }
    }

    override fun onStart() {
        super.onStart()
        client.onMessage { line -> binding.responseText.text = "받음: $line" }
    }

    private fun send(command: String) {
        binding.commandText.text = "보냄: $command"
        client.send(command)
    }

    override fun onStop() {
        client.onMessage(null)
        client.disconnect()
        super.onStop()
    }
}
