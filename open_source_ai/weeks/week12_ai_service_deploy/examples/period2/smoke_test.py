"""앱 서버 점검 — /health, /chat, /chat/stream 을 순서대로 호출하고 결과를 outputs/ 에 남긴다.

실행:  uv run python smoke_test.py
       uv run python smoke_test.py --skip-stream
       uv run python smoke_test.py --show-events        # SSE 원문 앞 몇 줄을 그대로 출력
       uv run python smoke_test.py --api http://localhost:8001

캡처 대신 이 스크립트가 만든 JSON 이 "정상·실패 경로를 재현했다"는 증거가 된다.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()


def parse_body(resp: httpx.Response) -> Any:
    try:
        return resp.json()
    except ValueError:
        return resp.text[:300]


def check_health(http: httpx.Client) -> dict[str, Any]:
    started = time.perf_counter()
    resp = http.get("/health")
    return {"status_code": resp.status_code, "elapsed_ms": round((time.perf_counter() - started) * 1000), "body": parse_body(resp)}


def check_chat(http: httpx.Client, prompt: str, max_tokens: int) -> dict[str, Any]:
    started = time.perf_counter()
    resp = http.post("/chat", json={"messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens})
    body = parse_body(resp)
    result = {"status_code": resp.status_code, "elapsed_ms": round((time.perf_counter() - started) * 1000), "request_id": resp.headers.get("x-request-id")}
    if resp.status_code == 200 and isinstance(body, dict):
        result.update({"reply": body.get("reply", ""), "eval_count": body.get("eval_count"), "eval_duration_ms": body.get("eval_duration_ms")})
    else:
        result["body"] = body
    return result


def check_stream(http: httpx.Client, prompt: str, max_tokens: int, show_events: bool) -> dict[str, Any]:
    started = time.perf_counter()
    text, first_ms, events, shown = "", None, 0, 0
    result: dict[str, Any] = {}
    with http.stream("POST", "/chat/stream", json={"messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens}) as resp:
        result["status_code"] = resp.status_code
        result["request_id"] = resp.headers.get("x-request-id")
        if resp.status_code != 200:
            resp.read()
            result["body"] = parse_body(resp)
            return result
        for line in resp.iter_lines():
            if not line.startswith("data: "):
                continue
            if show_events and shown < 5:
                print(f"    {line}")
                shown += 1
            events += 1
            event = json.loads(line[6:])
            if "delta" in event:
                if first_ms is None:
                    first_ms = round((time.perf_counter() - started) * 1000)
                text += event["delta"]
            elif "error" in event:
                result["error_event"] = event
            if event.get("done"):
                result["eval_count"] = event.get("eval_count")
    result.update({"first_chunk_ms": first_ms, "total_ms": round((time.perf_counter() - started) * 1000), "events": events, "reply_chars": len(text), "reply_head": text[:80]})
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="앱 서버 /health, /chat, /chat/stream 점검")
    parser.add_argument("--api", default=os.environ.get("API_BASE_URL", "http://localhost:8000"))
    parser.add_argument("--prompt", default="오픈소스 라이선스가 왜 필요한지 두 문장으로 설명해 줘.")
    parser.add_argument("--max-tokens", type=int, default=160)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--skip-stream", action="store_true")
    parser.add_argument("--show-events", action="store_true", help="SSE 원문 앞 5줄 출력")
    parser.add_argument("--out-dir", default=os.environ.get("LOG_DIR", "outputs"))
    args = parser.parse_args()

    report: dict[str, Any] = {"api": args.api, "checked_at": datetime.now().isoformat(timespec="seconds"), "prompt": args.prompt}
    try:
        with httpx.Client(base_url=args.api, timeout=args.timeout) as http:
            report["health"] = check_health(http)
            print(f"[health] {report['health']['status_code']} status={report['health']['body'].get('status') if isinstance(report['health']['body'], dict) else '?'}")
            report["chat"] = check_chat(http, args.prompt, args.max_tokens)
            print(f"[chat]   {report['chat']['status_code']} {report['chat']['elapsed_ms']}ms  {str(report['chat'].get('reply') or report['chat'].get('body'))[:100]!r}")
            if not args.skip_stream:
                report["stream"] = check_stream(http, args.prompt, args.max_tokens, args.show_events)
                s = report["stream"]
                print(f"[stream] {s['status_code']} first={s.get('first_chunk_ms')}ms total={s.get('total_ms')}ms events={s.get('events')}")
        code = 0
    except httpx.ConnectError:
        report["error"] = f"앱 서버 {args.api} 에 연결할 수 없다. uvicorn 이 실행 중인지, 포트가 맞는지 확인한다."
        print(f"[fail] {report['error']}")
        code = 1
    except httpx.TimeoutException:
        report["error"] = f"앱 서버가 {args.timeout:g}초 안에 응답하지 않았다."
        print(f"[fail] {report['error']}")
        code = 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"smoke-{datetime.now():%Y%m%d-%H%M%S}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"기록: {path}")
    raise SystemExit(code)


if __name__ == "__main__":
    main()
