package com.example.smartio.bleuno

import android.os.Handler
import android.os.Looper
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import org.json.JSONObject

// 보드 없이 앱을 만들고 시험할 때 쓰는 가짜 클라이언트.
// RealBleunoClient와 같은 순서·같은 JSON으로 답하되, 시간은 모두 메인 스레드 Handler.postDelayed로 흉내 낸다.
//   검색: 1초 뒤 ESP32_BLE_FAKE1, 2초 뒤 ESP32_BLE_FAKE2 발견, timeoutMs 뒤 onFinished
//   연결: connect → 연결 중(1초) → 서비스 확인 중(1초) → 준비됨
//   전송: send → 300ms 뒤 펌웨어와 같은 JSON 응답
//   이벤트: 준비됨 상태에서 10초마다 {"event":"input","index":0,"value":0|1}
//   simulateLost(): 보드 전원이 꺼진 것처럼 "끊김"으로 만든다
class FakeBleunoClient : BleunoClient {

    companion object {
        const val TAG = "BLE"
        const val FOUND_DELAY_1 = 1000L
        const val FOUND_DELAY_2 = 2000L
        const val CONNECT_DELAY = 1000L
        const val DISCOVER_DELAY = 1000L
        const val RESPONSE_DELAY = 300L
        const val INPUT_EVENT_INTERVAL = 10000L
        const val LED_COUNT = 4          // 수업 보드의 LED 개수 (인덱스 0~3)
    }

    private val fakeDevices = listOf(
        BleunoDevice("ESP32_BLE_FAKE1", "00:11:22:33:44:01", -50),
        BleunoDevice("ESP32_BLE_FAKE2", "00:11:22:33:44:02", -70),
    )

    // 용도별로 Handler를 나눠서 removeCallbacksAndMessages(null)로 그 용도의 예약만 취소한다
    private val scanHandler = Handler(Looper.getMainLooper())
    private val connectHandler = Handler(Looper.getMainLooper())
    private val sendHandler = Handler(Looper.getMainLooper())
    private val eventHandler = Handler(Looper.getMainLooper())

    private val _connectionState = MutableStateFlow(ConnState.DISCONNECTED)
    override val connectionState: StateFlow<String> = _connectionState
    override val isReady: Boolean
        get() = _connectionState.value == ConnState.READY

    private var isScanning = false
    private var onFinishedListener: (() -> Unit)? = null
    private var messageListener: ((String) -> Unit)? = null

    private var inputValue = 0     // 입력 이벤트의 value, 10초마다 0/1 토글
    private var dhtCount = 0       // dht11 응답 값을 조금씩 바꾸기 위한 횟수

    // ---------------------------------------------------------------- 검색

    override fun startScan(timeoutMs: Long, onFound: (BleunoDevice) -> Unit, onFinished: () -> Unit) {
        if (isScanning) stopScan()
        isScanning = true
        onFinishedListener = onFinished
        Log.d(TAG, "startScan(가짜): ${timeoutMs}ms 동안 검색")
        scanHandler.postDelayed({
            Log.d(TAG, "onScanResult(가짜): ${fakeDevices[0].name}")
            onFound(fakeDevices[0])
        }, FOUND_DELAY_1)
        scanHandler.postDelayed({
            Log.d(TAG, "onScanResult(가짜): ${fakeDevices[1].name}")
            onFound(fakeDevices[1])
        }, FOUND_DELAY_2)
        scanHandler.postDelayed({
            Log.d(TAG, "scan timeout(가짜) (${timeoutMs}ms)")
            stopScan()
        }, timeoutMs)
    }

    override fun stopScan() {
        if (!isScanning) return
        isScanning = false
        scanHandler.removeCallbacksAndMessages(null)
        Log.d(TAG, "stopScan(가짜)")
        val finished = onFinishedListener
        onFinishedListener = null
        finished?.invoke()
    }

    // ---------------------------------------------------------------- 연결

    override fun connect(address: String) {
        connectHandler.removeCallbacksAndMessages(null)
        eventHandler.removeCallbacksAndMessages(null)
        Log.d(TAG, "connectGatt(가짜): $address")
        _connectionState.value = ConnState.CONNECTING
        connectHandler.postDelayed({
            Log.d(TAG, "onConnectionStateChange(가짜): STATE_CONNECTED → 서비스 확인 중")
            _connectionState.value = ConnState.DISCOVERING
            connectHandler.postDelayed({
                Log.d(TAG, "onServicesDiscovered(가짜) → onDescriptorWrite → 준비됨")
                _connectionState.value = ConnState.READY
                scheduleInputEvent()
            }, DISCOVER_DELAY)
        }, CONNECT_DELAY)
    }

    override fun disconnect() {
        cancelAll()
        Log.d(TAG, "disconnect(가짜) → 연결 안 됨")
        _connectionState.value = ConnState.DISCONNECTED
    }

    // 보드 전원이 꺼진 상황을 흉내 낸다. 상태가 "끊김"이 된다.
    fun simulateLost() {
        cancelAll()
        Log.d(TAG, "simulateLost(가짜) → 끊김")
        _connectionState.value = ConnState.LOST
    }

    private fun cancelAll() {
        connectHandler.removeCallbacksAndMessages(null)
        sendHandler.removeCallbacksAndMessages(null)
        eventHandler.removeCallbacksAndMessages(null)
    }

    // 준비됨 상태인 동안 10초마다 입력 이벤트를 보낸다 (보드 버튼 입력 가안 형식)
    private fun scheduleInputEvent() {
        eventHandler.postDelayed({
            if (!isReady) return@postDelayed
            inputValue = 1 - inputValue
            val json = JSONObject()
            json.put("event", "input")
            json.put("index", 0)
            json.put("value", inputValue)
            deliver(json.toString())
            scheduleInputEvent()
        }, INPUT_EVENT_INTERVAL)
    }

    // ---------------------------------------------------------------- 전송

    override fun send(command: String) {
        if (!isReady) {
            Log.w(TAG, "send(가짜): 준비되지 않아 무시함 (\"$command\", 상태=${_connectionState.value})")
            return
        }
        Log.d(TAG, "writeCharacteristic(가짜): \"$command\"")
        // 펌웨어처럼 "\n"으로 나눈 명령마다 응답 한 줄씩 보낸다
        val lines = command.split("\n").filter { it.isNotBlank() }
        for (line in lines) {
            sendHandler.postDelayed({
                deliver(respond(line.trim()))
            }, RESPONSE_DELAY)
        }
    }

    override fun onMessage(listener: ((String) -> Unit)?) {
        messageListener = listener
    }

    private fun deliver(json: String) {
        Log.d(TAG, "onCharacteristicChanged(가짜): $json")
        messageListener?.invoke(json)
    }

    // 펌웨어 parseCmd와 같은 규칙으로 응답 JSON을 만든다
    private fun respond(line: String): String {
        val tokens = line.split(Regex("\\s+")).filter { it.isNotEmpty() }
        val res = JSONObject()
        if (tokens.isEmpty()) {
            res.put("result", "fail")
            res.put("ms", "need command")
            return res.toString()
        }
        when (tokens[0]) {
            "on" -> {
                if (tokens.size > 1) {
                    res.put("result", "ok")
                    res.put("ms", "led(s) on")
                } else {
                    res.put("result", "err")
                    res.put("ms", "need pin index")
                }
            }
            "off" -> {
                if (tokens.size > 1) {
                    res.put("result", "ok")
                    res.put("ms", "led(s) off")
                } else {
                    res.put("result", "err")
                    res.put("ms", "need pin index")
                }
            }
            "pwm" -> {
                if (tokens.size > 2) {
                    val index = tokens[1].toIntOrNull() ?: 0
                    val value = tokens[2].toIntOrNull() ?: 0
                    if (index < 0) {
                        res.put("result", "ok")
                        res.put("ms", "pwm set")
                    } else if (index >= LED_COUNT) {
                        res.put("result", "err")
                        res.put("ms", "pwm pin index error")
                    } else if (value < 0 || value > 255) {
                        res.put("result", "err")
                        res.put("ms", "pwm value range 0~255")
                    } else {
                        res.put("result", "ok")
                        res.put("ms", "pwm set")
                    }
                } else {
                    res.put("result", "err")
                    res.put("ms", "need pin index and pwm value")
                }
            }
            "dht11" -> {
                // 매번 조금씩 다른 값을 돌려줘서 이력 목록에서 구분되게 한다: 24.5/40.0 → 25.0/41.0 → 25.5/42.0 → 반복
                val step = dhtCount % 3
                dhtCount++
                val temperature = 24.5 + step * 0.5
                val humidity = 40.0 + step * 1.0
                res.put("result", "ok")
                res.put("value", String.format(java.util.Locale.US, "[%.1f,%.1f]", temperature, humidity))
            }
            "about" -> {
                res.put("result", "ok")
                res.put("os", "cronos-v1")
                res.put("app", "BLEuno")
                res.put("version", "1.0.5_dev")
                res.put("author", "gbox3d")
                res.put("chipid", 1234567890L)
            }
            "blink" -> {
                res.put("result", "ok")
                res.put("ms", "led blink")
            }
            "stopblk" -> {
                res.put("result", "ok")
                res.put("ms", "led stop blink")
            }
            else -> {
                res.put("result", "fail")
                res.put("ms", "unknown command")
            }
        }
        return res.toString()
    }
}
