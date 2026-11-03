package com.example.smartio

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch

// 9주차 1일차: 화면 없이 일을 맡는 started Service. 따로 스레드를 만들지 않으면 메인 스레드에서 돈다.
class LogService : Service() {

    // Service에는 ViewModel의 viewModelScope 같은 것이 없으므로 코루틴을 돌릴 자리를 직접 만든다.
    // Dispatchers.Main은 1일차에 Logcat으로 본 그 메인 스레드다. delay는 기다리는 동안 스레드를 붙잡지 않아 화면이 멈추지 않는다(9주차 2일차).
    private val scope = CoroutineScope(Dispatchers.Main)

    // 1초마다 세는 코루틴. 7주차 ConnViewModel의 scanJob과 같은 자리다(9주차 2일차).
    private var tickJob: Job? = null

    // 1. startService를 부를 때마다 불린다. 어느 스레드에서 도는지 Logcat에 남긴다(9주차 1일차).
    //    Service도 메인 스레드에서 돌므로 여기서 오래 걸리는 일을 하면 화면이 멈춘다. 5주차 Thread.sleep 시연과 같다.
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val name = Thread.currentThread().name
        Log.d("Service", "onStartCommand thread=$name")

        // 5. 이미 세고 있으면 새로 시작하지 않는다. [서비스 시작]을 여러 번 눌러도 코루틴은 하나만 돈다.
        //    7주차 ConnViewModel.startScan의 검사와 같은 모양이고, 여기서는 돌려줄 값이 있어 값까지 적는다(9주차 2일차).
        if (tickJob?.isActive == true) {
            return START_NOT_STICKY
        }

        // 6. 1초마다 ServiceState.tick을 1 올린다. delay는 기다리는 동안 스레드를 붙잡지 않으므로
        //    1일차에서 본 "Service도 메인 스레드에서 돈다" 문제가 생기지 않는다. 6주차 delay를 그대로 쓴다(9주차 2일차).
        tickJob = scope.launch {
            while (isActive) {
                delay(1000)
                ServiceState.tick.value++
            }
        }

        // 2. 시스템이 이 Service를 강제로 끝내도 다시 살리지 않는다(9주차 1일차).
        return START_NOT_STICKY
    }

    // 3. stopService로 멈추면 불린다(9주차 1일차).
    override fun onDestroy() {
        super.onDestroy()
        // 7. 세던 코루틴을 취소하고 숫자를 0으로 되돌린다. 취소하지 않으면 Service가 끝난 뒤에도 계속 센다.
        //    ServiceState는 앱에 하나뿐이라 값을 그대로 두면 다음에 시작할 때 이어서 올라간다(9주차 2일차).
        tickJob?.cancel()
        ServiceState.tick.value = 0
        Log.d("Service", "onDestroy")
    }

    // 4. 화면과 묶어 쓰는(bound) Service가 아니므로 null을 돌려준다. 빼면 빌드가 안 되는 틀이다(9주차 1일차).
    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}
