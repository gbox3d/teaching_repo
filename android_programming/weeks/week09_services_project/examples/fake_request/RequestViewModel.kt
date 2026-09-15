package com.example.project1

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

// 9주차 1차 과제 예시: fakeRequest()를 부르는 ViewModel. 7주차 ConnViewModel과 같은 모양이라 회전해도 결과가 남는다.
class RequestViewModel : ViewModel() {
    // 1. 화면에 보여 줄 값 두 가지: 결과 문구와 실패 여부.
    //    바꾸는 쪽(_result, _failed)은 안에만 두고, 화면에는 읽기 전용(result, failed)만 보여 준다(7주차 2일차).
    private val _result = MutableStateFlow("대기 중")
    val result: StateFlow<String> = _result
    private val _failed = MutableStateFlow(false)
    val failed: StateFlow<Boolean> = _failed

    // 2. [요청]·[다시 시도]가 시작한 코루틴(7주차 1일차).
    private var requestJob: Job? = null

    // 3. [요청]·[다시 시도]: fakeRequest()를 부르고 결과를 _result·_failed에 넣는다(9주차 1일차).
    //    viewModelScope 코루틴은 회전해도 끊기지 않는다. 요청 중에 회전해도 1초 뒤 결과가 새 화면에 나온다.
    fun request() {
        // 이미 요청 중이면 새로 시작하지 않는다(7주차 1일차).
        if (requestJob?.isActive == true) {
            return
        }
        requestJob = viewModelScope.launch {
            _failed.value = false
            _result.value = "요청 중…"
            try {
                val text = fakeRequest()
                _result.value = "결과: $text"
            } catch (e: Exception) {
                // 4. 실패하면 실패 문구를 넣고 [다시 시도]가 보이게 한다(6주차 2일차).
                _result.value = "요청 실패"
                _failed.value = true
            }
        }
    }
}
