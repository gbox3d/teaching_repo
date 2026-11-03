package com.example.smartio

import kotlinx.coroutines.flow.MutableStateFlow

// 1. Service가 센 값을 두는 자리. Service와 화면(Activity)은 서로 다른 객체여서 값을 바로 건넬 수 없다.
//    object는 앱에 하나만 생기므로 Service와 화면이 같은 ServiceState.tick을 본다. 7주차 ConnState와 같은 자리다(9주차 2일차).
// 2. 7주차 ConnViewModel은 바꾸는 쪽(_seconds)을 안에 숨기고 읽기 전용(seconds)만 내보냈다.
//    여기서 숨기려면 값을 올리는 함수도 같이 둬야 한다. 올리는 쪽이 이 파일 바깥의 Service라서다.
//    이번 예제는 새 파일을 한 줄로 두려고 숨기지 않는 쪽을 골랐다(9주차 2일차).
object ServiceState {
    val tick = MutableStateFlow(0)
}
