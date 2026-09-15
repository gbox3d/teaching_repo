package com.example.rehearsal

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.rehearsal.databinding.ActivityMainBinding
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 8주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: RehearsalViewModel by viewModels()

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

        // 1. [시작] 버튼: 카운트다운은 ViewModel에 맡긴다(8주차 1일차).
        binding.startButton.setOnClickListener {
            viewModel.startCountdown()
        }

        // 2. [취소] 버튼: 카운트다운 코루틴을 취소한다(8주차 1일차).
        binding.cancelButton.setOnClickListener {
            viewModel.cancelCountdown()
        }

        // 3. 상태를 받아 문구와 버튼을 고친다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(8주차 1일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect { state ->
                    binding.stateText.text = state
                    // 카운트다운 중에는 [취소]만, 그 밖에는 [시작]만 켠다.
                    if (state == "카운트다운 중") {
                        binding.startButton.isEnabled = false
                        binding.cancelButton.isEnabled = true
                    } else {
                        binding.startButton.isEnabled = true
                        binding.cancelButton.isEnabled = false
                    }
                }
            }
        }

        // 4. 남은 초를 받아 보여 준다. 3번과 같은 틀을 하나 더 쓴다(8주차 1일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.seconds.collect { seconds ->
                    binding.timeText.text = "남은 초: $seconds"
                }
            }
        }
    }
}
