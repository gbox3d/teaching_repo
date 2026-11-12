from shared import Board


def main():
    print("명령: on 0 / off 0 / pwm 1 128 / sensor. 종료: /bye")
    with Board() as board:
        while True:
            try:
                text = input("직접 제어> ").strip()
                if text == "/bye":
                    break
                if not text:
                    continue
                parts = text.split()
                if len(parts) == 2 and parts[0] in ("on", "off"):
                    calls = [{"name": "turn_on" if parts[0] == "on" else "turn_off",
                              "arguments": {"index": int(parts[1])}}]
                elif len(parts) == 3 and parts[0] == "pwm":
                    calls = [{"name": "set_brightness",
                              "arguments": {"index": int(parts[1]), "value": int(parts[2])}}]
                elif parts == ["sensor"]:
                    calls = [{"name": "read_environment", "arguments": {}}]
                else:
                    print("안내된 명령과 인자를 입력하세요.")
                    continue
                print(board.execute(calls))
                print("LED:", board.state()["leds"])
            except (EOFError, KeyboardInterrupt):
                print("\n제어를 종료합니다.")
                break
            except (ValueError, OSError, RuntimeError) as error:
                print("오류:", error)
