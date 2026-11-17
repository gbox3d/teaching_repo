package com.example.roomcontrol.wleno

// 앱 프로세스에서 공유하는 클라이언트. 화면이 중지되면 예제가 명시적으로 해제한다.
object Wleno {
    val client = WlenoClient()
}
