"""WlEno's public command, discovery and HTTP contract; no sockets or UI."""

from dataclasses import dataclass
import json
import re

if __package__:
    from .session import SessionClosed
    from .simulator import LED_COUNT
else:
    from session import SessionClosed
    from simulator import LED_COUNT


APP_NAME = "WlEno"
VERSION = "2.0.0"
MAX_BODY = 65536


@dataclass(frozen=True, slots=True)
class HttpReply:
    status: int
    body: bytes
    content_type: str = "application/json; charset=utf-8"
    headers: tuple[tuple[str, str], ...] = ()


def _json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


class WlenoProtocol:
    """A single owner of external formats and their mapping to Session operations."""

    HTTP_METHODS = {
        "/info": "GET", "/state": "GET", "/set": "POST", "/input": "POST",
        "/drop": "POST", "/leds": "POST", "/blink": "POST", "/reset": "POST",
    }

    def __init__(self, session, name="WlEno_SIM1", *, runtime_state=None,
                 drop_connections=None, discovery=None, log=None):
        self.session = session
        self.name = name
        self._runtime_state = runtime_state or (lambda: {})
        self._drop_connections = drop_connections or (lambda: 0)
        self._discovery = discovery or (lambda: {"tcp": None, "http": None})
        self._log = log or (lambda message: None)

    def hello(self):
        return _json({"event": "hello", "name": self.name, "app": APP_NAME}) + b"\n"

    def event_cursor(self):
        return self.session.snapshot().input_sequence

    def events_after(self, cursor):
        batch = self.session.events_after(cursor)
        lines = tuple(_json({"event": "input", "index": record.event.index,
                             "value": record.event.value, "sequence": record.sequence}) + b"\n"
                      for record in batch.events)
        return batch.cursor, lines, batch.missed

    @staticmethod
    def _integer(text):
        if not re.fullmatch(r"[+-]?[0-9]{1,10}", text):
            raise ValueError("expected a decimal integer")
        return int(text)

    @classmethod
    def _indices(cls, values):
        result = []
        for text in values:
            index = cls._integer(text)
            result.extend(range(LED_COUNT) if index == -1 else (index,))
        return result

    def handle_tcp(self, line):
        if line in (b"\n", b"\r\n", b""):
            return None
        try:
            text = line.decode("utf-8").strip()
            words = text.split()
            if not words:
                raise ValueError("need command")
            command, args = words[0], words[1:]
            if command in ("on", "off"):
                if not args:
                    raise ValueError("need pin index")
                self.session.set_leds(self._indices(args), 255 if command == "on" else 0)
                reply = {"result": "ok", "ms": "led(s) " + command}
            elif command == "pwm":
                if len(args) != 2:
                    raise ValueError("need pin index and pwm value")
                self.session.set_leds(self._indices(args[:1]), self._integer(args[1]))
                reply = {"result": "ok", "ms": "pwm set"}
            elif command in ("blink", "stopblk") and not args:
                self.session.set_blink(command == "blink")
                reply = {"result": "ok", "ms": "led blink" if command == "blink" else "led stop blink"}
            elif command == "dht11" and not args:
                state = self.session.snapshot().state
                reply = {"result": "ok", "value": "[%.1f,%.1f]" % (state.temperature, state.humidity)}
            elif command == "about" and not args:
                reply = {"result": "ok", "app": APP_NAME, "version": VERSION, "name": self.name}
            else:
                reply = {"result": "fail", "ms": "unknown command or unexpected arguments"}
        except (ValueError, UnicodeError) as error:
            reply = {"result": "err", "ms": str(error)}
        except SessionClosed as error:
            reply = {"result": "err", "ms": str(error)}
        encoded = _json(reply)
        # No output callback runs while the session holds its lock.
        self._log("TCP %s → %s" % (line[:160].decode("utf-8", "replace").strip(), encoded.decode("utf-8")))
        return encoded + b"\n"

    def handle_udp(self, data):
        if data.strip() != b"bleuno?":
            return None
        services = self._discovery()
        reply = {"name": self.name, "port": services.get("tcp")}
        if reply["port"] is None:
            reply["services"] = services
        return _json(reply)

    def state(self):
        snap = self.session.snapshot()
        state = snap.state
        runtime = self._runtime_state()
        return {"leds": list(state.leds), "blink": state.blink,
                "temperature": state.temperature, "humidity": state.humidity,
                "input_value": state.input_value, "revision": snap.revision,
                "input_sequence": snap.input_sequence,
                "clients": runtime.get("clients", 0), "log": runtime.get("log", []),
                "services": runtime.get("services", {})}

    def http_error(self, status, message):
        return HttpReply(status, _json({"result": "err", "ms": message}))

    @staticmethod
    def _body(raw, allowed, required=()):
        def reject_constant(value):
            raise ValueError("JSON numbers must be finite")

        data = json.loads(raw.decode("utf-8"), parse_constant=reject_constant) if raw else {}
        if not isinstance(data, dict):
            raise ValueError("expected a JSON object")
        if set(data) - set(allowed):
            raise ValueError("unexpected JSON field")
        if set(required) - set(data):
            raise ValueError("missing required JSON field")
        return data

    def handle_http(self, method, path, body=b""):
        expected = self.HTTP_METHODS.get(path)
        if expected is None:
            return self.http_error(404, "not found")
        if method != expected:
            return HttpReply(405, _json({"result": "err", "ms": "method not allowed"}),
                             headers=(("Allow", expected),))
        if len(body) > MAX_BODY:
            return self.http_error(413, "request body is too large")
        try:
            if path == "/state":
                payload = self.state()
            elif path == "/info":
                payload = {"app": APP_NAME, "version": VERSION, "name": self.name,
                           "endpoints": self.HTTP_METHODS, "services": self._discovery()}
            elif path == "/set":
                data = self._body(body, ("temperature", "humidity"))
                # Null is not a sensor measurement; omitted fields are unchanged.
                if any(value is None for value in data.values()):
                    raise ValueError("sensor values must be finite numbers")
                snap = self.session.set_environment(**data)
                payload = {"result": "ok", "revision": snap.revision}
            elif path == "/leds":
                data = self._body(body, ("indices", "brightness"), ("indices", "brightness"))
                if not isinstance(data["indices"], list):
                    raise ValueError("indices must be an array")
                snap = self.session.set_leds(data["indices"], data["brightness"])
                payload = {"result": "ok", "revision": snap.revision}
            elif path == "/blink":
                data = self._body(body, ("enabled",), ("enabled",))
                snap = self.session.set_blink(data["enabled"])
                payload = {"result": "ok", "revision": snap.revision}
            elif path == "/input":
                self._body(body, ())
                snap = self.session.press_input()
                payload = {"result": "ok", "value": snap.state.input_value,
                           "sequence": snap.input_sequence, "revision": snap.revision}
            elif path == "/reset":
                self._body(body, ())
                snap = self.session.reset()
                payload = {"result": "ok", "revision": snap.revision}
            else:  # /drop is an application operation, never a simulator transition.
                self._body(body, ())
                requested = self._drop_connections()
                return HttpReply(202 if requested else 200,
                                 _json({"result": "ok", "requested": requested}))
            if method == "POST":
                self._log("HTTP %s → %s" % (path, payload))
            return HttpReply(200, _json(payload))
        except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError) as error:
            return self.http_error(400, str(error))
        except SessionClosed as error:
            return self.http_error(503, str(error))
