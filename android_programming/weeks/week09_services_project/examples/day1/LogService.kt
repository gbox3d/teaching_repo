package com.example.smartio

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log

// 9주차 1일차: 화면 없이 일을 맡는 started Service. 따로 스레드를 만들지 않으면 메인 스레드에서 돈다.
class LogService : Service() {

    // 1. startService를 부를 때마다 불린다. 어느 스레드에서 도는지 Logcat에 남긴다(9주차 1일차).
    //    Service도 메인 스레드에서 돌므로 여기서 오래 걸리는 일을 하면 화면이 멈춘다. 5주차 Thread.sleep 시연과 같다.
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val name = Thread.currentThread().name
        Log.d("Service", "onStartCommand thread=$name")
        // 2. 시스템이 이 Service를 강제로 끝내도 다시 살리지 않는다(9주차 1일차).
        return START_NOT_STICKY
    }

    // 3. stopService로 멈추면 불린다(9주차 1일차).
    override fun onDestroy() {
        super.onDestroy()
        Log.d("Service", "onDestroy")
    }

    // 4. 화면과 묶어 쓰는(bound) Service가 아니므로 null을 돌려준다. 빼면 빌드가 안 되는 틀이다(9주차 1일차).
    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}
