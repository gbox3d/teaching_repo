"""The public contract is testable without a socket, GUI or TCP worker."""

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from protocol import WlenoProtocol
from session import BoardSession


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.session = BoardSession()
        self.protocol = WlenoProtocol(self.session, name="WlEno_TEST")

    def http(self, method, path, data=None):
        body = b"" if data is None else json.dumps(data).encode()
        response = self.protocol.handle_http(method, path, body)
        return response.status, json.loads(response.body)

    def test_android_control_and_public_errors(self):
        self.assertEqual(json.loads(self.protocol.hello()),
                         {"event": "hello", "name": "WlEno_TEST", "app": "WlEno"})
        self.assertEqual(json.loads(self.protocol.handle_tcp(b"on -1\n"))["result"], "ok")
        self.assertEqual(self.session.snapshot().state.leds, (255,) * 4)
        self.protocol.handle_tcp(b"pwm 1 128\n")
        self.assertEqual(self.session.snapshot().state.leds, (255, 128, 255, 255))
        before = self.session.snapshot()
        for line in (b"on 0 4\n", b"pwm -2 50\n", b"pwm 0 256\n", b"on abc\n", b"\xff\n"):
            with self.subTest(line=line):
                self.assertEqual(json.loads(self.protocol.handle_tcp(line))["result"], "err")
                self.assertEqual(self.session.snapshot(), before)
        self.assertIsNone(self.protocol.handle_tcp(b"\r\n"))
        self.assertEqual(json.loads(self.protocol.handle_tcp(b"dht11\n"))["value"], "[24.5,40.0]")

    def test_http_model_actions_need_no_tcp(self):
        status, result = self.http("POST", "/input", {})
        self.assertEqual((status, result["value"], result["sequence"]), (200, 1, 1))
        self.assertEqual(self.http("GET", "/state")[1]["input_value"], 1)
        self.assertEqual(self.http("POST", "/leds", {"indices": [0, 2], "brightness": 99})[0], 200)
        self.assertEqual(self.http("POST", "/blink", {"enabled": True})[0], 200)
        self.assertEqual(self.http("POST", "/set", {"temperature": 123.456, "humidity": -12.345})[0], 200)
        state = self.http("GET", "/state")[1]
        self.assertEqual(state["leds"], [99, 0, 99, 0])
        self.assertTrue(state["blink"])
        self.assertEqual((state["temperature"], state["humidity"]), (123.456, -12.345))
        self.assertEqual(self.http("POST", "/drop"), (200, {"result": "ok", "requested": 0}))
        self.assertEqual(self.http("POST", "/reset")[0], 200)
        self.assertEqual(self.http("GET", "/state")[1]["input_sequence"], 2)

    def test_bad_http_messages_do_not_change_state(self):
        before = self.session.snapshot()
        cases = [("/set", b'{"temperature":12,"humidity":true}'),
                 ("/set", b'{"temperature":null}'), ("/set", b'{"humidity":NaN}'),
                 ("/set", b'[]'), ("/set", b'{"other":1}'),
                 ("/set", b'[' * 2000 + b'0' + b']' * 2000),
                 ("/leds", b'{"indices":[0,9],"brightness":20}'),
                 ("/blink", b'{"enabled":1}'), ("/input", b'{"unexpected":true}')]
        for path, body in cases:
            with self.subTest(path=path, body=body):
                self.assertEqual(self.protocol.handle_http("POST", path, body).status, 400)
                self.assertEqual(self.session.snapshot(), before)
        self.assertEqual(self.http("POST", "/state")[0], 405)
        self.assertEqual(self.protocol.handle_http("POST", "/state").headers, (("Allow", "GET"),))
        self.assertEqual(self.http("GET", "/missing")[0], 404)
        self.assertEqual(self.protocol.handle_http("POST", "/set", b" " * 65537).status, 413)
        self.session.close()
        self.assertEqual(self.http("POST", "/input")[0], 503)

    def test_discovery_describes_only_available_endpoints(self):
        self.assertIsNone(self.protocol.handle_udp(b"unrelated"))
        self.assertIsNone(json.loads(self.protocol.handle_udp(b"bleuno?"))["port"])
        protocol = WlenoProtocol(self.session, discovery=lambda: {"tcp": 12345, "http": 23456})
        self.assertEqual(json.loads(protocol.handle_udp(b" bleuno?\n")),
                         {"name": "WlEno_SIM1", "port": 12345})

    def test_event_encoding_and_drop_request_completion_are_explicit(self):
        cursor = self.protocol.event_cursor()
        self.session.press_input()
        latest, lines, missed = self.protocol.events_after(cursor)
        self.assertFalse(missed)
        self.assertEqual(latest, 1)
        self.assertEqual(json.loads(lines[0]), {"event": "input", "index": 0, "value": 1, "sequence": 1})
        protocol = WlenoProtocol(self.session, drop_connections=lambda: 2)
        reply = protocol.handle_http("POST", "/drop")
        self.assertEqual(reply.status, 202)
        self.assertEqual(json.loads(reply.body)["requested"], 2)


if __name__ == "__main__":
    unittest.main()
