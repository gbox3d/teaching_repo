package com.example.smartio

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlin.random.Random

// 7주차 1일차: 연결 화면의 일을 맡는 ViewModel. 화면(Activity)보다 오래 살아서 회전해도 그대로 남는다.
class ConnViewModel : ViewModel() {
    // 1. 마지막으로 알린 문구. 회전 뒤 새 화면이 onCreate에서 다시 읽는다(7주차 1일차).
    var resultText = "대기 중"

    // 2. 문구가 바뀔 때 부를 화면 쪽 코드. 화면이 onCreate에서 넣고 onDestroy에서 null로 비운다(7주차 1일차).
    //    ViewModel은 화면보다 오래 살므로, 없어진 화면을 붙잡지 않게 반드시 비운다.
    var listener: ((String) -> Unit)? = null

    // 3. [검색]·[다시 시도]가 시작한 코루틴. 6주차에는 MainActivity에 있던 변수다(7주차 1일차).
    private var scanJob: Job? = null

    // 4. [검색]: 5초를 센 뒤 가짜 연결을 시도한다(7주차 1일차).
    fun startScan() {
        // 이미 돌고 있으면 새로 시작하지 않는다. 회전한 새 화면에서는 [검색]이 다시 켜져 있기 때문이다.
        if (scanJob?.isActive == true) {
            return
        }
        scanJob = viewModelScope.launch {
            for (i in 5 downTo 1) {
                show("검색 중… $i")
                delay(1000)
            }
            tryConnect()
        }
    }

    // 5. [중지]: 카운트다운 코루틴을 취소한다(7주차 1일차).
    fun stopScan() {
        scanJob?.cancel()
    }

    // 6. [다시 시도]: 카운트다운 없이 연결만 다시 시도한다(7주차 1일차).
    fun retry() {
        scanJob = viewModelScope.launch {
            tryConnect()
        }
    }

    // 문구를 Logcat에 남기고 resultText에 보관한 뒤, 등록된 화면이 있으면 알린다. 없으면(null) 보관만 한다.
    private fun show(text: String) {
        Log.d("Conn", text)
        resultText = text
        listener?.invoke(text)
    }

    // 연결을 흉내 낸다. 2초 걸리고 절반은 실패한다. 진짜 막히는 일이므로 IO로 옮긴다.
    private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
        Thread.sleep(2000)
        if (Random.nextBoolean()) {
            throw Exception("연결 실패")
        }
        true
    }

    // 가짜 연결을 시도하고 결과를 화면에 알린다.
    private suspend fun tryConnect() {
        show("연결 중…")
        var result = "연결됨"
        try {
            connectFake()
        } catch (e: Exception) {
            result = "연결 실패"
        }
        show(result)
    }
}
