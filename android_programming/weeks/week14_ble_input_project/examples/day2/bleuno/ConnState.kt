package com.example.smartio.bleuno

// 연결 상태를 나타내는 한글 문자열 모음.
// 화면의 TextView에 그대로 넣어 보여 준다. 7주차 ConnViewModel의 ConnState와 같은 다섯 가지다.
object ConnState {
    const val DISCONNECTED = "연결 안 됨"   // 처음 상태, 또는 사용자가 해제한 뒤
    const val CONNECTING = "연결 중"        // connect()를 부른 뒤 보드와 연결되기 전
    const val DISCOVERING = "서비스 확인 중" // 연결은 되었고 서비스·특성을 찾는 중
    const val READY = "준비됨"              // 명령을 보낼 수 있는 상태
    const val LOST = "끊김"                 // 사용자가 해제하지 않았는데 연결이 끊어짐
}
