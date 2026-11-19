#!/usr/bin/env python3
"""WlEno simulator entry point, native window, and service lifecycle.

Run ``python main.py`` with Python 3.10 or newer. Only the standard library is
required; ``--no-window`` does not import Tkinter.
"""

import argparse
from collections import deque
import importlib
import signal
import sys
import threading
import time
import unicodedata

from protocol import WlenoProtocol
from session import BoardSession


SERVICE_TYPES = (("tcp", "tcp", "TcpServer"), ("udp", "udp", "UdpServer"),
                 ("http", "http_api", "HttpServer"))


class Application:
    """Own the board session, optional adapters, logs, and main-thread window."""

    def __init__(self, args):
        self.args = args
        self.session = BoardSession()
        self.services = {}
        self.root = self.window = None
        self.stop_event = threading.Event()
        self.log_lock = threading.Lock()
        self.log_lines = deque(maxlen=20)
        self.closed = False
        self.started = False
        self.exit_code = 0
        self.protocol = WlenoProtocol(
            self.session, args.name, runtime_state=self.runtime_state,
            drop_connections=self.drop_connections, discovery=self.discovery, log=self.log)

    def log(self, message):
        line = time.strftime("[%H:%M:%S] ") + str(message)
        with self.log_lock:
            self.log_lines.append(line)
            print(line, flush=True)

    def service_status(self):
        statuses = {}
        for name, _, _ in SERVICE_TYPES:
            enabled = not getattr(self.args, "no_" + name)
            service = self.services.get(name)
            status = service.status() if service else {
                "running": False, "port": getattr(self.args, name) if enabled else None,
                "error": None}
            statuses[name] = dict(status, enabled=enabled)
        return statuses

    def runtime_state(self):
        statuses = self.service_status()
        with self.log_lock:
            lines = list(self.log_lines)
        return {"clients": statuses["tcp"].get("clients", 0),
                "log": lines, "services": statuses}

    def discovery(self):
        return {name: self.services[name].port
                if name in self.services and self.services[name].status()["running"] else None
                for name in ("tcp", "http")}

    def drop_connections(self):
        tcp = self.services.get("tcp")
        return tcp.drop_all() if tcp is not None and not self.closed else 0

    def start(self):
        if self.closed:
            raise RuntimeError("종료된 시뮬레이터는 다시 시작할 수 없습니다.")
        if self.started:
            return
        phase = "창 준비"
        try:
            if not self.args.no_window:
                if threading.current_thread() is not threading.main_thread():
                    raise RuntimeError("시뮬레이터 창은 메인 스레드에서 실행하세요.")
                tk = importlib.import_module("tkinter")
                self.root = tk.Tk()
                self.root.withdraw()
                self.window = Window(self.root, self)
            for name, module_name, class_name in SERVICE_TYPES:
                if getattr(self.args, "no_" + name):
                    continue
                phase = "%s 서비스 준비" % name.upper()
                cls = getattr(importlib.import_module(module_name), class_name)
                host = self.args.http_bind if name == "http" else self.args.bind
                self.services[name] = cls(self.protocol, host, getattr(self.args, name), log=self.log)
            # Nothing accepts requests until every selected socket has bound successfully.
            for name, service in self.services.items():
                phase = "%s 포트 %s 바인드" % (name.upper(), service.port)
                service.bind()
            for name, service in self.services.items():
                phase = "%s 포트 %s 시작" % (name.upper(), service.port)
                service.start()
            self.started = True
            if not self.check_health():
                raise RuntimeError("서비스가 시작 직후 중지되었습니다.")
            self.print_banner()
            if self.window is not None:
                self.window.refresh()
                self.window.schedule()
                self.root.deiconify()
        except Exception as exc:
            self.exit_code = 1
            self.close()
            if phase == "창 준비":
                self.log("Tcl/Tk 설치를 확인하세요. 창 없이 실행하려면 --no-window를 사용하세요.")
            raise RuntimeError("%s 실패: %s" % (phase, exc)) from exc

    def print_banner(self):
        self.log("WlEno 시뮬레이터: %s" % self.args.name)
        for name, status in self.service_status().items():
            host = self.args.http_bind if name == "http" else self.args.bind
            self.log("%s: %s" % (name.upper(),
                     "%s:%s" % (host, status["port"]) if status["enabled"] else "사용 안 함"))
        tcp = self.services.get("tcp")
        if tcp is not None:
            self.log("앱 주소: 에뮬레이터 10.0.2.2:%s, 실기기 이 PC의 LAN IPv4:%s"
                     % (tcp.port, tcp.port))
        self.log("종료: Ctrl+C" if self.args.no_window else "종료: 창 닫기 또는 Ctrl+C")

    def check_health(self):
        if self.stop_event.is_set():
            return False
        if self.started:
            for name, service in self.services.items():
                status = service.status()
                if status.get("error") or not status["running"]:
                    self.log("%s 서비스가 중지되었습니다: %s" %
                             (name.upper(), status.get("error") or "작업 스레드 종료"))
                    self.exit_code = 1
                    self.request_stop()
                    return False
        return True

    def request_stop(self):
        self.stop_event.set()
        if self.root is not None:
            self.root.quit()

    def run(self):
        previous = signal.getsignal(signal.SIGINT)
        try:
            signal.signal(signal.SIGINT, lambda *_: self.request_stop())
            self.start()
            if self.root is not None:
                self.root.mainloop()
            else:
                while not self.stop_event.wait(0.1):
                    if not self.check_health():
                        break
        except KeyboardInterrupt:
            self.request_stop()
        except Exception as exc:
            self.exit_code = 1
            self.log("시뮬레이터를 시작하거나 실행할 수 없습니다: %s" % exc)
        finally:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            self.close()
            signal.signal(signal.SIGINT, previous)
        return self.exit_code

    def close(self):
        if self.closed:
            return
        self.closed = True
        self.stop_event.set()
        if self.window is not None:
            self.window.close()
        self.session.close()
        for name, service in reversed(list(self.services.items())):
            try:
                service.close()
            except Exception as exc:
                self.exit_code = 1
                self.log("%s 종료 실패: %s" % (name.upper(), exc))
        if self.root is not None:
            self.root.destroy()
            self.root = None


class Window:
    """Native Tk view; all board mutations are synchronous Session calls."""

    def __init__(self, root, application):
        import tkinter as tk
        from tkinter import font, ttk

        self.root, self.app = root, application
        self.timer = None
        self.last_log = None
        root.title("WlEno 시뮬레이터 — %s" % application.args.name)
        root.minsize(980, 560)
        root.geometry("1040x620")
        root.protocol("WM_DELETE_WINDOW", application.request_stop)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        frame = ttk.Frame(root, padding=16)
        frame.grid(sticky="nsew")
        frame.columnconfigure(0, weight=1, minsize=440)
        frame.columnconfigure(1, weight=1, minsize=440)
        frame.rowconfigure(3, weight=1)
        self.heading_font = font.nametofont("TkDefaultFont").copy()
        self.heading_font.configure(size=17, weight="bold")
        title = "WlEno 시뮬레이터 — %s" % application.args.name
        while len(title) > 1 and self.heading_font.measure(title) > 930:
            title = title[:-2] + "…"
        ttk.Label(frame, text=title, font=self.heading_font).grid(
            row=0, column=0, columnspan=2, sticky="w")
        self.instructions = ttk.Label(frame, justify="left")
        self.instructions.grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 8))
        self.services = ttk.Label(frame)
        self.services.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 12))

        left = ttk.Frame(frame)
        left.grid(row=3, column=0, sticky="nsew", padx=(0, 12))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)
        leds = ttk.LabelFrame(left, text="LED (인덱스 0~3, 밝기 0~255)", padding=8)
        leds.grid(row=0, column=0, sticky="nsew")
        self.leds = tk.Canvas(leds, width=420, height=168, background="white", highlightthickness=0)
        self.leds.pack(fill="both", expand=True)
        self.led_circles, self.led_values = [], []
        for index in range(4):
            x = 52 + index * 100
            self.led_circles.append(self.leds.create_oval(
                x - 26, 20, x + 26, 72, fill="#dddddd", outline="#aaaaaa"))
            self.leds.create_text(x, 94, text="LED %d" % index)
            self.led_values.append(self.leds.create_text(x, 116, text="0"))
        self.blink_dot = self.leds.create_oval(12, 142, 24, 154, fill="#bbbbbb", outline="")
        self.blink_text = self.leds.create_text(32, 148, text="내장 LED: 꺼짐", anchor="w")

        sensors = ttk.LabelFrame(left, text="온도·습도 (dht11 응답)", padding=12)
        sensors.grid(row=1, column=0, sticky="ew", pady=12)
        sensors.columnconfigure(1, weight=1)
        self.sensor_values, self.sensor_labels = {}, {}
        for row, (key, label, lo, hi, unit) in enumerate((
            ("temperature", "온도", -10.0, 50.0, "°C"),
            ("humidity", "습도", 0.0, 100.0, "%"),
        )):
            ttk.Label(sensors, text=label).grid(row=row, column=0, padx=(0, 12), pady=8)
            variable = tk.DoubleVar(root)
            scale = ttk.Scale(sensors, from_=lo, to=hi, variable=variable,
                              command=lambda value, key=key: self.slide(key, value))
            scale.grid(row=row, column=1, sticky="ew", pady=8)
            shown = ttk.Label(sensors, width=15, anchor="e")
            shown.grid(row=row, column=2, padx=(8, 0))
            self.sensor_values[key] = (variable, unit)
            self.sensor_labels[key] = shown

        buttons = ttk.Frame(left)
        buttons.grid(row=2, column=0, sticky="ew")
        buttons.columnconfigure(3, weight=1)
        self.input_button = ttk.Button(buttons, command=self.press_input)
        self.input_button.grid(row=0, column=0, padx=(0, 8))
        self.drop_button = ttk.Button(buttons, text="연결 끊기", command=self.app.drop_connections)
        self.drop_button.grid(row=0, column=1, padx=(0, 8))
        ttk.Button(buttons, text="초기화", command=self.reset).grid(row=0, column=2)
        self.clients = ttk.Label(buttons, text="연결 수: 0", anchor="e")
        self.clients.grid(row=0, column=3, sticky="ew")

        logs = ttk.LabelFrame(frame, text="최근 로그 (최대 20줄)", padding=8)
        logs.grid(row=3, column=1, sticky="nsew")
        logs.rowconfigure(0, weight=1)
        logs.columnconfigure(0, weight=1)
        self.log = tk.Text(logs, width=48, height=20, wrap="char", state="disabled",
                           background="#1e1e1e", foreground="#dddddd", font="TkFixedFont")
        self.log.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(logs, command=self.log.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.log.configure(yscrollcommand=scroll.set)

    def slide(self, key, value):
        self.app.session.set_environment(**{key: round(float(value), 1) + 0.0})
        self.refresh()

    def press_input(self):
        self.app.session.press_input()
        self.refresh()

    def reset(self):
        self.app.session.reset()
        self.app.log("보드 상태 초기화")
        self.refresh()

    def refresh(self):
        state = self.app.session.snapshot().state
        runtime = self.app.runtime_state()
        for index, value in enumerate(state.leds):
            color = "#dddddd" if not value else "#ff%02x%02x" % ((210 - value * 170 // 255,) * 2)
            self.leds.itemconfigure(self.led_circles[index], fill=color)
            self.leds.itemconfigure(self.led_values[index], text=str(value))
        on = state.blink and time.monotonic() % 1.0 < 0.5
        self.leds.itemconfigure(self.blink_dot, fill="#2b7cff" if on else "#bbbbbb")
        self.leds.itemconfigure(self.blink_text, text="내장 LED: " + ("깜빡임" if state.blink else "꺼짐"))
        for key, (variable, unit) in self.sensor_values.items():
            value = getattr(state, key)
            # Variable.set does not invoke Scale.command. Preserve even out-of-range API values.
            variable.set(value)
            shown = ("%.1f " if abs(value) < 1e6 else "%.3g ") % value + unit
            self.sensor_labels[key].configure(text=shown)
        self.input_button.configure(text="입력 버튼: %s" % state.input_value)
        self.clients.configure(text="연결 수: %s" % runtime["clients"])
        self.drop_button.configure(state="normal" if runtime["clients"] else "disabled")
        tcp = runtime["services"]["tcp"]
        if tcp["enabled"]:
            port = tcp["port"]
            instructions = ("앱의 [시뮬레이터 주소]에 입력하고 [제어 시작]을 누르세요.\n"
                            "에뮬레이터: 10.0.2.2:%s · 실기기: 이 PC의 LAN IPv4:%s" % (port, port))
        else:
            instructions = "TCP 사용 안 함\n온도·습도와 입력 버튼으로 보드 상태를 변경하세요."
        self.instructions.configure(text=instructions)
        labels = []
        for name, status in runtime["services"].items():
            labels.append("%s: %s" % (name.upper(),
                          "%s (%s)" % (status["port"], "실행 중" if status["running"] else "중지됨")
                          if status["enabled"] else "사용 안 함"))
        self.services.configure(text=" · ".join(labels))
        if runtime["log"] != self.last_log:
            self.last_log = runtime["log"]
            lines = []
            for entry in runtime["log"]:
                text = entry[:300] + ("…" if len(entry) > 300 else "")
                lines.append("".join("?" if unicodedata.category(ch) == "Cc" else ch for ch in text))
            first, last = self.log.yview()
            self.log.configure(state="normal")
            self.log.delete("1.0", "end")
            self.log.insert("1.0", "\n".join(lines))
            self.log.configure(state="disabled")
            if last >= 0.999:
                self.log.see("end")
            else:
                self.log.yview_moveto(first)

    def schedule(self):
        self.timer = self.root.after(50, self.tick)

    def tick(self):
        self.timer = None
        if self.app.check_health():
            self.refresh()
            self.schedule()

    def close(self):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer = None


def port_number(value):
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("포트는 0~65535의 정수로 지정하세요.") from None
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError("포트는 0~65535의 정수로 지정하세요.")
    return port


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="WlEno 시뮬레이터", prog="main.py")
    parser.add_argument("--name", default="WlEno_SIM1", help="장치 이름 (기본 WlEno_SIM1)")
    parser.add_argument("--bind", default="0.0.0.0", help="TCP·UDP 바인드 주소")
    parser.add_argument("--http-bind", default="127.0.0.1", help="HTTP API 바인드 주소")
    for name, default in (("tcp", 8266), ("udp", 8267), ("http", 8080)):
        parser.add_argument("--" + name, type=port_number, default=default,
                            help="%s 포트 (기본 %s, 0: 자동 할당)" % (name.upper(), default))
        parser.add_argument("--no-" + name, action="store_true", help=name.upper() + " 사용 안 함")
    parser.add_argument("--no-window", action="store_true", help="Tkinter 없이 실행")
    args = parser.parse_args(argv)
    args.name = args.name.encode("utf-8", "replace").decode("utf-8")
    if not args.name.strip():
        parser.error("장치 이름을 입력하세요 (--name).")
    if args.no_window and args.no_tcp and args.no_udp and args.no_http:
        parser.error("창과 모든 서비스가 꺼져 있습니다. 창 또는 서비스를 하나 이상 사용하세요.")
    return args


def main(argv=None):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    return Application(parse_args(argv)).run()


if __name__ == "__main__":
    sys.exit(main())
