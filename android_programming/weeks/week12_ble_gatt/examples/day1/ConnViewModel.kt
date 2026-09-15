package com.example.smartio

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.smartio.bleuno.ConnState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlin.random.Random

// 7주차 1일차: 연결 화면의 일을 맡는 ViewModel. 화면(Activity)보다 오래 살아서 회전해도 그대로 남는다.
class ConnViewModel : ViewModel() {
    // 1. 화면에 보여 줄 값 두 가지: 연결 상태와 카운트다운 남은 초.
    //    바꾸는 쪽(_state, _seconds)은 안에만 두고, 화면에는 읽기 전용(state, seconds)만 보여 준다(7주차 2일차).
    private val _state = MutableStateFlow(ConnState.DISCONNECTED)
    val state: StateFlow<String> = _state
    private val _seconds = MutableStateFlow(0)
    val seconds: StateFlow<Int> = _seconds

    // 2. [검색]·[다시 시도]가 시작한 코루틴. 6주차에는 MainActivity에 있던 변수다(7주차 1일차).
    private var scanJob: Job? = null

    // 3. [검색]: 연결 중으로 바꾸고 5초를 센 뒤 가짜 연결을 시도한다. 값은 _state·_seconds에 넣는다(7주차 2일차).
    fun startScan() {
        // 이미 돌고 있으면 새로 시작하지 않는다(7주차 1일차).
        if (scanJob?.isActive == true) {
            return
        }
        scanJob = viewModelScope.launch {
            _state.value = ConnState.CONNECTING
            for (i in 5 downTo 1) {
                Log.d("Conn", "연결 중… $i")
                _seconds.value = i
                delay(1000)
            }
            _seconds.value = 0
            tryConnect()
        }
    }

    // 4. [중지]: 카운트다운 코루틴을 취소하고 연결 안 됨으로 돌린다(7주차 2일차).
    fun stopScan() {
        scanJob?.cancel()
        _seconds.value = 0
        _state.value = ConnState.DISCONNECTED
    }

    // 5. [다시 시도]: 카운트다운 없이 연결만 다시 시도한다(7주차 1일차).
    fun retry() {
        scanJob = viewModelScope.launch {
            tryConnect()
        }
    }

    // 6. [해제]: 연결 안 됨으로 돌린다(7주차 2일차).
    fun disconnect() {
        _state.value = ConnState.DISCONNECTED
    }

    // 연결을 흉내 낸다. 2초 걸리고 절반은 실패한다. 진짜 막히는 일이므로 IO로 옮긴다.
    private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
        Thread.sleep(2000)
        if (Random.nextBoolean()) {
            throw Exception("연결 실패")
        }
        true
    }

    // 가짜 연결을 시도하고 결과 상태를 _state에 넣는다.
    private suspend fun tryConnect() {
        _state.value = ConnState.DISCOVERING
        try {
            connectFake()
            _state.value = ConnState.READY
        } catch (e: Exception) {
            _state.value = ConnState.LOST
        }
        Log.d("Conn", _state.value)
    }
}
