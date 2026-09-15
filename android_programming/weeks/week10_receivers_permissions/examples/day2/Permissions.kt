package com.example.smartio

import android.Manifest
import android.os.Build

// 1. BLE 장치를 찾고 연결하려면 실행 중에 허락받아야 하는 권한 목록을 돌려준다(10주차 2일차).
//    Android 12(API 31) 이상: BLUETOOTH_SCAN·BLUETOOTH_CONNECT, Android 11 이하: ACCESS_FINE_LOCATION.
//    같은 권한이라도 이름이 Android 버전마다 달라서 기기 버전(SDK_INT)을 보고 고른다.
fun blePermissions(): Array<String> {
    if (Build.VERSION.SDK_INT >= 31) {
        return arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
    } else {
        return arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
    }
}
