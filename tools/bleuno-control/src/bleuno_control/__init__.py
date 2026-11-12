"""10~13주차가 같은 연결·검증·평가 함수를 사용한다."""

import json
import socket
from contextlib import suppress
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener

DATA_DIR = Path(__file__).parent / "data"


def http_json(url, body=None, timeout=30):
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = Request(url, data=data, headers={"Content-Type": "application/json"})
    with build_opener(ProxyHandler({})).open(request, timeout=timeout) as response:
        return json.load(response)


def validate_calls(calls):
    """전체 목록을 먼저 검사한다. 잘못된 뒤쪽 호출 때문에 앞쪽만 실행하지 않는다."""
    if not isinstance(calls, list) or len(calls) > 8:
        raise ValueError("호출 목록은 최대 8개여야 합니다.")
    fields = {"turn_on": {"index"}, "turn_off": {"index"},
              "set_brightness": {"index", "value"}, "read_environment": set()}
    for call in calls:
        if not isinstance(call, dict) or set(call) != {"name", "arguments"}:
            raise ValueError("호출에는 name과 arguments가 필요합니다.")
        name, args = call["name"], call["arguments"]
        if not isinstance(name, str) or name not in fields:
            raise ValueError("등록되지 않은 함수입니다.")
        if not isinstance(args, dict) or set(args) != fields[name]:
            raise ValueError("함수의 필수 인자가 없거나 다른 인자가 있습니다.")
        for key, high in (("index", 3), ("value", 255)):
            if key in args and (type(args[key]) is not int or not 0 <= args[key] <= high):
                raise ValueError(f"{key}는 0~{high} 범위의 정수여야 합니다.")
    return calls


class Board:
    """한 실습 동안 유지하는 TCP 연결. 닫으면 시뮬레이터 LED가 초기화된다."""

    def __init__(self, host="127.0.0.1", port=8266, http_url="http://127.0.0.1:8080"):
        self.http_url = http_url
        self.closed = False
        self.socket = socket.create_connection((host, port), timeout=5)
        self.file = self.socket.makefile("rw", encoding="utf-8", newline="\n")
        try:
            hello = json.loads(self.file.readline())
            if hello.get("event") != "hello":
                raise ValueError("시뮬레이터의 시작 응답을 확인할 수 없습니다.")
        except BaseException:
            self.close()
            raise

    def command(self, text):
        if getattr(self, "closed", False):
            raise ConnectionError("연결이 닫혔습니다. 시뮬레이터에 다시 연결하세요.")
        try:
            self.file.write(text + "\n")
            self.file.flush()
            # 입력 버튼 이벤트가 명령 응답보다 먼저 도착할 수 있다.
            for _ in range(32):
                line = self.file.readline()
                if not line:
                    raise ConnectionError("시뮬레이터 연결이 종료되었습니다.")
                reply = json.loads(line)
                if "event" not in reply:
                    if reply.get("result") != "ok":
                        raise RuntimeError(f"시뮬레이터 명령 실패: {reply}")
                    return reply
            raise ConnectionError("이벤트가 계속 도착해 연결을 닫았습니다. 다시 연결하세요.")
        except BaseException:
            # 응답 순서를 보장할 수 없는 연결을 다음 요청에 재사용하지 않는다.
            self.close()
            raise

    def execute(self, calls):
        validate_calls(calls)
        results = []
        for call in calls:
            name, args = call["name"], call["arguments"]
            if name == "read_environment":
                command = "dht11"
            elif name == "set_brightness":
                command = f"pwm {args['index']} {args['value']}"
            else:
                command = f"{'on' if name == 'turn_on' else 'off'} {args['index']}"
            results.append(self.command(command))
        return results

    def state(self):
        if getattr(self, "closed", False):
            raise ConnectionError("연결이 닫혔습니다. 시뮬레이터에 다시 연결하세요.")
        return http_json(self.http_url + "/state", timeout=5)

    def close(self):
        if not getattr(self, "closed", False):
            self.closed = True
            with suppress(OSError):
                self.file.close()
            with suppress(OSError):
                self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def load_cases():
    return json.loads((DATA_DIR / "control_cases.json").read_text(encoding="utf-8"))


def chat(predict, board):
    print("제어 요청을 입력하세요. /bye 또는 Ctrl+C로 종료합니다.")
    while True:
        try:
            question = input("요청> ").strip()
            if question == "/bye":
                break
            if not question:
                continue
            calls = predict(question)
            print("호출:", json.dumps(calls, ensure_ascii=False))
            if calls:
                print("응답:", board.execute(calls))
            else:
                print("실행할 호출이 없습니다.")
            print("LED:", board.state()["leds"])
        except (EOFError, KeyboardInterrupt):
            print("\n대화를 종료합니다.")
            break
        except Exception as error:
            print(f"오류: {error}")
            if board.closed:
                print("연결이 닫혔습니다. 프로그램을 다시 실행하세요.")
                break
