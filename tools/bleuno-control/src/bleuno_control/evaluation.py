"""호출 정확도와 실제 LED 상태를 구분해서 확인한다."""

import json
import math
import statistics
import time

from . import validate_calls

INITIAL_LEDS = [0, 64, 128, 255]


def expected_leds(calls, initial=INITIAL_LEDS):
    validate_calls(calls)
    leds = list(initial)
    for call in calls:
        name, args = call["name"], call["arguments"]
        if name != "read_environment":
            leds[args["index"]] = (args["value"] if name == "set_brightness"
                                   else 255 if name == "turn_on" else 0)
    return leds


def evaluate(predict, board, cases):
    """모든 실패를 분모에 남긴다. 예열 호출은 실행하지 않는다."""
    if not cases:
        raise ValueError("평가 문항이 없습니다.")
    for case in cases:
        validate_calls(case["calls"])
    try:
        predict("Turn on LED 0")
    except Exception as exc:
        print(f"예열 호출 실패: {exc}. 각 평가 문항은 계속 확인합니다.")
    rows = []
    for case in cases:
        calls, error, valid, results = [], None, False, []
        elapsed, actual, state_ok = None, None, False
        try:
            for index, value in enumerate(INITIAL_LEDS):
                board.execute([{"name": "set_brightness", "arguments": {"index": index, "value": value}}])
            before = board.state()
            started = time.perf_counter()
            try:
                calls = predict(case["query"])
            finally:
                elapsed = time.perf_counter() - started
            validate_calls(calls)
            valid = True
            results = board.execute(calls)
            actual = board.state()["leds"]
            state_ok = actual == expected_leds(case["calls"])
            # 센서는 LED를 바꾸지 않는다. 반환값까지 대조한다.
            for call, reply in zip(calls, results):
                if call["name"] == "read_environment":
                    state_ok = state_ok and json.loads(reply.get("value", "null")) == [round(before["temperature"], 1), round(before["humidity"], 1)]
        except Exception as exc:
            error = str(exc)
        names_ok = valid and [c["name"] for c in calls] == [c["name"] for c in case["calls"]]
        exact = valid and calls == case["calls"]
        success = bool(exact and state_ok and error is None)
        row = {"id": case["id"], "language": case.get("language", "unknown"), "query": case["query"], "calls": calls,
               "function_ok": names_ok, "exact": exact, "state_ok": state_ok,
               "success": success, "latency": elapsed, "error": error,
               "no_call": not case["calls"], "false_call": bool(calls) and not case["calls"]}
        rows.append(row)
        timing = f"{elapsed:.3f}s" if elapsed is not None else "추론 미실행"
        print(f"{case['id']} {case['query']}\n  호출={calls}\n  LED={actual} 완전일치={exact} 성공={success} {timing} 오류={error}")
    n = len(rows)
    latencies = sorted(r["latency"] for r in rows if r["latency"] is not None)
    no_calls = [r for r in rows if r["no_call"]]
    summary = {"count": n, "function_accuracy": sum(r["function_ok"] for r in rows) / n,
               "call_accuracy": sum(r["exact"] for r in rows) / n,
               "success_rate": sum(r["success"] for r in rows) / n,
               "false_call_rate": sum(r["false_call"] for r in no_calls) / len(no_calls) if no_calls else None,
               "latency_count": len(latencies),
               "median_seconds": statistics.median(latencies) if latencies else None,
               "p95_seconds": latencies[math.ceil(.95 * len(latencies)) - 1] if latencies else None}
    summary["error_count"] = sum(r["error"] is not None for r in rows)
    summary["by_language"] = {
        language: sum(r["success"] for r in rows if r["language"] == language) /
        sum(r["language"] == language for r in rows)
        for language in sorted({r["language"] for r in rows})
    }
    print("평가 요약:", summary)
    return rows, summary
