package com.example.smartio

import android.os.Bundle
import android.widget.ArrayAdapter
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
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class ControlActivity : AppCompatActivity() {
    // ViewBinding 틀: activity_control.xml → ActivityControlBinding
    private lateinit var binding: ActivityControlBinding

    // 14주차 1일차: 입력 이력 목록(시각과 값 한 줄씩)과 그 목록을 ListView에 보여 주는 어댑터.
    // 응답을 받는 onStart(8번)에서도 써야 하므로 onCreate 밖, 클래스 안에 둔다. 어댑터는 onCreate에서 만든다(18번). lateinit은 binding과 같은 틀이다.
    // 이 목록은 이 화면이 가진 것이라, 회전해서 화면이 새로 만들어지면 빈 목록으로 다시 시작한다(받기도 27번 onStop에서 꺼진다).
    private val history = mutableListOf<String>()
    private lateinit var historyAdapter: ArrayAdapter<String>

    // 14주차 1일차: [온습도 받기 시작]이 시작한 반복 코루틴. [중지]에서 취소하려고 보관한다(6주차 scanJob과 같다). 아직 없으면 null이다.
    private var inputJob: Job? = null

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
                    // 26. 상태가 바뀌면(끊김 등) 온습도 받기를 멈추고, 준비됨일 때만 [온습도 받기 시작]을 켠다. 25번 함수가 한다(14주차 1일차).
                    stopInput()
                    // 29. 끊겼으면 Toast로 알린다. [재연결]은 연결 화면에 있으므로 [뒤로]로 돌아가라고 안내한다(14주차 1일차).
                    //     collect 틀 안에서는 this가 Activity가 아니어서 Toast는 30번 함수로 띄운다. 끊김인 채로 이 화면이 다시 보이면(회전 등) 또 뜬다.
                    if (state == ConnState.LOST) {
                        showLostToast()
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

        // 18. 입력 이력 ListView에 어댑터를 붙인다. 11주차 장치 목록(MainActivity 16번)과 같은 틀이다(14주차 1일차).
        historyAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, history)
        binding.inputList.adapter = historyAdapter

        // 19. [온습도 받기 시작] 버튼: 3초마다 "dht11" 명령을 보낸다. 응답은 onStart의 23번이 받아 이력에 넣는다(14주차 1일차).
        //     6주차 카운트다운처럼 lifecycleScope.launch 안에서 delay로 기다린다. while (isActive)는 "취소되지 않았으면 계속 되풀이한다"는 뜻이다.
        binding.inputStartButton.setOnClickListener {
            binding.inputStartButton.isEnabled = false
            binding.inputStopButton.isEnabled = true
            inputJob = lifecycleScope.launch {
                while (isActive) {
                    Bleuno.client?.send("dht11")
                    delay(3000)
                }
            }
        }

        // 20. [중지] 버튼: 반복 코루틴을 취소하고 버튼을 되돌린다. 25번 함수가 한다(14주차 1일차).
        binding.inputStopButton.setOnClickListener {
            stopInput()
        }

        // 28. 입력 이력의 한 줄을 누르면 그 줄을 띄어쓰기(" ")로 나눠 받은 시각과 값을 Toast로 보여 준다(14주차 1일차).
        //     history[position]은 history.get(position)과 같다(누른 줄 번호로 꺼내기). split(" ")은 글자를 " "가 있는 곳마다 잘라 목록으로 돌려준다.
        //     "12:00:03 [24.5,40.0]" → [0]은 "12:00:03"(시각), [1]은 "[24.5,40.0]"(값). 번호는 0부터 센다. 이력 줄은 늘 "시각 값"이라 [1]까지 있다(24번).
        binding.inputList.setOnItemClickListener { _, _, position, _ ->
            val parts = history[position].split(" ")
            val time = parts[0]
            val value = parts[1]
            Toast.makeText(this, "받은 시각: $time · 값: $value", Toast.LENGTH_SHORT).show()
        }
    }

    // 8. 화면이 보이기 시작하면 보드가 보내는 응답(JSON 한 줄)을 받도록 등록한다(13주차 1일차).
    //    명령 하나마다 응답이 한 줄씩 온다. { json -> }는 메인 스레드에서 불리므로 안에서 View를 바로 바꿔도 된다.
    override fun onStart() {
        super.onStart()
        Bleuno.client?.onMessage { json ->
            // 9. JSON에서 "result"(ok·err·fail) 값을 꺼내 보고, 명령의 응답이면 받은 JSON 한 줄을 그대로 로그에 남긴다(13주차 1일차).
            //    로그 예: 응답: {"result":"ok","ms":"led(s) on"}. result가 없는 줄은 명령의 응답이 아니다(가짜 보드가 10초마다 보내는 입력 이벤트, 14주차에 다룬다). 로그에 넣지 않는다.
            //    14주차 1일차: 입력 이벤트(22번)와 dht11 응답(23번)은 명령 로그 대신 입력 이력에 넣는다. 그래서 if (result != null) 앞에 else를 붙였다.
            val result = BleunoMessage.result(json)
            // 21. "event"(보드가 먼저 보낸 이벤트 종류)와 "value"(값)도 꺼낸다. 그 키가 없는 줄이면 null이다(14주차 1일차).
            val event = BleunoMessage.event(json)
            val value = BleunoMessage.value(json)
            if (event == "input") {
                // 22. event가 "input"이면 보드가 먼저 보낸 입력 이벤트다(예: {"event":"input","index":0,"value":1}). "입력=값"으로 이력에 넣는다(14주차 1일차).
                //     입력 이벤트에도 "value"가 들어 있으므로 23번보다 먼저 확인한다.
                //     28번이 이력 줄을 띄어쓰기로 나누므로 "입력=1"처럼 띄어쓰기 없이 붙여 적는다.
                addHistory("입력=$value")
            } else if (value != null) {
                // 23. value가 있으면 dht11 응답이다(예: {"result":"ok","value":"[24.5,40.0]"}). 값만 "시각 값" 한 줄로 이력에 넣는다(14주차 1일차).
                addHistory(value)
            } else if (result != null) {
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
        // 27. 응답을 받지 않는 동안에는 온습도 요청도 보내지 않는다. [중지]를 누른 것과 같다(14주차 1일차).
        stopInput()
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

    // 24. 받은 글자 앞에 지금 시각을 붙여 입력 이력 맨 아래에 한 줄 넣고, 어댑터에 알려 화면을 고친다(14주차 1일차).
    //     SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())는 지금 시각을 "12:00:03"(시:분:초) 글자로 만드는 틀이다.
    //     activity_control.xml의 inputList에 transcriptMode="alwaysScroll"을 적어 두어서 새 줄이 들어오면 목록이 맨 아래로 내려간다.
    private fun addHistory(text: String) {
        val time = SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())
        history.add("$time $text")
        historyAdapter.notifyDataSetChanged()
    }

    // 25. 온습도 받기를 멈추고 두 버튼을 되돌린다. [중지](20번)·상태가 바뀔 때(26번)·onStop(27번)이 함께 쓴다(14주차 1일차).
    //     6주차 job.cancel()로 반복을 멈춘다. 아직 시작한 적이 없으면(null) ?.에서 멈춘다. [온습도 받기 시작]은 준비됨일 때만 켠다(15번과 같은 방법).
    private fun stopInput() {
        inputJob?.cancel()
        binding.inputStartButton.isEnabled = false
        binding.inputStopButton.isEnabled = false
        if (Bleuno.client?.isReady == true) {
            binding.inputStartButton.isEnabled = true
        }
    }

    // 30. 제어 화면에서 끊겼다고 알리는 Toast. 29번(collect 안)에서 부른다(14주차 1일차).
    //     연결 화면 46번과 같은 이유로 함수로 뺐다. 함수 안의 this는 Activity라서 Toast.makeText(this, …)를 그대로 쓴다.
    private fun showLostToast() {
        Toast.makeText(this, "연결이 끊겼습니다. [뒤로] → [재연결]을 누르세요", Toast.LENGTH_SHORT).show()
    }
}
