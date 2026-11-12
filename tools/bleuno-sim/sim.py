#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pygame-ce>=2.5"]
# ///
# BLEuno 시뮬레이터 — PC에서 돌리는 가짜 보드.
#
# 보드 없이 Wi-Fi(TCP)로 앱을 연습하거나, AI 에이전트 같은 다른 프로그램이 보드 대신 붙을 때 쓴다.
# 명령·응답은 bleuno 보드와 같다.
#   TCP  8266 : 한 줄 명령 → JSON 한 줄 응답 (앱이 붙는 곳)
#   UDP  8267 : "bleuno?" 를 받으면 {"name":..,"port":8266} 로 답한다 (앱의 [검색])
#   HTTP 8080 : HTTP API. GET /state, POST /set·/input·/drop (기본은 이 PC에서만 열린다)
#   화면      : 따로 뜨는 창. LED·온도·습도·입력 버튼·연결 끊기·로그
#
# 실행: python sim.py [--name ESP32_BLE_SIM1] [--tcp 8266] [--udp 8267] [--http 8080]
#                     [--bind 0.0.0.0] [--http-bind 127.0.0.1] [--no-window]
# 이름은 ESP32_BLE 로 시작해야 12~15주차 예제의 [검색] 목록에 나온다.
# 끝내기: 시뮬레이터 창을 닫거나 Ctrl+C
# 화면은 pygame-ce 로 그린다(Python 3.10 이상, 설치: py -m pip install pygame-ce).
# --no-window 로 창 없이 돌리면 표준 라이브러리만 쓴다(Python 3.9 이상).

import argparse
import asyncio
import ipaddress
import json
import math
import os
import signal
import socket
import sys
import threading
import time
import unicodedata
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LED_COUNT = 4        # LED 4개, 인덱스 0~3
LOG_LINES = 20       # 화면에 보여 주는 최근 로그 줄 수
APP_NAME = "BLEuno-SIM"


# ---------------------------------------------------------------- JSON 한 줄

def dumps(obj):
    # 보드 응답과 같은 모양: 공백 없이, 키는 넣은 순서대로
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def to_int(text):
    # Fake 클라이언트의 toIntOrNull() ?: 0 과 같은 규칙으로 읽는다. 맨 앞 부호(+/-) 하나,
    # 그 뒤는 십진 숫자만, 32비트 정수 범위. 아니면 0이다(밑줄이 든 1_0, 소수 1.5 도 0).
    # Kotlin 은 글자를 UTF-16 한 칸씩 보므로 U+FFFF 밖의 숫자(수학 굵은 숫자 등)는 숫자가 아니다
    neg = text[:1] == "-"
    body = text[1:] if text[:1] in ("+", "-") else text
    if not body:
        return 0
    n = 0
    for ch in body:
        d = unicodedata.decimal(ch, -1) if ord(ch) <= 0xFFFF else -1
        if d < 0:
            return 0
        n = n * 10 + d
        if n > 2147483648:
            return 0
    n = -n if neg else n
    return n if n <= 2147483647 else 0


# ---------------------------------------------------------------- 보드 상태

class Board:
    """LED·온습도·로그를 한 곳에 둔다. 명령(asyncio)·HTTP API·화면 스레드가 함께 쓰므로 lock으로 지킨다."""

    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self.leds = [0] * LED_COUNT     # 밝기 0~255
        self.blink = False              # 내장 LED 깜빡임
        self.temperature = 24.5
        self.humidity = 40.0
        self.clients = 0
        self.log_lines = deque(maxlen=LOG_LINES)

    # ---- 로그: 화면용 deque 에 넣고 터미널에도 한 줄 찍는다
    def log(self, text):
        line = time.strftime("[%H:%M:%S] ") + text
        with self.lock:
            self.log_lines.append(line)
        print(line, flush=True)

    # ---- 화면(초당 30번)과 GET /state 가 읽어 가는 상태
    def state(self):
        with self.lock:
            return {
                "leds": list(self.leds),
                "blink": self.blink,
                "temperature": self.temperature,
                "humidity": self.humidity,
                "clients": self.clients,
                "log": list(self.log_lines),
            }

    def set_env(self, temperature=None, humidity=None):
        # JSON 의 숫자만 받는다. true·"30" 같은 값은 TypeError, NaN·Infinity 는 ValueError,
        # float 로 바꿀 수 없는 큰 정수는 OverflowError. 두 값을 먼저 검사해 하나라도 틀리면 아무것도 바꾸지 않는다
        def number(v):
            if v is None:
                return None
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise TypeError("숫자가 아니다")
            v = float(v)
            if not math.isfinite(v):
                raise ValueError("NaN·Infinity 는 받지 않는다")
            return v
        t, h = number(temperature), number(humidity)
        with self.lock:
            if t is not None:
                self.temperature = t
            if h is not None:
                self.humidity = h

    # ---- 보드 펌웨어처럼 앱이 연결될 때(onConnect → ledOff(-1))와
    #      연결이 끝날 때(onDisconnect → clearAllControl()) LED 를 모두 끈다
    def leds_off(self):
        with self.lock:
            self.leds = [0] * LED_COUNT

    # ---- LED 값 쓰기. 인덱스 -1은 전체, 범위 밖은 무시한다
    def _set_led(self, index, value):
        value = max(0, min(255, value))
        if index == -1:
            self.leds = [value] * LED_COUNT
        elif 0 <= index < LED_COUNT:
            self.leds[index] = value

    # ---- 명령 한 줄 → 응답 JSON 한 줄. 규칙은 FakeBleunoClient.respond()와 같다. Fake 와 다른 것은
    #      dht11 값(화면 슬라이더), about 의 app·version, 공백만 있는 줄이다(Fake 는 send() 가 걸러 답이 없다).
    #      str.split() 은 탭·전각 공백 같은 다른 공백 글자도 띄어쓰기로 본다(보드는 반각 띄어쓰기로만 나눈다)
    def respond(self, line):
        tokens = line.split()
        if not tokens:
            return dumps({"result": "fail", "ms": "need command"})
        cmd, args = tokens[0], tokens[1:]

        if cmd == "on":
            if not args:
                return dumps({"result": "err", "ms": "need pin index"})
            with self.lock:
                for a in args:
                    self._set_led(to_int(a), 255)
            return dumps({"result": "ok", "ms": "led(s) on"})

        if cmd == "off":
            if not args:
                return dumps({"result": "err", "ms": "need pin index"})
            with self.lock:
                for a in args:
                    self._set_led(to_int(a), 0)
            return dumps({"result": "ok", "ms": "led(s) off"})

        if cmd == "pwm":
            if len(args) < 2:
                return dumps({"result": "err", "ms": "need pin index and pwm value"})
            index, value = to_int(args[0]), to_int(args[1])
            if index < 0:
                with self.lock:
                    self._set_led(-1, value)
                return dumps({"result": "ok", "ms": "pwm set"})
            if index >= LED_COUNT:
                return dumps({"result": "err", "ms": "pwm pin index error"})
            if value < 0 or value > 255:
                return dumps({"result": "err", "ms": "pwm value range 0~255"})
            with self.lock:
                self._set_led(index, value)
            return dumps({"result": "ok", "ms": "pwm set"})

        if cmd == "dht11":
            with self.lock:
                t, h = self.temperature, self.humidity
            return dumps({"result": "ok", "value": "[%.1f,%.1f]" % (t, h)})

        if cmd == "about":
            return dumps({
                "result": "ok",
                "os": "cronos-v1",
                "app": APP_NAME,
                "version": "1.0.5_sim",
                "author": "gbox3d",
                "chipid": 1234567890,
            })

        if cmd == "blink":
            with self.lock:
                self.blink = True
            return dumps({"result": "ok", "ms": "led blink"})

        if cmd == "stopblk":
            with self.lock:
                self.blink = False
            return dumps({"result": "ok", "ms": "led stop blink"})

        return dumps({"result": "fail", "ms": "unknown command"})


# ---------------------------------------------------------------- TCP 서버 (명령·응답·이벤트)

class TcpSide:
    """연결된 앱마다 handle() 하나. 응답은 보낸 쪽에만, 이벤트는 모두에게 보낸다.

    연결 받기(accept)만은 스레드에서 보통 소켓으로 한다(UdpSide 와 같은 까닭). Windows 의
    asyncio 는 연결 직후 끊긴 연결을 받다가 오류가 나면 명령 포트를 닫아 버려, 그 뒤로는
    앱이 붙지 못한다. 받은 연결은 asyncio 로 넘겨 handle() 이 맡는다.
    """

    def __init__(self, board):
        self.board = board
        self.writers = set()      # asyncio 스레드에서만 만진다
        self.tasks = set()        # 연결마다 도는 작업. 끝나기 전에 사라지지 않게 잡아 둔다
        self.input_value = 0      # 입력 이벤트 value. 누를 때마다 0/1 바뀐다
        self.loop = None
        self.main_task = None     # run() 작업. 화면을 닫으면 stop() 이 취소한다
        self.sock = None
        self.running = True

    def listen(self, bind, port):
        self.sock = socket.create_server((bind, port))   # 포트를 못 열면 여기서 OSError
        self.sock.settimeout(0.5)                        # 0.5초마다 깨어나 끝낼지 확인한다
        threading.Thread(target=self._accept_loop, name="tcp", daemon=True).start()

    def _accept_loop(self):
        while self.running:
            try:
                conn, _ = self.sock.accept()
            except socket.timeout:
                continue
            except OSError:
                if not self.running:
                    break                      # close() 로 닫혔다
                continue                       # 연결 직후 끊긴 연결 등. 무시하고 계속 받는다
            try:
                self.loop.call_soon_threadsafe(self._start, conn)
            except RuntimeError:               # 이미 끝나는 중이다
                conn.close()
                break

    def _start(self, conn):
        if not self.running:                   # 끝나는 중에 들어온 연결은 받지 않는다
            conn.close()
            return
        task = self.loop.create_task(self._serve(conn))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    async def _serve(self, conn):
        try:
            reader, writer = await asyncio.open_connection(sock=conn)
        except OSError:
            conn.close()
            return
        await self.handle(reader, writer)

    def close(self):
        self.running = False
        try:
            self.sock.close()
        except OSError:
            pass

    async def handle(self, reader, writer):
        peer = writer.get_extra_info("peername") or ("?", 0)
        tag = "[%s:%s]" % (peer[0], peer[1])
        self.writers.add(writer)
        self._count()
        self.board.log("%s 연결 (%d개)" % (tag, len(self.writers)))
        try:
            self.board.leds_off()                  # 보드처럼 연결되면 LED 를 모두 끈다
            # 연결 직후 서버가 먼저 보내는 인사 한 줄
            hello = dumps({"event": "hello", "name": self.board.name, "app": APP_NAME})
            writer.write((hello + "\n").encode("utf-8"))
            await writer.drain()
            while True:
                raw = await reader.readline()
                if not raw.endswith(b"\n"):
                    break                          # 상대가 끊음(EOF). 줄 끝 없이 남은 조각은 버린다
                if raw in (b"\n", b"\r\n"):
                    # 길이 0인 줄(\n)에는 보드처럼 답하지 않는다. \r\n 만 있는 줄에도 답하지 않는다
                    # (보드는 펌웨어 소스로 보면 \r 을 명령으로 읽어 unknown command 로 답한다)
                    continue
                line = raw.decode("utf-8", "replace").strip()
                resp = self.board.respond(line)
                self.board.log("%s %s → %s" % (tag, line, resp))
                writer.write((resp + "\n").encode("utf-8"))
                await writer.drain()
        except ValueError:
            # 한 줄이 64KiB 를 넘었다. readline 이 ValueError 를 던진다. 연결을 끊는다
            self.board.log("%s 너무 긴 줄 → 연결 끊음" % tag)
        except (OSError, asyncio.IncompleteReadError):
            pass
        finally:
            self.writers.discard(writer)
            self._count()
            self._close(writer)
            self.board.leds_off()                  # 보드처럼 연결이 끝나면 LED 를 모두 끈다
            self.board.log("%s 해제 (%d개)" % (tag, len(self.writers)))

    def _count(self):
        with self.board.lock:
            self.board.clients = len(self.writers)

    @staticmethod
    def _close(writer):
        try:
            writer.close()
        except Exception:
            pass

    # ---- 화면 [입력 버튼]·POST /input: 연결된 모두에게 input 이벤트. src 는 로그에 남길 출처
    def send_input_event(self, src="화면"):
        self.input_value = 1 - self.input_value
        event = dumps({"event": "input", "index": 0, "value": self.input_value})
        self.board.log("[%s] 입력 버튼 → %s (%d개에 전송)" % (src, event, len(self.writers)))
        for w in list(self.writers):
            try:
                w.write((event + "\n").encode("utf-8"))
            except Exception:
                pass

    # ---- 화면 [연결 끊기]·POST /drop: 소켓을 모두 닫는다. 앱은 "끊김"이 된다
    def drop_all(self, src="화면"):
        self.board.log("[%s] 연결 끊기 (%d개)" % (src, len(self.writers)))
        for w in list(self.writers):
            self._close(w)

    # HTTP·화면 스레드에서 부르는 통로. asyncio 스레드로 넘긴다
    def call_from_thread(self, fn):
        if self.loop is not None:
            try:
                self.loop.call_soon_threadsafe(fn)
            except RuntimeError:
                pass                           # 끝나는 중이라 루프가 이미 닫혔다

    # ---- 화면을 닫거나 화면에서 Ctrl+C 를 받으면 메인 스레드가 부른다. run() 을 끝낸다
    def stop(self):
        if self.main_task is not None:
            self.call_from_thread(self.main_task.cancel)


# ---------------------------------------------------------------- UDP (장치 찾기)

class UdpSide:
    """'bleuno?' 를 받으면 보낸 쪽에 이름과 TCP 포트를 알려 준다.

    asyncio 대신 스레드에서 보통 소켓으로 받는다. Windows 의 Python 3.9·3.10 은
    asyncio UDP 가 닫힌 포트로 답을 한 번 보내면 그 뒤로 받기를 멈추기 때문이다.
    """

    def __init__(self, board, bind, port, tcp_port):
        self.board = board
        self.tcp_port = tcp_port
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind((bind, port))       # 포트를 못 열면 여기서 OSError
        except OSError:
            self.sock.close()
            raise
        self.sock.settimeout(0.5)              # 0.5초마다 깨어나 끝낼지 확인한다

    def start(self):
        threading.Thread(target=self._loop, name="udp", daemon=True).start()

    def _loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(512)
            except socket.timeout:
                continue
            except OSError:
                if not self.running:
                    break                      # close() 로 닫혔다
                # Windows 는 앞서 보낸 답이 닫힌 포트로 갔을 때 여기로 알린다(연결 재설정).
                # 너무 큰 데이터도 여기로 온다. 무시하고 계속 받는다
                continue
            if data.strip() != b"bleuno?":
                continue
            reply = dumps({"name": self.board.name, "port": self.tcp_port})
            self.board.log("[%s:%s] bleuno? → %s" % (addr[0], addr[1], reply))
            try:
                self.sock.sendto(reply.encode("utf-8"), addr)
            except OSError:
                pass

    def close(self):
        self.running = False
        try:
            self.sock.close()
        except OSError:
            pass


# ---------------------------------------------------------------- HTTP API

def make_handler(board, tcp):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass                                   # 요청마다 찍히는 기본 로그는 끈다

        def _send(self, code, body, ctype):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj, code=200):
            self._send(code, dumps(obj).encode("utf-8"), "application/json; charset=utf-8")

        def do_GET(self):
            if self.path == "/state":
                self._json(board.state())
            else:
                self._json({"result": "fail", "ms": "not found"}, 404)

        def do_POST(self):
            # /set 의 본문은 수십 바이트다. 길이가 숫자가 아니거나 너무 크면 읽지 않는다
            try:
                length = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                length = -1
            if not 0 <= length <= 65536:
                self._json({"result": "err", "ms": "bad Content-Length"}, 400)
                return
            raw = self.rfile.read(length) if length > 0 else b""
            if self.path == "/set":
                try:
                    data = json.loads(raw.decode("utf-8")) if raw else {}
                    board.set_env(data.get("temperature"), data.get("humidity"))
                except (ValueError, TypeError, AttributeError, OverflowError):
                    self._json({"result": "err", "ms": "need json {temperature, humidity}"}, 400)
                    return
                self._json({"result": "ok"})
            elif self.path == "/input":
                tcp.call_from_thread(lambda: tcp.send_input_event("API"))
                self._json({"result": "ok"})
            elif self.path == "/drop":
                tcp.call_from_thread(lambda: tcp.drop_all("API"))
                self._json({"result": "ok"})
            else:
                self._json({"result": "fail", "ms": "not found"}, 404)

    return Handler


# ---------------------------------------------------------------- 화면 (pygame 창)

# 한글이 들어 있는 글꼴. 앞의 것부터 찾는다(Windows, macOS, Linux 순)
FONT_NAMES = ["malgungothic", "applesdgothicneo", "nanumgothic", "notosanscjkkr", "notosanskr"]


def load_pygame():
    # 화면을 그리는 pygame-ce 와 못 불러온 까닭. 불러오면 (pygame, None), 못 불러오면 (None, 까닭).
    # 가져올 때 찍히는 인사 줄은 끈다
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    try:
        import pygame
        import pygame.freetype
    except ImportError as e:
        return None, str(e)
    return pygame, None


def mix(a, b, t):
    # 색 a 에서 b 쪽으로 t(0~1) 만큼 옮긴 색
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


class Window:
    """시뮬레이터 화면. 메인 스레드에서 초당 30번 상태를 읽어 다시 그린다.

    명령(TCP)·검색(UDP)·HTTP API 는 다른 스레드에서 돈다. 다만 Windows 에서 창 제목 줄을 누르고
    있는 동안에는 pygame 이 GIL 을 쥔 채 멈추므로 그 스레드들도 함께 멈췄다가, 놓으면 이어서 답한다.
    """

    W, H = 980, 484
    BG = (244, 245, 247)
    CARD = (255, 255, 255)
    INK = (34, 34, 34)
    HEAD = (68, 68, 68)
    SUB = (102, 102, 102)
    OFF = (221, 221, 221)
    RING = (187, 187, 187)
    RED = (255, 60, 40)
    BLUE = (43, 124, 255)
    TRACK = (210, 212, 216)
    LOG_BG = (30, 30, 30)
    LOG_INK = (221, 221, 221)
    DANGER = (187, 0, 0)
    LOG_CHARS = 300          # 로그 한 줄을 화면에 보일 때의 최대 글자 수(터미널에는 다 찍힌다)

    def __init__(self, pg, board, tcp, args):
        self.pg, self.board, self.tcp = pg, board, tcp
        pg.display.init()
        pg.freetype.init()
        self.screen = pg.display.set_mode((self.W, self.H))
        pg.display.set_caption("BLEuno 시뮬레이터 — %s" % board.name)
        path = pg.font.match_font(FONT_NAMES)
        if path is None:
            print("주의: 한글 글꼴을 찾지 못했다. 화면의 한글이 네모로 보일 수 있다.", flush=True)

        def font(size, bold=False):
            f = pg.freetype.Font(path, size)
            f.origin = True                    # 그리는 자리의 y 는 글자의 기준선
            f.strong = bold
            return f

        self.f_title = font(20, True)
        self.f_head = font(15, True)
        self.f_text = font(14)
        self.f_small = font(13)
        self.f_log = font(12)
        self.clock = pg.time.Clock()
        self.drag = None                       # 끌고 있는 슬라이더("temperature"·"humidity")
        self.wrapped = {}                      # 접은 줄 캐시
        self.sub = ("TCP %d · UDP %d · [검색]에 나오지 않으면 앱의 주소 칸에 직접 입력하세요. "
                    "에뮬레이터: 10.0.2.2:%d, 실기기: 이 PC의 IP:%d" % (args.tcp, args.udp, args.tcp, args.tcp))
        R = pg.Rect
        self.c_led = R(16, 92, 470, 182)
        self.c_dht = R(16, 286, 470, 110)
        self.c_btn = R(16, 408, 470, 60)
        self.c_log = R(498, 92, self.W - 514, 376)
        x, w = self.c_dht.x + 70, self.c_dht.w - 70 - 110
        self.sliders = {
            "temperature": ("온도", R(x, self.c_dht.y + 53, w, 6), -10.0, 50.0, "°C"),
            "humidity": ("습도", R(x, self.c_dht.y + 83, w, 6), 0.0, 100.0, "%"),
        }
        self.b_input = R(self.c_btn.x + 16, self.c_btn.y + 12, 120, 36)
        self.b_drop = R(self.c_btn.x + 148, self.c_btn.y + 12, 120, 36)

    # ---- 글자 한 줄. y 는 줄의 위쪽. anchor 가 "right" 면 x 가 오른쪽 끝, "center" 면 가운데
    def put(self, font, text, color, x, y, anchor="left"):
        if anchor != "left":
            w = font.get_rect(text).width
            x -= w if anchor == "right" else w // 2
        font.render_to(self.screen, (x, y + font.get_sized_ascender()), text, color)

    # ---- 폭 width 에 맞게 글자 단위로 접는다
    def wrap(self, font, text, width):
        key = (id(font), text, width)
        lines = self.wrapped.get(key)
        if lines is None:
            lines, cur, used = [], "", 0.0
            for ch, m in zip(text, font.get_metrics(text)):
                adv = m[4] if m else 0.0
                if cur and used + adv > width:
                    lines.append(cur)
                    cur, used = "", 0.0
                cur += ch
                used += adv
            lines.append(cur)
            if len(self.wrapped) > 500:
                self.wrapped.clear()
            self.wrapped[key] = lines
        return lines

    # ---- 폭 width 를 넘으면 뒤를 줄이고 … 를 붙인다(아주 긴 --name)
    def fit(self, font, text, width):
        key = ("fit", id(font), text, width)
        out = self.wrapped.get(key)
        if out is None:
            out = text
            while len(out) > 1 and font.get_rect(out).width > width:
                out = out[:-2] + "…"
            self.wrapped[key] = out
        return out

    def led_center(self, i):
        # 밝은 LED 의 번짐(반지름 46)이 카드 제목에 닿지 않는 높이
        return self.c_led.x + 56 + i * 100, self.c_led.y + 80

    def card(self, r, title=None):
        self.pg.draw.rect(self.screen, self.CARD, r, border_radius=10)
        if title:
            self.put(self.f_head, title, self.HEAD, r.x + 16, r.y + 12)

    def draw(self, s):
        pg, scr = self.pg, self.screen
        scr.fill(self.BG)
        self.put(self.f_title, self.fit(self.f_title, "BLEuno 시뮬레이터 — %s" % self.board.name, self.W - 32),
                 self.INK, 16, 12)
        y = 46
        for line in self.wrap(self.f_small, self.sub, self.W - 32)[:2]:
            self.put(self.f_small, line, self.SUB, 16, y)
            y += self.f_small.get_sized_height() + 3

        # LED 4개와 내장 LED
        c = self.c_led
        self.card(c, "LED (인덱스 0~3, 밝기 0~255)")
        for i in range(LED_COUNT):
            v = s["leds"][i]
            cx, cy = self.led_center(i)
            if v:
                a = 0.25 + 0.75 * v / 255
                glow = round(18 * v / 255)
                if glow:
                    r = 28 + glow
                    halo = pg.Surface((2 * r, 2 * r), pg.SRCALPHA)
                    pg.draw.circle(halo, self.RED + (round(70 * a),), (r, r), r)
                    scr.blit(halo, (cx - r, cy - r))
                fill = mix(self.CARD, self.RED, a)
            else:
                fill = self.OFF
            pg.draw.circle(scr, fill, (cx, cy), 28)
            pg.draw.circle(scr, self.RING, (cx, cy), 28, 2)
            self.put(self.f_small, "LED %d" % i, self.SUB, cx, cy + 36, "center")
            self.put(self.f_small, str(v), self.INK, cx, cy + 54, "center")
        on = s["blink"] and time.monotonic() % 1.0 < 0.5
        dot_y = c.bottom - 22
        pg.draw.circle(scr, self.BLUE if on else self.RING, (c.x + 23, dot_y), 7)
        self.put(self.f_small, "내장 LED: " + ("깜빡임" if s["blink"] else "꺼짐"), self.SUB,
                 c.x + 38, dot_y - self.f_small.get_sized_height() // 2)

        # 온도·습도 슬라이더
        c = self.c_dht
        self.card(c, "DHT11 (dht11 명령이 읽어 가는 값)")
        for key, (label, track, lo, hi, unit) in self.sliders.items():
            val = s[key]
            # HTTP API 로 넣은 아주 큰 값은 지수로 줄여 보인다
            shown = ("%.1f " if abs(val) < 1e6 else "%.3g ") % val + unit
            mid = track.centery - self.f_text.get_sized_height() // 2
            self.put(self.f_text, label, self.INK, c.x + 16, mid)
            pg.draw.rect(scr, self.TRACK, track, border_radius=3)
            kx = track.x + round((min(max(val, lo), hi) - lo) / (hi - lo) * track.w)
            if kx > track.x:
                pg.draw.rect(scr, self.BLUE, (track.x, track.y, kx - track.x, track.h), border_radius=3)
            pg.draw.circle(scr, self.CARD, (kx, track.centery), 9)
            pg.draw.circle(scr, self.BLUE, (kx, track.centery), 9, 2)
            self.put(self.f_text, shown, self.INK, c.right - 16, mid, "right")

        # 버튼과 연결 수
        c = self.c_btn
        self.card(c)
        mouse = pg.mouse.get_pos()
        for r, label, danger in ((self.b_input, "입력 버튼", False), (self.b_drop, "연결 끊기", True)):
            pg.draw.rect(scr, (238, 238, 238) if r.collidepoint(mouse) else (250, 250, 250), r, border_radius=6)
            pg.draw.rect(scr, (221, 51, 51) if danger else (153, 153, 153), r, 1, border_radius=6)
            self.put(self.f_text, label, self.DANGER if danger else self.INK,
                     r.centerx, r.centery - self.f_text.get_sized_height() // 2, "center")
        self.put(self.f_text, "연결 수: %d" % s["clients"], self.INK,
                 c.right - 16, c.centery - self.f_text.get_sized_height() // 2, "right")

        # 최근 명령 로그. 칸에 다 들어가지 않으면 최근 줄만 보인다
        c = self.c_log
        self.card(c, "최근 명령 로그")
        box = pg.Rect(c.x + 12, c.y + 40, c.w - 24, c.h - 52)
        pg.draw.rect(scr, self.LOG_BG, box, border_radius=6)
        lh = self.f_log.get_sized_height() + 2
        y = box.y + 8
        for line in self.log_rows(s["log"], box.w - 20, (box.h - 16) // lh):
            self.put(self.f_log, line, self.LOG_INK, box.x + 10, y)
            y += lh

    # ---- 로그 칸에 보일 줄. 긴 줄은 접고, fit 줄을 넘으면 최근 줄만 남긴다
    def log_rows(self, log, width, fit):
        rows = []
        for entry in reversed(log):
            if len(rows) >= fit:
                break
            if len(entry) > self.LOG_CHARS:
                entry = entry[:self.LOG_CHARS] + "…"
            # 제어 문자(앱이 보낸 \x00 등)와 글꼴에 없는 글자(이모지 등, metrics 가 None)는 ? 로 보인다.
            # 글꼴에 없는 글자는 폭을 잴 수 없어 그대로 두면 줄을 접지 못한다
            entry = "".join("?" if m is None or unicodedata.category(ch) == "Cc" else ch
                            for ch, m in zip(entry, self.f_log.get_metrics(entry)))
            rows[:0] = self.wrap(self.f_log, entry, width)
        return rows[max(0, len(rows) - fit):] if fit > 0 else []

    def slide(self, x):
        _, track, lo, hi, _ = self.sliders[self.drag]
        frac = min(max((x - track.x) / track.w, 0.0), 1.0)
        value = round(lo + frac * (hi - lo), 1) + 0.0      # + 0.0: -0.0 을 0.0 으로
        self.board.set_env(**{self.drag: value})

    def handle(self, ev):
        pg = self.pg
        if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
            if self.b_input.collidepoint(ev.pos):
                self.tcp.call_from_thread(self.tcp.send_input_event)
            elif self.b_drop.collidepoint(ev.pos):
                self.tcp.call_from_thread(self.tcp.drop_all)
            else:
                for key, (_, track, _, _, _) in self.sliders.items():
                    if track.inflate(24, 24).collidepoint(ev.pos):
                        self.drag = key
                        self.slide(ev.pos[0])
        elif ev.type == pg.MOUSEMOTION and self.drag:
            if ev.buttons[0]:
                self.slide(ev.pos[0])
            else:
                self.drag = None
        elif ev.type == pg.MOUSEBUTTONUP and ev.button == 1:
            self.drag = None

    # ---- 이벤트를 처리하고 한 번 그린다. 창을 닫으면 False
    def step(self):
        for ev in self.pg.event.get():
            if ev.type == self.pg.QUIT:
                return False
            self.handle(ev)
        self.draw(self.board.state())
        self.pg.display.flip()
        return True

    def loop(self, alive):
        while alive() and self.step():
            self.clock.tick(30)


# ---------------------------------------------------------------- 시작 안내

# 같은 Wi-Fi 에서 쓰는 사설 주소. 이 주소를 앞에 둔다
PRIVATE_NETS = [ipaddress.ip_network(n) for n in ("192.168.0.0/16", "10.0.0.0/8", "172.16.0.0/12")]
VPN_NET = ipaddress.ip_network("100.64.0.0/10")        # Tailscale 같은 VPN 이 쓰는 주소
AUTO_NET = ipaddress.ip_network("169.254.0.0/16")      # 주소를 못 받았을 때 스스로 붙인 주소


def ip_rank(ip):
    # 0: 사설 주소(먼저 시도), 1: 그 밖, 2: VPN·자동 할당(뒤로)
    a = ipaddress.ip_address(ip)
    if a in VPN_NET or a in AUTO_NET:
        return 2
    if any(a in n for n in PRIVATE_NETS):
        return 0
    return 1


def ip_label(ip):
    a = ipaddress.ip_address(ip)
    if a in VPN_NET:
        return ip + "(VPN?)"
    if a in AUTO_NET:
        return ip + "(자동 할당)"
    return ip


def local_ipv4_list():
    # 이 PC의 IPv4 주소. 실기기에서 입력할 주소다. 127.x 는 뺀다.
    # 기본 경로 주소를 맨 앞에 두고, 사설 주소 → 그 밖 → VPN·자동 할당 순서로 다시 놓는다.
    found = []
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127.") and ip not in found:
                found.append(ip)
    except OSError:
        pass
    route_ip = None
    try:
        # 기본 경로가 쓰는 주소를 하나 더 확인한다(실제로 보내지는 않는다)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if not ip.startswith("127."):
            route_ip = ip
            if ip not in found:
                found.append(ip)
    except OSError:
        pass
    # VPN·자동 할당은 맨 뒤, 그 밖에서는 기본 경로 주소가 맨 앞. 순서 값이 같으면 원래 순서를 지킨다
    found.sort(key=lambda ip: (ip_rank(ip) == 2, ip != route_ip, ip_rank(ip)))
    return found


def print_banner(args):
    ips = local_ipv4_list()
    print("=== BLEuno 시뮬레이터 (%s) ===" % args.name)
    print("명령(TCP) 포트 %d, 검색(UDP) 포트 %d, 바인드 %s" % (args.tcp, args.udp, args.bind))
    print("이 PC의 IPv4 주소(실기기용, 앞의 것부터): %s"
          % (", ".join(ip_label(ip) for ip in ips) if ips else "(찾지 못함. ipconfig 로 확인)"))
    print("에뮬레이터에서는 10.0.2.2:%d" % args.tcp)
    api_host = "127.0.0.1" if args.http_bind in ("0.0.0.0", "") else args.http_bind
    print("HTTP API: http://%s:%d/state" % (api_host, args.http))
    if not args.name.startswith("ESP32_BLE"):
        print("주의: 이름이 ESP32_BLE 로 시작하지 않으면 12~15주차 예제의 [검색] 목록에 나오지 않는다.")
    print("Windows 방화벽 창이 뜨면 [액세스 허용]을 누른다. 안 뜨면 포트 %d·%d을 인바운드로 허용한다."
          % (args.tcp, args.udp))
    print("끝내려면 Ctrl+C" if args.no_window else "끝내려면 시뮬레이터 창을 닫거나 Ctrl+C")
    sys.stdout.flush()


# ---------------------------------------------------------------- 메인

class SimHTTPServer(ThreadingHTTPServer):
    # Windows 에서 주소 재사용을 켜면 다른 프로그램이 쓰는 포트에도 열려 버린다.
    # 그러면 "포트를 열 수 없다" 안내가 안 나온다. 그래서 Windows 에서는 끈다.
    allow_reuse_address = (os.name != "nt")
    allow_reuse_port = False
    daemon_threads = True

    def handle_error(self, request, client_address):
        # 요청한 쪽이 응답을 다 받기 전에 끊으면 조용히 넘어간다
        if isinstance(sys.exc_info()[1], ConnectionError):
            return
        super().handle_error(request, client_address)


async def run(args, board, tcp, httpd, ready=None):
    loop = asyncio.get_running_loop()
    tcp.loop = loop
    tcp.main_task = asyncio.current_task()

    # 끊긴 연결에서 나온 OSError(재설정 등)를 asyncio 가 끝날 때 따로 알리지 않게 한다.
    # 그 밖의 오류는 그대로 보인다
    def on_loop_error(loop, context):
        if not isinstance(context.get("exception"), OSError):
            loop.default_exception_handler(context)
    loop.set_exception_handler(on_loop_error)

    if sys.version_info < (3, 11) and threading.current_thread() is threading.main_thread():
        # 3.9·3.10 의 asyncio.run 은 Ctrl+C 를 루프 안 아무 곳에서나 KeyboardInterrupt 로 던져서
        # 끝내기가 멈추거나 오류 줄이 남는다. 3.11 이후처럼 이 작업만 취소하게 한다
        # (화면이 있으면 이 함수는 다른 스레드에서 돌고, Ctrl+C 는 화면 쪽이 받는다)
        main_task = asyncio.current_task()

        def on_sigint(signum, frame):
            try:
                loop.call_soon_threadsafe(main_task.cancel)
            except RuntimeError:
                pass                           # 루프가 이미 닫혔다
        signal.signal(signal.SIGINT, on_sigint)

    tcp.listen(args.bind, args.tcp)
    try:
        udp = UdpSide(board, args.bind, args.udp, args.tcp)
    except OSError:
        tcp.close()
        raise
    udp.start()

    board.log("시작: TCP %d, UDP %d, HTTP %d" % (args.tcp, args.udp, args.http))
    if ready is not None:
        ready.set()

    try:
        # Windows 에서 Ctrl+C 가 바로 먹도록 짧게 깨어난다
        while True:
            await asyncio.sleep(0.5)
    finally:
        udp.close()
        tcp.close()
        for w in list(tcp.writers):
            tcp._close(w)
        # 남은 연결 작업이 '해제' 줄을 찍고 끝날 때까지 잠깐(최대 1초) 기다린다
        for t in list(tcp.tasks):
            t.cancel()
        if tcp.tasks:
            await asyncio.wait(list(tcp.tasks), timeout=1.0)


def run_here(args, board, tcp, httpd):
    # 창 없이(--no-window): 메인 스레드에서 asyncio 를 돌린다. Ctrl+C 로 끝난다
    try:
        asyncio.run(run(args, board, tcp, httpd))
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    except OSError as e:
        print("포트를 열 수 없다: %s (--tcp/--udp 로 다른 포트를 준다)" % e)
        return 1
    return 0


def run_with_window(args, board, tcp, httpd, pg):
    # 화면이 있으면 asyncio 는 다른 스레드에서 돌리고 메인 스레드는 창을 그린다
    # (macOS 는 창을 메인 스레드에서만 열 수 있다). 창을 닫거나 Ctrl+C 를 누르면 끝난다
    ready = threading.Event()
    failed = []

    def net():
        try:
            asyncio.run(run(args, board, tcp, httpd, ready))
        except asyncio.CancelledError:
            pass                               # stop() 으로 끝났다
        except OSError as e:
            failed.append(e)

    thread = threading.Thread(target=net, name="net", daemon=True)
    thread.start()
    code = 0
    try:
        while not ready.wait(0.1):
            if not thread.is_alive():
                print("포트를 열 수 없다: %s (--tcp/--udp 로 다른 포트를 준다)" % (failed[0] if failed else "?"),
                      flush=True)
                return 1
        Window(pg, board, tcp, args).loop(thread.is_alive)
        if not thread.is_alive():
            code = 1                           # 창을 닫기 전에 명령 쪽이 멈췄다
    except KeyboardInterrupt:
        pass
    except pg.error as e:
        print("시뮬레이터 창을 열 수 없다: %s (화면이 없는 컴퓨터면 --no-window 로 실행한다)" % e, flush=True)
        code = 1
    finally:
        # 끝내는 동안 Ctrl+C 를 한 번 더 눌러도 트레이스백 없이 끝나게 한다
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        pg.quit()
        tcp.stop()
        thread.join(5)
    return code


def main():
    p = argparse.ArgumentParser(description="BLEuno 시뮬레이터")
    p.add_argument("--name", default="ESP32_BLE_SIM1",
                   help="장치 이름 (기본 ESP32_BLE_SIM1). ESP32_BLE 로 시작해야 예제 목록에 나온다")
    p.add_argument("--tcp", type=int, default=8266, help="명령 포트 (기본 8266)")
    p.add_argument("--udp", type=int, default=8267, help="검색 포트 (기본 8267)")
    p.add_argument("--http", type=int, default=8080, help="HTTP API 포트 (기본 8080)")
    p.add_argument("--bind", default="0.0.0.0", help="TCP·UDP 바인드 주소 (기본 0.0.0.0)")
    p.add_argument("--http-bind", default="127.0.0.1",
                   help="HTTP API 바인드 주소 (기본 127.0.0.1: 이 PC에서만 열린다)")
    p.add_argument("--no-window", action="store_true",
                   help="시뮬레이터 창 없이 돌린다. pygame-ce 가 없어도 된다")
    args = p.parse_args()
    # 글자로 바꿀 수 없는 바이트가 든 이름(POSIX 의 surrogateescape)은 ? 로 바꿔 둔다.
    # 그대로 두면 창 제목·hello·검색 답을 만들다 멈춘다
    args.name = args.name.encode("utf-8", "replace").decode("utf-8")

    # 터미널 인코딩이 무엇이든 로그 때문에 멈추지 않게 한다
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass

    pg = None
    if not args.no_window:
        pg, why = load_pygame()
        if pg is None:
            print("화면을 그리는 pygame-ce 를 불러오지 못했다: %s" % why)
            if os.name == "nt":
                print("이 Python 에 한 번만 설치한다: py -m pip install pygame-ce"
                      " (python sim.py 로 실행했으면 python -m pip install pygame-ce)")
            else:
                print("이 Python 에 한 번만 설치한다: python3 -m pip install pygame-ce")
            print("이 Python: %s" % sys.executable)
            print("창 없이 돌리려면 --no-window 를 붙인다.")
            return 1

    board = Board(args.name)
    tcp = TcpSide(board)
    try:
        httpd = SimHTTPServer((args.http_bind, args.http), make_handler(board, tcp))
    except OSError as e:
        print("HTTP API %d 포트를 열 수 없다: %s (--http 로 다른 포트를 준다)" % (args.http, e))
        return 1

    print_banner(args)
    # HTTP API 와 검색(UDP)은 따로 스레드에서 돈다. TCP 는 asyncio 가 맡는다
    threading.Thread(target=httpd.serve_forever, name="http", daemon=True).start()
    if pg is None:
        code = run_here(args, board, tcp, httpd)
    else:
        code = run_with_window(args, board, tcp, httpd, pg)
    # 끝내는 동안(최대 0.5초) Ctrl+C 를 한 번 더 눌러도 트레이스백 없이 끝나게 한다
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    httpd.shutdown()
    httpd.server_close()
    print("종료")
    return code


if __name__ == "__main__":
    sys.exit(main())
