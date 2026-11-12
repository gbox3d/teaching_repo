#!/usr/bin/env python3
# BLEuno 시뮬레이터 — PC에서 돌리는 가짜 보드.
#
# 보드 없이 Wi-Fi(TCP)로 앱을 연습할 때 쓴다. 명령·응답은 bleuno 보드와 같다.
#   TCP  8266 : 한 줄 명령 → JSON 한 줄 응답 (앱이 붙는 곳)
#   UDP  8267 : "bleuno?" 를 받으면 {"name":..,"port":8266} 로 답한다 (앱의 [검색])
#   HTTP 8080 : 브라우저 화면. LED·온도·습도·입력 버튼·연결 끊기 (기본은 이 PC에서만 열린다)
#
# 실행: python sim.py [--name ESP32_BLE_SIM1] [--tcp 8266] [--udp 8267] [--http 8080]
#                     [--bind 0.0.0.0] [--http-bind 127.0.0.1]
# 이름은 ESP32_BLE 로 시작해야 12~15주차 예제의 [검색] 목록에 나온다.
# 끝내기: Ctrl+C
# 표준 라이브러리만 쓴다(3.9 이상). 외부 패키지 설치가 필요 없다.

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
    """LED·온습도·로그를 한 곳에 둔다. HTTP 스레드와 asyncio 스레드가 함께 쓰므로 lock으로 지킨다."""

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

    # ---- 화면이 0.5초마다 읽어 가는 JSON
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
        # 두 값을 먼저 숫자로 바꿔 본다. 하나라도 틀리면 아무것도 바꾸지 않는다(ValueError)
        t = None if temperature is None else float(temperature)
        h = None if humidity is None else float(humidity)
        for v in (t, h):
            if v is not None and not math.isfinite(v):
                raise ValueError("NaN·Infinity 는 받지 않는다")
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
                    continue                       # 길이 0인 줄에는 보드처럼 답하지 않는다
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

    # ---- 화면 [입력 버튼]: 연결된 모두에게 input 이벤트
    def send_input_event(self):
        self.input_value = 1 - self.input_value
        event = dumps({"event": "input", "index": 0, "value": self.input_value})
        self.board.log("[화면] 입력 버튼 → %s (%d개에 전송)" % (event, len(self.writers)))
        for w in list(self.writers):
            try:
                w.write((event + "\n").encode("utf-8"))
            except Exception:
                pass

    # ---- 화면 [연결 끊기]: 소켓을 모두 닫는다. 앱은 "끊김"이 된다
    def drop_all(self):
        self.board.log("[화면] 연결 끊기 (%d개)" % len(self.writers))
        for w in list(self.writers):
            self._close(w)

    # HTTP 스레드에서 부르는 통로. asyncio 스레드로 넘긴다
    def call_from_thread(self, fn):
        if self.loop is not None:
            try:
                self.loop.call_soon_threadsafe(fn)
            except RuntimeError:
                pass                           # 끝나는 중이라 루프가 이미 닫혔다


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


# ---------------------------------------------------------------- HTTP (브라우저 화면)

PAGE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<title>BLEuno 시뮬레이터 — __NAME__</title>
<style>
  body { font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif; background: #f4f5f7; color: #222; margin: 0; padding: 16px; }
  h1 { font-size: 20px; margin: 0 0 4px; }
  .sub { color: #666; font-size: 13px; margin-bottom: 16px; }
  .card { background: #fff; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }
  .card h2 { font-size: 15px; margin: 0 0 10px; color: #444; }
  .leds { display: flex; gap: 22px; align-items: flex-end; }
  .led { text-align: center; font-size: 12px; color: #666; }
  .led .dot { width: 56px; height: 56px; border-radius: 50%; margin: 0 auto 6px; border: 2px solid #bbb;
              background: #ddd; transition: background .2s, box-shadow .2s; }
  .builtin { display: flex; align-items: center; gap: 10px; margin-top: 12px; font-size: 13px; color: #555; }
  .builtin .dot { width: 14px; height: 14px; border-radius: 50%; background: #bbb; }
  .builtin .dot.on { background: #2b7cff; animation: blink 1s steps(1) infinite; }
  @keyframes blink { 50% { background: #bbb; } }
  .row { display: flex; align-items: center; gap: 10px; margin: 8px 0; font-size: 14px; }
  .row label { width: 48px; }
  .row input[type=range] { flex: 1; }
  .row .val { width: 72px; text-align: right; font-variant-numeric: tabular-nums; }
  button { font-size: 14px; padding: 8px 14px; border-radius: 6px; border: 1px solid #999; background: #fafafa; cursor: pointer; }
  button:hover { background: #eee; }
  button.danger { border-color: #d33; color: #b00; }
  .btns { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
  .status { font-size: 14px; margin-left: auto; }
  pre { background: #1e1e1e; color: #ddd; font-size: 12px; padding: 10px; border-radius: 6px; height: 300px;
        overflow: auto; margin: 0; white-space: pre-wrap; word-break: break-all; }
</style>
</head>
<body>
<h1>BLEuno 시뮬레이터 — __NAME__</h1>
<div class="sub">TCP __TCP__ · UDP __UDP__ · [검색]이 안 되면 앱의 주소 칸에 직접 넣는다: 에뮬레이터는 10.0.2.2:__TCP__, 실기기는 이 PC의 IP:__TCP__</div>

<div class="card">
  <h2>LED (인덱스 0~3, 밝기 0~255)</h2>
  <div class="leds" id="leds"></div>
  <div class="builtin"><div class="dot" id="builtin"></div><span id="builtin-text">내장 LED: 멈춤</span></div>
</div>

<div class="card">
  <h2>DHT11 (dht11 명령이 읽어 가는 값)</h2>
  <div class="row"><label>온도</label><input type="range" id="temp" min="-10" max="50" step="0.1"><span class="val" id="temp-val"></span></div>
  <div class="row"><label>습도</label><input type="range" id="hum" min="0" max="100" step="0.1"><span class="val" id="hum-val"></span></div>
</div>

<div class="card">
  <div class="btns">
    <button id="btn-input">입력 버튼</button>
    <button id="btn-drop" class="danger">연결 끊기</button>
    <span class="status">연결 수: <b id="clients">0</b></span>
  </div>
</div>

<div class="card">
  <h2>최근 명령 로그</h2>
  <pre id="log"></pre>
</div>

<script>
(function () {
  var ledsBox = document.getElementById('leds');
  var dots = [];
  for (var i = 0; i < 4; i++) {
    var d = document.createElement('div');
    d.className = 'led';
    d.innerHTML = '<div class="dot"></div>LED ' + i + '<br><span class="v">0</span>';
    ledsBox.appendChild(d);
    dots.push(d);
  }
  var temp = document.getElementById('temp'), hum = document.getElementById('hum');
  var tempVal = document.getElementById('temp-val'), humVal = document.getElementById('hum-val');

  function post(path, body) {
    return fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' },
                         body: body ? JSON.stringify(body) : '' }).catch(function () {});
  }

  function draw(s) {
    for (var i = 0; i < 4; i++) {
      var v = s.leds[i] || 0;
      var dot = dots[i].querySelector('.dot');
      if (v === 0) {
        dot.style.background = '#ddd';
        dot.style.boxShadow = 'none';
      } else {
        var a = 0.25 + 0.75 * v / 255;
        dot.style.background = 'rgba(255, 60, 40, ' + a + ')';
        dot.style.boxShadow = '0 0 ' + Math.round(18 * v / 255) + 'px rgba(255, 60, 40, ' + a + ')';
      }
      dots[i].querySelector('.v').textContent = v;
    }
    var b = document.getElementById('builtin');
    b.className = 'dot' + (s.blink ? ' on' : '');
    document.getElementById('builtin-text').textContent = '내장 LED: ' + (s.blink ? '깜빡임' : '멈춤');
    // 슬라이더를 잡고 있는 동안은 서버 값으로 덮어쓰지 않는다
    if (document.activeElement !== temp) temp.value = s.temperature;
    if (document.activeElement !== hum) hum.value = s.humidity;
    tempVal.textContent = Number(temp.value).toFixed(1) + ' °C';
    humVal.textContent = Number(hum.value).toFixed(1) + ' %';
    document.getElementById('clients').textContent = s.clients;
    var log = document.getElementById('log');
    var atBottom = log.scrollTop + log.clientHeight >= log.scrollHeight - 4;
    log.textContent = s.log.join('\n');
    if (atBottom) log.scrollTop = log.scrollHeight;
  }

  function poll() {
    fetch('/state').then(function (r) { return r.json(); }).then(draw).catch(function () {});
  }
  setInterval(poll, 500);
  poll();

  function sendEnv() {
    post('/set', { temperature: Number(temp.value), humidity: Number(hum.value) });
    tempVal.textContent = Number(temp.value).toFixed(1) + ' °C';
    humVal.textContent = Number(hum.value).toFixed(1) + ' %';
  }
  temp.addEventListener('input', sendEnv);
  hum.addEventListener('input', sendEnv);
  document.getElementById('btn-input').addEventListener('click', function () { post('/input'); });
  document.getElementById('btn-drop').addEventListener('click', function () { post('/drop'); });
})();
</script>
</body>
</html>
"""


def make_handler(board, tcp, args):
    page = (PAGE.replace("__NAME__", board.name.replace("<", "&lt;").replace(">", "&gt;"))
                .replace("__TCP__", str(args.tcp))
                .replace("__UDP__", str(args.udp))).encode("utf-8")

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
            if self.path == "/" or self.path.startswith("/?"):
                self._send(200, page, "text/html; charset=utf-8")
            elif self.path == "/state":
                self._json(board.state())
            else:
                self._json({"result": "fail", "ms": "not found"}, 404)

        def do_POST(self):
            # 화면이 보내는 본문은 수십 바이트다. 길이가 숫자가 아니거나 너무 크면 읽지 않는다
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
                except (ValueError, TypeError, AttributeError):
                    self._json({"result": "err", "ms": "need json {temperature, humidity}"}, 400)
                    return
                self._json({"result": "ok"})
            elif self.path == "/input":
                tcp.call_from_thread(tcp.send_input_event)
                self._json({"result": "ok"})
            elif self.path == "/drop":
                tcp.call_from_thread(tcp.drop_all)
                self._json({"result": "ok"})
            else:
                self._json({"result": "fail", "ms": "not found"}, 404)

    return Handler


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
    page_host = "127.0.0.1" if args.http_bind in ("0.0.0.0", "") else args.http_bind
    print("화면: http://%s:%d" % (page_host, args.http))
    if not args.name.startswith("ESP32_BLE"):
        print("주의: 이름이 ESP32_BLE 로 시작하지 않으면 12~15주차 예제의 [검색] 목록에 나오지 않는다.")
    print("Windows 방화벽 창이 뜨면 [액세스 허용]을 누른다. 안 뜨면 포트 %d·%d을 인바운드로 허용한다."
          % (args.tcp, args.udp))
    print("끝내려면 Ctrl+C")
    sys.stdout.flush()


# ---------------------------------------------------------------- 메인

class SimHTTPServer(ThreadingHTTPServer):
    # Windows 에서 주소 재사용을 켜면 다른 프로그램이 쓰는 포트에도 열려 버린다.
    # 그러면 "포트를 열 수 없다" 안내가 안 나온다. 그래서 Windows 에서는 끈다.
    allow_reuse_address = (os.name != "nt")
    allow_reuse_port = False
    daemon_threads = True

    def handle_error(self, request, client_address):
        # 브라우저가 응답을 다 받기 전에 끊으면(탭 닫기·새로 고침) 조용히 넘어간다
        if isinstance(sys.exc_info()[1], ConnectionError):
            return
        super().handle_error(request, client_address)


async def run(args, board, tcp, httpd):
    loop = asyncio.get_running_loop()
    tcp.loop = loop

    # 끊긴 연결에서 나온 OSError(재설정 등)를 asyncio 가 끝날 때 따로 알리지 않게 한다.
    # 그 밖의 오류는 그대로 보인다
    def on_loop_error(loop, context):
        if not isinstance(context.get("exception"), OSError):
            loop.default_exception_handler(context)
    loop.set_exception_handler(on_loop_error)

    if sys.version_info < (3, 11):
        # 3.9·3.10 의 asyncio.run 은 Ctrl+C 를 루프 안 아무 곳에서나 KeyboardInterrupt 로 던져서
        # 끝내기가 멈추거나 오류 줄이 남는다. 3.11 이후처럼 이 작업만 취소하게 한다
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


def main():
    p = argparse.ArgumentParser(description="BLEuno 시뮬레이터 (표준 라이브러리만)")
    p.add_argument("--name", default="ESP32_BLE_SIM1",
                   help="장치 이름 (기본 ESP32_BLE_SIM1). ESP32_BLE 로 시작해야 예제 목록에 나온다")
    p.add_argument("--tcp", type=int, default=8266, help="명령 포트 (기본 8266)")
    p.add_argument("--udp", type=int, default=8267, help="검색 포트 (기본 8267)")
    p.add_argument("--http", type=int, default=8080, help="화면 포트 (기본 8080)")
    p.add_argument("--bind", default="0.0.0.0", help="TCP·UDP 바인드 주소 (기본 0.0.0.0)")
    p.add_argument("--http-bind", default="127.0.0.1",
                   help="화면 바인드 주소 (기본 127.0.0.1: 이 PC에서만 열린다)")
    args = p.parse_args()

    # 터미널 인코딩이 무엇이든 로그 때문에 멈추지 않게 한다
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass

    board = Board(args.name)
    tcp = TcpSide(board)
    try:
        httpd = SimHTTPServer((args.http_bind, args.http), make_handler(board, tcp, args))
    except OSError as e:
        print("화면 %d 포트를 열 수 없다: %s (--http 로 다른 포트를 준다)" % (args.http, e))
        return 1

    print_banner(args)
    # 화면(HTTP)과 검색(UDP)은 따로 스레드에서 돈다. TCP 는 asyncio 가 맡는다
    threading.Thread(target=httpd.serve_forever, name="http", daemon=True).start()
    code = 0
    try:
        asyncio.run(run(args, board, tcp, httpd))
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    except OSError as e:
        print("포트를 열 수 없다: %s (--tcp/--udp 로 다른 포트를 준다)" % e)
        code = 1
    # 끝내는 동안(최대 0.5초) Ctrl+C 를 한 번 더 눌러도 트레이스백 없이 끝나게 한다
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    httpd.shutdown()
    httpd.server_close()
    print("종료")
    return code


if __name__ == "__main__":
    sys.exit(main())
