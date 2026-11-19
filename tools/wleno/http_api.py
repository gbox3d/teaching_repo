"""HTTP framing and bounded workers, independent of the TCP transport."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socket
import threading
import time


MAX_BODY = 64 * 1024
MAX_WORKERS = 32
READ_TIMEOUT = 2.0


class _HTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    block_on_close = False
    allow_reuse_address = False
    allow_reuse_port = False

    def __init__(self, address, owner):
        self.owner = owner
        self.closing = threading.Event()
        self.worker_lock = threading.Lock()
        self.workers = {}
        self.slots = threading.BoundedSemaphore(MAX_WORKERS)
        super().__init__(address, _Handler, bind_and_activate=False)

    def server_bind(self):
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        else:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

    def process_request(self, request, client_address):
        request.settimeout(READ_TIMEOUT)
        if not self.slots.acquire(blocking=False):
            reply = self.owner.protocol.http_error(503, "too many HTTP requests")
            header = (f"HTTP/1.1 {reply.status} Service Unavailable\r\n"
                      f"Content-Type: {reply.content_type}\r\n"
                      f"Content-Length: {len(reply.body)}\r\n"
                      "Connection: close\r\n\r\n").encode("ascii")
            try:
                request.settimeout(0.05)
                request.sendall(header + reply.body)
                request.shutdown(socket.SHUT_WR)
                # A close with unread request bytes can reset the connection on
                # Windows before the client sees 503. Briefly drain after FIN.
                deadline = time.monotonic() + 0.05
                remaining = MAX_BODY + 65536
                while remaining and time.monotonic() < deadline:
                    request.settimeout(max(0.001, deadline - time.monotonic()))
                    data = request.recv(min(4096, remaining))
                    if not data:
                        break
                    remaining -= len(data)
            except OSError:
                pass
            finally:
                self.shutdown_request(request)
            return
        worker = threading.Thread(target=self.process_request_thread,
                                  args=(request, client_address),
                                  name="wleno-http-request", daemon=True)
        with self.worker_lock:
            if self.closing.is_set():
                self.slots.release()
                self.shutdown_request(request)
                return
            self.workers[worker] = request
            try:
                worker.start()
            except Exception:
                self.workers.pop(worker)
                self.slots.release()
                self.shutdown_request(request)
                raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            with self.worker_lock:
                self.workers.pop(threading.current_thread(), None)
            self.slots.release()

    def handle_error(self, request, client_address):
        import sys
        error = sys.exc_info()[1]
        if not isinstance(error, (OSError, TimeoutError)):
            self.owner._record_error(error)

    def close_workers(self, deadline):
        with self.worker_lock:
            workers = tuple(self.workers.items())
        for _, conn in workers:
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            conn.close()
        for worker, _ in workers:
            if worker is not threading.current_thread():
                worker.join(max(0.0, deadline - time.monotonic()))


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        pass

    def _send(self, reply):
        self.close_connection = True
        self.send_response(reply.status)
        self.send_header("Content-Type", reply.content_type)
        self.send_header("Content-Length", str(len(reply.body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        for name, value in reply.headers:
            self.send_header(name, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(reply.body)

    def send_error(self, code, message=None, explain=None):
        self._send(self.server.owner.protocol.http_error(int(code), message or "bad request"))

    def _dispatch(self):
        if self.headers.get_all("Transfer-Encoding"):
            self.send_error(400, "Transfer-Encoding is not supported")
            return
        lengths = self.headers.get_all("Content-Length", [])
        value = lengths[0] if len(lengths) == 1 else "0"
        if len(lengths) > 1 or not value.isascii() or not value.isdecimal():
            self.send_error(400, "invalid Content-Length")
            return
        # Bound the digit count before int(), including malicious long headers.
        if len(value) > 10 or int(value) > MAX_BODY:
            self.send_error(413, "request body exceeds 64 KiB")
            return
        length = int(value)
        try:
            body = self.rfile.read(length) if length else b""
        except TimeoutError:
            self.send_error(408, "request body timeout")
            return
        if len(body) != length:
            self.send_error(400, "incomplete request body")
            return
        reply = self.server.owner.protocol.handle_http(self.command, self.path, body)
        self._send(reply)

    do_GET = do_POST = do_HEAD = do_PUT = do_PATCH = do_DELETE = do_OPTIONS = _dispatch


class HttpServer:
    def __init__(self, protocol, host, port, *, log=lambda message: None):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.log = log
        self._server = None
        self._thread = None
        self._lock = threading.Lock()
        self._running = False
        self._closed = False
        self._error = None

    def bind(self):
        if self._server is not None or self._closed:
            raise RuntimeError("HTTP server has already been bound or closed")
        server = _HTTPServer((self.host, self.port), self)
        try:
            server.server_bind()
            server.server_activate()
        except Exception as exc:
            server.server_close()
            self._record_error(exc)
            raise
        self._server = server
        self.port = server.server_address[1]

    def start(self):
        if self._server is None or self._closed:
            raise RuntimeError("HTTP server must be bound before start")
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run, name="wleno-http", daemon=True)
        with self._lock:
            self._running = True
        try:
            self._thread.start()
        except Exception:
            with self._lock:
                self._running = False
            self._thread = None
            raise

    def status(self):
        with self._lock:
            return {"running": self._running, "port": self.port, "error": self._error}

    def _record_error(self, error):
        with self._lock:
            self._error = f"{type(error).__name__}: {error}"
        try:
            self.log(f"HTTP: {self._error}")
        except Exception:
            pass

    def _run(self):
        try:
            self._server.serve_forever(poll_interval=0.05)
        except Exception as exc:
            self._record_error(exc)
        finally:
            self._server.closing.set()
            self._server.server_close()
            with self._lock:
                self._running = False

    def close(self):
        if self._closed:
            return
        self._closed = True
        server = self._server
        if server is None:
            return
        deadline = time.monotonic() + 2.5
        server.closing.set()
        # shutdown() waits forever if serve_forever() has never been called.
        if self._thread is not None and self._thread.is_alive():
            server.shutdown()
        server.server_close()
        server.close_workers(deadline)
        if self._thread is not None and self._thread is not threading.current_thread():
            self._thread.join(max(0.0, deadline - time.monotonic()))
