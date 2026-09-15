package com.example.project1

import android.os.Bundle
import android.view.View
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.project1.databinding.ActivityMainBinding
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 7주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: RequestViewModel by viewModels()

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

        // 1. [요청] 버튼: 요청은 ViewModel이 보낸다. 화면은 부탁만 한다(9주차 1일차).
        binding.requestButton.setOnClickListener {
            viewModel.request()
        }

        // 2. [다시 시도] 버튼: 실패한 요청을 한 번 더 보낸다. [요청]과 같은 함수를 부른다(9주차 1일차).
        binding.retryButton.setOnClickListener {
            viewModel.request()
        }

        // 3. 결과 문구를 받아 화면에 보여 준다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(7주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.result.collect { result ->
                    binding.resultText.text = result
                }
            }
        }

        // 4. 실패 여부를 받아 [다시 시도]를 보이거나 숨긴다. 3번과 같은 틀을 하나 더 쓴다(7주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.failed.collect { failed ->
                    if (failed) {
                        binding.retryButton.visibility = View.VISIBLE
                    } else {
                        binding.retryButton.visibility = View.GONE
                    }
                }
            }
        }
    }
}
