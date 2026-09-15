package com.example.smartio.bleuno

import android.annotation.SuppressLint
import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCallback
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothGattDescriptor
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothProfile
import android.bluetooth.BluetoothStatusCodes
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.Context
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.util.UUID

// 실제 bleuno 보드와 BluetoothGatt로 이야기하는 클라이언트.
// 콜백 사슬: startScan → (timeoutMs 뒤) stopScan → connectGatt → onConnectionStateChange(CONNECTED)
//   → requestMtu(185) → onMtuChanged → discoverServices → onServicesDiscovered
//   → setCharacteristicNotification + CCCD 쓰기 → onDescriptorWrite → 준비됨
//   → writeCharacteristic → onCharacteristicWrite(다음 명령) / onCharacteristicChanged(응답)
// 모든 콜백은 Log.d("BLE", …)로 남기므로 Logcat에서 태그 BLE로 순서를 볼 수 있다.
// 권한 검사는 PermissionHelper.hasAll로 하고, 없으면 로그만 남기고 아무것도 하지 않는다(요청은 앱 책임).
@SuppressLint("MissingPermission")
class RealBleunoClient(
    context: Context,
    private val nameFilter: String = "ESP32_BLE",   // 이 문자열로 시작하는 이름의 기기만 onFound에 알린다
) : BleunoClient {

    companion object {
        const val TAG = "BLE"
        val SERVICE_UUID: UUID = UUID.fromString("c6f8b088-2af8-4388-8364-ca2a907bdeb8")
        val CHARACTERISTIC_UUID: UUID = UUID.fromString("f6aa83ca-de53-46b4-bdea-28a7cb57942e")
        val CCCD_UUID: UUID = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")
        const val MTU = 185
    }

    private val appContext: Context = context.applicationContext
    private val bluetoothManager: BluetoothManager? =
        appContext.getSystemService(Context.BLUETOOTH_SERVICE) as? BluetoothManager

    // 콜백은 바인더 스레드에서 오므로, 화면과 리스너에는 항상 이 Handler로 메인 스레드에서 전달한다
    private val mainHandler = Handler(Looper.getMainLooper())
    // 검색 시간 초과 전용 Handler (removeCallbacksAndMessages로 검색 것만 취소하기 위해 분리)
    private val scanHandler = Handler(Looper.getMainLooper())

    private val _connectionState = MutableStateFlow(ConnState.DISCONNECTED)
    override val connectionState: StateFlow<String> = _connectionState
    override val isReady: Boolean
        get() = _connectionState.value == ConnState.READY

    // ---- 검색 ----
    private var isScanning = false
    private var onFoundListener: ((BleunoDevice) -> Unit)? = null
    private var onFinishedListener: (() -> Unit)? = null
    private val foundAddresses = HashSet<String>()   // 같은 기기를 두 번 알리지 않기 위한 주소 집합

    // ---- 연결 ----
    private var gatt: BluetoothGatt? = null
    private var characteristic: BluetoothGattCharacteristic? = null
    private var userDisconnect = false               // disconnect()를 사용자가 불렀는지

    // ---- 전송 큐 ----
    private val queue = ArrayDeque<String>()         // 아직 보내지 않은 명령("\n" 포함)
    private var writing = false                      // onCharacteristicWrite를 기다리는 중이면 true

    private var messageListener: ((String) -> Unit)? = null

    // ---------------------------------------------------------------- 검색

    private val scanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            val device = result.device ?: return
            val name = result.scanRecord?.deviceName ?: device.name ?: return
            if (!name.startsWith(nameFilter)) return
            val found = BleunoDevice(name, device.address, result.rssi)
            mainHandler.post {
                if (!isScanning) return@post
                if (!foundAddresses.add(found.address)) return@post   // 이미 알린 기기
                Log.d(TAG, "onScanResult: ${found.name} ${found.address} rssi=${found.rssi}")
                onFoundListener?.invoke(found)
            }
        }

        override fun onScanFailed(errorCode: Int) {
            Log.w(TAG, "onScanFailed: errorCode=$errorCode")
            mainHandler.post { stopScan() }
        }
    }

    override fun startScan(timeoutMs: Long, onFound: (BleunoDevice) -> Unit, onFinished: () -> Unit) {
        if (!PermissionHelper.hasAll(appContext)) {
            Log.w(TAG, "startScan: 권한이 없어 무시함 (${PermissionHelper.missing(appContext).joinToString()})")
            return
        }
        val scanner = bluetoothManager?.adapter?.bluetoothLeScanner
        if (scanner == null) {
            Log.w(TAG, "startScan: 블루투스가 꺼져 있거나 없음 → onFinished")
            onFinished()
            return
        }
        if (isScanning) stopScan()
        foundAddresses.clear()
        onFoundListener = onFound
        onFinishedListener = onFinished
        isScanning = true
        val settings = ScanSettings.Builder()
            .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
            .build()
        scanner.startScan(null, settings, scanCallback)
        Log.d(TAG, "startScan: ${timeoutMs}ms 동안 \"$nameFilter\"로 시작하는 기기 검색")
        scanHandler.postDelayed({
            Log.d(TAG, "scan timeout (${timeoutMs}ms)")
            stopScan()
        }, timeoutMs)
    }

    override fun stopScan() {
        if (!isScanning) return
        isScanning = false
        scanHandler.removeCallbacksAndMessages(null)
        bluetoothManager?.adapter?.bluetoothLeScanner?.stopScan(scanCallback)
        Log.d(TAG, "stopScan: 찾은 기기 ${foundAddresses.size}개")
        val finished = onFinishedListener
        onFoundListener = null
        onFinishedListener = null
        finished?.invoke()
    }

    // ---------------------------------------------------------------- 연결

    private val gattCallback = object : BluetoothGattCallback() {

        override fun onConnectionStateChange(g: BluetoothGatt, status: Int, newState: Int) {
            Log.d(TAG, "onConnectionStateChange: status=$status newState=$newState")
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                Log.d(TAG, "STATE_CONNECTED → requestMtu($MTU)")
                mainHandler.post { _connectionState.value = ConnState.DISCOVERING }
                val requested = g.requestMtu(MTU)
                Log.d(TAG, "requestMtu($MTU) 호출 결과=$requested")
            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                Log.d(TAG, "STATE_DISCONNECTED → gatt.close()")
                g.close()
                mainHandler.post {
                    gatt = null
                    characteristic = null
                    queue.clear()
                    writing = false
                    _connectionState.value = if (userDisconnect) ConnState.DISCONNECTED else ConnState.LOST
                }
            }
        }

        override fun onMtuChanged(g: BluetoothGatt, mtu: Int, status: Int) {
            Log.d(TAG, "onMtuChanged: mtu=$mtu status=$status → discoverServices()")
            // MTU 변경이 실패해도 기본 MTU로 쓸 수 있으므로 서비스 탐색은 그대로 진행한다
            val started = g.discoverServices()
            Log.d(TAG, "discoverServices() 호출 결과=$started")
        }

        override fun onServicesDiscovered(g: BluetoothGatt, status: Int) {
            Log.d(TAG, "onServicesDiscovered: status=$status")
            val service = g.getService(SERVICE_UUID)
            val ch = service?.getCharacteristic(CHARACTERISTIC_UUID)
            if (ch == null) {
                Log.w(TAG, "서비스 또는 특성을 찾지 못함 → disconnect()")
                g.disconnect()
                return
            }
            Log.d(TAG, "characteristic 확보: ${ch.uuid}")
            mainHandler.post { characteristic = ch }
            g.setCharacteristicNotification(ch, true)
            val descriptor = ch.getDescriptor(CCCD_UUID)
            if (descriptor == null) {
                Log.w(TAG, "CCCD descriptor 없음 → disconnect()")
                g.disconnect()
                return
            }
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                g.writeDescriptor(descriptor, BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE)
            } else {
                @Suppress("DEPRECATION")
                descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
                @Suppress("DEPRECATION")
                g.writeDescriptor(descriptor)
            }
            Log.d(TAG, "writeDescriptor(CCCD, ENABLE_NOTIFICATION_VALUE)")
        }

        override fun onDescriptorWrite(g: BluetoothGatt, descriptor: BluetoothGattDescriptor, status: Int) {
            Log.d(TAG, "onDescriptorWrite: status=$status → 준비됨")
            mainHandler.post { _connectionState.value = ConnState.READY }
        }

        override fun onCharacteristicWrite(g: BluetoothGatt, ch: BluetoothGattCharacteristic, status: Int) {
            Log.d(TAG, "onCharacteristicWrite: status=$status")
            mainHandler.post {
                writing = false
                writeNext()
            }
        }

        // API 33 이상에서 불리는 응답 콜백
        override fun onCharacteristicChanged(g: BluetoothGatt, ch: BluetoothGattCharacteristic, value: ByteArray) {
            deliver(value)
        }

        // API 32 이하에서 불리는 응답 콜백
        @Deprecated("Deprecated in Java")
        override fun onCharacteristicChanged(g: BluetoothGatt, ch: BluetoothGattCharacteristic) {
            @Suppress("DEPRECATION")
            val value = ch.value ?: return
            deliver(value)
        }
    }

    // 받은 바이트를 UTF-8 문자열로 바꿔 메인 스레드에서 리스너에 전달한다
    private fun deliver(bytes: ByteArray) {
        val text = String(bytes, Charsets.UTF_8)
        Log.d(TAG, "onCharacteristicChanged: $text")
        mainHandler.post { messageListener?.invoke(text) }
    }

    override fun connect(address: String) {
        if (!PermissionHelper.hasAll(appContext)) {
            Log.w(TAG, "connect: 권한이 없어 무시함")
            return
        }
        val adapter = bluetoothManager?.adapter
        if (adapter == null) {
            Log.w(TAG, "connect: 블루투스 어댑터 없음")
            return
        }
        val device = try {
            adapter.getRemoteDevice(address)
        } catch (e: IllegalArgumentException) {
            Log.w(TAG, "connect: 잘못된 주소 $address")
            return
        }
        // 이전 연결이 남아 있으면 정리하고 새로 시작한다
        gatt?.close()
        gatt = null
        characteristic = null
        queue.clear()
        writing = false
        userDisconnect = false

        _connectionState.value = ConnState.CONNECTING
        Log.d(TAG, "connectGatt($address, autoConnect=false)")
        val created = device.connectGatt(appContext, false, gattCallback)
        if (created == null) {
            Log.w(TAG, "connectGatt 실패 (블루투스 꺼짐?)")
            _connectionState.value = ConnState.DISCONNECTED
            return
        }
        gatt = created
    }

    override fun disconnect() {
        userDisconnect = true
        val g = gatt
        if (g == null) {
            Log.d(TAG, "disconnect: 연결 없음 → 연결 안 됨")
            _connectionState.value = ConnState.DISCONNECTED
            return
        }
        Log.d(TAG, "gatt.disconnect()")
        g.disconnect()   // 결과는 onConnectionStateChange(STATE_DISCONNECTED)에서 처리
    }

    // ---------------------------------------------------------------- 전송

    override fun send(command: String) {
        if (!PermissionHelper.hasAll(appContext)) {
            Log.w(TAG, "send: 권한이 없어 무시함")
            return
        }
        if (!isReady) {
            Log.w(TAG, "send: 준비되지 않아 무시함 (\"$command\", 상태=${_connectionState.value})")
            return
        }
        queue.addLast(command + "\n")
        Log.d(TAG, "send: 큐에 추가 \"$command\" (대기 ${queue.size}개)")
        if (!writing) writeNext()
    }

    // 큐의 맨 앞 명령 하나를 보낸다. 다음 것은 onCharacteristicWrite가 온 뒤에 보낸다.
    private fun writeNext() {
        val g = gatt ?: return
        val ch = characteristic ?: return
        val text = queue.removeFirstOrNull() ?: return
        val bytes = text.toByteArray(Charsets.UTF_8)
        writing = true
        val ok = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            val code = g.writeCharacteristic(ch, bytes, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT)
            code == BluetoothStatusCodes.SUCCESS
        } else {
            @Suppress("DEPRECATION")
            ch.value = bytes
            @Suppress("DEPRECATION")
            g.writeCharacteristic(ch)
        }
        Log.d(TAG, "writeCharacteristic(\"${text.trim()}\") 호출 결과=$ok")
        if (!ok) {
            // 호출 자체가 실패하면 onCharacteristicWrite가 오지 않으므로 바로 다음 것을 시도한다
            writing = false
            writeNext()
        }
    }

    override fun onMessage(listener: ((String) -> Unit)?) {
        messageListener = listener
    }
}
