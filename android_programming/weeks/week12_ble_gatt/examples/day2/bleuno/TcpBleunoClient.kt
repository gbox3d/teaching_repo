package com.example.smartio.bleuno

import android.os.Handler
import android.os.Looper
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import org.json.JSONObject
import java.io.BufferedReader
import java.io.BufferedWriter
import java.io.IOException
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress
import java.net.InetSocketAddress
import java.net.Socket
import java.net.SocketTimeoutException
import java.util.concurrent.Executors

// PC에서 돌리는 시뮬레이터(tools/bleuno-sim)와 Wi-Fi(TCP)로 이야기하는 클라이언트.
// 보드와 블루투스 없이 RealBleunoClient와 같은 명령·같은 JSON으로 연습한다. 앱 코드는 그대로다.
//   검색: UDP로 "bleuno?"를 뿌리고, 답한 시뮬레이터마다 onFound(이름, "ip:포트"), timeoutMs 뒤 onFinished
//   연결: connect("10.0.2.2:8266") → 연결 중 → 서비스 확인 중 → (첫 줄 hello를 받으면) 준비됨
//         3초 안에 연결되지 않거나, 연결된 뒤 3초 안에 첫 줄이 오지 않으면 "끊김"
//         (연결 3초는 IP 주소 기준이다. 이름을 넣으면 이름을 IP로 바꾸는 시간은 이 3초에 들지 않는다)
//   전송: send → 한 줄 쓰기 → 응답 JSON 한 줄이 onMessage로
//   끊김: 시뮬레이터를 끄거나 화면의 [연결 끊기]를 누르면 "끊김"
// 소켓 일은 Thread에서 하고, 상태 변경과 리스너 호출은 모두 메인 스레드 Handler로 전달한다.
// 모든 단계는 Log.d("TCP", …)로 남기므로 Logcat에서 태그 TCP로 순서를 볼 수 있다.
class TcpBleunoClient : BleunoClient {

    companion object {
        const val TAG = "TCP"
        const val DEFAULT_PORT = 8266              // 명령·응답 TCP 포트 (주소에 포트가 없으면 이 값)
        const val DISCOVERY_PORT = 8267            // 검색용 UDP 포트
        const val DISCOVERY_QUERY = "bleuno?"      // 검색할 때 보내는 글자
        const val EMULATOR_HOST = "10.0.2.2"       // 에뮬레이터에서 보는 PC 주소
        const val CONNECT_TIMEOUT = 3000           // connect 기다리는 시간(ms)
        const val HELLO_TIMEOUT = 3000             // 연결된 뒤 첫 줄(hello)을 기다리는 시간(ms)
        const val RECEIVE_TIMEOUT = 500            // UDP 응답을 한 번에 기다리는 시간(ms)
    }

    // 소켓 스레드에서 온 결과는 항상 이 Handler로 메인 스레드에서 처리한다
    private val mainHandler = Handler(Looper.getMainLooper())
    // 검색 시간 초과 전용 Handler (removeCallbacksAndMessages로 검색 예약만 취소하려고 따로 둔다)
    private val scanHandler = Handler(Looper.getMainLooper())

    private val _connectionState = MutableStateFlow(ConnState.DISCONNECTED)
    override val connectionState: StateFlow<String> = _connectionState
    override val isReady: Boolean
        get() = _connectionState.value == ConnState.READY

    // ---- 검색 ----
    @Volatile private var isScanning = false
    @Volatile private var scanSocket: DatagramSocket? = null
    @Volatile private var scanId = 0                 // 검색 회차. startScan·stopScan마다 1 늘린다. 회차가 다른 검색 스레드는 곧 끝난다
    private var onFoundListener: ((BleunoDevice) -> Unit)? = null
    private var onFinishedListener: (() -> Unit)? = null
    private val foundAddresses = HashSet<String>()   // 같은 시뮬레이터를 두 번 알리지 않기 위한 주소 집합

    // ---- 연결 ----
    @Volatile private var socket: Socket? = null     // 지금 회차의 소켓. 메인 스레드에서만 넣고 뺀다
    @Volatile private var writer: BufferedWriter? = null
    @Volatile private var connectId = 0              // 연결 회차. connect()·disconnect()·끊김 처리마다 1 늘린다. 회차가 다른 스레드의 결과는 버린다

    // ---- 전송 ----
    // 명령을 순서대로 하나씩 쓴다. 이 클라이언트는 앱 전체에 하나만 쓴다(Bleuno.client). 그래서 따로 닫지 않는다.
    private val sendExecutor = Executors.newSingleThreadExecutor()

    private var messageListener: ((String) -> Unit)? = null

    // ---------------------------------------------------------------- 검색

    override fun startScan(timeoutMs: Long, onFound: (BleunoDevice) -> Unit, onFinished: () -> Unit) {
        if (isScanning) stopScan()
        foundAddresses.clear()
        onFoundListener = onFound
        onFinishedListener = onFinished
        val id = ++scanId
        isScanning = true
        Log.d(TAG, "startScan: ${timeoutMs}ms 동안 UDP $DISCOVERY_PORT 로 \"$DISCOVERY_QUERY\" 검색")
        Thread {
            runDiscovery(id)
        }.start()
        scanHandler.postDelayed({
            Log.d(TAG, "scan timeout (${timeoutMs}ms)")
            stopScan()
        }, timeoutMs)
    }

    // 지금 회차의 검색인지 본다. stopScan()이나 새 startScan()이 불렸으면 false다.
    private fun isCurrentScan(id: Int): Boolean {
        return isScanning && id == scanId
    }

    // 검색 스레드. "bleuno?"를 두 곳에 보내고, 멈출 때까지 응답을 받는다.
    private fun runDiscovery(id: Int) {
        var udp: DatagramSocket? = null
        try {
            udp = DatagramSocket()
            udp.broadcast = true
            udp.soTimeout = RECEIVE_TIMEOUT
            scanSocket = udp
            // 소켓을 넣기 전에 stopScan()이 불렸으면 stopScan()은 닫을 소켓이 없었다. 회차를 보고 여기서 끝낸다.
            if (!isCurrentScan(id)) return
            val query = DISCOVERY_QUERY.toByteArray(Charsets.UTF_8)
            // 같은 Wi-Fi의 PC(실기기)와 에뮬레이터를 띄운 PC, 두 곳에 보낸다
            for (host in listOf("255.255.255.255", EMULATOR_HOST)) {
                try {
                    udp.send(DatagramPacket(query, query.size, InetAddress.getByName(host), DISCOVERY_PORT))
                    Log.d(TAG, "UDP 보냄: $host:$DISCOVERY_PORT \"$DISCOVERY_QUERY\"")
                } catch (e: IOException) {
                    Log.w(TAG, "UDP 보내기 실패 ($host): $e")
                }
            }
            val buffer = ByteArray(512)
            while (isCurrentScan(id)) {
                val packet = DatagramPacket(buffer, buffer.size)
                try {
                    udp.receive(packet)
                } catch (e: SocketTimeoutException) {
                    continue   // 500ms 동안 응답이 없었다. 멈출지 확인하고 다시 기다린다
                }
                val text = String(packet.data, packet.offset, packet.length, Charsets.UTF_8)
                val ip = packet.address.hostAddress ?: continue
                Log.d(TAG, "UDP 받음: $ip $text")
                val json = try {
                    JSONObject(text)
                } catch (e: Exception) {
                    Log.w(TAG, "UDP 응답이 JSON이 아님: $text")
                    continue
                }
                val name = json.optString("name", "")
                if (name.isEmpty()) continue
                val port = json.optInt("port", DEFAULT_PORT)
                val found = BleunoDevice(name, "$ip:$port", 0)
                mainHandler.post {
                    if (!isCurrentScan(id)) return@post
                    if (!foundAddresses.add(found.address)) return@post   // 이미 알린 시뮬레이터
                    Log.d(TAG, "onFound: ${found.name} ${found.address}")
                    onFoundListener?.invoke(found)
                }
            }
        } catch (e: IOException) {
            // stopScan()이 소켓을 닫으면 receive가 여기로 풀린다. 검색 중이었다면 끝낸다.
            scanFailed(id, e)
        } catch (e: SecurityException) {
            // INTERNET 권한이 없으면 여기로 온다. 앱을 끝내지 않고 검색만 끝낸다.
            scanFailed(id, e)
        } finally {
            udp?.close()
            if (scanSocket === udp) scanSocket = null
        }
    }

    // 검색 스레드에서 오류가 났다. 지금 회차의 검색이면 메인 스레드에서 검색을 끝낸다.
    private fun scanFailed(id: Int, e: Exception) {
        if (isCurrentScan(id)) {
            Log.w(TAG, "UDP 검색 중 오류: $e")
            mainHandler.post { if (id == scanId) stopScan() }
        }
    }

    override fun stopScan() {
        if (!isScanning) return
        isScanning = false
        scanId++              // 회차를 올린다. 검색 스레드는 회차가 바뀐 것을 보고 곧 끝난다
        scanHandler.removeCallbacksAndMessages(null)
        scanSocket?.close()   // 검색 스레드의 receive를 풀어 준다
        Log.d(TAG, "stopScan: 찾은 시뮬레이터 ${foundAddresses.size}개")
        val finished = onFinishedListener
        onFoundListener = null
        onFinishedListener = null
        finished?.invoke()
    }

    // ---------------------------------------------------------------- 연결

    override fun connect(address: String) {
        // 새 회차로 시작하고, 이전 연결이 남아 있으면 정리한다.
        // disconnect()처럼 회차를 먼저 올린다. 그래야 소켓이 닫혀 풀린 지난 연결 스레드가 회차가 바뀐 것을 보고 Log.d만 남긴다.
        val id = ++connectId
        closeSocket()

        // "host:port". 포트가 없으면 8266
        val host = address.substringBefore(":").trim()
        val portText = address.substringAfter(":", "").trim()
        val port = if (portText.isEmpty()) DEFAULT_PORT else (portText.toIntOrNull() ?: -1)
        if (host.isEmpty() || port !in 1..65535) {
            // ":" 앞에 IP가 있어야 하고, 포트는 1~65535 숫자여야 한다. 잘못된 주소로는 연결하지 않고, 다른 실패와 같이 연결 중 → 끊김 순서로 둔다.
            // IP가 빈 채(예: ":8266")로 연결하면 PC가 아니라 이 기기 자신(localhost)에 붙으려 한다. 그래서 여기서 막는다.
            // StateFlow는 같은 값을 두 번 내보내지 않는다. 연결 중을 거쳐야 이미 끊김일 때도 화면이 끊김을 다시 받는다.
            if (host.isEmpty()) {
                Log.w(TAG, "connect: IP가 없음 (\"$address\") → 끊김")
            } else {
                Log.w(TAG, "connect: 포트가 잘못됨 (\"$address\") → 끊김")
            }
            _connectionState.value = ConnState.CONNECTING
            endConnection(id)
            return
        }

        // 소켓은 여기(메인 스레드)서 만들어 보관한 뒤 연결 스레드에 넘긴다.
        // Socket()은 만들기만 하고 네트워크는 쓰지 않는다. 보관해 두었으므로 disconnect()가 언제든 닫을 수 있다.
        val s = Socket()
        socket = s
        _connectionState.value = ConnState.CONNECTING
        Log.d(TAG, "connect: $host:$port (${CONNECT_TIMEOUT}ms 안에 연결)")
        Thread {
            runConnection(id, s, host, port)
        }.start()
    }

    // 연결 스레드. 연결 → 첫 줄(hello) → 준비됨 → 이후 줄마다 onMessage. 끊어지면 끊김.
    private fun runConnection(id: Int, s: Socket, host: String, port: Int) {
        try {
            s.connect(InetSocketAddress(host, port), CONNECT_TIMEOUT)
            Log.d(TAG, "connected: $host:$port → 서비스 확인 중")

            val reader = BufferedReader(InputStreamReader(s.getInputStream(), Charsets.UTF_8))
            val w = BufferedWriter(OutputStreamWriter(s.getOutputStream(), Charsets.UTF_8))
            // writer는 회차가 같을 때만 넣는다. 메인 스레드에서 확인하므로 그사이 disconnect()가 불려도 섞이지 않는다.
            mainHandler.post {
                if (id == connectId) {
                    writer = w
                    _connectionState.value = ConnState.DISCOVERING
                }
            }

            // 첫 줄(hello)은 3초만 기다린다. 다른 포트(예: HTTP API :8080)에 붙으면 첫 줄이 오지 않는다.
            s.soTimeout = HELLO_TIMEOUT
            val first = try {
                reader.readLine()
            } catch (e: SocketTimeoutException) {
                Log.w(TAG, "hello 없음: ${HELLO_TIMEOUT}ms 안에 첫 줄이 오지 않았다. 포트가 $DEFAULT_PORT 인지 확인한다 → 끊김")
                endConnection(id)
                return
            }
            if (first == null) {
                Log.d(TAG, "EOF: 첫 줄을 받기 전에 상대가 연결을 닫음")
                endConnection(id)
                return
            }
            // 첫 줄을 받았다. 이제부터는 시간 제한 없이 기다린다.
            // keepAlive는 상대가 소리 없이 사라졌을 때(PC가 잠들거나 Wi-Fi가 바뀜) 그것을 알아내려고 켠다.
            // 기본값으로는 2시간 동안 조용해야 확인을 시작하므로, 그런 끊김은 아주 늦게 안다.
            s.soTimeout = 0
            s.keepAlive = true
            Log.d(TAG, "첫 줄 받음 → 준비됨: $first")
            mainHandler.post { if (id == connectId) _connectionState.value = ConnState.READY }
            // hello 줄은 앱에 전달하지 않는다. 첫 줄이 hello가 아니면 그 줄도 전달한다.
            if (!isHello(first)) deliver(id, first)

            while (true) {
                val line = reader.readLine() ?: break   // null이면 상대가 닫았다(EOF)
                deliver(id, line)
            }
            Log.d(TAG, "EOF: 상대가 연결을 닫음")
            endConnection(id)
        } catch (e: IOException) {
            // 연결 실패(타임아웃·거부), 읽기 중 오류, disconnect()가 소켓을 닫은 경우
            connectionFailed(id, e)
        } catch (e: IllegalArgumentException) {
            // 주소를 만들 수 없는 경우. 앱을 끝내지 않고 끊김으로 둔다.
            connectionFailed(id, e)
        } catch (e: SecurityException) {
            // INTERNET 권한이 없는 경우. 앱을 끝내지 않고 끊김으로 둔다.
            connectionFailed(id, e)
        } finally {
            closeQuietly(s)
        }
    }

    // 연결 스레드에서 오류가 났다. 지난 회차(disconnect()·새 connect()·끊김 처리가 닫은 소켓)면 Log.d만 남기고 상태는 바꾸지 않는다.
    private fun connectionFailed(id: Int, e: Exception) {
        if (id == connectId) {
            Log.w(TAG, "connect/read 오류: $e")
        } else {
            Log.d(TAG, "지난 연결 스레드 끝남: $e")
        }
        endConnection(id)
    }

    // 연결이 끝났다(시뮬레이터 종료·연결 실패·hello 없음·write 오류·잘못된 주소). 지금 회차일 때만 끊김으로 둔다.
    // 끊김으로 둘 때 회차를 올린다. write 오류 뒤 여기서 소켓을 닫으면 읽기 스레드가 풀리는데, 그 결과는 지난 회차라 Log.d만 남는다.
    // disconnect()는 회차를 올리므로, 사용자가 끊은 뒤에는 여기서 아무것도 바꾸지 않는다(연결 안 됨 그대로).
    private fun endConnection(id: Int) {
        mainHandler.post {
            if (id != connectId) return@post
            connectId++   // 이 회차는 끝났다. 소켓을 닫기 전에 올려야 풀린 스레드가 지난 회차로 본다
            Log.d(TAG, "connection ended → 끊김")
            closeSocket()
            _connectionState.value = ConnState.LOST
        }
    }

    // {"event":"hello", …} 줄인지 본다. JSON이 아니면 hello가 아니다.
    private fun isHello(line: String): Boolean {
        return try {
            JSONObject(line).optString("event", "") == "hello"
        } catch (e: Exception) {
            false
        }
    }

    // 지금 회차의 소켓을 닫는다. 연결 스레드의 readLine이 풀려 끝난다. 두 번 불려도 괜찮다. 메인 스레드에서 부른다.
    private fun closeSocket() {
        val s = socket
        socket = null
        writer = null
        if (s != null) closeQuietly(s)
    }

    private fun closeQuietly(s: Socket) {
        try {
            s.close()
        } catch (e: IOException) {
            Log.w(TAG, "socket.close 오류: $e")
        }
    }

    override fun disconnect() {
        connectId++   // 회차를 올린다. 지금 연결 스레드가 보내는 결과(상태·메시지)는 모두 버려진다
        if (socket == null) {
            Log.d(TAG, "disconnect: 연결 없음 → 연결 안 됨")
        } else {
            Log.d(TAG, "disconnect: socket.close() → 연결 안 됨")
            closeSocket()
        }
        _connectionState.value = ConnState.DISCONNECTED
    }

    // 받은 한 줄을 메인 스레드에서 리스너에 전달한다. 지난 회차의 줄은 버린다.
    private fun deliver(id: Int, line: String) {
        Log.d(TAG, "received: $line")
        mainHandler.post {
            if (id == connectId) messageListener?.invoke(line)
        }
    }

    // ---------------------------------------------------------------- 전송

    override fun send(command: String) {
        if (!isReady) {
            Log.w(TAG, "send: 준비되지 않아 무시함 (\"$command\", 상태=${_connectionState.value})")
            return
        }
        val w = writer
        if (w == null) {
            Log.w(TAG, "send: writer 없음 → 무시함 (\"$command\")")
            return
        }
        val id = connectId
        // RealBleunoClient처럼 끝에 언제나 "\n"을 붙인다. 빈 글자도 거르지 않는다(빈 줄 하나를 보낸다).
        val text = command + "\n"
        // 단일 스레드 executor라서 보낸 순서대로 하나씩 쓴다
        sendExecutor.execute {
            try {
                w.write(text)
                w.flush()
                Log.d(TAG, "sent: \"${text.trim()}\"")
            } catch (e: IOException) {
                Log.w(TAG, "write 오류: $e → 끊김")
                endConnection(id)
            }
        }
    }

    override fun onMessage(listener: ((String) -> Unit)?) {
        messageListener = listener
    }
}
