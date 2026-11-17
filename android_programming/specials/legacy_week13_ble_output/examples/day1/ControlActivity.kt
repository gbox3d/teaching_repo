package com.example.smartio

import android.os.Bundle
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.smartio.bleuno.Bleuno
import com.example.smartio.bleuno.BleunoMessage
import com.example.smartio.databinding.ActivityControlBinding
import kotlinx.coroutines.launch

class ControlActivity : AppCompatActivity() {
    // ViewBinding 틀: activity_control.xml → ActivityControlBinding
    private lateinit var binding: ActivityControlBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityControlBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 1. 연결 화면이 보낸 장치 이름을 꺼내 상단에 보여 준다.
        val name = intent.getStringExtra("name") ?: ""
        binding.deviceText.text = "장치: $name"

        // 2. LED Switch: 켜면 on, 끄면 off 명령을 로그에 쌓는다.
        //    13주차 1일차: 입력 칸은 이제 핀 번호가 아니라 LED 번호(0~3)다. 로그에 쌓기 전에 보드에도 명령을 보낸다(5·6번).
        binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
            val pin = binding.pinEdit.text.toString()
            if (pin.isEmpty()) {
                Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
            } else if (isChecked) {
                // 5. 입력한 글자를 숫자(LED 번호)로 바꿔 "on 번호" 명령을 보드에 보내고, 보낸 명령을 로그에 남긴다(13주차 1일차).
                //    send는 끝에 "\n"을 붙여 차례대로 보낸다. Bleuno.client가 없으면(null) ?.에서 멈추고 아무것도 보내지 않는다.
                val index = pin.toInt()
                Bleuno.client?.send("on $index")
                binding.logText.append("on $index\n")
            } else {
                // 6. 끄면 "off 번호" 명령을 보낸다. 5번과 같은 모양이다(13주차 1일차).
                val index = pin.toInt()
                Bleuno.client?.send("off $index")
                binding.logText.append("off $index\n")
            }
        }

        // 3. [뒤로] 버튼: 이 화면을 닫고 연결 화면으로 돌아간다.
        binding.backButton.setOnClickListener {
            finish()
        }

        // 4. 연결 화면이 만든 클라이언트를 Bleuno.client로 꺼내 연결 상태를 상단에 보여 준다(12주차 2일차).
        //    MainActivity 7번과 같은 collect 틀이다. client가 없으면(null) ?.에서 멈추고 "상태: ?"가 그대로 남는다.
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                Bleuno.client?.connectionState?.collect { state ->
                    binding.stateText.text = "상태: $state"
                }
            }
        }

        // 7. [전체 끄기] 버튼: 번호 자리에 -1을 보내면 보드의 LED가 모두 꺼진다(13주차 1일차).
        binding.allOffButton.setOnClickListener {
            Bleuno.client?.send("off -1")
            binding.logText.append("off -1\n")
        }
    }

    // 8. 화면이 보이기 시작하면 보드가 보내는 응답(JSON 한 줄)을 받도록 등록한다(13주차 1일차).
    //    명령 하나마다 응답이 한 줄씩 온다. { json -> }는 메인 스레드에서 불리므로 안에서 View를 바로 바꿔도 된다.
    override fun onStart() {
        super.onStart()
        Bleuno.client?.onMessage { json ->
            // 9. JSON에서 "result"(ok·err·fail) 값을 꺼내 보고, 명령의 응답이면 받은 JSON 한 줄을 그대로 로그에 남긴다(13주차 1일차).
            //    로그 예: 응답: {"result":"ok","ms":"led(s) on"}. result가 없는 줄은 명령의 응답이 아니다(가짜 보드가 10초마다 보내는 입력 이벤트, 14주차에 다룬다). 로그에 넣지 않는다.
            val result = BleunoMessage.result(json)
            if (result != null) {
                binding.logText.append("응답: $json\n")
            }
        }
    }

    // 10. 화면이 안 보이게 되면 응답 받기를 푼다(null). onStart의 등록과 반드시 짝을 맞춘다(13주차 1일차).
    //     10주차 배터리 Receiver의 등록·해제와 같은 규칙이다. 풀지 않으면 보이지 않는 화면의 로그를 계속 고치려 한다.
    override fun onStop() {
        super.onStop()
        Bleuno.client?.onMessage(null)
    }
}
