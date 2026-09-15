package com.example.project1

import kotlinx.coroutines.delay
import kotlin.random.Random

// 9주차 1차 과제 제공 코드: 이 파일을 그대로 프로젝트에 복사한다. package 줄만 자기 프로젝트에 맞춘다.

// 1. 요청을 보낸 척한다. 1초 기다린 뒤 절반은 실패(throw)하고, 나머지는 "성공"을 돌려준다(9주차 1일차).
//    delay를 쓰는 suspend 함수이므로 코루틴 안에서만 부를 수 있다. 회전해도 결과를 남기려면 viewModelScope.launch { } 안에서 부른다.
//    실패하면 앱이 꺼지지 않도록 부르는 쪽에서 try/catch로 감싼다.
suspend fun fakeRequest(): String {
    delay(1000)
    if (Random.nextBoolean()) {
        throw Exception("요청 실패")
    }
    return "성공"
}
