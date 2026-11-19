"""Exercise actual loopback sockets against the production protocol and model."""

import http.client
import json
from pathlib import Path
import socket
import sys
import time
import unittest
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from http_api import HttpServer, MAX_WORKERS
from protocol import WlenoProtocol
from session import BoardSession
from tcp import TcpServer, MAX_LINE
from udp import UdpServer


HOST = "127.0.0.1"


def eventually(predicate, timeout=2.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("condition did not become true before timeout")


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.session = BoardSession()
        self.tcp = None
        self.http = None
        self.protocol = WlenoProtocol(
            self.session, "WlEno_TEST",
            runtime_state=lambda: {"clients": self.tcp.status()["clients"] if self.tcp else 0},
            drop_connections=lambda: self.tcp.drop_all() if self.tcp else 0,
            discovery=lambda: {"tcp": self.tcp.port if self.tcp else None,
                               "http": self.http.port if self.http else None},
        )

    def start(self, cls):
        server = cls(self.protocol, HOST, 0)
        self.addCleanup(server.close)
        server.bind()
        server.start()
        if cls is TcpServer:
            self.tcp = server
        elif cls is HttpServer:
            self.http = server
        return server

    def connect(self):
        conn = socket.create_connection((HOST, self.tcp.port), timeout=2)
        self.addCleanup(conn.close)
        stream = conn.makefile("rb")
        self.addCleanup(stream.close)
        self.assertEqual(json.loads(stream.readline()),
                         {"event": "hello", "name": "WlEno_TEST", "app": "WlEno"})
        return conn, stream

    def request(self, method, path, data=None):
        conn = http.client.HTTPConnection(HOST, self.http.port, timeout=3)
        try:
            body = json.dumps(data).encode() if data is not None else None
            conn.request(method, path, body=body,
                         headers={"Content-Type": "application/json"})
            response = conn.getresponse()
            return response.status, json.loads(response.read())
        finally:
            conn.close()

    def raw_http(self, raw, *, eof=False):
        with socket.create_connection((HOST, self.http.port), timeout=3) as conn:
            conn.sendall(raw)
            if eof:
                conn.shutdown(socket.SHUT_WR)
            response = http.client.HTTPResponse(conn)
            response.begin()
            body = response.read()
            self.assertIn("application/json", response.getheader("Content-Type"))
            self.assertEqual(int(response.getheader("Content-Length")), len(body))
            return response.status, json.loads(body)

    def test_tcp_fragmented_commands_utf8_and_reconnect_preserve_state(self):
        self.start(TcpServer)
        conn, stream = self.connect()
        conn.sendall(b"pw")
        conn.sendall(b"m 1 73\r\nabout\n\xff\n")
        self.assertEqual(json.loads(stream.readline())["result"], "ok")
        self.assertEqual(json.loads(stream.readline())["app"], "WlEno")
        self.assertEqual(json.loads(stream.readline())["result"], "err")
        self.assertEqual(self.session.snapshot().state.leds, (0, 73, 0, 0))
        stream.close()
        conn.close()
        eventually(lambda: self.tcp.status()["clients"] == 0)
        self.connect()
        self.assertEqual(self.session.snapshot().state.leds, (0, 73, 0, 0))
        self.assertIsNone(self.tcp.status()["error"])

    def test_tcp_line_limit_and_service_survives_bad_client(self):
        self.start(TcpServer)
        conn, stream = self.connect()
        conn.sendall(b"about" + b" " * (MAX_LINE - 6) + b"\n")
        self.assertEqual(json.loads(stream.readline())["app"], "WlEno")
        conn.sendall(b"x" * MAX_LINE)
        try:
            self.assertEqual(stream.read(1), b"")
        except ConnectionResetError:
            pass
        other, other_stream = self.connect()
        other.sendall(b"about\n")
        self.assertEqual(json.loads(other_stream.readline())["result"], "ok")
        self.assertTrue(self.tcp.status()["running"])

    def test_tcp_output_limit_closes_only_overloaded_client(self):
        self.start(TcpServer)
        conn, stream = self.connect()
        # A smaller bound makes queue saturation deterministic on every OS;
        # all bytes and command responses still come from the real protocol.
        with patch("tcp.MAX_OUTPUT", 128):
            conn.sendall(b"about\n" * 40)
            eventually(lambda: self.tcp.status()["clients"] == 0)
        self.assertTrue(self.tcp.status()["running"])
        other, other_stream = self.connect()
        other.sendall(b"about\n")
        self.assertEqual(json.loads(other_stream.readline())["result"], "ok")

    def test_tcp_connection_limit_preserves_existing_client(self):
        self.start(TcpServer)
        conn, stream = self.connect()
        with patch("tcp.MAX_CLIENTS", 1):
            with socket.create_connection((HOST, self.tcp.port), timeout=2) as extra:
                self.assertEqual(extra.recv(1), b"")
            conn.sendall(b"about\n")
            self.assertEqual(json.loads(stream.readline())["result"], "ok")
        self.assertEqual(self.tcp.status()["clients"], 1)

    def test_input_broadcast_has_per_client_cursor_and_no_old_replay(self):
        self.start(TcpServer)
        self.start(HttpServer)
        self.session.press_input()  # An event before connection is not replayed.
        _, first = self.connect()
        _, second = self.connect()
        code, result = self.request("POST", "/input", {})
        self.assertEqual((code, result["sequence"]), (200, 2))
        expected = {"event": "input", "index": 0, "value": 0, "sequence": 2}
        self.assertEqual(json.loads(first.readline()), expected)
        self.assertEqual(json.loads(second.readline()), expected)
        _, newest = self.connect()
        self.session.press_input()
        for stream in (first, second, newest):
            self.assertEqual(json.loads(stream.readline())["sequence"], 3)

    def test_lost_event_history_disconnects_without_rolling_back_state(self):
        self.session = BoardSession(history_limit=1)
        self.protocol.session = self.session
        self.start(TcpServer)
        self.connect()
        for _ in range(1000):
            self.session.press_input()
        eventually(lambda: self.tcp.status()["clients"] == 0)
        self.assertEqual(self.session.snapshot().input_sequence, 1000)
        self.assertTrue(self.tcp.status()["running"])

    def test_drop_is_queued_and_http_remains_available(self):
        self.start(TcpServer)
        self.start(HttpServer)
        _, first = self.connect()
        _, second = self.connect()
        self.session.set_leds((0, 3), 117)
        code, result = self.request("POST", "/drop", {})
        self.assertEqual((code, result["requested"]), (202, 2))
        self.assertEqual(first.readline(), b"")
        self.assertEqual(second.readline(), b"")
        self.assertEqual(self.request("GET", "/state")[1]["leds"], [117, 0, 0, 117])
        self.assertEqual(self.request("POST", "/drop", {}), (200, {"result": "ok", "requested": 0}))

    def test_http_and_udp_work_without_tcp(self):
        self.start(HttpServer)
        udp = self.start(UdpServer)
        self.assertEqual(self.request("POST", "/leds", {"indices": [0], "brightness": 91})[0], 200)
        self.assertEqual(self.request("POST", "/input", {})[1]["sequence"], 1)
        self.assertEqual(self.request("GET", "/state")[1]["leds"], [91, 0, 0, 0])
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            client.settimeout(2)
            client.sendto(b"invalid discovery", (HOST, udp.port))
            client.sendto(b"bleuno?", (HOST, udp.port))
            reply = json.loads(client.recvfrom(65535)[0])
        self.assertIsNone(reply["port"])
        self.assertEqual(reply["services"]["http"], self.http.port)
        self.assertTrue(udp.status()["running"])

    def test_udp_discovery_announces_actual_tcp_port(self):
        self.start(TcpServer)
        udp = self.start(UdpServer)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            client.settimeout(2)
            for payload in (b"bleuno?", b" bleuno?\n"):
                client.sendto(payload, (HOST, udp.port))
                self.assertEqual(json.loads(client.recvfrom(65535)[0]),
                                 {"name": "WlEno_TEST", "port": self.tcp.port})

    def test_http_body_and_header_errors_are_json_and_atomic(self):
        self.start(HttpServer)
        cases = [
            (b"Content-Length: -1\r\n", b"", 400),
            (b"Content-Length: nope\r\n", b"", 400),
            (b"Content-Length: 2\r\nContent-Length: 2\r\n", b"{}", 400),
            (b"Content-Length: 65537\r\n", b"", 413),
            (b"Transfer-Encoding: chunked\r\n", b"0\r\n\r\n", 400),
            (b"Content-Length: 8\r\n", b"{}", 400),
            (b"Content-Length: 1\r\n", b"\xff", 400),
        ]
        for headers, body, expected in cases:
            with self.subTest(headers=headers):
                raw = b"POST /set HTTP/1.1\r\nHost: localhost\r\n" + headers + b"\r\n" + body
                code, payload = self.raw_http(raw, eof=True)
                self.assertEqual(code, expected)
                self.assertEqual(payload["result"], "err")
        self.assertEqual(self.session.snapshot().revision, 0)
        self.assertEqual(self.request("GET", "/state")[0], 200)

    def test_http_wrong_method_includes_protocol_allow_header(self):
        self.start(HttpServer)
        for method, path, allowed in (("POST", "/state", "GET"),
                                      ("GET", "/input", "POST")):
            with self.subTest(method=method, path=path):
                conn = http.client.HTTPConnection(HOST, self.http.port, timeout=2)
                try:
                    conn.request(method, path)
                    response = conn.getresponse()
                    self.assertEqual(response.status, 405)
                    self.assertEqual(response.getheader("Allow"), allowed)
                    self.assertEqual(json.loads(response.read())["result"], "err")
                finally:
                    conn.close()
        self.assertEqual(self.session.snapshot().revision, 0)

    def test_http_incomplete_body_times_out(self):
        self.start(HttpServer)
        started = time.monotonic()
        code, body = self.raw_http(b"POST /set HTTP/1.1\r\nHost: local\r\nContent-Length: 9\r\n\r\n{}")
        self.assertEqual(code, 408)
        self.assertLess(time.monotonic() - started, 2.8)
        self.assertEqual(self.session.snapshot().revision, 0)

    def test_http_worker_limit_and_close_interrupts_pending_reads(self):
        self.start(HttpServer)
        connections = []
        for _ in range(MAX_WORKERS):
            conn = socket.create_connection((HOST, self.http.port), timeout=2)
            self.addCleanup(conn.close)
            connections.append(conn)
            conn.sendall(b"GET /state HTTP/1.1\r\n")
        eventually(lambda: len(self.http._server.workers) == MAX_WORKERS)
        code, _ = self.raw_http(b"GET /state HTTP/1.1\r\nHost: local\r\n\r\n")
        self.assertEqual(code, 503)
        with self.http._server.worker_lock:
            workers = tuple(self.http._server.workers)
        started = time.monotonic()
        self.http.close()
        self.http.close()
        self.assertLess(time.monotonic() - started, 2.8)
        self.assertFalse(self.http.status()["running"])
        self.assertTrue(all(not worker.is_alive() for worker in workers))

    def test_bind_conflicts_bound_only_close_and_ports_are_released(self):
        for cls in (TcpServer, UdpServer, HttpServer):
            with self.subTest(server=cls.__name__):
                first = cls(self.protocol, HOST, 0)
                self.addCleanup(first.close)
                first.bind()
                second = cls(self.protocol, HOST, first.port)
                self.addCleanup(second.close)
                with self.assertRaises(OSError):
                    second.bind()
                self.assertIsNotNone(second.status()["error"])
                started = time.monotonic()
                first.close()  # HTTP has been bound but has never served.
                first.close()
                self.assertLess(time.monotonic() - started, 0.5)
                replacement = cls(self.protocol, HOST, first.port)
                self.addCleanup(replacement.close)
                replacement.bind()
                replacement.start()
                replacement.close()
                replacement.close()
                self.assertFalse(replacement.status()["running"])
                third = cls(self.protocol, HOST, first.port)
                self.addCleanup(third.close)
                third.bind()

    def test_background_protocol_failure_is_visible_and_closes_tcp(self):
        self.start(TcpServer)
        conn, stream = self.connect()
        with patch.object(self.protocol, "handle_tcp", side_effect=RuntimeError("injected failure")):
            conn.sendall(b"about\n")
            eventually(lambda: not self.tcp.status()["running"])
        self.assertIn("injected failure", self.tcp.status()["error"])
        self.assertEqual(stream.readline(), b"")
        self.assertEqual(self.tcp.status()["clients"], 0)


if __name__ == "__main__":
    unittest.main()
