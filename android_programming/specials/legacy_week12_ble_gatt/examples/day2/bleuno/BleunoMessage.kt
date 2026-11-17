package com.example.smartio.bleuno

import org.json.JSONException
import org.json.JSONObject

// 보드가 보낸 JSON 한 줄에서 값을 꺼내는 도우미.
// 예: {"result":"ok","ms":"led(s) on"} → result(json) == "ok", message(json) == "led(s) on"
// 잘못된 JSON이면 예외를 던지지 않고 null을 돌려준다.
object BleunoMessage {

    // "result" 값: "ok" | "err" | "fail" | null(없거나 JSON이 아님)
    fun result(json: String): String? = field(json, "result")

    // "ms" 값: 사람이 읽는 메시지 (예: "led(s) on", "unknown command")
    fun message(json: String): String? = field(json, "ms")

    // "value" 값: dht11 응답의 "[24.5,40.0]" 처럼 값이 들어 있는 문자열
    fun value(json: String): String? = field(json, "value")

    // "event" 값: 보드가 먼저 보내는 이벤트 종류 (입력 이벤트 가안: "input")
    fun event(json: String): String? = field(json, "event")

    // result가 "ok"이면 true
    fun isOk(json: String): Boolean = result(json) == "ok"

    // 키 하나를 문자열로 꺼낸다. 키가 없거나 JSON이 아니면 null.
    private fun field(json: String, key: String): String? {
        return try {
            val obj = JSONObject(json)
            if (obj.has(key)) obj.getString(key) else null
        } catch (e: JSONException) {
            null
        }
    }
}
