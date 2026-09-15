package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.smartio.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 7주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: ConnViewModel by viewModels()

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
            viewModel.startScan()
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
        }

        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            binding.retryButton.visibility = View.GONE
            binding.scanButton.isEnabled = false
            binding.scanProgress.visibility = View.VISIBLE
            viewModel.retry()
        }

        // 6. ViewModel이 문구를 알려 줄 때 부를 코드를 등록한다. 회전으로 새 화면이 생기면 새 화면이 다시 등록한다(7주차 1일차).
        viewModel.listener = { text ->
            showState(text)
        }

        // 7. 회전으로 새로 만들어진 화면: ViewModel에 남은 문구를 다시 읽어 보여 준다(7주차 1일차).
        binding.stateText.text = viewModel.resultText
        if (viewModel.resultText == "연결 실패") {
            binding.retryButton.visibility = View.VISIBLE
        }
    }

    // 8. 화면이 없어질 때(회전 포함) 등록을 푼다. ViewModel이 없어진 옛 화면을 붙잡지 않게 한다(7주차 1일차).
    override fun onDestroy() {
        super.onDestroy()
        viewModel.listener = null
    }

    // 9. ViewModel이 알려 준 문구를 보여 주고, 문구에 맞게 버튼을 고친다(7주차 1일차).
    private fun showState(text: String) {
        binding.stateText.text = text
        if (text == "연결 중…") {
            binding.stopButton.isEnabled = false
        } else if (text == "연결됨") {
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            val intent = Intent(this, ControlActivity::class.java)
            intent.putExtra("name", binding.deviceNameEdit.text.toString())
            startActivity(intent)
        } else if (text == "연결 실패") {
            Toast.makeText(this, text, Toast.LENGTH_SHORT).show()
            binding.retryButton.visibility = View.VISIBLE
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
        }
    }
}
