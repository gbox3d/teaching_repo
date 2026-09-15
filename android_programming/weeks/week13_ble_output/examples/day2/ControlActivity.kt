package com.example.smartio

import android.os.Bundle
import android.widget.SeekBar
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.smartio.bleuno.Bleuno
import com.example.smartio.bleuno.BleunoMessage
import com.example.smartio.bleuno.ConnState
import com.example.smartio.databinding.ActivityControlBinding
import kotlinx.coroutines.delay
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
            } else if (isAllowedIndex(pin.toInt()) == false) {
                // 11. 허용되지 않는 번호면 보드에 보내지 않고 Toast로 알린다. 번호 확인은 12번 함수가 한다(13주차 2일차).
                Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
            } else if (isChecked) {
                // 5. 입력한 글자를 숫자(LED 번호)로 바꿔 "on 번호" 명령을 보드에 보내고, 보낸 명령을 로그에 남긴다(13주차 1일차).
                //    send는 끝에 "\n"을 붙여 차례대로 보낸다. Bleuno.client가 없으면(null) ?.에서 멈추고 아무것도 보내지 않는다.
                val index = pin.toInt()
                Bleuno.client?.send("on $index")
                binding.logText.append("on $index\n")
                // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다. 끄고 켜는 일은 15번 함수가 한다(13주차 2일차).
                pauseButtons()
            } else {
                // 6. 끄면 "off 번호" 명령을 보낸다. 5번과 같은 모양이다(13주차 1일차).
                val index = pin.toInt()
                Bleuno.client?.send("off $index")
                binding.logText.append("off $index\n")
                // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다(13주차 2일차).
                pauseButtons()
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
                    // 13. 먼저 모두 끄고, 준비됨일 때만 LED Switch·[전체 끄기]를 켠다. MainActivity 8번과 같은 방법이다(13주차 2일차).
                    //     준비되지 않았을 때 보낸 명령은 라이브러리가 버리므로 아예 누르지 못하게 한다.
                    binding.ledSwitch.isEnabled = false
                    binding.allOffButton.isEnabled = false
                    binding.pwmSeekBar.isEnabled = false // (확장) 17번 SeekBar도 같이 끈다.
                    if (state == ConnState.READY) {
                        binding.ledSwitch.isEnabled = true
                        binding.allOffButton.isEnabled = true
                        binding.pwmSeekBar.isEnabled = true // (확장)
                    }
                }
            }
        }

        // 7. [전체 끄기] 버튼: 번호 자리에 -1을 보내면 보드의 LED가 모두 꺼진다(13주차 1일차).
        binding.allOffButton.setOnClickListener {
            Bleuno.client?.send("off -1")
            binding.logText.append("off -1\n")
            // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다(13주차 2일차).
            pauseButtons()
        }

        // 17. (확장) SeekBar로 LED 0의 밝기(0~255)를 정한다. 손을 뗄 때 "pwm 0 값" 명령을 한 번 보낸다(13주차 2일차).
        //     object : SeekBar.OnSeekBarChangeListener { … }는 10주차 BroadcastReceiver와 같은 익명 객체 틀이다. 함수 세 개를 모두 적어야 한다.
        binding.pwmSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                // 끌고 있는 동안에는 보내지 않는다. 움직일 때마다 보내면 명령이 너무 많이 쌓인다.
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
                // 손을 댈 때는 할 일이 없다.
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
                val value = binding.pwmSeekBar.progress
                Bleuno.client?.send("pwm 0 $value")
                binding.logText.append("pwm 0 $value\n")
                pauseButtons()
            }
        })
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
                // 16. result가 "ok"가 아니면(err·fail) 로그 글자를 colors.xml의 빨간색으로 바꾸고, "ms"(설명) 값을 꺼내 AlertDialog로 알린다(13주차 2일차).
                //     ok면 초록색으로 되돌린다. 응답은 onStart~onStop 사이(거의 항상 화면이 보이는 동안)에만 받으므로 여기서 창을 띄운다.
                if (result != "ok") {
                    val message = BleunoMessage.message(json) ?: ""
                    binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_error))
                    AlertDialog.Builder(this)
                        .setTitle("보드가 오류를 알렸습니다")
                        .setMessage("응답: $result · $message")
                        .setPositiveButton("확인", null)
                        .show()
                } else {
                    binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_ok))
                }
            }
        }
    }

    // 10. 화면이 안 보이게 되면 응답 받기를 푼다(null). onStart의 등록과 반드시 짝을 맞춘다(13주차 1일차).
    //     10주차 배터리 Receiver의 등록·해제와 같은 규칙이다. 풀지 않으면 보이지 않는 화면의 로그를 계속 고치려 한다.
    override fun onStop() {
        super.onStop()
        Bleuno.client?.onMessage(null)
    }

    // 12. 보드에 보내도 되는 번호면 true, 아니면 false(13주차 2일차).
    //     수업 보드의 LED 번호는 0~3이고, -1은 "전체"라는 약속이다(7번 [전체 끄기]). 입력 칸은 inputType이 number라 -를 적을 수 없다.
    //     펌웨어는 번호 범위를 확인하지 않아서 이 밖의 번호를 보내면 보드가 어떻게 될지 모른다. 그래서 보내기 전에 앱이 막는다.
    private fun isAllowedIndex(index: Int): Boolean {
        if (listOf(0, 1, 2, 3).contains(index)) {
            return true
        }
        if (index == -1) {
            return true
        }
        return false
    }

    // 15. 명령을 보낸 직후 300ms 동안 LED Switch·[전체 끄기]를 꺼 두어 연달아 누르지 못하게 한다(13주차 2일차).
    //     5주차 isEnabled로 버튼 막기에 6주차 코루틴 delay를 썼다. 300ms 뒤에도 준비됨일 때만 다시 켠다(그사이 끊겼으면 13번이 끈 채로 둔다).
    private fun pauseButtons() {
        binding.ledSwitch.isEnabled = false
        binding.allOffButton.isEnabled = false
        binding.pwmSeekBar.isEnabled = false // (확장)
        lifecycleScope.launch {
            delay(300)
            if (Bleuno.client?.isReady == true) {
                binding.ledSwitch.isEnabled = true
                binding.allOffButton.isEnabled = true
                binding.pwmSeekBar.isEnabled = true // (확장)
            }
        }
    }
}
