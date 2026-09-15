package com.example.rehearsal

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

// 8주차 1일차: 리허설 화면의 일을 맡는 ViewModel. 화면(Activity)보다 오래 살아서 회전해도 그대로 남는다.
class RehearsalViewModel : ViewModel() {
    // 1. 화면에 보여 줄 값 두 가지: 상태 문구와 남은 초.
    //    바꾸는 쪽(_state, _seconds)은 안에만 두고, 화면에는 읽기 전용(state, seconds)만 보여 준다(8주차 1일차).
    private val _state = MutableStateFlow("대기 중")
    val state: StateFlow<String> = _state
    private val _seconds = MutableStateFlow(0)
    val seconds: StateFlow<Int> = _seconds

    // 2. [시작]이 시작한 코루틴. [취소]에서 멈추려고 보관한다. 아직 없으면 null이다(8주차 1일차).
    private var job: Job? = null

    // 3. [시작]: 카운트다운 중으로 바꾸고 5초를 센 뒤 완료로 바꾼다(8주차 1일차).
    fun startCountdown() {
        // TODO(1) job이 이미 돌고 있으면(isActive) 그냥 돌아간다.
        //         아니면 viewModelScope.launch로 코루틴을 시작하고 그 Job을 job에 보관한다. 코루틴 안에서는
        //         _state를 "카운트다운 중"으로 바꾸고, 5부터 1까지 _seconds에 넣으며 1초씩 기다린 뒤,
        //         _seconds를 0, _state를 "완료"로 바꾼다. for 안 첫 줄에 Log.d("Rehearsal", "남은 초: $i"), "완료"로 바꾼 다음 줄에 Log.d("Rehearsal", "완료")를 찍는다.
    }

    // 4. [취소]: 카운트다운 코루틴을 멈추고 취소됨으로 바꾼다. 남은 초는 멈춘 숫자 그대로 둔다(8주차 1일차).
    fun cancelCountdown() {
        // TODO(2) 보관한 job을 취소하고 _state를 "취소됨"으로 바꾼다. job은 null일 수 있다. 그다음 줄에 Log.d("Rehearsal", "취소됨")을 찍는다.
    }
}
