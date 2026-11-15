package com.example.smartio

// 1. 연결 상태를 나타내는 한글 문자열 모음. 화면의 TextView에 그대로 넣어 보여 준다(7주차 2일차).
// 12주차 bleuno 라이브러리의 ConnState와 이름·값이 같다. 12주차에는 이 파일 대신 import만 바꾼다.
// 장치를 찾는 동안의 "검색 중"은 연결 상태가 아니라서 여기에 넣지 않고 ConnViewModel.kt의 ScanState에 따로 둔다(11주차 1일차).
object ConnState {
    const val DISCONNECTED = "연결 안 됨"   // 처음 상태, 또는 [중지]·[해제]를 누른 뒤
    const val CONNECTING = "연결 중"        // 가짜 연결(2초)을 기다리는 중
    const val DISCOVERING = "서비스 확인 중" // 이번 주 가짜 연결에서는 나오지 않는다. 12주차에 라이브러리로 연결하면 "연결 중" 다음에 나온다
    const val READY = "준비됨"              // 연결 성공
    const val LOST = "끊김"                 // 연결 실패
}
