package com.example.smartio.bleuno

// 검색으로 찾은 보드 하나의 정보.
// name: 기기 이름(ESP32_BLE로 시작), address: 연결할 때 쓰는 주소, rssi: 신호 세기(클수록 가까움, 보통 음수)
data class BleunoDevice(val name: String, val address: String, val rssi: Int)
